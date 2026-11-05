# 02 — Standardized Social Needs Screening Questionnaire

**Version:** 0.1 (draft for patient-advisor and clinic review)
**Administration:** staff-read aloud (default) or self-completed. About 5–7 minutes.
**Eligible:** adults ≥ 18 at a clinic visit who have not completed a screen in the past 90 days (see [03](03-screening-protocol.md)).

Item text for Q1–Q10 is from the CMS **Accountable Health Communities HRSN Screening Tool** (public). Q11 is the **Single Item Literacy Screener** (Morris 2006). Items marked **(local)** are developed for this project and have not been validated.

A printable version is in [`templates/screening-form.md`](../templates/screening-form.md).

---

### Intro script (read aloud)
> "We ask everyone we see the same few questions about things like food, transportation, and safety, because these affect health. Your answers are private and won't affect the care you get today. You can skip any question. If something comes up, we can connect you with help, only if you want it."

---

### Housing
**Q1. What is your living situation today?** *(AHC)*
- ☐ I have a steady place to live
- ☐ I have a place to live today, but I am worried about losing it in the future → **POSITIVE (at risk)**
- ☐ I do not have a steady place to live (I am temporarily staying with others, in a hotel, in a shelter, living outside on the street, on a beach, in a car, abandoned building, bus or train station, or in a park) → **POSITIVE (unstable)**

**Q1a. Where did you sleep last night?** *(local, used for referral routing, not scoring)*
☐ Outside / street / park / woods ☐ Vehicle ☐ Emergency shelter / hypothermia site ☐ Staying with friends/family ☐ Motel/hotel ☐ Own apartment/room ☐ Other: ____

**Q2. Think about the place you live. Do you have problems with any of the following?** *(AHC, **skip if Q1 = "do not have a steady place to live"**)*
☐ Pests ☐ Mold ☐ Lead paint or pipes ☐ Lack of heat ☐ Oven or stove not working ☐ Smoke detectors missing or not working ☐ Water leaks ☐ None of the above
→ **POSITIVE** if any problem is selected.

### Food
**Q3. Within the past 12 months, you worried that your food would run out before you got money to buy more.** *(AHC / Hunger Vital Sign)*
☐ Often true ☐ Sometimes true ☐ Never true

**Q4. Within the past 12 months, the food you bought just didn't last and you didn't have money to get more.** *(AHC / Hunger Vital Sign)*
☐ Often true ☐ Sometimes true ☐ Never true

→ **POSITIVE** if "Often true" or "Sometimes true" on **either** Q3 or Q4.

### Transportation
**Q5. In the past 12 months, has lack of reliable transportation kept you from medical appointments, meetings, work, or from getting things needed for daily living?** *(AHC)*
☐ Yes → **POSITIVE** ☐ No

### Utilities
**Q6. In the past 12 months has the electric, gas, oil, or water company threatened to shut off services in your home?** *(AHC, **skip if Q1 = "do not have a steady place to live"**)*
☐ Yes → **POSITIVE** ☐ No ☐ Already shut off → **POSITIVE**

### Interpersonal safety
> **Ask only if the patient is alone and the conversation cannot be overheard.** If privacy is not possible, mark "Deferred: no privacy" and retry at the next visit.

*(AHC, adapted from HITS)* How often does anyone, including family and friends:

| | Never (1) | Rarely (2) | Sometimes (3) | Fairly often (4) | Frequently (5) |
|---|---|---|---|---|---|
| **Q7.** physically hurt you? | ☐ | ☐ | ☐ | ☐ | ☐ |
| **Q8.** insult or talk down to you? | ☐ | ☐ | ☐ | ☐ | ☐ |
| **Q9.** threaten you with harm? | ☐ | ☐ | ☐ | ☐ | ☐ |
| **Q10.** scream or curse at you? | ☐ | ☐ | ☐ | ☐ | ☐ |

→ **POSITIVE** if Q7–Q10 total **≥ 11**. Follow the safety pathway in [03](03-screening-protocol.md) §6 and do not wait for the full score if imminent danger is disclosed.

### Health literacy
**Q11. How often do you need to have someone help you when you read instructions, pamphlets, or other written material from your doctor or pharmacy?** *(SILS)*
☐ Never ☐ Rarely ☐ Sometimes ☐ Often ☐ Always
→ **POSITIVE** if "Sometimes", "Often", or "Always".
*A positive result changes how we communicate (teach-back, verbal instructions, pictograms). It is not a referral.*

### ID / documents *(local, unvalidated)*
**Q12. Do you have these documents with you or somewhere safe that you can get to?**

| Document | Have it | Don't have it | Want help getting it? |
|---|---|---|---|
| Photo ID (state ID / driver's license) | ☐ | ☐ | ☐ Yes ☐ No |
| Social Security card | ☐ | ☐ | ☐ Yes ☐ No |
| Birth certificate | ☐ | ☐ | ☐ Yes ☐ No |
| Health insurance / Medicaid card | ☐ | ☐ | ☐ Yes ☐ No |

→ **POSITIVE** if any document is missing.

### Desire for help *(local)*
**Q13. For each area that came up, would you like help with it today?**
☐ Housing ☐ Food ☐ Transportation ☐ Utilities ☐ Safety ☐ ID/documents ☐ None right now

### Contact for follow-up *(local, operational)*
**Q14. What is the best way for us to reach you in the next few weeks?**
☐ Phone/text: ________ ☐ Through shelter/case manager: ________ ☐ At the next clinic stop ☐ Other: ________ ☐ Prefer no follow-up

---

## Scoring summary

| Domain | Positive if | Not applicable when |
|---|---|---|
| Housing (status) | Q1 ≠ steady | — |
| Housing (quality) | Any Q2 problem | Q1 = no steady place |
| Food | Q3 or Q4 = often/sometimes | — |
| Transportation | Q5 = Yes | — |
| Utilities | Q6 = Yes / already shut off | Q1 = no steady place |
| Safety | Q7–10 sum ≥ 11 | Deferred (no privacy) → record `deferred` |
| Health literacy | Q11 ≥ sometimes | — |
| ID/documents | Any document missing | — |

**Screen "complete"** means Q1, Q3–Q5, Q11, and Q12 are answered (or patient declined that item), and safety is either answered or recorded as deferred. Skipped-by-logic items count as complete.

## Coding for data entry
See [data/data-dictionary.md](../data/data-dictionary.md). Optional standard codes for an EHR (Phase 2): LOINC panel 96777-8 (AHC HRSN screening tool) and ICD-10-CM Z55–Z65 for documented needs (e.g., Z59.0x homelessness, Z59.41 food insecurity, Z59.82 transportation insecurity). **Verify the current code set before use.**

## Translation
The AHC tool is available in multiple languages from CMS. Use professionally translated versions where available. The local items need translation and back-translation, especially into Spanish. Fairfax County's Coordinated Services Planning line offers many languages for referrals ([04](04-resource-directory.md)).
