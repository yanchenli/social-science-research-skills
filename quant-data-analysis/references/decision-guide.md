# 检验选择与分析规范速查

配合`SKILL.md`阶段2–4使用。文献出处见文末；标了"待核对"的条目是经典文献，页码等细节引用前请对照原文。

## 1. 检验选择表

| 设计与变量 | 首选 | 说明 |
|---|---|---|
| 两组，连续DV | Welch t检验＋Hedges g与置信区间 | 默认Welch，不必先做方差齐性检验 |
| 三组及以上，单因素，连续DV | Welch ANOVA＋Games-Howell；或`factorial_anova.py`（可加`--robust`） | 两种都报告是稳妥做法 |
| 2×2及更多，被试间 | `factorial_anova.py`（Type III） | 交互显著→简单效应；交互不显著→主效应按"平均于另一因子"解读 |
| 有协变量 | ANCOVA（`--covariate`） | 见第4节 |
| 连续预测×连续/二分调节 | `simple_slopes.py` | 简单斜率＋Johnson-Neyman |
| 二分类DV | 逻辑回归 | 无现成脚本，现场写并验证 |
| 分类×分类 | 卡方／Fisher精确检验 | 期望频数过小用Fisher |
| DV严重偏态或有序 | 稳健方法或非参数，并说明理由 | 非参数不是"万能补救"，先看分布与研究问题 |
| 被试内、混合设计、多层数据 | 见第6节 | 没有现成脚本 |
| 中介、有调节的中介、SEM | 转`sem-analysis-tutor` | |

## 2. 假设与稳健方法

- **不要把Levene检验当守门员**：Delacre, Lakens & Leys (2017)指出，先做方差齐性检验再决定用Student t还是Welch t，往往给不出合适的答案，建议默认用Welch；Delacre, Leys, Mora & Lakens (2019)对单因素ANOVA给出同样建议，默认用Welch的W检验。本skill里的Levene输出只是诊断信息
- 方差明显不齐且单元格不平衡时，经典F不可靠：用`--robust`（HC3）并报告这一选择
- 正态性：看残差的偏度、峰度和Q-Q图，样本较大时Shapiro-Wilk几乎必然显著，不宜据此下结论
- 独立性：由设计保证（如同一组的被试是否互相影响），统计上查不出来，要在设计层面交代

## 3. 效应量

| 场景 | 报告 |
|---|---|
| 两组均值比较 | Hedges g（小样本校正）及95%置信区间；说明用的是合并标准差还是各组标准差 |
| ANOVA | 偏η²，并可加偏ω²（更少偏倚）；脚本两者都给 |
| 事后/简单效应 | 均值差＋置信区间＋d（脚本里d是均值差除以模型残差标准差） |
| 回归 | 标准化前后的系数、ΔR² |

不要报告"事后功效"（observed power）：它只是p值的函数，不提供额外信息（Hoenig & Heisey, 2001，待核对）。需要的话报告"敏感性分析"：在现有样本量下能检出多大的效应。

## 4. ANCOVA注意事项

- **协变量应在处理之前测量**：如果协变量本身可能被实验处理影响（例如处理后测的态度），放进去会引入偏差（Miller & Chapman, 2001，待核对）
- 先看斜率同质性（脚本会检验协变量×因子交互）；若显著，标准ANCOVA的假设被破坏，改用调节模型
- 不要指望用协变量"修正"未随机分配的组间差异
- 调整后均值报告在协变量均值处

## 5. 多重比较与分析自由度

