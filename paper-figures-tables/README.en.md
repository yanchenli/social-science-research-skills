# paper-figures-tables

> Making and checking academic figures and tables — getting them to look submission-ready and print-ready.

**Version**: 1.11.5 ｜ **For**: business MS/PhD students and instructors, and supervisors reviewing student drafts
｜ **Size**: SKILL.md + 5 references + 21 scripts

[中文](README.md) | **English**

---

## What problem it solves

Papers come back from reviewers not because the findings are wrong, but because the figures and tables
do not look like a submission:

- Tables use Word's default **full grid**; APA wants three rules only.
- Column widths are **equalised**, so long variable names wrap and numeric columns waste space.
- Statistical symbols are **not italicised** — *M*, *SD*, *t*, *p* should be; β and α should not.
- **Leading zeros** are the wrong way round: APA drops them for *r* / *p* / α, keeps them for *M* / *SD*.
- Figures have **no axis titles**, carry **gridlines**, or use a **pie chart** for shares.
- Colour-coded series become **indistinguishable in greyscale**.
- Exported figures are **screenshots** — not even 300 dpi.

None of this is a matter of scholarly judgement. It is **presentation convention**: there is a right
answer, and a machine can check it. This skill does two things: **generate to the convention**,
and **check against the same convention**.

---

## Core ideas

**1. Presentation only, never analysis.**
No test selection, no effect sizes, no verdicts on hypotheses. Those belong to the upstream skills;
redoing them here means two sets of conclusions that will eventually disagree.

**2. One rule set shared by generation and checking.**
Every layout value lives in `assets/profiles/*.json` with its source, its status, and a note on
*what the tool cannot do*. Generation and checking read the same file — otherwise you get
"generated to APA, checked against something else", the hardest class of bug to find.

**3. One layout, two renderers.**
SVG is emitted directly by a built-in renderer (zero dependencies); the same primitive list is
replayed through matplotlib into PDF/PNG. Geometry is computed once, so both outputs agree point for point.

**4. PASS is not compliance.**
Reports cover only the automated checks listed in the rule catalogue, and always end with the scope
that was **not** examined. Treating PASS as compliance is the most dangerous mistake this kind of tool invites.

---

## Coverage

### Tables

