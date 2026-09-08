# Data

Synthetic dataset used for Submiq development and evaluation.

- `raw/` — original synthetic dataset as generated (e.g. `submiq_dataset.csv`)
- `processed/` — cleaned splits: `development.csv`, `validation.csv`, `test.csv`

Split ratios: 70% development / 20% validation / 10% test.

- Development set: build the system
- Validation set: choose weights, thresholds, configuration
- Test set: final evaluation only — do not tune against it
