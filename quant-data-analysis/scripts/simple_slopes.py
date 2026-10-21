#!/usr/bin/env python3
"""Moderation by regression: interaction test, simple slopes, Johnson-Neyman region.

Usage:
  python simple_slopes.py --file data.csv --y outcome --x predictor --m moderator
        [--covariates c1,c2] [--no-center-x] [--robust] [--out report.txt]

- x may be continuous or two-level (two-level x is recoded 0/1 in sorted order, mapping printed;
  it is NOT centered). Continuous x and the moderator m are mean-centered.
- Simple slopes of x are estimated at m = mean-1SD, mean, mean+1SD (original units printed).
- Johnson-Neyman: the range of m (within the observed range) where the slope of x is p < .05.
For bootstrapped indirect effects / moderated mediation use the sem-analysis-tutor skill.
"""
import argparse
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf
from common import load_data, fmt_p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--y", required=True)
    ap.add_argument("--x", required=True)
    ap.add_argument("--m", required=True)
    ap.add_argument("--covariates", default="")
    ap.add_argument("--no-center-x", action="store_true")
    ap.add_argument("--robust", action="store_true", help="HC3 standard errors")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    covs = [c.strip() for c in a.covariates.split(",") if c.strip()]
    raw = load_data(a.file)
    need = [a.y, a.x, a.m] + covs
    for c in need:
        if c not in raw.columns:
            raise SystemExit(f"Column not found: {c}. Available: {list(raw.columns)}")
    out = []
    P = out.append
    df = raw[need].dropna().copy()
    P(f"N in file = {len(raw)}; complete cases used = {len(df)} (dropped {len(raw)-len(df)})")

    d = pd.DataFrame({"y": pd.to_numeric(df[a.y], errors="raise")})
    # predictor
    xs = df[a.x]
    if xs.nunique() == 2:
        lv = sorted(xs.unique().tolist(), key=str)
        d["x"] = (xs == lv[1]).astype(float)
        P(f"x is two-level: coded {lv[0]!r} = 0, {lv[1]!r} = 1 (not centered)")
        x_binary = True
    else:
        xn = pd.to_numeric(xs, errors="raise")
        x_mean = xn.mean()
        d["x"] = xn if a.no_center_x else xn - x_mean
        P(f"x is continuous: mean = {x_mean:.3f}" + (" (NOT centered)" if a.no_center_x else " (centered)"))
        x_binary = False
    mn = pd.to_numeric(df[a.m], errors="raise")
    m_mean, m_sd = mn.mean(), mn.std(ddof=1)
    d["m"] = mn - m_mean
    P(f"moderator {a.m}: mean = {m_mean:.3f}, SD = {m_sd:.3f}, observed range [{mn.min():.3f}, {mn.max():.3f}] (centered)")
    cov_terms = []
    for i, c in enumerate(covs):
        d[f"c{i}"] = pd.to_numeric(df[c], errors="raise")
        cov_terms.append(f"c{i}")
    rhs = "x * m" + ("".join(" + " + t for t in cov_terms))
    base = smf.ols("y ~ x + m" + ("".join(" + " + t for t in cov_terms)), d).fit()
    fit = smf.ols(f"y ~ {rhs}", d).fit()
    res = fit.get_robustcov_results(cov_type="HC3") if a.robust else fit
    names = list(fit.params.index)

    P("\n== Regression coefficients (" + ("HC3-robust SEs" if a.robust else "OLS SEs") + ") ==")
    ci = np.asarray(res.conf_int())
    params, bse = np.asarray(res.params), np.asarray(res.bse)
    tvals, pvals = np.asarray(res.tvalues), np.asarray(res.pvalues)
    label = {"x": a.x, "m": a.m + " (centered)", "x:m": f"{a.x} x {a.m}"}
    label.update({f"c{i}": c + " (covariate)" for i, c in enumerate(covs)})
    for i, nme in enumerate(names):
        nm = label.get(nme, nme)
        P(f"{nm:<28} b = {params[i]:>8.3f}  SE = {bse[i]:.3f}  t = {tvals[i]:>6.2f}  "
          f"p {fmt_p(pvals[i])}  95% CI [{ci[i][0]:.3f}, {ci[i][1]:.3f}]")
    dR2 = fit.rsquared - base.rsquared
    Fchg = dR2 / (1 - fit.rsquared) * fit.df_resid
    P(f"\nR2 = {fit.rsquared:.3f}; interaction adds dR2 = {dR2:.3f}, F(1, {int(fit.df_resid)}) = {Fchg:.2f}, "
      f"p {fmt_p(1 - st.f.cdf(Fchg, 1, fit.df_resid))}")

    ix, im, iint = names.index("x"), names.index("m"), names.index("x:m")

    def slope_at(mv):
        c = np.zeros(len(names)); c[ix] = 1; c[iint] = mv
        t = res.t_test(c)
        est, se = float(np.squeeze(t.effect)), float(np.squeeze(t.sd))
        p = float(np.squeeze(t.pvalue)); cint = np.asarray(t.conf_int()).reshape(-1)
        return est, se, float(np.squeeze(t.tvalue)), p, cint

    P(f"\n== Simple slopes of {a.x} on {a.y} ==")
    for lab, mv in (("-1 SD", -m_sd), ("mean", 0.0), ("+1 SD", m_sd)):
        est, se, tv, p, c = slope_at(mv)
        P(f"{a.m} = {m_mean+mv:.3f} ({lab}): slope = {est:.3f}, SE = {se:.3f}, t({int(fit.df_resid)}) = {tv:.2f}, "
          f"p {fmt_p(p)}, 95% CI [{c[0]:.3f}, {c[1]:.3f}]")

    # Johnson-Neyman
    tc = st.t.ppf(.975, fit.df_resid)
    V = np.asarray(res.cov_params())
    bx, bi = params[ix], params[iint]
    vxx, vxi, vii = V[ix, ix], V[ix, iint], V[iint, iint]
    A = bi**2 - tc**2 * vii
    B = 2 * (bx * bi - tc**2 * vxi)
    C = bx**2 - tc**2 * vxx
    roots = []
    if abs(A) > 1e-12:
        disc = B**2 - 4 * A * C
        if disc >= 0:
            roots = sorted([(-B - np.sqrt(disc)) / (2 * A), (-B + np.sqrt(disc)) / (2 * A)])
    grid = np.linspace(mn.min() - m_mean, mn.max() - m_mean, 2001)
    sig = np.array([abs(bx + bi * g) / np.sqrt(vxx + 2 * g * vxi + g**2 * vii) > tc for g in grid])
    P("\n== Johnson-Neyman (slope of x significant at p < .05) ==")
    if sig.all():
        P("Slope is significant across the ENTIRE observed range of the moderator.")
    elif (~sig).all():
        P("Slope is NOT significant anywhere in the observed range of the moderator.")
    else:
        edges = np.flatnonzero(np.diff(sig.astype(int)) != 0)
        segs, start = [], 0
        for e in list(edges) + [len(grid) - 1]:
            segs.append((grid[start], grid[e], bool(sig[start])))
            start = e + 1
        for lo, hi, sflag in segs:
            P(f"{a.m} from {lo+m_mean:.3f} to {hi+m_mean:.3f}: slope {'significant' if sflag else 'not significant'}")
        inr = [r + m_mean for r in roots if grid.min() <= r <= grid.max()]
        if inr:
            P("Transition point(s) in original units: " + ", ".join(f"{r:.3f}" for r in inr))
    P("Note: regions are conditional on this model; with unequal variances rerun with --robust.")

    text = "\n".join(out)
    print(text)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