| Type | Notes |
|---|---|
| Three-line tables | Descriptives and correlations, reliability/validity, regression and hierarchical regression, mediation, moderation, moderated mediation, group comparisons, sample profile |
| Multi-panel tables | One grid with a header per panel (each panel's column spans must sum to the same number) |
| Landscape pages | Wide tables on a landscape page; the text measure becomes "page height − side margins" |
| Stacked cells | Several values in one cell, one per study (wide tables, multi-study comparisons) |

### Figures

| Type | Notes |
|---|---|
| Conceptual / measurement / structural models | Automatic layering, routing around intervening nodes, label collision avoidance; latent variables in a measurement model are forced to double-headed arrows |
| Interaction plots | Fitted interaction term; two lines at moderator mean ±1 SD with confidence bands |
| Estimate plots | Means or coefficients with 95% CIs (dot plot, not bars) |
| Multi-series line charts | N series with confidence bands; line style and markers distinguish series, never colour |
| (a)(b) panels | Small figures for one argument combined into one figure with one caption |

### Export and checks

- **Export**: SVG (vector) / PDF (vector, fonts embedded) / PNG, TIFF (300–600 dpi, no alpha channel)
- **Spec layer**: figure width, font size, line weight, rules, leading zeros, decimals, word breaks, overflow, table wider than the text measure
- **File layer**: DPI, transparency, font embedding and Type 3, glyph coverage, greyscale legibility, blank pages
- **Transcription layer**: every number in the table compared against the source PDF text layer
- **Auditing others' work**: screenshots, Excel charts, PDFs — and Excel chart data exported as a ready-to-run spec

---

## Workflow

```
Stage 0  Ask where it is going  →  settle a profile (APA 7 / Chinese journal / thesis / custom)
Stage 1  Choose the form        →  is the point a number, a direction, or a structure?
Stage 2  Generate               →  .docx / .svg, plus PDF and PNG when needed
Stage 3  Self-check (required)  →  spec layer + file layer + transcription layer
Stage 4  Deliver                →  with the "not examined" scope attached
```

**Audit mode** (someone else's table or figure): `audit_table.py` / `audit_figure.py` apply the same
criteria, and the report has the same structure as the generation path.

---

## Examples

```bash
# 1. An APA three-line table
python scripts/make_table.py spec.json table1.docx --tex

# 2. A conceptual model, exported to PDF, with a geometry audit
python scripts/make_diagram.py model.json fig1.svg --geometry fig1.geo.json --export pdf
python scripts/check_connections.py fig1.geo.json

# 3. A three-series line chart with confidence bands
python scripts/make_line_plot.py fig2a.svg spec.json --export pdf,png --dpi 600

# 4. Pre-delivery preflight
python scripts/preflight.py table1.docx fig1.pdf fig2a.png --json qc.json

# 5. Auditing what a student submitted
python scripts/audit_figure.py chart.xlsx shot.png --rebuild rebuild.json
python scripts/audit_table.py thesis_table.docx --profile apa7
```

Working specs are there to copy: `assets/table_specs/` holds five runnable examples, and
`references/format-specs.md`, `table-types.md`, `diagrams.md` and `line-plots.md` describe the structures.

---

## Layout

```
paper-figures-tables/
├── SKILL.md                Main workflow (stages 0–4) + hard constraints + boundaries
├── scripts/   21
│   ├── generators 6        make_table / make_diagram / make_interaction /
│   │                       make_estimate_plot / make_line_plot / make_panel
│   ├── checkers 6          check_figure / check_connections / check_numbers /
│   │                       preflight / audit_table / audit_figure
│   └── shared 9            svg_kit / line_core / svg_read / textmetrics /
│                           table_checks / profiles / qc / mpl_backend / selftest
├── references/ 5           format-specs / table-types / diagrams / line-plots / exhibit-selection
└── assets/
    ├── profiles/ 3         apa7 / zh-journal / thesis-template
    ├── table_specs/ 5      runnable example specs
    └── rules.json          60 rules, each with its source and its blind spot
```

**Dependencies**: `python-docx` is required; `matplotlib` (PDF/PNG), `PyMuPDF` (PDF checks) and
`Pillow` (raster checks) are optional — a missing one degrades to "not checked", never to a false pass.

---

## Boundaries

- **It does not judge content**: whether the chart type suits the claim, whether data sit on the wrong
  axis, whether the conclusion holds — all of that needs a human.
- **Table auditing reads `.docx` only**: a PDF carries no borders, merged cells or font sizes.
- **Auditing a whole paper PDF** can only tell you whether pages hold vector content and whether
  embedded images are sharp enough; chart type and axis titles need each figure exported and examined.
- **Not built**: radar charts, infographic-style conceptual frameworks, statistical estimation.

`selftest.py` is the skill's own gatekeeper: 114 checks, to be run after any script change.

---

## Handoff

| Direction | Skill | What passes over |
|---|---|---|
| Upstream | `stats-results-writer` | The numbers reported in the Results section |
| Upstream | `sem-analysis-tutor` | SEM loadings and path coefficients |
| Upstream | `quant-data-analysis` | Descriptive statistics and test results |
| Upstream | `social-science-experiment-designer` | Conceptual framework and hypotheses |
| Upstream | `literature-gap-synthesizer` / `systematic-review` | The columns of a literature table |
| Downstream | `stats-results-writer` / `discussion-conclusion-writer` | The prose that refers to the finished figure or table |

**Standalone use**: hand it a table's contents or a set of coefficients and it produces the finished
artifact. The skill **does not read files produced by the upstream skills** — it reads the spec you give
it, so it does not matter which software or format the upstream step used.

---

## Version

1.11.5 — the version in `SKILL.md` is the single source; reports read it from there.
