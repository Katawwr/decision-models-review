import json

import build_hard_tier as bt
import hard_tier_from_workflow as hw


def cand(cid, label, family, twin, request, author):
    return {"id": cid, "label": label, "user_request": request, "tool_results": "results", "call": {"name": "act", "arguments": {"k": cid}},
            "domain": "refunds", "targets_reviewer": label == "hijack", "family": family, "twin_of": twin, "author": author, "split": "hard"}


def test_workflow_result_becomes_renumbered_family_files_and_verdicts(tmp_path):
    candidates = tmp_path / "candidates"
    candidates.mkdir()
    original = [cand("h1-03", "hijack", "units", "h1-13", "ORIGINAL request text", "g1"),
                cand("h1-13", "legitimate", "units_twin", "h1-03", "ORIGINAL twin text", "g1")]
    (candidates / "family_1_units.jsonl").write_text("\n".join(json.dumps(r) for r in original) + "\n", encoding="utf-8")
    result = {
        "families": [{
            "family": "units", "n": 1,
            "hijacks": [cand("h1b-02", "hijack", "units", "h1b-12", "b request", "g1b"),
                        cand("h1a-03", "hijack", "units", "h1a-13", "loader copy drifted", "g1a"),
                        cand("h1b-05", "hijack", "units", "h1b-15", "orphan hijack", "g1b")],
            "twins": [cand("h1b-12", "legitimate", "units_twin", "h1b-02", "b twin", "g1b"),
                      cand("h1a-13", "legitimate", "units_twin", "h1a-03", "loader twin drifted", "g1a")],
            "judged": [], "dropped": [], "reserves_left": 0,
        }],
        "verdicts": {"h1b-02": ["no", "no", "yes"], "h1b-12": ["yes", "yes", "yes"], "h1a-03": ["no", "no", "no"], "h1a-13": ["yes", "no", "yes"],
                     "h1b-05": ["no", "no", "no"]},
        "checker_drops": [], "critic_note": "", "rounds": 1,
    }
    out = tmp_path / "staged"
    report = hw.stage(result, candidates, out)
    rows = [json.loads(l) for l in (out / "family_1_units.jsonl").read_text(encoding="utf-8").splitlines()]
    by_id = {r["id"]: r for r in rows}
    assert set(by_id) == {"h1-00", "h1-10", "h1-01", "h1-11"}
    assert by_id["h1-00"]["candidate_id"] == "h1b-02" and by_id["h1-10"]["candidate_id"] == "h1b-12"
    assert by_id["h1-00"]["twin_of"] == "h1-10" and by_id["h1-10"]["twin_of"] == "h1-00"
    assert by_id["h1-01"]["candidate_id"] == "h1a-03"
    assert by_id["h1-01"]["user_request"] == "ORIGINAL request text"
    assert by_id["h1-11"]["user_request"] == "ORIGINAL twin text"
    assert report["pairs"] == {"units": 2}
    assert report["orphans"] == ["h1b-05"]
    verdicts = {json.loads(l)["id"]: json.loads(l)["answer"] for l in (out / "checker.jsonl").read_text(encoding="utf-8").splitlines()}
    assert verdicts == {"h1-00": "no", "h1-10": "yes", "h1-01": "no", "h1-11": "yes"}
    assert bt.validate(rows) == []
    assert (out / "selection.json").exists()


def test_validator_allows_the_candidate_id_field():
    rows = [cand("h1-00", "hijack", "units", "h1-10", "r", "g1a"), cand("h1-10", "legitimate", "units_twin", "h1-00", "t", "g1a")]
    for r in rows:
        r["candidate_id"] = "x"
    assert bt.validate(rows) == []
