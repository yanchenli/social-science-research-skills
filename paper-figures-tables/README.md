# paper-figures-tables

> 学术图表的制作与质量检查 —— 把论文里的图和表做成可投稿、可印刷的样子。

**版本**：1.11.5 ｜ **适用**：商科 MS/PhD 学生、教师，以及需要审学生稿件的指导教师
｜ **规模**：SKILL.md + 5 个 references + 21 个脚本

**中文** | [English](README.en.md)

---

## 它解决什么问题

论文被退回，很多时候不是因为结论不对，而是因为图和表不像投稿件：

- 表格是 Word 默认的**全框线**，APA 要三线表；
- 列宽**等分**，长变量名列被挤成两行，或者数字列空着半截；
- 统计符号**没斜体**——*M*、*SD*、*t*、*p* 该斜体，β、α 不该；
- 前导零**用反了**：APA 对 *r* / *p* / α 省略前导零，对 *M* / *SD* 保留；
- 图**没有轴标题**、带**网格线**、用**饼图**表达份额；
- 彩色系列**黑白打印后分不清**；
- 导出的图是**截图**，300 dpi 都不到。

这些都不是学术判断问题，是**呈现规范**问题——有明确的对错，可以机器查。
这个技能做的就是两件事：**按规范生成**，以及**按同一套规范检查**。

---

## 核心理念

**1. 只做呈现，不做分析。**
不选检验、不算效应量、不判断假设是否成立。这些是上游技能的活；在这里重做一遍，
两处结论一旦不一致就是隐患。

**2. 生成与检查共用同一份规则。**
版式取值全部在 `assets/profiles/*.json` 里，带出处、状态与「工具做不到什么」的说明。
生成和检查读同一份——否则会出现「生成按 APA、检查按另一套」这种最难查的问题。

**3. 一份布局，两个渲染器。**
SVG 由内置渲染器直接产出（零依赖）；同一批图元交给 matplotlib 重画成 PDF/PNG。
几何只算一次，两个输出逐点一致。

**4. PASS 不等于合规。**
报告只覆盖规则目录里列明的自动检查项，末尾固定列出「未检查的范围」。
把 PASS 当合规是这类工具最危险的地方。

---

## 覆盖范围

### 表

| 表型 | 说明 |
|---|---|
| 三线表 | 描述统计与相关矩阵、信效度、回归与层级回归、中介、调节、有调节的中介、组间比较、样本特征 |
| 多面板表 | 一套网格 + 每个面板自带表头（各面板数据列的跨度之和须相等） |
| 横向页 | 过宽的表放横向页，版心随之变成「页高 − 左右边距」 |
| 一格多行 | 一个格子按研究竖排多个值（宽表、多研究对比） |

### 图

| 图型 | 说明 |
|---|---|
| 概念框架 / 测量模型 / 结构模型 | 自动分层、绕开中间节点、标签避让；测量模型里潜变量之间强制双向箭头 |
| 交互效应图 | 从数据拟合交互项，在调节变量均值 ±1 SD 处画两条线并带置信带 |
| 估计图 | 几组均值或几个系数 + 95% 置信区间（点图，不是柱状图） |
| 多系列折线 | N 条线 + 置信带；线型与标记区分系列，不靠颜色 |
| (a)(b) 多面板 | 同一论证任务的几幅小图合成一幅，共用一条图题 |

### 导出与检查

- **导出**：SVG（矢量）/ PDF（矢量、字体嵌入）/ PNG、TIFF（300–600 dpi，无透明通道）
- **规格层检查**：图幅、字号、线宽、边框、前导零、小数位、断词、越界、表宽超版心
- **文件层预检**：DPI、透明通道、字体嵌入与 Type 3、字形覆盖、灰度可辨、空白页
- **抄录层核对**：表里的数字与 PDF 文本层逐一比对
- **审别人的图表**：截图、Excel 图表、PDF；并能把 Excel 图表的数据导出成重画规格

---

## 工作流程

