"""表格层的共用检查。生成后的自检（check_figure）与审别人的表（audit_table）都调这里。

为什么抽出来
------------
同一批判据（三条横线、表头下线、前导零、小数位）如果生成路径与审核路径各写一份，
改了一边忘了另一边，症状是「自己生成的说没问题，审别人的说有问题」——
而两边用的其实是同一份 profile。判据只能有一份。

本模块只处理「一个 python-docx 的 Table 对象 + 一个 profile」，不读文件、不打印。
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from qc import E, W, Finding  # noqa: E402

# APA：统计符号斜体，希腊字母不斜体。这一条三个实现都标成「需人工」，
# 其实表头里能机器判——只要按 run 精确比对，不去猜语义。
ITALIC_SYMBOLS = {"M", "SD", "N", "n", "r", "t", "F", "p", "B", "SE",
                  "R2", "R²", "d", "f", "χ2", "η2"}
UPRIGHT_SYMBOLS = {"α", "β", "χ²", "η²", "ω", "λ", "γ", "Δ", "χ2", "η2", "βs"}

CAP_EN = re.compile(r"^\s*Table\s+([0-9]+[A-Za-z]?)\s*[.:]?\s*(.*)$", re.I)
CAP_ZH = re.compile(r"^\s*表\s*([0-9]+(?:[-.][0-9]+)?)\s*[.:：]?\s*(.*)$")

# 允许千分位逗号：真实论文里 AIC/BIC 常写成 10,109.33
NUM_RE = re.compile(r"^(-?)([\d,]*)(?:\.(\d+))?(\**)$")


def _qn():
    from docx.oxml.ns import qn
    return qn


def header_end(t) -> int:
    """表头到第几行为止（1 = 普通表头，2 = 有分组表头）。

    判据：前两行里第一条带下边线的行。找不到就按 1 处理。
    """
    qn = _qn()
    for ri, row in enumerate(t.rows[:2]):
        for c in row.cells:
            tcPr = c._tc.tcPr
            tb = tcPr.find(qn("w:tcBorders")) if tcPr is not None else None
            if tb is not None and tb.find(qn("w:bottom")) is not None:
                return ri + 1
    return 1


def border_findings(t) -> list[Finding]:
    """三线表：无竖线、有顶底线。"""
    qn = _qn()
    out: list[Finding] = []
    b = t._tbl.tblPr.find(qn("w:tblBorders"))
    if b is None:
        return [Finding("PFT-TBL-001", E,
                        "表格没有显式设置边框——Word 会用默认全框线",
                        limit="只查表格级边框；单元格级补画的线查不到")]
    vals = {el.tag.split("}")[1]: el.get(qn("w:val")) for el in b}
    for edge in ("left", "right", "insideV"):
        if vals.get(edge) != "nil":
            out.append(Finding("PFT-TBL-001", E,
                               f"{edge} 边框不是 nil——三线表不能有竖线"))
    if vals.get("top") == "nil" or vals.get("bottom") == "nil":
        out.append(Finding("PFT-TBL-001", E, "顶线或底线缺失"))
    return out


def header_rule_findings(t, h_end: int) -> list[Finding]:
    """表头行必须有下边线，否则不是三线表。"""
    qn = _qn()
    for row in t.rows[:max(h_end, 1)]:
        for c in row.cells:
            tcPr = c._tc.tcPr
            tb = tcPr.find(qn("w:tcBorders")) if tcPr is not None else None
            if tb is not None and tb.find(qn("w:bottom")) is not None:
                return []
    return [Finding("PFT-TBL-002", E, "表头行没有下边线——三线表的中间那条线缺了")]


def empty_run_findings(t) -> list[Finding]:
    n = sum(1 for r in t.rows for c in r.cells
            if any(not run.text.strip() for run in c.paragraphs[0].runs))
    if not n:
        return []
    return [Finding("PFT-TBL-000", W, f"{n} 个单元格含空 run，检查是否残留空文本")]


def leading_zero_findings(t, h_end: int, profile: dict,
                          keep: set[str] | None = None) -> list[Finding]:
    """前导零：APA 省略 r/β/p/R²/α 的，保留 B/SE/M/SD/t/F/d 的；中文刊一律保留。

    `keep` 是生成器显式声明「这一列保留前导零」的表头名，审核别人的表时为空。
    """
    if profile["table"]["leading_zero"]:
        return []
    keep = keep or set()
    out: list[Finding] = []
    head_row = t.rows[max(h_end - 1, 0)]
    for j in range(len(t.columns)):
        try:
            head = head_row.cells[j].text.strip()
        except IndexError:
            head = ""
        if head in keep:
            continue
        hits = [line.strip()
                for r in t.rows[h_end:] if j < len(r.cells)
                for line in r.cells[j].text.split("\n")
                if re.fullmatch(r"0\.\d+", line.strip())]
        if hits:
            out.append(Finding(
                "PFT-TBL-003", W,
                f"「{head or f'第 {j+1} 列'}」列有 {len(hits)} 个单元格写作 0.xx"
                f"（如 {hits[0]}）：APA 对 r / β / p / R² / α 省略前导零，"
                "对 B / SE / M / SD / t / F / d 保留——按列的性质确认，"
                "或在该列写 \"leading_zero\": true / false",
                limit="检查器不知道每列在统计上是什么量，只能按列报"))
    return out


def decimals_findings(t, h_end: int) -> list[Finding]:
    """同一列小数位必须一致——右对齐只在各格小数位相同时才等于按小数点对齐。"""
    out: list[Finding] = []
    for j in range(len(t.columns)):
        decs, samples = set(), []
        for r in t.rows[h_end:]:
            if j >= len(r.cells):
                continue
            for txt in (x.strip() for x in r.cells[j].text.split("\n")):
                m = NUM_RE.match(txt)
                if not m or (m.group(2) == "" and m.group(3) is None):
                    continue
                decs.add(len(m.group(3) or ""))
                samples.append(txt)
        if len(decs) > 1 and len(samples) >= 2:
            out.append(Finding(
                "PFT-TBL-004", W,
                f"第 {j+1} 列的小数位不一致（{min(decs)}–{max(decs)} 位，如 "
                f"{samples[0]} / {samples[-1]}）：右对齐不会让小数点对齐，"
                "建议在该列写 \"decimals\": N 统一，或核对原始数据",
                limit="只提示，不替你补零——补零等于声明了不存在的精度"))
    return out


def _is_negative_zero(s: str) -> bool:
    """`-0.00` 这种「四舍五入后是零却带负号」的写法。"""
    t = str(s).strip().rstrip("*")
    if not t.startswith("-"):
        return False
    body = t[1:].replace(",", "").strip()
    return bool(body) and set(body) <= set("0.") and body.count(".") <= 1


# 数字 token：负号 + 可选的整数部分 + 小数部分。用它从「-0.00（-0.08）」这种
# 复合单元格里把每个数拆出来——只按整格匹配会漏掉嵌在括号里的那个。
NUM_TOKEN = re.compile(r"-?\d[\d,]*(?:\.\d+)?")

DASH_RUN = re.compile(r"^[-–—]{2,}$")


def negative_zero_findings(t) -> list[Finding]:
    """不该出现 -0.00。

    它是四舍五入的产物：真实值 −0.004 报成 −0.00，读者会读成「负的、只是很小」，
    而实际上检验不显著、方向也不可靠。APA 要求写成 0.00（去掉负号），
    或者多给一位小数让符号有意义。
    """
    hits = []
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            for tok in NUM_TOKEN.findall(cell.text):
                if _is_negative_zero(tok):
                    hits.append((ri + 1, ci + 1, cell.text.strip()[:24]))
                    break
    if not hits:
        return []
    return [Finding("PFT-TBL-015", E,
                    f"{len(hits)} 个单元格里出现负零（第 {hits[0][0]} 行第 {hits[0][1]} 列「{hits[0][2]}」）："
                    "四舍五入到 0 的负数应当写成 0.00，不带负号——"
                    "-0.00 会让读者以为「负向但很小」，而实际方向并不可靠",
                    limit="按数字 token 扫；-0.004 这类不算")]


def placeholder_findings(t) -> list[Finding]:
    """空缺用连字符串（----）冒充破折号。"""
    hits = []
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            s = cell.text.strip()
            if s and DASH_RUN.match(s):
                hits.append((ri + 1, ci + 1, s))
    if not hits:
        return []
    sample = hits[0][2]
    return [Finding("PFT-TBL-016", W,
                    f"{len(hits)} 个空缺格写成「{sample}」（连字符串）："
                    "规范写法是一个破折号「—」或留空，并在表注里说明空缺的含义",
                    limit="只认整格都是连字符的情况；格内混排不查")]


def width_findings(t) -> list[Finding]:
    """单元格宽度必须与列网格一致。

    合并单元格时 python-docx 只加 gridSpan，**tcW 仍是合并前各格之和**；固定列宽的表里
    Word 按 tcW 排版，于是「95% CI」这类跨列标题只占一列宽、挤在左边。
    这个错在 XML 里一眼看不出来（gridSpan 是对的），但打开 Word 就看得见——
    所以必须把 tcW 与 gridCol 对起来查。
    """
    qn = _qn()
    grid_el = t._tbl.find(qn("w:tblGrid"))
    if grid_el is None:
        return []
    grid = [int(g.get(qn("w:w"))) for g in grid_el.findall(qn("w:gridCol"))]
    if not grid:
        return []
    out: list[Finding] = []
    for ri, row in enumerate(t.rows):
        col = 0
        for tc in row._tr.findall(qn("w:tc")):
            tcPr = tc.tcPr
            span = tcPr.find(qn("w:gridSpan")) if tcPr is not None else None
            n = int(span.get(qn("w:val"))) if span is not None else 1
            tcW = tcPr.find(qn("w:tcW")) if tcPr is not None else None
            wtype = tcW.get(qn("w:type")) if tcW is not None else None
            w = int(tcW.get(qn("w:w"))) if tcW is not None and tcW.get(qn("w:w")) else None
            want = sum(grid[col:col + n])
            # 只比 dxa（缇）；百分比等其他单位的 w 值不是长度，比了就是误报
            if w is not None and wtype in (None, "dxa") and abs(w - want) > 20:
                out.append(Finding(
                    "PFT-TBL-012", E,
                    f"第 {ri+1} 行第 {col+1} 列的单元格宽 {w/20:.1f} pt，"
                    f"但列网格是 {want/20:.1f} pt（跨 {n} 列）——"
                    "合并单元格后没有重设宽度，Word 里跨列标题会挤在左边",
                    limit="只比 dxa 单位；没有 tcW 的单元格跳过"))
            col += n
        if len(out) >= 4:
            break
    return out


def page_fit_findings(t, doc) -> list[Finding]:
    """表宽不能超过版心。

    过宽的表要么缩字号、要么改成横向页。工具**不替你决定**，但要把它查出来——
    否则 Word 会把表挤出页面右边，打印时直接切掉最右一列，而在屏幕上看不出来。
    横向页的版心是「页高 − 左右边距」，所以要读 section 的实际几何，不能写死 6.5 in。
    """
    qn = _qn()
    grid_el = t._tbl.find(qn("w:tblGrid"))
    if grid_el is None:
        return []
    total = sum(int(g.get(qn("w:w"))) for g in grid_el.findall(qn("w:gridCol"))) / 20.0
    if total <= 0:
        return []
    sec = doc.sections[0]
    try:
        # Length 相减会退化成普通 int，所以先各自取 .pt 再算
        avail = sec.page_width.pt - sec.left_margin.pt - sec.right_margin.pt
    except (AttributeError, TypeError):     # 老文档可能没有显式页宽/边距
        return []
    landscape = getattr(sec, "orientation", None) == 1
    if total > avail + 1.0:
        return [Finding(
            "PFT-TBL-014", E,
            f"表宽 {total:.0f} pt，超过当前版心 {avail:.0f} pt"
            f"（{'横向' if landscape else '纵向'}页）——Word 会把最右一列挤到页外，"
            f"打印时被切掉。要么缩字号/缩列名，要么加 \"landscape\": true",
            limit="只比总宽与版心；单元格内部是否拥挤不在本项判断范围内")]
    return []


def word_break_findings(t, profile: dict) -> list[Finding]:
    """单元格宽度必须放得下它最长的那个词。

    Word 在单元格窄于单词时**从词中间断开**（实测 `Relational` 被断成
    `Relationa / l`）。这属于「打开文件才看得见」的缺陷：XML 结构完全合法，
    gridSpan 也对，只有把 tcW 与文字宽度对起来才发现。

    折行是排版差异，断词是缺陷——读者会把它当成拼写错误。
    """
    qn = _qn()
    from textmetrics import _segments, word_min_width
    pad = 2 * profile["table"]["cell_pad"] + 2
    out: list[Finding] = []
    for ri, row in enumerate(t.rows):
        for ci, cell in enumerate(row.cells):
            text = cell.text.strip()
            if not text or len(text) < 4:
                continue
            size = None
            for p in cell.paragraphs:
                for run in p.runs:
                    if run.text.strip() and run.font.size is not None:
                        size = run.font.size.pt
                        break
                if size:
                    break
            if not size:
                size = profile["table"]["size"]
            need = word_min_width(text, size)
            w = cell.width.pt if cell.width is not None else None
            if w is not None and w - pad < need - 0.5:
                longest = max(_segments(text), key=lambda s: word_min_width(s, size))
                out.append(Finding(
                    "PFT-TBL-013", E,
                    f"第 {ri+1} 行第 {ci+1} 列「{text[:16]}」只有 {w:.0f} pt，"
                    f"放不下 {need:.0f} pt 的「{longest}」——Word 会从词中间断开",
                    limit="按 Times 字宽估算；字体不是 Times 时实际宽度有 5% 上下浮动"))
                if len(out) >= 3:
                    return out
    return out


def _run_sizes(t) -> list[float]:
    sizes = []
    for row in t.rows:
        for c in row.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    if run.text.strip() and run.font.size is not None:
                        sizes.append(run.font.size.pt)
    return sizes


def font_size_findings(t, profile: dict) -> list[Finding]:
    """表内字号：既要落在允许区间内，又要前后一致。

    APA 允许表内 8–14 pt（可与正文不同），所以不能像某些实现那样卡死一个值——
    那会把合规的 10.5 pt 判成错误。真正该报的是「出了区间」和「同一张表里不一致」。
    """
    out: list[Finding] = []
    sizes = _run_sizes(t)
    if not sizes:
        return out
    lo = float(profile["figure"]["min_text_pt"])
    hi = float(profile["figure"]["max_text_pt"])
    if min(sizes) < lo - 0.05 or max(sizes) > hi + 0.05:
        out.append(Finding("PFT-TBL-010", E,
                           f"表内字号 {min(sizes):.1f}–{max(sizes):.1f} pt，"
                           f"超出 profile（{profile['profile_id']}）允许的 {lo:g}–{hi:g} pt",
                           limit="按 Word 里记录的字号算；插入文档后被缩放的情况看不到"))
    elif max(sizes) - min(sizes) > 0.6:
        out.append(Finding("PFT-TBL-010", W,
                           f"同一张表里字号不一致（{min(sizes):.1f}–{max(sizes):.1f} pt），"
                           "多半是粘贴时带进了别的样式",
                           limit="只比字号数值，不判断哪一处才是作者的本意"))
    return out


def stat_symbol_findings(t) -> list[Finding]:
    """表头里的统计符号该斜体的斜体、希腊字母不该斜体的不斜体。

    按 run 精确比对：只在整段文字恰好是某个符号时才判，
    避免把 "M (SD)" 这种混合表头误判成符号没斜体。
    """
    out: list[Finding] = []
    rows = t.rows[:1]
    for row in rows:
        for c in row.cells:
            for p in c.paragraphs:
                for run in p.runs:
                    s = run.text.strip()
                    if not s:
                        continue
                    if s in ITALIC_SYMBOLS and not run.italic:
                        out.append(Finding("PFT-TBL-011", W,
                                           f"表头符号 {s} 未设为斜体",
                                           limit="只检查表头；正文与表注里的符号需人工看"))
                    elif s in UPRIGHT_SYMBOLS and run.italic:
                        out.append(Finding("PFT-TBL-011", W,
                                           f"表头符号 {s} 是希腊字母，不应斜体"))
    # 同一符号在多列重复报太吵，按符号去重
    seen, uniq = set(), []
    for f in out:
        key = str(f)
        if key not in seen:
            seen.add(key)
            uniq.append(f)
    return uniq


def caption_context(blocks, table_idx: int):
    """表格前最多两段（由近及远）与表格后一段。

    APA 的表题是**两行**：先「Table 1」，下一行才是标题。只看紧邻的一段会把
    「Table 1」判成缺失——审核器第一版就这么误报了。
    """
    prevs = [b for b in blocks[max(0, table_idx - 2):table_idx]
             if not hasattr(b, "rows")]
    after = blocks[table_idx + 1] if table_idx + 1 < len(blocks) else None
    return prevs, after


def _is_caption(text: str) -> tuple[bool, str]:
    m = CAP_EN.match(text) or CAP_ZH.match(text)
    if not m:
        return False, ""
    return True, m.group(1)


def caption_findings(prevs, after, profile: dict) -> list[Finding]:
    """表题：有没有、在不在表格上方、编号对不对、对齐与字重是否符合 profile。"""
    out: list[Finding] = []
    prevs = list(prevs or [])
    text_after = (after.text if after is not None else "").strip()

    # 由近及远找「表 N / Table N」那一段
    cap = None
    cap_pos = None
    for k in range(len(prevs) - 1, -1, -1):
        if _is_caption(prevs[k].text.strip())[0]:
            cap, cap_pos = prevs[k], k
            break

    if cap is None:
        if _is_caption(text_after)[0]:
            out.append(Finding("PFT-TBL-009", E,
                               f"表题「{text_after[:20]}」在表格下方，应在表格上方",
                               limit="只按段落顺序判断；文本框里的表题看不到"))
        else:
            out.append(Finding("PFT-TBL-009", E,
                               "表格前面没有表题段落（形如「表 1 …」或「Table 1 …」）",
                               limit="表题若放在文本框或页眉里，本检查看不到"))
        return out

    # 两行式：表号一行（靠前）、标题一行（紧邻表格）。
    # 注意方向——表号在**前**，标题在**后**；第一版把位置判反了，于是把合规的两行式
    # 报成「同一行」并且连带报了「表题未斜体」。
    two_line = (cap_pos == len(prevs) - 2) and bool(prevs[-1].text.strip())
    want_two = bool(profile["table"]["title_on_separate_line"])
    if two_line and not want_two:
        out.append(Finding("PFT-TBL-009", W,
                           "表号与表题分成了两行，该 profile 要求同一行",
                           limit="只按段落判断；用换行符分行的情况查不到"))
    if not two_line and want_two:
        out.append(Finding("PFT-TBL-009", W,
                           "表号与表题在同一行，该 profile 要求分两行（APA：表号一行、标题一行）"))

    want_align = profile["table"]["title_align"]
    got_align = {0: "left", 1: "center", 2: "right"}.get(
        int(cap.paragraph_format.alignment or -1), "inherit")
    if got_align not in (want_align, "inherit"):
        out.append(Finding("PFT-TBL-009", W,
                           f"表题对齐为 {got_align}，profile 要求 {want_align}",
                           limit="只读段落级对齐；用制表符或空格凑出来的对齐查不到"))

    want_num_bold = profile["table"]["number_bold"]
    want_title_italic = profile["table"]["title_italic"]
    runs = [r for r in cap.runs if r.text.strip()]
    if runs:
        if want_num_bold and not runs[0].bold:
            out.append(Finding("PFT-TBL-009", W,
                               f"表号「{runs[0].text.strip()[:12]}」未加粗（profile 要求加粗）"))
        if want_title_italic:
            # 两行式时斜体应在标题那一段；一行式时在表号之后
            title_para = prevs[-1] if two_line else cap
            if title_para.text.strip() and not any(r.italic for r in title_para.runs):
                out.append(Finding("PFT-TBL-009", W,
                                   "表题未设斜体（profile 要求斜体）"))
        elif any(r.italic for r in cap.runs):
            out.append(Finding("PFT-TBL-009", W, "表题用了斜体，但该 profile 要求正体"))
    return out
