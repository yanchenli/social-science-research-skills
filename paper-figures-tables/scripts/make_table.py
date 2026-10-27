"""把一张表的规格变成可投稿的 .docx（或 .tex）。

用法：
    python make_table.py spec.json out.docx [--tex]

三档格式（`format` 字段）：
    apa7    —— APA 第 7 版：表号加粗在上、表题斜体在下一行、仅三条横线、无竖线
    zh      —— 中文期刊：表题居中在表上方、三线表（顶/底 1.5 pt、表头下 0.75 pt）
    custom  —— 学校或目标期刊自己的要求，用 `style` 覆盖任意参数

规格示例见 references/format-specs.md。

为什么必须生成 .docx 而不是 markdown 表：markdown 没有字号、线宽、列宽，
打印出来不是投稿件。三线表的边框在 python-docx 里没有现成 API，
只能直接写 w:tblBorders / w:tcBorders。
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import profiles  # noqa: E402

# python-docx 只在生成 .docx 时才真正需要。用 --tex 的人往往装的是 TeX 而不是它，
# 所以导入失败不在这里报错，等真的要写 docx 时再给一句能照做的提示。
try:
    from docx import Document
    from docx.enum.section import WD_ORIENT
    from docx.enum.table import WD_CELL_VERTICAL_ALIGNMENT, WD_TABLE_ALIGNMENT
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.oxml import OxmlElement
    from docx.oxml.ns import qn
    from docx.shared import Pt
    HAS_DOCX = True
except ImportError:                      # pragma: no cover
    HAS_DOCX = False
    Document = WD_TABLE_ALIGNMENT = WD_ALIGN_PARAGRAPH = WD_ORIENT = None
    WD_CELL_VERTICAL_ALIGNMENT = None
    OxmlElement = qn = Pt = None

DOCX_HINT = ("生成 .docx 需要 python-docx：\n"
             "    pip install python-docx\n"
             "只想出 LaTeX 的话加 --tex，它不需要 python-docx。")

# 版式取值全部搬到了 assets/profiles/*.json（见 profiles.py）。
# 这里不再保留第二份默认值——两份默认值是「生成按 APA、检查按另一套」的起点。
ALIGN = {} if not HAS_DOCX else {"left": WD_ALIGN_PARAGRAPH.LEFT,
         "center": WD_ALIGN_PARAGRAPH.CENTER,
         "right": WD_ALIGN_PARAGRAPH.RIGHT}


from textmetrics import strip_tags, text_width, word_min_width  # noqa: E402


def auto_widths(cols, rows, style, total=None):
    """按内容分配列宽，而不是等分。

    等分会让长变量名列折行、窄数字列浪费空间——这是几何审计里最常被挑的一处。
    但「按内容比例缩放」也有个下限问题：内容总宽超过版心时，等比缩小会把
    每一列都压窄，压到装不下一个单词，Word 就从词中间断开。所以缩放之后
    必须再用「最长单词」兜底。
    """
    total = total or 432.0          # Letter + 1.25 in 边距 = 6.0 in 版心
    pad = 2 * style["cell_pad"]
    need, floor = [], []
    for j, c in enumerate(cols):
        label = c.get("label", c["key"])
        w = text_width(strip_tags(label), style["size"])
        f = word_min_width(label, style["size"])
        for r in rows:
            v = r.get(c["key"], "") if isinstance(r, dict) else r[j]
            for line in (v if isinstance(v, (list, tuple)) else [v]):
                w = max(w, text_width(strip_tags(line), style["size"]))
                f = max(f, word_min_width(line, style["size"]))
        need.append(w + pad + 3)
        floor.append(f + pad + 2)
    s = sum(need) or 1.0
    out = [max(w * total / s, fl) for w, fl in zip(need, floor)]
    if sum(out) > total + 0.5:
        # 下限之和就超过版心：照下限出，让 PFT-TBL-014 去报「超出页宽」。
        # 硬压成版心宽等于替作者决定「从词中间断开」，那是错的。
        return out
    spare = total - sum(out)
    if spare > 0.5:
        base = sum(out) or 1.0
        out = [x + spare * x / base for x in out]
    return out


# 只认「纯数字 + 可选的显著性星号」：`-0.53**`、`.82`、`12`、`0.85`
# 括号里的数（如 AVE 平方根 `(.85)`）、破折号、NA 一律不动。
# 允许千分位逗号：真实论文里 AIC/BIC 常写成 10,109.33
NUM_RE = re.compile(r"^(-?)([\d,]*)(?:\.(\d+))?(\**)$")


def parse_num(s):
    """返回 (int 部分, 小数部分, 星号) 或 None。"""
    m = NUM_RE.match(str(s).strip())
    if not m:
        return None
    sign, ip, dp, stars = m.groups()
    ip = (ip or "").replace(",", "")          # 千分位逗号只是写法，不参与数值
    if ip == "" and dp is None:
        return None
    return sign, ip, dp, stars


def fmt_num(parts, decimals: int, leading_zero: bool, thousands: bool = False) -> str:
    sign, ip, dp, stars = parts
    v = float((ip or "0") + ("." + dp if dp is not None else ""))
    if sign == "-":
        v = -v
    s = f"{v:.{decimals}f}"
    if not leading_zero and abs(v) < 1:
        s = s.replace("-0.", "-.", 1) if s.startswith("-0.") else s.replace("0.", ".", 1)
    if thousands and abs(v) >= 1000:
        # AIC/BIC 这类四位数按千分位写，读者才数得清位数
        neg = s.startswith("-")
        body = s[1:] if neg else s
        head, dot, tail = body.partition(".")
        s = ("-" if neg else "") + f"{int(head):,}" + (dot + tail if dot else "")
    return s + stars


def norm_align(a: str) -> str:
    """decimal 在 docx 里就是右对齐（小数位已统一，右对齐即小数点对齐）。"""
    return "right" if a == "decimal" else a


def column_decimals(col: dict, rows: list) -> int | None:
    """该列要统一到几位小数。

    **只在显式写了 `decimals` 时才格式化。** `align: "decimal"` 只负责右对齐，
    不猜小数位——把 `.5` 自动补成 `.500` 等于替作者声明了并不存在的精度。
    小数位不一致时由 check_figure.py 报警，让作者自己决定补到几位。
    """
    return col["decimals"] if isinstance(col.get("decimals"), int) else None


def format_rows(spec: dict, style: dict) -> list:
    """把每列的数字按该列的小数位统一，返回新的行列表。非数字原样保留。"""
    cols = spec["columns"]
    rows = [dict(r) if isinstance(r, dict) else r for r in spec["rows"]]
    for c in cols:
        dec = column_decimals(c, rows)
        if dec is None:
            continue
        lz = c.get("leading_zero", style["leading_zero"])
        for r in rows:
            if not isinstance(r, dict):
                continue
            v = r.get(c["key"], "")
            if isinstance(v, (list, tuple)):
                # 一格多行：逐行套同一套小数位规则
                r[c["key"]] = [
                    x if "<" in str(x) or parse_num(x) is None
                    else fmt_num(parse_num(x), dec, lz, bool(c.get("thousands")))
                    for x in v]
                continue
            if "<" in str(v):
                # 带行内标记的单元格不参与数字格式化——把 <i> 包着的数补零会改坏标签
                continue
            p = parse_num(v)
            if p is None:
                continue
            r[c["key"]] = fmt_num(p, dec, lz, bool(c.get("thousands")))
    return rows


def resolve_profile(spec: dict) -> dict:
    """按 spec 取 profile：`profile` 优先，其次 `format`（apa7 / zh / custom）。

    `custom` 的含义是「以 APA 为底，用 style 覆盖」，与旧行为一致。
    """
    ref = spec.get("profile") or spec.get("format") or "apa7"
    if ref == "custom":
        ref = "apa7"
    prof = profiles.load(ref, spec.get("style"))
    # 只改 size 不改 note_size 时，表注会比表体还大——表注是附注，不该压过数据。
    style = spec.get("style") or {}
    if "size" in style and "note_size" not in style:
        prof["table"]["note_size"] = min(prof["table"]["note_size"], style["size"])
    return prof


# ---------- docx 底层 ----------
def _border(tag: str, sz: int | None):
    el = OxmlElement(tag)
    if sz:
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(int(sz)))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "000000")
    else:
        el.set(qn("w:val"), "nil")
    return el


def set_table_borders(table, style: dict):
    """只留三条横线。insideH / insideV / left / right 全部 nil。"""
    tblPr = table._tbl.tblPr
    for old in tblPr.findall(qn("w:tblBorders")):
        tblPr.remove(old)
    borders = OxmlElement("w:tblBorders")
    for tag, sz in (("w:top", style["rule_top"]),
                    ("w:left", None),
                    ("w:bottom", style["rule_bottom"]),
                    ("w:right", None),
                    ("w:insideH", None),
                    ("w:insideV", None)):
        borders.append(_border(tag, sz))
    tblPr.append(borders)


def set_cell_border(cell, edge: str, sz: int | None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn("w:tcBorders"))
    if tcBorders is None:
        tcBorders = OxmlElement("w:tcBorders")
        tcPr.append(tcBorders)
    for old in tcBorders.findall(qn(f"w:{edge}")):
        tcBorders.remove(old)
    tcBorders.append(_border(f"w:{edge}", sz))


def set_cell_pad(table, pad_pt: float):
    tblPr = table._tbl.tblPr
    mar = OxmlElement("w:tblCellMar")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:w"), str(int(pad_pt * 20)))   # twips
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tblPr.append(mar)


def fixed_layout(table):
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)


def repeat_header(table, n_rows: int) -> None:
    """跨页时重复表头。

    长表（20 行以上）几乎一定会跨页，而 Word 默认不重复表头——第二页起
    只剩数字没有列名，读者只能翻回上一页去对。这是投稿件里最常见的
    「看起来没问题、印出来不能用」的一处。
    """
    for r in table.rows[:n_rows]:
        trPr = r._tr.get_or_add_trPr()
        el = OxmlElement("w:tblHeader")
        el.set(qn("w:val"), "true")
        trPr.append(el)


def keep_rows_together(table, start: int) -> None:
    """禁止一行被分页切成两半。

    断成两半的行会被读成两行数据，比页末留白更糟。
    """
    for r in table.rows[start:]:
        trPr = r._tr.get_or_add_trPr()
        el = OxmlElement("w:cantSplit")
        el.set(qn("w:val"), "true")
        trPr.append(el)


# 单元格里的行内标记。APA 要求统计符号斜体（*B*、*SE*、*p*）、希腊字母不斜体，
# 表注里的上标注释字母（a、b、c）也要真的排成上标——纯文本做不到这两件事。
TAG_RE = re.compile(r"</?(i|b|sup|sub)>")
# strip_tags 从 textmetrics 导入——生成与检查必须用同一份宽度判据，
# 各留一份实现迟早会出现「生成的说没问题、检查的说有问题」。


def _run(p, text: str, style: dict, size: float, italic: bool, bold: bool,
         sup: bool, sub: bool, font: str | None = None):
    run = p.add_run(text)
    run.font.name = font or style["font"]
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    if sup:
        run.font.superscript = True
    if sub:
        run.font.subscript = True
    # 中文字体要单独设 eastAsia，否则 Word 会用西文字体渲染中文
    rpr = run._element.get_or_add_rPr()
    rfonts = rpr.find(qn("w:rFonts"))
    if rfonts is None:
        rfonts = OxmlElement("w:rFonts")
        rpr.append(rfonts)
    rfonts.set(qn("w:eastAsia"), font or style["font"])


def add_runs(p, text, style: dict, *, size=None, italic=False, bold=False,
             font: str | None = None):
    """把带 <i>/<b>/<sup>/<sub> 的字符串写成一串 run。

    标签必须成对；未闭合的标签会一直生效到结尾（不报错，但也不会吞字）。
    """
    s = str(text)
    size = size or style["size"]
    st = {"i": False, "b": False, "sup": False, "sub": False}
    pos = 0
    for m in TAG_RE.finditer(s):
        seg = s[pos:m.start()]
        if seg:
            _run(p, seg, style, size, italic or st["i"], bold or st["b"],
                 st["sup"], st["sub"], font)
        closing, tag = m.group(0).startswith("</"), m.group(1)
        st[tag] = not closing
        pos = m.end()
    tail = s[pos:]
    if tail:
        _run(p, tail, style, size, italic or st["i"], bold or st["b"],
             st["sup"], st["sub"], font)


def tighten_cell(cell, style: dict, align="center"):
    """把单元格的段落格式调紧，但不写任何文字。

    合并前必须先把参与合并的每个格子调一遍：没写过的格子带着 Word 默认的
    段后间距（8 pt），而跨列标题那一行的行高由最高的格子决定——于是
    「信度与收敛效度」这一行比数据行高出十来个点，表看起来是散的。
    """
    p = cell.paragraphs[0]
    for old_run in list(p.runs):
        old_run._element.getparent().remove(old_run._element)
    p.alignment = ALIGN[align]
    pf = p.paragraph_format
    pf.space_before = Pt(1)
    pf.space_after = Pt(1)
    pf.line_spacing = 1.0


def write_cell(cell, text, style: dict, *, bold=False, italic=False,
               align="center", size=None):
    """写一个单元格。`text` 是列表时写成一格多行（每元素一段）。

    一格多行是宽表常见的写法：一个格子里装 4 个研究各自的系数。行与行之间
    用段而不是换行符——Word 的软换行（Shift+Enter）不会让两个值各自对齐，
    复制出去也粘成一整段。
    """
    lines = list(text) if isinstance(text, (list, tuple)) else [text]
    # 全空的多行格（三角矩阵的下半部）不必写成 4 个空段——一段就够，行高由邻格决定
    if not lines or all(str(x).strip() == "" for x in lines):
        lines = [""]
    # 复用单元格时先清掉多余段落，否则旧内容会留在下面
    for extra in cell.paragraphs[1:]:
        extra._element.getparent().remove(extra._element)
    # 不能用 cell.text = ""——那会留下一个空 run，每个单元格都多一段空文本
    p0 = cell.paragraphs[0]
    for old_run in list(p0.runs):
        old_run._element.getparent().remove(old_run._element)
    # 多行的格子里，其他格只有一行；不居中的话数字会贴在格顶，与堆叠行错位
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    for i, line in enumerate(lines):
        p = p0 if i == 0 else cell.add_paragraph()
        p.alignment = ALIGN[align]
        pf = p.paragraph_format
        pf.space_before = Pt(1)
        pf.space_after = Pt(1)
        pf.line_spacing = 1.0
        add_runs(p, line, style, size=size, italic=italic, bold=bold)


def add_note(doc, spec: dict, style: dict):
    notes = spec.get("notes") or {}
    if not notes:
        return
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.line_spacing = 1.0
    sz = style["note_size"]
    sep = " " if style["note_prefix"].endswith(".") else ""
    # 表注同样支持行内标记：APA 的 "Note." 本身就是斜体，N、p 也该斜体
    add_runs(p, style["note_prefix"] + sep, style, size=sz,
             italic=style["note_italic_prefix"])
    if notes.get("general"):
        add_runs(p, str(notes["general"]) + " ", style, size=sz)
    for i, s in enumerate(notes.get("specific") or []):
        _run(p, chr(ord("a") + i), style, sz, False, False, True, False)
        add_runs(p, str(s) + " ", style, size=sz)
    if notes.get("probability"):
        add_runs(p, str(notes["probability"]), style, size=sz)


def build_docx(spec: dict, out: Path) -> None:
    if not HAS_DOCX:
        raise SystemExit(DOCX_HINT)
    prof = resolve_profile(spec)
    fmt = spec.get("format") or prof["profile_id"]
    style = prof["table"]
    if spec.get("panels"):
        # 多面板表：没有顶层 columns，走单独路径
        return build_panel_docx(spec, out)
    cols = spec["columns"]
    rows = format_rows(spec, style)
    doc = Document()
    landscape = bool(spec.get("landscape"))
    avail = apply_page(doc, prof, landscape)

    # ---- 表号与表题
    write_title(doc, spec, style)

    # ---- 表体
    n_head = 2 if spec.get("spanners") else 1
    table = doc.add_table(rows=n_head + len(rows), cols=len(cols))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    fixed_layout(table)
    set_table_borders(table, style)
    set_cell_pad(table, style["cell_pad"])

    # 不指定 table_width 时用整幅版心——横向页是 9 in，纵向是 6.5 in。
    widths = spec.get("widths") or auto_widths(
        cols, rows, style, spec.get("table_width") or avail)
    for j, w in enumerate(widths):
        table.columns[j].width = Pt(w)

    def put(row_idx, col_idx, text, **kw):
        cell = table.cell(row_idx, col_idx)
        write_cell(cell, text, style, **kw)
        cell.width = Pt(widths[col_idx])

    hr = n_head - 1
    for j, c in enumerate(cols):
        align = style["first_col_align"] if j == 0 else norm_align(
            c.get("align", style["header_align"]))
        put(hr, j, c.get("label", c["key"]), bold=style["header_bold"], align=align)

    if spec.get("spanners"):
        # 整行先按列宽设一遍：add_table 给每个单元格的默认宽度是「总宽÷列数」，
        # 与 auto_widths 算出来的列宽并不一致。不先设，未参与合并的单元格会带着
        # 默认宽度进文件。
        # 这一遍只能在合并**之前**做一次：合并后 table.cell(0, j) 会把 j 映射到
        # 已合并的单元格上，第二个跨列标题的循环会把它改回单列宽。
        for j in range(len(cols)):
            table.cell(0, j).width = Pt(widths[j])
            tighten_cell(table.cell(0, j), style)
        for sp in spec["spanners"]:
            idx = [next(j for j, c in enumerate(cols) if c["key"] == k) for k in sp["span"]]
            lo, hi = min(idx), max(idx)
            cell = table.cell(0, lo).merge(table.cell(0, hi))
            # 合并后必须重设宽度：python-docx 只加 gridSpan，tcW 仍是合并前各格之和。
            # 固定列宽的表里 Word 按 tcW 排版，于是「95% CI」只占一列宽、挤在 LL 上方。
            cell.width = Pt(sum(widths[lo:hi + 1]))
            write_cell(cell, sp["label"], style, align="center")

    for i, row in enumerate(rows):
        for j, c in enumerate(cols):
            val = row.get(c["key"], "") if isinstance(row, dict) else row[j]
            align = style["first_col_align"] if j == 0 else norm_align(
                c.get("align", "right"))
            put(n_head + i, j, val, align=align)

    # 表头下那条线（APA 三条横线之一）
    for j in range(len(cols)):
        set_cell_border(table.cell(hr, j), "bottom", style["rule_header"])

    if spec.get("repeat_header", True):
        repeat_header(table, n_head)
        keep_rows_together(table, n_head)

    add_note(doc, spec, style)
    # 把档位与「明确要求保留前导零的列」写进文档属性：
    # check_figure.py 靠它判断前导零该不该省略。没有这一条，审核器只能对每一列
    # 都报「0.xx 应该省略前导零」——而 B / SE / M / SD 恰恰**必须**保留。
    lz_cols = [strip_tags(c.get("label", c["key"])) for c in cols
               if c.get("leading_zero") is True]
    meta = f"pft-format:{fmt};pft-profile:{prof['profile_id']}"
    if lz_cols:
        meta += ";pft-lz:" + ",".join(lz_cols)
    set_core_properties(doc, meta)
    doc.save(str(out))


def to_tex(s) -> str:
    """把行内标记转成 LaTeX，并转义 & % _ 这几个在 tabular 里会出事字符。"""
    s = str(s)
    s = re.sub(r"<i>(.*?)</i>", lambda m: r"\textit{" + m.group(1) + "}", s)
    s = re.sub(r"<b>(.*?)</b>", lambda m: r"\textbf{" + m.group(1) + "}", s)
    s = re.sub(r"<sup>(.*?)</sup>", lambda m: r"\textsuperscript{" + m.group(1) + "}", s)
    s = re.sub(r"<sub>(.*?)</sub>", lambda m: r"\textsubscript{" + m.group(1) + "}", s)
    return (s.replace("&", r"\&").replace("%", r"\%").replace("_", r"\_"))


def build_tex(spec: dict, out: Path) -> None:
    out = Path(out)
    style = resolve_profile(spec)["table"]
    cols = spec["columns"]
    spec = dict(spec, rows=format_rows(spec, style))
    align = "".join("l" if j == 0 else "r" for j in range(len(cols)))
    head = " & ".join(to_tex(c.get("label", c["key"])) for c in cols) + r" \\"
    body = []
    for row in spec["rows"]:
        cells = [to_tex(row.get(c["key"], "")) if isinstance(row, dict) else to_tex(row[j])
                 for j, c in enumerate(cols)]
        body.append(" & ".join(cells) + r" \\")

    if spec.get("longtable"):
        # 长表必须用 longtable：tabular 不能跨页，超过一页的部分会被裁掉。
        # \endhead 之后的表头就是续页的表头。
        lines = [rf"\begin{{longtable}}{{{align}}}",
                 rf"\caption{{{spec.get('title', '')}}}\\",
                 r"\toprule", head, r"\midrule", r"\endfirsthead",
                 rf"\multicolumn{{{len(cols)}}}{{l}}{{\footnotesize (continued)}}\\",
                 r"\toprule", head, r"\midrule", r"\endhead",
                 r"\bottomrule", r"\endlastfoot"]
        lines += body
        lines.append(r"\end{longtable}")
    else:
        lines = [r"\begin{table}[htbp]", r"\centering",
                 rf"\caption{{{spec.get('title', '')}}}",
                 rf"\begin{{tabular}}{{{align}}}", r"\toprule",
                 head, r"\midrule"]
        lines += body
        lines += [r"\bottomrule", r"\end{tabular}"]

    notes = spec.get("notes") or {}
    if notes:
        parts = [to_tex(notes.get("general", "")).strip()]
        for i, s in enumerate(notes.get("specific") or []):
            parts.append(rf"\textsuperscript{{{chr(ord('a') + i)}}}{to_tex(s)}")
        parts.append(to_tex(notes.get("probability", "")).strip())
        txt = " ".join(p for p in parts if p)
        lines.append(rf"\begin{{tablenotes}}\footnotesize\item \textit{{Note.}} {txt}"
                     rf"\end{{tablenotes}}")
    if not spec.get("longtable"):
        lines.append(r"\end{table}")
    if spec.get("landscape"):
        lines.insert(0, "% 本表按横向页面排版：LaTeX 侧请用 rotating 宏包的 sidewaystable")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) < 2:
        print(__doc__)
        return 2
    from qc import load_spec
    spec = load_spec(args[0])
    if "panels" not in spec and "columns" not in spec:
        raise SystemExit(f"{Path(args[0]).name} 里既没有 columns 也没有 panels：\n"
                         "  普通表要写 \"columns\" 与 \"rows\"；多面板表写 \"panels\"。\n"
                         "  例子里有现成的结构可抄：assets/table_specs/")
    out = Path(args[1])
    if out.suffix.lower() == ".tex":
        build_tex(spec, out)
    else:
        build_docx(spec, out)
    print(f"已生成 {out}")
    if "--tex" in sys.argv and out.suffix.lower() != ".tex":
        tex = out.with_suffix(".tex")
        build_tex(spec, tex)
        print(f"已生成 {tex}")
    return 0



# ---------------------------------------------------------------------------
# 多面板表
# ---------------------------------------------------------------------------
def apply_page(doc, prof: dict, landscape: bool) -> float:
    """按 profile 设置页面，返回版心宽（pt）。

    横向页不是「把 orientation 一设就好」：python-docx 只改 orientation 标记，
    页宽页高还是纵向的值，Word 打开后仍按纵向排。必须显式对调。
    """
    from docx.shared import Inches
    sec = doc.sections[0]
    w_pt, h_pt = profiles.page_pt(prof, landscape)
    sec.orientation = WD_ORIENT.LANDSCAPE if landscape else WD_ORIENT.PORTRAIT
    sec.page_width = Pt(w_pt)
    sec.page_height = Pt(h_pt)
    top, right, bottom, left = prof["page"].get("margins_in", [1, 1, 1, 1])
    sec.top_margin = Inches(top)
    sec.bottom_margin = Inches(bottom)
    sec.left_margin = Inches(left)
    sec.right_margin = Inches(right)
    return profiles.text_width_pt(prof, landscape)


def set_core_properties(doc, comments: str) -> None:
    """写文档属性：清掉模板自带的作者与 2013 年的假日期。

    python-docx 的默认模板把 `author` 写成 "python-docx"、`created` 写成 2013-12-23。
    学生把这张表交上去，Word 的「属性」里就写着 python-docx 与 2013 年——
    既暴露了工具，也明显不对。作者留空，交给用户在 Word 里自然填写。
    `comments` 要留着：检查器靠它读「生成时用的是哪个档位、哪些列保留前导零」。
    """
    from datetime import datetime
    cp = doc.core_properties
    cp.author = ""
    cp.last_modified_by = ""
    now = datetime.now().replace(microsecond=0)
    cp.created = now
    cp.modified = now
    cp.comments = comments


def write_title(doc, spec: dict, style: dict) -> None:
    """表号与表题。生成路径与多面板路径共用，避免只改一边。"""
    if style["title_on_separate_line"]:
        p1 = doc.add_paragraph()
        p1.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p1.paragraph_format.space_after = Pt(0)
        r = p1.add_run(f"Table {spec.get('number', '1')}")
        r.bold = style["number_bold"]
        r.font.name = style["title_font"]
        r.font.size = Pt(style["size"] + 0.5)

        p2 = doc.add_paragraph()
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(6)
        r2 = p2.add_run(str(spec.get("title", "")))
        r2.italic = style["title_italic"]
        r2.font.name = style["title_font"]
        r2.font.size = Pt(style["size"] + 0.5)
    else:
        p = doc.add_paragraph()
        p.alignment = ALIGN[style["title_align"]]
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(f"表 {spec.get('number', '1')} " + str(spec.get("title", "")))
        r.bold = style["number_bold"]
        r.font.name = style["title_font"]
        r.font.size = Pt(style["size"] + 0.5)


def check_panels(spec: dict) -> tuple[list, int]:
    """校验面板结构，返回 (panels, K)。

    关键约束：各面板的数据列**跨度之和**必须相等。6 列的面板每列 span=2、
    4 列的面板每列 span=3，合计都是 12——这样一个网格就能同时容纳两者。
    凑不出相等的跨度，说明它们本来就不该放进一张表。
    """
    panels = spec.get("panels") or []
    if not panels:
        raise SystemExit("panels 为空")
    K = None
    for i, p in enumerate(panels, 1):
        cols = p.get("columns") or []
        if not cols:
            raise SystemExit(f"第 {i} 块面板没有 columns")
        total = sum(int(c.get("span", 1)) for c in cols)
        if K is None:
            K = total
        elif total != K:
            raise SystemExit(
                f"第 {i} 块面板的列跨度合计 {total}，与第一块的 {K} 不一致。\n"
                "多面板表要求各面板的数据列跨度之和相等——例如 6 列的面板每列 span=2、"
                "4 列的面板每列 span=3，合计都是 12。\n"
                "凑不出相等的跨度，就说明这些面板本来不该放进一张表，请拆成两张。")
        for r in p.get("rows") or []:
            vals = r.get("values") or []
            if len(vals) != len(cols):
                raise SystemExit(
                    f"第 {i} 块面板有一行给了 {len(vals)} 个值，但该面板有 {len(cols)} 列")
    return panels, K


def _panel_widths(panels, K: int, spec: dict, style: dict,
                  avail: float = 468.0) -> tuple[list[float], list[str]]:
    """给多面板表算列宽：先满足每个单元格的最长单词，再分配余量。

    多面板表最容易错的地方是「按网格列数均分」——6 列的面板每列跨 2 格、
    4 列的面板每列跨 3 格，均分之后前者的格子只有后者的 2/3 宽，装不下
    "Relational" 这种词，Word 就从词中间断开。所以下限必须按**单元格**算，
    再折算回它跨过的每个网格列。
    """
    pad = 2 * style["cell_pad"] + 2
    size = style["size"]
    need = [12.0] * K

    def bump(ci: int, span: int, text: str) -> None:
        per = (word_min_width(text, size) + pad) / span
        for g in range(ci, ci + span):
            need[g] = max(need[g], per)

    for p in panels:
        ci = 0
        for c in p["columns"]:
            span = int(c.get("span", 1))
            bump(ci, span, str(c.get("label", "")))
            ci += span
        for r in p.get("rows") or []:
            ci = 0
            for c, v in zip(p["columns"], r.get("values") or []):
                span = int(c.get("span", 1))
                bump(ci, span, str(v))
                ci += span

    stub_texts = [str(p.get("stub", "")) for p in panels]
    stub_texts += [str(r.get("label", "")) for p in panels for r in (p.get("rows") or [])]
    stub_one_line = max([text_width(t, size) for t in stub_texts] + [60.0]) + pad
    stub_word = max([word_min_width(t, size) for t in stub_texts] + [40.0]) + pad

    table_w = float(spec.get("table_width") or avail)
    data_min = sum(need)
    notes: list[str] = []

    # 标签列优先保证一行放下；放不下就让它折行，把宽度让给数据列。
    stub_w = max(stub_word, min(stub_one_line, table_w - data_min))
    if stub_w < stub_one_line:
        notes.append(f"标签列从 {stub_one_line:.0f} pt 收到 {stub_w:.0f} pt，"
                     f"最长的行标签会折行（数据列需要 {data_min:.0f} pt 才不断词）")

    total_min = stub_w + data_min
    if total_min > table_w + 0.5:
        notes.append(f"列宽下限合计 {total_min:.0f} pt，超过设定的 {table_w:.0f} pt；"
                     f"已按 {total_min:.0f} pt 出表——要么调宽 table_width，"
                     f"要么把字号调小，要么缩短列名。硬压会从词中间断开")
        return [stub_w] + need, notes

    # 余量按现有比例分配，避免窄列被拉得过宽
    spare = table_w - total_min
    scaled = [w + spare * w / data_min for w in need]
    return [stub_w] + scaled, notes


def build_panel_docx(spec: dict, out: Path) -> None:
    """多面板表：一套网格，每个面板自带标签行与表头行。"""
    prof = resolve_profile(spec)
    fmt = spec.get("format") or prof["profile_id"]
    style = prof["table"]
    panels, K = check_panels(spec)
    doc = Document()
    landscape = bool(spec.get("landscape"))
    avail = apply_page(doc, prof, landscape)
    write_title(doc, spec, style)

    grid = 1 + K
    total_rows = sum(2 + len(p.get("rows") or []) for p in panels)
    table = doc.add_table(rows=total_rows, cols=grid)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    fixed_layout(table)
    set_table_borders(table, style)
    set_cell_pad(table, style["cell_pad"])

    widths, width_notes = _panel_widths(panels, K, spec, style, avail)
    for note in width_notes:
        print(f"  ! {note}")
    for j, w in enumerate(widths):
        table.columns[j].width = Pt(w)

    def put(ri, ci, text, span=1, **kw):
        cell = table.cell(ri, ci)
        if span > 1:
            cell = cell.merge(table.cell(ri, ci + span - 1))
        write_cell(cell, text, style, **kw)
        cell.width = Pt(sum(widths[ci:ci + span]))
        return cell

    ri = 0
    for pi, p in enumerate(panels):
        # 面板标签行：整行合并
        put(ri, 0, str(p.get("label", "")), span=grid, align="left",
            bold=style["header_bold"])
        ri += 1
        # 表头行
        put(ri, 0, str(p.get("stub", "")), align=style["first_col_align"],
            bold=style["header_bold"])
        ci = 1
        for c in p["columns"]:
            span = int(c.get("span", 1))
            put(ri, ci, c.get("label", ""), span=span, align="center",
                bold=style["header_bold"])
            ci += span
        for j in range(grid):
            set_cell_border(table.cell(ri, j), "bottom", style["rule_header"])
        ri += 1
        # 数据行
        for r in p.get("rows") or []:
            put(ri, 0, str(r.get("label", "")), align=style["first_col_align"])
            ci = 1
            for c, v in zip(p["columns"], r.get("values") or []):
                span = int(c.get("span", 1))
                put(ri, ci, v, span=span, align=norm_align(c.get("align", "right")))
                ci += span
            ri += 1
        # 面板之间加一条细线（最后一块不加，避免与表底线重复）
        if pi < len(panels) - 1:
            for j in range(grid):
                set_cell_border(table.cell(ri - 1, j), "bottom", style["rule_header"])

    add_note(doc, spec, style)
    set_core_properties(doc, f"pft-format:{fmt};pft-profile:{prof['profile_id']};pft-panels:1")
    doc.save(str(out))


if __name__ == "__main__":
    sys.exit(main())
