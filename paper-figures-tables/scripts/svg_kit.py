"""零依赖 SVG 绘图基元。单位统一为磅（pt），1 in = 72 pt。

为什么默认不用 matplotlib：本技能的目标是「装不上任何东西也能出印刷级矢量图」。
SVG 是文本，可 diff、可手改，任何期刊系统、Word、Illustrator、Inkscape 都能转 PDF/EPS。
代价是坐标要自己算——但学术图表的类型有限，模板化之后并不难。

**但同一个 Svg 对象会同时记录一份图元清单（`ops`）**，供 `mpl_backend.py`
用 matplotlib 重画成 PDF/PNG/TIFF。布局只算一次，两个渲染器共用同一批坐标，
所以 SVG 与 PDF 的几何必然一致——不会出现「两份实现各自漂移」。
matplotlib 是可选依赖：没装时 SVG 照常出，只是导不出位图与 PDF。
"""
from __future__ import annotations

import math
from pathlib import Path

PT_PER_INCH = 72.0

# 西文在前、中文在后：浏览器与 Inkscape 都按这个顺序回退。
# 中文期刊要宋体 → 用 SERIF；APA 图表多用无衬线 → 用 SANS。
SERIF = "'Times New Roman', 'SimSun', 'Songti SC', 'Noto Serif CJK SC', serif"
SANS = "'Arial', 'Helvetica', 'Microsoft YaHei', 'PingFang SC', 'Noto Sans CJK SC', sans-serif"

# APA 7 图幅：整幅 6.5 in，半幅 3.25 in
FULL_WIDTH = 6.5 * PT_PER_INCH
HALF_WIDTH = 3.25 * PT_PER_INCH


def esc(s: object) -> str:
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
            .replace('"', "&quot;"))


def n(v: float) -> str:
    """数字格式化：最多三位小数，去掉尾随零。"""
    s = f"{float(v):.3f}".rstrip("0").rstrip(".")
    return s if s not in ("", "-0") else "0"


def text_width(s: str, size: float) -> float:
    """粗略估算文本宽度：中日韩字符按 1 em，其余按 0.55 em。"""
    w = 0.0
    for ch in s:
        w += size * (1.0 if ord(ch) > 0x2E7F else 0.55)
    return w


def wrap(s: str, max_width: float, size: float) -> list[str]:
    """按估算宽度折行。中文逐字断，英文按词断。"""
    if text_width(s, size) <= max_width:
        return [s]
    lines, cur = [], ""
    for token in _tokens(s):
        trial = cur + token
        if cur and text_width(trial, size) > max_width:
            lines.append(cur.rstrip())
            cur = token.lstrip()
        else:
            cur = trial
    if cur.strip():
        lines.append(cur.rstrip())
    return lines or [s]


def _tokens(s: str) -> list[str]:
    """中文单字成 token，英文按空格切。"""
    out, buf = [], ""
    for ch in s:
        if ord(ch) > 0x2E7F:
            if buf:
                out.append(buf)
                buf = ""
            out.append(ch)
        elif ch == " ":
            buf += ch
            out.append(buf)
            buf = ""
        else:
            buf += ch
    if buf:
        out.append(buf)
    return out


