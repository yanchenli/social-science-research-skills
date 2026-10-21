# qualitative-research-methods

> 质性研究方法 —— 严谨不是统计显著性，是可信性。

**版本**：1.0.0 ｜ **适用**：商科 MS/PhD/DBA 学生及教师 ｜ **规模**：SKILL.md + 8 个 references

---

## 它解决什么问题

量化路线有一整套工具，质性路线常常只能靠「导师说怎么改」。这个技能补上整条链：

传统选择 → 抽样与工具设计 → 编码与分析 → 严谨性核查 → Findings 撰写。

它是这套技能里**唯一不依赖统计**的一条路径，也是唯一把「引语」当作核心证据的路径。

---

## 核心理念

**质性研究的「严谨」不是统计显著性，是可信性（trustworthiness）。**

质性研究里设计、收集、分析常常交织进行——尤其扎根理论的「理论抽样」，分析结果会反过来指导
下一步该找谁访谈。所以技能里的阶段划分是一张**入口地图**，不代表必须严格按顺序走一遍。

> ⚠️ **引语之于质性，相当于数字之于量化。**
> 编码、分析、Findings 撰写都必须基于用户提供的真实转录稿/田野笔记：
> **不得凭空生成「看起来像」的访谈内容，也不得把用户的引语「润色」成更漂亮的版本。**

AI 负责结构化——选传统、搭工具、建编码框架草案、核对严谨性标准、起草和诊断 Findings；
真正的解读判断、编码取舍、理论建构，是研究者的活。
**质性分析里的主观介入本身就是方法的一部分，不是要被消除的噪音。**

---

## 工作流程（五阶段）

| 阶段 | 内容 | 关键产出 |
|---|---|---|
| 1. 范式与传统选择 | 五种传统的适用条件；扎根理论三派的分辨 | 传统 + 版本的选择及理由 |
| 2. 抽样与资料收集设计 | 目的性/极端案例/理论/滚雪球抽样；访谈提纲、焦点小组、观察记录 | 抽样方案 + 工具 |
| 3. 编码与分析 | 主题分析、扎根理论编码、Gioia 数据结构、交叉案例分析 | 编码框架 + 主题结构 |
| 4. 严谨性核查 | Lincoln & Guba 四要素；进入 Findings 前的留痕清单 | 可信性说明 |
| 5. Findings 撰写 | 按传统分册的写作规范；引语使用；双语引语翻译 | Findings 正文 |

### 阶段 1：五种传统

| 传统 | 适合的研究问题形状 |
|---|---|
| 案例研究（尤其 Eisenhardt 式理论建构） | 「某情境下 X 是如何发生/展开的」，想从案例归纳出新理论 |
| 扎根理论 | 对一个过程/现象还没有现成理论解释，想直接从资料里「长出」理论 |
| 现象学 | 想理解某段经历对当事人而言「是什么感觉」，不追问因果 |
| 民族志 | 想理解一个群体/组织的文化、日常实践如何运作，能做长期浸入 |
| 叙事研究 | 想理解人们如何用「讲故事」为经历赋予意义、建构身份 |

商科/管理研究里，**案例研究与扎根理论**是最常见的两条路；用户没有强烈偏好时优先从这两个判断。

**扎根理论三派必须分清**：Glaser & Strauss 经典版（理论从资料「涌现」）、
Strauss & Corbin 系统版（更结构化的编码步骤）、Charmaz 建构主义版（理论是研究者「建构」的）。
三派对编码步骤与研究者角色的假设不同，**选定后阶段 3 要对应同一版本，不要中途混用**。

### 阶段 4：可信性四要素

credibility（三角验证 / 成员检验 / 同行汇报）、transferability（厚描述）、
dependability（审计轨迹）、confirmability（反身性陈述）。

技能会逐项核对是否**有实质性交代**，而不是只挂了术语。

---

## Findings 写作按传统分册

这是本技能最有价值的设计之一——质性论文的 Findings 没有统一模板，
不同传统的写法差别很大：

| 参考文件 | 适用 |
|---|---|
| `references/findings-01-general.md` | 通用规范：引语使用、原封不动原则、占位符约定 |
| `references/findings-02-thematic.md` | 主题分析式叙述 |
| `references/findings-03-gioia.md` | Gioia 方法论：一阶概念 / 二阶主题 / 聚合维度 + 数据结构图讲解 |
| `references/findings-04-grounded-theory.md` | 扎根理论：范畴、属性、维度与理论饱和度 |
| `references/findings-05-case-study.md` | 案例研究：跨案例比较、命题提炼 |
| `references/findings-06-other-traditions.md` | 现象学、民族志、叙事研究 |

---

## 使用示例

```
我有 14 份访谈转录稿，做的是中层管理者对数字化转型的理解。
用的是 Gioia 方法论，编码表已经做了两轮，帮我写 Findings，英文。
```

技能会先确认传统与版本是否与编码步骤一致、抽样与饱和是否有交代，
再读 `findings-03-gioia.md` 的写作规范，逐项诊断现有编码表（二阶主题是否真的比一阶概念更抽象，
还是只换了说法），最后按 Gioia 的叙述结构起草 Findings。

**引语缺失时不会编。** 会写成骨架并用 `[引语待补：P?，支持××]` 占位。

---

## 目录结构

```
qualitative-research-methods/
├── SKILL.md                              五阶段流程、五种传统、编码方法、可信性核查
└── references/
    ├── qualitative-traditions.md         五种传统的假设、适用条件、代表作
    ├── coding-and-rigor.md               编码方法、Lincoln & Guba 四要素、留痕清单
    ├── findings-01-general.md            通用写作规范与引语原则
    ├── findings-02-thematic.md           主题分析式 Findings
    ├── findings-03-gioia.md              Gioia 方法论 Findings
    ├── findings-04-grounded-theory.md    扎根理论 Findings
    ├── findings-05-case-study.md         案例研究 Findings
    └── findings-06-other-traditions.md   现象学/民族志/叙事研究 Findings
```

---

## 边界与注意事项

- **不替研究者编码或下解释判断。** 可以提编码框架草案、标注可能的主题、起草并诊断 Findings，
  但主题成立与否、解读方向，最终判断权在研究者。
- **不编造引语。** 见上文核心提醒。
- **不把「饱和」当数字。** 样本量要有理论饱和依据（如「最后几次访谈未再产生新主题」），
  不是随意给一个数。
- **不假装能做 NVivo。** 没有质性分析软件也完全可以做——用表格/文档手动编码，
  技能可以在你提供的文本上直接标注、归类、生成编码框架初稿。

---

## 与相邻技能的分工

- **选题与文献缺口** → [`literature-gap-synthesizer`](../literature-gap-synthesizer/)。
- **写 Introduction / Literature Review** → [`academic-writing-assistant`](../academic-writing-assistant/)。
- **写 Discussion 与贡献** → [`discussion-conclusion-writer`](../discussion-conclusion-writer/)。
- **研究设计阶段的伦理与数据治理** → [`research-data-preparation`](../research-data-preparation/) 的
  `primary-qualitative.md` 覆盖访谈后勤、记录与治理。

---

## 版本

**1.0.0** —— 五阶段流程、五种质性传统、扎根理论三派分辨、六册 Findings 写作规范、可信性四要素核查。
