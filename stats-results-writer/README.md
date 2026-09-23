# stats-results-writer

> 统计结果解读与撰写助手 —— 把软件输出变成规范的 APA 报告段落。

**版本**：1.0.0 ｜ **适用**：商科 MS/PhD 学生及教师 ｜ **规模**：SKILL.md + 8 个 references

---

## 它解决什么问题

跑完分析只是完成了一半。把输出写成论文能直接用的 Results 段落，是另一件需要训练的事：

- 哪些指标**必须**报告，哪些可以省略？
- 拟合指标怎么措辞？χ² 显著但 CFI 很好该怎么写？
- 中介效应报告要不要写间接效应的置信区间？Bootstrap 多少次？
- 多重共线性怎么交代？效应量要不要报？
- 中文期刊和英文期刊的句式差别在哪？

这个技能把每个方法的**报告标准 + 判断阈值 + 中英文写作模板**整理成 8 册分方法参考。

---

## 核心理念

**AI 解读数字、撰写文字；研究者确认判断、核实数据。**

> ⚠️ **重要提醒**：AI 根据用户提供的数字进行解读和写作。
> 如数字有误，结论亦会有误。请始终以原始软件输出为准，
> 核实粘贴的数据无误后再使用生成的文字。

---

## 覆盖范围

### 8 册分方法参考

| 参考文件 | 覆盖内容 |
|---|---|
| `references/01-measurement.md` | 信度、效度、CFA、共同方法偏差（CMB） |
| `references/02-anova-ttest.md` | ANOVA、独立样本 t、配对 t（22 个代码块，本册最厚） |
| `references/03-regression.md` | OLS、层次回归、Logistic |
| `references/04-mediation.md` | 中介效应（Baron & Kenny / Bootstrap / PROCESS） |
| `references/05-moderation.md` | 调节效应、简单斜率、Johnson-Neyman |
| `references/06-moderated-mediation.md` | 有调节的中介（PROCESS Model 7/14/58） |
| `references/07-cb-sem.md` | CB-SEM（AMOS / Mplus / lavaan）整体拟合与路径 |
| `references/08-pls-sem.md` | PLS-SEM（SmartPLS）测量模型 + 结构模型 + Bootstrap |

### 软件输出识别

技能内置了一份「软件输出识别指南」，能根据你粘贴的内容自动判断来源，
无需你说明用的是哪个软件：

| 软件 | 典型标志 |
|---|---|
| AMOS | `Regression Weights`、`Standardized RW`、`Model Fit`、χ²/df |
| SmartPLS | `Outer Loadings`、`Path Coefficients`、`Bootstrapping Results`、`HTMT` |
| JASP | 整洁表格、`BF₁₀`（贝叶斯因子）、`η²`、荷兰语界面残留 |
| R (lavaan) | `lavaan`、`Estimate Std.Err z-value`、`CFI`、`SRMR` |
| R (lm/lme4) | `Coefficients:`、`Residual standard error`、`Multiple R-squared` |
| R (mediation/PROCESS) | `ACME`、`ADE`、`Indirect Effect`、`Boot CI` |
| Python (statsmodels) | `OLS Regression Results`、`coef std err t P>\|t\|` |
| SPSS | `Unstandardized B`、`Standardized Beta`、`Sig.` 列 |

---

## 工作流程（五步）

| 步骤 | 内容 |
|---|---|
| 1. 信息收集 | 确认软件、分析方法、写作语言、汇报格式、假设列表、样本量 |
| 2. 读取对应参考文件 | 获取该方法的报告标准、判断阈值、写作模板 |
| 3. 逐项解读 | 按「指标 → 数值 → 判断」结构输出，标注假设检验结论与风险提示 |
| 4. 生成学术写作文本 | 数值精确、完整、判断明确、不过度解读、括号格式规范 |
| 5. （可选）输出 Word | 生成含文字段落、APA 统计表格、假设检验汇总表的 `.docx` |

---

## 一个值得单独说的部分：`07-cb-sem.md`

这一册能代表整体水准。它把 AMOS / lavaan / Mplus 三个软件的输出字段
**逐一映射**到 APA 报告句式，并给出：

