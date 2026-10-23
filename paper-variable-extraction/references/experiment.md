# 分支 B · 实验设计法 / Experimental Design

适用于含随机分配、情境/材料操纵、实验组与控制组的文章（实验室实验、田野实验、情景实验、在线实验等）。

## 0. 刺激材料清单 / Stimuli Inventory（最高优先级）

研究者最常复用的就是材料本身，必须**单独成表、粒度到具体内容**。每个研究先给一张刺激材料表，再讲变量。

| 字段 | 说明 |
|---|---|
| **材料集合** | 该材料属于哪个操纵/任务（如「暴露操纵-品牌条件」「选择任务-礼物选项」） |
| **材料类型** | 文本 Text / 情境故事 Vignette / 图片 Image / 品牌标识 Logo / 视频 Video / 实体环境 Environment / 真实产品 Product / 任务 Task / 音频 Audio |
| **原文内容** | **逐字摘录**（vignette 摘录关键段落、指令语、提示语、选项名称清单），长材料摘录核心段并注明"节选" |
| **中文对照** | 原文对应的中文翻译 |
| **数量** | 如 14 个 logo、30 个刺激物、6 个选项 |
| **呈现方式** | 同时呈现 Simultaneous / 顺序呈现 Sequential；呈现位置（如"贴在隔间墙上"） |
| **时长 / 试次** | 呈现时长、试次数、是否限时 |
| **预测试** | 是否做过 pretest / pilot，结果与目的 |
| **来源** | 作者自制 / 改编自 XX (年份) / 真实素材（如真实品牌 logo、Google Maps 实景） |

**必须逐字提取的材料类别**（遇到就照抄原文）：
- 情境故事（vignette、scenario）的关键段落
- 参与者看到的**指令语 / 提示语**（如 "Important: When you are ready to start making a decision, please press the next button."）
- 操纵材料中出现的**具体词语清单**（词语启动范式中的词表）
- 选择集的具体选项（产品名、属性、价格）
- 封面故事（cover story）原文
- 实验材料所在的附录编号（Appendix A / web appendix C 等），便于读者回查

## 0.5 设计类型 / Design Type（先记，再讲变量）

多实验论文常见「实验 1 建立效应 → 实验 2 操纵中介 → 实验 3 阻断效应」，设计类型不同，能推出的因果结论也不同。**每个实验先标设计类型**，再进刺激材料表。

| 类型 | 含义 | 典型表述关键词 |
|---|---|---|
| `Between-subjects` | 组间设计 | "randomly assigned to conditions" |
| `Within-subjects` | 组内设计 | "all participants completed both" |
| `Factorial` | 析因设计，注明阶数（2×2、2×3） | "2 (X: high vs. low) × 2 (Y: ...)" |
| `Double randomization` | 双随机化：研究 A 随机化 X 后测 M 与 Y，研究 B 固定 X 后随机化 M | Pirlott & MacKinnon (2016) |
| `Experimental-causal-chain` | 实验因果链：一串实验分别建立 X→Y、X→M、M→Y | Spencer, Zanna, & Fong (2005) |
| `Moderation-of-process` | 以过程为调节：操纵中介来阻断 X→Y | Vancouver & Carlson (2015) |
| `Blocking design` | 阻断设计：设置条件系统性阻断某机制，看效应是否消失 | "designed to permit or block the influence of X" |
| `Field experiment` | 田野实验 | 真实组织 / 实地场景 |

**阻断设计（blocking）要额外记录**：
- 阻断的是哪个机制（Mediator）
- 每个阻断条件对应的干预内容（见刺激材料表）
- 判定标准：阻断条件下效应是否「与零无显著差异」（常用 95% CI 是否跨 0）
- 控制条件的设定（是"允许效应发生"而非"什么都不做"时，要写清控制条件的内容）

## 1. 提取范围

**自变量 IV → 因变量 DV → 中介变量 Mediator → 调节变量 Moderator → 控制变量 Control → 操纵检验 Manipulation Check**

