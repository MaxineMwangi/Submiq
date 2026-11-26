from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PATH = BASE_DIR / "data" / "processed" / "submiq_dataset_processed.csv"
OUTPUT_DIR = BASE_DIR / "data" / "processed"
SEED = 42

df = pd.read_csv(DATA_PATH)

required = {"submission_id", "source"}
if not required.issubset(df.columns):
    raise ValueError(f"Dataset must contain {sorted(required)}")

if len(df) != 120 or df["submission_id"].duplicated().any():
    raise ValueError("Expected 120 rows with unique submission IDs.")

# First reserve 12 test records, stratified by source.
development_validation, test = train_test_split(
    df,
    test_size=12,
    random_state=SEED,
    stratify=df["source"],
)

# Split the remaining 108 into 84 development and 24 validation.
development, validation = train_test_split(
    development_validation,
    test_size=24,
    random_state=SEED,
    stratify=development_validation["source"],
)

splits = {
    "development": development,
    "validation": validation,
    "test": test,
}

all_ids = []
for name, split_df in splits.items():
    split_df.to_csv(OUTPUT_DIR / f"{name}.csv", index=False)
    all_ids.extend(split_df["submission_id"].tolist())
    print(f"\n{name.upper()}: {len(split_df)} rows")
    print(split_df["source"].value_counts().to_string())

if len(all_ids) != 120 or len(set(all_ids)) != 120:
    raise ValueError("Split validation failed: records are missing or duplicated.")

print("\nAll 120 records are preserved exactly once.")
