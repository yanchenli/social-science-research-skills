#!/usr/bin/env python3
"""prisma_flow.py — PRISMA 2020 流程图的数字核对与生成。

只做两件事：**保证每一格能加得起来**，以及**全文排除的原因有分类计数**。
审稿人最常一眼看出的硬伤就是这两处。

用法
    python prisma_flow.py --identified-db 1240 --identified-other 35 \
        --duplicates 260 --screened-excluded 812 --not-retrieved 11 \
        --assessed-excluded 168 --included-meta 20 \
        --exclusion-reasons '{"非实证研究":45,"自变量或因变量不匹配":60,"效应量无法提取":63}'

推导关系（脚本自行计算，不接受直接指定）：
    screened = identified − duplicates
    sought   = screened − screened_excluded
    assessed = sought − not_retrieved
    included = assessed − assessed_excluded

PRISMA 2020 要求：全文阶段排除的**每一项原因及其频次**都要报。
`--exclusion-reasons` 的合计必须精确等于 `--assessed-excluded`，否则报错。
"""
from __future__ import annotations

import argparse
import json
import sys


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--identified-db", type=int, required=True, help="数据库命中数")
    ap.add_argument("--identified-other", type=int, default=0, help="其他来源命中数")
    ap.add_argument("--duplicates", type=int, default=0, help="去重删除数")
    ap.add_argument("--screened-excluded", type=int, required=True, help="标题摘要阶段排除数")
    ap.add_argument("--not-retrieved", type=int, default=0, help="全文无法获取数")
    ap.add_argument("--assessed-excluded", type=int, required=True, help="全文阶段排除数")
    ap.add_argument("--included-meta", type=int, default=None, help="进入元分析的研究数")
    ap.add_argument("--exclusion-reasons", default=None,
                    help='全文排除原因，JSON 字典，如 \'{"非实证研究":45,"效应量缺失":60}\'')
    ap.add_argument("--json", action="store_true", help="同时输出 JSON")
    args = ap.parse_args()

    identified = args.identified_db + args.identified_other
    screened = identified - args.duplicates
    sought = screened - args.screened_excluded
    assessed = sought - args.not_retrieved
    included = assessed - args.assessed_excluded
    in_meta = args.included_meta if args.included_meta is not None else included

    errors: list[str] = []
    if args.identified_db < 0 or args.identified_other < 0:
        errors.append("命中数不能为负")
    if args.duplicates > identified:
        errors.append(f"去重数 {args.duplicates} 大于总命中数 {identified}")
    if args.screened_excluded > screened:
        errors.append(f"标题摘要排除数 {args.screened_excluded} 大于可筛数 {screened}")
    if args.not_retrieved > sought:
        errors.append(f"无法获取数 {args.not_retrieved} 大于拟获取数 {sought}")
    if args.assessed_excluded > assessed:
        errors.append(f"全文排除数 {args.assessed_excluded} 大于可评估数 {assessed}")
    if in_meta > included:
        errors.append(f"进入元分析数 {in_meta} 大于纳入综述数 {included}")

    # ---- 排除原因：合计必须等于全文排除总数
    reasons: dict[str, int] = {}
    if args.exclusion_reasons:
        try:
            raw = json.loads(args.exclusion_reasons)
        except json.JSONDecodeError as exc:
            errors.append(f"--exclusion-reasons 不是合法 JSON：{exc}")
            raw = {}
        if not isinstance(raw, dict):
            errors.append("--exclusion-reasons 必须是 JSON 对象（原因 → 计数）")
            raw = {}
        reasons = {str(k): int(v) for k, v in raw.items()}
        if any(v < 0 for v in reasons.values()):
            errors.append("排除原因的计数不能为负")
        total = sum(reasons.values())
        if total != args.assessed_excluded:
            errors.append(
                f"全文排除原因合计 {total} 与 --assessed-excluded {args.assessed_excluded} 不一致"
                f"（差 {args.assessed_excluded - total}）")

    if errors:
        print("!! PRISMA 流程图数字对不上：", file=sys.stderr)
        for e in errors:
            print(f"   {e}", file=sys.stderr)
        return 1

    print("=== PRISMA 2020 流程图 ===")
    print("Identification")
    print(f"  数据库命中              n = {args.identified_db}")
    print(f"  其他来源                n = {args.identified_other}")
    print(f"  合计识别                n = {identified}")
    print(f"  去重删除                n = {args.duplicates}")
    print("Screening")
    print(f"  标题摘要筛选            n = {screened}")
    print(f"  此阶段排除              n = {args.screened_excluded}")
    print(f"  拟获取全文              n = {sought}")
    print(f"  全文无法获取            n = {args.not_retrieved}")
    print(f"  全文评估                n = {assessed}")
    print(f"  此阶段排除              n = {args.assessed_excluded}")
    if reasons:
        for name, cnt in sorted(reasons.items(), key=lambda kv: -kv[1]):
            print(f"      · {name:<28} n = {cnt}")
    print("Included")
    print(f"  纳入综述                n = {included}")
    print(f"  进入元分析              n = {in_meta}")
    if in_meta != included:
        print(f"  （差额 {included - in_meta} 项：须在正文说明原因，如效应量无法提取）")
    if not reasons and args.assessed_excluded > 0:
        print("\n⚠️  未提供 --exclusion-reasons。PRISMA 2020 要求报告全文排除的"
              "各项原因及频次，建议补齐。", file=sys.stderr)

    print("\n=== 等式核对（全部成立）===")
    print(f"  {identified} − {args.duplicates} = {screened}      (识别 − 去重 = 可筛)")
    print(f"  {screened} − {args.screened_excluded} = {sought}      (可筛 − 排除 = 拟获取)")
    print(f"  {sought} − {args.not_retrieved} = {assessed}      (拟获取 − 未获取 = 可评估)")
    print(f"  {assessed} − {args.assessed_excluded} = {included}      (可评估 − 排除 = 纳入)")

    print("\n=== Markdown（可直接贴进报告）===")
    print("| 阶段 | 数量 |")
    print("|---|---|")
    print(f"| 数据库命中 | {args.identified_db} |")
    if args.identified_other:
        print(f"| 其他来源命中 | {args.identified_other} |")
    print(f"| 去重后 | {screened} |")
    print(f"| 标题摘要筛选后 | {sought} |")
    print(f"| 全文评估 | {assessed} |")
    print(f"| **纳入综述** | **{included}** |")
    print(f"| **进入元分析** | **{in_meta}** |")

    if reasons:
        print("\n**全文阶段排除原因**\n")
        print("| 排除原因 | 数量 |")
        print("|---|---|")
        for name, cnt in sorted(reasons.items(), key=lambda kv: -kv[1]):
            print(f"| {name} | {cnt} |")
        print(f"| **合计** | **{sum(reasons.values())}** |")

    if args.json:
        print("\n" + json.dumps({
            "identified_db": args.identified_db,
            "identified_other": args.identified_other,
            "identified": identified,
            "duplicates": args.duplicates,
            "screened": screened,
            "screened_excluded": args.screened_excluded,
            "sought": sought,
            "not_retrieved": args.not_retrieved,
            "assessed": assessed,
            "assessed_excluded": args.assessed_excluded,
            "exclusion_reasons": reasons,
            "included": included,
            "included_meta": in_meta,
        }, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
