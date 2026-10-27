"""从模型描述生成概念框架图 / 结构模型图 / 测量模型图（SVG，零依赖）。

用法：
    python make_diagram.py spec.json out.svg

模型描述（JSON）示例见 references/diagrams.md。核心约定：

- `level` 不写就按最长路径自动分层（左→右）。
- 调节变量不指向节点，**指向它所调节的那条边的中点**——这是概念框架图
  最容易画错的地方：指到节点上，读者会以为是主效应。
- **测量模型（type = measurement）里两个潜变量之间是相关，必须双向箭头**
  （`"bidirectional": true`）；单向箭头是结构模型的因果路径，别混用。
- 控制变量用虚线指向因变量，不参与假设编号。
- 跨列的长边若穿过中间节点，会自动绕开（二次曲线），不会从方框里穿过去。
"""
from __future__ import annotations

import json
import math
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from svg_kit import (FULL_WIDTH, HALF_WIDTH, SANS, SERIF, Svg, clip_to_box,
                     clip_to_ellipse, text_width, wrap)
from mpl_backend import summarize

MARGIN = 26.0
ROW_GAP = 24.0
MIN_W = 58.0
LINE_H = 12.5
PAD_Y = 7.0
ARROW_TRIM = 7.0
NODE_SIZE = 9.5
H_LABEL_SIZE = 8.5

# 宽度自适应：依次尝试 (节点最大宽, 列间距)，取第一个放得进 6.5 in 的组合
FIT_CANDIDATES = [(124, 52), (112, 44), (100, 36), (90, 28)]


def node_size(label: str, max_w: float, size: float = NODE_SIZE) -> tuple[float, float]:
    lines = wrap(label, max_w - 12, size)
    w = min(max_w, max(MIN_W, max(text_width(l, size) for l in lines) + 14))
    h = max(26.0, len(lines) * LINE_H + PAD_Y * 2)
    return w, h


def assign_levels(nodes: list[dict], edges: list[dict]) -> dict[str, int]:
    if all("level" in x for x in nodes):
        return {x["id"]: int(x["level"]) for x in nodes}
    ids = [x["id"] for x in nodes]
    lvl = {i: 0 for i in ids}
    for _ in range(len(ids)):
        changed = False
        for e in edges:
            a, b = e.get("from"), e.get("to")
            if a in lvl and b in lvl and lvl[b] < lvl[a] + 1:
                lvl[b] = lvl[a] + 1
                changed = True
        if not changed:
            break
    return lvl


def layout(nodes, mods, lvl, max_w, gap, row_gap=None):
    """返回 (尺寸表, 每列宽, 列序, content_w, content_h)。"""
    row_gap = ROW_GAP if row_gap is None else row_gap
    sizes = {x["id"]: node_size(str(x.get("label", x["id"])), max_w) for x in nodes}
    msizes = {m["id"]: node_size(str(m.get("label", m["id"])), min(max_w, 86.0), 8.8)
              for m in mods}
    cols: dict[int, list[str]] = {}
    for x in nodes:
        cols.setdefault(lvl[x["id"]], []).append(x["id"])
    order = sorted(cols)
    col_w = {c: max(sizes[i][0] for i in cols[c]) for c in order}
    col_h = {c: sum(sizes[i][1] for i in cols[c]) + row_gap * (len(cols[c]) - 1)
             for c in order}
    content_w = sum(col_w.values()) + gap * (len(order) - 1)
    content_h = max(col_h.values())
    return sizes, msizes, cols, order, col_w, col_h, content_w, content_h


def bez(p1, c, p2, steps=22):
    out = []
    for i in range(steps + 1):
        t = i / steps
        x = (1 - t) ** 2 * p1[0] + 2 * (1 - t) * t * c[0] + t ** 2 * p2[0]
        y = (1 - t) ** 2 * p1[1] + 2 * (1 - t) * t * c[1] + t ** 2 * p2[1]
        out.append((x, y))
    return out


def _seg_point_dist(pt, a, b):
    ax, ay = a
    bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((pt[0] - ax) * dx + (pt[1] - ay) * dy) / L2))
    return math.hypot(pt[0] - (ax + t * dx), pt[1] - (ay + t * dy))


def hits_box(p1, p2, cx, cy, w, h, clearance=4.0):
    """线段是否穿过某个方框，或离它不足 clearance pt（欧氏距离）。

    口径必须是欧氏距离。早先用「轴对齐外扩矩形」判定，在方框四角会偏严：
    一条线离框角 11 pt 却被判成不足 10 pt，逼得选边搜索退到更差的方案，
    画出来就是从框里穿过去。
    """
    return _box_dist(p1, p2, cx, cy, w, h) < clearance


SIDES = ("left", "right", "top", "bottom")
CLEARANCE = 10.0          # 连线与无关方框的最小净空（pt）


def _box_dist(p1, p2, cx, cy, w, h):
    """线段到方框的最短距离；线段穿过方框时为 0。"""
    hw, hh = w / 2, h / 2
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    steps = max(int(L / 1.5), 8)
    best = 1e9
    for i in range(steps + 1):
        t = i / steps
        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t
        dx = max(cx - hw - x, 0.0, x - cx - hw)
        dy = max(cy - hh - y, 0.0, y - cy - hh)
        best = min(best, math.hypot(dx, dy))
        if best == 0.0:
            return 0.0
    return best


def _seg_enters_box(p1, p2, cx, cy, w, h, margin=1.5, skip=2.5):
    """线段是否进入了方框内部（贴着边不算）。用于检查连线别穿过自己两端的框。"""
    hw, hh = w / 2 - margin, h / 2 - margin
    if hw <= 0 or hh <= 0:
        return False
    L = math.hypot(p2[0] - p1[0], p2[1] - p1[1])
    if L == 0:
        return False
    steps = max(int(L / 1.5), 8)
    for i in range(steps + 1):
        t = i / steps
        if t * L < skip or (1 - t) * L < skip:
            continue
        x = p1[0] + (p2[0] - p1[0]) * t
        y = p1[1] + (p2[1] - p1[1]) * t
        if abs(x - cx) < hw and abs(y - cy) < hh:
            return True
    return False


