# Excel 变量表规范 / Excel Codebook Schema

目标：**一列一个字段**，一行一个变量（或一行一题项），可直接用于元分析编码、量表库建设、跨论文比对。

## 工作表结构（7 个 sheet）

| Sheet | 行粒度 | 用途 |
|---|---|---|
| `Studies` | 一行 = 一个研究 | 研究地图：方法、样本、数据结构、目标、研究间关系 |
| `Variables` | 一行 = 一个「变量 × 研究」 | 主表：概念定义 + 操作化 + 信度 + 来源 |
| `Items` | 一行 = 一个题项 | 量表题项逐字对照（元分析编码核心） |
| `Indicators` | 一行 = 一个构成指标 | **二手数据**中多指标合成变量的指标清单（来源、口径、编码方向） |
| `Hypotheses` | 一行 = 一条假设 | 假设内容 + 检验类型 + 结果 + 是否支持 |
| `Stimuli` | 一行 = 一组刺激材料 | 实验材料清单（词语/图片/情境/环境） |
| `EffectSizes` | 一行 = 一个效应量 | **元分析**核心产物：对比基准 × 结果变量 × 模型 |

`Items` 与 `Indicators` **必须分开**：前者是「受访者读到的问法」，后者是「数据的来源与口径」，语义不同，混在一张表会让元分析编码无法判断该列是什么。

`EffectSizes` 只在元分析论文中使用，其余论文留空表头（保留列序以便跨论文堆叠）。

## 字段定义 · Variables（主表）

| 字段名 | 说明 | 缺失填 |
|---|---|---|
| `study_id` | 研究编号，如 `E1`、`Study2`、`GD`（总讨论研究） | — |
| `study_label` | 研究标签，如 `Experiment 1` | — |
| `method_type` | `Experiment` / `Survey` / `Secondary Data` / `Qualitative` / `Mixed` / `Expert Judgment` / `Item Sorting` / `Scale Development` | — |
| `variable_name_en` | 变量英文名（原文） | — |
| `variable_name_cn` | 变量中文名 | — |
| `role` | `IV` / `DV` / `Mediator` / `Moderator` / `Control` / `Manipulation Check` / `Confound Check` / `Alternative Explanation` / `Theme` / `Target Construct` / `Context Factor` / `Covariate` | — |
| `variable_type` | `Self-report`（自陈）/ `Behavioral`（行为）/ `Objective`（客观指标，如反应时、销售数据）/ `Manipulated`（被操纵）/ `Coded`（编码）/ `Expert-rated`（专家评定）/ `Binary`（二分） | — |
| `conceptual_definition_en` | 概念性定义原文 | NA |
| `conceptual_definition_cn` | 概念性定义中文 | NA |
| `operationalization` | 一句话操作化概括 | NA |
| `composite` | 是否由多个指标合成：`Yes` / `No` | NA |
| `n_indicators` | 构成指标数量（二手数据潜变量） | NA |
| `composite_method` | 合成方式，如 `标准化后取均值` / `因子得分` / `加总` | NA |
| `measurement_model` | **只放 CFA / 测量模型拟合**，如 `CFA: CFI=.95, RMSEA=.08, SRMR=.08`；分类器性能放 `model_performance` | NA |
| `scale_type` | 量表性质：`Formative`（形成性）/ `Reflective`（反映性）/ `Single-item`（单题项） | NA |
| `coding_direction` | **高分代表什么**，如 `高分 = 更强调女性家庭职责 / 女性能动性越低` | NA |
| `n_items` | 量表题项总数（整数） | NA |
| `items_given` | **论文实际给出的题项条数**（整数）。论文只给样例题项时必填，且须在 `missing_fields` 记 `items` | NA |
| `items_text` | 题项原文（多条用全角竖线「｜」分隔，**不要用半角 `|`**，会把 Excel/Markdown 表格切坏） |
| `response_scale` | 响应量尺，如 `7-point Likert` | NA |
| `scale_anchors` | 锚点，如 `1 = Strongly disagree, 7 = Strongly agree` | NA |
| `reverse_coded` | `Yes` / `No` / `Partial` | NA |
| `reliability_type` | `Cronbach's α` / `CR` / `ω` / `κ` / `Krippendorff's α` / `test-retest` | NA |
| `reliability_value` | 数值，如 `.89`（用于 α/CR 之外的类型：ω、κ、Krippendorff's α、test-retest） | NA |
| `cr` | 复合信度 Composite reliability，如 `.895` | NA |
| `alpha` | Cronbach's α，如 `.893` | NA |
| `ave` | 平均方差抽取量 AVE / VEE，如 `.634` | NA |
| `avg_loading` | 平均题项载荷，如 `.790` | NA |
| `model_performance` | 计算测量中**该构念上**的模型指标，如 `accuracy 88.6%, AUC .846` | NA |
| `validation_agreement` | 与外部基准的一致性，如 `vs 人类多数 AUC .93、一致率 83%` | NA |
| `source_apa` | 完整 APA 出处 | NA |
| `adaptation` | `Adopted from` / `Adapted from` / `Self-developed` / `NA` | NA |
| `manipulation_conditions` | 操纵条件（实验法） | NA |
| `manipulation_materials` | 操纵材料描述 | NA |
| `procedure` | 流程步骤 | NA |
| `manipulation_check` | 操纵检验题项与结果 | NA |
| `data_source` | 二手数据的库/表/指标/年份 | NA |
| `coding_rule` | 编码/转换规则 | NA |
| `aggregation` | 聚合方式（取均值/加总/因子得分） | NA |
| `sample_n` | 该研究样本量 | NA |
| `notes` | 备注（如原文内部不一致说明） | NA |
| `missing_fields` | 该变量缺失字段列表（**无缺失时留空**，Excel 该列也留空，不写 NA） | 空 |

