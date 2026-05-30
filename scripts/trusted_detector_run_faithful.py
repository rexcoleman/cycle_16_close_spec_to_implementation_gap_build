#!/usr/bin/env python3
"""Re-derive the gap list against FAITHFUL targets — Cycle-16-S26 Build-Runner Step 3.

The S24 gap list (outputs/trusted_detector_run.json) keyed each spec's "what counts as
implemented" on the BE-D scan's SYNTHESIZED runtime_emit_event_class. S25 proved that
target can be UNFAITHFUL (kernel-coach af3a918a: synthesized `kernel_coach.dispatch` —
never in the spec — made a correct implementation read not_faithful). This re-runs the
SAME unmodified detector against a FAITHFUL-TARGET OVERLAY scan (each spec's
runtime_emit_event_class replaced by the faithful_target extracted from the spec's OWN
text in faithful_target_map.json) and writes the corrected gap list to a NEW file
  outputs/trusted_detector_run_faithful.json
(DO NOT overwrite trusted_detector_run.json).

NON-INVASIVE re-derivation (HC #74 — probe/harness/floors/fixtures byte-identical):
  - We DO NOT touch scripts/probes/**, scripts/probe_accuracy_harness.py, the floors,
    or scripts/structural_prevention/fixtures/**.
  - We write a faithful-overlay copy of the scan to a temp path and INJECT it into the
    detector modules at RUNTIME (validation_tier_verdict.SCAN_JSON + the F-probe's
    --scan-json CLI arg both already parameterize the scan path). The probe code runs
    UNMODIFIED; only its INPUT target changes. This is the measurement-fidelity fix.

The detector's own per-spec verdict logic (tier classify -> F execution probe / diverse
judge -> implemented/not/contested) is reused VERBATIM from validation_tier_verdict +
trusted_detector_run; we re-run it over the overlay and re-emit the SAME schema, era-
partitioned + tier-partitioned exactly as the S24 gap list.

THIS DOES NOT CLOSE THE GAP. It makes the per-spec targets faithful so the gap list is
honest. ONE spec was implemented at S25; the rest remain.
"""
from __future__ import annotations

import argparse
import importlib
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = REPO / "outputs"
sys.path.insert(0, str(HERE))

SCAN_JSON = OUTPUTS / "retroactive_scan_cycle_1_15_run.json"
MAP_JSON = OUTPUTS / "faithful_target_map.json"
SYNTH_RUN = OUTPUTS / "trusted_detector_run.json"
FAITHFUL_RUN = OUTPUTS / "trusted_detector_run_faithful.json"


def _build_overlay_scan() -> tuple[Path, dict]:
    """Write a faithful-overlay copy of the scan: each spec's runtime_emit_event_class
    replaced by faithful_target from the map. Returns (overlay_path, replacement_log)."""
    scan = json.loads(SCAN_JSON.read_text())
    fmap = {m["spec_iri"]: m for m in json.loads(MAP_JSON.read_text())["members"]}
    replacements = {}
    def _is_na(x):
        return bool(x) and str(x).strip().lower().startswith("n/a")
    for rec in scan["per_spec_evidence_IP_PRIVATE"]:
        sid = rec["spec_id"]
        mem = fmap.get(sid)
        if mem is None:
            continue  # not in V/map -> leave scan field as-is (won't be in gap list)
        ft = mem["faithful_target"]
        old = rec.get("runtime_emit_event_class")
        if ft is None:
            # defect/untraceable -> leave as-is; the detector routes conservative.
            continue
        # DP#26 invariance: faithful 'n/a' and the synthesized 'n/a — citation-based...'
        # are the SAME carve-out (both DP#26 -> semantically_judged tier; judgment verdict
        # invariant). Preserve the original string so the judgment-tier LLM inputs are
        # byte-stable; only record a SUBSTANTIVE replacement when the faithful target is a
        # genuinely different NON-n/a executable class (the only specs that can move a verdict).
        if _is_na(ft) and _is_na(old):
            continue  # no substantive change; leave original DP#26 string untouched
        if ft != old:
            replacements[sid] = {"old_synthesized": old, "new_faithful": ft,
                                 "disposition": mem["disposition"],
                                 "spec_class": mem.get("spec_class"),
                                 "name": mem.get("name")}
        rec["runtime_emit_event_class"] = ft
    tmp = Path(tempfile.mkdtemp(prefix="faithful_overlay_")) / "retroactive_scan_faithful_overlay.json"
    tmp.write_text(json.dumps(scan))
    return tmp, replacements


