# 分支 F · 元分析 / Meta-Analysis

适用于对**已发表研究做效应量合成**的文章：报告效应量（Cohen's d / Hedges' g / r / Fisher's z / OR / 回归系数）、meta-regression、异质性 I²、发表偏倚检验、森林图/漏斗图、纳入文献数与效应量数。

**元分析不是文献综述。** 综述提炼构念与命题，元分析产出**可量化的效应量估计**——两者的提取单元完全不同。判定线索：出现 "effect size"、"Cohen's d"、"meta-regression"、"fail-safe N"、"funnel plot"、"k effect sizes"、"I²"。综述型理论构建走 `qualitative.md` §7，不要混用。

---

## 0. 元分析的「变量」是什么（与实证研究根本不同）

**分析单元是效应量，不是被试。** 变量表要按四层录入：

| 层 | `role` 取值 | 说明 | 本文例子 |
|---|---|---|---|
| 结果/效应量 | `Effect Size` | 被解释对象，相当于 DV | Attitudinal response (d)、Behavioral response (d) |
| 调节变量 | `Moderator` | 研究层面的编码特征 | 15 个 CM 调节变量 |
| 方法学控制 | `Covariate` / `Control` | 与理论无关但需控制 | 学生样本、发表年份、发表状态、期刊等级 |
| 概念支柱 | `Conceptual Pillar` | 调节变量的更高阶聚合（写入 `parent_theme`） | 透明度 / 真诚信号 / 情感依附 / 购买情境 |

**关键差异：元分析中「变量的操作化」= 「编码规则 + 取值来源」，不是量表题项。**
`response_scale`、`n_items`、`reliability_value` 这类字段一律填 `NA`；改用：

- `coding_rule`：编码规则原文（如「Known NPO disclosed vs. other [ref. = no NPO]」）
- `coding_values`：编码水平（如「1 = utilitarian to 5 = hedonic」）
- `coding_source`：取值从哪来（见 §5，**必须区分五类**）
- `reliability_type` / `reliability_value`：填**编码者间信度**（Cohen's κ、Krippendorff's α、ICC2(k)），不是 Cronbach's α

---

## 1. 检索与纳入（Studies 表）

元分析的「样本」是文献，不是人。必填：

| 字段 | 内容 |
|---|---|
| `search_databases` | 数据库清单（如 ABI/INFORM、Business Source Complete、ECONIS、Emerald、Google Scholar、JSTOR、ScienceDirect、SpringerLink） |
| `search_terms` | 检索词原文，逐条列出（常是一长串关键词） |
| `additional_search` | 数据库之外的补充检索：手工检索指定期刊、滚雪球（参考文献）、灰色文献（working paper 库、学位论文库、会议论文集） |
| `inclusion_criteria` | 纳入标准（含因变量类型、操纵成功、效应量信息充分） |
| `n_primary_papers` / `n_primary_studies` / `k_effect_sizes` | **三个数字不同，必须分别记**（如 159 papers / 237 studies / 205 effect sizes） |
| `n` | 累计参与者数（如 118,582） |
| `data_collection_period` | 文献覆盖时间跨度（如 1992-01 至 2021-12）+ 文献检索截止日 |
| `time_span` | 同上可简写 |

**排除记录**：报告排除篇数与原因（如「33 项研究报告信息不足被排除」）、是否纳入未发表文献及占比、样本构成（期刊论文 / 学位论文 / 会议 / 工作论文各多少）。这些直接关涉发表偏倚判断。

---

## 2. 效应量（EffectSizes 表）

一行 = 一个「对比基准 × 结果变量 × 模型」的效应量。必填：

`study_id`、`analysis_id`、`comparison`、`outcome`、`model`、`k_studies`、`k_effect_sizes`、`total_n`、`effect_size_metric`、`effect_size_value`、`se`、`ci_low`、`ci_high`、`p_value`、`heterogeneity_i2`、`cles`、`fail_safe_n`、`note`

**`comparison`（对比基准）必须写清**——元分析常同时报好几组对比，混在一起会彻底误读：

> CM vs. no-CM baseline ／ CM vs. philanthropy ／ CM vs. advocacy advertising ／ CM vs. sales-linked product donations ／ CM vs. discount promotion

**`model`（模型类型）必填**，同一效应量在不同模型下数值与显著性会变：

- `Unconditional`（无条件模型，仅截距）
- `Full meta-regression`（同时控制所有调节变量）
- `Subgroup analysis`（每次只放一个调节变量，遗漏变量偏差最大）
- `Bivariate moderator synthesis`（无对照组研究的操纵对比双变量合成）
- `Sensitivity` / `Publication bias`

还要记：效应量**计算口径**（均值差 / 合并组内 SD）、**转换来源**（从 M+SD+n 还是 p+n 转换）、**方向约定**（正值代表什么，如正值 = CM 有利）、**CLES 换算**、**缺失数据处理**（如 33 项研究只报方向与显著性时如何插补）。

---

## 3. 异质性与模型设定

- **I² 及判读阈值**：<25% 低、25–75% 中、>75% 高（Higgins & Thompson 2002）；τ²、Q 检验一并记录
- **数据结构**：效应量嵌套于研究 → `data_structure = Effect sizes nested in studies`；`level_1_unit` / `level_2_unit` 分别写 effect size / study
- **估计方法**：层级随机效应（hierarchical / three-level）、REML、`rma.mv`（metafor）、稳健方差估计（RVE）
- **模型拟合**：预测值-观测值相关平方 R²、VIF（多重共线性诊断）
- **异常值与影响诊断**：标准化残差、Cook's 距离、剔除后的敏感性分析结果

