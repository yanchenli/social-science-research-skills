# 社会科学研究方法技能包

> Six AI agent skills for social-science research methods — experiment design,
> scale development & translation, SEM analysis, results reporting, academic
> writing support (Introduction & Literature Review), and citation auditing.
> Bilingual (English / 中文). Built for graduate students and supervisors in
> management, marketing, consumer behaviour and organizational behaviour.

面向**管理学、营销学、消费者行为学、组织行为学**方向的研究生（MS / PhD / DBA）
与指导教师的 AI 方法学助手技能包。6 个技能覆盖从实验设计、测量、分析、报告、
写作到引用审计的完整研究链路。

---

## ⚠️ 使用前必读：这是什么，不是什么

**这是方法学辅导与规范检查工具，不是代写工具。**

技能包帮你把「该怎么做、该怎么报」讲清楚，**不替你产生研究结论，也不替你判断**。
6 个技能内部都写入了硬约束，其中最重要的是：

| 约束 | 出处 |
|---|---|
| **数字原封不动**——所有统计数值必须来自你自己的软件输出，不得估算或修改 | `stats-results-writer` |
| **不依赖记忆，必须搜索**——每条文献核实结论必须基于搜索结果，禁止凭训练记忆断言 | `academic-citation-auditor` |
| **存疑不等于伪造**——严格区分「无法核实」与「虚构」，单一数据库无结果不得判定 | `academic-citation-auditor` |
| **AI 提议、研究者决定**——构念选择、量表取舍、题项措辞的最终判断由研究者做 | `scale-research` |
| **所有 α / AVE / CR 必须来自你自己的数据**——不得引用 AI 给出的信效度数字 | `scale-research` |
| **回译必须由「人」完成**——这是期刊评审的核查点，AI 回译不能作为质量证明 | `scale-research` |
| **禁止「边缘显著」**——p = .06 直接报告为不显著 | `sem-analysis-tutor`、`stats-results-writer` |
| **先审后建**——任何建议提出前先完成批判性审查，不得直接给建议而不附分析 | `social-science-experiment-designer` |
| **引用一律标红待核实**——AI 给出的文献信息不得当作已核实事实使用 | `academic-writing-assistant` |
| **不编造统计数据**——缺少的数据以占位符标出，不得填入任何虚构数字 | `academic-writing-assistant` |

**研究者本人对研究设计、判断与结论负最终责任。** 本技能包的所有输出均为辅助性质，
应结合实际情境、机构要求与导师意见评估后使用。

### 关于 `academic-writing-assistant` 需要单独说明

它是本技能包中**唯一直接产出论文正文**（Introduction 与 Literature Review）的技能，
因此也最容易被误用。它的定位是**写作脚手架**：帮你理清研究缺口的论证链条、
假设推导的逻辑、以及文献整合（而非逐篇罗列）的组织方式——**而不是替你决定
研究贡献是什么**。

它不生成任何未经核实的数据；所有文献引用一律以 `[待核实: Author, Year]` 标红输出，
并在文末附核验清单，要求你在真实数据库中逐条核实。

> **请自行确认所在院校对学位论文使用 AI 工具的规定。** 各校政策正在收紧，
> 且差异很大；期刊对 AI 辅助写作的披露要求也不一致。**是否使用、如何使用、
> 是否披露，由你与导师决定。**

---

## 技能一览

| 技能 | 一句话 | 覆盖环节 | 规模 |
|---|---|---|---|
| [`social-science-experiment-designer`](social-science-experiment-designer/) | 从零设计严谨的多实验研究方案，产出六个标准交付文件 | 研究**设计** | SKILL.md + 5 个 references |
| [`scale-research`](scale-research/) | 量表搜寻、评估、EN↔ZH 回译与情境改编全流程 | 测量**工具** | SKILL.md + 3 个 references |
| [`sem-analysis-tutor`](sem-analysis-tutor/) | 手把手带你完成 SEM 分析全流程（CB-SEM / PLS-SEM 双轨） | 数据**分析** | SKILL.md + 12 个 references |
| [`stats-results-writer`](stats-results-writer/) | 把统计软件输出转成规范的 APA 报告段落（中/英） | 结果**报告** | SKILL.md + 8 个 references |
| [`academic-writing-assistant`](academic-writing-assistant/) | 引导撰写 Introduction 与 Literature Review，含缺口论证与假设推导框架 | 论文**写作** | SKILL.md + 4 个 references |
| [`academic-citation-auditor`](academic-citation-auditor/) | 逐条核实参考文献真实性，识别 AI 幻觉文献与引用失实 | 学术**核查** | SKILL.md |

每个技能目录下都有一份 `README.md`（使用手册），说明它解决什么问题、
什么时候用、工作流程、目录结构与注意事项。

---

## 建议的使用顺序

这 6 个技能沿**研究流程**与**写作流程**两条线衔接：

