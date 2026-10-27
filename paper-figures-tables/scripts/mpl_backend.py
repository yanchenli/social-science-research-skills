"""matplotlib 渲染后端：把同一个 `Svg` 的图元清单重画成 PDF / PNG / TIFF。

为什么要有这一层
----------------
期刊与学位论文的图件要求，一半是 SVG 给不了的：矢量 PDF（字体嵌入）、
300/600 dpi 的无损位图、去掉透明通道、以及「本机有没有这个字体」的如实交代。
matplotlib 能把这些一次做完。

为什么不让生成器直接调 matplotlib
--------------------------------
布局（分层、绕障、标签避让、坐标轴）是这套技能最贵的部分，只写一遍。
本模块**只消费 `Svg.ops`**，不参与任何几何计算——所以 SVG 与 PDF 的
几何必然逐点一致。两份实现各自漂移是这类工具最常见的退化方式。

matplotlib 是可选依赖：没装时 `Svg.export()` 会明确报错并给安装命令，
不会静默只出 SVG 却假装导出了。
"""
from __future__ import annotations

import math
import re
from pathlib import Path

DPI_DEFAULT = 600
# 与 svg_kit 的 marker 定义一致：viewBox 10×10、markerWidth 6、refX 9
ARROW_LEN = 0.6 * (9.0 - 0.5)      # 5.1 pt
ARROW_HALF = 0.6 * (5.0 - 1.2)     # 2.28 pt

CJK_RE = re.compile(r"[\u2e80-\u9fff\uf900-\ufaff\uff00-\uffef]")


def _families(css: str | None) -> list[str]:
    """把 CSS 的 font-family 串拆成 matplotlib 能用的列表。"""
    if not css:
        return []
    out = []
    for part in css.split(","):
        part = part.strip().strip("'\"")
        if not part or part in ("serif", "sans-serif", "monospace", "cursive", "fantasy"):
            continue
        out.append(part)
    return out


_FONT_CACHE: dict[tuple, list[str]] = {}


def _resolve(fams: list[str]) -> list[str]:
    """只保留本机真实存在的字体名。

    直接把整串候选交给 matplotlib 会**逐条打印** findfont 警告（一张图几十行），
    而且它仍然会去试那些不存在的名字。先过滤一遍，噪声与解析都干净。
    """
    key = tuple(fams)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    try:
        from matplotlib import font_manager
        avail = {f.name for f in font_manager.fontManager.ttflist}
    except Exception:                                      # noqa: BLE001
        avail = set()
    keep = [f for f in fams if f in avail]
    _FONT_CACHE[key] = keep
    return keep


def _dashes(spec: str | None):
    if not spec:
        return None
    return tuple(float(v) for v in spec.replace(",", " ").split())


def _line_kw(op, gray, default="#000") -> dict:
    """Line2D 的参数。dashes 为 None 时**不能传**——传 None 会让 set_dashes 崩。"""
    kw = dict(color=_color(op.get("stroke"), gray, default), linewidth=op["sw"])
    d = _dashes(op.get("dash"))
    if d:
        kw["dashes"] = d
    return kw


def _gray(hexcolor: str) -> str:
    """把颜色换成同等亮度的灰。用于 --gray：确认黑白印刷时仍能分辨。"""
    c = hexcolor.lstrip("#")
    if len(c) != 6:
        return hexcolor
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    y = round(0.299 * r + 0.587 * g + 0.114 * b)
    return f"#{y:02x}{y:02x}{y:02x}"


def _color(c: str | None, gray: bool, default="none"):
    if c is None:
        return default
    if c == "none":
        return "none"
    return _gray(c) if gray else c


