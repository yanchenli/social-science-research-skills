# 社会科学研究方法技能包

> Eighteen AI agent skills for social-science research methods — turning a
> vague observation into a research question, variable extraction from papers,
> literature gap analysis, systematic review and
> meta-analysis, experiment design, data preparation, scale development &
> translation, quantitative analysis, SEM, results reporting, discussion
> writing, qualitative methods, citation auditing, manuscript and grant
> reviewing, journal selection, and reviewer response. Bilingual
> (English / 中文). Built for graduate students and supervisors in management,
> marketing, consumer behaviour and organizational behaviour.

**中文** | [English](README.en.md)

面向**管理学、营销学、消费者行为学、组织行为学**方向的研究生（MS / PhD / DBA）
与指导教师的 AI 方法学助手技能包。18 个技能覆盖从**现象到问题**、读文献提变量、选题、系统综述、
设计、数据准备、测量、分析、写作到**选刊投稿**、核查、评审与审稿回应的完整研究链路。

---

## ⚠️ 使用前必读：这是什么，不是什么

**这是方法学辅导与规范检查工具，不是代写工具。**

技能包帮你把「该怎么做、该怎么报」讲清楚，**不替你产生研究结论，也不替你判断**。
18 个技能内部都写入了硬约束，其中最重要的是：

| 约束 | 出处 |
|---|---|
| **数字原封不动**——所有统计数值必须来自你自己的软件输出，不得估算或修改 | `stats-results-writer` |
| **数字来自代码运行，不来自口算或记忆**——不得心算统计量，也不得在没有数据文件时「示范性地」编一个结果 | `quant-data-analysis` |
| **不「试到显著为止」**——先按预注册计划分析，计划之外的分析一律标注为探索性 | `quant-data-analysis` |
| **引语原封不动**——不得凭空生成「看起来像」的访谈内容，也不得把引语「润色」 | `qualitative-research-methods` |
| **不编造文献**——无法核实的文献一律标 `[待核实]`，不凭印象补全作者/年份/期刊 | `literature-gap-synthesizer` |
| **不依赖记忆，必须搜索**——每条文献核实结论必须基于搜索结果，禁止凭训练记忆断言 | `academic-citation-auditor` |
| **存疑不等于伪造**——严格区分「无法核实」与「虚构」，单一数据库无结果不得判定 | `academic-citation-auditor` |
| **AI 提议、研究者决定**——构念选择、量表取舍、题项措辞的最终判断由研究者做 | `scale-research` |
| **所有 α / AVE / CR 必须来自你自己的数据**——不得引用 AI 给出的信效度数字 | `scale-research` |
| **回译必须由「人」完成**——这是期刊评审的核查点，AI 回译不能作为质量证明 | `scale-research` |
| **禁止「边缘显著」**——p = .06 直接报告为不显著 | `sem-analysis-tutor`、`stats-results-writer` |
| **先审后建**——任何建议提出前先完成批判性审查，不得直接给建议而不附分析 | `social-science-experiment-designer` |
| **运行数据剖面本身就是一次数据接触**——盲化必须在运行前指定，之后「盲化」已经晚了 | `research-data-preparation` |
| **引用一律标红待核实**——AI 给出的文献信息不得当作已核实事实使用 | `academic-writing-assistant` |
| **不编造统计数据**——缺少的数据以占位符标出，不得填入任何虚构数字 | `academic-writing-assistant` |
| **不用「支持了理论 X」当贡献**——验证不等于贡献 | `discussion-conclusion-writer` |
| **红队之后必须走蓝队与事实核查**——红队的原始输出不能直接当审稿意见 | `management-paper-reviewer` |
| **不假装做了修改**——R&R 里做不到的要求要老实说明，改写成承认局限 | `response-to-reviewers` |

**研究者本人对研究设计、判断与结论负最终责任。** 本技能包的所有输出均为辅助性质，
应结合实际情境、机构要求与导师意见评估后使用。

### 关于直接产出正文的技能

`academic-writing-assistant`、`stats-results-writer`、`discussion-conclusion-writer`
三者会**直接产出论文正文**（Introduction / Literature Review、Results、Discussion），
因此也最容易被误用。它们的定位是**写作脚手架**：帮你理清论证链条、假设推导的逻辑、
结果报告的规范，以及贡献的讲法——**而不是替你决定研究贡献是什么**。

