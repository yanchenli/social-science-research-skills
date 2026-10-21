# stats-results-writer

> Statistical reporting assistant — turning software output into APA-compliant paragraphs.

**Version**: 1.0.0 ｜ **For**: business MS/PhD students and instructors ｜ **Size**: SKILL.md + 8 references

**English** | [中文](README.md)

---

## The problem it solves

Running the analysis is only half the job. Turning the output into a Results section a journal will
accept is a separate skill:

- Which statistics **must** be reported, and which can be omitted?
- How do you phrase fit indices? What if χ² is significant but CFI is excellent?
- Should a mediation report include the confidence interval for the indirect effect? How many bootstrap resamples?
- How is multicollinearity disclosed? Should effect sizes be reported?
- How do Chinese and English journal conventions differ?

The skill packages the **reporting standard + decision thresholds + bilingual templates** for each
method into eight method-specific references.

---

## Core principle

**The AI interprets the numbers and writes the prose; the researcher confirms the judgements and verifies the data.**

> ⚠️ **Important**: the AI interprets and writes from the numbers you supply.
> If the numbers are wrong, the conclusions will be wrong. Always work from the original
> software output and check the pasted data before using the generated text.

---

## Coverage

### Eight method-specific references

| Reference | Content |
|---|---|
| `references/01-measurement.md` | Reliability, validity, CFA, common method bias |
| `references/02-anova-ttest.md` | ANOVA, independent and paired t-tests (22 code blocks — the thickest volume) |
| `references/03-regression.md` | OLS, hierarchical regression, logistic |
| `references/04-mediation.md` | Mediation (Baron & Kenny / bootstrap / PROCESS) |
| `references/05-moderation.md` | Moderation, simple slopes, Johnson-Neyman |
| `references/06-moderated-mediation.md` | Moderated mediation (PROCESS Models 7/14/58) |
| `references/07-cb-sem.md` | CB-SEM (AMOS / Mplus / lavaan) fit and paths |
| `references/08-pls-sem.md` | PLS-SEM (SmartPLS) measurement and structural model |

### Software output recognition

A built-in guide identifies the source from what you paste — you do not need to say which package
you used:

| Software | Typical markers |
|---|---|
| AMOS | `Regression Weights`, `Standardized RW`, `Model Fit`, χ²/df |
| SmartPLS | `Outer Loadings`, `Path Coefficients`, `Bootstrapping Results`, `HTMT` |
| JASP | tidy tables, `BF₁₀`, `η²`, residual Dutch interface strings |
| R (lavaan) | `lavaan`, `Estimate Std.Err z-value`, `CFI`, `SRMR` |
| R (lm/lme4) | `Coefficients:`, `Residual standard error`, `Multiple R-squared` |
| R (mediation/PROCESS) | `ACME`, `ADE`, `Indirect Effect`, `Boot CI` |
| Python (statsmodels) | `OLS Regression Results`, `coef std err t P>\|t\|` |
| SPSS | `Unstandardized B`, `Standardized Beta`, `Sig.` column |

---

## Workflow (five steps)

| Step | Content |
|---|---|
| 1. Gather information | Software, method, writing language, reporting format, hypothesis list, sample size |
| 2. Read the matching reference | Reporting standard, thresholds, templates for that method |
| 3. Interpret item by item | "Indicator → value → judgement", with hypothesis verdicts and risk notes |
| 4. Generate the text | Numerically exact, complete, explicit verdicts, no over-interpretation, correct bracket format |
| 5. (Optional) Word output | `.docx` with paragraphs, APA tables and a hypothesis summary table |

---

## One part worth calling out: `07-cb-sem.md`

This volume represents the overall standard. It maps the output fields of AMOS / lavaan / Mplus
**field by field** onto APA sentences, and provides:

