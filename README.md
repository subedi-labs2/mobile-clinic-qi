# Mobile Clinic Social Needs Screening — QI Project

An academic quality improvement (QI) project for a mobile clinic in **Chantilly, Virginia (Fairfax County)** serving about 30 patients experiencing homelessness.

**Problem:** Social needs screening depends on which staff member sees the patient. Some patients are asked about food, housing, or transportation, and others are never asked.

**Goal:** Every eligible patient is screened with the same standardized questionnaire, and every identified need is offered a referral with documented follow-up.

> **Phase 1 (this repository):** research, screening protocol, implementation plan, measurement plan, data templates, and analysis code. There is no application code yet.
> **Phase 2:** decide what to build. See [docs/09-phase2-decision-guide.md](docs/09-phase2-decision-guide.md).

## Contents

| # | Document | Purpose |
|---|----------|---------|
| 00 | [Project charter](docs/00-project-charter.md) | Problem, SMART aim, scope, team, timeline |
| 01 | [Evidence review](docs/01-evidence-review.md) | Screening tool comparison and recommendation |
| 02 | [Screening questionnaire](docs/02-screening-questionnaire.md) | The standardized instrument and scoring rules |
| 03 | [Screening protocol (SOP)](docs/03-screening-protocol.md) | Who, when, how; positive-screen response |
| 04 | [Resource directory](docs/04-resource-directory.md) | Fairfax County / Chantilly referral resources |
| 05 | [Training plan](docs/05-training-plan.md) | Staff curriculum, scripts, competency check |
| 06 | [Implementation plan](docs/06-implementation-plan.md) | Phases, PDSA cycles, driver diagram, roles |
| 07 | [Measurement plan](docs/07-measurement-plan.md) | Measure definitions, run-chart rules, targets |
| 08 | [Ethics, privacy & QI determination](docs/08-ethics-privacy.md) | IRB/QI determination, HIPAA, safety reporting |
| 09 | [Phase 2 decision guide](docs/09-phase2-decision-guide.md) | Open questions and build options |
| 10 | [Real data plan](docs/10-real-data-plan.md) | Getting real data: approvals, public sources, contacts, outreach templates |
| — | [Data dictionary](data/data-dictionary.md) | Field definitions for the CSV logs |
| — | [Templates](templates/) | Printable screening form, PDSA worksheet, logs |

## Data analysis

The data templates and the synthetic dataset use the same schema, so the analysis runs unchanged on real data later.

```bash
pip install -r analysis/requirements.txt
python analysis/generate_synthetic_data.py --weeks 16 --baseline-weeks 4 --seed 42
python analysis/analyze.py --data-dir data/synthetic --out-dir output
```

Outputs: run charts in `output/figures/` and a measure summary in `output/summary.md`.

> ⚠️ Everything in `data/synthetic/` is **simulated**. It shows how the analysis works and must not be cited as findings.

**Real data** goes in `data/real/`, which is git-ignored, and only on clinic-approved storage. See [10](docs/10-real-data-plan.md) first. Keep `data/synthetic/` and `output/` as the demo.

```bash
python analysis/analyze.py --data-dir data/real --out-dir data/real/output --strict
```

## Word / PDF versions

```bash
./scripts/build_docs.sh     # requires pandoc; writes dist/*.docx and dist/*.pdf
```

## Key decisions so far

- **Instrument:** AHC-HRSN core items, adapted for homelessness, plus the Single Item Literacy Screener and a locally developed ID/documents item. See [01](docs/01-evidence-review.md).
- **Domains:** housing, food, transportation, utilities, interpersonal safety, health literacy, ID/documents.
- **Out of scope:** behavioral health and substance-use screening stay in the separate clinical workflow until referral capacity is confirmed.
- **Timeline:** not decided. The plan uses a 16-week default (4 baseline + 12 intervention), which can be changed.
- **Data system:** unknown. The plan is paper-first and system-agnostic.
