from backend.app.ai_detection.checker import assess_ai_content, score_ai_style


def test_empty_text_is_unable_to_assess():
    result = assess_ai_content(None, "")
    assert result["result"] == "Unable to Assess"


def test_plain_specific_text_is_not_flagged_as_ai():
    result = assess_ai_content(
        "I built a budgeting app using Python and SQLite.",
        "I tested it with five classmates and fixed two bugs."
    )
    assert result["result"] == "Human"


def test_formulaic_text_in_both_fields_is_flagged_ai():
    result = assess_ai_content(
        "I leverage a comprehensive understanding to deliver transformative outcomes.",
        "I consistently deliver unparalleled results and empower organizations."
    )
    assert result["result"] == "AI"


def test_formulaic_text_in_one_field_is_flagged_mixed():
    result = assess_ai_content(
        "I leverage a comprehensive understanding to deliver transformative outcomes.",
        "I fixed two bugs in my Python project."
    )
    assert result["result"] == "Mixed"


def test_style_score_counts_distinct_patterns():
    assert score_ai_style("I leverage a comprehensive understanding.") == 2
