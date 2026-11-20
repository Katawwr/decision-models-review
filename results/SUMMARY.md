# Results

## accuracy

| model_key | n | correct | accuracy | accuracy_lo | accuracy_hi | misses | n_hijack | miss_rate | miss_lo | miss_hi | false_blocks | n_legit | false_block_rate | false_block_lo | false_block_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 1020 | 1017 | 0.9971 | 0.9914 | 0.999 | 2 | 441 | 0.004535 | 0.001245 | 0.01638 | 1 | 579 | 0.001727 | 0.0003049 | 0.009718 |
| gemini | 1020 | 1017 | 0.9971 | 0.9914 | 0.999 | 2 | 441 | 0.004535 | 0.001245 | 0.01638 | 1 | 579 | 0.001727 | 0.0003049 | 0.009718 |
| jev | 1020 | 1017 | 0.9971 | 0.9914 | 0.999 | 3 | 441 | 0.006803 | 0.002316 | 0.01981 | 0 | 579 | 0 | 0 | 0.006591 |

## accuracy_by_group

| model_key | group | n | wrong | wrong_rate | wrong_lo | wrong_hi | miss_rate | misses |
|---|---|---|---|---|---|---|---|---|
| clef | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 |
| clef | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 |
| clef | legitimate | 579 | 1 | 0.001727 | 0.0003049 | 0.009718 |  |  |
| gemini | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 |
| gemini | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 |
| gemini | legitimate | 579 | 1 | 0.001727 | 0.0003049 | 0.009718 |  |  |
| jev | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 |
| jev | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 |
| jev | legitimate | 579 | 0 | 0 | 0 | 0.006591 |  |  |

## operating_points

| model_key | max_false_block_rate | threshold | tune_false_block_rate | miss_rate | miss_lo | miss_hi | misses | n_hijack_report | false_block_rate | false_blocks | n_legit_report | false_block_lo | false_block_hi |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 0.01 | 0.6058 | 0.006803 | 0 | 0 | 0.0174 | 0 | 217 | 0.003509 | 1 | 285 | 0.0006196 | 0.0196 |
| clef | 0.05 | 0.8281 | 0.04762 | 0 | 0 | 0.0174 | 0 | 217 | 0.03158 | 9 | 285 | 0.0167 | 0.05892 |
| gemini | 0.01 | 0.5688 | 0.006803 | 0 | 0 | 0.0174 | 0 | 217 | 0.01053 | 3 | 285 | 0.003586 | 0.03049 |
| gemini | 0.05 | 0.8457 | 0.04762 | 0 | 0 | 0.0174 | 0 | 217 | 0.04912 | 14 | 285 | 0.02948 | 0.08076 |
| jev | 0.01 | 0.71 | 0.006803 | 0 | 0 | 0.0174 | 0 | 217 | 0.01404 | 4 | 285 | 0.005471 | 0.03553 |
| jev | 0.05 | 0.87 | 0.04422 | 0 | 0 | 0.0174 | 0 | 217 | 0.05263 | 15 | 285 | 0.03215 | 0.08501 |

## confidently_wrong

| model_key | legitimate_at_or_below_0.05 | hijack_at_or_above_0.95 | total |
|---|---|---|---|
| clef | 0 | 0 | 0 |
| gemini | 0 | 0 | 0 |
| jev | 0 | 1 | 1 |

## calibration

| model_key | n | brier | decision_score |
|---|---|---|---|
| clef | 1020 | 0.005944 | 99.56 |
| gemini | 1020 | 0.005378 | 99.58 |
| jev | 1020 | 0.005626 | 99.57 |

## margins

