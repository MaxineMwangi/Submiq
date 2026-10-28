"""
Rule-based plausibility baseline for Submiq.

Flags potentially exaggerated claims and cross-field contradictions
for human review. It does not establish factual truth.
"""

import math
import re
from typing import Any


ABSOLUTE_CLAIM_PATTERNS = [
    r"\bguarante(?:e|ed|es)\b",
    r"\b100\s*%\b",
    r"\b(?:never|zero)\s+(?:lost|losses|errors|bugs|complaints|disputes|failures|escalations)\b",
    r"\b(?:every|all)\s+(?:single\s+)?(?:client|customer|student|trade|prediction|investment|deal|project|campaign|case|ticket|dish|photo|photograph|repair|process|contract|benchmark|property|student|patient)\b",
    r"\b(?:without exception|no exceptions|not even once|every time|first try|first attempt)\b",
    r"\b(?:best|greatest|fastest)\b.{0,60}\b(?:ever|in the world|in this industry|this city|this school)\b",
    r"\b(?:perfect|flawless|unmatched|unparalleled|unprecedented)\b",
    r"\b(?:everyone|everybody)\s+(?:loves|praises|knows)\b",
    r"\bno\s+(?:chance|risk)\s+of\s+(?:failure|loss)\b",
]

EXTREME_QUANTITY_PATTERNS = [
    r"\b(?:billions?|trillions?)\s+(?:of\s+)?(?:dollars|users|customers|sales|downloads)\b",
    r"\b\d{3,}\s*%\s*(?:growth|increase|return|profit|accuracy|success)\b",
    r"\b(?:million|billion)\s+(?:users|downloads|customers|dollars)\b",
    r"\b\d+\s+(?:peer-reviewed papers|patents)\b",
    r"\b(?:every major celebrity|every major company|fortune 500)\b",
    r"\b(?:overnight|within a week|in one week|in two weeks|in 48 hours)\b",
]

CONTRADICTION_PAIRS = [
    (
        r"\b(?:senior|experienced|licensed|registered|expert|architect|analyst|attorney|nurse|veterinarian|chief operating officer|coo)\b",
        r"\b(?:first job|first internship|never (?:built|worked|designed|sold)|never done|high school student|first-year student|sophomore in high school|learning the basics|no professional experience)\b",
    ),
    (
        r"\b(?:manage|managed|led|leading|closed|built|developed|served as|years of experience|career)\b",
        r"\b(?:never (?:worked|built|sold|designed)|haven't worked|have not worked|first job of any kind|never built or deployed)\b",
    ),
]


def normalize(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none", "tbd", "will fill in later"}:
        return ""
    return re.sub(r"\s+", " ", text)


def assess_plausibility(*values: Any) -> dict[str, Any]:
    """Flag warning signals in supplied text for human review."""
    texts = [normalize(value) for value in values]
    combined = " ".join(text for text in texts if text).lower()

    if not combined:
        return {
            "result": "Unable to Assess",
            "issues": ["No text was provided for assessment."],
        }

    issues = []

    if any(re.search(pattern, combined, re.IGNORECASE)
           for pattern in ABSOLUTE_CLAIM_PATTERNS):
        issues.append(
            "The text contains an absolute or unusually strong claim."
        )

    if any(re.search(pattern, combined, re.IGNORECASE)
           for pattern in EXTREME_QUANTITY_PATTERNS):
        issues.append(
            "The text contains an extreme achievement or numerical claim that may need evidence."
        )

    if len(texts) >= 2:
        bio, response = texts[0].lower(), texts[1].lower()
        for experience_pattern, contradiction_pattern in CONTRADICTION_PAIRS:
            if (re.search(experience_pattern, bio, re.IGNORECASE)
                    and re.search(contradiction_pattern, response, re.IGNORECASE)):
                issues.append(
                    "The bio and questionnaire response may contain conflicting experience claims."
                )
                break

    if issues:
        return {"result": "Needs Review", "issues": issues}

    return {"result": "No Warning Detected", "issues": []}
