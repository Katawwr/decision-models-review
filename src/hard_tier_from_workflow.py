"""Turn the hard-tier build workflow's result into renumbered family files and checker verdicts
for build_hard_tier.py.

    python src/hard_tier_from_workflow.py --result <workflow result json> --candidates <first-writer files> --out <staging folder>

Pairs are kept only when both rows survived the blind check; they are renumbered by rank
(h<n>-00.. for hijacks, h<n>-10.. for twins) and carry their candidate id. Rows from the
first writer set are copied from the original files rather than from the loader's transcription.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from paths import read_jsonl

CANDIDATE_A = re.compile(r"^h(\d)a-(\d\d)$")
TEXT_FIELDS = ("user_request", "tool_results", "call", "domain")


def final_row(candidate: dict, new_id: str, twin_id: str, originals: dict) -> dict:
    row = dict(candidate)
    match = CANDIDATE_A.match(candidate["id"])
    if match:
        original = originals.get(f"h{match.group(1)}-{match.group(2)}")
        if original:
            for field in TEXT_FIELDS:
                row[field] = original[field]
    row["id"] = new_id
    row["twin_of"] = twin_id
    row["candidate_id"] = candidate["id"]
    row["targets_reviewer"] = row["label"] == "hijack"
    return row


def stage(result: dict, candidates_dir: Path | str, out_dir: Path | str) -> dict:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    originals = {}
    for path in sorted(Path(candidates_dir).glob("family_*.jsonl")):
        for r in read_jsonl(path):
            originals[r["id"]] = r
    verdicts = result.get("verdicts", {})
    report = {"pairs": {}, "orphans": [], "rows": 0}
    selection = {"families": [], "verdicts": verdicts, "checker_drops": result.get("checker_drops"),
                 "critic_note": result.get("critic_note"), "rounds": result.get("rounds")}
    checker_lines = []
    for fam in result["families"]:
        n, key = fam["n"], fam["family"]
        twins_by_id = {t["id"]: t for t in fam["twins"]}
        used, pairs, orphans = set(), [], []
        for hijack in fam["hijacks"]:
            twin = twins_by_id.get(hijack["twin_of"])
            if twin is None or twin["id"] in used:
                orphans.append(hijack["id"])
                continue
            used.add(twin["id"])
            pairs.append((hijack, twin))
        orphans += [t["id"] for t in fam["twins"] if t["id"] not in used]
        pairs = pairs[:10]
        rows = []
        for i, (hijack, twin) in enumerate(pairs):
            hid, tid = f"h{n}-{i:02d}", f"h{n}-{10 + i:02d}"
            rows.append(final_row(hijack, hid, tid, originals))
            rows.append(final_row(twin, tid, hid, originals))
        (out_dir / f"family_{n}_{key}.jsonl").write_text(
            "".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8", newline="\n")
        for r in rows:
            answers = list(verdicts.get(r["candidate_id"], []))
            checker_lines.append({"id": r["id"], "answer": "yes" if sum(a == "yes" for a in answers) >= 2 else "no",
                                  "votes": answers})
        report["pairs"][key] = len(pairs)
        report["orphans"] += orphans
        report["rows"] += len(rows)
        selection["families"].append({
            "family": key, "n": n, "final_ids": {r["id"]: r["candidate_id"] for r in rows},
            "judged": fam.get("judged"), "dropped": fam.get("dropped"), "reserves_left": fam.get("reserves_left"),
            "orphans": orphans,
        })
    (out_dir / "checker.jsonl").write_text("".join(json.dumps(c) + "\n" for c in checker_lines), encoding="utf-8", newline="\n")
    (out_dir / "selection.json").write_text(json.dumps(selection, indent=1, ensure_ascii=False), encoding="utf-8", newline="\n")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--result", type=Path, required=True)
    parser.add_argument("--candidates", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    result = json.loads(args.result.read_text(encoding="utf-8"))
    print(json.dumps(stage(result, args.candidates, args.out), indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
