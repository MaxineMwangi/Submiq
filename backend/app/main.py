"""FastAPI entry point for Submiq verification."""

from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from backend.app.verification.engine import verify_submission

app = FastAPI(
    title="Submiq Verification API",
    description="Explainable onboarding submission verification.",
    version="0.1.0",
)


class SubmissionRequest(BaseModel):
    """Submission fields accepted by the verification engine."""

    model_config = ConfigDict(extra="ignore")

    experience_level: str | None = None
    skills: str | None = None
    bio: str | None = None
    questionnaire_response: str | None = None


@app.get("/health")
def health() -> dict[str, str]:
    """Report API availability."""
    return {"status": "ok"}


@app.post("/api/v1/verify")
def verify(request: SubmissionRequest) -> dict[str, Any]:
    """Run the existing verification checks on a submission."""
    return verify_submission(request.model_dump())
