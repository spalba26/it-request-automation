def calculate_priority(impact: str, urgency:  str) -> str:
    scores={"low": 1, "medium": 2, "high": 3}   
    score = 2 * scores[impact] + scores[urgency]
    if score < 5:
        return "LOW"
    elif score < 8:
        return "MEDIUM"
    else:
        return "HIGH"