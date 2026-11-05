# 01 — Evidence Review: Selecting a Social Needs Screening Instrument

## Question
Which standardized instrument should a small mobile clinic serving adults experiencing homelessness use? It should cover housing, food, transportation, utilities, interpersonal safety, health literacy, and ID/documents. It must be short enough for a mobile visit, and every domain must map to a referral the clinic can actually make.

## Method
Targeted review of instrument documentation, the UCSF SIREN screening-tool comparison (which also covers WE CARE, Health Leads, and others), and key primary literature (references below). This is not a systematic review. If your program requires a formal search strategy (databases, search terms, PRISMA flow), add it here.

## Instruments compared

| Criterion | **AHC-HRSN** (CMS) | **PRAPARE** (NACHC) | **Hunger Vital Sign** |
|---|---|---|---|
| Length | 10 core items (+ supplemental) | ~21 items (core + optional) | 2 items |
| Housing | ✅ status + quality | ✅ status + worry | — |
| Food | ✅ (Hunger Vital Sign) | ✅ | ✅ |
| Transportation | ✅ | ✅ | — |
| Utilities | ✅ | ✅ | — |
| Interpersonal safety | ✅ (HITS-based, scored) | ✅ (optional) | — |
| Health literacy | — | — | — |
| ID/documents | — | — | — |
| Cost/licensing | Free (public, CMS) | Free (see NACHC terms) | Free |
| Origin setting | Clinical settings serving Medicare/Medicaid beneficiaries | Community health centers (FQHCs) | Pediatrics / general |
| Validation note | Items drawn from previously validated measures; TEP-reviewed (Billioux 2017) | Extensive field use; FHIR/LOINC mappings | Sensitivity ~97 %, specificity ~83 % vs. USDA 18-item (Hager 2010) |

*Sources: SIREN comparison table; instrument documentation. Few social-risk tools have gone through full gold-standard psychometric development (SIREN). We found no validation study specific to unsheltered adults.*

## Key findings
1. **Brevity matters in mobile settings.** Both AHC-HRSN core and PRAPARE take about 5–10 minutes. AHC core covers all five of our required "core" domains in 10 items. PRAPARE adds demographics the clinic may already collect elsewhere.
2. **The housing item works differently for this population.** Nearly all patients will screen positive on "living situation." The useful information is the *type* of homelessness (unsheltered, shelter, doubled-up, vehicle), because that decides the referral (Coordinated Entry, shelter, hypothermia program). We therefore add a "where did you sleep last night" follow-up.
3. **Some items do not apply.** Housing-quality and utility-shutoff items assume a dwelling. For unsheltered patients they should be skipped, not scored as negative.
4. **Health literacy and ID/documents are not covered by any of the main tools.**
   - Health literacy: the **Single Item Literacy Screener (SILS)** (Morris 2006) is one item, published, and widely used.
   - ID/documents: we found no validated item. Lack of ID blocks access to shelter, benefits, Medicaid enrollment, and employment. We use a **locally developed** item and label it as unvalidated.
5. **Ask whether the patient wants help.** Screening positive does not mean the patient wants assistance. Studies find substantial mismatch between reported risk and interest in help (De Marchis 2020). Asking "would you like help with this?" respects autonomy and makes referral measures more meaningful.
6. **Screening is acceptable to most patients** when the reason is explained (De Marchis 2019, Byhoff 2019). Privacy and a clear purpose matter, especially for safety questions.
7. **Screening without a response pathway is the most common failure mode.** Navigation (in-person help) outperformed written information alone in an RCT (Gottlieb 2016). This supports a warm handoff plus follow-up, not just a handout.
8. **The federal measure landscape changed in 2025.** CMS removed the "Screening for Social Drivers of Health" quality measure (Quality ID 487) from the MSSP APP Plus set. NCQA's HEDIS **Social Need Screening and Intervention (SNS-E)** measure continues, with technical updates for MY 2026. This project's measures are internal QI measures modeled on these definitions, so they do not depend on federal reporting.

