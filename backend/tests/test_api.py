from fastapi.testclient import TestClient

from backend.app.main import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_verify_endpoint_returns_expected_structure():
    response = client.post(
        "/api/v1/verify",
        json={
            "experience_level": "Intermediate",
            "skills": "Python, SQL, networking",
            "bio": (
                "I am a computer science student interested in "
                "cybersecurity and software development."
            ),
            "questionnaire_response": (
                "I have worked on Python projects and database applications. "
                "I want to improve my software development and security skills."
            ),
        },
    )

    assert response.status_code == 200

    result = response.json()
    assert result["verdict"] in {
        "Verified",
        "Needs Improvement",
        "Flagged for Review",
    }
    assert "reasons" in result
    assert "checks" in result
    assert "review_note" in result

    assert {
        "completeness",
        "bio_quality",
        "response_quality",
        "consistency",
        "plausibility",
        "ai_detection",
    }.issubset(result["checks"])


def test_verify_endpoint_accepts_missing_optional_fields():
    response = client.post(
        "/api/v1/verify",
        json={
            "bio": "I am a student learning software development.",
            "questionnaire_response": "I want to improve my technical skills.",
        },
    )

    assert response.status_code == 200
    assert response.json()["verdict"] in {
        "Verified",
        "Needs Improvement",
        "Flagged for Review",
    }