- 必须报告的拟合指标表（含报告格式，如 `RMSEA = .XXX [.XXX, .XXX]`）
- CB-SEM vs PLS-SEM 选择对照（理论基础、样本量、分布假设、适用期刊）
- 测量不变性的三步检验与判据（ΔCFI ≤ .010 且 ΔRMSEA ≤ .015，Cheung & Rensvold, 2002）
- **「χ² 显著但其他指标良好」的标准写法**——附 Bentler & Bonett (1980) 的引用
- 修正指数的使用边界：**每次只添加一个，且需有实质性理由**
- 竞争模型比较的写作模板（Δχ²、ΔCFI）

这类「把软件输出翻译成规范报告」的操作性知识，平时散落在论坛与师兄师姐的经验里，
很少有整理成册的。

---

## 关键阈值速查（技能内置）

**显著性**：p < .05 显著（*）／ p < .01 高度显著（**）／ p < .001 极显著（***）／
p ≥ .05 不显著（ns）

> ⚠️ **不要使用「边缘显著」**：p = .06 / .07 等应直接报告为不显著，
> 可在 Discussion 中说明趋势。

**CB-SEM 拟合**：χ²/df < 2 良好、< 3 可接受；CFI/TLI ≥ .95 良好、≥ .90 可接受；
RMSEA < .05 良好、< .08 可接受；SRMR 同 RMSEA

**PLS-SEM 测量模型**：外部载荷 ≥ .70；AVE ≥ .50；CR ≥ .70；HTMT < .85（严格）/ < .90（宽松）

**回归**：VIF < 5 理想、< 10 可接受、≥ 10 需警惕；f² 效应量 .02 小 / .15 中 / .35 大

---

## 使用示例

```
这是我的 AMOS 输出（粘贴表格）：
Model Fit: CMIN=412.3, DF=180, P=.000, CMIN/DF=2.29, CFI=.941, TLI=.931,
RMSEA=.064, SRMR=.051
路径：语言风格 → 信任  Estimate=.412, S.E.=.078, C.R.=5.28, P=***
      信任 → 购买意愿  Estimate=.531, S.E.=.081, C.R.=6.55, P=***
假设：H1 语言具体性正向影响信任；H2 信任正向影响购买意愿
样本量 N=320
帮我写 Results 部分，英文。
```

技能会逐项解读、标注哪些达标哪些需要注意（此例 CFI .941 属「可接受」而非「良好」，
它会指出），然后生成符合 APA 7th 的英文段落，并对每条假设给出
supported / not supported 的明确判断。

---

## 目录结构

```
stats-results-writer/
├── SKILL.md                        工作流程、软件识别指南、阈值速查
└── references/
    ├── 01-measurement.md           信度效度、CFA、CMB
    ├── 02-anova-ttest.md           ANOVA、t 检验
    ├── 03-regression.md            OLS、层次回归、Logistic
    ├── 04-mediation.md             中介效应
    ├── 05-moderation.md            调节效应
    ├── 06-moderated-mediation.md   有调节的中介
    ├── 07-cb-sem.md                CB-SEM（AMOS/Mplus/lavaan）
    └── 08-pls-sem.md               PLS-SEM（SmartPLS）
```

---

## 边界与注意事项

- **数字原封不动。** 写作文本中的所有数字必须来自你提供的输出，
  技能不得自行估算或修改。**但如果粘贴的数字本身有误，结论也会有误**——
  请以原始软件输出为准。
- **它不会把不显著写成显著。** 技能明确禁止「边缘显著」等模糊表述。
- **缺失信息会主动提示。** 若你提供的数字不足以完整报告（如缺 SE 或置信区间），
  技能会明确告诉你需要补充哪些数据，而不是猜一个填上。
- **学位论文 vs 期刊**：学位论文可更详尽；期刊投稿应简洁，详细表格入正文、文字简述。

---

## 与 sem-analysis-tutor 的分工

**这个技能负责「写」，不负责「做」。** 如果你还没跑分析、或指标不达标不知道怎么处理，
用 [`sem-analysis-tutor`](../sem-analysis-tutor/)——它会带你逐步完成分析。

---

## 版本

**1.0.0** —— 8 册分方法参考、9 类软件输出识别、中英文双语写作模板、
CB-SEM/PLS-SEM 双轨阈值速查。