## 字段定义 · Variables（元分析专用）

元分析中「变量的操作化」是**编码规则 + 取值来源**，不是量表题项。`n_items` / `items_text` / `response_scale` / `scale_anchors` / `reverse_coded` 一律填 `NA`，改用下面三列：

| 字段名 | 说明 | 缺失填 |
|---|---|---|
| `coding_source` | 编码取值来源，**五选一**：`Coded from literature`（编码自原始文献）/ `Secondary index`（外部二手指标，如 Hofstede）/ `Survey-rated`（作者另做调查评定）/ `Expert-rated average`（专家评定取均值）/ `Automated text`（自动文本分析，如 LIWC） | NA |
| `coding_values` | 编码水平，如 `1 = utilitarian to 5 = hedonic` / `Local/national vs. international` / `Cents vs. percent vs. vague` | NA |
| `k_studies` | 该调节变量在多少项研究中出现（不足 5 项时作者通常不做合成） | NA |

其余字段的元分析填法：

- `role`：结果变量写 `Effect Size`；调节变量写 `Moderator`；方法学控制写 `Covariate`；概念支柱写 `Conceptual Pillar`
- `variable_type`：`Derived effect size` / `Coded from literature` / `Secondary index` / `Automated text` / `Survey-rated` / `Expert-rated average`
- `theme_level`：概念支柱写 `Conceptual pillar`，其下的调节变量写 `NA` 并把支柱名写进 `parent_theme`
- `reliability_type` / `reliability_value`：填**编码者间信度**（`Cohen's kappa` = .92、`ICC2(k)` = .99），不是 Cronbach's α
- `coding_direction`：高分代表什么；**反向编码必须标明**（如 Hofstede 原始 individualism 被反转成 1=个人主义 至 100=集体主义）

## 字段定义 · Variables（主题层级，质性论文用）

- `parent_theme`：上级主题/构念名，**必须与上级行的 `variable_name_en` 完全一致**（大小写敏感）。无上级写 `NA`。脚本会做断链检查
- `theme_level`：`Core construct` / `Marker` / `Aggregate dimension` / `Second-order theme` / `First-order concept` / `Code` / `NA`

质性论文的"变量"是主题树，靠这两列表达嵌套关系。量化论文这两列写 `NA`。

## 字段定义 · Items

`study_id`, `variable_name_en`, `item_no`, `item_en`, `item_cn`, `dimension`（多维量表的维度名）, `reverse_coded`, `response_scale`, `factor_loading`, `dimension_cr`, `dimension_ave`

后三个字段是**量表开发论文的核心信息**——这类论文常只报 CR/AVE/因子载荷而不报 Cronbach's α，若只填 `reliability_value` 会丢失 Table 3 级别的细节：

- `factor_loading`：该题项的标准化载荷。同一题项在多个研究中都报了时，写成 `.90 (S4) | .94 (S5) | .94 (S6) | .95 (S7)`
- `dimension_cr`：该维度在该研究中的组合信度，如 `Affective CR: .90 (S4) | .96 (S5)`
- `dimension_ave`：该维度在该研究中的平均方差抽取量，如 `.75 (S4) | .90 (S5)`

