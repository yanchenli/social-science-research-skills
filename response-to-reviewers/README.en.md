# response-to-reviewers

> Reviewer response assistant — R&R is not about editing the paper, it is about convincing the editor that every point was taken seriously.

**Version**: 1.0.0 ｜ **For**: business MS/PhD/DBA students and instructors with a paper under review ｜ **Size**: SKILL.md (single file)

**English** | [中文](README.md)

---

## The problem it solves

The moment a Revise & Resubmit decision arrives, most authors face two or three sets of comments
that contradict each other, a pile of requests they are unsure whether to follow, and the worry
that "will this rebuttal sound too aggressive".

The skill does three things:

1. Turns scattered comments into a traceable, item-by-item list;
2. Chooses a strategy for each item (rather than deciding by emotion);
3. Drafts a response letter that can be submitted with the revised manuscript.

---

## Core principle

**The letter is written for the editor, not for the reviewers.**

The editor is the one who decides. The letter's job is to let the editor confirm that every point
was handled seriously **without re-reading the reviews**.

> **Scope note**: this skill handles the response after an R&R (revise and resubmit) decision.
> If the paper was **rejected** and you want to appeal the decision, that is a different genre
> (appeal letter) with different logic and strategy, and it is **out of scope**.

---

## Workflow (five stages)

| Stage | Content |
|---|---|
| 1. Organise and classify | Source, type (substantive / editorial), section |
| 2. Strategy per point | One of four, below |
| 3. Draft the letter | Structure, opening, tone |
| 4. Conflicting reviewer demands | Surface them; ask the editor to adjudicate |
| 5. Delivery | Generate the formal letter as `.docx` |

### A key move in stage 1

Group by **section of the paper** (Intro / Methods / Results / Discussion), not rigidly by reviewer number.

Two reviewers often make the same point in different words. Handling them together lets you merge
the explanation in the letter and avoids missing one.

### Stage 2: the four strategies

| Strategy | When to use it |
|---|---|
| Full compliance | The reviewer is right; do it |
| Partial compliance + explanation | Partly reasonable, but full compliance would create another problem |
| Polite but firm disagreement | The reviewer misread the paper, or the request conflicts with the study's fundamental logic — **argue with evidence, not with attitude** |
| Refer to the editor | Two reviewers demand incompatible things |

---

## Two easily missed techniques

**One: leave a trace even when you disagree.**

Even in the "polite but firm disagreement" case, add a clarifying sentence to the text rather than
changing nothing at all. That way the next reader — including a future reviewer — will not form the
same misreading. Genuine "absolutely nothing can be adjusted" cases are rare.

**Two: if you truly cannot do it, say so.**

Do not pretend. Explain why it is impossible and formally acknowledge it as a boundary or limitation
of the study — this connects directly to stage 4 of
[`discussion-conclusion-writer`](../discussion-conclusion-writer/).

Pretending to comply while changing nothing is the single most reputation-damaging move in an R&R.

---

## Usage

```
The reviews are back. Reviewer 1 says the theoretical framework is too narrow and suggests
adding a competing theory; Reviewer 2 says there are too many theories and asks me to focus
on a single one for internal consistency. Another point says the sample is too small, but
we can't collect more data.
Organise these and draft the response letter, in English.
```

The skill does four things: classifies the three points (two are really the same "scope of theory"
issue pulling in opposite directions), identifies this as a **reviewer conflict** needing explicit
editorial adjudication, handles the sample-size point by acknowledging a limitation rather than
pretending to collect more data, and produces a letter grouped by reviewer.

---

## Boundaries

- **It does not decide whether to comply.** It lays out the options and consequences; the researcher decides.
- **It does not invent revisions.** If you have not actually made the change, it asks you to make it first, or reframes the response as acknowledging a limitation.
- **It does not handle appeal letters.** See the scope note above.
- **There is no "aggressive mode".** The tone is polite and non-defensive throughout — the reviewer is criticising the paper, not attacking you.

---

## Division of labour

- **Want to know how your paper will be attacked** → [`management-paper-reviewer`](../management-paper-reviewer/). Two sides of one coin: that one finds the flaws, this one responds to them.
- **Need to write limitations into the manuscript** → [`discussion-conclusion-writer`](../discussion-conclusion-writer/) stage 4.
- **A comment questions the statistics and results must be re-reported** → [`stats-results-writer`](../stats-results-writer/) or [`quant-data-analysis`](../quant-data-analysis/).

---

## Version

**1.0.0** — five-stage workflow, four response strategies, adjudication of conflicting reviews, tone conventions.