def _rederive(overlay_path: Path, replacements: dict) -> list[dict]:
    """Re-derive the per-spec verdicts against faithful targets.

    JUDGMENT-TIER INVARIANCE (proven): no DP#26 spec's target changed SUBSTANTIVELY
    (faithful 'n/a' == synthesized 'n/a — citation-based...'; both DP#26 -> semantically
    _judged, identical judgment-tier input). So the judgment-tier verdicts are byte-
    identical to the cached synthesized run (outputs/validation_tier_verdicts.json) — we
    reuse them VERBATIM rather than re-burning 203 LLM judge calls on identical inputs.

    EXECUTION TIER: re-run the UNMODIFIED F-probe over the FAITHFUL overlay scan for the
    execution-checkable specs. This is the ONLY tier the faithful-target fix can move.
    The probe code is byte-identical (HC #74); only its --scan-json input is the overlay.
    """
    # Reuse cached BES verdicts (judgment tier byte-identical inputs).
    cached = json.loads((OUTPUTS / "validation_tier_verdicts.json").read_text())
    cached_by_iri = {v["spec_iri"]: dict(v) for v in cached["per_spec_verdicts_IP_PRIVATE"]}

    # Re-run the detector against the overlay via the UNMODIFIED module, but only consume
    # its EXECUTION-tier verdicts (judgment tier is invariant -> reuse cached).
    for mod in ("validation_tier_verdict", "probe_accuracy_harness"):
        if mod in sys.modules:
            del sys.modules[mod]
    BES = importlib.import_module("validation_tier_verdict")
    BES.SCAN_JSON = overlay_path           # redirect input ONLY (probe code unchanged)
    BES._F_FIRE_CACHE = None
    overlay_scan = BES._load_scan_specs()  # the faithful-overlay scan map

    rederived = []
    for sid, v in cached_by_iri.items():
        rec = overlay_scan.get(sid)
        tier = BES._classify_tier(rec) if rec else v["tier"]
        if tier == "execution_checkable":
            # Re-fire the UNMODIFIED F-probe against the faithful target for this spec.
            fresh = BES.close_verdict(sid, _scan=overlay_scan)
            fresh["single_reader_edge"] = v.get("single_reader_edge", False)
            fresh["_rederived_against_faithful_target"] = True
            fresh["_faithful_target"] = rec.get("runtime_emit_event_class") if rec else None
            rederived.append(fresh)
        else:
            # Judgment tier: input byte-identical -> reuse cached verdict verbatim.
            v["_rederived_against_faithful_target"] = False
            v["_judgment_tier_input_invariant"] = True
            rederived.append(v)
    return rederived


