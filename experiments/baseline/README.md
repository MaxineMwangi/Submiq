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