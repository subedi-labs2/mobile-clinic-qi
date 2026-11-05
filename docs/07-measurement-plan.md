# 07 — Measurement Plan

**Unit of analysis:** weekly, for run charts. **Data sources:** `screening_log.csv`, `referral_log.csv` ([data dictionary](../data/data-dictionary.md)).
**Analysis:** [`analysis/analyze.py`](../analysis/analyze.py).

## Measure set

| ID | Type | Measure | Numerator | Denominator | Target |
|---|---|---|---|---|---|
| **P1** | Process (primary) | Up-to-date screening rate | Adult visits where the patient has a **complete** screen at that visit **or** within the prior 90 days | All adult visits (incl. declines; excl. documented medical exclusions) | ≥ 80 % |
| **P1a** | Process | Due-screen completion | Visits where a screen was **due** and was completed at that visit | Visits where a screen was due (no complete screen in prior 90 days) | ≥ 80 % (pre/post; small n) |
| **P1b** | Process | Panel coverage | Patients with ≥ 1 complete screen to date (cumulative) | Patients seen to date | Monitor |
| **P2** | Process | Referral offer rate | Positive-screen visits where a referral was offered for **every** actionable positive domain\* | Visits with ≥ 1 actionable positive domain | ≥ 90 % |
| **P3** | Process | Referral acceptance | Referrals accepted | Referrals offered | Monitor (no target; autonomy) |
| **P4** | Process | Fidelity: safety items | Complete screens with safety answered privately | Complete screens | Monitor; reduce `deferred` |
| **O1** | Outcome | Follow-up documented | Accepted referrals with a follow-up status other than `pending` by day 30 | Accepted referrals with ≥ 30 days elapsed | ≥ 50 % |
| **O2** | Outcome | Connection rate | Accepted referrals with `connected` by day 30 | Accepted referrals with ≥ 30 days elapsed | Monitor (establish baseline) |
| **B1** | Balancing | Decline rate | Due visits where the patient declined | Visits where a screen was due | Monitor; investigate if > 20 % |
| **B2** | Balancing | Added visit time | Median screening minutes | Screens with time recorded | ≤ 8 min |
| **B3** | Balancing | Staff burden | Mean rating on "screening is manageable" (1–5) | Staff surveyed (start/end) | ≥ 3.5 |
| **D1** | Descriptive | Need prevalence by domain | Patients positive per domain | Patients with ≥ 1 complete screen | — |

\*Health literacy is **not** an actionable referral domain. Its response is clinical (teach-back), so it is excluded from P2.

### Why P1 is "up to date" rather than "screened at this visit"
With a panel of about 30 patients and a 90-day rescreening interval, most patients are *not due* at most visits once screening starts. A "screened this visit" rate would have weekly denominators of 0–3, too small for a run chart. P1 asks the question that matters for every visit: *does the care team know this patient's current social needs?* It keeps weekly denominators at the visit volume. P1a (did we screen when due?) is reported pre/post or biweekly. If the clinic actually sees about 30 **different** patients per session, P1a becomes plottable weekly. Confirm the panel size and visit volume.

## Baseline data collection
Baseline uses a chart audit of every adult visit during the baseline weeks. Count a visit as "screened" only if **all** core domains (housing, food, transportation, utilities or N/A, safety or deferred, health literacy, ID/documents) are documented. Partial screening is recorded in `notes` but counts as not complete. This matches the problem statement that questions vary by provider. Also record whether any single domain was asked, to describe how inconsistent the baseline is.

## Run chart rules (Perla, Provost & Murray 2011)
Plot the weekly percentage, with the centerline at the **baseline median**. A non-random signal is:
1. **Shift:** 6 or more consecutive points all above or all below the median. Points on the median don't count and don't break the run.
2. **Trend:** 5 or more consecutive points all going up or all going down. Repeated values don't count.
3. **Too few or too many runs:** compare against the Swed–Eisenhart table for the number of useful points.
4. **Astronomical point:** an obviously extreme value, judged visually.

Annotate each chart with the PDSA start dates. After a sustained shift, the median may be re-baselined.

**Why run charts and not p-values:** with about 30 patients and 10–20 visits a week, the data are too small and too autocorrelated for meaningful hypothesis tests. Run charts detect improvement over time, which is the standard approach for QI projects. Pre/post percentages are reported descriptively, with 95 % Wilson confidence intervals.

**Small weekly denominators:** if a week has fewer than 5 eligible visits, combine it with the next week or plot biweekly. The analysis script flags these weeks.

## Data quality
- Weekly: the project lead checks 100 % of logs against forms during PDSA 1, then a 20 % sample.
- Missing data: a screen with a missing core item counts as **incomplete**. Report the missing-data rate.
- The analysis script validates the schema and allowed values, and lists errors before computing measures.

## Stratification (if n allows)
Report by screener role, language, and sleeping location. This checks whether screening is consistent across groups, which is the core equity goal. With small numbers, report counts and avoid percentages for cells with n < 5.

## Reporting
- Weekly: run chart P1 (+ P2 after PDSA 2) posted for staff.
- End of project: all measures in a SQUIRE 2.0 report. The final run charts come from `analysis/analyze.py`.

## References
- Perla RJ, Provost LP, Murray SK. The run chart: a simple analytical tool for learning from variation in healthcare processes. *BMJ Qual Saf.* 2011;20(1):46-51.
- Langley GJ, Moen RD, Nolan KM, et al. *The Improvement Guide.* 2nd ed. Jossey-Bass; 2009.
- Ogrinc G, Davies L, Goodman D, et al. SQUIRE 2.0: revised publication guidelines from a detailed consensus process. *BMJ Qual Saf.* 2016;25(12):986-992.
