"""折线图的公共实现：N 条系列 + 可选置信带。

交互效应图与多系列折线图用的是同一段画图代码——两份实现迟早会漂移，
症状是「交互图对了、折线图错位」，而看代码看不出来。

**黑白印刷下怎么区分系列**（APA 的立场是别靠颜色）：实线 / 长虚线 / 点线 / 点划线，
再配四种标记形状。所以系列超过 2 条时不要给颜色，给线型。
"""
from __future__ import annotations

from svg_kit import FULL_WIDTH, SANS, SERIF, Svg, nice_ticks, text_width, wrap

FS = 8.5
PAD_L, PAD_T, PAD_B = 66.0, 16.0, 40.0

# 黑白印刷下仍能分辨的四种线型与标记（顺序即默认分配顺序）
# 点线要留够空隙，否则缩到半幅时看起来跟实线一样
DASHES = [None, "5 2.5", "2 3", "6 2 1.5 2"]
MARKERS = ["circle", "square", "triangle", "diamond"]


def _marker(svg: Svg, x: float, y: float, kind: str, size: float = 2.6) -> None:
    if kind == "circle":
        svg.circle(x, y, size, fill="#fff", stroke="#000", sw=0.7)
    elif kind == "square":
        svg.rect(x - size, y - size, size * 2, size * 2, fill="#fff", stroke="#000", sw=0.7)
    elif kind == "triangle":
        svg.polygon([(x, y - size * 1.2), (x + size * 1.1, y + size * 0.8),
                     (x - size * 1.1, y + size * 0.8)], fill="#fff", stroke="#000", sw=0.7)
    elif kind == "diamond":
        svg.polygon([(x, y - size * 1.3), (x + size * 1.1, y),
                     (x, y + size * 1.3), (x - size * 1.1, y)],
                    fill="#fff", stroke="#000", sw=0.7)


def _corner_legend(svg: Svg, series: list, styles: list, x1: float, y1: float,
                   size: float = FS) -> None:
    """右上角的小图例。图例条目少、标签短时才用；否则优先线端标注。"""
    rows = [(s.get("label", ""), st[0], st[1]) for s, st in zip(series, styles)]
    w = max(text_width(lbl, size) for lbl, _, _ in rows) + 34
    h = 11.0 * len(rows) + 4
    x0, y0 = x1 - w - 6, y1 + 6
    svg.rect(x0, y0, w, h, fill="#fff", stroke="#000", sw=0.6)
    for i, (lbl, dash, mk) in enumerate(rows):
        cy = y0 + 9 + i * 11
        svg.line(x0 + 4, cy, x0 + 22, cy, sw=1.1, dash=dash)
        if mk:
            _marker(svg, x0 + 13, cy, mk, 2.2)
        svg.text(x0 + 26, cy + 3, lbl, size)


def _legend_rows(series: list, styles: list, avail: float,
                 size: float = FS) -> list[list[tuple]]:
    """把图例条目排成若干行，每行不超过可用宽度。"""
    rows = [(s.get("label", ""), st[0], st[1]) for s, st in zip(series, styles)]
    item_w = [26 + text_width(lbl, size) for lbl, _, _ in rows]
    gap = 14.0
    lines, cur, curw = [], [], 0.0
    for item, w in zip(rows, item_w):
        add = w + (gap if cur else 0)
        if cur and curw + add > avail:
            lines.append(cur)
            cur, curw = [], 0.0
            add = w
        cur.append((*item, w))
        curw += add
    if cur:
        lines.append(cur)
    return lines


def _top_legend(svg: Svg, lines: list, x0: float, x1: float, bottom_y: float,
                size: float = FS) -> None:
    """横排图例，画在绘图区上方。

    放在绘图区里（右上角）迟早会压住数据——线是斜的，右上角往往正是终点所在。
    上方横排是唯一不会撞上数据的位置；一行放不下就折成多行向上叠。
    """
    gap = 14.0
    for li, line in enumerate(lines):
        total = sum(it[3] for it in line) + gap * (len(line) - 1)
        cx = (x0 + x1) / 2 - total / 2
        cy = bottom_y - 11.0 * (len(lines) - 1 - li)
        for lbl, dash, mk, w in line:
            svg.line(cx, cy, cx + 18, cy, sw=1.1, dash=dash)
            if mk:
                _marker(svg, cx + 9, cy, mk, 2.2)
            svg.text(cx + 22, cy + 3, lbl, size)
            cx += w + gap


