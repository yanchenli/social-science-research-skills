---
name: paper-figures-tables
description: >-
  把论文里的图和表做成可投稿、可印刷的样子。适用于 APA 7（英文期刊）、中文期刊、以及学位论文
  （按学校格式文件定制）三档规格。覆盖五类产物：三线表（描述统计、信效度、路径系数、假设汇总、
  文献编码矩阵）、概念框架图、测量模型图与结构模型图、交互效应图、组间均值与系数图
  （点图 + 95% 置信区间）、多系列折线与置信带；并支持把几幅小图合成 (a)(b) 多面板图、
  过宽的表放横向页、一格内按研究竖排多个值。
  输出为矢量 SVG 与带真实边框的 .docx，不是 markdown 表格；装了 matplotlib 时
  可另存矢量 PDF 与 300/600 dpi 的 PNG/TIFF（期刊投稿格式），并对导出文件做发布前预检
  （DPI、透明通道、字体嵌入、字形覆盖、灰度可辨）。
  也能审别人交上来的图表（截图、Excel 图表、PDF），并把 Excel 图表的数据导出成重画规格。
  不负责决定「放什么数」——那由分析类技能定；本技能负责「怎么呈现」。
version: 1.11.5
license: CC-BY-4.0
---

# 论文图表：从数据到可投稿的成品

> **一句话定位**：上游技能决定「放什么」，本技能负责「怎么呈现」。
> 内容不是这里定的，形式与规格是。

## 核心判断：先问投哪里

图表的规格由**目标刊物**决定，不由偏好决定。同一张表：

- 投英文刊：`.53`（省略前导零），表题斜体左对齐在表上方，图题在图上**方**
- 投中文刊：`0.53`（保留前导零），表题居中在表上方，图题在图**下**方
- 投学位论文：**以学校格式文件为准**，各校差异比想象中大

顺序反了就要整篇返工。所以阶段 0 只做一件事：**问清楚**。

---

## 阶段 0 — 先问三件事

**不要跳过这一步直接生成。** 生成之后改规格，比先问清楚贵得多。

1. **投哪里？** 英文期刊 / 中文期刊 / 学位论文 / 还没定（默认 APA 7）
2. **这份图表要说明什么？** 一句话即可——用来判断该用表还是图
3. **有没有格式文件？**
   - 学位论文：**必须索取**学校的《学位论文格式规范》，按 `references/format-specs.md`
     第四节建一个 profile（每条要求记条号），**不要凭印象填**
   - 有目标期刊：查该刊「投稿须知」里的图表部分，同样落成 profile
   - 都没有：用内置的 `apa7`（有出处）或 `zh-journal`（通行做法，会提醒核对）

```bash
python scripts/profiles.py        # 列出内置 profile 及状态
```

内置三档：`apa7`（documented）、`zh-journal`（convention）、`thesis-template`（template，待填）。
状态决定提醒方式：`template` / `simulated` 每次使用都会警告，
`convention` / `observed` 提醒「投稿前核对」，只有 `documented` 不提醒。

> 学校格式文件通常只给几条要求（表题位置、线宽、字号、编号方式）。
> 不要凭「一般学校都这样」去猜——猜错要整篇返工。
> profile 里还有四个字段专门装「说不清的部分」：`pending_confirmation`（待确认）、
> `unsupported`（工具做不到）、`manual_checks`（需人工）、`unspecified_defaults`（规范没写、用了默认）。
> 它们每次运行都会打到 stderr，不会被悄悄忽略。

---

## 阶段 1 — 选形式：表还是图

对照 `references/exhibit-selection.md`。核心是一条：

**表用来查数，图用来看形。**

- 读者要核对「这个系数是 .53 还是 .35」→ 表
- 读者要看出「高承诺组随信任上升得更快」→ 图

两者都能做到时，**选表**——信息密度更高，审稿人核对更方便。

### 几条反向规则（要主动说「不」）

学生普遍爱画图。以下情况应当明确劝阻：

| 情形 | 应当说 |
|---|---|
| 只有 2–3 个数值 | 「两个数写进句子里就行，不必画柱状图」 |
| 想画饼图 | 「改成表或条形图，人读角度不准」 |
| 想画双 Y 轴 | 「两个纵轴比例可以任意调，读者判断不了谁涨得快」 |
| 想用图展示相关矩阵 | 「相关矩阵必须用表，读者要查数」 |
| 一幅图塞了框架 + 测量 + 结构 | 「拆成三幅，每幅承担一个论证任务」 |

