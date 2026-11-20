from pathlib import Path

import pandas as pd
import pytest

import charts


def tables():
    return {
        "accuracy": pd.DataFrame([
            {"model_key": "gemini", "n": 1020, "accuracy": 0.97, "accuracy_lo": 0.96, "accuracy_hi": 0.98, "misses": 18, "n_hijack": 441,
             "miss_rate": 0.04, "miss_lo": 0.025, "miss_hi": 0.06, "false_blocks": 12, "n_legit": 579, "false_block_rate": 0.02, "false_block_lo": 0.01, "false_block_hi": 0.035},
            {"model_key": "jev", "n": 1020, "accuracy": 0.95, "accuracy_lo": 0.94, "accuracy_hi": 0.96, "misses": 31, "n_hijack": 441,
             "miss_rate": 0.07, "miss_lo": 0.05, "miss_hi": 0.09, "false_blocks": 17, "n_legit": 579, "false_block_rate": 0.03, "false_block_lo": 0.02, "false_block_hi": 0.045},
            {"model_key": "clef", "n": 1020, "accuracy": 0.93, "accuracy_lo": 0.92, "accuracy_hi": 0.945, "misses": 44, "n_hijack": 441,
             "miss_rate": 0.10, "miss_lo": 0.08, "miss_hi": 0.13, "false_blocks": 23, "n_legit": 579, "false_block_rate": 0.04, "false_block_lo": 0.03, "false_block_hi": 0.06},
        ]),
        "operating_points": pd.DataFrame([
            {"model_key": m, "max_false_block_rate": b, "threshold": 0.5, "miss_rate": r, "miss_lo": r - 0.02, "miss_hi": r + 0.03,
             "misses": round(r * 221), "false_block_rate": b, "n_hijack_report": 221, "n_legit_report": 285}
            for m, pairs in {"gemini": [(0.01, 0.12), (0.05, 0.05)], "jev": [(0.01, 0.20), (0.05, 0.08)], "clef": [(0.01, 0.30), (0.05, 0.12)]}.items()
            for b, r in pairs
        ]),
        "fooling": pd.DataFrame([
            {"model_key": m, "group": g, "view": v, "n": 40, "miss_rate": r, "wrong_rate": r, "wrong_lo": max(0, r - 0.05), "wrong_hi": min(1, r + 0.05)}
            for m in ("gemini", "jev", "clef")
            for g, v, r in [("hijack_plain", "B", 0.02), ("hijack_reviewer_naive", "B", 0.10), ("hijack_reviewer_informed", "B", 0.25),
                            ("hijack_plain", "A", 0.03), ("hijack_reviewer_naive", "A", 0.05), ("hijack_reviewer_informed", "A", 0.15)]
        ]),
        "rewording": pd.DataFrame([
            {"model_key": m, "pair": p, "n": 1020, "flips": f, "flip_share": f / 1020, "flip_lo": f / 1020 - 0.005, "flip_hi": f / 1020 + 0.008, "mean_abs_change": c}
            for m in ("gemini", "jev", "clef")
            for p, f, c in [("main_vs_paraphrase", 12, 0.03), ("main_vs_flipped", 30, 0.06), ("paraphrase_vs_flipped", 28, 0.05), ("any_pair", 40, None)]
        ]),
        "speed": pd.DataFrame([
            {"model_key": m, "run": "pooled", "n": 12240, "median_ms": med, "p95_ms": p95, "mean_ms": med + 20}
            for m, med, p95 in [("gemini", 335, 520), ("jev", 199, 224), ("clef", 341, 713)]
        ]),
        "cost": pd.DataFrame([
            {"model_key": m, "n_calls": 12240, "usd_per_1000_decisions": c, "mean_input_tokens": 400, "usd_per_1000_at_openrouter_list": c}
            for m, c in [("gemini", 0.040), ("jev", 0.024), ("clef", 0.097)]
        ]),
    }


def test_every_planned_chart_is_written_at_double_resolution(tmp_path):
    written = charts.render_all(tables(), tmp_path)
    assert set(written) >= {"errors_at_half", "operating_points", "fooling", "rewording", "speed_cost"}
    for name, path in written.items():
        assert Path(path).exists() and Path(path).stat().st_size > 10_000, name
        assert Path(path).suffix == ".png"
    with (tmp_path / "errors_at_half.png").open("rb") as handle:
        header = handle.read(24)
    width = int.from_bytes(header[16:20], "big")
    assert width >= 1600


def test_titles_carry_the_takeaway_computed_from_the_data():
    titles = charts.titles(tables())
    assert "Gemini" in titles["errors_at_half"] and "%" in titles["errors_at_half"]
    assert "5%" in titles["operating_points"]
    assert "Jev" in titles["speed_cost"]


def test_models_keep_fixed_colours_whatever_the_order():
    assert charts.MODEL_COLOURS["gemini"] != charts.MODEL_COLOURS["jev"] != charts.MODEL_COLOURS["clef"]
    assert list(charts.MODEL_ORDER) == ["gemini", "jev", "clef"]
    assert charts.MODEL_NAMES["gemini"] == "Gemini Decision 1"


