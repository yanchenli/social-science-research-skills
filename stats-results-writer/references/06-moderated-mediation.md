# 参考文件06：有调节的中介效应（Moderated Mediation）

## 适用场景
- 第一阶段调节（W调节X→M，即a路径被调节）→ PROCESS Model 7
- 第二阶段调节（W调节M→Y，即b路径被调节）→ PROCESS Model 14
- 直接效应被调节（W调节X→Y，即c'路径被调节）→ PROCESS Model 1（简单调节）
- 同时调节第一和第二阶段 → PROCESS Model 58
- 双调节变量（V调节a路径，W调节b路径）→ PROCESS Model 83
- 被调节的中介（Mediated Moderation）→ 概念不同，注意区分

---

## 核心概念：条件间接效应

有调节的中介的核心结果是**条件间接效应（Conditional Indirect Effect）**：
在调节变量W的不同水平上，间接效应a×b是否显著，以及是否存在差异。

```
Model 7示意（W调节a路径）：
X ──a(W)──→ M ──b──→ Y
X ──────c'──────────→ Y

条件间接效应 = a(W) × b
= (a₁ + a₃×W) × b

当W取不同值时，条件间接效应大小不同。
检验调节中介：条件间接效应在不同W水平间是否有显著差异（即"index of moderated mediation"是否显著）
```

---

## 必须报告的统计量

| 统计量 | 说明 | 报告要求 |
|--------|------|---------|
| a路径主效应 | X→M，B, SE, p | 必报 |
| a×W交互项（Model 7）| X×W对M，B, SE, p | 必报 |
| b路径 | M→Y，B, SE, p | 必报 |
| b×W交互项（Model 14）| M×W对Y，B, SE, p | 必报 |
| c'直接效应 | X→Y，B, SE, p | 必报 |
| 条件间接效应 | W=低/均/高时的a×b | 必报，含Bootstrap 95% CI |
| 调节中介指数（Index of MM） | 检验调节效应是否显著改变了中介效应 | 强烈推荐，含Bootstrap 95% CI |

---

## PROCESS输出对应

### Model 7（第一阶段调节）
```
OUTCOME VARIABLE: M（中介变量方程）
  Coeff    se    t      p
X  a₁     ...          → X的主效应
W  a₂     ...          → W的主效应
X*W a₃   ...          → 交互项（调节效应）

OUTCOME VARIABLE: Y（结果变量方程）
  Coeff    se    t      p
X  c'     ...          → 直接效应
M  b      ...          → M的效应
W  ...                 → W的主效应（在c'方程中）

CONDITIONAL INDIRECT EFFECTS OF X ON Y:
W            Effect  BootSE  BootLLCI  BootULCI
-1SD         X.XXX   X.XXX   X.XXX     X.XXX
Mean         X.XXX   ...
+1SD         X.XXX   ...

INDEX OF MODERATED MEDIATION:
Index  BootSE  BootLLCI  BootULCI
X.XXX  X.XXX   X.XXX     X.XXX
```

---

## 写作模板

### 有调节的中介（英文，Model 7：W调节a路径）
```
We tested a first-stage moderated mediation model (Hayes, 2022, Model 7)
in which [W] was hypothesized to moderate the indirect effect of [X] on
[Y] through [M]. We used PROCESS with 5,000 bootstrap samples.
All continuous variables were mean-centered prior to analysis.

Results for the mediator ([M]) equation revealed a significant interaction
between [X] and [W] (B = [value], SE = [value], p [< .001 / = .XXX]),
indicating that [W] moderated the effect of [X] on [M].

Simple slope analyses showed that [X] significantly predicted [M]
when [W] was high (B = [value], SE = [value], p [< .001]),
but not when [W] was low (B = [value], SE = [value], p = [value]).

[M] significantly predicted [Y] after controlling for [X] and [W]
(B = [value], SE = [value], p [< .001]).

The index of moderated mediation was significant
(index = [value], 95% CI [[BootLL], [BootUL]]),
confirming that the indirect effect of [X] on [Y] via [M]
was contingent on [W].

Specifically, the conditional indirect effect was significant at high
levels of [W] (effect = [value], 95% CI [[BootLL], [BootUL]])
but not at low levels (effect = [value], 95% CI [[BootLL], [BootUL]]),
supporting Hypothesis [X].
```

