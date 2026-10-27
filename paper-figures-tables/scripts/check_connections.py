"""连线几何审计：读 make_diagram.py --geometry 的输出，逐条核对。

查六件事（都是「一旦有人认真看图就会被指出」的）：
  1 每条连线到「非端点方框」的最小净空——贴边、穿框
  2 连线是否钻进了自己两端节点的框内
  3 线线交叉（并说明是结构性必然还是可避免）
  4 每个编号到「自己那条线」的距离，以及到次近线的距离
  5 编号之间是否重叠
  6 箭头端点落在目标框的哪条边、离边界多远

用法：
    python check_connections.py geo.json
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

CLEAR_MIN = 10.0      # 连线与无关方框的最小净空
LABEL_SLACK = 8.0     # 编号离自己那条线的最大距离 = 自身宽度一半 + 这个松弛量
MARGIN_MIN = 3.0      # 编号离自己线要比离别的线近多少
ARROW_GAP_MAX = 9.0   # 箭头线端离目标边界多远算正常


def text_w(s: str, size: float) -> float:
    """与 make_diagram 一致的宽度估算：中日韩字符 1 em，其余 0.55 em。"""
    return sum(size * (1.0 if ord(ch) > 0x2E7F else 0.55) for ch in s)


def seg_pt(pt, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((pt[0] - ax) * dx + (pt[1] - ay) * dy) / L2))
    return math.hypot(pt[0] - (ax + t * dx), pt[1] - (ay + t * dy))


def path_dist(pt, path):
    return min(seg_pt(pt, a, b) for a, b in zip(path, path[1:]))


def box_dist(pt, box):
    x0, y0, x1, y1 = box
    dx = max(x0 - pt[0], 0.0, pt[0] - x1)
    dy = max(y0 - pt[1], 0.0, pt[1] - y1)
    return math.hypot(dx, dy)


def path_box_dist(path, box, step=1.2):
    """路径到方框的最近距离；进入框内返回 0。"""
    best = 1e9
    for a, b in zip(path, path[1:]):
        L = math.dist(a, b)
        n = max(int(L / step), 2)
        for i in range(n + 1):
            t = i / n
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            d = box_dist(q, box)
            best = min(best, d)
            if best == 0.0:
                return 0.0
    return best


def enters_box(path, box, margin=1.5, skip=2.5):
    """路径是否进入方框内部（贴着边走不算）。

    跳过路径两端各 skip 之内：连线本来就从框边界出发，那不算「穿框」。
    """
    x0, y0, x1, y1 = box
    for a, b in zip(path, path[1:]):
        L = math.dist(a, b)
        if L == 0:
            continue
        n = max(int(L / 1.2), 4)
        for i in range(n + 1):
            t = i / n
            q = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
            if x0 + margin < q[0] < x1 - margin and y0 + margin < q[1] < y1 - margin:
                if math.dist(q, path[0]) > skip and math.dist(q, path[-1]) > skip:
                    return True
    return False


def segs_cross(p1, p2, p3, p4):
    def orient(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        return 0 if abs(v) < 1e-9 else (1 if v > 0 else -1)

    o1, o2 = orient(p1, p2, p3), orient(p1, p2, p4)
    o3, o4 = orient(p3, p4, p1), orient(p3, p4, p2)
    if 0 in (o1, o2, o3, o4):
        return False
    return o1 != o2 and o3 != o4


def paths_cross(p, q):
    for a, b in zip(p, p[1:]):
        for c, d in zip(q, q[1:]):
            if segs_cross(a, b, c, d):
                return True
    return False


def _overlap(a, b) -> bool:
    """两个 [x0, y0, x1, y1] 矩形是否相交。"""
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def side_of(pt, box):
    x0, y0, x1, y1 = box
    d = {"左": abs(pt[0] - x0), "右": abs(pt[0] - x1),
         "上": abs(pt[1] - y0), "下": abs(pt[1] - y1)}
    return min(d, key=d.get), min(d.values())


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="连线几何审计：读 make_diagram.py --geometry 的输出，逐条核对净空、穿框、交叉、编号归属。")
    ap.add_argument("geo", help="make_diagram.py --geometry 生成的 .geo.json")
    args = ap.parse_args()

    p = Path(args.geo)
    if not p.exists():
        print(f"找不到 {p}：先用 make_diagram.py … --geometry {p.name} 生成几何快照")
        return 2
    try:
        geo = json.loads(p.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        print(f"{p.name} 不是有效的 JSON：{e}")
        return 2
    for key in ("nodes", "edges", "labels", "canvas"):
        if key not in geo:
            print(f"{p.name} 缺字段 {key!r}：这不像 make_diagram.py 输出的几何快照")
            return 2

    nodes = geo["nodes"]
    edges = geo["edges"]
    labels = geo["labels"]
    mods = geo.get("moderators", [])

    def nlab(nid):
        return nodes[nid]["label"].replace("\n", " ")[:20]

    print(f"画布 {geo['canvas'][0]:.0f} × {geo['canvas'][1]:.0f} pt "
          f"= {geo['canvas'][0]/72:.2f} × {geo['canvas'][1]/72:.2f} in")
    print(f"节点 {len(nodes)}，连线 {len(edges)}，标签 {len(labels)}，调节变量 {len(mods)}")

    # ---- 1 净空
    print("\n[1] 连线到无关方框的最小净空")
    bad = 0
    for e in edges:
        p = [tuple(q) for q in e["path"]]
        worst, wlab = 1e9, ""
        for nid, n in nodes.items():
            if nid in (e["from"], e["to"]):
                continue
            d = path_box_dist(p, n["box"])
            if d < worst:
                worst, wlab = d, nlab(nid)
        flag = ""
        if worst == 0:
            flag = "  ✗ 穿过"
            bad += 1
        elif worst < CLEAR_MIN:
            flag = f"  ✗ 净空不足（<{CLEAR_MIN:.0f}）"
            bad += 1
        print(f"  {nlab(e['from']):22}→{nlab(e['to']):22} 最近 {wlab:22} {worst:5.1f} pt{flag}")
    print(f"  结论：{bad} 条不合格")

    # ---- 2 自己两端
    print("\n[2] 连线是否钻进自己两端节点的框内")
    bad2 = 0
    for e in edges:
        p = [tuple(q) for q in e["path"]]
        for nid in (e["from"], e["to"]):
            if enters_box(p, nodes[nid]["box"]):
                print(f"  ✗ {nlab(e['from'])}→{nlab(e['to'])} 穿过了 {nlab(nid)} 自己的框")
                bad2 += 1
    print(f"  结论：{bad2} 条不合格")

    # ---- 3 交叉
    print("\n[3] 线线交叉")
    pairs = []
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if paths_cross([tuple(q) for q in edges[i]["path"]],
                           [tuple(q) for q in edges[j]["path"]]):
                pairs.append((edges[i], edges[j]))
    for a, b in pairs:
        print(f"  · {nlab(a['from'])}→{nlab(a['to'])} × {nlab(b['from'])}→{nlab(b['to'])}")
    print(f"  结论：{len(pairs)} 处")

    # ---- 4 编号归属
    print("\n[4] 编号到自己那条线的距离")
    bad4 = 0
    for lb in labels:
        pt = (lb["x"], lb["y"])
        own = [e for e in edges if f"{e['from']}->{e['to']}" == lb["owner"]]
        if own:
            d_own = path_dist(pt, [tuple(q) for q in own[0]["path"]])
            others = [path_dist(pt, [tuple(q) for q in e["path"]])
                      for e in edges if e is not own[0]]
        else:
            mid = [m for m in mods if "moderator:" + str(m["id"]) == lb["owner"]]
            if not mid:
                continue
            ar = mid[0]["arrow"]
            d_own = seg_pt(pt, (ar[0], ar[1]), (ar[2], ar[3]))
            others = [path_dist(pt, [tuple(q) for q in e["path"]]) for e in edges]
        d_other = min(others) if others else 1e9
        flags = []
        # 上限随文字宽度走：宽编号放在竖直边旁，光是为了不压线就需要较大偏移
        limit = max(text_w(lb["s"], lb["size"]), lb["size"]) / 2 + LABEL_SLACK
        if d_own > limit:
            flags.append(f"离自己线 {d_own:.1f} > {limit:.1f}")
        if d_other - d_own < MARGIN_MIN:
            flags.append(f"归属不清（次近 {d_other:.1f}）")
        if flags:
            bad4 += 1
        print(f"  {lb['s']:5} 自己 {d_own:5.1f}  次近 {d_other:5.1f}"
              f"  {'✓' if not flags else '✗ ' + '；'.join(flags)}")
    print(f"  结论：{bad4} 个不合格")

    # ---- 5 标签重叠
    print("\n[5] 编号重叠")
    boxes = [(lb["s"], (lb["x"] - len(lb["s"]) * lb["size"] * 0.3,
                        lb["y"] - lb["size"] * 0.55,
                        lb["x"] + len(lb["s"]) * lb["size"] * 0.3,
                        lb["y"] + lb["size"] * 0.45)) for lb in labels]
    bad5 = 0
    for i in range(len(boxes)):
        for j in range(i + 1, len(boxes)):
            a, b = boxes[i][1], boxes[j][1]
            if not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1]):
                print(f"  ✗ {boxes[i][0]} 与 {boxes[j][0]} 重叠")
                bad5 += 1
    print(f"  结论：{bad5} 处")

    # ---- 6 箭头端点
    print("\n[6] 箭头端点落点")
    for e in edges:
        p = [tuple(q) for q in e["path"]]
        end = p[-1]
        side, gap = side_of(end, nodes[e["to"]]["box"])
        flag = "" if gap <= ARROW_GAP_MAX else "  ✗ 离边界过远"
        print(f"  {nlab(e['from']):22}→{nlab(e['to']):22} 从 {side} 边进，离边界 {gap:4.1f} pt{flag}")

    # ---- 7 图题压到图元上
    print("\n[7] 图题与图元")
    bad7 = 0
    title = geo.get("title")
    if not title:
        print("  无图题（图题通常写在文档里，不画进图）")
    else:
        tb = title["box"]
        hits = [f"节点「{nlab(nid)}」" for nid, n in nodes.items()
                if _overlap(tb, n["box"])]
        hits += [f"调节变量「{m.get('id', '')}」" for m in mods
                 if _overlap(tb, m["box"])]
        for h in hits:
            print(f"  ✗ 图题压住了{h}")
        print(f"  结论：{len(hits)} 处")
        bad7 = len(hits)

    total = bad + bad2 + len(pairs) + bad4 + bad5 + bad7
    print(f"\n合计问题 {total} 项（交叉 {len(pairs)} 处单列，未必可避免）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