跨研究共用同一套题项时，`study_id` 写 `S4-S7 (共用)`，只在 Items 表里出现一次，不要按研究重复 4 遍。

## 字段定义 · Studies

`study_id`, `study_label`, `method_type`（`Experiment` / `Survey` / `Secondary Data` / `Qualitative` / `Mixed` / `Scale Development` / `Expert Judgment` / `Item Sorting` / **`Literature Review`** / `Simulation` / **`Computational Measurement`** / **`Analytical Model`**）, `n`, `n_unit`, `sample_source`（学生/Prolific/MTurk/数据库…）, `design`, `data_structure`, `time_span`, `level_1_unit`, `level_2_unit`, `n_observations`, `estimator`, `main_purpose`, `role_in_paper`, `key_finding`, `relation_to_other_studies`, `data_collection_period`, `preregistration`, `supplement_location`

后两组是新加的，面向纵贯与二手数据：

- `data_structure`：`Cross-sectional` / `Panel` / `Time-series` / `Nested` / `Cross-classified` / `Repeated cross-section`
- `level_1_unit` / `level_2_unit`：如 `州-年观测` / `州`
- `n_observations`：观测数（与 `n` 的聚类数区分开，如 `n=50 州，n_observations=500 州-年`）
- `estimator`：如 `MLM (Mplus 8.0, FIML)` / `Path analysis (Mplus 8.0)` / `Cross-classified model`
- **计算测量专用**（`method_type = Computational Measurement` 时必填，其余填 `NA`）：
  - `n_unit`：`n` 的单位——`图像` / `判断条数` / `品牌` / `受访者` / `论文`。**多方法论文里这四种语义常同时出现，必须逐行标明**
  - `train_n` / `val_n` / `holdout_n`：训练 / 验证 / 留出集的规模（整数）；比例写进 `model_spec`
  - `model_spec`：架构 + 基座 + 关键超参，如 `多标签 CNN，CaffeNet 微调，学习率 .0001`
  - `model_metrics`：汇总性能，如 `留出集准确率 90%，平均 AUC .85`
- **分析模型专用**（`method_type = Analytical Model` 时必填，其余填 `NA`）：
  - `model_setup`：主体、时序、竞争结构、消费者偏好与成本的一段话摘要
  - `key_assumptions`：**逐条**列关键假设，含作者自己承认的强假设（用 ` | ` 分隔）
  - `solution_concept`：均衡概念 + 求解方法 + 是否证明唯一性
  - `model_results`：命题 / 比较静态的摘要，逐条编号
- `design`：实验研究写设计类型（`Between-subjects` / `Double randomization` / `Moderation-of-process` / `Factorial` / `Blocking design`…）；非实验研究写分析设计（`Path analysis` / `Multilevel` / `Correlational`）；仿真研究写 `Simulation` / `Agent-based model`；二手数据用准实验识别时写 `Difference-in-differences` / `Instrumental variable` / `Regression discontinuity` / `Event study` / `Quasi-experiment`
- `design` **只放设计类型**。估计方法（OLS / FE / 2SLS / SEM / MLM）写进 `estimator` 列，不要塞进 design
- `preregistration`：预注册链接（如 `aspredicted.org/c6na5`），无则 `NA`
- `supplement_location`：在线补充材料位置（如 `SSRN abstract=3719543`），无则 `NA`

元分析专用（其余方法填 `NA`）：

- `search_databases`：检索数据库清单，用 ` | ` 分隔
- `search_terms`：检索词原文
- `additional_search`：数据库之外的补充检索（手工检索期刊、滚雪球、灰色文献来源）
- `inclusion_criteria`：纳入标准（含因变量类型、效应量信息要求）+ 排除篇数与原因
- `n_primary_papers` / `n_primary_studies` / `k_effect_sizes`：**三个数字不同，必须分别记**（如 159 / 237 / 205）
- `n`：累计参与者数（如 118,582）
- `effect_size_metric`：效应量指标（如 `Cohen's d`）与计算口径
- `effect_size_conversion`：转换与缺失数据处理（如从 M+SD+n 转换；33 项只报方向与显著性的研究用同方向同操纵组研究的平均 p 值插补）
- `coding_reliability`：编码者间信度，如 `Cohen's kappa = .92 (2 coders × 50 studies each)`
- `publication_bias_tests`：发表偏倚检验，如 `未发表文献占比 20%/18% | Rosenthal fail-safe N = 12,400 / 14,148 | contour-enhanced funnel plot：原始略不对称，meta-regression 残差图对称`
- `missing_data_handling`：缺失数据处理（同上可并入 `effect_size_conversion`）
- `software`：软件与估计方法，如 `metafor::rma.mv（层级随机效应，REML）`
- `data_structure`：写 `Effect sizes nested in studies`；`level_1_unit` = `effect size`，`level_2_unit` = `study`
- `design`：`Meta-analysis` / `Meta-regression` / `Subgroup analysis` / `Bivariate moderator synthesis`

