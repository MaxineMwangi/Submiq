# Completeness-Only Baseline

## Purpose

The completeness-only baseline establishes a simple reference point for evaluating the Submiq verification system.

The baseline determines whether an onboarding submission contains all required fields. It uses only field presence and does not use text quality, plausibility, consistency, AI-generated content detection, or the final expected verdict.

## Required Fields

The baseline checks the following four fields:

- `experience_level`
- `skills`
- `bio`
- `questionnaire_response`

`submission_id` is treated as an identifier and is not included in the completeness calculation.

## Methodology

For each submission, the baseline:

1. Checks whether each required field contains information.
2. Counts the number of present required fields.
3. Calculates a completeness score.

The completeness score is calculated as:

`Completeness Score = Present Required Fields / Total Required Fields`

With four required fields, possible scores include:

- `1.00` = all four fields are present
- `0.75` = three fields are present
- `0.50` = two fields are present
- `0.25` = one field is present
- `0.00` = no required fields are present

A score of `1.00` is classified as `Complete`. Any lower score is classified as `Incomplete`.

## Ground Truth Comparison

The dataset uses:

- `Yes` = complete
- `No` = incomplete

For evaluation, these labels are mapped to the baseline result categories:

- `Yes` → `Complete`
- `No` → `Incomplete`

The original dataset labels are not modified.

## Dataset

The baseline uses the processed Submiq synthetic dataset:

`data/processed/submiq_dataset_processed.csv`

The dataset contains 120 submissions.

## Results

| Metric | Result |
|---|---:|
| Dataset rows | 120 |
| Required fields | 4 |
| Complete predictions | 111 |
| Incomplete predictions | 9 |
| Accuracy | 97.50% |
| False positives | 3 |
| False negatives | 0 |

### Completeness Score Distribution

| Score | Number of submissions |
|---:|---:|
| 0.50 | 5 |
| 0.75 | 4 |
| 1.00 | 111 |

## Interpretation

The completeness-only baseline achieved an accuracy of 97.50% against the dataset's `completeness_label`.

The baseline produced three false positives and zero false negatives.

The result provides a reference point for later experiments. The full Submiq verification system will introduce additional verification dimensions, including text quality, cross-field consistency, claim plausibility, and AI-generated content detection.

## Scope and Limitations

This baseline evaluates only the presence of required information.

It does not determine:

- whether submitted claims are true;
- whether the writing is high quality;
- whether information across fields is consistent;
- whether content was generated using AI;
- whether a submission should receive the final Submiq verdict.

The baseline is therefore kept separate from the multidimensional verification engine.

## Reproducibility

Run the baseline from the project root:

```text
python experiments/baseline/completeness_baseline.py
## Completeness Module Evaluation

The completeness module was evaluated against the 120-submission synthetic dataset using four required fields: experience level, skills, bio, and questionnaire response.

- **Accuracy:** 97.50% (117/120)
- **False positives:** 3
- **False negatives:** 0

The three false positives were S019, S022, and S024. Although all four fields contained text, the responses indicated skipped answers, incomplete information, or missing supporting evidence.

This highlights a limitation of presence-based completeness checking: populated fields are not necessarily meaningfully completed. The baseline remains focused on field presence. Detecting skipped answers, incomplete responses, and missing attachments requires additional validation rules.

These results apply to the synthetic dataset and should not be interpreted as evidence of equivalent performance on real-world submissions.
## Text Quality Module Evaluation

The text quality module uses explainable, rule-based signals to assess text length, placeholder content, potentially exaggerated claims, specificity, informal wording, and repetition.

### Evaluation results

- Dataset: 120 synthetic submissions.
- Accuracy: 50.00%.
- Macro F1-score: 0.47.
- Weighted F1-score: 0.48.

| Actual label | Predicted Good | Predicted Fair | Predicted Poor |
|---|---:|---:|---:|
| Good | 34 | 9 | 1 |
| Fair | 22 | 16 | 7 |
| Poor | 8 | 13 | 10 |

### Limitations

The baseline shows partial agreement with the existing dataset labels but frequently confuses Good and Fair submissions. It should not be treated as a reliable standalone quality decision system.

The rules are heuristic and the dataset is synthetic. Because the rules were refined using examples from this dataset, these results are exploratory rather than an independent measure of generalization. Further evaluation on a held-out dataset and human-reviewed examples is needed.

The module does not detect AI authorship, verify factual claims, or replace human review.
