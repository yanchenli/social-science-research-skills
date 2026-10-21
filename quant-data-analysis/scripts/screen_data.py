#!/usr/bin/env python3
"""Step 1: data screening. Reports problems; DOES NOT delete anything unless
--exclude rules are given, and every exclusion is written to an exclusion log.

Usage:
  python screen_data.py --file data.csv --dv score --factors condition,gender \
      --id pid [--exclude "attention_check != 1"] [--exclude "duration < 60"] \
      [--outdir out]

Outputs (in --outdir): screening_report.txt, exclusion_log.csv, data_clean.csv
"""
import argparse, os
import numpy as np
import pandas as pd
from common import load_data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--dv", required=True, help="comma-separated DV column(s)")
    ap.add_argument("--factors", default="", help="comma-separated grouping columns")
    ap.add_argument("--id", default=None, help="participant id column")
    ap.add_argument("--exclude", action="append", default=[],
                    help="pandas query string for rows to EXCLUDE; repeatable")
    ap.add_argument("--outdir", default="screen_out")
    a = ap.parse_args()

    os.makedirs(a.outdir, exist_ok=True)
    df = load_data(a.file)
    dvs = [c.strip() for c in a.dv.split(",") if c.strip()]
    factors = [c.strip() for c in a.factors.split(",") if c.strip()]
    for c in dvs + factors + ([a.id] if a.id else []):
        if c not in df.columns:
            raise SystemExit(f"Column not found: {c}. Available: {list(df.columns)}")

    lines = []
    P = lines.append
    P(f"File: {a.file}")
    P(f"Rows: {len(df)}   Columns: {df.shape[1]}")

    # duplicates
    if a.id:
        dup = df[df.duplicated(a.id, keep=False)]
        P(f"\n[Duplicates] duplicated {a.id}: {dup[a.id].nunique()} ids / {len(dup)} rows")
    full_dup = int(df.duplicated().sum())
    P(f"[Duplicates] fully identical rows: {full_dup}")

    # missing
    P("\n[Missing] per analysis variable")
    for c in dvs + factors:
        n_miss = int(df[c].isna().sum())
        P(f"  {c}: {n_miss} missing ({n_miss/len(df):.1%})")

    # exclusions (logged)
    log_rows = []
    work = df.copy()
    work["_row"] = np.arange(len(work))
    for rule in a.exclude:
        try:
            hit = work.query(rule)
        except Exception as e:
            raise SystemExit(f"Bad --exclude rule '{rule}': {e}")
        for _, r in hit.iterrows():
            log_rows.append({"row": int(r["_row"]),
                             "id": r[a.id] if a.id else "",
                             "rule": rule})
        P(f"\n[Exclusion rule] {rule!r}: {len(hit)} rows flagged")
        work = work.drop(hit.index)
    P(f"\nRows after applying {len(a.exclude)} exclusion rule(s): {len(work)}"
      f"  (excluded {len(df)-len(work)})")

    # cell sizes
    if factors:
        cell = work.groupby(factors, dropna=False).size()
        P("\n[Cell sizes]\n" + cell.to_string())
        if cell.min() < 20:
            P("  NOTE: smallest cell < 20 -> assumption checks and effect estimates are shaky.")
        if cell.max() / max(cell.min(), 1) > 1.5:
            P("  NOTE: cell sizes are unbalanced (max/min > 1.5); use Type III SS and check "
              "homogeneity of variance carefully.")

    # per DV: descriptives + outliers (flag only)
    for dv in dvs:
        P(f"\n[DV: {dv}]")
        s = pd.to_numeric(work[dv], errors="coerce")
        if s.isna().sum() > work[dv].isna().sum():
            P("  WARNING: non-numeric entries were coerced to NaN.")
        P(f"  M = {s.mean():.3f}, SD = {s.std():.3f}, min = {s.min():.3f}, max = {s.max():.3f}")
        groups = work.groupby(factors) if factors else [("all", work)]
        flagged = 0
        for key, g in groups:
            x = pd.to_numeric(g[dv], errors="coerce").dropna()
            if len(x) < 4:
                continue
            med = x.median()
            mad = 1.4826 * (x - med).abs().median()          # scaled MAD (consistent with SD under normality)
            if mad == 0:
                continue
            out = x[((x - med).abs() / mad) > 3]
            if len(out):
                flagged += len(out)
                ids = ""
                if a.id:
                    ids = " ids=" + ",".join(map(str, g.loc[out.index, a.id].tolist()))
                P(f"  outliers in cell {key}: {len(out)}{ids}")
        P(f"  total flagged outliers (|x - median| > 3 scaled MADs within cell): {flagged}")
        P("  Flags use the median/MAD rule (robust; mean/SD z-scores are distorted by the very "
          "outliers they try to detect). Flags only: removal is a researcher decision -- decide the "
          "rule BEFORE seeing results if possible, run the analysis with and without, report both.")

    open(os.path.join(a.outdir, "screening_report.txt"), "w", encoding="utf-8").write("\n".join(lines))
    pd.DataFrame(log_rows, columns=["row", "id", "rule"]).to_csv(
        os.path.join(a.outdir, "exclusion_log.csv"), index=False)
    work.drop(columns=["_row"]).to_csv(os.path.join(a.outdir, "data_clean.csv"), index=False)
    print("\n".join(lines))
    print(f"\nWritten to {a.outdir}/: screening_report.txt, exclusion_log.csv, data_clean.csv")


if __name__ == "__main__":
    main()
