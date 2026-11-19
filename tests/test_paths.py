import paths


def test_pins_are_full_commit_hashes_on_github():
    assert set(paths.PINS) == {"fusion-first", "jevbench", "when2call"}
    for pin in paths.PINS.values():
        assert len(pin["commit"]) == 40
        assert int(pin["commit"], 16) >= 0
        assert pin["url"].startswith("https://github.com/")


def test_models_are_the_three_pinned_openrouter_ids():
    assert paths.MODELS == {
        "gemini": "google/gemini-decision-1",
        "jev": "typesafe/jev-1.14",
        "clef": "cloudflare/clef",
    }


def test_jsonl_round_trip(tmp_path):
    path = tmp_path / "x.jsonl"
    paths.append_jsonl(path, {"a": 1, "text": "ünïcode"})
    paths.append_jsonl(path, {"b": [1, 2]})
    assert paths.read_jsonl(path) == [{"a": 1, "text": "ünïcode"}, {"b": [1, 2]}]
    assert paths.read_jsonl(tmp_path / "missing.jsonl") == []


def test_clef_is_pinned_to_its_maker_and_the_others_are_not():
    assert paths.PROVIDER_PINS == {"cloudflare/clef": "Cloudflare"}
