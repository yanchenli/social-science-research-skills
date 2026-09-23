# 参考文件08：PLS-SEM（SmartPLS）

## 适用场景
- SmartPLS测量模型评估（反映型/形成型构念）
- PLS路径系数与Bootstrap显著性检验
- R²、Q²、f²、q²效应量
- 预测相关性（PLSpredict）
- HTMT判别效度
- 多群组分析（MGA）

---

## PLS-SEM两步流程

```
Step 1：评估测量模型（Outer Model）
  反映型（Reflective）→ 信度、收敛效度、判别效度
  形成型（Formative）→ 指标权重、VIF、外部效度

Step 2：评估结构模型（Inner Model）
  路径系数、R²、Q²、f²、间接效应Bootstrap检验
```

---

## 反映型测量模型评估标准

| 指标 | 标准 | SmartPLS输出位置 |
|------|------|----------------|
| 外部载荷（Outer Loading） | ≥ .70 | Outer Loadings表 |
| AVE | ≥ .50 | Construct Reliability表 |
| CR（组合信度） | ≥ .70 | Construct Reliability表 |
| Cronbach's α | ≥ .70 | Construct Reliability表 |
| HTMT（判别效度） | < .85（严格）/ < .90（宽松） | HTMT表 |

**HTMT Bootstrap检验**：HTMT的95% CI不含1.00，也可作为判别效度证据。

**Fornell-Larcker准则**（传统，已部分被HTMT取代）：
AVE的平方根 > 各构念间相关系数

---

## 形成型测量模型评估标准

| 指标 | 标准 | 说明 |
|------|------|------|
| 指标VIF | < 5（< 3.3更严格） | 多重共线性 |
| 外部权重（Outer Weight）| Bootstrap检验显著 | 各指标贡献 |
| 外部载荷（作为参考） | ≥ .50 | 权重不显著时参考载荷 |

---

## 结构模型评估标准

| 指标 | 标准 | 说明 |
|------|------|------|
| 路径系数 | Bootstrap检验 | t > 1.96（双尾p < .05） |
| R² | .25=弱, .50=中, .75=强（Hair等建议） | 内生变量方差解释 |
| Q²（预测相关性） | > 0 | Blindfolding；> 0 = 模型有预测相关性 |
| f²（效应量） | .02=小, .15=中, .35=大 | 每条路径的效应量 |
| SRMR | < .08（< .05更好） | 整体拟合 |

---

## SmartPLS输出对应

### 测量模型
```
Outer Loadings表：
  每个构念的每个指标 → 载荷值（≥.70）

Construct Reliability and Validity表：
  Cronbach's Alpha | rho_A | Composite Reliability | AVE
  每行一个构念

HTMT表：
  矩阵形式，上三角或下三角，数值 < .85/.90

Fornell-Larcker Criterion表：
  对角线 = √AVE；其余 = 构念间相关
```

### 结构模型
```
Path Coefficients表：
  每条路径 → Original Sample, Sample Mean, Std. Dev., T Statistics, P Values

R Square表：
  每个内生变量 → R², R² Adjusted

Indirect Effects表（Bootstrap）：
  间接效应路径 → 效应值, Bootstrap CI (2.5%, 97.5%)

f² Effect Size表：
  每条路径的效应量

Q² (Construct Crossvalidated Redundancy)：
  每个内生构念的Q²
```

---

## 写作模板

### PLS测量模型（英文）
```
We assessed the measurement model following Hair et al. (2022).
For reflective constructs, all outer loadings exceeded the recommended
threshold of .70 (range: [min]–[max]), providing evidence of indicator
reliability. AVE values ranged from [min] to [max], all above .50,
supporting convergent validity. Composite reliability (CR) and
Cronbach's alpha ranged from [min] to [max] and [min] to [max],
respectively, both exceeding .70, indicating adequate construct reliability.

Discriminant validity was assessed using the HTMT criterion
(Henseler et al., 2015). All HTMT values were below .85
(range: [min]–[max]), and bootstrapped 95% confidence intervals
did not include 1.00, supporting discriminant validity.
```

