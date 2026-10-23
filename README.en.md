# Social-Science Research Methods — Agent Skill Pack

> Seventeen AI agent skills for social-science research methods — variable
> extraction from papers, literature gap analysis, systematic review and
> meta-analysis, experiment design, data preparation, scale development &
> translation, quantitative analysis, SEM, results reporting, discussion
> writing, qualitative methods, citation auditing, manuscript and grant
> reviewing, journal selection, and reviewer response. Bilingual
> (English / 中文). Built for graduate students and supervisors in management,
> marketing, consumer behaviour and organizational behaviour.

**English** | [中文](README.md)

An AI methodology assistant skill pack for graduate students (MS / PhD / DBA) and
their supervisors in **management, marketing, consumer behaviour and organizational
behaviour**. The seventeen skills cover the full research chain: reading papers and
extracting variables, topic selection, systematic review, design, data preparation,
measurement, analysis, writing, journal selection and submission, verification,
reviewing, and responding to reviewers.

---

## ⚠️ Read this first: what this is, and what it is not

**These are methodology coaching and compliance-checking tools, not ghostwriting tools.**

They make the "how should this be done, how should it be reported" explicit.
They do **not** produce research conclusions for you, and they do **not** make
judgements on your behalf. All seventeen skills carry hard constraints; the most
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
| [`paper-variable-extraction`](paper-variable-extraction/) | Extract every variable and its operationalisation from a paper; Markdown report + Excel codebook | Reading & **variable extraction** | SKILL.md + 9 refs + 1 script |
| [`literature-gap-synthesizer`](literature-gap-synthesizer/) | Synthesise a body of literature, diagnose gap types, produce a positioning brief | Topic & **literature** | SKILL.md + 2 references |
| [`systematic-review`](systematic-review/) | Systematic review and meta-analysis: PRISMA 2020, effect-size conversion, heterogeneity, publication bias | **Evidence synthesis** | SKILL.md + 5 refs + 3 scripts |
| [`academic-writing-assistant`](academic-writing-assistant/) | Guide the writing of Introduction and Literature Review, including gap argument and hypothesis derivation | **Writing (front half)** | SKILL.md + 4 references |
| [`social-science-experiment-designer`](social-science-experiment-designer/) | Design a rigorous multi-study programme from scratch; six standard deliverables | **Design** | SKILL.md + 5 references |
| [`research-data-preparation`](research-data-preparation/) | Pre-acquisition planning, exposure audit, decision status, handoff spec | **Data preparation** | SKILL.md + 10 refs + 6 scripts + 1 template |
| [`scale-research`](scale-research/) | Scale search, evaluation, EN↔ZH back-translation and contextual adaptation | **Measurement** | SKILL.md + 3 references |
| [`quant-data-analysis`](quant-data-analysis/) | Data screening, ANOVA/ANCOVA, regression moderation — actually executed (scripts included) | **Core statistics** | SKILL.md + 2 refs + 4 scripts |
| [`sem-analysis-tutor`](sem-analysis-tutor/) | Step-by-step SEM analysis (CB-SEM and PLS-SEM tracks) | **SEM** | SKILL.md + 12 references |
| [`stats-results-writer`](stats-results-writer/) | Turn software output into APA-compliant report paragraphs (EN / ZH) | **Results** | SKILL.md + 8 references |
| [`discussion-conclusion-writer`](discussion-conclusion-writer/) | Theoretical contribution, practical implications, limitations, conclusion (Whetten / Corley & Gioia / Bartunek & Rynes) | **Writing (back half)** | SKILL.md + 1 reference |
| [`journal-submission`](journal-submission/) | Tier the paper, search candidate journals, assess fit and desk-reject risk, prepare the submission | **Journal selection** | SKILL.md + 4 refs |

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

The seventeen skills follow the **research pipeline**, with two side tracks:

```
① Read & extract       paper-variable-extraction
      ↓
② Topic & literature   literature-gap-synthesizer → systematic-review (when synthesis is needed)
      ↓
③ Writing (front)      academic-writing-assistant      ← Introduction / Literature Review
      ↓
④ Design               social-science-experiment-designer
      ↓
⑤ Data preparation     research-data-preparation
      ↓
⑥ Measurement          scale-research
      ↓
⑦ Core statistics      quant-data-analysis
      ↓
⑧ SEM                  sem-analysis-tutor
      ↓
⑨ Results              stats-results-writer
      ↓
⑩ Discussion           discussion-conclusion-writer
      ↓
⑪ Verify & submit      academic-citation-auditor → management-paper-reviewer
                       → journal-submission → response-to-reviewers

Side track A (qualitative)   qualitative-research-methods
Side track B (grants)        grant-proposal-reviewer
```

The writing track is **threaded through**, not left to the end: Introduction and
Literature Review usually get drafted before data collection and revised afterwards;
`academic-citation-auditor` provides the final citation self-check before submission.

- **Need to read a batch of papers and tabulate variables and scales** → `paper-variable-extraction`
- **Only a broad topic, no idea what to study yet** → `literature-gap-synthesizer`
- **Need to synthesise a set of empirical studies (including meta-analysis)** → `systematic-review`
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
- **No idea which tier this paper can reach, or which journals to try** → `journal-submission`
- **Want to know how your paper will be attacked** → `management-paper-reviewer`
- **Reviewer comments have arrived** → `response-to-reviewers`