---

## 阶段 2 — 生成

八个脚本。**布局只算一次，两种渲染器共用同一批坐标**：
SVG 由内置渲染器直接产出（零依赖），PDF/PNG/TIFF 由 matplotlib 重画同一批图元。
所以「装了 matplotlib」与「没装」出的图，几何逐点一致，不会各走一套。
外部依赖只有两处：生成 .docx 要 python-docx，导 PDF/位图要 matplotlib。

| 产物 | 脚本 | 输出 |
|---|---|---|
| 三线表 | `scripts/make_table.py` | `.docx`（另可 `--tex`） |
| 概念框架 / 测量模型 / 结构模型 | `scripts/make_diagram.py` | `.svg`（可 `--export pdf,png`） |
| 交互效应图 | `scripts/make_interaction.py` | `.svg`（可 `--export`） |
| 组间均值 / 系数图（点图 + CI） | `scripts/make_estimate_plot.py` | `.svg`（可 `--export`） |
| 多系列折线 + 置信带 | `scripts/make_line_plot.py` | `.svg` |
| (a)(b) 多面板合成 | `scripts/make_panel.py` | `.svg` |
| — | `scripts/svg_kit.py` | 绘图基元 + 图元清单，被上面四个调用 |
| — | `scripts/mpl_backend.py` | matplotlib 渲染后端（PDF / PNG / TIFF） |
| — | `scripts/selftest.py` | 自检：一次跑完上面全部并验证规则 |

### 表格

```bash
python scripts/make_table.py spec.json table1.docx --tex
```

**列该怎么摆，先查 `references/table-types.md`。** 八种常见表型：描述统计与相关矩阵、
回归/层级回归、中介、调节（含简单斜率）、**有调节的中介**、组间比较、样本特征、信效度。
每种都写了「必须报告什么」与「最常见的错法」。
可直接运行的示例规格在 `assets/table_specs/`（文件名以 `.example.json` 结尾，
数字是示例，换成真实结果后删掉 `_note` 那一行）。

spec 的最小结构：

```json
{
  "number": "1",
  "title": "Descriptive Statistics and Correlations",
  "format": "apa7",
  "columns": [{"key": "var", "label": "Variable"}, {"key": "m", "label": "M"}],
  "rows": [{"var": "1. Brand trust", "m": "4.21"}],
  "notes": {"general": "N = 344.", "probability": "**p < .01."}
}
```

数字列建议写 `"decimals": 2`：APA 要求**按小数点对齐**，而右对齐只在各格
小数位相同时才等价。小数位不一致时 `check_figure.py` 会报警。
`align: "decimal"` 只做右对齐、不猜小数位——把 `.5` 自动补成 `.500`
等于替作者声明了并不存在的精度。完整字段见 `references/format-specs.md`。

`profile` 指定版式（内置名或 `.json` 路径）；旧写法 `format: apa7 | zh | custom` 仍可用，
`custom` 的含义是「以 APA 为底，用 `style` 覆盖」。`style` 里的字段名写错会**直接报错**——
静默忽略拼错的键，是这类工具最坏的行为。

```json
{"profile": "zh-journal", "style": {"size": 10.5}, "columns": [...]}
```

完整字段见 `references/format-specs.md`。

**列宽按「最长的单词」定下限，不是按网格均分。** 单元格窄于一个单词时，
Word 会**从词中间断开**（`Relational` → `Relationa / l`）——折行是排版差异，
断词是缺陷，读者会当成拼写错误。生成时保证这条，`check_figure.py` 用
PFT-TBL-013 独立复核。列宽下限之和超过 `table_width` 时脚本会报出实际需要多少 pt，
并说明三条出路：调宽、调小字号、缩短列名——**不会硬压成断词**。

**统计符号必须斜体。** 单元格与表注支持行内标记 `<i>` `<b>` `<sup>` `<sub>`：

```json
{"label": "<i>B</i>"}          "notes": {"general": "<i>N</i> = 344."}
```

APA 要求 *B*、*SE*、*t*、*p*、*M*、*SD* 斜体，而 **β、α、χ² 不斜体**。
纯文本表做不到这一条，而它是投稿件里最显眼的格式错误。`--tex` 会转成 `\textit{}`。
带标记的单元格不参与 `decimals` 格式化（否则补零会把标签改坏）。