## 字段定义 · EffectSizes

`study_id`, `analysis_id`, `comparison`, `outcome`, `model`, `k_studies`, `k_effect_sizes`, `total_n`, `effect_size_metric`, `effect_size_value`, `se`, `ci_low`, `ci_high`, `p_value`, `heterogeneity_i2`, `cles`, `fail_safe_n`, `note`

- `comparison`：**对比基准必填**——`CM vs. no-CM baseline` / `CM vs. philanthropy` / `CM vs. discount promotion` …
- `outcome`：结果变量，如 `Attitudinal` / `Behavioral` / `Overall`
- `model`：`Unconditional`（仅截距）/ `Full meta-regression`（同时控制所有调节变量）/ `Subgroup analysis`（单调节变量，遗漏变量偏差最大）/ `Bivariate moderator synthesis`（无对照组研究）/ `Sensitivity` / `Publication bias`
- `k_studies` / `k_effect_sizes`：**研究数与效应量数分开记**（如 40 研究 / 94 效应量）
- `heterogeneity_i2`：异质性，如 `87%`
- `cles`：common language effect size，如 `.627`（随机选一个受 CM 影响的消费者比未受影响者反应更有利的概率）
- `fail_safe_n`：如 `12,400（阈值 5k+10）`
- 显著性用 `†p < .10` / `*p < .05` / `**p < .01` / `***p < .001` 标记在 `p_value` 或 `note`

**同一效应量在不同 `model` 下数值与显著性会变，务必分行记录**，不要把全模型结果当成唯一结论。

民族志 / 质性研究专用：

- `sampling_strategy`：`Purposive` / `Theoretical` / `Snowball` / `Convenience` / `Maximum variation`；多种用 ` | ` 分隔
- `field_sites`：田野点清单，格式 `地点（类型；方式；规模）`，多个用 ` | ` 分隔，如 `Fairlawn（居住社区；家庭访谈+参与观察；4 户/9 人/110 小时） | Smith Motors（品牌经销商；非参与观察；5 次到访/25 小时）`
- `researcher_positionality`：研究者在场方式与身份，如 `第一作者非参与观察；第二作者本人为社群成员（emic + etic 双视角）`
- `data_volume`：**与 `n` 分开**。`n` 填人数，`data_volume` 填数据量，如 `访谈与观察 110 小时` / `300+ 页网页数据`。民族志常只报小时数或页数，混填会让人误以为有 110 个受访者
- `mermaid_node`：**脚本自动填充**，无需手写。该研究对应的 Mermaid 节点定义（如 `S1["S1 · 建立主效应<br/>n=140 · 二手数据"]`），需要手工拼图时直接从这一列复制

### 顶层可选键：控制研究地图

```json
{
  "paper": {...},
  "studies": [...],
  "mermaid_groups": {"① 条目生成": ["S1A","S1B","S1C"], "② 条目筛选": ["S2","S3"]},
  "mermaid_edges": ["S1A --> S1B", "S2 --> S3 --> S4", "S6pre -.-> S6"]
}
```

- `mermaid_groups`：按阶段分组（量表开发、多方法论文必用）；不提供且节点 > 9 时脚本按 `method_type` 自动分组
- `mermaid_edges`：边的推进顺序。**不提供时脚本按 studies 顺序串联**，会把 pretest 节点排进主链条，务必用此键校正
- 未列入 `mermaid_groups` 的节点（如 pretest）脚本会自动补出，不会丢

## 字段定义 · Indicators（二手数据专用）

`study_id`, `variable_name_en`, `indicator_no`, `indicator_name_en`, `indicator_name_cn`, `data_source_detail`, `unit`, `coding_direction`, `standardized`, `coverage`, `factor_loading`, `notes`

