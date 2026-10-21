---
name: "quant-data-analysis"
description: "帮助研究者（尤其是商科MS/PhD/DBA学生及教师）把实验与问卷的原始数据真正\"跑出来\"： 数据筛查（缺失、重复、离群值、排除规则留痕）、检验选择、单因素/双因素方差分析与 ANCOVA（Type III、Welch/稳健方法、简单效应、效应量、Holm校正）、操纵检验、回归调节效应 （简单斜率、Johnson-Neyman）、敏感性分析，最终产出分析记录与可交给stats-results-writer 的结果包。自带经过测试的Python脚本，上传csv/xlsx/sav/dta数据即可运行。不含SEM与中介 分析（转sem-analysis-tutor），不负责撰写Results文字（转stats-results-writer）。\n触发场景（满足以下任一条件即应使用本skill）： - 用户上传实验或问卷数据文件，要求\"跑一下\"\"分析一下\"\"检验假设\"\"做ANOVA/t检验/回归\" - 用户提到\"数据清洗\"\"数据筛查\"\"离群值\"\"排除被试\"\"注意力检查\"\"操纵检验\" - 用户提到\"ANCOVA\"\"协变量\"\"简单效应\"\"简单斜率\"\"调节效应检验\"\"Johnson-Neyman\"\n  \"效应量\"\"事后比较\"\"方差不齐\"\"Welch\"\n- 用户问\"该用哪个检验\"\"这个结果怎么跑\"\"SPSS/JASP/R里怎么做\" - 帮学生复核实验数据分析是否合规、是否存在分析自由度问题\n即使用户只是说\"数据收完了，接下来怎么分析\"，或直接甩来一个数据文件说\"看看有没有 显著\"，也应触发本skill——先确认预注册的分析计划，再进入筛查。\n"
version: 1.0.0
license: CC-BY-4.0
---

# 量化数据分析助手 — Experiment & Survey Data Analysis

## 核心理念

**这个skill负责"把数据跑出来并留下完整记录"，不负责把结果写成论文段落。** 现有分工：`sem-analysis-tutor`管SEM与PROCESS路径分析，`stats-results-writer`管把结果写成Results，本skill补上中间那一段——基础统计分析的实际执行。

三条底线，都是为了让结果经得起`dissertation-peer-review`和`management-paper-reviewer`的核查：

1. **每个分析决定都留痕**：排除了谁、为什么、按什么规则、用了哪个检验、为什么换检验。脚本会把这些写进日志，AI在对话里也要复述
2. **不"试到显著为止"**：先确认预注册的分析计划（`social-science-experiment-designer`产出的预注册文档），按计划分析；计划之外的分析一律标注为探索性
3. **数字来自代码运行，不来自口算或记忆**：AI不得心算统计量，也不得在没有数据文件的情况下"示范性地"编一个结果

> 脚本在`scripts/`下，已用模拟数据（含已知真值）测试过，并与pingouin及手写numpy最小二乘交叉核对。运行前若缺库：`pip install statsmodels pingouin pyreadstat --break-system-packages`。

## 快速入口：你目前在哪个阶段？

| 你的情况 | 进入阶段 |
|---|---|
| 刚拿到数据文件，还没看过 | **阶段0** → 阶段1 |
| 数据已清理，要选检验并运行 | **阶段2** → 阶段3 |
| 结果出来了，想检查稳不稳 | **阶段4** |
| 分析做完，要交给写作/评审 | **阶段5** |
| 数据是中介、SEM、量表开发 | 转`sem-analysis-tutor` / `scale-research` |

---

## 阶段0 — 信息与前置

先确认（缺失时询问，不要猜）：

| 信息项 | 说明 |
|---|---|
| 研究设计 | 被试间／被试内／混合；因子数与水平数；是否有协变量 |
| 因变量与自变量 | 变量名、类型（连续／分类）、量表得分是否已计算 |
| **预注册的分析计划** | 有就按它来；没有就在这一步把计划写下来，再动数据 |
| 排除规则 | 注意力检查、作答时长、重复作答等，**是否在看数据前就定好了** |
| 数据文件 | 上传后先用`file-reading` skill的方式读取，确认列名与编码 |

**若已有`research_data_spec.json`**（由`research-data-preparation`生成）：先读它，再提问。其中`data_exposure.level`是研究者接触数据的程度，`decision_status`说明每个决定是事前锁定还是数据驱动，`sample_rules`和`analysis_plan`就是预先规定的排除规则与分析计划。`pre_locked`的按计划做；`data_driven`的分析在结果里标为探索性；`evidence_status`为`needs_verification`的信息不要当作已验证。规格里写明的内容不要重复向用户询问。

