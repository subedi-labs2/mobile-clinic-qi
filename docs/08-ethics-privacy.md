# 08 — Ethics, Privacy, and QI Determination

> This document is guidance for planning. It is **not legal advice**. Confirm every item with the faculty advisor, the institution's IRB, and the clinic's compliance or privacy officer.

## 1. QI vs. research determination
Academic QI projects usually need a formal **determination** from the student's institution, either "QI, not human-subjects research" or IRB review. Get it **before** collecting any data, including baseline chart audits.

Features of this project that point to QI:
- The aim is to improve local practice using an established standard (AHC-HRSN).
- Everyone eligible gets the improved process. There is no randomization or withholding.
- Data are used for local improvement.

Features that may call for IRB review:
- An intent to publish generalizable findings. Many IRBs still allow QI publication, so ask.
- Collecting data beyond routine care, such as patient interviews or surveys for research.
- The vulnerable population. People experiencing homelessness may be treated as needing added protections.

**Action:** submit the institution's QI determination form with this charter, protocol, and measurement plan.

## 2. Privacy (HIPAA)
- The clinic is likely a HIPAA covered entity. The student needs a role in the clinic's workforce (for example, a student or volunteer agreement) or a data use arrangement to access PHI.
- **Minimum necessary:** the QI logs use a **study ID** only, with no names, DOB, addresses, or phone numbers. The study-ID-to-patient key stays at the clinic, locked, and separate from the logs.
- **The coded logs are still PHI.** Replacing names with study IDs does not de-identify them. `visit_date`, `referral_date`, `followup_date`, and the `week` number derived from them are date elements. HIPAA's Safe Harbor method requires removing all date elements except the year (45 CFR 164.514(b)). Converting dates to week numbers does **not** meet that standard. Coded logs with dates are at most a **Limited Data Set** (45 CFR 164.514(e)).
- Phone numbers from Q14 stay on the paper form and in the clinic record. **Never put them in the CSV logs or this repository.**
- **Never commit real patient data to GitHub.** This repo is for templates and synthetic data only. `.gitignore` blocks `data/real/`.
- Small cells: with about 30 patients, suppress or merge cells with n < 5 in reports to reduce re-identification risk.

### Getting data out of the clinic
Before the baseline audit, choose one route in writing with the clinic's privacy officer:

| Route | What leaves the clinic | Requirement |
|---|---|---|
| **1. Analyze on site** | Aggregate results only | Student has workforce status (student or volunteer agreement, HIPAA training) and works only on clinic-controlled storage |
| **2. Clinic runs the analysis** | Aggregate results only | Clinic staff run `analysis/analyze.py` and share the summary |
| **3. Limited Data Set** | Coded logs, including dates | Signed **Data Use Agreement** between the clinic and the student or school |

Aggregate results (run charts, percentages, the summary) go into the thesis or report only after the privacy officer reviews them. `analyze.py` suppresses small cells in the prevalence table, but the weekly counts in `weekly_measures.csv` and the run charts are **not** suppressed. If weekly counts are small, report percentages or monthly totals. See [10](10-real-data-plan.md) for the full plan.

## 3. Consent and autonomy
- Screening is part of routine care, so a separate research consent is normally not required for QI. The patient may still decline any or all items without any effect on care.
- Ask about desire for help separately from risk. Patients may decline referrals.
- Do not give written materials on safety resources without asking whether it is safe for the patient to carry them.

## 4. Safety disclosures and mandated reporting (Virginia)
- **Adults 60+ or incapacitated adults:** Virginia law makes certain professionals mandated reporters of suspected abuse, neglect, or exploitation to Adult Protective Services (Va. Code § 63.2-1606). Confirm which clinic roles this applies to.
- **Other adults (IPV):** confirm with compliance whether any injury-reporting rules apply to the clinicians. Otherwise, follow a patient-centered response: hotline, safety planning, and patient choice.
- **Minors** are out of scope (adults only). If a minor is encountered, follow child protective services reporting rules.
- Document the clinic's final policy in [03](03-screening-protocol.md) §6 before go-live.

## 5. Equity considerations
- Screen everyone the same way. That consistency is the purpose of the project.
- Provide language access (interpreters and translated forms).
- Avoid documentation that could be used against patients. Keep QI logs minimal and coded.
- Include a patient or lived-experience advisor in reviewing wording and acceptability.

## 6. Checklist
- [ ] Institutional QI/IRB determination letter on file
- [ ] Clinic data-access agreement / workforce status for student
- [ ] Route for getting data out of the clinic chosen in writing (on-site analysis, clinic-run analysis, or Limited Data Set + DUA)
- [ ] Compliance sign-off on safety pathway and reporting
- [ ] Data storage location approved (encrypted, clinic-controlled)
- [ ] Data retention/destruction plan for the linking key
