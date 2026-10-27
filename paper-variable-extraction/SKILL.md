---
name: paper-variable-extraction
license: CC-BY-4.0
description: "从学术论文中系统提取全部变量及其操作化信息（概念性定义、测量量表原始题项、响应量尺、信度、量表来源、实验刺激材料与操纵流程、操纵检验、二手数据来源与编码、质性编码方案），并可选输出 Excel 变量表（元分析编码友好）。当用户上传/指定论文并要求提取变量、变量操作化、构念定义、测量量表、题项、信度效度、实验材料、操纵检验、变量定义表、编码说明、假设与结果时触发。关键词：变量提取、操作化、operationalization、measurement、scale items、Cronbach、manipulation check、stimuli、vignette、变量说明表、codebook"
---

# 论文变量操作化信息提取 / Paper Variable Operationalization Extraction

> **Goal**：把一篇（或多研究）学术论文中的**所有变量**及其**操作化细节**，整理成结构清晰、可直接复用的变量词典（codebook），并刻画研究地图与假设验证情况。

## When to Use

- 用户上传/指向一篇论文（PDF、Word、Markdown、图片、文本粘贴均可），要求提取变量、变量操作化、构念定义、测量量表、题项、信度、来源、实验刺激材料、操纵检验、变量编码、假设与结果等
- 用户要求做「变量说明表」「变量对照表」「codebook」「量表汇总」「元分析编码表」

## When NOT to Use

- 用户要的是论文全文翻译、摘要、文献综述或批判性评价（变量只是顺带提及）
- 用户要的是统计结果（回归系数、效应量）本身，而非变量定义与假设验证结论

## 工作流

### Step 0 · 获取论文内容

1. 先定位用户提供的文件。各环境的上传目录不同（有的是只读挂载），**以用户给出的路径为准**；路径含中文或空格时用双引号包裹。
2. **先判断 PDF 有没有文本层**：抽一遍文本，字符数接近 0 就是扫描件（`pymupdf` 的 `page.get_text()` 返回空）。扫描件按下面三步走，**不要跳过**：
   - **渲染成图再读**：`page.get_pixmap(dpi=170)` 逐页导出 PNG，再逐页识读。本机通常没有 tesseract，不要假设能调 OCR。
   - **密集表格必须放大**：Table、附录这类小字号区域，用 `clip=` 裁出该区域，以 **≥350 DPI** 重渲染后再读。**凭整页图读系数、信度、样本量一定会错**——实测过：整页读一张结构模型表读错 4 个路径系数，放大后才纠正。
   - **同一数字交叉核对**：若某数值在正文、表格、附录三处都出现，逐处比对；不一致按「原文内部不一致」如实并列。
3. **不要凭标题或摘要臆测内容**——必须读到全文，尤其**附录、Table、Appendix、脚注、web appendix、supplementary materials**。题项与刺激材料常藏在这些位置。检索线索："Appendix"、"web appendix"、"Table 1"、"α"、"Items"、"7-point"、"Likert"、"Procedure"、"Stimuli"、"Pretest"。
4. **正文出现外部补充材料链接时，主动抓取**。常见形式：`online supplement`、`web appendix`、`https://ssrn.com/abstract=...`、`aspredicted.org/...`、`osf.io/...`、期刊官网 supplementary materials。
   - **优先抓预注册**（aspredicted / OSF）——通常含完整题项、操纵文本、排除规则，比正文更全。
   - **用所在环境提供的网页抓取能力抓**，不要用命令行 `curl`：期刊与预注册站点常有 WAF，curl 会返回 403/406，环境自带的抓取工具通常能过。
   - 抓到的材料并入对应研究的 `manipulation_materials` / `items_text`，并在 Studies 表 `preregistration` / `supplement_location` 记录链接。
   - **抓不到就明确记录**：在「信息缺口清单」里单列一类**「外部补充材料不可及」**，写明 URL、该材料包含什么（如"实验操纵全文"）、失败原因（403 / 需登录）。**绝不因为抓不到就跳过或编造。**

### Step 1 · 研究方法清单（不是单一判定）

**多研究论文必须逐个研究判定方法**（同一篇文章完全可能是质性 + 调查 + 实验 + 二手数据）。对每个 Study / Experiment / 分析单元给出方法类型：

