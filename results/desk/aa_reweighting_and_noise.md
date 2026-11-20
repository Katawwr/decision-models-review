# AA Decision Index: reweighting and noise

Component scores: 16 Nov 2026 snapshot (benchlm.ai mirror of AA). Weights and item counts: AA methodology page, 19 Nov 2026.

## Index with and without the knowledge and reasoning exams

| Model | Published | Recomputed | Without Omniscience and HLE | Change |
|---|---|---|---|---|
| Jev 1.14 | 66.2 | 66.22 | 72.2 | +6.0 |
| Gemini Decision 1 | 66.0 | 65.98 | 69.6 | +3.6 |
| Clef | 60.3 | 60.34 | 64.8 | +4.5 |
| Drex Max v1.1 | 72.6 | 72.62 | 80.8 | +8.2 |

Knowledge and reasoning (AA-Omniscience-Decision and HLE-MultiChoice) carry 30% of the index.

## Noise

Each component is a mean over its items. With a per-item standard deviation s of the Decision Score, the standard error of the index is sqrt(sum over components of (weight^2 * s^2 / items)). Per-item scores lie in [0, 100], so s is at most 50; for a model near 60 with moderate confidence it is around 40.

| Per-item sd | Index SE | 95% half-width, one model | 95% half-width, gap between two models |
|---|---|---|---|
| 30 | 0.56 | ±1.1 | ±1.5 |
| 40 | 0.74 | ±1.5 | ±2.1 |
| 50 | 0.93 | ±1.8 | ±2.6 |

The reweighted index drops two components and renormalises the other four, so its noise band is wider: Symmetry's weight rises from 15% to 21%.

| Per-item sd | 95% half-width, gap between two models on the reweighted index |
|---|---|
| 30 | ±1.9 |
| 40 | ±2.5 |
| 50 | ±3.2 |

Share of the index variance by component (independent of s):

| Component | Weight | Items | Share of variance |
|---|---|---|---|
| symmetry | 0.15 | 120 | 55% |
| paperclip | 0.30 | 1,500 | 17% |
| omniscience | 0.15 | 500 | 13% |
| hle | 0.15 | 509 | 13% |
| onet | 0.15 | 6,582 | 1% |
| when2call | 0.10 | 3,423 | 1% |

## Reading

- AA's published tie between Jev 1.14 and Gemini Decision 1 (66.2 vs 66.0) depends on the weighting. Jev leads Gemini on all four decision-type components; Gemini leads on both knowledge and reasoning exams.
- Without the two knowledge and reasoning exams the gap is 2.6 points. The 95% band for a gap on the reweighted index is about ±2.5 at a per-item sd of 40 (±1.9 at 30, ±3.2 at 50), so the gap sits at the edge of noise, neither comfortably outside it nor inside it. The claim to make is that the tie depends on the weighting, not that Jev is ahead.
- The per-item sd is an assumption, not a measurement: per-item Decision Scores lie in [0, 100], so 50 is the ceiling and 40 is a plausible value for models scoring near 60. AA publishes no per-item data to replace it.
- AA-Symmetry, with 120 questions and a 15% weight, contributes more than half of the index's sampling variance on its own.
- The gap estimate treats the two models' item-level errors as independent. On shared items they are usually positively correlated, which would narrow the band and push the gap further out; without per-item data this cannot be checked.
