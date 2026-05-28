#!/usr/bin/env python3
"""Design-Anchor Disclosure Gate (Cycle 16 BE-H / Done #15g).

At LANDSCAPE close: require enumeration of the load-bearing mechanism DESIGN
elements, each tagged either:
    external-anchored      (design grounded in an external source/precedent)
    internally-inherited   (design inherited from our own prior cycle work)

When a LOAD-BEARING design element (not merely a substrate primitive) is
`internally-inherited`, the gate emits a Stage 2->3 checkpoint flag + a
paradigm-escalation-candidate marker (recursive-anchoring risk: we keep
reusing our own design skeleton without external grounding).

The gate REFUSES (exit non-zero) when the disclosure column is ABSENT from the
supplied enumeration (every row must carry an `anchor` field with one of the
two allowed values).

DP#44 refuse-on-missing-precondition: enumeration file absent -> refuse.

Sink: outputs/structural_prevention_design_anchor_disclosure_events.jsonl

Usage:
  design_anchor_disclosure_gate.py --project-dir DIR --enumeration-json FILE \
      [--run-id-prefix PFX]
  design_anchor_disclosure_gate.py --self-test
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import uuid

ALLOWED_ANCHORS = {"external-anchored", "internally-inherited"}


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _emit(sink: str, ec: str, run_id: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(sink), exist_ok=True)
    ev = {"schema_version": "0.1",
          "namespace": "cycle_16.be_h.design_anchor_disclosure_gate",
          "event_class": ec, "predicateType": "cycle16:design_anchor_disclosure_v1",
          "timestamp": _utc(), "run_id": run_id, "payload": payload}
    with open(sink, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")


def judge(enumeration: list[dict]) -> dict:
    missing_col = []
    bad_value = []
    internal_load_bearing = []
    for i, row in enumerate(enumeration):
        anchor = row.get("anchor")
        if anchor is None:
            missing_col.append({"row": i, "element": row.get("element", "?")})
            continue
        if anchor not in ALLOWED_ANCHORS:
            bad_value.append({"row": i, "anchor": anchor})
            continue
        if anchor == "internally-inherited" and row.get("load_bearing") is True:
            internal_load_bearing.append({"row": i, "element": row.get("element", "?")})
    # Disclosure column ABSENT (any row missing anchor) -> refuse.
    if missing_col or bad_value:
        return {"verdict": "FAIL", "reason": "disclosure_column_absent_or_invalid",
                "missing_column_rows": missing_col, "bad_value_rows": bad_value,
                "internal_load_bearing": internal_load_bearing}
    return {"verdict": "PASS",
            "reason": "all_elements_disclosed",
            "internal_load_bearing": internal_load_bearing,
            "checkpoint_flag": bool(internal_load_bearing),
            "paradigm_escalation_candidate": bool(internal_load_bearing)}


def run_gate(project_dir, enum_path, run_id_prefix) -> int:
    sink = os.path.join(project_dir, "outputs",
                        "structural_prevention_design_anchor_disclosure_events.jsonl")
    if not enum_path or not os.path.exists(enum_path):
        _emit(sink, "design_anchor_disclosure_gate.refuse.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"reason": "enumeration_file_absent", "path": enum_path, "refuse": True})
        print(f"REFUSE: enumeration file absent ({enum_path})", file=sys.stderr)
        return 3
    with open(enum_path) as f:
        enumeration = json.load(f)
    res = judge(enumeration)
    if res["verdict"] == "FAIL":
        _emit(sink, "design_anchor_disclosure_gate.refuse.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}", {**res, "refuse": True})
        print(f"REFUSE: {res['reason']}", file=sys.stderr)
        return 1
    # PASS, but emit checkpoint + escalation markers if internal load-bearing.
    _emit(sink, "design_anchor_disclosure_gate.pass.event",
          f"{run_id_prefix}_{uuid.uuid4().hex[:8]}", {**res, "refuse": False})
    if res["internal_load_bearing"]:
        _emit(sink, "design_anchor_disclosure_gate.checkpoint_flag.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"stage_2_3_checkpoint": True, "paradigm_escalation_candidate": True,
               "internal_load_bearing": res["internal_load_bearing"], "refuse": False})
    print(f"Design-Anchor Disclosure: PASS "
          f"(internal-load-bearing={len(res['internal_load_bearing'])}; "
          f"checkpoint_flag={res['checkpoint_flag']})")
    return 0


def _self_test() -> int:
    """Missing-disclosure-column fixture -> FAIL; complete enumeration -> PASS
    (and emits checkpoint marker when an internally-inherited load-bearing
    element is present)."""
    bad = [{"element": "four-gate skeleton"}]  # no anchor column
    good = [{"element": "SPARQL write boundary", "anchor": "external-anchored",
             "load_bearing": True},
            {"element": "four-gate skeleton", "anchor": "internally-inherited",
             "load_bearing": True}]
    rb = judge(bad); rg = judge(good)
    ok = (rb["verdict"] == "FAIL" and rg["verdict"] == "PASS"
          and rg["checkpoint_flag"] is True)
    print(f"self-test: absent-column-fail={rb['verdict']=='FAIL'} "
          f"complete-pass={rg['verdict']=='PASS'} "
          f"internal-checkpoint={rg['checkpoint_flag']}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Design-Anchor Disclosure Gate (Done #15g)")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--enumeration-json", default=None)
    ap.add_argument("--run-id-prefix", default="s13_be_h_production_design_anchor_disclosure")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return _self_test()
    return run_gate(os.path.abspath(a.project_dir), a.enumeration_json, a.run_id_prefix)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
