# 第 5 步：中介 / 调节效应分析（如适用）

## ⚡ 快速路由：你的模型属于哪种？

| 情形 | 跳转 |
|------|------|
| 只有中介，没有调节 | 继续阅读本文件 §A |
| 只有调节，没有中介 | 继续阅读本文件 §B |
| **同时有中介和调节，且调节作用于中介链的某条路径** | 📄 读取 `references/step5-modmed.md` |
| 中介和调节相互独立（调节的是主效应，中介是另一条路径）| 先 §A，再 §B，独立报告 |

> ✅ 若用户不确定属于哪种情形，询问："W（调节变量）影响的是哪条箭头的强弱？"帮助判断后再确认路由。

---

## 触发条件

若第 0 步已确认模型包含中介或调节变量，本步骤自动衔接第 4 步；若无，跳过进入第 6 步。

---

## A. 中介效应分析

### 核心概念（向用户解释）

> "中介效应检验的是：X 对 Y 的影响，是否通过 M 这个'中间人'来传递。例如：社交媒体使用（X）通过提升品牌认知（M）来影响购买意愿（Y）。"

### CB-SEM 路径（lavaan indirect effect）

```r
model_mediation <- '
  # 测量模型（复制第3步验证通过的版本）
  X =~ X1 + X2 + X3
  M =~ M1 + M2 + M3
  Y =~ Y1 + Y2 + Y3

  # 路径（用字母标记用于定义间接效应）
  M ~ a * X          # X → M
  Y ~ b * M + c * X  # M → Y（b路径），X → Y 直接效应（c路径）

  # 定义间接效应和总效应
  indirect := a * b
  total    := c + a * b
'

fit_med <- sem(model_mediation,
               data = data,
               se = "bootstrap",
               bootstrap = 5000)

# 查看包含 Bootstrap CI 的结果
parameterEstimates(fit_med,
                   boot.ci.type = "bca.simple",
                   level = 0.95)
```

### PLS-SEM 路径（SmartPLS）

在 **Bootstrapping** 结果中，查看 **Specific Indirect Effects** 报告：
- 间接效应值（Indirect Effect）
- $t$ 值
- 95% Bootstrap CI（2.5% 和 97.5%）

### 中介效应判断标准

| 情形 | 结论 |
|------|------|
| 间接效应 95% CI **不含零** | 中介效应显著 |
| 间接效应 95% CI **含零** | 中介效应不显著 |
| 间接效应显著 + 直接效应（$c'$）不显著 | **完全中介** |
| 间接效应显著 + 直接效应（$c'$）也显著 | **部分中介** |

> ⚠️ **不要使用 Baron & Kenny 的"4步法"来判断中介**，现代方法只看 Bootstrap CI 是否含零。

---

## B. 调节效应分析

### 核心概念（向用户解释）

> "调节效应检验的是：W 会不会改变 X 对 Y 影响的强弱或方向？例如：社交媒体使用对购买意愿的影响，在高品牌认同的人群中是否更强？"

### CB-SEM 路径（lavaan 乘积项法）

对于**观测变量调节**（W 是单一变量而非潜变量）：

```r
# ① 先对 X 和 W 进行均值中心化（避免多重共线性）
data$X_c <- scale(data$X, center = TRUE, scale = FALSE)
data$W_c <- scale(data$W, center = TRUE, scale = FALSE)

# ② 创建交互项
data$XW <- data$X_c * data$W_c

# ③ 在结构模型中加入交互项
model_mod <- '
  Y ~ b1 * X_c + b2 * W_c + b3 * XW
'
fit_mod <- lm(Y ~ X_c + W_c + XW, data = data)
summary(fit_mod)
```

> ⚠️ **注意**：上述 `lm()` 代码仅适用于 **Y 是单一观测变量**（非潜变量）的情形。若 Y 是多题项潜变量，需在 lavaan 的结构模型中加入交互项，或切换至 PLS-SEM（SmartPLS 内置 Interaction Term 功能，对潜变量×潜变量调节更方便）。若 X 和 W **均为多题项潜变量**，强烈推荐使用 PLS-SEM 或 Mplus LMS 法；详见 `step5-modmed.md`。

对于**潜变量调节**（X 和 W 均为多题项构念），推荐使用：
- lavaan 的 **乘积指标法（Product Indicator）** 或
- 更精确的 **LMS 法**（需使用 Mplus）

### PLS-SEM 路径（SmartPLS）

1. 在模型中添加 X 和 W 之间的 **Interaction Term**（SmartPLS 内置功能）
2. 运行 **Bootstrapping**
3. 查看交互项 → Y 的路径系数是否显著

### 调节效应解读

| 情形 | 结论 |
|------|------|
| 交互项路径系数显著（$p < .05$） | 调节效应成立 |
| 系数为正 | W 越高，X → Y 的正向效应越强（正向调节） |
| 系数为负 | W 越高，X → Y 的正向效应越弱（负向调节） |

**显著后建议绘制简单斜率图**：
```r
# R 中使用 interactions 包
library(interactions)
interact_plot(fit_mod, pred = X_c, modx = W_c,
              modx.values = c(-1, 0, 1),  # 低/均值/高
              plot.points = FALSE)
```

---

## 需要用户提供的结果

**中介效应**：
- 间接效应值（$a \times b$）
- 95% Bootstrap CI 的下限和上限

**调节效应**：
- 交互项路径系数 $\beta$
- $t$ 值、$p$ 值
- （如有简单斜率图，描述图形走势）

---

## 等待与判断

收到结果后，帮助用户：
1. 判断中介效应是否显著，是完全/部分中介
2. 判断调节效应方向与含义
3. 记录对应假设的支持/不支持结论

完成后进入**第 6 步**。

---

> 📎 **异常情况参考**：间接效应 CI 含零、交互项不显著、$a$ 路径断裂等处理策略 → 见 `error-handling.md` **§ 中介 / 调节阶段**  
> 📎 **有调节的中介异常** → 见 `error-handling.md` **§ 有调节的中介阶段**
