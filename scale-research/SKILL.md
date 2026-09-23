---
name: scale-research
description: >
  Guide graduate students (管理学、营销学、人力资源 MS/PhD) through the full
  academic scale-research workflow: clarifying constructs, discovering and
  evaluating measurement instruments, translating scales (EN↔ZH with
  back-translation), and adapting items to a target context. Use this skill
  whenever the user mentions any of: 量表, 问卷, scale, measure, instrument,
  Likert, 构念, construct, Cronbach, 信效度, 翻译量表, 改编量表, 回译,
  back-translation, 问卷翻译, 寻找量表, 量表搜寻, 研究方法, measurement tool,
  psychometric, AVE, CR, factor loading, survey items, 题项, or asks how to
  measure a psychological or organizational construct. Even if the request
  seems simple (e.g., "帮我找个量表"), trigger this skill — the structured
  workflow prevents common research errors.
version: 1.0.0
license: CC-BY-4.0
---

# AI-Assisted Scale Research — Full Workflow

## Core Principles (Remind the user at the start)

1. **AI proposes options; the researcher decides.** Never let the AI make final
   judgement calls on construct selection, scale choice, or item wording.
2. **Triangle verification.** Every piece of bibliographic information the AI
   provides (author, year, journal) must be verified in a real database before
   citation.
3. **Your data, your stats.** Reliability/validity numbers in a thesis must
   come from the student's own sample — not from the AI's own knowledge.

---

## Quick-Start: Which stage to enter?

Ask the user (or infer from context) where they are right now:

| User's situation | Enter at |
|---|---|
| Only has a vague phenomenon in mind | Stage 1 — Concept Clarification |
| Knows the construct name, needs a scale | Stage 2 — Scale Discovery |
| Already has candidate scales, needs comparison | Stage 2B — Scale Evaluation |
| Has a scale, needs ZH translation | Stage 3 — Translation |
| Has a translated scale, needs adaptation | Stage 4 — Adaptation |

---

## Stage 1 — Concept Clarification

**Goal:** Convert a vague, colloquial description into searchable academic constructs.

### Prompt Template 1-A — Construct Identification

```
## Role
You are a research methods expert familiar with [management / marketing /
organizational behavior / consumer behavior].

## My Research Phenomenon
I am a graduate student in [field]. I want to study this phenomenon:
[Describe in your own words — include: who, in what context, what
psychological state or behavioral outcome]

## Please complete these four tasks:

1. [Construct Mapping] List 3–5 academic constructs that best match my
   description. For each, provide:
   Chinese name | English term | One-sentence definition | Match level (High/Med/Low)

2. [Disambiguation] For the 2–3 most easily confused constructs, use the
   format "If you want to measure X, choose A; if Y, choose B" to help me
   decide.

3. [Search Keywords] For each candidate, list 3–5 English search terms
   (synonyms, abbreviations) and Chinese equivalents.

4. [Recommendation] Which construct do you think I most likely want to
   measure? Explain your reasoning. (Final decision is mine.)

Present task 1 as a table; tasks 2–4 as bullet points.
```

### Prompt Template 1-B — Construct Precision (after construct is named)

```
The construct I want to study is: [name (EN + ZH)]

Please:
1. [Authoritative Definitions] 2–3 most-cited definitions; format:
   "Definition" (Author, approx. year — I will verify the original text)
2. [Dimension Debates] Main competing dimension structures with representative
   scholars for each.
3. [Boundary Warnings] 2–3 constructs most easily confused with this one;
   one sentence on the difference each.
4. [Context Fit] How has this construct been used in
   [your research context]? Any special caveats?
```

### ✅ Human Checkpoint A — before moving to Stage 2
- [ ] Run the keywords in WOS / CNKI / Google Scholar and confirm hits exist
- [ ] Read 2–3 recent reviews to confirm construct understanding direction
- [ ] Document your research context (industry, group, culture) — needed in every later stage
- [ ] Verbally confirm construct choice with supervisor

---

## Stage 2 — Scale Discovery & Evaluation

**Goal:** Find the most authoritative, best-fitting scale(s) for your construct.

### Prompt Template 2-A — Finding Classic Scales (starting from scratch)

