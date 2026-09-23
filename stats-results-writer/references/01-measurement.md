# 参考文件01：测量模型 — 信度、效度、CFA、共同方法偏差

## 适用场景
- 报告Cronbach's α、CR、AVE等信度效度指标
- 报告验证性因子分析（CFA）结果
- 报告判别效度（AVE法、HTMT法、Fornell-Larcker准则）
- 报告共同方法偏差（CMB）检验结果

---

## 必须报告的指标清单

### 信度
| 指标 | 符号 | 报告要求 |
|------|------|---------|
| Cronbach's Alpha | α | 每个构念必报 |
| 组合信度 | CR | 推荐与α同时报告；PLS必报 |

### 收敛效度
| 指标 | 符号 | 标准 | 报告要求 |
|------|------|------|---------|
| 因子载荷 | λ | ≥ .50（理想≥ .70） | 每个题项必报 |
| 平均提取方差 | AVE | ≥ .50 | 每个构念必报 |

### 判别效度（三选一或多选，说明用哪种方法）
| 方法 | 标准 | 适用情境 |
|------|------|---------|
| Fornell-Larcker准则 | AVE的平方根 > 与其他构念的相关系数 | CB-SEM常用 |
| HTMT（异质-单质比） | < .85（严格）或 < .90（宽松） | PLS-SEM推荐 |
| AVE法（CB-SEM） | φ²（相关系数²）< AVE | 传统方法 |

---

## CFA拟合指标

报告以下全部指标（CB-SEM/AMOS/lavaan/Mplus）：

| 指标 | 良好 | 可接受 | 报告格式 |
|------|------|--------|---------|
| χ² (df, p) | — | — | χ²(df) = X.XX, p = .XXX |
| χ²/df (CMIN/DF) | < 2 | < 3 | X.XX |
| CFI | ≥ .95 | ≥ .90 | .XXX |
| TLI (NNFI) | ≥ .95 | ≥ .90 | .XXX |
| RMSEA [90% CI] | < .05 | < .08 | .XXX [.XXX, .XXX] |
| SRMR | < .05 | < .08 | .XXX |

---

## 共同方法偏差（CMB）检验

常用方法及报告模板：

### Harman单因子检验
**判断标准**：单一因子解释方差 < 50%

**英文模板**：
```
We conducted Harman's single-factor test to assess common method bias.
The results showed that a single factor accounted for [XX]% of the total variance,
which is below the 50% threshold, suggesting that common method bias is not
a serious concern in this study.
```

**中文模板**：
```
为检验共同方法偏差，本研究采用Harman单因子检验。结果显示，单一因子解释的方差为[XX]%，
低于50%的临界值，表明共同方法偏差对本研究结论不构成实质性威胁。
```

### 标记变量法（Marker Variable）
```
Following Lindell and Whitney (2001), we included a theoretically unrelated
marker variable. The correlations between study variables did not change
substantially after partialing out the marker variable (average change = .0X),
suggesting minimal common method bias.
```

### CFA模型对比法（推荐）
```
We conducted a confirmatory factor analysis comparing our hypothesized
measurement model against a single-factor model. The hypothesized model
fit the data significantly better (Δχ²(Δdf) = XXX, p < .001), providing
evidence against substantial common method variance.
```

---

## 写作模板

### 测量模型整体描述（英文，CB-SEM）
```
We assessed the measurement model using confirmatory factor analysis (CFA)
in AMOS [version]. The model demonstrated acceptable fit to the data:
χ²([df]) = [value], χ²/df = [value], CFI = [value], TLI = [value],
RMSEA = [value] (90% CI [lower, upper]), SRMR = [value].

All factor loadings were statistically significant (ps < .001) and ranged
from [min] to [max] (M = [mean]), supporting convergent validity.
Average variance extracted (AVE) values ranged from [min] to [max],
all exceeding the recommended threshold of .50 (Fornell & Larcker, 1981).
Composite reliability (CR) ranged from [min] to [max], all above .70,
indicating adequate reliability.

To assess discriminant validity, we compared the square root of each
construct's AVE with its correlations with other constructs. As shown in
Table [X], the square root of AVE for each construct exceeded its
correlations with all other constructs, supporting discriminant validity.
```

### 测量模型整体描述（中文，CB-SEM）
```
本研究采用AMOS [版本]进行验证性因子分析（CFA）以评估测量模型。
模型拟合指标如下：χ²([df]) = [值]，χ²/df = [值]，CFI = [值]，
TLI = [值]，RMSEA = [值]（90% CI [下限, 上限]），SRMR = [值]，
整体拟合良好。

所有因子载荷均达到显著水平（ps < .001），范围为[最小值]至[最大值]
（M = [均值]），支持收敛效度。各构念的平均提取方差（AVE）范围为
[最小值]至[最大值]，均超过.50的推荐阈值（Fornell & Larcker, 1981）。
组合信度（CR）范围为[最小值]至[最大值]，均高于.70，信度良好。

判别效度方面，各构念AVE平方根均大于其与其他构念的相关系数
（见表[X]），判别效度得到支持。
```

### PLS测量模型描述（英文，SmartPLS）
```
The measurement model was evaluated following the two-step approach
recommended by Anderson and Gerbing (1988). For reflective constructs,
all outer loadings exceeded .70 (range: [min]–[max]), and AVE values
ranged from [min] to [max], all above the .50 threshold, demonstrating
convergent validity. CR values ranged from [min] to [max], indicating
adequate reliability.

Discriminant validity was assessed using the HTMT criterion (Henseler
et al., 2015). All HTMT values were below .85 (range: [min]–[max]),
supporting discriminant validity.
```

---

## 信度效度汇总表格格式

### APA格式（英文论文）

```
Table X
Descriptive Statistics, Reliabilities, and Correlations

Construct  M    SD    α    CR   AVE    1      2      3
1. [Name]  X.XX X.XX  .XX  .XX  .XX  (.XX)
2. [Name]  X.XX X.XX  .XX  .XX  .XX   .XX   (.XX)
3. [Name]  X.XX X.XX  .XX  .XX  .XX   .XX    .XX   (.XX)

Note. Diagonal elements in parentheses are the square roots of AVE.
* p < .05. ** p < .01. *** p < .001.
```

---

## 常见问题处理

### 载荷低于.50的题项
```
建议：报告时注明该题项已删除，并说明删除原因。
写法：Item [X] was removed due to a low factor loading (λ = .XX),
which is below the acceptable threshold of .50.
```

### AVE略低于.50（如.48）
```
处理方式：若CR > .60且载荷整体可接受，部分期刊可接受。
需在文中说明：Although the AVE for [construct] was slightly below .50
(AVE = .48), its CR exceeded .70 (CR = .XX), suggesting adequate
reliability (Fornell & Larcker, 1981).
```

### 判别效度未通过
```
诚实报告，在Limitations中讨论：
The discriminant validity between [X] and [Y] was not fully established
(HTMT = .XX, exceeding the .85 threshold). This overlap may reflect
the conceptual proximity of these constructs, which we acknowledge
as a limitation.
```
