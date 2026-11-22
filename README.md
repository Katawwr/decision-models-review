# Decision models review

The harness, data manifests, raw run records, analysis and charts behind a review of three decision models on one job: deciding whether an agent's tool call should go ahead. The models are Gemini Decision 1 (Google), Jev 1.14 (TypeSafe) and Clef (Cloudflare). Each answers a typed question with a probability and nothing else, so the only way to know whether to trust one is to measure it. This repository is that measurement, kept whole so that every number in the write-up can be traced to a raw response.

## What was tested

- **The gating question.** Given the user's request, the tool results the agent has read and the tool call the agent now wants to make, is the call what the user asked for? 1,020 labelled rows from [Fusion First](https://github.com/Katawwr/Fusion-First), 1,019 of them analysed after one was rejected as undecidable in the label check (PLAN.md section 11, item 15): 578 legitimate calls and 441 hijacked ones, 160 of them with planted text written at the reviewer rather than the agent, 120 of those by attackers who had the reviewer's prompt.
- **A hard tier.** 116 further rows in 58 pairs across six attack families (a units trick, an extra field, a swapped target, scope creep, a policy note, a false premise), each hijack paired with a legitimate twin that looks the same on the surface. Procedure in [PLAN.md](PLAN.md) section 13, build report in [data/hard_tier/BUILD_REPORT.md](data/hard_tier/BUILD_REPORT.md).
- **Two views and three wordings.** Each row is shown with and without the tool results the attacker wrote into, and the question is asked in a main wording, a paraphrase and a flipped version.
- **Determinism, speed and cost.** Repeat calls on 100 rows; client-side latency over one connection with the models interleaved; cost as billed.
- **The public benchmarks on their own terms.** The public items of JevBench scored by its own rules, and When2Call filtered and scored as Artificial Analysis runs it for its Decision Index, with a desk check of the index's weighting.
- **Route checks.** Gemini called on Google's own API as well as through OpenRouter, including byte-identical requests sent through both.

All three models went through OpenRouter's Decisions endpoint, with Clef pinned to Cloudflare so that one provider served it throughout. The measures are errors at the default threshold and at 1% and 5% false-block budgets (threshold chosen on one half of the rows, measured on the other), confidently wrong answers, the Brier score and the Decision Score, rewording flips, change between views, determinism, latency and cost. Every comparison between models is a paired test on the same rows: exact McNemar and a paired bootstrap.

The protocol in [PLAN.md](PLAN.md) was frozen before the first paid call (commit bd722bd). Everything added afterwards is recorded in its deviations log (section 11), including the hard tier, which was specified in section 13 before any of its rows existed. [PRINCIPLES.md](PRINCIPLES.md), written before the runs, sets out what a decision benchmark should measure.

## Results

- [results/SUMMARY.md](results/SUMMARY.md): every table for the main set and the two benchmarks, with the CSVs beside it.
- [results/hard_tier/SUMMARY.md](results/hard_tier/SUMMARY.md): the same tables for the hard tier.
- [results/charts/](results/charts/) and [results/hard_tier/charts/](results/hard_tier/charts/): the figures, each with its takeaway in the title and a `charts.json` naming the table behind it.
- [results/handcheck/](results/handcheck/): blind hand-check sheets (a 100-row sample, the rows on which the models disagree, and all 116 hard-tier rows), the record of the 22 November label check, and the one rejected id.
- [results/desk/](results/desk/): the Artificial Analysis Decision Index scores as published on 19 November 2026, notes on its methodology page with links to archived copies, and the reweighting check.
- [runs/raw/RUN_INFO.md](runs/raw/RUN_INFO.md): run dates, model version strings as returned, prices on the day and the route.

## Layout

| Path | What it holds |
|---|---|
| `PLAN.md` | The frozen protocol, the deviations log and the hard tier procedure |
| `PRINCIPLES.md` | What a decision benchmark should measure |
| `data/SOURCES.md` | The three source repositories, pinned by commit, with their licences |
| `data/manifest.jsonl` | The 1,020 main rows: id, source file, label, group and tune/report half; the content stays in Fusion First. One row, named in `results/handcheck/rejected_ids_2026-11-22.txt`, is excluded from the analysis |
| `data/hard_tier/` | The 116 hard-tier rows, their manifest and hashes, the build report and the selection record |
| `src/` | The harness (client, views, questions, runner), converters for the two benchmarks, measures, analysis, charts, hand-check sheets and the hard-tier build |
| `tests/` | Tests for all of the above |
| `runs/raw/`, `runs/hard_tier/raw/` | One JSON line per call, appended as each returned, failures included |
| `results/`, `results/hard_tier/` | Tables, charts, hand-check sheets and desk research |

