from pathlib import Path

import sys
import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from backend.app.plausibility.checker import assess_plausibility


ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "raw" / "submiq_dataset.csv"


def main():
    df = pd.read_csv(DATA_PATH)
    required = {"bio", "questionnaire_response", "plausibility_label"}
    missing = required - set(df.columns)

    if missing:
        raise ValueError(f"Missing dataset columns: {sorted(missing)}")

    actual = []
    predicted = []
    unable = 0

    for _, row in df.iterrows():
        result = assess_plausibility(
            row["bio"],
            row["questionnaire_response"],
        )

        if result["result"] == "Unable to Assess":
            unable += 1
            continue

        label = str(row["plausibility_label"]).strip()
        if label not in {"Plausible", "Implausible"}:
            continue

        actual.append(label)
        predicted.append(
            "Implausible"
            if result["result"] == "Needs Review"
            else "Plausible"
        )

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
            labels=["Plausible", "Implausible"],
            zero_division=0,
        )
    )
    print("Confusion matrix (rows = actual, columns = predicted):")
    print(
        pd.DataFrame(
            confusion_matrix(
                actual,
                predicted,
                labels=["Plausible", "Implausible"],
            ),
            index=["Actual Plausible", "Actual Implausible"],
            columns=["Predicted Plausible", "Predicted Implausible"],
        )
    )


if __name__ == "__main__":
    main()

