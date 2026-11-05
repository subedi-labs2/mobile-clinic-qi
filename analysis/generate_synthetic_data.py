#!/usr/bin/env python3
"""Generate a SYNTHETIC (simulated) dataset for demonstrating the QI analysis.

The output follows data/data-dictionary.md. All values are simulated. The
probabilities below are illustrative assumptions, NOT estimates from the
literature or from any real clinic. Do not cite them as findings.
"""
from __future__ import annotations

import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

SCREEN_FIELDS = [
    "visit_id", "patient_id", "visit_date", "week", "phase", "excluded",
    "exclusion_reason", "screen_status", "screener_role", "language", "minutes",
    "housing_status", "sleep_location", "housing_quality_pos", "food_pos",
    "transport_pos", "utilities_pos", "safety_pos", "literacy_pos",
    "id_docs_pos", "notes",
]
REFERRAL_FIELDS = [
    "referral_id", "visit_id", "patient_id", "referral_date", "domain",
    "accepted", "referral_type", "resource", "followup_date", "followup_status",
]

# Illustrative behaviour by phase (simulated improvement trajectory).
PHASE_PARAMS = {
    #            P(complete | due)  P(partial | due)  P(decline | attempted)  P(offer | positive)  P(follow-up documented)  P(safety deferred)
    "baseline": dict(complete=0.05, partial=0.35, decline=0.05, offer=0.40, followup=0.10, deferred=0.30),
    "pdsa1":    dict(complete=0.65, partial=0.10, decline=0.08, offer=0.65, followup=0.15, deferred=0.25),
    "pdsa2":    dict(complete=0.85, partial=0.05, decline=0.07, offer=0.92, followup=0.20, deferred=0.15),
    "pdsa3":    dict(complete=0.90, partial=0.03, decline=0.06, offer=0.95, followup=0.75, deferred=0.10),
}

RESOURCES = {
    "housing": ["OPEH/shelter intake", "Embry Rucker Shelter", "CSP", "Hypothermia Prevention Program"],
    "food": ["WFCM", "DFS SNAP"],
    "transportation": ["Cardinal Care NEMT", "TOPS/TRIP"],
    "utilities": ["DFS Energy Assistance", "CSP"],
    "safety": ["DSV 24-Hour Hotline"],
    "id_docs": ["VA DMV", "Vital Records", "SSA", "CSP"],
}