- `data_source_detail`：**精确到可复现**，如 `Human Development Report (2014), 每名女性平均生育数`；禁止只写「世界银行」
- `coding_direction`：`正向` / `反向计分（高分 = 更严格）`；反向的一律标明
- `coverage`：覆盖度与年份，如 `140 国, 2014`
- `standardized`：`Yes` / `No`
- 只有当变量 `composite = Yes` 时才需要这个 sheet 的行；单一指标变量不必重复录入

## 字段定义 · Hypotheses

`study_id`, `hypothesis_id`（`H1`、`H2a`…；未编号用 `Predicted-1`）, `hypothesis_en`, `hypothesis_cn`, `iv`, `dv`, `mediator`, `moderator`, **`test_type`**, `test_method`（ANOVA / regression / PROCESS / chi-square…）, `statistic`（如 `F(2,222)=5.97`）, `p_value`, `effect_size`（如 `d = .46`、`η² = .051`）, `direction`, `supported`（`Supported` / `Partially supported` / `Not supported` / `Reversed` / `NA`）, `note`

`test_type` 区分同一条假设在不同角色下被检验：

- `Primary`：主检验（该研究的核心假设检验）
- `Replication`：复制（同一假设在另一个样本/情境中再验一次，如 H1 在全球样本与美国样本各验一次）
- `Robustness`：稳健性检验（加控制变量、换指标后重验）
- `Supplemental`：补充分析
- `Manipulation check`：操纵检验

**一条假设在多个研究中被检验时，每个研究各一行**（如 H1 在 Study 1 与 Study 2a 各一行），便于看效应是否跨样本复现。

## 字段定义 · Stimuli

`study_id`, `stimulus_set`（该材料所属集合，如「暴露操纵-品牌条件」）, `stimulus_type`（`Text` / `Vignette` / `Image` / `Logo` / `Video` / `Environment` / `Product` / `Scenario` / `Task`）, `content_en`（原文内容，vignette 摘录关键段落）, `content_cn`, `quantity`（数量，如 14 / 30）, `presentation_mode`（`Simultaneous` / `Sequential`）, `duration`（呈现时长或试次数）, `pretest`（预测试情况）, `source`（材料出处：作者自制 / 改编自… / 真实素材）

## 生成方式

1. 把提取结果整理成 JSON 文件，结构：

```json
{
  "paper": {"title": "...", "authors": "...", "year": 2021, "journal": "...", "doi": "..."},
  "studies": [ {...} ],
  "variables": [ {...} ],
  "items": [ {...} ],
  "indicators": [ {...} ],
  "hypotheses": [ {...} ],
  "stimuli": [ {...} ],
  "effectsizes": [ {...} ]    // 仅元分析；也可写成 effect_sizes
}
```

`items`、`indicators`、`effectsizes` 可以只填与本论文方法相关的那个，脚本会输出空表而不是报错。

2. 运行脚本（字段缺失填 `NA` 或留空，脚本会补全列）：

```bash
python3 scripts/export_codebook.py input.json "变量操作化提取_XXX.xlsx"
# 脚本路径相对于技能根目录；输出路径由用户指定（Windows 上命令可能是 python 或 py）
```

3. 脚本行为：按上述字段顺序生成 7 个 sheet，冻结首行、自动列宽、表头加粗加底色；JSON 中未出现的字段自动补空列，保证跨论文列名一致。

## 元分析论文的特殊处理

元分析（title 含 meta-analysis / meta-analytic review / a meta-analysis of）的提取单元是**效应量与调节变量编码**，不是被试层面的变量。容易在四处失真：

1. **不要当成文献综述**。综述提炼构念与命题；元分析产出可量化效应量，必须有 `EffectSizes` 表。判定线索：Cohen's d、I²、fail-safe N、funnel plot、k effect sizes。
2. **三个数字分开记**：`n_primary_papers`（159）/ `n_primary_studies`（237）/ `k_effect_sizes`（205）/ `n`（118,582 累计参与者）。只写一个会让人误判证据基础。
3. **每个效应量标 `comparison` 与 `model`**。元分析常同时报「CM vs. 无对照基线」「CM vs. 慈善」「CM vs. 折扣」「CM vs. 倡导广告」等多组对比，且同一效应量在全模型 / 亚组 / 双变量合成下数值与显著性不同。不标清楚，跨论文合并效应量时一定会张冠李戴。
4. **调节变量的「操作化」是编码规则与取值来源**，不要去找题项和 α。`coding_source` 必须区分五类（文献编码 / 外部二手指标 / 作者另做调查 / 专家评定 / 自动文本分析——如 LIWC 情感分析），`coding_values` 写编码水平，反向编码写进 `coding_direction`。
5. **有对照组与无对照组两类子样本要分开**。无 no-CM 对照组的研究无法估计主效应，其「调节效应」实际混入了主效应（如品牌强度在两类研究中方向相反），并列呈现而不是替作者挑一个。
6. **假设表填理论预期**：元分析常无 H1/H2，只有 Table 1 那类「CM 效应在…时更高」的方向性预期。用 `Predicted-N` 记录，`test_type` 写 `Primary`，结果按态度/行为两类分别判定。

