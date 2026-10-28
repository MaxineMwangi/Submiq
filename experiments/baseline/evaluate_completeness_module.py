
from pathlib import Path
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.completeness.checker import check_completeness


DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "submiq_dataset.csv"

REQUIRED_FIELDS = [
    "experience_level",
    "skills",
    "bio",
    "questionnaire_response",
]


def main():
    df = pd.read_csv(DATASET_PATH)

    df["actual"] = df["completeness_label"].map(
        {"Yes": "Complete", "No": "Incomplete"}
    )

    df["predicted"] = df.apply(
        lambda row: check_completeness(
            {field: row[field] for field in REQUIRED_FIELDS}
        )["result"],
        axis=1,
    )

    correct = (df["actual"] == df["predicted"]).sum()
    total = len(df)
    accuracy = correct / total

    false_positives = (
        (df["predicted"] == "Complete")
        & (df["actual"] == "Incomplete")
    ).sum()

    false_negatives = (
        (df["predicted"] == "Incomplete")
        & (df["actual"] == "Complete")
    ).sum()

    print(f"Total submissions: {total}")
    print(f"Correct predictions: {correct}")
    print(f"Accuracy: {accuracy:.2%}")
    print(f"False positives: {false_positives}")
    print(f"False negatives: {false_negatives}")
    print("\nConfusion matrix:")
    print(
        pd.crosstab(
            df["actual"],
            df["predicted"],
            rownames=["Actual"],
            colnames=["Predicted"],
            dropna=False,
        )
    )


if __name__ == "__main__":
    main()
