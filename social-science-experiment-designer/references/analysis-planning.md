# 统计分析策略规划指南

本文件供第 6 步「功效分析与样本量规划」使用，与功效分析同步完成。

---

## 一、根据假设类型选择分析方法

| 假设类型 | 对应分析方法 | 推荐软件 |
|---------|------------|---------|
| 主效应（H1：X → Y） | 独立样本 t 检验 / 单因素 ANOVA | SPSS, R, JASP |
| 中介效应（H2：X → M → Y） | Bootstrap 中介检验（PROCESS） | PROCESS macro（R/SPSS）, lavaan |
| 调节效应（H3：X×W → Y） | 双因素 ANOVA / 回归交互项 | PROCESS, SPSS, R |
| 有调节的中介（H4） | Conditional process analysis | PROCESS macro |
| 概念性复制跨实验比较 | 元分析式效果量对比 | R (metafor) |

---

## 二、中介分析规范（X → M → Y）

### 推荐方法：Bootstrap 置信区间法

**为什么不用 Baron & Kenny (1986) 四步法**：
- 四步法要求主效应显著才能检验中介，但即使存在完全中介，直接效应也可能不显著
- Bootstrap 法直接检验间接效应（a×b），不依赖主效应是否显著
- Bootstrap 法在小样本下统计功效更高，是当前领域标准

**PROCESS macro 操作规范**（Hayes, 2022）：
```
Model 4 = 简单中介（X → M → Y）
Bootstrap 次数 = 5,000（最低要求，建议 10,000）
置信区间 = 95% BC（偏差校正）置信区间
报告格式：indirect effect = [点估计], 95% CI [下限, 上限]
若 CI 不包含 0，则中介效应显著
```

**报告模板**：
> 「Bootstrap 分析（5,000 次重复抽样）显示，[M] 的间接效应显著，
> indirect effect = X.XX, 95% BC CI [X.XX, X.XX]，
> 置信区间不包含 0，支持 [M] 的中介作用（H2）。」

**测量中介 vs. 操纵中介**：
- Study 1 中的测量中介提供相关证据（间接效应），但无法排除第三变量
- Study 2 中的操纵中介提供因果证据（参见 materials-design.md）
- 论文中两种证据应并列呈现，说明各自的逻辑贡献

---

## 三、调节分析规范（X×W → Y）

### ANOVA 交互效应

**适用条件**：自变量 X 和调节变量 W 均为分类变量（被试间因子设计）

**报告格式**：
> 「双因素 ANOVA 结果显示，X×W 的交互效应显著，F(1, N) = X.XX, p = .XXX, ηp² = .XX。
> 简单效应分析表明，在 W 高条件下，X 的效应显著 [报告细节]；
> 在 W 低条件下，X 的效应不显著 [报告细节]。」

**调节效应图**：必须呈现交互效应图（2×2 折线图），视觉化呈现效应模式

### 调节回归（Floodlight Analysis）

**适用条件**：调节变量 W 为连续变量

**推荐方法**：Johnson-Neyman 技术（PROCESS macro 自动生成）
- 输出「显著区间」：W 在哪个范围内 X 的效应显著
- 比「简单斜率分析」（仅看 ±1SD）提供更完整的信息
- **PROCESS 操作**：在 Model 1 中勾选「Johnson-Neyman」选项

**报告模板**：
> 「Johnson-Neyman 分析显示，当 W ≥ X.XX（样本第 XX 百分位数）时，
> X 对 Y 的效应显著为正；当 W ≤ X.XX 时，效应不显著。」

---

## 四、有调节的中介分析（Moderated Mediation）

**理论含义**：中介路径（a 路径、b 路径或整个间接效应）的强度受调节变量 W 的影响

**PROCESS Macro 模型选择**：

| 调节发生在哪条路径 | Hayes 模型编号 | 适用情景 |
|----------------|-------------|---------|
| W 调节 a 路径（X→M） | Model 7 | 「X 在什么条件下才会激活 M？」 |
| W 调节 b 路径（M→Y） | Model 14 | 「M 在什么条件下才会影响 Y？」 |
| W 同时调节 a、b 路径 | Model 58 | 两条路径都受调节 |
| W 调节直接效应 | Model 1 | 仅检验直接效应的调节 |

