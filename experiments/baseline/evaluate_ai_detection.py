from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

from backend.app.ai_detection.checker import assess_ai_content


DATA_PATH = ROOT / "data" / "raw" / "submiq_dataset.csv"
LABELS = ["Human", "AI", "Mixed"]


def main():
    df = pd.read_csv(DATA_PATH)

    required = {"bio", "questionnaire_response", "source"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing dataset columns: {sorted(missing)}")

    actual = []
    predicted = []
    unable = 0

    for _, row in df.iterrows():
        result = assess_ai_content(
            row["bio"],
            row["questionnaire_response"],
        )

        label = str(row["source"]).strip()
        if label not in LABELS:
            continue

        if result["result"] == "Unable to Assess":
            unable += 1
            continue

        actual.append(label)
        predicted.append(result["result"])

    print(f"Total submissions: {len(df)}")
    print(f"Unable to assess: {unable}")
    print(f"Evaluated submissions: {len(actual)}")

    if not actual:
        print("No labelled submissions available for evaluation.")
        return

    print(f"Accuracy: {accuracy_score(actual, predicted):.2%}")
    print("\nClassification report:")
    print(
        classification_report(
            actual,
            predicted,
            labels=LABELS,
            zero_division=0,
        )
    )

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
