---
name: stats-results-writer
description: >
  将统计分析输出结果转化为规范的学术论文Results section写作，支持中文和英文两种模式。
  适用于商科MS/PhD学生及教师，覆盖AMOS、SmartPLS、JASP、R、Python等主流软件的输出解读，
  以及方差分析、t检验、回归分析、结构方程模型（CB-SEM/PLS-SEM）、中介效应、调节效应、
  有调节的中介效应（Moderated Mediation）等分析方法。

  触发场景（满足以下任一条件即应使用本skill）：
  - 用户粘贴或上传统计软件的输出结果（表格、截图、数字）
  - 用户提到"帮我写Results"、"帮我解读结果"、"这个结果怎么写"
  - 用户提到具体统计指标：β、p值、R²、CFI、RMSEA、AVE、CR、VIF、F值、t值等
  - 用户提到分析方法：SEM、PLS、回归、方差分析、t检验、中介、调节、Hayes PROCESS
  - 用户提到软件名称：AMOS、SmartPLS、JASP、R、Python、SPSS、Mplus
  - 用户说"我的假设支持了吗"、"这个路径显著吗"、"怎么报告这个结果"
  - 用户上传论文草稿要求改进Results部分的写作质量

  即使用户只是把一堆数字粘贴过来说"帮我看看"，也应触发本skill。
version: 1.1.0
license: CC-BY-4.0
---

# 统计结果解读与撰写助手

## 核心理念

**AI解读数字、撰写文字；研究者确认判断、核实数据。**

> ⚠️ **重要提醒**：AI根据用户提供的数字进行解读和写作。如数字有误，结论亦会有误。请始终以原始软件输出为准，核实粘贴的数据无误后再使用生成的文字。

---

## 快速入口：选择你的分析类型

根据用户描述（或粘贴的输出内容）判断分析类型，直接跳转对应参考文件：

| 分析类型 | 参考文件 |
|---------|---------|
| **测量模型** — 信度、效度、CFA、共同方法偏差 | `references/01-measurement.md` |
| **方差分析 / t检验** — ANOVA、独立样本t、配对t | `references/02-anova-ttest.md` |
| **回归分析** — OLS、层次回归、Logistic | `references/03-regression.md` |
| **中介效应** — Baron & Kenny、Bootstrap、PROCESS | `references/04-mediation.md` |
| **调节效应** — 交互项、简单斜率、Johnson-Neyman | `references/05-moderation.md` |
| **有调节的中介** — Moderated Mediation、PROCESS Model 7/14/58 | `references/06-moderated-mediation.md` |
| **CB-SEM** — AMOS / Mplus / lavaan，整体模型拟合与路径 | `references/07-cb-sem.md` |
| **PLS-SEM** — SmartPLS，测量模型+结构模型+Bootstrap | `references/08-pls-sem.md` |

**如果用户的分析涉及多个类型**（如：先做CFA，再做SEM），按照论文Results section的逻辑顺序依次处理：测量模型 → 结构模型 → 假设检验。

---

## 工作流程（每次任务必须遵循）

### 第一步：信息收集

收到请求后，先确认以下信息（从上下文推断，缺失时询问）：

| 信息项 | 说明 | 若未提供 |
|--------|------|---------|
| **使用的软件** | AMOS / SmartPLS / JASP / R / Python / SPSS | 从输出格式推断 |
| **分析方法** | 见上表 | 从数字特征推断 |
| **写作语言** | 中文 / 英文 | 默认英文（期刊）；学位论文询问 |
| **汇报格式** | APA 7th / 期刊自定义 | 默认APA 7th |
| **假设列表** | H1: X→Y 正向影响…… | 有假设时必须提供，用于判断是否支持 |
| **样本量** | N = ? | 计算效应量和自由度时需要 |

### 第二步：读取对应参考文件

根据分析类型，使用 `Read` 工具读取对应的 `references/0X-xxx.md` 文件，获取：
- 该方法的**报告标准**（哪些指标必须报告）
- **判断阈值**（显著性标准、拟合指标cut-off等）
- **写作模板**（中英文句式）

### 第三步：逐项解读

按以下结构输出解读：

```
📊 数据解读
├── [指标名]: [数值] → [判断: 显著/不显著 / 达标/未达标]
├── [指标名]: [数值] → [判断]
└── ...

✅ 假设检验结论（如用户提供了假设）
├── H1: [方向] [显著性] → 支持 / 不支持
└── ...

⚠️ 需注意（如有问题）
└── [如：VIF > 10，存在多重共线性风险]
```

### 第四步：生成学术写作文本

根据解读结果，生成可直接用于论文的段落。写作规范：
- **精确**：数值保留小数位与原始输出一致（通常2-3位）
- **完整**：包含所有APA要求报告的统计量
- **判断明确**：每个假设明确写出"supported"/"not supported"或"显著"/"不显著"
- **不过度解读**：不对不显著结果做"边缘显著"等模糊表述
- **括号格式**：统计量用括号报告，如 (β = .32, SE = .08, p < .001)

