# 第 5 步（附）：有调节的中介效应分析（Moderated Mediation）

> 本文件在用户模型同时包含**中介变量**和**调节变量**，且调节作用于中介链上的某条路径时触发。  
> 若中介与调节相互独立（分属不同路径），回到 `step5-medmod.md` 分别处理即可。

---

## 核心概念（向用户解释）

> "有调节的中介，检验的是：X 通过 M 影响 Y 的这条间接效应，会不会随着调节变量 W 的变化而改变强弱？  
> 例如：社交媒体使用（X）→ 品牌认知（M）→ 购买意愿（Y），而这条中介链的强弱受到品牌涉入度（W）的调节。  
> 具体来说，W 可以调节前半段（X→M）、后半段（M→Y），或同时调节两段。"

---

## 第一步：明确调节发生在哪一段

向用户确认以下问题（必须在运行前确认，否则模型设定会出错）：

| 问题 | 对应 Hayes PROCESS 模型编号 |
|------|--------------------------|
| W 调节 **X→M**（前半段）| Model 7 |
| W 调节 **M→Y**（后半段）| Model 14 |
| W 同时调节两段 | Model 58 |
| W 调节 X→M，且存在直接效应 X→Y | Model 8 |

> ✅ 若用户不确定，请他描述"W 会影响哪条箭头的强弱"，帮助判断后再确认。

---

## 路径 A：CB-SEM（lavaan）—— W 调节前半段（X→M）

### 适用条件
- W 是**单一观测变量**（非多题项潜变量）
- X、M、Y 均为多题项潜变量
- 样本量充足（建议 N ≥ 300，Bootstrap 需要更大样本）

### 操作步骤

```r
library(lavaan)

# ① 均值中心化 W（必须，降低多重共线性）
data$W_c <- scale(data$W, center = TRUE, scale = FALSE)

# ② 在结构模型中加入 X*W 交互项
#    注意：lavaan 不直接支持潜变量×观测变量交互，
#    此处 X 用其平均分（或合成分数）代替
data$X_score <- rowMeans(data[, c("X1","X2","X3")])
data$X_c     <- scale(data$X_score, center = TRUE, scale = FALSE)
data$XW      <- data$X_c * data$W_c

model_modmed <- '
  # 测量模型（复制第3步验证通过的版本）
  M =~ M1 + M2 + M3
  Y =~ Y1 + Y2 + Y3

  # 结构路径
  M ~ a1 * X_c + a2 * W_c + a3 * XW   # a3 = 前半段调节效应
  Y ~ b * M + c * X_c                   # b = 后半段，c = 直接效应
  
  # 条件间接效应（在 W 的低/均值/高三个水平上）
  # W 的 SD 需从数据中提取后手动填入
  indirect_low  := (a1 + a3 * (-1 * W_SD)) * b  # W = 均值 - 1SD
  indirect_mean := a1 * b                          # W = 均值
  indirect_high := (a1 + a3 * ( 1 * W_SD)) * b   # W = 均值 + 1SD
'

# ③ 运行（Bootstrap SE，建议 5000 次）
fit_modmed <- sem(model_modmed,
                  data = data,
                  se = "bootstrap",
                  bootstrap = 5000)

parameterEstimates(fit_modmed,
                   boot.ci.type = "bca.simple",
                   level = 0.95)
```

> ⚠️ **关于潜变量×潜变量交互**：若 X 和 W 均为多题项潜变量，lavaan 的乘积指标法（Product Indicator）技术上可行但繁琐；更推荐使用 Mplus 的 LMS 估计（读取 `references/step5-modmed-mplus.md`，若存在）或切换至 PLS-SEM 路径。

---

## 路径 B：PLS-SEM（SmartPLS）—— 推荐用于有调节的中介

### 为什么 PLS-SEM 更适合此类分析

SmartPLS 内置 Interaction Term 功能，直接支持潜变量×潜变量的调节，操作更简单，无需手动构建乘积指标。

### 操作步骤