| model_key | legit_min_p | legit_p5 | hijack_max_p | hijack_p95 | hijack_at_or_above_0.2 | hijack_at_or_above_0.5 | informed_at_or_above_0.2 | informed_at_or_above_0.5 |
|---|---|---|---|---|---|---|---|---|
| clef | 0.4573 | 0.8347 | 0.886 | 0.0558 | 0.01587 | 0.004535 | 0.05 | 0.01667 |
| gemini | 0.4338 | 0.8457 | 0.9376 | 0.03171 | 0.00907 | 0.004535 | 0.03333 | 0.01667 |
| jev | 0.53 | 0.87 | 0.98 | 0.09 | 0.02494 | 0.006803 | 0.08333 | 0.01667 |

## rewording

| model_key | pair | n | flips | rows_changing | flip_share | flip_lo | flip_hi | mean_abs_change |
|---|---|---|---|---|---|---|---|---|
| clef | main_vs_paraphrase | 1020 | 3 | 3 | 0.002941 | 0.001001 | 0.008612 | 0.01114 |
| clef | main_vs_flipped | 1020 | 2 | 2 | 0.001961 | 0.0005379 | 0.007121 | 0.01327 |
| clef | paraphrase_vs_flipped | 1020 | 3 | 3 | 0.002941 | 0.001001 | 0.008612 | 0.01513 |
| clef | any_pair | 1020 | 4 | 4 | 0.003922 | 0.001526 | 0.01004 |  |
| gemini | main_vs_paraphrase | 1020 | 2 | 2 | 0.001961 | 0.0005379 | 0.007121 | 0.01025 |
| gemini | main_vs_flipped | 1020 | 5 | 5 | 0.004902 | 0.002096 | 0.01142 | 0.01691 |
| gemini | paraphrase_vs_flipped | 1020 | 3 | 3 | 0.002941 | 0.001001 | 0.008612 | 0.01363 |
| gemini | any_pair | 1020 | 5 | 5 | 0.004902 | 0.002096 | 0.01142 |  |
| jev | main_vs_paraphrase | 1020 | 4 | 4 | 0.003922 | 0.001526 | 0.01004 | 0.009971 |
| jev | main_vs_flipped | 1020 | 3 | 3 | 0.002941 | 0.001001 | 0.008612 | 0.01159 |
| jev | paraphrase_vs_flipped | 1020 | 3 | 3 | 0.002941 | 0.001001 | 0.008612 | 0.0126 |
| jev | any_pair | 1020 | 5 | 5 | 0.004902 | 0.002096 | 0.01142 |  |

## fooling

| model_key | group | n | wrong | wrong_rate | wrong_lo | wrong_hi | miss_rate | misses | view |
|---|---|---|---|---|---|---|---|---|---|
| clef | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 | B |
| clef | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 | B |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | B |
| clef | legitimate | 579 | 1 | 0.001727 | 0.0003049 | 0.009718 |  |  | B |
| gemini | hijack_plain | 281 | 0 | 0 | 0 | 0.01349 | 0 | 0 | B |
| gemini | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 | B |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | B |
| gemini | legitimate | 579 | 1 | 0.001727 | 0.0003049 | 0.009718 |  |  | B |
| jev | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 | B |
| jev | hijack_reviewer_informed | 120 | 2 | 0.01667 | 0.004582 | 0.05874 | 0.01667 | 2 | B |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | B |
| jev | legitimate | 579 | 0 | 0 | 0 | 0.006591 |  |  | B |
| clef | hijack_plain | 281 | 2 | 0.007117 | 0.001954 | 0.02558 | 0.007117 | 2 | A |
| clef | hijack_reviewer_informed | 120 | 12 | 0.1 | 0.05813 | 0.1667 | 0.1 | 12 | A |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | A |
| clef | legitimate | 579 | 7 | 0.01209 | 0.005868 | 0.02474 |  |  | A |
| gemini | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 | A |
| gemini | hijack_reviewer_informed | 120 | 4 | 0.03333 | 0.01304 | 0.08258 | 0.03333 | 4 | A |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | A |
| gemini | legitimate | 579 | 35 | 0.06045 | 0.04378 | 0.08291 |  |  | A |
| jev | hijack_plain | 281 | 1 | 0.003559 | 0.0006285 | 0.01988 | 0.003559 | 1 | A |
| jev | hijack_reviewer_informed | 120 | 9 | 0.075 | 0.03996 | 0.1364 | 0.075 | 9 | A |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0.08762 | 0 | 0 | A |
| jev | legitimate | 579 | 4 | 0.006908 | 0.00269 | 0.01763 |  |  | A |

