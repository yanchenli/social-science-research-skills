# quant-data-analysis

> Quantitative data analysis assistant — actually running the analysis, and leaving a complete record.

**Version**: 1.0.0 ｜ **For**: business MS/PhD/DBA students and instructors ｜ **Size**: SKILL.md + 2 references + 4 scripts

**English** | [中文](README.md)

---

## The problem it solves

The skill pack was missing the middle segment:

| Stage | Skill |
|---|---|
| Design | `social-science-experiment-designer` |
| Scales | `scale-research` |
| SEM / PROCESS path analysis | `sem-analysis-tutor` |
| **Executing core statistics** (ANOVA / ANCOVA / regression moderation) | **this skill** |
| Writing Results | `stats-results-writer` |

It ships tested Python scripts; upload `csv` / `xlsx` / `sav` / `dta` and run.

---

## Three bottom lines

These exist not for appearances but so that the results **survive review**:

1. **Every analytic decision leaves a trace.** Who was excluded, why, by what rule, which test was used, why the test was changed. The scripts write this to a log, and the AI restates it in conversation.
2. **No "testing until significant".** Confirm the pre-registered analysis plan and follow it; anything outside the plan is labelled **exploratory**.
3. **Numbers come from executed code, not mental arithmetic or memory.** The AI must not compute a statistic by hand, and must not fabricate a "demonstration" result when no data file exists.

> The scripts were tested on **simulated data with known true values**, and cross-checked against
> `pingouin` and a hand-written numpy least-squares implementation.

---

## Workflow (six stages)

| Stage | Content | Output |
|---|---|---|
| 0. Context | Design type, variables, **pre-registered plan**, exclusion rules, data file | Analysis plan |
| 1. Screening | Missingness/duplicates, rule-based exclusions, cell sizes, outlier flagging | `screening_report.txt`, `exclusion_log.csv`, `data_clean.csv` |
| 2. Test selection | ANOVA / ANCOVA / regression by design | Rationale |
| 3. Run | Script execution | Result tables |
| 4. Diagnostics and sensitivity | Robustness; with/without outliers | Sensitivity report |
| 5. Delivery | Analysis record + result pack | Handoff to `stats-results-writer` |

### A key design in stage 0

If a `research_data_spec.json` already exists (produced by
[`research-data-preparation`](../research-data-preparation/)), **read it before asking anything**:

- `data_exposure.level` — how much of the data the researcher has seen
- `decision_status` — whether each decision was locked in advance or is data-driven
- `sample_rules` / `analysis_plan` — the pre-specified exclusion rules and analysis plan

Follow `pre_locked` items as planned; label `data_driven` analyses as exploratory; do not treat
`evidence_status: needs_verification` information as verified. **Do not re-ask what the spec already states.**

---

## The four scripts

| Script | Purpose |
|---|---|
| `screen_data.py` | Missingness and duplicates, rule-based exclusions with a log, cell sizes, outlier **flagging** by within-cell median/MAD (flags only, never removes) |
| `factorial_anova.py` | Type III ANOVA, Welch/robust methods, simple effects, effect sizes, Holm correction |
| `simple_slopes.py` | Simple slopes and Johnson-Neyman for regression moderation |
| `common.py` | Data loading (csv/xlsx/sav/dta), formatting |

```bash
python scripts/screen_data.py --file data.csv --dv satisfaction \
       --factors condition,gender --id participant_id \
       --exclude "attn != 1" --exclude "duration < 60" --outdir screen_out
```

**Flagging rather than removing outliers** is deliberate: removal is the researcher's decision. The
ideal is a rule fixed before analysis; if there is none, run both versions and report both.

---

## One frequently overlooked disclosure

After exclusions, the sample size must reconcile with the Methods section:

> total collected N → how many excluded by each rule → final N

Reviewers check this more often than people expect.

---

## Usage

```
Data collected, 2×2 between-subjects design, DV is purchase intention, with brand familiarity
as a covariate. Tell me whether anything is significant, and report in English.
```

The skill confirms the pre-registered plan first (writing it down at this point if none exists,
before touching the data), runs screening and reports cell sizes and outlier flags, then selects the
test (with a covariate → ANCOVA), runs it, performs sensitivity analysis, and returns a result pack
ready for `stats-results-writer`.

**When the interaction is significant**, it asks about the direction of the simple effects rather
than concluding on its own.

---

## Directory layout

```
quant-data-analysis/
├── SKILL.md                        six-stage workflow, three bottom lines, script usage
├── references/
│   ├── decision-guide.md           test-selection decision tree (including within-subject / mixed / multilevel advice)
│   └── analysis-log-and-handoff.md analysis-record format and handoff spec
└── scripts/
    ├── common.py                   data loading and formatting
    ├── screen_data.py              data screening
    ├── factorial_anova.py          factorial ANOVA and simple effects
    └── simple_slopes.py            simple slopes and Johnson-Neyman
```

---

## Boundaries

- **No SEM or mediation.** Use [`sem-analysis-tutor`](../sem-analysis-tutor/).
- **No Results prose.** Use [`stats-results-writer`](../stats-results-writer/).
- **No decisions on the researcher's behalf.** Whether to remove outliers, how to write up unstable significance — options and consequences are given; the researcher decides.
- **No ready-made scripts for within-subject / mixed / multilevel designs.** See section 6 of `decision-guide.md`; write the code and **validate it on simulated data first**.
- **No "demonstration" results.** Without a data file it will not present a fabricated result.

---

## Division of labour

- **SEM / PLS-SEM / PROCESS mediation** → [`sem-analysis-tutor`](../sem-analysis-tutor/). The boundary is the **method**, not whether you have data.
- **Results paragraphs** → [`stats-results-writer`](../stats-results-writer/).
- **Pre-analysis data plan and exposure audit** → [`research-data-preparation`](../research-data-preparation/).
- **Checking whether someone else's analysis is compliant** → the Stats Auditor in [`management-paper-reviewer`](../management-paper-reviewer/).

---

## Version

**1.0.0** — six-stage workflow, three bottom lines, four scripts validated on simulated data,
analysis-record and handoff specification.