**多面板表**（中介/调节/多研究对比常见）用 `panels` 而不是拆表：

```json
{"panels": [
  {"label": "A: 路径系数", "stub": "",
   "columns": [{"label": "X (1)", "span": 2}, {"label": "Y (2)", "span": 2}],
   "rows": [{"label": "a: X → M", "values": [".41***", ".29***"]}]},
  {"label": "B: 条件间接效应", "stub": "",
   "columns": [{"label": "Attitude (3)", "span": 4}],
   "rows": [{"label": "−1 SD", "values": [".12"]}]}
]}
```

规则只有一条：**各面板数据列的跨度之和必须相等**（上面两块都是 4）。
6 列的面板每列 `span: 2`、4 列的面板每列 `span: 3`，合计都是 12——这样一个网格就能同时容纳。
凑不出相等的跨度，说明它们本来不该放进一张表，脚本会直接报错让你拆。
多面板表不走 `--tex`（LaTeX 侧还没做）。

**表太宽就放横向页**，不要靠缩字号硬塞：

```json
{"landscape": true}
```

版心随之变成「页高 − 左右边距」——Letter 是 **648 pt（9 in）**，A4 是 697.5 pt。
不写 `table_width` 就铺满版心。`page` 段在 profile 里（`size: letter|a4`、`margins_in`），
中文期刊与学位论文多为 A4，需要自行改。

三条边界：

- **横向页是整份文档的页面设置**，不是「表旋转 90°」。投稿系统与学位论文都接受这种做法；
  若目标刊要求表本身旋转（reader 转页），得另做。
- **`--tex` 只加一行注释**提醒用 `sidewaystable`，不生成旋转环境。
- 表宽超过版心时 `check_figure.py` 报 **PFT-TBL-014**，并说明是纵向页还是横向页——
  Word 会把最右一列挤出页面，屏幕上却看不出来。

**一个格子装多个值**（多研究对比、上下两组数字）写成列表，一格多行：

```json
{"label": "A", "key": "A", "decimals": 2}
...
{"A": [".75", ".90", ".88", ".86"]}
```

每个元素是**一段**，不是用换行符连起来的——软换行（Shift+Enter）不会让各值
各自对齐，复制出去还会粘成一整段。`decimals` 逐行生效；行内标记也照用
（`["<b>.75</b>", ...]` 标对角线）。

配套的判据都已按「逐行」改过：前导零、小数位一致、断词、数字核对，
不会因为一格多行而漏查或误报。下三角留空就写 `""`——工具不会替你补破折号，
因为「空着」和「不适用」在统计上不是一回事，该由作者在表注里说明。

### 示意图

```bash
python scripts/make_diagram.py model.json figure1.svg --geometry figure1.geo.json
```

模型描述（节点、边、调节变量、控制变量）见 `references/diagrams.md`。
自动分层、自动绕开中间节点、标签自动避让。

**连线不是按方向硬连的**：出入口边在 16 种组合里按代价挑（穿框 > 交叉 > 贴边），
并且禁止线钻进自己两端节点的框内。净空阈值 10 pt。

**调节变量指向边、不指向节点**——这是概念框架图最容易画错的一处，脚本已按正确画法实现。

**测量模型里潜变量之间是相关，必须双向箭头**（`"bidirectional": true`），且不标 H；
单向箭头只用于结构模型的因果路径。`"type": "measurement"` 时脚本会自动检查这一条，
写错会直接给警告。双向箭头两端各留 7 pt，所以行距（`row_gap`）要 ≥ 36。

`--geometry` 会另存一份坐标快照，供 `check_connections.py` 精确核对。

**写规格前先校验**，比生成失败后再看回溯快：

```bash
python scripts/make_diagram.py model.json out.svg --validate
```

它会一次性列出所有问题（id 打错、键名拼错、调节变量只给一个端点、
measurement 里潜变量之间漏了双向箭头…），并给出可用值。

### 交互效应图

```bash
python scripts/make_interaction.py fig.svg --data d.csv --dv y --x x --mod m \
       --xlabel "Brand trust" --ylabel "Purchase intention"
```

从数据拟合 `y = b0 + b1·x + b2·m + b3·x·m`，在 m 的 **均值 ± 1 SD** 处画两条线，
带 95% 置信带，同时报出交互项系数与简单斜率。

