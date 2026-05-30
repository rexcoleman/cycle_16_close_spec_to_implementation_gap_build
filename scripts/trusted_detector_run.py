#!/usr/bin/env python3
"""Cycle-16-S24 BE-T part (ii) — trusted-detector run over the validated set V (#47).

Runs the trusted execution-tier detectors over the reconciled validated commitment set V
(`outputs/validated_commitment_set.json`, NOT a single-reader BE-D scan), tier-labelling
each verdict per BE-S (`validation_tier_verdict.close_verdict`). Emits the per-spec
spec->implementation GAP LIST.

Acceptance: ED §5.phase11.3 BE-T thresholds 3-6.
  T3: detector_input_path == validated_commitment_set.json + detector_input_is_reconciled
      _validated_set:true (single-reader BE-D scan REFUSED).
  T4: per-spec implemented / not-implemented / contested + validation tier; aggregate rate
      [measured] + tier-partitioned; CONTESTED specs NOT counted as implemented.
  T5: probe_accuracy_harness --self-test independence_clean==true BEFORE accepting the run;
      carried into the output. If not clean -> REFUSE.
  T6: any "100%" scoped to the discoverable population + residual R + tier-labelled; the
      §1ee-class honest gaps disclosed verbatim. No un-scoped "100%".

The honest gap list IS the deliverable. The implemented-rate is [measured], never engineered.
"""
from __future__ import annotations

import argparse
import json
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = REPO / "outputs"
sys.path.insert(0, str(HERE))

import validation_tier_verdict as BES  # noqa: E402

V_JSON = OUTPUTS / "validated_commitment_set.json"
BE_D_SCAN = OUTPUTS / "retroactive_scan_cycle_1_15_run.json"
DENOM_JSON = OUTPUTS / "denominator_dual_method.json"
GUARD_POP_JSON = OUTPUTS / "guard_the_guards_population.json"
BES_VERDICTS = OUTPUTS / "validation_tier_verdicts.json"
HARNESS = HERE / "probe_accuracy_harness.py"
RUN_OUT = OUTPUTS / "trusted_detector_run.json"

# §1ee-class honest gaps disclosed VERBATIM (HC #70, T6).
HONEST_GAPS_VERBATIM = [
    "6/9 AgentContracts have no executable observable (DP#26 carve-out — most AgentContracts commit no emitted runtime_emit_event_class).",
    "3/10 KG ontologies have no SHACL shapes (Class B CONTESTED — the probe aggregate path never target-class-checks despite real conforming instances).",
    "228/232 E-status are not independently re-derivable (Class E status-match CONTESTED, contested_fraction 0.9828 — only n_eval=4 status pairs independently derivable).",
]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _assert_independence() -> dict:
    """T5: re-assert harness independence BEFORE accepting the run (validate-the-validator)."""
    proc = subprocess.run([sys.executable, str(HARNESS), "--self-test"],
                          capture_output=True, text=True, timeout=60)
    clean = False
    att = {}
    try:
        att = json.loads(proc.stdout)
        clean = bool(att.get("independence_clean")) and proc.returncode == 0
    except json.JSONDecodeError:
        pass
    return {"independence_clean": clean, "self_test_rc": proc.returncode,
            "attestation": att}


def _v_manifest() -> dict:
    v = json.loads(V_JSON.read_text())
    return {"detector_input_path": "outputs/validated_commitment_set.json",
            "detector_input_is_reconciled_validated_set": bool(v.get("detector_input_is_reconciled_validated_set")),
            "v_size_commitments": v.get("v_size"),
            "v_distinct_spec_ids": len({m["spec_id"] for m in v["members"]}),
            "aggregate_jaccard": v.get("aggregate_jaccard"),
            "wired_to_be_d_single_reader_scan": False,
            "reconciliation_rule": v.get("reconciliation_rule")}


# ---------------------------------------------------------------------------
# Cycle-16-S24 NARROW DISCLOSURE RE-EMIT (additive ONLY; no verdict change,
# no detector re-run). The blocks below are computed from artifacts already on
# disk — the BE-D scan `cycle_authored` join + the denominator + the
# guard-the-guards population. They ADD reconciliation/disclosure fields; they
# change NO per-spec verdict and re-fire NO detector. (kc-54 R3 disposition.)
# ---------------------------------------------------------------------------

def _scan_cycle_map() -> dict:
    """spec_id -> cycle_authored, from the BE-D retroactive scan (join key)."""
    scan = json.loads(BE_D_SCAN.read_text())
    return {p["spec_id"]: p.get("cycle_authored")
            for p in scan["per_spec_evidence_IP_PRIVATE"]}


