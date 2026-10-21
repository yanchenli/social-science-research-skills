# research-data-preparation

> Research data preparation and pre-analysis decision management — write down the decisions that will affect your conclusions before you see the outcome data.

**Version**: 1.0.0 ｜ **For**: business MS/PhD/DBA students and instructors ｜ **Size**: SKILL.md + 10 references + 6 scripts + 1 workbook template

**English** | [中文](README.md)

---

## The problem it solves

Most methods training starts at "how to analyse" and skips the earlier question: **to what extent may
a researcher flexibly adjust the design and analytic decisions after having seen the data?**

For primary data the risk is choosing exclusion rules and tests after the fact. For secondary data the
risk is subtler — the data already exists, so time windows, sample restrictions and thresholds can all
be "adjusted" after the results are known.

The skill does four things, not just a plan document:

1. **Data exposure audit** — how much of the data the researcher has seen (E0–E4)
2. **Decision status management** — whether each key decision was pre-locked, locked after exposure, data-driven, or undetermined
3. **Readiness judgement** — whether the study can proceed to data acquisition (not a verdict on the data's quality)
4. **Handoff specification** — a workbook plus a machine-readable spec that downstream skills and other agents can read

---

## Core principle

**Before seeing outcome data, write down the decisions that will affect the conclusions; later changes are not forbidden, but they must be recorded.**

> What it does **not** do: redesign the study, power analysis, statistical analysis, actually field
> the survey or scrape the data, access unauthorised data, or reach legal and ethical conclusions
> (these are identified and marked "requires human verification").

---

## Workflow (seven stages)

| Stage | Content |
|---|---|
| 0. Question and data-path diagnosis | Ask first: **can existing data answer the research question?** Do not default to collecting new data |
| 1. Sources, feasibility, exposure audit | E0–E4 grading; three-layer source feasibility check; limited data profile |
| 2. Shared design and pre-analysis decisions | Sample rules, variable dictionary, analysis plan |
| 3. Path-specific preparation | Primary quantitative / primary qualitative / secondary structured (conditional branches) |
| 4. Ethics, governance, quality assurance | DMP, personal data, authorisation and compliance |
| 5. Freeze, version, risk register | Lock the spec version; register known risks |
| 6. Handoff and acceptance | Workbook + `research_data_spec.json` to downstream |

### A counter-intuitive reminder for stage 0

Ask a question that comes before "how to collect": **can existing data answer the research question?**
What would need supplementing? What are the cost and access barriers?

Do not default to collecting new data — this is the step students skip most often, at the highest cost.

### Stage 1: exposure levels E0–E4

**Do this before touching the data.** Establish what the researcher has seen, inspected or tested, and grade it.

---

## The six scripts

| Script | Purpose |
|---|---|
| `profile_dataset.py` | Read-only data profile: missingness, quantiles, category counts, risk signals |
| `mde_fixed_sample.py` | Minimum detectable effect at a fixed sample size (two-group / correlation / anova) |
| `validate_spec.py` | Validate a spec against the JSON Schema, reporting every error |
| `make_workbook.py` | Generate the nine-sheet data workbook (`.xlsx`) |
| `workbook_to_spec.py` | Workbook → machine-readable spec (`research_data_spec.json`) |
| `common.py` | Data loading and shared functions |

### A design point that must be stated in advance

> ⚠️ **Running the profile script is itself a data exposure.**

The script requires the current level to be declared, upgrades it after the run, and appends to
`exposure_log.jsonl`. To blind outcome variables, they must be specified with `--outcome-vars`
**before the run** — "blinding" afterwards is too late. The skill therefore requires telling the
researcher this before running anything.

---

## Lightweight mode

For small student projects with a single path, run only **stages 0, 2 and 5**, filling three workbook
sheets: 说明 (Notes), Variable Dictionary, and Decision & Deviation Log.

Use the full mode when secondary data, personal information, multiple sources, or external
registration are involved.

---

## The nine workbook sheets

```
Notes | Construct Map | Variable Dictionary | Sample & Rules | Data Acquisition
Analysis Plan | Ethics & DMP | Decision & Deviation Log | Handoff & QA
```

The workbook is for humans to fill in; `workbook_to_spec.py` converts it into the machine-readable
`research_data_spec.json`, which [`quant-data-analysis`](../quant-data-analysis/) reads before
starting work — **that is what "handoff" means concretely here**.

---

## Usage

```
I want to use a transaction dataset from an e-commerce platform. I have the data but
haven't started analysing it.
```

The skill runs the exposure audit first (which fields have you seen? have you looked at
distributions?), then profiles the data at structure level with the outcome variable **blinded**,
gives a feasibility judgement and risk register, and produces the data plan and spec.

**It will not decide whether the data is usable** — it supplies auditable evidence for you to fill
in `evidence_status`.

---

## Directory layout

```
research-data-preparation/
├── SKILL.md                                seven-stage workflow, lightweight mode, script usage
├── references/
│   ├── core-plan-and-decisions.md          data paths and purposes, E0–E4 exposure levels, decision status
│   ├── primary-quantitative.md             primary quantitative: survey/experiment build spec
│   ├── primary-qualitative.md              primary qualitative: interview logistics, recording, governance
│   ├── secondary-structured.md             secondary structured data: source verification, windows, restrictions
│   ├── governance-and-dmp.md               ethics, data governance, DMP
│   ├── handoff-and-schema.md               handoff format and schema documentation
│   ├── research_data_spec.schema.json      JSON Schema for the machine-readable spec
│   └── examples/                           three example specs (primary quant / primary qual / secondary)
├── scripts/                                six scripts (see above)
└── templates/
    └── data_workbook_blank.xlsx            blank nine-sheet data workbook
```

---

## Boundaries

- **No redesigning the study.** Use [`social-science-experiment-designer`](../social-science-experiment-designer/).
- **No statistical analysis.** Use [`quant-data-analysis`](../quant-data-analysis/) or [`sem-analysis-tutor`](../sem-analysis-tutor/).
- **No legal or ethical conclusions.** These are identified and marked "requires human verification".
- **No verdict on whether the data is "good".** It provides auditable evidence; the judgement belongs to the researcher and the committee.
- **No unauthorised data access.** It will not field the survey or scrape data for you.

---

## Division of labour

- **Design not yet settled** → [`social-science-experiment-designer`](../social-science-experiment-designer/).
- **Design settled, data in hand, analysis next** → [`quant-data-analysis`](../quant-data-analysis/), which reads the `research_data_spec.json` this skill produces and avoids re-asking.
- **Logistics of qualitative data collection** → `primary-qualitative.md` here complements stage 2 of [`qualitative-research-methods`](../qualitative-research-methods/).

---

## Version

**1.0.0** — seven-stage workflow, E0–E4 exposure audit, decision status management, six scripts,
nine-sheet workbook and machine-readable spec.
