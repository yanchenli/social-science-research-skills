---
name: "research-data-preparation"
description: "帮助研究者在获取数据、动手分析之前，把会影响结论的决定先理清并留痕：覆盖一手数据 （问卷、实验、访谈）与二手数据（交易记录、数据库、公开统计）的准备，产出带数据接触 等级与决策状态的研究数据计划、数据工作簿、机器可读规格（可供其他agent读取）和风险 记录。含只读的数据剖面脚本（可盲化结果变量并记录接触）、固定样本的最小可检测效应 脚本、规格校验脚本。不重新设计实验（转social-science-experiment-designer），不做统计 分析（转quant-data-analysis），不替研究者作法律或伦理结论。\n触发场景（满足以下任一条件即应使用本skill）： - 用户问\"收集数据前要准备什么\"\"这个数据能不能用\"\"二手数据怎么准备\"\"怎么预注册既有数据\" - 用户提到\"数据获取\"\"数据计划\"\"变量字典\"\"编码表\"\"数据接触\"\"分析自由度\"\"时间窗口\"\n  \"样本选择\"\"数据来源是否可靠\"\"DMP\"\"数据管理计划\"\n- 用户有一份数据（交易记录、平台数据、公开数据集）想在分析前先评估可行性 - 用户要把实验设计转成问卷或平台的搭建规格，或准备访谈的后勤与记录\n即使用户只是说\"我想用这份数据做研究，不知道从哪开始\"，也应触发本skill。\n"
version: 1.0.0
license: CC-BY-4.0
---

# 研究数据准备与分析前决策管理

## 核心理念

**在看到结果数据之前，把会影响结论的决定写下来；之后的调整不禁止，但要有记录。**

研究者真正要管理的问题是：研究者可以在多大程度上根据已经看到的数据，灵活调整研究设计与分析决策？一手数据的风险是事后挑排除规则和检验；二手数据的风险更隐蔽，因为数据早就在那里，时间窗口、样本限制、阈值，都可能在看过结果之后才"调整"。所以这个skill做的不只是一份计划书，而是四件事：

1. **数据接触审计**：研究者已经看过数据的哪一部分（E0–E4）
2. **决策状态管理**：每个关键决定是事前锁定、接触后锁定、数据驱动，还是尚未确定
3. **准备状态判断**：研究是否可以进入数据获取（不是给数据评"好坏"）
4. **可交接的规格**：工作簿＋机器可读规格，下游skill和其他agent可以直接读

> 它**不做**的事：重新设计实验（`social-science-experiment-designer`）、功效分析、统计分析（`quant-data-analysis`、`sem-analysis-tutor`）、真的发问卷或抓数据、未经授权访问数据、作出法律与伦理结论（这些只识别并标注"需人工核验"）。

## 快速入口

| 你的情况 | 怎么走 |
|---|---|
| 刚有想法，还不知道要不要收集数据 | **阶段0** |
| 手上有一份数据，想先评估能不能用 | **阶段1**（先问接触等级，再用剖面脚本） |
| 要准备问卷/实验的搭建规格 | **阶段2** → 阶段3读`primary-quantitative.md` |
| 要准备访谈或观察 | **阶段2** → 阶段3读`primary-qualitative.md` |
| 要给既有数据写分析前计划或预注册 | **阶段1、2、5**，读`secondary-structured.md` |
| 计划已写好，要交给分析或其他agent | **阶段6** |
| 小型学生项目、路径单一 | **轻量模式**：阶段0、2、5（见下） |

**轻量模式**：只走阶段0、2、5，工作簿只填"说明"、"Variable Dictionary"、"Decision & Deviation Log"三页。涉及二手数据、个人信息、多数据源或需要对外登记时，用完整模式。

---

## 阶段0 — 研究问题与数据路径诊断

澄清：研究问题、目标人群、核心构念、研究目的。然后分两个维度判断（详见`references/core-plan-and-decisions.md`第1节）：

- **数据路径**：一手量化／一手质性／二手结构化／二手文本与数字痕迹／混合
- **研究目的**：确认性／预测／探索性／测量开发／描述／理论建构／混合

先问一个比"怎么收集"更前面的问题：**现有数据能不能回答研究问题？** 需要补充什么？获取成本与障碍是什么？不要默认必须收集新数据。

## 阶段1 — 数据来源、可行性与接触审计

1. **数据接触审计**（所有路径都要做）：问清楚研究者接触过什么、看过什么、检验过什么，归入E0–E4（`core-plan-and-decisions.md`第2节）。**这一步在碰数据之前做。**
2. **来源与获取可行性**：对每个拟用来源现场联网核实官方入口，填证据卡，区分"产品存在／当前账户有访问权限／支持本研究"三层（`secondary-structured.md`第1、8节）
3. **有限的数据剖面**（有数据文件时）：

```
python scripts/profile_dataset.py --file sample.csv --current-exposure E1 \
       --id 用户ID --time 日期 --outcome-vars 结果变量 --level structure
```

