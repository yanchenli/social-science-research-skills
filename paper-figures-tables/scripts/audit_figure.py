"""审别人交上来的图：截图、Excel/SPSS 导出、PDF、手绘拍照。

**能查什么、查不了什么，都写在结论里。** 这个脚本看的是文件与像素，
它不知道「这张图画得对不对」——图表类型选错、数据放错轴、结论不成立，
这些要人看。它只负责把**机器能确定的事**钉死：

- 位图分辨率够不够印
- 是不是截图（有 UI 底色、有边框条）
- 彩色图在黑白打印时还分不分得清
- Excel 图表是不是饼图 / 3D / 带网格线 / 图例在右侧
- PDF 里到底是矢量还是位图

`--rebuild` 会把 Excel 图表的数据与结构转成我们生成器的规格，
这样「审完」之后可以直接重画，而不是只说哪里不好。
"""
from __future__ import annotations

import argparse
import json
import sys
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET

sys.path.insert(0, str(Path(__file__).parent))

import profiles  # noqa: E402
from qc import E, I, W, Finding, print_findings, write_report  # noqa: E402

NS_C = "{http://schemas.openxmlformats.org/drawingml/2006/chart}"
NS_A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"

# 这些图表类型在学术论文里基本不成立：饼图读不出精确值、3D 会扭曲比较
BAD_CHARTS = {"pieChart": "饼图：读者读不出精确数值，且无法比较相近的份额",
              "doughnutChart": "圆环图：同饼图，且面积与数值不成比例",
              "radarChart": "雷达图：面积随维度排列顺序变化，跨图不可比",
              "ofPieChart": "复合饼图：同饼图"}
BAD_3D = {"bar3DChart", "pie3DChart", "line3DChart", "area3DChart"}


# ---------------------------------------------------------------- 位图
def audit_image(path: Path, prof: dict) -> list[Finding]:
    out: list[Finding] = []
    try:
        from PIL import Image
    except ImportError:
        return [Finding("PFT-AUD-000", I, "没装 Pillow，位图检查未执行",
                        limit="pip install pillow 后可查分辨率、背景、颜色可辨性")]

    im = Image.open(path)
    w, h = im.size
    dpi = im.info.get("dpi")
    min_dpi = prof["figure"]["min_dpi"]

    if not dpi:
        out.append(Finding("PFT-AUD-001", W,
                           f"位图没有 DPI 元数据（{w} × {h} px）："
                           "投稿系统会按 96 dpi 解释，实际印刷尺寸无法确定",
                           limit="没有 DPI 时只能按像素数估计，无法换算物理尺寸"))
    else:
        eff = min(dpi)
        if eff < min_dpi:
            out.append(Finding("PFT-AUD-001", E,
                               f"分辨率 {eff:.0f} dpi，低于要求的 {min_dpi} dpi——印出来会糊",
                               limit="只读文件里的 DPI 元数据，不判断原始出处"))

    # 按 6.5 in 版心反推需要的像素数
    need_px = int(prof["figure"]["width_in"] * min_dpi)
    if w < need_px:
        # 差得不多是「排版时要留意」，差一半以上就是「这张图不能用」
        sev = E if w < need_px * 0.6 else W
        out.append(Finding("PFT-AUD-002", sev,
                           f"图宽 {w} px：按 {min_dpi} dpi 铺满 {prof['figure']['width_in']} in "
                           f"版心需要 {need_px} px，只有 {w/need_px:.0%}——放大会糊",
                           limit="只比像素数；图是否真的满幅由作者决定"))

    rgb = im.convert("RGB")
    colors = rgb.getcolors(maxcolors=1 << 20) or []
    n_color = len(colors)
    if n_color > 20000:
        # 照片或带抗锯齿的复杂图，不做背景/配色判断，避免误报
        out.append(Finding("PFT-AUD-003", I,
                           f"颜色数超过 2 万（{n_color}），像是照片或复杂位图："
                           "背景与配色的自动判断已跳过",
                           limit="这类图只能人工看，脚本的判断没有意义"))
    else:
        white = sum(c for c, px in colors if min(px) >= 250)
        total = w * h
        if white / total < 0.55:
            out.append(Finding("PFT-AUD-003", W,
                               f"白色像素只占 {white/total:.0%}："
                               "图表通常应当是白底；有色底多为截图或带主题色的导出",
                               limit="只统计接近纯白的像素；浅灰底也算有色底"))
        # 四边是否有一条与内部不同的均匀色带（截图常见）
        border = _border_band(rgb)
        if border:
            out.append(Finding("PFT-AUD-004", W, border,
                               limit="只在颜色数较少的图上判断，照片不适用"))
        # 彩色 → 灰度后是否还分得清
        out += _gray_collision(colors, w, h)

    return out