若原始研究确实做了二分操纵（高/低两组），用 `--levels 0,1` 显式指定。

### 多系列折线（N 条线 + 置信带）

```bash
python scripts/make_line_plot.py fig2a.svg spec.json --export pdf,png --dpi 600
```

三条以上系列、带置信带、分类横轴（阶段/组别）都用这个。规格见 `references/line-plots.md`。

与交互效应图**共用同一段画图代码**（`line_core.py`）——两份实现迟早会漂移，
今天交互图对了、折线图错位，看代码看不出来。

三条硬规矩：

- **不靠颜色区分系列。** 默认按顺序给实线/长虚线/点线/点划线，配四种标记。
  黑白印刷会把三种彩色印成三条一样的灰线，这是最常被退稿的原因之一。
- **有自然边界的量必须给 `y_range`。** 李克特 1–7 的数据在 3.8–4.4 之间时，
  自动缩放会把纵轴压成 3.75–4.45，读者以为差异很大。脚本会在检测到这种数据时提示。
- **置信带要么两端都给，要么都不给。** 只给 `lo` 不给 `hi` 直接报错，不替你猜。

### 估计图（几组均值 / 几个系数）

```bash
python scripts/make_estimate_plot.py figure2.svg --data d.csv --dv y --by cond \
       --xlabel "Mean purchase intention (95% CI)"
```

也可以从汇总值画（均值与区间都已知时）：

```bash
python scripts/make_estimate_plot.py figure2.svg spec.json --validate   # 先校验
python scripts/make_estimate_plot.py figure2.svg spec.json
```

**默认点图，不是柱状图**——理由见 `references/exhibit-selection.md`：
柱状图必须从 0 起，而均值的零点常常没有意义，差异被压成柱顶的一小截。
柱状图用 `"style": "bar"`，留给比例、频次这类 0 有意义的量。

**只给 `est` 不给 `lo`/`hi` 会直接报错。** 误差棒的长度是结论的一部分，
脚本不替你估。`--data` 按 t 分布算区间（`t(.975, n−1)·SE`），不是 1.96：
n = 11 时 t = 2.23，用 1.96 会把区间画窄 12%。

两组并排（如两个研究里的同一批系数）用 `--by2`，或在 spec 里写两个 `series`；
黑白印刷靠**点形状**区分（圆 / 方 / 三角 / 菱形），不靠颜色。

### 多面板：(a)(b)

```bash
python scripts/make_panel.py figure2.svg --panels 2a.svg 2b.svg \
       --labels "(a),(b)" --note "Error bars are 95% CIs."
```

同一论证任务的几幅小图必须合成一幅图、共用一条图题；分别编号成 Figure 2 与
Figure 3 会被要求合并。合成只做平移与等比缩放，不重排内容。

**缩放会缩小字号。** 脚本报出缩放后的有效最小字号，低于 8 pt 就不能投稿——
这时应当把面板画窄（`--width`）或拆成两幅，而不是硬缩。

### 导出：PDF 与位图

```bash
python scripts/make_diagram.py model.json fig1.svg --export pdf,png --dpi 600
```

同一批图元由 matplotlib 重画成 **PDF**（矢量、字体嵌入）与 **PNG/TIFF**（不透明、带 DPI）。
`--gray` 按灰度渲染，用来确认黑白印刷时各系列仍分得清。
没装 matplotlib 时**明确报错并给安装命令**，不会只出 SVG 却假装导出了。

脚本会如实报告字体：找不到 Times New Roman 时说明用了什么替代；中文字形缺失会列出
具体字符——印出来是方框，事后无法补救。

---

## 阶段 3 — 自检（必做）

```bash
python scripts/check_figure.py figure1.svg table1.docx
python scripts/check_connections.py figure1.geo.json    # 示意图专用
```

`check_figure.py` 检查：图宽是否超过 6.5 in、字号是否低于 8 pt、线宽是否过细、
**文字是否超出画布**、表格是否有竖线、表头是否有下边线、单元格是否有残留空文本、
前导零是否与档位一致、同一列的小数位是否一致。

`check_connections.py` 检查连线的几何：**线离无关方框是否 ≥ 10 pt、有没有从框里穿过、
线线交叉几处、每个编号离自己那条线多远、编号是否互相重叠、箭头端点落在哪条边**。

**报错就修，不要绕过。** 这两个脚本抓到的问题在印刷阶段都会被放大。