```
研究流程   ① 研究设计  →  ② 测量工具  →  ③ 数据分析  →  ⑤ 结果报告
           experiment-    scale-         sem-analysis-  stats-results-
           designer       research       tutor          writer

写作流程   ④ 论文写作 ──────────────────────────────────►  ⑥ 学术核查
           academic-writing-assistant                     academic-citation-
           （Introduction / Literature Review）            auditor
```

写作线是**贯穿**的，不排在最后：Introduction 与 Literature Review 通常在
收数据之前就要动笔，拿到结果后再回改；`academic-citation-auditor` 在定稿前
做最后一道引用自查。

- **有研究想法、还没收数据** → 从 `social-science-experiment-designer` 开始
- **要动笔写 Introduction / Literature Review** → `academic-writing-assistant`
- **要做问卷/量表** → `scale-research`
- **数据收好了要跑 SEM** → `sem-analysis-tutor`
- **跑完要写 Results** → `stats-results-writer`
- **论文定稿前自查引用** → `academic-citation-auditor`

**注意三处容易混淆的分工：**

1. `sem-analysis-tutor` 带你**做**分析（读数据、判断指标、处理异常）；
   `stats-results-writer` 帮你**写**分析结果（把已跑出的输出转成 APA 段落）。
   先做后写，不要用后者替代前者。
2. `academic-writing-assistant` 写的是 **Introduction 与 Literature Review**；
   `stats-results-writer` 写的是 **Results**。两者的写作规范不同，不要混用。
3. `academic-writing-assistant` 生成引用时**一律标红待核实**；
   `academic-citation-auditor` 才是**真正去核实**的那一个。写完之后要用它过一遍。

---

## 安装

技能就是一个含 `SKILL.md` 的目录。把需要的技能目录复制到你所用 agent 环境的技能目录下：

| 环境 | 技能目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| WorkBuddy | `~/.workbuddy-ai/skills/` |
| 其他兼容 Agent Skills 规范的环境 | 参见该环境的文档 |

```bash
# 例：安装全部 6 个技能到 Claude Code
git clone https://github.com/<your-name>/social-science-research-skills.git
cp -r social-science-research-skills/*/ ~/.claude/skills/
```

安装后**不需要任何配置**。技能的 `description` 字段里写了触发条件，
当你提到 SEM、量表、实验设计、Results、文献综述、参考文献核实等话题时会自动加载。

---

## 触发方式

用自然语言提需求即可，例如：

- 「我有个研究想法，想做三个实验验证中介和调节，帮我设计」
- 「我要测品牌依恋，帮我找量表，需要中文版」
- 「帮我跑 SEM，用 SmartPLS，这是我的数据」
- 「AMOS 输出贴给你了，帮我写 Results 部分」
- 「我要写 Introduction，但不知道怎么论证研究缺口」
- 「这些文献帮我整理成综述，别写成流水账」
- 「这篇论文的参考文献是真的吗，帮我核实一下」

---

## 已知局限

这些技能不隐瞒自己的能力边界，各技能内都写了「已知局限」章节。汇总如下：

1. **中文数据库访问不稳定**——知网（CNKI）在境外网络环境下受限，
   中文文献核实可靠性低于英文文献，建议人工在知网补充核查。
2. **超长文献列表覆盖率下降**——参考文献超过 30 条时会启动优先核实策略，
   不保证全量核实。
3. **付费全文不可访问**——引用内容匹配核查依赖公开摘要，付费全文的核查深度有限。
4. **AI 自身幻觉风险**——技能通过强制搜索与自我校验机制降低此风险，但无法完全消除。
   高风险判定建议人工交叉确认。
5. **统计判断依赖你提供的输出**——若粘贴的数字有误，结论亦会有误。
6. **写作技能不产生研究贡献**——`academic-writing-assistant` 能帮你把逻辑写清楚，
   但「这个缺口是否真的存在」「这个贡献是否够新」必须由你和导师判断，
   技能无法替你评估原创性。

---

## 许可

本项目采用 **[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)** 许可。

你可以自由地**共享**（以任何媒介或格式复制、发行本作品）和**演绎**
（修改、转换、以本作品为基础进行创作），包括用于商业目的，
但必须**署名**——给出适当的署名、提供指向本许可的链接，并说明是否作出了修改。

---

## 贡献

欢迎提 Issue 反馈问题，或提 Pull Request 补充方法学内容。
若你发现某个判断阈值有误、或某个软件输出字段的映射不准确，请附上文献依据。

---

## 声明

本技能包为研究方法辅助工具，**不构成对任何具体研究设计的专业保证**。
实验设计、量表选择、统计方法、写作规范与报告标准最终应以你所在学科的主流文献、
目标期刊要求、所在院校规定与导师意见为准。

使用本工具产出的任何学术作品，其学术诚信责任由作者本人承担。
