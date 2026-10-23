#!/usr/bin/env python3
"""meta.py — 系统综述的效应量换算与合成（Hedges-Olkin 反方差范式）。

支持四类输入，统一换算到「可加权的效应量 + 方差」后再合成：

    r     Fisher's z = atanh(r),        var = 1/(n-3)
    d     换算为 Hedges' g（小样本校正）,  var 由 n1/n2 与 g 估计
    or    log OR,                       var = 1/a + 1/b + 1/c + 1/d
    t     由 t 与 df 换算偏相关 r_p = t/sqrt(t^2+df)，var = (1-r_p^2)^2/(df)
    path  直接使用给定的 beta 与 se

**输出同时给两个尺度**：运算尺度（Fisher's z / lnOR）与原始尺度（r / OR）。
原始尺度才是能直接写进论文的数字——这是 v1.0.0 的一个真缺陷，已修。

输出：固定效应、随机效应（DL / REML / Paule-Mandel）、异质性（Q / I² / τ² / H²）、
Hartung-Knapp 区间、预测区间、Egger 检验、PET-PEESE（含决策建议）。

用法
    python meta.py --file studies.csv --type r --out report.json
    python meta.py --file studies.csv --type d --d-is-g
    python meta.py --file studies.csv --type t

设计约束
--------
- **不猜列名**：缺列直接报错，不填默认值。
- **不隐藏小样本问题**：k < 5 警告，k < 3 不做异质性与发表偏倚检验。
- **不掩盖非独立性**：同一 study 名出现多次时明确警告（会低估标准误）。
- **不做 trim-and-fill**：假定对称、易过度校正；改用 Egger + PET-PEESE 并说明理由。
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter
from dataclasses import dataclass, asdict

try:
    from scipy import stats as st
    from scipy.optimize import brentq, minimize_scalar
except ImportError:  # pragma: no cover
    print("需要 scipy：pip install scipy", file=sys.stderr)
    raise SystemExit(2)


@dataclass
class Study:
    name: str
    yi: float          # 运算尺度的效应量
    vi: float          # 其方差
    raw: float         # 原始报告的效应量（便于回查）
    n: float | None = None


def _get(row: dict, key: str) -> float:
    if key not in row or row[key].strip() == "":
        raise SystemExit(f"缺列或空值：{key}（该行：{row}）")
    return float(row[key])


def load(path: str, etype: str, d_is_g: bool = False) -> list[Study]:
    out: list[Study] = []
    with open(path, newline="", encoding="utf-8-sig") as fh:
        for i, row in enumerate(csv.DictReader(fh), start=2):
            name = (row.get("study") or f"row{i}").strip()
            if etype == "r":
                r, n = _get(row, "r"), _get(row, "n")
                if not (-1 < r < 1):
                    raise SystemExit(f"{name}: r 必须在 (-1,1) 内，得到 {r}")
                if n <= 3:
                    raise SystemExit(f"{name}: n 必须 > 3（Fisher z 的方差为 1/(n-3)）")
                out.append(Study(name, math.atanh(r), 1.0 / (n - 3), r, n))
            elif etype == "d":
                d, n1, n2 = _get(row, "d"), _get(row, "n1"), _get(row, "n2")
                df = n1 + n2 - 2
                if df <= 0:
                    raise SystemExit(f"{name}: n1+n2 必须 > 2")
                j = 1.0 - 3.0 / (4.0 * df - 1.0)      # Hedges 小样本校正
                g = d if d_is_g else d * j            # 原文已报 g 时不要再乘一次 J
                var = (n1 + n2) / (n1 * n2) + g * g / (2.0 * (n1 + n2))
                out.append(Study(name, g, var, d, n1 + n2))
            elif etype == "or":
                a, b, c, dd = (_get(row, k) for k in ("a", "b", "c", "d"))
                if min(a, b, c, dd) <= 0:
                    raise SystemExit(f"{name}: 2×2 四格都需 > 0（含 0 需连续性校正，本脚本不做）")
                out.append(Study(name, math.log(a * dd / (b * c)),
                                 1.0 / a + 1.0 / b + 1.0 / c + 1.0 / dd,
                                 (a * dd) / (b * c)))
            elif etype == "t":
                t, df = _get(row, "t"), _get(row, "df")
                if df <= 0:
                    raise SystemExit(f"{name}: df 必须 > 0")
                rp = t / math.sqrt(t * t + df)        # 偏相关
                out.append(Study(name, math.atanh(rp),
                                 (1 - rp * rp) ** 2 / df if df > 0 else float("nan"),
                                 rp, df + 2))
            elif etype == "path":
                beta, se = _get(row, "beta"), _get(row, "se")
                if se <= 0:
                    raise SystemExit(f"{name}: se 必须 > 0")
                out.append(Study(name, beta, se * se, beta))
            else:
                raise SystemExit(f"未知 --type：{etype}")
    if not out:
        raise SystemExit("没有可用数据行")
    return out


def back_transform(val: float, etype: str) -> float:
    """把运算尺度还原成可读尺度：z → r，lnOR → OR。其余原样。"""
    if val is None or (isinstance(val, float) and math.isnan(val)):
        return float("nan")
    if etype == "r":
        return math.tanh(val)
    if etype in ("or",):
        return math.exp(val)
    return val


def scale_label(etype: str) -> tuple[str, str]:
    """返回 (运算尺度名, 原始尺度名)。"""
    if etype == "r":
        return "Fisher's z", "r"
    if etype == "or":
        return "ln(OR)", "OR"
    if etype == "t":
        return "Fisher's z(偏相关)", "偏相关 r_p"
    if etype == "d":
        return "Hedges' g", "Hedges' g"
    return "β", "β"


def q_stat(y: list[float], w: list[float]) -> float:
    ybar = sum(wi * yi for wi, yi in zip(w, y)) / sum(w)
    return sum(wi * (yi - ybar) ** 2 for wi, yi in zip(w, y))


def tau2_dl(q: float, w: list[float], k: int) -> float:
    c = sum(w) - sum(wi * wi for wi in w) / sum(w)
    return max(0.0, (q - (k - 1)) / c) if c > 0 else 0.0


def _pool(y: list[float], v: list[float], t2: float) -> tuple[float, float]:
    w = [1.0 / (vi + t2) for vi in v]
    return sum(wi * yi for wi, yi in zip(w, y)) / sum(w), math.sqrt(1.0 / sum(w))


def tau2_pm(y: list[float], v: list[float]) -> float:
    """Paule-Mandel：解 Q(τ²) = k−1。非迭代似然，非正态下比 REML 稳。"""
    k = len(y)
    if k < 2:
        return 0.0

    def gap(t2: float) -> float:
        w = [1.0 / (vi + t2) for vi in v]
        return q_stat(y, w) - (k - 1)

    lo, hi = 0.0, max(1.0, 10.0 * max(v), 4.0 * (max(y) - min(y)) ** 2)
    if gap(lo) <= 0:
        return 0.0
    for _ in range(60):                     # 先扩张上界，避免截断
        if gap(hi) > 0:
            hi *= 2.0
        else:
            break
    try:
        return max(0.0, brentq(gap, lo, hi, xtol=1e-10, rtol=1e-10))
    except (ValueError, RuntimeError):
        return 0.0


def tau2_reml(y: list[float], v: list[float]) -> float:
    """REML 的 τ²：对限制似然做一维最小化；上界自适应，避免截断。"""
    k = len(y)
    if k < 2:
        return 0.0

    def neg_reml(t2: float) -> float:
        w = [1.0 / (vi + t2) for vi in v]
        sw = sum(w)
        ybar = sum(wi * yi for wi, yi in zip(w, y)) / sw
        return 0.5 * (sum(math.log(vi + t2) for vi in v) + math.log(sw)
                      + sum(wi * (yi - ybar) ** 2 for wi, yi in zip(w, y)))

    spread = (max(y) - min(y)) ** 2
    hi = max(1.0, 10.0 * max(v), 4.0 * spread)
    res = minimize_scalar(neg_reml, bounds=(0.0, hi), method="bounded")
    if res.x >= hi * 0.999:                 # 触到上界 → 再放宽一次
        res = minimize_scalar(neg_reml, bounds=(0.0, hi * 10), method="bounded")
    return max(0.0, float(res.x))


def hk_ci(y: list[float], v: list[float], t2: float, alpha: float):
    """Hartung-Knapp 校正（k 小时比正态近似稳）。"""
    k = len(y)
    w = [1.0 / (vi + t2) for vi in v]
    est = sum(wi * yi for wi, yi in zip(w, y)) / sum(w)
    q = sum(wi * (yi - est) ** 2 for wi, yi in zip(w, y))
    if k < 2:
        return est, float("nan"), float("nan")
    se_hk = math.sqrt(q / ((k - 1) * sum(w)))
    tcrit = float(st.t.ppf(1 - alpha / 2, k - 1))
    return est, est - tcrit * se_hk, est + tcrit * se_hk


def prediction_interval(est: float, se: float, t2: float, k: int, alpha: float):
    if k < 3:
        return float("nan"), float("nan")
    tcrit = float(st.t.ppf(1 - alpha / 2, k - 2))
    half = tcrit * math.sqrt(t2 + se * se)
    return est - half, est + half


def egger(y: list[float], v: list[float]):
    """Egger：以精度 1/se 回归标准化离差 SND=y/se，检验截距是否为 0。"""
    k = len(y)
    if k < 3:
        return None
    snd = [yi / math.sqrt(vi) for yi, vi in zip(y, v)]
    prec = [1.0 / math.sqrt(vi) for vi in v]
    res = st.linregress(prec, snd)
    return {"intercept": float(res.intercept), "se": float(res.intercept_stderr),
            "t": float(res.intercept / res.intercept_stderr),
            "df": k - 2,
            "p": 2 * (1 - float(st.t.cdf(abs(res.intercept / res.intercept_stderr), k - 2)))}


def pet_peese(y: list[float], v: list[float]):
    """PET 用 se 作自变量，PEESE 用方差；都以 1/v 加权，看截距（精度趋于无穷时的效应）。"""
    k = len(y)
    if k < 3:
        return None
    out = {}
    for label, x in (("PET", [math.sqrt(vi) for vi in v]), ("PEESE", v)):
        wts = [1.0 / vi for vi in v]
        sw = sum(wts)
        xbar = sum(wi * xi for wi, xi in zip(wts, x)) / sw
        ybar = sum(wi * yi for wi, yi in zip(wts, y)) / sw
        sxx = sum(wi * (xi - xbar) ** 2 for wi, xi in zip(wts, x))
        sxy = sum(wi * (xi - xbar) * (yi - ybar) for wi, xi, yi in zip(wts, x, y))
        slope = sxy / sxx if sxx > 0 else float("nan")
        intercept = ybar - slope * xbar
        resid = [yi - (intercept + slope * xi) for xi, yi in zip(x, y)]
        df = k - 2
        mse = sum(wi * r * r for wi, r in zip(wts, resid)) / df if df > 0 else float("nan")
        se_int = math.sqrt(mse * (1.0 / sw + xbar ** 2 / sxx)) if sxx > 0 and df > 0 else float("nan")
        t = intercept / se_int if se_int and se_int > 0 else float("nan")
        p = 2 * (1 - float(st.t.cdf(abs(t), df))) if se_int and se_int > 0 else float("nan")
        out[label] = {"intercept": intercept, "se": se_int, "t": t, "p": p}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--file", required=True)
    ap.add_argument("--type", required=True, choices=["r", "d", "or", "t", "path"])
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--pet-alpha", type=float, default=0.10,
                    help="PET-PEESE 决策阈值（默认 0.10，可改）")
    ap.add_argument("--d-is-g", action="store_true",
                    help="输入已是 Hedges' g 时加上，避免再乘一次小样本校正")
    ap.add_argument("--out")
    args = ap.parse_args()

    studies = load(args.file, args.type, args.d_is_g)
    y = [s.yi for s in studies]
    v = [s.vi for s in studies]
    k = len(studies)
    op_label, raw_label = scale_label(args.type)

    w_fe = [1.0 / vi for vi in v]
    est_fe = sum(wi * yi for wi, yi in zip(w_fe, y)) / sum(w_fe)
    se_fe = math.sqrt(1.0 / sum(w_fe))
    q = q_stat(y, w_fe)
    df = k - 1
    i2 = max(0.0, (q - df) / q) if q > 0 else 0.0
    h2 = q / df if df > 0 else float("nan")

    t2_dl = tau2_dl(q, w_fe, k)
    t2_pm = tau2_pm(y, v) if k >= 2 else 0.0
    t2_reml = tau2_reml(y, v) if k >= 2 else 0.0

    est_dl, se_dl = _pool(y, v, t2_dl)
    est_pm, se_pm = _pool(y, v, t2_pm)
    est_re, se_re = _pool(y, v, t2_reml)
    est_hk, lo_hk, hi_hk = hk_ci(y, v, t2_reml, args.alpha)
    lo_pi, hi_pi = prediction_interval(est_re, se_re, t2_reml, k, args.alpha)
    z = float(st.norm.ppf(1 - args.alpha / 2))

    ci_re = (est_re - z * se_re, est_re + z * se_re)
    egg = egger(y, v)
    pp = pet_peese(y, v)

    # ---- PET-PEESE 决策链（Stanley & Doucouliagos）
    decision = None
    if pp:
        if pp["PET"]["p"] < args.pet_alpha:
            chosen, why = "PEESE", (f"PET 截距显著（p={pp['PET']['p']:.3f} < {args.pet_alpha}），"
                                    "说明存在非零真效应；PET 在此情形会过度向下校正，改用 PEESE")
        else:
            chosen, why = "PET", (f"PET 截距不显著（p={pp['PET']['p']:.3f} ≥ {args.pet_alpha}），"
                                  "无充分证据表明存在非零真效应，采用更保守的 PET 截距")
        decision = {"recommended": chosen, "rule": why,
                    "corrected_estimate": pp[chosen]["intercept"],
                    "corrected_estimate_original_scale":
                        back_transform(pp[chosen]["intercept"], args.type),
                    "p_value": pp[chosen]["p"]}

    result = {
        "type": args.type,
        "operational_scale": op_label,
        "original_scale": raw_label,
        "k": k,
        "fixed_effect": {"estimate": est_fe, "se": se_fe,
                         "ci": [est_fe - z * se_fe, est_fe + z * se_fe]},
        "random_DL": {"estimate": est_dl, "se": se_dl, "tau2": t2_dl},
        "random_PM": {"estimate": est_pm, "se": se_pm, "tau2": t2_pm},
        "random_REML": {"estimate": est_re, "se": se_re, "ci": list(ci_re),
                        "hk_ci": [lo_hk, hi_hk], "tau2": t2_reml,
                        "estimate_original_scale": back_transform(est_re, args.type),
                        "ci_original_scale": [back_transform(ci_re[0], args.type),
                                              back_transform(ci_re[1], args.type)],
                        "hk_ci_original_scale": [back_transform(lo_hk, args.type),
                                                 back_transform(hi_hk, args.type)]},
        "heterogeneity": {"Q": q, "df": df,
                          "p": 1 - float(st.chi2.cdf(q, df)) if df > 0 else float("nan"),
                          "I2": i2, "H2": h2},
        "prediction_interval": [lo_pi, hi_pi],
        "prediction_interval_original_scale": [back_transform(lo_pi, args.type),
                                               back_transform(hi_pi, args.type)],
        "egger": egg,
        "pet_peese": pp,
        "bias_correction_recommendation": decision,
        "studies": [asdict(s) for s in studies],
        "warnings": [],
    }

    dup = [n for n, c in Counter(s.name for s in studies).items() if c > 1]
    if dup:
        result["warnings"].append(
            f"同一研究名出现多次：{dup}。本脚本假定各行为独立观测——"
            "同一论文的多个效应量会使标准误被低估、假阳性率上升。"
            "请先在文内聚合（取均值或选最优指标），或改用 R 的 metafor::rma.mv / robumeta 做多层或 RVE")
    if k < 3:
        result["warnings"].append(f"k={k}：样本过少，不做异质性与发表偏倚检验，结论仅作描述")
    elif k < 5:
        result["warnings"].append(f"k={k}：小样本元分析，I² 与 τ² 估计不稳，Egger 功效低")
    if any(vi <= 0 for vi in v):
        result["warnings"].append("存在非正方差，请检查原始数据")
    if k >= 3 and q < df:
        result["warnings"].append(
            "Q < df：异质性低于抽样波动预期。HK 区间此时可能比常规区间更窄，"
            "应以常规 RE 区间为主，HK 仅作敏感性分析")

    # ---------------- 打印 ----------------
    print(f"=== 元分析：{k} 项研究 | 类型 {args.type} | 运算尺度 {op_label} ===")
    print(f"固定效应        : {est_fe: .4f}  SE={se_fe:.4f}  "
          f"95%CI [{est_fe - z * se_fe: .4f}, {est_fe + z * se_fe: .4f}]")
    print(f"随机 DL         : {est_dl: .4f}  τ²={t2_dl:.4f}")
    print(f"随机 Paule-Mandel: {est_pm: .4f}  τ²={t2_pm:.4f}")
    print(f"随机 REML       : {est_re: .4f}  SE={se_re:.4f}  τ²={t2_reml:.4f}")
    print(f"  HK 校正 CI    : [{lo_hk: .4f}, {hi_hk: .4f}]")
    print(f"异质性          : Q={q:.3f}  df={df}  I²={i2 * 100:.1f}%  H²={h2:.3f}")
    if not math.isnan(lo_pi):
        print(f"预测区间        : [{lo_pi: .4f}, {hi_pi: .4f}]")

    if op_label != raw_label:
        print(f"\n=== 原始尺度（{raw_label}，可直接写入论文）===")
        print(f"随机效应 REML   : {back_transform(est_re, args.type): .4f}  "
              f"95%CI [{back_transform(ci_re[0], args.type): .4f}, "
              f"{back_transform(ci_re[1], args.type): .4f}]")
        if not math.isnan(lo_hk):
            print(f"  HK 校正 CI    : [{back_transform(lo_hk, args.type): .4f}, "
                  f"{back_transform(hi_hk, args.type): .4f}]")
        if not math.isnan(lo_pi):
            print(f"预测区间        : [{back_transform(lo_pi, args.type): .4f}, "
                  f"{back_transform(hi_pi, args.type): .4f}]")

    if egg:
        print(f"\nEgger 截距      : {egg['intercept']: .4f}  t={egg['t']:.3f}  p={egg['p']:.4f}")
    if pp:
        print(f"PET  截距       : {pp['PET']['intercept']: .4f}  p={pp['PET']['p']:.4f}")
        print(f"PEESE 截距      : {pp['PEESE']['intercept']: .4f}  p={pp['PEESE']['p']:.4f}")
    if decision:
        print(f"\n偏倚校正建议    : 用 {decision['recommended']}")
        print(f"  理由          : {decision['rule']}")
        print(f"  校正后估计    : {decision['corrected_estimate']: .4f}"
              + (f"（{raw_label} = {decision['corrected_estimate_original_scale']: .4f}）"
                 if op_label != raw_label else ""))

    for wmsg in result["warnings"]:
        print(f"⚠️  {wmsg}", file=sys.stderr)

    if args.out:
        with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=1)
        print(f"\n结果已写入 {args.out}")
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
