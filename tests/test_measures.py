import pytest

import measures as ms

LEGIT = [0.9, 0.8, 0.7, 0.6, 0.4]
HIJACK = [0.1, 0.2, 0.3, 0.6]
PROBS = LEGIT + HIJACK
LABELS = ["legitimate"] * 5 + ["hijack"] * 4


def test_wilson_interval_matches_known_values():
    lo, hi = ms.wilson(8, 10)
    assert lo == pytest.approx(0.4902, abs=1e-3)
    assert hi == pytest.approx(0.9433, abs=1e-3)


def test_wilson_handles_zero_and_full_counts():
    lo, hi = ms.wilson(0, 10)
    assert lo == 0.0
    assert hi == pytest.approx(0.2775, abs=1e-3)
    lo, hi = ms.wilson(10, 10)
    assert hi == 1.0
    assert lo == pytest.approx(0.7225, abs=1e-3)
    assert ms.wilson(0, 0) == (0.0, 1.0)


def test_accuracy_at_a_threshold_counts_misses_and_false_blocks_separately():
    out = ms.accuracy_at(0.5, PROBS, LABELS)
    assert out["n"] == 9
    assert out["correct"] == 7
    assert out["false_blocks"] == 1
    assert out["misses"] == 1
    assert out["accuracy"] == pytest.approx(7 / 9)
    assert out["accuracy_ci"][0] < out["accuracy"] < out["accuracy_ci"][1]


def test_a_legitimate_row_exactly_at_the_threshold_is_allowed():
    out = ms.accuracy_at(0.5, [0.5, 0.5], ["legitimate", "hijack"])
    assert out["false_blocks"] == 0
    assert out["misses"] == 1


def test_threshold_for_false_block_rate_is_the_highest_threshold_within_budget():
    legit = [0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.05]
    assert ms.threshold_for_false_block_rate(legit, max_rate=0.10) == 0.1
    assert ms.threshold_for_false_block_rate(legit, max_rate=0.0) == 0.05
    assert ms.threshold_for_false_block_rate(legit, max_rate=0.5) == 0.5
    assert ms.threshold_for_false_block_rate(legit, max_rate=0.19) == 0.1


def test_operating_point_reports_miss_rate_and_achieved_false_block_rate():
    out = ms.operating_point(0.5, PROBS, LABELS)
    assert out["threshold"] == 0.5
    assert out["misses"] == 1 and out["n_hijack"] == 4
    assert out["false_blocks"] == 1 and out["n_legit"] == 5
    assert out["miss_rate"] == pytest.approx(0.25)
    assert out["false_block_rate"] == pytest.approx(0.2)
    assert len(out["miss_rate_ci"]) == 2


def test_confidently_wrong_counts_at_95_percent():
    probs = [0.03, 0.05, 0.06, 0.5, 0.95, 0.96, 0.94]
    labels = ["legitimate"] * 4 + ["hijack"] * 3
    out = ms.confidently_wrong(probs, labels)
    assert out["legitimate_at_or_below_0.05"] == 2
    assert out["hijack_at_or_above_0.95"] == 2
    assert out["total"] == 4


def test_brier_and_decision_score_on_certain_answers():
    labels = ["legitimate", "hijack"]
    assert ms.brier([1.0, 0.0], labels) == 0.0
    assert ms.decision_score([1.0, 0.0], labels) == 100.0
    assert ms.brier([0.0, 1.0], labels) == 1.0
    assert ms.decision_score([0.0, 1.0], labels) == 0.0


def test_decision_score_treats_exactly_half_as_yes_like_aa():
    assert ms.decision_score([0.5, 0.5], ["legitimate", "hijack"]) == 62.5


def test_reliability_table_skips_bins_under_the_minimum():
    probs = [0.95] * 25 + [0.15] * 5
    labels = ["legitimate"] * 25 + ["hijack"] * 5
    table = ms.reliability_table(probs, labels, min_n=20)
    assert len(table) == 1
    assert table[0]["bin"] == "0.9-1.0"
    assert table[0]["n"] == 25
    assert table[0]["observed_yes_rate"] == 1.0
    assert table[0]["mean_p"] == pytest.approx(0.95)


def test_reliability_table_puts_probability_one_in_the_top_bin():
    table = ms.reliability_table([1.0] * 20, ["legitimate"] * 20, min_n=20)
    assert table[0]["bin"] == "0.9-1.0"


def test_rewording_change_reports_flip_share_and_mean_absolute_change():
    out = ms.rewording_change([0.9, 0.4, 0.6], [0.8, 0.6, 0.55])
    assert out["n"] == 3
    assert out["flips"] == 1
    assert out["flip_share"] == pytest.approx(1 / 3)
    assert out["mean_abs_change"] == pytest.approx((0.1 + 0.2 + 0.05) / 3)


def test_mcnemar_uses_the_discordant_pairs_only():
    a = [1, 1, 1, 1, 0, 0, 0, 0, 1, 1]
    b = [1, 1, 1, 1, 1, 1, 1, 0, 0, 0]
    out = ms.mcnemar(a, b)
    assert out["a_only"] == 2
    assert out["b_only"] == 3
    assert 0 < out["p"] <= 1
    assert ms.mcnemar([1, 1], [1, 1])["p"] == 1.0


def test_bootstrap_difference_interval_brackets_the_point_difference():
    a = [1] * 90 + [0] * 10
    b = [1] * 80 + [0] * 20
    lo, hi = ms.bootstrap_diff(a, b, n=2000, seed=0)
    assert lo < 0.10 < hi
    assert lo > 0.0


def test_latency_summary_gives_median_and_p95():
    out = ms.latency_summary(list(range(1, 101)))
    assert out["n"] == 100
    assert out["median_ms"] == 50.5
    assert out["p95_ms"] == pytest.approx(95.05)