def _era_partition(verdicts: list, cycle_map: dict) -> dict:
    """Partition the EXISTING per-spec verdicts by authorship era + tier.

    Re-uses the verdicts byte-identically (no re-classification): each spec's
    tier/verdict/implemented are taken as-is; we only split by era. The
    judgment-tier predicates are IDENTICAL to run()'s (VALIDATED-JUDGMENT /
    NOT-VALIDATED / CONTESTED). Past = cycle_authored<=15; present = ==16.
    """
    def era_of(iri):
        c = cycle_map.get(iri)
        if isinstance(c, int) and c <= 15:
            return "cycles_1_15_past"
        if c == 16:
            return "cycle_16_present_in_flight"
        return None

    out = {}
    for era in ("cycles_1_15_past", "cycle_16_present_in_flight"):
        sub = [v for v in verdicts if era_of(v["spec_iri"]) == era]
        execs = [v for v in sub if v["tier"] == "execution_checkable"]
        judg = [v for v in sub if v["tier"] == "semantically_judged"]
        ex_impl = [v for v in execs if v["implemented"]]
        ex_not = [v for v in execs if (not v["implemented"]) and v not in ex_impl]
        ju_impl = [v for v in judg if v["implemented"] and v["verdict"] == "VALIDATED-JUDGMENT"]
        ju_not = [v for v in judg if v["verdict"] == "NOT-VALIDATED" and not v["implemented"]]
        ju_con = [v for v in judg if v["verdict"] == "CONTESTED"]
        n = len(sub)
        agg_impl = len(ex_impl) + len(ju_impl)
        out[era] = {
            "n": n,
            "label": ("past — cycles 1-15 authored, retroactively scanned"
                      if era == "cycles_1_15_past"
                      else "present/in-flight — cycle-16-authored (self-audit; guard-the-guards #22/#47)"),
            "execution_tier": {
                "total": len(execs),
                "implemented": len(ex_impl),
                "not_implemented": len(ex_not),
            },
            "judgment_tier": {
                "total": len(judg),
                "diverse_judge_validated_implemented": len(ju_impl),
                "diverse_judge_not_implemented": len(ju_not),
                "contested_not_counted": len(ju_con),
            },
            "aggregate_implemented_count": agg_impl,
            "aggregate_implemented_rate_tier_partitioned": round(agg_impl / n, 4) if n else None,
        }
    return out


def _three_population_reconciliation(v_distinct: int, cycle_map: dict, v_ids: set) -> dict:
    """Reconcile M1' (193 disclosed-bound) / V (206=167+39) / guard-pop (230=193+37 infra)."""
    denom = json.loads(DENOM_JSON.read_text())["method_1_recorded"]
    guard = json.loads(GUARD_POP_JSON.read_text())
    m1_prime = denom["m1_cycles_1_15_records"]                 # 193
    m1_c16_excl = denom["m1_cycle16_authored_excluded"]        # 39
    # V split by era via the scan join (re-derived, not taken on faith).
    v_le15 = {i for i in v_ids if isinstance(cycle_map.get(i), int) and cycle_map[i] <= 15}
    v_eq16 = {i for i in v_ids if cycle_map.get(i) == 16}
    coverage = round(len(v_le15) / m1_prime, 4) if m1_prime else None
    infra = guard["infra_entry_count"]                         # 37
    guard_pop = guard["audited_population_count"]              # 230
    # Re-derive + assert the arithmetic ties out before disclosing.
    assert m1_prime == 193, m1_prime
    assert len(v_le15) == 167, len(v_le15)
    assert len(v_eq16) == 39 == m1_c16_excl, (len(v_eq16), m1_c16_excl)
    assert len(v_le15) + len(v_eq16) == v_distinct == 206, (len(v_le15), len(v_eq16), v_distinct)
    assert m1_prime + infra == guard_pop == 230, (m1_prime, infra, guard_pop)
    return {
        "M1_prime_disclosed_bound": {
            "value": m1_prime,
            "definition": "cycles 1-15 disclosed-bound denominator (frozen-unit, post-grain-pin); excludes the 39 cycle-16-authored specs.",
        },
        "V_gap_list_input": {
            "value": v_distinct,
            "composition": f"{len(v_le15)} (of the {m1_prime} cycles-1-15 disclosed-bound) + {len(v_eq16)} (cycle-16-authored, present/self-audit) = {v_distinct}",
            "cycles_1_15_distinct": len(v_le15),
            "cycle_16_distinct": len(v_eq16),
            "cycles_1_15_coverage_of_disclosed_bound": coverage,
            "coverage_note": f"{len(v_le15)}/{m1_prime} = {coverage} ({round(coverage*100,1)}%) of the disclosed-bound denominator is covered by V; the rest is the {m1_prime - len(v_le15)}-absent extraction-coverage gap (see absent_disclosed_bound_finding).",
        },
        "guard_pop": {
            "value": guard_pop,
            "composition": f"{m1_prime} disclosed-bound + {infra} enforcement-infra = {guard_pop}",
            "infra_count": infra,
            "infra_count_by_class": guard.get("infra_count_by_class"),
            "distinct_from_V_cycle16_note": (
                f"This {infra}-infra cut (6 probes / 21 gates / 9 agent_specs / 1 harness, each --self-test-audited; "
                f"{infra} fire-events) is DISTINCT from V's {len(v_eq16)} cycle-16 SPECS. "
                "Overlapping-but-not-equal: enforcement-infra surfaces vs authored specs — do NOT conflate the two cuts."
            ),
        },
        "reconciliation_assertions": {
            "m1_prime_eq_193": True,
            "v_cycles_1_15_eq_167": True,
            "v_cycle16_eq_39_eq_excluded": True,
            "v_split_sums_to_206": True,
            "guard_pop_eq_193_plus_37_eq_230": True,
        },
        "tag": "[measured] — every value re-derived from the scan cycle_authored join + denominator + guard-pop on disk.",
    }


