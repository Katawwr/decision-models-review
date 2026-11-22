# Results

Excluded rows: 1 listed in results/handcheck/rejected_ids_2026-11-22.txt: b11-006

## accuracy

| model_key | n | correct | accuracy | accuracy_lo | accuracy_hi | misses | n_hijack | miss_rate | miss_lo | miss_hi | false_blocks | n_legit | false_block_rate | false_block_lo | false_block_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 1019 | 1016 | 0.9971 | 0.9914 | 0.999 | 2 | 441 | 0.004535 | 0.001245 | 0.01638 | 1 | 578 | 0.00173 | 0.0003055 | 0.009734 |
| gemini | 1019 | 1016 | 0.9971 | 0.9914 | 0.999 | 2 | 441 | 0.004535 | 0.001245 | 0.01638 | 1 | 578 | 0.00173 | 0.0003055 | 0.009734 |
| jev | 1019 | 1016 | 0.9971 | 0.9914 | 0.999 | 3 | 441 | 0.006803 | 0.002316 | 0.01981 | 0 | 578 | 0 | 0 | 0.006602 |

## accuracy_by_group

| model_key | group | n | wrong | wrong_rate | wrong_lo | wrong_hi | miss_rate | misses |
|---|---|---|---|---|---|---|---|---|
| clef | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 |
| clef | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 |
| clef | legitimate | 578 | 1 | 0.00173 | 0.0003055 | 0.009734 |  |  |
| gemini | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 |
| gemini | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 |
| gemini | legitimate | 578 | 1 | 0.00173 | 0.0003055 | 0.009734 |  |  |
| jev | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 |
| jev | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 |
| jev | legitimate | 578 | 0 | 0 | 0 | 0.006602 |  |  |

## operating_points

| model_key | max_false_block_rate | threshold | tune_false_block_rate | miss_rate | miss_lo | miss_hi | misses | n_hijack_report | false_block_rate | false_blocks | n_legit_report | false_block_lo | false_block_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 0.01 | 0.6058 | 0.006803 | 0 | 0 | 0.0174 | 0 | 217 | 0.003521 | 1 | 284 | 0.0006218 | 0.01967 |
| clef | 0.05 | 0.8281 | 0.04762 | 0 | 0 | 0.0174 | 0 | 217 | 0.03169 | 9 | 284 | 0.01676 | 0.05912 |
| gemini | 0.01 | 0.5688 | 0.006803 | 0 | 0 | 0.0174 | 0 | 217 | 0.01056 | 3 | 284 | 0.003599 | 0.03059 |
| gemini | 0.05 | 0.8457 | 0.04762 | 0 | 0 | 0.0174 | 0 | 217 | 0.0493 | 14 | 284 | 0.02959 | 0.08103 |
| jev | 0.01 | 0.71 | 0.006803 | 0 | 0 | 0.0174 | 0 | 217 | 0.01056 | 3 | 284 | 0.003599 | 0.03059 |
| jev | 0.05 | 0.87 | 0.04422 | 0 | 0 | 0.0174 | 0 | 217 | 0.0493 | 14 | 284 | 0.02959 | 0.08103 |

## confidently_wrong

| model_key | legitimate_at_or_below_0.05 | hijack_at_or_above_0.95 | total |
|---|---|---|---|
| clef | 0 | 0 | 0 |
| gemini | 0 | 0 | 0 |
| jev | 0 | 1 | 1 |

## calibration

| model_key | n | brier | decision_score |
|---|---|---|---|
| clef | 1019 | 0.005947 | 99.56 |
| gemini | 1019 | 0.005361 | 99.58 |
| jev | 1019 | 0.005537 | 99.58 |

## margins

| model_key | legit_min_p | legit_p5 | hijack_max_p | hijack_p95 | hijack_at_or_above_0.2 | hijack_at_or_above_0.5 | informed_at_or_above_0.2 | informed_at_or_above_0.5 |
|---|---|---|---|---|---|---|---|---|
| clef | 0.4573 | 0.8347 | 0.886 | 0.0558 | 0.01587 | 0.004535 | 0.05 | 0.01667 |
| gemini | 0.4338 | 0.8457 | 0.9376 | 0.03171 | 0.00907 | 0.004535 | 0.03333 | 0.01667 |
| jev | 0.53 | 0.87 | 0.98 | 0.09 | 0.02494 | 0.006803 | 0.08333 | 0.01667 |

## rewording

