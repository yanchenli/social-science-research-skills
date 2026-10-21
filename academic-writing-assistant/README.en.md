# academic-writing-assistant

> Academic writing assistant — guiding the Introduction and Literature Review.

**Version**: 1.0.0 ｜ **For**: business MS/PhD students and instructors ｜ **Size**: SKILL.md + 4 references

**English** | [中文](README.md)

---

## ⚠️ First, the boundary: this is a writing scaffold, not ghostwriting

This is the skill that **produces manuscript prose directly**, which makes it the easiest one to misuse.

**What it does**: helps you make the **chain of argument** explicit — how a research gap is argued,
how hypotheses are derived step by step from premises, how literature is integrated by theme
rather than listed paper by paper, and how paragraphs and sections connect.

**What it does not do**: it does not decide whether the gap really exists or whether the
contribution is novel enough. **Originality is your and your supervisor's call**; the skill
has no capacity to assess it.

**The guardrails it carries**: every citation is emitted in red as `[待核实: Author, Year]`
with a verification checklist at the end; missing statistics are left as `[请填入真实数据]`
placeholders — **no numbers are invented**.

> **Please confirm your own institution's rules on AI use in theses.** Policies are tightening
> and vary widely; journals' disclosure requirements for AI-assisted writing are inconsistent.
> Whether to use it, how to use it, and whether to disclose it is a decision for you and your supervisor.

---

## The problem it solves

Introduction and Literature Review are the hardest chapters to start because the difficulty is
**logic**, not language:

- How do you argue a gap without forcing it? "Nobody has studied this" is not an argument.
- How are hypotheses derived? Jumping straight from theory to H1 is instantly visible to reviewers.
- How do you avoid a literature review that is just a pile of summaries — one paper per paragraph?
- How do paragraphs connect? How do sections transition?
- How do Chinese and English journal conventions differ, including length?

The skill turns this **structural knowledge** into six executable stages plus phrase banks.

---

## Core principle

**AI assists the writing; the researcher owns the content.**

The AI handles **structure, logic, language and format**; the researcher confirms the direction
of the argument, verifies citations, and supplies the research context.

> ⚠️ **Important**: every bibliographic detail the AI produces must be verified in a real database
> (Google Scholar, Web of Science, …) before use. The red `[待核实: Author, Year]` tag is
> **an action item, not decoration**.

---

## Workflow (six stages)

| Your situation | Enter at |
|---|---|
| Only a topic or an idea | **Stage 1** — pre-writing planning |
| Have a reading list, unsure how to organise it | **Stage 2** — literature mapping and framework |
| Have a framework, starting the Introduction | **Stage 3** — Introduction |
| Have a framework, starting the Literature Review | **Stage 4** — Literature Review |
| Have a draft needing polish, rewriting or expansion | **Stage 5** — revision |
| Have complete content, need Word output | **Stage 6** — document generation |

### Stage 1 — pre-writing planning

Confirm topic, research question, target journal type, discipline, writing language, corpus size
and word limit, then fix the positioning with a one-sentence frame:

```
This study examines the effect of [IV / phenomenon] on [DV / outcome],
focusing on [context / boundary condition],
taking [theoretical lens] as its perspective,
to address the gap in [existing research].
```

### Stage 2 — literature mapping

Three grouping dimensions (by theme / by chronology / by finding), plus **five gap types with phrases**:

| Gap type | Example phrasing |
|---|---|
| Theoretical | `Prior research has not theorized...` |
| Contextual | `Little attention has been paid to X in the context of Y...` |
| Mechanistic | `The underlying mechanism remains unclear...` |
| Boundary | `When and for whom X affects Y is largely unexplored...` |
| Methodological | `Previous studies relying on... may have overstated...` |

### Stage 3 — Introduction

Written as a **funnel**, with guidance and English phrasing at each layer:

