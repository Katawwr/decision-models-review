import math

import pytest

import desk_aa as d

PUBLISHED = {"Jev 1.14": 66.2, "Gemini Decision 1": 66.0, "Clef": 60.3, "Drex Max v1.1": 72.6}


def test_weights_sum_to_one():
    assert sum(d.WEIGHTS.values()) == pytest.approx(1.0)
    assert set(d.WEIGHTS) == set(d.ITEMS) == {"paperclip", "onet", "when2call", "omniscience", "hle", "symmetry"}


def test_index_reproduces_the_published_scores_from_the_components():
    for name, published in PUBLISHED.items():
        assert d.index(d.SCORES[name]) == pytest.approx(published, abs=0.05)


def test_reweighting_without_knowledge_and_reasoning_matches_the_brief():
    drop = ("omniscience", "hle")
    assert d.index(d.SCORES["Jev 1.14"], drop=drop) == pytest.approx(72.2, abs=0.05)
    assert d.index(d.SCORES["Gemini Decision 1"], drop=drop) == pytest.approx(69.6, abs=0.05)
    assert d.index(d.SCORES["Clef"], drop=drop) == pytest.approx(64.8, abs=0.05)


def test_index_standard_error_combines_components_by_weight():
    assert d.index_se({"x": 1.0}, {"x": 100}, per_item_sd=40) == pytest.approx(4.0)
    two = d.index_se({"x": 0.5, "y": 0.5}, {"x": 100, "y": 100}, per_item_sd=40)
    assert two == pytest.approx(math.sqrt(2 * (0.5 * 4.0) ** 2))


def test_symmetry_contributes_the_largest_share_of_index_variance():
    shares = d.variance_shares(d.WEIGHTS, d.ITEMS, per_item_sd=40)
    assert sum(shares.values()) == pytest.approx(1.0)
    assert max(shares, key=shares.get) == "symmetry"


def test_difference_half_width_is_wider_than_a_single_score():
    se = d.index_se(d.WEIGHTS, d.ITEMS, per_item_sd=40)
    assert d.half_width(se) == pytest.approx(1.96 * se)
    assert d.difference_half_width(se) == pytest.approx(1.96 * math.sqrt(2) * se)
