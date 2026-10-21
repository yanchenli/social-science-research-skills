# research-data-preparation

> 研究数据准备与分析前决策管理 —— 在看到结果数据之前，把会影响结论的决定写下来。

**版本**：1.0.0 ｜ **适用**：商科 MS/PhD/DBA 学生及教师 ｜ **规模**：SKILL.md + 10 个 references + 6 个脚本 + 1 个工作簿模板

**中文** | [English](README.en.md)

---

## 它解决什么问题

多数方法学训练从「怎么分析」开始，跳过了更前面的一步：**研究者可以在多大程度上，
根据已经看到的数据，灵活调整研究设计与分析决策？**

一手数据的风险是事后挑排除规则和检验。二手数据的风险更隐蔽——数据早就在那里，
时间窗口、样本限制、阈值，都可能在看过结果之后才「调整」。

这个技能做的不只是一份计划书，而是四件事：

1. **数据接触审计** —— 研究者已经看过数据的哪一部分（E0–E4）
2. **决策状态管理** —— 每个关键决定是事前锁定、接触后锁定、数据驱动，还是尚未确定
3. **准备状态判断** —— 研究是否可以进入数据获取（不是给数据评「好坏」）
4. **可交接的规格** —— 工作簿 + 机器可读规格，下游技能与其他 agent 可直接读

---

## 核心理念

**在看到结果数据之前，把会影响结论的决定写下来；之后的调整不禁止，但要有记录。**

> 它**不做**的事：重新设计实验、功效分析、统计分析、真的发问卷或抓数据、
> 未经授权访问数据、作出法律与伦理结论（这些只识别并标注「需人工核验」）。

---

## 工作流程（七阶段）

| 阶段 | 内容 |
|---|---|
| 0. 研究问题与数据路径诊断 | 先问：**现有数据能不能回答研究问题？** 不要默认必须收集新数据 |
| 1. 数据来源、可行性与接触审计 | E0–E4 定级；来源可行性三层核实；有限数据剖面 |
| 2. 共同研究设计与分析前决策 | 样本规则、变量字典、分析计划 |
| 3. 按数据路径执行准备 | 一手量化 / 一手质性 / 二手结构化（条件分支） |
| 4. 伦理、数据治理与质量保障 | DMP、个人信息、授权与合规 |
| 5. 冻结、版本化与风险登记 | 锁定规格版本，登记已知风险 |
| 6. 交接与验收 | 工作簿 + `research_data_spec.json` 交给下游 |

### 阶段 0 的一个反直觉提醒

先问一个比「怎么收集」更前面的问题：**现有数据能不能回答研究问题？**
需要补充什么？获取成本与障碍是什么？

不要默认必须收集新数据——这是学生最容易跳过、代价最高的一步。

### 阶段 1：接触等级 E0–E4

**这一步在碰数据之前做。** 问清楚研究者接触过什么、看过什么、检验过什么，归入等级。

---

## 六个脚本

| 脚本 | 作用 |
|---|---|
| `profile_dataset.py` | 只读数据剖面：缺失率、分位数、分类水平计数、风险线索 |
| `mde_fixed_sample.py` | 固定样本下的最小可检测效应（two-group / correlation / anova） |
| `validate_spec.py` | 按 JSON Schema 校验规格，逐条报错 |
| `make_workbook.py` | 生成 9 页数据工作簿（`.xlsx`） |
| `workbook_to_spec.py` | 工作簿 → 机器可读规格（`research_data_spec.json`） |
| `common.py` | 数据读取与公共函数 |

### 一个必须提前说的设计

> ⚠️ **运行剖面脚本本身就是一次数据接触。**

脚本要求先声明当前等级，运行后自动升级并写入 `exposure_log.jsonl`。
要盲化结果变量，**必须在运行前**用 `--outcome-vars` 指定——运行之后再「盲化」已经晚了。
所以技能要求在运行前先告诉研究者这一点。

---

## 轻量模式

小型学生项目、路径单一，可以只走**阶段 0、2、5**，工作簿只填三页：
说明、Variable Dictionary、Decision & Deviation Log。

涉及二手数据、个人信息、多数据源或需要对外登记时，用完整模式。

---

## 工作簿的九个页面

```
说明 | Construct Map | Variable Dictionary | Sample & Rules | Data Acquisition
Analysis Plan | Ethics & DMP | Decision & Deviation Log | Handoff & QA
```

工作簿是给人填的，`workbook_to_spec.py` 把它转成机器可读的 `research_data_spec.json`，
下游的 [`quant-data-analysis`](../quant-data-analysis/) 会先读这份规格再开始分析——
**这就是「交接」的具体形式**。

---

## 使用示例

```
我想用某电商平台的交易记录做研究，数据已经拿到了，但还没开始分析。
```

技能会先做接触审计（你已经看过哪些字段？看过分布吗？），
再用 `profile_dataset.py` 在**盲化结果变量**的前提下做结构级剖面，
给出可行性判断与风险登记，最后产出数据计划与规格。

**它不会替你决定这份数据能不能用**——只提供可复核的证据，供你填写 `evidence_status`。

---

## 目录结构

```
research-data-preparation/
├── SKILL.md                                七阶段流程、轻量模式、脚本用法
├── references/
│   ├── core-plan-and-decisions.md          数据路径与研究目的、E0–E4 接触等级、决策状态
│   ├── primary-quantitative.md             一手量化：问卷/实验的搭建规格
│   ├── primary-qualitative.md              一手质性：访谈后勤、记录与治理
│   ├── secondary-structured.md             二手结构化数据：来源核实、时间窗口、样本限制
│   ├── governance-and-dmp.md               伦理、数据治理、DMP
│   ├── handoff-and-schema.md               交接格式与 schema 说明
│   ├── research_data_spec.schema.json      机器可读规格的 JSON Schema
│   └── examples/                           三份示例规格（一手量化/一手质性/二手结构化）
├── scripts/                                六个脚本（见上表）
└── templates/
    └── data_workbook_blank.xlsx            空白数据工作簿（9 页）
```

---

## 边界与注意事项

- **不重新设计实验。** 转 [`social-science-experiment-designer`](../social-science-experiment-designer/)。
- **不做统计分析。** 转 [`quant-data-analysis`](../quant-data-analysis/) 或
  [`sem-analysis-tutor`](../sem-analysis-tutor/)。
- **不替研究者作法律或伦理结论。** 只识别并标注「需人工核验」。
- **不给数据评「好坏」。** 它提供可复核的证据，判断由研究者与委员会做。
- **不访问未经授权的数据。** 也不替你发问卷或抓数据。

---

## 与相邻技能的分工

- **还没确定设计** → [`social-science-experiment-designer`](../social-science-experiment-designer/)。
- **设计定了、数据到手、要开始分析** → [`quant-data-analysis`](../quant-data-analysis/)。
  它会读本技能产出的 `research_data_spec.json`，避免重复提问。
- **质性资料收集的后勤** → 本技能的 `primary-qualitative.md` 与
  [`qualitative-research-methods`](../qualitative-research-methods/) 阶段 2 互补。

---

## 版本

**1.0.0** —— 七阶段流程、E0–E4 接触审计、决策状态管理、六个脚本、9 页工作簿与机器可读规格。
