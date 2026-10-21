#!/usr/bin/env python3
"""Minimum detectable effect for a FIXED sample (secondary data, or data already collected).

This is NOT a power analysis for designing a new study (that belongs to
social-science-experiment-designer) and it must not be used as 'post-hoc power'
on an observed effect. It answers: given this N, how large would a true effect
have to be for the planned test to detect it with the stated power?

  python mde_fixed_sample.py two-group --n1 300 --n2 280 [--alpha .05 --power .8]
  python mde_fixed_sample.py correlation --n 1200
  python mde_fixed_sample.py anova --k 3 --n-total 450

Assumes independent observations, a single test, and the usual normality assumptions.
Clustered / repeated observations (several rows per customer) reduce the effective N:
use the number of independent units, not the number of rows.
"""
import argparse
import numpy as np
from scipy import stats
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="mode", required=True)
    for name in ("two-group", "correlation", "anova"):
        p = sub.add_parser(name)
        p.add_argument("--alpha", type=float, default=.05)
        p.add_argument("--power", type=float, default=.80)
        if name == "two-group":
            p.add_argument("--n1", type=int, required=True)
            p.add_argument("--n2", type=int, required=True)
        elif name == "correlation":
            p.add_argument("--n", type=int, required=True)
        else:
            p.add_argument("--k", type=int, required=True)
            p.add_argument("--n-total", type=int, required=True)
    a = ap.parse_args()

    if a.mode == "two-group":
        d = TTestIndPower().solve_power(effect_size=None, nobs1=a.n1, alpha=a.alpha, power=a.power,
                                        ratio=a.n2 / a.n1, alternative="two-sided")
        print(f"Two-group comparison, n1={a.n1}, n2={a.n2}, alpha={a.alpha}, power={a.power}: "
              f"minimum detectable |d| = {d:.3f}")
    elif a.mode == "correlation":
        za = stats.norm.ppf(1 - a.alpha / 2)
        zb = stats.norm.ppf(a.power)
        r = np.tanh((za + zb) / np.sqrt(a.n - 3))
        print(f"Correlation, N={a.n}, alpha={a.alpha}, power={a.power}: minimum detectable |r| = {r:.3f} "
              f"(Fisher-z approximation)")
    else:
        f = FTestAnovaPower().solve_power(effect_size=None, nobs=a.n_total, alpha=a.alpha,
                                          power=a.power, k_groups=a.k)
        print(f"One-way ANOVA, k={a.k}, N total={a.n_total}, alpha={a.alpha}, power={a.power}: "
              f"minimum detectable Cohen's f = {f:.3f} (equal group sizes assumed)")
    print("Reminder: this describes sensitivity of the design. It does not say the effect exists, and "
          "it is not valid to compute it from an observed effect after the fact.")


if __name__ == "__main__":
    main()