### 有调节的中介（中文，Model 7）
```
本研究采用Hayes（2022）的PROCESS宏（模型7）检验有调节的中介模型，
即[W]对[X]通过[M]影响[Y]的间接效应的调节作用。Bootstrap重抽样
5,000次，连续变量进行均值中心化处理。

中介变量（[M]）方程中，[X]与[W]的交互项显著
（B = [值], SE = [值], p [< .001 / = .XXX]），
表明[W]调节了[X]对[M]的影响。

简单斜率分析显示，当[W]高（+1SD）时，[X]对[M]的影响显著
（B = [值], SE = [值], p [< .001]）；当[W]低（−1SD）时，
该影响不显著（B = [值], SE = [值], p = [值]）。

[M]在控制[X]和[W]后对[Y]具有显著影响
（B = [值], SE = [值], p [< .001]）。

调节中介指数显著（index = [值], 95% CI [[下限], [上限]]），
表明[X]通过[M]对[Y]的间接效应受到[W]的显著调节，假设[H?]得到支持。

具体而言，当[W]较高时，条件间接效应显著
（effect = [值], 95% CI [[下限], [上限]]）；当[W]较低时不显著
（effect = [值], 95% CI [[下限], [上限]]）。
```

### 有调节的中介（中文，Model 14：W调节b路径）
```
本研究采用PROCESS模型14检验[W]是否调节[M]→[Y]的路径（第二阶段调节）。

结果变量（[Y]）方程中，[M]与[W]的交互项[显著/不显著]
（B = [值], SE = [值], p = [值]）。

[如显著]：简单斜率分析显示，当[W]高时，[M]对[Y]的影响更强
（B = [值], SE = [值], p [< .001]）；当[W]低时，影响减弱
（B = [值], SE = [值], p = [值]）。

调节中介指数为[值]（95% CI [[下限], [上限]]），
置信区间[不含/含]零，假设[H?][得到/未得到]支持。
```

---

## 条件间接效应汇总表格

```
Table X
Conditional Indirect Effects of [X] on [Y] via [M]

[W] Level    Indirect Effect    Boot SE    95% CI
Low (−1 SD)      X.XXX           X.XXX    [X.XXX, X.XXX]
Mean (0)          X.XXX           X.XXX    [X.XXX, X.XXX]
High (+1 SD)     X.XXX           X.XXX    [X.XXX, X.XXX]

Index of Moderated Mediation: X.XXX, 95% CI [X.XXX, X.XXX]

Note. Bootstrap 95% CI based on 5,000 resamples.
      CI not containing zero indicates significance at p < .05.
```

---

## 常见PROCESS模型编号速查

| 模型 | 结构描述 | 调节位置 |
|------|---------|---------|
| Model 1 | X→Y，W调节 | c'路径 |
| Model 4 | X→M→Y（简单中介） | 无调节 |
| Model 7 | X→M→Y，W调节a路径 | 第一阶段 |
| Model 14 | X→M→Y，W调节b路径 | 第二阶段 |
| Model 58 | X→M→Y，W同时调节a和b | 两阶段 |
| Model 8 | X→M→Y，W调节a路径和c'路径 | a路径+直接效应 |
| Model 83 | X→M→Y，V调节a路径，W调节b路径 | 双调节变量 |

---

## 常见注意事项

### "调节中介"vs."中介调节"的区分
```
Moderated Mediation（有调节的中介）：
  → 调节变量W影响间接效应的大小
  → 核心问题："何时/对谁，中介效应更强？"
  → 更常见于管理学研究

Mediated Moderation（有中介的调节）：
  → 调节变量W的效应通过M传递
  → 较少使用，需明确区分
```

### Index of Moderated Mediation的重要性
```
仅报告条件间接效应在某个W水平显著而在另一水平不显著，
不足以证明调节效应存在（因为这可能只是统计效力差异）。
必须同时报告调节中介指数（Index of MM）且其CI不含0，
才能正式声明调节中介效应显著。
```