def _border_band(im) -> str:
    """检测四边是否有与内部明显不同的均匀色带——截图的典型特征。"""
    w, h = im.size
    px = im.load()

    def row_color(y):
        seen = {px[x, y] for x in range(0, w, max(1, w // 40))}
        return seen

    edges = []
    for y in (0, 1, h - 2, h - 1):
        s = row_color(y)
        if len(s) == 1:
            edges.append(next(iter(s)))
    if not edges:
        return ""
    inner = px[w // 2, h // 2]
    if any(abs(sum(e) - sum(inner)) > 90 for e in edges):
        return ("图片四边有与内部不同的纯色条带，像是从软件界面截的图："
                "投稿要用导出功能，不要截图")
    return ""


def _gray_collision(colors, w: int, h: int) -> list[Finding]:
    """把有代表性的颜色转成灰度，看有没有两两亮度几乎相同。

    黑白印刷时这两条线会变成同一种灰——这是「屏幕上看没问题、印出来分不清」
    的根源，也是这类图最常见的退稿理由之一。
    """
    if not colors:
        return []
    total = w * h
    main = [(c, px) for c, px in colors if c / total >= 0.004 and max(px) < 250]
    if len(main) < 2:
        return []
    lum = []
    for c, px in main:
        r, g, b = px[:3]
        lum.append((0.299 * r + 0.587 * g + 0.114 * b, px, c))
    lum.sort()
    close = [(lum[i], lum[i + 1]) for i in range(len(lum) - 1)
             if abs(lum[i + 1][0] - lum[i][0]) < 12]
    if not close:
        return []
    a, b = close[0]
    hexs = lambda px: "#%02x%02x%02x" % px[:3]
    return [Finding("PFT-AUD-005", W,
                    f"黑白打印时两种颜色会变成几乎相同的灰（{hexs(a[1])} 与 {hexs(b[1])}，"
                    f"亮度差 {abs(b[0]-a[0]):.0f}）：靠颜色区分的系列在灰度下会混在一起，"
                    "改用线型或标记",
                    limit="按亮度换算判断；实际印刷的网点响应会有出入")]


# ---------------------------------------------------------------- Excel 图表
def _read_shared_strings(z: zipfile.ZipFile) -> list[str]:
    try:
        root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    except KeyError:
        return []
    return ["".join(t.text or "" for t in si.iter("{http://schemas.openxmlformats.org/"
                                                  "spreadsheetml/2006/main}t"))
            for si in root]


def _sheet_cells(z: zipfile.ZipFile) -> dict[str, list[list[str]]]:
    """把每个 sheet 读成二维字符串表（按行号/列号摆放，空位补空串）。

    不依赖 openpyxl：xlsx 就是一个 zip，sharedStrings + sheetN.xml 够用了。
    """
    ns = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    shared = _read_shared_strings(z)
    out: dict[str, list[list[str]]] = {}
    for name in z.namelist():
        if not (name.startswith("xl/worksheets/sheet") and name.endswith(".xml")):
            continue
        root = ET.fromstring(z.read(name))
        grid: list[list[str]] = []
        for row in root.iter(f"{ns}row"):
            cells: dict[int, str] = {}
            for c in row.findall(f"{ns}c"):
                ref = c.get("r") or ""
                col = 0
                for ch in ref:
                    if ch.isalpha():
                        col = col * 26 + (ord(ch.upper()) - 64)
                    else:
                        break
                t = c.get("t")
                if t == "inlineStr":
                    val = "".join(x.text or "" for x in c.iter(f"{ns}t"))
                else:
                    v = c.find(f"{ns}v")
                    val = v.text if v is not None and v.text else ""
                    if t == "s" and val.isdigit():
                        idx = int(val)
                        val = shared[idx] if idx < len(shared) else ""
                cells[col - 1] = val
            if cells:
                width = max(cells) + 1
                grid.append([cells.get(i, "") for i in range(width)])
            else:
                grid.append([])
        out[Path(name).stem.lower()] = grid
    return out


def _range_values(sheets: dict, ref: str) -> list[str]:
    """解析 `Sheet1!$B$2:$B$5`，取出这一列的字符串值。"""
    if "!" not in ref:
        return []
    sheet, rng = ref.split("!", 1)
    sheet = sheet.strip("'").lower()
    grid = sheets.get(sheet)
    if grid is None:
        return []
    import re
    m = re.match(r"\$?([A-Z]+)\$?(\d+)(?::\$?([A-Z]+)\$?(\d+))?", rng.replace("$", ""))
    if not m:
        return []
    c1, r1 = m.group(1), int(m.group(2))
    c2 = m.group(3) or c1
    r2 = int(m.group(4) or r1)

    def col_idx(s):
        n = 0
        for ch in s:
            n = n * 26 + (ord(ch.upper()) - 64)
        return n - 1

    vals = []
    for r in range(r1 - 1, r2):
        row = grid[r] if r < len(grid) else []
        ci = col_idx(c1)
        vals.append(row[ci] if ci < len(row) else "")
    return vals


def audit_xlsx(path: Path, prof: dict) -> tuple[list[Finding], dict | None]:
    """读 xlsx 里的图表 XML。返回 (结论, 可重建的规格)。"""
    out: list[Finding] = []
    try:
        z = zipfile.ZipFile(path)
    except zipfile.BadZipFile:
        return [Finding("PFT-AUD-000", E, "不是有效的 xlsx（zip 打不开）")], None
    charts = [n for n in z.namelist() if n.startswith("xl/charts/chart") and n.endswith(".xml")]
    if not charts:
        return [Finding("PFT-AUD-006", W,
                        "这个工作簿里没有图表（只有数据）："
                        "若学生交的是数据，用 make_line_plot / make_estimate_plot 直接画",
                        limit="只找 xl/charts/chartN.xml；图片形式的图表不在其中")], None

    sheets = _sheet_cells(z)
    kinds: dict[str, int] = {}
    series_info: list[dict] = []
    has_grid = has_legend_right = False
    axis_titles: set[str] = set()
    fonts: list[float] = []
    colors: set[str] = set()

    for name in charts:
        root = ET.fromstring(z.read(name))
        for el in root.iter():
            tag = el.tag.replace(NS_C, "")
            if tag in BAD_CHARTS or tag in BAD_3D:
                kinds[tag] = kinds.get(tag, 0) + 1
            elif tag.endswith("Chart") and tag not in ("chart",):
                kinds.setdefault(tag, 0)
            elif tag == "majorGridlines":
                has_grid = True
            elif tag == "legendPos" and el.get("val") in ("r", "b", "tr"):
                has_legend_right = True
            elif tag == "title":
                txt = "".join(t.text or "" for t in el.iter(f"{NS_A}t"))
                if txt:
                    axis_titles.add(txt)
            elif tag in ("defRPr", "rPr"):
                sz = el.get("sz")
                if sz:
                    fonts.append(int(sz) / 100.0)
        for ser in root.iter(f"{NS_C}ser"):
            tx = ser.find(f"{NS_C}tx")
            lbl, lbl_ref = "", ""
            if tx is not None:
                # 系列名有两种写法：内联富文本，或指向某个单元格
                lbl = "".join(t.text or "" for t in tx.iter(f"{NS_A}t"))
                tf = tx.find(f".//{NS_C}f")
                lbl_ref = tf.text if tf is not None and tf.text else ""
            cats = ser.find(f"{NS_C}cat")
            vals = ser.find(f"{NS_C}val")
            cf = cats.find(f".//{NS_C}f") if cats is not None else None
            vf = vals.find(f".//{NS_C}f") if vals is not None else None
            if not lbl and lbl_ref:
                got = _range_values(sheets, lbl_ref)
                lbl = got[0] if got else ""
            series_info.append({
                "label": lbl,
                "cat_ref": cf.text if cf is not None else "",
                "val_ref": vf.text if vf is not None else "",
            })
        for el in root.iter(f"{NS_A}srgbClr"):
            v = el.get("val")
            if v and v.upper() not in ("000000", "FFFFFF"):
                colors.add(v.upper())

    for tag, why in BAD_CHARTS.items():
        if tag in kinds:
            out.append(Finding("PFT-AUD-007", E,
                               f"用了 {tag.replace('Chart','')}：{why}——换成条形图或点图",
                               limit="只按图表类型判断；若作者能论证必要，需在图注说明"))
    for tag in BAD_3D & set(kinds):
        out.append(Finding("PFT-AUD-008", E,
                           f"用了 3D 图（{tag}）：三维透视会让读者比较错误的长度，"
                           "学术论文一律用平面图",
                           limit="只认图表标签，不看渲染效果"))

    if has_grid:
        out.append(Finding("PFT-AUD-009", W,
                           "图里有横向/纵向网格线：APA 不要网格线，"
                           "刻度已经够读，网格只是噪声",
                           limit="只查 majorGridlines 标签，手动画的网格线查不到"))
    if has_legend_right:
        out.append(Finding("PFT-AUD-010", W,
                           "图例放在右侧或底部：优先在线端直接标注，"
                           "读者不用在图与图例之间来回看",
                           limit="只读 legendPos；图例是否其实多余，需人判断"))
    if not axis_titles:
        out.append(Finding("PFT-AUD-011", W,
                           "两个坐标轴都没有标题：读者不知道横纵轴是什么量、什么单位",
                           limit="只读 chart title 元素；文本框写的轴标题查不到"))
    if fonts:
        small = [f for f in fonts if f < prof["figure"]["min_text_pt"]]
        if small:
            out.append(Finding("PFT-AUD-012", W,
                               f"图内字号最小 {min(small):.1f} pt，低于 "
                               f"{prof['figure']['min_text_pt']} pt——缩到版心宽后会更小",
                               limit="只读显式声明的字号；继承默认值的查不到"))
    if len(colors) >= 3:
        out.append(Finding("PFT-AUD-013", W,
                           f"用了 {len(colors)} 种彩色（{', '.join(sorted(colors)[:4])}…）："
                           "黑白打印时这些颜色会变成相近的灰，改用线型或标记区分",
                           limit="只统计显式声明的 RGB 色；主题色查不到"))

    if not out:
        out.append(Finding("PFT-AUD-014", I,
                           "图表结构上没有查出硬伤（分辨率/配色/网格线/轴标题未报问题）",
                           limit="本脚本不判断图表类型选得对不对、数据放错轴、结论是否成立"))

    spec = _to_spec(series_info, sheets, prof)
    return out, spec


def _to_spec(series: list[dict], sheets: dict, prof: dict) -> dict | None:
    """把 Excel 图表的系列与数据转成我们折线图的规格。取不到数就返回 None。"""
    out = []
    for s in series:
        xs = _range_values(sheets, s["cat_ref"]) if s["cat_ref"] else []
        ys = _range_values(sheets, s["val_ref"]) if s["val_ref"] else []
        if not ys:
            continue
        # 分类轴可能是文字（阶段名），也可能是数字
        numeric = all(_is_float(v) for v in xs) and xs
        out.append({
            "label": s["label"] or f"Series {len(out)+1}",
            "x": [float(v) for v in xs] if numeric else list(range(1, len(ys) + 1)),
            "y": [float(v) for v in ys if _is_float(v)],
            **({"x_ticks": [{"v": i + 1, "label": v} for i, v in enumerate(xs)]}
               if xs and not numeric else {}),
        })
    out = [s for s in out if len(s["x"]) == len(s["y"]) and s["y"]]
    if not out:
        return None
    spec = {
        "series": [{"label": s["label"], "x": s["x"], "y": s["y"]} for s in out],
        "xlabel": "", "ylabel": "",
        "note": "Note. 由 Excel 图表的数据重建，坐标轴标题与图注需作者补。",
    }
    ticks = next((s["x_ticks"] for s in out if "x_ticks" in s), None)
    if ticks:
        spec["x_ticks"] = ticks
    return spec


def _is_float(v) -> bool:
    try:
        float(v)
        return True
    except (TypeError, ValueError):
        return False


# ---------------------------------------------------------------- PDF
def audit_pdf(path: Path, prof: dict) -> list[Finding]:
    """PDF 里的图：**逐页**看是矢量还是位图，并量每张嵌入图的有效分辨率。

    只查第一页是错的——整篇论文的第 1 页通常是文字页，真正的图在第 3、7 页。
    有效分辨率 = 像素数 ÷ 放置尺寸（英寸），这才是「放大糊不糊」的判据；
    文件里写的 DPI 元数据在 PDF 里根本不起作用。
    """
    try:
        import pymupdf
    except ImportError:
        return [Finding("PFT-AUD-000", I, "没装 PyMuPDF，PDF 检查未执行",
                        limit="pip install pymupdf 后可判断矢量/位图与有效分辨率")]

    doc = pymupdf.open(str(path))
    out: list[Finding] = []
    min_dpi = prof["figure"]["min_dpi"]
    pages = len(doc)
    blank, raster_only, low_dpi, raster_fig = [], [], [], []

    for i, page in enumerate(doc, 1):
        drawings = len(page.get_drawings())
        text = page.get_text().strip()
        images = page.get_images(full=True)
        if not drawings and not text and not images:
            blank.append(i)
            continue
        if images and not drawings and not text:
            raster_only.append(i)
        for img in images:
            xref = img[0]
            try:
                info = doc.extract_image(xref)
            except Exception:                       # noqa: BLE001
                continue
            for rect in page.get_image_rects(xref):
                # 按面积筛掉图标与装饰。不能按单边长度筛：横长的框图（比如
                # 「信任承诺 → 关系行为 → 关系绩效」那种）高度只有 0.4 in，
                # 按高度筛会把真图漏掉。
                if rect.width * rect.height < 1200:      # ≈ 0.23 in²
                    continue
                eff = info["width"] / (rect.width / 72.0)
                raster_fig.append((i, eff, info["ext"]))
                if eff < min_dpi * 0.98:
                    low_dpi.append((i, eff, info["ext"]))

    if blank:
        out.append(Finding("PFT-AUD-015", E,
                           f"第 {', '.join(map(str, blank[:6]))} 页上什么都没有",
                           limit="只判断页面上有没有东西"))
    if raster_only:
        out.append(Finding("PFT-AUD-015", W,
                           f"第 {', '.join(map(str, raster_only[:6]))} 页只有位图、没有矢量元素："
                           "这些页是整页扫描或截图，放大就糊",
                           limit="只比较有无矢量图元与文本层"))
    if low_dpi:
        worst = min(low_dpi, key=lambda t: t[1])
        out.append(Finding("PFT-AUD-016", E,
                           f"{len(low_dpi)} 张嵌入图有效分辨率低于 {min_dpi} dpi"
                           f"（最低第 {worst[0]} 页 {worst[1]:.0f} dpi）——"
                           "按放置尺寸算，文件里写的 DPI 元数据在 PDF 里不起作用",
                           limit="按「像素数 ÷ 放置尺寸」算；矢量图不参与"))
    if raster_fig and not low_dpi:
        effs = sorted({round(e) for _, e, _ in raster_fig})
        fmts = sorted({x.upper() for _, _, x in raster_fig})
        out.append(Finding("PFT-AUD-017", W,
                           f"全篇 {len(raster_fig)} 张嵌入图都是位图（{'/'.join(fmts)}），"
                           f"有效分辨率 {effs[0]}–{effs[-1]} dpi。"
                           "刚好达标不等于没问题：位图没有余量，印刷厂再缩放一次就糊，"
                           "框图与路径图应当用矢量导出",
                           limit="只量分辨率；JPEG 的压缩伪影无法量化，只能看出格式"))
    elif raster_fig:
        out.append(Finding("PFT-AUD-017", I,
                           f"全篇 {len(raster_fig)} 张嵌入图，均为位图（见上一条）",
                           limit="只量分辨率"))

    if pages > 3 and not out:
        out.append(Finding("PFT-AUD-018", I,
                           f"这是一份 {pages} 页的文档，逐页都没有查出硬伤",
                           limit="本脚本只看「有没有矢量内容、嵌入图够不够清晰」；"
                                 "单张图的设计问题（图型、坐标轴、系列区分）要逐图看"))
    return out


# ---------------------------------------------------------------- 入口
def audit(path: Path, prof: dict) -> tuple[list[Finding], dict | None]:
    suf = path.suffix.lower()
    if suf in (".png", ".jpg", ".jpeg", ".tif", ".tiff", ".bmp"):
        return audit_image(path, prof), None
    if suf in (".xlsx", ".xlsm"):
        return audit_xlsx(path, prof)
    if suf == ".pdf":
        return audit_pdf(path, prof), None
    return [Finding("PFT-AUD-000", W,
                    f"不支持的文件类型 {suf}：位图（png/jpg/tif）、Excel（xlsx）、PDF 可以查",
                    limit="手绘稿请先拍照或扫描成 png/tif 再交")], None


def main() -> int:
    ap = argparse.ArgumentParser(description="审别人交上来的图")
    ap.add_argument("files", nargs="+")
    ap.add_argument("--profile", default="apa7")
    ap.add_argument("--json", help="把结论写成 JSON 报告")
    ap.add_argument("--rebuild", help="把 Excel 图表的数据导出成重画规格（.json）")
    args = ap.parse_args()

    prof = profiles.load(args.profile, quiet=True)
    all_findings: list[Finding] = []
    rebuilt: dict | None = None
    for name in args.files:
        f = Path(name)
        print(f"\n{f.name}")
        if not f.exists():
            all_findings.append(Finding("PFT-GEN-404", E, f"{f.name} 不存在"))
            print("  ✗ 文件不存在")
            continue
        got, spec = audit(f, prof)
        if spec and rebuilt is None:
            rebuilt = spec
        for x in got:
            all_findings.append(x)
        print_findings(got)

    n_err, n_warn = print_findings([])
    errs = [x for x in all_findings if x.severity == E]
    warns = [x for x in all_findings if x.severity == W]
    print(f"\n合计 {len(errs)} 个必须改的问题，{len(warns)} 个提示")
    print("本报告只覆盖「文件与像素层面」能确定的事：图表类型选得对不对、"
          "数据有没有放错轴、结论是否成立，都要人看。")

    if args.rebuild:
        if rebuilt:
            Path(args.rebuild).write_text(
                json.dumps(rebuilt, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8", newline="\n")
            print(f"已导出重画规格：{args.rebuild}"
                  f"（{len(rebuilt['series'])} 条系列）——"
                  "补上轴标题与图注后可直接用 make_line_plot 出图")
        else:
            print("没有可导出的数据（只有 Excel 图表能导出重画规格）")

    if args.json:
        write_report(args.json, all_findings,
                     targets=[str(Path(x).name) for x in args.files],
                     tool="paper-figures-tables/audit_figure")
        print(f"报告已写入 {args.json}")
    return 0 if not errs else 1


if __name__ == "__main__":
    sys.exit(main())