## determinism

| model_key | rows | identical_share | max_abs_difference | mean_abs_difference |
|---|---|---|---|---|
| clef | 100 | 1 | 0 | 0 |
| gemini | 100 | 1 | 0 | 0 |
| jev | 100 | 0.54 | 0.08 | 0.0069 |

## speed

| model_key | run | n | median_ms | p95_ms | mean_ms |
|---|---|---|---|---|---|
| clef | A1 | 1020 | 303 | 817.5 | 411.6 |
| gemini | A1 | 1020 | 289 | 530 | 341.3 |
| jev | A1 | 1020 | 205 | 264 | 213 |
| clef | A2 | 1020 | 268 | 717 | 350.3 |
| gemini | A2 | 1020 | 284.5 | 523 | 337.7 |
| jev | A2 | 1020 | 184 | 234 | 192.2 |
| clef | A3-paraphrase | 1020 | 287 | 815.2 | 379.5 |
| gemini | A3-paraphrase | 1020 | 282 | 530 | 341.4 |
| jev | A3-paraphrase | 1020 | 194 | 244 | 197.8 |
| clef | A3-flipped | 1020 | 291 | 671 | 359.7 |
| gemini | A3-flipped | 1020 | 299 | 533 | 351.3 |
| jev | A3-flipped | 1020 | 213 | 272 | 218.9 |
| clef | pooled | 4080 | 288 | 754 | 375.3 |
| gemini | pooled | 4080 | 290 | 530 | 342.9 |
| jev | pooled | 4080 | 199 | 256 | 205.5 |

## cost

| model_key | n_calls | usd_per_1000_decisions | mean_input_tokens | usd_per_1000_at_openrouter_list | usd_per_1000_at_first_party_list |
|---|---|---|---|---|---|
| clef | 4080 | 0.09143 | 380.9 | 0.07314 | 0.09143 |
| gemini | 4080 | 0.03714 | 371.4 | 0.03714 | 0.03714 |
| jev | 4080 | 0.02298 | 547.2 | 0.02298 | 0.02298 |

## tokens

| model_key | reference | n | mean_input_tokens | min_input_tokens | max_input_tokens | slope_vs_reference | intercept_vs_reference | r2_vs_reference |
|---|---|---|---|---|---|---|---|---|
| clef | gemini | 1020 | 403 | 319 | 491 | 0.9833 | 14.83 | 0.9897 |
| gemini | gemini | 1020 | 394.8 | 309 | 479 |  |  |  |
| jev | gemini | 1020 | 569.4 | 484 | 661 | 1.006 | 172.1 | 0.9869 |

## between_models

| pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | miss_rate_diff | miss_rate_diff_lo | miss_rate_diff_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| clef_vs_gemini | 1020 | 2 | 2 | 1 | 0 | -0.003922 | 0.003922 | 0 | -0.006803 | 0.006803 |
| clef_vs_jev | 1020 | 1 | 1 | 1 | 0 | -0.002941 | 0.002941 | -0.002268 | -0.006803 | 0 |
| gemini_vs_jev | 1020 | 2 | 2 | 1 | 0 | -0.003922 | 0.003922 | -0.002268 | -0.01134 | 0.004535 |

## between_models_views