## Recommendation
Use the **AHC-HRSN core 10 items** as the base, because they are free, public-domain, short, and cover the required domains. Adapt them for homelessness:

| Domain | Item source | Adaptation |
|---|---|---|
| Housing status | AHC Q1 | + "where did you sleep last night" (local) for referral routing |
| Housing quality | AHC Q2 | Skip if no steady place to live |
| Food | AHC Q3–4 (Hunger Vital Sign) | None |
| Transportation | AHC Q5 | None |
| Utilities | AHC Q6 | Skip if no steady place to live |
| Interpersonal safety | AHC Q7–10 (HITS) | Ask only in private; otherwise defer and document |
| Health literacy | SILS (Morris 2006) | None |
| ID/documents | Local item | Flag as unvalidated; review with patient advisor |
| Desire for help | Local item (modeled on De Marchis 2020) | Asked once per positive domain |

**Alternative:** if the clinic is an FQHC or Health Care for the Homeless (HCH) grantee already reporting PRAPARE (UDS), use PRAPARE instead so the data stay consistent. **Confirm this before go-live** (see [09](09-phase2-decision-guide.md)).

## Gaps to state in the write-up
- We found no instrument validated specifically among unsheltered adults.
- The ID/documents item is unvalidated.
- With n≈30, findings about need prevalence are descriptive only.

## References
1. Billioux A, Verlander K, Anthony S, Alley D. Standardized screening for health-related social needs in clinical settings: the Accountable Health Communities screening tool. *NAM Perspectives.* 2017. doi:10.31478/201705b
2. Hager ER, Quigg AM, Black MM, et al. Development and validity of a 2-item screen to identify families at risk for food insecurity. *Pediatrics.* 2010;126(1):e26-e32.
3. Sherin KM, Sinacore JM, Li XQ, Zitter RE, Shakil A. HITS: a short domestic violence screening tool for use in a family practice setting. *Fam Med.* 1998;30(7):508-512.
4. Morris NS, MacLean CD, Chew LD, Littenberg B. The Single Item Literacy Screener: evaluation of a brief instrument to identify limited reading ability. *BMC Fam Pract.* 2006;7:21.
5. Gottlieb LM, Hessler D, Long D, et al. Effects of social needs screening and in-person service navigation on child health: a randomized clinical trial. *JAMA Pediatr.* 2016;170(11):e162521.
6. De Marchis EH, Hessler D, Fichtenberg C, et al. Part I: A quantitative study of social risk screening acceptability in patients and caregivers. *Am J Prev Med.* 2019;57(6 Suppl 1):S25-S37.
7. Byhoff E, De Marchis EH, Hessler D, et al. Part II: A qualitative study of social risk screening acceptability in patients and caregivers. *Am J Prev Med.* 2019;57(6 Suppl 1):S38-S46.
8. De Marchis EH, Hessler D, Fichtenberg C, et al. Assessment of social risk factors and interest in receiving health care–based social assistance among adult patients and adult caregivers of pediatric patients. *JAMA Netw Open.* 2020;3(10):e2021201.
9. National Association of Community Health Centers. PRAPARE: Protocol for Responding to and Assessing Patients' Assets, Risks, and Experiences. https://prapare.org
10. UCSF SIREN. Social Needs Screening Tool Comparison Table. https://sirenetwork.ucsf.edu/tools-resources/resources/screening-tools-comparison
11. NCQA. Social Need Screening and Intervention: What's changing in the MY 2026 Technical Update. Dec 2025. https://www.ncqa.org/blog/social-need-screening-and-intervention-whats-changing/
12. Centers for Medicare & Medicaid Services. CY 2026 Medicare Physician Fee Schedule final rule (removal of Quality ID 487 from APP Plus measure set). 2025.

> Verify each citation against the full text before academic submission. Some details here (for example, page ranges) come from secondary sources.