def font_report(svg) -> list[str]:
    """报告字体解析结果与缺字情况。

    这是「如实交代」的一半：找不到 Times New Roman 时不能假装用了它，
    中文缺字更要提前说——印出来是方框，事后无法补救。
    """
    try:
        from matplotlib import font_manager
    except ImportError:                                   # pragma: no cover
        return []

    notes: list[str] = []
    seen: dict[tuple, str] = {}
    for op in svg.ops:
        if op["op"] != "text" or not op["s"].strip():
            continue
        fams = _families(op.get("family") or svg.font)
        key = tuple(fams)
        if key in seen:
            continue
        seen[key] = op["s"]
    for fams, sample in seen.items():
        want = fams[0] if fams else "(默认)"
        try:
            path = font_manager.findfont(
                font_manager.FontProperties(family=list(fams)),
                fallback_to_default=False)
        except Exception:                                  # noqa: BLE001
            path = font_manager.findfont(font_manager.FontProperties())
            got = Path(path).stem
            notes.append(f"字体 {want} 本机没有，已用 {got} 替代；"
                         "出版前应在装了指定字体的机器上重新导出")
        try:
            from matplotlib.ft2font import FT2Font
            cmap = FT2Font(path).get_charmap()
        except Exception:                                  # noqa: BLE001
            continue
        missing = sorted({ch for ch in sample if ch not in " \n" and ord(ch) not in cmap})
        if missing:
            notes.append(f"字体 {Path(path).stem} 缺少这些字符：{''.join(missing[:12])}"
                         "——印出来会是方框，请换用含中文字形的字体")
    return notes


def render(svg, dpi: int = DPI_DEFAULT, gray: bool = False):
    """把 `Svg.ops` 画到一张 matplotlib 图上。返回 (fig, 提示)。"""
    try:
        import matplotlib
        matplotlib.use("Agg")
        import logging
        logging.getLogger("matplotlib.font_manager").setLevel(logging.ERROR)
        # 默认 pdf.fonttype=3，matplotlib 会把字体嵌成 **Type 3 位图字体**，
        # 多数期刊直接拒收。42 = TrueType 子集嵌入，这是投稿件该用的值。
        matplotlib.rcParams["pdf.fonttype"] = 42
        matplotlib.rcParams["ps.fonttype"] = 42
        import matplotlib.pyplot as plt
        from matplotlib.lines import Line2D
        from matplotlib.patches import Circle, Ellipse, Polygon, Rectangle
    except ImportError:
        raise SystemExit(
            "导出 PDF/PNG/TIFF 需要 matplotlib：\n"
            "    pip install matplotlib\n"
            "不装也能用：SVG 由内置渲染器直接产出，任何浏览器/Illustrator 都能打开。")

    fig = plt.figure(figsize=(svg.w / 72.0, svg.h / 72.0), dpi=dpi)
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, svg.w)
    ax.set_ylim(svg.h, 0)          # 与 SVG 一致：y 向下
    ax.axis("off")
    fig.patch.set_facecolor("white")

    for op in svg.ops:
        kind = op["op"]
        if kind == "text":
            fams = _resolve(_families(op.get("family") or svg.font))
            kw = dict(fontsize=op["size"], color=_color(op["fill"], gray, "#000"),
                      ha={"start": "left", "middle": "center", "end": "right"}[op["anchor"]],
                      va="baseline", fontstyle=op["style"])
            if fams:
                kw["family"] = fams
            if op["weight"] != "normal":
                kw["fontweight"] = op["weight"]
            if op.get("opacity") is not None:
                kw["alpha"] = op["opacity"]
            if op.get("rotate"):
                # SVG 的 rotate 在 y 向下时是顺时针为正，matplotlib 是逆时针为正
                kw["rotation"] = -op["rotate"]
                kw["rotation_mode"] = "anchor"
            ax.text(op["x"], op["y"], op["s"], **kw)

        elif kind == "line":
            ax.add_line(Line2D([op["x1"], op["x2"]], [op["y1"], op["y2"]],
                               solid_capstyle="butt", **_line_kw(op, gray)))

        elif kind == "arrow":
            x1, y1, x2, y2 = op["x1"], op["y1"], op["x2"], op["y2"]
            ax.add_line(Line2D([x1, x2], [y1, y2], solid_capstyle="butt",
                               **_line_kw({"stroke": "#000", "sw": op["sw"],
                                           "dash": op["dash"]}, gray)))
            dx, dy = x2 - x1, y2 - y1
            d = math.hypot(dx, dy)
            if d < 1e-9:
                continue
            ux, uy = dx / d, dy / d
            bx, by = x2 - ux * ARROW_LEN, y2 - uy * ARROW_LEN
            tip = [(x2, y2), (bx - uy * ARROW_HALF, by + ux * ARROW_HALF),
                   (bx + uy * ARROW_HALF, by - ux * ARROW_HALF)]
            filled = op.get("kind", "arrow") == "arrow"
            ax.add_patch(Polygon(tip, closed=True,
                                 facecolor="#000" if filled else "none",
                                 edgecolor="#000", linewidth=0.8,
                                 joinstyle="round"))

        elif kind == "rect":
            ax.add_patch(Rectangle((op["x"], op["y"]), op["w"], op["h"],
                                   facecolor=_color(op["fill"], gray),
                                   edgecolor=_color(op["stroke"], gray),
                                   linewidth=op["sw"], linestyle="solid",
                                   alpha=op.get("opacity") if op.get("opacity") is not None else 1.0))
            if op["dash"]:
                ax.patches[-1].set_linestyle((0, _dashes(op["dash"])))

        elif kind == "ellipse":
            ax.add_patch(Ellipse((op["cx"], op["cy"]), 2 * op["rx"], 2 * op["ry"],
                                 facecolor=_color(op["fill"], gray),
                                 edgecolor=_color(op["stroke"], gray),
                                 linewidth=op["sw"]))
            if op["dash"]:
                ax.patches[-1].set_linestyle((0, _dashes(op["dash"])))

        elif kind == "circle":
            ax.add_patch(Circle((op["cx"], op["cy"]), op["r"],
                                facecolor=_color(op["fill"], gray),
                                edgecolor=_color(op["stroke"], gray),
                                linewidth=op["sw"]))

        elif kind == "polygon":
            ax.add_patch(Polygon(op["pts"], closed=True,
                                 facecolor=_color(op["fill"], gray),
                                 edgecolor=_color(op["stroke"], gray),
                                 linewidth=op["sw"],
                                 alpha=op.get("opacity") if op.get("opacity") is not None else 1.0))

        elif kind == "polyline":
            xs = [p[0] for p in op["pts"]]
            ys = [p[1] for p in op["pts"]]
            ax.add_line(Line2D(xs, ys, solid_joinstyle="round",
                               solid_capstyle="round", **_line_kw(op, gray)))

    return fig, font_report(svg)