```
1. Macro hook (1–2 sentences)        ← why the phenomenon matters
2. What is known (2–4 sentences)     ← the state of the literature
3. The gap (1–2 sentences)           ← but / however / remains unclear
4. Purpose and contribution (2–3)    ← what this study does
5. Roadmap (optional)
```

The gap paragraph is **the critical layer**. The skill insists on acknowledging prior work
("although prior research has contributed..., it remains unclear whether...") rather than
dismissing the field.

### Stage 4 — Literature Review

Each subsection follows a five-part structure (definition → historical arc → core findings →
controversies and limits → transition), with a side-by-side contrast between
**critical** and **descriptive** reviewing:

| Descriptive (avoid) | Critical (prefer) |
|---|---|
| "Smith (2020) found that X affects Y." | "Smith (2020) demonstrated X→Y, but used a student sample, limiting generalizability." |
| One paper per sentence | Integrate several papers by theme |
| Only what was done | What it contributed, and where it is limited |

It also includes a **hypothesis-derivation template**: premise 1 (theory) → premise 2 (evidence) → therefore H1.

### Stage 5 — revision

A six-dimension diagnostic (structural completeness / gap argument / hypothesis logic / literature
integration / academic register / transitions), then repair strategies for four common problems —
"hypotheses falling from the sky" and "summary piles" being the two most typical.

### Stage 6 — document generation

Outputs `.docx` with built-in style specifications (Times New Roman 12 pt / SimSun 小四, double or
1.5 spacing, A4 with 2.54 cm margins), document structure, and annotation rules (citations in red,
data placeholders highlighted).

---

## Directory layout

```
academic-writing-assistant/
├── SKILL.md                          six-stage workflow, gap identification, hypothesis derivation
└── references/
    ├── writing-templates-en.md       English templates and phrase bank
    ├── writing-templates-zh.md       Chinese templates and phrase bank
    ├── gap-phrases.md                gap phrasing (EN / ZH)
    └── transition-phrases.md         paragraph transitions and connectives (EN / ZH)
```

---

## Usage

```
Topic: how the linguistic concreteness of livestream hosts affects purchase intention
Research question: through what mechanism, and under what boundary conditions?
Theory: construal level theory (CLT)
Context: Chinese livestream commerce platforms
Language: English
Target: journal article
References: 32 so far
Write the Introduction (~800 words) and the Literature Review.
```

The skill confirms the positioning, returns a hierarchical review framework for approval, then
writes the Introduction as a funnel and each subsection in the five-part structure.
**Every citation is tagged `[待核实: Author, Year]`**, with a checklist at the end; missing data
is left as `[请填入真实数据]` rather than invented.

Afterwards, run [`academic-citation-auditor`](../academic-citation-auditor/) over the red-flagged citations.

---

## Boundaries

- **No invented statistics.** Where the hook needs a real figure, a placeholder is left for you to fill.
- **No unverified citations.** All citations are flagged — this is a hard constraint, not a suggestion.
- **No first person.** Academic register throughout.
- **No originality assessment.** "Is this gap real", "is this contribution new" is beyond it.
- **Conventions vary by journal.** What it provides is general academic convention; follow your target journal's guide for specifics.
- **Thesis vs journal article**: length and detail differ greatly (journal Introduction ≈ 400–800 words; thesis often 1,500–3,000 characters). The skill adjusts to the type you specify.

---

## Division of labour with stats-results-writer

Both produce manuscript prose, but **different sections under different conventions — do not mix them**:

| Skill | Section | Basis |
|---|---|---|
| `academic-writing-assistant` | Introduction, Literature Review | Literature logic and theoretical derivation |
| [`stats-results-writer`](../stats-results-writer/) | Results | Your own software output |

---

## Version

**1.0.0** — six-stage workflow, five gap types, funnel Introduction, critical-review contrast table,
hypothesis-derivation template, four repair strategies, bilingual templates and phrase banks,
`.docx` style specification.
