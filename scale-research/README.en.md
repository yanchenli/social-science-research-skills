# scale-research

> Scale research workflow — from a fuzzy phenomenon to a questionnaire you can field.

**Version**: 1.0.0 ｜ **For**: management, marketing and HRM MS/PhD ｜ **Size**: SKILL.md + 3 references

**English** | [中文](README.md)

---

## The problem it solves

Scale research has four stages, and each has its own classic failure:

| Stage | Classic failure |
|---|---|
| Clarifying the construct | Measuring something other than what you meant (construct confusion) |
| Finding the scale | Ending up with a second-hand citation whose α was copied from another paper |
| Translating the scale | Literal translation produces "translationese" participants cannot parse |
| Contextual adaptation | Adapting so much that it no longer measures the original construct |

The skill chains the four stages into one workflow and **inserts a human checkpoint between
each pair** — it will not skip the parts that require your judgement.

---

## Core principles (stated at the start of every run)

1. **AI proposes options; the researcher decides.** Construct choice, scale selection and item wording are yours.
2. **Triangle verification.** Every bibliographic detail the AI gives you must be verified in a real database before it is cited.
3. **Your data, your statistics.** Reliability and validity figures in the paper must come from **your own sample**, never from the AI.

---

## When to use it

- You have a vague phenomenon but no idea which academic construct it maps to
- You know the construct name and need to find a scale
- You have candidate scales and need to compare them
- You have an English scale and need a Chinese version
- You have a Chinese version and need to adapt it to a new context (e.g. from "store" to "livestream")

---

## Workflow (four stages + four human checkpoints)

| Stage | Content | Templates |
|---|---|---|
| **1. Construct clarification** | Turn the colloquial description into a searchable academic construct: mapping, disambiguation, keywords, recommendation with reasons | 1-A construct identification, 1-B construct refinement |
| **2. Scale search and evaluation** | Find 3–5 candidates, ranked by citations, Chinese-context validation, and availability of an existing Chinese version | 2-A classic scale search, 2-B multi-scale comparison |
| **3. Translation and semantic validation** | Not literal translation but semantic equivalence; includes reverse-scoring markers and translator notes | 3-A professional forward translation, 3-B back-translation analysis |
| **4. Contextual adaptation and finalisation** | Minimum necessary change; edits marked 【】 with the type of change noted | 4-A necessity assessment, 4-B execution, 4-C simulated expert content-validity review |

### The four checkpoints (the skill stops you)

- **Checkpoint A** (before stage 2): keywords findable in WOS/CNKI/Google Scholar; read 2–3 recent reviews; record the context; confirm the construct choice verbally with your supervisor
- **Checkpoint B** (before stage 3): find the **original development paper** (not just papers citing it); download it and locate the full item set in the appendix; search "scale name + China / Chinese sample" for local validation; **check copyright** (MBTI, Gallup Q12 and similar commercial scales require a licence)
- **Checkpoint C** (before stage 4): **a human does independent back-translation** — reviewers check this; fix every ⚠ and ❌ item; cognitive interviews (3–5 target participants reading each item aloud); document the translation process
- **Checkpoint D** (final gate): supervisor sign-off; 2–3 domain experts rate content validity; pilot N ≥ 30 (N ≥ 100 recommended) with EFA; keep a complete adaptation log

---

## A particularly useful part: the hallucination hotspots list

The skill names the **hallucination hotspots** specific to scale literature:

> Misspelled author names; years off by 1–3 (confusing the original paper with a validation study);
> α reported as "typical" rather than taken from a specific study.

**How to check**: Google Scholar → "author surname + year + construct keyword". Not found = hallucinated.

This matters especially for students now using AI to find literature — the rate of fabricated
scale citations is high.

---

## Directory layout

```
scale-research/
├── SKILL.md                        four-stage workflow, 4 human checkpoints, hallucination hotspots
└── references/
    ├── translation-guide.md        translation standards and the 4 special requirements for Likert items
    ├── adaptation-guide.md         adaptation safety boundary map and pilot requirements
    └── writing-templates.md        scale information card and Methods-section writing templates
```

---

## Usage

```
I need to measure "brand attachment" among young consumers in tier-1 Chinese cities.
I need a Chinese version, and the whole questionnaire should stay under 60 items.
```

The skill clarifies the construct first (distinguishing brand attachment from brand affect and
brand loyalty), returns a comparison table of candidate scales, then moves to translation — and at
Checkpoint C explicitly requires you to **find a human back-translator**; AI back-translation
cannot stand in as evidence of quality.

---

## Common pitfalls (built-in table)

| Pitfall | Symptom | Correct practice |
|---|---|---|
| AI hallucination | Author/year/journal not found in any database | Verify each item in WOS or Google Scholar before citing |
| Trusting AI-supplied α | Copying the AI's α into the paper | Every reported statistic must come from your own data |
| Skipping human back-translation | Using AI back-translation as proof | Human back-translation is mandatory; reviewers check |
| Over-adaptation | Dropping dimensions, reversing the scoring direction, no pilot | Anything beyond wording substitution needs a pilot + EFA + disclosure in Methods |
| Copyright infringement | Using MBTI or Gallup Q12 without a licence | Check copyright; commercial scales need written permission |
| Skipping the supervisor | Running the whole process without checking in | Confirm at two points: construct choice, and adaptation sign-off |

---

## Boundaries

- **Do not substitute AI back-translation for human back-translation.** The skill repeats this because it is a real review checkpoint.
- **Do not cite the α / AVE / CR the skill shows you.** Those are reference values only; the paper needs your own data.
- **Adaptation has a safety boundary.** The skill classifies changes as "safe" or "high-risk"; anything beyond wording substitution needs extra validation steps and disclosure in Methods.

---

## Version

**1.0.0** — four-stage workflow, 4 human checkpoints, hallucination hotspot list, adaptation safety
boundary map, 6-pitfall comparison table.
