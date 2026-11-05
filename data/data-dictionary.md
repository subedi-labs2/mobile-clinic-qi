# Data Dictionary

Two CSV logs with one shared schema. They are used for synthetic data (`data/synthetic/`), blank templates (`data/templates/`), and real coded data (`data/real/`, **git-ignored, never commit**).

**No direct identifiers in these files:** no names, DOB, addresses, phone numbers, or free-text clinical detail. `patient_id` is a study code (e.g., `P001`). The linking key stays at the clinic. Real logs are still **PHI** because they contain dates of service. See [08 §2](../docs/08-ethics-privacy.md) before any data leaves the clinic.

## `screening_log.csv` — one row per adult visit

| Field | Type | Allowed values | Notes |
|---|---|---|---|
| `visit_id` | text | unique, e.g. `V0001` | |
| `patient_id` | text | e.g. `P001` | Study code |
| `visit_date` | date | `YYYY-MM-DD` | HIPAA date element; see 08 §2 before sharing |
| `week` | int | 1..N | Project week (week 1 = first baseline week); derived from dates, so still a date element |
| `phase` | text | `baseline`, `pdsa1`, `pdsa2`, `pdsa3`, `sustain` | |
| `excluded` | Y/N | `Y`, `N` | Y = medical/unable; removed from denominators |
| `exclusion_reason` | text | blank, `medical_unstable`, `unable_to_participate` | Required if `excluded = Y` |
| `screen_status` | text | `complete`, `partial`, `declined`, `not_screened`, `not_due` | `not_due` = complete screen within prior 90 days |
| `screener_role` | text | `MA`, `RN`, `CHW`, `clinician`, `volunteer`, blank | Blank if not screened |
| `language` | text | `en`, `es`, `other` | |
| `minutes` | int | blank or ≥ 0 | Time to administer (balancing B2) |
| `housing_status` | text | `steady`, `at_risk`, `unstable`, blank | Q1 |
| `sleep_location` | text | `unsheltered`, `vehicle`, `shelter`, `doubled_up`, `motel`, `own_place`, `other`, blank | Q1a |
| `housing_quality_pos` | text | `Y`, `N`, `NA`, blank | Q2; `NA` if no steady place |
| `food_pos` | text | `Y`, `N`, blank | Q3–4 |
| `transport_pos` | text | `Y`, `N`, blank | Q5 |
| `utilities_pos` | text | `Y`, `N`, `NA`, blank | Q6; `NA` if no steady place |
| `safety_pos` | text | `Y`, `N`, `deferred`, blank | Q7–10 sum ≥ 11 |
| `literacy_pos` | text | `Y`, `N`, blank | Q11 (clinical response, not a referral) |
| `id_docs_pos` | text | `Y`, `N`, blank | Q12 |
| `notes` | text | short, **no identifiers or clinical detail** | e.g. `baseline: food asked only` |

Domain fields are filled when `screen_status` is `complete` or `partial`. During baseline, `partial` records which domains happened to be asked.

## `referral_log.csv` — one row per domain referral offered

| Field | Type | Allowed values | Notes |
|---|---|---|---|
| `referral_id` | text | unique, e.g. `R0001` | |
| `visit_id` | text | must exist in screening log | |
| `patient_id` | text | | |
| `referral_date` | date | `YYYY-MM-DD` | |
| `domain` | text | `housing`, `food`, `transportation`, `utilities`, `safety`, `id_docs` | Housing quality → `housing` |
| `accepted` | Y/N | `Y`, `N` | N = offered, patient declined |
| `referral_type` | text | `warm_handoff`, `direct_referral`, `information_only` | |
| `resource` | text | short name from the [resource directory](../docs/04-resource-directory.md) | e.g. `WFCM`, `CSP` |
| `followup_date` | date | blank or `YYYY-MM-DD` | |
| `followup_status` | text | `pending`, `connected`, `not_connected`, `unable_to_reach`, `declined_followup` | |

Every row is an *offered* referral. "Offered for every actionable positive domain" (P2) is checked by matching domains to the visit's positive screen fields.

## Derived variables (computed in `analysis/analyze.py`)
- `housing_pos` = `housing_status` ∈ {`at_risk`, `unstable`}
- `due` = no `complete` screen for that patient in the 90 days before `visit_date`
- `up_to_date` = `complete` at this visit, or a `complete` screen within the prior 90 days
- `actionable_positive_domains` = positive among housing (status or quality), food, transportation, utilities, safety, id_docs
