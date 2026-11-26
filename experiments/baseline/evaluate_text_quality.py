"""Evaluate Submiq's rule-based text quality baseline."""

import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from backend.app.text_quality.checker import assess_text

DATA_PATH = ROOT / "data" / "raw" / "submiq_dataset.csv"
LABEL_ORDER = ["Good", "Fair", "Poor"]


def combine_text(row):
    fields = []
    for column in ["bio", "questionnaire_response"]:
        value = row[column]
        if pd.notna(value) and str(value).strip():
            fields.append(str(value).strip())
    return " ".join(fields)


def main():
    df = pd.read_csv(DATA_PATH)

    required = {"bio", "questionnaire_response", "text_quality_label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing required columns: {sorted(missing)}")

    df["combined_text"] = df.apply(combine_text, axis=1)
    df["predicted_label"] = df["combined_text"].apply(
        lambda text: assess_text(text)["label"]
    )

    actual = df["text_quality_label"].astype(str).str.strip()
    predicted = df["predicted_label"]

    print(f"Total submissions: {len(df)}")
    print(f"Accuracy: {accuracy_score(actual, predicted):.2%}")
    print("\nClassification report:")
    print(
        classification_report(
            actual,
            predicted,
            labels=LABEL_ORDER,
            zero_division=0,
        )
    )

    print("Confusion matrix (rows = actual, columns = predicted):")
    print(
        pd.DataFrame(
            confusion_matrix(actual, predicted, labels=LABEL_ORDER),
            index=[f"Actual {label}" for label in LABEL_ORDER],
            columns=[f"Predicted {label}" for label in LABEL_ORDER],
        )
    )


if __name__ == "__main__":
    main()
