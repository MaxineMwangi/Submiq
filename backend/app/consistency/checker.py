"""
Explainable cross-field consistency baseline for Submiq.

Detects selected contradictions between a bio and questionnaire response.
It does not verify factual truth or establish that undetected claims agree.
"""

import re
from typing import Any


SENIOR_EXPERIENCE = re.compile(
    r"\b(?:"
    r"\d+\s*\+?\s*years?\s+(?:of\s+)?experience|"
    r"senior\s+\w+|"
    r"chief operating officer|"
    r"vice president|"
    r"registered nurse|"
    r"licensed veterinarian|"
    r"licensed architect|"
    r"senior python architect|"
    r"currently manage|"
    r"have worked as|"
    r"i've worked as|"
    r"i have worked as|"
    r"i spent a decade"
    r")\b",
    re.IGNORECASE,
)

NOVICE_CLAIMS = re.compile(
    r"\b(?:"
    r"never sold anything before|"
    r"first job of any kind|"
    r"first job application ever|"
    r"no professional experience|"
    r"first-year computer science student|"
    r"first internship|"
    r"never worked in an office before|"
    r"still learning the basics|"
    r"don't really use computers much|"
    r"never designed a building before|"
    r"never built or deployed a project before"
    r")\b",
    re.IGNORECASE,
)

ROLE_TERMS = {
    "accounting": r"\b(?:bookkeeper|accountant|tax preparer)\b",
    "restaurant": r"\b(?:line cook|chef|cook)\b",
    "sales": r"\b(?:sales territory|sales pipeline|sales representative|sales manager)\b",
    "nursing": r"\b(?:registered nurse|nurse|pediatric ward)\b",
    "graphic design": r"\b(?:graphic designer|brand identity|print materials)\b",
    "software engineering": r"\b(?:backend engineer|software engineer|python architect)\b",
    "investment banking": r"\b(?:investment bank|m&a deals|vice president)\b",
    "teaching": r"\b(?:teacher|taught high school|teaching)\b",
    "mechanical engineering": r"\b(?:mechanical engineer|turbine components)\b",
    "executive management": r"\b(?:chief operating officer|overseeing all day-to-day operations)\b",
    "cybersecurity": r"\b(?:cybersecurity analyst|penetration tests|incident response)\b",
    "veterinary": r"\b(?:veterinarian|small-animal practice)\b",
    "architecture": r"\b(?:licensed architect|commercial buildings|designed a building)\b",
}


def normalize(value: Any) -> str:
    """Normalize a field and treat missing values as empty."""
    if value is None:
        return ""
    text = str(value).strip()
    if not text or text.lower() in {"nan", "none"}:
        return ""
    return re.sub(r"\s+", " ", text).lower()


def find_roles(text: str) -> set[str]:
    """Find occupation or professional-domain signals."""
    return {
        role
        for role, pattern in ROLE_TERMS.items()
        if re.search(pattern, text, re.IGNORECASE)
    }


def extract_years(text: str) -> list[int]:
    """Extract explicit claims about years of professional experience."""
    patterns = [
        r"\b(\d+)\s*\+?\s*years?\s+(?:of\s+)?experience\b",
        r"\b(?:for|over|about|around)\s+(\d+)\s+years?\b",
    ]
    values = []
    for pattern in patterns:
        values.extend(int(value) for value in re.findall(pattern, text))
    return values


def check_consistency(
    bio: Any,
    questionnaire_response: Any,
) -> dict[str, Any]:
    """Return a preliminary consistency result and explanations."""
    bio_text = normalize(bio)
    response_text = normalize(questionnaire_response)
    issues = []

    if not bio_text or not response_text:
        missing = []
        if not bio_text:
            missing.append("bio")
        if not response_text:
            missing.append("questionnaire_response")
        return {
            "result": "Unable to Assess",
            "issues": ["Missing text in: " + ", ".join(missing)],
        }

    bio_years = extract_years(bio_text)
    response_years = extract_years(response_text)

    if bio_years and response_years and set(bio_years).isdisjoint(response_years):
        issues.append(
            "Experience duration claims differ between the bio and questionnaire response."
        )

    explicit_contradictions = [
        (r"\bno experience\b", r"\bextensive experience\b"),
        (r"\bnever used\b", r"\b(?:regularly use|extensive use of)\b"),
        (r"\bno knowledge of\b", r"\bexpert in\b"),
    ]

    for first, second in explicit_contradictions:
        if (
            re.search(first, bio_text) and re.search(second, response_text)
        ) or (
            re.search(second, bio_text) and re.search(first, response_text)
        ):
            issues.append(
                "The bio and questionnaire contain conflicting experience or skill claims."
            )
            break

    bio_has_senior_experience = bool(SENIOR_EXPERIENCE.search(bio_text))
    response_claims_novice_status = bool(NOVICE_CLAIMS.search(response_text))

    # Detect opposing experience claims about the same named skill.
    no_experience = re.search(r"\bno experience in\s+(\w+)", bio_text)
    extensive_experience = re.search(
        r"\bextensive experience in\s+(\w+)", response_text
    )
    reverse_no_experience = re.search(
        r"\bno experience in\s+(\w+)", response_text
    )
    reverse_extensive_experience = re.search(
        r"\bextensive experience in\s+(\w+)", bio_text
    )

    if (
        no_experience and extensive_experience
        and no_experience.group(1) == extensive_experience.group(1)
    ) or (
        reverse_no_experience and reverse_extensive_experience
        and reverse_no_experience.group(1) == reverse_extensive_experience.group(1)
    ):
        issues.append(
            "The bio and questionnaire make conflicting experience claims about the same skill."
        )

    if bio_has_senior_experience and response_claims_novice_status:
        issues.append(
            "The bio claims substantial professional experience, "
            "but the questionnaire describes novice status or no prior experience."
        )

    bio_roles = find_roles(bio_text)
    response_roles = find_roles(response_text)

    shared_roles = bio_roles & response_roles
    distinct_roles = bio_roles - response_roles, response_roles - bio_roles

    # Only compare different roles when both fields explicitly contain
    # occupational signals and the response describes a role or work history.
    response_describes_role = bool(re.search(
        r"\b(?:my most recent role|as a|worked as|i work as|i'm a|"
        r"i am a|i've been a|i have been a)\b",
        response_text,
    ))

    if response_describes_role and bio_roles and response_roles:
        bio_only, response_only = distinct_roles
        if bio_only and response_only and not shared_roles:
            issues.append(
                "The bio and questionnaire describe different professional roles; "
                "these claims may need review."
            )

    if issues:
        return {"result": "Potential Contradiction", "issues": issues}

    return {
        "result": "No Explicit Contradiction Detected",
        "issues": [],
    }
