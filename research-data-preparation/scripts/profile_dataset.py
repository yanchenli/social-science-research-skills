#!/usr/bin/env python3
"""Data profiling for feasibility scouting. READ-ONLY: never modifies the input file.

IMPORTANT: running this IS a form of data exposure. You must declare your current exposure
level first (--current-exposure E0..E4); the run is appended to exposure_log.jsonl together
with the exposure level it implies, so the plan can disclose it honestly.

  python profile_dataset.py --file data.csv --current-exposure E1 \
      [--id customer_id] [--time order_date] [--outcome-vars spend,repeat_purchase] \
      [--level structure|full] [--min-cell 5] [--outdir profile_out]

--level structure : shape, types, missingness, duplicates, ids, record counts over time  -> exposure >= E2
--level full      : + distributions of NON-outcome variables and their missingness drift over time
                      -> exposure >= E3
Outcome variables (--outcome-vars) are BLINDED in both levels: only type and overall missing
count are shown -- no distributions, no trends, no group comparisons. This is the
"blinding to summary statistics" option; it only works if you name the outcomes BEFORE running.
Categorical level counts below --min-cell are suppressed ("<5") to reduce re-identification risk.
Outputs: profile_report.md, profile_summary.json (machine-readable), exposure_log.jsonl (appended).
"""
import argparse, hashlib, json, os, datetime as dt
import numpy as np
import pandas as pd
from common import load_data