⚠️ **运行剖面本身就是一次数据接触。** 脚本要求先声明当前等级，运行后自动升级并写入`exposure_log.jsonl`；要盲化结果变量，必须**在运行前**用`--outcome-vars`指定。运行前先告诉研究者这一点。

## 阶段2 — 共同研究设计与分析前决策

对照`core-plan-and-decisions.md`，写出并给每项标`decision_status`：研究问题与假设、目标估计量（确认性解释研究用大白话写）、构念—测量—字段映射、分析单位、抽样框架、样本规则、主要结果与分析策略、缺失/离群值/多重检验预案。**哪些必须事前锁定，哪些保留灵活性**，由阶段0的研究目的决定。

## 阶段3 — 按数据路径执行准备（条件分支）

| 路径 | 读哪个文件 |
|---|---|
| 一手量化 | `references/primary-quantitative.md`（搭建规格、预试边界、停止规则、上线验收） |
| 一手质性 | `references/primary-qualitative.md`（可追溯记录、信息力、转录与翻译） |
| 二手结构化 | `references/secondary-structured.md`（构念效度、数据生成机制、窗口、机械关系、合并粒度） |
| 二手文本与数字痕迹 | `secondary-structured.md`第11节简要检查（完整模块第二版） |
| 混合 | 各自分支＋在阶段2写明整合逻辑与先后顺序（完整模块第二版） |

二手数据的"留出验证样本"只是三种手段之一（盲化、留出、披露），**不是默认要求**，按研究目的选（`core-plan-and-decisions.md`第7节）。

固定样本的灵敏度：`python scripts/mde_fixed_sample.py two-group --n1 300 --n2 280`——这是"能检出多大效应"，不是事后功效；设计阶段的功效计算归`social-science-experiment-designer`。

## 阶段4 — 伦理、数据治理与质量保障

读`references/governance-and-dmp.md`，对八个主题记录当前答案。**所有分支都要做。** 涉及个人信息、跨境、平台规则、数据使用条款、第三方服务的事项，一律写入`items_needing_human_verification`，不自行裁决。

## 阶段5 — 冻结、版本化与风险登记

形成带日期、版本和接触声明的**基线计划**。之后的调整只在决策日志里**追加**一行（日期、原方案、新方案、原因、调整时的接触等级），不覆盖旧行。同时登记风险：最可能出问题的几处与应对。需要对外登记时，把接触等级翻译成对方表单的表述。

## 阶段6 — 交接与验收

```
python scripts/make_workbook.py --out data_workbook.xlsx
# 研究者在工作簿里填写
python scripts/workbook_to_spec.py data_workbook.xlsx --out research_data_spec.json
python scripts/validate_spec.py research_data_spec.json
```

校验的**错误必须改**，**警告必须处理或说明**（例如E4下仍标`pre_locked`、确认性主要分析标成`data_driven`、排除规则在看结果之后才定）。交接契约和其他agent的读取规则见`references/handoff-and-schema.md`。

交付前对照该文件第6节的验收清单自检；交给下游时说明：**哪些信息已验证，哪些仍是研究者陈述或待核实。**

---

## 输出

| 产物 | 说明 |
|---|---|
| 研究数据计划（.docx或.md） | 用所在环境提供的文档生成能力（如 `python-docx` 库或 `pandoc` 转换；若环境中已有专门的 docx 技能，优先使用它）生成；含数据路径、研究目的、接触声明、决策状态、实施计划、治理、风险 |
| `data_workbook.xlsx` | 研究者唯一手工编辑的地方（`templates/data_workbook_blank.xlsx`为空白模板） |
| `research_data_spec.json` | 由工作簿生成，供下游skill与其他agent读取；字段定义见`references/research_data_spec.schema.json` |
| 剖面输出 | `profile_report.md`、`profile_summary.json`、`exposure_log.jsonl`（用过脚本时） |

## 参考文件

- `references/core-plan-and-decisions.md`：两个维度、接触审计、决策与证据状态、冻结基线、估计目标、三种手段、准备状态
- `references/primary-quantitative.md`、`primary-qualitative.md`、`secondary-structured.md`：三个分支
- `references/governance-and-dmp.md`：共用的伦理与数据管理计划
- `references/handoff-and-schema.md`：交接包、读取规则、下游契约、验收清单
- `references/research_data_spec.schema.json`、`references/examples/`：规格的JSON Schema和三个示例（一手量化、一手质性、二手结构化）

## 重要原则

1. **接触要先于剖面声明**：不先问接触等级就不跑剖面；要盲化的变量必须在运行前指定
2. **计划先于结果，但不要求研究过程僵化**：确认性研究严格锁定，探索性与质性研究记录初始设计与调整，不禁止调整
3. **冻结的是决策依据，不是研究者的思考**：每个决定保存时间、依据、状态、变更记录
4. **准备状态不是数据质量评级**：脚本和检查表只给证据与线索，不说数据"好"或"坏"
5. **不替人裁决合规**：法律、伦理、使用条款只识别并标注需人工核验
6. **证据状态必须诚实**：没核实的写`needs_verification`，不要因为计划写得完整就标成已验证
7. **来源信息现场核实**：不从记忆里写数据产品的内容；查不到就写"未核实"
