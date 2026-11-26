
import pytest

from backend.app.completeness.checker import (
    calculate_score,
    check_completeness,
    find_missing_fields,
)


@pytest.fixture
def complete_submission():
    return {
        "experience_level": "Intermediate",
        "skills": "Python, SQL",
        "bio": "Student developer",
        "questionnaire_response": "I enjoy solving problems",
    }


def test_complete_submission(complete_submission):
    result = check_completeness(complete_submission)

    assert result["score"] == 1.0
    assert result["result"] == "Complete"
    assert result["missing_fields"] == []


def test_one_missing_field(complete_submission):
    complete_submission["bio"] = ""

    result = check_completeness(complete_submission)

    assert result["score"] == 0.75
    assert result["result"] == "Incomplete"
    assert result["missing_fields"] == ["bio"]


def test_none_is_missing(complete_submission):
    complete_submission["skills"] = None

    assert calculate_score(complete_submission) == 0.75
    assert find_missing_fields(complete_submission) == ["skills"]


def test_whitespace_is_missing(complete_submission):
    complete_submission["bio"] = "   "

    assert calculate_score(complete_submission) == 0.75


def test_all_fields_missing():
    result = check_completeness({})

    assert result["score"] == 0.0
    assert result["result"] == "Incomplete"
    assert len(result["missing_fields"]) == 4


def test_extra_fields_are_ignored(complete_submission):
    complete_submission["email"] = "student@example.com"

    assert calculate_score(complete_submission) == 1.0


def test_nan_is_missing(complete_submission):
    complete_submission["bio"] = float("nan")

    result = check_completeness(complete_submission)

    assert result["score"] == 0.75
    assert result["missing_fields"] == ["bio"]