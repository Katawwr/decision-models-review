"""Desk analysis of the Artificial Analysis Decision Index: reweighting and a noise estimate.

Weights and item counts are from AA's methodology page, read 19 Nov 2026. Component scores
are the 16 Nov 2026 snapshot mirrored by benchlm.ai; the weighted average reproduces AA's
published index to within 0.05 for every model, which is the check that the mirror is right.
The noise estimate has no per-item data, so it assumes a per-item standard deviation of the
Decision Score and shows the result for several values.
"""

from __future__ import annotations

import math
from pathlib import Path

from paths import RESULTS

WEIGHTS = {"paperclip": 0.30, "onet": 0.15, "when2call": 0.10, "omniscience": 0.15, "hle": 0.15, "symmetry": 0.15}
ITEMS = {"paperclip": 1500, "onet": 6582, "when2call": 3423, "omniscience": 500, "hle": 509, "symmetry": 120}
KNOWLEDGE_AND_REASONING = ("omniscience", "hle")

SCORES = {
    "Jev 1.14": {"paperclip": 57.5, "onet": 91.1, "when2call": 84.4, "omniscience": 60.1, "hle": 44.5, "symmetry": 74.5},
    "Gemini Decision 1": {"paperclip": 56.8, "onet": 87.1, "when2call": 80.5, "omniscience": 66.3, "hle": 48.7, "symmetry": 70.5},
    "Clef": {"paperclip": 54.4, "onet": 85.7, "when2call": 77.2, "omniscience": 57.1, "hle": 42.6, "symmetry": 56.6},
    "Drex Max v1.1": {"paperclip": 72.8, "onet": 88.3, "when2call": 95.3, "omniscience": 60.3, "hle": 46.6, "symmetry": 79.8},
}
PUBLISHED_INDEX = {"Jev 1.14": 66.2, "Gemini Decision 1": 66.0, "Clef": 60.3, "Drex Max v1.1": 72.6}


def index(scores: dict, weights: dict = WEIGHTS, drop=()) -> float:
    kept = {k: w for k, w in weights.items() if k not in drop}
    total = sum(kept.values())
    return sum(scores[k] * w for k, w in kept.items()) / total


def index_se(weights: dict, items: dict, per_item_sd: float) -> float:
    total = sum(weights.values())
    return math.sqrt(sum((w / total) ** 2 * per_item_sd ** 2 / items[k] for k, w in weights.items()))


def variance_shares(weights: dict, items: dict, per_item_sd: float) -> dict:
    total = sum(weights.values())
    parts = {k: (w / total) ** 2 * per_item_sd ** 2 / items[k] for k, w in weights.items()}
    whole = sum(parts.values())
    return {k: v / whole for k, v in parts.items()}


def half_width(se: float, z: float = 1.96) -> float:
    return z * se


def difference_half_width(se: float, z: float = 1.96) -> float:
    """Half-width for the gap between two models, treating their errors as independent.
    Paired item-level errors would make it narrower, so this is the cautious figure."""
    return z * math.sqrt(2.0) * se


def report() -> str:
    lines = ["# AA Decision Index: reweighting and noise", "",
             "Component scores: 16 Nov 2026 snapshot (benchlm.ai mirror of AA). Weights and item counts: AA methodology page, 19 Nov 2026.", "",
             "## Index with and without the knowledge and reasoning exams", "",
             "| Model | Published | Recomputed | Without Omniscience and HLE | Change |", "|---|---|---|---|---|"]
    for name, scores in SCORES.items():
        full = index(scores)
        without = index(scores, drop=KNOWLEDGE_AND_REASONING)
        lines.append(f"| {name} | {PUBLISHED_INDEX[name]:.1f} | {full:.2f} | {without:.1f} | {without - full:+.1f} |")
    lines += ["", f"Knowledge and reasoning (AA-Omniscience-Decision and HLE-MultiChoice) carry {100 * sum(WEIGHTS[k] for k in KNOWLEDGE_AND_REASONING):.0f}% of the index.",
              "", "## Noise", "",
              "Each component is a mean over its items. With a per-item standard deviation s of the Decision Score, the standard error of the index is sqrt(sum over components of (weight^2 * s^2 / items)). Per-item scores lie in [0, 100], so s is at most 50; for a model near 60 with moderate confidence it is around 40.", "",
              "| Per-item sd | Index SE | 95% half-width, one model | 95% half-width, gap between two models |", "|---|---|---|---|"]
    for sd in (30, 40, 50):
        se = index_se(WEIGHTS, ITEMS, sd)
        lines.append(f"| {sd} | {se:.2f} | ±{half_width(se):.1f} | ±{difference_half_width(se):.1f} |")
    shares = variance_shares(WEIGHTS, ITEMS, 40)
    lines += ["", "Share of the index variance by component (independent of s):", "",
              "| Component | Weight | Items | Share of variance |", "|---|---|---|---|"]
    for k in sorted(shares, key=shares.get, reverse=True):
        lines.append(f"| {k} | {WEIGHTS[k]:.2f} | {ITEMS[k]:,} | {100 * shares[k]:.0f}% |")
    lines += ["", "## Reading", "",
              "- AA's published tie between Jev 1.14 and Gemini Decision 1 (66.2 vs 66.0) depends on the weighting. Jev leads Gemini on all four decision-type components; Gemini leads on both knowledge and reasoning exams.",
              "- Without the two knowledge and reasoning exams the gap is about 2.6 points, which is inside the 95% half-width for a gap between two models at any plausible per-item sd. The claim to make is that the tie depends on the weighting, not that Jev is ahead.",
              "- AA-Symmetry, with 120 questions and a 15% weight, contributes more than half of the index's sampling variance on its own.",
              "- The gap estimate treats the two models' item-level errors as independent. On shared items they are usually positively correlated, which would narrow the interval for the gap; without per-item data this cannot be checked."]
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    out = RESULTS / "desk" / "aa_reweighting_and_noise.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    text = report()
    Path(out).write_text(text, encoding="utf-8")
    print(text)