### PLS测量模型（中文）
```
本研究遵循Hair等人（2022）的建议对测量模型进行评估。
反映型构念的外部载荷均超过.70的推荐阈值（范围：[最小值]–[最大值]），
表明指标信度良好。各构念的平均提取方差（AVE）范围为[最小值]至[最大值]，
均超过.50，支持收敛效度。组合信度（CR）和Cronbach's α分别介于
[最小值]至[最大值]之间，均超过.70，构念信度良好。

判别效度方面，采用HTMT准则（Henseler等, 2015）进行评估，
所有HTMT值均低于.85（范围：[最小值]–[最大值]），
且Bootstrap 95%置信区间均不含1.00，判别效度得到支持。
```

### PLS结构模型与假设检验（英文）
```
We evaluated the structural model using 5,000 bootstrap samples
(Hair et al., 2022). The model explained [XX]% of the variance
in [Y] (R² = [value]).

As hypothesized, [X] had a significant positive effect on [Y]
(β = [value], t = [value], p [< .001 / = .XXX], 95% CI [[BootLL], [BootUL]]),
supporting Hypothesis [X].

[X2] did not significantly predict [Y] (β = [value], t = [value],
p = [value], 95% CI [[BootLL], [BootUL]]), and Hypothesis [Y]
was not supported.

The predictive relevance of the model was confirmed (Q² = [value] > 0).
Effect sizes (f²) ranged from [min] to [max], indicating
[small to large] practical significance.
```

### PLS结构模型与假设检验（中文）
```
采用Bootstrap（5,000次重抽样）对结构模型进行评估（Hair等, 2022）。
模型对[Y]的解释方差为[XX]%（R² = [值]）。

[X]对[Y]具有显著的正向影响（β = [值], t = [值], p [< .001 / = .XXX],
95% CI [[下限], [上限]]），假设[H?]得到支持。

[X2]对[Y]的影响不显著（β = [值], t = [值], p = [值],
95% CI [[下限], [上限]]），假设[H?]未得到支持。

模型的预测相关性良好（Q² = [值] > 0），路径效应量（f²）
范围为[最小值]至[最大值]，表明各路径具有[小至大]的实践显著性。
```

---

## 假设检验汇总表格（PLS）

```
Table X
Results of PLS Structural Model: Path Coefficients and Hypothesis Tests

Hypothesis  Path         β      t      p      95% CI          Result
H1          X1 → M      .XX   X.XX  .XXX  [X.XX, X.XX]      Supported
H2          X1 → Y      .XX   X.XX  .XXX  [X.XX, X.XX]      Supported
H3          M  → Y      .XX   X.XX  .XXX  [X.XX, X.XX]      Supported
H4          X2 → Y      .XX   X.XX  .XXX  [X.XX, X.XX]  Not Supported

Indirect Effect (H5)
X1 → M → Y             .XX    —    —    [X.XX, X.XX]      Supported

Note. N = [X]. Bootstrap 95% CI based on 5,000 resamples.
R² values: M = .XX, Y = .XX. Q² values: M = .XX, Y = .XX.
```

---

## PLS-SEM特有说明

### t值判断标准（单/双尾）
```
单尾检验（方向性假设，如"X正向影响Y"）：
  t > 1.645 → p < .05
  t > 2.326 → p < .01

双尾检验（无方向假设）：
  t > 1.960 → p < .05
  t > 2.576 → p < .01

大多数管理学期刊要求双尾检验，即t > 1.960。
```

### SRMR在PLS中的解释
```
PLS-SEM没有等价于CB-SEM的全局拟合指标。
SRMR < .08 作为参考，但不如CB-SEM中严格。
部分期刊不强制要求PLS的整体拟合指标。
```

### 关于共同方法偏差（CMB）
```
PLS中可用Full Collinearity VIF（AFVIF）检验CMB：
AFVIF < 3.3 表明无严重CMB问题。
```
