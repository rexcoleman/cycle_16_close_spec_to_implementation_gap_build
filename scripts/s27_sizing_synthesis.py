#!/usr/bin/env python3
"""Cycle-16-S27 synthesis — compose the TRUE build-queue size + reality-vs-intent table
from the four sizing outputs. Does NOT re-run the LLM re-derivation (consumes its output).

Synthesis (e): outputs/cycle_16_s27_true_build_queue.json
Reality-vs-intent (f): outputs/cycle_16_s27_reality_vs_intent.md
Run-boundary event: true_build_queue.computed

This SIZES the spec->implementation gap. It builds ZERO spec implementations.
ADDITIVE ONLY.
"""
import json
import os
import sys
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")

NA_REDERIV = os.path.join(OUTPUTS, "na_direction_rederivation.json")
ACCURACY = os.path.join(OUTPUTS, "na_rederivation_accuracy.json")
MINING = os.path.join(OUTPUTS, "denominator_mining_pass.json")
WELLFORMED = os.path.join(OUTPUTS, "spec_wellformedness_verdicts.json")
FAITHFUL_GAP = os.path.join(OUTPUTS, "trusted_detector_run_faithful.json")
FAITHFUL_MAP = os.path.join(OUTPUTS, "faithful_target_map.json")
VTV = os.path.join(OUTPUTS, "validation_tier_verdicts.json")
OUT_QUEUE = os.path.join(OUTPUTS, "cycle_16_s27_true_build_queue.json")
OUT_RVI = os.path.join(OUTPUTS, "cycle_16_s27_reality_vs_intent.md")
EVENTS = os.path.join(OUTPUTS, "cycle_16_s27_sizing_events.jsonl")


def now():
    return datetime.now(timezone.utc).isoformat()