编号归属是最容易被忽略的一项：判据是「离自己那条线 ≤ 17 pt，且比离任何别的线近 ≥ 3 pt」。
只满足第一条不够——夹在两条平行线中间的编号，读者会把它读成更近的那条。

### 文件层：导出的东西能不能投

```bash
python scripts/preflight.py figure1.png figure1.pdf --dpi-min 300 --json qc.json
```

`check_figure.py` 查的是**规格**（图幅、字号、线宽、边框、前导零、越界），
`preflight.py` 查的是**文件本身**：DPI 元数据、透明通道、PDF 字体是否嵌入
（以及有没有 Type 3）、可疑码位（U+FFFD、私用区）、声明的字体有没有所用字形、
颜色转灰后的亮度差、同名不同后缀的文件尺寸是否一致。

两类问题性质不同：规格错了改脚本重生成；文件不合格要改导出参数。
**这一层刚加上就抓到两处真问题**——matplotlib 默认把字体嵌成 Type 3（多数期刊拒收），
PNG 即使 `transparent=False` 也照写 alpha 通道（投稿系统常按透明拒收）。

### 抄录层：数字与来源核对

```bash
python scripts/check_numbers.py table5.docx source.pdf --page 15
```

从 PDF、软件输出或截图**抄完表**之后跑一遍：表里每个数字能不能在来源中找到。
抓抄错一位、漏抄一行、凭空多一个数。**只报「找不到」，不判对错**。

**它查不到符号**，所以会单独提醒：「docx 里有 15 个负数，来源只找到 3 个负号」——
PDF 文本层常丢负号（本轮复刻里 Table 5 面板 C 的八个负号全丢），
出现这条提示就必须对着高 DPI 裁图逐个核符号，别信文本层。

它同样查不到「数字对但放错格子」，那一条只能目视。

### 每条结论都有规则编号

```bash
python scripts/preflight.py --rules
```

列出规则目录（`assets/rules.json`）：每条带编号、出处、自动还是人工，
以及**这条检查查不到什么**。报告里的 `[PFT-EXP-003]` 就是它。
改检查逻辑时先改目录——否则规则会悄悄漂移。

两个检查器都能 `--json` 出报告，报告里固定写 `publication_ready_claim: false`。

机器查不了的，人眼过一遍 `references/format-specs.md` 第七节的后半张清单。

### 改过脚本之后

```bash
python scripts/selftest.py
```

一次跑完六个生成器 + 六个检查器 + 24 个负向用例 + 规则目录完整性 + profile 一致性 + 表型模板 + 多面板表 + 列宽断词 + 横向页面 + 一格多行 + 折线图 + 审图 + 导出后端，共 114 项。
**改任何脚本之后都要跑它**——「图看起来还行」骗得过眼睛，骗不过这个脚本。

---

## 阶段 4 — 交付

| 产物 | 交付形式 |
|---|---|
| 表 | `.docx`（可直接插入论文，边框是真实线，不是字符） |
| 图 | `.svg`（矢量，可插 Word、可转 PDF/EPS） |
| 投稿要 PDF / 位图 | `--export pdf,png`（matplotlib；600 dpi，无透明通道） |
| 需要 LaTeX | 同时给 `.tex`（booktabs / longtable） |

**不要把图截成 PNG 再插**。位图放大会糊，期刊通常要求 300 dpi 以上或矢量。
SVG 在 Word 里会保留矢量，转 PDF 后仍是矢量；要位图就用 `--export`，不要截图。

---

## 审核模式：别人做好的表

学生交上来一张表问「这样行吗」时用这个，不是从头生成。

```bash
python scripts/audit_table.py paper.docx --profile apa7 --json report.json
```

查的是**表格层**：表题有没有、在不在表格上方、编号与对齐；三条横线与表头下线；
表内字号是否落在允许区间且前后一致；表头统计符号斜体（希腊字母不斜体）；
前导零；同列小数位。`--table N` 只审第 N 张，多表文档逐张出结论。

**不查**页边距、行距、页眉页脚、章节编号、图表目录——那是整篇论文的排版，
超出本技能的边界。硬查会带来大量「该刊/该校本来就这样」的误报：
同一篇论文按 APA 审，风格差异能报出几十条。

报告末尾固定列出「未检查的范围」：表内每个缩写是否在表注中定义、
表里的数字与原始输出是否一致、表是否在正文中被引用。这三件事只能人来核。