def _tick_labels(lo: float, hi: float, target: int = 5) -> list[tuple[float, str]]:
    """刻度值与其标签。小数位数全列统一——同一根轴上写 5 和 5.5 是排版失误。"""
    vals = nice_ticks(lo, hi, target)
    if not vals:
        return []
    step = min(abs(b - a) for a, b in zip(vals, vals[1:])) if len(vals) > 1 else 1.0
    dec = 0
    for s in (step,):
        while dec < 4 and abs(round(s, dec) - s) > 1e-9:
            dec += 1
    return [(v, f"{v:.{dec}f}") for v in vals]


def build(spec: dict, opts: dict | None = None) -> Svg:
    """画一张折线图。spec 见 references/line-plots.md。"""
    opts = opts or {}
    lang = opts.get("lang") or spec.get("lang") or "en"
    series = spec["series"]
    if not series:
        raise SystemExit("series 为空：至少给一条线")

    for i, s in enumerate(series):
        if "x" not in s or "y" not in s:
            raise SystemExit(f"第 {i+1} 条系列缺 x 或 y")
        if len(s["x"]) != len(s["y"]):
            raise SystemExit(f"第 {i+1} 条系列的 x 与 y 长度不同"
                             f"（{len(s['x'])} vs {len(s['y'])}）")
        has_lo, has_hi = "lo" in s, "hi" in s
        if has_lo != has_hi:
            # 只给一半的区间画不出来，也不该猜另一半
            raise SystemExit(f"第 {i+1} 条系列只给了 {'lo' if has_lo else 'hi'}，"
                             "置信带需要同时给 lo 与 hi")

    legend_mode = spec.get("legend", "end")
    # 线型与标记只在这里解析一次：图例读的是同一份，否则「默认分配」的线型
    # 画到图上是虚线、画到图例里却是实线。
    use_markers = bool(spec.get("markers"))
    styles = [(s.get("dash", DASHES[i % len(DASHES)]),
               s.get("marker", MARKERS[i % len(MARKERS)] if use_markers else None))
              for i, s in enumerate(series)]
    end_labels = legend_mode == "end"
    label_w = max((text_width(s.get("label", ""), FS) for s in series), default=0)
    PAD_R = (14.0 + label_w) if end_labels else 22.0

    W = opts.get("width") or spec.get("width") or max(FULL_WIDTH, PAD_L + 200 + PAD_R)
    xs = [v for s in series for v in s["x"]]
    ys = [v for s in series for v in s["y"]]
    for s in series:
        ys += list(s.get("lo") or []) + list(s.get("hi") or [])

    x_lo, x_hi = min(xs), max(xs)
    y_lo, y_hi = min(ys), max(ys)
    # 李克特量表、百分比这类有自然边界的量，必须由作者给范围：
    # 按数据范围自动缩放会把 1–7 的画成 3.8–4.4，读者以为差异很大。
    if spec.get("x_range"):
        x_lo, x_hi = spec["x_range"]
    if spec.get("y_range"):
        y_lo, y_hi = spec["y_range"]
    else:
        pad = (y_hi - y_lo) * 0.08 or 0.1
        y_lo, y_hi = y_lo - pad, y_hi + pad
    if x_hi <= x_lo or y_hi <= y_lo:
        raise SystemExit("x_range / y_range 的上界必须大于下界")

    plot_w = W - PAD_L - PAD_R
    plot_h = opts.get("height") or spec.get("height") or 190.0
    legend_lines = (_legend_rows(series, styles, W - PAD_L - PAD_R)
                    if legend_mode == "top" else [])
    pad_t = PAD_T + (13.0 * len(legend_lines) + 3.0 if legend_lines else 0.0)
    # 图注按画布宽折行：不折的话长图注会被画布裁掉，屏幕上还看不出来
    note_lines = wrap(spec["note"], W - 24, 8.2) if spec.get("note") else []
    pad_b = PAD_B + 11.0 * max(0, len(note_lines) - 1) + (12.0 if note_lines else 0.0)
    H = pad_t + plot_h + pad_b
    svg = Svg(W, H, font=SERIF if lang == "zh" else SANS)

    x0, y0 = PAD_L, pad_t + plot_h
    x1, y1 = PAD_L + plot_w, pad_t

    def sx(v):
        return x0 + (v - x_lo) / (x_hi - x_lo) * plot_w

    def sy(v):
        return y0 - (v - y_lo) / (y_hi - y_lo) * plot_h

    # 分类轴：给了 x_ticks 就按它标，不再算 nice_ticks
    if spec.get("x_ticks"):
        xt = [(sx(float(t["v"])), str(t["label"])) for t in spec["x_ticks"]]
    else:
        xt = [(sx(v), lab) for v, lab in _tick_labels(x_lo, x_hi, 5)]
    yt = [(sy(v), lab) for v, lab in _tick_labels(y_lo, y_hi, 5)]
    svg.axes(x0, y0, x1, y1, xt, yt, size=FS,
             xlabel=spec.get("xlabel", ""), ylabel=spec.get("ylabel", ""))

    # 参考线先画，别盖住数据
    ref = spec.get("refline")
    if ref:
        v = float(ref["v"])
        pos = ref.get("label_pos", "left")
        side = ref.get("label_side", "above")
        if ref.get("axis", "y") == "y":
            ry = sy(v)
            svg.line(x0, ry, x1, ry, sw=0.75, dash="3 2")
            if ref.get("label"):
                # 标签默认放左侧、线下方：右侧要留给线端标注，线上方多半压着数据
                ty = ry - 3 if side == "above" else ry + 9
                if pos == "right":
                    svg.text(x1 - 3, ty, ref["label"], 8.0, anchor="end")
                else:
                    svg.text(x0 + 3, ty, ref["label"], 8.0, anchor="start")
        else:
            rx = sx(v)
            svg.line(rx, y0, rx, y1, sw=0.75, dash="3 2")
            if ref.get("label"):
                svg.text(rx + 3, y1 + 8, ref["label"], 8.0, anchor="start")

    end_y: list[tuple[float, str]] = []
    for i, s in enumerate(series):
        dash, mk = styles[i]
        if s.get("lo") and s.get("hi"):
            top = [(sx(a), sy(b)) for a, b in zip(s["x"], s["hi"])]
            bot = [(sx(a), sy(b)) for a, b in zip(reversed(s["x"]), reversed(s["lo"]))]
            svg.polygon(top + bot, fill="#000", stroke="none", opacity=0.08)
        pts = [(sx(a), sy(b)) for a, b in zip(s["x"], s["y"])]
        svg.polyline(pts, sw=1.1, dash=dash)
        if mk:
            for px, py in pts:
                _marker(svg, px, py, mk)
        if end_labels:
            end_y.append((pts[-1][1], s.get("label", ""), pts[-1][0]))

    if end_labels:
        # 线端直接标注比图例省版面，也不要求读者在图与图例之间来回看。
        # 但两条线在末端靠得很近时，两个标签会叠在一起——按最小间距往下推，
        # 推的时候只动标签不动数据。
        end_y.sort()
        placed: list[float] = []
        for yv, _lbl, _lx in end_y:
            if placed and yv - placed[-1] < 9.5:
                yv = placed[-1] + 9.5
            placed.append(yv)
        for (yv, lbl, lx), ny in zip(end_y, placed):
            svg.text(lx + 4, ny + 3, lbl, FS, anchor="start")

    if legend_mode == "corner":
        _corner_legend(svg, series, styles, x1, y1)
    elif legend_mode == "top":
        _top_legend(svg, legend_lines, x0, x1, y1 - 6)

    for i, line in enumerate(note_lines):
        svg.text(12, H - 11 - 11.0 * (len(note_lines) - 1 - i), line, 8.2)
    return svg
