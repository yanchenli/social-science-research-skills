# 参考文件03：回归分析

## 适用场景
- 简单线性回归（Simple Linear Regression）
- 多元线性回归（Multiple Linear Regression）
- 层次回归（Hierarchical Regression）
- Logistic回归（Binary / Ordinal / Multinomial）
- 含控制变量的回归报告

---

## 必须报告的统计量

### OLS线性回归
| 统计量 | 报告要求 |
|--------|---------|
| R² / Adjusted R² | 整体模型必报 |
| F(df₁, df₂), p | 整体模型显著性 |
| β（非标准化）, SE | 每个预测变量必报 |
| β*（标准化） | 推荐报告，便于比较 |
| t, p | 每个预测变量 |
| 95% CI for β | 推荐报告（APA 7th鼓励） |
| VIF | 多元回归必检查（< 5 理想，< 10 可接受） |

### 层次回归额外报告
| 统计量 | 说明 |
|--------|------|
| ΔR² | 每步新增预测力 |
| ΔF(df₁, df₂), p | 增量显著性检验 |

---

## 软件输出对应字段

### SPSS
```
Model Summary表：R, R², Adjusted R², Std. Error of Estimate
ANOVA表：F, df, Sig.（整体模型检验）
Coefficients表：B（非标准化）, Std. Error, Beta（标准化）, t, Sig., 95% CI, VIF
```

### R (lm)
```
summary(lm())输出：
- Coefficients部分：Estimate（=B）, Std. Error, t value, Pr(>|t|)
- 底部：Multiple R-squared, Adjusted R-squared, F-statistic, p-value
VIF：car::vif(model)
```

### Python (statsmodels)
```
OLS Regression Results：
- coef列 = B（非标准化）
- std err = SE
- t列 = t值
- P>|t| = p值
- [0.025 0.975] = 95% CI
- R-squared, Adj. R-squared, F-statistic, Prob (F-statistic)
```

### JASP
```
ANOVA表：F值、df、p、R²
Coefficients表：Unstandardized B, SE, Standardized β, t, p, 95% CI
```

---

## 写作模板

### 简单/多元回归（英文）
```
[A / Multiple] linear regression was conducted to examine the effects of
[predictor(s)] on [outcome]. The model was statistically significant,
F([df₁], [df₂]) = [value], p [< .001 / = .XXX], R² = [value],
adjusted R² = [value], indicating that the predictor(s) accounted for
[XX]% of the variance in [outcome].

[Predictor A] significantly predicted [outcome] (B = [value], SE = [value],
β = [value], t([df]) = [value], p [< .001 / = .XXX], 95% CI [[lower], [upper]]).

[Predictor B] was not a significant predictor (B = [value], SE = [value],
β = [value], t([df]) = [value], p = [value]).
```

### 层次回归（英文）
```
Hierarchical multiple regression was conducted to examine [research question].
In Step 1, [control variables] were entered; in Step 2, [main predictors]
were added.

Step 1 was statistically significant, F([df₁], [df₂]) = [value], p = [value],
R² = [value]. In Step 2, the addition of [predictors] significantly increased
explained variance, ΔR² = [value], ΔF([df₁], [df₂]) = [value], p [< .001 / = .XXX],
total R² = [value], adjusted R² = [value].

[Variable A] significantly predicted [outcome] (B = [value], SE = [value],
β = [value], p [< .001 / = .XXX]).
```

### 多元回归（中文）
```
本研究以[结果变量]为因变量，以[预测变量们]为自变量进行多元线性回归分析。
回归模型整体显著，F([df₁], [df₂]) = [值], p [< .001 / = .XXX]，
R² = [值]，调整后R² = [值]，预测变量共解释[结果变量][XX]%的方差。

[变量A]对[结果变量]具有显著的正向（负向）预测作用（B = [值], SE = [值],
β = [值], t = [值], p [< .001 / = .XXX], 95% CI [[下限], [上限]]）。

[变量B]对[结果变量]的预测效果不显著（B = [值], SE = [值], β = [值],
t = [值], p = [值]）。
```

### 层次回归（中文）
```
本研究采用层次回归分析[研究问题]。第一步纳入[控制变量]；
第二步加入[主要预测变量]。

第一步回归模型显著，F([df₁], [df₂]) = [值], p = [值], R² = [值]。
第二步新增变量后，模型解释力显著提升，ΔR² = [值]，
ΔF([df₁], [df₂]) = [值], p [< .001 / = .XXX]，总R² = [值]（调整后R² = [值]）。

[变量A]对[结果变量]具有显著预测作用（B = [值], SE = [值], β = [值],
p [< .001 / = .XXX]）。
```

---

## 回归结果表格格式（APA）

```
Table X
Results of Hierarchical Regression Analysis Predicting [Outcome]

                    Step 1              Step 2
Variable         B     SE    β        B     SE    β
Control 1       X.XX  X.XX  .XX     X.XX  X.XX  .XX
Control 2       X.XX  X.XX  .XX     X.XX  X.XX  .XX
Predictor A                         X.XX  X.XX  .XX**
Predictor B                         X.XX  X.XX  .XX*

R²              .XX                 .XX
ΔR²             .XX                 .XX
F             X.XX**              X.XX**

Note. N = [X]. Unstandardized coefficients reported.
* p < .05. ** p < .01. *** p < .001.
```

---

## Logistic回归写作模板

### 二元Logistic（英文）
```
Binary logistic regression was conducted to predict [outcome].
The model was statistically significant, χ²([df]) = [value], p [< .001],
Nagelkerke R² = [value].

[Predictor A] significantly predicted [outcome] (B = [value], SE = [value],
Wald = [value], p [< .001], OR = [value], 95% CI [[lower], [upper]]),
indicating that a one-unit increase in [A] was associated with a [XX]%
[increase/decrease] in the odds of [outcome].
```

---

## 共线性诊断与处理

```
VIF检查（必须在文中注明）：

If VIF < 5（正常）：
"Variance inflation factors (VIFs) for all predictors were below 5.0
(range: [min]–[max]), indicating no multicollinearity concern."

If 5 ≤ VIF < 10（中等）：
"Although VIF for [variable] was somewhat elevated ([value]),
it remained below the conservative threshold of 10,
suggesting multicollinearity did not critically compromise the results."

If VIF ≥ 10（严重）：需告知用户考虑变量删除、岭回归或PCA降维。
```
