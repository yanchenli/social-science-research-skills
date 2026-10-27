"""发布前预检：查**导出的文件**能不能投，不是查规格对不对。

两个检查器分工：

| 脚本 | 查什么 | 输入 |
|---|---|---|
| `check_figure.py` | 规格层：图幅、字号、线宽、边框、前导零、小数位 | `.svg` / `.docx` |
| `preflight.py` | 文件层：DPI、透明通道、字体嵌入、可疑码位、字形覆盖、灰度可辨 | `.svg` / `.pdf` / `.png` / `.tif` |

为什么要分开：规格对了，导出的文件仍可能不合格——PNG 没写 DPI、PDF 没嵌字体、
颜色转成灰分不开、某个中文字符在目标字体里不存在（印出来是方框）。
这些只有看**文件本身**才能发现。

用法：

    python scripts/preflight.py fig.png fig.pdf --dpi-min 300
    python scripts/preflight.py fig.svg --json report.json
    python scripts/preflight.py --rules            # 列出规则目录

**这不是合规认证。** 报告里固定写 `publication_ready_claim: false`——
它只覆盖 `assets/rules.json` 里列明的自动检查项。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from qc import E, I, W, Finding, print_findings, write_report  # noqa: E402

HERE = Path(__file__).resolve().parent
RULES_PATH = HERE.parent / "assets" / "rules.json"
SVG_NS = "{http://www.w3.org/2000/svg}"
DPI_MIN_DEFAULT = 300
LUM_DELTA_MIN = 18.0          # 灰度亮度差小于这个值，黑白印刷分不开
SUSPECT_LIMIT = 30


# ---------------------------------------------------------------- 规则目录
def load_rules() -> dict:
    return json.loads(RULES_PATH.read_text(encoding="utf-8"))


def print_rules() -> int:
    cat = load_rules()
    print(f"规则目录 {cat['catalog_version']}（{cat['status']}）— {len(cat['rules'])} 条\n")
    print(cat["note"] + "\n")
    for r in cat["rules"]:
        auto = "自动" if r["automated"] else "人工"
        print(f"{r['id']}  [{r['scope']}/{auto}] {r['title']}")
        print(f"  检查：{r['check']}")
        print(f"  出处：{cat['sources'].get(r['source'], r['source'])}")
        print(f"  局限：{r['limit']}\n")
    return 0


# ---------------------------------------------------------------- 通用工具
def _lum(rgb: tuple[int, int, int]) -> float:
    return 0.299 * rgb[0] + 0.587 * rgb[1] + 0.114 * rgb[2]


def _hex_rgb(c: str) -> tuple[int, int, int] | None:
    c = c.strip().lstrip("#")
    if len(c) == 3:
        c = "".join(ch * 2 for ch in c)
    if len(c) != 6 or not re.fullmatch(r"[0-9a-fA-F]{6}", c):
        return None
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def unicode_audit(text: str, where: str) -> list[Finding]:
    """找替换字符、私用区、未分配码位与意外控制字符。

    这些字符在屏幕上可能看着正常，换台机器就是方框或乱码——
    而且它们通常是「复制粘贴带进来的」，作者自己不会发现。
    """
    out: list[Finding] = []
    bad = []
    for i, ch in enumerate(text):
        cp = ord(ch)
        if ch == "\ufffd":
            kind = "替换字符 U+FFFD（说明某处编码失败）"
        elif 0xE000 <= cp <= 0xF8FF or 0xF0000 <= cp <= 0xFFFFD:
            kind = f"私用区字符 U+{cp:04X}"
        elif unicodedata.category(ch) == "Cn":
            kind = f"未分配码位 U+{cp:04X}"
        elif unicodedata.category(ch) == "Cc" and ch not in "\t\r\n":
            kind = f"控制字符 U+{cp:04X}"
        else:
            continue
        bad.append((cp, kind, text[max(0, i - 12):i + 13]))
        if len(bad) >= SUSPECT_LIMIT:
            break
    if bad:
        sample = "；".join(f"{k}（…{ctx}…）" for _, k, ctx in bad[:3])
        out.append(Finding("PFT-EXP-004", E,
                           f"{where} 含 {len(bad)} 个可疑码位：{sample}",
                           limit="只报可疑码位；是否真的缺字要看 PFT-EXP-005 的字形检查"))
    return out


def color_luminance_audit(colors: set[str], where: str) -> list[Finding]:
    """灰度亮度差过小的颜色对。

    只读 `style="fill:#..."` 是不够的——呈现属性 `fill="#..."` 同样常见，
    只认一种写法会让检查静默通过（这正是我从别人的实现里学到的一课）。
    """
    items = []
    for c in sorted(colors):
        rgb = _hex_rgb(c)
        if rgb is None:
            continue
        items.append((c, _lum(rgb)))
    pairs = []
    for i, (c1, l1) in enumerate(items):
        for c2, l2 in items[i + 1:]:
            if abs(l1 - l2) < LUM_DELTA_MIN:
                pairs.append((c1, c2, abs(l1 - l2)))
    if not pairs:
        return []
    sample = "；".join(f"{a} 与 {b}（差 {d:.0f}）" for a, b, d in pairs[:3])
    return [Finding("PFT-FIG-008", W,
                    f"{where} 有 {len(pairs)} 对颜色的灰度亮度差 < {LUM_DELTA_MIN:.0f}：{sample}",
                    limit="只看颜色亮度差，不判断它们是否属于同一数据系列；"
                          "若已用线型/标记区分则无需处理")]


def glyph_audit(text: str, families: list[str], where: str) -> list[Finding]:
    """声明的字体有没有这些字形。没装 matplotlib 时如实报「未检查」。"""
    chars = {ch for ch in text if ch.strip()}
    if not chars:
        return []
    try:
        from matplotlib import font_manager
        from matplotlib.ft2font import FT2Font
    except ImportError:
        return [Finding("PFT-EXP-005", I,
                        f"{where} 未检查字形覆盖：没有 matplotlib",
                        limit="pip install matplotlib 后可查")]
    try:
        path = font_manager.findfont(font_manager.FontProperties(family=families or None),
                                     fallback_to_default=True)
        cmap = FT2Font(path).get_charmap()
    except Exception as e:                                   # noqa: BLE001
        return [Finding("PFT-EXP-005", I, f"{where} 未检查字形覆盖：{type(e).__name__}")]
    missing = sorted({ch for ch in chars if ord(ch) not in cmap})
    if not missing:
        return []
    return [Finding("PFT-EXP-005", E,
                    f"{where} 用的字体（{Path(path).stem}）缺这些字符：{''.join(missing[:12])}",
                    limit="查的是本机字体；目标排版机字体不同，仍需在那台机器上复核")]


# ---------------------------------------------------------------- 各类文件
def png_info(path: Path) -> dict:
    """读 PNG 头：尺寸、位深、颜色类型、pHYs 里的 DPI、有没有 tRNS。"""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("不是 PNG")
    pos, info = 8, {"dpi": None, "trns": False}
    while pos + 8 <= len(data):
        ln = int.from_bytes(data[pos:pos + 4], "big")
        typ = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR":
            info["width"] = int.from_bytes(body[0:4], "big")
            info["height"] = int.from_bytes(body[4:8], "big")
            info["bit_depth"] = body[8]
            info["color_type"] = body[9]
        elif typ == b"pHYs" and len(body) >= 9:
            px = int.from_bytes(body[0:4], "big")
            if body[8] == 1 and px:                       # 单位：米
                info["dpi"] = px * 0.0254
        elif typ == b"tRNS":
            info["trns"] = True
        elif typ == b"IEND":
            break
        pos += 12 + ln
    return info


def check_png(path: Path, dpi_min: int) -> list[Finding]:
    out: list[Finding] = []
    try:
        info = png_info(path)
    except Exception as e:                                   # noqa: BLE001
        return [Finding("PFT-EXP-000", E, f"{path.name} 读不出 PNG 头：{e}")]
    dpi = info.get("dpi")
    if dpi is None:
        out.append(Finding("PFT-EXP-001", I,
                           f"{path.name} 没写 DPI 元数据，无法判定分辨率"
                           f"（{info['width']}×{info['height']} px）",
                           limit="有的导出工具不写 pHYs 块；按 300 dpi 折算需 "
                                  f"{info['width']/300*2.54:.1f} cm 宽"))
    elif dpi + 0.5 < dpi_min:
        out.append(Finding("PFT-EXP-001", E,
                           f"{path.name} 为 {dpi:.0f} dpi，低于 {dpi_min}",
                           limit="期刊常要求线条图 ≥ 300 dpi，以目标刊为准"))
    if info.get("color_type") in (4, 6) or info.get("trns"):
        out.append(Finding("PFT-EXP-002", E,
                           f"{path.name} 带透明通道（color type {info.get('color_type')}"
                           f"{'，含 tRNS' if info.get('trns') else ''}）",
                           limit="部分投稿系统会拒收带透明通道的图"))
    return out


def check_pdf(path: Path) -> list[Finding]:
    out: list[Finding] = []
    try:
        import pymupdf
    except ImportError:
        return [Finding("PFT-EXP-003", I, f"{path.name} 未检查字体嵌入：没有 PyMuPDF",
                        limit="pip install pymupdf 后可查")]
    with pymupdf.open(str(path)) as doc:
        page = doc[0]
        fonts = page.get_fonts(full=True)
        not_embedded = [f[3] for f in fonts if not f[1]]
        type3 = [f[3] for f in fonts if (f[2] or "").lower() == "type3"]
        if not_embedded:
            out.append(Finding("PFT-EXP-003", E,
                               f"{path.name} 有 {len(not_embedded)} 个字体未嵌入："
                               f"{', '.join(not_embedded[:4])}",
                               limit="未嵌入的字体在别人机器上会被替换，版式会跑"))
        if type3:
            out.append(Finding("PFT-EXP-003", E,
                               f"{path.name} 用了 Type 3 位图字体：{', '.join(type3[:4])}",
                               limit="多数期刊不接受 Type 3"))
        text = "".join(p.get_text() for p in doc)
        # 空白页检查：字体嵌好、DPI 达标，页面上却什么都没有——这类 PDF 一路
        # 通过所有文件层检查，直到有人打开它。合成图导出时最容易出这个。
        ink = [i for i, p in enumerate(doc)
               if len(p.get_drawings()) or p.get_text().strip() or p.get_images()]
        if not ink:
            out.append(Finding("PFT-EXP-007", E,
                               f"{path.name} 的 {len(doc)} 页上没有任何矢量图元、文字或图片——"
                               "这是一张空白页。多面板图导出成 PDF 时最容易出这个："
                               "合成若只把子图的 SVG 文本塞进 <g>，图元清单是空的",
                               limit="只判断页面上有没有东西，不判断内容对不对"))
        out += unicode_audit(text, f"{path.name}（文本层）")
    return out


def check_tiff(path: Path, dpi_min: int) -> list[Finding]:
    try:
        from PIL import Image
    except ImportError:
        return [Finding("PFT-EXP-001", I, f"{path.name} 未检查 TIFF：没有 Pillow",
                        limit="pip install pillow 后可查")]
    with Image.open(path) as im:
        out: list[Finding] = []
        dpi = im.info.get("dpi")
        if not dpi:
            out.append(Finding("PFT-EXP-001", I, f"{path.name} 没写 DPI，无法判定分辨率"))
        elif min(dpi) + 0.5 < dpi_min:
            out.append(Finding("PFT-EXP-001", E,
                               f"{path.name} 为 {min(dpi):.0f} dpi，低于 {dpi_min}"))
        if im.mode in ("RGBA", "LA", "PA") or "transparency" in im.info:
            out.append(Finding("PFT-EXP-002", E,
                               f"{path.name} 带透明通道（mode {im.mode}）"))
        return out


def svg_texts(root) -> tuple[str, list[str]]:
    """取出全部文字与声明过的字体族。"""
    text, fams = [], []
    for el in root.iter(f"{SVG_NS}text"):
        if el.text:
            text.append(el.text)
        f = el.get("font-family")
        if f:
            fams.append(f)
    root_f = root.get("font-family")
    if root_f:
        fams.append(root_f)
    flat: list[str] = []
    for f in fams:
        for part in f.split(","):
            part = part.strip().strip("'\"")
            if part and part not in ("serif", "sans-serif", "monospace"):
                flat.append(part)
    return "".join(text), flat


def check_svg(path: Path, dpi_min: int) -> list[Finding]:
    """只做**文件层**检查。规格层（字号/线宽/越界）交给 check_figure.py。"""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return [Finding("PFT-EXP-000", E, f"{path.name} XML 解析失败：{e}")]
    out: list[Finding] = []
    text, fams = svg_texts(root)
    out += unicode_audit(text, path.name)
    out += glyph_audit(text, fams, path.name)

    colors: set[str] = set()
    for el in root.iter():
        for key in ("fill", "stroke"):
            v = el.get(key)
            if v and v.startswith("#"):
                colors.add(v)
        style = el.get("style") or ""
        for m in re.finditer(r"(?:^|;)\s*(?:fill|stroke)\s*:\s*(#[0-9a-fA-F]{3,6})", style):
            colors.add(m.group(1))
    out += color_luminance_audit(colors, path.name)
    return out


# ---------------------------------------------------------------- 尺寸一致性
def _pt_size(path: Path) -> tuple[float, float] | None:
    """读文件的物理尺寸（pt）。"""
    suffix = path.suffix.lower()
    if suffix == ".svg":
        root = ET.parse(path).getroot()
        w = (root.get("width") or "").replace("pt", "").replace("px", "")
        h = (root.get("height") or "").replace("pt", "").replace("px", "")
        try:
            return float(w), float(h)
        except ValueError:
            return None
    if suffix == ".pdf":
        try:
            import pymupdf
        except ImportError:
            return None
        with pymupdf.open(str(path)) as doc:
            r = doc[0].rect
            return float(r.width), float(r.height)
    if suffix == ".png":
        try:
            info = png_info(path)
        except Exception:                                    # noqa: BLE001
            return None
        dpi = info.get("dpi") or 0
        if not dpi:
            return None
        return info["width"] / dpi * 72, info["height"] / dpi * 72
    return None


def check_size_match(files: list[Path]) -> list[Finding]:
    """同名不同后缀的文件，物理尺寸应当一致。

    这是「SVG 与 PDF 是不是同一张图」的机器判据：布局只算一次、两个渲染器
    共用坐标，尺寸就必然相等。哪天不相等，说明有一边跑偏了。
    """
    by_stem: dict[str, list[Path]] = {}
    for f in files:
        by_stem.setdefault(f.stem, []).append(f)
    out: list[Finding] = []
    for stem, group in by_stem.items():
        if len(group) < 2:
            continue
        sizes = {p.suffix.lower(): _pt_size(p) for p in group}
        known = {k: v for k, v in sizes.items() if v}
        if len(known) < 2:
            continue
        ref_ext, ref = next(iter(known.items()))
        for ext, size in known.items():
            if ext == ref_ext:
                continue
            if abs(size[0] - ref[0]) > 0.6 or abs(size[1] - ref[1]) > 0.6:
                out.append(Finding("PFT-EXP-006", E,
                                   f"{stem}{ext} 尺寸 {size[0]:.1f}×{size[1]:.1f} pt "
                                   f"与 {stem}{ref_ext} 的 {ref[0]:.1f}×{ref[1]:.1f} pt 不一致",
                                   limit="只比对首页/画布尺寸；多页 PDF 需人工看"))
    return out


# ---------------------------------------------------------------- 入口
def main() -> int:
    ap = argparse.ArgumentParser(description="发布前预检（文件层）")
    ap.add_argument("files", nargs="*")
    ap.add_argument("--json", help="把结论写成 JSON 报告")
    ap.add_argument("--dpi-min", type=int, default=DPI_MIN_DEFAULT)
    ap.add_argument("--rules", action="store_true", help="列出规则目录")
    args = ap.parse_args()

    if args.rules:
        return print_rules()
    if not args.files:
        print(__doc__)
        return 2

    files = [Path(f) for f in args.files]
    findings: list[Finding] = []
    for f in files:
        print(f"\n{f.name}")
        if not f.exists():
            findings.append(Finding("PFT-EXP-000", E, f"{f.name} 不存在"))
            print(f"  ✗ 文件不存在")
            continue
        suffix = f.suffix.lower()
        if suffix == ".svg":
            got = check_svg(f, args.dpi_min)
        elif suffix == ".pdf":
            got = check_pdf(f)
        elif suffix == ".png":
            got = check_png(f, args.dpi_min)
        elif suffix in (".tif", ".tiff"):
            got = check_tiff(f, args.dpi_min)
        else:
            got = [Finding("PFT-EXP-000", I, f"{f.name} 不支持的文件类型：{suffix}")]
        findings += got
        if not got:
            print("  ✓ 文件层检查通过")
        else:
            print_findings(got)

    if len(files) > 1:
        same = check_size_match(files)
        if same:
            print("\n尺寸一致性")
            print_findings(same)
            findings += same

    n_err = sum(1 for f in findings if f.severity == E)
    n_warn = sum(1 for f in findings if f.severity == W)
    n_skip = sum(1 for f in findings if f.severity == I)
    print(f"\n合计 {n_err} 个必须修的问题，{n_warn} 个提示，{n_skip} 项未检查")
    print("本报告不构成期刊合规认证：只覆盖规则目录里列明的自动检查项。")

    if args.json:
        p = write_report(args.json, findings, targets=[str(f) for f in files],
                         tool="paper-figures-tables/preflight")
        print(f"报告：{p}")
    return 1 if n_err else 0


if __name__ == "__main__":
    sys.exit(main())
