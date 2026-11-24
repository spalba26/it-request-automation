import pytest
from app.services import calculate_priority

@pytest.mark.parametrize(
    "impact, urgency, expected",
    [
        ("low", "low", "LOW"),
        ("low", "medium", "LOW"),
        ("low", "high", "MEDIUM"),
        ("medium", "low", "MEDIUM"),
        ("medium", "medium", "MEDIUM"),
        ("medium", "high", "MEDIUM"),
        ("high", "low", "MEDIUM"),
        ("high", "medium", "HIGH"),
        ("high", "high", "HIGH"),
    ],
)
def test_calculate_priority(impact, urgency, expected):
    assert calculate_priority(impact, urgency) == expected