- 事后比较用**Holm校正**（Holm, 1979，待核对）：比Bonferroni更有检验力且同样控制家族错误率
- 简单效应按"每个因子水平"作为一个比较家族，脚本内已校正；若你的假设本来就是几个预先规定的对比，就按预注册的对比做，不要事后全比一遍
- 分析自由度：排除规则、离群值处理、协变量选择、DV的取舍、停止收集数据的时机，每一项都会放大假阳性率（Simmons, Nelson & Simonsohn, 2011，待核对）。所以第0阶段就要把计划写下来
- 离群值：均值±3SD的z分数规则会被离群值本身扭曲，脚本用中位数/MAD规则标记；Leys, Delacre, Mora, Lakens & Ley (2019, *International Review of Social Psychology*, 32(1))也建议用MAD，并提倡预注册离群值规则`[作者顺序与页码待核对]`。多变量离群另用Mahalanobis距离类方法，脚本未包含

## 6. 被试内、混合设计与多层数据

`scripts/`目前只覆盖被试间设计与回归调节。遇到重复测量、混合设计、多层数据：

1. 说明这一段没有现成脚本，要现场写代码
2. 常用工具：pingouin的`rm_anova`、`mixed_anova`，statsmodels的`MixedLM`（多层）
3. **先用模拟数据（设定已知效应）验证代码**，再跑用户数据，这是本skill的硬要求
4. 被试内设计要检查球形假设（不满足用Greenhouse-Geisser校正），并报告用了哪种
5. 结果仍按阶段5整理成分析记录与结果包

## 7. 调节效应：简单斜率与Johnson-Neyman

- 连续预测变量与调节变量先均值中心化；二分预测变量不中心化（脚本会打印编码）
- 简单斜率常取调节变量均值±1SD，这是惯例，不是理论要求；有理论依据的取值（如某个临界分数）更好
- Johnson-Neyman给出调节变量取值范围内斜率显著的区间，适合没有天然分类点的连续调节（Bauer & Curran, 2005，待核对）
- 交互项显著才值得做简单斜率；交互不显著时，不要把"某个水平下斜率显著"讲成调节效应
- 方差不齐时加`--robust`，并说明

## 8. 常见错误速查

| 错误 | 更好的做法 |
|---|---|
| 先看结果再定排除规则 | 排除规则在看结果之前定，写入记录 |
| 交互不显著却报简单效应 | 先报交互；探索性简单效应要标注 |
| 把"不显著"写成"没有差异" | 报告置信区间，必要时用等效检验 |
| 用协变量"控制"被处理影响的变量 | 协变量应在处理前测量 |
| 只报p值 | 同时报效应量与置信区间 |
| 选择对自己有利的一版结果 | 含/不含离群值、含/不含排除都报告 |
| Levene不显著就用经典F | 默认Welch/稳健，Levene仅作诊断 |

## 参考文献

已在本次核实的：

- Delacre, M., Lakens, D., & Leys, C. (2017). Why psychologists should by default use Welch's t-test instead of Student's t-test. *International Review of Social Psychology*, 30(1), 92–101. https://doi.org/10.5334/irsp.82
- Delacre, M., Leys, C., Mora, Y. L., & Lakens, D. (2019). Taking parametric assumptions seriously: Arguments for the use of Welch's F-test instead of the classical F-test in one-way ANOVA. *International Review of Social Psychology*, 32(1). https://doi.org/10.5334/irsp.198

经典文献，细节凭记忆写成，引用前请核对原文：

- Aiken, L. S., & West, S. G. (1991). *Multiple Regression: Testing and Interpreting Interactions*. Sage.
- Bauer, D. J., & Curran, P. J. (2005). Probing interactions in fixed and multilevel regression. *Multivariate Behavioral Research*, 40(3), 373–400.
- Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics*, 6(2), 65–70.
- Hoenig, J. M., & Heisey, D. M. (2001). The abuse of power. *The American Statistician*, 55(1), 19–24.
- Miller, G. A., & Chapman, J. P. (2001). Misunderstanding analysis of covariance. *Journal of Abnormal Psychology*, 110(1), 40–48.
- Olejnik, S., & Algina, J. (2003). Generalized eta and omega squared statistics. *Psychological Methods*, 8(4), 434–447.
- Simmons, J. P., Nelson, L. D., & Simonsohn, U. (2011). False-positive psychology. *Psychological Science*, 22(11), 1359–1366.
