# 参考文件02：方差分析与t检验

## 适用场景
- 独立样本t检验（Independent Samples t-test）
- 配对样本t检验（Paired Samples t-test）
- 单因素方差分析（One-Way ANOVA）
- 多因素方差分析（Factorial ANOVA）
- 重复测量方差分析（Repeated Measures ANOVA）
- 协方差分析（ANCOVA）

---

## 必须报告的统计量

### t检验
| 统计量 | 符号 | 说明 |
|--------|------|------|
| t值 | t(df) | 含自由度 |
| p值 | p | 双尾 |
| 均值差 | M_diff | 两组均值之差 |
| 95%置信区间 | 95% CI | 均值差的置信区间 |
| 效应量 | d | Cohen's d；.20=小，.50=中，.80=大 |
| 各组均值和标准差 | M, SD | 必须报告 |

### ANOVA
| 统计量 | 符号 | 说明 |
|--------|------|------|
| F值 | F(df₁, df₂) | 含组间和组内自由度 |
| p值 | p | |
| 效应量 | η² 或 ηₚ² | .01=小，.06=中，.14=大 |
| 事后检验 | Tukey / Bonferroni | 当F显著时必须报告 |

---

## 软件输出识别与对应字段

### SPSS输出
```
独立样本t检验：
- "Levene's Test for Equality of Variances" → 先看方差齐性
- "t-test for Equality of Means" → 取对应行的t, df, Sig.
- 若Levene's F显著(p<.05)：用"Equal variances not assumed"那行

ANOVA输出：
- "Between Groups" → F值所在行
- "Within Groups" → 误差项
- "Total" → 总变异
```

### JASP输出
```
t检验：直接给出 t, df, p, Cohen's d, 95% CI
ANOVA：给出 F, df, p, η², ηₚ²
事后检验：给出成对比较结果（均值差、p值、效应量）
```

### R输出（t.test / aov）
```
t.test(): t = X.XX, df = XX, p-value = X.XXX
           95 percent confidence interval: [lower] [upper]

summary(aov()): Df Sum Sq Mean Sq F value Pr(>F)
                组间  X   X.XX   X.XX    X.XX   X.XXX
```

---

## 写作模板

### 独立样本t检验（英文）
```
An independent-samples t-test was conducted to examine [research question].
The results indicated that [Group A] (M = [value], SD = [value]) scored
significantly [higher/lower/differently] than [Group B] (M = [value],
SD = [value]), t([df]) = [value], p [< .001 / = .XXX], d = [value],
95% CI [[lower], [upper]].
```

**假设不显著时**：
```
The results indicated no significant difference between [Group A]
(M = [value], SD = [value]) and [Group B] (M = [value], SD = [value]),
t([df]) = [value], p = [value], d = [value], 95% CI [[lower], [upper]].
```

### 配对样本t检验（英文）
```
A paired-samples t-test indicated that [Time2/Condition B] scores
(M = [value], SD = [value]) were significantly [higher/lower] than
[Time1/Condition A] scores (M = [value], SD = [value]),
t([df]) = [value], p [< .001 / = .XXX], d = [value],
95% CI [[lower], [upper]].
```

### 单因素ANOVA（英文）
```
A one-way ANOVA revealed a significant effect of [IV] on [DV],
F([df₁], [df₂]) = [value], p [< .001 / = .XXX], η² = [value].

Post hoc comparisons using [Tukey HSD / Bonferroni correction] indicated
that [Group A] (M = [value], SD = [value]) scored significantly
[higher/lower] than [Group B] (M = [value], SD = [value]),
p [< .001 / = .XXX], d = [value].
[Groups X and Y did not differ significantly, p = .XXX.]
```

### 多因素ANOVA（英文，含交互效应）
```
A [2 × 2 / X × Y] factorial ANOVA was conducted with [Factor A] and
[Factor B] as between-subjects factors.

The main effect of [Factor A] was significant, F([df₁], [df₂]) = [value],
p = [value], ηₚ² = [value].

The main effect of [Factor B] was [significant/not significant],
F([df₁], [df₂]) = [value], p = [value], ηₚ² = [value].

Critically, the [Factor A] × [Factor B] interaction was [significant/
not significant], F([df₁], [df₂]) = [value], p = [value], ηₚ² = [value].
[If significant: → proceed to Simple Main Effects section below]
```

---

## Simple Main Effects（简单主效应）

**适用时机**：多因素ANOVA的交互效应显著后，必须进行简单主效应分析以解释交互的具体模式。不要仅报告交互效应显著就停下来。

**逻辑**：将数据在某个因素的每个水平上分开，检验另一个因素的效应。

### 软件操作对应

