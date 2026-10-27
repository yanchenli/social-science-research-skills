"""把 SVG 读回图元清单（ops）。

为什么需要这个：`make_panel` 合成多面板图时，原先是把各面板的 SVG **文本**直接
塞进 `<g transform=…>`。SVG 显示没问题，但 `svg.ops` 是空的——用 matplotlib
重画 PDF 时没有任何图元，导出的 PDF 只剩 (a)(b) 两个标签，页面上是一片空白。

所以合成必须走「读回图元 → 用同一套绘制方法重画」，让 SVG 与 ops 始终是同一份。
"""
from __future__ import annotations

import re
from xml.etree import ElementTree as ET

NS = "{http://www.w3.org/2000/svg}"
MARKER_KIND = {"ar": "arrow", "aro": "arrow_open", "ard": "arrow_dash"}


def _f(el, name, default=0.0) -> float:
    v = el.get(name)
    if v is None:
        return default
    m = re.match(r"-?[\d.]+", str(v))
    return float(m.group(0)) if m else default


def _points(s: str) -> list[tuple[float, float]]:
    nums = [float(x) for x in re.findall(r"-?[\d.]+", s or "")]
    return list(zip(nums[0::2], nums[1::2]))


def _rotate(el):
    tr = el.get("transform") or ""
    m = re.search(r"rotate\(\s*(-?[\d.]+)\s+(-?[\d.]+)\s+(-?[\d.]+)\s*\)", tr)
    return float(m.group(1)) if m else None


def parse_ops(text: str) -> tuple[list[dict], list[str]]:
    """返回 (ops, 未识别的标签名)。未识别不是错误，但调用方应当知道。"""
    root = ET.fromstring(text)
    ops: list[dict] = []
    unknown: list[str] = []

    for el in root.iter():
        tag = el.tag.replace(NS, "")
        if tag in ("svg", "defs", "marker", "g", "title", "path"):
            # path 只出现在 <marker> 的箭头里（正文我们不用 path），跳过
            continue
        if tag == "text":
            # 只取直属文本，忽略 tspan 嵌套（我们不用）
            s = "".join(el.itertext())
            if s == "":
                continue
            ops.append({
                "op": "text", "x": _f(el, "x"), "y": _f(el, "y"), "s": s,
                "size": _f(el, "font-size", 9.0),
                "anchor": el.get("text-anchor", "start"),
                "weight": el.get("font-weight", "normal"),
                "style": el.get("font-style", "normal"),
                "fill": el.get("fill", "#000"),
                "family": el.get("font-family"),
                "opacity": (float(el.get("fill-opacity"))
                            if el.get("fill-opacity") else None),
                "rotate": _rotate(el),
            })
        elif tag == "line":
            me = el.get("marker-end") or ""
            mid = re.search(r"#(\w+)", me)
            if mid and mid.group(1) in MARKER_KIND:
                ops.append({"op": "arrow", "x1": _f(el, "x1"), "y1": _f(el, "y1"),
                            "x2": _f(el, "x2"), "y2": _f(el, "y2"),
                            "sw": _f(el, "stroke-width", 0.75),
                            "dash": el.get("stroke-dasharray"),
                            "kind": MARKER_KIND[mid.group(1)]})
            else:
                ops.append({"op": "line", "x1": _f(el, "x1"), "y1": _f(el, "y1"),
                            "x2": _f(el, "x2"), "y2": _f(el, "y2"),
                            "sw": _f(el, "stroke-width", 0.75),
                            "dash": el.get("stroke-dasharray"),
                            "stroke": el.get("stroke", "none")})
        elif tag == "polyline":
            ops.append({"op": "polyline", "pts": _points(el.get("points")),
                        "sw": _f(el, "stroke-width", 1.0),
                        "fill": el.get("fill", "none"),
                        "stroke": el.get("stroke", "none"),
                        "dash": el.get("stroke-dasharray")})
        elif tag == "polygon":
            ops.append({"op": "polygon", "pts": _points(el.get("points")),
                        "fill": el.get("fill", "#000"),
                        "stroke": el.get("stroke", "none"),
                        "sw": _f(el, "stroke-width", 0.0),
                        "opacity": (float(el.get("fill-opacity"))
                                    if el.get("fill-opacity") else None)})
        elif tag == "rect":
            ops.append({"op": "rect", "x": _f(el, "x"), "y": _f(el, "y"),
                        "w": _f(el, "width"), "h": _f(el, "height"),
                        "rx": _f(el, "rx"), "fill": el.get("fill", "none"),
                        "stroke": el.get("stroke", "none"),
                        "sw": _f(el, "stroke-width", 0.75),
                        "dash": el.get("stroke-dasharray"),
                        "opacity": (float(el.get("fill-opacity"))
                                    if el.get("fill-opacity") else None)})
        elif tag == "circle":
            ops.append({"op": "circle", "cx": _f(el, "cx"), "cy": _f(el, "cy"),
                        "r": _f(el, "r"), "fill": el.get("fill", "#000"),
                        "stroke": el.get("stroke", "none"),
                        "sw": _f(el, "stroke-width", 0.75)})
        elif tag == "ellipse":
            ops.append({"op": "ellipse", "cx": _f(el, "cx"), "cy": _f(el, "cy"),
                        "rx": _f(el, "rx"), "ry": _f(el, "ry"),
                        "fill": el.get("fill", "none"),
                        "stroke": el.get("stroke", "none"),
                        "sw": _f(el, "stroke-width", 0.75),
                        "dash": el.get("stroke-dasharray")})
        else:
            unknown.append(tag)

    return ops, sorted(set(unknown))
