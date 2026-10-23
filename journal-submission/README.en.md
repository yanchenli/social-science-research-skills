# journal-submission

> Journal selection and submission preparation — place the paper at the right tier before choosing a journal.

**Version**: 2.2.0 ｜ **For**: business MS / PhD / DBA students and faculty ｜ **Size**: SKILL.md + 4 reference files

**English** | [中文](README.md)

---

## The problem it solves

Submissions fail in two ways, at very different costs:

- **Bad paper** — reviewers say the method is weak or the contribution is thin. Painful, but you get feedback.
- **Wrong journal** — a paper that would clear a 3-star outlet is thrown at a 4-star one and desk-rejected;
  or a paper that could reach 4 stars is sent two tiers down. **No feedback at all**, just three to six
  months gone.

The second failure is more common and almost never taught. This skill addresses it: **tier the paper
before picking a journal**, then build a reach / match / safety list.

---

## Core principles

**Blind-rate the six dimensions first; look at journals second.**

Reverse that order and things go wrong: pick the target journal first and the assessment gets written
to just barely clear that tier. Editors see through it.

| Rule | Meaning |
|---|---|
| **The weakest dimension caps the tier** | Not an average. Strong theory + weak method submitted to a 4\* gets desk-rejected — editors look at the short board |
| **"Strong" can come from any dimension** | Tier 4 needs two strong dimensions; they need not be methodological. What is actually blocked by "method can only be medium" is 4\* |
| **Academic reputation and institutional lists, side by side** | Some journals are highly regarded by peers but absent from your school's list — and vice versa. Which line governs is the user's call |
| **No built-in ranking tables** | Lists change every year; hard-coding them guarantees errors. Every candidate journal's position is looked up live; if it cannot be verified, say so |

---

## Workflow

### Gate 0 — four exclusion layers (before any recommendation)

A hit means exclusion regardless of tier:

1. Publisher level (MDPI, Frontiers, and similar)
2. Journal level (Web of Science "On-Hold" is an automatic veto)
3. Official watchlists (the CAS *International Journal Early Warning List*)
4. Institutional blacklists (your own institution's rules override everything)

> **Two things that quietly stop working**: the 2025 watchlist contains only 5 journals and **does not
> include MDPI** — banning MDPI is an institutional policy, not an official finding. And the Hindawi
> brand has been retired (absorbed into Wiley), so **excluding by publisher name silently fails**;
> exclusion must be done by ISSN.

### Stage 0 — two splits (which ruler to use)

| Split | Options |
|---|---|
| **Discipline track** | A micro-behavioural / B archival-econometric / B2 asset pricing / C practice / D qualitative / E conceptual-review / F configurational (QCA) |
| **Input completeness** | Full manuscript / abstract only — the latter permits only an "upper-bound estimate" and **must be stated as such** |

> **Split by method, not by discipline.** Strategy research using archival data goes to B, using surveys
> to A, using QCA to F.

### Stage 1 — six-dimension tiering

Theoretical contribution / methodological rigour / data and sample / analytical depth / writing
completeness / reader fit. Each rated strong / medium / weak, with evidence cited.

**Dimension 2 judges whether threats are addressed, not which design label is attached.**
Rating "strong" because the paper says DID or IV, and "medium" because it uses fixed effects or PSM, is a
common error — the same design can be two tiers apart depending on execution.

### Stages 2–5 — search, fit, preparation, delivery

Candidate search (must be online) → per-journal fit and desk-reject risk → cover letter, materials
checklist, formatting and anonymisation, rejection-to-resubmission strategy → selection report.

---

## Example

```
I'm a marketing PhD student; I want to place this in an SSCI journal.
Data are a CSMAR panel, I ran a DID but no parallel-trends test.
Tell me what tier I can target and name a few journals.
```

The skill runs Gate 0 exclusions, classifies the track (B archival-econometric), rates each dimension
with evidence, flags that the method dimension is capped by the missing parallel-trends test, and returns
three tiers of candidates with their ranking-list positions.

---

## Boundaries

- **No acceptance guarantee.** Tiering is a pre-submission screen, not a prediction.
- **Ranking positions are looked up live.** The skill ships no lists; if a position cannot be verified,
  it says so rather than guessing.
- **The B-track criteria have not been reviewed by a human domain expert.** That track's skeleton comes
  from Roberts & Whited (2013) and related literature, and went through one systematic review — by an AI
  reviewer, not a human peer. **Judgements of the form "what would a reviewer at tier X actually push
  back on" still need a human.** The review log, including what was adopted and what was rejected, is in
  `references/b-track-review-log.md` and can be audited.
- **Does not rewrite the paper** and does not draft reviewer responses (see below).

---

## Related skills

| Need | Use |
|---|---|
| Revise the manuscript (intro / literature review) | [`academic-writing-assistant`](../academic-writing-assistant/) |
| Write the Results section | [`stats-results-writer`](../stats-results-writer/) |
| Write Discussion & Conclusion | [`discussion-conclusion-writer`](../discussion-conclusion-writer/) |
| Respond to reviewers | [`response-to-reviewers`](../response-to-reviewers/) |
| Run a systematic review / meta-analysis | [`systematic-review`](../systematic-review/) |

---

## Version history

**2.2.0** — Four-layer Gate 0; seven-track split; six-dimension tiering (method dimension now judged by
whether threats are addressed); mutually exclusive three-tier recommendation; multi-list comparison
(ABS / FT50 / UTD24 / ABDC / JCR); academic and institutional lines reported side by side.

**2.1.0** — Added the discipline split, multi-list comparison, and a literature-checked rewrite of the
B-track criteria.

**1.0.0** — First release.