它们不生成任何未经核实的数据；所有文献引用一律以 `[待核实: Author, Year]` 标红输出，
并在文末附核验清单，要求你在真实数据库中逐条核实。

> **请自行确认所在院校对学位论文使用 AI 工具的规定。** 各校政策正在收紧，
> 且差异很大；期刊对 AI 辅助写作的披露要求也不一致。**是否使用、如何使用、
> 是否披露，由你与导师决定。**

### 关于两个评审技能

`management-paper-reviewer` 与 `grant-proposal-reviewer` 是**评审方**的工具，
不是作者方的工具。使用前请想清楚两件事：

1. 如果你本人是某期刊/基金的审稿人或评审委员，用它们生成的意见仍须由你判断——
   技能本身反复强调红队输出必须经过蓝队辩护与事实核查才能采用。
2. 如果你是把它们当作者用（预演自己会被怎么挑刺），这完全合理，
   但**不要因此假设真实审稿人会按同样的逻辑提问**。

---

## 技能一览

### 研究主线

| 技能 | 一句话 | 覆盖环节 | 规模 |
|---|---|---|---|
| [`phenomenon-to-question`](phenomenon-to-question/) | 把模糊的观察收敛成可研究的问题：前提压力测试、跨领域理论透镜、候选问题生成 | **从现象到问题** | SKILL.md + 4 个 references |
| [`literature-gap-synthesizer`](literature-gap-synthesizer/) | 系统梳理文献、诊断缺口类型、产出研究定位简报 | 选题与**文献** | SKILL.md + 2 个 references |
| [`systematic-review`](systematic-review/) | 系统综述与元分析：PRISMA 2020、效应量换算、异质性与发表偏倚 | **证据合成** | SKILL.md + 5 refs + 3 scripts |
| [`paper-variable-extraction`](paper-variable-extraction/) | 从论文中提取全部变量及其操作化信息，产出 Markdown 报告 + Excel 变量表 | 读论文与**变量提取** | SKILL.md + 9 refs + 1 script |
| [`academic-writing-assistant`](academic-writing-assistant/) | 引导撰写 Introduction 与 Literature Review，含缺口论证与假设推导 | 论文**写作（前段）** | SKILL.md + 4 个 references |
| [`social-science-experiment-designer`](social-science-experiment-designer/) | 从零设计严谨的多实验研究方案，产出六个标准交付文件 | 研究**设计** | SKILL.md + 5 个 references |
| [`research-data-preparation`](research-data-preparation/) | 数据获取前的计划、接触审计、决策状态与可交接规格 | 数据**准备** | SKILL.md + 10 refs + 6 scripts + 1 模板 |
| [`scale-research`](scale-research/) | 量表搜寻、评估、EN↔ZH 回译与情境改编全流程 | 测量**工具** | SKILL.md + 3 个 references |
| [`quant-data-analysis`](quant-data-analysis/) | 数据筛查、ANOVA/ANCOVA、回归调节的实际执行（含脚本） | 基础**统计** | SKILL.md + 2 refs + 4 scripts |
| [`sem-analysis-tutor`](sem-analysis-tutor/) | 手把手带你完成 SEM 分析全流程（CB-SEM / PLS-SEM 双轨） | **SEM** 分析 | SKILL.md + 12 个 references |
| [`stats-results-writer`](stats-results-writer/) | 把统计软件输出转成规范的 APA 报告段落（中/英） | 结果**报告** | SKILL.md + 8 个 references |
| [`discussion-conclusion-writer`](discussion-conclusion-writer/) | 理论贡献、实践启示、局限与结论段（Whetten / Corley & Gioia / Bartunek & Rynes） | 论文**写作（后段）** | SKILL.md + 1 个 references |
| [`journal-submission`](journal-submission/) | 论文定档、候选刊检索、匹配度与 desk reject 风险、投稿准备 | **选刊与投稿** | SKILL.md + 4 refs |

### 旁支与评审

