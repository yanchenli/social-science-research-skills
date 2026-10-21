# Findings通用写作规范

配合`SKILL.md`阶段5使用，**每次写或改Findings都要先读这份**，再按分析取向读对应的02–06。相当于`stats-results-writer`里"写作规范"的质性版本。

---

## 1. Findings的位置与职责

Findings呈现的是**分析的结果与证据**：主题（或维度、模型、命题）是什么，凭什么这么说。理论贡献的展开、与文献的对话、实践启示，主要放在Discussion（交给`discussion-conclusion-writer`）。

但界线随传统不同而模糊：归纳式理论建构类论文（Gioia式、扎根理论、Eisenhardt式案例研究）里，Findings本身往往就是浮现出来的理论模型，与Discussion的分工要看目标期刊或学校的惯例。**动笔前先问清楚**：Findings里要不要放模型图与命题？Discussion是否再展开？

## 2. 骨架

1. **概览段**：告诉读者接下来有几个主题/维度、整体说明了什么、更多证据在哪张表里
2. **主体**：按主题/维度分节。每一节：主张（主题名＋一句话定义）→ 证据（引语/观察）→ 解读（这条证据为什么支持主张、意味着什么）→ 边界或变异
3. **收束**：主题之间怎么关联（整合模型或文字梳理），过渡到Discussion

## 3. tell–show–tell（证据三明治）

每个论点的基本单位：先**告诉**读者这一段要看什么（tell），再**展示**证据（show），最后**解释**证据说明了什么、应该带走什么（tell）。这一写法常被归于Golden-Biddle & Locke的《Composing Qualitative Research》（Sage）。

两种常见失败，都对应Pratt (2009)列出的典型错误：
- **只讲不展示**：断言一堆，没有证据，读者只能选择相信
- **只展示不解读**：一串引语接一串引语，分析缺席（"引语堆砌"），读者不知道该从中看出什么

## 4. 引语使用规范

**4.1 原封不动**：引语必须来自用户提供的转录稿/田野笔记，一字不改。AI不得编造引语，也不得把它"润色成更好听的版本"。发现某条引语与所配主题不匹配，指出问题，不要替用户换一条。用户尚未提供引语时，写骨架，用`[引语待补：P?，支持××]`占位。

**4.2 允许的技术处理（都要披露）**：
- 去掉口头填充词（"嗯""那个""you know"）：在Methods里说明做了这种清理
- 省略中间部分：用省略号（如 […]）
- 插入说明性文字：用方括号，如 "他[指门店经理]说……"
- 格式（省略号、方括号写法）统一，按目标期刊或学校规范

**4.3 长度**：短引语嵌入句子；较长引语另起缩进块引（APA 7：40词以上）。块引要少用，用了就要有解读。

**4.4 归属**：编号或化名＋必要的背景（角色、行业、年限），不足以识别身份，并与知情同意与匿名化方案一致。

**4.5 一条引语要"做工"**：能被分析所解释，是这个论点的诊断性证据，不是装饰。

**4.6 "强有力引语"与"证明性引语"**：管理学质性论文里常区分两种用法——简短、有力、嵌入正文的引语，用来"说明"论点；数量较多、往往放进表格的引语，用来"证明"这个模式在数据里是稳固的。这一区分常被追溯到Pratt的方法论文章，`[具体出处待核实：常见归于Pratt (2008, ORM 11(3), 481–509) 或 Pratt (2009, AMJ 52(5), 856–862)]`。表格的写法可参考Cloutier & Ravasi (2021, *Strategic Organization*, 19(1), 113–133)关于"用表格增强质性研究可信性"的讨论。

## 5. 一阶与二阶声音

Gioia, Corley & Hamilton (2013)区分**一阶**（informant-centric，受访者自己的词与视角）与**二阶**（researcher-centric，研究者的理论化解释）。不管用不用Gioia方法论，写作时都让两种声音可辨：

- 引语承载一阶；研究者的分析和主题标签承载二阶
- 不要把研究者的解释伪装成受访者原话
- 也不要只停在一阶复述，没有理论化——那是描述，不是发现

## 6. 频率与程度的措辞

- "所有／大多数／多位／少数／个别"要**定义并一致使用**（例如"多位"在全文里始终指同一量级）
- **不写百分比，不做伪量化**（Pratt, 2009列出的典型错误之一）——质性发现不追求统计代表性，百分比会让读者按统计逻辑去理解
- 可以说明证据来自多少位受访者，用于体现证据基础，但不要用它暗示统计显著或可推广
- 不要用频率措辞暗示推广性；可迁移性靠厚描述交代情境边界（见`coding-and-rigor.md`）

## 7. 反例与变异

不符合主流模式的受访者或案例要**明确报告**，并说明它揭示的边界条件或对理论的启示。悄悄忽略反例是对可信性最直接的伤害，`dissertation-peer-review`和`management-paper-reviewer`的质性维度也会查这一点。

## 8. 证据分布检查

写完一个主题，检查它的引语是否来自较多不同受访者，而不是只靠一两位善于表达的受访者。一个主题的证据几乎全部来自同一位受访者，说明这个主题证据单薄，或者它其实是那位受访者的个人观点。多位受访者的引语读起来措辞句式几乎一样，也是警讯（评审会核查，见`dissertation-peer-review`质性校准附录的"同质性核查"）。

## 9. 双语研究：引语翻译

中文访谈、英文论文（或反过来）时的处理原则，讨论可参考Temple & Young (2004, *Qualitative Research*, 4(2), 161–178)对翻译困境的分析——是否披露翻译、谁来翻译、翻译者参与到什么程度，都有方法论后果：

