# Mplus LMS 法：潜变量×潜变量调节（高阶交互）

> 本文件在以下情形触发：  
> - X 和 W **均为多题项潜变量**，且需要检验 X×W 的交互效应  
> - 用户使用 Mplus，或 lavaan/SmartPLS 的乘积指标法不适用  
>
> 若只有一个是潜变量，或使用 SmartPLS 的 Two-Stage 法，回到 `step5-modmed.md`。

---

## 为什么需要 Mplus LMS

当 X 和 W **都是潜变量**时（即各由多道题项构成），常规的乘积项（X_score × W_score）会引入大量测量误差，导致调节效应估计有偏。

**LMS 法（Latent Moderated Structural Equations）**由 Klein & Moosbrugger (2000) 提出，是目前估计潜变量×潜变量调节效应最为严谨的方法，也是顶级期刊（JMR、AMJ、JCR）最认可的方案。

---

## Mplus 安装与版本要求

- Mplus 版本 6.0 及以上均支持 LMS
- 学生版（Student Edition）支持最多 6 个因变量，通常满足 SEM 需求
- 若无 Mplus，可考虑：（a）切换至 SmartPLS Two-Stage 法，（b）使用 R 包 `modsem`（见本文末尾）

---

## Mplus LMS 代码框架

以下为标准有调节的中介模型（W 调节 X→M 前半段）：

```mplus
TITLE: Moderated Mediation with LMS (W moderates X -> M path)

DATA:
  FILE = "your_data.dat";       ! 数据文件（.dat 格式，无表头，空格分隔）

VARIABLE:
  NAMES = X1 X2 X3              ! 自变量题项
          M1 M2 M3              ! 中介变量题项
          Y1 Y2 Y3              ! 因变量题项
          W1 W2 W3;             ! 调节变量题项
  USEVARIABLES = X1-X3 M1-M3 Y1-Y3 W1-W3;
  MISSING = .;                  ! 缺失值标记

DEFINE:
  ! 均值中心化（建议，降低多重共线性）
  CENTER X1 X2 X3 W1 W2 W3 (GRANDMEAN);

ANALYSIS:
  TYPE = RANDOM;                ! LMS 法必须使用 TYPE = RANDOM
  ALGORITHM = INTEGRATION;     ! 数值积分
  INTEGRATION = 15;            ! 积分点数，通常 15 足够；复杂模型可提高至 20

MODEL:
  ! 测量模型
  X BY X1* X2 X3;
  X@1;                         ! 固定方差为1（标准化）
  M BY M1* M2 M3;
  M@1;
  Y BY Y1* Y2 Y3;
  Y@1;
  W BY W1* W2 W3;
  W@1;

  ! 定义潜变量交互项（LMS 核心语句）
  XW | X XWITH W;

  ! 结构路径
  M ON X (a1)                  ! a1：X → M 主效应
         W (a2)                ! a2：W → M 主效应
         XW (a3);              ! a3：X×W → M（调节效应）
  Y ON M (b)                   ! b：M → Y
         X (c);                ! c：X → Y 直接效应

MODEL CONSTRAINT:
  ! 定义条件间接效应（需提前计算 W 的 SD，填入下方）
  NEW(ind_low ind_mean ind_high W_SD);
  W_SD = 1.0;                  ! <<< 替换为实际 W 的标准差（从数据中提取）
  ind_low  = (a1 + a3 * (-W_SD)) * b;
  ind_mean = a1 * b;
  ind_high = (a1 + a3 * (W_SD)) * b;

OUTPUT:
  TECH1 TECH8;                 ! 诊断输出
  CINTERVAL(BCBOOTSTRAP);      ! Bootstrap CI（需在 ANALYSIS 中加 BOOTSTRAP = 5000）
```

> ⚠️ **注意**：LMS 法本身使用数值积分而非 Bootstrap，输出的是基于 Delta 法的 SE 和 CI。若要获得 Bootstrap CI，需将 `ANALYSIS` 中加入 `BOOTSTRAP = 5000;` 并将 `ALGORITHM = INTEGRATION` 改为 `ALGORITHM = INTEGRATION BOOTSTRAP;`（Mplus 8.x 支持）。

---

## 关键输出说明

运行完成后，在 OUTPUT 中重点查找：

| 输出项 | 含义 | 位置 |
|--------|------|------|
| `XW ON M`（即 a3） | 调节效应（X×W → M）| MODEL RESULTS |
| `ind_low / ind_mean / ind_high` | 三个 W 水平下的条件间接效应 | MODEL CONSTRAINT 部分 |
| 各条件间接效应的 SE 和 p 值 | 推断显著性 | MODEL CONSTRAINT 部分 |
| LL / BIC | 模型整体拟合（LMS 不输出 CFI/RMSEA）| SUMMARY OF ANALYSIS |

---

## 结果解读

**第一步：看 a3（交互项）是否显著**
- $p < .05$ → 调节效应存在，继续看条件间接效应
- $p ≥ .05$ → 有调节的中介整体不成立

**第二步：看三个 W 水平下的条件间接效应**
- 95% CI 不含零 → 该水平下间接效应显著
- 至少一个水平显著、另一个不显著 → 有调节的中介成立

---

## 数据格式转换（.dat 文件）

Mplus 需要纯数值 `.dat` 文件（无表头，空格分隔，缺失值用 `.` 表示）。

```r
# 在 R 中导出 Mplus 格式数据
library(MplusAutomation)
prepareMplusData(data[, c("X1","X2","X3","M1","M2","M3",
                           "Y1","Y2","Y3","W1","W2","W3")],
                filename = "your_data.dat")
```

---

## 替代方案：R 包 `modsem`（无需 Mplus）

若用户没有 Mplus，R 包 `modsem` 可以在 lavaan 框架内实现多种潜变量调节估计方法（包括 LMS 近似）：

```r
# 安装
install.packages("modsem")
library(modsem)

model_lms <- '
  X =~ X1 + X2 + X3
  W =~ W1 + W2 + W3
  M =~ M1 + M2 + M3
  Y =~ Y1 + Y2 + Y3

  M ~ X + W + X:W
  Y ~ M + X
'

fit_lms <- modsem(model_lms, data = data, method = "lms")
summary(fit_lms)
```

> `modsem` 的 LMS 实现与 Mplus 高度一致，可作为论文的主要分析工具，并在方法部分注明使用了 Klein & Moosbrugger (2000) 的 LMS 估计方法（通过 `modsem` 包实现）。

---

> 📎 **报告撰写**：完成后进入第 6 步，Mplus LMS 结果的报告格式与 `step5-modmed.md` 中的模板一致，将 Bootstrap 字样改为"LMS 估计"即可。  
> 📎 **异常情况** → 见 `error-handling.md` **§ 有调节的中介阶段**