def save_all(fig, base, formats=("pdf", "png"), dpi: int = DPI_DEFAULT):
    """按后缀保存。返回 (文件列表, 提示列表)。"""
    base = Path(base)
    if base.suffix:
        base = base.with_suffix("")
    files: list[Path] = []
    notes: list[str] = []
    for fmt in formats:
        fmt = fmt.lower().strip()
        if fmt in ("svg", "svgz"):
            notes.append("SVG 由内置渲染器直接产出，不经 matplotlib；"
                         "需要时用同一次运行输出的 .svg 文件")
            continue
        out = base.with_suffix(f".{fmt}")
        try:
            fig.savefig(out, format=fmt, dpi=dpi, facecolor="white",
                        edgecolor="none", transparent=False)
            if fmt == "png":
                notes += _flatten_png(out, dpi)
            files.append(out)
        except Exception as e:                             # noqa: BLE001
            if fmt in ("tif", "tiff"):
                notes.append("TIFF 需要 Pillow：pip install pillow（其余格式不受影响）")
            else:
                notes.append(f"{fmt} 导出失败：{type(e).__name__}: {e}")
    if files:
        notes.append(f"位图分辨率 {dpi} dpi；PDF 为矢量（字体已嵌入）")
    return files, notes


def _flatten_png(path: Path, dpi: int) -> list[str]:
    """把 RGBA 的 PNG 压成 RGB。

    matplotlib 即使 `transparent=False` 也照写 alpha 通道（只是全不透明），
    而投稿系统常按「带透明通道」拒收。用 Pillow 转一次 RGB 并写回 DPI 元数据。
    """
    try:
        from PIL import Image
    except ImportError:
        return ["PNG 仍带 alpha 通道：装 Pillow 可自动转 RGB（pip install pillow）"]
    with Image.open(path) as im:
        if im.mode == "RGB":
            return []
        im.convert("RGB").save(path, format="PNG", dpi=(dpi, dpi))
    return []


def summarize(files, notes) -> None:
    for f in files:
        print(f"  导出 {f}")
    for n in notes:
        print(f"  ! {n}")