| run | subset | pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi |
|---|---|---|---|---|---|---|---|---|---|
| A1 | all | clef_vs_gemini | 1020 | 2 | 2 | 1 | 0 | -0.003922 | 0.003922 |
| A1 | all | clef_vs_jev | 1020 | 1 | 1 | 1 | 0 | -0.002941 | 0.002941 |
| A1 | all | gemini_vs_jev | 1020 | 2 | 2 | 1 | 0 | -0.003922 | 0.003922 |
| A1 | legitimate | clef_vs_gemini | 579 | 1 | 1 | 1 | 0 | -0.005181 | 0.005181 |
| A1 | legitimate | clef_vs_jev | 579 | 0 | 1 | 1 | -0.001727 | -0.005181 | 0 |
| A1 | legitimate | gemini_vs_jev | 579 | 0 | 1 | 1 | -0.001727 | -0.005181 | 0 |
| A1 | hijack_plain | clef_vs_gemini | 281 | 0 | 0 | 1 | 0 | 0 | 0 |
| A1 | hijack_plain | clef_vs_jev | 281 | 1 | 0 | 1 | 0.003559 | 0 | 0.01068 |
| A1 | hijack_plain | gemini_vs_jev | 281 | 1 | 0 | 1 | 0.003559 | 0 | 0.01068 |
| A1 | hijack_reviewer_naive | clef_vs_gemini | 40 | 0 | 0 | 1 | 0 | 0 | 0 |
| A1 | hijack_reviewer_naive | clef_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 |
| A1 | hijack_reviewer_naive | gemini_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 |
| A1 | hijack_reviewer_informed | clef_vs_gemini | 120 | 1 | 1 | 1 | 0 | -0.025 | 0.025 |
| A1 | hijack_reviewer_informed | clef_vs_jev | 120 | 0 | 0 | 1 | 0 | 0 | 0 |
| A1 | hijack_reviewer_informed | gemini_vs_jev | 120 | 1 | 1 | 1 | 0 | -0.025 | 0.025 |
| A2 | all | clef_vs_gemini | 1020 | 32 | 13 | 0.006609 | 0.01863 | 0.005882 | 0.03137 |
| A2 | all | clef_vs_jev | 1020 | 7 | 14 | 0.1892 | -0.006863 | -0.01569 | 0.001961 |
| A2 | all | gemini_vs_jev | 1020 | 10 | 36 | 0.0001564 | -0.02549 | -0.03824 | -0.01275 |
| A2 | legitimate | clef_vs_gemini | 579 | 32 | 4 | 1.942e-06 | 0.04836 | 0.02936 | 0.06908 |
| A2 | legitimate | clef_vs_jev | 579 | 4 | 7 | 0.5488 | -0.005181 | -0.01727 | 0.005181 |
| A2 | legitimate | gemini_vs_jev | 579 | 4 | 35 | 3.353e-07 | -0.05354 | -0.07427 | -0.03282 |
| A2 | hijack_plain | clef_vs_gemini | 281 | 0 | 1 | 1 | -0.003559 | -0.01068 | 0 |
| A2 | hijack_plain | clef_vs_jev | 281 | 0 | 1 | 1 | -0.003559 | -0.01068 | 0 |
| A2 | hijack_plain | gemini_vs_jev | 281 | 0 | 0 | 1 | 0 | 0 | 0 |
| A2 | hijack_reviewer_naive | clef_vs_gemini | 40 | 0 | 0 | 1 | 0 | 0 | 0 |
| A2 | hijack_reviewer_naive | clef_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 |
| A2 | hijack_reviewer_naive | gemini_vs_jev | 40 | 0 | 0 | 1 | 0 | 0 | 0 |
| A2 | hijack_reviewer_informed | clef_vs_gemini | 120 | 0 | 8 | 0.007812 | -0.06667 | -0.1167 | -0.025 |
| A2 | hijack_reviewer_informed | clef_vs_jev | 120 | 3 | 6 | 0.5078 | -0.025 | -0.075 | 0.025 |
| A2 | hijack_reviewer_informed | gemini_vs_jev | 120 | 6 | 1 | 0.125 | 0.04167 | 0 | 0.09167 |

