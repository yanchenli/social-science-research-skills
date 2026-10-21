# 反身性主题分析的Findings写法

配合`SKILL.md`阶段5使用，先读`findings-01-general.md`。

## 先确认：用的是哪一种主题分析

"主题分析"在文献里其实是三种做法（Braun & Clarke及合作者的划分），Findings的写法和质量标准不同：

| 取向 | 主题是什么 | 质量靠什么 |
|---|---|---|
| **反身性主题分析**（Braun & Clarke的当前取向） | 研究者生成的、围绕一个中心概念的共享意义模式 | 反身性、分析深度、连贯性、透明度；**不用编码者间信度** |
| 编码信度取向（如Boyatzis） | 预先定义的编码单位，主题常被当作"领域摘要" | 多位编码者的一致性（如Cohen's kappa） |
| 码本/模板取向（如框架分析、模板分析） | 介于两者之间，用结构化码本，编码更有解释性 | 码本的系统性与迭代 |

**内部不一致是评审最常抓的点**：论文引用Braun & Clarke的反身性取向，同时报告编码者间信度，等于引用了一个明确不接受这项质量标准的方法。发现用户这样写，提醒他们确认自己实际用的是哪一种，并在Methods里如实说清楚。

## 报告标准

Findings应当呈现：
- **主题清单**，每个主题有名称与一句话定义
- **每个主题的证据**：诊断性引语，来自多位受访者
- **主题之间的关系**：主题图（thematic map）可选，或用文字说明
- 与研究问题的对应关系

Methods里应交代（不在Findings里重复）：采用反身性主题分析（Braun & Clarke, 2006, 2019）；归纳还是理论驱动；语义层面还是潜在层面的主题；谁编码、如何处理研究者的立场（反身性陈述）。

## 判断标准：什么才算主题

- **主题是围绕中心概念组织起来的共享意义模式，不是话题或领域摘要**。检验方法：这个主题名称是不是对资料的一个**主张**？"价格"是话题；"价格被用作判断品牌是否'值得'的身份信号"是主题
- **主题不等于引语**：引语是证据，不是主题本身
- **主题之间有清晰边界又相互关联**：两个主题读起来像同一件事，需要合并或重新划分；一个主题下的内容各说各话，需要拆分
- **每个主题都应该服务于回答研究问题**，而不是把资料里所有有趣的东西都列出来
- **主题是生成的，不是"涌现"出来的**：Braun & Clarke (2019)明确强调研究者的能动性，写作里避免"主题从资料中自然涌现"这类表述，可改为"我们在分析中生成了……"

## 话题标签 vs 主题：对照示例（示例，非真实数据）

| 话题标签（不合格） | 分析性主题（合格） |
|---|---|
| 价格 | 价格被当作品牌是否"值得"的身份信号，而不只是成本 |
| 麻烦 | 可持续行为的"麻烦"被重新解释为身份验证的代价 |
| 社交媒体 | 社交平台把私人的消费选择变成需要向他人交代的公开表演 |

## 结构模板

1. **概览段**：几个主题，共同说明什么（见`findings-01-general.md`第12节）
2. **每个主题一节**，内部按 主题名与定义 → 分析叙述（交织引语，遵循tell–show–tell）→ 边界或变异 → 小结
3. **主题之间的关系**：用一小段说明主题如何相互支撑，若有主题图就在这里讲解
4. 过渡到Discussion

主题的顺序要有逻辑（时间顺序、因果链条，或由表及里），不要按"访谈中出现的先后"排。

## 中英文模板

- **说明分析取向（多在Methods，Findings开头可简要重申）**
  - EN: We conducted reflexive thematic analysis (Braun & Clarke, 2006, 2019), generating themes through [inductive/theoretically informed] engagement with the data. Themes are our interpretive constructions rather than patterns waiting to be discovered.
  - 中: 我们采用反身性主题分析（Braun & Clarke, 2006, 2019），以[归纳/理论引导]的方式在与资料的持续互动中生成主题。这些主题是我们的解释性建构，而不是等待被发现的现成模式。
- **主题定义句**
  - EN: This theme captures the way in which [participants] [make sense of / experience / negotiate] [X], organized around the idea that [central concept].
  - 中: 这一主题刻画了[受访者][理解/体验/协商][X]的方式，围绕的中心概念是[中心概念]。
- **主题小结**
  - EN: Taken together, these accounts suggest that [theme] is not simply [surface reading] but [deeper reading].
  - 中: 综合这些叙述，[主题]并不只是[表层理解]，而是[更深层的理解]。

## 常见坑

- 主题只是话题标签或领域摘要
- 主题过多过碎，彼此重叠
- 用"涌现"描述主题，忽视研究者的生成作用
- 用编码者间一致性"证明"反身性主题分析的质量
- 声称归纳，实际是套用预设框架（Pratt, 2009所说的"演绎式速记"）
- 分析停留在按访谈问题整理受访者说了什么

## 参考文献（均已核实）

- Braun, V., & Clarke, V. (2006). Using thematic analysis in psychology. *Qualitative Research in Psychology*, 3(2), 77–101.
- Braun, V., & Clarke, V. (2019). Reflecting on reflexive thematic analysis. *Qualitative Research in Sport, Exercise and Health*, 11(4), 589–597.
