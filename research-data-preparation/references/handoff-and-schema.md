# 交接包与机器可读规格

配合`SKILL.md`阶段6使用。这套规格要给**其他agent也能读**，所以接口要明确：上游交付什么、下游接收什么，避免不同agent重复询问同样的问题、重新定义变量、重复做数据质量检查，或者把探索性结果当成确认性证据。

## 1. 交接包（第一版）

| 文件 | 内容 | 谁读 |
|---|---|---|
| `research_data_plan`（.docx或.md） | 研究目标、数据路径、设计、决策状态、实施计划、伦理与治理、主要风险 | 研究者阅读、审阅、修订 |
| `data_workbook.xlsx` | 构念映射、变量字典、样本规则、数据来源、分析计划、伦理与DMP、决策日志、交接与验收 | 研究者**唯一手工编辑的地方** |
| `research_data_spec.json` | 由工作簿转换生成的机器可读规格 | 下游skill与其他agent |
| `profile_report.md`、`profile_summary.json`、`exposure_log.jsonl` | 数据剖面与接触记录（用过脚本时） | 研究者与下游agent |
| `data_acquisition_checklist` | 实际采集、下载、招募、预试、访谈准备的操作检查清单 | 执行者 |

**单一来源原则**：研究者只改工作簿，JSON由脚本生成，两者不会不同步：

```
python scripts/make_workbook.py --out data_workbook.xlsx                    # 空白模板
python scripts/workbook_to_spec.py data_workbook.xlsx --out research_data_spec.json
python scripts/validate_spec.py research_data_spec.json
```

已有JSON想生成填好的工作簿：`make_workbook.py --out x.xlsx --from-spec spec.json`。

## 2. 规格里每个字段的意思

完整定义见`research_data_spec.schema.json`（JSON Schema draft-07）。要点：

- `data_exposure.level`：E0–E4，**该skill的操作性分级**，不是学术标准
- `decision_status`：`pre_locked`／`locked_after_exposure`／`data_driven`／`open`，说明**决定何时怎样定下来**
- `evidence_status`：`researcher_stated`／`source_documented`／`profile_verified`／`needs_verification`，说明**信息核实到什么程度**
- `readiness.status`：研究准备状态，**不是数据质量评级**
- `holdout_or_blinding.strategy`：`none`／`blinded_summary`／`holdout_sample`／`disclosure_only`
- `governance.items_needing_human_verification`：需要人工核验的法律、伦理、使用条款事项

## 3. 其他agent读取时必须遵守的规则

1. **先读规格，再提问**：规格里已经写明的信息不要重复向用户询问；只问`open`和`needs_verification`的项目
2. **不要把`needs_verification`或`researcher_stated`当成已验证**：写作或分析时对这些项目保持保留
3. **不要重新定义变量**：变量以规格里的`derivation`为准；若发现问题，记录并报告给用户，而不是悄悄改
4. **尊重接触等级**：`data_exposure.level`为E3或E4时，不得把相关决定说成事前计划
5. **探索性与确认性不混写**：`decision_status`为`data_driven`的分析，报告时标为探索性
6. **不重复做已做的质量检查**：规格里有`profile_verified`的项目，引用剖面报告，不另起炉灶重跑
7. **治理事项不自行裁决**：`items_needing_human_verification`里的内容，交给人，不要自行判断合规与否
8. **发现规格与实际数据不一致**：在决策日志里新增一行说明，不要直接修改基线

## 4. 下游交接契约

| 下游 | 接收的核心资料 | 它要完成的工作 |
|---|---|---|
| `social-science-experiment-designer`（上游） | 研究问题、假设、变量、拟用数据路径 | 完成实验设计、随机化、功效分析，其SOP与预注册文档再作为本skill的输入 |
| `quant-data-analysis` | 规格、变量字典、样本规则、分析计划、接触声明 | 按事前计划分析，记录偏离，做敏感性分析 |
| `sem-analysis-tutor` | 构念定义、测量项目、样本与数据结构 | 测量模型与结构方程分析指导 |
| `qualitative-research-methods` | 研究立场、访谈或观察计划、抽样逻辑、资料管理方案、各版本提纲 | 方法与分析过程指导 |
| `scale-research`（上游） | 构念清单 | 量表选择、翻译、改编，其结果回到变量字典 |
| `dissertation-peer-review` | 规格、决策日志、接触声明 | 评审时可据此核对研究者自由度与数据真实性 |

用户另有的其他skill或agent（例如专门的数据质量检查工具）也可以读规格，但**本skill不为不确定存在的接收方预设接口**；有明确接收方时再补充契约。

## 5. 版本与偏离

- 规格有`spec_version`；基线计划带日期
- 之后的调整只在`decision_log`里**追加**，不覆盖
- 最终报告里，对照基线说明：哪些分析按原计划做，哪些经记录调整，哪些是事后探索

## 6. 验收清单（交接前自检）

- [ ] 规格通过`validate_spec.py`，没有错误；每条警告都有处理或说明
- [ ] 数据接触等级和日期已写明，与`exposure_log.jsonl`一致
- [ ] 每个核心构念都有映射，每个变量都有`derivation`
- [ ] 排除规则标明了是否在看结果前确定
- [ ] 伦理与数据治理事项已列出，需人工核验的已标明
- [ ] 准备状态已填写，条件已列出
- [ ] 交接对象与交付内容已列在"Handoff & QA"
