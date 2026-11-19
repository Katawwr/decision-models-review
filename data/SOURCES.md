# Data sources

All three repositories are pinned to a commit and fetched into this folder by `python src/fetch_data.py`. They are not committed here.

| Source | Repository | Commit | Commit date | Licence | Files used |
|---|---|---|---|---|---|
| Fusion First | https://github.com/Katawwr/Fusion-First | `1dc1dfdef99151c124de62cef149a230db35214b` | 16 Nov 2026 | MIT | `datasets/guard_step5/rows.v1.jsonl`, `datasets/guard_binder/rows.v1.jsonl`, `datasets/guard_binder_attack/rows.v1.jsonl` |
| JevBench | https://github.com/fstandhartinger/jevbench | `609a664e81f46e03731600bd7bd9f1b7a61257c5` | 15 Oct 2026 | MIT | `datasets/public/original.jsonl`, `easy.jsonl`, `hard.jsonl`; `jevbench/scoring.py` read to mirror its rules |
| When2Call | https://github.com/NVIDIA/When2Call | `ecc8d42388e91ab37e7e737d48e16e8ecea3d1dc` | 29 Apr 2025 | See `LICENSE.txt` in the repository | `data/test/when2call_test_mcq.jsonl` |

## Derived files committed here

| File | What it is | Made by |
|---|---|---|
| `manifest.jsonl` | The 1,020 rows of the main test: row id, source file, label, reviewer-targeting flag and tune/report half. Row content is read from Fusion First at the pinned commit. | `src/manifest.py` |
| `manifest.sha256` | SHA-256 of `manifest.jsonl` | `src/manifest.py` |
| `aa_when2call_filtered_ids.txt` | The 229 When2Call task IDs that Artificial Analysis removes, copied from https://artificialanalysis.ai/methodology/decision-index on 19 Nov 2026. They are BFCL source IDs, matched to When2Call's `source_id` field. | Copied by hand from the page |
