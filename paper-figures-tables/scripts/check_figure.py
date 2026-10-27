"""交付前自检（规格层）：检查 SVG / DOCX 是否符合排版规格。

用法：
    python check_figure.py out.svg
    python check_figure.py table.docx
    python check_figure.py out.svg table.docx --json report.json

只做**能机器判定**的检查，每条结论都带规则编号（见 `assets/rules.json`）。
判断类的问题（这个图该不该画、表里放什么）不在这里，那属于 SKILL.md 的决策步骤。

两层分工：本脚本查**规格**（图幅、字号、线宽、边框、前导零、小数位、越界）；
导出的文件能不能投（DPI、透明通道、字体嵌入、可疑码位）交给 `preflight.py`。
"""
from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import profiles  # noqa: E402
import table_checks  # noqa: E402
from qc import E, I, W, Finding, print_findings, write_report  # noqa: E402

SVG_NS = "{http://www.w3.org/2000/svg}"

# 兜底取值。实际运行时由 profile 决定（见 assets/profiles/*.json）：
# 中文期刊允许图内文字到 7.5 pt，学位论文可能又不同，写死会在别处误报。
FS_MIN, FS_MAX = 8.0, 14.0
WIDTH_MAX_IN = 6.5          # APA 整幅宽
LINE_MIN = 0.4              # 数据线不应细于 0.4 pt


def _default_profile() -> dict:
    return profiles.load("apa7", quiet=True)


def _est_width(s: str, size: float) -> float:
    """与 svg_kit.text_width 同一套估算：CJK 按 1 em，其余按 0.55 em。"""
    return sum(size * (1.0 if ord(ch) > 0x2E7F else 0.55) for ch in s)


def _overflowing_text(root, w: float, h: float, tol: float = 4.0) -> list[tuple[str, str]]:
    """找出跑到画布外面的文字。

    为什么要有这一条：SVG 不会替你报错，超出 viewBox 的字在浏览器里看得见、
    插进 Word 或转 PDF 时被裁掉。之前只查了字号，没查位置，
    所以「轴标题压在数据上」「刻度数字落进绘图区」这类问题全靠人眼看。
    旋转文字（纵轴标题）的包围盒要按旋转后算，估算不可靠，直接跳过。
    """
    bad = []
    for el in root.iter(f"{SVG_NS}text"):
        if el.get("transform"):
            continue
        s = (el.text or "").strip()
        if not s:
            continue
        size = float(el.get("font-size") or 9)
        x, y = float(el.get("x") or 0), float(el.get("y") or 0)
        tw = _est_width(s, size)
        anchor = el.get("text-anchor", "start")
        x0 = x - tw / 2 if anchor == "middle" else (x - tw if anchor == "end" else x)
        x1 = x0 + tw
        y0, y1 = y - size * 0.8, y + size * 0.25
        if x0 < -tol or x1 > w + tol or y0 < -tol or y1 > h + tol:
            bad.append((s[:30], f"x {x0:.1f}–{x1:.1f}, y {y0:.1f}–{y1:.1f}"))
    return bad


def check_svg(path: Path, prof: dict | None = None) -> tuple[list[Finding], list[Finding]]:
    errs: list[Finding] = []
    warns: list[Finding] = []
    prof = prof or _default_profile()
    fig = prof["figure"]
    fs_min, fs_max = float(fig["min_text_pt"]), float(fig["max_text_pt"])
    width_max = float(fig["width_in"])
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [Finding("PFT-FIG-000", E, f"XML 解析失败：{e}")], []

    w = float(str(root.get("width", "0")).replace("pt", "") or 0)
    h = float(str(root.get("height", "0")).replace("pt", "") or 0)
    if not w or not h:
        warns.append(Finding("PFT-FIG-001", W,
                             "SVG 没有显式的 width/height（pt），排版软件可能按 96 dpi 解释",
                             limit="只有 width/height 或 viewBox 才决定物理尺寸"))
    else:
        if w / 72 > width_max + 0.01:
            errs.append(Finding("PFT-FIG-001", E,
                                f"图宽 {w/72:.2f} in 超过 profile（{prof['profile_id']}）"
                                f"的 {width_max} in",
                                limit="只查画布声明宽度；插入文档后是否被缩放看不到"))

    sizes = []
    for el in root.iter(f"{SVG_NS}text"):
        fs = el.get("font-size")
        if fs:
            sizes.append((float(fs), (el.text or "")[:24]))
    if not sizes:
        warns.append(Finding("PFT-FIG-000", W,
                             "没有找到任何文本元素——检查是否只画了图形没有标签"))
    small = [(s, t) for s, t in sizes if s < fs_min]
    big = [(s, t) for s, t in sizes if s > fs_max]
    if small:
        errs.append(Finding("PFT-FIG-002", E,
                            f"{len(small)} 处字号小于 {fs_min:g} pt，印刷后会读不清"
                            f"（最小 {min(s for s, _ in small):.1f} pt：{small[0][1]!r}）",
                            limit="按图的声明尺寸计算；缩小后再插入文档时实际字号更小"))
    if big:
        warns.append(Finding("PFT-FIG-002", W,
                             f"{len(big)} 处字号大于 {fs_max:g} pt"
                             f"（{big[0][0]:.1f} pt：{big[0][1]!r}）"))

    thin = []
    for tag in ("line", "polyline", "path", "rect"):
        for el in root.iter(f"{SVG_NS}{tag}"):
            sw = el.get("stroke-width")
            if not sw:
                continue
            # 有填充、线宽 0 的是实心标记（方块/三角/菱形）——它靠填充表达，
            # 不是数据线，不该按「线太细」报。
            if float(sw) == 0 and el.get("fill") not in (None, "none"):
                continue
            if float(sw) < LINE_MIN:
                thin.append(float(sw))
    if thin:
        warns.append(Finding("PFT-FIG-003", W,
                             f"{len(thin)} 条线的线宽小于 {LINE_MIN} pt"
                             f"（最细 {min(thin):.2f}）",
                             limit="只判断粗细，不判断这条线该不该画"))

    for bad in ("filter", "linearGradient", "radialGradient"):
        if list(root.iter(f"{SVG_NS}{bad}")):
            warns.append(Finding("PFT-FIG-010", W,
                                 f"含 {bad}：APA 图表不用阴影与渐变"))

    if w and h:
        over = _overflowing_text(root, w, h)
        if over:
            errs.append(Finding("PFT-FIG-004", E,
                                f"{len(over)} 处文字超出画布，导出/插入时会缺字"
                                f"（如 {over[0][0]!r}：{over[0][1]}）",
                                limit="宽度按 0.55 em/字符估算；旋转文字跳过"))

    if sizes:
        print(f"  SVG  {w/72:.2f} × {h/72:.2f} in，"
              f"文本 {len(sizes)} 处，字号 {min(s for s, _ in sizes):.1f}–"
              f"{max(s for s, _ in sizes):.1f} pt")
    return errs, warns