def _absent_disclosed_bound_finding(cycle_map: dict, v_ids: set) -> dict:
    """The 26 cycles-1-15 disclosed-bound specs (cycle_authored<=15) ABSENT from V."""
    scan_le15 = {sid for sid, c in cycle_map.items() if isinstance(c, int) and c <= 15}
    absent = sorted(scan_le15 - v_ids)
    assert len(absent) == 26, len(absent)  # 193 - 167
    return {
        "absent_count": len(absent),
        "derivation": "193 (scan cycle_authored<=15 distinct = M1') - 167 (V cycles-1-15 distinct) = 26",
        "absent_spec_ids": absent,
        "framing": (
            "extraction-coverage gap (#28) — specs the gap list cannot speak to because extraction "
            "(E1/E2/E1') did not cover them; disclosed, not hidden, NOT counted as implemented or "
            "not-implemented. This is itself an honest coverage finding."
        ),
        "tag": "[measured]",
    }


def run(use_cached_bes: bool = True) -> dict:
    # T5 FIRST: refuse the run if independence is not clean (the prober would be its own proxy).
    indep = _assert_independence()
    if not indep["independence_clean"]:
        raise SystemExit("REFUSED: harness independence not clean — the prober would be its own proxy (BE-T T5).")

    # T3: detector input == reconciled V (single-reader BE-D scan REFUSED).
    manifest = _v_manifest()
    if not manifest["detector_input_is_reconciled_validated_set"]:
        raise SystemExit("REFUSED: detector input is not the reconciled validated set V (BE-T T3).")

    # Get the BE-S per-spec tier-labelled verdicts (reuse the cached run if present + complete).
    bes = None
    if use_cached_bes and BES_VERDICTS.exists():
        bes = json.loads(BES_VERDICTS.read_text())
        v_ids = {m["spec_id"] for m in json.loads(V_JSON.read_text())["members"]}
        covered = {v["spec_iri"] for v in bes["per_spec_verdicts_IP_PRIVATE"]}
        if not v_ids.issubset(covered):
            bes = None  # incomplete cache -> recompute
    if bes is None:
        bes = BES.run_all()

    verdicts = bes["per_spec_verdicts_IP_PRIVATE"]
    edge_ids = set(bes["single_reader_edge_spec_ids"])

    # Partition the gap list by tier + verdict.
    exec_specs = [v for v in verdicts if v["tier"] == "execution_checkable"]
    judg_specs = [v for v in verdicts if v["tier"] == "semantically_judged"]

    exec_implemented = [v for v in exec_specs if v["implemented"]]
    exec_not_impl = [v for v in exec_specs if (v["verdict"] in ("PASS-LOW-POWER", "VALIDATED-FULL-RIGOR")) and not v["implemented"]]
    exec_contested = [v for v in exec_specs if v["verdict"] in ("NOT-VALIDATED", "CONTESTED") and v["verdict"] != "PASS-LOW-POWER" and not v["implemented"] and v not in exec_not_impl]
    # (an execution spec that produced no probe fire -> NOT-VALIDATED -> contested)
    exec_contested = [v for v in exec_specs if v not in exec_implemented and v not in exec_not_impl]

    judg_implemented = [v for v in judg_specs if v["implemented"] and v["verdict"] == "VALIDATED-JUDGMENT"]
    judg_not_impl = [v for v in judg_specs if v["verdict"] == "NOT-VALIDATED" and not v["implemented"]]
    judg_contested = [v for v in judg_specs if v["verdict"] == "CONTESTED"]

    total = len(verdicts)
    # Tier-partitioned implemented-rate. CONTESTED specs are NOT counted as implemented.
    exec_rate = round(len(exec_implemented) / len(exec_specs), 4) if exec_specs else None
    # Aggregate implemented over the WHOLE V (execution-implemented + judgment-validated-implemented),
    # tier-disclosed (the judgment tier carries the diverse-judge residual).
    agg_implemented = len(exec_implemented) + len(judg_implemented)
    agg_rate_all = round(agg_implemented / total, 4) if total else None
    # The EXECUTION-PROVEN rate (the only tier with a behavioral observable) over V.
    exec_proven_rate = round(len(exec_implemented) / total, 4) if total else None

    gap_list = {
        "execution_tier": {
            "total": len(exec_specs),
            "implemented": [v["spec_iri"] for v in exec_implemented],
            "not_implemented": [v["spec_iri"] for v in exec_not_impl],
            "contested": [v["spec_iri"] for v in exec_contested],
            "implemented_count": len(exec_implemented),
            "not_implemented_count": len(exec_not_impl),
            "contested_count": len(exec_contested),
            "tier_label": "PASS-LOW-POWER (F-detector accuracy n_eval=2 per §1ee — NOT FULL-RIGOR)",
        },
        "judgment_tier": {
            "total": len(judg_specs),
            "diverse_judge_validated_implemented": len(judg_implemented),
            "diverse_judge_not_implemented": len(judg_not_impl),
            "contested_not_counted": len(judg_contested),
            "contested_fraction": round(len(judg_contested) / len(judg_specs), 4) if judg_specs else None,
            "tier_label": "diverse-agreeing-judge with fail-safe; CONTESTED -> NOT counted as implemented",
        },
    }

    # -----------------------------------------------------------------
    # Cycle-16-S24 NARROW DISCLOSURE RE-EMIT (additive; computed from
    # artifacts on disk via the scan cycle_authored join). No verdict
    # change, no detector re-run.
    # -----------------------------------------------------------------
    cycle_map = _scan_cycle_map()
    v_ids = {m["spec_id"] for m in json.loads(V_JSON.read_text())["members"]}
    three_pop = _three_population_reconciliation(total, cycle_map, v_ids)
    absent_finding = _absent_disclosed_bound_finding(cycle_map, v_ids)
    per_era = _era_partition(verdicts, cycle_map)
    # Era partition MUST reconcile to the aggregate gap_list (past+present == aggregate).
    _pe_past, _pe_pres = per_era["cycles_1_15_past"], per_era["cycle_16_present_in_flight"]
    assert (_pe_past["execution_tier"]["implemented"] + _pe_pres["execution_tier"]["implemented"]
            == len(exec_implemented)), "era exec-impl != aggregate"
    assert (_pe_past["execution_tier"]["not_implemented"] + _pe_pres["execution_tier"]["not_implemented"]
            == len(exec_not_impl)), "era exec-not != aggregate"
    assert (_pe_past["judgment_tier"]["diverse_judge_validated_implemented"]
            + _pe_pres["judgment_tier"]["diverse_judge_validated_implemented"]
            == len(judg_implemented)), "era judg-val != aggregate"
    assert (_pe_past["judgment_tier"]["diverse_judge_not_implemented"]
            + _pe_pres["judgment_tier"]["diverse_judge_not_implemented"]
            == len(judg_not_impl)), "era judg-not != aggregate"
    assert (_pe_past["judgment_tier"]["contested_not_counted"]
            + _pe_pres["judgment_tier"]["contested_not_counted"]
            == len(judg_contested)), "era judg-contested != aggregate"
    assert _pe_past["n"] + _pe_pres["n"] == total, "era n != V total"

    _cov = three_pop["V_gap_list_input"]["cycles_1_15_coverage_of_disclosed_bound"]
    updated_close_claim = (
        "Three populations reconciled (cycles 1-16, era-disclosed): "
        "M1'=193 (cycles-1-15 disclosed-bound denominator) / "
        f"V={total}=167+39 (167 of the 193 cycles-1-15 [coverage {_cov}={round(_cov*100,1)}%] "
        "+ 39 cycle-16-authored present/self-audit) / "
        "guard-pop=230=193+37 (37 enforcement-infra, DISTINCT from V's 39 cycle-16 specs). "
        f"26 cycles-1-15 disclosed-bound specs (193-167) are ABSENT from V — an extraction-coverage gap (#28), "
        "disclosed, NOT counted implemented-or-not. "
        "Per-era tier-partitioned [measured]: cycles-1-15 PAST n=167 -> exec "
        f"{_pe_past['execution_tier']['implemented']} impl/{_pe_past['execution_tier']['not_implemented']} not, "
        f"judgment {_pe_past['judgment_tier']['diverse_judge_validated_implemented']} validated/"
        f"{_pe_past['judgment_tier']['diverse_judge_not_implemented']} not/"
        f"{_pe_past['judgment_tier']['contested_not_counted']} contested-not-counted "
        f"(agg-impl-rate {_pe_past['aggregate_implemented_rate_tier_partitioned']}); "
        "cycle-16 PRESENT/IN-FLIGHT n=39 -> exec "
        f"{_pe_pres['execution_tier']['implemented']} impl/{_pe_pres['execution_tier']['not_implemented']} not, "
        f"judgment {_pe_pres['judgment_tier']['diverse_judge_validated_implemented']} validated/"
        f"{_pe_pres['judgment_tier']['diverse_judge_not_implemented']} not/"
        f"{_pe_pres['judgment_tier']['contested_not_counted']} contested-not-counted "
        f"(agg-impl-rate {_pe_pres['aggregate_implemented_rate_tier_partitioned']}). "
        f"Era counts sum to the aggregate: execution-proven {len(exec_implemented)} implemented / "
        f"{len(exec_not_impl)} not-implemented (PASS-LOW-POWER); judgment tier {len(judg_specs)} specs with "
        f"{len(judg_contested)} CONTESTED->not-counted; aggregate implemented {agg_implemented}/{total}={agg_rate_all}. "
        "Every percentage is tier-scoped + era-disclosed to the discoverable population; no un-scoped, "
        "no uniform-100%% completion claim."
    ).replace("%%", "%")

    out = {
        "schema_version": "be_t_trusted_detector_run.v1",
        "build_event": "BE-T part (ii) — trusted-detector run over V; the spec->implementation gap list (Cycle-16-S24)",
        "timestamp": _now(),
        # T5
        "independence_clean": indep["independence_clean"],
        "independence_attestation": indep["attestation"],
        # T3
        "detector_input_path": manifest["detector_input_path"],
        "detector_input_is_reconciled_validated_set": manifest["detector_input_is_reconciled_validated_set"],
        "detector_input_manifest": manifest,
        # carried-forward residuals (§5)
        "denominator_disclosed_bound": "M1'=193 disclosed-bound (NOT a clean all-specs); residual R disclosed, never zeroed.",
        "classification_surplus_residual": "+53 DesignDecision classification-surplus (M3 raw-census 172 vs M1 classified 119); the gap list runs over the trusted V, not the raw census.",
        "single_reader_edge_spec_ids": sorted(edge_ids),
        "single_reader_edge_caveat": "These 6 structured-form specs have rule-based second-reader solo==0 (E1 subset of E2) -> effectively SINGLE-READER; any 'implemented' verdict on them rests on ONE reader's extraction. Identity confirmed: 2 bare-date degenerate (paradigm_dispositions:disposition_date, p=0.0) + 4 at p~=0.44 (decisions_log entries).",
        "be_j_3388_not_promoted": "BE-J's 33.88% is SUSPECT and is NOT carried as a trusted rate here.",
        # T4 — THE GAP LIST
        "v_total_specs": total,
        "gap_list": gap_list,
        "aggregate_implemented_rate_tier_partitioned": {
            "execution_proven_implemented_over_V": exec_proven_rate,
            "execution_tier_implemented_rate": exec_rate,
            "aggregate_implemented_incl_judgment_validated": agg_rate_all,
            "aggregate_implemented_count": agg_implemented,
            "note": "execution tier is the only behaviorally-proven tier; the judgment tier carries the diverse-judge residual (CONTESTED specs NOT counted as implemented).",
        },
        # --- Cycle-16-S24 NARROW DISCLOSURE RE-EMIT (additive blocks) ---
        "three_population_reconciliation": three_pop,
        "absent_disclosed_bound_finding": absent_finding,
        "per_era_rates": per_era,
        # T6 — honest gaps verbatim + scoped close claim (now era-reconciled)
        "honest_gaps_verbatim": HONEST_GAPS_VERBATIM,
        "close_claim": updated_close_claim,
        "close_claim_prior_superseded": (
            "100% of the disclosed-bound discoverable population (M1'=193 / V "
            f"{total} specs), residual R disclosed, tier-labelled: execution-proven "
            f"{len(exec_implemented)} implemented / {len(exec_not_impl)} not-implemented "
            f"(PASS-LOW-POWER); judgment tier {len(judg_specs)} specs with "
            f"{len(judg_contested)} CONTESTED->not-counted. Every percentage is "
            "tier-scoped to the discoverable population; no un-scoped completion claim."
        ),
        "per_spec_gap_list_IP_PRIVATE": [
            {"spec_iri": v["spec_iri"], "spec_class": v.get("spec_class"),
             "current_status": v.get("current_status"), "tier": v["tier"],
             "verdict": v["verdict"], "implemented": v["implemented"],
             "single_reader_edge": v.get("single_reader_edge", False),
             "evidence": v["evidence"][:200]}
            for v in verdicts
        ],
    }
    # Byte-identical guarantee (Cycle-16-S24 re-emit): the gap_list counts,
    # v_total_specs, aggregate rates, and the full per_spec_gap_list_IP_PRIVATE
    # MUST equal the prior file's. ADD blocks only; change NO verdict.
    if RUN_OUT.exists():
        prior = json.loads(RUN_OUT.read_text())
        _assert_byte_identical(prior, out)

    RUN_OUT.write_text(json.dumps(out, indent=1))
    return out