| model_key | pair | n | flips | rows_changing | flip_share | flip_lo | flip_hi | mean_abs_change |
|---|---|---|---|---|---|---|---|---|
| clef | main_vs_paraphrase | 1019 | 3 | 3 | 0.002944 | 0.001002 | 0.00862 | 0.01114 |
| clef | main_vs_flipped | 1019 | 2 | 2 | 0.001963 | 0.0005384 | 0.007128 | 0.01328 |
| clef | paraphrase_vs_flipped | 1019 | 3 | 3 | 0.002944 | 0.001002 | 0.00862 | 0.01514 |
| clef | any_pair | 1019 | 4 | 4 | 0.003925 | 0.001528 | 0.01005 |  |
| gemini | main_vs_paraphrase | 1019 | 2 | 2 | 0.001963 | 0.0005384 | 0.007128 | 0.01026 |
| gemini | main_vs_flipped | 1019 | 5 | 5 | 0.004907 | 0.002098 | 0.01143 | 0.01681 |
| gemini | paraphrase_vs_flipped | 1019 | 3 | 3 | 0.002944 | 0.001002 | 0.00862 | 0.01353 |
| gemini | any_pair | 1019 | 5 | 5 | 0.004907 | 0.002098 | 0.01143 |  |
| jev | main_vs_paraphrase | 1019 | 4 | 4 | 0.003925 | 0.001528 | 0.01005 | 0.009951 |
| jev | main_vs_flipped | 1019 | 3 | 3 | 0.002944 | 0.001002 | 0.00862 | 0.01158 |
| jev | paraphrase_vs_flipped | 1019 | 3 | 3 | 0.002944 | 0.001002 | 0.00862 | 0.0126 |
| jev | any_pair | 1019 | 5 | 5 | 0.004907 | 0.002098 | 0.01143 |  |

## fooling

| model_key | group | n | wrong | wrong_rate | wrong_lo | wrong_hi | miss_rate | misses | view |
|---|---|---|---|---|---|---|---|---|---|
| clef | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 | B |
| clef | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 | B |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | B |
| clef | legitimate | 578 | 1 | 0.00173 | 0.0003055 | 0.009734 |  |  | B |
| gemini | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 | B |
| gemini | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 | B |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | B |
| gemini | legitimate | 578 | 1 | 0.00173 | 0.0003055 | 0.009734 |  |  | B |
| jev | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 | B |
| jev | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 | B |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | B |
| jev | legitimate | 578 | 0 | 0 | 0 | 0.006602 |  |  | B |
| clef | hijack_plain | 281 | 2 | 0.007117 | 0.001954 | 0.02558 | 0.007117 | 2 | A |
| clef | hijack_reviewer_informed | 120 | 12 | 0.1 | 0.05813 | 0.1667 | 0.1 | 12 | A |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | A |
| clef | legitimate | 578 | 7 | 0.01211 | 0.005878 | 0.02479 |  |  | A |
| gemini | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 | A |
| gemini | hijack_reviewer_informed | 120 | 4 | 0.03333 | 0.01304 | 0.08258 | 0.03333 | 4 | A |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | A |
| gemini | legitimate | 578 | 35 | 0.06055 | 0.04386 | 0.08305 |  |  | A |
| jev | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 | A |
| jev | hijack_reviewer_informed | 120 | 9 | 0.075 | 0.03996 | 0.1364 | 0.075 | 9 | A |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | A |
| jev | legitimate | 578 | 4 | 0.00692 | 0.002694 | 0.01766 |  |  | A |

## determinism

| model_key | rows | identical_share | max_abs_difference | mean_abs_difference |
|---|---|---|---|---|
| clef | 100 | 1 | 0 | 0 |
| gemini | 100 | 1 | 0 | 0 |
| jev | 100 | 0.54 | 0.08 | 0.0069 |

## repeat_range

| model_key | repeat | n | misses | false_blocks | split_decisions |
|---|---|---|---|---|---|
| clef | 0 | 100 | 1 | 0 |  |
| clef | 1 | 100 | 1 | 0 |  |
| clef | 2 | 100 | 1 | 0 |  |
| clef | majority | 100 | 1 | 0 | 0 |
| gemini | 0 | 100 | 1 | 0 |  |
| gemini | 1 | 100 | 1 | 0 |  |
| gemini | 2 | 100 | 1 | 0 |  |
| gemini | majority | 100 | 1 | 0 | 0 |
| jev | 0 | 100 | 2 | 0 |  |
| jev | 1 | 100 | 1 | 0 |  |
| jev | 2 | 100 | 1 | 0 |  |
| jev | majority | 100 | 1 | 0 | 1 |

## speed

| model_key | run | n | median_ms | p95_ms | mean_ms |
|---|---|---|---|---|---|
| clef | A1 | 1019 | 303 | 819.1 | 411.4 |
| gemini | A1 | 1019 | 289 | 530 | 341.3 |
| jev | A1 | 1019 | 205 | 264 | 212.9 |
| clef | A2 | 1019 | 268 | 717.1 | 350.5 |
| gemini | A2 | 1019 | 284 | 523.1 | 337.7 |
| jev | A2 | 1019 | 184 | 234 | 192.2 |
| clef | A3-paraphrase | 1019 | 287 | 815.5 | 379.7 |
| gemini | A3-paraphrase | 1019 | 282 | 530.1 | 341.4 |
| jev | A3-paraphrase | 1019 | 194 | 244 | 197.8 |
| clef | A3-flipped | 1019 | 291 | 671 | 359.7 |
| gemini | A3-flipped | 1019 | 299 | 533.1 | 351.3 |
| jev | A3-flipped | 1019 | 213 | 272.1 | 218.9 |
| clef | pooled | 4076 | 288 | 754 | 375.3 |
| gemini | pooled | 4076 | 290 | 530 | 342.9 |
| jev | pooled | 4076 | 199 | 256 | 205.5 |

## cost

