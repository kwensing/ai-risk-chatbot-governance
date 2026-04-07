def calculate_risk(toxicity, bias, hallucination, privacy):
    """
    Aggregate different risk signals into a single score and level.

    toxicity:  tuple (label, score)
    bias: tuple (has_bias: bool, found_terms: list[str])
    hallucination: bool
    privacy: bool
    """
    score = 0
    details = []
    
    # Toxicity: higher weight because of direct harm
    if toxicity[1] > 0.7:
        score += 3
        details.append("High toxicity")

    # Bias: harmful stereotypes / discrimination
    if bias[0]:
        score += 2
        details.append("Potential bias")

    # Hallucination: unreliable content
    if hallucination:
        score += 2
        details.append("Possible hallucination")

    #Privacy: Personally Identifiable Information Leakage
    if privacy:
        score += 3
        details.append("Privacy risk")

    if score >= 6:
        level = "HIGH"
    elif score >= 3:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level, details