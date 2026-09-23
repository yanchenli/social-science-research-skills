# Writing Templates for Scale Documentation

## Scale Information Card Prompt

Use this after finalising your scale to generate a standardised record card.

```
Please generate a standardised scale information card based on the following
information (for my research archive, not for direct citation — I will verify
all bibliographic details from the original paper):

[Paste everything you have collected; write "To verify" for unknowns]

Card structure needed:
① Basic info: name, developer(s), year, original language
② My version: translation/adaptation notes
③ Dimension structure and item distribution (include reverse-item numbers)
④ Scoring: Likert points; direction of each item
⑤ Original psychometric summary (mark all figures as "To verify")
⑥ Methods-section paragraph (~120 words; mark all placeholder values with
   [INSERT: your own α] etc.)
```

---

## Methods Section — Scale Description Templates

### Template A: Adopted existing Chinese scale

> 本研究采用[原作者, 年份]开发、[汉化作者, 年份]汉化的[构念名称]量表，
> 共[X]题，采用[X]点Likert计分（1 = [锚点], [X] = [锚点]）。
> 该量表在中国情境下已得到广泛验证（[近期引用文献]），具有良好的信效度。
> 本研究样本中，该量表的Cronbach's α为[X]，验证性因子分析结果表明
> 各题项标准化因子载荷介于[X]至[X]之间，模型拟合指数满足可接受标准
> （CFI = [X], RMSEA = [X]）。

### Template B: Translated from English with back-translation procedure

> 本研究采用[原作者, 年份]开发的[构念名称]量表（[X]题，[X]点Likert计分）。
> 量表原版为英文，本研究采用翻译-回译程序进行中文化处理（Brislin, 1970）：
> 研究者首先将英文题项翻译为中文，随后由未接触原版的双语学者独立进行
> 回译，经对比修订后，通过认知访谈（N = [X]）确认题意理解无误。
> 本研究样本中，该量表的Cronbach's α为[X]。

### Template C: Adapted scale (context modification)

> 本研究以[原作者, 年份]的[构念名称]量表为基础，参照[方法依据]，
> 针对[目标情境]将部分情境措辞进行调整（具体改编内容详见附录X）。
> 改编后量表共[X]题，采用[X]点Likert计分。经[N]名[群体描述]预测试，
> 探索性因子分析确认因子结构与原量表一致。
> 正式调研样本中，该量表Cronbach's α为[X]。

---

## Reverse-Scored Item Reminder

Before data collection, confirm:
- Reverse items are correctly identified (marked R in your item list)
- Data processing code reverses their values before calculating scale score
- Cronbach's α is computed on the corrected (post-reversal) scores

Standard reverse-coding formula: `reversed_score = (max_point + 1) - raw_score`
E.g., for 5-point scale: reversed = 6 − raw

---

## Checklist: Methods Section Completeness

- [ ] Scale name, original developer, year cited correctly
- [ ] Number of items stated
- [ ] Number of Likert points and anchor labels stated
- [ ] Reverse items identified
- [ ] Translation/adaptation procedure described (if applicable)
- [ ] Pre-test sample described (if adaptation performed)
- [ ] Your sample's α reported (NOT from AI or from original paper)
- [ ] CFA fit indices reported (if CFA was run)
- [ ] Factor loadings range reported
- [ ] AVE and CR reported (if relevant to discriminant validity argument)
