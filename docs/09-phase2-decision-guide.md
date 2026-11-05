# 09 — Phase 2 Decision Guide: What Should We Build?

Phase 1 is paper-first so the project can start without depending on any system. Phase 2 decides whether a tool would improve reliability, and which one.

## Open questions (must answer first)
| # | Question | Why it matters | Answer |
|---|---|---|---|
| 1 | **What does the clinic use to document today?** Paper, EHR (which one?), spreadsheet? | Decides whether we build inside an EHR or standalone | *Unknown — find out* |
| 2 | Does the clinic have tablets/phones and reliable cellular data on the van? | Offline capability may be required | |
| 3 | Is the clinic an FQHC / Health Care for the Homeless grantee reporting UDS? | May require PRAPARE instead of AHC-HRSN | |
| 4 | Does the county or region use a closed-loop referral platform (e.g., Unite Us, findhelp)? | Integrate with it rather than build | |
| 5 | Who will own and maintain any tool after the student leaves? | Avoid building something unsupported | |
| 6 | What is the project timeline? | Limits how much can be built and tested | *Not decided* |
| 7 | Where may data be stored (HIPAA-compliant, clinic-controlled)? | Rules out many free tools | |
| 8 | Will patients self-administer on a tablet, or will staff read the questions? | UX design, literacy | |
| 9 | Is there a confirmed clinic partner and an approved route for getting data out of the clinic? | No real data or testing without one; see [10](10-real-data-plan.md) | *Not yet* |

## Build options

| Option | Effort | Pros | Cons | Fits when |
|---|---|---|---|---|
| **A. Stay on paper + spreadsheet** (this repo's templates + `analyze.py`) | Very low | Zero cost; works offline; no IT approval | Transcription errors; manual follow-up tracking | No devices or IT support; short timeline |
| **B. EHR-native form/flowsheet** | Low–medium (EHR analyst) | Data in the chart; reportable; sustainable | Needs vendor/IT support; less flexible | Clinic has an EHR with a configurable template |
| **C. REDCap or similar secure survey tool** | Low–medium | HIPAA-capable via institution; offline mobile app; built-in exports | Separate from the chart; institution must host | Academic partner with REDCap; no EHR flexibility |
| **D. Existing referral platform** | Low (config) | Closed-loop referrals built in | Licensing cost; partner adoption varies | Region already uses one |
| **E. Custom app** (offline PWA: screening + referral log + dashboard) | High | Tailored workflow and dashboard | Security, hosting, HIPAA, and maintenance burden | Only if A–D are not feasible and there is a long-term owner |

**Current recommendation:** start with **A**. Move to **C** (REDCap) or **B** (EHR) when Question 1 is answered. Option E is the last resort. If a custom tool is built, a **QI dashboard** that reads the coded CSV logs (no direct identifiers) and runs on clinic-controlled storage is the safest and most useful thing to build first.

## What Phase 1 already provides
- A data schema ([data dictionary](../data/data-dictionary.md)) that every option can export to.
- Analysis code that produces the run charts from any option's CSV export.
- A paper form that can be converted directly into REDCap or EHR fields.