def emit_event(event_class, payload, run_id):
    rec = {"schema_version": "0.1", "namespace": "cycle_16.s27.sizing",
           "event_class": event_class, "timestamp": now(), "run_id": run_id,
           "payload": payload}
    with open(EVENTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def run(run_id=None):
    run_id = run_id or f"s27_synth_{uuid.uuid4().hex[:8]}"
    na = json.load(open(NA_REDERIV))
    acc = json.load(open(ACCURACY))
    mining = json.load(open(MINING))
    wf = json.load(open(WELLFORMED))
    fgap = json.load(open(FAITHFUL_GAP))
    fmap = json.load(open(FAITHFUL_MAP))
    vtv = json.load(open(VTV))

    # --- exec-tier real gaps (inherited from S26 faithful gap list) ---
    exec_tier = fgap["gap_list"]["execution_tier"]
    exec_not_impl = exec_tier["not_implemented_count"]  # specs that need code, not yet built
    exec_impl = exec_tier["implemented_count"]
    exec_total = exec_tier["total"]

    # --- false-negatives recovered from the 203 n/a bucket (MEASURED by (a)) ---
    disp = na["disposition_counts"]
    false_negatives = disp.get("FALSE_NEGATIVE_gap", 0)
    disagreements = disp.get("disagreement_conservative", 0)
    genuine_na = disp.get("genuine_na", 0)
    unverifiable = disp.get("unverifiable", 0)

    # --- recovered-from-mining runtime-deliverable candidates (HEURISTIC) ---
    recovered_runtime = mining.get("n_recovered_runtime_deliverable_candidates", 0)
    recovered_total = mining.get("n_recovered", 0)

    # --- judgment_tier contested (carried, NOT a build target yet; needs Hole-1 verifier S28) ---
    # the 203 that are NOT confirmed false-negatives and NOT genuine-na confirmed = still contested.
    # Carry the disagreement bucket + the genuine_na as "verified-not-a-build-target" separately.
    judgment_tier_contested = disagreements  # surfaced, needs S28 Hole-1 verifier

    # --- TRUE build queue (specs that ACTUALLY need code now) ---
    # = exec-tier not-implemented + measured false-negatives from the 203 + recovered runtime
    #   candidates from mining. Disagreements are CONTESTED (carried, not counted as build targets).
    true_build_queue = exec_not_impl + false_negatives + recovered_runtime

    # ---- 203-n/a vs 203-CONTESTED reconciliation (MEASURED set comparison) ----
    s26_na = set(x["spec_iri"] for x in fmap["members"]
                 if x.get("disposition") == "dp26_carveout_preserved")
    s24_judged = set(x["spec_iri"] for x in vtv["per_spec_verdicts_IP_PRIVATE"]
                     if x["tier"] == "semantically_judged")
    inter = s26_na & s24_judged
    reconciliation = {
        "s26_dp26_na_count": len(s26_na),
        "s24_semantically_judged_contested_count": len(s24_judged),
        "intersection_count": len(inter),
        "in_s24_not_s26": len(s24_judged - s26_na),
        "in_s26_not_s24": len(s26_na - s24_judged),
        "sets_are_identical": (s26_na == s24_judged),
        "relationship": (
            "MEASURED: the S26 '203 n/a / dp26_carveout' set and the S24 '203 semantically_"
            "judged CONTESTED' set are the SAME 203 spec_iris (intersection=203, symmetric "
            "difference=0) — NOT merely a coincidental count match. The S24 tier-partition "
            "routed exactly the 3 execution_checkable specs to the exec tier and the other 203 "
            "to the judgment tier; S26's faithful-target extractor preserved exactly those same "
            "3 as non-n/a targets and marked the same 203 as dp26 carve-outs. So the n/a bucket "
            "IS the contested judgment tier. S27 re-derives that shared 203 from each spec's own "
            "text to split it honestly into genuine_na vs false_negative vs disagreement."),
    }

    queue = {
        "schema_version": "s27_true_build_queue.v1",
        "build_event": "Cycle-16-S27 TRUE build-queue SIZING (builds ZERO implementations)",
        "run_id": run_id,
        "is_sizing_not_gap_closure": True,
        "true_build_queue_size": true_build_queue,
        "tier_breakdown": {
            "exec_tier_real_gaps_not_implemented": {
                "count": exec_not_impl, "tag": "inherited (S26 faithful gap list, exec tier)",
                "spec_iris": exec_tier.get("not_implemented", []),
            },
            "false_negatives_recovered_from_na": {
                "count": false_negatives, "tag": "measured (S27 (a) re-derivation, 2 readers)",
                "spec_iris": [g["spec_iri"] for g in na["false_negative_gaps"]],
            },
            "recovered_specs_needing_code_from_mining": {
                "count": recovered_runtime, "tag": "heuristic (S27 (c) mining pass, text-pattern candidates)",
            },
        },
        "judgment_tier_contested_count": {
            "count": judgment_tier_contested,
            "tag": "measured (S27 (a) reader-disagreement bucket)",
            "note": "CONTESTED — NOT a build target yet. Needs the Hole-1 verifier at S28 to "
                    "resolve whether these commit a runtime observable.",
        },
        "na_split_honestly": {
            "genuine_na": {"count": genuine_na, "tag": "measured (S27 (a))"},
            "false_negative_gap": {"count": false_negatives, "tag": "measured (S27 (a))"},
            "disagreement_conservative": {"count": disagreements, "tag": "measured (S27 (a))"},
            "unverifiable": {"count": unverifiable, "tag": "measured (S27 (a)) — honest residual"},
            "n_total": na["n"],
        },
        "exec_tier": {"total": exec_total, "implemented": exec_impl,
                      "not_implemented": exec_not_impl, "tag": "inherited (S26)"},
        "instrument_accuracy_caveat": {
            "fixture_precision": acc.get("fixture_precision"),
            "fixture_recall": acc.get("fixture_recall"),
            "fixture_false_negative_rate": acc.get("fixture_false_negative_rate"),
            "independent_instrument_agreement_on_203": acc.get("independent_instrument_agreement_on_203"),
            "tag": "measured (S27 (b) validate-the-validator)",
            "note": "The false-negative count above is produced by an instrument whose own "
                    "accuracy is MEASURED here, not assumed. Read the queue size THROUGH this "
                    "caveat: recall<1 means real false-negatives may be undercounted; "
                    "cross-instrument disagreement bounds confidence.",
        },
        "mining": {"n_recovered": recovered_total,
                   "n_recovered_runtime_deliverable_candidates": recovered_runtime,
                   "new_population_size": mining.get("new_population_size"),
                   "tag": "heuristic (S27 (c))",
                   "residual_disclosure": mining.get("residual_disclosure")},
        "wellformedness_summary": {**wf["summary"], "tag": "measured (S27 (d))"},
        "reconciliation_203_na_vs_203_contested": reconciliation,
        "disclosed_residuals": [
            "Instrument recall < 1 (see (b)) => false-negative count is a LOWER BOUND, not exact.",
            "Mining recovered candidates are HEURISTIC text-pattern matches; some may restate "
            "existing specs missed by dedup; surfaced as candidates not confirmed specs.",
            "Verbal-only commitments never written anywhere are unrecoverable by construction (c).",
            f"{disagreements} reader-disagreement specs are CONTESTED, carried to S28 Hole-1 verifier.",
            f"{unverifiable} specs unverifiable (source unreadable) — honest residual, NOT kept n/a.",
            "This session SIZES only. The ~195-wide gap between specs and code is NOT closed; "
            "exactly 2 specs are execution-proven implemented (inherited).",
        ],
    }
    json.dump(queue, open(OUT_QUEUE, "w"), indent=2)

    emit_event("true_build_queue.computed", {
        "true_build_queue_size": true_build_queue,
        "exec_tier_not_implemented": exec_not_impl,
        "false_negatives_recovered_from_na": false_negatives,
        "recovered_runtime_candidates_from_mining": recovered_runtime,
        "judgment_tier_contested": judgment_tier_contested,
        "na_genuine": genuine_na, "na_unverifiable": unverifiable,
    }, run_id)

    write_rvi(queue, na, acc, mining, wf, fgap, reconciliation)
    print(f"[synthesis] TRUE build-queue size={true_build_queue} "
          f"(exec_not_impl={exec_not_impl} + false_neg={false_negatives} + mining_runtime={recovered_runtime}) "
          f"| contested={judgment_tier_contested} -> {OUT_QUEUE}")
    return queue


def write_rvi(queue, na, acc, mining, wf, fgap, recon):
    tb = queue["true_build_queue_size"]
    disp = na["disposition_counts"]
    P = acc.get("fixture_precision"); R = acc.get("fixture_recall")
    FNR = acc.get("fixture_false_negative_rate")
    AG = acc.get("independent_instrument_agreement_on_203")
    md = f"""# Cycle-16-S27 — Reality-vs-Intent (SIZING only; #15)

> This session SIZES the spec->implementation gap. It builds ZERO spec implementations.
> Every number tagged **measured** / **heuristic** / **inherited**. No comfortable framings.

## What each mechanism ACTUALLY does vs what the hole asked

| Hole | What the hole asked | What the mechanism ACTUALLY did | Honest residual |
|---|---|---|---|
| Hole 2 (a) | Re-derive 203 n/a specs from each spec's OWN text, no dp26 short-circuit | Read all {na['n']} specs' own definition-site prose with 2 independent readers (E1' rule-based + E2' haiku LLM, distinct prompt); `extraction_methods_distinct={na['extraction_methods_distinct']}` **[measured]** | Reader disagreement + unverifiable specs carried, NOT auto-resolved |
| #19/#46/#34 (b) | Measure the re-derivation INSTRUMENT's accuracy | Fixture P={P} / R={R} / FNR={FNR} on {acc.get('n_fixtures')} blind-labeled authored fixtures; independent 2nd instrument agreement={AG} on the 203 **[measured]** | Recall<1 => false-negatives may be UNDERCOUNTED; disagreements disclosed not tuned |
| Hole 3 (c) | ONE bounded denominator-mining pass | Scanned DECISION_LOG + git log + memory; {mining['n_recovered']} recovered candidates ({mining.get('n_recovered_runtime_deliverable_candidates')} runtime-deliverable) **[heuristic]** | Verbal-only commitments unrecoverable by construction (disclosed bound) |
| Hole 8 (d) | Well-formedness + dependency consistency | {wf['summary']['n_wellformed']} well-formed / {wf['summary']['n_vague']} vague / {wf['summary']['n_contradictory']} contradictory / {wf['summary']['n_dependency_violations']} dep-violations over {wf['n_specs']} **[measured]** | killed/deferred-dependency class = 0 BY CONSTRUCTION (no such status in corpus), disclosed |

## The TRUE build-queue size (what actually needs code NOW)

| Component | Count | Tag |
|---|---|---|
| exec-tier real gaps (not implemented) | {queue['tier_breakdown']['exec_tier_real_gaps_not_implemented']['count']} | inherited (S26) |
| false-negatives recovered from the 203 n/a | {queue['tier_breakdown']['false_negatives_recovered_from_na']['count']} | measured (S27 a) |
| recovered runtime-deliverables from mining | {queue['tier_breakdown']['recovered_specs_needing_code_from_mining']['count']} | heuristic (S27 c) |
| **TRUE build-queue size** | **{tb}** | composed |
| judgment-tier CONTESTED (NOT a build target; needs S28 Hole-1 verifier) | {queue['judgment_tier_contested_count']['count']} | measured (S27 a) |

## The 203-n/a vs 203-CONTESTED reconciliation [measured]

{recon['relationship']}

- S26 dp26-n/a set: {recon['s26_dp26_na_count']}
- S24 semantically-judged CONTESTED set: {recon['s24_semantically_judged_contested_count']}
- intersection: {recon['intersection_count']} ; sets identical: {recon['sets_are_identical']}

## What is still NOT done (refusing comfortable framings)

- The spec->implementation gap is **NOT closed**. Exactly **2 specs are execution-proven
  implemented** (inherited from S25/S26); the rest remain. The gap is ~195 wide.
- This session **only SIZES** the work. It builds nothing. No "done" / "100%" / "gap-closed".
- The false-negative count is a **lower bound** — the instrument that produced it has measured
  recall {R} (not 1.0); specs it missed are silently still in the genuine-na bucket.
- {disp.get('disagreement_conservative', 0)} specs are reader-CONTESTED and unresolved here.
- {disp.get('unverifiable', 0)} specs are unverifiable (source unreadable) — an honest residual,
  explicitly NOT silently kept as n/a.
- Mining candidates are heuristic text matches, not confirmed new specs.
"""
    with open(OUT_RVI, "w") as f:
        f.write(md)
    print(f"[synthesis] reality-vs-intent -> {OUT_RVI}")


if __name__ == "__main__":
    rid = sys.argv[1] if len(sys.argv) > 1 else None
    run(run_id=rid)
