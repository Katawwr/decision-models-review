"""Assemble the hard tier (PLAN.md section 13): validate the family files, apply the blind
checker's verdicts, drop disagreements, and write the frozen rows, manifest and hash.

    python src/build_hard_tier.py --src <folder of family_*.jsonl> --verdicts <checker.jsonl>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manifest import build_tier_manifest, write_manifest
from paths import DATA, read_jsonl

FAMILIES = ("units", "extra_field", "swapped_target", "scope_creep", "policy_note", "false_premise")
FIELDS = {"id", "label", "user_request", "tool_results", "call", "domain", "targets_reviewer", "family",
          "twin_of", "author", "split"}
OPTIONAL_FIELDS = {"candidate_id"}
ID_RE = re.compile(r"^h([1-6])-(\d{2})$")


def validate(rows: list[dict]) -> list[str]:
    problems: list[str] = []
    for row_id, count in Counter(r.get("id") for r in rows).items():
        if count > 1:
            problems.append(f"{row_id}: duplicate id")
    by_id = {r.get("id"): r for r in rows}
    pairs: Counter = Counter()
    for r in rows:
        rid = str(r.get("id", "?"))
        missing, extra = FIELDS - set(r), set(r) - FIELDS - OPTIONAL_FIELDS
        if missing:
            problems.append(f"{rid}: missing fields {sorted(missing)}")
        if extra:
            problems.append(f"{rid}: unexpected fields {sorted(extra)}")
        match = ID_RE.match(rid)
        if not match:
            problems.append(f"{rid}: id does not match h<family>-<nn>")
            continue
        expected_label = "hijack" if int(match.group(2)) < 10 else "legitimate"
        if r.get("label") != expected_label:
            problems.append(f"{rid}: label {r.get('label')!r} does not match its id range ({expected_label})")
        family = str(r.get("family", ""))
        base = family[:-5] if family.endswith("_twin") else family
        if base not in FAMILIES:
            problems.append(f"{rid}: unknown family {family!r}")
        elif (r.get("label") == "legitimate") != family.endswith("_twin"):
            problems.append(f"{rid}: family {family!r} does not match the label")
        elif FAMILIES.index(base) + 1 != int(match.group(1)):
            problems.append(f"{rid}: family {family!r} does not match the id's family number")
        if bool(r.get("targets_reviewer")) != (r.get("label") == "hijack"):
            problems.append(f"{rid}: targets_reviewer must be true for hijacks and false for twins")
        twin = r.get("twin_of")
        if twin not in by_id:
            problems.append(f"{rid}: twin {twin!r} not found")
        elif by_id[twin].get("twin_of") != rid:
            problems.append(f"{rid}: twin link not symmetric with {twin}")
        elif by_id[twin].get("label") == r.get("label"):
            problems.append(f"{rid}: twin {twin} has the same label")
        call = r.get("call")
        if not isinstance(call, dict) or not isinstance(call.get("name"), str) or not isinstance(call.get("arguments"), dict):
            problems.append(f"{rid}: call must be an object with a name and an arguments object")
        for field in ("user_request", "tool_results"):
            if not isinstance(r.get(field), str) or not r[field].strip():
                problems.append(f"{rid}: {field} must be non-empty text")
        if r.get("split") != "hard":
            problems.append(f"{rid}: split must be 'hard'")
        pairs[(r.get("user_request"), json.dumps(call, sort_keys=True) if isinstance(call, dict) else None)] += 1
    for (request, _), count in pairs.items():
        if count > 1:
            problems.append(f"duplicate request and call pair: {str(request)[:60]!r}")
    return problems


def apply_checker(rows: list[dict], verdicts: dict[str, str]) -> tuple[list[dict], list[dict]]:
    """Keep the rows where the blind checker's yes/no agrees with the label."""
    kept, dropped = [], []
    for r in rows:
        if r["id"] not in verdicts:
            raise ValueError(f"no checker verdict for {r['id']}")
        answer = str(verdicts[r["id"]]).strip().lower()
        if (answer == "yes") == (r["label"] == "legitimate"):
            kept.append(r)
        else:
            dropped.append({"id": r["id"], "label": r["label"], "family": r["family"], "checker": answer})
    return kept, dropped


def load_families(src: Path | str) -> list[dict]:
    rows: list[dict] = []
    for path in sorted(Path(src).glob("family_*.jsonl")):
        rows += read_jsonl(path)
    return rows


def load_verdicts(path: Path | str) -> dict[str, str]:
    return {rec["id"]: rec["answer"] for rec in read_jsonl(path)}


def assemble(src: Path | str, verdicts_path: Path | str, out_dir: Path | str) -> dict:
    rows = load_families(src)
    problems = validate(rows)
    if problems:
        raise ValueError("validation failed:\n" + "\n".join(problems))
    kept, dropped = apply_checker(rows, load_verdicts(verdicts_path))
    kept.sort(key=lambda r: r["id"])
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n" for r in kept)
    (out_dir / "rows.v1.jsonl").write_bytes(text.encode("utf-8"))
    rows_sha = hashlib.sha256(text.encode("utf-8")).hexdigest()
    manifest_sha = write_manifest(build_tier_manifest({r["id"]: r for r in kept}, source=out_dir.name),
                                  out_dir / "manifest.jsonl")
    by_family = Counter((r["family"], r["label"]) for r in kept)
    report = {
        "rows_in": len(rows), "rows_kept": len(kept), "dropped": dropped,
        "rows_sha256": rows_sha, "manifest_sha256": manifest_sha,
        "by_family": {f"{family} {label}": n for (family, label), n in sorted(by_family.items())},
    }
    lines = ["# Hard tier build report", "",
             f"Rows handed to the assembly step: {len(rows)}. Kept after its blind-check verdicts: {len(kept)}. "
             f"Dropped because the checker disagreed with the label: {len(dropped)}. Counts of candidates written and "
             f"judged are in the build's selection record, not here.", "",
             f"SHA-256 of rows.v1.jsonl: `{rows_sha}`", f"SHA-256 of manifest.jsonl: `{manifest_sha}`", "",
             "| Family | Label | Kept |", "|---|---|---|"]
    lines += [f"| {family} | {label} | {n} |" for (family, label), n in sorted(by_family.items())]
    if dropped:
        lines += ["", "## Dropped rows", "", "| Row | Label | Family | Checker said |", "|---|---|---|---|"]
        lines += [f"| {d['id']} | {d['label']} | {d['family']} | {d['checker']} |" for d in dropped]
    (out_dir / "BUILD_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    return report


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--src", type=Path, required=True, help="folder holding family_*.jsonl")
    parser.add_argument("--verdicts", type=Path, required=True, help="checker verdicts, one {id, answer} per line")
    parser.add_argument("--out", type=Path, default=DATA / "hard_tier")
    args = parser.parse_args(argv)
    report = assemble(args.src, args.verdicts, args.out)
    print(json.dumps(report, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
