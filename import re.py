import re
from collections import defaultdict

def clean_text(text):
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

WEIGHTS = {
    "urgency": 2,
    "scarcity": 3,
    "confirmshaming": 4,
    "drip_pricing": 4,
    "hidden_information": 3
}

RISK_THRESHOLDS = {
    "low": 0,
    "medium": 6,
    "high": 14,
}

def get_risk_level(score: int) -> str:
    if score >= RISK_THRESHOLDS["high"]:
        return "high"
    if score >= RISK_THRESHOLDS["medium"]:
        return "medium"
    return "low"

def score_from_counts(counts: dict) -> dict:
    breakdown = {}
    total = 0
    for category, count in counts.items():
        weight = WEIGHTS.get(category, 0)
        contribution = weight * count
        breakdown[category] = {
            "count": count,
            "weight": weight,
            "contribution": contribution,
        }
        total += contribution
    return {
        "total_score": total,
        "risk_level": get_risk_level(total),
        "breakdown": breakdown,
    }
def counts_from_matches(matches: dict) -> dict:
    return {category: len(hits) for category, hits in matches.items()}

def mock_regex_module_output() -> dict:
    return {
        "urgency": 2,
        "scarcity": 2,
        "confirmshaming": 2,
        "drip_pricing": 2,
        "hidden_information": 3,
    }

TEST_CASES = [
    ("no dark patterns", {}),
    ("only urgency", {"urgency": 5}),
    ("only confirmshaming", {"confirmshaming": 1}),
    ("mixed - should read medium", {"urgency": 1, "scarcity": 1}),
    ("mixed - should read high", mock_regex_module_output()),
]
 
if __name__ == "__main__":
    for label, counts in TEST_CASES:
        result = score_from_counts(counts)
        print(f"\n[{label}]")
        print("  input counts:", counts)
        print("  total_score:", result["total_score"])
        print("  risk_level:", result["risk_level"])