def phase_for_week(week: int, baseline_weeks: int, total_weeks: int) -> str:
    if week <= baseline_weeks:
        return "baseline"
    remaining = total_weeks - baseline_weeks
    cycle_len = max(1, -(-remaining // 3))  # ceil division into 3 PDSA cycles
    idx = (week - baseline_weeks - 1) // cycle_len
    return ["pdsa1", "pdsa2", "pdsa3"][min(idx, 2)]


def yn(rng: random.Random, p: float) -> str:
    return "Y" if rng.random() < p else "N"


def make_patients(n: int, rng: random.Random) -> list[dict]:
    patients = []
    for i in range(1, n + 1):
        r = rng.random()
        housing = "unstable" if r < 0.85 else ("at_risk" if r < 0.95 else "steady")
        if housing == "unstable":
            sleep = rng.choices(
                ["unsheltered", "vehicle", "shelter", "doubled_up", "motel"],
                weights=[35, 20, 30, 10, 5])[0]
        else:
            sleep = "own_place"
        patients.append(dict(
            patient_id=f"P{i:03d}",
            housing_status=housing,
            sleep_location=sleep,
            p_food=0.60, p_transport=0.45, p_utilities=0.30, p_quality=0.40,
            p_safety=0.15, p_literacy=0.30, p_id=0.40,
            language="es" if rng.random() < 0.2 else ("other" if rng.random() < 0.05 else "en"),
            visit_prob=rng.uniform(0.15, 0.45),
        ))
    return patients


def screen_answers(pt: dict, rng: random.Random, params: dict, partial: bool) -> dict:
    no_home = pt["housing_status"] == "unstable"
    ans = dict(
        housing_status=pt["housing_status"],
        sleep_location=pt["sleep_location"],
        housing_quality_pos="NA" if no_home else yn(rng, pt["p_quality"]),
        food_pos=yn(rng, pt["p_food"]),
        transport_pos=yn(rng, pt["p_transport"]),
        utilities_pos="NA" if no_home else yn(rng, pt["p_utilities"]),
        safety_pos="deferred" if rng.random() < params["deferred"] else yn(rng, pt["p_safety"]),
        literacy_pos=yn(rng, pt["p_literacy"]),
        id_docs_pos=yn(rng, pt["p_id"]),
    )
    if partial:
        # Baseline reality: only some domains asked, depending on provider.
        keep = rng.sample(list(ans), k=rng.randint(1, 3))
        ans = {k: (v if k in keep else "") for k, v in ans.items()}
    return ans


def actionable_positive_domains(ans: dict) -> list[str]:
    d = []
    if ans.get("housing_status") in ("at_risk", "unstable") or ans.get("housing_quality_pos") == "Y":
        d.append("housing")
    for field, dom in [("food_pos", "food"), ("transport_pos", "transportation"),
                       ("utilities_pos", "utilities"), ("safety_pos", "safety"),
                       ("id_docs_pos", "id_docs")]:
        if ans.get(field) == "Y":
            d.append(dom)
    return d


def generate(args) -> tuple[list[dict], list[dict]]:
    rng = random.Random(args.seed)
    patients = make_patients(args.patients, rng)
    start = date.fromisoformat(args.start_date)
    start -= timedelta(days=start.weekday())  # align to Monday
    session_offsets = [1, 3, 5][: args.sessions_per_week]  # Tue/Thu/Sat

    visits, referrals = [], []
    last_complete: dict[str, date] = {}
    v_n = r_n = 0

    for week in range(1, args.weeks + 1):
        phase = phase_for_week(week, args.baseline_weeks, args.weeks)
        params = PHASE_PARAMS[phase]
        for off in session_offsets:
            vdate = start + timedelta(weeks=week - 1, days=off)
            for pt in patients:
                if rng.random() >= pt["visit_prob"]:
                    continue
                v_n += 1
                row = {f: "" for f in SCREEN_FIELDS}
                row.update(visit_id=f"V{v_n:04d}", patient_id=pt["patient_id"],
                           visit_date=vdate.isoformat(), week=week, phase=phase,
                           excluded="N", language=pt["language"])
                if rng.random() < 0.02:
                    row.update(excluded="Y", exclusion_reason=rng.choice(
                        ["medical_unstable", "unable_to_participate"]),
                        screen_status="not_screened")
                    visits.append(row)
                    continue

                prev = last_complete.get(pt["patient_id"])
                if prev and (vdate - prev).days <= 90:
                    row["screen_status"] = "not_due"
                    visits.append(row)
                    continue

                r = rng.random()
                if r < params["complete"]:
                    status = "complete"
                elif r < params["complete"] + params["partial"]:
                    status = "partial"
                else:
                    status = "not_screened"
                if status in ("complete", "partial") and rng.random() < params["decline"]:
                    status = "declined"
                row["screen_status"] = status

                if status in ("complete", "partial"):
                    ans = screen_answers(pt, rng, params, partial=(status == "partial"))
                    row.update(ans)
                    row["screener_role"] = (rng.choice(["clinician", "RN"]) if phase == "baseline"
                                            else rng.choice(["CHW", "MA", "RN", "volunteer"]))
                    if status == "complete":
                        row["minutes"] = max(3, round(rng.gauss(7 if phase == "pdsa1" else 6, 1.5)))
                        last_complete[pt["patient_id"]] = vdate
                    else:
                        row["notes"] = "baseline: some domains asked" if phase == "baseline" else "incomplete"

                    for dom in actionable_positive_domains(ans):
                        if rng.random() >= params["offer"]:
                            continue
                        r_n += 1
                        accepted = yn(rng, 0.70)
                        fu_status, fu_date = "pending", ""
                        # Follow-up behaviour depends on the phase when follow-up is due,
                        # so PDSA 3 also closes the loop on earlier referrals.
                        due_date = vdate + timedelta(days=rng.randint(7, 28))
                        due_week = (due_date - start).days // 7 + 1
                        fu_phase = (phase_for_week(due_week, args.baseline_weeks, args.weeks)
                                    if due_week <= args.weeks else None)
                        p_fu = PHASE_PARAMS[fu_phase]["followup"] if fu_phase else 0.0
                        if accepted == "Y" and rng.random() < p_fu:
                            fu_status = rng.choices(
                                ["connected", "not_connected", "unable_to_reach"],
                                weights=[55, 20, 25])[0]
                            fu_date = due_date.isoformat()
                        elif accepted == "N":
                            fu_status = "declined_followup"
                        referrals.append(dict(
                            referral_id=f"R{r_n:04d}", visit_id=row["visit_id"],
                            patient_id=pt["patient_id"], referral_date=vdate.isoformat(),
                            domain=dom, accepted=accepted,
                            referral_type=rng.choices(
                                ["warm_handoff", "direct_referral", "information_only"],
                                weights=[2, 3, 5] if phase == "baseline" else [5, 3, 2])[0],
                            resource=rng.choice(RESOURCES[dom]),
                            followup_date=fu_date, followup_status=fu_status))
                visits.append(row)
    return visits, referrals


def write_csv(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--patients", type=int, default=30)
    ap.add_argument("--weeks", type=int, default=16)
    ap.add_argument("--baseline-weeks", type=int, default=4)
    ap.add_argument("--sessions-per-week", type=int, default=2, choices=[1, 2, 3])
    ap.add_argument("--start-date", default="2026-01-05")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out-dir", default="data/synthetic")
    ap.add_argument("--templates-dir", default="data/templates",
                    help="Also write header-only CSV templates here ('' to skip)")
    args = ap.parse_args()
    if not 0 < args.baseline_weeks < args.weeks:
        ap.error("--baseline-weeks must be between 1 and --weeks - 1")

    visits, referrals = generate(args)
    out = Path(args.out_dir)
    write_csv(out / "screening_log.csv", SCREEN_FIELDS, visits)
    write_csv(out / "referral_log.csv", REFERRAL_FIELDS, referrals)
    if args.templates_dir:
        t = Path(args.templates_dir)
        write_csv(t / "screening_log.csv", SCREEN_FIELDS, [])
        write_csv(t / "referral_log.csv", REFERRAL_FIELDS, [])
    print(f"Wrote {len(visits)} visits and {len(referrals)} referrals to {out}/ (SYNTHETIC)")


if __name__ == "__main__":
    main()
