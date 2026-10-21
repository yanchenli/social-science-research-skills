# Social-Science Research Methods — Agent Skill Pack

> Fourteen AI agent skills for social-science research methods — literature gap
> analysis, experiment design, data preparation, scale development & translation,
> quantitative analysis, SEM, results reporting, discussion writing, qualitative
> methods, citation auditing, manuscript and grant reviewing, and reviewer
> response. Bilingual (English / 中文). Built for graduate students and
> supervisors in management, marketing, consumer behaviour and organizational
> behaviour.

**English** | [中文](README.md)

An AI methodology assistant skill pack for graduate students (MS / PhD / DBA) and
their supervisors in **management, marketing, consumer behaviour and organizational
behaviour**. The fourteen skills cover the full research chain: topic selection,
literature, design, data preparation, measurement, analysis, writing, verification,
reviewing, and responding to reviewers.

---

## ⚠️ Read this first: what this is, and what it is not

**These are methodology coaching and compliance-checking tools, not ghostwriting tools.**

They make the "how should this be done, how should it be reported" explicit.
They do **not** produce research conclusions for you, and they do **not** make
judgements on your behalf. All fourteen skills carry hard constraints; the most
important are:

| Constraint | Skill |
|---|---|
| **Numbers stay untouched** — every statistic must come from your own software output; no estimating, no editing | `stats-results-writer` |
| **Numbers come from executed code, not mental arithmetic or memory** — never compute a statistic by hand, and never fabricate a "demonstration" result when no data file is present | `quant-data-analysis` |
| **No "testing until significant"** — analyse according to the pre-registered plan; anything outside it is labelled exploratory | `quant-data-analysis` |
| **Quotations stay verbatim** — never invent plausible-sounding interview content, and never "polish" a participant's words | `qualitative-research-methods` |
| **No fabricated references** — anything unverifiable is marked `[待核实]`; never fill in authors, years or journals from memory | `literature-gap-synthesizer` |
| **Do not rely on memory; search** — every verification conclusion must rest on a search result, never on training recall | `academic-citation-auditor` |
| **Unverifiable ≠ fabricated** — these are strictly distinguished; a null result in one database is not grounds for a verdict | `academic-citation-auditor` |
| **AI proposes, the researcher decides** — construct choice, scale selection and item wording are the researcher's call | `scale-research` |
| **All α / AVE / CR must come from your own data** — never quote reliability figures supplied by the AI | `scale-research` |
| **Back-translation must be done by a human** — reviewers check this; AI back-translation is not evidence of quality | `scale-research` |
| **No "marginally significant"** — p = .06 is reported as not significant | `sem-analysis-tutor`, `stats-results-writer` |
| **Critique before prescribing** — no recommendation without a completed critical review attached | `social-science-experiment-designer` |
| **Profiling the data is itself a data exposure** — blinding must be specified *before* the run; "blinding" afterwards is too late | `research-data-preparation` |
| **All citations flagged for verification** — AI-supplied bibliographic details are never treated as verified fact | `academic-writing-assistant` |
| **No invented statistics** — missing values are marked with placeholders, never filled with fabricated numbers | `academic-writing-assistant` |
| **"Supported theory X" is not a contribution** — verification is not contribution | `discussion-conclusion-writer` |
| **Red team must be followed by blue team and fact-checking** — raw red-team output is not a review | `management-paper-reviewer` |
| **Never pretend a revision was made** — if a request cannot be met, say so and reframe it as a limitation | `response-to-reviewers` |

**The researcher bears final responsibility for the design, the judgements and the
conclusions.** Everything here is advisory and should be weighed against your own
context, your institution's requirements, and your supervisor's guidance.

### On the skills that produce manuscript prose

`academic-writing-assistant`, `stats-results-writer` and `discussion-conclusion-writer`
**do produce manuscript text** (Introduction / Literature Review, Results, Discussion)
and are therefore the easiest to misuse. They are **writing scaffolds**: they help you
clarify the chain of argument, the logic of hypothesis derivation, the conventions of
statistical reporting, and how a contribution can be framed — **they do not decide what
your contribution is.**