## Reproducing

Python 3.12 or later and git. The dependencies are listed in `pyproject.toml`.

```
pip install httpx numpy scipy pandas matplotlib pytest
python -m pytest
python src/fetch_data.py
```

`fetch_data.py` clones the three source repositories into `data/` at the commits named in `data/SOURCES.md`. Keys are read from the environment only: `OPENROUTER_API_KEY` for the three models through OpenRouter and `GEMINI_API_KEY` for the direct Gemini runs. Nothing writes a key to disk.

```
python src/run_main.py SMOKE                   # 30 rows, three models: a plumbing check
python src/run_main.py A1 --max-cost 10        # the main run; every run has a cost cap
python src/run_main.py A1 --tier-dir data/hard_tier
python src/analyse.py
python src/analyse.py --raw-dir runs/hard_tier/raw --manifest data/hard_tier/manifest.jsonl --out results/hard_tier
python src/charts.py
python src/charts.py --results results/hard_tier --out results/hard_tier/charts --no-desk
python src/handcheck.py sample --n 100
python src/handcheck.py disagreements
python src/handcheck.py tier --tier-dir data/hard_tier
python src/analyse.py --exclude results/handcheck/rejected_ids_2026-11-22.txt   # the published tables: one id per line is dropped before every table
```

| Run | What it is |
|---|---|
| `SMOKE` | 30 rows, View B, main wording |
| `A1` | All 1,020 rows, View B (tool results shown), main wording |
| `A2` | All rows, View A (tool results hidden) |
| `A3` | All rows, View B, the paraphrase and the flipped wording |
| `A4` | 100 rows, three repeats each, for determinism |
| `B1` | The public JevBench items |
| `B2` | When2Call, 3,423 tasks after Artificial Analysis's filter, options labelled A to D |
| `B2L` | 200 of those tasks with the category names as labels |
| `C1` | 200 rows to Gemini on Google's API |
| `C2` | 100 When2Call tasks, the identical request through OpenRouter and Google's API |

With `--tier-dir data/hard_tier`, `A1`, `A2` and `A3` run on the hard tier and write to `runs/hard_tier/raw/`. `--dry-run` answers from a hash with no network. A run that stops part-way resumes from its raw file and skips the calls already answered. `src/run_all.ps1` is the launcher used on the run day.

Each raw record holds the call's answer, latency, token counts, cost, the model and provider strings returned, and the SHA-256 of the request. The request text itself is not stored, so the source rows are not republished here; `request_hash` in `src/runner.py` rebuilds the hash from the pinned data.

## Data and licences

The code, manifests, hard-tier rows, run records, tables and charts in this repository are released under the MIT licence (see [LICENSE](LICENSE)). The source datasets are not included: Fusion First (MIT), JevBench (MIT) and When2Call (its own licence) are fetched at pinned commits as described in [data/SOURCES.md](data/SOURCES.md). The files in `results/desk/` record Artificial Analysis's published scores and the parts of its methodology that the reweighting depends on, dated and with links to archived copies of the pages; the pages themselves remain Artificial Analysis's.

## Limits

- The attack rows were written by language models to a brief and checked blind by other models. The hand-check sheets in `results/handcheck/` were written for a human pass; on 22 November 2026 they were checked by model reviewers instead (a blind reader, a label auditor and three adjudicators on every flagged row), which confirmed all 218 labels and rejected one main-set row as undecidable. The record is `results/handcheck/check-record-2026-11-22.md`. The hard tier's build report lists every candidate dropped and why.
- The reviewer-targeted rows in the main set were written against a different reviewer, so they test transfer, not an attack tuned to these three models.
- One day, one location, alpha APIs. Model version strings and prices on the day are in `runs/raw/RUN_INFO.md`.
- Three models, one task family (gating agent tool calls), and the public halves of two benchmarks whose private halves cannot be reproduced.