| 技能 | 一句话 | 覆盖环节 | 规模 |
|---|---|---|---|
| [`qualitative-research-methods`](qualitative-research-methods/) | 五种质性传统、编码分析、可信性核查、Findings 撰写 | **质性**研究 | SKILL.md + 8 个 references |
| [`academic-citation-auditor`](academic-citation-auditor/) | 逐条核实参考文献真实性，识别 AI 幻觉文献与引用失实 | 学术**核查** | SKILL.md |
| [`management-paper-reviewer`](management-paper-reviewer/) | 期刊论文深度评审：红队五攻击者 → 蓝队辩护 → 事实核查 | 论文**评审** | SKILL.md |
| [`grant-proposal-reviewer`](grant-proposal-reviewer/) | 基金/项目申请书评审，产出委员会版与申请人版两份意见 | 基金**评审** | SKILL.md |
| [`response-to-reviewers`](response-to-reviewers/) | R&R 意见整理、逐条策略、意见冲突裁决、回复信撰写 | 审稿**回应** | SKILL.md |

每个技能目录下都有一份 `README.md`（使用手册），说明它解决什么问题、
什么时候用、工作流程、目录结构与注意事项。

---

## 建议的使用顺序

这 18 个技能沿**研究流程**衔接，另有两支旁支：

```
① 从现象到问题 phenomenon-to-question
      ↓
② 选题与文献   literature-gap-synthesizer → systematic-review（需定量合成时）
      ↓   ↕ 读文献时提变量：paper-variable-extraction
③ 写作（前段） academic-writing-assistant      ← Introduction / Literature Review
      ↓
④ 研究设计     social-science-experiment-designer
      ↓
⑤ 数据准备     research-data-preparation
      ↓
⑥ 测量         scale-research
      ↓
⑦ 基础统计     quant-data-analysis
      ↓
⑧ SEM          sem-analysis-tutor
      ↓
⑨ 结果写作     stats-results-writer
      ↓
⑩ 讨论与结论   discussion-conclusion-writer
      ↓
⑪ 核查与投稿   academic-citation-auditor → management-paper-reviewer
                → journal-submission → response-to-reviewers

旁支 A（质性路线）  qualitative-research-methods
旁支 B（基金申请）  grant-proposal-reviewer
```

写作线是**贯穿**的，不排在最后：Introduction 与 Literature Review 通常在收数据之前
就要动笔，拿到结果后再回改；`academic-citation-auditor` 在定稿前做最后一道引用自查。

- **有一个现象，但不知道该研究什么** → `phenomenon-to-question`
- **要读一批论文、把变量与量表整理成表** → `paper-variable-extraction`
- **只有一个宽泛主题，不知道该研究什么** → `literature-gap-synthesizer`
- **要把一批实证研究合成一个结论（含元分析）** → `systematic-review`
- **要动笔写 Introduction / Literature Review** → `academic-writing-assistant`
- **有想法、还没收数据** → `social-science-experiment-designer`
- **数据还没到手，想先想清楚数据计划** → `research-data-preparation`
- **要做问卷/量表** → `scale-research`
- **数据收好了，要跑 ANOVA / 回归** → `quant-data-analysis`
- **要跑 SEM / 中介** → `sem-analysis-tutor`
- **跑完要写 Results** → `stats-results-writer`
- **结果写完了，不知道怎么讲贡献** → `discussion-conclusion-writer`
- **做的是访谈/案例** → `qualitative-research-methods`
- **论文定稿前自查引用** → `academic-citation-auditor`
- **不知道这篇稿子能投什么档、投哪几本** → `journal-submission`
- **想知道自己的论文会被怎么挑刺** → `management-paper-reviewer`
- **审稿意见回来了** → `response-to-reviewers`

### 八处容易混淆的分工

1. **`sem-analysis-tutor` vs `quant-data-analysis`** —— 边界是**方法**，不是「有没有数据」。
   SEM / PLS-SEM / PROCESS 中介走前者；ANOVA / ANCOVA / 回归调节 / 简单斜率走后者。
   两者都会做数据筛查，但语境不同。
2. **三个写作技能** —— `academic-writing-assistant` 写 **Introduction 与 Literature Review**；
   `stats-results-writer` 写 **Results**；`discussion-conclusion-writer` 写 **Discussion 与 Conclusion**。
   三者的写作规范不同，不要混用。
3. **`management-paper-reviewer` vs `grant-proposal-reviewer`** —— 前者评**已完成的研究**
   （期刊论文），后者评**计划**（基金申请）。标准不同：后者多出可行性、预算、团队资质、时间规划。
4. **`literature-gap-synthesizer` vs `academic-writing-assistant` 阶段 2** ——
   前者做的是更前面、更重的活（文献量大、主题模糊、需要系统论证「为什么这是真缺口」）；
   后者有一个轻量的缺口分类步骤，适合「文献已经理清、只是要写成一段话」。
   两者用同一套研究定位模板，可以直接对接。