They generate no unverified data. Every citation is emitted in red as
`[待核实: Author, Year]`, with a verification checklist at the end, requiring you to
check each item against a real database.

> **Please confirm your own institution's rules on AI use in theses.** Policies are
> tightening and vary widely; journals' disclosure requirements for AI-assisted writing
> are inconsistent too. **Whether to use these tools, how to use them, and whether to
> disclose that use is a decision for you and your supervisor.**

### On the two reviewing skills

`management-paper-reviewer` and `grant-proposal-reviewer` are tools for the
**reviewing side**, not the authoring side. Two things to settle before using them:

1. If you sit on a journal or grant review panel, the opinions these skills generate
   are still yours to judge — the skills themselves insist that red-team output must
   pass through blue-team rebuttal and fact-checking before it can be used.
2. Using them as an author (to rehearse how your work might be attacked) is entirely
   legitimate, but **do not assume real reviewers will reason the same way.**

---

## Skills at a glance

### The research pipeline

| Skill | In one line | Stage | Size |
|---|---|---|---|
| [`literature-gap-synthesizer`](literature-gap-synthesizer/) | Synthesise a body of literature, diagnose gap types, produce a positioning brief | Topic & **literature** | SKILL.md + 2 references |
| [`academic-writing-assistant`](academic-writing-assistant/) | Guide the writing of Introduction and Literature Review, including gap argument and hypothesis derivation | **Writing (front half)** | SKILL.md + 4 references |
| [`social-science-experiment-designer`](social-science-experiment-designer/) | Design a rigorous multi-study programme from scratch; six standard deliverables | **Design** | SKILL.md + 5 references |
| [`research-data-preparation`](research-data-preparation/) | Pre-acquisition planning, exposure audit, decision status, handoff spec | **Data preparation** | SKILL.md + 10 refs + 6 scripts + 1 template |
| [`scale-research`](scale-research/) | Scale search, evaluation, EN↔ZH back-translation and contextual adaptation | **Measurement** | SKILL.md + 3 references |
| [`quant-data-analysis`](quant-data-analysis/) | Data screening, ANOVA/ANCOVA, regression moderation — actually executed (scripts included) | **Core statistics** | SKILL.md + 2 refs + 4 scripts |
| [`sem-analysis-tutor`](sem-analysis-tutor/) | Step-by-step SEM analysis (CB-SEM and PLS-SEM tracks) | **SEM** | SKILL.md + 12 references |
| [`stats-results-writer`](stats-results-writer/) | Turn software output into APA-compliant report paragraphs (EN / ZH) | **Results** | SKILL.md + 8 references |
| [`discussion-conclusion-writer`](discussion-conclusion-writer/) | Theoretical contribution, practical implications, limitations, conclusion (Whetten / Corley & Gioia / Bartunek & Rynes) | **Writing (back half)** | SKILL.md + 1 reference |

### Adjacent tracks and reviewing

| Skill | In one line | Stage | Size |
|---|---|---|---|
| [`qualitative-research-methods`](qualitative-research-methods/) | Five qualitative traditions, coding and analysis, trustworthiness, Findings writing | **Qualitative** research | SKILL.md + 8 references |
| [`academic-citation-auditor`](academic-citation-auditor/) | Verify every reference; detect AI-hallucinated sources and misattributed citations | **Verification** | SKILL.md |
| [`management-paper-reviewer`](management-paper-reviewer/) | Deep review of journal manuscripts: red-team attackers → blue-team rebuttal → fact-check | **Manuscript review** | SKILL.md |
| [`grant-proposal-reviewer`](grant-proposal-reviewer/) | Review grant proposals; produce a candid committee version and a constructive applicant version | **Grant review** | SKILL.md |
| [`response-to-reviewers`](response-to-reviewers/) | Organise R&R comments, choose a strategy per point, adjudicate conflicts, draft the response letter | **Reviewer response** | SKILL.md |

