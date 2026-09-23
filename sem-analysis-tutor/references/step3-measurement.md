# 第 3 步：测量模型评估（外模型 / CFA）

## 目标

验证量表题项是否真的在测你想测的东西（信度与效度）。**这是 SEM 分析的基石——测量模型不合格，结构模型的结果就没有意义。**

---

## 向用户解释本步骤目的

> "我们现在要检验你的量表是否可靠（信度）和有效（效度）。简单来说，就是确认每道题确实在测它应该测的那个构念，而且不同构念之间能被区分开来。"

---

## CB-SEM 路径（lavaan / AMOS）

### 运行代码（lavaan 示例）

```r
library(lavaan)
library(semTools)

# ① 定义测量模型（CFA）
# 将下方构念名称和题项替换为你的实际变量名
model_cfa <- '
  构念A =~ A1 + A2 + A3
  构念B =~ B1 + B2 + B3
  构念C =~ C1 + C2 + C3
'

# ② 运行 CFA
fit_cfa <- cfa(model_cfa,
               data = data,
               estimator = "MLR")   # 若数据正态可改为 "ML"

# ③ 查看结果
summary(fit_cfa, fit.measures = TRUE, standardized = TRUE)

# ④ 提取信度与效度指标
reliability(fit_cfa)     # Cronbach's α, CR, AVE

# ⑤ 区分效度：HTMT
library(semTools)
htmt(model_cfa, data = data)
```

### CB-SEM 测量模型指标清单

请用户提供以下所有数值：

**模型整体拟合**
| 指标 | 可接受标准 | 良好标准 |
|------|-----------|---------|
| $\chi^2/df$ | < 3.0 | < 2.0 |
| CFI | ≥ .90 | ≥ .95 |
| TLI | ≥ .90 | ≥ .95 |
| RMSEA | < .08 | < .05 |
| SRMR | < .08 | < .05 |

**各构念指标**
| 指标 | 可接受标准 | 说明 |
|------|-----------|------|
| 标准化因子载荷 | ≥ .50（理想 ≥ .70） | 每道题的值 |
| Cronbach's $\alpha$ | ≥ .70 | 内部一致性信度 |
| 组合信度（CR） | ≥ .70 | 比 α 更推荐 |
| AVE | ≥ .50 | 收敛效度 |
| HTMT | < .90（严格 < .85） | 区分效度 |

---

## PLS-SEM 路径（SmartPLS / seminr）

### SmartPLS 操作步骤

1. 建好模型后，点击 **Calculate → PLS Algorithm**
2. 运行完成后，查看以下报告页面：
   - **Outer Loadings**（外部载荷）
   - **Construct Reliability and Validity**（包含 CR、AVE、$\rho_A$）
   - **Discriminant Validity → HTMT**

### PLS-SEM 测量模型指标清单

请用户提供以下所有数值：

| 指标 | 可接受标准 | 说明 |
|------|-----------|------|
| 外部载荷（Outer Loading） | ≥ .60（理想 ≥ .70） | 每道题的值 |
| 组合信度（CR / $\rho_c$） | ≥ .70 | 内部一致性 |
| $\rho_A$（rho_A） | ≥ .70 | PLS 特有信度指标 |
| AVE | ≥ .50 | 收敛效度 |
| HTMT | < .90（严格 < .85） | 区分效度 |

> ⚠️ **PLS-SEM 不使用 CFI/RMSEA 等整体拟合指标**，不要混用 CB-SEM 的拟合标准。

---

## 诊断与删题建议

收到用户结果后，逐项检查：

| 情形 | 建议 |
|------|------|
| 因子载荷 < .40 | 强烈建议删除该题项 |
| .40 ≤ 因子载荷 < .60 | 评估删题后 AVE/CR 变化，再决定是否删除 |
| 删题后 AVE 仍 < .50 | 与用户讨论量表来源，考虑重新审视构念定义 |
| HTMT ≥ .90（两个构念之间） | 两个构念可能存在区分效度问题，讨论是否合并或修改 |
| CFA 拟合较差（如 RMSEA > .10） | 检查修正指数（Modification Indices），考虑增加误差相关或修改模型设定 |

> 删题后需**重新运行测量模型**并再次提交结果，直至所有指标达标。

---

> ⚠️ **关于 Fornell-Larcker 准则**：不应作为区分效度的主要证据（Henseler et al., 2015），请使用 **HTMT 作为首选**。Fornell-Larcker 仅可在报告中作为补充参考，且务必同步报告 HTMT。

---

## 等待与判断

- ✅ 所有指标达标（或已充分讨论未达标原因）→ 进入**第 4 步**
- ⚠️ 有低于阈值的指标 → 讨论删题/修模方案 → 重跑 → 再次提交

---

> 📎 **异常情况参考**：CFA 拟合差、载荷偏低、HTMT 超标等详细处理策略 → 见 `error-handling.md` **§ 测量模型阶段**