---

## 4. 发表偏倚（元分析必检，最容易漏）

逐项记录作者用了哪些、结论如何：

| 方法 | 记录内容 |
|---|---|
| 未发表文献纳入 | 数量与占比（如态度类 20%、行为类 18% 的效应量来自未发表研究） |
| Fail-safe N | 数值 + 参照阈值（Rosenthal 5k+10）+ 结论 |
| 漏斗图 | 是否对称、是否 contour-enhanced、残余漏斗图（meta-regression 后） |
| 回归法 | Egger's regression / Begg's rank |
| 其他 | trim-and-fill、p-curve、selection model、PET-PEESE |

---

## 5. 编码方案与编码信度（Variables 表）

- **编码手册**：是否提供（常在 Web Appendix Table W3 / W4）
- **编码者间信度**：指标 + 数值 + 判读标准（如 Cohen's κ = .92，>.80 视为可靠）
- **独立编码比例与分歧解决**（如两人各独立编码 50 项，讨论解决分歧后单人完成其余）
- **`coding_source` 必须区分五类**——这是元分析最容易含糊的地方，写「编码自文献」会丢掉关键差异：

| 取值 | 含义 | 本文例子 |
|---|---|---|
| `Coded from literature` | 直接从原始研究报告中读取 | NPO 是否披露、捐赠额框架 |
| `Secondary index` | 取自外部二手指标 | 文化情境（Hofstede individualism，**反向编码**为 1=个人主义 至 100=集体主义） |
| `Survey-rated` | 作者另做调查让被试评定 | 享乐 vs 实用产品类型（348 名 panel 被试，5 点量表，ICC2(k) = .99） |
| `Expert-rated average` | 专家评定后取均值 | 品牌–NPO 契合度（5 位专家，89 组联盟，ICC2(k) = .95） |
| `Automated text` | 自动文本分析 | 捐赠诉求情感倾向（LIWC，正向词占比减负向词占比） |

- **反向编码**要在 `coding_direction` 标明（如 Hofstede 原始编码被反转以匹配理论预期）
- **`k_studies`**：该调节变量在多少项研究中出现；不足 5 项时作者通常不做合成，要注明

---

## 6. 调节变量结果的三种口径

**全模型、亚组分析、双变量合成三者数值不同、结论可能相反，必须分开记录。**

典型分歧（本文实证）：
- **品牌强度**：纯调节研究显示强品牌态度更高（反映了品牌强度的主效应），而有 no-CM 对照组的研究显示**相反**——CM 对弱势品牌更有效。原因是前者把主效应误当调节效应。
- **捐赠金额**：有对照组的研究发现显著正向效应，纯调节研究无效应（操纵水平差异太大）。

因此每条调节变量结论必须标注**来源模型**，并在报告里提示读者：无 no-CM 对照组的研究无法估计 CM 主效应，其调节效应不可与主效应调节混为一谈。

两种系数都要记：**非标准化 `b`**（实际意义）与**标准化 `β`**（相对重要性）。态度与行为两类结果分别给。

---

## 7. 常见遗漏点（务必检查）

- **Web Appendix**：编码手册全文（Table W3）、编码汇总（W4）、纳入文献清单（W2）、逐研究效应量明细（W6）、相关矩阵（W9.1/W9.2）、敏感性分析（W8.1/W8.2）。**元分析的题项级信息基本都在附录**，正文只有结果表。
- **论文数 / 研究数 / 效应量数**三个数字（159 / 237 / 205）不要只记一个
- **有对照组 vs 无对照组的子样本**分别报了多少（51 papers / 67 studies 有 no-CM 对照）
- **功效分析**：达到 80% 检验力所需每组样本量（用 G*Power 算出的 60 / 156）
- **模拟/预测应用**：作者用模型系数对具体案例做的预测值（如 Yoplait d = .952 / .675 vs. KFC d = −.254 / −.263）
- **概念支柱的效应量分解**（Figure 2 这类 min–max 分解）
- 未能检验的心理机制（如 warm glow、skepticism 无法从编码文献中观测）——作者通常在局限里明说

---

## 8. 输出示例

### 效应量主表

| 对比基准 | 结果变量 | k (研究/效应量) | 总 N | d | CLES | I² | Fail-safe N |
|---|---|---|---|---|---|---|---|
| CM vs. no-CM | 态度 | 40 / 94 | NA | .458*** | .627 | 87% | 12,400 |
| CM vs. no-CM | 行为 | 50 / 111 | NA | .283*** | .579 | 87% | 14,148 |

（模型 = Unconditional；†p<.10 \*p<.05 \*\*p<.01 \*\*\*p<.001）

### 调节变量条目

**Variable / 变量**: Why Framing of Donation Appeal / 捐赠诉求「为什么」框架
**Role / 角色**: Moderator
**Parent theme / 所属支柱**: 情感依附 / Emotional Attachment
**概念性定义**: 说明捐赠的共同目的（shared purpose），而非捐赠款项如何被使用
**Coding rule / 编码规则**: 「Shared purpose specified vs. not」——是否阐明捐赠的共同目的
**Coding source / 取值来源**: Coded from literature（编码自原始文献）
**Result / 结果**:
- 全模型：态度 b = .429, β = .177, p < .001；行为 b = .126, β = .060, p < .05
- 组间差异 Δb = .303, p < .01（对态度的影响显著大于对行为的影响）
- 亚组分析：态度 b = .192（n.s.）、行为 b = .043（n.s.）——**未纳入全模型控制时不显著**
**Supported / 是否支持**: Supported（预期方向）
