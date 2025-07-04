import datetime as dt
from project import compute_score, choose_beach, format_report

MOCK_FORECAST = {
    "hours": [
        {"waveHeight": {"noaa": 1.0}, "windSpeed": {"noaa": 6}}
    ] * 8
}

def test_compute_score_typical():
    assert 5 <= compute_score(MOCK_FORECAST) <= 10

def test_choose_beach():
    assert choose_beach({"A": 3.0, "B": 2.0}) == "A"

def test_format_report_contains_best():
    scores = {"A": 3.0, "B": 2.0}
    best = choose_beach(scores)
    assert "Recommendation: A" in format_report(scores, best, dt.date(2025, 7, 4))
