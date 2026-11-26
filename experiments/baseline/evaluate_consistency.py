"""Evaluate Submiq's rule-based consistency checker."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from backend.app.consistency.checker import check_consistency

DATA_PATH = ROOT / "data" / "raw" / "submiq_dataset.csv"
LABELS = ["Consistent", "Contradictory"]


def map_prediction(result):
    if result["result"] == "Potential Contradiction":
        return "Contradictory"
    if result["result"] == "No Explicit Contradiction Detected":
        return "Consistent"
    return "Unable to Assess"


def main():
    df = pd.read_csv(DATA_PATH)

    required = {"bio", "questionnaire_response", "consistency_label"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing dataset columns: {sorted(missing)}")

    results = df.apply(
        lambda row: check_consistency(row["bio"], row["questionnaire_response"]),
        axis=1,
    )
    df["predicted_label"] = results.apply(map_prediction)

    assessable = df[df["predicted_label"] != "Unable to Assess"].copy()
    actual = assessable["consistency_label"].astype(str).str.strip()
    predicted = assessable["predicted_label"]

    print(f"Total submissions: {len(df)}")
    print(f"Unable to assess: {(df['predicted_label'] == 'Unable to Assess').sum()}")
    print(f"Evaluated submissions: {len(assessable)}")
    print(f"Accuracy on evaluated submissions: {accuracy_score(actual, predicted):.2%}")

    print("\nClassification report:")
    print(classification_report(actual, predicted, labels=LABELS, zero_division=0))

    print("Confusion matrix (rows = actual, columns = predicted):")
    print(
        pd.DataFrame(
            confusion_matrix(actual, predicted, labels=LABELS),
            index=[f"Actual {label}" for label in LABELS],
            columns=[f"Predicted {label}" for label in LABELS],
        )
    )


if __name__ == "__main__":
    main()