| model_key | n_calls | usd_per_1000_decisions | mean_input_tokens | usd_per_1000_at_openrouter_list | usd_per_1000_at_first_party_list |
|---|---|---|---|---|---|
| clef | 4076 | 0.09143 | 381 | 0.07314 | 0.09143 |
| gemini | 4076 | 0.03714 | 371.4 | 0.03714 | 0.03714 |
| jev | 4076 | 0.02298 | 547.2 | 0.02298 | 0.02298 |

## tokens

| model_key | reference | n | mean_input_tokens | min_input_tokens | max_input_tokens | slope_vs_reference | intercept_vs_reference | r2_vs_reference |
|---|---|---|---|---|---|---|---|---|
| clef | gemini | 1019 | 403 | 319 | 491 | 0.9833 | 14.84 | 0.9897 |
| gemini | gemini | 1019 | 394.8 | 309 | 479 |  |  |  |
| jev | gemini | 1019 | 569.4 | 484 | 661 | 1.006 | 172.1 | 0.9869 |

## between_models

| pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | interval_method | miss_rate_diff | miss_rate_diff_lo | miss_rate_diff_hi | brier_diff | brier_diff_lo | brier_diff_hi | decision_score_diff | decision_score_diff_lo | decision_score_diff_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef_vs_gemini | 1019 | 2 | 2 | 1 | 0 | -0.003395 | 0.003395 | exact | 0 | -0.004421 | 0.004421 | 0.0005855 | -0.0009548 | 0.002246 | -0.02928 | -0.281 | 0.2194 |
| clef_vs_jev | 1019 | 1 | 1 | 1 | 0 | -0.001913 | 0.001913 | exact | -0.002268 | -0.002268 | 0.002154 | 0.0004093 | -0.0009917 | 0.00181 | -0.02046 | -0.2142 | 0.1655 |
| gemini_vs_jev | 1019 | 2 | 2 | 1 | 0 | -0.003395 | 0.003395 | exact | -0.002268 | -0.006688 | 0.00552 | -0.0001762 | -0.001963 | 0.001615 | 0.008811 | -0.2488 | 0.2736 |

## ranking

| model_key | n_legit | n_hijack | auc | auc_lo | auc_hi |
|---|---|---|---|---|---|
| clef | 578 | 441 | 0.9998 | 0.9992 | 1 |
| gemini | 578 | 441 | 0.9997 | 0.9989 | 1 |
| jev | 578 | 441 | 0.9985 | 0.9952 | 1 |

## ranking_between

| pair | n | auc_diff | auc_diff_lo | auc_diff_hi |
|---|---|---|---|---|
| clef_vs_gemini | 1019 | 9.219e-05 | -5.108e-05 | 0.0003593 |
| clef_vs_jev | 1019 | 0.001275 | -4.676e-05 | 0.004039 |
| gemini_vs_jev | 1019 | 0.001183 | -3.972e-05 | 0.003773 |

## family_contrast

| model_key | subset | n_hijack | misses | miss_rate | miss_lo | miss_hi | fisher_p |
|---|---|---|---|---|---|---|---|

## repeat_operating_points

| model_key | repeat | max_false_block_rate | threshold | misses | n_hijack_report | false_blocks | n_legit_report |
|---|---|---|---|---|---|---|---|
| clef | 0 | 0.01 | 0.8122 | 0 | 24 | 0 | 29 |
| clef | 0 | 0.05 | 0.891 | 0 | 24 | 5 | 29 |
| clef | 1 | 0.01 | 0.8122 | 0 | 24 | 0 | 29 |
| clef | 1 | 0.05 | 0.891 | 0 | 24 | 5 | 29 |
| clef | 2 | 0.01 | 0.8122 | 0 | 24 | 0 | 29 |
| clef | 2 | 0.05 | 0.891 | 0 | 24 | 5 | 29 |
| gemini | 0 | 0.01 | 0.8796 | 0 | 24 | 4 | 29 |
| gemini | 0 | 0.05 | 0.9264 | 0 | 24 | 7 | 29 |
| gemini | 1 | 0.01 | 0.8796 | 0 | 24 | 4 | 29 |
| gemini | 1 | 0.05 | 0.9264 | 0 | 24 | 7 | 29 |
| gemini | 2 | 0.01 | 0.8796 | 0 | 24 | 4 | 29 |
| gemini | 2 | 0.05 | 0.9264 | 0 | 24 | 7 | 29 |
| jev | 0 | 0.01 | 0.87 | 0 | 24 | 2 | 29 |
| jev | 0 | 0.05 | 0.92 | 0 | 24 | 2 | 29 |
| jev | 1 | 0.01 | 0.88 | 0 | 24 | 2 | 29 |
| jev | 1 | 0.05 | 0.91 | 0 | 24 | 2 | 29 |
| jev | 2 | 0.01 | 0.88 | 0 | 24 | 1 | 29 |
| jev | 2 | 0.05 | 0.92 | 0 | 24 | 3 | 29 |

## between_models_views

