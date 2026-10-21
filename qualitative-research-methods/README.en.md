# qualitative-research-methods

> Qualitative research methods — rigour is not statistical significance, it is trustworthiness.

**Version**: 1.0.0 ｜ **For**: business MS/PhD/DBA students and instructors ｜ **Size**: SKILL.md + 8 references

**English** | [中文](README.md)

---

## The problem it solves

The quantitative track has a full toolkit; the qualitative track often has only "my supervisor said
to change it". This skill supplies the whole chain:

tradition selection → sampling and instrument design → coding and analysis → trustworthiness check → Findings writing.

It is the only **non-statistical** path in the pack, and the only one that treats **quotations** as the core evidence.

---

## Core principle

**In qualitative research, rigour is not statistical significance — it is trustworthiness.**

Design, collection and analysis are often interleaved — especially in grounded theory's "theoretical
sampling", where emerging analysis determines who you interview next. So the stages here are an
**entry map**, not a mandatory sequence.

> ⚠️ **Quotations are to qualitative work what numbers are to quantitative work.**
> Coding, analysis and Findings must rest on the transcripts or field notes the user supplies:
> **never invent plausible-sounding interview content, and never "polish" a participant's words
> into something prettier.**

The AI handles structure — selecting the tradition, building instruments, drafting a coding
framework, checking rigour criteria, drafting and diagnosing Findings. The interpretive judgement,
coding decisions and theory building are the researcher's work.
**Subjective involvement is part of the method, not noise to be eliminated.**

---

## Workflow (five stages)

| Stage | Content | Key output |
|---|---|---|
| 1. Paradigm and tradition | Applicability of five traditions; the three grounded-theory schools | Tradition + version, with reasons |
| 2. Sampling and data collection design | Purposive / extreme-case / theoretical / snowball sampling; interview guides, focus groups, observation records | Sampling plan + instruments |
| 3. Coding and analysis | Thematic analysis, grounded-theory coding, Gioia data structure, cross-case analysis | Coding framework + theme structure |
| 4. Trustworthiness | Lincoln & Guba's four criteria; the trace checklist before Findings | Trustworthiness statement |
| 5. Findings writing | Tradition-specific conventions; quotation use; bilingual quotation translation | Findings text |

### Stage 1: the five traditions

| Tradition | Shape of research question |
|---|---|
| Case study (especially Eisenhardt-style theory building) | "How does X unfold in this context?" — inducing new theory from cases |
| Grounded theory | No existing theoretical account of a process; let theory emerge from the data |
| Phenomenology | What an experience is *like* for the person living it; not causal |
| Ethnography | How a group's or organisation's culture and daily practice work; requires sustained immersion |
| Narrative research | How people use storytelling to make meaning and construct identity |

In business and management, **case study and grounded theory** are the two most common routes; when
the user has no strong preference, judge from these two first.

**The three grounded-theory schools must be distinguished**: Glaser & Strauss (theory *emerges*),
Strauss & Corbin (more structured coding), Charmaz (constructivist — theory is *constructed*). Their
assumptions about coding steps and the researcher's role differ, so **once chosen, stage 3 must use
the same version throughout; do not mix them mid-project**.

### Stage 4: the four trustworthiness criteria

Credibility (triangulation / member checking / peer debriefing), transferability (thick description),
dependability (audit trail), confirmability (reflexivity statement).

The skill checks whether each is **substantively addressed**, rather than merely named.

---

## Findings writing, one volume per tradition

This is one of the skill's most valuable designs — qualitative Findings have no single template, and
conventions differ sharply by tradition:

| Reference | Applies to |
|---|---|
| `references/findings-01-general.md` | General conventions: quotation use, verbatim principle, placeholder protocol |
| `references/findings-02-thematic.md` | Thematic analysis narrative |
| `references/findings-03-gioia.md` | Gioia methodology: first-order concepts / second-order themes / aggregate dimensions + data structure |
| `references/findings-04-grounded-theory.md` | Grounded theory: categories, properties, dimensions, saturation |
| `references/findings-05-case-study.md` | Case study: cross-case comparison, proposition development |
| `references/findings-06-other-traditions.md` | Phenomenology, ethnography, narrative research |

---

## Usage

```
I have 14 interview transcripts on how middle managers understand digital transformation.
I'm using the Gioia methodology and have coded twice. Write the Findings, in English.
```

The skill first checks that the tradition and version match the coding steps, and that sampling and
saturation are accounted for, then reads the `findings-03-gioia.md` conventions, diagnoses the
existing coding table item by item (are the second-order themes genuinely more abstract than the
first-order concepts, or just renamed?), and drafts the Findings in Gioia's narrative structure.

**It will not invent a quotation.** Missing ones are left as skeletons with `[引语待补：P?，支持××]` placeholders.

---

## Directory layout

```
qualitative-research-methods/
├── SKILL.md                              five-stage workflow, five traditions, coding, trustworthiness
└── references/
    ├── qualitative-traditions.md         assumptions, applicability and exemplars of the five traditions
    ├── coding-and-rigor.md               coding methods, Lincoln & Guba's four criteria, trace checklist
    ├── findings-01-general.md            general writing conventions and quotation principles
    ├── findings-02-thematic.md           thematic-analysis Findings
    ├── findings-03-gioia.md              Gioia-methodology Findings
    ├── findings-04-grounded-theory.md    grounded-theory Findings
    ├── findings-05-case-study.md         case-study Findings
    └── findings-06-other-traditions.md   phenomenology / ethnography / narrative Findings
```

---

## Boundaries

- **It does not code for the researcher or make interpretive judgements.** It may propose a draft framework, flag possible themes, draft and diagnose Findings — but whether a theme holds, and which reading to take, is the researcher's call.
- **No invented quotations.** See the core principle.
- **Saturation is not a number.** Sample size needs a saturation rationale (e.g. "the last few interviews produced no new themes"), not an arbitrary figure.
- **It does not pretend to be NVivo.** Qualitative analysis is entirely possible without dedicated software — tables and documents work, and the skill can annotate, group and draft a framework directly on the text you supply.

---

## Division of labour

- **Topic and literature gap** → [`literature-gap-synthesizer`](../literature-gap-synthesizer/).
- **Introduction / Literature Review** → [`academic-writing-assistant`](../academic-writing-assistant/).
- **Discussion and contribution** → [`discussion-conclusion-writer`](../discussion-conclusion-writer/).
- **Ethics and data governance at the design stage** → `primary-qualitative.md` in [`research-data-preparation`](../research-data-preparation/) covers interview logistics, recording and governance.

---

## Version

**1.0.0** — five-stage workflow, five qualitative traditions, the three grounded-theory schools,
six Findings writing volumes, the four trustworthiness criteria.
