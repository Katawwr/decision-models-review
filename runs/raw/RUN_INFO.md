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
