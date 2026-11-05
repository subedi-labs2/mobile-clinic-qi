# 03 — Screening Protocol (Standard Operating Procedure)

**Purpose:** Every eligible patient is screened the same way, and every positive screen gets the same response.

## 1. Eligibility
| Rule | Definition |
|---|---|
| Logged visit | Every visit by a patient ≥ 18 for any clinical encounter. Log **all** adult visits, not only screened ones, because they form the denominator for P1. |
| Screen **due** | No complete screen in the prior **90 days** |
| Screen not due | Record `screen_status = not_due`. The visit still counts toward P1 (up to date). |
| Excluded from denominator | Patient medically unstable / transferred to ED; patient unable to participate (e.g., acute intoxication, severe distress). *Document the reason and retry at the next visit.* |
| Patient declines | **Stays in the denominator** (counts as not screened) but is recorded as `declined`. Decline rate is a balancing measure. |

*Why 90 days:* living situation and needs change quickly in this population. Annual rescreening (common in primary care) would miss changes. Adjust the interval if the clinic's visit frequency differs.

## 2. Roles
| Step | Primary | Backup |
|---|---|---|
| Check whether screen is due | Intake/registration staff | Screening champion |
| Administer screen | MA / RN / CHW (trained) | Clinician |
| Review positives + ask desire for help | Person who screened | Clinician |
| Warm handoff / referral | Referral owner (CHW / case manager) | Screener |
| Safety-positive response | Clinician (licensed) | Clinic lead |
| 30-day follow-up | Referral owner | Screening champion |
| Data entry (logs) | Screener (same day) | Project lead (weekly audit) |

## 3. Workflow

```
Arrival --> Intake: screen due? (log / flag)
               | no -------------------------------> usual visit
               | yes
               v
         Private space available? (needed for safety items Q7-Q10; if not, mark deferred)
               |
               v
     Administer Q1–Q14 (read aloud)  -- patient declines -> record "declined", offer resource card
               |
               v
     Score domains (paper key)
               |
     +---------+----------+
  No positives        ≥1 positive
     |                    |
  Thank patient     Ask desire for help (Q13)
     |                    |
     |        +-----------+----------+
     |     Wants help           Declines help
     |        |                      |
     |  Referral per domain     Give resource card,
     |  (warm handoff if        document "offered, declined"
     |   possible, else
     |   written + call)
     |        |
     |  Record referral log + contact method (Q14)
     |        |
     +--------+--> Clinician reviews results during visit (literacy → teach-back)
                         |
                         v
                 30-day follow-up (§7)
```

## 4. Administration standards
- Read questions **exactly as written**, without paraphrasing the scored items. A brief clarification is OK after the scripted question.
- Use a professional interpreter (phone/video) for non-English speakers. Do not use family or friends as interpreters for safety items.
- Use the intro script from [02](02-screening-questionnaire.md).
- Record answers on the paper form, then transcribe to the screening log the same day.

## 5. Responding to positive screens (non-safety)

| Domain | First-line response | Referral target (see [04](04-resource-directory.md)) |
|---|---|---|
| Housing: unsheltered / shelter / vehicle | Warm call to shelter intake / Coordinated Entry; hypothermia program Dec–Mar | Fairfax OPEH / shelters / Hypothermia Prevention Program |
| Housing: at risk of losing housing | Eviction-prevention referral | Coordinated Services Planning (CSP) |
| Housing quality | Referral to CSP | CSP |
| Food | Same-day food if available; pantry referral; SNAP application help | WFCM; DFS (SNAP) |
| Transportation | NEMT info if Medicaid; reduced-fare programs | Cardinal Care NEMT; TOPS / TRIP |
| Utilities | Energy assistance referral | DFS Energy Assistance; CSP |
| Health literacy | **Clinical response:** teach-back, verbal instructions, pictograms, plain-language handouts | (no external referral) |
| ID/documents | Help with application; fee-waiver eligibility | VA DMV / Vital Records (free if < 21 and homeless); CSP |

**Referral types (record one):** `warm_handoff` (staff calls or introduces the patient during the visit), `direct_referral` (staff sends the referral), `information_only` (written resource given).

## 6. Safety pathway (HITS ≥ 11, or any disclosure of current danger)
1. Thank the patient for sharing. Make sure the patient is in a private space.
2. Clinician assesses **immediate danger**. If the patient is in imminent danger, call **911**.
3. Offer the **Fairfax County Domestic and Sexual Violence 24-Hour Hotline: 703-360-7273 (TTY 711)**. Offer to call with the patient.
4. Do **not** give written materials that could put the patient at risk if found. Ask first.
5. **Mandatory reporting:** Virginia requires certain professionals to report suspected abuse, neglect, or exploitation of adults aged 60+ or incapacitated adults to Adult Protective Services (Va. Code § 63.2-1606). **Confirm reporting obligations with the clinic's compliance lead before go-live** (see [08](08-ethics-privacy.md)).
6. Document per clinic policy in the clinical record. Record only `safety_positive = Y` and the referral in the QI log, with no narrative detail.

## 7. Follow-up (closed loop)
- At **14 ± 7 days**, and again by **30 days** if needed, the referral owner contacts the patient using the Q14 method (phone, shelter or case manager, or the next clinic stop).
- Ask: "Were you able to connect with ___? Did you get what you needed?"
- Record the `followup_status`: `connected`, `not_connected`, `unable_to_reach`, `declined_followup`, or `pending`.
- If the patient was not connected, re-refer or remove the barrier, for example with a bus fare or a call made together.

## 8. Rescreening
- Rescreen every 90 days, or sooner if the patient reports a major change (eviction, new shelter, safety event).

## 9. Documentation
| What | Where (paper-first) | Phase 2 |
|---|---|---|
| Completed form | Locked binder / scanned to chart | EHR flowsheet |
| Screening log | `screening_log.csv` (coded with study ID) | Export |
| Referral log | `referral_log.csv` | Closed-loop referral platform |
| Study ID ↔ patient key | **Separate, locked**, held by clinic only | — |