### Seven boundaries that are easy to confuse

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
6. **`paper-variable-extraction` vs `systematic-review`** — the former **reads one paper and
   extracts its variables** into a codebook; the latter **synthesises many papers** into effect
   sizes. The former feeds the latter (its Excel can be used directly at the coding stage), but
   they answer different questions: "how did this paper measure it" versus "what do these papers
   say together".
7. **`journal-submission` vs `management-paper-reviewer`** — the former judges **tier and target**;
   the latter judges **whether the paper itself is any good**. Before submitting, attack the paper
   with the latter first, then choose journals with the former — reverse the order and the
   assessment gets written to fit the journal.

---

## Installation

A skill is just a directory containing `SKILL.md`. Copy the skill directories you want
into your agent environment's skill directory:

| Environment | Skill directory |
|---|---|
| Claude Code | `~/.claude/skills/` |
| WorkBuddy | `~/.workbuddy-ai/skills/` |
| DeepSeek Harness (DSH) | `~/.dsh/skills/` (project-level: `<project root>/.dsh/skills/`) |
| Other Agent Skills-compatible environments | see that environment's documentation |

> **Two things to know about DSH**: it scans only **one level** of the skills
> directory, and `skills/<skill-name>/SKILL.md` is exactly the shape it expects —
> copy the directories wholesale. Skill names must stay kebab-case (every directory
> here already is). A project-level directory takes precedence over the user-level
> one, so a same-named skill in `<project>/.dsh/skills/` shadows `~/.dsh/skills/`.

```bash
# Install all 17 skills into Claude Code
git clone https://github.com/yanchenli/social-science-research-skills.git
cp -r social-science-research-skills/*/ ~/.claude/skills/
```

### Let the agent install it for you

Paste one of the prompts below into whichever agent you use — Claude Code, Codex, DeepSeek Harness or
WorkBuddy all work. Both prompts make the agent **confirm the directory first, check for name clashes,
and self-check afterwards** rather than copying blindly.

**① Global install** (available in every project on this machine)

```
Install the skills from https://github.com/yanchenli/social-science-research-skills into this machine's user-level skills directory.

1. First work out which skills directory applies: Claude Code uses ~/.claude/skills/,
   WorkBuddy uses ~/.workbuddy-ai/skills/, DeepSeek Harness uses ~/.dsh/skills/.
   If you cannot tell, ask me — do not guess.
2. Clone the repository into a temporary directory; if git is unavailable, download the zip and extract it.
3. Copy only directories that contain a SKILL.md. Do not copy README.md, README.en.md, LICENSE or .git.
4. Before copying, check whether any same-named skill already exists in the target directory.
   If so, show me the list and ask whether to overwrite — do not overwrite silently.
5. When done, verify and report: how many were installed, which ones, whether SKILL.md exists in each,
   and which skills ship scripts that need extra dependencies.
```

**② Project-workspace install** (available only inside this project)

```
Install the skills from https://github.com/yanchenli/social-science-research-skills into this project's project-level skills directory,
but only the ones I name.

1. First work out the project-level directory: Claude Code uses <project root>/.claude/skills/,
   DeepSeek Harness uses <project root>/.dsh/skills/,
   WorkBuddy uses <project root>/.workbuddy-ai/skills/. If you cannot tell, ask me.
2. Clone the repository into a temporary directory; if git is unavailable, download the zip and extract it.
3. The skills I want are: <list skill names here, e.g. paper-variable-extraction, systematic-review>.
   If I did not list any, show me the skill list and let me choose.
4. Copy only those skill directories. Do not copy README.md, README.en.md, LICENSE or .git.
5. Check for name clashes before copying and ask me if there are any.
6. When done, verify and report: what was installed, whether SKILL.md exists, and what needs dependencies.
```

> **Project-level takes precedence over user-level**: a same-named skill shadows the user-level one, so
> option ② is the safer way to try the pack inside a single project. If your environment is not in the
> table above, replace the directory in step 1 with your actual path.

No configuration is needed. Each skill's `description` field carries its trigger
conditions, so it loads automatically when you mention SEM, scales, experiment design,
Results, discussion, qualitative coding, reviewer comments and similar topics.

> **Skills with scripts need extra dependencies.**
>
> - `quant-data-analysis` and `research-data-preparation`: `pandas` / `numpy` / `scipy` /
>   `statsmodels` / `openpyxl`; reading SPSS data additionally requires `pyreadstat`;
> - `paper-variable-extraction`: only `openpyxl`;
> - the three `systematic-review` scripts use **only the Python standard library** — nothing to install.
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
9. **The B-track criteria in `journal-submission` have not been reviewed by a human peer** —
   the archival-econometric track (DID / IV / RD / event studies) rests on the literature and went
   through one systematic review, but **the reviewer was an AI, not a domain expert**. Judgements
   of the form "what would a reviewer at tier X actually push back on" still need a human. The
   full review log, including what was adopted and rejected, is in that skill's
   `references/b-track-review-log.md`.
10. **The meta-analysis scripts produce intermediate quantities** — `meta.py` / `hs_meta.py` in
    `systematic-review` output quantities from the pooling process; before writing up, recompute in
    R (`metafor` / `psychmeta`) and check that the two agree.
11. **Variable extraction does not replace close reading** — `paper-variable-extraction` structures
    *how the paper measured things*; whether the argument holds is still yours to judge, and it
    recomputes no statistics.

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
