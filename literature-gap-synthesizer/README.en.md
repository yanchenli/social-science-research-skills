# literature-gap-synthesizer

> Systematic literature synthesis and gap analysis — diagnose before you write.

**Version**: 1.0.0 ｜ **For**: business MS/PhD/DBA students and instructors ｜ **Size**: SKILL.md + 2 references

**English** | [中文](README.md)

---

## The problem it solves

"Has anyone done this?" and "what is actually missing here?" are questions every topic-selection
stage must answer — yet most people search a few papers and conclude "little research exists".

This skill turns a scattered pile of literature into a map that shows **where the consensus is,
where the conflicts are, and where the gap is**, then converts the gap into a defensible
positioning statement.

---

## Core principle

**Diagnose first, write second.**

This is the earliest and most frequently skipped step in the pipeline. Its output plugs directly
into stage 1 of [`academic-writing-assistant`](../academic-writing-assistant/), so the Introduction
can be written immediately afterwards.

> ⚠️ **No fabricated references.** Every source must come from a real search or from material the
> user supplied. Anything unverifiable is marked `[待核实]`, and a pass through
> [`academic-citation-auditor`](../academic-citation-auditor/) is recommended before finalising.

---

## Workflow (five stages)

| Stage | Goal |
|---|---|
| 1. Scope and search | Narrow a fuzzy topic into a searchable scope; build a search strategy |
| 2. Synthesis matrix | Organise into a matrix that can be compared across rows |
| 3. Thematic clustering and gap diagnosis | Read the structure: consensus, conflict, untouched corners |
| 4. Gap evaluation and positioning | Pick one candidate gap; write the positioning statement |
| 5. Delivery and handoff | Document + handoff to the next skill |

### Stage 1: decompose the query into three dimensions

Do not search with one broad keyword. Decompose into **construct × theory × method/context**:

```
Brand equity × digital context:
- Construct: brand equity, brand asset, customer-based brand equity
- Theory: signalling theory, self-congruity theory, social identity theory
- Method/context: social media, short video platform, cross-cultural
```

Search **batch by construct**, not all keywords at once — batching makes it easier to see the
research density and the blank spots within each sub-area.

### Stage 2: eight fields in the synthesis matrix

Author (year) ｜ type (with journal tier) ｜ theoretical basis ｜ core constructs/variables ｜
method ｜ sample and context ｜ core finding (in your own words, not copied) ｜ limitations

Under 20 papers, a Markdown table is enough; beyond that, and if you need to sort and filter, use `.xlsx`.

**Construct consistency checking** is the point of this stage: is the same word measuring different
things across papers? Do different papers set contradictory boundary conditions for the same theory?
Flag inconsistencies explicitly — do not smooth them over, because they are the raw material for stage 3.

### Stage 3: distinguish two kinds of gap first

This distinction comes from Sandberg & Alvesson (2011, *Organization*):

| What you found | Closer to |
|---|---|
| A relationship nobody has tested in a given context | gap-spotting (application) |
| Findings conflict and nobody explains why | gap-spotting (confusion) |
| A clearly relevant corner nobody has touched | gap-spotting (neglect) |
| An assumption the field takes for granted may be wrong | **problematization** |

Neither is superior, but the choice sets the **ambition and difficulty** of the research story, and
determines how the contribution is later framed.

---

## An easily overlooked inclusion criterion

**Exclude undergraduate and master's theses.**

The reasoning is stated in the skill: not peer reviewed, and defence standards are looser. Skip them
at the search stage, do not include them in the matrix, and do not use them as evidence even if
found. Doctoral theses may be included (committee defence brings them close to peer review).

This matters in practice — many "nobody has studied this" impressions come from searching only
low-quality sources.

---

## Usage

```
I'm working on brand anthropomorphism and want to know what's actually missing.
I have 18 papers, list attached.
```

The skill builds the matrix, runs the construct-consistency check, clusters consensus / conflict /
untouched corners, proposes 2–4 candidate gaps, evaluates them on novelty, interestingness,
feasibility, contribution potential and practical value, then writes the positioning statement:

```
This study examines the effect of [IV / phenomenon] on [DV / outcome],
focusing on [context / boundary condition],
taking [theoretical lens] as its perspective,
to address the gap in [existing research].
```

This template is **identical** to stage 1.2 of `academic-writing-assistant` — copy it straight across.

---

## Directory layout

```
literature-gap-synthesizer/
├── SKILL.md                        five-stage workflow, search strategy, gap evaluation
└── references/
    ├── gap-taxonomy.md             three gap-spotting subtypes and problematization (with sources);
    │                               content-dimension gap types with bilingual examples
    └── journal-tiers.md            cross-field journal tier list (top / excellent / credible / practitioner),
                                    including a list of disallowed publishers
```

---

## Boundaries

- **No fabricated references.** Unverifiable items are marked `[待核实]`; never fill in authors, years or journals from memory.
- **Does not decide for the researcher.** Which gap to pursue, and how to tell the theoretical story, is the researcher's call.
- **Does not smooth over conflicts.** Contradictions and inconsistent operationalisations are presented as they are.
- **Delivers in stages.** With a large corpus, do not generate everything at once — show each stage before continuing.
- **Practitioner journals** (HBR, MIT Sloan Management Review, …) may support the practical framing of an applied paper, but must not carry the academic argument.

---

## Division of labour

- **Literature already clear, just needs writing up** → [`academic-writing-assistant`](../academic-writing-assistant/) stage 2, which has a lightweight gap-classification step. This skill does the earlier, heavier work.
- **Gap settled, need an experiment or a scale** → [`social-science-experiment-designer`](../social-science-experiment-designer/) / [`scale-research`](../scale-research/).
- **Suspect the sources themselves** → [`academic-citation-auditor`](../academic-citation-auditor/).
- **Contribution unclear later** → [`discussion-conclusion-writer`](../discussion-conclusion-writer/) stage 2 maps back to the positioning.

---

## Version

**1.0.0** — five-stage workflow, three-dimension query decomposition, eight-field synthesis matrix,
gap-spotting/problematization diagnosis, journal tier reference.