def _segs_cross(p1, p2, p3, p4) -> bool:
    """两条线段是否真交叉（不含端点相接）。"""
    def orient(a, b, c):
        v = (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
        if abs(v) < 1e-9:
            return 0
        return 1 if v > 0 else -1

    o1, o2 = orient(p1, p2, p3), orient(p1, p2, p4)
    o3, o4 = orient(p3, p4, p1), orient(p3, p4, p2)
    if 0 in (o1, o2, o3, o4):
        return False
    return o1 != o2 and o3 != o4


TOP_KEYS = {"type", "lang", "title", "subtitle", "width", "row_gap",
            "nodes", "edges", "moderators", "controls", "note"}
NODE_KEYS = {"id", "label", "shape", "level"}
EDGE_KEYS = {"from", "to", "label", "coef", "dash", "bidirectional"}
MOD_KEYS = {"id", "label", "on", "position", "label_on_edge"}
SHAPES = {"box", "ellipse", "dashed"}


def validate_spec(spec: dict) -> tuple[list[str], list[str]]:
    """返回 (错误, 警告)。错误会阻止生成，警告只提示。

    手写 JSON 最常见的错是 id 打错和键名拼错，这两类必须给出「错在哪一行」，
    否则用户看到的是 KeyError 回溯。
    """
    errs: list[str] = []
    warns: list[str] = []

    if not isinstance(spec, dict):
        return ["顶层必须是一个 JSON 对象"], []

    for k in spec:
        if k not in TOP_KEYS:
            errs.append(f"未知的顶层键 `{k}`；可用的是 {sorted(TOP_KEYS)}")

    nodes = spec.get("nodes")
    if not isinstance(nodes, list) or not nodes:
        return errs + ["`nodes` 必须是非空数组"], warns

    ids: list[str] = []
    for i, n in enumerate(nodes, 1):
        if not isinstance(n, dict):
            errs.append(f"nodes 第 {i} 项不是对象")
            continue
        for k in n:
            if k not in NODE_KEYS:
                errs.append(f"nodes 第 {i} 项有未知键 `{k}`；可用的是 {sorted(NODE_KEYS)}")
        nid = n.get("id")
        if not nid or not isinstance(nid, str):
            errs.append(f"nodes 第 {i} 项缺 `id`（必须是非空字符串）")
            continue
        if nid in ids:
            errs.append(f"节点 id `{nid}` 重复；id 必须唯一")
        ids.append(nid)
        if not str(n.get("label", "")).strip():
            warns.append(f"节点 `{nid}` 没有 label，图里会显示 id")
        shape = n.get("shape", "box")
        if shape not in SHAPES:
            errs.append(f"节点 `{nid}` 的 shape = `{shape}` 不认识；可用的是 {sorted(SHAPES)}")
        if "level" in n and not isinstance(n["level"], int):
            errs.append(f"节点 `{nid}` 的 level 必须是整数（列号）")

    known = set(ids)
    edges = spec.get("edges", [])
    if not isinstance(edges, list):
        errs.append("`edges` 必须是数组")
        edges = []
    seen_edges: set[tuple[str, str]] = set()
    for i, e in enumerate(edges, 1):
        if not isinstance(e, dict):
            errs.append(f"edges 第 {i} 项不是对象")
            continue
        for k in e:
            if k not in EDGE_KEYS:
                errs.append(f"edges 第 {i} 项有未知键 `{k}`；可用的是 {sorted(EDGE_KEYS)}")
        for end in ("from", "to"):
            if end not in e:
                errs.append(f"edges 第 {i} 项缺 `{end}`")
            elif e[end] not in known:
                errs.append(f"edges 第 {i} 项的 {end} = `{e[end]}` 不在 nodes 里"
                            f"（现有 id：{sorted(known)}）")
        a, b = e.get("from"), e.get("to")
        if a and b and a == b:
            warns.append(f"edges 第 {i} 项是自环（{a} → {a}），通常不该出现")
        if a and b:
            if (a, b) in seen_edges:
                warns.append(f"edges 第 {i} 项与前面某条边重复（{a} → {b}）")
            seen_edges.add((a, b))
        if "bidirectional" in e and not isinstance(e["bidirectional"], bool):
            errs.append(f"edges 第 {i} 项的 bidirectional 必须是 true/false")

    mods = spec.get("moderators", [])
    if not isinstance(mods, list):
        errs.append("`moderators` 必须是数组")
        mods = []
    for i, m in enumerate(mods, 1):
        if not isinstance(m, dict):
            errs.append(f"moderators 第 {i} 项不是对象")
            continue
        for k in m:
            if k not in MOD_KEYS:
                errs.append(f"moderators 第 {i} 项有未知键 `{k}`；可用的是 {sorted(MOD_KEYS)}")
        on = m.get("on")
        if not isinstance(on, list) or len(on) != 2:
            errs.append(f"moderators 第 {i} 项的 on 必须是两个节点 id 组成的数组")
            continue
        for o in on:
            if o not in known:
                errs.append(f"moderators 第 {i} 项的 on 里 `{o}` 不在 nodes 里")
        if all(o in known for o in on):
            pair = {(on[0], on[1]), (on[1], on[0])}
            if not (pair & seen_edges):
                warns.append(
                    f"moderators 第 {i} 项调节 {on[0]} 与 {on[1]}，但 edges 里没有这条边；"
                    "调节变量的箭头会指到两个节点中间的空处")

    ctrl = spec.get("controls")
    if ctrl is not None:
        if not isinstance(ctrl, dict):
            errs.append("`controls` 必须是对象")
        else:
            for t in ctrl.get("to") or []:
                if t not in known:
                    errs.append(f"controls.to 里 `{t}` 不在 nodes 里")

    if "width" in spec and not isinstance(spec["width"], (int, float)):
        errs.append("`width` 必须是数字（pt）")
    if "row_gap" in spec and not isinstance(spec["row_gap"], (int, float)):
        errs.append("`row_gap` 必须是数字（pt）")

    return errs, warns


def build(spec: dict, geo_out: dict | None = None) -> tuple[Svg, list[str]]:
    errs, spec_warns = validate_spec(spec)
    if errs:
        raise SystemExit("规格有问题，未生成：\n"
                         + "\n".join(f"  {i}. {e}" for i, e in enumerate(errs, 1)))

    lang = spec.get("lang", "en")
    nodes = spec["nodes"]
    edges = spec.get("edges", [])
    mods = spec.get("moderators", [])
    ctrl = spec.get("controls")
    warns: list[str] = list(spec_warns)

    by_id = {x["id"]: x for x in nodes}

    # 测量模型（CFA）里两个潜变量之间是「相关」，必须画双向箭头；
    # 单向箭头表示因果路径，那是结构模型/路径图的事。混用是审稿人会直接指出的错误。
    if spec.get("type") == "measurement":
        for e in edges:
            both_latent = (by_id.get(e["from"], {}).get("shape") == "ellipse"
                           and by_id.get(e["to"], {}).get("shape") == "ellipse")
            if both_latent and not e.get("bidirectional"):
                warns.append(
                    f"{e['from']} 与 {e['to']} 都是潜变量，连线应为双向箭头（相关/协方差）；"
                    "单向箭头表示因果路径，属于结构模型。加 \"bidirectional\": true 修正。")
    lvl = assign_levels(nodes, edges)
    target_w = float(spec.get("width", FULL_WIDTH))
    row_gap = float(spec.get("row_gap", ROW_GAP))
    avail = target_w - MARGIN * 2

    # ---- 宽度自适应
    chosen = None
    for max_w, gap in FIT_CANDIDATES:
        cand = layout(nodes, mods, lvl, max_w, gap, row_gap)
        if cand[6] <= avail:
            chosen = (max_w, gap) + cand
            break
    if chosen is None:
        max_w, gap = FIT_CANDIDATES[-1]
        chosen = (max_w, gap) + layout(nodes, mods, lvl, max_w, gap, row_gap)
        need = chosen[8] + MARGIN * 2
        warns.append(
            f"内容宽 {chosen[8]:.0f} pt 放不进 {target_w/72:.2f} in（需 {need/72:.2f} in）。"
            f"建议缩短标签、减少并列节点，或拆成两幅图。")

    max_w, gap, sizes, msizes, cols, order, col_w, col_h, content_w, content_h = chosen

    title = spec.get("title", "")
    subtitle = spec.get("subtitle", "")
    note = spec.get("note", "")
    title_h = (16 if title else 0) + (13 if subtitle else 0) + (8 if title or subtitle else 0)

    # 控制变量框的高度要提前算进画布
    ctrl_lines, ctrl_w, ctrl_h = [], 0.0, 0.0
    if ctrl:
        ctrl_lines = wrap(str(ctrl.get("label", "Controls")), 132, 8.5)
        ctrl_w = max(text_width(l, 8.5) for l in ctrl_lines) + 16
        ctrl_h = max(22.0, len(ctrl_lines) * 11 + 10)
    ctrl_block = (ctrl_h + 20) if ctrl else 0

    need_w = content_w + MARGIN * 2
    if "width" in spec:
        W = max(float(spec["width"]), need_w)
    else:
        # 没指定宽度时贴合内容——6.5 in 画布配 4 in 内容会留两英寸空白
        W = max(need_w, HALF_WIDTH)

    # 控制变量框不能撑大画布：超宽就把文字折窄，而不是让图超出 6.5 in
    if ctrl:
        cap = W - 2 * MARGIN
        if ctrl_w > cap:
            ctrl_lines = wrap(str(ctrl.get("label", "Controls")), max(cap - 16, 40), 8.5)
            ctrl_w = max(text_width(l, 8.5) for l in ctrl_lines) + 16
            ctrl_h = max(22.0, len(ctrl_lines) * 11 + 10)
    H = MARGIN + title_h + content_h + ctrl_block + (16 if note else 0) + MARGIN

    # ---- 位置（先算坐标，再定画布高度：调节变量可能顶进图题那一条带）
    x0 = (W - content_w) / 2
    col_x, cur = {}, x0
    for c in order:
        col_x[c] = cur + col_w[c] / 2
        cur += col_w[c] + gap

    top = MARGIN + title_h
    pos: dict[str, tuple[float, float]] = {}
    for c in order:
        yy = top + (content_h - col_h[c]) / 2
        for nid in cols[c]:
            w, h = sizes[nid]
            pos[nid] = (col_x[c], yy + h / 2)
            yy += h + row_gap

    # 调节变量画在两端节点**上方**。若两端在顶行，框会顶进图题那一条带——
    # 自检夹具里就真的重叠过（图题压在「Uncertainty」框上），而此前没有任何
    # 判据查「图题与节点重叠」。这里先把内容整体下移，再往下算连线。
    above_top = None
    for m in mods:
        if m.get("position", "above") != "above":
            continue
        mh = msizes[m["id"]][1]
        tops = [pos[n][1] - sizes[n][1] / 2 for n in (m.get("on") or []) if n in pos]
        if tops:
            # 与下面 mod_geo 的公式对齐：框中心 = 最上端点顶边 − mh/2 − 14，
            # 所以框**顶边** = 最上端点顶边 − mh − 14。少减一个 mh/2 就会算错一半。
            t = min(tops) - mh - 14
            above_top = t if above_top is None else min(above_top, t)
    if above_top is not None and above_top < top + 4:
        shift = top + 4 - above_top
        top += shift
        H += shift
        pos = {nid: (x, yy + shift) for nid, (x, yy) in pos.items()}

    svg = Svg(W, H, font=SERIF if lang == "zh" else SANS)

    y = MARGIN + 12
    if title:
        svg.text_c(W / 2, y, title, 10.5, weight="bold")
        y += 15
    if subtitle:
        svg.text_c(W / 2, y, subtitle, 8.8, style="italic")
        y += 13

    def boundary(nid, toward, prefer=None):
        """求射线与节点边界的交点。

        prefer="right"/"left" 时强制从那条边出入——左右流向的图里，
        让边从右边出、从左边进，比按几何交点走更像流程图。
        """
        cx, cy = pos[nid]
        w, h = sizes[nid]
        if by_id[nid].get("shape") == "ellipse":
            return clip_to_ellipse(cx, cy, w / 2, h / 2, *toward)
        if prefer in ("right", "left"):
            yy = min(max(toward[1], cy - h / 2 + 7), cy + h / 2 - 7)
            return (cx + w / 2 if prefer == "right" else cx - w / 2), yy
        return clip_to_box(cx, cy, w, h, *toward)

    # ---- 接入点分配：多条线进同一个节点时沿目标边分散，避免挤成一个点
    # 接入点分散：四条边都做。
    # 只在左右分散时，两条都从底边进的线会挤在同一个点，进而互相交叉。
    def _spread(nid: str, side: str, idxs: list[int], is_target: bool):
        cx, cy = pos[nid]
        w, h = sizes[nid]
        if side in ("left", "right"):
            lo, hi = cy - h / 2 + 8, cy + h / 2 - 8
            if is_target:
                other = lambda i: pos[edges[i]["from"]][1]
            else:
                # 出口按「出发斜率」排序：平缓的在上、陡的在下，
                # 否则同一个节点引出的两条线会在框外立刻交叉。
                # 早先按目标 y 排序，两个目标同高时退化成任意顺序。
                other = lambda i: ((pos[edges[i]["to"]][1] - cy)
                                   / max(abs(pos[edges[i]["to"]][0] - cx), 1e-6))
            fixed = (cx - w / 2) if side == "left" else (cx + w / 2)
            mk = lambda v: (fixed, v)
        else:
            lo, hi = cx - w / 2 + 8, cx + w / 2 - 8
            if is_target:
                other = lambda i: pos[edges[i]["from"]][0]
            else:
                other = lambda i: ((pos[edges[i]["to"]][0] - cx)
                                   / max(abs(pos[edges[i]["to"]][1] - cy), 1e-6))
            fixed = (cy - h / 2) if side == "top" else (cy + h / 2)
            mk = lambda v: (v, fixed)
        if hi <= lo:
            lo = hi = (lo + hi) / 2
        ordered = sorted(idxs, key=other)
        k = len(ordered)
        mid = (lo + hi) / 2
        if k == 1:
            return {ordered[0]: mk(mid)}
        span = min(hi - lo, 11.0 * (k - 1))
        return {i: mk(mid - span / 2 + span * j / (k - 1))
                for j, i in enumerate(ordered)}

    incoming: dict[str, list[int]] = {}
    outgoing: dict[str, list[int]] = {}
    for i, e in enumerate(edges):
        a, b = e["from"], e["to"]
        if abs(pos[a][0] - pos[b][0]) < 1:
            continue
        incoming.setdefault(b, []).append(i)
        outgoing.setdefault(a, []).append(i)

    spread_t: dict[tuple[str, str], dict[int, tuple[float, float]]] = {}
    spread_s: dict[tuple[str, str], dict[int, tuple[float, float]]] = {}
    for nid, idxs in incoming.items():
        for side in SIDES:
            spread_t[(nid, side)] = _spread(nid, side, idxs, True)
    for nid, idxs in outgoing.items():
        for side in SIDES:
            spread_s[(nid, side)] = _spread(nid, side, idxs, False)

    # ---- 标签避让：沿边试多个位置，避开所有节点框与已放的标签
    # 标签统一在节点之后绘制——否则会被节点框的白色填充盖住。
    label_boxes: list[tuple[float, float, float, float]] = []
    pending: list[tuple[float, float, str, float, bool, str, str]] = []
    # 几何快照：--geometry 时输出，供审计脚本精确核对
    geo: dict = {"edges": [], "labels": [], "moderators": [], "nodes": {}}
    if title:
        # 图题的包围盒也进快照：图题压住节点/调节变量框是肉眼很难在缩略图上
        # 发现、但一定会在印刷品上出现的问题，交给 check_connections.py 判。
        _tw = text_width(title, 10.5)
        _base = MARGIN + 12
        geo["title"] = {"s": title,
                        "box": [round(W / 2 - _tw / 2, 2), round(_base - 8.4, 2),
                                round(W / 2 + _tw / 2, 2), round(_base + 2.6, 2)]}
    segs_all: list[tuple[float, float, float, float]] = []
    drawn_segs: list[tuple[float, float, float, float]] = []
    jobs: list[tuple] = []

    def _overlap(a, b):
        return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

    def _hits_node(lx, ly, tw, th):
        for nid, (cx, cy) in pos.items():
            nw, nh = sizes[nid]
            if abs(lx - cx) < (nw + tw) / 2 and abs(ly - cy) < (nh + th) / 2:
                return True
        return False

    def _path_dist(pt, path):
        return min(_seg_point_dist(pt, a, b) for a, b in zip(path, path[1:]))

    def _hits_line(lx, ly, tw, th, own=None):
        """标签框是否压到别的边。own 传自己那条路径，自己那条不算。

        早先用 `s is own` 比较，但 segs_all 存的是坐标元组、own 是路径对象，
        永远不相等——等于自己的线也被算成「压线」，
        结果每个候选都被否掉，最后只能用兜底位置，编号就被甩到别的线旁边。
        """
        own_pairs = set()
        if own:
            for i in range(len(own) - 1):
                own_pairs.add(((own[i][0], own[i][1]), (own[i + 1][0], own[i + 1][1])))
                own_pairs.add(((own[i + 1][0], own[i + 1][1]), (own[i][0], own[i][1])))
        limit = max(tw, th) / 2 + 3
        for s in segs_all:
            if ((s[0], s[1]), (s[2], s[3])) in own_pairs:
                continue
            for frac in (0.0, 0.5, 1.0):
                p0 = (s[0] + (s[2] - s[0]) * frac, s[1] + (s[3] - s[1]) * frac)
                p1 = (s[0] + (s[2] - s[0]) * (frac + 0.5), s[1] + (s[3] - s[1]) * (frac + 0.5))
                if _seg_point_dist((lx, ly), p0, p1) < limit:
                    return True
        return False

    def place_label(path, text, size, own=None):
        """在边旁找位置放编号：不压节点、不压别的编号、不压别的线，
        且离自己这条线比离别的线近至少 3 pt。

        先按「中点优先、两侧、由近及远」找合格位置；都不合格时取「最不坏」
        的那个（归属最清楚），而不是固定往上偏——固定偏移正是编号漂到
        别的线旁边、被读成那条线编号的原因。
        """
        # 沿真实路径取点：折线边不能拿首尾弦当方向，否则标签会压到弧线上
        segs_of_path = list(zip(path, path[1:]))
        lens = [math.dist(a, b) for a, b in segs_of_path]
        total = sum(lens) or 1.0

        def at(frac):
            target, acc = frac * total, 0.0
            for (a, b), L in zip(segs_of_path, lens):
                if acc + L >= target or (a, b) is segs_of_path[-1]:
                    k = (target - acc) / L if L else 0.0
                    k = min(max(k, 0.0), 1.0)
                    ang = math.atan2(b[1] - a[1], b[0] - a[0])
                    return (a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k, ang)
                acc += L
            a, b = segs_of_path[-1]
            return b[0], b[1], math.atan2(b[1] - a[1], b[0] - a[0])

        tw, th = text_width(text, size), size
        # 短线（<45 pt）没有空间放 14 pt 的偏移，收紧到 9 pt
        offs = (9.0,) if total < 45 else (10 + th * 0.5, 8 + th * 0.5, 13 + th * 0.5)
        best = None          # (margin, d_own, lx, ly, box)

        for off in offs:
            for t in (0.5, 0.42, 0.58, 0.34, 0.66, 0.26, 0.74, 0.18, 0.82):
                px, py, ang = at(t)
                nx, ny = -math.sin(ang), math.cos(ang)
                if abs(nx) > 0.7:           # 竖直边：标签放右侧
                    nx, ny = 1.0, 0.0
                elif ny > 0:                # SVG 的 y 轴向下：先试线的上方
                    nx, ny = -nx, -ny
                for s in (1, -1):
                    # 偏移量要按「文字往哪边占地方」算：
                    # 标签在线的左右侧时占的是字宽，在上下方时占的是字高。
                    # 一律按字高算，竖直边上的编号会压到线上（.53*** 就是这种情况）。
                    need = (tw / 2 + 3) if abs(ny) < 0.7 else (th / 2 + 3)
                    use = max(off, need)
                    lx, ly = px + nx * use * s, py + ny * use * s
                    box = (lx - tw / 2 - 1.5, ly - th / 2 - 1.5,
                           lx + tw / 2 + 1.5, ly + th / 2 + 1.5)
                    if _hits_node(lx, ly, tw, th):
                        continue
                    if any(_overlap(box, b) for b in label_boxes):
                        continue
                    if _hits_line(lx, ly, tw, th, own):
                        continue
                    d_own = _path_dist((lx, ly), path)
                    # 上限随文字宽度走，不用固定值：宽编号（如 .53***）放在竖直边旁
                    # 光是为了不压线就需要 17 pt，固定 17 会把它判成「太远」。
                    if d_own > max(tw, th) / 2 + 8:
                        continue
                    d_other = min((_path_dist((lx, ly), q)
                                   for q in all_paths if q is not path), default=1e9)
                    margin = d_other - d_own
                    if best is None or (margin, -d_own) > (best[0], -best[1]):
                        best = (margin, d_own, lx, ly, box)
                    if margin >= 3.0:
                        label_boxes.append(box)
                        return lx, ly

        if best is not None:
            _, _, lx, ly, box = best
            label_boxes.append(box)
            return lx, ly

        # 连不压节点/标签/线的位置都没有：紧贴自己那条线放
        mx, my, ang = at(0.5)
        nx, ny = -math.sin(ang), math.cos(ang)
        if abs(nx) > 0.7:
            nx, ny = 1.0, 0.0
        elif ny > 0:
            nx, ny = -nx, -ny
        use_fb = max(offs[-1], (tw / 2 + 3) if abs(ny) < 0.7 else (th / 2 + 3))
        lx, ly = mx + nx * use_fb, my + ny * use_fb
        label_boxes.append((lx - tw / 2, ly - th / 2, lx + tw / 2, ly + th / 2))
        return lx, ly

    # ---- 边（先画，节点覆盖其上）
    for idx, e in enumerate(edges):
        a, b = e["from"], e["to"]
        pa, pb = pos[a], pos[b]
        dash = e.get("dash")
        bi = bool(e.get("bidirectional"))
        ent_side = ext_side = "vertical"
        side_cost = 0.0
        if abs(pa[0] - pb[0]) < 1:
            # 同列：上下相邻就直接画竖线（测量模型里潜变量之间的相关就该这样），
            # 只有竖直方向挤不下时才绕到右侧画曲线。
            wa, ha = sizes[a]
            wb, hb = sizes[b]
            down = pb[1] > pa[1]
            sy = pa[1] + (ha / 2 if down else -ha / 2)
            ey = pb[1] - (hb / 2 if down else -hb / 2)
            if abs(ey - sy) > 10:
                sx = ex = pa[0]
                # 箭头线端要留出画箭头的 7 pt；几何快照记的也必须是这个端点，
                # 否则审计会以为箭头一直画到框边上（报「离边界 0.0 pt」）。
                # 双向箭头两端都要留。
                if bi:
                    sy = sy + (ARROW_TRIM if down else -ARROW_TRIM)
                ey = ey - (ARROW_TRIM if down else -ARROW_TRIM)
                svg.arrow(sx, sy, ex, ey, sw=0.9, dash=dash, both=bi)
                drawn_segs.append((sx, sy, ex, ey))
            else:
                ax, bx = pa[0] + wa / 2, pb[0] + wb / 2
                sx, sy, ex, ey = ax, pa[1], bx, pb[1]
                pts = bez((sx, sy), (max(ax, bx) + 26, (pa[1] + pb[1]) / 2), (ex, ey))
                svg.polyline(pts, sw=0.9, dash=dash)
                svg.arrow(pts[-2][0], pts[-2][1], pts[-1][0], pts[-1][1], sw=0.9, dash=dash)
                if bi:
                    svg.arrow(pts[1][0], pts[1][1], pts[0][0], pts[0][1], sw=0.9, dash=dash)
        else:
            dxe, dye = pb[0] - pa[0], pb[1] - pa[1]
            if abs(dxe) >= abs(dye):
                ent_pref = "left" if dxe > 0 else "right"
                ext_pref = "right" if dxe > 0 else "left"
            else:
                ent_pref = "top" if dye > 0 else "bottom"
                ext_pref = "bottom" if dye > 0 else "top"

            def _side_pt(nid, side, other):
                cx_, cy_ = pos[nid]
                w_, h_ = sizes[nid]
                lox, hix = cx_ - w_ / 2 + 7, cx_ + w_ / 2 - 7
                loy, hiy = cy_ - h_ / 2 + 7, cy_ + h_ / 2 - 7
                if lox > hix:
                    lox = hix = cx_
                if loy > hiy:
                    loy = hiy = cy_
                if side == "left":
                    return cx_ - w_ / 2, min(max(other[1], loy), hiy)
                if side == "right":
                    return cx_ + w_ / 2, min(max(other[1], loy), hiy)
                if side == "top":
                    return min(max(other[0], lox), hix), cy_ - h_ / 2
                return min(max(other[0], lox), hix), cy_ + h_ / 2

            def _cost(p1, p2):
                """代价：穿框最重，交叉次之，贴边最轻。"""
                bad = 0
                clr = 1e9
                for nid2 in sizes:
                    if nid2 in (a, b):
                        # 两端点在自己的框上：只禁止线段钻进框内，
                        # 否则会选出「从左边出、横穿自己的框、再进目标右边缘」这种线
                        if _seg_enters_box(p1, p2, *pos[nid2], *sizes[nid2]):
                            bad += 1
                        continue
                    if hits_box(p1, p2, *pos[nid2], *sizes[nid2], clearance=CLEARANCE):
                        bad += 1
                    clr = min(clr, _box_dist(p1, p2, *pos[nid2], *sizes[nid2]))
                cross = sum(1 for s2 in drawn_segs
                            if _segs_cross(p1, p2, (s2[0], s2[1]), (s2[2], s2[3])))
                return bad * 1000 + cross * 40 + max(0.0, CLEARANCE - clr)

            best_choice = None
            for es in [ent_pref] + [s for s in SIDES if s != ent_pref]:
                for xs in [ext_pref] + [s for s in SIDES if s != ext_pref]:
                    tx, ty = (spread_t.get((b, es), {}).get(idx)
                              or _side_pt(b, es, pa))
                    sx, sy = (spread_s.get((a, xs), {}).get(idx)
                              or _side_pt(a, xs, (tx, ty)))
                    if math.dist((sx, sy), (tx, ty)) < 12:
                        continue
                    c = _cost((sx, sy), (tx, ty))
                    if os.environ.get("DIAGRAM_DEBUG") == "1":
                        print(f"    {a}->{b} {es}/{xs} cost={c:8.1f} "
                              f"({sx:6.1f},{sy:6.1f})→({tx:6.1f},{ty:6.1f})")
                    if best_choice is None or c < best_choice[0]:
                        best_choice = (c, sx, sy, tx, ty, es, xs)
                    if c == 0:
                        break
                if best_choice and best_choice[0] == 0:
                    break
            _, sx, sy, tx, ty, ent_side, ext_side = best_choice
            side_cost = best_choice[0]

            blocked = [(nid, *pos[nid], *sizes[nid]) for nid in sizes
                       if nid not in (a, b) and hits_box((sx, sy), (tx, ty), *pos[nid], *sizes[nid])]
            if blocked:
                # 绕行不该是「往上或往下鼓」，而要绕过挡路方框最近的角。
                # 先列出所有候选角（每个障碍框四个角，各外扩 6 pt），
                # 按「离原线段多近」排序，取第一个真能清空障碍的。
                def _d2seg(pt, p1, p2):
                    ax_, ay_ = p1
                    bx_, by_ = p2
                    dx_, dy_ = bx_ - ax_, by_ - ay_
                    L2_ = dx_ * dx_ + dy_ * dy_
                    tt_ = 0.0 if L2_ == 0 else max(0.0, min(1.0, ((pt[0] - ax_) * dx_ + (pt[1] - ay_) * dy_) / L2_))
                    return math.hypot(pt[0] - (ax_ + tt_ * dx_), pt[1] - (ay_ + tt_ * dy_))

                corners = []
                for nid, cx2, cy2, w2, h2 in blocked:
                    for cxx, cyy in ((cx2 - w2 / 2 - 7, cy2 - h2 / 2 - 7),
                                     (cx2 + w2 / 2 + 7, cy2 - h2 / 2 - 7),
                                     (cx2 - w2 / 2 - 7, cy2 + h2 / 2 + 7),
                                     (cx2 + w2 / 2 + 7, cy2 + h2 / 2 + 7)):
                        corners.append((_d2seg((cxx, cyy), (sx, sy), (tx, ty)),
                                        (cxx, cyy), (cx2, cy2)))
                corners.sort()

                def _curve_clear(cp) -> tuple[int, list]:
                    cand = bez((sx, sy), cp, (tx, ty))
                    n_hit = 0
                    for nid in sizes:
                        if nid in (a, b):
                            continue
                        for i in range(0, len(cand) - 1, 2):
                            if hits_box(cand[i], cand[i + 1], *pos[nid], *sizes[nid]):
                                n_hit += 1
                                break
                    return n_hit, cand

                # 二次贝塞尔只走到控制点一半的位置，所以控制点要往外多推一点。
                # 由近到远试，直到曲线真正清空所有方框。
                best = None
                for _, cp, (ocx, ocy) in corners:
                    vx, vy = cp[0] - ocx, cp[1] - ocy
                    L = math.hypot(vx, vy) or 1.0
                    for push in (0, 10, 20, 32):
                        cp2 = (cp[0] + vx / L * push, cp[1] + vy / L * push)
                        n_hit, cand = _curve_clear(cp2)
                        if best is None or n_hit < best[0]:
                            best = (n_hit, cand)
                        if n_hit == 0:
                            break
                    if best[0] == 0:
                        break
                _, pts = best
                ang = math.atan2(pts[-1][1] - pts[-2][1], pts[-1][0] - pts[-2][0])
                ex = pts[-1][0] - ARROW_TRIM * math.cos(ang)
                ey = pts[-1][1] - ARROW_TRIM * math.sin(ang)
                svg.polyline(pts[:-1], sw=0.9, dash=dash)
                svg.arrow(pts[-2][0], pts[-2][1], ex, ey, sw=0.9, dash=dash)
                if bi:
                    svg.arrow(pts[1][0], pts[1][1], pts[0][0], pts[0][1],
                              sw=0.9, dash=dash)
            else:
                ang = math.atan2(ty - sy, tx - sx)
                ex = tx - ARROW_TRIM * math.cos(ang)
                ey = ty - ARROW_TRIM * math.sin(ang)
                if bi:
                    # 双向：起点也留出箭头的位置
                    sx = sx + ARROW_TRIM * math.cos(ang)
                    sy = sy + ARROW_TRIM * math.sin(ang)
                svg.arrow(sx, sy, ex, ey, sw=0.9, dash=dash, both=bi)

        path = pts if blocked else [(sx, sy), (ex, ey)]
        for i in range(len(path) - 1):
            seg = (path[i][0], path[i][1], path[i + 1][0], path[i + 1][1])
            segs_all.append(seg)
            drawn_segs.append(seg)
        jobs.append((path, e.get("label", ""), e.get("coef", ""), a, b,
                     ent_side, ext_side, side_cost))

    # ---- 调节变量几何：先算出来，标签避让才能看见它的箭头
    mod_geo = []
    for m in mods:
        on = m.get("on") or []
        if len(on) != 2:
            raise SystemExit(f"调节变量 {m.get('id')} 的 on 必须给两个节点 id")
        mw, mh = msizes[m["id"]]
        (axm, aym), (bxm, bym) = pos[on[0]], pos[on[1]]
        ahm, bhm = sizes[on[0]][1], sizes[on[1]][1]
        mxm, mym = (axm + bxm) / 2, (aym + bym) / 2
        side_m = m.get("position", "above")
        if side_m == "above":
            cym = min(aym - ahm / 2, bym - bhm / 2) - mh / 2 - 14
            a0m, a1m = cym + mh / 2, mym - 5
        else:
            cym = max(aym + ahm / 2, bym + bhm / 2) + mh / 2 + 14
            a0m, a1m = cym - mh / 2, mym + 5
        mod_geo.append(dict(m=m, mx=mxm, cy=cym, a0=a0m, a1=a1m, mw=mw, mh=mh))
        segs_all.append((mxm, a0m, mxm, a1m))
        geo["moderators"].append({"id": m.get("id", ""), "on": list(on),
                                  "box": [round(mxm - mw / 2, 2), round(cym - mh / 2, 2),
                                          round(mxm + mw / 2, 2), round(cym + mh / 2, 2)],
                                  "arrow": [round(mxm, 2), round(a0m, 2),
                                            round(mxm, 2), round(a1m, 2)]})

    # ---- 标签：等所有边画完再放，这样能同时避开节点、别的标签、以及所有的线
    all_paths = [q for q, _, _, _, _, _, _, _ in jobs]
    for ei, (path, lab, coef, ea, eb, ent_s, ext_s, s_cost) in enumerate(jobs):
        owner = f"{ea}->{eb}"
        geo["edges"].append({"from": ea, "to": eb, "label": lab,
                             "entry": ent_s, "exit": ext_s, "cost": round(s_cost, 1),
                             "path": [[round(x, 2), round(y, 2)] for x, y in path]})
        if lab:
            lx, ly = place_label(path, lab, H_LABEL_SIZE, own=path)
            pending.append((lx, ly, lab, H_LABEL_SIZE, False, "middle", owner))
            if coef:
                cw = text_width(coef, H_LABEL_SIZE)
                lw = text_width(lab, H_LABEL_SIZE)
                placed = False
                for cxx, cyy in ((lx, ly + 10),
                                 (lx + lw / 2 + cw / 2 + 5, ly),
                                 (lx, ly - 10),
                                 (lx - lw / 2 - cw / 2 - 5, ly)):
                    box2 = (cxx - cw / 2 - 1.5, cyy - H_LABEL_SIZE / 2 - 1.5,
                            cxx + cw / 2 + 1.5, cyy + H_LABEL_SIZE / 2 + 1.5)
                    if _hits_node(cxx, cyy, cw, H_LABEL_SIZE):
                        continue
                    if any(_overlap(box2, b) for b in label_boxes):
                        continue
                    label_boxes.append(box2)
                    pending.append((cxx, cyy, coef, H_LABEL_SIZE, True, "middle", owner))
                    placed = True
                    break
                if not placed:
                    pending.append((lx, ly + 10, coef, H_LABEL_SIZE, True, "middle", owner))
        elif coef:
            lx, ly = place_label(path, coef, H_LABEL_SIZE, own=path)
            pending.append((lx, ly, coef, H_LABEL_SIZE, True, "middle", owner))

    # ---- 调节变量：先算几何（标签避让要看见它的箭头），再画
    for g in mod_geo:
        m, mx, cy, a0, a1, mw, mh = (g["m"], g["mx"], g["cy"],
                                     g["a0"], g["a1"], g["mw"], g["mh"])
        svg.arrow(mx, a0, mx, a1, sw=0.9, kind="arrow_open")
        svg.rect(mx - mw / 2, cy - mh / 2, mw, mh, rx=2,
                 fill="#fff", stroke="#000", sw=0.9, dash="3 2")
        svg.block(mx, cy, wrap(str(m.get("label", "")), mw - 10, 8.8), 8.8)
        lab = m.get("label_on_edge", "")
        if lab:
            tw2 = text_width(lab, H_LABEL_SIZE)
            placed2 = False
            for dxx, yy, anc in ((-7, 0.42, "end"), (7, 0.42, "start"),
                                 (-7, 0.3, "end"), (7, 0.3, "start"),
                                 (-7, 0.6, "end"), (7, 0.6, "start")):
                lx2 = mx + dxx
                ly2 = a0 + (a1 - a0) * yy
                x0b = lx2 - tw2 if anc == "end" else lx2
                box2 = (x0b - 1.5, ly2 - H_LABEL_SIZE / 2 - 1.5,
                        x0b + tw2 + 1.5, ly2 + H_LABEL_SIZE / 2 + 1.5)
                if any(_overlap(box2, b) for b in label_boxes):
                    continue
                if _hits_node(lx2, ly2, tw2, H_LABEL_SIZE):
                    continue
                label_boxes.append(box2)
                pending.append((lx2, ly2, lab, H_LABEL_SIZE, False, anc,
                                "moderator:" + str(m.get("id", ""))))
                placed2 = True
                break
            if not placed2:
                pending.append((mx - 7, a0 + (a1 - a0) * 0.42, lab,
                                H_LABEL_SIZE, False, "end",
                                "moderator:" + str(m.get("id", ""))))

    # ---- 节点
    for x in nodes:
        cx, cy = pos[x["id"]]
        w, h = sizes[x["id"]]
        geo["nodes"][x["id"]] = {"label": str(x.get("label", x["id"])),
                                 "box": [round(cx - w / 2, 2), round(cy - h / 2, 2),
                                         round(cx + w / 2, 2), round(cy + h / 2, 2)],
                                 "shape": x.get("shape", "box")}
        shape = x.get("shape", "box")
        if shape == "ellipse":
            svg.ellipse(cx, cy, w / 2, h / 2, fill="#fff", stroke="#000", sw=0.9)
        else:
            svg.rect(cx - w / 2, cy - h / 2, w, h, rx=2,
                     fill="#fff", stroke="#000", sw=0.9,
                     dash="3 2" if shape == "dashed" else None)
        svg.block(cx, cy, wrap(str(x.get("label", x["id"])), w - 10, NODE_SIZE), NODE_SIZE)

    # ---- 标签（节点之后，确保不被覆盖）
    for lx, ly, s, size, italic, anchor, owner in pending:
        svg.text(lx, ly + size * 0.35, s, size, anchor=anchor,
                 style="italic" if italic else "normal")
        geo["labels"].append({"s": s, "x": round(lx, 2), "y": round(ly, 2),
                              "size": size, "owner": owner})

    # ---- 控制变量：放在最右列下方居中，虚线指向目标
    if ctrl:
        last = order[-1]
        cx0 = min(max(col_x[last], MARGIN + ctrl_w / 2), W - MARGIN - ctrl_w / 2)
        cy0 = top + content_h + 20 + ctrl_h / 2
        targets = ctrl.get("to") or [cols[last][0]]
        svg.rect(cx0 - ctrl_w / 2, cy0 - ctrl_h / 2, ctrl_w, ctrl_h, rx=2,
                 fill="#fff", stroke="#000", sw=0.7, dash="3 2")
        svg.block(cx0, cy0, ctrl_lines, 8.5)
        for t in targets:
            ex, ey = boundary(t, (cx0, cy0))
            svg.arrow(cx0, cy0 - ctrl_h / 2 if cy0 > ey else cy0 + ctrl_h / 2,
                      ex, ey + 5, sw=0.7, kind="arrow_open", dash="3 2")

    if note:
        svg.text(MARGIN, H - MARGIN + 2, note, 8.2)
    if geo_out is not None:
        geo["canvas"] = [round(W, 2), round(H, 2)]
        geo_out.update(geo)
    return svg, warns


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(
        description="从模型描述生成概念框架图 / 结构模型图 / 测量模型图（SVG，零依赖）。")
    ap.add_argument("spec", help="模型描述 .json（结构见 references/diagrams.md）")
    ap.add_argument("out", nargs="?", help="输出 .svg（用 --validate 时可省略）")
    ap.add_argument("--validate", action="store_true", help="只校验规格，不画图")
    ap.add_argument("--geometry", metavar="PATH",
                    help="同时写出几何快照，供 check_connections.py 审计")
    ap.add_argument("--export", help="另存矢量/位图，如 pdf,png")
    ap.add_argument("--dpi", type=int, default=600)
    ap.add_argument("--gray", action="store_true", help="按灰度导出，核对黑白印刷")
    args = ap.parse_args()

    from qc import load_spec
    spec = load_spec(args.spec, required=("nodes",))

    if args.validate:
        errs, warns = validate_spec(spec)
        print(f"节点 {len(spec.get('nodes', []))} 个，"
              f"连线 {len(spec.get('edges', []))} 条，"
              f"调节变量 {len(spec.get('moderators', []))} 个")
        for e in errs:
            print(f"  ✗ {e}")
        for w in warns:
            print(f"  ! {w}")
        if errs:
            print(f"\n{len(errs)} 个错误，{len(warns)} 个警告")
            return 1
        print(f"\n通过（{len(warns)} 个警告）")
        return 0

    if not args.out:
        ap.error("要输出图就必须给 out.svg（只想校验请加 --validate）")

    geo: dict = {}
    svg, warns = build(spec, geo)
    out = svg.save(args.out)
    if args.geometry:
        gp = Path(args.geometry)
        gp.write_text(json.dumps(geo, ensure_ascii=False, indent=1),
                      encoding="utf-8", newline="\n")
        print(f"几何快照：{gp}（{len(geo.get('edges', []))} 条边、"
              f"{len(geo.get('labels', []))} 个标签）")
    print(f"已生成 {out}  ({svg.w:.0f} × {svg.h:.0f} pt = {svg.w/72:.2f} × {svg.h/72:.2f} in)")
    for w in warns:
        print(f"  警告：{w}")
    if args.export:
        files, notes = svg.export(out, formats=args.export.split(","),
                                  dpi=args.dpi, gray=args.gray)
        summarize(files, notes)
    return 0


if __name__ == "__main__":
    sys.exit(main())
