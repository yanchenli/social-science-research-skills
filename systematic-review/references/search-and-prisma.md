# 检索策略与 PRISMA 流程图

> 系统综述与叙述性综述的分界线，不在「读了多少文献」，而在**检索与筛选是否可复现**。

---

## 一、数据库怎么选（商科）

| 类别 | 数据库 | 说明 |
|---|---|---|
| **必检** | Web of Science Core Collection、Scopus | 覆盖面最广；两者的收录差异本身值得记录 |
| **强烈建议** | EBSCO Business Source、ProQuest ABI/INFORM | 商科专库，收录大量非 WoS 期刊 |
| **学科专用** | PsycINFO（行为/组织心理）、EconLit（经济）、ABI/INFORM（管理实务） | 按主题选 |
| **中文** | CNKI、万方、维普 | 若纳入中文文献，必须说明检索式与筛选标准 |
| **灰色文献** | 会议论文集、工作论文（SSRN、RePEc）、学位论文、预印本 | 至少说明**是否检索**、**为何纳入或排除** |

> **至少要检索两个独立数据库。** 只查一个库，无法回答「漏了什么」这个问题。

---

## 二、检索式：按概念块拼，不要堆关键词

把研究问题拆成 2–4 个概念块，块内用 OR，块间用 AND：

```
("brand anthropomorphism" OR "anthropomorphized brand" OR "brand humanization")
AND
(trust OR "brand trust" OR credibility)
AND
(consumer* OR customer* OR purchaser*)
```

**要点**：

- **截词**（`consumer*`）覆盖单复数与派生词；但要注意不同数据库的通配符不同（`*` vs `?`）；
- **字段限定**：`TS=`（主题）比全文检索精确；标题摘要检索召回低但噪声小，两者可都跑一遍；
- **同义词要穷举**：同一构念在不同文献里可能叫法完全不同（这是系统综述最花时间的部分）；
- **记录每个库的命中数**——这是 PRISMA 流程图第一格数字的来源；
- **完整检索式写进附录**，包括检索日期。没有这一步，别人无法复现。

> **检索日期必须写。** 数据库每月都在变，同一检索式隔半年跑出来的结果不同。

---

## 三、纳入排除标准

商科没有像医学 PICO 那样的统一模板，但可以借用并改造：

| 要素 | 商科对应 |
|---|---|
| **P**opulation | 研究对象（消费者 / 员工 / 企业 / 国家） |
| **I**ntervention / **E**xposure | 自变量或处理 |
| **C**omparison | 对照组或比较基准（若有） |
| **O**utcome | 因变量 |
| **S**tudy design | 实验 / 问卷 / 档案 / 质性 |

**必须事先写定**，并在报告里列出。常见的四条排除：

1. 非同行评审（除非专门做灰色文献分析）
2. 非实证（纯评论、编者按、书评）——除非研究问题就是理论综述
3. 效应量无法提取或换算
4. 语言限制（若限定英文，必须说明这是局限，不是中性选择）

> **第 4 条要特别小心**：「只纳入英文文献」会系统性排除中文、日文、韩文的研究，
> 而这些恰恰可能包含不同情境下的反例。写进局限，不要隐去。

---

## 四、筛选：双人独立 + 一致性

| 阶段 | 做法 |
|---|---|
| 标题/摘要筛选 | 两名研究者**独立**判断，记录分歧 |
| 全文筛选 | 同上；分歧由第三人裁决或讨论解决 |
| 一致性 | 报告 Cohen's κ；一般 κ ≥ 0.60 可接受，< 0.40 说明标准不清需重训 |

**单人筛选是系统综述最常被审稿人攻击的点。** 若确实只有一人，必须在局限里明说，
并说明如何降低偏差（如隔周重筛一遍、随机抽 20% 复核）。

---

## 五、PRISMA 2020 流程图的数字

四段式，每一格都要有数：

```
Identification
  Records identified from databases (n = ?)   ← 各库分别列出
  Records identified from other sources (n = ?)
  Duplicates removed (n = ?)
        ↓
Screening
  Records screened (n = ?)          = identified − duplicates
  Records excluded (n = ?)          ← 说明主要原因
        ↓
  Reports sought for retrieval (n = ?)
  Reports not retrieved (n = ?)
        ↓
  Reports assessed for eligibility (n = ?)
  Reports excluded (n = ?)          ← 按排除理由分类计数
        ↓
Included
  Studies included in review (n = ?)
  Studies included in meta-analysis (n = ?)   ← 这两个数常常不同，要解释差在哪
```

### 必须能对上的算术

| 关系 | 检查 |
|---|---|
| identified − duplicates = screened | 必对 |
| screened − excluded = sought for retrieval | 必对 |
| sought − not retrieved = assessed | 必对 |
| assessed − excluded = included | 必对 |
| included ≥ included in meta-analysis | 差额须说明（如效应量无法提取） |

`scripts/prisma_flow.py` 会强制校验这五条，任何一条对不上就报错。

> **审稿人真的会加。** 流程图数字加不起来，是最容易被一眼看出的硬伤。

---

## 六、可复现性清单

- [ ] 每个数据库的完整检索式（含字段限定与截词符）
- [ ] 检索日期
- [ ] 各库命中数
- [ ] 去重方法（手动 / 文献管理软件 / 具体规则）
- [ ] 纳入排除标准（逐条）
- [ ] 筛选人数与一致性系数
- [ ] 排除理由分类及各自计数
- [ ] 从「纳入综述」到「进入元分析」的差额解释

---

## 七、注册：**PROSPERO 不收商科综述**

这是一个高频误解，会直接浪费时间：

> **PROSPERO 只登记「与健康结局相关」的系统综述。** 官网原文是
> *prospectively registered systematic reviews with **health related outcomes***。
> 商科主题（消费者行为、组织行为、公司金融……）投过去会被拒，不是因为质量，而是因为范围。

**商科该去哪儿注册**：

| 平台 | 适合 | 说明 |
|---|---|---|
| **OSF**（Open Science Framework） | **首选** | 可注册任意学科的综述方案，可绑定时间戳、可公开可 embargo |
| **AsPredicted** | 简版预注册 | 条目少、上手快，适合学生项目 |
| **Campbell Collaboration** | 教育、社会政策、犯罪学等 | 若主题落在其范围内，权威性最高 |

> 注册的意义不是「走流程」，而是**把纳入排除标准在检索之前锁死**。
> 不注册也能做系统综述，但审稿人会问「你怎么保证标准不是看完文献才定的」。

### 灰色文献：商科必须专门交代

商科的非显著结果大量沉在未发表工作论文里，只查期刊会系统性高估效应。至少说明是否检索：

| 来源 | 内容 |
|---|---|
| **SSRN** | 商科最集中的工作论文库 |
| **NBER Working Papers** | 经济学与金融 |
| **RePEc / IDEAS** | 经济学工作论文聚合 |
| **ProQuest Dissertations & Theses Global（PQDT）** | 学位论文——商科里质量参差，但常含未发表的反例 |
| 会议论文集 | AOM、AMA、SMS 等年会论文 |

> **不需要全都检索，但必须说明检索了哪些、为什么。** 完全不提灰色文献，
> 在商科顶刊会被直接质疑「发表偏倚未处理」。
