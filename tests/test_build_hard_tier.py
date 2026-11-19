import json

import pytest

import build_hard_tier as bt


def row(i, label, family, twin, **extra):
    base = {
        "id": i, "label": label, "user_request": f"request {i}", "tool_results": f"results {i}",
        "call": {"name": "do_thing", "arguments": {"x": i}}, "domain": "refunds",
        "targets_reviewer": label == "hijack", "family": family, "twin_of": twin, "author": "g1", "split": "hard",
    }
    base.update(extra)
    return base


GOOD = [row("h1-00", "hijack", "units", "h1-10"), row("h1-10", "legitimate", "units_twin", "h1-00")]


def test_validate_accepts_a_well_formed_pair():
    assert bt.validate(GOOD) == []


def test_validate_reports_id_label_twin_and_flag_mismatches():
    bad = [
        row("h1-00", "legitimate", "units", "h1-10"),
        row("h1-10", "legitimate", "units_twin", "h1-00", targets_reviewer=True),
        row("h1-01", "hijack", "units", "h1-99"),
    ]
    problems = bt.validate(bad)
    text = " ".join(problems)
    assert "h1-00" in text and "label" in text
    assert "targets_reviewer" in text
    assert "twin" in text


def test_validate_rejects_duplicate_ids_and_bad_families():
    dup = [row("h1-00", "hijack", "units", "h1-10"), row("h1-00", "hijack", "units", "h1-10")]
    assert any("duplicate" in p for p in bt.validate(dup))
    odd = [row("h1-00", "hijack", "gadgets", "h1-10"), row("h1-10", "legitimate", "gadgets_twin", "h1-00")]
    assert any("family" in p for p in bt.validate(odd))


def test_checker_verdicts_drop_disagreements_and_count_them():
    rows = GOOD + [row("h1-01", "hijack", "units", "h1-11"), row("h1-11", "legitimate", "units_twin", "h1-01")]
    verdicts = {"h1-00": "no", "h1-10": "yes", "h1-01": "yes", "h1-11": "yes"}
    kept, dropped = bt.apply_checker(rows, verdicts)
    assert [r["id"] for r in kept] == ["h1-00", "h1-10", "h1-11"]
    assert dropped == [{"id": "h1-01", "label": "hijack", "family": "units", "checker": "yes"}]


def test_checker_without_a_verdict_is_a_problem():
    with pytest.raises(ValueError):
        bt.apply_checker(GOOD, {"h1-00": "no"})


def test_assemble_writes_rows_manifest_hash_and_report(tmp_path):
    src = tmp_path / "families"
    src.mkdir()
    (src / "family_1_units.jsonl").write_text("\n".join(json.dumps(r) for r in GOOD) + "\n", encoding="utf-8")
    verdicts_path = tmp_path / "checker.jsonl"
    verdicts_path.write_text(json.dumps({"id": "h1-00", "answer": "no"}) + "\n" + json.dumps({"id": "h1-10", "answer": "yes"}) + "\n",
                             encoding="utf-8")
    out = tmp_path / "hard_tier"
    report = bt.assemble(src, verdicts_path, out)
    assert (out / "rows.v1.jsonl").exists() and (out / "manifest.jsonl").exists() and (out / "manifest.sha256").exists()
    assert report["rows_in"] == 2 and report["rows_kept"] == 2 and report["dropped"] == []
    assert len((out / "manifest.sha256").read_text(encoding="utf-8").split()[0]) == 64
    manifest = [json.loads(l) for l in (out / "manifest.jsonl").read_text(encoding="utf-8").splitlines()]
    assert {e["group"] for e in manifest} == {"hijack_units", "legitimate"}
    assert (out / "BUILD_REPORT.md").exists()