```
## Role
You are a measurement expert familiar with [management / psychology] scales.

## Task
I want a scale measuring "[construct name]". My research context:
[research subjects] + [industry/setting] + [country/region]

Please provide the following (note: all citations are leads for me to verify —
no need to repeat this caveat in your output):

## Output format — strict table:
| Scale name/abbr | Developer & year | Dimensions / Items | Original sample | Original α | Why recommended |

List 3–5 scales, prioritising:
① High citation count (note order of magnitude: e.g., "1000+")
② Validated in Chinese or Asian contexts
③ Existing Chinese version publicly available

After the table, one paragraph: which scale deserves first attention for my
context, and why.
```

> ⚠️ **Hallucination hotspots:** author name misspellings, year off by 1–3
> years (mixing original paper with validation studies), α values stated as
> "typical" rather than from a specific study. Verification method: Google
> Scholar → "Author surname + year + construct keyword". Not found = hallucination.

### Prompt Template 2-B — Multi-Scale Comparison (when you already have candidates)

```
## Role
You are a rigorous research methods reviewer.

## My situation
- Construct: [name]
- Research context: [detailed]
- Max questionnaire items: [e.g., total ≤ 60]
- Need Chinese version: [yes / no / can translate]

## Candidate scales (fill what you know; write "unknown" for gaps)
Scale A: name= developer/year= dimensions= items= original context= α=
Scale B: ...

## Comparison table (please produce):
| Evaluation dimension | Scale A | Scale B | Scale C |
Dimensions: ① Construct fit ② Context similarity ③ Measurement quality
④ Chinese-context use history ⑤ Practicality

End with your recommendation and 2–3 things I still need to check myself.
```

### Scale Quality Quick-Reference

| Metric | Minimum | Good | Notes |
|---|---|---|---|
| Cronbach's α | ≥ 0.70 | ≥ 0.80 | Original sample only; you must re-check in your own data |
| Factor loading | ≥ 0.50 | ≥ 0.70 | CFA standardised; EFA values carry less weight |
| AVE | ≥ 0.50 | ≥ 0.60 | Convergent validity; may need to find from Chinese validation studies |
| CR | ≥ 0.60 | ≥ 0.80 | Alongside α for multi-dimensional scales |

### ✅ Human Checkpoint B — before moving to Stage 3
- [ ] Locate the *original development article* (not just a citing article) in WOS / Google Scholar
- [ ] Download it; find the full item list in the Appendix or Tables
- [ ] Search "scale name + China / Chinese sample" for local validation evidence
- [ ] Discuss candidate scale with supervisor and get sign-off
- [ ] Check copyright: commercial scales (e.g., MBTI, Gallup Q12) require permission

---

## Stage 3 — Translation & Semantic Verification

**Goal:** Produce a Chinese version with semantic equivalence — not literal word-for-word translation.

See `references/translation-guide.md` for detailed translation standards and the four special requirements for Likert-scale items.

### Prompt Template 3-A — Professional Initial Translation (EN → ZH)

```
## Role
You are a bilingual expert in English psychometrics and Chinese questionnaire
design, with extensive experience localising English scales.

## Translation task
Scale name: [name] | Construct: [name]
Research subjects: [e.g., full-time employees at Chinese internet companies]
Scale format: [e.g., 5-point Likert, 1 = strongly disagree, 5 = strongly agree]

Original English items:
[Paste numbered items, one per line]

## Requirements
1. Language: colloquial, natural, suitable for self-administered questionnaire;
   no "translationese"
2. Consistency: keep sentence structure consistent within each dimension
   (e.g., all start with "在工作中，我……")
3. Reverse items: mark with (R) on the right

## Output format — strict table:
| # | English original | Chinese translation | Reverse (R)? | Translation notes |

Notes column: fill ONLY when (a) you handled an ambiguity or cultural gap in a
non-literal way, or (b) you are uncertain and flag for my review.

After the table, 3–5 sentences on the overall translation strategy used.
```

### Prompt Template 3-B — Back-Translation Analysis

*Get a human back-translator (not AI) first, then use this prompt.*

```
## Task
Analyse semantic equivalence of scale translation.

Original English items: [paste]
Chinese translation: [paste]
Human back-translation to English: [paste]

## Analysis — produce this table:
| # | Original EN | Back-translated EN | Consistency | Issue location | Revision suggestion |

Consistency levels: ✅ High | ⚠ Minor deviation | ❌ Clear divergence

For ⚠ and ❌ items, diagnose root cause:
A. Problem in Chinese translation → provide revised Chinese wording
B. Ambiguity in original English → note it; suggest I consult the source authors' usage notes

Final summary: high-consistency items / total items; overall translation quality rating.
```

