from backend.app.consistency.checker import check_consistency


def test_consistent_text():
    result = check_consistency(
        "I have 3 years of experience in data analysis.",
        "I have 3 years of experience building dashboards."
    )
    assert result["result"] == "No Explicit Contradiction Detected"


def test_conflicting_years():
    result = check_consistency(
        "I have 3 years of experience in data analysis.",
        "I have 8 years of experience in data analysis."
    )
    assert result["result"] == "Potential Contradiction"


def test_conflicting_experience_claims():
    result = check_consistency(
        "I have no experience in Python.",
        "I have extensive experience in Python."
    )
    assert result["result"] == "Potential Contradiction"


def test_missing_bio():
    result = check_consistency(
        None,
        "I built a dashboard using Python."
    )
    assert result["result"] == "Unable to Assess"


def test_missing_questionnaire():
    result = check_consistency(
        "I am a data analyst.",
        ""
    )
    assert result["result"] == "Unable to Assess"


def test_unrelated_text_is_not_flagged():
    result = check_consistency(
        "I work as a data analyst.",
        "I enjoy building dashboards."
    )
    assert result["result"] == "No Explicit Contradiction Detected"
