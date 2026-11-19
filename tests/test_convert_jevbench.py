from collections import Counter

import pytest

import convert_jevbench as cj
from paths import JEVBENCH

needs_data = pytest.mark.skipif(not JEVBENCH.exists(), reason="JevBench data not fetched")


@needs_data
def test_loads_231_public_items_with_their_tier():
    items = cj.load_public_items()
    assert len(items) == 231
    assert Counter(i["tier"] for i in items) == {"original": 72, "easy": 48, "hard": 111}
    assert Counter(i["question"]["type"] for i in items) == {"noul": 74, "choice": 139, "score": 18}
    assert len({i["id"] for i in items}) == 231


@needs_data
def test_request_passes_state_and_question_through_unchanged():
    item = cj.load_public_items()[0]
    req = cj.request_for(item)
    assert req["state"] == item["state"]
    assert req["questions"] == {"q": item["question"]}


def test_probs_from_a_yes_no_answer_use_the_yes_and_no_labels():
    item = {"question": {"type": "noul"}, "labels": ["no", "yes"]}
    probs = cj.probs_from_answer(item, {"type": "noul", "noul": 0.8})
    assert probs == {"yes": 0.8, "no": pytest.approx(0.2)}


def test_probs_from_a_choice_answer_take_the_probabilities_map():
    item = {"question": {"type": "choice"}, "labels": ["a", "b"]}
    answer = {"type": "choice", "choice": "a", "confidence": 0.7, "probabilities": {"a": 0.7, "b": 0.3}}
    assert cj.probs_from_answer(item, answer) == {"a": 0.7, "b": 0.3}


def test_probs_from_a_score_answer_are_keyed_by_level_index_whichever_shape_arrives():
    item = {"question": {"type": "score", "criteria": ["c0", "c1", "c2"]}, "labels": ["0", "1", "2"]}
    as_list = {"type": "score", "score": 1, "confidence": 0.6, "probabilities": [0.2, 0.6, 0.2]}
    assert cj.probs_from_answer(item, as_list) == {"0": 0.2, "1": 0.6, "2": 0.2}
    as_dict = {"type": "score", "score": 1, "probabilities": {"0": 0.2, "1": 0.6, "2": 0.2}}
    assert cj.probs_from_answer(item, as_dict) == {"0": 0.2, "1": 0.6, "2": 0.2}
    as_int_keys = {"type": "score", "score": 1, "probabilities": {0: 0.2, 1: 0.6, 2: 0.2}}
    assert cj.probs_from_answer(item, as_int_keys) == {"0": 0.2, "1": 0.6, "2": 0.2}


def test_refusal_or_missing_answer_gives_none():
    item = {"question": {"type": "noul"}, "labels": ["no", "yes"]}
    assert cj.probs_from_answer(item, {"type": "refusal"}) is None
    assert cj.probs_from_answer(item, None) is None


def test_score_item_mirrors_jevbench_argmax_with_lexicographic_tie_break():
    item = {"question": {"type": "choice"}, "labels": ["a", "b"], "expected": "a"}
    out = cj.score_item(item, {"a": 0.5, "b": 0.5})
    assert out["valid"] is True
    assert out["predicted"] == "a"
    assert out["correct"] is True


def test_score_item_rejects_bad_sums_but_renormalises_rounded_ones_like_jevbench():
    item = {"question": {"type": "choice"}, "labels": ["a", "b"], "expected": "a"}
    bad = cj.score_item(item, {"a": 0.6, "b": 0.6})
    assert bad["valid"] is False
    assert bad["correct"] is False
    rounded = cj.score_item(item, {"a": 0.605, "b": 0.4})
    assert rounded["valid"] is True
    assert rounded["strict_valid"] is False
    assert rounded["renormalized"] is True
    assert rounded["correct"] is True
    assert sum(rounded["probs"].values()) == pytest.approx(1.0)
    assert cj.score_item(item, {"a": 1.0})["valid"] is False
    assert cj.score_item(item, {"a": 0.5, "b": 0.5, "c": 0.0})["valid"] is False
    assert cj.score_item(item, None)["valid"] is False


def test_score_family_compares_the_argmax_level_with_the_expected_level_as_a_string():
    item = {"question": {"type": "score"}, "labels": ["0", "1", "2", "3"], "expected": 1}
    out = cj.score_item(item, {"0": 0.1, "1": 0.6, "2": 0.2, "3": 0.1})
    assert out["correct"] is True
    assert out["predicted"] == "1"
    assert out["ordinal_ev"] == pytest.approx(1.3)


def test_brier_uses_the_jevbench_two_class_convention_for_yes_no():
    assert cj.brier({"yes": 0.8, "no": 0.2}, "yes", ["no", "yes"]) == pytest.approx(0.08)
    assert cj.brier({"a": 0.7, "b": 0.2, "c": 0.1}, "a", ["a", "b", "c"]) == pytest.approx(0.14)


def test_chance_corrected_accuracy_is_clipped_at_zero():
    assert cj.chance_corrected(0.75, chance=0.5) == pytest.approx(0.5)
    assert cj.chance_corrected(0.2, chance=0.25) == 0.0


def test_tier_chance_is_the_mean_of_one_over_the_option_count():
    items = [{"labels": ["no", "yes"]}, {"labels": ["a", "b", "c", "d"]}]
    assert cj.tier_chance(items) == pytest.approx((0.5 + 0.25) / 2)