### 第五步（可选）：输出为Word文档

如用户需要，用所在环境提供的文档生成能力（如 `python-docx` 库或 `pandoc` 转换；若环境中已有专门的 docx 技能，优先使用它）输出规范格式的 `.docx` 文件，包含：
- 文字结果段落
- APA格式统计表格
- 假设检验汇总表

---

## 软件输出识别指南

快速识别用户粘贴的是哪个软件的输出：

| 软件 | 典型标志 |
|------|---------|
| **AMOS** | "Regression Weights"、"Standardized RW"、"Model Fit"、χ²/df |
| **SmartPLS** | "Outer Loadings"、"Path Coefficients"、"Bootstrapping Results"、"HTMT" |
| **JASP** | 整洁表格、"BF₁₀"（贝叶斯因子）、"η²"、荷兰语界面残留 |
| **R (lavaan)** | "lavaan"、"Estimate Std.Err z-value"、"CFI"、"SRMR" |
| **R (lm/lme4)** | "Coefficients:"、"Residual standard error"、"Multiple R-squared" |
| **R (mediation/PROCESS)** | "ACME"、"ADE"、"Indirect Effect"、"Boot CI" |
| **Python (statsmodels)** | "OLS Regression Results"、"coef std err t P>\|t\|" |
| **Python (semopy/pingouin)** | 类似R格式，含"GFI"或"pingouin" |
| **SPSS** | "Unstandardized B"、"Standardized Beta"、"Sig."列 |

---

## 常见判断阈值快速参考

### 显著性标准
- p < .05 → 显著（*）
- p < .01 → 高度显著（**）
- p < .001 → 极显著（***）
- p ≥ .05 → 不显著（ns）

> ⚠️ **不要使用"边缘显著"（marginally significant）**：p = .06/.07等应直接报告为不显著，可在Discussion中说明趋势。

### SEM拟合指标（CB-SEM）
| 指标 | 良好标准 | 可接受标准 |
|------|---------|----------|
| χ²/df | < 2 | < 3 |
| CFI | ≥ .95 | ≥ .90 |
| TLI | ≥ .95 | ≥ .90 |
| RMSEA | < .05 | < .08 |
| SRMR | < .05 | < .08 |

### PLS-SEM测量模型
| 指标 | 标准 |
|------|------|
| 外部载荷 (Outer Loading) | ≥ .70 |
| AVE | ≥ .50 |
| CR (Composite Reliability) | ≥ .70 |
| HTMT（判别效度） | < .85（严格）或 < .90（宽松） |

### 回归/路径分析
| 指标 | 关注点 |
|------|-------|
| VIF | < 5（理想）；< 10（可接受）；≥ 10 需警惕多重共线性 |
| R² | 报告值，结合领域惯例解释（社科 .10-.30 属中等） |
| f² (效应量) | .02=小；.15=中；.35=大 |

---

## 参考文件索引

详细写作模板和判断标准见各参考文件：

- `references/01-measurement.md` — 信度效度、CFA、CMB
- `references/02-anova-ttest.md` — ANOVA、t检验
- `references/03-regression.md` — OLS回归、层次回归、Logistic
- `references/04-mediation.md` — 中介效应（Baron & Kenny / Bootstrap）
- `references/05-moderation.md` — 调节效应、简单斜率分析
- `references/06-moderated-mediation.md` — 有调节的中介效应
- `references/07-cb-sem.md` — CB-SEM（AMOS/Mplus/lavaan）
- `references/08-pls-sem.md` — PLS-SEM（SmartPLS）

---

## 重要原则

1. **数字原封不动**：写作文本中的所有数字必须来自用户提供的输出，不得自行估算或修改
2. **判断有据可依**：每个"显著/不显著"、"支持/不支持"的判断都基于明确阈值，不模糊表达
3. **缺失信息提示**：若用户提供的数字不足以完整报告（如缺少SE或置信区间），明确告知需要补充哪些数据
4. **分段清晰**：生成的Results段落按"测量模型→结构模型→假设检验"或"描述统计→假设检验"的逻辑组织
5. **学位论文 vs 期刊**：学位论文可更详尽；期刊投稿应简洁，将详细表格放入正文，文字简述

## 交接：从哪来、到哪去

| 方向 | 技能 | 交接什么 |
|---|---|---|
| 上游 | `quant-data-analysis` | 方差分析、回归、t 检验的软件输出 |
| 上游 | `sem-analysis-tutor` | 测量模型与结构模型的系数、拟合指标、中介与调节的检验结果 |
| 下游 | `paper-figures-tables` | 同一批数字做成表与图：结果段落里报的数，表里也得对得上 |
| 下游 | `discussion-conclusion-writer` | Results 写完，接着讲这些结果意味着什么 |
| 下游 | `academic-citation-auditor` | 定稿前核对：正文引用的每个数字都能在表里找到 |

**单独使用**：粘贴软件输出（AMOS、SmartPLS、JASP、R、Python 的表格或截图）就能写，
不要求上游按什么格式交付。数字的准确性由你保证——本技能照你给的数写。
