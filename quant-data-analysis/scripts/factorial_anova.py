#!/usr/bin/env python3
"""Between-subjects ANOVA / ANCOVA (1 or 2 categorical factors, optional covariate).

Usage:
  python factorial_anova.py --file data.csv --dv y --factors A,B [--covariate c]
         [--robust] [--out report.txt]

What it does (all decisions are printed, nothing is silently changed):
  1. drops rows with missing values on the analysis variables (and says how many)
  2. descriptives per cell
  3. assumption diagnostics (Levene/Brown-Forsythe, Shapiro on residuals, variance/n ratios)
  4. Type III ANOVA with sum-to-zero contrasts; partial eta^2 and partial omega^2
     (--robust switches the F tests to HC3 heteroscedasticity-consistent versions)
  5. ANCOVA only: homogeneity-of-regression-slopes check and adjusted means
  6. follow-up comparisons that use the model's pooled error term, Holm-corrected:
       - 1 factor : all pairwise comparisons (+ Welch ANOVA / Games-Howell if Levene fails)
       - 2 factors: simple effects of each factor at each level of the other
                    (run whenever the interaction is p < .10, or always with --always-simple)
"""
import argparse, itertools, sys
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels.formula.api as smf
from statsmodels.stats.anova import anova_lm
from statsmodels.stats.multitest import multipletests
from common import load_data, fmt_p, fmt_num


def partial_eta2(ss, ss_res):
    return ss / (ss + ss_res)


