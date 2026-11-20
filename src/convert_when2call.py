"""When2Call as Artificial Analysis runs it: AA's 229 filtered tasks removed, each task a choice
among the four candidate replies under neutral labels, option order shuffled per task with a
fixed seed, scored with AA's Decision Score.

AA's filtered list names BFCL source IDs. Each listed source ID has three When2Call variants
(tool_call, request_for_info, cannot_answer); AA filters "ask for more information" tasks, so
the request_for_info variant of each listed ID is removed. That leaves 3,423 tasks, AA's count.
"""

from __future__ import annotations

import random
from pathlib import Path

from paths import AA_FILTERED_IDS, WHEN2CALL, read_jsonl

CATEGORIES = ("tool_call", "request_for_info", "cannot_answer", "direct")
LABELS = ("A", "B", "C", "D")
DEFAULT_SEED = 20261119
INSTRUCTIONS = (
    "An assistant with the listed tools has received the user's message. Which of the four candidate "
    "replies should the assistant give?"
)


def load_items(path: Path | str = WHEN2CALL) -> list[dict]:
    return read_jsonl(path)


def load_filtered_source_ids(path: Path | str = AA_FILTERED_IDS) -> set[str]:
    return {line.strip() for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()}


def apply_aa_filter(items: list[dict], filtered_ids: set[str]) -> tuple[list[dict], list[dict]]:
    kept, removed = [], []
    for item in items:
        if item["source_id"] in filtered_ids and item["correct_answer"] == "request_for_info":
            removed.append(item)
        else:
            kept.append(item)
    return kept, removed


def build_task(item: dict, seed: int = DEFAULT_SEED, named: bool = False) -> dict:
    """One When2Call task as a choice question. Labels are A to D in a per-task shuffled order,
    or, with named=True, the category names themselves in the same shuffled order."""
    rng = random.Random(f"{seed}:{item['uuid']}")
    categories = list(CATEGORIES)
    rng.shuffle(categories)
    option_to_category = dict(zip(categories if named else LABELS, categories))
    criteria = {label: item["answers"][category] for label, category in option_to_category.items()}
    correct_label = next(label for label, category in option_to_category.items() if category == item["correct_answer"])
    tools = "\n".join(item["tools"])
    state = f"TOOLS AVAILABLE TO THE ASSISTANT:\n{tools}\n\nUSER MESSAGE:\n{item['question']}"
    return {
        "uuid": item["uuid"],
        "source_id": item.get("source_id"),
        "state": state,
        "question": {"type": "choice", "instructions": INSTRUCTIONS, "criteria": criteria},
        "option_to_category": option_to_category,
        "correct_label": correct_label,
        "correct_answer": item["correct_answer"],
    }


def decision_score(correct: bool, p: float) -> float:
    c = 1.0 if correct else 0.0
    return 50.0 * (1.0 + c - (p - c) ** 2)


def missing_answer_score(n_options: int) -> float:
    return 50.0 * (1.0 + 1.0 / n_options ** 2)


def score_task(task: dict, answer) -> dict:
    probs = None
    if isinstance(answer, dict) and answer.get("type") != "refusal":
        probs = answer.get("probabilities")
    if not probs:
        return {
            "predicted_label": None,
            "predicted_category": None,
            "correct": False,
            "p": None,
            "decision_score": missing_answer_score(len(task["option_to_category"])),
            "missing": True,
            "declared_choice_differs": None,
        }
    probs = {str(k): float(v) for k, v in probs.items()}
    label = max(sorted(probs), key=lambda k: probs[k])
    category = task["option_to_category"].get(label)
    correct = category == task["correct_answer"]
    declared = answer.get("choice")
    return {
        "predicted_label": label,
        "predicted_category": category,
        "correct": correct,
        "p": probs[label],
        "decision_score": decision_score(correct, probs[label]),
        "missing": False,
        "declared_choice_differs": declared is not None and str(declared) != label,
    }