- **尽量晚翻译**：用原语言编码，只在报告时翻译要引用的片段
- **披露**：在Methods里说明访谈语言、编码语言、谁翻译、如何核对（例如双语同事对照原文核对、抽样回译）。**只写实际做过的**，不能因为模板里有就写上
- **文化负载词**：保留原词（拼音或汉字）加注释，如"面子（mianzi，大致对应'face'）"，不要硬翻成一个看似等价的英文词
- **保留原文**：把中文原文放在附录或补充材料，或表格里中英对照
- 翻译不能顺手"润色"：翻译是忠实转述，不是修辞加工

## 10. 人称、时态与语气

- 反身性传统和多数管理学质性论文接受第一人称（we/I）来表明研究者的能动性；中文学位论文常用"本研究"，遵循学校或导师规范
- 英文Findings常见做法：叙述访谈中发生的事用过去时，陈述分析结论用现在时；以目标期刊惯例为准
- 语气克制：不用"显然""毫无疑问"这类超出证据的措辞

## 11. 常见问题速查

| 问题 | 表现 | 处理 |
|---|---|---|
| 引语堆砌 | 连续多条引语，没有分析 | 每条引语后补解读，或删掉不做工的引语 |
| 只断言不展示 | 有结论没有证据 | 补诊断性引语或观察 |
| 主题是话题标签 | "沟通""价格"这样的名词 | 改成对资料的主张，见`findings-02-thematic.md` |
| 停在描述 | 复述受访者说了什么，没有上升到概念 | 补二阶解释与理论意义 |
| 一二阶混淆 | 研究者的解释写成受访者原话 | 拆开，让引语归引语，解释归解释 |
| 伪量化 | "67%的受访者……" | 换成一致定义的频率措辞 |
| 只选漂亮引语 | 证据来自一两位善言的受访者 | 检查分布，补其他受访者，报告变异 |
| 引语与主题不匹配 | 引语其实说的是别的 | 指出并请用户重新核对，不要替换 |
| 过度概括 | 情境性发现写成普遍规律 | 收窄措辞，交代边界 |
| 翻译失真/未披露 | 引语被润色或没有说明翻译 | 补披露，核对原文 |
| 泄露身份 | 背景描述足以识别 | 泛化背景信息 |
| 混用归纳与演绎 | 称归纳，实际套用理论框架 | 如实交代方法取向（Pratt, 2009） |

## 12. 中英文写作模板

（方括号内是待填内容，引语和事实必须用用户的真实材料）

**概览段**
- EN: Our analysis yielded [N] themes that together explain [phenomenon]: (1) [theme 1], (2) [theme 2], and (3) [theme 3]. We present each in turn, drawing on illustrative data; additional evidence appears in Table [X].
- 中: 我们的分析形成了[N]个主题，共同说明了[现象]：（1）[主题1]，（2）[主题2]，（3）[主题3]。下文逐一说明，并以代表性数据为证，更多证据见表[X]。

**引入主题**
- EN: The first theme, [name], captures [one-sentence definition]. It appeared in the accounts of [n] of the [N] participants, across [roles/contexts].
- 中: 第一个主题"[主题名]"指的是[一句话定义]。它出现在[N]位受访者中[n]位的叙述里，涉及[角色/情境]。

**嵌入短引语**
- EN: As [P7], a [role with X years' experience], put it: "[quote]." This illustrates [analytic point].
- 中: 正如[P7]（[角色，X年经验]）所说："[引语]"。这说明[分析要点]。

**引入并解读块引**
- EN: [P3] described in detail how [process]: [block quote]. Here, [P3] does not merely [description]; she [analytic interpretation].
- 中: [P3]详细描述了[过程]：[块引]。这里，[P3]不只是[描述]，而是[分析性解读]。

**报告变异或反例**
- EN: Not all participants described [pattern]. [P4] and [P11], for example, [contrasting account], suggesting that [boundary condition].
- 中: 并非所有受访者都描述了[模式]。例如[P4]和[P11][相反的叙述]，这提示[边界条件]。

**主题之间的过渡**
- EN: If [theme 1] captures [aspect], the second theme shows how [link].
- 中: 如果说[主题1]刻画的是[方面]，那么第二个主题则说明了[联系]。

**翻译说明（放Methods，须与实际做法一致）**
- EN: Interviews were conducted in [language] and coded in the original language. Excerpts reported here were translated into English by [who] and checked against the original by [who/how]; culturally embedded terms are retained in [pinyin/characters] with glosses.
- 中: 访谈以[语言]进行，并在原语言下编码；文中引用的片段由[谁]译成[目标语言]，并由[谁/如何]对照原文核对；带有文化内涵的术语保留原词并附注释。

---

## 参考文献（均已核实）

- Pratt, M. G. (2009). From the editors: For the lack of a boilerplate: Tips on writing up (and reviewing) qualitative research. *Academy of Management Journal*, 52(5), 856–862.
- Bansal, P., & Corley, K. (2012). From the editors: Publishing in AMJ—Part 7: What's different about qualitative research? *Academy of Management Journal*, 55(3), 509–513.
- Gioia, D. A., Corley, K. G., & Hamilton, A. L. (2013). Seeking qualitative rigor in inductive research: Notes on the Gioia methodology. *Organizational Research Methods*, 16(1), 15–31.
- Cloutier, C., & Ravasi, D. (2021). Using tables to enhance trustworthiness in qualitative research. *Strategic Organization*, 19(1), 113–133.
- Temple, B., & Young, A. (2004). Qualitative research and translation dilemmas. *Qualitative Research*, 4(2), 161–178.
