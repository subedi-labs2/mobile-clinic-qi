# 10 — Real Data Plan: Replacing the Synthetic Data

> This is planning guidance, **not legal advice**. Confirm each step with the faculty advisor, the school's IRB, and the clinic's privacy officer. Contacts were checked against public websites and directories in November 2026. Confirm them before use.

## 1. What "real data" means for this project
The screening and referral logs this project measures **do not exist yet**, so no one can send them. They are created when a clinic uses the protocol. Public data can describe the community, but it cannot measure this clinic's screening or referral rates (P1–P4 in [07](07-measurement-plan.md)).

| Data | Exists today? | How to get it | Replaces synthetic data? |
|---|---|---|---|
| Screening and referral logs | No. Created by running the protocol | Clinic partner + approvals (§2) | **Yes** |
| Baseline chart audit | Yes, in the clinic's records | Clinic partner + approvals (§2) | **Yes** (baseline weeks) |
| Public aggregate data (homeless count, health centers, food insecurity) | Yes | Download (§4) | No. Background, comparison, and simulation inputs only |
| Resource directory checks | Can be collected now | Phone calls (§7) | No. Supports [03](03-screening-protocol.md) and [04](04-resource-directory.md) |

## 2. Path to real clinic data
Do not open patient records until steps 1–5 are done.

| # | Step | Who | Result | See |
|---|---|---|---|---|
| 1 | Find a clinic partner and sponsor | Student | Letter or email of support | §5, Template A |
| 2 | Advisor approves the plan | Faculty advisor | Approval | [00](00-project-charter.md), [06](06-implementation-plan.md) |
| 3 | QI vs. research determination | School IRB | Determination letter or IRB approval | [08 §1](08-ethics-privacy.md) |
| 4 | Clinic onboarding | Clinic HR or compliance | Student or volunteer agreement, HIPAA training, confidentiality agreement | [08 §2](08-ethics-privacy.md) |
| 5 | Choose how data leaves the clinic | Clinic privacy officer | Written choice of route (§3) | [08 §2](08-ethics-privacy.md) |
| 6 | Adapt and verify materials | Student and sponsor | Resource directory verified; safety pathway signed off | [03](03-screening-protocol.md), [04](04-resource-directory.md) |
| 7 | Baseline chart audit (weeks 1–4) | Student, on clinic systems | Baseline rows in `screening_log.csv` | [07](07-measurement-plan.md) |
| 8 | Go live with PDSA cycles | Clinic staff | Screening and referral logs, collected as visits happen | [06](06-implementation-plan.md) |
| 9 | Analyze and report | Student or clinic staff | Aggregate results only | §3 |

Steps 1–5 can take weeks to months. Start partner calls and the IRB question early.

## 3. Handling the real data
**Coded logs are not de-identified.** They contain dates of service, so they are PHI under HIPAA even without names. Pick one route with the privacy officer ([08 §2](08-ethics-privacy.md)):

| Route | Who handles row-level data | Paperwork | What leaves the clinic |
|---|---|---|---|
| 1. Analyze on site | Student, as a clinic workforce member, on clinic-controlled storage | Student or volunteer agreement; HIPAA training | Aggregate results |
| 2. Clinic runs the analysis | Clinic staff only | Privacy officer reviews outputs | Aggregate results |
| 3. Limited Data Set | Student, off site | Data Use Agreement | Coded logs with dates |

Run the analysis on the approved machine:

```bash
mkdir -p data/real                    # git-ignored
cp data/templates/*.csv data/real/    # blank logs with the right headers (or save clinic exports here)
# enter or export the data, then:
python analysis/analyze.py --data-dir data/real --out-dir data/real/output --strict
git status --short                    # data/real must not appear
```

- `--strict` stops on values that don't match the [data dictionary](../data/data-dictionary.md). Fix the log and rerun.
- Keep `data/synthetic/` and `output/` as the demo. Never overwrite them with real data.
- Never commit anything from `data/real/`. Don't move it through cloud sync, email, or personal devices unless the clinic approves.
- `weekly_measures.csv` and the run charts contain unsuppressed weekly counts. The privacy officer reviews them before they leave the clinic.

## 4. Data that is already available
These sources are free and public, and need no approval. Use them for the background section, for comparisons, and to ground the simulation's assumptions. Do **not** present them as this project's results.

| Source | What it gives | Where |
|---|---|---|
| Fairfax County Point-in-Time Count 2026 (OPEH) | 1,365 people experiencing homelessness on Feb 4, 2026 (up 3% from 1,322 in 2025); demographics; shelter and housing inventory | fairfaxcounty.gov/homeless/point-time-count-2026 |
| HRSA Uniform Data System (UDS) | National, state, and health-center data, including patients experiencing homelessness. Starting with 2026 data, Table 6A adds counts of patients screened for upstream drivers of health and patients with food insecurity, housing instability, or financial insecurity. The first public release is likely in mid-2027 | data.hrsa.gov |
| CDC PLACES (December 2025 release) | County and census-tract model estimates of 7 health-related social needs, including food insecurity, housing insecurity, and transportation barriers. Virginia is covered (it used the BRFSS social needs module in 2023). CDC cautions against using PLACES to evaluate programs | cdc.gov/places |
| Feeding America, Map the Meal Gap | County food insecurity estimates (data through 2024, released July 2026); dataset request form | map.feedingamerica.org |
| Capital Area Food Bank, Hunger Report 2026 | NORC survey of 3,804 adults (May 2026): 27% of Fairfax County households food insecure; 38% across the region | capitalareafoodbank.org |

General-population rates likely understate needs among people experiencing homelessness. If you use them in the simulation, say so and cite the source.