## 量表开发论文的特殊处理

量表开发论文（title 含 scale development / conceptualization and measurement / a X-item scale）与假设检验论文结构不同，容易漏掉关键环节。遇到时必须：

1. **按开发阶段建 Studies 行**，不要只建"主研究"：条目生成（质性）→ 条目筛选（专家 / 消费者分类）→ 纯化与初始验证（EFA/CFA）→ 已知群组效度 → 跨情境不变性 → 法则网络验证。每个阶段即使只是"筛条目"也要单独一行，`method_type` 用 `Qualitative` / `Expert Judgment` / `Item Sorting`。
2. **条目池的每一步数量变化**写进 `key_finding`（如 `104 → 102 → 72 → 33 → 18`），并写明每一步的剔除标准（题总相关、因子载荷、修正指数、实质效度系数）。这是复用量表的关键信息。
3. **信度字段优先 CR / AVE**：这类论文常不报 Cronbach's α。`reliability_type` 写 `CR`，`missing_fields` 注明 `cronbach_alpha`，**不要**因为没 α 就留空或去别处猜一个。
4. **核心变量 role 用 `Target Construct`**（它不是 IV 也不是 DV，而是被开发与验证的对象）；只有当它在某个研究里充当中介/后果时才改填 `Mediator` / `DV`。
5. **把构念的维度定义与边界也当变量提取**：量表论文的"维度"就是构念的操作化骨架，每个维度一行或至少在 Items 表用 `dimension` 列区分。
6. **假设表填效度检验预期**，编号用 `Predicted-N` 并注明「原文未编号」。量表论文的"假设"通常是"模型应为六因子""应满足测量不变性""应区分效价"这类预期，不是 H1/H2。
7. **应用示范也要记**：量表论文常在末尾示范如何用（如痛点分析、画像分析），若涉及具体统计结果，写进对应研究的 `key_finding`。

## 二手数据 + 潜变量建模论文的特殊处理

跨国 / 跨州档案研究（如「宗教性与性别工资差距」这类）与问卷论文的编码难点不同，容易在两处失真：

1. **不要把合成变量拆成 N 个独立变量**。一个构念由 4 个档案指标合成时，Variables 表只占**一行**（`composite = Yes`、`n_indicators = 4`、`composite_method = 标准化后取均值`、`measurement_model = CFA: CFI=.95…`），4 个指标进 `Indicators` 表。若拆成 4 行，元分析编码会把一个构念当成四个变量。
2. **`coding_direction` 必须填**。档案指标的反向计分（如「允许堕胎的理由数」反向后高分=更严格）如果漏记，符号解释会整个反过来。这是二手数据最常出错的地方。
3. **观测数 ≠ 样本数**。纵贯研究写 `n = 50 州`，`n_observations = 500 州-年`。只写 500 会让人误以为有 500 个独立个体。
4. **补充变量也要录**。描述统计表里标为 supplementary 的变量（Hofstede 文化维度、政体指数等）只在稳健性分析中出现，但它们是理解主效应稳健性的关键，role 填 `Covariate`，`sample_n` 填实际可用的较小 n。
5. **同一构念在不同研究换了指标时**，Variables 表按「变量 × 研究」拆行，`operationalization` 各写各的，并在报告的跨研究对照表里并列。

## 编码一致性规则

- 缺失值统一用 **`NA`**，不要留空、不要写「无」「未提供」
- 数值型信度统一写成 `.89`（带前导点，与 APA 一致）
- 多值字段（如多个条件）用 ` | ` 分隔
- 变量名在同一篇论文内必须**完全一致**（含大小写），否则跨研究合并会断链
- 一条变量若在多个研究出现，**Variables 表按「变量 × 研究」拆行**（不是每行一个变量），便于看各研究 α 差异