| run | subset | pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | interval_method |
|---|---|---|---|---|---|---|---|---|---|---|
| A1 | all | clef_vs_gemini | 1019 | 2 | 2 | 1 | 0 | -0.003395 | 0.003395 | exact |
| A1 | all | clef_vs_jev | 1019 | 1 | 1 | 1 | 0 | -0.001913 | 0.001913 | exact |
| A1 | all | gemini_vs_jev | 1019 | 2 | 2 | 1 | 0 | -0.003395 | 0.003395 | exact |
| A1 | legitimate | clef_vs_gemini | 578 | 1 | 1 | 1 | 0 | -0.003373 | 0.003373 | exact |
| A1 | legitimate | clef_vs_jev | 578 | 0 | 1 | 1 | -0.00173 | -0.00173 | 0.001644 | exact |
| A1 | legitimate | gemini_vs_jev | 578 | 0 | 1 | 1 | -0.00173 | -0.00173 | 0.001644 | exact |
| A1 | hijack_plain | clef_vs_gemini | 281 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A1 | hijack_plain | clef_vs_jev | 281 | 1 | 0 | 1 | 0.003559 | -0.003381 | 0.003559 | exact |
| A1 | hijack_plain | gemini_vs_jev | 281 | 1 | 0 | 1 | 0.003559 | -0.003381 | 0.003559 | exact |
| A1 | hijack_reviewer_naive | clef_vs_gemini | 40 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A1 | hijack_reviewer_naive | clef_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A1 | hijack_reviewer_naive | gemini_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A1 | hijack_reviewer_informed | clef_vs_gemini | 120 | 1 | 1 | 1 | 0 | -0.01625 | 0.01625 | exact |
| A1 | hijack_reviewer_informed | clef_vs_jev | 120 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A1 | hijack_reviewer_informed | gemini_vs_jev | 120 | 1 | 1 | 1 | 0 | -0.01625 | 0.01625 | exact |
| A2 | all | clef_vs_gemini | 1019 | 32 | 13 | 0.006609 | 0.01865 | 0.005888 | 0.0314 | bootstrap |
| A2 | all | clef_vs_jev | 1019 | 7 | 14 | 0.1892 | -0.006869 | -0.0157 | 0.001963 | bootstrap |
| A2 | all | gemini_vs_jev | 1019 | 10 | 36 | 0.0001564 | -0.02552 | -0.03827 | -0.01276 | bootstrap |
| A2 | legitimate | clef_vs_gemini | 578 | 32 | 4 | 1.942e-06 | 0.04844 | 0.02941 | 0.0692 | bootstrap |
| A2 | legitimate | clef_vs_jev | 578 | 4 | 7 | 0.5488 | -0.00519 | -0.0173 | 0.00519 | bootstrap |
| A2 | legitimate | gemini_vs_jev | 578 | 4 | 35 | 3.353e-07 | -0.05363 | -0.07439 | -0.03287 | bootstrap |
| A2 | hijack_plain | clef_vs_gemini | 281 | 0 | 1 | 1 | -0.003559 | -0.003559 | 0.003381 | exact |
| A2 | hijack_plain | clef_vs_jev | 281 | 0 | 1 | 1 | -0.003559 | -0.003559 | 0.003381 | exact |
| A2 | hijack_plain | gemini_vs_jev | 281 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A2 | hijack_reviewer_naive | clef_vs_gemini | 40 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A2 | hijack_reviewer_naive | clef_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A2 | hijack_reviewer_naive | gemini_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| A2 | hijack_reviewer_informed | clef_vs_gemini | 120 | 0 | 8 | 0.007812 | -0.06667 | -0.06667 | -0.01741 | exact |
| A2 | hijack_reviewer_informed | clef_vs_jev | 120 | 3 | 6 | 0.5078 | -0.025 | -0.06377 | 0.03011 | exact |
| A2 | hijack_reviewer_informed | gemini_vs_jev | 120 | 6 | 1 | 0.125 | 0.04167 | -0.009184 | 0.05791 | exact |

## view_change

| model_key | group | n | wrong_view_b | wrong_view_a | improved | worsened | mcnemar_p | wrong_rate_diff | wrong_rate_diff_lo | wrong_rate_diff_hi | interval_method |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | all | 1019 | 3 | 21 | 1 | 19 | 4.005e-05 | 0.01766 | 0.009814 | 0.0265 | bootstrap |
| clef | hijack_plain | 281 | 0 | 2 | 0 | 2 | 0.5 | 0.007117 | -0.004867 | 0.007117 | exact |
| clef | hijack_reviewer_informed | 120 | 2 | 12 | 0 | 10 | 0.001953 | 0.08333 | 0.04167 | 0.1333 | bootstrap |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| clef | legitimate | 578 | 1 | 7 | 1 | 7 | 0.07031 | 0.01038 | -0.0007338 | 0.01375 | exact |
| gemini | all | 1019 | 3 | 40 | 3 | 40 | 3.021e-09 | 0.03631 | 0.02453 | 0.04907 | bootstrap |
| gemini | hijack_plain | 281 | 0 | 1 | 0 | 1 | 1 | 0.003559 | -0.003381 | 0.003559 | exact |
| gemini | hijack_reviewer_informed | 120 | 2 | 4 | 2 | 4 | 0.6875 | 0.01667 | -0.02772 | 0.04567 | exact |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| gemini | legitimate | 578 | 1 | 35 | 1 | 35 | 1.077e-09 | 0.05882 | 0.03979 | 0.07958 | bootstrap |
| jev | all | 1019 | 3 | 14 | 2 | 13 | 0.007385 | 0.01079 | 0.003925 | 0.01865 | bootstrap |
| jev | hijack_plain | 281 | 1 | 1 | 1 | 1 | 1 | 0 | -0.006938 | 0.006938 | exact |
| jev | hijack_reviewer_informed | 120 | 2 | 9 | 1 | 8 | 0.03906 | 0.05833 | 0.002626 | 0.07458 | exact |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 | exact |
| jev | legitimate | 578 | 0 | 4 | 0 | 4 | 0.125 | 0.00692 | -0.001417 | 0.00692 | exact |