| 判定依据 | 分支 | 参考文件 |
|---|---|---|
| 随机分配、实验组/控制组、刺激材料、manipulation check | **A. 实验设计法** | `references/experiment.md` |
| 问卷/量表施测、自陈报告、Cronbach's α、Likert | **B. 问卷调查法** | `references/survey.md` |
| 数据库、档案数据、公开统计指标、面板数据 | **C. 二手数据法** | `references/secondary-data.md` |
| 访谈、焦点小组、民族志/网络民族志、参与观察、扎根理论、现象学、案例研究、主题分析、内容分析、话语分析、开放式编码 | **D. 质性方法** | `references/qualitative.md`（民族志另见 §8） |
| 系统性/整合性文献综述、理论构建（有检索式、纳入文献数、编码段落数、编码方案） | **E. 文献综述型理论构建** | `references/qualitative.md` §7 |
| 效应量合成（Cohen's d / r / OR）、meta-regression、异质性 I²、发表偏倚检验、森林图/漏斗图、纳入文献数与效应量数 | **F. 元分析** | `references/meta-analysis.md` |
| 自训分类器/神经网络测量构念（图像、文本、音频、行为日志）、fine-tune、AUC、人类对照验证 | **G. 计算测量法** | `references/computational-measurement.md` |
| 形式化建模：效用函数、均衡、一阶条件、比较静态、命题/引理（博弈论、最优化、结构模型的理论部分） | **H. 分析模型** | `references/analytical-modeling.md` |

**综述型理论构建也算一个研究单元**（即使没有"样本"）。管理学期刊常见「先综述构建理论，再用 2–3 个研究检验」；综述提炼出的维度要作为构念录入 Variables，并在 Studies 表占一行（`method_type = Literature Review`）。

**计算测量 ≠ 二手数据**：二手数据问「数据从哪来」，计算测量问「**测量工具怎么造**」。一篇论文可以同时属于两者（用 Instagram 的图喂给自训的分类器）。判定：若换一批同类数据、结论仍成立 → 二手数据；若结论依赖作者新造的模型 → 计算测量。

**分析模型 ≠ 文献综述型理论构建**：E 从**文献**归纳命题，H 从**假设**演绎命题。判定问一句：**有没有形式化的目标函数或均衡？** 有 → H。

**元分析 ≠ 文献综述**：综述产出构念与命题，元分析产出**可量化的效应量**。判定线索是 "effect size"、"Cohen's d"、"meta-regression"、"I²"、"fail-safe N"、"funnel plot"、"k effect sizes"。元分析的提取单元是**效应量与调节变量编码**，产出必须有 `EffectSizes` 表（字段见 `references/meta-analysis.md` §2）。

- 判定后**按需读取**对应 reference 文件（不要一次全读），严格按字段清单执行。
- 若某研究同时含两种数据收集（如实验 + 二手数据校验），标注为「混合」，两种分支的字段都要填。

### Step 2 · 研究地图（多研究论文必做）

在变量提取**之前**先建立研究地图，说明：

- **研究数量**：共几个 Study / Experiment（含预测试、后测、附加研究，只要报告了数据就计入）
- **每个研究的目标**：一句话说明该研究回答什么问题
- **研究间关系**：推进逻辑（如「E1 建立主效应与中介 → E2 通过操纵中介做调节验证 → E3 换刺激排除替代解释 → E4 边界条件 → E5–6 现实情境与下游结果」）
- **方法分布**：哪个研究用哪种方法（多方法论文在这里一眼可见）
- **样本**：每个研究的 n、样本来源（学生 / Prolific / MTurk / 数据库年份等）

判断研究间关系的常见类型：主效应验证 → 机制检验（中介/调节）→ 排除替代解释 / 稳健性 → 边界条件 → 外部效度与现实结果 → 复制（exact replication）。

### Step 3 · 提取变量与假设

**变量提取**：覆盖 **IV、DV、Mediator、Moderator、Control**，以及操纵检验变量、协变量。每个变量必含：

- **变量名称 / Variable Name**：原文英文名 + 中文译名
- **概念性定义 / Conceptual Definition**：作者给出的理论/抽象定义，引用原文 + 中文翻译；不要自行概括改写

再按各研究的方法分支补充操作化细节。

**跨研究共用变量（重要）**：同一变量在多个研究中重复出现时，**合并呈现一次**（概念定义、题项、量尺只写一遍），再用一张**跨研究对照表**列出各研究中的差异（信度 α、来源、是否改编、n）。禁止同一量表重复描述 N 遍。

**假设与验证结果**：抽取每个研究检验的假设（含 H1、H2… 或文中隐含的研究预期），并给出：假设内容（原文 + 中文）、涉及的 IV/DV/中介/调节、检验方法、统计结果、**是否支持**（支持 / 部分支持 / 未支持 / 反向）。文中未编号的预期用「研究预期 1」等表述，并标注「原文未编号」。

**刺激材料（实验类必做）**：按 `references/experiment.md` 的刺激材料表逐项提取，粒度到「具体词语、图片类型、情境故事原文」。

### Step 4 · 输出

两份产物，**都要给**：

1. **Markdown 报告** — 结构见 `references/output-format.md`，保存为 `变量操作化提取_<论文简称>.md`（放在用户指定的输出目录）
2. **Excel 变量表** — 字段规范见 `references/excel-codebook.md`，用 `scripts/export_codebook.py` 生成同名 `.xlsx`（同一目录）