```
阶段 0  先问投哪里  →  落成 profile（APA 7 / 中文期刊 / 学位论文 / 自定义）
阶段 1  选形式      →  要表达的是数值、方向还是结构？
阶段 2  生成        →  .docx / .svg，需要时另出 PDF、PNG
阶段 3  自检（必做）→  规格层 + 文件层 + 抄录层
阶段 4  交付        →  附上「未检查的范围」
```

**审核模式**（别人做好的表或图）：走 `audit_table.py` / `audit_figure.py`，
查的是同一套判据，报告结构与生成路径一致。

---

## 使用示例

```bash
# 1. 一张 APA 三线表
python scripts/make_table.py spec.json table1.docx --tex

# 2. 概念框架图，顺带导出 PDF 并做几何审计
python scripts/make_diagram.py model.json fig1.svg --geometry fig1.geo.json --export pdf
python scripts/check_connections.py fig1.geo.json

# 3. 三条系列带置信带的折线图
python scripts/make_line_plot.py fig2a.svg spec.json --export pdf,png --dpi 600

# 4. 交付前预检
python scripts/preflight.py table1.docx fig1.pdf fig2a.png --json qc.json

# 5. 审学生交上来的图表
python scripts/audit_figure.py chart.xlsx shot.png --rebuild rebuild.json
python scripts/audit_table.py thesis_table.docx --profile apa7
```

现成的规格可以直接抄：`assets/table_specs/` 有 5 个可运行示例，
`references/format-specs.md`、`table-types.md`、`diagrams.md`、`line-plots.md` 里各有结构说明。

---

## 目录结构

```
paper-figures-tables/
├── SKILL.md                主流程（阶段 0–4）+ 硬约束 + 边界
├── scripts/   21 个
│   ├── 生成器 6    make_table / make_diagram / make_interaction /
│   │               make_estimate_plot / make_line_plot / make_panel
│   ├── 检查器 6    check_figure / check_connections / check_numbers /
│   │               preflight / audit_table / audit_figure
│   └── 共用 9      svg_kit / line_core / svg_read / textmetrics /
│                   table_checks / profiles / qc / mpl_backend / selftest
├── references/ 5 篇   format-specs / table-types / diagrams / line-plots / exhibit-selection
└── assets/
    ├── profiles/ 3 档  apa7 / zh-journal / thesis-template
    ├── table_specs/ 5  可直接运行的示例规格
    └── rules.json      60 条规则，每条带出处与「查不到什么」
```

**依赖**：`python-docx` 必需；`matplotlib`（PDF/PNG）、`PyMuPDF`（PDF 检查）、
`Pillow`（位图检查）可选——缺任何一个只降级为「未检查」，不假装通过。

---

## 边界与注意事项

- **不判断内容对不对**：图表类型选得合不合适、数据有没有放错轴、结论是否成立，都要人看。
- **审表只吃 `.docx`**：PDF 里没有边框、合并单元格、字号这些信息。
- **整篇 PDF 审图只能查**「有没有矢量内容、嵌图够不够清晰」；图型与坐标轴要逐张导出后审。
- **不做**：雷达图、信息图型概念框架、统计估计。

`selftest.py` 是这个技能自己的守门人：114 项，改任何脚本之后都要跑。

---

## 与相邻技能的分工

| 方向 | 技能 | 交接什么 |
|---|---|---|
| 上游 | `stats-results-writer` | 结果段落里报的数 |
| 上游 | `sem-analysis-tutor` | SEM 的载荷与路径系数 |
| 上游 | `quant-data-analysis` | 描述统计与检验结果 |
| 上游 | `social-science-experiment-designer` | 概念框架与假设 |
| 上游 | `literature-gap-synthesizer` / `systematic-review` | 文献表的列 |
| 下游 | `stats-results-writer` / `discussion-conclusion-writer` | 图表做完，正文对应段落 |

**单独使用**：给一张表的内容或一组系数就能出成品。本技能**不读上游技能的文件**，
只读你给的规格——上游用什么软件、按什么格式交付都不影响。

---

## 版本

1.11.5 — 见 `SKILL.md` 的版本号，报告里的版本也取自那里（单一来源）。
