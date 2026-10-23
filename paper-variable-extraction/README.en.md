# paper-variable-extraction

> Variable operationalisation extraction — turning variable information scattered across body text, appendices and footnotes into a reusable codebook.

**Version**: 1.0.0 ｜ **For**: business MS / PhD / DBA students and faculty ｜ **Size**: SKILL.md + 9 reference files + 1 script

**English** | [中文](README.md)

---

## The problem it solves

In an empirical paper, variable information is never in one place:

- Conceptual definitions sit in the theory section, items in the appendix, reliability in a Table 1
  footnote, the response scale in half a sentence in the method section;
- In multi-study papers the same construct uses different scales in Study 1 and Study 3;
- In meta-analyses, a moderator's "operationalisation" is not items at all but **a coding rule**.

The result: re-reading the source while writing the literature review, coding from memory during
meta-analysis, and two people extracting the same paper producing two different codebooks.

This skill fixes *what to extract, at what granularity, and how to record what is missing*, and produces
two directly usable outputs: **a Markdown report** and **an Excel variable table** whose columns are
consistent across papers (so meta-analytic coding is mechanical).

---

## Core principles

**Verbatim, never invented.**

| Principle | Meaning |
|---|---|
| **Items and stimuli are copied verbatim** | No polishing, no paraphrasing. When the paper gives only sample items, copy them and label them "sample items only" |
| **Missing means "not reported"** | `NA` in Excel. **Never fabricate items, reliability values, APA references or indicator codes** |
| **Internal inconsistencies are reported side by side** | Body text says "nine items were adapted", appendix says "(5 items)" — record both, do not pick one for the author |
| **Determine the method first, then extract** | Using the wrong branch's ruler produces feedback that reads professionally and is entirely off-target |

### Eight method branches, eight rulers

| Branch | Tell-tale signs | What to extract |
|---|---|---|
| A Experimental | Random assignment, stimuli, manipulation checks | Verbatim stimuli, manipulation procedure, manipulation checks |
| B Survey | Scales administered, Cronbach's α, Likert | Every item, scale anchors, reliability, scale source |
| C Secondary data | Databases, panels, public statistics | Database / table / indicator code / years, cleaning and aggregation rules |
| D Qualitative | Interviews, grounded theory, ethnography, coding | Sampling rationale, coding scheme, inter-coder reliability, theme tree |
| E Literature-based theory building | Search strings, papers included, paragraphs coded | Search strategy, coding procedure, saturation criteria |
| F Meta-analysis | Effect sizes, I², funnel plots, fail-safe N | Effect sizes and moderator coding (produces an EffectSizes table) |
| G Computational measurement | Self-trained classifiers, fine-tuning, AUC, human comparison | Training data and splits, model performance, agreement with humans |
| H Analytical modelling | Utility functions, equilibrium, first-order conditions | Setup, assumptions, equilibrium, propositions, comparative statics |

> **G vs C**: C asks where the data came from; G asks how the measuring instrument was built.
> **H vs E**: E induces propositions from literature; H deduces them from assumptions.

---

## Workflow

| Step | Content |
|---|---|
| 0 | **Obtain the full text** (including scanned PDFs: render to images → re-render dense tables at ≥350 DPI before reading → cross-check any number appearing in more than one place) |
| 1 | **Determine the method for each study separately** (a multi-study paper may combine qualitative + survey + experiment + archival data) |
| 2 | **Build the study map** (how many studies, each one's goal, the progression logic, method distribution, samples) |
| 3 | **Extract variables and hypotheses** (IV / DV / mediator / moderator / control, with conceptual definitions and operationalisations) |
| 4 | **Produce two outputs**: Markdown report + Excel variable table |

### The script and its checks

`scripts/export_codebook.py` turns the extracted JSON into Excel, validating structure before export:

```bash
python3 scripts/export_codebook.py codebook.json --validate    # validate only
python3 scripts/export_codebook.py codebook.json out.xlsx      # validate and export
python3 scripts/export_codebook.py codebook.json --mermaid     # print the study-map source only
```

The validator catches: values outside the controlled vocabularies; variable-name casing that would break
cross-study merging; Mermaid edges pointing at undefined nodes; an item count with an empty item table;
reliability values outside 0–1; an analytical model missing assumptions or propositions; computational
measurement missing a model description.

> **Dependency**: the script needs `openpyxl` (`pip install openpyxl`). Everything else is plain text.

---

## Example

```
Extract every variable in this paper and how each was operationalised — I want to see which items each
scale used and what the reliability was. Also give me an Excel file for meta-analytic coding.
```

The skill determines the method branch, builds the study map, extracts each variable (verbatim items with
translation, response scale, reliability, source), and produces both the Markdown report and a
fixed-column Excel file — with a gap list naming everything the paper does not report.

---

## Boundaries

- **Does not replace close reading.** It structures information; judging the argument remains your job.
- **Does no statistics.** It records what the paper reports; it does not recompute or infer.
- **What the paper does not report is recorded as absent.** The report carries an explicit
  "missing information" list rather than a plausible-looking number.
- **Scanned PDFs are read as images, not OCR'd.** Dense tables must be zoomed before reading — measured
  case: reading a structural-model table at full-page scale produced four wrong path coefficients, all
  corrected only after re-rendering at 420 DPI.
- **The Excel column set grows across versions.** New fields are appended after the fixed block; older
  files remain readable, but check column names before merging across versions.

---

## Related skills

| Need | Use |
|---|---|
| Map a literature and locate gaps | [`literature-gap-synthesizer`](../literature-gap-synthesizer/) |
| Run a systematic review and meta-analysis | [`systematic-review`](../systematic-review/) |
| Analyse your own survey or experimental data | [`quant-data-analysis`](../quant-data-analysis/) |
| Write a scale-development paper | [`scale-research`](../scale-research/) |
| Review a paper (rather than extract from it) | [`management-paper-reviewer`](../management-paper-reviewer/) |

---

## Version history

**1.0.0** — Eight method branches (experimental / survey / secondary / qualitative / review /
meta-analysis / computational measurement / analytical modelling); multi-study map with Mermaid
visualisation; Markdown + Excel dual output; JSON structural validation with controlled vocabularies;
scanned-PDF reading workflow; explicit gap list and side-by-side recording of internal inconsistencies.