class Svg:
    """一个 SVG 画布。所有坐标与尺寸都用 pt。"""

    def __init__(self, width: float, height: float, font: str = SANS):
        self.w, self.h, self.font = float(width), float(height), font
        self._body: list[str] = []
        self._need: set[str] = set()
        self.ops: list[dict] = []      # 供 matplotlib 后端重画用

    # ---------- 内部 ----------
    def _marker(self, kind: str) -> str:
        """箭头标记。kind: arrow / arrow_open / arrow_dash"""
        mid = {"arrow": "ar", "arrow_open": "aro", "arrow_dash": "ard"}[kind]
        if mid not in self._need:
            self._need.add(mid)
            fill = "#000" if kind == "arrow" else "none"
            self._defs_extra = getattr(self, "_defs_extra", [])
            self._defs_extra.append(
                f'<marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
                f'markerWidth="6" markerHeight="6" orient="auto-start-reverse" '
                f'markerUnits="userSpaceOnUse">'
                f'<path d="M0.5,1.2 L9,5 L0.5,8.8{" Z" if kind == "arrow" else ""}" '
                f'fill="{fill}" stroke="#000" stroke-width="0.8" '
                f'stroke-linejoin="round"/></marker>')
        return mid

    # ---------- 图元 ----------
    def text(self, x, y, s, size=9, anchor="start", weight="normal", style="normal",
             fill="#000", family=None, opacity=None, rotate=None):
        extra = ""
        if rotate:
            extra += f' transform="rotate({n(rotate)} {n(x)} {n(y)})"'
        if weight != "normal":
            extra += f' font-weight="{weight}"'
        if style != "normal":
            extra += f' font-style="{style}"'
        if family:
            extra += f' font-family="{family}"'
        if opacity is not None:
            extra += f' fill-opacity="{n(opacity)}"'
        self._body.append(
            f'<text x="{n(x)}" y="{n(y)}" font-size="{n(size)}" '
            f'text-anchor="{anchor}" fill="{fill}"{extra}>{esc(s)}</text>')
        self.ops.append({"op": "text", "x": float(x), "y": float(y), "s": str(s),
                         "size": float(size), "anchor": anchor, "weight": weight,
                         "style": style, "fill": fill, "family": family,
                         "opacity": opacity, "rotate": rotate})

    def text_c(self, x, cy, s, size=9, **kw):
        """以 (x, cy) 为视觉中心放一行字。不用 dominant-baseline，兼容性更稳。"""
        kw.setdefault("anchor", "middle")
        self.text(x, cy + size * 0.35, s, size, **kw)

    def block(self, x, cy, lines, size=9, leading=1.25, **kw):
        """多行文本，整体在 cy 上垂直居中。"""
        if not lines:
            return
        step = size * leading
        top = cy - (len(lines) - 1) * step / 2
        for i, line in enumerate(lines):
            self.text_c(x, top + i * step, line, size, **kw)

    def rect(self, x, y, w, h, rx=0, fill="none", stroke="#000", sw=0.75,
             dash=None, opacity=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        o = f' fill-opacity="{n(opacity)}"' if opacity is not None else ""
        self._body.append(
            f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{n(h)}" '
            f'rx="{n(rx)}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{n(sw)}"{d}{o}/>')
        self.ops.append({"op": "rect", "x": float(x), "y": float(y), "w": float(w),
                         "h": float(h), "rx": float(rx), "fill": fill, "stroke": stroke,
                         "sw": float(sw), "dash": dash, "opacity": opacity})

    def ellipse(self, cx, cy, rx, ry, fill="none", stroke="#000", sw=0.75, dash=None):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._body.append(
            f'<ellipse cx="{n(cx)}" cy="{n(cy)}" rx="{n(rx)}" ry="{n(ry)}" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="{n(sw)}"{d}/>')
        self.ops.append({"op": "ellipse", "cx": float(cx), "cy": float(cy),
                         "rx": float(rx), "ry": float(ry), "fill": fill,
                         "stroke": stroke, "sw": float(sw), "dash": dash})

    def line(self, x1, y1, x2, y2, sw=0.75, dash=None, stroke="#000"):
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._body.append(
            f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" '
            f'stroke="{stroke}" stroke-width="{n(sw)}"{d}/>')
        self.ops.append({"op": "line", "x1": float(x1), "y1": float(y1),
                         "x2": float(x2), "y2": float(y2), "sw": float(sw),
                         "dash": dash, "stroke": stroke})

    def arrow(self, x1, y1, x2, y2, sw=0.75, kind="arrow", dash=None, both=False):
        """画带箭头的线。both=True 时两端都有箭头（相关/协方差）。

        双向箭头用两条方向相反、坐标完全重合的线实现，而不是 marker-start：
        后者要依赖 SVG 2 的 orient="auto-start-reverse"，Illustrator 等
        印刷流程里的工具不一定认，两条线则任何渲染器都对。
        """
        d = f' stroke-dasharray="{dash}"' if dash else ""
        mid = self._marker(kind)
        self._body.append(
            f'<line x1="{n(x1)}" y1="{n(y1)}" x2="{n(x2)}" y2="{n(y2)}" '
            f'stroke="#000" stroke-width="{n(sw)}"{d} marker-end="url(#{mid})"/>')
        self.ops.append({"op": "arrow", "x1": float(x1), "y1": float(y1),
                         "x2": float(x2), "y2": float(y2), "sw": float(sw),
                         "dash": dash, "kind": kind})
        if both:
            self._body.append(
                f'<line x1="{n(x2)}" y1="{n(y2)}" x2="{n(x1)}" y2="{n(y1)}" '
                f'stroke="#000" stroke-width="{n(sw)}"{d} marker-end="url(#{mid})"/>')
            self.ops.append({"op": "arrow", "x1": float(x2), "y1": float(y2),
                             "x2": float(x1), "y2": float(y1), "sw": float(sw),
                             "dash": dash, "kind": kind})

    def polyline(self, pts, sw=1.0, fill="none", stroke="#000", dash=None):
        p = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self._body.append(
            f'<polyline points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{n(sw)}" stroke-linejoin="round" stroke-linecap="round"{d}/>')
        self.ops.append({"op": "polyline", "pts": [(float(x), float(y)) for x, y in pts],
                         "sw": float(sw), "fill": fill, "stroke": stroke, "dash": dash})

    def polygon(self, pts, fill="#000", stroke="none", sw=0.0, opacity=None):
        p = " ".join(f"{n(x)},{n(y)}" for x, y in pts)
        o = f' fill-opacity="{n(opacity)}"' if opacity is not None else ""
        self._body.append(
            f'<polygon points="{p}" fill="{fill}" stroke="{stroke}" '
            f'stroke-width="{n(sw)}"{o}/>')
        self.ops.append({"op": "polygon", "pts": [(float(x), float(y)) for x, y in pts],
                         "fill": fill, "stroke": stroke, "sw": float(sw),
                         "opacity": opacity})

    def circle(self, cx, cy, r, fill="#000", stroke="none", sw=0.75):
        self._body.append(
            f'<circle cx="{n(cx)}" cy="{n(cy)}" r="{n(r)}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="{n(sw)}"/>')
        self.ops.append({"op": "circle", "cx": float(cx), "cy": float(cy),
                         "r": float(r), "fill": fill, "stroke": stroke, "sw": float(sw)})

    # ---------- 复合 ----------
    def replay(self, ops, dx: float = 0.0, dy: float = 0.0, scale: float = 1.0):
        """把另一张图的图元按「平移 + 等比缩放」重画到本图上。

        走这里而不是把 SVG 文本塞进 `<g transform>`：文本塞进去，`ops` 仍是空的，
        用 matplotlib 重画 PDF 时就什么都没有——导出的 PDF 会是一片空白，
        而 SVG 看起来完全正常。
        """
        def X(v):
            return dx + float(v) * scale

        def Y(v):
            return dy + float(v) * scale

        def L(v):
            return float(v) * scale

        def dash(d):
            if not d:
                return None
            return " ".join(n(float(p) * scale)
                            for p in str(d).replace(",", " ").split())

        for op in ops:
            k = op["op"]
            if k == "text":
                self.text(X(op["x"]), Y(op["y"]), op["s"], L(op["size"]),
                          anchor=op["anchor"], weight=op["weight"],
                          style=op["style"], fill=op["fill"],
                          family=op["family"], opacity=op["opacity"],
                          rotate=op.get("rotate"))
            elif k == "line":
                self.line(X(op["x1"]), Y(op["y1"]), X(op["x2"]), Y(op["y2"]),
                          sw=L(op["sw"]), dash=dash(op["dash"]),
                          stroke=op["stroke"])
            elif k == "arrow":
                self.arrow(X(op["x1"]), Y(op["y1"]), X(op["x2"]), Y(op["y2"]),
                           sw=L(op["sw"]), kind=op.get("kind", "arrow"),
                           dash=dash(op["dash"]))
            elif k == "rect":
                self.rect(X(op["x"]), Y(op["y"]), L(op["w"]), L(op["h"]),
                          rx=L(op["rx"]), fill=op["fill"], stroke=op["stroke"],
                          sw=L(op["sw"]), dash=dash(op["dash"]),
                          opacity=op["opacity"])
            elif k == "circle":
                self.circle(X(op["cx"]), Y(op["cy"]), L(op["r"]),
                            fill=op["fill"], stroke=op["stroke"], sw=L(op["sw"]))
            elif k == "ellipse":
                self.ellipse(X(op["cx"]), Y(op["cy"]), L(op["rx"]), L(op["ry"]),
                             fill=op["fill"], stroke=op["stroke"], sw=L(op["sw"]),
                             dash=dash(op["dash"]))
            elif k == "polyline":
                self.polyline([(X(a), Y(b)) for a, b in op["pts"]], sw=L(op["sw"]),
                              fill=op["fill"], stroke=op["stroke"],
                              dash=dash(op["dash"]))
            elif k == "polygon":
                self.polygon([(X(a), Y(b)) for a, b in op["pts"]],
                             fill=op["fill"], stroke=op["stroke"],
                             sw=L(op["sw"]), opacity=op["opacity"])
            else:
                raise SystemExit(f"replay 不认识图元 {k!r}")

    def axes(self, x0, y0, x1, y1, xticks, yticks, size=8.5,
             xlabel="", ylabel="", xfmt=None, yfmt=None, tick_len=2.5):
        """只画左轴与下轴（APA 不要上/右边框，也不要网格线）。

        (x0, y0) 是左下角，(x1, y1) 是右上角。
        xticks / yticks 是 [(数值位置, 标签)] 或 [数值位置]。

        **刻度与刻度文字一律画在轴的外侧。** SVG 的 y 轴向下，所以下轴的刻度
        要往 y0 的**下方**（坐标变大）画。原实现写成了 `y0 - …`，整排刻度数字
        落在绘图区里，轴标题压在数据上——缩略图上看不出来，印出来就压线。
        """
        self.line(x0, y0, x1, y0, sw=0.75)          # x 轴
        self.line(x0, y0, x0, y1, sw=0.75)          # y 轴
        for t in xticks:
            pos, lab = t if isinstance(t, (tuple, list)) else (t, (xfmt or n)(t))
            self.line(pos, y0, pos, y0 + tick_len, sw=0.75)
            self.text_c(pos, y0 + tick_len + size * 0.85, lab, size)
        for t in yticks:
            pos, lab = t if isinstance(t, (tuple, list)) else (t, (yfmt or n)(t))
            self.line(x0, pos, x0 - tick_len, pos, sw=0.75)
            self.text(x0 - tick_len - 2, pos + size * 0.35, lab, size, anchor="end")
        if xlabel:
            self.text_c((x0 + x1) / 2, y0 + tick_len + size * 2.6, xlabel, size + 0.5)
        if ylabel:
            self.text(x0 - 34, (y0 + y1) / 2, ylabel, size + 0.5,
                      anchor="middle", rotate=-90)

    # ---------- 输出 ----------
    def save(self, path: str | Path) -> Path:
        path = Path(path)
        defs = ""
        if getattr(self, "_defs_extra", None):
            defs = "<defs>" + "".join(self._defs_extra) + "</defs>"
        doc = (
            f'<svg xmlns="http://www.w3.org/2000/svg" '
            f'width="{n(self.w)}pt" height="{n(self.h)}pt" '
            f'viewBox="0 0 {n(self.w)} {n(self.h)}" '
            f'font-family="{self.font}">\n'
            f'<rect x="0" y="0" width="{n(self.w)}" height="{n(self.h)}" fill="#fff"/>\n'
            f'{defs}\n' + "\n".join(self._body) + "\n</svg>\n")
        path.write_text(doc, encoding="utf-8", newline="\n")
        return path

    def export(self, base: str | Path, formats=("pdf", "png"), dpi: int = 600,
               gray: bool = False) -> tuple[list[Path], list[str]]:
        """用 matplotlib 把同一批图元导出成 PDF / PNG / TIFF。

        返回 (写出的文件, 提示)。没有 matplotlib 时抛 SystemExit 并说明怎么装——
        不静默降级成「只出了 SVG 但没说」。
        """
        from mpl_backend import render, save_all
        fig, notes = render(self, dpi=dpi, gray=gray)
        files, more = save_all(fig, base, formats, dpi=dpi)
        return files, notes + more


def nice_ticks(lo: float, hi: float, target: int = 5) -> list[float]:
    """给一段区间挑好看的刻度值（1/2/5 × 10^k 步长）。"""
    if hi <= lo:
        return [lo]
    raw = (hi - lo) / max(target, 1)
    mag = 10 ** math.floor(math.log10(raw)) if raw > 0 else 1
    for mult in (1, 2, 2.5, 5, 10):
        step = mag * mult
        if step >= raw:
            break
    start = math.ceil(lo / step) * step
    out, v = [], start
    while v <= hi + step * 1e-9:
        out.append(round(v, 10))
        v += step
    return out


def clip_to_box(cx, cy, w, h, tx, ty):
    """从节点中心 (cx,cy) 指向 (tx,ty) 的射线与矩形边界的交点。

    用于让箭头正好停在方框边缘，而不是扎进框里。
    """
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    hw, hh = w / 2, h / 2
    scale = min(hw / abs(dx) if dx else float("inf"),
                hh / abs(dy) if dy else float("inf"))
    return cx + dx * scale, cy + dy * scale


def clip_to_ellipse(cx, cy, rx, ry, tx, ty):
    """射线与椭圆边界的交点。"""
    dx, dy = tx - cx, ty - cy
    if dx == 0 and dy == 0:
        return cx, cy
    denom = math.sqrt((dx / rx) ** 2 + (dy / ry) ** 2)
    return cx + dx / denom, cy + dy / denom
