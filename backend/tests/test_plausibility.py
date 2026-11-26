
from backend.app.plausibility.checker import assess_plausibility


def test_normal_claim_has_no_warning():
    result = assess_plausibility(
        "I developed a student budgeting application using Python."
    )
    assert result["result"] == "No Warning Detected"


def test_guaranteed_claim_is_flagged():
    result = assess_plausibility(
        "I guarantee success in every project."
    )
    assert result["result"] == "Needs Review"


def test_extreme_percentage_is_flagged():
    result = assess_plausibility(
        "Our product achieved 5000% growth."
    )
    assert result["result"] == "Needs Review"


def test_missing_text():
    result = assess_plausibility(None, "")
    assert result["result"] == "Unable to Assess"


def test_normal_claim_is_not_automatically_flagged():
    result = assess_plausibility(
        "I have three years of experience in software development."
    )
    assert result["result"] == "No Warning Detected"


def test_absolute_claim_is_flagged():
    result = assess_plausibility(
        "Every client I train gets perfect results without exception."
    )
    assert result["result"] == "Needs Review"


def test_extreme_achievement_is_flagged():
    result = assess_plausibility(
        "My app has one billion downloads."
    )
    assert result["result"] == "Needs Review"


def test_conflicting_experience_is_flagged():
    result = assess_plausibility(
        "I am a senior cybersecurity analyst with nine years of experience.",
        "I have never worked in tech and am learning the basics."
    )
    assert result["result"] == "Needs Review"
