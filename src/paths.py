"""Project paths, pinned data sources, model IDs and JSONL helpers."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RUNS = ROOT / "runs"
RESULTS = ROOT / "results"

FUSION = DATA / "fusion-first" / "datasets"
JEVBENCH = DATA / "jevbench" / "datasets" / "public"
WHEN2CALL = DATA / "when2call" / "data" / "test" / "when2call_test_mcq.jsonl"
AA_FILTERED_IDS = DATA / "aa_when2call_filtered_ids.txt"
MANIFEST = DATA / "manifest.jsonl"

PINS = {
    "fusion-first": {
        "url": "https://github.com/Katawwr/Fusion-First",
        "commit": "1dc1dfdef99151c124de62cef149a230db35214b",
    },
    "jevbench": {
        "url": "https://github.com/fstandhartinger/jevbench",
        "commit": "609a664e81f46e03731600bd7bd9f1b7a61257c5",
    },
    "when2call": {
        "url": "https://github.com/NVIDIA/When2Call",
        "commit": "ecc8d42388e91ab37e7e737d48e16e8ecea3d1dc",
    },
}

MODELS = {
    "gemini": "google/gemini-decision-1",
    "jev": "typesafe/jev-1.14",
    "clef": "cloudflare/clef",
}
GEMINI_DIRECT_MODEL = "gemini-decision-1"

# OpenRouter providers to pin per model, with fallbacks off. Empty until the plan is signed off.
PROVIDER_PINS: dict[str, str] = {}


def read_jsonl(path: Path | str) -> list[dict]:
    path = Path(path)
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]


def append_jsonl(path: Path | str, record: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")
