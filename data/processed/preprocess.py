"""
Preprocess the raw Submiq synthetic onboarding dataset.

The raw dataset is never modified. The script:
1. Loads the raw dataset.
2. Standardizes missing values.
3. Normalizes text fields.
4. Preserves missingness.
5. Preserves submission IDs and labels.
6. Validates row counts and labels.
7. Writes the processed dataset.

Run from the project root:
    python data/processed/preprocess.py
"""

from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parents[2]

RAW_PATH = BASE_DIR / "data" / "raw" / "submiq_dataset.csv"
PROCESSED_PATH = BASE_DIR / "data" / "processed" / "submiq_dataset_processed.csv"


TEXT_COLUMNS = [
    "scenario_category",
    "experience_level",
    "skills",
    "bio",
    "questionnaire_response",
    "source",
    "completeness_label",
    "text_quality_label",
    "plausibility_label",
    "consistency_label",
    "expected_verdict",
]


REQUIRED_COLUMNS = [
    "submission_id",
    *TEXT_COLUMNS,
]


def normalize_text(value):
    """Normalize non-missing text without destroying missing values."""
    if pd.isna(value):
        return pd.NA

    value = str(value)
    value = " ".join(value.split())

    return value if value else pd.NA


def preprocess_dataset():
    """Load, preprocess, validate, and save the dataset."""

    if not RAW_PATH.exists():
        raise FileNotFoundError(f"Raw dataset not found: {RAW_PATH}")

    df = pd.read_csv(RAW_PATH, dtype="string")

    original_row_count = len(df)
    original_ids = df["submission_id"].copy()
    original_labels = df["expected_verdict"].copy()

    # Validate expected columns.
    missing_columns = [
        column for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    # Standardize missing values.
    df = df.replace(
        {
            "": pd.NA,
            " ": pd.NA,
            "nan": pd.NA,
            "NaN": pd.NA,
        }
    )

    # Normalize text while preserving missing values.
    for column in TEXT_COLUMNS:
        df[column] = df[column].map(normalize_text)

        # Validate that submission IDs were preserved.
    if not df["submission_id"].astype("string").equals(
        original_ids.astype("string")
    ):
        raise ValueError("Submission IDs changed during preprocessing.")

    # Validate that ground-truth verdicts were preserved.
    if not df["expected_verdict"].astype("string").equals(
        original_labels.astype("string")
    ):
        raise ValueError(
            "Ground-truth labels changed during preprocessing."
        )

    # Validate row count.
    if len(df) != original_row_count:
        raise ValueError(
            "Row count changed during preprocessing."
        )

    # Save processed dataset.
    df.to_csv(PROCESSED_PATH, index=False)

    print(f"Raw dataset:       {RAW_PATH}")
    print(f"Processed dataset: {PROCESSED_PATH}")
    print(f"Rows:              {len(df)}")
    print(f"Columns:           {len(df.columns)}")
    print("\nMissing values after preprocessing:")
    print(df.isna().sum())


if __name__ == "__main__":
    preprocess_dataset()