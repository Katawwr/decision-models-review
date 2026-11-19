# What a decision benchmark should measure

Dated 19 November 2026. Written before any model was run on the test set, and committed so that the date can be checked against the run files.

Decision models answer typed questions with a probability and nothing else. They are sold as a fast, cheap stand-in for the LLM calls that route, gate and judge inside agent systems. That is the use. The measures should follow from it.

## 1. Errors at the operating point, not average accuracy

A decision model's answer is acted on when its probability clears a threshold the operator sets. Nobody runs a guard at 0.5 by choice. The number that matters is how many bad decisions get through at the false-alarm rate the operator can live with, for example hijacked calls allowed when at most 1% or 5% of legitimate calls are blocked. Two models can have the same accuracy at 0.5 and differ exactly where you would run them.

## 2. The two kinds of error reported apart

A blocked legitimate call costs a retry or an annoyed user. A hijacked call let through can move money or data to an attacker. One blended score, whether plain accuracy or a proper scoring rule, prices these the same. A benchmark should report both error rates and let the reader weigh them for their own case.

## 3. Confidently wrong answers counted, not averaged

There is no explanation to inspect, so a wrong answer at 0.98 looks identical, at the point of use, to a right one. Calibration measures such as the Brier score penalise overconfidence on average. The count of wrong answers given at or above a stated confidence is the figure an operator needs, because those are the decisions no threshold would have caught.

## 4. Consistency under rewording

With no reasoning to read, the main assurance that a model understood the question is that it gives the same answer when the question is paraphrased, its options are reordered, or its polarity is flipped. Report the share of decisions that change and the size of the probability swing, per model.

## 5. Text written to steer the model

In the gating and judging roles the model reads material from outside: tool results, web pages, documents, emails. Some of that text will be written by people who know a model is reading it. The benchmark needs rows where the input carries text aimed at the reviewer, and should report how the model does on them against rows without it, and whether seeing the planted text helps or hurts.

## 6. The decisions LLM calls are actually used for

The pitch is replacing LLM calls in pipelines: is this tool call what the user asked for, does this reply refuse, is this document relevant, which route applies. Knowledge recall and hard exam reasoning measure something else. If they are included in a headline index, the weight should be stated and the index reported with and without them, so a buyer of a routing model is not ranking on trivia.

## 7. Labels that can be checked, and a test that can be rerun

People pick from leaderboards, and a leaderboard is only as good as its labels. Where the correct answer is another model's opinion, say so. Where items are private, say how many. Where the prompt is unpublished, say so. Enough must be public that an outsider can rerun a slice and get the same ranking. The hard rows at least should be hand-checked by a person, with the count published. This applies to the test in this project too, which is why its rows, wordings, raw responses and hand-check counts will be published.

## 8. Speed and cost next to accuracy, not folded into it

Latency and price decide whether a model fits a pipeline, so they must be measured and shown, with the route, the location and the date stated. Folding them into one composite with accuracy hides which trade-off the buyer is making.

## 9. Intervals, and the size of each gap

A handful of models, a few hundred items in some components, and uneven weights: ranking noise is large. A two-point gap means nothing without an interval, and a ranking should be reported as gaps with intervals rather than as an order.

## 10. Determinism

A model that returns a different probability for the same input on a different call cannot be thresholded reliably. Repeat a sample and report whether the probabilities move.

## What this means for the test in this project

- Accuracy at 0.5 is reported, but the headline is the share of hijacks let through at 1% and 5% false blocks, with the threshold chosen on a tune half and reported on a separate report half.
- Misses and false blocks are reported separately throughout.
- Confidently wrong answers are counted at 95% confidence.
- Three wordings of the question: the main one, a paraphrase and a polarity flip.
- Rows with text aimed at the reviewer, written by attackers with and without the reviewer's prompt, are reported separately, and each row is run with and without the planted text visible.
- The decision is one that LLM calls are used for today: does the user's request ask for this tool call.
- The rows, wordings, split rule and raw responses are published, and the rows are hand-checked.
- Speed and cost are measured on the same route, interleaved, and reported beside accuracy, never blended.
- Every gap carries an interval.
- A sample is repeated to test determinism.
