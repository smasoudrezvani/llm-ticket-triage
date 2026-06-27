import json

from ticket_triage.data import RESPONSE_TAG, format_example, format_prompt


def test_format_example_contains_ticket_and_label():
    out = format_example("My order never arrived", "delivery_issue", "high")
    assert "My order never arrived" in out
    assert '"category": "delivery_issue"' in out
    assert '"priority": "high"' in out


def test_inference_prompt_is_prefix_of_training_example():
    text = "My order never arrived"
    full = format_example(text, "delivery_issue", "high")
    prompt = format_prompt(text)
    # the inference prompt must be exactly the start of the training string
    assert full.startswith(prompt.rstrip())


def test_completion_is_valid_json():
    out = format_example("App keeps crashing", "app_issue", "medium")
    completion = out.split(RESPONSE_TAG, 1)[1]
    parsed = json.loads(completion)
    assert parsed == {"category": "app_issue", "priority": "medium"}


def test_invalid_label_is_rejected():
    import pytest
    from pydantic import ValidationError

    with pytest.raises(ValidationError):
        format_example("whatever", "not_a_real_category", "high")