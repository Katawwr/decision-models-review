import hashlib
from collections import Counter

import pytest

import manifest as m
from paths import FUSION

needs_data = pytest.mark.skipif(not FUSION.exists(), reason="Fusion First data not fetched")


def test_split_half_follows_sha1_parity_of_the_row_id():
    for rid in ["b01-037", "s01-000", "x03-011", "b12-013"]:
        parity = int(hashlib.sha1(rid.encode()).hexdigest(), 16) % 2
        assert m.split_half(rid) == ("tune" if parity == 0 else "report")


def test_pilot_ids_are_the_forty_from_the_brief():
    assert len(m.PILOT_IDS) == 40
    assert "b12-013" in m.PILOT_IDS
    assert "x08-002" in m.PILOT_IDS


def test_group_of_distinguishes_the_four_groups():
    assert m.group_of("guard_step5", {"label": "legitimate"}) == "legitimate"
    assert m.group_of("guard_step5", {"label": "hijack"}) == "hijack_plain"
    assert m.group_of("guard_binder", {"label": "legitimate", "targets_reviewer": False}) == "legitimate"
    assert m.group_of("guard_binder", {"label": "hijack", "targets_reviewer": False}) == "hijack_plain"
    assert m.group_of("guard_binder", {"label": "hijack", "targets_reviewer": True}) == "hijack_reviewer_naive"
    assert m.group_of("guard_binder_attack", {"label": "hijack", "targets_reviewer": True}) == "hijack_reviewer_informed"


@needs_data
def test_load_rows_returns_every_source_row_with_its_source_name():
    rows = m.load_rows()
    assert len(rows) == 1060
    assert rows["b01-037"]["source"] == "guard_binder"
    assert rows["x03-011"]["source"] == "guard_binder_attack"


@needs_data
def test_manifest_has_1020_rows_with_the_expected_composition():
    entries = m.build_manifest()
    assert len(entries) == 1020
    assert len({e["id"] for e in entries}) == 1020
    assert not ({e["id"] for e in entries} & m.PILOT_IDS)
    assert Counter(e["label"] for e in entries) == {"legitimate": 579, "hijack": 441}
    groups = Counter(e["group"] for e in entries)
    assert groups == {
        "legitimate": 579,
        "hijack_plain": 281,
        "hijack_reviewer_naive": 40,
        "hijack_reviewer_informed": 120,
    }
    assert set(entries[0]) == {"id", "source", "label", "group", "half"}


@needs_data
def test_tune_half_has_518_rows_of_which_294_legitimate():
    entries = m.build_manifest()
    tune = [e for e in entries if e["half"] == "tune"]
    assert len(tune) == 518
    assert sum(e["label"] == "legitimate" for e in tune) == 294


@needs_data
def test_write_manifest_is_deterministic_and_records_its_sha256(tmp_path):
    entries = m.build_manifest()
    digest_a = m.write_manifest(entries, tmp_path / "a.jsonl")
    digest_b = m.write_manifest(entries, tmp_path / "b.jsonl")
    assert digest_a == digest_b
    assert digest_a == hashlib.sha256((tmp_path / "a.jsonl").read_bytes()).hexdigest()
    assert (tmp_path / "a.sha256").read_text(encoding="utf-8").split()[0] == digest_a
    assert m.load_manifest(tmp_path / "a.jsonl") == entries
