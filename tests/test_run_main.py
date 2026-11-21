import hashlib

import pytest

import convert_jevbench as cj
import questions
import run_main as rm
import views
from manifest import build_manifest, load_rows
from paths import FUSION, JEVBENCH, WHEN2CALL

needs_data = pytest.mark.skipif(not (FUSION.exists() and JEVBENCH.exists() and WHEN2CALL.exists()),
                                reason="source data not fetched")


@pytest.fixture(scope="module")
def entries():
    return build_manifest()


@pytest.fixture(scope="module")
def rows():
    return load_rows()


def test_select_rows_takes_the_smallest_sha1_ids_in_order():
    sample = [{"id": i} for i in ["b01-000", "s02-010", "x03-011", "b07-006", "s01-000"]]
    chosen = rm.select_rows(sample, 3)
    digests = [hashlib.sha1(e["id"].encode()).hexdigest() for e in chosen]
    assert digests == sorted(digests)
    assert len(chosen) == 3
    assert rm.select_rows(sample, "all") == sample


@needs_data
def test_a1_covers_every_manifest_row_once_per_model_in_view_b(entries, rows):
    tasks = rm.build_tasks("A1", entries, rows)
    assert len(tasks) == 1020 * 3
    assert {t.run for t in tasks} == {"A1"}
    first = tasks[0]
    row = rows[first.row_id]
    assert first.state == views.render(row, "B")
    assert first.questions == {"covered": questions.build_question(questions.WORDINGS["main"], "B", "openrouter")}
    assert first.meta["route"] == "openrouter"
    assert first.meta["view"] == "B"
    assert first.meta["wording"] == "main"
    assert first.meta["label"] == row["label"]
    assert first.meta["group"] in {"legitimate", "hijack_plain", "hijack_reviewer_naive", "hijack_reviewer_informed"}
    assert first.meta["half"] in {"tune", "report"}
    assert {t.model_id for t in tasks} == {"google/gemini-decision-1", "typesafe/jev-1.14", "cloudflare/clef"}


@needs_data
def test_a2_uses_view_a_and_the_shorter_instructions(entries, rows):
    tasks = rm.build_tasks("A2", entries, rows)
    assert len(tasks) == 1020 * 3
    assert "TOOL RESULTS" not in tasks[0].state
    assert tasks[0].questions["covered"]["instructions"] == questions.instructions_for_view(questions.WORDINGS["main"], "A")
    assert tasks[0].meta["view"] == "A"


@needs_data
def test_a3_runs_the_two_rewordings_as_separate_runs(entries, rows):
    tasks = rm.build_tasks("A3", entries, rows)
    assert len(tasks) == 1020 * 3 * 2
    assert {t.run for t in tasks} == {"A3-paraphrase", "A3-flipped"}
    flipped = next(t for t in tasks if t.run == "A3-flipped")
    assert flipped.questions["covered"]["instructions"].startswith("Should this tool call be blocked")
    assert flipped.meta["wording"] == "flipped"


@needs_data
def test_a4_is_100_fixed_rows_three_times(entries, rows):
    tasks = rm.build_tasks("A4", entries, rows)
    assert len(tasks) == 100 * 3 * 3
    assert {t.repeat for t in tasks} == {0, 1, 2}
    assert {t.row_id for t in tasks} == {e["id"] for e in rm.select_rows(entries, 100)}


@needs_data
def test_c1_is_200_rows_through_gemini_direct_without_criteria(entries, rows):
    tasks = rm.build_tasks("C1", entries, rows)
    assert len(tasks) == 200
    assert {t.model_id for t in tasks} == {"gemini-decision-1"}
    assert {t.model_key for t in tasks} == {"gemini-direct"}
    assert "criteria" not in tasks[0].questions["covered"]
    assert tasks[0].meta["route"] == "gemini"
    assert {t.row_id for t in tasks} == {e["id"] for e in rm.select_rows(entries, 200)}


@needs_data
def test_smoke_is_30_rows_with_both_labels(entries, rows):
    tasks = rm.build_tasks("SMOKE", entries, rows)
    assert len(tasks) == 30 * 3
    assert {t.meta["label"] for t in tasks} == {"legitimate", "hijack"}