def _assert_byte_identical(prior: dict, out: dict) -> None:
    """Assert the preserved (non-additive) fields are unchanged vs the prior emit."""
    # gap_list counts
    for tier in ("execution_tier", "judgment_tier"):
        for k, pv in prior["gap_list"][tier].items():
            ov = out["gap_list"][tier][k]
            assert ov == pv, f"gap_list.{tier}.{k} changed: prior={pv} new={ov}"
    assert out["v_total_specs"] == prior["v_total_specs"], "v_total_specs changed"
    for k, pv in prior["aggregate_implemented_rate_tier_partitioned"].items():
        ov = out["aggregate_implemented_rate_tier_partitioned"][k]
        assert ov == pv, f"aggregate rate {k} changed: prior={pv} new={ov}"
    # full per-spec gap list byte-identical
    assert out["per_spec_gap_list_IP_PRIVATE"] == prior["per_spec_gap_list_IP_PRIVATE"], \
        "per_spec_gap_list_IP_PRIVATE changed"
    # preserved residuals
    for k in ("single_reader_edge_spec_ids", "single_reader_edge_caveat",
              "classification_surplus_residual", "be_j_3388_not_promoted",
              "denominator_disclosed_bound", "honest_gaps_verbatim"):
        assert out[k] == prior[k], f"residual {k} changed"
    print("BYTE-IDENTICAL ASSERTION PASSED: recomputed gap_list counts + "
          "per_spec_gap_list_IP_PRIVATE + aggregate rates + residuals == prior.")


def main() -> int:
    ap = argparse.ArgumentParser(description="BE-T trusted-detector run over V")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--no-cache", action="store_true", help="recompute BE-S verdicts")
    args = ap.parse_args()
    out = run(use_cached_bes=not args.no_cache)
    ap2 = out["aggregate_implemented_rate_tier_partitioned"]
    print(f"BE-T run: V={out['v_total_specs']} | exec implemented={out['gap_list']['execution_tier']['implemented_count']} "
          f"not-impl={out['gap_list']['execution_tier']['not_implemented_count']} "
          f"contested={out['gap_list']['execution_tier']['contested_count']} | "
          f"judgment total={out['gap_list']['judgment_tier']['total']} "
          f"contested={out['gap_list']['judgment_tier']['contested_not_counted']} | "
          f"independence_clean={out['independence_clean']}")
    print(f"  exec-proven-rate-over-V={ap2['execution_proven_implemented_over_V']} | agg-incl-judgment={ap2['aggregate_implemented_incl_judgment_validated']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
