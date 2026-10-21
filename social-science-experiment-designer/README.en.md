# social-science-experiment-designer

> Social-science experiment design assistant — from a research idea to a six-deliverable multi-study programme.

**Version**: 4.0.0 ｜ **For**: business graduate students and social-science researchers ｜ **Size**: SKILL.md + 5 references

**English** | [中文](README.md)

---

## The problem it solves

Designing a multi-study paper has a high bar: the studies must corroborate rather than repeat each
other, each must carry a distinct argumentative function, and you must anticipate where reviewers
will attack. The beginner's classic failure is not "the experiment was run wrong" but
"the three studies are actually testing the same thing".

The skill plays two roles, in a fixed order of precedence:

- **Primary: gatekeeper** — complete a critical review before offering any suggestion
- **Secondary: creative partner** — once the review passes, propose concrete, conditional options

Every material suggestion must follow **recommended option → methodological basis → potential
confound → control strategy → alternative**. **Suggestions without the critical analysis attached
are not allowed** — that is the difference between this and "design me an experiment".

---

## When to use it

- You have an idea, no data yet, and need a complete multi-study design
- Study 1 is done and you need to design the follow-ups (cross-study consistency is checked automatically)
- All data is in and you need a pre-registration document and an IRB draft
- Your hypotheses have been challenged and you need a structured stress test

**Three entry points are detected automatically**: from scratch → the full seven steps; partial data
→ enter at step 3; complete data → generate the deliverable pack directly.

---

## Workflow (seven steps)

| Step | What happens | Key mechanism |
|---|---|---|
| 1 | Introduction, background, scenario detection | Probes your experience (0–1 / 2–5 / 5+ papers) to set explanation depth; scales the number of studies to the target journal tier |
| 2 | **Hypothesis statement and critical review** | Six-dimension review: theoretical mechanism, alternative explanations, novelty, boundary conditions, **construct boundaries**, **falsifiability criteria**. Nothing advances until all six are covered |
| 3 | Research blueprint | Fill the "study function allocation table"; if resources are short, run a hypothesis-priority assessment (must test / conditional / defer) |
| 4 | Per-study design and materials | Manipulation design (five paradigms assessed by priority), measurement, questionnaire flow, pilot advice; **six cross-study consistency checks after each study** |
| 5 | Critical design review | Three threat checklists: internal, construct and statistical-conclusion validity |
| 6 | Power analysis and sample planning | Each study analysed separately; figures must not be shared across studies; effect-size sources in three tiers (same-paradigm literature → meta-analysis → Cohen's conventions) |
| 7 | Generate the full package | Six deliverables across execution / writing / compliance layers |

### Backtracking (the design core)

The flow is **not a one-way conveyor**. Four explicitly marked backtrack triggers:

- Materials design reveals a hypothesis is hard to operationalise → revise the hypothesis
- Power analysis shows resources cannot support the blueprint → adjust the study plan
- Consistency checks reveal a fundamental cross-study mismatch → resolve at blueprint level
- Analysis planning reveals the design cannot identify the target effect → adjust the design

### Automatic ethics triggers

Ethics discussion is triggered **immediately**, never deferred, when: vulnerable populations,
strong negative-emotion manipulations, purpose concealment, full deception, real monetary outlays or
sensitive personal data, or sensitive constructs such as discrimination, self-harm or illegality.

---

## The six deliverables

| Layer | Files |
|---|---|
| Execution | ① Experiment design document　② Standard operating procedure |
| Writing | ③ Cross-study argument map　④ Methods-section writing outline |
| Compliance | ⑤ Pre-registration document　⑥ IRB application draft |

When generating file ①, the skill also suggests adding a **contingency plan for unsupported
hypotheses**: check whether the manipulation worked → post-hoc power → report the result as an
exploratory finding without altering the pre-registered primary hypothesis.

---

## Directory layout

```
social-science-experiment-designer/
├── SKILL.md                                main flow and seven-step workflow
└── references/
    ├── hypothesis-review.md                six-dimension review prompts and examples (before step 2)
    ├── multi-study-architecture.md         multi-study planning and function allocation (before step 3)
    ├── materials-design.md                 manipulation materials, paradigm library, pilot templates (before step 4)
    ├── analysis-planning.md                analysis strategy: ANOVA / mediation / moderation / moderated mediation (step 6)
    └── deliverables.md                     full specifications for the six deliverables (before step 7)
```

---

## Usage

```
Here's my idea: the linguistic style of online reviews (concrete vs abstract) affects
consumers' trust in the product, which in turn affects purchase intention, and the effect
may be moderated by product type.
I'm targeting JCR, the budget is limited, and participants will mostly come from Credamo.
```

The skill asks about your experience first (which sets explanation depth), then starts with the
six-dimension review at step 2 — including pressing you on "what result would count as supporting
your hypothesis" and "which alternative explanation is a reviewer most likely to raise".

---

## Boundaries

- **It does not invent studies, data or references.** A citation is given in APA form only when it can be found on Google Scholar; when uncertain it says so and asks you to verify.
- **Design is always a trade-off** between validities and between the ideal and the feasible; the skill keeps that visible rather than pretending a "perfect design" exists.
- **The final design is the researcher's responsibility**; all suggestions should be weighed against institutional requirements and your supervisor's guidance.

---

## Version

**4.0.0** — six-dimension hypothesis review (including construct boundaries and falsifiability),
three entry scenarios, four backtrack triggers, six automatic ethics triggers, six cross-study
consistency checks, three-tier effect-size sourcing for power analysis.