```
SPSS：
  语法：/EMMEANS = TABLES(A*B) COMPARE(A) ADJ(BONFERRONI)
        表示：在B的每个水平上，比较A的各组
  输出："Tests of Simple Main Effects"表
  → 给出每个B水平上A效应的F, df, p
  → "Pairwise Comparisons"表给出具体成对比较

JASP：
  ANOVA → Post Hoc Tests → 勾选交互项
  或：Simple Main Effects模块直接输出

R（emmeans包，推荐）：
  library(emmeans)
  emm <- emmeans(model, ~ A | B)   # 在B的每个水平上看A
  pairs(emm, adjust = "bonferroni")
  # 输出：contrast, estimate, SE, df, t.ratio, p.value

  也可反向：
  emm2 <- emmeans(model, ~ B | A)  # 在A的每个水平上看B
```

### 必须报告的统计量

| 统计量 | 说明 |
|--------|------|
| F([df₁],[df₂]), p | 每个水平上的简单主效应 |
| 均值差（MD）, SE | 具体成对比较 |
| p（校正后） | Bonferroni或Tukey校正 |
| 效应量 d 或 ηₚ² | 每个比较的效应量 |

### 写作模板（英文）

```
To interpret the significant [A × B] interaction, we conducted simple
main effects analyses using the emmeans package in R (Lenth, 2023),
with Bonferroni correction applied to all pairwise comparisons.

When [B = Condition 1], [Factor A] had a significant effect on [DV],
F([df₁], [df₂]) = [value], p [< .001 / = .XXX], ηₚ² = [value].
Pairwise comparisons revealed that [Group A1] (M = [value], SD = [value])
scored significantly [higher/lower] than [Group A2] (M = [value],
SD = [value]), MD = [value], SE = [value], p [< .001 / = .XXX],
d = [value].

When [B = Condition 2], the effect of [Factor A] was not significant,
F([df₁], [df₂]) = [value], p = [value], ηₚ² = [value], suggesting
that [A1] and [A2] did not differ under [Condition 2].
```

### 写作模板（中文）

```
为进一步解释显著的[A × B]交互效应，本研究采用R中的emmeans包
（Lenth, 2023）进行简单主效应分析，成对比较采用Bonferroni校正。

当[B = 条件1]时，[因素A]对[因变量]的简单主效应显著，
F([df₁], [df₂]) = [值], p [< .001 / = .XXX], ηₚ² = [值]。
成对比较结果显示，[A1组]（M = [值], SD = [值]）显著[高于/低于]
[A2组]（M = [值], SD = [值]），MD = [值], SE = [值],
p [< .001 / = .XXX], d = [值]。

当[B = 条件2]时，[因素A]的简单主效应不显著，
F([df₁], [df₂]) = [值], p = [值], ηₚ² = [值]，
表明[A1组]与[A2组]在[条件2]下无显著差异。
```

---

## Planned Contrasts（计划对比）

**适用时机**：研究者在数据收集**前**已有明确的方向性理论预测，直接检验特定的组间差异，无需先做整体F检验。

**与事后检验的关键区别**：

| | Planned Contrasts | Post Hoc（事后检验） |
|---|---|---|
| 时机 | 数据收集前预先设定 | 整体F显著后探索 |
| 前提 | 无需整体F显著 | 需整体F显著 |
| I类错误控制 | 较宽松（比较次数少） | 较严格 |
| 检验效力 | 较高 | 较低 |
| 适用 | 有明确理论预测时 | 探索性分析时 |

### 对比系数（Contrast Weights）设置

```
示例：4组（Control, Low, Medium, High）

对比1：Control vs. 所有处理组
  系数：[-3, 1, 1, 1]（所有系数之和=0）
  解读：检验控制组是否整体不同于处理组

对比2：线性趋势（Low < Medium < High）
  系数：[0, -1, 0, 1]（只比较Low vs. High）
  或线性：[0, -1.5, 0, 1.5]（等间距线性）

对比3：低剂量 vs. 高剂量
  系数：[0, -1, 0, 1]

注意：每个对比的系数之和必须为0；
      正交对比（两个对比系数的乘积之和=0）互不相关。
```

### 软件操作对应

```
SPSS：
  One-Way ANOVA → Contrasts → 输入每组系数
  输出："Contrast Tests"表 → t, df, p（等/不等方差两行）

R：
  # 方法1：contrasts包
  library(emmeans)
  emm <- emmeans(model, ~ Group)
  contrast(emm, list(
    "Control vs Treatment" = c(-3, 1, 1, 1),
    "Low vs High"          = c(0, -1, 0, 1)
  ))

  # 方法2：直接在lm中设置contrast matrix
  contrasts(df$Group) <- cbind(c(-3,1,1,1), c(0,-1,0,1))

JASP：
  ANOVA → Contrasts → Custom → 输入每个水平的系数
```

### 必须报告的统计量

| 统计量 | 说明 |
|--------|------|
| 对比名称/描述 | 说明这个对比检验的是什么 |
| t([df]) 或 F([df₁],[df₂]) | 对比检验统计量 |
| p | 单尾或双尾（说明使用哪种） |
| 均值差 MD, SE | 对比涉及的均值差 |
| 效应量 d 或 r | 建议报告 |