多实验文章（Experiment 1/2/3 或 Study 1/2）按实验分节，每个实验独立给出：刺激材料清单 → 变量 → 操纵检验 → 假设与结果。

## 自变量（IV）的字段清单

- **变量名称 / 变量名称（EN）** + 角色标注
- **概念性定义 / Conceptual Definition**：理论定义（原文 + 中文翻译）
- **操纵细节 / Manipulation Details**
  - **实验条件 / Experimental Conditions**：各组名称与含义，如「High-power condition vs. Low-power condition / 高权力感组 vs. 低权力感组」；注明是组间（between-subjects）还是组内（within-subjects）设计，以及组数（2×2 等）
  - **操纵材料 / Manipulation Materials**：材料的完整描述与关键原文措辞，如「参与者阅读两段情景短文之一」「同谋者按既定脚本互动」「观看一段 3 分钟视频」。关键文本（vignette 原文）应逐字摘录核心段落
  - **流程 / Procedure**：步骤化的操作顺序（编号列表），含时间、顺序、干扰任务、随机化方式
  - **操纵强度/剂量**：若涉及程度差异（如奖励金额、曝光次数），写明具体数值

## 因变量 / 中介 / 调节变量的字段清单

- **变量名称 / 变量名称（EN）** + 角色标注
- **概念性定义 / Conceptual Definition**
- **测量量表 / Measurement Scale**（若用量表测量，字段同问卷法）
  - 题项 / Items（逐字 + 中英对照）
  - 响应量尺 / Response Scale
  - 信度 / Reliability
  - 来源 / Source（APA）
- **行为/客观指标**：若 DV 是行为任务、选择、反应时、生理指标等，说明具体任务名称、指标计算方式（如「分配给对方的金额（0–10 中的整数）」「反应时取对数转换」）

## 操纵检验 / Manipulation Check 的字段清单

- **流程 / Procedure**：作者如何检验操纵有效性（何时施测、比较哪些组、统计检验）
- **测量 / Measurement**：
  - 具体题项原文（中英对照）
  - 响应量尺
  - 来源（APA）
  - **结果**：组间差异的统计结果（如「M_高权力 = 5.62 vs. M_低权力 = 3.10, t(118) = 8.44, p < .001」）——文中给出则报告

## 输出格式示例

```markdown
### 自变量 / IV：Power Sense / 权力感（组间设计，2 组）

**概念性定义 / Conceptual Definition**
> "…" —— 原文引用 + 中文翻译

**操纵细节 / Manipulation Details**
- **实验条件 / Experimental Conditions**：High-power condition vs. Low-power condition / 高权力感组 vs. 低权力感组（between-subjects）
- **操纵材料 / Manipulation Materials**：参与者阅读一段回忆写作任务指示……
- **流程 / Procedure**：
  1. …
  2. …
- **操纵剂量 / Dosage**：写作时长 5 分钟

---

### 操纵检验 / Manipulation Check：权力感

- **流程 / Procedure**：操纵后，参与者完成 3 题权力感量表，比较两组均值
- **测量 / Measurement**：
  1. "In my interactions with others, I feel I have a great deal of power." / 在与他人的互动中，我感到自己拥有很大的权力。
  - **响应量尺 / Response Scale**：7-point Likert (1 = Strongly Disagree, 7 = Strongly Agree) / 7点李克特量表
  - **来源 / Source**：Adopted from Anderson, C., John, O. P., & Keltner, D. (2012). …
- **结果 / Result**：M_high = 5.62 vs. M_low = 3.10, t(118) = 8.44, p < .001
```

## 常见遗漏点（务必检查）

- 多个实验共用同一 DV 但操纵方式不同 → 按实验分节
- 混淆变量控制（随机化、注意力检验、排除标准）
- 协变量与操纵检验的区别
- 附录中的完整情景材料原文（vignette、图片描述、脚本）