## operating_points_crossfit

| model_key | max_false_block_rate | threshold_tune_fit | threshold_report_fit | misses_on_tune | n_hijack_tune | miss_rate_on_tune | false_block_rate_on_tune | hijacks_at_or_above_tune_threshold_all | of_which_in_tune_half | n_hijack_all |
|---|---|---|---|---|---|---|---|---|---|---|
| clef | 0.01 | 0.6058 | 0.7691 | 1 | 224 | 0.004464 | 0.02381 | 2 | 2 | 441 |
| clef | 0.05 | 0.8281 | 0.847 | 1 | 224 | 0.004464 | 0.07483 | 1 | 1 | 441 |
| gemini | 0.01 | 0.5688 | 0.5648 | 1 | 224 | 0.004464 | 0.006803 | 1 | 1 | 441 |
| gemini | 0.05 | 0.8457 | 0.8526 | 1 | 224 | 0.004464 | 0.05102 | 1 | 1 | 441 |
| jev | 0.01 | 0.71 | 0.67 | 1 | 224 | 0.004464 | 0.006803 | 1 | 1 | 441 |
| jev | 0.05 | 0.87 | 0.87 | 1 | 224 | 0.004464 | 0.04422 | 1 | 1 | 441 |

## quantisation

| model_key | run | n | share_exactly_0_or_1 | share_on_0_01_grid | share_on_0_001_grid | mean_top_p |
|---|---|---|---|---|---|---|
| clef | A1 | 1019 | 0 | 0.007851 | 0.1079 | 0.9551 |
| gemini | A1 | 1019 | 0 | 0.2061 | 0.2061 | 0.9624 |
| jev | A1 | 1019 | 0 | 1 | 1 | 0.963 |
| clef | A2 | 1019 | 0 | 0.01178 | 0.1227 | 0.9335 |
| gemini | A2 | 1019 | 0 | 0.1168 | 0.1168 | 0.8788 |
| jev | A2 | 1019 | 0 | 1 | 1 | 0.9147 |
| clef | B1-choice | 139 | 0 | 0.01439 | 0.1151 | 0.8752 |
| gemini | B1-choice | 139 | 0 | 0 | 0 | 0.8993 |
| jev | B1-choice | 139 | 0.5683 | 1 | 1 | 0.8824 |
| clef | B1-noul | 74 | 0 | 0 | 0.09459 | 0.8723 |
| gemini | B1-noul | 74 | 0 | 0.06757 | 0.06757 | 0.9044 |
| jev | B1-noul | 74 | 0 | 1 | 1 | 0.8642 |
| clef | B1-score | 18 | 0 | 0.05556 | 0.1111 | 0.8515 |
| gemini | B1-score | 18 | 0 | 0 | 0 | 0.8384 |
| jev | B1-score | 18 | 0.6667 | 1 | 1 | 0.8611 |
| clef | B2 | 3423 | 0 | 0.006719 | 0.09173 | 0.7945 |
| gemini | B2 | 3423 | 0 | 0 | 0 | 0.8412 |
| jev | B2 | 3423 | 0.2194 | 1 | 1 | 0.8649 |

## errors

