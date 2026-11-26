"""
Completeness-only baseline for the Submiq onboarding dataset.

The baseline evaluates submissions using only required-field presence.
It does not use text quality, plausibility, consistency, AI detection,
or the final expected verdict.

Run from the project root:
    python experiments/baseline/completeness_baseline.py
"""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = (
    BASE_DIR / "data" / "processed" / "submiq_dataset_processed.csv"
)

REQUIRED_FIELDS = [
    "experience_level",
    "skills",
    "bio",
    "questionnaire_response",
]


def is_present(value):
    """Return True when a required field contains information."""
    return pd.notna(value) and str(value).strip() != ""


def calculate_completeness(row):
    """Calculate the proportion of required fields that are present."""
    present_fields = sum(
        is_present(row[field])
        for field in REQUIRED_FIELDS
    )

    return present_fields / len(REQUIRED_FIELDS)


def classify_completeness(score):
    """Classify a submission as Complete or Incomplete."""
    if score == 1.0:
        return "Complete"

    return "Incomplete"


def evaluate_baseline():
    """Run the completeness-only baseline and evaluate its performance."""

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH, dtype="string")

    missing_columns = [
        column
        for column in REQUIRED_FIELDS + ["completeness_label"]
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    df["baseline_score"] = df.apply(
        calculate_completeness,
        axis=1,
    )

    df["baseline_result"] = df["baseline_score"].apply(
        classify_completeness
    )

    expected_result = df["completeness_label"].map({
        "Yes": "Complete",
        "No": "Incomplete",
    })

    df["baseline_correct"] = (
        df["baseline_result"] == expected_result
    )

    accuracy = df["baseline_correct"].mean()

    false_positives = (
        (df["baseline_result"] == "Complete")
        & (expected_result == "Incomplete")
    ).sum()

    false_negatives = (
        (df["baseline_result"] == "Incomplete")
        & (expected_result == "Complete")
    ).sum()

    print("Submiq Completeness-Only Baseline")
    print("=" * 40)

    print(f"Dataset rows: {len(df)}")
    print(f"Required fields: {len(REQUIRED_FIELDS)}")

    print("\nRequired fields:")
    for field in REQUIRED_FIELDS:
        print(f"- {field}")

    print("\nBaseline results:")
    print(df["baseline_result"].value_counts())

    print("\nEvaluation:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")

    print("\nCompleteness score distribution:")
    print(df["baseline_score"].value_counts().sort_index())

    return df


if __name__ == "__main__":
    evaluate_baseline()