"""Tests for Submiq's overall verification engine."""

from backend.app.verification.engine import verify_submission


def valid_submission():
    return {
        "experience_level": "Intermediate",
        "skills": "Python, SQL, and data analysis",
        "bio": (
            "I developed a sales dashboard using Python and SQL. "
            "The dashboard reduced weekly reporting time by 20 percent."
        ),
        "questionnaire_response": (
            "I analyzed sales records and created charts for the team. "
            "I tested the dashboard with five users."
        ),
    }


def test_complete_submission_without_warnings_is_verified():
    result = verify_submission(valid_submission())
    assert result["verdict"] == "Verified"
    assert "checks" in result
    assert "review_note" in result


def test_missing_required_field_needs_improvement():
    submission = valid_submission()
    submission["skills"] = ""
    result = verify_submission(submission)
    assert result["verdict"] == "Needs Improvement"


def test_poor_text_needs_improvement():
    submission = valid_submission()
    submission["bio"] = "N/A for now"
    result = verify_submission(submission)
    assert result["verdict"] == "Needs Improvement"


def test_plausibility_warning_takes_priority():
    submission = valid_submission()
    submission["bio"] = (
        "I guarantee 100% success in every single project."
    )
    result = verify_submission(submission)
    assert result["verdict"] == "Flagged for Review"


def test_consistency_contradiction_takes_priority():
    submission = valid_submission()
    submission["bio"] = (
        "I have 10 years of experience in software engineering."
    )
    submission["questionnaire_response"] = (
        "This is my first job of any kind and I have no professional experience."
    )
    result = verify_submission(submission)
    assert result["verdict"] == "Flagged for Review"


def test_ai_style_result_is_reported_separately_from_verdict():
    submission = valid_submission()
    result = verify_submission(submission)

    assert result["verdict"] == "Verified"
    assert result["checks"]["ai_detection"]["result"] == "Human"
    assert "review_note" in result


def test_result_includes_reasons_and_all_checks():
    result = verify_submission(valid_submission())
    assert isinstance(result["reasons"], list)
    assert set(result["checks"]) == {
        "completeness",
        "bio_quality",
        "response_quality",
        "consistency",
        "plausibility",
        "ai_detection",
    }