# academic-citation-auditor

> Academic citation audit — verify every reference, and catch AI-hallucinated sources and misattributed citations.

**Version**: 1.0.0 (skill declares v1.1) ｜ **For**: supervisors, instructors, graduate students ｜ **Size**: SKILL.md (single file, no references)

**English** | [中文](README.md)

---

## The problem it solves

AI-generated references are now commonplace. A submitted paper may contain:

- **Fabricated sources** — titles that fit the topic perfectly but appear in no database
- **Metadata errors** — the source exists, but authors, year, volume or pages are wrong
- **Bait-and-switch citations** — the paper claims "Smith (2020) showed X→Y", but Smith actually studied Z
- **Predatory journals** — not indexed in SSCI/SCI/ESCI/CSSCI, and on a blacklist
- **Second-hand citations** — bulk-copied from a review without crediting the intermediary
- **Anomalous citation structure** — one author exceeds 30% of all citations, or everything clusters in a single year (a sign of bulk generation)

Checking a 60-reference paper by hand is hours of work. This skill turns it into an executable procedure.

---

## Core principle

> **Do not rely on memory; search. If you cannot find it, mark it uncertain. Uncertain is not the same as fabricated.**

The skill explicitly acknowledges that **it too can hallucinate**, therefore:

- every verification conclusion **must** state its basis (what was searched, what was found)
- asserting that a reference is real or fake **from memory is forbidden**
- a self-check runs before the final verdict: *"My judgement rests on search results, not on training recall."*

**"Uncertain is not fabricated" is the key design decision.** Incomplete database coverage
(grey literature, conference papers, non-English sources) produces "not found", which is not
the same as fabrication — the cost of falsely accusing an author is higher than the cost of a miss.

---

## Four-phase workflow

### PHASE 1 — Information extraction (must run first)

1. Extract the **in-text citation list**, including context: **what the author is trying to prove with this citation** (this is the basis for the later content-match check)
2. Extract the **reference list**, transcribing every visible metadata field
3. Build a **cross-reference table** — flagging citations with no reference, and references never cited

### PHASE 2 — Per-item authenticity check

| Step | Content |
|---|---|
| **Step A** | Direct DOI / URL check (preferred) — via doi.org or CrossRef |
| **Step B** | Database search — three keyword combinations each time: ① full title ② first author + year ③ journal + volume/issue |
| **Step C** | Author identity check — does the author exist, and do they publish in this area? |
| **Step D** | **Content match** — what the source actually studied vs what the citation claims |

> ⚠️ **Minimum search requirement**: a null result in a *single* database must **not** lead directly
> to ❓ or 🔴. At least two different databases must fail before marking "unverifiable" or
> "highly likely fabricated".

Database priority: English — Google Scholar → CrossRef (then PubMed/Scopus); Chinese — CNKI → Wanfang (then VIP).

### Four verdict levels

| Symbol | Meaning | Criterion |
|---|---|---|
| ✅ | Verified | Exact matching record in an authoritative database |
| ⚠️ | Partly doubtful | Source exists, but year/volume/pages deviate |
| ❓ | Unverifiable | Not found — **not fabricated**; coverage is incomplete |
| 🔴 | Highly likely fabricated | Author + title + journal absent everywhere, and journal/author look dubious |

### PHASE 3 — Six risk-signal checks

Hallucination-typical sources, predatory journals, misrepresented citation purpose,
**anomalous citation structure (quantified thresholds)**, format anomalies, suspected second-hand citation.

The structural thresholds are concrete: one author > 30% of citations; more than 50% from one journal;
years tightly clustered; more than 60% of sources older than ten years.

### PHASE 4 — Structured audit report

Six sections: anomaly warning table, verified-sources summary, citation consistency check,
format problems, overall conclusion, and a statement of audit limitations.

**Four conclusion levels**: ✅ pass ／ 🔧 minor revision ／ ⚠️ risk, recommend review ／ 🚨 integrity risk, rewrite.

---

## Seven execution constraints

1. **Search first** — every conclusion rests on a search result; judging from training memory is forbidden
2. **Transparent trail** — each item records which database, which keywords, what was returned
3. **Conservative verdicts** — strictly distinguish "unverifiable" from "fabricated", to avoid false accusations
4. **Coverage and degradation strategy** — beyond 30 references, prioritise highly-cited, anomalous and unidentifiable items, and state the coverage rate at the top of the report
5. **No pre-judgement** — verdicts follow the evidence, not the paper's overall quality
6. **Separate second-hand citation from fabrication** — the former is a formatting fix; only the latter escalates to an integrity risk
7. **Self-check before output** — confirm the basis is search results, not training memory

Constraints 3, 5 and 6 together form a **mechanism for not harming students**.

---

## Usage

```
(upload the paper PDF, or paste the reference list)
Verify the references in this paper.
```

You can also submit only a reference list (no body text) — the skill skips the body-dependent
steps and states in the report that "only the reference list was verified; no body text was
provided, so the citation consistency check could not be performed".

Format checking defaults to **APA 7th**; GB/T 7714, Harvard and others can be specified.

---

## Directory layout

```
academic-citation-auditor/
└── SKILL.md        four-phase workflow, four verdict levels, six risk signals, seven constraints, known limits
```

Single-file skill — all procedures and criteria live in `SKILL.md`.

---

## Known limitations (declared in the skill)

1. **Chinese database access is unstable** — CNKI is restricted from some networks; Chinese-source verification is less reliable than English. Supplement manually.
2. **Coverage drops on long lists** — beyond 30 references a prioritised strategy kicks in; full verification is not guaranteed.
3. **Paywalled full text is inaccessible** — content matching relies on public abstracts.
4. **Grey literature is hard to judge** — government reports, white papers and unpublished working papers are easily marked ❓, which **does not mean fabricated**.
5. **The AI can still hallucinate** — mitigated by mandatory search and self-checks, not eliminated. Cross-check high-stakes verdicts by hand.

---

## Boundaries

- **This is supporting evidence, not a final verdict.** Items marked ❓ should be re-checked by hand, ideally with the author supplying a screenshot of the source.
- **It distinguishes "non-standard" from "fraudulent".** Second-hand citation and messy formatting are non-standard; only highly likely fabricated sources or systematic misrepresentation escalate to an integrity risk.
- **The report is written for supervisors and instructors**, and its summary section is framed for that audience.

---

## Version

**v1.1** — added signal 6 (second-hand citation); added a recency threshold to signal 4;
added the large-list degradation strategy and minimum search requirement to the constraints;
fixed signal 3 to avoid duplicate execution; added the known-limitations section.