5. **标红待核实 vs 真正去核实** —— 写作技能生成引用时**一律标红待核实**；
   `academic-citation-auditor` 才是**真正去核实**的那一个。写完之后要用它过一遍。
6. **`paper-variable-extraction` vs `systematic-review`** —— 前者**读单篇论文、提取变量**，
   产出变量词典；后者**合成多篇论文**，产出效应量。前者是后者的上游（编码阶段可直接用它的 Excel），
   但两者解决的问题不同：一个问「这篇论文怎么测的」，一个问「这些论文合起来说明什么」。
7. **`journal-submission` vs `management-paper-reviewer`** —— 前者判**档位与去哪投**；
   后者判**这篇稿子本身好不好**。投稿前建议先用后者挑刺、再用前者选刊——
   顺序反了会按期刊偏好倒推评语。
8. **`phenomenon-to-question` vs `literature-gap-synthesizer`** —— 区别在**起点**：
   前者从**现象**出发（"我观察到 X，这能不能做研究"），产出研究问题；
   后者从**主题/构念**出发（"我想研究 X，文献缺什么"），产出研究定位。
   用户只有一个模糊的观察时先走前者，已有明确构念时直接走后者。

---

## 安装

技能就是一个含 `SKILL.md` 的目录。把需要的技能目录复制到你所用 agent 环境的技能目录下：

| 环境 | 技能目录 |
|---|---|
| Claude Code | `~/.claude/skills/` |
| WorkBuddy | `~/.workbuddy-ai/skills/` |
| DeepSeek Harness（DSH） | `~/.dsh/skills/`（项目级用 `<项目根>/.dsh/skills/`） |
| 其他兼容 Agent Skills 规范的环境 | 参见该环境的文档 |

> **DSH 的两个注意点**：它只扫描**一级**目录，`skills/<技能名>/SKILL.md` 正是它要求的结构，
> 直接整目录复制即可；技能名必须保持 kebab-case（本仓库所有技能目录名都是）。
> 项目级目录（`<项目根>/.dsh/skills/`）优先级高于用户级（`~/.dsh/skills/`），
> 同名技能以后者被前者覆盖。

```bash
# 例：安装全部 18 个技能到 Claude Code
git clone https://github.com/yanchenli/social-science-research-skills.git
cp -r social-science-research-skills/*/ ~/.claude/skills/
```

### 让 AI agent 自己装（不用碰命令行）

把下面这段话直接发给你在用的 agent——Claude Code / Codex / DeepSeek Harness / WorkBuddy 都适用。
两段提示词都要求它**先确认目录、先检查同名冲突、装完自检**，而不是闷头复制。

**① 全局安装**（本机所有项目可用）

```
请把 https://github.com/yanchenli/social-science-research-skills 里的技能安装到本机的用户级技能目录。

1. 先确认我的技能目录是哪个：Claude Code 是 ~/.claude/skills/，WorkBuddy 是 ~/.workbuddy-ai/skills/，
   DeepSeek Harness 是 ~/.dsh/skills/。判断不了就问我，不要猜。
2. 把仓库克隆到临时目录；没有 git 就下载 zip 解压。
3. 只复制含 SKILL.md 的目录，不要复制 README.md、README.en.md、LICENSE、.git。
4. 复制前检查目标目录里有没有同名技能。有的话先把清单给我，问我要不要覆盖，不要直接盖。
5. 装完自检并报告：装了几个、分别是哪些、每个目录下 SKILL.md 是否存在、
   哪些技能带脚本需要额外装依赖。
```

**② 项目工作区安装**（只在这个项目里可用）

```
请把 https://github.com/yanchenli/social-science-research-skills 里的技能装到当前项目的项目级技能目录，只装我指定的几个。

1. 先确认项目级目录：Claude Code 是 <项目根>/.claude/skills/，
   DeepSeek Harness 是 <项目根>/.dsh/skills/，WorkBuddy 是 <项目根>/.workbuddy-ai/skills/。
   判断不了就问我。
2. 把仓库克隆到临时目录；没有 git 就下载 zip 解压。
3. 我要装的是：<在这里写技能名，如 paper-variable-extraction、systematic-review>。
   我没写的话，先把技能清单列出来让我选。
4. 只复制这些技能目录，不要复制 README.md、README.en.md、LICENSE、.git。
5. 复制前检查同名冲突，有冲突先问我。
6. 装完自检并报告：装了什么、SKILL.md 是否存在、哪些需要装依赖。
```

