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
# When2Call's own default prompt, copied from evaluation/mcq/lm_eval_harness/when2call/utils.py at the pinned
# commit (Apache-2.0), and the question Artificial Analysis shows on its When2Call evaluation page's example tasks
# (read 22 November 2026; present in the Wayback Machine capture of 14 November 2026).
WHEN2CALL_SYSTEM_PROMPT = (
    "You are a helpful AI assistant. \n"
    "You have access to the following tools described in <tool></tool> which you can use to answer the user's questions.\n"
    "Only use a tool if it directly answers the user's question.\n"
)
WHEN2CALL_TOOL_USE = (
    "To use a tool, return JSON in the following format:\n"
    '{"name": "tool_name", "arguments": {"argument1": "value1", "argument2": "value2", ...}}\n'
)
AA_INSTRUCTIONS = (
    "The state is a conversation between a user and an AI assistant that can use the tools listed in its system "
    "prompt. Which of these replies should the assistant give to the user's last message?"
)
# Presentations of the same task. "letters" is the B2 run and "named" the B2L run; "minimal", "numbered" and "bare"
# change one thing each against "letters"; "aa" reproduces the format on Artificial Analysis's evaluation page
# (PLAN.md section 11, item 14).
VARIANTS = {
    "letters": {"labels": LABELS, "instructions": INSTRUCTIONS, "state": "headers"},
    "named": {"labels": None, "instructions": INSTRUCTIONS, "state": "headers"},
    "minimal": {"labels": LABELS, "instructions": "Which reply should the assistant give?", "state": "headers"},
    "numbered": {"labels": ("1", "2", "3", "4"), "instructions": INSTRUCTIONS, "state": "headers"},
    "bare": {"labels": LABELS, "instructions": INSTRUCTIONS, "state": "bare"},
    "aa": {"labels": LABELS, "instructions": AA_INSTRUCTIONS, "state": "aa"},
}


def render_state(item: dict, style: str) -> str:
    tools = "\n".join(item["tools"])
    if style == "headers":
        return f"TOOLS AVAILABLE TO THE ASSISTANT:\n{tools}\n\nUSER MESSAGE:\n{item['question']}"
    if style == "bare":
        return f"{tools}\n\n{item['question']}"
    if style == "aa":
        tool_string = "\n\n".join(f"<tool>{tool}</tool>" for tool in item["tools"])  # When2Call's default_format_tools
        system = f"{WHEN2CALL_SYSTEM_PROMPT}\n{WHEN2CALL_TOOL_USE}\n\n{tool_string}"  # When2Call's process_docs_default
        return f"<system>\n{system}\n</system>\n\n<user>\n{item['question']}\n</user>"
    raise ValueError(f"unknown state style {style!r}")


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


def build_task(item: dict, seed: int = DEFAULT_SEED, named: bool = False, variant: str | None = None) -> dict:
    """One When2Call task as a choice question. Labels are A to D in a per-task shuffled order,
    or, with named=True, the category names themselves in the same shuffled order. A variant from
    VARIANTS changes the labels, the instruction or the state framing; the shuffle is the same for all."""
    spec = VARIANTS["named" if named else (variant or "letters")]
    rng = random.Random(f"{seed}:{item['uuid']}")
    categories = list(CATEGORIES)
    rng.shuffle(categories)
    labels = categories if spec["labels"] is None else spec["labels"]
    option_to_category = dict(zip(labels, categories))
    criteria = {label: item["answers"][category] for label, category in option_to_category.items()}
    correct_label = next(label for label, category in option_to_category.items() if category == item["correct_answer"])
    return {
        "uuid": item["uuid"],
        "source_id": item.get("source_id"),
        "state": render_state(item, spec["state"]),
        "question": {"type": "choice", "instructions": spec["instructions"], "criteria": criteria},
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
