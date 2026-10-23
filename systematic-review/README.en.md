# systematic-review

> Systematic review and meta-analysis — turning "impressions from a few papers" into reproducible evidence synthesis.

**Version**: 1.1.0 ｜ **For**: business MS / PhD / DBA students and faculty ｜ **Size**: SKILL.md + 5 reference files + 3 scripts

**English** | [中文](README.md)

---

## The problem it solves

Most first attempts at a literature review are, in substance, **abstracts strung together**: there is a
theme and there are citations, but no reproducible search or screening process.

Three concrete consequences:

1. **"How did you find these papers?" has no answer** — no search string, no databases, no exclusion criteria.
2. **The conclusion cannot be checked** — no reader can rerun the process and see whether the same set emerges.
3. **Quantitative synthesis is done wrong** — effect sizes averaged without conversion, or r and d pooled together.

This skill breaks the review into seven auditable steps and supplies criteria and tools at each.

---

## Core principles

**Reproducibility first; conclusions second.**

| Principle | Meaning |
|---|---|
| **Search and screening must be rerunnable** | Search strings, databases, date ranges, exclusion reasons and counts — all on the record |
| **Paradigm before statistics** | Business research has two incompatible meta-analytic traditions; picking wrong gets the method section challenged outright |
| **Effect sizes must be on one scale** | r, d, OR and z cannot be averaged directly |
| **No numbers without support** | When heterogeneity and publication bias cannot be estimated (k < 5), do not run a meta-analysis — write a narrative synthesis and say why |

### The split that matters most in business research

| | **Hunter–Schmidt (psychometric)** | **Hedges–Olkin (inverse-variance random effects)** |
|---|---|---|
| Core operation | Correct for measurement error: ρ = r / √(r_xx·r_yy) | No correction; pool observed effect sizes |
| Weighting | By sample size N | By 1/variance |
| Main interval | Credibility interval | Confidence interval + prediction interval |
| Dominant fields | OB / HRM / industrial-organisational psychology | Strategy / finance / accounting / economics |

> Marketing and consumer behaviour **use both**. The deciding evidence is **what the target journal has
> published in the last three years**, not personal preference.

---

## Workflow

| Stage | Content |
|---|---|
| 0 | **Three splits**: review type / input completeness / statistical paradigm |
| 1 | Structuring the research question (PICOC or equivalent) |
| 2 | Search strategy (databases, strings, grey literature, inclusion and exclusion criteria) |
| 3 | Screening and PRISMA 2020 flow diagram (with exclusion reasons and counts) |
| 4 | Coding and risk-of-bias assessment (AMSTAR 2 / ROBIS / a business-specific seven-dimension list) |
| 5 | Effect-size extraction and conversion |
| 6 | Synthesis, heterogeneity, publication bias |
| 7 | Reporting (PRISMA 2020 checklist, reproducible appendix) |

### Three scripts

| Script | What it does |
|---|---|
| `scripts/meta.py` | Conversion and pooling across five effect-size types (r / d / OR / t / path coefficient); REML / DL / Paule–Mandel; HK correction; Egger and the PET–PEESE decision chain |
| `scripts/hs_meta.py` | Hunter–Schmidt psychometric meta-analysis: reliability correction, N weighting, credibility intervals, variance decomposition |
| `scripts/prisma_flow.py` | PRISMA flow diagram: stage counts, exclusion-reason totals validated (errors out on mismatch) |

All three use only the Python standard library — nothing to install.

---

## Example

```
I'm meta-analysing "brand community participation → purchase intention" and have 42 papers.
Can I run this at that k? How do I put the effect sizes on one scale?
Should I test for publication bias?
```

The skill determines the paradigm (both are used in marketing; the target journal's practice decides),
checks whether the effect sizes can be converted to a common scale, assesses what heterogeneity and
publication-bias tests are meaningful at k = 42, and states which tests would be uninformative there.

---

## Boundaries

- **No meta-analysis below k = 5.** Heterogeneity and publication bias cannot be estimated; switch to a
  systematic review with narrative synthesis, and say so.
- **PROSPERO only accepts health outcomes.** Business reviews pre-register on OSF or AsPredicted — that is
  the registry's scope, not a gap in the workflow.
- **Deliberately does not run trim-and-fill.** Under heterogeneity its correction direction is unreliable
  and can produce a false "corrected" conclusion; the skill uses a PET–PEESE decision chain instead and
  requires the uncorrected estimate to be reported.
- **Does not do MASEM.** When structural equation modelling must be combined with meta-analysis, use a
  dedicated tool (e.g. `metaSEM` in R).
- **The scripts produce intermediate quantities, not final numbers.** Before writing up, recompute in R
  (`metafor` / `psychmeta`) and check that the two agree.

---

## Related skills

| Need | Use |
|---|---|
| Map a literature and locate gaps (no synthesis) | [`literature-gap-synthesizer`](../literature-gap-synthesizer/) |
| Choose a journal and submit | [`journal-submission`](../journal-submission/) |
| Extract variables and operationalisations from included papers | [`paper-variable-extraction`](../paper-variable-extraction/) |
| Analyse your own primary data | [`quant-data-analysis`](../quant-data-analysis/) |

---

## Version history

**1.1.0** — Three splits (including the business paradigm split); PRISMA 2020 exclusion validation;
five-type effect-size conversion with back-transformation; REML / DL / Paule–Mandel; HK correction and
prediction intervals; Egger + PET–PEESE decision chain; Hunter–Schmidt script; business-specific
seven-dimension bias list; OSF pre-registration guidance.

**1.0.0** — First release.
