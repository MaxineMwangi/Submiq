"""
Experimental AI-style detection baseline for Submiq.

Scores formulaic language separately in the bio and questionnaire response.
Style signals are not proof of AI authorship.
"""

import math
import re
from typing import Any


AI_STYLE_PATTERNS = [
    r"\bleverage\b",
    r"\bsynergistic\b",
    r"\btransformative\b",
    r"\bunparalleled\b",
    r"\bcutting[- ]edge\b",
    r"\bresults[- ]driven\b",
    r"\bcomprehensive understanding\b",
    r"\bconsistently deliver(?:s|ed|ing)?\b",
    r"\bempower(?:s|ing|ed)?\b",
    r"\bproven track record\b",
    r"\bfoster(?:s|ing|ed)?\b",
    r"\bpassionate\b",
    r"\bcommitted to\b",
    r"\bseamless(?:ly)?\b",
    r"\b(?:unprecedented|exceptional|unmatched)\b",
    r"\b(?:dynamic|visionary|meticulous|detail-oriented)\b",
    r"\bdrive (?:meaningful|strategic|sustainable|measurable)\b",
    r"\b(?:holistic|client-centric|user-centric|mission-driven)\b",
    r"\b(?:actionable insights|operational excellence|stakeholder alignment)\b",
]


def normalize(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value).strip()
    if text.lower() in {"nan", "none"}:
        return ""
    return re.sub(r"\s+", " ", text)


def score_ai_style(value: Any) -> int:
    text = normalize(value).lower()
    return sum(
        1 for pattern in AI_STYLE_PATTERNS
        if re.search(pattern, text, re.IGNORECASE)
    )


def assess_ai_content(bio: Any, questionnaire_response: Any) -> dict[str, Any]:
    bio_text = normalize(bio)
    response_text = normalize(questionnaire_response)

    if not bio_text and not response_text:
        return {
            "result": "Unable to Assess",
            "bio_score": 0,
            "response_score": 0,
            "reason": "No text was provided.",
        }

    bio_score = score_ai_style(bio_text)
    response_score = score_ai_style(response_text)

    # Two or more distinct style signals indicate a formulaic field.
    bio_flagged = bio_score >= 2
    response_flagged = response_score >= 2

    if bio_flagged and response_flagged:
        result = "AI"
    elif bio_flagged or response_flagged:
        result = "Mixed"
    else:
        result = "Human"

    return {
        "result": result,
        "bio_score": bio_score,
        "response_score": response_score,
        "reason": (
            "Classification is based on predefined writing-style signals, "
            "not verified authorship."
        ),
    }
