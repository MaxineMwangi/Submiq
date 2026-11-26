from backend.app.text_quality.checker import assess_text


def test_empty_text_is_poor():
    result = assess_text("")
    assert result["label"] == "Poor"
    assert result["score"] == 0.0


def test_none_is_handled():
    result = assess_text(None)
    assert result["label"] == "Poor"


def test_short_text_is_flagged():
    result = assess_text("I am a developer")
    assert "Text is very short." in result["issues"]


def test_placeholder_content_is_flagged():
    result = assess_text("I am a developer and will update my profile later.")
    assert any("placeholder" in issue.lower() for issue in result["issues"])


def test_good_text_receives_good_label():
    result = assess_text(
        "I am a software developer with experience in Python and database design. "
        "I enjoy building useful applications and solving technical problems."
    )
    assert result["label"] == "Good"
    assert result["score"] >= 0.7


def test_repeated_words_are_flagged():
    result = assess_text("Python Python Python Python Python Python Python")
    assert any("repetition" in issue.lower() for issue in result["issues"])


def test_result_has_expected_fields():
    result = assess_text("I develop applications using Python and SQL.")
    assert set(result.keys()) == {"score", "label", "issues"}
    assert 0.0 <= result["score"] <= 1.0
    assert result["label"] in {"Good", "Fair", "Poor"}
    assert isinstance(result["issues"], list)

