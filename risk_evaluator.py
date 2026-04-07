from transformers import pipeline
import re

# Toxicity classifier using Hugging Face model
toxic_model_name = "unitary/toxic-bert"
toxicity_model = pipeline("text-classification", model=toxic_model_name)

def check_toxicity(text: str):
    """
    Return (label, score) from the toxicity model.
    Truncate long inputs to avoid exceeing the model's max length.
    """
    # Hugging Face BERT models typically support up to 512 tokesn.
    # Defensively truncate the text before sending it to the model.
    result = toxicity_model(
        text,
        truncation=True,
        max_length=512,
    )[0]
    return result["label"], float(result["score"])

def check_bias(text: str):
    """
    Naive bias detection based on keywords.
    Returns (has_bias, found_terms).
    """
    bias_keywords = ["male", "female", "man", "men", "woman", "women", "race", "religion", "gender"]
    lowered = text.lower()
    found = [word for word in bias_keywords if word in lowered]
    return len(found) > 0, found

def check_hallucination(response: str):
    """
    Simple heuristic fact check: 
    if the model expresses uncertainty then flag it as possible hallucination.
    """
    uncertainty_words = ["might", "possibly", "uncertain", "not sure"]
    lowered = response.lower()
    return any(u in lowered for u in uncertainty_words)

def check_privacy(text: str):
    """
    Detect obvious personal data patterns (credit card numbers, email addresses).
    To add more robust detection if required.
    """
    patterns = [
        # Credit card: 16 digits, possibly separated
        r"\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b",
        # Email address
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
    ]

    for p in patterns:
        if re.search(p, text, re.IGNORECASE):
            return True
    return False