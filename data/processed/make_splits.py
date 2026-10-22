
"""
Split the processed Submiq synthetic onboarding dataset into
development (70%), validation (20%), and test (10%) sets.

The split is stratified by expected_verdict, uses a fixed random
seed, and preserves every submission exactly once.
"""

import csv
import random
from collections import defaultdict
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]

PROCESSED_PATH = (
    BASE_DIR / "data" / "processed" / "submiq_dataset_processed.csv"
)

SPLIT_SIZES = {
    "development": 84,
    "validation": 24,
    "test": 12,
}

RANDOM_SEED = 42


def allocate_counts(group_size, split_names, remaining_capacity):
    """Allocate a verdict group across splits using largest remainders."""
    total_capacity = sum(remaining_capacity.values())

    if total_capacity < group_size:
        raise ValueError("Insufficient split capacity.")

    exact = {
        split: group_size * remaining_capacity[split] / total_capacity
        for split in split_names
    }

    counts = {
        split: min(int(exact[split]), remaining_capacity[split])
        for split in split_names
    }

    remaining = group_size - sum(counts.values())

    order = sorted(
        split_names,
        key=lambda split: exact[split] - int(exact[split]),
        reverse=True,
    )

    while remaining > 0:
        progressed = False

        for split in order:
            if counts[split] < remaining_capacity[split]:
                counts[split] += 1
                remaining -= 1
                progressed = True

                if remaining == 0:
                    break

        if not progressed:
            raise ValueError("Unable to allocate all rows.")

    return counts


def main():
    if not PROCESSED_PATH.exists():
        raise FileNotFoundError(
            f"Processed dataset not found: {PROCESSED_PATH}"
        )

    with open(PROCESSED_PATH, encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        rows = list(reader)

    if not rows:
        raise ValueError("Processed dataset is empty.")

    if not fieldnames or "expected_verdict" not in fieldnames:
        raise ValueError("Dataset must contain expected_verdict.")

    if "submission_id" not in fieldnames:
        raise ValueError("Dataset must contain submission_id.")

    if any(
        not (row.get("expected_verdict") or "").strip()
        for row in rows
    ):
        raise ValueError("Every row must have an expected_verdict.")

    if len(rows) != sum(SPLIT_SIZES.values()):
        raise ValueError(
            f"Expected {sum(SPLIT_SIZES.values())} rows, "
            f"but found {len(rows)}."
        )

    original_ids = [row["submission_id"] for row in rows]

    if len(set(original_ids)) != len(original_ids):
        raise ValueError("Source dataset contains duplicate submission IDs.")

    rng = random.Random(RANDOM_SEED)
    groups = defaultdict(list)

    for row in rows:
        groups[row["expected_verdict"]].append(row)

    split_names = list(SPLIT_SIZES)
    remaining_capacity = SPLIT_SIZES.copy()
    output = {split: [] for split in split_names}

    # Allocate each verdict group while respecting remaining split capacity.
    verdicts = list(groups)
    rng.shuffle(verdicts)

    for index, verdict in enumerate(verdicts):
        group = groups[verdict]
        rng.shuffle(group)

        if index == len(verdicts) - 1:
            counts = remaining_capacity.copy()
            if sum(counts.values()) != len(group):
                raise ValueError(
                    "Final verdict group does not fit remaining capacity."
                )
        else:
            counts = allocate_counts(
                len(group),
                split_names,
                remaining_capacity,
            )

        start = 0

        for split in split_names:
            count = counts[split]
            output[split].extend(group[start:start + count])
            start += count
            remaining_capacity[split] -= count

    if any(remaining_capacity.values()):
        raise ValueError(
            f"Split allocation incomplete: {remaining_capacity}"
        )

    for split_rows in output.values():
        rng.shuffle(split_rows)

    # Validate exact sizes and ensure each source record appears once.
    for split, target_size in SPLIT_SIZES.items():
        if len(output[split]) != target_size:
            raise ValueError(
                f"{split} has {len(output[split])} rows; "
                f"expected {target_size}."
            )

    split_ids = [
        row["submission_id"]
        for split_rows in output.values()
        for row in split_rows
    ]

    if len(split_ids) != len(original_ids) or set(split_ids) != set(original_ids):
        raise ValueError("Split IDs do not match the source dataset.")

    # Write the split files only after all validations pass.
    for split, split_rows in output.items():
        path = BASE_DIR / "data" / "processed" / f"{split}.csv"

        with open(path, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(split_rows)

        print(f"{split}: {len(split_rows)} rows -> {path.name}")

    print(f"Total: {sum(len(split) for split in output.values())} rows")
    print("Validation passed: all source submission IDs are preserved.")


if __name__ == "__main__":
    main()
