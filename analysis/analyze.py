#!/usr/bin/env python3
"""Compute QI measures and run charts from the screening and referral logs.

Works on synthetic data (data/synthetic) or real coded data in the same
schema (see data/data-dictionary.md). Measure definitions: docs/07-measurement-plan.md.
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

RESCREEN_DAYS = 90
FOLLOWUP_WINDOW_DAYS = 30
MIN_WEEKLY_DENOM = 5
ACTIONABLE = ["housing", "food", "transportation", "utilities", "safety", "id_docs"]
PHASE_ORDER = ["baseline", "pdsa1", "pdsa2", "pdsa3", "sustain"]

ALLOWED = {
    "screening": {
        "phase": set(PHASE_ORDER),
        "excluded": {"Y", "N"},
        "exclusion_reason": {"", "medical_unstable", "unable_to_participate"},
        "screen_status": {"complete", "partial", "declined", "not_screened", "not_due"},
        "screener_role": {"", "MA", "RN", "CHW", "clinician", "volunteer"},
        "language": {"en", "es", "other"},
        "housing_status": {"", "steady", "at_risk", "unstable"},
        "sleep_location": {"", "unsheltered", "vehicle", "shelter", "doubled_up", "motel", "own_place", "other"},
        "housing_quality_pos": {"", "Y", "N", "NA"},
        "food_pos": {"", "Y", "N"},
        "transport_pos": {"", "Y", "N"},
        "utilities_pos": {"", "Y", "N", "NA"},
        "safety_pos": {"", "Y", "N", "deferred"},
        "literacy_pos": {"", "Y", "N"},
        "id_docs_pos": {"", "Y", "N"},
    },
    "referral": {
        "domain": set(ACTIONABLE),
        "accepted": {"Y", "N"},
        "referral_type": {"warm_handoff", "direct_referral", "information_only"},
        "followup_status": {"pending", "connected", "not_connected", "unable_to_reach", "declined_followup"},
    },
}


# ---------------------------------------------------------------- loading ---
def load(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, list[str]]:
    s = pd.read_csv(data_dir / "screening_log.csv", dtype=str, keep_default_na=False)
    r = pd.read_csv(data_dir / "referral_log.csv", dtype=str, keep_default_na=False)
    errors = validate(s, r)
    s["visit_date"] = pd.to_datetime(s["visit_date"], errors="coerce")
    s["week"] = pd.to_numeric(s["week"], errors="coerce").astype("Int64")
    s["minutes"] = pd.to_numeric(s["minutes"], errors="coerce")
    r["referral_date"] = pd.to_datetime(r["referral_date"], errors="coerce")
    r["followup_date"] = pd.to_datetime(r["followup_date"], errors="coerce")
    return s, r, errors


def validate(s: pd.DataFrame, r: pd.DataFrame) -> list[str]:
    errs: list[str] = []
    for name, df in (("screening", s), ("referral", r)):
        for col, allowed in ALLOWED[name].items():
            if col not in df.columns:
                errs.append(f"{name}_log: missing column '{col}'")
                continue
            bad = df.loc[~df[col].isin(allowed), col]
            for idx, val in bad.items():
                errs.append(f"{name}_log row {idx + 2}: {col}='{val}' not allowed")
    if s["visit_id"].duplicated().any():
        errs.append("screening_log: duplicate visit_id values")
    if pd.to_datetime(s["visit_date"], errors="coerce").isna().any():
        errs.append("screening_log: unparseable visit_date")
    if pd.to_numeric(s["week"], errors="coerce").isna().any():
        errs.append("screening_log: missing/invalid week")
    missing_reason = s[(s["excluded"] == "Y") & (s["exclusion_reason"] == "")]
    errs += [f"screening_log row {i + 2}: excluded=Y without exclusion_reason" for i in missing_reason.index]
    orphan = ~r["visit_id"].isin(s["visit_id"])
    errs += [f"referral_log row {i + 2}: visit_id '{v}' not in screening_log" for i, v in r.loc[orphan, "visit_id"].items()]
    if r["referral_id"].duplicated().any():
        errs.append("referral_log: duplicate referral_id values")
    return errs


# ----------------------------------------------------------- derivations ---
def derive(s: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    s = s.sort_values(["patient_id", "visit_date", "visit_id"]).copy()
    due, utd = [], []
    last_complete: dict[str, pd.Timestamp] = {}
    for row in s.itertuples():
        prev = last_complete.get(row.patient_id)
        recent = prev is not None and (row.visit_date - prev).days <= RESCREEN_DAYS
        is_complete = row.screen_status == "complete"
        due.append(not recent)
        utd.append(recent or is_complete)
        if is_complete:
            last_complete[row.patient_id] = row.visit_date
    s["due"] = due
    s["up_to_date"] = utd
    s["included"] = s["excluded"] != "Y"

    s["housing_pos"] = s["housing_status"].isin(["at_risk", "unstable"]) | (s["housing_quality_pos"] == "Y")
    domain_cols = {"housing": "housing_pos", "food": "food_pos", "transportation": "transport_pos",
                   "utilities": "utilities_pos", "safety": "safety_pos", "id_docs": "id_docs_pos"}
    pos = pd.DataFrame({d: (s[c] == "Y") if c != "housing_pos" else s[c] for d, c in domain_cols.items()})
    s["positive_domains"] = pos.apply(lambda x: {d for d in ACTIONABLE if x[d]}, axis=1)

    offered = r.groupby("visit_id")["domain"].agg(set).to_dict()
    s["offered_domains"] = s["visit_id"].map(lambda v: offered.get(v, set()))
    s["has_positive"] = (s["screen_status"] == "complete") & s["positive_domains"].map(bool)
    s["all_offered"] = [p <= o for p, o in zip(s["positive_domains"], s["offered_domains"])]
    return s.sort_values(["visit_date", "visit_id"]).reset_index(drop=True)


# ----------------------------------------------------------- statistics ---
def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (math.nan, math.nan)
    p = k / n
    denom = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return (max(0.0, centre - half), min(1.0, centre + half))


def run_rules(values: list[float], median: float) -> dict:
    """Detect shifts (>=6 points one side of median) and trends (>=5 points up/down)."""
    shifts, trends = [], []
    run_side, run_idx = 0, []
    for i, v in enumerate(values):
        if v is None or math.isnan(v) or v == median:
            continue  # points on the median neither make nor break a shift
        side = 1 if v > median else -1
        if side == run_side:
            run_idx.append(i)
        else:
            if len(run_idx) >= 6:
                shifts.append((run_idx[0], run_idx[-1], run_side))
            run_side, run_idx = side, [i]
    if len(run_idx) >= 6:
        shifts.append((run_idx[0], run_idx[-1], run_side))

    pts = [(i, v) for i, v in enumerate(values) if v is not None and not math.isnan(v)]
    dedup = [p for j, p in enumerate(pts) if j == 0 or p[1] != pts[j - 1][1]]  # like values ignored
    if len(dedup) >= 2:
        start, direction = 0, 0
        for j in range(1, len(dedup)):
            d = 1 if dedup[j][1] > dedup[j - 1][1] else -1
            if d != direction:
                if direction != 0 and j - start >= 5:
                    trends.append((dedup[start][0], dedup[j - 1][0], direction))
                start, direction = j - 1, d
        if direction != 0 and len(dedup) - start >= 5:
            trends.append((dedup[start][0], dedup[-1][0], direction))
    return {"shifts": shifts, "trends": trends}


# ------------------------------------------------------------ measures ---
def weekly(s: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    inc = s[s["included"]]
    g = inc.groupby("week")
    w = pd.DataFrame({
        "phase": g["phase"].agg(lambda x: x.mode().iat[0]),
        "visits": g.size(),
        "p1_num": g["up_to_date"].sum(),
        "due": g["due"].sum(),
        "p1a_num": g.apply(lambda x: ((x["screen_status"] == "complete") & x["due"]).sum(), include_groups=False),
        "declined": g.apply(lambda x: ((x["screen_status"] == "declined") & x["due"]).sum(), include_groups=False),
        "p2_den": g["has_positive"].sum(),
        "p2_num": g.apply(lambda x: (x["has_positive"] & x["all_offered"]).sum(), include_groups=False),
    })
    w["P1"] = w["p1_num"] / w["visits"]
    w["P1a"] = w["p1a_num"] / w["due"].where(w["due"] > 0)
    w["P2"] = w["p2_num"] / w["p2_den"].where(w["p2_den"] > 0)
    w["B1"] = w["declined"] / w["due"].where(w["due"] > 0)
    return w.reset_index()


def followup_measures(s: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    end = s["visit_date"].max()
    acc = r[(r["accepted"] == "Y")].copy()
    acc["matured"] = (end - acc["referral_date"]).dt.days >= FOLLOWUP_WINDOW_DAYS
    acc = acc[acc["matured"]]
    within = (acc["followup_date"] - acc["referral_date"]).dt.days <= FOLLOWUP_WINDOW_DAYS
    acc["documented"] = (acc["followup_status"] != "pending") & within
    acc["connected"] = (acc["followup_status"] == "connected") & within
    phase = s.set_index("visit_id")["phase"]
    acc["phase"] = acc["visit_id"].map(phase)
    out = acc.groupby("phase").agg(accepted=("referral_id", "size"),
                                   documented=("documented", "sum"),
                                   connected=("connected", "sum"))
    out.loc["all"] = out.sum()
    out["O1"] = out["documented"] / out["accepted"]
    out["O2"] = out["connected"] / out["accepted"]
    return out.reindex([p for p in PHASE_ORDER + ["all"] if p in out.index])


def pre_post(s: pd.DataFrame) -> pd.DataFrame:
    inc = s[s["included"]].copy()
    inc["period"] = inc["phase"].map(lambda p: "baseline" if p == "baseline" else "intervention")
    rows = []
    for period, x in inc.groupby("period"):
        due = x[x["due"]]
        pos = x[x["has_positive"]]
        for mid, k, n in [
            ("P1 up-to-date screen", int(x["up_to_date"].sum()), len(x)),
            ("P1a due-screen completed", int((due["screen_status"] == "complete").sum()), len(due)),
            ("P2 referral offered (all positive domains)", int(pos["all_offered"].sum()), len(pos)),
            ("B1 declined (due visits)", int((due["screen_status"] == "declined").sum()), len(due)),
        ]:
            lo, hi = wilson(k, n)
            rows.append(dict(measure=mid, period=period, num=k, den=n,
                             pct=(k / n if n else math.nan), ci_low=lo, ci_high=hi))
    return pd.DataFrame(rows)


def prevalence(s: pd.DataFrame, suppress: bool) -> pd.DataFrame:
    comp = s[s["screen_status"] == "complete"].sort_values("visit_date").groupby("patient_id").tail(1)
    rows = []
    # Denominator per domain = patients who answered it (excludes NA / deferred / blank).
    answered = lambda col: comp[col].isin(["Y", "N"])  # noqa: E731
    for label, mask, den_mask in [
        ("Housing unstable/at risk", comp["housing_status"].isin(["at_risk", "unstable"]), comp["housing_status"] != ""),
        ("Housing quality problem (of those with housing)", comp["housing_quality_pos"] == "Y", answered("housing_quality_pos")),
        ("Food", comp["food_pos"] == "Y", answered("food_pos")),
        ("Transportation", comp["transport_pos"] == "Y", answered("transport_pos")),
        ("Utilities (of those with housing)", comp["utilities_pos"] == "Y", answered("utilities_pos")),
        ("Interpersonal safety (of those asked privately)", comp["safety_pos"] == "Y", answered("safety_pos")),
        ("Safety deferred (no privacy)", comp["safety_pos"] == "deferred", comp["safety_pos"] != ""),
        ("Health literacy", comp["literacy_pos"] == "Y", answered("literacy_pos")),
        ("ID/documents", comp["id_docs_pos"] == "Y", answered("id_docs_pos")),
    ]:
        k, n = int(mask.sum()), int(den_mask.sum())
        hide = suppress and (0 < k < 5 or 0 < n - k < 5)
        rows.append(dict(domain=label, patients=("<5" if hide and k < 5 else str(k)), of=n,
                         pct=("—" if hide or n == 0 else f"{k / n:.0%}")))
    return pd.DataFrame(rows)


# --------------------------------------------------------------- charts ---
def run_chart(w: pd.DataFrame, col: str, den_col: str, title: str, target: float | None, path: Path) -> dict:
    base = w[w["phase"] == "baseline"][col].dropna()
    median = float(base.median()) if len(base) else float(w[col].median())
    values = [None if pd.isna(v) else float(v) for v in w[col]]
    rules = run_rules(values, median)

    fig, ax = plt.subplots(figsize=(10, 4.8))
    ax.plot(w["week"], w[col] * 100, marker="o", color="#1f4e79", lw=1.8, label=title)
    small = w[w[den_col] < MIN_WEEKLY_DENOM]
    if len(small):
        ax.scatter(small["week"], small[col] * 100, s=90, facecolors="none", edgecolors="orange",
                   lw=1.8, zorder=5, label=f"denominator < {MIN_WEEKLY_DENOM}")
    ax.axhline(median * 100, color="grey", ls="--", lw=1.2,
               label=f"baseline median {median:.0%}" + (" (provisional)" if len(base) < 10 else ""))
    if target is not None:
        ax.axhline(target * 100, color="green", ls=":", lw=1.4, label=f"target {target:.0%}")
    for i, (start, end, side) in enumerate(rules["shifts"]):
        ax.plot(w["week"].iloc[start:end + 1], w[col].iloc[start:end + 1] * 100, color="red", lw=3, alpha=.5,
                label="shift (≥6 points one side of median)" if i == 0 else None)
    starts = w.groupby("phase", sort=False)["week"].min()
    for ph, wk in starts.items():
        if ph != "baseline":
            ax.axvline(wk - 0.5, color="#888", lw=.8)
            ax.text(wk - 0.4, 102, ph.upper(), fontsize=8, va="bottom", color="#444")
    ax.set_ylim(0, 110)
    ax.set_xticks(w["week"])
    ax.set_xlabel("Project week")
    ax.set_ylabel("%")
    ax.set_title(title)
    ax.legend(loc="lower right", fontsize=8)
    ax.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return {"median": median, **rules}


def coverage_chart(s: pd.DataFrame, path: Path) -> pd.DataFrame:
    rows, seen, screened = [], set(), set()
    for wk, x in s.groupby("week"):
        seen |= set(x["patient_id"])
        screened |= set(x.loc[x["screen_status"] == "complete", "patient_id"])
        rows.append(dict(week=wk, seen=len(seen), screened=len(screened)))
    c = pd.DataFrame(rows)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(c["week"], c["seen"], marker="s", color="#999", label="patients seen (cumulative)")
    ax.plot(c["week"], c["screened"], marker="o", color="#1f4e79", label="patients with ≥1 complete screen")
    ax.set_xticks(c["week"])
    ax.set_xlabel("Project week")
    ax.set_ylabel("patients")
    ax.set_title("P1b Panel coverage")
    ax.legend(fontsize=8)
    ax.grid(alpha=.25)
    fig.tight_layout()
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return c


def funnel(s: pd.DataFrame, r: pd.DataFrame) -> pd.DataFrame:
    comp = s[s["screen_status"] == "complete"]
    n_pos = int(comp["positive_domains"].map(len).sum())
    rr = r[r["visit_id"].isin(comp["visit_id"])]
    acc = rr[rr["accepted"] == "Y"]
    return pd.DataFrame([
        ("Positive actionable domains (complete screens)", n_pos),
        ("Referrals offered", len(rr)),
        ("Referrals accepted", len(acc)),
        ("Follow-up documented (any time)", int((acc["followup_status"] != "pending").sum())),
        ("Connected", int((acc["followup_status"] == "connected").sum())),
    ], columns=["step", "count"])


# --------------------------------------------------------------- report ---
def fmt_pct(x: float) -> str:
    return "—" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.0%}"


def describe_rules(name: str, res: dict, weeks: pd.Series) -> str:
    parts = []
    for a, b, side in res["shifts"]:
        parts.append(f"shift {'above' if side > 0 else 'below'} median, weeks {weeks.iloc[a]}–{weeks.iloc[b]}")
    for a, b, d in res["trends"]:
        parts.append(f"trend {'up' if d > 0 else 'down'}, weeks {weeks.iloc[a]}–{weeks.iloc[b]}")
    return f"- **{name}** (baseline median {res['median']:.0%}): " + ("; ".join(parts) if parts else "no non-random signal detected")


def md_table(df: pd.DataFrame) -> str:
    cols = list(df.columns)
    lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for _, row in df.iterrows():
        lines.append("| " + " | ".join(str(row[c]) for c in cols) + " |")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--data-dir", default="data/synthetic")
    ap.add_argument("--out-dir", default="output")
    ap.add_argument("--strict", action="store_true", help="exit non-zero on validation errors")
    ap.add_argument("--no-suppress", action="store_true", help="show counts < 5 (synthetic data only)")
    args = ap.parse_args()

    data_dir, out = Path(args.data_dir), Path(args.out_dir)
    figs = out / "figures"
    figs.mkdir(parents=True, exist_ok=True)

    s, r, errors = load(data_dir)
    if errors:
        print(f"{len(errors)} validation issue(s):", file=sys.stderr)
        for e in errors[:50]:
            print("  -", e, file=sys.stderr)
        if args.strict:
            return 1
    if s.empty:
        print("No visits in screening_log.csv — nothing to analyze.", file=sys.stderr)
        return 1

    s = derive(s, r)
    w = weekly(s, r)
    res_p1 = run_chart(w, "P1", "visits", "P1 Visits with up-to-date social needs screen", .80, figs / "p1_up_to_date.png")
    res_p2 = run_chart(w, "P2", "p2_den", "P2 Positive screens offered referral for every need", .90, figs / "p2_referral_offered.png")
    res_p1a = run_chart(w, "P1a", "due", "P1a Due screens completed at visit", .80, figs / "p1a_due_completed.png")
    cov = coverage_chart(s, figs / "p1b_panel_coverage.png")
    pp = pre_post(s)
    fu = followup_measures(s, r)
    prev = prevalence(s, suppress=not args.no_suppress)
    fn = funnel(s, r)
    minutes = s.loc[s["screen_status"] == "complete", "minutes"].dropna()

    synthetic = "synthetic" in str(data_dir).lower()
    pp_disp = pp.assign(pct=pp["pct"].map(fmt_pct),
                        **{"95% CI": [f"{fmt_pct(a)}–{fmt_pct(b)}" for a, b in zip(pp["ci_low"], pp["ci_high"])]}
                        ).drop(columns=["ci_low", "ci_high"])
    w_disp = w[["week", "phase", "visits", "P1", "due", "P1a", "p2_den", "P2", "B1"]].copy()
    for c in ["P1", "P1a", "P2", "B1"]:
        w_disp[c] = w_disp[c].map(fmt_pct)
    fu_disp = fu.reset_index().assign(O1=lambda d: d["O1"].map(fmt_pct), O2=lambda d: d["O2"].map(fmt_pct))

    report = [
        "# QI Measure Summary",
        "",
        ("> ⚠️ **SYNTHETIC DATA — for demonstration only. Not real patients; do not cite.**\n" if synthetic else ""),
        f"Data: `{data_dir}` · visits: {len(s)} ({int((~s['included']).sum())} excluded) · patients: {s['patient_id'].nunique()} · "
        f"weeks: {int(w['week'].min())}–{int(w['week'].max())} · referrals: {len(r)}",
        "",
        f"Validation issues: {len(errors)}",
        "",
        "## Run chart signals (Perla et al. 2011 rules)",
        describe_rules("P1", res_p1, w["week"]),
        describe_rules("P1a", res_p1a, w["week"]),
        describe_rules("P2", res_p2, w["week"]),
        "",
        "![P1](figures/p1_up_to_date.png)",
        "![P1a](figures/p1a_due_completed.png)",
        "![P2](figures/p2_referral_offered.png)",
        "![P1b](figures/p1b_panel_coverage.png)",
        "",
        "## Baseline vs. intervention (descriptive, Wilson 95% CI)",
        md_table(pp_disp),
        "",
        f"**B2 Screening time:** median {minutes.median():.0f} min (IQR {minutes.quantile(.25):.0f}–{minutes.quantile(.75):.0f}), n={len(minutes)}"
        if len(minutes) else "**B2 Screening time:** no data",
        "",
        f"## Follow-up (accepted referrals ≥ {FOLLOWUP_WINDOW_DAYS} days old, grouped by phase of referral)",
        md_table(fu_disp),
        "",
        "## Referral funnel",
        md_table(fn),
        "",
        "## Need prevalence (latest complete screen per patient)",
        md_table(prev),
        "",
        f"P1b panel coverage at final week: {int(cov['screened'].iloc[-1])}/{int(cov['seen'].iloc[-1])} patients.",
        "",
        "## Weekly data",
        md_table(w_disp),
        "",
    ]
    (out / "summary.md").write_text("\n".join(report))
    w.to_csv(out / "weekly_measures.csv", index=False)
    print(f"Wrote {out / 'summary.md'} and {len(list(figs.glob('*.png')))} figures to {figs}/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