LEVELS = ["E0", "E1", "E2", "E3", "E4"]


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def looks_numeric_text(s):
    if s.dtype != object:
        return False
    x = s.dropna().astype(str).str.strip()
    if len(x) == 0:
        return False
    return pd.to_numeric(x, errors="coerce").notna().mean() > 0.9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--current-exposure", required=True, choices=LEVELS)
    ap.add_argument("--id", default=None)
    ap.add_argument("--time", default=None)
    ap.add_argument("--outcome-vars", default="")
    ap.add_argument("--level", default="structure", choices=["structure", "full"])
    ap.add_argument("--min-cell", type=int, default=5)
    ap.add_argument("--max-cat-levels", type=int, default=15)
    ap.add_argument("--outdir", default="profile_out")
    a = ap.parse_args()

    os.makedirs(a.outdir, exist_ok=True)
    df = load_data(a.file)
    outcomes = [c.strip() for c in a.outcome_vars.split(",") if c.strip()]
    for c in outcomes + [x for x in (a.id, a.time) if x]:
        if c not in df.columns:
            raise SystemExit(f"Column not found: {c}. Available: {list(df.columns)}")

    implied = "E2" if a.level == "structure" else "E3"
    after = LEVELS[max(LEVELS.index(a.current_exposure), LEVELS.index(implied))]

    R = {"file": os.path.basename(a.file), "sha256": sha256(a.file), "rows": int(len(df)),
         "columns": int(df.shape[1]), "level": a.level, "outcome_vars_blinded": outcomes,
         "exposure_before": a.current_exposure, "exposure_after": after, "flags": [], "variables": {}}
    flags = R["flags"]
    L = []
    P = L.append
    P(f"# 数据剖面报告\n\n文件：`{R['file']}`（SHA-256 前12位：`{R['sha256'][:12]}`）  \n"
      f"行数：{R['rows']}，列数：{R['columns']}  \n"
      f"剖面级别：**{a.level}**  \n接触等级：{a.current_exposure} → **{after}**（本次运行已记录）")
    if outcomes:
        P(f"\n已盲化的结果变量：{', '.join(outcomes)}（只显示类型与总缺失数）")
    elif a.level == "full":
        P("\n⚠️ 未指定结果变量，`full`级别的分布与趋势包含所有变量，**没有任何变量被盲化**。")
        flags.append("no_blinding_in_full_profile")

    # ---- duplicates and keys
    full_dup = int(df.duplicated().sum())
    R["duplicate_rows"] = full_dup
    P(f"\n## 记录与实体\n\n- 完全重复的行：{full_dup}")
    if full_dup:
        flags.append("duplicate_rows")
    cand = [c for c in df.columns if df[c].notna().all() and df[c].nunique() == len(df)]
    P(f"- 候选主键（全部唯一且无缺失）：{', '.join(cand) if cand else '无'}")
    if a.id:
        n_id = int(df[a.id].nunique())
        per = df.groupby(a.id).size()
        R["ids"] = {"unique": n_id, "rows_per_id_median": float(per.median()), "rows_per_id_max": int(per.max())}
        P(f"- `{a.id}` 唯一值：{n_id}；每个ID的记录数 中位数 {per.median():.0f}，最大 {per.max()}")
        if per.max() > 1:
            P("  - 同一ID有多条记录：**观测单位与分析单位是否一致需要确认**（重复观测/混合粒度）。")
            flags.append("multiple_rows_per_id")

    # ---- per-variable
    P("\n## 变量概况\n")
    P("| 变量 | 类型 | 缺失 | 说明 |\n|---|---|---|---|")
    for c in df.columns:
        s = df[c]
        nmiss = int(s.isna().sum())
        info = {"dtype": str(s.dtype), "missing": nmiss, "missing_pct": round(nmiss / len(df), 4)}
        notes = []
        if c in outcomes:
            notes.append("盲化")
        else:
            if s.nunique(dropna=True) <= 1:
                notes.append("常量列")
                flags.append(f"constant:{c}")
            if looks_numeric_text(s):
                notes.append("数字存成了文本")
                flags.append(f"numeric_as_text:{c}")
            if a.level == "full" and c == a.id:
                notes.append("标识符，不做分布统计")
            elif a.level == "full":
                if pd.api.types.is_numeric_dtype(s) and not pd.api.types.is_bool_dtype(s):
                    q = s.quantile([.01, .5, .99])
                    info.update({"p01": float(q.iloc[0]), "median": float(q.iloc[1]), "p99": float(q.iloc[2]),
                                 "zero_rate": round(float((s == 0).mean()), 4)})
                    notes.append(f"P1={q.iloc[0]:.3g}, 中位数={q.iloc[1]:.3g}, P99={q.iloc[2]:.3g}, "
                                 f"零值率={(s == 0).mean():.1%}")
                elif s.nunique(dropna=True) <= a.max_cat_levels and c != a.time:
                    vc = s.value_counts(dropna=False)
                    shown = {str(k): (int(v) if v >= a.min_cell else f"<{a.min_cell}") for k, v in vc.items()}
                    info["levels"] = shown
                    notes.append("; ".join(f"{k}:{v}" for k, v in list(shown.items())[:8]))
        R["variables"][c] = info
        P(f"| {c} | {s.dtype} | {nmiss} ({nmiss / len(df):.1%}) | {'; '.join(notes)} |")
    if a.level == "full":
        P(f"\n（数值型只给 P1/中位数/P99，不给最小/最大值；分类水平计数小于 {a.min_cell} 的以“<{a.min_cell}”显示。）")

    # ---- time
    if a.time:
        t_raw = pd.to_datetime(df[a.time], errors="coerce")
        bad = int(t_raw.isna().sum() - df[a.time].isna().sum())
        P(f"\n## 时间覆盖（`{a.time}`）\n")
        if bad:
            P(f"- ⚠️ {bad} 个值无法解析为日期")
            flags.append(f"unparseable_dates:{a.time}")
        t = t_raw.dropna()
        if len(t):
            m = t.dt.to_period("M").value_counts().sort_index()
            full_idx = pd.period_range(m.index.min(), m.index.max(), freq="M")
            m = m.reindex(full_idx, fill_value=0)
            R["time"] = {"start": str(t.min().date()), "end": str(t.max().date()), "months": int(len(m))}
            P(f"- 范围：{t.min().date()} 至 {t.max().date()}（{len(m)} 个月）")
            zero = [str(p) for p, v in m.items() if v == 0]
            if zero:
                P(f"- 记录数为0的月份：{', '.join(zero)}")
                flags.append("empty_months")
            med = m.median()
            mad = 1.4826 * (m - med).abs().median()
            odd = [(str(p), int(v)) for p, v in m.items() if mad > 0 and abs(v - med) / mad > 3]
            R["time"]["volume_anomalies"] = odd
            if odd:
                P("- 月度记录数明显偏离中位数的月份（>3个MAD）：" + "，".join(f"{p}（{v}）" for p, v in odd))
                P("  - 这是**可能的结构性断裂**线索（口径变化、政策或外部事件、采集中断），"
                  "需要在计划里说明如何处理，而不是事后看结果再决定。")
                flags.append("volume_anomaly")
            P("\n| 月份 | 记录数 |\n|---|---|")
            for p, v in m.items():
                P(f"| {p} | {int(v)} |")
            if a.level == "full":
                drift = []
                q = t_raw.dt.to_period("Q")
                for c in df.columns:
                    if c in outcomes or c == a.time:
                        continue
                    miss = df[c].isna().groupby(q).mean().dropna()
                    if len(miss) >= 3 and (miss.max() - miss.min()) > 0.2:
                        drift.append((c, float(miss.min()), float(miss.max())))
                R["time"]["missingness_drift"] = drift
                if drift:
                    P("\n**缺失率随时间明显变化的变量**（季度缺失率最大差超过20个百分点）：")
                    for c, lo, hi in drift:
                        P(f"- `{c}`：{lo:.0%} → {hi:.0%}")
                    flags.append("missingness_drift")

    P("\n## 风险提示（线索，不是结论）\n")
    if flags:
        names = {"duplicate_rows": "存在完全重复的记录", "multiple_rows_per_id": "同一ID多条记录，需确认分析单位",
                 "volume_anomaly": "月度记录数异常，可能存在结构性断裂", "empty_months": "存在无记录的月份",
                 "missingness_drift": "某些变量缺失率随时间变化，可能是采集口径变化",
                 "no_blinding_in_full_profile": "full剖面未盲化任何变量",
                 "constant": "常量列", "numeric_as_text": "数字存成了文本", "unparseable_dates": "日期无法解析"}
        for f in sorted(set(flags)):
            key = f.split(":")[0]
            P(f"- {names.get(key, key)}" + (f"（{f.split(':')[1]}）" if ":" in f else ""))
    else:
        P("- 未发现上述类型的明显问题（不代表数据没有问题：本脚本只检查结构与完整性，不检查构念效度和数据生成机制）。")
    P("\n> 本报告不判断数据“好”或“不好”，也不检查变量是否真的测量了你的构念。"
      "它只提供可复核的证据，用于填写计划中的 `evidence_status`。")

    open(os.path.join(a.outdir, "profile_report.md"), "w", encoding="utf-8").write("\n".join(L))
    json.dump(R, open(os.path.join(a.outdir, "profile_summary.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    entry = {"timestamp": dt.datetime.now().isoformat(timespec="seconds"), "file": R["file"], "sha256": R["sha256"],
             "level": a.level, "outcome_vars_blinded": outcomes, "exposure_before": a.current_exposure,
             "exposure_after": after, "args": {k: v for k, v in vars(a).items()}}
    with open(os.path.join(a.outdir, "exposure_log.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print("\n".join(L))
    print(f"\n[记录] 接触等级 {a.current_exposure} -> {after}，已写入 {a.outdir}/exposure_log.jsonl")


if __name__ == "__main__":
    main()
