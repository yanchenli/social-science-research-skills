# discussion-conclusion-writer

> Discussion and Conclusion assistant — turning "here is what we found" into "so what".

**Version**: 1.0.0 ｜ **For**: business MS/PhD/DBA students and instructors ｜ **Size**: SKILL.md + 1 reference

**English** | [中文](README.md)

---

## The problem it solves

This is where papers most often trail off: the results are reported, but the theoretical
contribution stays vague. One of the most common reasons reviewers reject a paper is
"the contribution is unclear" — not "the method is flawed".

This skill fills the one gap in the writing chain:

| Section | Skill |
|---|---|
| Introduction / Literature Review | `academic-writing-assistant` |
| Results | `stats-results-writer` |
| **Discussion / Conclusion** | **this skill** |

Together the three close the paper from opening to end.

---

## Core principle

**The Discussion is not a retelling of the Results; it answers "so what".**

Structurally it is the Introduction's inverted funnel: the Introduction narrows from a big question
to specific hypotheses; the Discussion reverses it — starting from the specific finding and widening
out to theory, practice and the field.

> ⚠️ The AI builds the structure and supplies the frameworks; **whether the finding matters, and
> how the contribution story is best told, is the researcher's judgement. The AI does not decide for you.**

---

## Workflow (five stages)

| Stage | Goal | Output |
|---|---|---|
| 1. Synthesise results and revisit the positioning | Put the findings back into "why did we do this" | A one-sentence synthesis (not "H1 supported, H2 not") |
| 2. Articulate the theoretical contribution | Turn "we found X" into "what this means for theory" | Contribution statement |
| 3. Practical and managerial implications | Translate into something useful, not platitudes | Implications paragraph |
| 4. Boundary conditions, limitations, future research | Honest without undermining yourself | Limitations and future directions |
| 5. Conclusion and delivery | Echo the opening hook | Conclusion + `.docx` |

---

## Three citable frameworks

Not a self-invented checklist — all with sources:

- **Whetten (1989), seven questions** — What's new / So what / Why so / Well done / Done well / Who cares / Why now. Originally for evaluating theoretical contributions; it works equally well as a self-check: whichever question you cannot answer is where the contribution is still unclear.
- **Corley & Gioia (2011), the 2×2** — originality (incremental vs revelatory) × utility (scientific vs practical). Incremental contributions are just as valuable, but you need to know which cell you are in, because the framing differs.
- **Bartunek & Rynes (2010)** — practical implications must say: for whom, what specifically, and why this recommendation follows from *this* finding.

---

## A very useful self-check

Paste your implications paragraph onto **a completely different paper**. Does it still read smoothly?

If yes, it is too generic — it did not grow out of your own findings.

The same test applies to limitations and future research: "future work should test this with a
larger sample" fits any paper and is therefore worth little. A good future direction is
"because we found X, question Y now becomes worth studying".

---

## Usage

```
The Results are done: H1 supported, H2 not, and the H3 moderation is only significant
among women. The gap I claimed in the Introduction was "no one has studied brand
anthropomorphism in a B2B context".
Write the Discussion, in Chinese.
```

The skill first maps results against the claimed positioning (was the gap actually filled?
partially? any unexpected findings?), then works through the stages.
**The H2 failure is not hidden** — unexpected results are often the most discussable part.

---

## Directory layout

```
discussion-conclusion-writer/
├── SKILL.md                              five-stage workflow, self-checks, core principles
└── references/
    └── contribution-frameworks.md        Whetten's seven questions, Corley & Gioia quadrants, Bartunek & Rynes, with examples
```

---

## Boundaries

- **No contribution talk detached from the original positioning.** The contribution must map back to the gap argued in the Introduction / Literature Review.
- **"Supported theory X" is not a contribution.** Verification is not contribution; a real contribution says how theory X now needs to be revised, extended or bounded.
- **No universally applicable limitations.** See the self-check above.
- **The AI does not decide how the story is told.** It supplies frameworks and checklists; the choice is the researcher's.

---

## Division of labour

- Gap not yet clear → [`literature-gap-synthesizer`](../literature-gap-synthesizer/). It uses the same positioning template as stage 1 here, so they connect directly.
- Introduction not yet written → [`academic-writing-assistant`](../academic-writing-assistant/). Stage 5's conclusion should echo the opening hook, which you can pull from there.
- Reviewer comments have arrived → [`response-to-reviewers`](../response-to-reviewers/). When a request cannot be met, it points to stage 4 here (how to write limitations).

---

## Version

**1.0.0** — five-stage workflow, three citable frameworks, two "paste it onto another paper" self-checks.