Each skill directory contains a `README.md` (currently in Chinese) explaining the
problem it solves, when to use it, its workflow, directory layout and caveats.

---

## Suggested order of use

The fourteen skills follow the **research pipeline**, with two side tracks:

```
① Topic & literature   literature-gap-synthesizer
      ↓
② Writing (front)      academic-writing-assistant      ← Introduction / Literature Review
      ↓
③ Design               social-science-experiment-designer
      ↓
④ Data preparation     research-data-preparation
      ↓
⑤ Measurement          scale-research
      ↓
⑥ Core statistics      quant-data-analysis
      ↓
⑦ SEM                  sem-analysis-tutor
      ↓
⑧ Results              stats-results-writer
      ↓
⑨ Discussion           discussion-conclusion-writer
      ↓
⑩ Verify & submit      academic-citation-auditor → management-paper-reviewer → response-to-reviewers

Side track A (qualitative)   qualitative-research-methods
Side track B (grants)        grant-proposal-reviewer
```

The writing track is **threaded through**, not left to the end: Introduction and
Literature Review usually get drafted before data collection and revised afterwards;
`academic-citation-auditor` provides the final citation self-check before submission.

- **Only a broad topic, no idea what to study yet** → `literature-gap-synthesizer`
- **Ready to draft Introduction / Literature Review** → `academic-writing-assistant`
- **Have an idea, no data yet** → `social-science-experiment-designer`
- **Data not in hand; want the data plan first** → `research-data-preparation`
- **Building a questionnaire or scale** → `scale-research`
- **Data collected; need ANOVA / regression** → `quant-data-analysis`
- **Need SEM / mediation** → `sem-analysis-tutor`
- **Analysis done; need to write Results** → `stats-results-writer`
- **Results written; unsure how to frame the contribution** → `discussion-conclusion-writer`
- **Doing interviews or case studies** → `qualitative-research-methods`
- **Citation self-check before submission** → `academic-citation-auditor`
- **Want to know how your paper will be attacked** → `management-paper-reviewer`
- **Reviewer comments have arrived** → `response-to-reviewers`

### Five boundaries that are easy to confuse

1. **`sem-analysis-tutor` vs `quant-data-analysis`** — the boundary is the **method**,
   not whether you have data. SEM / PLS-SEM / PROCESS mediation goes to the former;
   ANOVA / ANCOVA / regression moderation / simple slopes go to the latter. Both screen
   data, but in different contexts.
2. **The three writing skills** — `academic-writing-assistant` writes **Introduction and
   Literature Review**; `stats-results-writer` writes **Results**;
   `discussion-conclusion-writer` writes **Discussion and Conclusion**. Their conventions
   differ; do not mix them.
3. **`management-paper-reviewer` vs `grant-proposal-reviewer`** — the former reviews
   **completed research** (journal manuscripts); the latter reviews a **plan**
   (grant proposal). The criteria differ: the latter adds feasibility, budget, team
   qualifications and timeline.
4. **`literature-gap-synthesizer` vs `academic-writing-assistant` stage 2** — the former
   does the earlier, heavier work (large corpus, fuzzy topic, systematic argument for
   why the gap is real); the latter has a lightweight gap-classification step suited to
   "the literature is already clear, I just need it written up". Both use the same
   positioning template, so they connect directly.
5. **Flagged-for-verification vs actually verified** — the writing skills emit citations
   **flagged for verification**; `academic-citation-auditor` is the one that **actually
   verifies**. Run it after writing.

---

## Installation

A skill is just a directory containing `SKILL.md`. Copy the skill directories you want
into your agent environment's skill directory:

| Environment | Skill directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| WorkBuddy | `~/.workbuddy-ai/skills/` |
| Other Agent Skills-compatible environments | see that environment's documentation |

```bash
# Install all 14 skills into Claude Code
git clone https://github.com/<your-name>/social-science-research-skills.git
cp -r social-science-research-skills/*/ ~/.claude/skills/
```

