# 参考文件04：中介效应分析

## 适用场景
- Bootstrap间接效应检验（Hayes PROCESS / R mediation包 / lavaan）
- Sobel检验（已不推荐，但部分旧文献仍使用）
- 完全中介 vs. 部分中介的判断
- 多重中介（Multiple Mediators）

---

## 核心概念与符号

```
X ──a──→ M ──b──→ Y
X ──────c'──────→ Y  (直接效应)

间接效应 = a × b
总效应 = c = a×b + c'
中介比例 = (a×b) / c
```

---

## 必须报告的统计量

| 统计量 | 说明 | 报告要求 |
|--------|------|---------|
| a路径 | X→M，含B/β, SE, p | 必报 |
| b路径 | M→Y（控制X），含B/β, SE, p | 必报 |
| c'（直接效应） | X→Y（控制M），含B/β, SE, p | 必报 |
| c（总效应） | X→Y（不控制M），含B/β, SE, p | 必报 |
| 间接效应 a×b | 含点估计、SE、Bootstrap 95% CI | 必报 |
| Bootstrap样本量 | 通常5000次 | 必须注明 |

**判断标准**：
- Bootstrap 95% CI 不含0 → 间接效应显著（中介成立）
- Bootstrap 95% CI 含0 → 间接效应不显著
- 不再使用"完全中介/部分中介"的表述（现代做法是报告直接效应是否显著）

---

## 软件输出对应

### PROCESS (Hayes, SPSS/R)
```
关键输出位置：
- "a" coefficient → X→M路径
- "b" coefficient → M→Y路径（在Y方程中）
- "c'" (c-prime) → 直接效应
- "c" → 总效应
- "INDIRECT EFFECT" → 间接效应及Bootstrap CI
  - "BootLLCI" → 置信区间下限
  - "BootULCI" → 置信区间上限
```

### R (mediation包)
```
summary(mediate())输出：
- ACME = Average Causal Mediation Effect（间接效应）
- ADE  = Average Direct Effect（直接效应）
- Total Effect = 总效应
- Prop. Mediated = 中介比例
- 置信区间：95% CI lower / upper
```

### lavaan (R) / Mplus
```
使用sem()定义，indirect效应通过:=运算符计算：
indirect := a*b
直接效应：c'
总效应：c' + a*b
Bootstrap置信区间通过se = "bootstrap"或BOOTSTRAP命令获取
```

### SmartPLS (PLS-SEM中介)
```
Indirect Effects表：
- 间接效应值
- Bootstrap 95% CI（含LLCI, ULCI）
路径系数表：各路径系数和显著性
```

---

## 写作模板

### 简单中介（英文，Bootstrap）
```
We tested the mediating role of [M] in the relationship between [X] and [Y]
using the PROCESS macro (Hayes, 2022, Model 4) with 5,000 bootstrap samples.

The indirect effect of [X] on [Y] through [M] was [positive/negative]
and statistically significant (indirect effect = [value], SE = [value],
95% CI [[BootLL], [BootUL]]). Specifically, [X] was positively/negatively
associated with [M] (a = [value], SE = [value], p [< .001 / = .XXX]),
and [M] in turn significantly predicted [Y] after controlling for [X]
(b = [value], SE = [value], p [< .001 / = .XXX]).

The direct effect of [X] on [Y] was [significant: c' = [value], SE = [value],
p = [value] / not significant: c' = [value], SE = [value], p = [value]],
suggesting [partial/full] mediation.
The total effect of [X] on [Y] was also significant (c = [value],
SE = [value], p [< .001 / = .XXX]).
```

### 简单中介（中文，Bootstrap）
```
本研究采用Hayes（2022）的PROCESS宏（模型4）检验[中介变量M]在
[自变量X]与[因变量Y]之间的中介作用，Bootstrap重抽样次数为5,000次。

结果显示，[X]通过[M]对[Y]的间接效应显著（间接效应 = [值], SE = [值],
95% CI [[下限], [上限]]），置信区间不含0。具体而言，[X]对[M]具有
显著的正向（负向）影响（a = [值], SE = [值], p [< .001 / = .XXX]）；
在控制[X]后，[M]对[Y]的影响同样显著（b = [值], SE = [值],
p [< .001 / = .XXX]）。

[X]对[Y]的直接效应[显著（c' = [值], SE = [值], p = [值]），
表明[M]对两者关系起部分中介作用 /
不显著（c' = [值], SE = [值], p = [值]），
表明[M]完全中介了[X]对[Y]的影响]。
```

### 多重中介（英文）
```
We examined multiple mediation with [M1] and [M2] as parallel mediators
using PROCESS Model 4 (Hayes, 2022) with 5,000 bootstrap samples.

The total indirect effect of [X] on [Y] through both mediators was
significant (total indirect = [value], 95% CI [[BootLL], [BootUL]]).

Examining specific indirect paths, the indirect effect through [M1] was
significant (indirect = [value], 95% CI [[BootLL], [BootUL]]).
The indirect effect through [M2] was [significant/not significant]
(indirect = [value], 95% CI [[BootLL], [BootUL]]).

Contrast tests indicated that the two indirect effects did not differ
significantly ([contrast = value], 95% CI [[BootLL], [BootUL]]).
```

---

## 假设支持判断模板

```
H[X]（[M]在[X]→[Y]中起中介作用）：
→ Bootstrap CI 不含0：✅ 支持 H[X]
→ Bootstrap CI 含0：❌ 不支持 H[X]

写法：
支持：Hypothesis [X], which predicted that [M] mediates the [X]–[Y] relationship,
      was supported (indirect effect = [value], 95% CI [[LL], [UL]]).

不支持：Hypothesis [X] was not supported, as the bootstrap confidence interval
        for the indirect effect included zero (indirect effect = [value],
        95% CI [[LL], [UL]]).
```

---

## 中介分析结果汇总表格

```
Table X
Results of Mediation Analysis

Path               B      SE      p      95% CI
X → M (a)        X.XX   X.XX   .XXX   [X.XX, X.XX]
M → Y (b)        X.XX   X.XX   .XXX   [X.XX, X.XX]
X → Y (c')       X.XX   X.XX   .XXX   [X.XX, X.XX]  (direct)
X → Y (c)        X.XX   X.XX   .XXX   [X.XX, X.XX]  (total)
Indirect (a×b)   X.XX   X.XX    —     [X.XX, X.XX]ᵃ

Note. N = [X]. ᵃ Bootstrap 95% CI based on 5,000 resamples.
```

---

## 常见注意事项

### 关于"完全中介"的表述
```
现代建议（Hayes & Rockwood, 2020）：
不再使用"完全中介"/"部分中介"的二分法。
直接报告间接效应的点估计和CI，直接效应是否显著作为补充信息。

如审稿人要求："Although we avoid the full/partial mediation dichotomy
(Hayes & Rockwood, 2020), the direct effect was [significant/nonsignificant],
suggesting that [M] [partially/fully] accounts for the [X]–[Y] relationship."
```

### Bootstrap样本量
```
标准：5,000次（大多数期刊接受）
严格：10,000次（推荐用于发表）
低于1,000次不建议使用
```

### Sobel检验的处理
```
若用户提供了Sobel z/t检验结果：
可以报告，但需注明该检验假设间接效应正态分布，
统计效力低于Bootstrap方法，建议同时报告Bootstrap CI。
```
