import json

import runner as r
from client import CallResult

QUESTIONS = {"covered": {"type": "noul", "instructions": "x"}}
MODELS = {"a": "id/a", "b": "id/b", "c": "id/c"}


class FakeClient:
    def __init__(self, fail_states=(), p=0.7, cost=0.0):
        self.calls = []
        self.fail_states = set(fail_states)
        self.p = p
        self.cost = cost

    def decide(self, model, state, questions):
        self.calls.append((model, state))
        if state in self.fail_states:
            return CallResult(ok=False, status=502, latency_ms=5, attempts=3, error="upstream")
        return CallResult(
            ok=True,
            status=200,
            latency_ms=5,
            attempts=1,
            model_returned=model,
            provider_returned="Fake",
            input_tokens=10,
            output_tokens=0,
            cost=self.cost,
            p_yes=self.p,
            answers={"covered": {"type": "noul", "noul": self.p}},
        )


def rows(*ids):
    return [(rid, f"STATE {rid}") for rid in ids]


def test_plan_tasks_interleaves_the_models_and_rotates_their_order_per_row():
    tasks = r.plan_tasks(rows("r1", "r2", "r3"), MODELS, QUESTIONS, run="t")
    assert [(t.row_id, t.model_key) for t in tasks] == [
        ("r1", "a"), ("r1", "b"), ("r1", "c"),
        ("r2", "b"), ("r2", "c"), ("r2", "a"),
        ("r3", "c"), ("r3", "a"), ("r3", "b"),
    ]
    assert tasks[0].model_id == "id/a"
    assert tasks[0].state == "STATE r1"
    assert tasks[0].questions == QUESTIONS


def test_repeats_are_repeat_major_so_the_same_row_is_never_sent_twice_in_a_row():
    tasks = r.plan_tasks(rows("r1", "r2"), {"a": "id/a"}, QUESTIONS, run="t", repeats=3)
    assert [(t.repeat, t.row_id) for t in tasks] == [
        (0, "r1"), (0, "r2"), (1, "r1"), (1, "r2"), (2, "r1"), (2, "r2"),
    ]


def test_rows_can_carry_their_own_question_and_meta():
    own = {"q": {"type": "choice", "instructions": "x", "criteria": {"A": "a"}}}
    tasks = r.plan_tasks([("r1", "s1", own, {"tier": "hard"}), ("r2", "s2")], {"a": "id/a"}, QUESTIONS, run="t",
                         meta={"route": "openrouter"})
    assert tasks[0].questions == own
    assert tasks[0].meta == {"route": "openrouter", "tier": "hard"}
    assert tasks[1].questions == QUESTIONS
    assert tasks[1].meta == {"route": "openrouter"}


def test_run_writes_one_raw_line_per_call_with_the_required_fields(tmp_path):
    clients = {"a": FakeClient(), "b": FakeClient()}
    tasks = r.plan_tasks(
        rows("r1"), {"a": "id/a", "b": "id/b"}, QUESTIONS, run="t",
        meta={"view": "B", "wording": "main", "route": "openrouter"},
    )
    summary = r.run_tasks(tasks, clients, tmp_path / "raw.jsonl", warmup=False)
    records = [json.loads(line) for line in (tmp_path / "raw.jsonl").read_text(encoding="utf-8").splitlines()]
    assert len(records) == 2
    required = {
        "ts", "run", "row_id", "repeat", "model_key", "model_requested", "model_returned", "provider_returned",
        "route", "view", "wording", "status", "ok", "latency_ms", "attempts", "input_tokens", "output_tokens",
        "cost", "p_yes", "answers", "error", "request_sha256", "warmup",
    }
    for rec in records:
        assert required <= set(rec)
        assert rec["view"] == "B" and rec["wording"] == "main" and rec["route"] == "openrouter"
        assert rec["warmup"] is False
    assert summary.ok == 2
    assert summary.failed == 0
    assert summary.skipped == 0


def test_request_sha256_is_the_hash_of_the_request_body(tmp_path):
    tasks = r.plan_tasks(rows("r1"), {"a": "id/a"}, QUESTIONS, run="t")
    r.run_tasks(tasks, {"a": FakeClient()}, tmp_path / "raw.jsonl", warmup=False)
    rec = r.load_raw(tmp_path / "raw.jsonl")[0]
    assert rec["request_sha256"] == r.request_hash("id/a", "STATE r1", QUESTIONS)
    assert len(rec["request_sha256"]) == 64


def test_resume_skips_successful_calls_and_retries_failed_ones(tmp_path):
    tasks = r.plan_tasks(rows("r1", "r2"), {"a": "id/a"}, QUESTIONS, run="t")
    first = r.run_tasks(tasks, {"a": FakeClient(fail_states={"STATE r2"})}, tmp_path / "raw.jsonl", warmup=False)
    assert first.ok == 1
    assert first.failed == 1

    good = FakeClient()
    second = r.run_tasks(tasks, {"a": good}, tmp_path / "raw.jsonl", warmup=False)
    assert second.skipped == 1
    assert second.ok == 1
    assert [state for _, state in good.calls] == ["STATE r2"]

    records = r.load_raw(tmp_path / "raw.jsonl")
    assert len(records) == 3
    final = r.latest_ok(records)
    assert set(final) == {("t", "r1", "a", 0), ("t", "r2", "a", 0)}


def test_warmup_calls_are_logged_and_flagged(tmp_path):
    cl = FakeClient()
    tasks = r.plan_tasks(rows("r1"), {"a": "id/a"}, QUESTIONS, run="t")
    r.run_tasks(tasks, {"a": cl}, tmp_path / "raw.jsonl", warmup=True)
    records = r.load_raw(tmp_path / "raw.jsonl")
    assert [rec["warmup"] for rec in records] == [True, False]
    assert len(cl.calls) == 2
    assert ("t", "r1", "a", 0) in r.latest_ok(records)
    assert len(r.latest_ok(records)) == 1


def test_run_stops_when_the_cost_cap_is_reached(tmp_path):
    cl = FakeClient(cost=0.6)
    tasks = r.plan_tasks(rows("r1", "r2", "r3"), {"a": "id/a"}, QUESTIONS, run="t")
    summary = r.run_tasks(tasks, {"a": cl}, tmp_path / "raw.jsonl", warmup=False, max_cost=1.0)
    assert summary.ok == 2
    assert summary.stopped_for_cost is True
    assert summary.cost == 1.2


def test_summary_counts_refusals_separately(tmp_path):
    class Refuser(FakeClient):
        def decide(self, model, state, questions):
            return CallResult(ok=True, status=200, latency_ms=1, attempts=1, refused=True,
                              answers={"covered": {"type": "refusal"}})

    tasks = r.plan_tasks(rows("r1"), {"a": "id/a"}, QUESTIONS, run="t")
    summary = r.run_tasks(tasks, {"a": Refuser()}, tmp_path / "raw.jsonl", warmup=False)
    assert summary.ok == 1
    assert summary.refused == 1


def test_pacing_sleeps_between_calls(tmp_path):
    sleeps = []
    tasks = r.plan_tasks(rows("r1", "r2"), {"a": "id/a"}, QUESTIONS, run="t")
    r.run_tasks(tasks, {"a": FakeClient()}, tmp_path / "raw.jsonl", warmup=False, pace_seconds=2.6,
                sleep=sleeps.append)
    assert sleeps == [2.6, 2.6]