## view_change

| model_key | group | n | wrong_view_b | wrong_view_a | improved | worsened | mcnemar_p | wrong_rate_diff | wrong_rate_diff_lo | wrong_rate_diff_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| clef | all | 1020 | 3 | 21 | 1 | 19 | 4.005e-05 | 0.01765 | 0.009804 | 0.02647 |
| clef | hijack_plain | 281 | 0 | 2 | 0 | 2 | 0.5 | 0.007117 | 0 | 0.01779 |
| clef | hijack_reviewer_informed | 120 | 2 | 12 | 0 | 10 | 0.001953 | 0.08333 | 0.04167 | 0.1333 |
| clef | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| clef | legitimate | 579 | 1 | 7 | 1 | 7 | 0.07031 | 0.01036 | 0.001727 | 0.02073 |
| gemini | all | 1020 | 3 | 40 | 3 | 40 | 3.021e-09 | 0.03627 | 0.02451 | 0.04902 |
| gemini | hijack_plain | 281 | 0 | 1 | 0 | 1 | 1 | 0.003559 | 0 | 0.01068 |
| gemini | hijack_reviewer_informed | 120 | 2 | 4 | 2 | 4 | 0.6875 | 0.01667 | -0.025 | 0.05833 |
| gemini | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| gemini | legitimate | 579 | 1 | 35 | 1 | 35 | 1.077e-09 | 0.05872 | 0.03972 | 0.07945 |
| jev | all | 1020 | 3 | 14 | 2 | 13 | 0.007385 | 0.01078 | 0.003922 | 0.01863 |
| jev | hijack_plain | 281 | 1 | 1 | 1 | 1 | 1 | 0 | -0.01068 | 0.01068 |
| jev | hijack_reviewer_informed | 120 | 2 | 9 | 1 | 8 | 0.03906 | 0.05833 | 0.01667 | 0.1083 |
| jev | hijack_reviewer_naive | 40 | 0 | 0 | 0 | 0 | 1 | 0 | 0 | 0 |
| jev | legitimate | 579 | 0 | 4 | 0 | 4 | 0.125 | 0.006908 | 0.001727 | 0.01382 |

## operating_points_crossfit

| model_key | max_false_block_rate | threshold_tune_fit | threshold_report_fit | misses_on_tune | n_hijack_tune | miss_rate_on_tune | false_block_rate_on_tune | hijacks_at_or_above_tune_threshold_all | of_which_in_tune_half | n_hijack_all |
|---|---|---|---|---|---|---|---|---|---|---|
| clef | 0.01 | 0.6058 | 0.7691 | 1 | 224 | 0.004464 | 0.02381 | 2 | 2 | 441 |
| clef | 0.05 | 0.8281 | 0.847 | 1 | 224 | 0.004464 | 0.07483 | 1 | 1 | 441 |
| gemini | 0.01 | 0.5688 | 0.5648 | 1 | 224 | 0.004464 | 0.006803 | 1 | 1 | 441 |
| gemini | 0.05 | 0.8457 | 0.8496 | 1 | 224 | 0.004464 | 0.05102 | 1 | 1 | 441 |
| jev | 0.01 | 0.71 | 0.67 | 1 | 224 | 0.004464 | 0.006803 | 1 | 1 | 441 |
| jev | 0.05 | 0.87 | 0.86 | 1 | 224 | 0.004464 | 0.04082 | 1 | 1 | 441 |

## quantisation

| model_key | run | n | share_exactly_0_or_1 | share_on_0_01_grid | share_on_0_001_grid | mean_top_p |
|---|---|---|---|---|---|---|
| clef | A1 | 1020 | 0 | 0.007843 | 0.1078 | 0.9551 |
| gemini | A1 | 1020 | 0 | 0.2059 | 0.2059 | 0.9623 |
| jev | A1 | 1020 | 0 | 1 | 1 | 0.9627 |
| clef | A2 | 1020 | 0 | 0.01275 | 0.1235 | 0.9335 |
| gemini | A2 | 1020 | 0 | 0.1167 | 0.1167 | 0.8785 |
| jev | A2 | 1020 | 0 | 1 | 1 | 0.9146 |
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

| pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | decision_score_diff | decision_score_diff_lo | decision_score_diff_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| clef_vs_gemini | 231 | 3 | 12 | 0.03516 | -0.03896 | -0.07359 | -0.008658 | -3.011 | -5.316 | -0.9044 |
| clef_vs_jev | 231 | 9 | 9 | 1 | 0 | -0.03463 | 0.03463 | -0.4987 | -2.832 | 1.752 |
| gemini_vs_jev | 231 | 12 | 3 | 0.03516 | 0.03896 | 0.008658 | 0.07359 | 2.512 | 0.4901 | 4.643 |

## b2_models

| model_key | n | accuracy | accuracy_lo | accuracy_hi | decision_score | missing | median_ms | usd_per_1000_decisions | by_category_accuracy_tool_call | by_category_accuracy_request_for_info | by_category_accuracy_cannot_answer | by_category_accuracy_direct |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 3423 | 0.6959 | 0.6803 | 0.7111 | 75.83 | 0 | 309 | 0.2428 | 0.7429 | 0.9712 | 0.4718 |  |
| gemini | 3423 | 0.8124 | 0.799 | 0.8252 | 85.2 | 0 | 301 | 0.09698 | 0.9259 | 0.9592 | 0.6046 |  |
| jev | 3423 | 0.7935 | 0.7796 | 0.8067 | 83.07 | 0 | 201 | 0.05021 | 0.8849 | 0.9712 | 0.5876 |  |

## b2_between

| pair | n | a_only | b_only | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | decision_score_diff | decision_score_diff_lo | decision_score_diff_hi |
|---|---|---|---|---|---|---|---|---|---|---|
| clef_vs_gemini | 3423 | 123 | 522 | 2.178e-59 | -0.1166 | -0.1306 | -0.1025 | -9.37 | -10.32 | -8.441 |
| clef_vs_jev | 3423 | 129 | 463 | 4.123e-45 | -0.09758 | -0.1113 | -0.08414 | -7.234 | -8.174 | -6.307 |
| gemini_vs_jev | 3423 | 299 | 234 | 0.005519 | 0.01899 | 0.006135 | 0.03214 | 2.136 | 1.239 | 3.056 |

## route_identical

| rows | identical_share | mean_max_abs_difference | max_abs_difference | decision_flips | median_ms_openrouter | median_ms_direct | p95_ms_openrouter | p95_ms_direct |
|---|---|---|---|---|---|---|---|---|
| 100 | 1 | 0 | 0 | 0 | 289 | 355.5 | 463.9 | 542.1 |

## b2_presentation

| model_key | n | accuracy_labels_a_to_d | accuracy_named | named_only_correct | labels_only_correct | mcnemar_p | accuracy_diff | accuracy_diff_lo | accuracy_diff_hi | decision_score_labels | decision_score_named |
|---|---|---|---|---|---|---|---|---|---|---|---|
| clef | 200 | 0.725 | 0.775 | 14 | 4 | 0.03088 | 0.05 | 0.01 | 0.09 | 77.66 | 81.44 |
| gemini | 200 | 0.82 | 0.875 | 13 | 2 | 0.007385 | 0.055 | 0.02 | 0.09 | 85.54 | 89.52 |
| jev | 200 | 0.815 | 0.835 | 5 | 1 | 0.2188 | 0.02 | 0 | 0.045 | 84.64 | 85.74 |

## route

| rows | identical_share | mean_abs_difference | max_abs_difference | decision_flips | median_ms_openrouter | median_ms_direct |
|---|---|---|---|---|---|---|
| 200 | 0.185 | 0.01123 | 0.1484 | 0 | 293.5 | 287 |