@needs_data
def test_b1_sends_each_jevbench_item_unchanged_to_every_model():
    tasks = rm.build_tasks("B1")
    items = {i["id"]: i for i in cj.load_public_items()}
    assert len(tasks) == 231 * 3
    first = tasks[0]
    item = items[first.row_id]
    assert first.state == item["state"]
    assert first.questions == {"q": item["question"]}
    assert first.meta["tier"] == item["tier"]
    assert first.meta["expected"] == item["expected"]
    assert first.meta["labels"] == item["labels"]
    assert first.meta["question_type"] == item["question"]["type"]


@needs_data
def test_b2_sends_the_filtered_when2call_tasks_with_their_answer_key():
    tasks = rm.build_tasks("B2")
    assert len(tasks) == 3423 * 3
    first = tasks[0]
    assert first.questions["q"]["type"] == "choice"
    assert set(first.questions["q"]["criteria"]) == {"A", "B", "C", "D"}
    assert set(first.meta["option_to_category"].values()) == {"tool_call", "request_for_info", "cannot_answer", "direct"}
    assert first.meta["correct_label"] in "ABCD"
    assert first.meta["correct_answer"] in {"tool_call", "request_for_info", "cannot_answer", "direct"}


def test_unknown_run_is_rejected():
    with pytest.raises(ValueError):
        rm.build_tasks("Z9", [], {})


def test_dry_run_client_is_deterministic_and_never_calls_the_network():
    client = rm.DryRunClient()
    a = client.decide("m", "STATE 1", {"covered": {"type": "noul", "instructions": "x"}})
    b = client.decide("m", "STATE 1", {"covered": {"type": "noul", "instructions": "x"}})
    assert a.ok and a.p_yes == b.p_yes
    assert 0.0 <= a.p_yes <= 1.0
    choice = client.decide("m", "STATE 2", {"q": {"type": "choice", "instructions": "x", "criteria": {"A": "a", "B": "b"}}})
    assert set(choice.answers["q"]["probabilities"]) == {"A", "B"}
    assert abs(sum(choice.answers["q"]["probabilities"].values()) - 1.0) < 1e-9


@needs_data
def test_c2_sends_one_identical_choice_question_through_both_routes():
    tasks = rm.build_tasks("C2")
    assert len(tasks) == 100 * 2
    assert {t.model_key for t in tasks} == {"gemini", "gemini-direct"}
    by_row = {}
    for t in tasks:
        by_row.setdefault(t.row_id, {})[t.model_key] = t
    first = next(iter(by_row.values()))
    assert first["gemini"].questions == first["gemini-direct"].questions
    assert first["gemini"].state == first["gemini-direct"].state
    assert first["gemini"].questions["q"]["type"] == "choice"
    assert "criteria" in first["gemini"].questions["q"]
    assert first["gemini"].meta["route"] == "openrouter" and first["gemini-direct"].meta["route"] == "gemini"
    assert rm.MAIN_RUNS.get("C2") is None and "C2" in rm.ALL_RUNS


@needs_data
def test_b2l_uses_category_names_as_labels_on_200_tasks():
    tasks = rm.build_tasks("B2L")
    assert len(tasks) == 200 * 3
    q = tasks[0].questions["q"]
    assert set(q["criteria"]) == {"tool_call", "request_for_info", "cannot_answer", "direct"}
    assert tasks[0].meta["option_to_category"] == {c: c for c in q["criteria"]}
    assert tasks[0].meta["correct_label"] == tasks[0].meta["correct_answer"]
    b2_ids = {t.row_id for t in rm.build_tasks("B2")}
    assert {t.row_id for t in tasks} <= b2_ids


@needs_data
def test_all_rows_overrides_a_runs_row_count(entries, rows):
    tasks = rm.build_tasks("A4", entries, rows, all_rows=True)
    assert len(tasks) == len(entries) * 3 * 3
    assert {t.row_id for t in tasks} == {e["id"] for e in entries}
    assert {t.repeat for t in tasks} == {0, 1, 2}
