"""Tests for the Submiq FastAPI endpoints."""

from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


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


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_verify_endpoint_returns_verdict_and_checks():
    response = client.post("/api/v1/verify", json=valid_submission())

    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "Verified"
    assert "reasons" in data
    assert "checks" in data
    assert "review_note" in data


def test_verify_endpoint_handles_missing_fields():
    submission = valid_submission()
    submission.pop("skills")

    response = client.post("/api/v1/verify", json=submission)

    assert response.status_code == 200
    data = response.json()
    assert data["verdict"] == "Needs Improvement"
    assert data["checks"]["completeness"]["result"] == "Incomplete"


def test_verify_endpoint_ignores_unrecognized_fields():
    submission = valid_submission()
    submission["unexpected_field"] = "ignored"

    response = client.post("/api/v1/verify", json=submission)

    assert response.status_code == 200
    assert response.json()["verdict"] == "Verified"