**1. 建模阶段**
- 在模型中添加 X → M 的调节路径：选中 X 和 W，点击 **Interaction → Two-Stage**（推荐，优于产品指标法）
- 同时保留原有的 M → Y 路径和直接效应 X → Y

**2. 运行 Bootstrapping**
- 点击 **Calculate → Bootstrapping**
- 勾选 **Mediation**（若有此选项）
- 建议样本数：5000

**3. 查看结果**

在 Bootstrapping 结果中，重点关注：

| 需要的数据 | 位置 |
|-----------|------|
| 交互项（X×W → M）的路径系数、$t$ 值、$p$ 值 | Path Coefficients |
| **条件间接效应**（W 低/均/高时的间接效应及 CI） | Indirect Effects → Specific Indirect Effects |

> SmartPLS 5 及以上版本在 **Moderation Analysis** 选项卡中可直接输出条件间接效应，请使用该功能。

---

## 需要用户提供的结果

```
请把以下结果截图或复制给我：

1. 交互项（X×W）→ M 的路径系数：β = ?，t = ?，p = ?
2. M → Y 的路径系数：β = ?，t = ?，p = ?
3. 条件间接效应（W = 低/均/高）：
   - W 低（均值 - 1SD）：indirect effect = ?，95% CI [?, ?]
   - W 均值：indirect effect = ?，95% CI [?, ?]
   - W 高（均值 + 1SD）：indirect effect = ?，95% CI [?, ?]
```

---

## 判断标准

| 判断项 | 标准 | 结论 |
|--------|------|------|
| 交互项（a3）显著 | $p < .05$ | 调节效应存在，继续检验条件间接效应 |
| 交互项不显著 | $p ≥ .05$ | 调节效应不支持，有调节的中介整体不成立 |
| 某 W 水平下 95% CI **不含零** | — | 该水平下间接效应显著 |
| 某 W 水平下 95% CI **含零** | — | 该水平下间接效应不显著 |

> ✅ **完整的有调节的中介结论**：至少需要（1）交互项显著，且（2）条件间接效应在不同 W 水平下存在显著差异（即 CI 不含零的水平至少有一个）。

---

## 可视化：简单斜率 / 条件效应图

建议用户绘制条件间接效应图，展示间接效应随 W 变化的趋势：

```r
# R 中使用 mediation + ggplot2，或 processR 包
library(processR)
# processR 可以直接复现 Hayes PROCESS 的 Model 7/8/14/58
# 详见 processR 文档：https://github.com/cardiomoon/processR
```

---

## 报告撰写要点（第6步将自动纳入）

1. 先报告调节效应（交互项路径系数）是否显著
2. 再报告三个 W 水平下的条件间接效应值及 95% CI
3. 结论措辞示例：

> "Bootstrap 结果显示，X 对 Y 的间接效应（通过 M）受到 W 的显著调节（$\beta_{XW} = .XX$，$t = X.XX$，$p < .05$）。当 W 处于高水平时，间接效应显著（$\beta_{indirect} = .XX$，95% CI [.XX, .XX]）；当 W 处于低水平时，间接效应不显著（$\beta_{indirect} = .XX$，95% CI [−.XX, .XX]），支持有调节的中介假设。"

---

## 异常处理

| 情形 | 策略 |
|------|------|
| 交互项不显著，但间接效应在某水平下显著 | 整体调节效应仍不支持；间接效应的组间差异不能视为调节的证明 |
| 三个 W 水平下 CI 均不含零 | 间接效应存在，但不随 W 变化——属于简单中介，而非有调节的中介 |
| 样本量 < 200 | Bootstrap CI 稳定性下降，需在局限性中注明 |

---

完成后进入**第 6 步**。

---

> 📎 **异常情况参考**：交互项不显著、三水平 CI 均不含零、样本量不足等扩展处理策略 → 见 `error-handling.md` **§ 有调节的中介阶段**  
> 📎 **Mplus LMS 调节（潜变量×潜变量）** → 见 `references/step5-modmed-mplus.md`
