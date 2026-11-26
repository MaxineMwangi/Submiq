"""Combine Submiq verification checks into an explainable recommendation."""

from typing import Any

from backend.app.completeness.checker import check_completeness
from backend.app.text_quality.checker import assess_text
from backend.app.consistency.checker import check_consistency
from backend.app.plausibility.checker import assess_plausibility
from backend.app.ai_detection.checker import assess_ai_content


def verify_submission(submission: dict[str, Any]) -> dict[str, Any]:
    """Return an overall recommendation and the results of each check."""
    bio = submission.get("bio")
    response = submission.get("questionnaire_response")

    completeness = check_completeness(submission)
    bio_quality = assess_text(bio)
    response_quality = assess_text(response)
    consistency = check_consistency(bio, response)
    plausibility = assess_plausibility(bio, response)
    ai_detection = assess_ai_content(bio, response)

    reasons: list[str] = []

    if consistency["result"] == "Potential Contradiction":
        reasons.extend(consistency["issues"])

    if plausibility["result"] == "Needs Review":
        reasons.extend(plausibility["issues"])

    if reasons:
        verdict = "Flagged for Review"
    else:
        quality_labels = {
            bio_quality["label"],
            response_quality["label"],
        }

        if (
            completeness["result"] == "Incomplete"
            or "Poor" in quality_labels
        ):
            verdict = "Needs Improvement"
            if completeness["result"] == "Incomplete":
                reasons.append(
                    "Required fields are missing: "
                    + ", ".join(completeness["missing_fields"])
                    + "."
                )
            if "Poor" in quality_labels:
                reasons.append(
                    "At least one text field has a Poor quality rating."
                )
        else:
            verdict = "Verified"
            reasons.append(
                "No issues were identified by the implemented checks."
            )

    return {
        "verdict": verdict,
        "reasons": reasons,
        "checks": {
            "completeness": completeness,
            "bio_quality": bio_quality,
            "response_quality": response_quality,
            "consistency": consistency,
            "plausibility": plausibility,
            "ai_detection": ai_detection,
        },
        "review_note": (
            "Automated checks provide preliminary signals, not proof of "
            "truthfulness or authorship. Human review may still be needed."
        ),
    }