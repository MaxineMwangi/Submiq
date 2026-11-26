"""
Explainable, rule-based text quality baseline for Submiq.

Evaluates specificity, clarity, placeholder content, exaggerated claims,
and basic writing signals. It does not verify facts or detect AI authorship.
"""

import re
from typing import Any


PLACEHOLDER_PATTERNS = [
    r"\bwill update\b",
    r"\badd more details\b",
    r"\bnot sure what to put\b",
    r"\bskip for now\b",
    r"\bn/?a for now\b",
    r"\bto be added\b",
    r"\bcant think of\b",
    r"\bcan't think of\b",
    r"\bcant remember\b",
    r"\bcan't remember\b",
]

EXAGGERATION_PATTERNS = [
    r"\bnever\b",
    r"\bevery single\b",
    r"\bwithout fail\b",
    r"\bperfect(?:ly)?\b",
    r"\bthe best\b",
    r"\bno errors\b",
    r"\bno exceptions\b",
    r"\bevery (?:case|trade|prediction|dish|photo|project)\b",
    r"\btrust me\b",
    r"\bno cap\b",
    r"\bsixth sense\b",
    r"\beverything i\b",
]

SPECIFICITY_PATTERNS = [
    r"\b\d+(?:\.\d+)?%?\b",
    r"\b(?:built|developed|implemented|created|analyzed|analysed|reduced|increased|replaced|rewrote|designed|maintained|launched|automated|delivered|managed|deployed|completed|published|shipped)\b",
]


def assess_text(value: Any) -> dict[str, Any]:
    text = "" if value is None else str(value).strip()
    issues = []

    if not text:
        return {"score": 0.0, "label": "Poor", "issues": ["Text is empty."]}

    words = re.findall(r"\b[\w'-]+\b", text)
    word_count = len(words)
    lower_text = text.lower()
    score = 0.60

    if word_count < 5:
        score -= 0.25
        issues.append("Text is very short.")
    elif word_count >= 10:
        score += 0.10

    if any(re.search(pattern, lower_text) for pattern in PLACEHOLDER_PATTERNS):
        score -= 0.35
        issues.append("Text may contain placeholder or incomplete content.")

    exaggerations = sum(
        bool(re.search(pattern, lower_text))
        for pattern in EXAGGERATION_PATTERNS
    )
    if exaggerations:
        score -= min(0.40, exaggerations * 0.15)
        issues.append("Text contains potentially exaggerated or absolute claims.")

    specificity = sum(
        bool(re.search(pattern, lower_text))
        for pattern in SPECIFICITY_PATTERNS
    )
    if specificity >= 2:
        score += 0.20
    elif specificity == 1:
        score += 0.10
    else:
        issues.append("Text provides limited concrete evidence.")

    if re.search(r"\b(?:idk|rn|n stuff|no cap|cant|can't|ive|i've)\b", lower_text):
        score -= 0.10
        issues.append("Text uses informal wording.")

    if word_count >= 5:
        counts = {}
        for word in words:
            normalized = word.lower()
            counts[normalized] = counts.get(normalized, 0) + 1
        if max(counts.values()) / word_count > 0.4:
            score -= 0.15
            issues.append("Text contains excessive word repetition.")

    score = round(max(0.0, min(1.0, score)), 2)

    if score >= 0.70:
        label = "Good"
    elif score >= 0.40:
        label = "Fair"
    else:
        label = "Poor"

    return {"score": score, "label": label, "issues": issues}
