"""Run planned calls: models interleaved per row, resumable, one raw JSONL line per call."""

from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

from paths import append_jsonl, read_jsonl

STANDARD_META = ("route", "view", "wording")


@dataclass
class Task:
    run: str
    row_id: str
    repeat: int
    model_key: str
    model_id: str
    state: object
    questions: dict
    meta: dict = field(default_factory=dict)


@dataclass
class Summary:
    ok: int = 0
    failed: int = 0
    skipped: int = 0
    refused: int = 0
    cost: float = 0.0
    stopped_for_cost: bool = False


def plan_tasks(rows, models: dict[str, str], questions: dict, run: str, meta: dict | None = None,
               repeats: int = 1) -> list[Task]:
    """Rows are (row_id, state) pairs, optionally (row_id, state, questions, meta) to give a row
    its own question and metadata. Models are interleaved within each row and their order
    rotates from row to row, so no model is always called first. Repeats are repeat-major,
    so the same request is never sent twice in succession."""
    keys = list(models)
    tasks = []
    for repeat in range(repeats):
        for index, row in enumerate(rows):
            row_id, state = row[0], row[1]
            row_questions = row[2] if len(row) > 2 and row[2] is not None else questions
            row_meta = dict(meta or {})
            if len(row) > 3 and row[3]:
                row_meta.update(row[3])
            shift = index % len(keys)
            for key in keys[shift:] + keys[:shift]:
                tasks.append(Task(run, row_id, repeat, key, models[key], state, row_questions, dict(row_meta)))
    return tasks


def request_hash(model_id: str, state, questions: dict) -> str:
    body = json.dumps({"model": model_id, "state": state, "questions": questions}, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(body.encode("utf-8")).hexdigest()


def task_key(task_or_record) -> tuple:
    if isinstance(task_or_record, Task):
        return (task_or_record.run, task_or_record.row_id, task_or_record.model_key, task_or_record.repeat)
    rec = task_or_record
    return (rec["run"], rec["row_id"], rec["model_key"], rec["repeat"])


def load_raw(path: Path | str) -> list[dict]:
    return read_jsonl(path)


def latest_ok(records: list[dict]) -> dict[tuple, dict]:
    """The last successful, non-warm-up record for each (run, row, model, repeat)."""
    out: dict[tuple, dict] = {}
    for rec in records:
        if rec.get("warmup") or not rec.get("ok"):
            continue
        out[task_key(rec)] = rec
    return out


def make_record(task: Task, result, warmup: bool) -> dict:
    extra = {k: v for k, v in task.meta.items() if k not in STANDARD_META}
    record = {
        "ts": datetime.now(timezone.utc).isoformat(timespec="milliseconds"),
        "run": task.run,
        "row_id": task.row_id,
        "repeat": task.repeat,
        "model_key": task.model_key,
        "model_requested": task.model_id,
        "route": task.meta.get("route"),
        "view": task.meta.get("view"),
        "wording": task.meta.get("wording"),
        "warmup": warmup,
        "request_sha256": request_hash(task.model_id, task.state, task.questions),
    }
    record.update(result.to_record())
    if extra:
        record["meta"] = extra
    return record


def run_tasks(tasks: list[Task], clients: dict, raw_path: Path | str, warmup: bool = True,
              max_cost: float | None = None, log=None, pace_seconds: float = 0.0,
              sleep=time.sleep) -> Summary:
    raw_path = Path(raw_path)
    done = set(latest_ok(load_raw(raw_path)))
    summary = Summary()

    def note(message: str) -> None:
        if log:
            log(message)

    if warmup:
        for key in dict.fromkeys(t.model_key for t in tasks):
            first = next(t for t in tasks if t.model_key == key)
            result = clients[key].decide(first.model_id, first.state, first.questions)
            append_jsonl(raw_path, make_record(first, result, warmup=True))
            summary.cost += result.cost or 0.0
            note(f"warm-up {key}: ok={result.ok} {result.latency_ms} ms")
            if pace_seconds:
                sleep(pace_seconds)

    for number, task in enumerate(tasks, 1):
        if task_key(task) in done:
            summary.skipped += 1
            continue
        if max_cost is not None and summary.cost >= max_cost:
            summary.stopped_for_cost = True
            note(f"stopped: cost {summary.cost:.4f} reached the cap {max_cost}")
            break
        result = clients[task.model_key].decide(task.model_id, task.state, task.questions)
        append_jsonl(raw_path, make_record(task, result, warmup=False))
        if result.ok:
            summary.ok += 1
            done.add(task_key(task))
        else:
            summary.failed += 1
            note(f"failed {task.run} {task.row_id} {task.model_key}: {result.error}")
        if result.refused:
            summary.refused += 1
        summary.cost += result.cost or 0.0
        if number % 50 == 0:
            note(f"{number}/{len(tasks)} ok={summary.ok} failed={summary.failed} cost={summary.cost:.4f}")
        if pace_seconds:
            sleep(pace_seconds)
    return summary