> 表题的两行式（`Table 1` 一行、标题一行）与一行式都认。
> 审核器第一版只看紧邻表格的那一段，把合规的两行式判成「没有表题」——
> 现在会往回多看一段，并按 profile 的 `title_on_separate_line` 判断该用哪种。

---

## 审核模式：别人做好的图

```bash
python scripts/audit_figure.py shot.png chart.xlsx out.pdf --json report.json
python scripts/audit_figure.py chart.xlsx --rebuild fig2a.json   # 顺手导出重画规格
```

**能查什么**，按输入类型分：

| 输入 | 查什么 |
|---|---|
| 截图 / 导出位图（png / jpg / tif） | 分辨率与 DPI、像素宽度够不够铺满版心、是不是白底、四边有没有界面条带（截图特征）、彩色转灰后还分不分得清 |
| Excel 图表（xlsx） | 图表类型（饼图 / 圆环 / 雷达 / 3D 直接判必须改）、网格线、图例位置、轴标题、字号、是否只靠颜色区分 |
| PDF | **逐页**查：有没有空白页、哪些页只有位图、每张嵌入图的**有效分辨率**（像素 ÷ 放置尺寸）。整篇论文的第 1 页通常是文字页，只看第 1 页等于没查 |

**`--rebuild` 是这一节的重点**：Excel 图表里存着系列名与数据引用（`Sheet1!$B$2:$B$4`），
脚本会顺着引用把数从工作表里取出来，直接生成我们的折线图规格。
所以「审完」之后是**能重画的**，不是只说哪里不好。取到数之后补上轴标题与图注就能出图。

**整篇 PDF 只能查到「有没有矢量内容、嵌图够不够清晰」。** 图型选得对不对、坐标轴缺不缺、
系列怎么区分，必须把图单独导出后逐张审。审表更是只吃 `.docx`——PDF 里没有边框、
合并单元格、字号这些信息，拿 PDF 审表只能读到文字。

**查不了什么**（报告里逐条写明）：图表类型选得对不对（脚本只认饼图这类明显不成立的）、
数据有没有放错轴、结论是否成立、手绘稿的线条是否清楚、扫描件里的文字是否认得出来。

> 手绘稿与扫描件只能拍照/扫描成 png/tif 再进来：脚本能判分辨率和背景，
> 判不了「这张图画的是什么」。要读数据得靠人，别假装能 OCR。

---

## 硬约束

1. **先问投哪里，再动手。** 规格错了，做得再精细也是白费。
2. **学位论文必须先拿到学校格式文件。** 拿不到就先按 `zh` 做，并明确告诉用户这是待确认的默认值。
3. **表题位置按档位走，不要混。** APA 图题在上，中文期刊图题在下——这是最常被打回的一处。
4. **前导零按档位走。** 不超过 1 的统计量（r / p / α / β）在 APA 里省略前导零，中文刊保留。
5. **连续调节变量不二分。** 交互图画 ±1 SD；除非原始设计就是二分操纵。
6. **一幅图只讲一件事。** 框架、测量、结构分开画。
7. **交付前必跑 `check_figure.py`。**
8. **不编造数值。** 缺哪个数就问，不要用「大约」「示意」代替——图表里的数字会被当成真实结果。
9. **误差棒不能省，也不能由脚本猜。** 只画点不给区间，等于宣称「这个估计没有不确定性」。
   有原始数据就按 t 分布算，没有就先要到区间。
10. **多面板图共享一条图题。** 同一论证任务拆成两幅图编号，会被要求合并；
    但合成后字号低于 8 pt 说明面板本来就不该并排，应当改画窄或拆开。
11. **PASS 不等于合规。** 检查报告只覆盖 `assets/rules.json` 里列明的自动检查项；
    目标期刊或学校的其余要求必须单独核。报告里那句 `publication_ready_claim: false` 是认真的。
12. **本技能只做图表的制作与质量检查。** 不做统计估计、不拟合模型、不算效应量、
    不判断假设成立与否——那些是上游技能的活。

---

## 边界：与相邻技能的分工

**上游**（谁给我数字与结构）：`stats-results-writer`（结果段落里报的数）、
`sem-analysis-tutor`（SEM 的载荷与路径系数）、`quant-data-analysis`（描述统计与检验）、
`social-science-experiment-designer`（概念框架与假设）、
`literature-gap-synthesizer` / `systematic-review`（文献表的列）。