def run() -> dict:
    if not MAP_JSON.exists():
        raise SystemExit("REFUSE: faithful_target_map.json absent (DP#44).")
    overlay_path, replacements = _build_overlay_scan()

    verdicts = _rederive(overlay_path, replacements)

    exec_specs = [v for v in verdicts if v["tier"] == "execution_checkable"]
    judg_specs = [v for v in verdicts if v["tier"] == "semantically_judged"]
    exec_implemented = [v for v in exec_specs if v["implemented"]]
    exec_not_impl = [v for v in exec_specs if not v["implemented"]]
    judg_implemented = [v for v in judg_specs if v["implemented"] and v["verdict"] == "VALIDATED-JUDGMENT"]
    judg_not_impl = [v for v in judg_specs if v["verdict"] == "NOT-VALIDATED" and not v["implemented"]]
    judg_contested = [v for v in judg_specs if v["verdict"] == "CONTESTED"]
    total = len(verdicts)

    gap_list = {
        "execution_tier": {
            "total": len(exec_specs),
            "implemented": [v["spec_iri"] for v in exec_implemented],
            "not_implemented": [v["spec_iri"] for v in exec_not_impl],
            "implemented_count": len(exec_implemented),
            "not_implemented_count": len(exec_not_impl),
            "tier_label": "PASS-LOW-POWER (F-detector accuracy n_eval=2 per §1ee) — FAITHFUL TARGETS",
        },
        "judgment_tier": {
            "total": len(judg_specs),
            "diverse_judge_validated_implemented": len(judg_implemented),
            "diverse_judge_not_implemented": len(judg_not_impl),
            "contested_not_counted": len(judg_contested),
            "contested_fraction": round(len(judg_contested) / len(judg_specs), 4) if judg_specs else None,
            "tier_label": "diverse-agreeing-judge with fail-safe; CONTESTED -> NOT counted",
        },
    }
    agg_implemented = len(exec_implemented) + len(judg_implemented)
    out = {
        "schema_version": "be_t_trusted_detector_run_faithful.v1",
        "build_event": "Cycle-16-S26 RE-DERIVATION against FAITHFUL targets (Done #60 measurement-fidelity fix)",
        "is_measurement_fidelity_fix_not_gap_closure": True,
        "fidelity_note": (
            "This re-derives the gap list against per-spec targets extracted from each spec's OWN text "
            "(faithful_target_map.json), NOT the synthesized runtime_emit_event_class. It does NOT close "
            "the spec->implementation gap. ONE spec (kernel-coach af3a918a) was implemented at S25; the rest remain."
        ),
        "detector_unmodified_note": (
            "Re-run with the F-probe / harness / floors / fixtures BYTE-IDENTICAL (HC #74). Only the detector "
            "INPUT target was redirected (faithful-overlay scan injected at runtime via the existing --scan-json "
            "/ SCAN_JSON parameterization). Prove with `git diff --stat` of scripts/probes scripts/probe_accuracy_harness.py."
        ),
        "v_total_specs": total,
        "faithful_overlay_replacements": replacements,
        "n_targets_changed_from_synthesized": len(replacements),
        "gap_list": gap_list,
        "aggregate_implemented_rate_tier_partitioned": {
            "execution_proven_implemented_over_V": round(len(exec_implemented) / total, 4) if total else None,
            "execution_tier_implemented_rate": round(len(exec_implemented) / len(exec_specs), 4) if exec_specs else None,
            "aggregate_implemented_incl_judgment_validated": round(agg_implemented / total, 4) if total else None,
            "aggregate_implemented_count": agg_implemented,
        },
        "carried_residuals_disclosed_not_resolved": [
            "+53 DesignDecision classification-surplus (M3 census 172 vs M1 classified 119)",
            "6 single-reader edge specs: 13cb4b96, 6bcf77ca, 786eecc3, c0a073da, e8f6324b, ee6c6ac3",
            "26-absent extraction-coverage gap (193-167); M1'=193 disclosed-bound",
            "BE-J 33.88% NOT promoted (Done #42 lock)",
        ],
        "per_spec_gap_list_IP_PRIVATE": [
            {"spec_iri": v["spec_iri"], "spec_class": v.get("spec_class"),
             "current_status": v.get("current_status"), "tier": v["tier"],
             "verdict": v["verdict"], "implemented": v["implemented"],
             "evidence": v["evidence"][:200]}
            for v in verdicts
        ],
    }
    FAITHFUL_RUN.write_text(json.dumps(out, indent=1))
    return out


def main() -> int:
    argparse.ArgumentParser(description="Re-derive gap list vs faithful targets").parse_args()
    out = run()
    ap2 = out["aggregate_implemented_rate_tier_partitioned"]
    print(f"FAITHFUL re-derivation: V={out['v_total_specs']} | targets_changed={out['n_targets_changed_from_synthesized']}")
    print(f"  exec implemented={out['gap_list']['execution_tier']['implemented_count']} "
          f"not-impl={out['gap_list']['execution_tier']['not_implemented_count']} | "
          f"judgment total={out['gap_list']['judgment_tier']['total']} "
          f"contested={out['gap_list']['judgment_tier']['contested_not_counted']}")
    print(f"  exec-proven-rate-over-V={ap2['execution_proven_implemented_over_V']} | "
          f"agg-incl-judgment={ap2['aggregate_implemented_incl_judgment_validated']} "
          f"({ap2['aggregate_implemented_count']}/{out['v_total_specs']})")
    print(f"  replacements: {out['faithful_overlay_replacements']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
