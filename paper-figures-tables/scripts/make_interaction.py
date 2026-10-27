"""交互效应图（SVG，零依赖绘图）。

两种输入：

1) 从数据算（推荐）——拟合 y = b0 + b1·x + b2·m + b3·x·m，
   在 m = 均值 ± 1 SD 处画两条线，可加 95% 置信带：

       python make_interaction.py --data d.csv --dv y --x x --mod m \
              --xlabel "Brand trust" --ylabel "Purchase intention" out.svg

2) 从汇总值画——已知两组斜率与截距时直接给数：

       python make_interaction.py --summary s.json out.svg

为什么默认画 ±1 SD 而不是「高/低分组」：连续调节变量二分法会损失信息、
也会人为制造显著（MacCallum et al., 2002）。若原始研究确实用了二分操纵，
用 --levels 显式指定两组的取值。
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import line_core  # noqa: E402
from svg_kit import FULL_WIDTH, HALF_WIDTH, SANS, SERIF, Svg, n, text_width
from mpl_backend import summarize

PAD_L, PAD_T, PAD_B = 66.0, 16.0, 40.0
TICK = 3.0
FS = 8.5


def _mat_mul(A, B):
    n, k, m = len(A), len(B), len(B[0])
    return [[sum(A[i][t] * B[t][j] for t in range(k)) for j in range(m)]
            for i in range(n)]


def _transpose(A):
    return [list(r) for r in zip(*A)]


def _solve(A, b):
    """高斯消元（列主元）解 A x = b。A 会被复制，不改原矩阵。"""
    n = len(A)
    M = [row[:] + [b[i]] for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            raise ValueError("设计矩阵奇异（自变量共线或样本不足），无法拟合")
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        for r in range(col + 1, n):
            f = M[r][col] / pv
            if f:
                for c in range(col, n + 1):
                    M[r][c] -= f * M[col][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = M[r][n] - sum(M[r][c] * x[c] for c in range(r + 1, n))
        x[r] = s / M[r][r]
    return x


def _inverse(A):
    """高斯-约当求逆（4×4 够用）。"""
    n = len(A)
    M = [row[:] + [1.0 if i == j else 0.0 for j in range(n)]
         for i, row in enumerate(A)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        if abs(M[piv][col]) < 1e-12:
            raise ValueError("设计矩阵奇异，无法求系数协方差")
        M[col], M[piv] = M[piv], M[col]
        pv = M[col][col]
        M[col] = [v / pv for v in M[col]]
        for r in range(n):
            if r == col:
                continue
            f = M[r][col]
            if f:
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]


def _mean(v):
    return sum(v) / len(v)


def _sd(v):
    mu = _mean(v)
    return math.sqrt(sum((a - mu) ** 2 for a in v) / (len(v) - 1))


def ols(X, y):
    """最小二乘：解正规方程 X'X β = X'y，返回 (β, σ², 列数)。

    纯标准库实现——原版用 numpy.linalg.lstsq，学生在没装 numpy 的机器上
    跑 --data 会直接 ImportError。4 列的设计矩阵手解完全够用。
    """
    Xt = _transpose(X)
    XtX = _mat_mul(Xt, X)
    Xty = [sum(Xt[i][k] * y[k] for k in range(len(y))) for i in range(len(Xt))]
    beta = _solve(XtX, Xty)
    k = len(beta)
    resid = [y[i] - sum(X[i][j] * beta[j] for j in range(k)) for i in range(len(y))]
    dof = max(len(y) - k, 1)
    sigma2 = sum(r * r for r in resid) / dof
    return beta, sigma2, k


def fit_interaction(df, dv, xv, mod):
    """df 是 {列名: [值, ...]} 的字典（不再需要 pandas）。"""
    rows = []
    for i in range(len(df[dv])):
        vals = (df[dv][i], df[xv][i], df[mod][i])
        if any(v is None or (isinstance(v, float) and math.isnan(v)) for v in vals):
            continue
        rows.append(vals)
    if len(rows) < 8:
        raise SystemExit(f"有效样本只有 {len(rows)} 行，无法拟合交互项（至少需要 8 行）")
    y = [r[0] for r in rows]
    x = [r[1] for r in rows]
    m = [r[2] for r in rows]
    X = [[1.0, x[i], m[i], x[i] * m[i]] for i in range(len(y))]
    beta, sigma2, k = ols(X, y)
    XtX = _mat_mul(_transpose(X), X)
    inv = _inverse(XtX)
    cov = [[sigma2 * v for v in row] for row in inv]
    se = [math.sqrt(max(cov[i][i], 0.0)) for i in range(k)]
    return dict(beta=beta, cov=cov, se=se, x=x, m=m, y=y, n=len(y),
                x_mean=_mean(x), x_sd=_sd(x),
                m_mean=_mean(m), m_sd=_sd(m))


def predict(fit, x_grid, m_level):
    b = fit["beta"]
    yhat, se = [], []
    for xv in x_grid:
        row = [1.0, xv, m_level, xv * m_level]
        yhat.append(sum(row[j] * b[j] for j in range(4)))
        var = sum(row[i] * fit["cov"][i][j] * row[j]
                  for i in range(4) for j in range(4))
        se.append(math.sqrt(max(var, 0.0)))
    return yhat, se


def build(data: dict, opts: dict) -> Svg:
    """交互效应图的画法就是「两条线 + 各自的置信带」——交给 line_core 画。

    两份实现迟早会漂移：今天交互图对了、折线图错位，明天反过来。
    """
    spec = dict(data)
    for k in ("xlabel", "ylabel", "note", "width", "height", "lang"):
        if opts.get(k) is not None:
            spec[k] = opts[k]
    spec.setdefault("legend", "end")
    return line_core.build(spec, opts)


def _read_csv(path: str) -> dict:
    """读成 {列名: [float|None, ...]}。空值与无法解析的值记为 None。"""
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
                    data[c].append(None)
    return data


def from_data(args) -> dict:
    df = _read_csv(args.data)
    for c in (args.dv, args.x, args.mod):
        if c not in df:
            raise SystemExit(f"CSV 里没有列 `{c}`；现有列：{list(df)}")
    fit = fit_interaction(df, args.dv, args.x, args.mod)
    lo_x = fit["x_mean"] - 2 * fit["x_sd"]
    hi_x = fit["x_mean"] + 2 * fit["x_sd"]
    grid = [lo_x + (hi_x - lo_x) * i / 59 for i in range(60)]
    series = []
    if args.levels:
        levels = [float(v) for v in args.levels.split(",")]
        labels = [f"{args.mod} = {n(v)}" for v in levels]
    else:
        levels = [fit["m_mean"] - fit["m_sd"], fit["m_mean"] + fit["m_sd"]]
        labels = [f"Low {args.mod} (−1 SD)", f"High {args.mod} (+1 SD)"]
    for lv, lab in zip(levels, labels):
        yhat, se = predict(fit, grid, lv)
        series.append({"label": lab, "x": list(grid), "y": list(yhat),
                       "lo": [a - 1.96 * s for a, s in zip(yhat, se)],
                       "hi": [a + 1.96 * s for a, s in zip(yhat, se)]})
    b = fit["beta"]
    slope = b[1] + b[3] * fit["m_mean"]
    return {"series": series,
            "stats": {"n": fit["n"], "b_interaction": float(b[3]),
                      "se_interaction": float(fit["se"][3]),
                      "simple_slope_at_mean": float(slope)}}


def from_summary(path: str) -> dict:
    from qc import load_spec
    spec = load_spec(path, required=("series",))
    return {"series": spec["series"], "stats": spec.get("stats", {})}


def main() -> int:
    ap = argparse.ArgumentParser(description="交互效应图")
    ap.add_argument("out")
    ap.add_argument("--data")
    ap.add_argument("--dv")
    ap.add_argument("--x")
    ap.add_argument("--mod")
    ap.add_argument("--levels", help="显式给定两组的调节变量取值，如 0,1")
    ap.add_argument("--summary")
    ap.add_argument("--xlabel", default="")
    ap.add_argument("--ylabel", default="")
    ap.add_argument("--note", default="")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--width", type=float)
    ap.add_argument("--height", type=float, default=190.0)
    ap.add_argument("--export", help="另存 PDF/PNG/TIFF，逗号分隔，如 pdf,png")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--gray", action="store_true", help="按灰度渲染，确认黑白印刷可辨")
    args = ap.parse_args()

    if args.data:
        data = from_data(args)
    elif args.summary:
        data = from_summary(args.summary)
    else:
        print(__doc__)
        return 2

    svg = build(data, vars(args))
    out = svg.save(args.out)
    print(f"已生成 {out}  ({svg.w/72:.2f} × {svg.h/72:.2f} in)")
    st = data.get("stats") or {}
    if "b_interaction" in st:
        print(f"  交互项 b = {st['b_interaction']:.3f} (SE = {st['se_interaction']:.3f})"
              f"，N = {st['n']}")
        print(f"  调节变量取均值处的简单斜率 = {st['simple_slope_at_mean']:.3f}")
    if args.export:
        files, notes = svg.export(out, formats=args.export.split(","),
                                  dpi=args.dpi, gray=args.gray)
        summarize(files, notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