若设计是被试内或混合设计、重复测量、多层数据：`scripts/`里没有现成脚本，见`references/decision-guide.md`第6节，现场写代码并先用模拟数据验证。

## 阶段1 — 数据筛查

```
python scripts/screen_data.py --file data.csv --dv 因变量 --factors 因子1,因子2 \
       --id 被试编号 [--exclude "attn != 1"] [--exclude "duration < 60"] --outdir screen_out
```

它做的事：缺失与重复检查、按规则排除并**写入exclusion_log.csv**、各单元格样本量、按单元格用中位数/MAD规则**标记**离群值（只标记，不删除）。

读输出时：
- 单元格样本量差异大或很小，直接告诉用户后续检验的可靠性会受影响
- 离群值的处理是研究者的决定，理想情况是分析前就定好规则；没定好的，做"含/不含"两版并都报告（阶段4）
- 排除后样本量要能在Methods里对上：总收集N、各条排除规则各排除多少、最终N

## 阶段2 — 选检验

对照`references/decision-guide.md`第1节的选择表。几个默认做法：

- 两组比较、单因素多组：**默认看Welch版本**，不要用Levene检验当"守门员"决定用不用（Delacre et al., 2017, 2019）
- 双因素及以上：Type III平方和＋sum-to-zero编码；方差明显不齐时加`--robust`
- 有协变量：先看斜率同质性；协变量若是被处理影响的变量，不该放进去（见guide第4节）
- 多重比较用Holm校正，效应量一律报告并说明是哪一种

## 阶段3 — 运行

**方差分析／ANCOVA**（1或2个分类因子，可加协变量）：

```
python scripts/factorial_anova.py --file data_clean.csv --dv y --factors A,B [--covariate c] [--robust]
```

输出：单元格描述统计、假设诊断、ANOVA表（F、p、偏η²、偏ω²）、交互显著时的简单效应（Holm校正、置信区间、d）、ANCOVA的斜率同质性与调整后均值；单因素时同时给出Welch ANOVA与Games-Howell。

**回归调节效应**（连续或二分预测变量×连续调节变量）：

```
python scripts/simple_slopes.py --file data.csv --y 结果 --x 预测 --m 调节 [--covariates c1,c2] [--robust]
```

输出：回归系数、交互项的ΔR²、±1SD处的简单斜率、Johnson-Neyman显著区间。

**其他检验**（卡方、非参数、相关等）：现场用Python写，先说明选择理由，写完用已知答案的小例子验证一遍再用于用户数据。

## 阶段4 — 诊断与敏感性分析

结果出来后，至少做这几项，把差异**如实报告**，不挑对自己有利的那一版：

| 检查 | 做法 |
|---|---|
| 排除规则的影响 | 含全部被试 vs 按规则排除后，结论是否一致 |
| 离群值的影响 | 含 vs 不含被标记的离群值 |
| 方差不齐 | 经典F vs `--robust` / Welch，结论是否一致 |
| 操纵检验 | 操纵检验本身的结果要先报告，再谈假设检验（关联`social-science-experiment-designer`的操纵检验设计） |
| 探索性 vs 验证性 | 预注册之外的每个分析，明确标注"探索性" |

若显著性在不同合理处理下会翻转，如实告诉用户：这个结果不稳，写作时不能写成稳健发现。

## 阶段5 — 交付

产出两样东西（模板见`references/analysis-log-and-handoff.md`）：

1. **分析记录**：文件、N变化流水、排除规则与人数、检验选择及理由、偏离预注册之处、敏感性分析结论、运行的脚本与参数
2. **结果包**：可直接交给`stats-results-writer`的完整统计量（F/t、自由度、p、效应量及置信区间、均值与标准差、样本量）

交付前提醒用户：`dissertation-peer-review`会查缺失数据与离群值处理、操纵检验、效应量、分析自由度，这份分析记录就是应对这些核查的材料。

---

## 参考文件

- `references/decision-guide.md`：检验选择表、假设与稳健方法、效应量、多重比较、ANCOVA注意事项、离群值、被试内/混合设计怎么办、文献出处
- `references/analysis-log-and-handoff.md`：分析记录模板、交给`stats-results-writer`的结果包清单

## 重要原则

1. **数字来自运行结果**：不心算、不凭记忆、不在没有数据时示范性地编造结果
2. **决定必须留痕**：排除、变换、换检验、剔除离群值，都要写进记录，并在对话里复述
3. **计划先于数据**：按预注册分析；计划之外的分析标注为探索性
4. **不替研究者做取舍**：离群值删不删、显著性不稳时怎么写，AI给出选项与后果，判断权在研究者
5. **边界清楚**：中介与SEM转`sem-analysis-tutor`，写Results转`stats-results-writer`，量表开发转`scale-research`
