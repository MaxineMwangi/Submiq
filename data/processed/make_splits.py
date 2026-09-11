"""
Splits data/raw/submiq_dataset.csv into development (70%), validation (20%),
and test (10%) sets, stratified by expected_verdict so all three splits keep
a representative mix of Verified / Needs Improvement / Flagged examples.

Run from data/processed/:  python make_splits.py
"""

import csv
import random
from collections import defaultdict
from pathlib import Path

random.seed(42)  # fixed seed — matches generator, required for reproducibility

RAW_PATH = Path(__file__).parent.parent / "raw" / "submiq_dataset.csv"
SPLITS = {"development": 0.70, "validation": 0.20, "test": 0.10}


def main():
    with open(RAW_PATH, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    by_verdict = defaultdict(list)
    for row in rows:
        by_verdict[row["expected_verdict"]].append(row)

    out = {name: [] for name in SPLITS}
    for verdict, group in by_verdict.items():
        random.shuffle(group)
        n = len(group)
        n_dev = round(n * SPLITS["development"])
        n_val = round(n * SPLITS["validation"])
        out["development"] += group[:n_dev]
        out["validation"] += group[n_dev:n_dev + n_val]
        out["test"] += group[n_dev + n_val:]

    fieldnames = rows[0].keys()
    for name, split_rows in out.items():
        random.shuffle(split_rows)
        path = Path(__file__).parent / f"{name}.csv"
        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(split_rows)
        print(f"{name}: {len(split_rows)} rows -> {path.name}")


if __name__ == "__main__":
    main()
