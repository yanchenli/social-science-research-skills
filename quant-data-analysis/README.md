# quant-data-analysis

> 量化数据分析助手 —— 把实验与问卷数据真正跑出来，并留下完整记录。

**版本**：1.0.0 ｜ **适用**：商科 MS/PhD/DBA 学生及教师 ｜ **规模**：SKILL.md + 2 个 references + 4 个脚本

---

## 它解决什么问题

技能组合里原本缺了中间那一段：

| 环节 | 负责的技能 |
|---|---|
| 设计 | `social-science-experiment-designer` |
| 量表 | `scale-research` |
| SEM / PROCESS 路径分析 | `sem-analysis-tutor` |
| **基础统计的实际执行**（ANOVA / ANCOVA / 回归调节） | **本技能** |
| 写成 Results | `stats-results-writer` |

它自带经过测试的 Python 脚本，上传 `csv` / `xlsx` / `sav` / `dta` 即可运行。

---

## 三条底线

这三条不是为了好看，是为了让结果**经得起审稿核查**：

1. **每个分析决定都留痕。** 排除了谁、为什么、按什么规则、用了哪个检验、为什么换检验。
   脚本会写进日志，AI 在对话里也要复述。
2. **不「试到显著为止」。** 先确认预注册的分析计划，按计划分析；计划之外的分析一律标注为**探索性**。
3. **数字来自代码运行，不来自口算或记忆。** AI 不得心算统计量，也不得在没有数据文件的情况下
   「示范性地」编一个结果。

> 脚本已用**含已知真值的模拟数据**测试过，并与 `pingouin` 及手写 numpy 最小二乘交叉核对。

---

## 工作流程（六阶段）

| 阶段 | 内容 | 产出 |
|---|---|---|
| 0. 信息与前置 | 设计类型、变量、**预注册计划**、排除规则、数据文件 | 分析计划 |
| 1. 数据筛查 | 缺失/重复、按规则排除、单元格样本量、离群值标注 | `screening_report.txt`、`exclusion_log.csv`、`data_clean.csv` |
| 2. 选检验 | 按设计选 ANOVA / ANCOVA / 回归 | 选择理由 |
| 3. 运行 | 脚本执行 | 结果表 |
| 4. 诊断与敏感性分析 | 稳健性、含/不含离群值两版 | 敏感性报告 |
| 5. 交付 | 分析记录 + 结果包 | 可交给 `stats-results-writer` |

### 阶段 0 的一个关键设计

若已有 `research_data_spec.json`（由 [`research-data-preparation`](../research-data-preparation/) 生成），
**先读它，再提问**。其中：

- `data_exposure.level` —— 研究者接触数据的程度
- `decision_status` —— 每个决定是事前锁定还是数据驱动
- `sample_rules` / `analysis_plan` —— 预先规定的排除规则与分析计划

`pre_locked` 的按计划做；`data_driven` 的分析在结果里标为探索性；
`evidence_status` 为 `needs_verification` 的信息不当已验证。**规格里写明的内容不要重复问用户。**

---

## 四个脚本

| 脚本 | 作用 |
|---|---|
| `screen_data.py` | 缺失与重复检查、按规则排除并写日志、单元格样本量、按单元格用中位数/MAD 规则**标记**离群值（只标记，不删除） |
| `factorial_anova.py` | Type III ANOVA、Welch/稳健方法、简单效应、效应量、Holm 校正 |
| `simple_slopes.py` | 回归调节效应的简单斜率、Johnson-Neyman |
| `common.py` | 数据读取（csv/xlsx/sav/dta）、格式化 |

```bash
python scripts/screen_data.py --file data.csv --dv 满意度 \
       --factors 组别,性别 --id 被试编号 \
       --exclude "attn != 1" --exclude "duration < 60" --outdir screen_out
```

**离群值只标记不删除**是刻意的：删不删是研究者的决定。理想情况是分析前就定好规则；
没定好的，做「含/不含」两版并都报告。

---

## 一个容易被忽略的交代

排除之后，样本量要能在 Methods 里对上：

> 总收集 N → 各条排除规则各排除多少 → 最终 N

审稿人查这一项的频率比想象中高。

---

## 使用示例

```
数据收完了，2×2 被试间设计，DV 是购买意愿，有个协变量是品牌熟悉度。
帮我看看有没有显著，英文报告。
```

技能会先确认预注册计划（没有就在这一步写下来再动数据），跑筛查、报告单元格样本量与
离群值标记，再选检验（有协变量 → ANCOVA），跑完做敏感性分析，最后给出可交给
`stats-results-writer` 的结果包。

**交互显著时**会追问简单效应的方向，而不是直接下结论。

---

## 目录结构

```
quant-data-analysis/
├── SKILL.md                        六阶段流程、三条底线、脚本用法
├── references/
│   ├── decision-guide.md           检验选择的判断树（含被试内/混合/多层数据的处理建议）
│   └── analysis-log-and-handoff.md 分析记录格式与交接规格
└── scripts/
    ├── common.py                   数据读取与格式化
    ├── screen_data.py              数据筛查
    ├── factorial_anova.py          因子方差分析与简单效应
    └── simple_slopes.py            简单斜率与 Johnson-Neyman
```

---

## 边界与注意事项

- **不含 SEM 与中介分析。** 转 [`sem-analysis-tutor`](../sem-analysis-tutor/)。
- **不撰写 Results 文字。** 转 [`stats-results-writer`](../stats-results-writer/)。
- **不替研究者做取舍。** 离群值删不删、显著性不稳时怎么写，给出选项与后果，判断权在研究者。
- **被试内 / 混合 / 多层设计没有现成脚本。** 见 `decision-guide.md` 第 6 节，
  现场写代码并**先用模拟数据验证**。
- **不「示范性」编结果。** 没有数据文件时不会给一个假的结果演示。

---

## 与相邻技能的分工

- **SEM / PLS-SEM / PROCESS 中介** → [`sem-analysis-tutor`](../sem-analysis-tutor/)。
  两者的边界是**方法**，不是「有没有数据」。
- **要写 Results 段落** → [`stats-results-writer`](../stats-results-writer/)。
- **分析前的数据计划与接触审计** → [`research-data-preparation`](../research-data-preparation/)。
- **复核别人的分析是否合规** → [`management-paper-reviewer`](../management-paper-reviewer/) 的统计审计员。

---

## 版本

**1.0.0** —— 六阶段流程、三条底线、四个经模拟数据验证的脚本、分析记录与交接规格。
