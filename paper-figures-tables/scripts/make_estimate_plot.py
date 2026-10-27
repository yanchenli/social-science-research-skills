"""组间均值 / 系数图（点图 + 误差棒，SVG，零依赖）。

这是「结果图表」里最常缺的一类：几组的均值、几个系数、几条路径，
各带 95% 置信区间。默认画**点图**而不是柱状图，理由是方法性的：

  - 柱状图必须从 0 起，组间差异被压成柱顶的一小截，读者看不见；
  - 柱子的面积会让人以为「两倍高 = 两倍多」，而均值的零点常常没有意义；
  - 点图 + 误差棒把「估计值」和「不确定性」放在同一个视觉层级上，
    读者一眼能判断两组区间是否重叠。

APA 7 与多数期刊的图表指南都倾向点估计图。要柱状图也能画（`"style": "bar"`），
但那是作者的选择，不是默认。

两种输入
--------
1) 汇总值（已知均值与区间）：

       python make_estimate_plot.py spec.json out.svg

   spec.json::

       {
         "lang": "en",
         "xlabel": "Mean purchase intention (95% CI)",
         "style": "dot",
         "refline": 3.0,
         "refline_label": "Scale midpoint",
         "series": [
           {"label": "High trust",
            "points": [
              {"label": "Brand A", "est": 4.21, "lo": 3.98, "hi": 4.44, "sig": "**"},
              {"label": "Brand B", "est": 3.80, "lo": 3.55, "hi": 4.05}
            ]}
         ],
         "note": "Error bars are 95% CIs."
       }

2) 原始数据（按分组算均值与 95% CI，t 分布精确分位数）：

       python make_estimate_plot.py out.svg --data d.csv --dv y --by cond

   加 `--by2 series` 可画分组点图（如实验组 / 控制组并排）。

**不编造区间**：只给 `est` 不给 `lo`/`hi` 时不会替你估一个误差棒，
而是报错——误差棒的长度是结论的一部分，不能由绘图脚本猜。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svg_kit import FULL_WIDTH, SANS, SERIF, Svg, nice_ticks, n, text_width, wrap
# 本文件已有一个 summarize()（从 CSV 汇总均值），所以这里改名，避免覆盖
from mpl_backend import summarize as print_exports

FS = 8.5
ROW_H = 20.0
PAD_T = 12.0
TICK = 3.0
CAP = 3.2          # 误差棒端帽的半长
R_MARK = 2.9       # 点半径
MARKERS = ("circle", "square", "triangle", "diamond")
STYLES = ("dot", "bar")
ORIENT = ("horizontal", "vertical")

TOP_KEYS = {"lang", "title", "xlabel", "ylabel", "orientation", "style",
            "refline", "refline_label", "series", "note", "width", "height"}
SERIES_KEYS = {"label", "points"}
POINT_KEYS = {"label", "est", "lo", "hi", "n", "sig"}


# ---------------------------------------------------------------- t 分位数
# 95% CI 的正确写法是 mean ± t(.975, n−1)·SE。n 小的时候 1.96 会低估区间，
# 而学生数据常常只有二三十人。这里用不完全 Beta 函数算精确分位数，
# 不引入 scipy。
def _betacf(a: float, b: float, x: float) -> float:
    """不完全 Beta 函数的连分式（Lentz 算法）。"""
    maxit, eps, fpmin = 200, 3e-16, 1e-300
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c, d = 1.0, 1.0 - qab * x / qap
    if abs(d) < fpmin:
        d = fpmin
    d = 1.0 / d
    h = d
    for m in range(1, maxit + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        d = fpmin if abs(d) < fpmin else d
        c = 1.0 + aa / c
        c = fpmin if abs(c) < fpmin else c
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        d = fpmin if abs(d) < fpmin else d
        c = 1.0 + aa / c
        c = fpmin if abs(c) < fpmin else c
        d = 1.0 / d
        delta = d * c
        h *= delta
        if abs(delta - 1.0) < eps:
            break
    return h


def _betai(a: float, b: float, x: float) -> float:
    """正则化不完全 Beta 函数 I_x(a, b)。"""
    if x <= 0.0:
        return 0.0
    if x >= 1.0:
        return 1.0
    bt = math.exp(math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
                  + a * math.log(x) + b * math.log(1.0 - x))
    if x < (a + 1.0) / (a + b + 2.0):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1.0 - x) / b


def t_cdf(t: float, df: float) -> float:
    x = df / (df + t * t)
    p = 0.5 * _betai(df / 2.0, 0.5, x)
    return 1.0 - p if t > 0 else p


def t_crit(df: float, conf: float = 0.95) -> float:
    """双侧 t 分位数 t_{(1+conf)/2, df}。二分求解，df 可为非整数。"""
    if df <= 0:
        raise ValueError("自由度必须为正")
    target = 1.0 - (1.0 - conf) / 2.0
    lo, hi = 0.0, 1.0
    while t_cdf(hi, df) < target:
        hi *= 2.0
        if hi > 1e7:
            return float("inf")
    for _ in range(120):
        mid = (lo + hi) / 2.0
        if t_cdf(mid, df) < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


# ---------------------------------------------------------------- 汇总
def _mean(v):
    return sum(v) / len(v)


def _sd(v):
    mu = _mean(v)
    return math.sqrt(sum((a - mu) ** 2 for a in v) / (len(v) - 1))


def summarize(df: dict, dv: str, by: str, by2: str | None = None,
              conf: float = 0.95) -> tuple[list, list[str]]:
    """按 `by`（与可选 `by2`）分组，算每组均值与 t 分布 95% CI。"""
    warns: list[str] = []
    cats: list[str] = []
    for v in df[by]:
        if v is None:
            continue
        k = _label(v)
        if k not in cats:
            cats.append(k)

    series_labels = []
    if by2:
        for v in df[by2]:
            if v is not None:
                k = _label(v)
                if k not in series_labels:
                    series_labels.append(k)
    else:
        series_labels = [None]

    out = []
    for sl in series_labels:
        pts = []
        for cat in cats:
            vals = []
            for i in range(len(df[dv])):
                if _label(df[by][i]) != cat:
                    continue
                if sl is not None and _label(df[by2][i]) != sl:
                    continue
                y = df[dv][i]
                if y is not None:
                    vals.append(y)
            if len(vals) < 2:
                warns.append(f"「{cat}」组有效样本只有 {len(vals)} 个，画不出区间，已跳过")
                continue
            mu, sd = _mean(vals), _sd(vals)
            se = sd / math.sqrt(len(vals))
            t = t_crit(len(vals) - 1, conf)
            pts.append({"label": cat, "est": mu, "lo": mu - t * se,
                        "hi": mu + t * se, "n": len(vals)})
        if sl is not None:
            out.append({"label": sl, "points": pts})
        elif pts:
            out.append({"label": "", "points": pts})
    return out, warns


def _label(v) -> str:
    """分组值转标签：4.0 写成 4，不写成 4.0。"""
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


# ---------------------------------------------------------------- 校验
def validate_spec(spec: dict) -> tuple[list[str], list[str]]:
    errs: list[str] = []
    warns: list[str] = []
    unknown = set(spec) - TOP_KEYS
    if unknown:
        errs.append(f"未知的顶层键：{sorted(unknown)}；可用：{sorted(TOP_KEYS)}")
    if spec.get("orientation", "horizontal") not in ORIENT:
        errs.append(f"orientation 只能是 {ORIENT}，收到 {spec.get('orientation')!r}")
    if spec.get("style", "dot") not in STYLES:
        errs.append(f"style 只能是 {STYLES}，收到 {spec.get('style')!r}")

    series = spec.get("series")
    if not isinstance(series, list) or not series:
        errs.append("series 必须是非空列表")
        return errs, warns

    npts = None
    for si, s in enumerate(series):
        if not isinstance(s, dict):
            errs.append(f"series[{si}] 不是对象")
            continue
        unknown = set(s) - SERIES_KEYS
        if unknown:
            errs.append(f"series[{si}] 有未知键 {sorted(unknown)}；可用：{sorted(SERIES_KEYS)}")
        pts = s.get("points")
        if not isinstance(pts, list) or not pts:
            errs.append(f"series[{si}] 的 points 必须是非空列表")
            continue
        if npts is None:
            npts = len(pts)
        elif len(pts) != npts:
            errs.append(f"series[{si}] 有 {len(pts)} 个点，第一组有 {npts} 个——"
                        "各组的类别必须一一对应，否则会错位")
        for pi, p in enumerate(pts):
            where = f"series[{si}].points[{pi}]"
            if not isinstance(p, dict):
                errs.append(f"{where} 不是对象")
                continue
            unknown = set(p) - POINT_KEYS
            if unknown:
                errs.append(f"{where} 有未知键 {sorted(unknown)}；可用：{sorted(POINT_KEYS)}")
            for k in ("est", "lo", "hi"):
                if not isinstance(p.get(k), (int, float)):
                    errs.append(f"{where} 缺数值 `{k}`"
                                + ("（误差棒的长度是结论的一部分，不能由脚本猜）"
                                   if k != "est" else ""))
            if all(isinstance(p.get(k), (int, float)) for k in ("est", "lo", "hi")):
                if not (p["lo"] <= p["est"] <= p["hi"]):
                    errs.append(f"{where} 的区间不包含点估计：lo={p['lo']} "
                                f"est={p['est']} hi={p['hi']}")
                if p["lo"] == p["hi"]:
                    warns.append(f"{where} 的上下界相同，误差棒长度为 0")
    if spec.get("style") == "bar" and spec.get("refline") is None:
        warns.append("style=bar 且没给 refline：柱子将从 0 起。"
                     "若均值的零点没有意义，改用点图（style=dot）")
    return errs, warns


# ---------------------------------------------------------------- 绘图
def _marker(svg: Svg, kind: str, cx: float, cy: float, r: float = R_MARK) -> None:
    """黑白印刷下靠形状区分系列——不用颜色，因为期刊常印黑白。"""
    if kind == "circle":
        svg.circle(cx, cy, r, fill="#000")
    elif kind == "square":
        svg.rect(cx - r * 0.88, cy - r * 0.88, r * 1.76, r * 1.76, fill="#000", sw=0)
    elif kind == "triangle":
        svg.polygon([(cx, cy - r * 1.1), (cx - r * 1.05, cy + r * 0.8),
                     (cx + r * 1.05, cy + r * 0.8)], fill="#000")
    else:  # diamond
        svg.polygon([(cx, cy - r * 1.25), (cx + r * 1.1, cy),
                     (cx, cy + r * 1.25), (cx - r * 1.1, cy)], fill="#000")


def _span(values, extra=None) -> tuple[float, float]:
    lo, hi = min(values), max(values)
    if extra is not None:
        lo, hi = min(lo, extra), max(hi, extra)
    if hi <= lo:
        hi = lo + 1.0
    pad = (hi - lo) * 0.04
    return lo - pad, hi + pad


def build(spec: dict) -> tuple[Svg, list[str]]:
    """画一张估计图。返回 (Svg, 警告列表)。"""
    errs, warns = validate_spec(spec)
    if errs:
        raise SystemExit("规格有问题：\n  - " + "\n  - ".join(errs))

    lang = spec.get("lang", "en")
    series = spec["series"]
    orient = spec.get("orientation", "horizontal")
    style = spec.get("style", "dot")
    cats = [p["label"] for p in series[0]["points"]]
    k = len(series)
    show_legend = k > 1

    ests = [p["est"] for s in series for p in s["points"]]
    los = [p["lo"] for s in series for p in s["points"]]
    his = [p["hi"] for s in series for p in s["points"]]
    ref = spec.get("refline")
    # 柱状图的柱子要从基线起画；若基线（0 或 refline）落在数据范围之外，
    # 柱子会被画到轴外面去。所以画柱时必须把基线纳入定义域。
    base_line = ref if ref is not None else (0.0 if style == "bar" else None)
    v_lo, v_hi = _span(los + his, base_line)

    sig_w = max((text_width(p.get("sig", ""), FS) for s in series for p in s["points"]),
                default=0.0)
    xlabel = spec.get("xlabel", "")
    ylabel = spec.get("ylabel", "")

    if orient == "horizontal":
        return _horizontal(spec, cats, series, k, v_lo, v_hi, ref, sig_w,
                           xlabel, ylabel, style, show_legend, lang, warns)
    return _vertical(spec, cats, series, k, v_lo, v_hi, ref, xlabel, ylabel,
                     style, show_legend, lang, warns)


def _legend(svg: Svg, series, x: float, cy: float, size: float = FS) -> None:
    """一行图例：形状 + 文字。宽度按估算值推进。"""
    cx = x
    for i, s in enumerate(series):
        _marker(svg, MARKERS[i % len(MARKERS)], cx + 3.2, cy)
        svg.text(cx + 9, cy + size * 0.35, s.get("label", ""), size, anchor="start")
        cx += 9 + text_width(s.get("label", ""), size) + 14


def _horizontal(spec, cats, series, k, v_lo, v_hi, ref, sig_w,
                xlabel, ylabel, style, show_legend, lang, warns) -> tuple[Svg, list[str]]:
    fs = FS
    max_lab_w = 150.0
    labels = [wrap(c, max_lab_w, fs) for c in cats]
    lab_w = max(text_width(ln, fs) for lines in labels for ln in lines)
    pad_l = lab_w + 14.0
    pad_r = 14.0 + sig_w
    W = spec.get("width") or FULL_WIDTH
    plot_w = W - pad_l - pad_r
    if plot_w < 140:
        W = pad_l + 140 + pad_r
        plot_w = 140.0
        warns.append(f"标签占宽 {lab_w:.0f} pt，已把画布加宽到 {W/72:.2f} in；"
                     "若超过 6.5 in，请缩短类别标签")
    legend_h = 15.0 if show_legend else 0.0
    ref_lab = spec.get("refline_label") if ref is not None else ""
    # 自上而下的顺序是：参考线标签 → 图例 → 绘图区。三层各有各的高度，
    # 挤在一起就会出现「图例压在参考线标签上」——第二版就踩了这一处。
    ref_h = 11.0 if ref_lab else 0.0
    top = PAD_T + ref_h + legend_h
    plot_h = spec.get("height") or max(len(cats) * ROW_H, 40.0)
    # 表注在画布最底部，轴标题在它上方——两者会撞，所以有表注时要把下方留白加高
    pad_b = 36.0 + (12.0 if spec.get("note") else 0.0)
    H = top + plot_h + pad_b

    svg = Svg(W, H, font=SERIF if lang == "zh" else SANS)
    x0, y0 = pad_l, top + plot_h
    x1, y1 = pad_l + plot_w, top

    def sx(v):
        return x0 + (v - v_lo) / (v_hi - v_lo) * plot_w

    if show_legend:
        _legend(svg, series, 10.0, PAD_T + ref_h + 6.0)

    # 参考线在轴与数据之前画，避免盖住点
    if ref is not None:
        rx = sx(ref)
        svg.line(rx, y0, rx, y1, sw=0.75, dash="3 2")
        if ref_lab:
            # 标签放在绘图区上方的留白里：线两侧都是数据，放哪儿都会压点
            lw = text_width(ref_lab, 8.0)
            if rx + 3 + lw > x1:
                svg.text(rx - 3, PAD_T + 8, ref_lab, 8.0, anchor="end")
            else:
                svg.text(rx + 3, PAD_T + 8, ref_lab, 8.0, anchor="start")

    # 轴：刻度与刻度文字都在轴的外侧（下方）
    svg.line(x0, y0, x1, y0, sw=0.75)
    svg.line(x0, y0, x0, y1, sw=0.75)
    for v in nice_ticks(v_lo, v_hi, 5):
        tx = sx(v)
        svg.line(tx, y0, tx, y0 + TICK, sw=0.75)
        svg.text_c(tx, y0 + TICK + fs * 0.85, n(v), fs)
    if xlabel:
        svg.text_c((x0 + x1) / 2, y0 + TICK + fs * 2.7, xlabel, fs + 0.5)

    row = plot_h / max(len(cats), 1)
    dy = min(5.0, row * 0.45 / k) if k > 1 else 0.0
    bar_h = min(row * 0.62 / k, 9.0)

    for i, lines in enumerate(labels):
        cy = y1 + row * (i + 0.5)
        # 多行标签整体垂直居中，右端对齐到轴
        step = fs * 1.25
        top = cy - (len(lines) - 1) * step / 2
        for j, ln in enumerate(lines):
            svg.text_c(x0 - 7, top + j * step, ln, fs, anchor="end")

    for si, s in enumerate(series):
        off = (si - (k - 1) / 2) * dy
        for i, p in enumerate(s["points"]):
            cy = y1 + row * (i + 0.5) + off
            if style == "bar":
                base = sx(ref) if ref is not None else sx(0.0)
                left, right = sorted((base, sx(p["est"])))
                svg.rect(left, cy - bar_h / 2, max(right - left, 0.4), bar_h,
                         fill="#e6e6e6", sw=0.75)
            svg.line(sx(p["lo"]), cy, sx(p["hi"]), cy, sw=1.0)
            svg.line(sx(p["lo"]), cy - CAP, sx(p["lo"]), cy + CAP, sw=1.0)
            svg.line(sx(p["hi"]), cy - CAP, sx(p["hi"]), cy + CAP, sw=1.0)
            _marker(svg, MARKERS[si % len(MARKERS)], sx(p["est"]), cy)
            if p.get("sig"):
                svg.text(sx(p["hi"]) + 4, cy + fs * 0.35, p["sig"], 8.0, anchor="start")

    if spec.get("note"):
        svg.text(12, H - 9, spec["note"], 8.2)
    return svg, warns


def _vertical(spec, cats, series, k, v_lo, v_hi, ref, xlabel, ylabel,
              style, show_legend, lang, warns) -> tuple[Svg, list[str]]:
    fs = FS
    pad_l = 44.0 + (12.0 if ylabel else 0.0)
    W = spec.get("width") or FULL_WIDTH
    legend_h = 15.0 if show_legend else 0.0
    ref_lab = spec.get("refline_label") if ref is not None else ""
    # 参考线的标签放在绘图区右侧外面，和线端标注同一个思路：不压数据
    pad_r = 16.0 + (text_width(ref_lab, 8.0) + 6.0 if ref_lab else 0.0)
    plot_h = spec.get("height") or 160.0
    plot_w = W - pad_l - pad_r

    # 类别标签按格宽折行；超过两行就说明该换横向
    slot = plot_w / max(len(cats), 1)
    labels = [wrap(c, max(slot - 6.0, 18.0), fs) for c in cats]
    deepest = max(len(x) for x in labels)
    if deepest > 2:
        warns.append(f"类别标签最长的折到 {deepest} 行，纵向排布会挤压绘图区；"
                     "建议改 orientation=horizontal")
    lab_h = deepest * fs * 1.25
    pad_b = 22.0 + lab_h + (fs * 2.2 if xlabel else 0.0)
    pad_b += 12.0 if spec.get("note") else 0.0
    H = PAD_T + legend_h + plot_h + pad_b

    svg = Svg(W, H, font=SERIF if lang == "zh" else SANS)
    x0, y0 = pad_l, PAD_T + legend_h + plot_h
    x1, y1 = pad_l + plot_w, PAD_T + legend_h

    def sy(v):
        return y0 - (v - v_lo) / (v_hi - v_lo) * plot_h

    if show_legend:
        _legend(svg, series, 10.0, PAD_T + 6.0)

    if ref is not None:
        ry = sy(ref)
        svg.line(x0, ry, x1, ry, sw=0.75, dash="3 2")
        if ref_lab:
            svg.text_c(x1 + 4, ry, ref_lab, 8.0, anchor="start")

    svg.line(x0, y0, x1, y0, sw=0.75)
    svg.line(x0, y0, x0, y1, sw=0.75)
    for v in nice_ticks(v_lo, v_hi, 5):
        ty = sy(v)
        svg.line(x0, ty, x0 - TICK, ty, sw=0.75)
        svg.text(x0 - TICK - 2, ty + fs * 0.35, n(v), fs, anchor="end")
    if ylabel:
        svg.text(x0 - 34, (y0 + y1) / 2, ylabel, fs + 0.5, anchor="middle", rotate=-90)

    dx = min(8.0, slot * 0.4 / k) if k > 1 else 0.0
    bar_w = min(slot * 0.55 / k, 14.0)

    for i, lines in enumerate(labels):
        cx = x0 + slot * (i + 0.5)
        for j, ln in enumerate(lines):
            svg.text_c(cx, y0 + 8 + j * fs * 1.25 + fs * 0.4, ln, fs)
    if xlabel:
        svg.text_c((x0 + x1) / 2, y0 + 10 + lab_h + fs * 1.2, xlabel, fs + 0.5)

    for si, s in enumerate(series):
        off = (si - (k - 1) / 2) * dx
        for i, p in enumerate(s["points"]):
            cx = x0 + slot * (i + 0.5) + off
            if style == "bar":
                base = sy(ref) if ref is not None else sy(0.0)
                top, bot = sorted((base, sy(p["est"])))
                svg.rect(cx - bar_w / 2, top, max(bar_w, 0.4), max(bot - top, 0.4),
                         fill="#e6e6e6", sw=0.75)
            svg.line(cx, sy(p["lo"]), cx, sy(p["hi"]), sw=1.0)
            svg.line(cx - CAP, sy(p["lo"]), cx + CAP, sy(p["lo"]), sw=1.0)
            svg.line(cx - CAP, sy(p["hi"]), cx + CAP, sy(p["hi"]), sw=1.0)
            _marker(svg, MARKERS[si % len(MARKERS)], cx, sy(p["est"]))
            if p.get("sig"):
                svg.text(cx, sy(p["hi"]) - 4, p["sig"], 8.0, anchor="middle")

    if spec.get("note"):
        svg.text(12, H - 9, spec["note"], 8.2)
    return svg, warns


# ---------------------------------------------------------------- 输入
def _read_csv(path: str) -> dict:
    """读成 {列名: [float|None, ...]}。非数值原样保留为字符串。"""
    import csv
    with open(path, newline="", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        cols = rdr.fieldnames or []
        data: dict[str, list] = {c: [] for c in cols}
        for row in rdr:
            for c in cols:
                raw = (row.get(c) or "").strip()
                try:
                    data[c].append(float(raw))
                except ValueError:
                    data[c].append(raw if raw else None)
    return data


def main() -> int:
    ap = argparse.ArgumentParser(description="组间均值 / 系数图（点图 + 误差棒）")
    ap.add_argument("out")
    ap.add_argument("spec", nargs="?")
    ap.add_argument("--data", help="原始数据 CSV")
    ap.add_argument("--dv", help="因变量列")
    ap.add_argument("--by", help="分组列（横轴或纵轴的类别）")
    ap.add_argument("--by2", help="第二个分组列（画成不同形状的系列）")
    ap.add_argument("--ci", type=float, default=95.0, help="置信水平，默认 95")
    ap.add_argument("--style", choices=STYLES)
    ap.add_argument("--orientation", choices=ORIENT)
    ap.add_argument("--xlabel", default="")
    ap.add_argument("--ylabel", default="")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--width", type=float)
    ap.add_argument("--note", default="")
    ap.add_argument("--validate", action="store_true", help="只校验规格，不画图")
    ap.add_argument("--export", help="另存 PDF/PNG/TIFF，逗号分隔，如 pdf,png")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--gray", action="store_true", help="按灰度渲染，确认黑白印刷可辨")
    args = ap.parse_args()

    if args.data:
        if not (args.dv and args.by):
            raise SystemExit("--data 需要同时给 --dv 与 --by")
        df = _read_csv(args.data)
        for c in (args.dv, args.by, args.by2):
            if c and c not in df:
                raise SystemExit(f"CSV 里没有列 `{c}`；现有列：{list(df)}")
        series, warns = summarize(df, args.dv, args.by, args.by2, args.ci / 100.0)
        spec = {"lang": args.lang, "series": series,
                "xlabel": args.xlabel or f"Mean {args.dv} ({n(args.ci)}% CI)",
                "ylabel": args.ylabel, "note": args.note}
        if args.style:
            spec["style"] = args.style
        if args.orientation:
            spec["orientation"] = args.orientation
        if args.width:
            spec["width"] = args.width
        for w in warns:
            print(f"  ! {w}")
    else:
        if not args.spec:
            print(__doc__)
            return 2
        from qc import load_spec
        spec = load_spec(args.spec, required=("series",))
        for key in ("style", "orientation", "lang", "note", "width"):
            val = getattr(args, key, None)
            if val:
                spec[key] = val

    if args.validate:
        errs, warns = validate_spec(spec)
        for e in errs:
            print(f"  ✗ {e}")
        for w in warns:
            print(f"  ! {w}")
        print("规格可用。" if not errs else f"共 {len(errs)} 处必须改。")
        return 1 if errs else 0

    svg, warns = build(spec)
    out = svg.save(args.out)
    print(f"已生成 {out}  ({svg.w/72:.2f} × {svg.h/72:.2f} in)")
    for w in warns:
        print(f"  ! {w}")
    if args.export:
        files, notes = svg.export(out, formats=args.export.split(","),
                                  dpi=args.dpi, gray=args.gray)
        print_exports(files, notes)
    if args.data:
        for s in spec["series"]:
            tag = f"{s['label']}: " if s["label"] else ""
            for p in s["points"]:
                print(f"  {tag}{p['label']}  M = {p['est']:.3f}  "
                      f"[{p['lo']:.3f}, {p['hi']:.3f}]  n = {p['n']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