- a table of fit indices that must be reported, with formats (e.g. `RMSEA = .XXX [.XXX, .XXX]`)
- a CB-SEM vs PLS-SEM decision table (theory, sample size, distributional assumptions, suitable journals)
- the three-step measurement invariance test and its criteria (ΔCFI ≤ .010 and ΔRMSEA ≤ .015; Cheung & Rensvold, 2002)
- **the standard wording for "χ² significant but other indices good"**, with the Bentler & Bonett (1980) citation
- the boundary on modification indices: **add one at a time, and only with a substantive reason**
- a template for comparing competing models (Δχ², ΔCFI)

This kind of "translate software output into compliant reporting" knowledge usually lives in forums
and lab folklore; it is rarely written down as a manual.

---

## Threshold quick reference (built in)

**Significance**: p < .05 (*) ／ p < .01 (**) ／ p < .001 (***) ／ p ≥ .05 (ns)

> ⚠️ **Never use "marginally significant"**: p = .06 or .07 is reported as not significant;
> the trend may be noted in the Discussion.

**CB-SEM fit**: χ²/df < 2 good, < 3 acceptable; CFI/TLI ≥ .95 good, ≥ .90 acceptable;
RMSEA < .05 good, < .08 acceptable; SRMR likewise

**PLS-SEM measurement**: outer loadings ≥ .70; AVE ≥ .50; CR ≥ .70; HTMT < .85 strict / < .90 lenient

**Regression**: VIF < 5 ideal, < 10 acceptable, ≥ 10 needs attention; f² .02 small / .15 medium / .35 large

---

## Usage

```
Here's my AMOS output:
Model Fit: CMIN=412.3, DF=180, P=.000, CMIN/DF=2.29, CFI=.941, TLI=.931,
RMSEA=.064, SRMR=.051
Paths: language style → trust  Estimate=.412, S.E.=.078, C.R.=5.28, P=***
       trust → purchase intention  Estimate=.531, S.E.=.081, C.R.=6.55, P=***
Hypotheses: H1 linguistic concreteness positively affects trust; H2 trust positively affects purchase intention
N = 320
Write the Results section in English.
```

The skill interprets each item and flags which meet thresholds (here CFI .941 is "acceptable", not
"good" — it will say so), then produces an APA 7th English paragraph with an explicit
supported / not supported verdict for each hypothesis.

---

## Directory layout

```
stats-results-writer/
├── SKILL.md                        workflow, software identification, threshold quick reference
└── references/
    ├── 01-measurement.md           reliability, validity, CFA, CMB
    ├── 02-anova-ttest.md           ANOVA, t-tests
    ├── 03-regression.md            OLS, hierarchical regression, logistic
    ├── 04-mediation.md             mediation
    ├── 05-moderation.md            moderation
    ├── 06-moderated-mediation.md   moderated mediation
    ├── 07-cb-sem.md                CB-SEM (AMOS/Mplus/lavaan)
    └── 08-pls-sem.md               PLS-SEM (SmartPLS)
```

---

## Boundaries

- **Numbers stay untouched.** Every figure in the text must come from the output you supply; the skill must not estimate or alter anything. **But if the pasted numbers are wrong, the conclusions will be wrong** — always work from the original output.
- **It will not turn a null result into a significant one.** "Marginally significant" and similar hedges are explicitly forbidden.
- **Missing information is flagged.** If the numbers you supply are insufficient for a complete report (e.g. no SE or CI), the skill tells you what to add rather than guessing.
- **Thesis vs journal**: a thesis can be more detailed; a journal submission should be leaner, with detailed tables in the body and brief prose.

---

## Division of labour with sem-analysis-tutor

**This skill writes; it does not do.** If the analysis is not yet run, or indicators fail and you
do not know how to proceed, use [`sem-analysis-tutor`](../sem-analysis-tutor/) — it walks you
through the analysis.

---

## Version

**1.0.0** — eight method-specific references, nine software-output signatures, bilingual templates,
dual CB-SEM/PLS-SEM threshold reference.