## 5. Who to contact

### Possible clinic partners
| Organization | Why | Phone | Email |
|---|---|---|---|
| New Hope Housing, Mobile Medical Outreach | Mobile care for people experiencing homelessness; closest match | 703-799-2293 | admin@newhopehousing.org |
| Fairfax County Health Department, Homeless Healthcare Program | Nurse practitioners in shelters, drop-in centers, and street outreach | 703-246-2411 (main line; ask for the program) | |
| GMU MAP Clinics | Academic clinics, including shelter-based sites | 703-993-5880 | mapclinic@gmu.edu |
| Neighborhood Health (FQHC) | Health center; may share aggregate screening counts | 703-535-5568 | partners@nhnva.org |
| HealthWorks for Northern Virginia (FQHC) | Health center with a Sully site (13800 Wall Rd, Herndon) | 703-443-2000 | |

### Data holders
| Organization | Ask for | Phone | Email / mail |
|---|---|---|---|
| Fairfax County Office to Prevent and End Homelessness (OPEH) | Aggregate Point-in-Time or HMIS figures beyond the dashboard (Template B) | 703-246-5000 | OPEHGeneralMail@fairfaxcounty.gov · 3700 Pender Drive, Fairfax, VA 22030 |
| Fairfax County FOIA Office | Existing aggregate records only (Template C) | 703-324-7052 | FOIA@fairfaxcounty.gov · 12000 Government Center Pkwy, Suite 551, Fairfax, VA 22035 |
| HRSA UDS Support Center | Help reading UDS data | 866-UDS-HELP (866-837-4357) | udshelp330@bphcdata.net |
| Feeding America | Map the Meal Gap dataset | | Online request form (feedingamerica.org, Map the Meal Gap) |
| Your school's IRB or QI office | QI determination (step 3) | | |

### Questions to ask a clinic
1. Do you document on paper or in an EHR? Which one, and does it work offline?
2. Do you screen for social needs now? Which tool, who asks, and how often?
3. How many unique adult patients do you see per week, and how many visits?
4. Are you an FQHC or Health Care for the Homeless grantee that reports UDS?
5. How do you track referrals and follow-up?
6. Would you sponsor a student QI project? What onboarding is required?

## 6. Outreach templates
Replace everything in [brackets].

### Template A — Clinic partnership (email or letter)
> **Subject:** Student quality improvement project on social needs screening
>
> Dear [Name],
>
> I am a [program] student at [school], supervised by [advisor name, title]. For my quality improvement project, I have prepared a ready-to-use package for standard social needs screening at a mobile clinic serving people experiencing homelessness. It includes a short questionnaire based on the CMS Accountable Health Communities tool, a screening protocol, staff training, a Fairfax County resource directory, and a measurement plan.
>
> I am looking for a clinic partner to pilot it for about [16] weeks. The project would:
>
> - Screen adult patients for housing, food, transportation, utilities, safety, health literacy, and ID needs, and offer referrals.
> - Measure the share of eligible visits screened and referred, using coded logs that stay under the clinic's control.
> - Start only after my school's QI determination and your clinic's approval.
>
> Could we set up a 15-minute call? I would also like to learn how your clinic documents social needs today.
>
> Thank you,
> [Name] · [phone] · [email]

### Template B — Aggregate data request
> **Subject:** Request for aggregate data for a student QI project
>
> Dear [Name],
>
> I am a [program] student at [school] working on a quality improvement project about social needs screening for adults experiencing homelessness in Fairfax County. I am asking for **aggregate figures only**, with no patient-level data, for [time period], if they already exist:
>
> 1. [Number of adult patients or visits]
> 2. [Number screened for social needs, and the tool used]
> 3. [Number who screened positive for food, housing, or transportation needs]
> 4. [Number referred]
>
> Counts under [5] may be suppressed. I will use the figures only as background for my [course project/thesis] and will cite them as you direct.
>
> Thank you,
> [Name] · [phone] · [email] · Advisor: [name, email]

### Template C — Virginia FOIA request (existing records)
> **To:** Fairfax County FOIA Office, FOIA@fairfaxcounty.gov
>
> Under the Virginia Freedom of Information Act (Va. Code § 2.2-3700 et seq.), I request copies of the following existing public records: [for example, the most recent annual report or performance summary for the Health Department's Homeless Healthcare Program showing aggregate numbers of people served]. I am a Virginia resident. I prefer electronic copies. Please tell me in advance if costs will exceed $[amount].
>
> [Name] · [mailing address] · [email]

Virginia FOIA covers existing records only. Agencies do not have to create new reports, and patient health records are exempt. Requesters must be Virginia citizens or qualifying media.

## 7. If no partner is available in time
- Keep the synthetic data and label it **simulated** everywhere.
- Replace the example probabilities in `analysis/generate_synthetic_data.py` with sourced estimates, and cite each one. Prefer published studies of patients experiencing homelessness, and use the §4 data for local context.
- Ask the advisor whether an implementation-ready package with simulated results meets the course requirements.
- Collect real data that involves no patients now. Call every resource in [04](04-resource-directory.md), confirm hours, eligibility, and intake steps, and record the date in the "Verified" column.

## 8. Checklist
- [ ] Clinic partner and sponsor confirmed
- [ ] Advisor approval
- [ ] QI/IRB determination letter on file
- [ ] Clinic onboarding complete
- [ ] Route for getting data out of the clinic chosen in writing
- [ ] Resource directory verified by phone
- [ ] Baseline audit complete (weeks 1–4)
- [ ] Analysis run in `data/real/` on approved storage; outputs reviewed by the privacy officer