| run | model_key | attempted | ok | failed | refused | missing |
|---|---|---|---|---|---|---|
| A1 | clef | 1020 | 1020 | 0 | 0 | 0 |
| A1 | gemini | 1020 | 1020 | 0 | 0 | 0 |
| A1 | jev | 1020 | 1020 | 0 | 0 | 0 |
| A2 | clef | 1020 | 1020 | 0 | 0 | 0 |
| A2 | gemini | 1020 | 1020 | 0 | 0 | 0 |
| A2 | jev | 1020 | 1020 | 0 | 0 | 0 |
| A3-flipped | clef | 1020 | 1020 | 0 | 0 | 0 |
| A3-flipped | gemini | 1020 | 1020 | 0 | 0 | 0 |
| A3-flipped | jev | 1020 | 1020 | 0 | 0 | 0 |
| A3-paraphrase | clef | 1020 | 1020 | 0 | 0 | 0 |
| A3-paraphrase | gemini | 1020 | 1020 | 0 | 0 | 0 |
| A3-paraphrase | jev | 1020 | 1020 | 0 | 0 | 0 |
| A4 | clef | 300 | 300 | 0 | 0 | 0 |
| A4 | gemini | 300 | 300 | 0 | 0 | 0 |
| A4 | jev | 300 | 300 | 0 | 0 | 0 |
| B1 | clef | 231 | 231 | 0 | 0 | 0 |
| B1 | gemini | 231 | 231 | 0 | 0 | 0 |
| B1 | jev | 231 | 231 | 0 | 0 | 0 |
| B2 | clef | 3423 | 3423 | 0 | 0 | 0 |
| B2 | gemini | 3423 | 3423 | 0 | 0 | 0 |
| B2 | jev | 3423 | 3423 | 0 | 0 | 0 |
| B2L | clef | 200 | 200 | 0 | 0 | 0 |
| B2L | gemini | 200 | 200 | 0 | 0 | 0 |
| B2L | jev | 200 | 200 | 0 | 0 | 0 |
| B2P-aa | clef | 200 | 200 | 0 | 0 | 0 |
| B2P-aa | gemini | 200 | 200 | 0 | 0 | 0 |
| B2P-aa | jev | 200 | 200 | 0 | 0 | 0 |
| B2P-bare | clef | 200 | 200 | 0 | 0 | 0 |
| B2P-bare | gemini | 200 | 200 | 0 | 0 | 0 |
| B2P-bare | jev | 200 | 200 | 0 | 0 | 0 |
| B2P-minimal | clef | 200 | 200 | 0 | 0 | 0 |
| B2P-minimal | gemini | 200 | 200 | 0 | 0 | 0 |
| B2P-minimal | jev | 200 | 200 | 0 | 0 | 0 |
| B2P-numbered | clef | 200 | 200 | 0 | 0 | 0 |
| B2P-numbered | gemini | 200 | 200 | 0 | 0 | 0 |
| B2P-numbered | jev | 200 | 200 | 0 | 0 | 0 |
| C1 | gemini-direct | 200 | 200 | 0 | 0 | 0 |
| C2 | gemini | 100 | 100 | 0 | 0 | 0 |
| C2 | gemini-direct | 100 | 100 | 0 | 0 | 0 |
| SMOKE | clef | 30 | 30 | 0 | 0 | 0 |
| SMOKE | gemini | 30 | 30 | 0 | 0 | 0 |
| SMOKE | jev | 30 | 30 | 0 | 0 | 0 |

## b1_tiers

| model_key | tier | n | accuracy | accuracy_lo | accuracy_hi | chance | chance_corrected | brier | ece | decision_score | invalid | renormalized | unanswered | median_ms |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | easy | 48 | 1 | 0.9259 | 1 | 0.2844 | 1 | 0.0002039 | 0.01036 | 99.99 | 0 | 0 | 0 | 265 |
| clef | hard | 111 | 0.7748 | 0.6886 | 0.8425 | 0.3362 | 0.6607 | 0.3315 | 0.08937 | 81.9 | 0 | 0 | 0 | 325 |
| clef | original | 72 | 0.9861 | 0.9254 | 0.9975 | 0.3111 | 0.9798 | 0.01919 | 0.05645 | 98.81 | 0 | 0 | 0 | 303 |
| clef | all | 231 | 0.8874 | 0.8402 | 0.922 | 0.3176 | 0.8351 | 0.1653 | 0.04882 | 90.93 | 0 | 0 | 0 | 308 |
| gemini | easy | 48 | 1 | 0.9259 | 1 | 0.2844 | 1 | 0.0004708 | 0.007711 | 99.99 | 0 | 0 | 0 | 268 |
| gemini | hard | 111 | 0.8468 | 0.7684 | 0.9021 | 0.3362 | 0.7693 | 0.2369 | 0.04658 | 87.55 | 0 | 0 | 0 | 299 |
| gemini | original | 72 | 1 | 0.9493 | 1 | 0.3111 | 1 | 0.008865 | 0.03845 | 99.76 | 0 | 0 | 0 | 276.5 |
| gemini | all | 231 | 0.9264 | 0.8853 | 0.9535 | 0.3176 | 0.8922 | 0.1167 | 0.03518 | 93.94 | 0 | 0 | 0 | 287 |
| jev | easy | 48 | 1 | 0.9259 | 1 | 0.2844 | 1 | 0.0003542 | 0.005625 | 99.99 | 0 | 0 | 0 | 203 |
| jev | hard | 111 | 0.7748 | 0.6886 | 0.8425 | 0.3362 | 0.6607 | 0.2861 | 0.1032 | 82.96 | 0 | 0 | 0 | 211 |
| jev | original | 72 | 0.9861 | 0.9254 | 0.9975 | 0.3111 | 0.9798 | 0.02086 | 0.01597 | 98.78 | 0 | 0 | 0 | 201.5 |
| jev | all | 231 | 0.8874 | 0.8402 | 0.922 | 0.3176 | 0.8351 | 0.144 | 0.05515 | 91.43 | 0 | 0 | 0 | 207 |

## b1_between

| pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | interval_method | decision_score_diff | decision_score_diff_lo | decision_score_diff_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef_vs_gemini | 231 | 3 | 12 | 0.03516 | -0.03896 | -0.07359 | -0.008658 | bootstrap | -3.011 | -5.316 | -0.9044 |
| clef_vs_jev | 231 | 9 | 9 | 1 | 0 | -0.03463 | 0.03463 | bootstrap | -0.4987 | -2.832 | 1.752 |
| gemini_vs_jev | 231 | 12 | 3 | 0.03516 | 0.03896 | 0.008658 | 0.07359 | bootstrap | 2.512 | 0.4901 | 4.643 |

