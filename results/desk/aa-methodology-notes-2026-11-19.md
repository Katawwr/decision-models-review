# Artificial Analysis Decision Index: methodology notes

What this study used from Artificial Analysis's published material, in our own words, with archived copies of the pages. Read on 19 November 2026. A text copy of the methodology page and a screenshot of the index chart were kept in this folder until 21 November 2026, when they were replaced by these notes and the links below; both remain in the repository's history.

## Pages and archived copies

| Page | Read | Archived before the reading | Archived after |
|---|---|---|---|
| Methodology: https://artificialanalysis.ai/methodology/decision-index | 19 Nov 2026, 12:07 UTC | [14 Nov 2026, 09:59 UTC](https://web.archive.org/web/20261114095947/https://artificialanalysis.ai/methodology/decision-index) | [21 Nov 2026, 11:09 UTC](https://web.archive.org/web/20261121110910/https://artificialanalysis.ai/methodology/decision-index) |
| Index page: https://artificialanalysis.ai/evaluations/artificial-analysis-decision-index | 19 Nov 2026, 12:04 UTC | [17 Nov 2026, 14:39 UTC](https://web.archive.org/web/20261117143925/https://artificialanalysis.ai/evaluations/artificial-analysis-decision-index) | [21 Nov 2026, 11:09 UTC](https://web.archive.org/web/20261121110944/https://artificialanalysis.ai/evaluations/artificial-analysis-decision-index) |

On 21 November 2026 the live methodology page matched the 19 November reading on every point below; the only differences were in how the formulas render as text. Both archived copies of the methodology page describe version 2.1 with the same weights, item counts and filter.

## The index as read on 19 November 2026

Version 2.1, dated November 2026. The index is a weighted average of six evaluations: five scored by the Decision Score and one, AA-Symmetry, by its own Symmetry Score.

| Evaluation | What it tests | Items | Weight | Data |
|---|---|---|---|---|
| AA-Paperclip | Decisions and extraction on resumes, receipts and invoices, and research papers; each document's 15 answers scored as one decision | 1,500 documents | 30% | Private |
| EvalSafe-O*NET-AA | Judgements about synthetic workplace documents, from TypeSafe's EvalSafe O*NET benchmark (Apache-2.0) | 6,582 of 7,500 questions | 15% | Public |
| When2Call | NVIDIA's tool-calling test (CC BY 4.0), each task a choice among four replies: answer directly, call a tool, ask for more information, or say it cannot answer | 3,423 of 3,652 tasks | 10% | Public |
| AA-Omniscience-Decision v1.1 | Knowledge and hallucination: four answers and an option to decline | 500 questions | 15% | Private |
| HLE-MultiChoice v1.1 | Reasoning: the text-only multiple-choice questions of Humanity's Last Exam, with an option to decline | 509 of 513 questions | 15% | Public source |
| AA-Symmetry v1.1 | Whether a decision holds when its options are moved or reworded, or the question is negated | 120 questions in 460 forms | 15% | Forms not published |

At least 45% of the weight (AA-Paperclip and AA-Omniscience-Decision) rests on private data. Knowledge and reasoning (AA-Omniscience-Decision and HLE-MultiChoice) carry 30%; the check in `aa_reweighting_and_noise.md` drops those two and renormalises the other four.

## Points the study relies on

- **Decision Score.** For a question where the chosen answer was given probability p, and c is 1 if that answer is right and 0 if not, the question scores 50 × (1 + c − (p − c)²). An evaluation's score is the mean over its questions, which equals 50 × (1 + accuracy − Brier). A uniform guess over K answers is worth 50 × (1 + 1/K²) in expectation, and a question that errored or went unanswered is scored at that value. `src/convert_when2call.py` applies this scoring.
- **The chosen answer.** The option given the highest probability; for a yes/no question, yes when the probability of yes is 0.5 or more. A tie is scored as the average over a random tie-break.
- **How decision models are called.** The state and the questions are sent to the model's decision API. The page does not give the wording of the questions or any criteria text, so the exact request sent to the decision models is not published.
- **When2Call as the index runs it.** 229 "ask for more information" tasks are removed as ambiguous, leaving 3,423; the page lists their ids, copied in `data/aa_when2call_filtered_ids.txt`. The four candidate replies are shuffled per task. The headline accuracy is the share of tasks answered with the reply of the correct category.
- **EvalSafe-O*NET-AA.** The questions have no ground truth. The reference answer is the consensus of two language models named on the page, and the 918 questions on which they disagree are left out.
- **Symmetry Score.** Per question, 0 if the most probable option changes between forms, otherwise 1 minus the range across forms of the probability's margin above chance, rescaled so that questions with different numbers of options score alike; averaged from 0 to 100.
- **Calibration.** Each evaluation's Brier score is the mean of (p − c)² over its questions; the index Brier score averages them with the index weights.

## AA's cost and time per task, from the archived index page

The index page embeds each model's index score, average cost per task and average time per task; the two archived copies (17 and 21 November 2026, linked above) hold the same values. AA's cost per task is its average at current token prices and its time per task is its own measurement; the page does not say where its client ran or by what route.

| Model | Index score | Cost per million tasks, USD | Time per task, ms |
|---|---|---|---|
| Jev 1.14 | 66.2 | 156 | 92 |
| Gemini Decision 1 | 66.0 | 345 | 211 |
| Clef | 60.3 | 863 | 354 |
| Drex Max v1.1 | 72.6 | 103 | 283 |
| d1.2-ultra | 74.8 | 133 | 218 |

Read against this study's own frontier charts: AA's tasks are far longer than our rows (Gemini's $345 per million tasks at $0.10 per million input tokens implies about 3,500 input tokens per task, against 371 on our main set and 463 on the hard tier), so AA's cost per task is about seven times ours for the same model; AA shows Clef at 1.7 times Gemini's time per task, while from our UK client through OpenRouter the two have the same median and Clef differs only in its tail. Neither chart is wrong; they measure different inputs from different places.

## The index page as read on 19 November 2026

- `aa-index-scores-2026-11-19.json` holds the integer bar labels of the index chart as read from the page, 18 of 25 models shown: Jev 1.14 and Gemini Decision 1 at 66, Clef at 60, d1.2-ultra at 75 at the top.
- The component scores used in `src/desk_aa.py` come from the 16 November 2026 snapshot mirrored by benchlm.ai. Their weighted average reproduces the published index to within 0.05 for each of the four models checked, which is the test that the mirror is right.
