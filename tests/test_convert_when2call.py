from collections import Counter

import pytest

import convert_when2call as cw
from paths import WHEN2CALL

needs_data = pytest.mark.skipif(not WHEN2CALL.exists(), reason="When2Call data not fetched")

ANSWERS = {"tool_call": "TC", "request_for_info": "RFI", "cannot_answer": "CA", "direct": "D"}


def item(uuid="u1", correct="tool_call"):
    return {
        "uuid": uuid,
        "question": "update my latte",
        "tools": ['{"name": "ChaDri.change_drink", "description": "Modifies a drink"}'],
        "answers": dict(ANSWERS),
        "correct_answer": correct,
    }


def test_filtered_ids_file_has_229_unique_source_ids():
    ids = cw.load_filtered_source_ids()
    assert len(ids) == 229
    assert "live_multiple_0-0-0" in ids
    assert "live_simple_257-137-1" in ids


@needs_data
def test_aa_filter_removes_exactly_the_229_request_for_info_variants():
    items = cw.load_items()
    kept, removed = cw.apply_aa_filter(items, cw.load_filtered_source_ids())
    assert len(items) == 3652
    assert len(kept) == 3423
    assert len(removed) == 229
    assert all(i["correct_answer"] == "request_for_info" for i in removed)
    assert Counter(i["correct_answer"] for i in kept) == {
        "tool_call": 1295, "cannot_answer": 1295, "request_for_info": 833,
    }


def test_task_is_a_choice_over_four_neutral_labels_with_the_reply_texts_as_criteria():
    task = cw.build_task(item(), seed=20261119)
    assert task["question"]["type"] == "choice"
    assert set(task["question"]["criteria"]) == {"A", "B", "C", "D"}
    assert set(task["question"]["criteria"].values()) == set(ANSWERS.values())
    assert task["option_to_category"][task["correct_label"]] == "tool_call"
    assert task["correct_answer"] == "tool_call"
    assert "update my latte" in task["state"]
    assert "ChaDri.change_drink" in task["state"]
    assert task["uuid"] == "u1"


def test_shuffle_is_deterministic_for_a_seed_and_differs_between_seeds():
    assert cw.build_task(item(), seed=20261119) == cw.build_task(item(), seed=20261119)
    orders_a = [cw.build_task(item(uuid=f"u{i}"), seed=20261119)["option_to_category"] for i in range(30)]
    orders_b = [cw.build_task(item(uuid=f"u{i}"), seed=1)["option_to_category"] for i in range(30)]
    assert orders_a != orders_b


def test_shuffle_is_not_the_same_order_for_every_item():
    orders = {
        tuple(cw.build_task(item(uuid=f"u{i}"), seed=20261119)["option_to_category"][k] for k in "ABCD")
        for i in range(50)
    }
    assert len(orders) > 1


def test_aa_decision_score_formula():
    assert cw.decision_score(correct=True, p=1.0) == 100
    assert cw.decision_score(correct=False, p=1.0) == 0
    assert cw.decision_score(correct=True, p=0.5) == 87.5
    assert cw.decision_score(correct=False, p=0.5) == 37.5
    assert cw.missing_answer_score(n_options=4) == 53.125


def test_score_task_picks_the_argmax_and_maps_it_back_to_a_category():
    task = {
        "option_to_category": {"A": "direct", "B": "tool_call", "C": "cannot_answer", "D": "request_for_info"},
        "correct_label": "B",
        "correct_answer": "tool_call",
    }
    answer = {"type": "choice", "choice": "B", "confidence": 0.9, "probabilities": {"A": 0.05, "B": 0.9, "C": 0.03, "D": 0.02}}
    out = cw.score_task(task, answer)
    assert out["predicted_category"] == "tool_call"
    assert out["correct"] is True
    assert out["p"] == 0.9
    assert out["decision_score"] == pytest.approx(50 * (1 + 1 - 0.01))
    missing = cw.score_task(task, None)
    assert missing["correct"] is False
    assert missing["decision_score"] == 53.125
    assert missing["predicted_category"] is None


def test_score_task_uses_the_probabilities_not_the_declared_choice_when_they_disagree():
    task = {
        "option_to_category": {"A": "direct", "B": "tool_call", "C": "cannot_answer", "D": "request_for_info"},
        "correct_label": "B",
        "correct_answer": "tool_call",
    }
    answer = {"type": "choice", "choice": "A", "probabilities": {"A": 0.2, "B": 0.7, "C": 0.05, "D": 0.05}}
    out = cw.score_task(task, answer)
    assert out["predicted_category"] == "tool_call"
    assert out["declared_choice_differs"] is True


def test_presentation_variants_change_one_thing_each_and_keep_the_shuffle():
    base = cw.build_task(item(), seed=20261119)
    minimal = cw.build_task(item(), seed=20261119, variant="minimal")
    numbered = cw.build_task(item(), seed=20261119, variant="numbered")
    bare = cw.build_task(item(), seed=20261119, variant="bare")
    assert cw.build_task(item(), seed=20261119, variant="letters") == base
    assert minimal["state"] == base["state"] and minimal["option_to_category"] == base["option_to_category"]
    assert minimal["question"]["instructions"] != base["question"]["instructions"]
    assert list(numbered["option_to_category"]) == ["1", "2", "3", "4"]
    assert list(numbered["option_to_category"].values()) == list(base["option_to_category"].values())
    assert numbered["correct_answer"] == base["correct_answer"]
    assert bare["option_to_category"] == base["option_to_category"]
    assert "TOOLS AVAILABLE" not in bare["state"] and "USER MESSAGE" not in bare["state"]
    assert item()["question"] in bare["state"]


def test_aa_variant_reproduces_the_format_on_artificial_analysis_when2call_page():
    base = cw.build_task(item(), seed=20261119)
    aa = cw.build_task(item(), seed=20261119, variant="aa")
    assert aa["option_to_category"] == base["option_to_category"] and aa["correct_label"] == base["correct_label"]
    assert aa["question"]["instructions"].endswith("Which of these replies should the assistant give to the user's last message?")
    assert aa["state"].startswith("<system>\nYou are a helpful AI assistant. \n")
    assert "Only use a tool if it directly answers the user's question." in aa["state"]
    assert "To use a tool, return JSON in the following format:" in aa["state"]
    assert "<tool>" in aa["state"] and "</tool>" in aa["state"]
    assert aa["state"].endswith(f"</system>\n\n<user>\n{item()['question']}\n</user>")