生成 Excel 的流程：把提取结果整理成 JSON（schema 见 `references/excel-codebook.md`）写到临时目录，**先校验再导出**：

```bash
# 1) 预检：JSON 语法 + 结构 + 受控词表 + 变量名一致性
python3 scripts/export_codebook.py <input.json> --validate

# 2) 校验通过后再导出（会顺带输出研究地图源码）
python3 scripts/export_codebook.py <input.json> <output.xlsx>

# 只想看研究地图源码，不生成文件
python3 scripts/export_codebook.py <input.json> --mermaid
```

写 JSON 时**中文一律用「」而不是英文双引号**，可避免 90% 的解析失败；若解析失败，脚本会直接报出行号、列号、出错行上下文与修复建议，按提示改即可。

报告中的研究地图，≥3 个研究时**同时给 Mermaid 流程图**（规范见 `references/output-format.md`）。脚本会：

- 在 Studies 表末列写入 `mermaid_node`（逐节点的源文本，可复制拼接）
- 输出同名 `.mmd` 文件，并把源码打印到终端，直接粘进报告 1.2 节
- 按 `key_finding` 为每个节点生成悬停 tooltip

**自动串联的边几乎总要手工校正**（会把 pretest 排进主链条），用顶层 `mermaid_edges` / `mermaid_groups` 覆盖后再重新导出。

对话中输出**精简版报告**（研究地图 + 变量总览表 + 核心量表题项 + 假设与结果 + 信息缺口），完整版在文件里。

## 语言规则（强制）

1. **响应语言跟随用户查询语言**：中文提问 → 全篇中文；英文提问 → 全篇英文。
2. **量表与题项一律中英对照输出**：英文原文 + 中文翻译并排。
3. **刺激材料原文（vignette、指令语、提示语）保留英文原文 + 中文翻译**。
4. 变量名、量表名称、期刊名、APA 文献条目保留原文。

## 通用质量要求

- **逐字（verbatim）**：题项原文、刺激材料关键措辞、操纵指示语照抄，不做润色。
- **信度**：报告具体指标（Cronbach's α、CR、ω、κ、Krippendorff's α、test-retest 等）及数值；分研究、分维度给出时分别列出。
- **来源**：完整 APA 格式，并注明「改编 Adapted from」还是「采用 Adopted from」。文中未标明出处时写「原文未提供」。
- **缺失处理（重要）**：文中确实没写的字段写 `原文未提供`（Excel 中写 `NA`），并在「信息缺口清单」集中列出。**绝对禁止编造题项、信度数值、APA 出处、数据来源指标代码、统计结果。**
- **原文内部不一致**（如正文说 14 个材料、附录列 15 个）如实并列标注，不要替作者挑一个。

## 资源索引 / References

- `references/output-format.md` — 输出模板、跨研究变量合并表、研究地图、质量自检清单
- `references/experiment.md` — 实验法：刺激材料表、操纵细节、操纵检验
- `references/survey.md` — 问卷法：字段清单 + 示例
- `references/secondary-data.md` — 二手数据法：来源粒度 + 编码
- `references/computational-measurement.md` — 计算测量法：模型开发/验证/应用、六条红线、字段映射
- `references/analytical-modeling.md` — 分析模型：设定/假设/参数/均衡/命题/比较静态、五条红线
- `references/qualitative.md` — 质性方法：取样、提纲、编码方案、编码者信度
- `references/excel-codebook.md` — Excel 字段规范与 JSON schema
- `scripts/export_codebook.py` — JSON → xlsx 生成脚本

---

## 交接：从哪来、到哪去

| 方向 | 技能 | 交接什么 |
|---|---|---|
| 上游 | `phenomenon-to-question` | 研究问题定了，才知道该读哪些文献、盯哪几类变量 |
| 上游 | `literature-gap-synthesizer` / `systematic-review` | 待读文献的清单；系统综述还给出筛选后的最终集合 |
| 下游 | `scale-research` | 提取到的量表与原始题项——正是它要评估、翻译与改编的输入 |
| 下游 | `social-science-experiment-designer` | 别人怎么操纵、怎么测量这个构念，直接决定实验材料怎么写 |
| 下游 | `paper-figures-tables` | 提取结果整理成**文献编码矩阵表**（三线表） |
| 下游 | `academic-writing-assistant` | 写文献综述时引用：谁用了什么量表、在什么情境、结果如何 |

**单独使用**：给一篇（或一批）PDF 就能产出 Markdown 报告 + Excel 变量表，不需要上游提供任何特定格式。
本技能**不读上游技能的文件**，只读你给的论文——文献清单从哪来不影响提取流程。