def check_docx(path: Path, prof: dict | None = None) -> tuple[list[Finding], list[Finding]]:
    """查第一张表。判据都在 table_checks.py，与 audit_table.py 共用同一份。"""
    from docx import Document
    doc = Document(str(path))
    if not doc.tables:
        return [Finding("PFT-TBL-000", E, "文档里没有表格")], []

    t = doc.tables[0]

    # 生成器把 profile 与「显式保留前导零的列」写进文档属性，检查器读同一份规则——
    # 否则会出现「生成按 APA、检查按另一套」。
    fmt, prof_id, keep_lz = "", "", set()
    if doc.core_properties.comments:
        for part in doc.core_properties.comments.split(";"):
            if part.startswith("pft-format:"):
                fmt = part.split(":", 1)[1].strip()
            elif part.startswith("pft-profile:"):
                prof_id = part.split(":", 1)[1].strip()
            elif part.startswith("pft-lz:"):
                keep_lz = {s.strip() for s in part.split(":", 1)[1].split(",") if s.strip()}
    if prof is None:
        prof = profiles.load(prof_id or fmt or "apa7", quiet=True)

    h_end = table_checks.header_end(t)
    found = (table_checks.border_findings(t)
             + table_checks.width_findings(t)
             + table_checks.page_fit_findings(t, doc)
             + table_checks.negative_zero_findings(t)
             + table_checks.placeholder_findings(t)
             + table_checks.word_break_findings(t, prof))
    # 多面板表每个面板自带表头，没有「唯一表头行」这个概念：
    # 前导零、小数位、符号斜体这三项都按「表头 + 表体」划分，套上去只会误报。
    is_panel = "pft-panels:1" in (doc.core_properties.comments or "")
    if not is_panel:
        found += (table_checks.header_rule_findings(t, h_end)
                  + table_checks.font_size_findings(t, prof)
                  + table_checks.stat_symbol_findings(t)
                  + table_checks.leading_zero_findings(t, h_end, prof, keep_lz)
                  + table_checks.decimals_findings(t, h_end))
    found += table_checks.empty_run_findings(t)

    from docx.oxml.ns import qn
    b = t._tbl.tblPr.find(qn("w:tblBorders"))
    vals = ({el.tag.split("}")[1]: el.get(qn("w:val")) for el in b}
            if b is not None else {})
    print(f"  表格 {len(t.rows)} 行 × {len(t.columns)} 列，"
          f"边框 {vals.get('top')}/{vals.get('insideH')}/{vals.get('bottom')}")

    return ([f for f in found if f.severity == E],
            [f for f in found if f.severity != E])


def main() -> int:
    ap = argparse.ArgumentParser(description="交付前自检（规格层）")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json", help="把结论写成 JSON 报告")
    ap.add_argument("--profile", help="按哪个 profile 判定（默认读文档属性，否则 apa7）")
    args = ap.parse_args()
    if not args.files:
        print(__doc__)
        return 2

    # 显式给了 profile 就按它判（会打印状态提醒）；否则每个文件各读各的文档属性
    forced = profiles.load(args.profile) if args.profile else None

    all_findings: list[Finding] = []
    for name in args.files:
        f = Path(name)
        print(f"\n{f.name}")
        if not f.exists():
            all_findings.append(Finding("PFT-GEN-404", E, f"{f.name} 不存在"))
            print("  ✗ 文件不存在")
            continue
        if f.suffix.lower() == ".svg":
            errs, warns = check_svg(f, forced)
        elif f.suffix.lower() in (".docx", ".doc"):
            errs, warns = check_docx(f, forced)
        else:
            print(f"  跳过：不支持 {f.suffix}")
            continue
        all_findings += errs + warns
        if not errs and not warns:
            print("  ✓ 通过")
        else:
            print_findings(errs + warns)

    n_err = sum(1 for x in all_findings if x.severity == E)
    print(f"\n合计 {n_err} 个必须修的问题")
    print("本报告不构成期刊合规认证：只覆盖规则目录里列明的自动检查项。")
    if args.json:
        p = write_report(args.json, all_findings, targets=args.files,
                         tool="paper-figures-tables/check_figure")
        print(f"报告：{p}")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
