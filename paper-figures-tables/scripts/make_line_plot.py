"""多系列折线图（可带置信带）。交互效应图共用 line_core 的画法。

用法：
    python scripts/make_line_plot.py fig2a.svg spec.json
    python scripts/make_line_plot.py fig2a.svg spec.json --export pdf,png --dpi 600

规格见 references/line-plots.md。三条以上系列时不要靠颜色区分——
黑白印刷会把它们印成三条一样的灰线，用线型与标记。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import line_core  # noqa: E402
from mpl_backend import summarize  # noqa: E402


def validate(spec: dict) -> list[str]:
    errs: list[str] = []
    series = spec.get("series")
    if not isinstance(series, list) or not series:
        return ["series 必须是非空数组"]
    if len(series) > 4 and not spec.get("markers") and spec.get("legend") == "end":
        errs.append("系列超过 4 条：线型只有 4 种，建议开 markers 或改用小多图")
    labels = [s.get("label", "") for s in series]
    if any(not x for x in labels):
        errs.append("每条系列都要有 label——线端标注或图例都靠它")
    if len(set(labels)) != len(labels):
        errs.append(f"系列标签重复：{labels}")
    for i, s in enumerate(series, 1):
        if ("lo" in s) != ("hi" in s):
            errs.append(f"第 {i} 条只给了 lo 或 hi 之一——置信带需要同时给两端")
        if "lo" in s and len(s["lo"]) != len(s.get("x", [])):
            errs.append(f"第 {i} 条的 lo 长度与 x 不同")
        if "hi" in s and len(s["hi"]) != len(s.get("x", [])):
            errs.append(f"第 {i} 条的 hi 长度与 x 不同")
    # 纵轴范围：有自然边界的量（李克特、百分比）应当显式给
    if not spec.get("y_range"):
        vals = [v for s in series for v in s.get("y", [])]
        if vals and 0 <= min(vals) and max(vals) <= 7.01 and min(vals) > 2.5:
            errs.append("数值都在 2.5–7 之间，像是李克特量表——"
                        "建议给 y_range: [1, 7]，否则按数据范围缩放会放大差异")
    return errs


def build(spec: dict) -> tuple:
    warns = validate(spec)
    return line_core.build(spec), warns


def main() -> int:
    ap = argparse.ArgumentParser(description="多系列折线图 → SVG（可另出 PDF/PNG）")
    ap.add_argument("out", help="输出 .svg 路径")
    ap.add_argument("spec", nargs="?", help="规格 .json")
    ap.add_argument("--data", help="从 CSV 读数据（与 --x --y --by 配合）")
    ap.add_argument("--x", help="CSV 的 x 列名")
    ap.add_argument("--y", help="CSV 的 y 列名")
    ap.add_argument("--by", help="CSV 的系列列名")
    ap.add_argument("--xlabel")
    ap.add_argument("--ylabel")
    ap.add_argument("--note")
    ap.add_argument("--width", type=float)
    ap.add_argument("--height", type=float)
    ap.add_argument("--lang", choices=["en", "zh"], default="en")
    ap.add_argument("--export", help="另存矢量/位图，如 pdf,png")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--gray", action="store_true", help="按灰度导出，核对黑白印刷")
    ap.add_argument("--validate", action="store_true", help="只校验规格，不画图")
    args = ap.parse_args()

    if args.spec:
        from qc import load_spec
        spec = load_spec(args.spec, required=("series",))
    elif args.data:
        spec = _from_csv(args)
    else:
        ap.error("要么给 spec.json，要么给 --data 加 --x --y --by")
    for k in ("xlabel", "ylabel", "note", "width", "height"):
        if getattr(args, k) is not None:
            spec[k] = getattr(args, k)

    errs = validate(spec)
    if args.validate:
        if errs:
            print("规格有问题：")
            for e in errs:
                print("  ✗", e)
            return 1
        print("✓ 规格通过")
        return 0

    svg, warns = build(spec)
    out = svg.save(args.out)
    print(f"已生成 {out}  ({svg.w/72:.2f} × {svg.h/72:.2f} in，"
          f"{len(spec['series'])} 条系列)")
    for w in warns:
        print(f"  ! {w}")
    if args.export:
        files, notes = svg.export(out, formats=args.export.split(","),
                                  dpi=args.dpi, gray=args.gray)
        summarize(files, notes)
    return 0


def _from_csv(args) -> dict:
    import csv

    if not (args.x and args.y and args.by):
        raise SystemExit("--data 需要同时给 --x --y --by")
    groups: dict[str, dict[str, list]] = {}
    with open(args.data, encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            key = row[args.by]
            g = groups.setdefault(key, {"x": [], "y": []})
            try:
                g["x"].append(float(row[args.x]))
                g["y"].append(float(row[args.y]))
            except (TypeError, ValueError):
                continue
    series = [{"label": k, **v} for k, v in groups.items()]
    for s in series:
        order = sorted(range(len(s["x"])), key=lambda i: s["x"][i])
        s["x"] = [s["x"][i] for i in order]
        s["y"] = [s["y"][i] for i in order]
    return {"series": series}


if __name__ == "__main__":
    sys.exit(main())
