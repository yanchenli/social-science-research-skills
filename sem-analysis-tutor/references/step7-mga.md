# 多组分析（Multi-Group Analysis, MGA）

> 本文件在以下情形触发：  
> - 用户想比较不同群体（如男/女、高/低涉入、不同行业、不同品类）的路径系数是否存在显著差异  
> - 用户提到"性别是否调节主效应"、"跨文化比较"、"测量不变性"、"MGA"、"MICOM"  
>
> MGA 是一种**跨组调节检验**——它不需要调节变量进入模型，而是直接比较不同组的系数是否相等。

---

## 路径 A：CB-SEM 多组分析（lavaan）

CB-SEM 多组分析的核心逻辑是：通过**嵌套模型比较**，逐步检验各层次的测量不变性，再比较结构路径是否在组间相等。

### 三层次模型

| 模型 | 约束条件 | 检验内容 |
|------|---------|---------|
| **配置模型（Configural）** | 无约束，仅模式相同 | 两组是否有相同的因子结构 |
| **度量模型（Metric）** | 因子载荷相等 | 各题项对构念的权重是否跨组等同 |
| **标量模型（Scalar）** | 载荷 + 截距相等 | 量表的零点是否跨组等同（均值比较前提） |

> **最低要求**：比较路径系数时，至少需要**度量不变性**成立。标量不变性是均值比较（如 ANOVA）的前提，多数 SEM 跨组研究只要求度量不变性。

### 操作代码（lavaan）

```r
library(lavaan)
library(semTools)

# 定义测量模型（来自第3步）
model_cfa <- '
  构念A =~ A1 + A2 + A3
  构念B =~ B1 + B2 + B3
'

# ① 配置模型（最宽松，无跨组约束）
fit_config <- cfa(model_cfa,
                  data = data,
                  group = "group_var",       # 分组变量名（如 "gender"，编码为 1/2）
                  estimator = "MLR")

# ② 度量模型（因子载荷跨组等同）
fit_metric <- cfa(model_cfa,
                  data = data,
                  group = "group_var",
                  group.equal = "loadings",
                  estimator = "MLR")

# ③ 标量模型（载荷 + 截距跨组等同）
fit_scalar <- cfa(model_cfa,
                  data = data,
                  group = "group_var",
                  group.equal = c("loadings", "intercepts"),
                  estimator = "MLR")

# ④ 嵌套模型比较（Satorra-Bentler 校正卡方差检验）
compareFit(fit_config, fit_metric, fit_scalar)
```

### 判断标准

| 比较 | 关注指标 | 判断 |
|------|---------|------|
| Config vs Metric | $\Delta$CFI < .010 且 $\Delta$RMSEA < .015 | 度量不变性支持 |
| Metric vs Scalar | $\Delta$CFI < .010 且 $\Delta$RMSEA < .015 | 标量不变性支持 |

> 若 $\Delta$CFI ≥ .010，说明对应不变性不成立，需进行**部分不变性**检验（释放部分截距约束）。

### 检验结构路径是否跨组相等

```r
# 定义完整 SEM（测量+结构）
model_sem <- '
  构念A =~ A1 + A2 + A3
  构念B =~ B1 + B2 + B3
  构念B ~ 构念A
'

# 约束结构路径相等（零假设：两组路径系数相同）
fit_constrained <- sem(model_sem,
                       data = data,
                       group = "group_var",
                       group.equal = c("loadings", "regressions"))

# 释放结构路径（备择假设：路径系数可以不同）
fit_free <- sem(model_sem,
                data = data,
                group = "group_var",
                group.equal = "loadings")

# 比较两个模型
lavTestLRT(fit_constrained, fit_free)
```

- **$p < .05$**（卡方差检验显著）→ 两组路径系数存在显著差异 → 调节效应成立
- **$p ≥ .05$** → 路径系数跨组无显著差异 → 调节效应不成立

---

## 路径 B：PLS-SEM 多组分析（SmartPLS）

PLS-SEM 的 MGA 分两步：**先 MICOM，再 MGA**。

### 第一步：MICOM（测量不变性评估）

