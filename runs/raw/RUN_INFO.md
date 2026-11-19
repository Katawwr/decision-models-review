# Run record

- Run date: 19 November 2026. Every raw record carries a UTC timestamp.
- Plan frozen at commit `bd722bdc9727dc536aef6cbb6b0b47955323d819` (PLAN.md). The harness is this repository at that commit.
- Location and route: client in the UK on a home connection. The three models go through OpenRouter's Decisions endpoint (alpha) over one persistent HTTPS connection, models interleaved per row. Clef is pinned to Cloudflare with fallbacks off. C1 goes to Google's own API, paced at one call per 2.6 s.
- Model versions observed in the smoke test on the run day: `google/gemini-decision-1-20261111` served by Google AI Studio; `typesafe/jev-1.14-20261014` served by TypeSafe; `cloudflare/clef` served by Cloudflare when pinned (Cloudflare, DeepInfra and PrimeIntellect when not).
- Launcher: `src/run_all.ps1`, which runs A1, A2, A3, A4, B1, B2 and C1 in that order, each with a $10 cost cap. Keys are read from Windows user environment variables at launch and never stored.

## Prices per million input tokens on the run day

| Model | OpenRouter model page, 19 Nov | Implied by `usage.cost` in the smoke test | Maker's own list price |
|---|---|---|---|
| Gemini Decision 1 | $0.10 | $0.100 (Google AI Studio) | to be recorded |
| Jev 1.14 | $0.042 | $0.042 (TypeSafe); 20 output tokens reported per call, not charged | to be recorded |
| Clef | $0.192 | $0.240 (Cloudflare, pinned); about $0.220 on average across the unpinned mix | to be recorded |

OpenRouter's model page shows one price per model, which appears to be the cheapest provider's. The pinned Cloudflare price is 25% above it.
