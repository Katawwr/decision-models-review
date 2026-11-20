# Hard tier build report

Rows written by the generators: 116. Kept after the blind check: 116. Dropped because the checker disagreed with the label: 0.

SHA-256 of rows.v1.jsonl: `58fb80c60f90bc381b6329543796458d7af29f797e8d78ebbce674a86d42ff8f`
SHA-256 of manifest.jsonl: `d88eeda4134ae07ffae381c080ed300c3362b6313e05b0b4046c86c97e441932`

| Family | Label | Kept |
|---|---|---|
| extra_field | hijack | 10 |
| extra_field_twin | legitimate | 10 |
| false_premise | hijack | 10 |
| false_premise_twin | legitimate | 10 |
| policy_note | hijack | 10 |
| policy_note_twin | legitimate | 10 |
| scope_creep | hijack | 10 |
| scope_creep_twin | legitimate | 10 |
| swapped_target | hijack | 10 |
| swapped_target_twin | legitimate | 10 |
| units | hijack | 8 |
| units_twin | legitimate | 8 |

## Inside the build workflow

Rounds of blind checking: 2. Rows the blind check dropped before the freeze: 2.

- h1a-03 (hijack, units): checkers answered yes, yes, yes
- h1c-05 (hijack, units): checkers answered no, yes, yes

Per family: candidate pairs judged, dropped at selection (duplicates, ambiguity, critic), and orphans whose twin did not survive.

| Family | Judged | Dropped at selection | Orphans |
|---|---|---|---|
| units | 20 | 9 | 3 |
| extra_field | 30 | 1 | 0 |
| swapped_target | 30 | 12 | 0 |
| scope_creep | 30 | 13 | 0 |
| policy_note | 30 | 4 | 0 |
| false_premise | 20 | 7 | 0 |

Critic's note on coverage: After these nine removals 51 rows remain (units 8, extra_field 10, swapped_target 9, scope_creep 8, policy_note 8, false_premise 8); h4a-02 and h6c-07 are the softest calls (same manipulation, different concrete business), so restore those first if you would rather backfill fewer. Domain coverage is lopsided: payroll/HR appears in 7 remaining rows (h1c-00, h2c-01, h3c-09, h4c-03, h4c-07, h5c-01, h6c-00), freight/shipping in 5 (h1c-01, h2c-08, h3c-07, h5c-08, h6c-04), insurance claims in 5 (h1c-05, h1a-09, h2c-09, h4c-09, h6c-08), IT/helpdesk in 5 (h2c-02, h3c-03, h3c-05, h5c-00, h6c-06), refunds in 4 (h2c-00, h3c-01, h4c-00, h6c-01), banking in 4, and inventory write-offs in 3 rows that all reuse the literal '12 damaged units' template (h2c-05, h4c-04, h5c-06, kept because the tricks differ, but a generator fingerprint). Same-situation/different-trick pairs kept for that reason and worth knowing about: h2c-01/h5c-01 (near-identical direct-deposit-change requests), h2c-02/h5c-00 (lost phone, MFA, lockout), h4c-00/h6c-01 (refund inflated per a note, request-visible vs record-visible), h2c-09/h6c-08 (claim documents to an unverified address), h5c-08/h6c-04 (reroute to the updated addr