MICOM 检验三个层次：

| 层次 | 内容 | SmartPLS 输出 |
|------|------|-------------|
| 步骤1：配置不变性 | 模型设定相同 | 自动满足（若模型一致） |
| 步骤2：构念合成不变性 | 各组合成方式等同 | Permutation test，$p > .05$ = 不变性成立 |
| 步骤3：构念均值/方差不变性 | 均值和方差跨组等同 | Confidence interval 是否含零/一 |

**SmartPLS 操作**：
1. 点击 **Calculate → Measurement Invariance (MICOM)**
2. 选择分组变量
3. 建议置换次数：**5000**

### 第二步：MGA

**前提**：MICOM 步骤2（合成不变性）通过后，才能进行路径系数的跨组比较。

**SmartPLS 操作**：
1. 点击 **Calculate → Multi-Group Analysis**
2. 选择分组变量
3. 建议置换次数：**5000**

**输出解读**：

| 输出列 | 含义 |
|--------|------|
| 路径系数（组1/组2） | 各组的标准化路径系数 |
| 差异值 | 组1 − 组2 的差值 |
| $p$ 值（双尾） | 路径系数差异是否显著 |

- $p < .05$ → 两组路径系数存在显著差异 → 群组调节效应成立

---

## 结果汇总与报告框架

### CB-SEM 报告示例

> "为检验性别是否调节 X → Y 路径，本研究依次检验了配置不变性、度量不变性与标量不变性（Vandenberg & Lance, 2000）。嵌套模型比较结果显示，度量不变性成立（$\Delta$CFI = .003，$\Delta$RMSEA = .008），标量不变性亦成立（$\Delta$CFI = .005，$\Delta$RMSEA = .006）。随后对结构路径进行跨组约束检验，结果显示男女组的 X → Y 路径系数存在显著差异（$\Delta\chi^2$ = 8.34，$\Delta df$ = 1，$p$ = .004），支持性别的调节效应。男性组路径系数（$\beta$ = .42）显著高于女性组（$\beta$ = .18）。"

### PLS-SEM 报告示例

> "本研究首先采用 MICOM 程序检验测量不变性（Henseler et al., 2016）。结果显示，构念合成不变性成立（$p$ > .05）。随后进行 MGA（置换次数 = 5000），结果表明男女组的 X → Y 路径系数差异显著（$\beta_{男} = .45$，$\beta_{女} = .19$，差值 = .26，$p$ = .031），支持性别对该路径的调节作用。"

---

## 需要用户提供的结果

**CB-SEM 用户**
```
请提供以下结果：
1. 配置/度量/标量模型的 CFI、RMSEA 数值
2. 嵌套比较的 ΔCFI、ΔRMSEA（compareFit 输出）
3. 路径约束比较的卡方差检验结果（χ²差值、df、p 值）
4. 两组各自的标准化路径系数（β）
```

**PLS-SEM 用户**
```
请提供以下结果：
1. MICOM 步骤2：各构念的置换检验 p 值
2. MGA 输出：目标路径的两组系数、差值、p 值
```

---

## 常见异常处理

| 情形 | 策略 |
|------|------|
| 度量不变性不成立（CB-SEM）| 检查哪条载荷跨组差异大，进行**部分不变性**分析（释放该载荷约束），并在报告中如实说明 |
| MICOM 步骤2不通过（PLS-SEM）| 不应进行 MGA；建议报告测量不变性的限制，并在局限性中说明跨组比较的局限 |
| 样本量严重不均（如 80 vs 300）| MGA 统计检验力受影响，需在局限性中说明 |
| MGA $p$ 值在 .05–.10 之间 | 不显著，直接报告不支持；不得表述为"边缘显著" |

---

> 📎 **关键文献**：  
> - CB-SEM 测量不变性：Vandenberg & Lance (2000), *Organizational Research Methods*  
> - PLS-SEM MICOM：Henseler, Ringle & Sarstedt (2016), *MIS Quarterly*  
> 📎 **异常情况** → 见 `error-handling.md` **§ 多组分析阶段**
