"""Build and run the planned calls.

    python src/run_main.py SMOKE            # 30 rows, three models, OpenRouter
    python src/run_main.py A1 --max-cost 10
    python src/run_main.py B2 --dry-run     # plumbing check, no network
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import convert_jevbench as cj
import convert_when2call as cw
import questions
import views
from client import CallResult, GeminiClient, OpenRouterClient
from manifest import build_manifest, load_rows
from paths import GEMINI_DIRECT_MODEL, MODELS, PROVIDER_PINS, RUNS
from runner import plan_tasks, run_tasks

MAIN_RUNS = {
    "SMOKE": {"view": "B", "wordings": ["main"], "rows": 30, "repeats": 1, "route": "openrouter"},
    "A1": {"view": "B", "wordings": ["main"], "rows": "all", "repeats": 1, "route": "openrouter"},
    "A2": {"view": "A", "wordings": ["main"], "rows": "all", "repeats": 1, "route": "openrouter"},
    "A3": {"view": "B", "wordings": ["paraphrase", "flipped"], "rows": "all", "repeats": 1, "route": "openrouter"},
    "A4": {"view": "B", "wordings": ["main"], "rows": 100, "repeats": 3, "route": "openrouter"},
    "C1": {"view": "B", "wordings": ["main"], "rows": 200, "repeats": 1, "route": "gemini", "pace": 2.6},
}
BENCHMARK_RUNS = ("B1", "B2")
EXTRA_RUNS = ("C2", "B2L", "B2P", "B2Q")  # PLAN.md section 11 items 7 and 14
SWEEP_VARIANTS = ("minimal", "numbered", "bare")  # B2P: three further presentations of the B2L tasks
AA_VARIANTS = ("aa",)  # B2Q: the presentation shown on Artificial Analysis's When2Call page; recorded as run B2P-aa
ALL_RUNS = tuple(MAIN_RUNS) + BENCHMARK_RUNS + EXTRA_RUNS
RUN_PACE = {"C1": 2.6, "C2": 2.6}


def select_rows(entries: list[dict], how) -> list[dict]:
    """'all', or the N rows with the smallest SHA-1 of their id, in that order."""
    if how == "all":
        return list(entries)
    ranked = sorted(entries, key=lambda e: hashlib.sha1(e["id"].encode()).hexdigest())
    return ranked[: int(how)]


def select_when2call(items: list[dict], n: int) -> list[dict]:
    """The n When2Call tasks with the smallest SHA-1 of their uuid, in that order."""
    return sorted(items, key=lambda i: hashlib.sha1(i["uuid"].encode()).hexdigest())[:n]


def _when2call_planned(items: list[dict], named: bool, route: str, wording: str, variant: str | None = None) -> list:
    planned = []
    for item in items:
        task = cw.build_task(item, named=named, variant=variant)
        meta = {
            "route": route, "view": None, "wording": wording,
            "option_to_category": task["option_to_category"], "correct_label": task["correct_label"],
            "correct_answer": task["correct_answer"], "source_id": task["source_id"],
        }
        planned.append((task["uuid"], task["state"], {"q": task["question"]}, meta))
    return planned


def build_tasks(name: str, entries: list[dict] | None = None, rows: dict | None = None, all_rows: bool = False) -> list:
    """all_rows=True runs an A run on every manifest row whatever its own row count (A4 on an added tier)."""
    if name in MAIN_RUNS:
        spec = MAIN_RUNS[name]
        entries = build_manifest() if entries is None else entries
        rows = load_rows() if rows is None else rows
        selected = select_rows(entries, "all" if all_rows else spec["rows"])
        route = spec["route"]
        models = {"gemini-direct": GEMINI_DIRECT_MODEL} if route == "gemini" else dict(MODELS)
        tasks = []
        for wording_name in spec["wordings"]:
            wording = questions.WORDINGS[wording_name]
            question = {"covered": questions.build_question(wording, spec["view"], route)}
            planned = []
            for entry in selected:
                meta = {
                    "route": route, "view": spec["view"], "wording": wording_name,
                    "label": entry["label"], "group": entry["group"], "half": entry["half"], "source": entry["source"],
                }
                planned.append((entry["id"], views.render(rows[entry["id"]], spec["view"]), question, meta))
            run = f"{name}-{wording_name}" if len(spec["wordings"]) > 1 else name
            tasks.extend(plan_tasks(planned, models, question, run=run, repeats=spec["repeats"]))
        return tasks
    if name == "B1":
        planned = []
        for item in cj.load_public_items():
            meta = {
                "route": "openrouter", "view": None, "wording": "jevbench", "tier": item["tier"],
                "expected": item["expected"], "labels": item["labels"], "question_type": item["question"]["type"],
                "family": item.get("family"), "group": item.get("group"),
            }
            planned.append((item["id"], item["state"], {"q": item["question"]}, meta))
        return plan_tasks(planned, dict(MODELS), {}, run="B1")
    if name in ("B2", "B2L", "B2P", "B2Q", "C2"):
        kept, _ = cw.apply_aa_filter(cw.load_items(), cw.load_filtered_source_ids())
        if name == "B2":
            return plan_tasks(_when2call_planned(kept, False, "openrouter", "when2call"), dict(MODELS), {}, run="B2")
        if name == "B2L":
            planned = _when2call_planned(select_when2call(kept, 200), True, "openrouter", "when2call-named")
            return plan_tasks(planned, dict(MODELS), {}, run="B2L")
        if name in ("B2P", "B2Q"):
            tasks = []
            for variant in (SWEEP_VARIANTS if name == "B2P" else AA_VARIANTS):
                planned = _when2call_planned(select_when2call(kept, 200), False, "openrouter", f"when2call-{variant}",
                                             variant=variant)
                tasks.extend(plan_tasks(planned, dict(MODELS), {}, run=f"B2P-{variant}"))
            return tasks
        planned = _when2call_planned(select_when2call(kept, 100), False, "mixed", "when2call")
        models = {"gemini": MODELS["gemini"], "gemini-direct": GEMINI_DIRECT_MODEL}
        tasks = plan_tasks(planned, models, {}, run="C2")
        for task in tasks:
            task.meta["route"] = "gemini" if task.model_key == "gemini-direct" else "openrouter"
        return tasks
    raise ValueError(f"unknown run {name!r}; expected one of {ALL_RUNS}")


class DryRunClient:
    """Deterministic answers derived from a hash of the request. No network."""

    def __init__(self, latency_ms: int = 1):
        self.latency_ms = latency_ms

    def decide(self, model: str, state, questions_: dict) -> CallResult:
        seed = hashlib.sha256(
            json.dumps({"m": model, "s": state, "q": questions_}, sort_keys=True, ensure_ascii=False).encode("utf-8")
        ).hexdigest()
        rng = random.Random(seed)
        answers = {}
        for name, question in questions_.items():
            kind = question["type"]
            if kind == "noul":
                answers[name] = {"type": "noul", "noul": round(rng.random(), 4)}
            elif kind == "choice":
                labels = list(question["criteria"])
                weights = [rng.random() for _ in labels]
                probs = {label: w / sum(weights) for label, w in zip(labels, weights)}
                answers[name] = {"type": "choice", "choice": max(probs, key=probs.get),
                                 "confidence": max(probs.values()), "probabilities": probs}
            elif kind == "score":
                weights = [rng.random() for _ in question["criteria"]]
                probs = [w / sum(weights) for w in weights]
                answers[name] = {"type": "score", "score": probs.index(max(probs)), "confidence": max(probs),
                                 "probabilities": probs, "legend": list(question["criteria"])}
        tokens = len(json.dumps(state, ensure_ascii=False)) // 4 + 150
        single = next(iter(answers.values())) if len(answers) == 1 else None
        p_yes = single["noul"] if single and single["type"] == "noul" else None
        return CallResult(ok=True, status=200, latency_ms=self.latency_ms, attempts=1, model_returned=model,
                          provider_returned="dry-run", input_tokens=tokens, output_tokens=0,
                          cost=round(tokens / 1e6 * 0.1, 9), p_yes=p_yes, answers=answers)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("run", choices=ALL_RUNS)
    parser.add_argument("--dry-run", action="store_true", help="deterministic fake answers, no network")
    parser.add_argument("--max-cost", type=float, default=10.0, help="stop when usage.cost reaches this (USD)")
    parser.add_argument("--limit", type=int, default=None, help="only the first N planned calls")
    parser.add_argument("--out", type=Path, default=None, help="raw JSONL path")
    parser.add_argument("--no-warmup", action="store_true")
    parser.add_argument("--pace", type=float, default=None, help="seconds to wait between calls")
    parser.add_argument("--tier-dir", type=Path, default=None,
                        help="an added tier: a folder holding rows.v1.jsonl and manifest.jsonl; runs go to runs/<folder name>/")
    parser.add_argument("--all-rows", action="store_true",
                        help="run on every manifest row whatever the run's own row count, for A4 on an added tier")
    args = parser.parse_args(argv)

    if args.tier_dir:
        from manifest import load_manifest, load_rows_file
        tier_rows = load_rows_file(args.tier_dir / "rows.v1.jsonl", source=args.tier_dir.name)
        tasks = build_tasks(args.run, load_manifest(args.tier_dir / "manifest.jsonl"), tier_rows, all_rows=args.all_rows)
        default_out = RUNS / args.tier_dir.name / ("dryrun" if args.dry_run else "raw") / f"{args.run}.jsonl"
    else:
        tasks = build_tasks(args.run, all_rows=args.all_rows)
        default_out = RUNS / ("dryrun" if args.dry_run else "raw") / f"{args.run}.jsonl"
    if args.limit:
        tasks = tasks[: args.limit]
    out = args.out or default_out
    keys = set(t.model_key for t in tasks)
    if args.dry_run:
        clients = {key: DryRunClient() for key in keys}
    else:
        clients = {}
        if "gemini-direct" in keys:
            clients["gemini-direct"] = GeminiClient()
        if keys - {"gemini-direct"}:
            shared = OpenRouterClient(providers=PROVIDER_PINS)
            for key in keys - {"gemini-direct"}:
                clients[key] = shared
    pace = args.pace if args.pace is not None else RUN_PACE.get(args.run, MAIN_RUNS.get(args.run, {}).get("pace", 0.0))
    started = time.time()
    summary = run_tasks(tasks, clients, out, warmup=not args.no_warmup, max_cost=args.max_cost,
                        log=print, pace_seconds=pace)
    print(f"{args.run}: {len(tasks)} planned, {summary.ok} ok, {summary.failed} failed, {summary.skipped} skipped, "
          f"{summary.refused} refused, cost ${summary.cost:.4f}, {time.time() - started:.0f} s -> {out}")
    if summary.stopped_for_cost:
        print("STOPPED: the cost cap was reached")
        return 2
    return 1 if summary.failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
