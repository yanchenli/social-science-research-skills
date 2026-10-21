# sem-analysis-tutor

> Step-by-step SEM coaching — walks you through structural equation modelling the way a supervisor would.

**Version**: 1.0.0 ｜ **For**: management, marketing and consumer behaviour graduate students ｜ **Size**: SKILL.md + 12 references

**English** | [中文](README.md)

---

## The problem it solves

The real difficulty for a beginner doing SEM is not "which button to click":

- Not knowing whether to use CB-SEM or PLS-SEM, and mixing the two indicator systems
- Indicators failing (loadings below .70, AVE below .50) with no idea what to do
- A screen full of numbers, not knowing which must be reported and which can be omitted
- Being unsure whether "this result counts as supporting my hypothesis"

The skill breaks SEM into a fixed **step0 → step7** sequence, **advancing one step at a time**:
you report the result, it diagnoses, and only then does the next step open.

---

## Core principle

**Coach like a supervisor — one step at a time, never dumping everything at once.**

> ⚠️ **Data integrity**: every number in the report must come from the software output the user
> supplies. **No estimating, fabricating or substituting any value.**

### Five interaction rules

1. **Strictly stepwise** — one step per turn; stop and wait for the user's result
2. **Two tracks kept apart** — CB-SEM and PLS-SEM use entirely different indicator systems; **never mixed**
3. **Beginner-friendly** — each technical term gets a one-sentence intuition on first appearance (e.g. "AVE can be read as: on average, how much of the construct's variance the items explain")
4. **Anomalies are not avoided** — when an indicator fails, discuss a repair or state the limitation honestly; **never route around it**
5. **No vague wording** — p = .06 is reported as not significant; "marginally significant" and "approaching significance" are **forbidden**

---

## Standard operating procedure

```
Step 0 → Needs assessment and method diagnosis
Step 1 → Data check (descriptives, missingness, normality)
Step 2 → Common method bias (CMB)
Step 3 → Measurement model (outer model / CFA)
Step 4 → Structural model and hypothesis testing (inner model)
Step 5 → Mediation / moderation (where applicable)
Step 6 → Full academic report
```

Step 0 **cannot be skipped** — the skill first learns your context (number of constructs, sample
size, software, target journal) before recommending a method. Requests for code up front are
deflected back to Step 0.

---

## Two tracks

| | CB-SEM | PLS-SEM |
|---|---|---|
| Software | lavaan (R) / AMOS / Mplus | SmartPLS / seminr (R) |
| Indicators | CFI, TLI, RMSEA, SRMR and other fit indices | Outer loadings, AVE, CR, HTMT, Q² |
| Coverage | step3/step4 run both tracks in parallel, with FL-degradation notes | same, including Stone-Geisser Q² |

Advanced scenarios with dedicated chapters:

- **Moderated mediation** — full flow for both CB-SEM and PLS-SEM
- **Latent × latent moderation** — Mplus LMS, plus the modsem alternative
- **Multi-group analysis (MGA)** — CB-SEM measurement-invariance nesting tests + PLS-SEM MICOM/MGA

---

## Directory layout

```
sem-analysis-tutor/
├── SKILL.md                       SOP, five interaction rules, reporting conventions
└── references/
    ├── step0-diagnosis.md         user profiling (two rounds of questions) and method diagnosis
    ├── step1-data-check.md        data-check code and criteria
    ├── step2-cmb.md               CMB tests and anomaly handling
    ├── step3-measurement.md       measurement-model indicator list (both tracks)
    ├── step4-structural.md        structural-model code, indicators, hypothesis check (incl. Q²)
    ├── step5-medmod.md            mediation / moderation (with routing table)
    ├── step5-modmed.md            moderated mediation, full flow
    ├── step5-modmed-mplus.md      latent × latent moderation (LMS + modsem)
    ├── step6-report.md            report checklist, bilingual reporting conventions
    ├── step7-mga.md               multi-group analysis: invariance nesting + MICOM/MGA
    ├── thresholds.md              quick-reference thresholds for every indicator
    └── error-handling.md          anomaly strategies and limitation templates
```

---

## Usage

```
I'm running an SEM with 5 constructs on 320 responses, using SmartPLS,
targeting a Q2 journal. Here's my data file.
```

The skill will not hand you code first; it runs the Step 0 diagnosis (reflective or formative,
sample-to-construct ratio, mediation/moderation), then moves to Step 1. At the end of each step it
states exactly what result to feed back, and waits.

---

## Reporting conventions

- Standard LaTeX statistical symbols: $\beta$, $\chi^2$, $R^2$, $p$, $t$, $z$, $f^2$, $\alpha$, $\rho_A$
- Objective academic register, third person passive
- Decimal places matching the software output (usually 2–3)
- Failing indicators stated honestly under Limitations, never omitted
- Hypothesis summary as a Markdown table with explicit ✅ Supported / ❌ Not Supported

---

## Division of labour with stats-results-writer

**This skill helps you *do* the analysis** — read the data, judge indicators, handle anomalies,
decide the next step. If the analysis is already done and you only need APA paragraphs, use
[`stats-results-writer`](../stats-results-writer/).

The typical combined sequence: `sem-analysis-tutor` through step0–step5 → `stats-results-writer`
for the Results → back to `sem-analysis-tutor` step6 for the report check.

---

## Boundaries

- **It will not call a failing indicator passing.** It discusses repairs or coaches you to state the
  limitation honestly — it does not help you hide it.
- **All numbers must come from your software output.** Estimating, fabricating or substituting is forbidden.
- **It does not fabricate data.** If the data cannot support the hypothesis, the direction is
  "how to report honestly", not "how to tweak until significant".

---

## Version

**1.0.0** — complete step0–step7 SOP, CB-SEM/PLS-SEM dual track, 12 references (including three
advanced chapters: moderated mediation, Mplus LMS, MGA/MICOM).
