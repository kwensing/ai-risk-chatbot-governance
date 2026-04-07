import pytest

from risk_evaluator import check_toxicity, check_bias, check_hallucination, check_privacy
from risk_scoring import calculate_risk

def test_bias_detection_simple():
    text = "Men and women should have equal access to treatment."
    has_bias, terms = check_bias(text)
    assert has_bias is True
    assert "male" not in terms  # depending on your keywords
    assert "female" not in terms  # adjust this depending on your list

def test_privacy_detection_email():
    text = "Contact me at patient@example.com for more information."
    assert check_privacy(text) is True

def test_privacy_detection_credit_card():
    text = "My card is 4111 1111 1111 1111."
    assert check_privacy(text) is True

def test_hallucination_flag_uncertainty():
    response = "I am not sure, but this might help."
    assert check_hallucination(response) is True

def test_risk_scoring_high_privacy():
    # toxicity: (label, score)
    toxicity = ("NON_TOXIC", 0.1)
    bias = (False, [])
    hallucination = False
    privacy = True

    score, level, details = calculate_risk(toxicity, bias, hallucination, privacy)
    assert score >= 3
    assert level in ("MEDIUM", "HIGH")
    assert any("Privacy" in d for d in details)

def test_risk_scoring_high_toxicity_and_privacy():
    toxicity = ("TOXIC", 0.9)
    bias = (False, [])
    hallucination = False
    privacy = True

    score, level, details = calculate_risk(toxicity, bias, hallucination, privacy)
    assert score >= 6
    assert level == "HIGH"
    assert "High toxicity" in details
    assert "Privacy risk" in details