> **项目级优先于用户级**：同名技能会覆盖用户级的，所以「只想在某个项目里先试试」用第 ② 种更安全。
> 如果你的环境不在上表里，把提示词第 1 步的目录换成你的实际目录即可。

安装后**不需要任何配置**。技能的 `description` 字段里写了触发条件，
当你提到 SEM、量表、实验设计、Results、讨论、质性编码、审稿意见等话题时会自动加载。

> **带脚本的技能需要额外装依赖。**
>
> - `quant-data-analysis` 与 `research-data-preparation`：`pandas` / `numpy` / `scipy` /
>   `statsmodels` / `openpyxl`，读取 SPSS 数据还需要 `pyreadstat`；
> - `paper-variable-extraction`：只需 `openpyxl`；
> - `systematic-review` 的三个脚本**只用 Python 标准库**，无需安装任何包。
>
> ```bash
> pip install pandas numpy scipy statsmodels openpyxl pyreadstat
> ```

---

## 触发方式

用自然语言提需求即可，例如：

- 「帮我看看品牌拟人化这块文献到底缺什么」
- 「我有个研究想法，想做三个实验验证中介和调节，帮我设计」
- 「数据还没收，先帮我想清楚数据计划」
- 「我要测品牌依恋，帮我找量表，需要中文版」
- 「数据收好了，2×2 设计，帮我跑 ANOVA」
- 「帮我跑 SEM，用 SmartPLS，这是我的数据」
- 「AMOS 输出贴给你了，帮我写 Results 部分」
- 「结果都出来了，不知道怎么讲理论贡献」
- 「我有 14 份访谈转录稿，用 Gioia 方法论，帮我写 Findings」
- 「这篇论文的参考文献是真的吗，帮我核实一下」
- 「帮我审这篇论文，目标是 JCR」
- 「审稿意见回来了，帮我整理并起草回复信」

---

## 已知局限

这些技能不隐瞒自己的能力边界，各技能内都写了「已知局限」章节。汇总如下：

1. **中文数据库访问不稳定**——知网（CNKI）在境外网络环境下受限，
   中文文献核实可靠性低于英文文献，建议人工在知网补充核查。
2. **超长文献列表覆盖率下降**——参考文献超过 30 条时会启动优先核实策略，
   不保证全量核实。
3. **付费全文不可访问**——引用内容匹配核查依赖公开摘要，付费全文的核查深度有限。
4. **AI 自身幻觉风险**——技能通过强制搜索与自我校验机制降低此风险，但无法完全消除。
   高风险判定建议人工交叉确认。`management-paper-reviewer` 的红队阶段**刻意**激进，
   其原始输出必须经过蓝队辩护与事实核查才能采用。
5. **统计判断依赖你提供的输出**——若粘贴的数字有误，结论亦会有误。
6. **写作技能不产生研究贡献**——它们能帮你把逻辑写清楚，但「这个缺口是否真的存在」
   「这个贡献是否够新」必须由你和导师判断，技能无法替你评估原创性。
7. **质性技能不替代研究者的解读**——质性分析里的主观介入是方法的一部分，
   技能只负责结构化与规范核查，主题成立与否的判断权在你。
8. **评审技能不替代你的判断**——`management-paper-reviewer` 与 `grant-proposal-reviewer`
   给的是评分与理由，是否资助/接收由委员会或编辑决定。
9. **选刊判据的 B 轨尚未经真人同行审核**——`journal-submission` 的档案计量那一轨
   （DID / IV / RD / 事件研究）判据骨架来自文献，并做过一次系统审核，但**审核者是 AI，不是领域内同行**。
   「某档期刊的审稿人实际会追问什么」这类判断仍需真人把关；采纳与不采纳的完整记录见该技能的
   `references/b-track-review-log.md`，可自行核验。
10. **元分析脚本给的是中间量**——`systematic-review` 的 `meta.py` / `hs_meta.py` 输出的是
    合成过程中的量，定稿前建议用 R（`metafor` / `psychmeta`）复算一次，两边对上再写进论文。
11. **变量提取不替代精读**——`paper-variable-extraction` 结构化的是「论文怎么测的」，
    论文的论证是否成立仍需自己判断；它也不重算任何统计量。

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
