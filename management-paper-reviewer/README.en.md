# management-paper-reviewer

> Deep peer review for management manuscripts — red-team attack, blue-team defence, fact-checking; three gates before any verdict.

**Version**: 1.0.0 ｜ **For**: marketing / consumer behaviour / HRM / OB / strategy ｜ **Size**: SKILL.md (single file)

**English** | [中文](README.md)

---

## The problem it solves

The default "review" from a language model is pattern-matching: summarise the content, then add a
few gentle suggestions. That output looks like a review but misses the problems that actually cause
rejection.

This skill uses adversarial roles to force depth, then **strips out the fabricated parts with two
verification gates**.

---

## Two design principles

**One: aggression first.**

By default the model tends toward surface evaluation. Role-play and adversarial instruction are
required to force it to look for the real problems other reviewers miss.

**Two: verification filter.**

Aggressive prompting makes the model **fabricate problems** to please its "critic" persona. So the
aggressive stage must be followed by a verification chain that separates real problems from invented ones.

> These two are inseparable. **Aggression alone yields sharp-sounding but unsupportable criticism;
> verification alone finds nothing.**

---

## Pipeline (five stages)

```
Stage 0  Metadata extraction
Stage 1  Red-team attack (five specialist attackers, run independently)
Stage 2  Consolidation and blue-team defence → adjudication
Stage 3  Fact-checking and citation audit
Stage 4  Final review writing
Stage 5  (Optional) Author-side revision advice
```

### Stage 1: the five attackers

| Attacker | Focus |
|---|---|
| The Theory Breaker | Justification of the theory choice, construct definitions, authenticity of the contribution, logical derivation of hypotheses |
| The Method Butcher | Branches by study type: survey/scale, experiment, archival, qualitative |
| The Stats Auditor | Internal consistency of reported data, measurement model, structural model, effect sizes, robustness |
| The Literature Detective | Review completeness, citation accuracy, novelty, "the evidence of silence" |
| The Practice Skeptic | Actionability of managerial implications, contextual boundaries, reverse causality |

One line in the global attacker instruction is worth noting: **IGNORE PRESTIGE** — disregard journal
rank, author reputation, institutional affiliation and typographic polish. Prior publication is not
proof of correctness.

> For a purely qualitative study (per stage 0), the Stats Auditor **skips** — there are no
> statistics to audit, and data authenticity is covered by the Method Butcher's
> "data-to-finding traceability" item.

### Stage 2: blue team

A defence lawyer for the authors, giving the strongest rebuttal to each red-team finding from four
angles: defence on the merits (did the paper already address this in a footnote or appendix?),
field convention (is this a common limitation of the field rather than a defect of this paper?),
possible misreading, and verdict (Red Team Correct / Blue Team Correct / Debatable).

### Stage 3: fact-checking

> **Global rule: any claim about the paper's specific content is treated as false until verified against the text.**

Findings that are fabricated or untraceable are marked `[可疑]`; those involving external literature
are marked `[引用存疑]`; both are removed or downgraded in the final list.

---

## Severity levels

| Level | Meaning |
|---|---|
| **Fatal** | Fundamental; cannot be fixed by revision; data may need recollecting |
| **Major** | Fixable but requires substantial revision; may affect the core conclusion |
| **Moderate** | Needs revision but does not affect the core conclusion |
| **Minor** | Detail-level improvement |

---

## Field-specific checklists

Five domains have dedicated checklists, for example:

- **HRM**: with nested data (employee–team–organisation), was HLM/MLM used? Are causal claims backed by longitudinal data?
- **OB**: does team-level aggregation meet rwg / ICC requirements? Does the leadership measure distinguish behaviour from subordinate perception?
- **Strategy**: strategic choice is often endogenous to organisational characteristics — is endogeneity handled? Did strategy cause performance, or performance shape strategy?
- **Consumer behaviour**: in cross-cultural comparisons, was measurement invariance tested? Is external validity from online experiments to real purchase behaviour argued?

---

## Usage

```
Review this manuscript (PDF attached). Target is JCR — will it make it?
```

The skill extracts metadata (field, study type, core question, the 2–4 contributions the paper
claims), runs the five attackers independently, consolidates and de-duplicates, sends everything to
the blue team, and keeps only what survives fact-checking.

**The output states explicitly** what you would decide as an AE (accept / minor revision / major revision / reject), and why.

---

## Boundaries

- **Stage 1 aggression is a deliberate role design, not the final judgement.** Do not use raw red-team output as a review — stages 2 and 3 must run.
- **No fabricated external evidence.** Never claim what an uncited source says; you may only say "work of type X should be cited".
- **Cautious about quantitative claims.** Raise suspected statistical problems only from internal inconsistency (e.g. "the N in Table 2 does not match the Methods"), never from visual impressions of an equation.
- **Distinguish field convention from real problems.** Self-report scales are ubiquitous in social science; that does not make every paper defective.

---

## Division of labour

- **Reviews have arrived and you need to respond** → [`response-to-reviewers`](../response-to-reviewers/). Two sides of one coin.
- **Need to verify whether citations exist** → [`academic-citation-auditor`](../academic-citation-auditor/). This skill's citation check uses only the paper's own reference list.
- **Reviewing a thesis rather than a journal manuscript** → a separate blind-review workflow (not public).
- **Reviewing a grant proposal** → [`grant-proposal-reviewer`](../grant-proposal-reviewer/). Reviewing a plan and reviewing completed research use different criteria.

---

## Version

**1.0.0** — five-stage pipeline, five specialist attackers, blue-team defence and fact-checking,
field-specific checklists for five management subfields.
