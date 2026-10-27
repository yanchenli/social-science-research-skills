"""多面板图：(a)(b) 并排成一张图（SVG，零依赖）。

APA 与多数期刊都要求「同一论证任务的几幅小图合成一幅图」，用 (a)(b) 标注，
共用一条图题。学生常犯的错是当成两张图分别编号（Figure 2 与 Figure 3），
审稿人会要求合并。

用法：

    python make_panel.py out.svg --panels a.svg b.svg --labels "(a),(b)" \\
           --note "Error bars are 95% CIs."

    python make_panel.py out.svg --panels a.svg b.svg --layout column --width 234

设计取舍
--------
- **只做合成，不重排内容**：各面板由各自的生成器画好，这里只做平移与缩放。
  这样每个生成器只管自己的版式，不会出现「合成器又实现一遍坐标逻辑」。
- **缩放是等比的、所有面板同一个系数**。分别缩放会改变各面板的相对大小，
  而宽度本身可能是有意义的（半幅图就是为并排设计的）。
- **缩放会缩小字号**，所以合成后要把有效最小字号报出来：低于 8 pt 就
  不能投稿。这是唯一需要人回头改的地方（把面板画窄一点，或减少面板数）。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import svg_read  # noqa: E402
from svg_kit import SANS, SERIF, Svg, n  # noqa: E402

FULL_WIDTH = 6.5 * 72.0
FS_MIN = 8.0
LABEL_H = 13.0          # (a) 标注占的高度
SVG_OPEN = re.compile(r"<svg\b[^>]*>", re.S)
ATTR = re.compile(r'(\w[\w:-]*)="([^"]*)"')
MARKER = re.compile(r"<marker\b[^>]*>.*?</marker>", re.S)
DEFS = re.compile(r"<defs>.*?</defs>", re.S)
TEXT_SIZE = re.compile(r'font-size="([\d.]+)"')


def _attr(tag: str, name: str) -> str | None:
    for k, v in ATTR.findall(tag):
        if k == name:
            return v
    return None


def read_panel(path: Path) -> dict:
    """读出面板的尺寸与内部内容。"""
    text = path.read_text(encoding="utf-8")
    m = SVG_OPEN.search(text)
    if not m:
        raise SystemExit(f"{path.name} 不是 SVG：找不到 <svg> 标签")
    tag = m.group(0)
    body = text[m.end():text.rindex("</svg>")]

    def num(name, fallback=None):
        v = _attr(tag, name)
        if v is None:
            return fallback
        return float(re.sub(r"[^0-9.\-]", "", v) or 0)

    w, h = num("width"), num("height")
    vb = _attr(tag, "viewBox")
    if (not w or not h) and vb:
        parts = [float(p) for p in vb.replace(",", " ").split()]
        if len(parts) == 4:
            w, h = w or parts[2], h or parts[3]
    if not w or not h:
        raise SystemExit(f"{path.name} 既没有 width/height 也没有 viewBox，无法合成")

    # 顺序不能反：marker 在 <defs> 里面，先删 defs 就取不到箭头定义了，
    # 合成出来的图会一根箭头都没有（第一版就是这样，自检抓到）。
    body = MARKER.sub("", body)
    body = DEFS.sub("", body)
    sizes = [float(s) for s in TEXT_SIZE.findall(body)]
    ops, unknown = svg_read.parse_ops(text)
    if unknown:
        print(f"  ! {path.name} 里有不认识的元素：{', '.join(unknown)}"
              "——它们不会出现在导出的 PDF 里", file=sys.stderr)
    return {"name": path.name, "w": w, "h": h, "body": body, "ops": ops,
            "min_fs": min(sizes) if sizes else None}


def build(panels: list[dict], opts: dict) -> tuple[Svg, list[str], dict]:
    warns: list[str] = []
    labels = opts.get("labels") or [f"({chr(97 + i)})" for i in range(len(panels))]
    if len(labels) != len(panels):
        raise SystemExit(f"--labels 给了 {len(labels)} 个，但面板有 {len(panels)} 个")
    gap = float(opts.get("gap", 18.0))
    layout = opts.get("layout", "row")
    target = float(opts.get("width") or FULL_WIDTH)
    note = opts.get("note") or ""

    if layout == "row":
        span = sum(p["w"] for p in panels)
        other = max(p["h"] for p in panels)
        gaps = gap * (len(panels) - 1)
    else:
        span = max(p["w"] for p in panels)
        other = sum(p["h"] for p in panels)
        gaps = gap * (len(panels) - 1)

    # 只缩不放：面板本来就比目标窄时保持原尺寸，放大等于把 8 pt 的字吹大，
    # 会让同一篇里的两张图字号不一致。
    pad = 2.0
    inner = target - pad * 2
    budget = inner - gaps if layout == "row" else inner
    scale = min(1.0, budget / span) if span > budget > 0 else 1.0
    if scale < 1.0:
        warns.append(f"面板总宽 {span + gaps:.0f} pt 超过 {target:.0f} pt，"
                     f"已等比缩到 {scale:.3f}")

    note_h = 14.0 if note else 0.0
    W = pad * 2 + span * scale + gaps
    H = pad * 2 + LABEL_H + other * scale + note_h
    svg = Svg(W, H, font=SERIF if opts.get("lang") == "zh" else SANS)

    min_fs = None
    cursor = pad
    for i, p in enumerate(panels):
        if layout == "row":
            tx, ty = cursor, pad + LABEL_H
            cursor += p["w"] * scale + gap
        else:
            tx, ty = pad, pad + LABEL_H + cursor - pad
            cursor += p["h"] * scale + gap
        svg.text(tx, ty - 4, labels[i], 9.0, anchor="start")
        # 走 replay 而不是把 SVG 文本塞进 <g transform>：塞文本的话 ops 是空的，
        # 用 matplotlib 重画 PDF 时整页空白，而 SVG 看起来完全正常。
        svg.replay(p["ops"], tx, ty, scale)
        if p["min_fs"]:
            eff = p["min_fs"] * scale
            min_fs = eff if min_fs is None else min(min_fs, eff)

    if note:
        svg.text(pad, H - 6, note, 8.2)

    info = {"scale": scale, "min_font": min_fs, "panels": len(panels),
            "width_in": W / 72.0, "height_in": H / 72.0}
    if min_fs is not None and min_fs < FS_MIN - 1e-9:
        warns.append(f"缩放后最小字号 {min_fs:.1f} pt，低于 {FS_MIN} pt 的印刷下限；"
                     "把面板画窄一些（--width 减小）或拆成两幅图")
    if W / 72.0 > FULL_WIDTH / 72.0 + 0.01:
        warns.append(f"合成后图宽 {W/72:.2f} in，超过 APA 整幅 {FULL_WIDTH/72:.1f} in")
    return svg, warns, info


def main() -> int:
    ap = argparse.ArgumentParser(description="把几幅 SVG 合成一张多面板图")
    ap.add_argument("out")
    ap.add_argument("--panels", nargs="+", required=True)
    ap.add_argument("--labels", help='如 "(a),(b)"，逗号分隔')
    ap.add_argument("--layout", choices=("row", "column"), default="row")
    ap.add_argument("--gap", type=float, default=18.0, help="面板间距（pt），默认 18")
    ap.add_argument("--width", type=float, help="目标总宽（pt），默认 468 = 6.5 in")
    ap.add_argument("--note", default="")
    ap.add_argument("--lang", default="en")
    ap.add_argument("--export", help="另存矢量/位图，如 pdf,png")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--gray", action="store_true", help="按灰度导出，核对黑白印刷")
    args = ap.parse_args()

    panels = [read_panel(Path(p)) for p in args.panels]
    labels = [s.strip() for s in args.labels.split(",")] if args.labels else None
    svg, warns, info = build(panels, {"labels": labels, "gap": args.gap,
                                      "layout": args.layout, "width": args.width,
                                      "note": args.note, "lang": args.lang})
    out = svg.save(args.out)
    if args.export:
        from mpl_backend import summarize
        files, notes = svg.export(out, formats=args.export.split(","),
                                  dpi=args.dpi, gray=args.gray)
        summarize(files, notes)
    print(f"已生成 {out}  ({info['width_in']:.2f} × {info['height_in']:.2f} in，"
          f"{info['panels']} 个面板，缩放 {info['scale']:.3f}）")
    if info["min_font"]:
        print(f"  缩放后最小字号 {info['min_font']:.1f} pt")
    for w in warns:
        print(f"  ! {w}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