### 写作模板（英文）

```
Prior to data collection, we specified [X] planned contrasts based
on our theoretical predictions.

Contrast 1 tested whether [Control group] differed from the combined
[treatment groups]. As predicted, the control group scored significantly
lower than the treatment groups combined,
t([df]) = [value], p [< .001 / = .XXX] (one-tailed), d = [value].

Contrast 2 examined a linear trend across [Low], [Medium], and [High]
conditions. A significant linear trend emerged,
t([df]) = [value], p [< .001 / = .XXX], d = [value],
indicating that [DV] increased monotonically with [IV level].
```

### 写作模板（中文）

```
在数据收集前，本研究依据理论预测预先设定了[X]个计划对比。

对比1检验[控制组]与[处理组合并]之间的差异。结果与预测一致，
控制组显著低于处理组整体，t([df]) = [值], p [< .001 / = .XXX]
（单尾），d = [值]。

对比2检验[低]、[中]、[高]条件间的线性趋势，结果发现显著的线性趋势，
t([df]) = [值], p [< .001 / = .XXX], d = [值]，
表明[因变量]随[自变量水平]的提高而单调递增。
```

---

## 三类跟进分析的选择决策树

```
交互效应显著？
├── 是 → 进行 Simple Main Effects
│         ↓
│         每个简单主效应显著且有2+组？
│         └── 是 → 对该水平进行成对比较（Bonferroni校正）
│
└── 否 → 主效应显著且有2+组？
          ├── 是，探索性 → 事后检验（Tukey / Bonferroni / Games-Howell）
          └── 是，有预测 → 计划对比（Planned Contrasts）
```

---

## 中文写作模板（补充多因素ANOVA）

### 多因素ANOVA含简单主效应（中文）
```
以[因素A]（[A1] vs. [A2]）和[因素B]（[B1] vs. [B2]）为自变量，
以[因变量]为因变量进行2×2被试间方差分析。

[因素A]的主效应显著，F([df₁], [df₂]) = [值], p [< .001],
ηₚ² = [值]；[因素B]的主效应[显著/不显著]，
F([df₁], [df₂]) = [值], p = [值], ηₚ² = [值]。
更重要的是，[A] × [B]的交互效应显著，
F([df₁], [df₂]) = [值], p [< .001], ηₚ² = [值]。

简单主效应分析结果（Bonferroni校正）显示：
在[B1]条件下，[A1组]（M = [值], SD = [值]）的[因变量]
显著[高于/低于][A2组]（M = [值], SD = [值]），
F([df₁], [df₂]) = [值], p [< .001], d = [值]；
在[B2]条件下，[A1组]与[A2组]差异不显著，
F([df₁], [df₂]) = [值], p = [值]，与研究假设[H?]一致。
```

### 独立样本t检验（中文）
```
本研究采用独立样本t检验比较[A组]与[B组]在[因变量]上的差异。
结果显示，[A组]（M = [值], SD = [值]）显著[高于/低于][B组]
（M = [值], SD = [值]），t([df]) = [值], p [< .001 / = .XXX],
Cohen's d = [值], 95% CI [[下限], [上限]]。
```

### 单因素方差分析（中文）
```
单因素方差分析结果显示，[自变量]对[因变量]的主效应显著，
F([df₁], [df₂]) = [值], p [< .001 / = .XXX], η² = [值]。

事后检验（[Tukey/Bonferroni]）结果表明：[A组]（M = [值], SD = [值]）
显著[高于/低于][B组]（M = [值], SD = [值]），p [< .001 / = .XXX]，
效应量d = [值]。
```

---

## 效应量解释（Cohen, 1988）

| 统计方法 | 效应量指标 | 小 | 中 | 大 |
|---------|----------|----|----|---|
| t检验 | Cohen's d | .20 | .50 | .80 |
| ANOVA | η² | .01 | .06 | .14 |
| ANOVA | ηₚ² (偏η²) | .01 | .06 | .14 |

---

## 常见注意事项

### 方差齐性检验
```
若Levene's F显著（p < .05）：使用Welch校正的t检验（df为小数），
并在文中注明：Levene's test indicated unequal variances (F = X.XX, p = .XXX);
therefore, equal variances were not assumed.
```

### 正态性假设
```
若样本量 N > 30：通常可依据中心极限定理假设正态性满足。
若N较小（< 30）：报告Shapiro-Wilk检验结果，或改用非参数检验。
写法：The assumption of normality was verified using the Shapiro-Wilk test,
W = [value], p = [value].
```

### 事后检验的选择
```
- Tukey HSD：各组样本量相等时推荐
- Bonferroni：比较次数较少时推荐，控制I类错误较保守
- Games-Howell：方差不齐时推荐（无需等方差假设）
```
