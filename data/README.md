# Submiq Synthetic Dataset

## Structure

```
data/
├── raw/
│   ├── generate_synthetic_dataset.py   # reproducible generator (fixed seed)
│   └── submiq_dataset.csv              # generated output — the primary dataset (120 rows)
├── processed/
│   ├── make_splits.py                  # stratified split generator (fixed seed)
│   ├── development.csv                 # 85 rows (~70%) — used for module tuning
│   ├── validation.csv                  # 25 rows (~20%) — used for weight selection (Sec 3.2.3)
│   └── test.csv                        # 10 rows (~10%) — held out, touched once
└── README.md
```

The synthetic dataset **is** the research dataset for this project (not an
auxiliary/fallback set), so it lives directly under `raw/` rather than in a
separate `synthetic/` folder. `processed/` only ever contains derived,
deterministic splits of `raw/submiq_dataset.csv` — nothing here is edited by
hand.

## Why labels beyond "AI vs human"

A completeness-only or AI-detection-only ground truth would let Submiq learn
the wrong lesson (that AI-written = bad). The dataset instead labels each
submission across all five verification dimensions independently, so the
five modules can each be evaluated on their own accuracy, and the aggregator
can be evaluated on whether combining them beats any single signal —
directly supporting Research Question iv.

## Scenario categories (12 examples each, 120 rows total)

| # | Category | Rows | Why it matters |
|---|----------|------|-----------------|
| 1 | Complete, genuine-looking (human) | 12 | Baseline positive case |
| 2 | Incomplete | 12 | Tests completeness module in isolation |
| 3 | Poor-quality writing | 12 | Tests text-quality module in isolation |
| 4 | Contradictory information | 12 | Tests cross-field consistency module |
| 5 | Implausible claims | 12 | Tests claim-plausibility module |
| 6 | AI-generated but plausible | 12 | The key nuance case — should NOT auto-flag |
| 7 | AI-generated and suspicious | 12 | Should flag, but via multiple signals, not AI-detection alone |
| 8 | Human-written but suspicious | 12 | Proves the system isn't just an AI-detector in disguise |
| 9 | Mixed human/AI-edited text | 12 | Realistic middle-ground case, hardest to label |
| 10 | Edge cases | 12 | Emoji/bullet formatting, career changers, overqualified applicants, very short/long text, non-English, all-caps, minimal skills |

Domains covered across the dataset: software engineering (frontend,
backend, mobile, embedded, DevOps, data engineering, QA), data/analytics,
design (UX/UI, UX research), marketing, sales, HR/recruiting, healthcare
(clinic admin, nursing, veterinary), legal (paralegal), finance/accounting,
education, warehouse/logistics, hospitality/retail, customer support/IT
helpdesk, real estate, construction, photography, fitness coaching, and
more — so no verification module can overfit to one writing style or
industry.

## Columns

- `submission_id` — unique identifier
- `scenario_category` — one of the 10 categories above (for stratified analysis)
- `experience_level`, `skills`, `bio`, `questionnaire_response` — the raw submission fields
- `source` — `Human`, `AI`, or `Mixed` (ground truth of how the text was produced — used only for evaluating the AI-detection module, never fed to the scoring pipeline itself)
- `completeness_label` — `Yes` / `No` (human-annotated ground truth)
- `text_quality_label` — `Good` / `Fair` / `Poor`
- `plausibility_label` — `Plausible` / `Implausible`
- `consistency_label` — `Consistent` / `Contradictory`
- `expected_verdict` — `Verified` / `Needs Improvement` / `Flagged` — the target label for end-to-end evaluation against your baseline

## Class balance

Across the 120 rows: 48 Flagged, 44 Needs Improvement, 28 Verified. This is
intentionally not perfectly balanced — flagged/borderline cases are
over-represented relative to a real onboarding funnel because those are the
cases your modules most need to be evaluated against. If you want the
overall dataset to better mirror production traffic (where most submissions
are fine), add more "Complete, genuine" and "AI-generated, plausible" rows
before your final evaluation run, and re-run the generator.

## Extending the dataset

Add new rows to the `EXAMPLES` list in `generate_synthetic_dataset.py`
(keeps everything reproducible and diff-able in git — do not hand-edit the
CSV directly), then re-run `generate_synthetic_dataset.py` followed by
`make_splits.py`. Keep the random seed fixed when you add behavioral-metadata
simulation later, per your reproducibility requirement in Sec 3.2.2.

## Before you use this for real evaluation

These 120 rows and their labels are a **starting draft**, not
annotator-verified ground truth. Your methodology (Sec 3.2.1) calls for
independent labeling by at least two reviewers with Cohen's Kappa agreement
— have a second person review these labels (especially the borderline
"Needs Improvement" calls) before reporting evaluation numbers from them.