def partial_omega2(df_eff, F, N):
    # omega^2_p for fixed-effects between-subjects designs
    return max(0.0, df_eff * (F - 1) / (df_eff * (F - 1) + N))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--dv", required=True)
    ap.add_argument("--factors", required=True, help="one or two categorical columns, comma-separated")
    ap.add_argument("--covariate", default=None)
    ap.add_argument("--robust", action="store_true", help="HC3-robust F tests")
    ap.add_argument("--always-simple", action="store_true")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()

    factors = [f.strip() for f in a.factors.split(",") if f.strip()]
    if not 1 <= len(factors) <= 2:
        raise SystemExit("This script handles 1 or 2 factors. For more, use the decision guide.")
    raw = load_data(a.file)
    need = [a.dv] + factors + ([a.covariate] if a.covariate else [])
    for c in need:
        if c not in raw.columns:
            raise SystemExit(f"Column not found: {c}. Available: {list(raw.columns)}")

    out = []
    P = out.append
    df = raw[need].copy()
    n0 = len(df)
    df = df.dropna()
    P(f"N in file = {n0}; complete cases used = {len(df)} (dropped {n0-len(df)} with missing values)")

    # safe internal names
    ren = {a.dv: "y"}
    for i, f in enumerate(factors):
        ren[f] = f"F{i+1}"
    if a.covariate:
        ren[a.covariate] = "cov"
    inv = {v: k for k, v in ren.items()}
    d = df.rename(columns=ren)
    d["y"] = pd.to_numeric(d["y"], errors="raise")
    fnames = [f"F{i+1}" for i in range(len(factors))]
    for f in fnames:
        d[f] = d[f].astype("category")
        if d[f].nunique() < 2:
            raise SystemExit(f"Factor {inv[f]} has fewer than 2 levels after cleaning.")
    if a.covariate:
        d["cov"] = pd.to_numeric(d["cov"], errors="raise")
        cov_mean = d["cov"].mean()
        d["cov_c"] = d["cov"] - cov_mean

    # ---- descriptives
    P("\n== Descriptives (cell M, SD, n) ==")
    desc = d.groupby(fnames, observed=True)["y"].agg(["count", "mean", "std"])
    desc.index.names = [inv[n] for n in desc.index.names]
    P(desc.round(3).to_string())
    N = len(d)
    cells = d.groupby(fnames, observed=True).size()
    if cells.min() < 2:
        raise SystemExit("A cell has fewer than 2 observations; cannot estimate variance.")

    # ---- model
    rhs = " * ".join(f"C({f}, Sum)" for f in fnames)
    if a.covariate:
        rhs += " + cov_c"
    model = smf.ols(f"y ~ {rhs}", data=d).fit()
    resid = model.resid

    # ---- assumptions
    P("\n== Assumption diagnostics (diagnostics, not gatekeepers) ==")
    groups = [g["y"].values for _, g in d.groupby(fnames, observed=True)]
    lev = st.levene(*groups, center="median")
    P(f"Levene (Brown-Forsythe, median-centered): W = {lev.statistic:.2f}, p {fmt_p(lev.pvalue)}")
    vars_ = np.array([np.var(g, ddof=1) for g in groups])
    P(f"Largest/smallest cell variance ratio = {vars_.max()/vars_.min():.2f}; "
      f"largest/smallest cell n = {cells.max()}/{cells.min()}")
    if N <= 5000:
        sh = st.shapiro(resid)
        P(f"Shapiro-Wilk on residuals: W = {sh.statistic:.3f}, p {fmt_p(sh.pvalue)}")
    P(f"Residual skew = {st.skew(resid):.2f}, excess kurtosis = {st.kurtosis(resid):.2f}")
    heter = lev.pvalue < .05 or (vars_.max()/vars_.min() > 4)
    unbal = cells.max() / cells.min() > 1.5
    serious = (lev.pvalue < .05 and unbal) or (vars_.max()/vars_.min() > 4)
    if heter and unbal:
        P("-> Unequal variances AND unbalanced cells: classical F is unreliable. "
          "Re-run with --robust and report that choice.")
    elif heter:
        P("-> Variances look unequal (cells roughly balanced): F is fairly tolerant, "
          "but consider --robust as a sensitivity analysis.")
    if N < 30 * len(cells):
        P("-> Small cells: normality of residuals matters more; inspect a Q-Q plot.")

    # ---- ANCOVA slope homogeneity
    if a.covariate:
        P("\n== ANCOVA check: homogeneity of regression slopes ==")
        full = smf.ols(f"y ~ {rhs} + cov_c:" + ":".join(f"C({f}, Sum)" for f in fnames), data=d).fit()
        cmp_ = anova_lm(model, full)
        P(f"Covariate x factor(s) interaction: F({int(cmp_['df_diff'].iloc[1])}, "
          f"{int(full.df_resid)}) = {cmp_['F'].iloc[1]:.2f}, p {fmt_p(cmp_['Pr(>F)'].iloc[1])}")
        if cmp_["Pr(>F)"].iloc[1] < .05:
            P("-> Slopes differ across groups: the standard ANCOVA assumption is violated. "
              "Do not report adjusted means as if the covariate effect were common; "
              "consider a moderation model instead.")

    # ---- ANOVA table
    P("\n== ANOVA (Type III, sum-to-zero contrasts)" + (" with HC3-robust F ==" if a.robust else " =="))
    tab = anova_lm(model, typ=3, robust="hc3") if a.robust else anova_lm(model, typ=3)
    ss_tab = anova_lm(model, typ=3)  # classical sums of squares (used for effect sizes)
    df_res = int(model.df_resid)
    rows = []
    for name in tab.index:
        if name in ("Intercept", "Residual"):
            continue
        pretty = name
        for k in fnames:
            pretty = pretty.replace(f"C({k}, Sum)", inv[k])
        pretty = pretty.replace("cov_c", f"{a.covariate}(cov)" if a.covariate else "cov")
        dfe = int(tab.loc[name, "df"])
        F = float(tab.loc[name, "F"])          # robust F if --robust, else classical
        p = float(tab.loc[name, "PR(>F)"])
        ss = float(ss_tab.loc[name, "sum_sq"])
        F_classic = (ss / dfe) / (model.ssr / df_res)   # effect sizes always from classical F
        rows.append((pretty, dfe, df_res, F, p, partial_eta2(ss, model.ssr),
                     partial_omega2(dfe, F_classic, N)))
    P(f"{'Effect':<28}{'df':>4}{'df_res':>8}{'F':>10}{'p':>10}{'eta_p^2':>10}{'omega_p^2':>11}")
    for r in rows:
        P(f"{r[0]:<28}{r[1]:>4}{r[2]:>8}{r[3]:>10.2f}{('<.001' if r[4] < .001 else f'{r[4]:.3f}'):>10}"
          f"{r[5]:>10.3f}{r[6]:>11.3f}")
    P("(eta_p^2 uses the classical sums of squares even when --robust is used; "
      "the robust column changes only F and p.)")

    # ---- estimated marginal contrasts
    exog = pd.DataFrame(model.model.exog, columns=model.params.index, index=d.index)
    mse = model.mse_resid
    sd_pool = np.sqrt(mse)
    levels = {f: list(d[f].cat.categories) for f in fnames}

    def design_row(lv):
        """Design-matrix row of the cell `lv` (covariate fixed at its mean).
        Taken from an observed row of that cell, so it works across statsmodels versions."""
        mask = np.ones(len(d), dtype=bool)
        for k, v in lv.items():
            mask &= (d[k] == v).values
        r = exog[mask].iloc[0].copy()
        if a.covariate:
            r["cov_c"] = 0.0
        return r.values.astype(float)

    contrast_model = model.get_robustcov_results(cov_type="HC3") if a.robust else model
    cov_note = "HC3-robust SEs" if a.robust else "pooled MSE (assumes equal variances)"

    def contrast_family(pairs, title):
        res = []
        for (l1, l2) in pairs:
            c = design_row(l1) - design_row(l2)
            t = contrast_model.t_test(c)
            est = float(np.squeeze(t.effect)); se = float(np.squeeze(t.sd))
            tv = float(np.squeeze(t.tvalue)); pv = float(np.squeeze(t.pvalue))
            ci = np.asarray(t.conf_int()).reshape(-1)
            res.append((l1, l2, est, se, tv, pv, ci, est / sd_pool))
        if not res:
            return
        adj = multipletests([r[5] for r in res], method="holm")[1]
        P(f"\n-- {title} (df = {df_res}; {cov_note}; Holm over {len(res)} comparison(s); "
          f"d = mean diff / sqrt(MSE)) --")
        for r, pa in zip(res, adj):
            def nm(l): return ", ".join(f"{inv[k]}={v}" for k, v in l.items())
            P(f"{nm(r[0])}  vs  {nm(r[1])}: diff = {r[2]:.3f}, SE = {r[3]:.3f}, "
              f"t({df_res}) = {r[4]:.2f}, p_raw {fmt_p(r[5])}, p_Holm {fmt_p(pa)}, "
              f"95% CI [{r[6][0]:.3f}, {r[6][1]:.3f}], d = {r[7]:.2f}")

    if len(factors) == 1:
        f = fnames[0]
        pairs = [({f: x}, {f: y}) for x, y in itertools.combinations(levels[f], 2)]
        P("\n== Follow-up comparisons ==")
        if serious and not a.robust and not a.covariate:
            P("Variances are clearly unequal, so pooled-error pairwise tests would be misleading; "
              "Games-Howell (Welch-type) comparisons are the primary follow-up below. "
              "Use --robust for HC3-based pairwise tests instead.")
        else:
            if serious and not a.robust and a.covariate:
                P("NOTE: variances are clearly unequal and Games-Howell cannot include a covariate; "
                  "re-run with --robust (HC3) and report it. The pooled-error results below are provisional.")
            elif heter and not a.robust:
                P("NOTE: Levene is significant but cells are balanced and variance ratios moderate; "
                  "pooled-error comparisons are usually acceptable, but report a --robust check.")
            contrast_family(pairs, f"Pairwise comparisons of {inv[f]}")
        if not a.covariate:
            try:
                import pingouin as pg
                P("\n-- Welch ANOVA + Games-Howell (reported by default for one-factor designs; "
                  "equal-variance tests are not used as a gate) --")
                w = pg.welch_anova(data=d, dv="y", between=f)
                P(w.round(4).to_string(index=False))
                gh = pg.pairwise_gameshowell(data=d, dv="y", between=f)
                P(gh.round(4).to_string(index=False))
            except Exception as e:
                P(f"(Welch/Games-Howell unavailable: {e})")
        if len(levels[f]) == 2 and not a.covariate:
            g1, g2 = [d.loc[d[f] == l, "y"].values for l in levels[f]]
            n1, n2 = len(g1), len(g2)
            v1, v2 = g1.var(ddof=1), g2.var(ddof=1)
            se = np.sqrt(v1 / n1 + v2 / n2)
            diff = g1.mean() - g2.mean()
            dfw = se**4 / ((v1 / n1) ** 2 / (n1 - 1) + (v2 / n2) ** 2 / (n2 - 1))
            tw = diff / se
            pw = 2 * st.t.sf(abs(tw), dfw)
            ci = (diff - st.t.ppf(.975, dfw) * se, diff + st.t.ppf(.975, dfw) * se)
            sp = np.sqrt(((n1 - 1) * v1 + (n2 - 1) * v2) / (n1 + n2 - 2))
            dd = diff / sp
            g_h = dd * (1 - 3 / (4 * (n1 + n2) - 9))
            P(f"\nWelch t-test ({levels[f][0]} vs {levels[f][1]}): diff = {diff:.3f}, "
              f"t({dfw:.1f}) = {tw:.2f}, p {fmt_p(pw)}, 95% CI [{ci[0]:.3f}, {ci[1]:.3f}], "
              f"Cohen's d = {dd:.2f}, Hedges g = {g_h:.2f}")
    else:
        f1, f2 = fnames
        inter = [r for r in rows if ":" in r[0]]
        p_int = inter[0][4] if inter else 1.0
        if p_int < .10 or a.always_simple:
            P(f"\n== Simple effects (interaction p {fmt_p(p_int)}) ==")
            if heter and not a.robust:
                P("NOTE: variances look unequal; these simple effects use the pooled error term. "
                  "Re-run with --robust for HC3-based versions and report both if they differ.")
            for tgt, other in ((f1, f2), (f2, f1)):
                for lv_o in levels[other]:
                    pairs = [({tgt: x, other: lv_o}, {tgt: y, other: lv_o})
                             for x, y in itertools.combinations(levels[tgt], 2)]
                    contrast_family(pairs, f"Effect of {inv[tgt]} at {inv[other]} = {lv_o}")
        else:
            P(f"\nInteraction p {fmt_p(p_int)}: simple effects not run (use --always-simple to force). "
              "If you test main effects, describe them as averaged over the other factor.")

    # ---- marginal means
    if a.covariate:
        P(f"\n== Adjusted (estimated marginal) means at {a.covariate} = {cov_mean:.3f} ==")
        for combo in itertools.product(*[levels[f] for f in fnames]):
            lv = dict(zip(fnames, combo))
            r = design_row(lv)
            est = float(r @ model.params.values)
            se = float(np.sqrt(r @ model.cov_params().values @ r))
            P(", ".join(f"{inv[k]}={v}" for k, v in lv.items()) + f": {est:.3f} (SE {se:.3f})")

    text = "\n".join(out)
    print(text)
    if a.out:
        open(a.out, "w", encoding="utf-8").write(text)


if __name__ == "__main__":
    main()
