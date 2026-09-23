# 参考文件05：调节效应分析

## 适用场景
- 交互项回归（Moderation via Interaction Term）
- 简单斜率分析（Simple Slope Analysis）
- Johnson-Neyman区间（Floodlight Analysis）
- 连续型调节变量 / 二分类调节变量
- PROCESS Model 1

---

## 必须报告的统计量

| 统计量 | 说明 | 报告要求 |
|--------|------|---------|
| 交互项系数 | X×W的β/B, SE, t, p | 调节效应核心，必报 |
| ΔR² | 加入交互项后的增量R² | 必报 |
| ΔF | 增量F检验 | 必报 |
| 简单斜率 | 高/低W（±1SD）时X→Y的斜率 | 交互显著时必报 |
| 简单斜率t, p | 各斜率是否显著 | 必报 |
| 主效应 X, W | B/β, SE, p | 必报（但中心化后解读变化） |

**关键前提**：自变量X和调节变量W必须进行**均值中心化（mean centering）**再计算交互项，以减少多重共线性并使主效应可解释。

---

## 软件输出对应

### PROCESS (Hayes, Model 1)
```
关键输出：
Block 1（主效应）：X的系数、W的系数
Block 2（交互项）：X*W的系数（Int_1）
Model Summary for Y：R², ΔR², F, ΔF

Conditional Effects（简单斜率）：
W值（通常是M-1SD, M, M+1SD）+ 对应的X→Y效应、SE、t、p、95% CI

Johnson-Neyman Analysis（floodlight）：
显著区域的W值边界点
```

### R (interactions包 / lm)
```
模型：lm(Y ~ X * W, data = df)
提取交互项：summary() → X:W行
简单斜率：sim_slopes(model, pred = X, modx = W)
可视化：interact_plot(model, pred = X, modx = W)
```

### JASP
```
ANOVA框架下：A×B交互效应的F, p, ηₚ²
回归框架下：Moderator Analysis模块，直接给出简单斜率
```

### SmartPLS
```
MGA (Multi-Group Analysis) 用于二分类调节
连续调节：Interaction Effects功能，输出路径系数和Bootstrap CI
```

---

## 写作模板

### 连续调节变量（英文，PROCESS Model 1）
```
We tested the moderating role of [W] in the [X]–[Y] relationship using
PROCESS Model 1 (Hayes, 2022) with 5,000 bootstrap samples.
Prior to analysis, [X] and [W] were mean-centered to reduce
multicollinearity (Aiken & West, 1991).

The interaction term (X × W) significantly predicted [Y]
(B = [value], SE = [value], t([df]) = [value], p [< .001 / = .XXX]),
explaining an additional [XX]% of variance (ΔR² = [value],
ΔF([df₁], [df₂]) = [value], p [< .001 / = .XXX]).

To probe the interaction, we examined the conditional effect of [X]
on [Y] at low (−1 SD), mean, and high (+1 SD) levels of [W].
[X] had a significant positive effect on [Y] when [W] was high
(B = [value], SE = [value], p [< .001]), but not when [W] was low
(B = [value], SE = [value], p = [value]), supporting [H?].
```

### 连续调节变量（中文）
```
本研究采用Hayes（2022）的PROCESS宏（模型1）检验[调节变量W]对
[自变量X]与[因变量Y]关系的调节作用，Bootstrap重抽样5,000次。
分析前对[X]和[W]进行均值中心化处理（Aiken & West, 1991）。

结果显示，交互项（X×W）对[Y]具有显著影响
（B = [值], SE = [值], t([df]) = [值], p [< .001 / = .XXX]），
纳入交互项后解释方差显著增加（ΔR² = [值], ΔF([df₁], [df₂]) = [值],
p [< .001 / = .XXX]），假设[H?]得到支持。

简单斜率分析结果显示，当[W]高（+1SD）时，[X]对[Y]的正向影响显著
（B = [值], SE = [值], p [< .001]）；当[W]低（−1SD）时，
该影响不显著（B = [值], SE = [值], p = [值]），表明[W]对[X]→[Y]
关系起正向调节作用。
```

### 二分类调节变量（英文）
```
We examined whether [W] moderated the [X]–[Y] relationship by
including the [X] × [W dummy] interaction term.

The interaction was [significant: B = [value], SE = [value], p = [value] /
not significant: B = [value], SE = [value], p = [value]].

When [W = Group A], [X] significantly predicted [Y]
(B = [value], SE = [value], p = [value]).
When [W = Group B], the effect was [significant/not significant]
(B = [value], SE = [value], p = [value]).
```

---

## 简单斜率结果汇总表格

```
Table X
Results of Moderation Analysis: Conditional Effects of [X] on [Y]

                          B      SE      t       p      95% CI
[W] = Low (−1 SD)       X.XX   X.XX   X.XX   .XXX   [X.XX, X.XX]
[W] = Mean              X.XX   X.XX   X.XX   .XXX   [X.XX, X.XX]
[W] = High (+1 SD)      X.XX   X.XX   X.XX   .XXX   [X.XX, X.XX]

Interaction (X × W)     X.XX   X.XX   X.XX   .XXX
ΔR²                      .XX
ΔF([df₁], [df₂])        X.XX***
```

---

## Johnson-Neyman区间写法

```
To identify the precise range of [W] for which [X] significantly
predicted [Y], we conducted a floodlight analysis (Johnson & Neyman, 1936;
Spiller et al., 2013). The effect of [X] on [Y] was significant when
[W] was [below X.XX / above X.XX] (or: between X.XX and X.XX),
which corresponded to [XX]% of participants in our sample.
```

---

## 调节效应的图形描述

```
Figure [X] illustrates the two-way interaction. As shown, the positive
effect of [X] on [Y] was stronger [when/for] [high-W group]
compared to [low-W group], consistent with our hypothesis.
```

---

## 常见注意事项

### 中心化（必须做）
```
均值中心化步骤：
X_c = X - mean(X)
W_c = W - mean(W)
XW = X_c × W_c

注意：标准化（z-score）也可使用，但均值中心化更常见。
二分类虚拟变量无需中心化。
```

### 交互项不显著时
```
不要说"边缘显著"。直接报告不显著结果：
"The interaction term was not statistically significant
(B = [value], p = [value]), indicating that [W] did not moderate
the [X]–[Y] relationship. Hypothesis [X] was not supported."
```

### 效应量
```
调节效应的效应量：f² = ΔR² / (1 - R²_full)
- .02 = 小效应
- .15 = 中效应
- .35 = 大效应

推荐报告f²：The effect size for the interaction was small/medium/large
(f² = [value]).
```