No configuration is needed. Each skill's `description` field carries its trigger
conditions, so it loads automatically when you mention SEM, scales, experiment design,
Results, discussion, qualitative coding, reviewer comments and similar topics.

> **Skills with scripts need extra dependencies.** The scripts in `quant-data-analysis`
> and `research-data-preparation` depend on `pandas` / `numpy` / `scipy` /
> `statsmodels` / `openpyxl`; reading SPSS data additionally requires `pyreadstat`:
>
> ```bash
> pip install pandas numpy scipy statsmodels openpyxl pyreadstat
> ```

---

## Triggering the skills

Just describe what you need, in natural language. For example:

- "What's actually missing in the brand anthropomorphism literature?"
- "I have an idea for three experiments testing mediation and moderation — design it"
- "I haven't collected data yet; help me think through the data plan first"
- "I need to measure brand attachment — find me a scale, with a Chinese version"
- "Data collected, 2×2 design — run the ANOVA for me"
- "Run the SEM for me in SmartPLS, here's my data"
- "Here's my AMOS output — write the Results section"
- "All the results are in, but I don't know how to frame the contribution"
- "I have 14 interview transcripts, using the Gioia methodology — write the Findings"
- "Are the references in this paper real? Verify them"
- "Review this manuscript for me — targeting JCR"
- "Reviewer comments are back; organise them and draft the response"

---

## Known limitations

These skills do not hide their limits; each one documents its own. Aggregated:

1. **Chinese database access is unstable** — CNKI is restricted from some networks,
   so verification of Chinese-language sources is less reliable than for English ones.
   Supplement manually on CNKI.
2. **Coverage drops on very long reference lists** — beyond 30 references a prioritised
   strategy kicks in and full verification is not guaranteed.
3. **Paywalled full text is inaccessible** — content-matching relies on public
   abstracts, so verification depth is limited for paywalled work.
4. **The AI can still hallucinate** — the skills reduce this through mandatory search
   and self-checks, but cannot eliminate it. Cross-check high-stakes judgements.
   `management-paper-reviewer`'s red-team stage is **deliberately** aggressive; its raw
   output must pass blue-team rebuttal and fact-checking before use.
5. **Statistical judgements depend on the output you supply** — if the pasted numbers
   are wrong, the conclusions will be wrong.
6. **Writing skills do not generate research contributions** — they clarify your logic,
   but "does this gap really exist" and "is this contribution novel enough" are yours
   and your supervisor's to judge. No skill can assess originality for you.
7. **The qualitative skill does not replace the researcher's interpretation** —
   subjective involvement is part of the method; the skill structures and checks
   compliance, but the judgement of whether a theme holds is yours.
8. **The reviewing skills do not replace your judgement** — they produce scores and
   reasons; funding and acceptance decisions belong to committees and editors.
9. **Stages not yet covered** — **journal selection and submission preparation**
   (journal fit, cover letter, submission checklist) and **PRISMA diagrams and
   meta-analysis** (`literature-gap-synthesizer` stops at search strategy and
   inclusion/exclusion criteria). Both are currently gaps.

---

## Licence

This project is licensed under
**[Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE)**.

You are free to **share** (copy and redistribute the material in any medium or format)
and **adapt** (remix, transform, and build upon it), including for commercial purposes,
provided you give **appropriate credit**, link to the licence, and indicate whether
changes were made.

---

## Contributing

Issues and pull requests are welcome. If you find an incorrect threshold or a
mis-mapped software output field, please include the supporting reference.

---

## Disclaimer

This pack is a research-methods aid and **constitutes no professional guarantee for any
specific research design**. Experiment design, scale selection, statistical methods,
writing conventions and reporting standards should ultimately follow the mainstream
literature in your discipline, your target journal's requirements, your institution's
regulations, and your supervisor's guidance.

Responsibility for the academic integrity of any work produced with these tools rests
with the author.
