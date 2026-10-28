from pathlib import Path
import json

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, f1_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data" / "processed"
RESULTS = ROOT / "experiments" / "baseline" / "ai_detection_ml_results.json"

LABELS = ["Human", "AI", "Mixed"]


def load_split(name):
    df = pd.read_csv(DATA / f"{name}.csv")
    df["bio"] = df["bio"].fillna("").astype(str)
    df["questionnaire_response"] = (
        df["questionnaire_response"].fillna("").astype(str)
    )
    df["text"] = df["bio"] + " " + df["questionnaire_response"]
    return df


development = load_split("development")
validation = load_split("validation")
test = load_split("test")

# Keep the test set untouched until configuration selection is complete.
configurations = [
    {"ngram_range": (1, 1), "min_df": 1, "C": 0.1},
    {"ngram_range": (1, 2), "min_df": 1, "C": 0.1},
    {"ngram_range": (1, 2), "min_df": 1, "C": 1.0},
    {"ngram_range": (1, 3), "min_df": 1, "C": 1.0},
    {"ngram_range": (1, 2), "min_df": 2, "C": 1.0},
]

candidates = []

for config in configurations:
    model = Pipeline([
        ("tfidf", TfidfVectorizer(
            lowercase=True,
            strip_accents="unicode",
            ngram_range=config["ngram_range"],
            min_df=config["min_df"],
            sublinear_tf=True,
        )),
        ("classifier", LogisticRegression(
            C=config["C"],
            class_weight="balanced",
            max_iter=2000,
            random_state=42,
        )),
    ])

    model.fit(development["text"], development["source"])
    predictions = model.predict(validation["text"])
    macro_f1 = f1_score(
        validation["source"],
        predictions,
        labels=LABELS,
        average="macro",
        zero_division=0,
    )

    candidates.append((macro_f1, config, model))
    print(
        f"Validation macro F1={macro_f1:.3f} | "
        f"config={config}"
    )

# Select using validation macro F1 only.
best_score, best_config, _ = max(candidates, key=lambda item: item[0])

# Refit the chosen configuration on development + validation.
train = pd.concat([development, validation], ignore_index=True)

final_model = Pipeline([
    ("tfidf", TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=best_config["ngram_range"],
        min_df=best_config["min_df"],
        sublinear_tf=True,
    )),
    ("classifier", LogisticRegression(
        C=best_config["C"],
        class_weight="balanced",
        max_iter=2000,
        random_state=42,
    )),
])

final_model.fit(train["text"], train["source"])
test_predictions = final_model.predict(test["text"])

test_accuracy = accuracy_score(test["source"], test_predictions)
test_macro_f1 = f1_score(
    test["source"],
    test_predictions,
    labels=LABELS,
    average="macro",
    zero_division=0,
)

print("\nSELECTED CONFIGURATION")
print(best_config)
print(f"Validation macro F1: {best_score:.3f}")

print("\nHELD-OUT TEST RESULTS")
print(f"Test accuracy: {test_accuracy:.3f}")
print(f"Test macro F1: {test_macro_f1:.3f}")
print("\nClassification report:")
print(classification_report(
    test["source"],
    test_predictions,
    labels=LABELS,
    zero_division=0,
))
print("Confusion matrix (actual rows, predicted columns):")
print(confusion_matrix(
    test["source"],
    test_predictions,
    labels=LABELS,
))

RESULTS.parent.mkdir(parents=True, exist_ok=True)
report = {
    "method": "TF-IDF + Logistic Regression",
    "labels": LABELS,
    "selected_configuration": {
        **best_config,
        "ngram_range": list(best_config["ngram_range"]),
    },
    "validation_macro_f1": float(best_score),
    "test_accuracy": float(test_accuracy),
    "test_macro_f1": float(test_macro_f1),
    "test_classification_report": classification_report(
        test["source"],
        test_predictions,
        labels=LABELS,
        output_dict=True,
        zero_division=0,
    ),
    "test_confusion_matrix": confusion_matrix(
        test["source"],
        test_predictions,
        labels=LABELS,
    ).tolist(),
    "test_submission_ids": test["submission_id"].tolist(),
    "note": (
        "Exploratory results on a small synthetic dataset. "
        "Source labels describe dataset construction and do not prove "
        "AI authorship. Test results may be unstable with few examples."
    ),
}
RESULTS.write_text(json.dumps(report, indent=2), encoding="utf-8")
print(f"\nResults saved to {RESULTS.relative_to(ROOT)}")
