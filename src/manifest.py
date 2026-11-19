"""The fixed row manifest for the main test: the Fusion First rows minus the 40 pilot rows."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from paths import FUSION, MANIFEST, read_jsonl

SOURCE_FILES = {
    "guard_step5": "guard_step5/rows.v1.jsonl",
    "guard_binder": "guard_binder/rows.v1.jsonl",
    "guard_binder_attack": "guard_binder_attack/rows.v1.jsonl",
}

# Rows used in the 17 Nov 2026 pilot. They are excluded from every run.
PILOT_IDS = frozenset(
    """
    b12-013 b07-006 b09-005 b10-009 b09-017 b05-012 b11-008 b05-001 b05-017 b11-015 b04-000
    b03-007 b07-011 b09-021 b02-013 b08-016 b06-035 b06-030 b07-026 b10-030 b02-035 b09-026
    b11-033 b08-025 b07-040 b11-040 b02-039 b10-038 b04-039 b02-037 b05-040 b10-036
    x03-011 x03-010 x08-013 x05-011 x08-004 x06-003 x04-008 x08-002
    """.split()
)


def split_half(row_id: str) -> str:
    """Tune half when the SHA-1 of the id is even, report half otherwise."""
    return "tune" if int(hashlib.sha1(row_id.encode()).hexdigest(), 16) % 2 == 0 else "report"


def group_of(source: str, row: dict) -> str:
    if row["label"] == "legitimate":
        return "legitimate"
    if source == "guard_binder_attack":
        return "hijack_reviewer_informed"
    if row.get("targets_reviewer"):
        return "hijack_reviewer_naive"
    return "hijack_plain"


def load_rows(fusion_dir: Path | str = FUSION) -> dict[str, dict]:
    rows: dict[str, dict] = {}
    for source, relative in SOURCE_FILES.items():
        for row in read_jsonl(Path(fusion_dir) / relative):
            if row["id"] in rows:
                raise ValueError(f"duplicate row id {row['id']}")
            rows[row["id"]] = dict(row, source=source)
    return rows


def build_manifest(fusion_dir: Path | str = FUSION) -> list[dict]:
    entries = []
    for row in load_rows(fusion_dir).values():
        if row["id"] in PILOT_IDS:
            continue
        entries.append(
            {
                "id": row["id"],
                "source": row["source"],
                "label": row["label"],
                "group": group_of(row["source"], row),
                "half": split_half(row["id"]),
            }
        )
    return entries


def load_rows_file(path: Path | str, source: str) -> dict[str, dict]:
    """Rows of one file, keyed by id, each tagged with its source name."""
    rows: dict[str, dict] = {}
    for row in read_jsonl(path):
        if row["id"] in rows:
            raise ValueError(f"duplicate row id {row['id']}")
        rows[row["id"]] = dict(row, source=source)
    return rows


def build_tier_manifest(rows: dict[str, dict], source: str) -> list[dict]:
    """Manifest for an added tier: hijacks grouped by family, the same split rule."""
    entries = []
    for row in rows.values():
        group = "legitimate" if row["label"] == "legitimate" else f"hijack_{row.get('family', 'unknown')}"
        entries.append({
            "id": row["id"], "source": source, "label": row["label"], "group": group,
            "half": split_half(row["id"]), "family": row.get("family"), "twin_of": row.get("twin_of"),
        })
    return entries


def write_manifest(entries: list[dict], path: Path | str = MANIFEST) -> str:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n" for entry in entries)
    data = text.encode("utf-8")
    path.write_bytes(data)
    digest = hashlib.sha256(data).hexdigest()
    path.with_suffix(".sha256").write_text(f"{digest}  {path.name}\n", encoding="utf-8")
    return digest


def load_manifest(path: Path | str = MANIFEST) -> list[dict]:
    return read_jsonl(path)


def manifest_sha256(path: Path | str = MANIFEST) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


if __name__ == "__main__":
    manifest_entries = build_manifest()
    print(f"{len(manifest_entries)} rows -> {MANIFEST}")
    print(f"sha256 {write_manifest(manifest_entries)}")
