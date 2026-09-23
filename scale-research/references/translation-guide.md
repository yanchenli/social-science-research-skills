# Scale Translation Reference Guide

## Four Special Requirements for Likert-Scale Item Translation

Unlike general translation, questionnaire items must satisfy:

1. **Logical pairing with response anchors.** Item stems must be declarative
   statements (not yes/no questions) that pair naturally with anchors like
   "完全不同意 — 完全同意". Avoid interrogative sentences.

2. **Consistent sentence structure within dimensions.** Items in the same
   subscale should share a sentence template (e.g., all starting with "在工作中，我……")
   so respondents do not experience format-switching cognitive load.

3. **Clear reverse-scored wording.** In Chinese, the placement of "不" matters
   significantly ("我从不……" vs "我不……" carry different implications). Mark
   reverse items with (R) and review them extra carefully in back-translation.

4. **Avoid double negatives, culturally opaque expressions, and overly
   academic phrasing.** Test every item against the question: would a typical
   respondent in my target group understand this immediately?

---

## Back-Translation Procedure (Brislin 1970 Standard)

```
Step 1 — Forward Translation
  The AI (or bilingual researcher A) translates EN → ZH
  Goal: meaning equivalence, natural Chinese expression

Step 2 — Independent Back-Translation
  A different bilingual person (NOT the original translator, NOT AI)
  translates ZH → EN without seeing the original English items

Step 3 — Comparison & Gap Analysis
  Use Prompt 3-B to systematically compare original EN vs back-translated EN
  Classify each item: ✅ High | ⚠ Minor | ❌ Clear divergence

Step 4 — Revision
  Revise Chinese items where ⚠ or ❌; repeat Steps 2–3 if gaps are large

Step 5 — Cognitive Interview
  3–5 target respondents read each item aloud
  Ask: "What do you think this question is asking?"
  Revise any items where understanding differs from intent
```

> **Why human back-translation cannot be replaced by AI:**
> AI knows the source language and is biased toward producing back-translations
> that look like the original. A human who has only seen the Chinese version
> will reveal genuine ambiguities in the translation.

---

## Methods Section Wording — Translation Procedure

Template for reporting translation in thesis/paper Methods section:

> 本研究采用翻译-回译程序对量表进行中文化处理（Brislin, 1970）。
> 首先，研究者将英文原版题项翻译为中文；随后，由一名未接触英文原版的
> 双语研究者将中文译文回译为英文，并与原版逐题比对。对存在语义偏差的
> 题项进行修改后，通过认知访谈（N = [X]）确认目标被试能准确理解各题意图，
> 最终确定正式量表。

Replace bracketed items with your own data before submitting.

---

## Common Translation Errors

| Error type | Example | Fix |
|---|---|---|
| Translationese | "我置身于一种情感劳动的状态中" | "工作中我不得不压抑真实感受" |
| Interrogative item | "你是否会在客户面前假装情绪？" | "面对客户时，我会假装某种情绪" |
| Double negative | "我不是不会在意同事的看法" | "我在意同事对我的看法"(R) |
| Inconsistent structure | Mixed 我……/在工作中，我……/有时我…… | Standardise to one template |
| Overly abstract | "我的情感真实性受到职业规范的制约" | "工作要求我表现出与内心不符的情绪" |
