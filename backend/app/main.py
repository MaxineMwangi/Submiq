"""FastAPI entry point for Submiq."""

from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict

from backend.app.verification.engine import verify_submission


app = FastAPI(
    title="Submiq Verification API",
    description="API for evaluating onboarding submission quality.",
    version="0.1.0",
)


class SubmissionRequest(BaseModel):
    """Onboarding submission received by the API."""

    model_config = ConfigDict(extra="ignore")

    experience_level: str | None = None
    skills: str | None = None
    bio: str | None = None
    questionnaire_response: str | None = None


@app.get("/health")
def health_check():
    """Confirm that the API is running."""
    return {"status": "ok"}


@app.post("/api/v1/verify")
def verify(request: SubmissionRequest):
    """Evaluate a submission and return its verdict and check results."""
    return verify_submission(request.model_dump())
