"""JevBench public items: requests sent unchanged, and scoring that mirrors jevbench/scoring.py
and jevbench/metrics.py at the pinned commit.

Mirrored rules: probabilities must cover exactly the item's labels, lie in [0, 1] and sum to 1
within 1e-3 (strict) or 2e-2 (rescaled and flagged); anything else is invalid and wrong. The
answer is the argmax with ties broken by the lexicographically smallest label. Score questions
compare the argmax level with str(expected). Brier is the multi-class sum, which for yes/no is
2 * (p_yes - y)^2.
"""

from __future__ import annotations

import math
from pathlib import Path

from paths import JEVBENCH, read_jsonl

TIERS = ("original", "easy", "hard")
SUM_TOL = 1e-3
RENORM_TOL = 2e-2


class InvalidDistribution(ValueError):
    pass


def load_public_items(directory: Path | str = JEVBENCH) -> list[dict]:
    items = []
    for tier in TIERS:
        for item in read_jsonl(Path(directory) / f"{tier}.jsonl"):
            items.append(dict(item, tier=tier))
    return items


def request_for(item: dict) -> dict:
    return {"state": item["state"], "questions": {"q": item["question"]}}


def probs_from_answer(item: dict, answer) -> dict | None:
    if not isinstance(answer, dict) or answer.get("type") == "refusal":
        return None
    if item["question"]["type"] == "noul":
        if answer.get("noul") is None:
            return None
        p_yes = float(answer["noul"])
        return {"yes": p_yes, "no": 1.0 - p_yes}
    probs = answer.get("probabilities")
    if probs is None:
        return None
    if isinstance(probs, list):
        return {str(i): float(p) for i, p in enumerate(probs)}
    return {str(k): float(v) for k, v in probs.items()}


def validate_probs(probs, labels: list[str], sum_tol: float) -> dict:
    if not isinstance(probs, dict):
        raise InvalidDistribution("probs is not a dict")
    if set(probs) != set(labels):
        raise InvalidDistribution(f"label keys mismatch: got {sorted(probs)} want {sorted(labels)}")
    out = {}
    total = 0.0
    for key, value in probs.items():
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise InvalidDistribution(f"prob[{key!r}] is not a number")
        number = float(value)
        if not math.isfinite(number) or number < 0.0 or number > 1.0:
            raise InvalidDistribution(f"prob[{key!r}] out of [0, 1]: {number}")
        out[str(key)] = number
        total += number
    if abs(total - 1.0) > sum_tol:
        raise InvalidDistribution(f"probs sum to {total}, tolerance {sum_tol}")
    return out


def argmax_label(probs: dict) -> str:
    best, best_p = None, -1.0
    for key in sorted(probs):
        if probs[key] > best_p:
            best, best_p = key, probs[key]
    return best


def expected_value(probs: dict) -> float:
    return sum(float(k) * v for k, v in probs.items())


def _invalid(error: str) -> dict:
    return {"valid": False, "strict_valid": False, "renormalized": False, "error": error,
            "correct": False, "predicted": None, "probs": None}


def score_item(item: dict, probs) -> dict:
    labels = [str(label) for label in item["labels"]]
    try:
        clean = validate_probs(probs, labels, SUM_TOL)
        strict_valid, renormalized = True, False
    except InvalidDistribution as strict_error:
        try:
            clean = validate_probs(probs, labels, RENORM_TOL)
        except InvalidDistribution:
            return _invalid(str(strict_error))
        total = sum(clean.values())
        if total <= 0:
            return _invalid("probabilities sum to zero")
        clean = {k: v / total for k, v in clean.items()}
        strict_valid, renormalized = False, True
    out = {"valid": True, "strict_valid": strict_valid, "renormalized": renormalized, "probs": clean}
    predicted = argmax_label(clean)
    out["predicted"] = predicted
    if item["question"]["type"] == "score":
        out["ordinal_ev"] = expected_value(clean)
    expected = item.get("expected")
    out["correct"] = None if expected is None else predicted == str(expected)
    return out


def brier(probs: dict, expected, labels: list) -> float:
    labels = [str(label) for label in labels]
    expected = str(expected)
    if len(labels) == 2:
        p_yes = float(probs[expected])
        other = labels[0] if labels[1] == expected else labels[1]
        p_no = float(probs.get(other, 1.0 - p_yes))
        return (p_yes - 1.0) ** 2 + p_no ** 2
    return sum((float(probs.get(label, 0.0)) - (1.0 if label == expected else 0.0)) ** 2 for label in labels)


def chance_corrected(accuracy: float, chance: float) -> float:
    return max(0.0, (accuracy - chance) / (1.0 - chance))


def tier_chance(items: list[dict]) -> float:
    return sum(1.0 / len(item["labels"]) for item in items) / len(items)