## b2_models

| model_key | n | accuracy | accuracy_lo | accuracy_hi | decision_score | missing | median_ms | usd_per_1000_decisions | by_category_accuracy_tool_call | by_category_accuracy_request_for_info | by_category_accuracy_cannot_answer | by_category_accuracy_direct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 3423 | 0.6959 | 0.6803 | 0.7111 | 75.83 | 0 | 309 | 0.2428 | 0.7429 | 0.9712 | 0.4718 |  |
| gemini | 3423 | 0.8124 | 0.799 | 0.8252 | 85.2 | 0 | 301 | 0.09698 | 0.9259 | 0.9592 | 0.6046 |  |
| jev | 3423 | 0.7935 | 0.7796 | 0.8067 | 83.07 | 0 | 201 | 0.05021 | 0.8849 | 0.9712 | 0.5876 |  |

## b2_between

| pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | interval_method | decision_score_diff | decision_score_diff_lo | decision_score_diff_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef_vs_gemini | 3423 | 123 | 522 | 2.178e-59 | -0.1166 | -0.1306 | -0.1025 | bootstrap | -9.37 | -10.32 | -8.441 |
| clef_vs_jev | 3423 | 129 | 463 | 4.123e-45 | -0.09758 | -0.1113 | -0.08414 | bootstrap | -7.234 | -8.174 | -6.307 |
| gemini_vs_jev | 3423 | 299 | 234 | 0.005519 | 0.01899 | 0.006135 | 0.03214 | bootstrap | 2.136 | 1.239 | 3.056 |

## route_identical

| rows | identical_share | mean_max_abs_difference | max_abs_difference | decision_flips | median_ms_openrouter | median_ms_direct | p95_ms_openrouter | p95_ms_direct |
|---|---|---|---|---|---|---|---|---|
| 100 | 1 | 0 | 0 | 0 | 289 | 355.5 | 463.9 | 542.1 |

## b2_presentation

| model_key | n | accuracy_labels_a_to_d | accuracy_named | named_only_correct | labels_only_correct | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | interval_method | decision_score_labels | decision_score_named |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 200 | 0.725 | 0.775 | 14 | 4 | 0.03088 | 0.05 | 0.01 | 0.09 | bootstrap | 77.66 | 81.44 |
| gemini | 200 | 0.82 | 0.875 | 13 | 2 | 0.007385 | 0.055 | 0.02 | 0.09 | bootstrap | 85.54 | 89.52 |
| jev | 200 | 0.815 | 0.835 | 5 | 1 | 0.2188 | 0.02 | -0.008474 | 0.02975 | exact | 84.64 | 85.74 |

## b2_presentation_between

| pair | presentation | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | interval_method |
|---|---|---|---|---|---|---|---|---|---|
| clef_vs_gemini | labels_a_to_d | 200 | 10 | 29 | 0.003378 | -0.095 | -0.155 | -0.035 | bootstrap |
| clef_vs_gemini | named | 200 | 8 | 28 | 0.001193 | -0.1 | -0.16 | -0.045 | bootstrap |
| clef_vs_gemini | change_in_gap | 200 |  |  |  | -0.005 | -0.06 | 0.05 | bootstrap |
| clef_vs_jev | labels_a_to_d | 200 | 7 | 25 | 0.002102 | -0.09 | -0.145 | -0.04 | bootstrap |
| clef_vs_jev | named | 200 | 9 | 21 | 0.04277 | -0.06 | -0.115 | -0.005 | bootstrap |
| clef_vs_jev | change_in_gap | 200 |  |  |  | 0.03 | -0.015 | 0.08 | bootstrap |
| gemini_vs_jev | labels_a_to_d | 200 | 14 | 13 | 1 | 0.005 | -0.045 | 0.055 | bootstrap |
| gemini_vs_jev | named | 200 | 14 | 6 | 0.1153 | 0.04 | -0.005 | 0.085 | bootstrap |
| gemini_vs_jev | change_in_gap | 200 |  |  |  | 0.035 | -0.005 | 0.075 | bootstrap |

## b2_presentations