**下游**（我的产物交给谁）：图表做完，正文对应段落回到 `stats-results-writer`（结果）
或 `discussion-conclusion-writer`（讨论）；定稿前 `academic-citation-auditor` 会核对图表在正文里是否被引用。

**单独使用**：给一张表的内容或一组系数就能出成品。本技能**不读上游技能的文件**，
只读你给的规格——上游用什么软件、按什么格式交付都不影响。

| 问题 | 谁定 | 本技能做什么 |
|---|---|---|
| 文献综述表该放哪些列 | `literature-gap-synthesizer`、`systematic-review` | 把列做成三线表 |
| 概念框架里有哪些构念、几条假设 | `social-science-experiment-designer` | 把模型画成图 |
| 结果表里放哪些系数、报告哪些指标 | `stats-results-writer` | 把内容做成 APA 表格 |
| 测量模型与结构模型的系数从哪来 | `sem-analysis-tutor` | 画成测量/结构模型图 |
| 结论怎么写、贡献怎么讲 | `discussion-conclusion-writer` | 不管 |

**本技能不做的事**：不选检验、不解释结果、不判断假设是否成立、不写正文段落。
这些都是上游技能的活；在这里重做一遍，两处结论一旦不一致就是隐患。

---

## 资源索引

| 文件 | 用途 |
|---|---|
| `references/exhibit-selection.md` | 论点 → 该用表还是图；反向规则；一句话判定表 |
| `references/format-specs.md` | APA 7 / 中文期刊 / 学位论文 三档规格，精确到磅值 |
| `references/diagrams.md` | 模型描述的 JSON 格式；四类图的构图规则；常见错误 |
| `scripts/make_table.py` | 三线表 → .docx / .tex |
| `scripts/make_diagram.py` | 概念框架 / 测量 / 结构模型 → SVG |
| `scripts/make_interaction.py` | 交互效应图 → SVG（从数据算简单斜率） |
| `scripts/make_estimate_plot.py` | 组间均值 / 系数图 → SVG（点图 + t 分布区间，可 `--data`） |
| `scripts/make_line_plot.py` | 多系列折线图 → SVG（线型与标记区分系列，可带置信带） |
| `scripts/line_core.py` | 折线的公共画法，交互效应图与折线图共用 |
| `scripts/make_panel.py` | (a)(b) 多面板合成 → SVG（等比缩放并报有效字号） |
| `scripts/svg_kit.py` | 零依赖 SVG 绘图基元（同时记录图元清单供 matplotlib 重画） |
| `scripts/mpl_backend.py` | matplotlib 后端：PDF / PNG / TIFF、灰度渲染、字体与缺字报告 |
| `scripts/check_figure.py` | 交付前自检（规格层，按 profile 判） |
| `scripts/audit_table.py` | 审别人做好的表（只查表格层） |
| `scripts/audit_figure.py` | 审别人做好的图（截图/Excel/PDF），`--rebuild` 导出重画规格 |
| `scripts/table_checks.py` | 表格层判据，生成路径与审核路径共用这一份 |
| `scripts/textmetrics.py` | 字宽估算（Times 真实字宽表），定列宽与验列宽共用 |
| `scripts/svg_read.py` | 把 SVG 读回图元清单（多面板合成与 PDF 导出共用） |
| `scripts/preflight.py` | 交付前预检（文件层：DPI/透明/字体嵌入/字形/灰度） |
| `scripts/check_numbers.py` | 抄录层：表内数字与 PDF/文本来源核对 |
| `scripts/profiles.py` | 版式 profile：读入、合并、校验、列出状态 |
| `assets/profiles/*.json` | 版式取值 + 出处 + 状态 + 待确认/做不到/需人工 |
| `references/table-types.md` | 八种表型：列结构、必须报的统计量、常见错法 |
| `assets/table_specs/*.example.json` | 可直接运行的示例规格（数字为示例） |
| `scripts/qc.py` | 结论的统一形式（代码 + 严重度 + 局限）与 JSON 报告 |
| `assets/rules.json` | 规则目录：编号、出处、自动/人工、**每条查不到什么** |
| `scripts/check_connections.py` | 交付前自检（连线几何层，读 `--geometry` 快照） |
| `scripts/selftest.py` | 技能自检：三个生成器 + 两个检查器 + 负向用例 |
