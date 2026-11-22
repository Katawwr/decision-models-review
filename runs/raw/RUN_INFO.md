# Run record

- Run date: 19 November 2026. Every raw record carries a UTC timestamp.
- Plan frozen at commit `bd722bdc9727dc536aef6cbb6b0b47955323d819` (PLAN.md). The harness is this repository at that commit.
- Location and route: client in the UK on a home connection. The three models go through OpenRouter's Decisions endpoint (alpha) over one persistent HTTPS connection, models interleaved per row. Clef is pinned to Cloudflare with fallbacks off. C1 goes to Google's own API, paced at one call per 2.6 s.
- Model versions observed in the smoke test on the run day: `google/gemini-decision-1-20261111` served by Google AI Studio; `typesafe/jev-1.14-20261014` served by TypeSafe; `cloudflare/clef` served by Cloudflare when pinned (Cloudflare, DeepInfra and PrimeIntellect when not).
- Launcher: `src/run_all.ps1`, which runs A1, A2, A3, A4, B1, B2 and C1 in that order, each with a $10 cost cap. Keys are read from Windows user environment variables at launch and never stored.

## Prices per million input tokens on the run day

| Model | OpenRouter model page, 19 Nov | Implied by `usage.cost` in the smoke test | Maker's own list price |
|---|---|---|---|
| Gemini Decision 1 | $0.10 | $0.100 (Google AI Studio) | $0.10 paid tier, free tier free of charge; 0 output tokens |
| Jev 1.14 | $0.042 | $0.042 (TypeSafe); 20 output tokens reported per call, not charged | $0.042 ($42 per billion); output tokens free |
| Clef | $0.192 | $0.240 (Cloudflare, pinned); about $0.220 on average across the unpinned mix | $0.240 on Workers AI (21,818 neurons per million tokens at $0.011 per 1,000 neurons); no output price listed; Clef-flash $0.038, Clef-omni $0.150 |

OpenRouter's model page shows one price per model, which appears to be the cheapest provider's. The pinned Cloudflare price is 25% above it and equals Cloudflare's own list price. For all three models the maker's own price and the price paid through OpenRouter are the same, so OpenRouter adds no mark-up here.

Makers' prices read on 19 November 2026 from: https://ai.google.dev/gemini-api/docs/pricing (Gemini Decision 1 section); https://docs.typesafe.ai/models (price table, Jev 1.14 available from 14 October 2026); https://developers.cloudflare.com/workers-ai/platform/pricing/ (other model pricing table, page modified 18 November 2026).

## Second run day, 20 November 2026

- Plan state: sections 1 to 9 frozen since 19 November; the hard tier (section 13) and the two extra runs (section 11, item 9) were recorded in the plan before their rows were selected or their calls made. Commit history carries the order.
- Runs: hard tier A1, A2, A3 into `runs/hard_tier/raw/` (18:49 to 18:56 UTC); C2 and B2L into `runs/raw/` (18:55 to 19:08 UTC). Same client, OpenRouter route, Clef pin and key handling as the first day. C2 sends the identical choice request to Google's own API and to OpenRouter, interleaved, paced at one call per 2.6 s because the direct calls use the free tier.
- Model versions returned: the same strings as on 19 November for the OpenRouter models. The direct Gemini calls return no model string.
- Prices: unchanged from the table above, checked by the per-call `usage.cost` of the new runs.
- 21 November 2026, 11:14 to 11:19 UTC: A4 on the hard tier, all 116 rows, three repeats per model (`--all-rows`), 1,044 calls, none failed, $0.070, into `runs/hard_tier/raw/A4.jsonl`. Same client, route, pin and key handling. Model strings returned unchanged from 19 and 20 November.

## Third run day, 22 November 2026

- Plan state: item 14 of the deviations log recorded before the first call, and amended (the `aa` presentation) before B2Q ran.
- Runs: B2P, the three generic presentations of the 200 B2L tasks (`minimal`, `numbered`, `bare`), 10:58 to 11:06 UTC, 1,800 calls, none failed, $0.238, into `runs/raw/B2P.jsonl` under the run names `B2P-minimal`, `B2P-numbered` and `B2P-bare`. B2Q, the presentation shown on Artificial Analysis's When2Call page (`aa`), 11:02 to 11:05 UTC, 600 calls, none failed, $0.090, into `runs/raw/B2Q.jsonl` under the run name `B2P-aa`. B2Q ran concurrently with the last third of B2P from the same client; latency from these runs is not used.
- Same client, OpenRouter route, Clef pin and key handling as the earlier days. Model versions returned: the same strings as before.
- Tables: `results/b2_presentations.csv` and `results/b2_presentations_between.csv`.
- B2A, all 3,423 When2Call tasks in the `aa` presentation, 11:59 to 12:44 UTC, 10,269 calls, none failed, $1.495, into `runs/raw/B2A.jsonl`. Same client, route, pin and key handling. Model versions returned: the same strings as before. Tables `results/b2_aa_models.csv`, `b2_aa_tasks.csv` and `b2_aa_between.csv`.
