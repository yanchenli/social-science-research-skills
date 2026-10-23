#!/usr/bin/env python3
"""hs_meta.py — Hunter-Schmidt 心理测量元分析（QMA）。

为什么需要单独一个脚本
----------------------
微观商科（OB / HRM / 工业组织心理）的主流范式是 Hunter-Schmidt，不是 Hedges-Olkin：

- **做测量误差校正**：把观测相关 r 校正为潜在相关 ρ = r / sqrt(r_xx · r_yy)；
- **按样本量加权**（不是反方差加权）；
- **报可信区间（credibility interval）**，基于校正后真相关的标准差 σ_ρ，
  与基于抽样误差的置信区间、预测区间概念不同。

这些与 meta.py 的假设不兼容，所以分开实现，而不是塞进同一个脚本。

输入列
------
    study, r, n, rxx, ryy
    rxx / ryy 为两个变量的信度（Cronbach's α 或复合信度）。
    若某研究未报信度，可用该构念在本领域的**平均信度**（须在报告中说明，
    并做「未校正 vs 校正」的敏感性分析）。

用法
    python hs_meta.py --file studies.csv
    python hs_meta.py --file studies.csv --rho-xx .85 --rho-yy .88   # 用领域平均信度
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass, asdict

try:
    from scipy import stats as st
except ImportError:  # pragma: no cover
    print("需要 scipy：pip install scipy", file=sys.stderr)
    raise SystemExit(2)


@dataclass
class Row:
    name: str
    r: float
    n: float
    rxx: float
    ryy: float
    rho: float          # 校正后相关
    a: float            # 校正因子 sqrt(rxx*ryy)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--rho-xx", type=float, default=None, help="缺信度时用的领域平均 rxx")
    ap.add_argument("--rho-yy", type=float, default=None, help="缺信度时用的领域平均 ryy")
    ap.add_argument("--cred", type=float, default=0.80, help="可信区间宽度（默认 80%%）")
    ap.add_argument("--out", default=None, help="结果写入 JSON")
    args = ap.parse_args()

    rows: list[Row] = []
    with open(args.file, newline="", encoding="utf-8-sig") as fh:
        for i, row in enumerate(csv.DictReader(fh), start=2):
            name = (row.get("study") or f"row{i}").strip()
            try:
                r = float(row["r"]); n = float(row["n"])
            except (KeyError, ValueError):
                raise SystemExit(f"{name}: 需要 r 与 n 两列且为数值")
            rxx_s, ryy_s = (row.get("rxx") or "").strip(), (row.get("ryy") or "").strip()
            rxx = float(rxx_s) if rxx_s else args.rho_xx
            ryy = float(ryy_s) if ryy_s else args.rho_yy
            if rxx is None or ryy is None:
                raise SystemExit(f"{name}: 缺 rxx/ryy，且未给 --rho-xx/--rho-yy")
            if not (0 < rxx <= 1 and 0 < ryy <= 1):
                raise SystemExit(f"{name}: 信度必须在 (0,1] 内，得到 {rxx}, {ryy}")
            a = math.sqrt(rxx * ryy)
            rows.append(Row(name, r, n, rxx, ryy, r / a, a))

    k = len(rows)
    if k < 3:
        print(f"⚠️  k={k}：可信区间与方差分解不稳，仅作描述", file=sys.stderr)

    # ---- 未校正：按 n 加权的 r
    sw = sum(x.n for x in rows)
    r_bar = sum(x.n * x.r for x in rows) / sw
    var_r = sum(x.n * (x.r - r_bar) ** 2 for x in rows) / sw
    var_e = sum(x.n * (1 - x.r ** 2) ** 2 / (x.n - 1) for x in rows) / sw
    var_rho_obs = max(0.0, var_r - var_e)
    sd_r_obs = math.sqrt(var_r)
    ci_r = (r_bar - 1.96 * sd_r_obs / math.sqrt(k), r_bar + 1.96 * sd_r_obs / math.sqrt(k))

    # ---- 校正后：按 n 加权的 ρ
    rho_bar = sum(x.n * x.rho for x in rows) / sw
    var_rho_total = sum(x.n * (x.rho - rho_bar) ** 2 for x in rows) / sw
    # 校正后的抽样误差方差（近似）：var_e / (a^2 的加权均值)
    a2_bar = sum(x.n * x.a ** 2 for x in rows) / sw
    var_e_corr = var_e / a2_bar
    var_rho_res = max(0.0, var_rho_total - var_e_corr)
    sd_rho = math.sqrt(var_rho_res)

    # 80% 可信区间：ρ 的分布，不含估计本身的不确定性
    zc = float(st.norm.ppf(0.5 + args.cred / 2))
    cred_lo, cred_hi = rho_bar - zc * sd_rho, rho_bar + zc * sd_rho

    # 抽样误差可解释的方差比例
    pv_art = (var_e_corr / var_rho_total * 100) if var_rho_total > 0 else float("nan")

    print(f"=== Hunter-Schmidt 心理测量元分析：{k} 项研究 ===")
    print(f"总样本量            : {int(sw):,d}")
    print()
    print("【未校正】")
    print(f"  样本量加权 r      : {r_bar: .4f}")
    print(f"  观测方差          : {var_r:.5f}（SD = {math.sqrt(var_r):.4f}）")
    print(f"  95% 置信区间      : [{ci_r[0]: .4f}, {ci_r[1]: .4f}]")
    print()
    print("【测量误差校正后】")
    print(f"  校正后 ρ（均值）  : {rho_bar: .4f}")
    print(f"  校正后总方差      : {var_rho_total:.5f}")
    print(f"  抽样误差方差      : {var_e_corr:.5f}")
    print(f"  真方差 σ_ρ²       : {var_rho_res:.5f}（σ_ρ = {sd_rho:.4f}）")
    if sd_rho > 0:
        print(f"  {int(args.cred * 100)}% 可信区间      : [{cred_lo: .4f}, {cred_hi: .4f}]")
    else:
        print(f"  {int(args.cred * 100)}% 可信区间      : 无法估计（真方差估计为 0）")
    if math.isnan(pv_art) or pv_art > 100:
        print("  抽样误差可解释比例: >100% —— 观测方差小于抽样误差预期。")
        print("                      提示真实异质极小，或存在范围限制/截断；此时可信区间不具解释力。")
    else:
        print(f"  抽样误差可解释比例: {pv_art:.1f}%")
    print()
    print("【三个区间别搞混】")
    print("  置信区间（CI）   ：ρ 均值的抽样不确定性——回答「这个均值估得准不准」")
    print(f"  可信区间（CV）   ：真相关 ρ 的分布范围——回答「不同情境下效应会不会变号」")
    print("  预测区间（PI）   ：未来一项研究的观测值范围——含抽样误差，比 CV 更宽")
    print()
    print("提示：若 CV 包含 0 或跨过 0，说明「效应可能在某些情境下不存在或反向」，")
    print("      这本身是有价值的结论，不要因为均值显著就忽略它。")

    if args.rho_xx or args.rho_yy:
        print(f"\n⚠️  部分研究使用了领域平均信度（rxx={args.rho_xx}, ryy={args.rho_yy}），"
              "须在报告中说明，并做「未校正 vs 校正」的敏感性分析。", file=sys.stderr)

    out = {"k": k, "n_total": int(sw),
           "uncorrected": {"r_bar": r_bar, "var": var_r, "ci": list(ci_r)},
           "corrected": {"rho_bar": rho_bar, "var_total": var_rho_total,
                         "var_sampling": var_e_corr, "var_residual": var_rho_res,
                         "sd_rho": sd_rho,
                         "credibility_interval": [cred_lo, cred_hi]},
           "rows": [asdict(r) for r in rows]}
    if args.out:
        import json
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=1)
        print(f"\n结果已写入 {args.out}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