def tier_tables():
    """A tier like the hard one: six attack families, no reviewer-aimed groups, two models tied at zero."""
    t = tables()
    t["accuracy"] = pd.DataFrame([
        {"model_key": "gemini", "n": 116, "accuracy": 0.922, "accuracy_lo": 0.86, "accuracy_hi": 0.96, "misses": 8, "n_hijack": 58,
         "miss_rate": 8 / 58, "miss_lo": 0.07, "miss_hi": 0.25, "false_blocks": 1, "n_legit": 58, "false_block_rate": 1 / 58, "false_block_lo": 0.003, "false_block_hi": 0.09},
        {"model_key": "jev", "n": 116, "accuracy": 0.784, "accuracy_lo": 0.70, "accuracy_hi": 0.85, "misses": 25, "n_hijack": 58,
         "miss_rate": 25 / 58, "miss_lo": 0.31, "miss_hi": 0.56, "false_blocks": 0, "n_legit": 58, "false_block_rate": 0.0, "false_block_lo": 0.0, "false_block_hi": 0.06},
        {"model_key": "clef", "n": 116, "accuracy": 0.888, "accuracy_lo": 0.82, "accuracy_hi": 0.93, "misses": 12, "n_hijack": 58,
         "miss_rate": 12 / 58, "miss_lo": 0.12, "miss_hi": 0.33, "false_blocks": 1, "n_legit": 58, "false_block_rate": 1 / 58, "false_block_lo": 0.003, "false_block_hi": 0.09},
    ])
    t["operating_points"] = pd.DataFrame([
        {"model_key": m, "max_false_block_rate": b, "threshold": 0.5, "miss_rate": r, "miss_lo": max(0.0, r - 0.05), "miss_hi": r + 0.15,
         "misses": round(r * 32), "false_block_rate": b, "n_hijack_report": 32, "n_legit_report": 34}
        for m, pairs in {"gemini": [(0.01, 5 / 32), (0.05, 0.0)], "jev": [(0.01, 2 / 32), (0.05, 2 / 32)], "clef": [(0.01, 8 / 32), (0.05, 0.0)]}.items()
        for b, r in pairs
    ])
    rates = {
        "gemini": {"hijack_units": (0.5, 0.125), "hijack_extra_field": (0.0, 0.1), "hijack_swapped_target": (0.3, 0.2),
                   "hijack_scope_creep": (0.0, 0.0), "hijack_policy_note": (0.0, 0.0), "hijack_false_premise": (0.1, 0.7)},
        "jev": {"hijack_units": (1.0, 0.625), "hijack_extra_field": (0.5, 0.5), "hijack_swapped_target": (0.6, 0.4),
                "hijack_scope_creep": (0.0, 0.0), "hijack_policy_note": (0.0, 0.1), "hijack_false_premise": (0.6, 0.9)},
        "clef": {"hijack_units": (0.875, 0.875), "hijack_extra_field": (0.2, 0.7), "hijack_swapped_target": (0.2, 0.4),
                 "hijack_scope_creep": (0.0, 0.0), "hijack_policy_note": (0.0, 0.1), "hijack_false_premise": (0.1, 1.0)},
    }
    rows = []
    for m, groups in rates.items():
        for g, (b, a) in groups.items():
            for view, r in (("B", b), ("A", a)):
                rows.append({"model_key": m, "group": g, "view": view, "n": 10, "miss_rate": r, "wrong_rate": r,
                             "wrong_lo": max(0.0, r - 0.2), "wrong_hi": min(1.0, r + 0.2)})
        for view in ("B", "A"):
            rows.append({"model_key": m, "group": "legitimate", "view": view, "n": 58, "miss_rate": float("nan"), "wrong_rate": 0.017,
                         "wrong_lo": 0.003, "wrong_hi": 0.09})
    t["fooling"] = pd.DataFrame(rows)
    t["rewording"] = pd.DataFrame([
        {"model_key": m, "pair": p, "n": 116, "flips": f, "flip_share": f / 116, "flip_lo": max(0.0, f / 116 - 0.03), "flip_hi": f / 116 + 0.05, "mean_abs_change": c}
        for m, flips in {"gemini": (4, 4, 4, 6), "jev": (6, 5, 3, 7), "clef": (2, 5, 5, 6)}.items()
        for p, f, c in zip(("main_vs_paraphrase", "main_vs_flipped", "paraphrase_vs_flipped", "any_pair"), flips, (0.035, 0.04, 0.04, None))
    ])
    return t


def test_tier_fooling_title_names_the_hardest_family_and_the_best_model_on_it():
    title = charts.titles(tier_tables())["fooling"]
    assert "units trick" in title.lower()
    assert "Jev 1.14" in title and "100%" in title
    assert "Gemini Decision 1" in title and "50%" in title


def test_operating_point_title_names_every_model_at_zero_when_only_some_reach_it():
    title = charts.titles(tier_tables())["operating_points"]
    assert "Gemini Decision 1 and Clef" in title
    assert "Jev 1.14" in title and "6.2%" in title
    assert "0%" not in title


def test_rewording_title_names_both_models_sharing_the_lowest_flip_share():
    title = charts.titles(tier_tables())["rewording"]
    assert "Jev 1.14 changes 6.0%" in title
    assert "Gemini Decision 1 and Clef change 5.2%" in title


def test_tier_charts_render_without_the_desk_chart(tmp_path):
    import json

    written = charts.render_all(tier_tables(), tmp_path, desk=False)
    assert "aa_reweighting" not in written
    assert not (tmp_path / "aa_reweighting.png").exists()
    manifest = json.loads((tmp_path / "charts.json").read_text(encoding="utf-8"))
    assert set(manifest) == set(written) == {"errors_at_half", "operating_points", "fooling", "rewording", "speed_cost"}


def test_fooling_chart_grows_with_the_number_of_groups(tmp_path):
    charts.render_all(tables(), tmp_path / "main", desk=False)
    charts.render_all(tier_tables(), tmp_path / "tier", desk=False)

    def height(path):
        with path.open("rb") as handle:
            return int.from_bytes(handle.read(24)[20:24], "big")

    assert height(tmp_path / "tier" / "fooling.png") > height(tmp_path / "main" / "fooling.png")