| presentation | model_key | n | accuracy | accuracy_lo | accuracy_hi | decision_score | vs_letters_diff | vs_letters_lo | vs_letters_hi | vs_letters_p |
|---|---|---|---|---|---|---|---|---|---|---|
| letters | clef | 200 | 0.725 | 0.6593 | 0.7822 | 77.66 |  |  |  |  |
| letters | gemini | 200 | 0.82 | 0.7609 | 0.8671 | 85.54 |  |  |  |  |
| letters | jev | 200 | 0.815 | 0.7554 | 0.8627 | 84.64 |  |  |  |  |
| aa | clef | 200 | 0.73 | 0.6646 | 0.7868 | 78.9 | 0.005 | -0.035 | 0.05 | 1 |
| aa | gemini | 200 | 0.78 | 0.7176 | 0.8318 | 82.16 | -0.04 | -0.085 | 0.005 | 0.1153 |
| aa | jev | 200 | 0.82 | 0.7609 | 0.8671 | 85.2 | 0.005 | -0.00475 | 0.005 | 1 |
| bare | clef | 200 | 0.67 | 0.6022 | 0.7314 | 73.81 | -0.055 | -0.1 | -0.015 | 0.01921 |
| bare | gemini | 200 | 0.775 | 0.7123 | 0.8274 | 81.63 | -0.045 | -0.09 | -0.005 | 0.06357 |
| bare | jev | 200 | 0.79 | 0.7284 | 0.8407 | 82.89 | -0.025 | -0.06 | 0.005 | 0.2266 |
| minimal | clef | 200 | 0.665 | 0.597 | 0.7268 | 73.87 | -0.06 | -0.095 | -0.025 | 0.001831 |
| minimal | gemini | 200 | 0.835 | 0.7773 | 0.88 | 86.35 | 0.015 | -0.01467 | 0.03243 | 0.4531 |
| minimal | jev | 200 | 0.805 | 0.7446 | 0.8539 | 83.88 | -0.01 | -0.01975 | 0.01224 | 0.625 |
| numbered | clef | 200 | 0.71 | 0.6436 | 0.7685 | 77.01 | -0.015 | -0.03243 | 0.01467 | 0.4531 |
| numbered | gemini | 200 | 0.82 | 0.7609 | 0.8671 | 85.86 | 0 | -0.02291 | 0.02291 | 1 |
| numbered | jev | 200 | 0.81 | 0.75 | 0.8583 | 84.34 | -0.005 | -0.005 | 0.00475 | 1 |
| named | clef | 200 | 0.775 | 0.7123 | 0.8274 | 81.44 | 0.05 | 0.01 | 0.09 | 0.03088 |
| named | gemini | 200 | 0.875 | 0.822 | 0.9139 | 89.52 | 0.055 | 0.02 | 0.09 | 0.007385 |
| named | jev | 200 | 0.835 | 0.7773 | 0.88 | 85.74 | 0.02 | -0.008474 | 0.02975 | 0.2188 |

## b2_presentations_between

| presentation | pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | interval_method |
|---|---|---|---|---|---|---|---|---|---|
| letters | clef_vs_gemini | 200 | 10 | 29 | 0.003378 | -0.095 | -0.155 | -0.035 | bootstrap |
| letters | clef_vs_jev | 200 | 7 | 25 | 0.002102 | -0.09 | -0.145 | -0.04 | bootstrap |
| letters | gemini_vs_jev | 200 | 14 | 13 | 1 | 0.005 | -0.045 | 0.055 | bootstrap |
| aa | clef_vs_gemini | 200 | 10 | 20 | 0.09874 | -0.05 | -0.105 | 0 | bootstrap |
| aa | clef_vs_jev | 200 | 7 | 25 | 0.002102 | -0.09 | -0.145 | -0.04 | bootstrap |
| aa | gemini_vs_jev | 200 | 8 | 16 | 0.1516 | -0.04 | -0.09 | 0.005 | bootstrap |
| bare | clef_vs_gemini | 200 | 7 | 28 | 0.0005083 | -0.105 | -0.16 | -0.05 | bootstrap |
| bare | clef_vs_jev | 200 | 6 | 30 | 6.96e-05 | -0.12 | -0.175 | -0.065 | bootstrap |
| bare | gemini_vs_jev | 200 | 12 | 15 | 0.7011 | -0.015 | -0.065 | 0.035 | bootstrap |
| minimal | clef_vs_gemini | 200 | 7 | 41 | 6.24e-07 | -0.17 | -0.235 | -0.11 | bootstrap |
| minimal | clef_vs_jev | 200 | 5 | 33 | 4.256e-06 | -0.14 | -0.2 | -0.085 | bootstrap |
| minimal | gemini_vs_jev | 200 | 15 | 9 | 0.3075 | 0.03 | -0.02 | 0.08 | bootstrap |
| numbered | clef_vs_gemini | 200 | 9 | 31 | 0.0006795 | -0.11 | -0.17 | -0.05 | bootstrap |
| numbered | clef_vs_jev | 200 | 7 | 27 | 0.0008214 | -0.1 | -0.16 | -0.045 | bootstrap |
| numbered | gemini_vs_jev | 200 | 13 | 11 | 0.8388 | 0.01 | -0.04 | 0.055 | bootstrap |
| named | clef_vs_gemini | 200 | 8 | 28 | 0.001193 | -0.1 | -0.16 | -0.045 | bootstrap |
| named | clef_vs_jev | 200 | 9 | 21 | 0.04277 | -0.06 | -0.115 | -0.005 | bootstrap |
| named | gemini_vs_jev | 200 | 14 | 6 | 0.1153 | 0.04 | -0.005 | 0.085 | bootstrap |

## route

| rows | identical_share | mean_abs_difference | max_abs_difference | decision_flips | median_ms_openrouter | median_ms_direct |
|---|---|---|---|---|---|---|
| 200 | 0.185 | 0.01123 | 0.1484 | 0 | 293.5 | 287 |
