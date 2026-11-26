
"""
Completeness verification module for Submiq.

Checks whether required onboarding fields contain information.
It does not modify submitted data or evaluate other verification dimensions.
"""
import math
from typing import Any


REQUIRED_FIELDS = [
    "experience_level",
    "skills",
    "bio",
    "questionnaire_response",
]


def is_present(value: Any) -> bool:
    """Return True if a field contains non-empty information."""
    if value is None:
        return False

    if isinstance(value, float) and math.isnan(value):
        return False

    return str(value).strip() != ""


def calculate_score(submission: dict[str, Any]) -> float:
    """Return the proportion of required fields that are present."""
    present_fields = sum(
        is_present(submission.get(field))
        for field in REQUIRED_FIELDS
    )
    return present_fields / len(REQUIRED_FIELDS)


def find_missing_fields(submission: dict[str, Any]) -> list[str]:
    """Return the required fields that are missing."""
    return [
        field
        for field in REQUIRED_FIELDS
        if not is_present(submission.get(field))
    ]


def classify_score(score: float) -> str:
    """Classify a submission as Complete or Incomplete."""
    if score == 1.0:
        return "Complete"
    return "Incomplete"


def check_completeness(submission: dict[str, Any]) -> dict[str, Any]:
    """Return the completeness score, result, and missing fields."""
    score = calculate_score(submission)
    missing_fields = find_missing_fields(submission)

    return {
        "score": score,
        "result": classify_score(score),
        "missing_fields": missing_fields,
    }