**核心检验指标**：条件间接效应（Conditional Indirect Effect）
```
检验 W 的不同水平下，间接效应（a×b）是否存在显著差异
报告：W 在低、均值、高（或 Johnson-Neyman 区间）条件下的间接效应及其 95% CI
若 CI 在不同 W 水平下从包含 0 变为不包含 0，说明有调节的中介成立
```

**Index of Moderated Mediation（IMM）**：
- Hayes（2015）提出的整合检验指标
- 若 IMM 的 95% CI 不包含 0，则整体有调节的中介效应显著
- 在论文中应同时报告 IMM 和各 W 水平下的条件间接效应

**报告模板**：
> 「为检验有调节的中介假设（H4），我们使用 PROCESS macro（Model X）进行 Bootstrap 分析
> （5,000 次重复抽样）。结果显示，调节中介指数（index of moderated mediation）显著，
> IMM = X.XX, 95% CI [X.XX, X.XX]，CI 不包含 0。
> 进一步的条件间接效应分析显示：在 W 低条件下，间接效应为 X.XX，
> 95% CI [X.XX, X.XX]；在 W 高条件下，间接效应为 X.XX，
> 95% CI [X.XX, X.XX]，仅后者的 CI 不包含 0，支持 H4。」

---

## 五、软件选择建议

| 软件 | 优势 | 局限 | 推荐用途 |
|-----|-----|-----|---------|
| **PROCESS macro（SPSS/R）** | 上手快，输出格式与论文报告接近 | 仅支持回归框架，不支持 SEM | 中介、调节、有调节的中介 |
| **SPSS** | 界面友好，普及度高 | 灵活性低，高级分析需 PROCESS | 描述统计、t 检验、ANOVA |
| **R（lavaan）** | 灵活，支持 SEM 和路径分析 | 学习曲线较陡 | 复杂模型、测量模型检验 |
| **JASP** | 界面友好，输出可直接用于论文 | 功能不如 R 全面 | 贝叶斯分析、频率主义基础分析 |
| **jamovi** | 免费，界面类似 SPSS，支持 PROCESS | 部分高级功能尚不完善 | 初学者的 SPSS 替代方案 |

**针对商科研究生的建议路径**：
- **起步**：SPSS + PROCESS macro（最快上手，论文报告格式成熟）
- **进阶**：R + lavaan（当涉及测量模型或复杂路径结构时）
- **Bayesian 补充**：JASP（当需要报告贝叶斯因子支持零假设时）

---

## 六、结果不支持假设时的分析处理流程

当主要结果不支持假设（效应方向相反或不显著），按以下顺序检查，**不得在未报告检查结果的情况下修改假设**：

**Step 1：操纵检查**
> 操纵是否成功？如未成功（高/低条件无显著差异），结果不支持假设属于方法问题，而非理论问题。

**Step 2：功效事后分析（Post-hoc Power Analysis）**
> 基于获得的效果量，当前样本量对应的统计功效是多少？
> 若功效 < 0.80，则结果不显著可能是第二类错误，而非假设错误。
> 使用 G*Power 或 R 的 `pwr` 包计算。

**Step 3：探索性分析（明确标注为探索性，不更改预注册假设）**
> 检查协变量模式，识别是否存在未预期的调节变量
> 在论文中明确区分验证性分析（预注册）和探索性分析

**Step 4：理论层面的讨论**
> 在 Discussion 中坦诚报告结果，讨论可能的理论解释：
> ① 机制路径与假设不一致（提示理论修正方向）
> ② 情景边界条件未被充分考虑（提示后续研究方向）

**不得做的事**（HARKing — Hypothesizing After Results are Known）：
- 将事后发现的显著结果改写为预先假设
- 删除不支持假设的数据以获得显著结果（p-hacking）
- 在未说明探索性质的情况下报告多次检验后偶然显著的分析

---

## 参考文献

Hayes, A. F. (2022). *Introduction to mediation, moderation, and conditional process analysis: A regression-based approach* (3rd ed.). Guilford Press.

Hayes, A. F. (2015). An index and test of linear moderated mediation. *Multivariate Behavioral Research*, *50*(1), 1–22.

Preacher, K. J., & Hayes, A. F. (2008). Asymptotic and resampling strategies for assessing and comparing indirect effects in multiple mediator models. *Behavior Research Methods*, *40*(3), 879–891.