### ✅ Human Checkpoint C — before moving to Stage 4
- [ ] Obtain a **human** (non-AI) independent back-translation — this is a peer-review audit point
- [ ] Revise all ⚠ and ❌ items; re-check after revision
- [ ] Cognitive interview: 3–5 target respondents read every item aloud; confirm understood as intended
- [ ] Document translation procedure (who, what changed, why) for the Methods section
- [ ] Verify final item scoring directions (positive / reverse) are correct

---

## Stage 4 — Adaptation & Finalisation

**Goal:** Minimum necessary edits to fit the target context — not arbitrary rewrites.

See `references/adaptation-guide.md` for the adaptation safety boundary chart and pre-test requirements.

### Prompt Template 4-A — Assess Adaptation Necessity

```
## Role
Research methods expert with deep knowledge of scale adaptation norms.

## My situation
Original scale: [name] | Original context: [description]
My research context: [detailed]

Sample items from original (2–3): [paste]
My initial reasons for adaptation: [your judgement]

## Please:
1. Are my reasons sufficient? Any adaptation necessity I missed?
2. For the sample items above, classify each proposed change as
   "safe adaptation" or "high-risk adaptation" and explain the risk.
3. If I make [describe extent] of changes, what extra validation steps and
   Methods-section disclosures are required?
4. Is there another existing scale that already fits my context better,
   reducing adaptation scope? (Provide 1–2 leads for me to verify.)
```

### Prompt Template 4-B — Execute Contextual Adaptation

```
## Adaptation task
Scale: [name]
Original context: [description] → Target context: [description]

## Adaptation rules (strictly follow)
1. Preserve the core measurement intent of each item
2. Minimum necessary changes only; mark changes with 【brackets】
3. Context-word substitution table: [e.g., "顾客"→"粉丝", "门店"→"直播间"]
4. If an item is completely inapplicable in the target context, mark
   "Suggest delete" with reason

## Original items: [paste with numbers]

## Output format:
| # | Original item | Adapted item (changes in 【】) | Change type | Notes |

Change types: A-Context word substitution / B-Sentence structure adjustment /
C-Cultural adaptation / D-Suggest delete

After the table: items retained ___, deleted ___; main change areas;
suggested Methods-section wording for these changes.
```

### Prompt Template 4-C — Simulated Expert Content Validity Review

```
## Role
You are an anonymous peer reviewer for a leading [management / marketing]
journal with extremely high standards for measurement.

## My scale
Construct: [name and definition]
Research subjects: [description]
Adaptation notes: [brief summary of what you changed]

Items for review: [paste complete list]

## Review dimensions (check each):
1. Does each item accurately tap the core construct definition?
   (Any items "off-target" or "out of scope"?)
2. Item wording problems: double negatives, ambiguity, leading questions,
   overly abstract, overly specific?
3. Dimension coverage: are all dimensions adequately represented?
   Any over- or under-represented?
4. Adaptation validity: in your view, did the changes alter the original
   measurement intent?

Write in the voice of reviewer comments; flag item numbers needing revision.
End with an overall content-validity verdict and the top 1–2 improvement priorities.
```

### ✅ Human Checkpoint D — final gate
- [ ] Submit adaptation plan to supervisor for sign-off
- [ ] 2–3 domain experts (not AI) rate each adapted item for content validity
- [ ] Pre-test: N ≥ 30 minimum (N ≥ 100 recommended); run EFA to confirm factor structure
- [ ] Save complete adaptation log for Methods section
- [ ] All α / AVE / CR / loading values in thesis must come from YOUR data analysis

---

## Supplementary: Documentation & Writing Assistance

For scale information cards and Methods-section draft wording, see
`references/writing-templates.md`.

---

## Common Pitfalls Summary

| Pitfall | Symptom | Correct practice |
|---|---|---|
| AI hallucination | Author / year / journal not found in database | Verify every citation in WOS or GS before use |
| Trusting AI's α | Copying AI-provided α into thesis | All reported statistics must come from your own data |
| Skipping human back-translation | Using AI back-translation as proof of quality | Human back-translator is required; reviewers check this |
| Over-adaptation | Deleting dimensions, reversing item direction, no pre-test | Beyond word substitution → pre-test + EFA + justify in Methods |
| Copyright violation | Using MBTI, Gallup Q12 without permission | Check copyright; commercial scales need written authorisation |
| Skipping supervisor | Full workflow done without supervisor input | Check in at construct selection AND adapted-scale finalisation |
