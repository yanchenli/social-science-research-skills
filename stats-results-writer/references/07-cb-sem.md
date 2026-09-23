# 参考文件07：CB-SEM（AMOS / Mplus / lavaan）

## 适用场景
- 结构方程模型整体拟合评估
- 路径系数报告（直接效应）
- SEM中的间接效应（Bootstrap）
- 竞争模型比较（Model Comparison）
- 多群组分析（Multi-Group Analysis / Measurement Invariance）

---

## CB-SEM vs. PLS-SEM 选择提示

| 维度 | CB-SEM | PLS-SEM |
|------|--------|---------|
| 理论基础 | 验证理论（reflective构念） | 预测导向（也支持formative） |
| 样本量要求 | 较大（N > 200推荐） | 较小（N > 100可接受） |
| 分布假设 | 多变量正态（ML估计） | 无分布假设 |
| 拟合指标 | 丰富（CFI, RMSEA等） | 有限 |
| 适用期刊 | 顶级管理/营销期刊主流 | MISQ、信息系统、小样本研究 |

---

## 必须报告的拟合指标

| 指标 | 良好 | 可接受 | 报告格式 |
|------|------|--------|---------|
| χ²(df, p) | — | — | χ²(df) = X.XX, p = .XXX |
| χ²/df (CMIN/DF) | < 2 | ≤ 3 | X.XX |
| CFI | ≥ .95 | ≥ .90 | .XXX |
| TLI (NNFI) | ≥ .95 | ≥ .90 | .XXX |
| RMSEA [90% CI] | < .05 | < .08 | .XXX [.XXX, .XXX] |
| SRMR | < .05 | < .08 | .XXX |
| GFI | ≥ .95 | ≥ .90 | .XXX（部分期刊已不要求） |

> **注**：近年来部分顶刊（如JM, AMJ）建议将RMSEA < .06作为良好标准（Hu & Bentler, 1999）。需对照目标期刊要求。

---

## 软件输出对应

### AMOS
```
Model Fit Summary表：
- CMIN → χ²值，DF，P
- CMIN/DF → χ²/df
- CFI → .XXX
- TLI → .XXX（AMOS中为TLI）
- RMSEA → .XXX（含LO 90, HI 90 = 90% CI下上限）
- SRMR（需勾选输出）

路径系数：
- Estimate（非标准化）
- S.E.（标准误）
- C.R.（Critical Ratio，即t/z值）
- P → 显著性（***表示p<.001，AMOS用***代替精确p值）
- Standardized（标准化路径系数）
```

### lavaan (R)
```
lavaan::summary(fit, fit.measures = TRUE, standardized = TRUE)

拟合指标在"Model Test User Model"和"Model Fit Indices"部分：
- chisq, df, pvalue
- cfi, tli, rmsea, rmsea.ci.lower, rmsea.ci.upper, srmr

路径系数：
Regressions部分：Estimate, Std.Err, z-value, P(>|z|), Std.all
```

### Mplus
```
MODEL FIT INFORMATION部分：
- Chi-Square Test, df, p-value
- CFI, TLI, RMSEA, SRMR

MODEL RESULTS部分：
- Estimate, S.E., Est./S.E.（z值）, Two-Tailed P-Value
- Standardized（STDYX STANDARDIZATION）
```

---

## 写作模板

### 整体模型拟合（英文）
```
Structural equation modeling was conducted using [AMOS version X /
lavaan in R / Mplus version X] with maximum likelihood estimation.
The structural model demonstrated [acceptable/good] fit to the data:
χ²([df]) = [value], χ²/df = [value], CFI = [value], TLI = [value],
RMSEA = [value] (90% CI [lower, upper]), SRMR = [value].
```

### 整体模型拟合（中文）
```
本研究采用[AMOS版本X / R中的lavaan包 / Mplus版本X]进行结构方程模型分析，
使用最大似然估计法。结构模型的拟合结果如下：
χ²([df]) = [值], χ²/df = [值], CFI = [值], TLI = [值],
RMSEA = [值]（90% CI [[下限], [上限]]）, SRMR = [值]，
模型整体拟合[良好/可接受]。
```

### 路径系数汇报（英文）
```
[X] had a significant positive effect on [Y] (β = [value], SE = [value],
z = [value], p [< .001 / = .XXX]).

[X] did not significantly predict [Y] (β = [value], SE = [value],
z = [value], p = [value]).
```

### SEM中的间接效应（Bootstrap，英文）
```
We tested the indirect effect of [X] on [Y] via [M] using
bootstrapped standard errors (5,000 samples). The indirect effect
was significant (β = [value], 95% CI [[BootLL], [BootUL]]),
supporting the mediating role of [M].
```

### 竞争模型比较（英文）
```
We compared the hypothesized model against two alternative models.
Model 1 (hypothesized) fit the data [well], whereas Model 2
(all paths direct) showed poorer fit: Δχ²([Δdf]) = [value], p [< .001].
Model 3 (alternative theory) also fit worse than the hypothesized model:
Δχ²([Δdf]) = [value], p [< .001], ΔCFI = [value].
These results support the hypothesized model structure.
```

---

## 路径系数结果表格（APA格式）

```
Table X
Standardized Path Coefficients for the Structural Model

Path                           β      SE      z       p
X1 → M                       .XX    .XX    X.XX   .XXX
X2 → M                       .XX    .XX    X.XX   .XXX
M  → Y                       .XX    .XX    X.XX   .XXX
X1 → Y (direct)              .XX    .XX    X.XX   .XXX
X2 → Y (direct)              .XX    .XX    X.XX   .XXX

Model fit: χ²([df]) = X.XX, χ²/df = X.XX, CFI = .XXX, TLI = .XXX,
           RMSEA = .XXX [.XXX, .XXX], SRMR = .XXX
```

---

## 多群组分析（Measurement Invariance）

### 不变性检验步骤与写法
```
步骤：
1. 形态不变性（Configural）：相同的因子结构，所有参数自由估计
2. 量度不变性（Metric）：因子载荷相等
3. 标量不变性（Scalar）：载荷 + 截距相等

模型比较标准（推荐）：ΔCFI ≤ .010 且 ΔRMSEA ≤ .015（Cheung & Rensvold, 2002）

英文写法：
We tested measurement invariance across [groups] following
Vandenberg and Lance (2000). The configural model fit well
(CFI = [value], RMSEA = [value]). Metric invariance was supported
(ΔCFI = [value], ΔRMSEA = [value]), indicating equivalent factor loadings.
[Scalar invariance was also supported (ΔCFI = [value], ΔRMSEA = [value]),
allowing meaningful comparison of latent means across groups.]
```

---

## 常见问题处理

### χ²显著但其他指标良好
```
ML估计对样本量敏感，大样本下χ²几乎总是显著。
写法："Although the chi-square statistic was significant, χ²([df]) = [value],
p < .001, this statistic is known to be sensitive to sample size (Bentler &
Bonett, 1980). Other fit indices indicated acceptable fit (CFI = .XX,
RMSEA = .XX), and we proceed with model interpretation."
```

### 修正指数（Modification Indices）
```
若根据MI添加了误差相关项：
"Based on modification indices, we added [one/two] correlated
error terms between [Item X] and [Item Y]. This modification
was theoretically justified because [reason]."
注意：每次只添加一个，且需有实质性理由。
```
