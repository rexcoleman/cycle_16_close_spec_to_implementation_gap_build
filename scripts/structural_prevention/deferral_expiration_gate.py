#!/usr/bin/env python3
"""Deferral-Expiration Gate (Cycle 16 BE-H / Done #15f).

A deferred spec MUST carry ALL FOUR fields:
    1. named_target_session
    2. reason
    3. reactivation_condition
    4. maximum_dormancy_window   (integer sessions)
Missing ANY of the 4 -> refuse (one refuse per missing-field negative fixture).

A deferral whose age (current_session_index - deferred_at_session_index)
EXCEEDS its maximum_dormancy_window auto-routes to kill (kill_spec) OR Rex
re-disposition — silent deferral persistence is a FORBIDDEN state (refuse).

DP#44 refuse-on-missing-precondition: deferrals file absent -> refuse.

Sink: outputs/structural_prevention_deferral_expiration_events.jsonl

Usage:
  deferral_expiration_gate.py --project-dir DIR --deferrals-json FILE \
      [--current-session-index N] [--run-id-prefix PFX]
  deferral_expiration_gate.py --self-test
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
import uuid

REQUIRED_FIELDS = [
    "named_target_session",
    "reason",
    "reactivation_condition",
    "maximum_dormancy_window",
]


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _emit(sink: str, ec: str, run_id: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(sink), exist_ok=True)
    ev = {"schema_version": "0.1",
          "namespace": "cycle_16.be_h.deferral_expiration_gate",
          "event_class": ec, "predicateType": "cycle16:deferral_expiration_v1",
          "timestamp": _utc(), "run_id": run_id, "payload": payload}
    with open(sink, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")


def judge_deferral(d: dict, current_idx: int | None) -> dict:
    spec = d.get("spec_iri") or d.get("id") or "(unnamed)"
    missing = [f for f in REQUIRED_FIELDS
               if d.get(f) in (None, "", []) or
               (f == "maximum_dormancy_window" and not isinstance(d.get(f), int))]
    if missing:
        return {"spec": spec, "verdict": "FAIL",
                "reason": "missing_required_field", "missing_fields": missing}
    # Expiry check.
    if current_idx is not None and "deferred_at_session_index" in d:
        age = current_idx - int(d["deferred_at_session_index"])
        if age > int(d["maximum_dormancy_window"]):
            return {"spec": spec, "verdict": "FAIL",
                    "reason": "deferral_exceeded_max_dormancy_window",
                    "age_sessions": age,
                    "max_window": int(d["maximum_dormancy_window"]),
                    "auto_route": "kill_spec_or_rex_redisposition"}
    return {"spec": spec, "verdict": "PASS",
            "reason": "all_4_fields_present_and_within_window"}


def run_gate(project_dir, deferrals_path, current_idx, run_id_prefix) -> int:
    sink = os.path.join(project_dir, "outputs",
                        "structural_prevention_deferral_expiration_events.jsonl")
    if not deferrals_path or not os.path.exists(deferrals_path):
        _emit(sink, "deferral_expiration_gate.refuse.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"reason": "deferrals_file_absent", "path": deferrals_path, "refuse": True})
        print(f"REFUSE: deferrals file absent ({deferrals_path})", file=sys.stderr)
        return 3
    with open(deferrals_path) as f:
        deferrals = json.load(f)
    results = [judge_deferral(d, current_idx) for d in deferrals]
    fails = [r for r in results if r["verdict"] == "FAIL"]
    for r in results:
        ec = ("deferral_expiration_gate.refuse.event" if r["verdict"] == "FAIL"
              else "deferral_expiration_gate.pass.event")
        _emit(sink, ec, f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {**r, "refuse": r["verdict"] == "FAIL"})
    print(f"Deferral-Expiration: {len(results)-len(fails)} PASS, {len(fails)} FAIL")
    for r in fails:
        print(f"  FAIL {r['spec']}: {r['reason']} "
              f"{r.get('missing_fields','')}", file=sys.stderr)
    return 1 if fails else 0


def _self_test() -> int:
    """4 negative fixtures (one per missing field) FAIL + 1 complete deferral PASS +
    1 expired deferral FAIL."""
    base = {"spec_iri": "cycle16:s1", "named_target_session": "S20",
            "reason": "blocked on X", "reactivation_condition": "X resolved",
            "maximum_dormancy_window": 3}
    negs = []
    for f in REQUIRED_FIELDS:
        d = dict(base); d.pop(f); negs.append(d)
    neg_ok = all(judge_deferral(d, None)["verdict"] == "FAIL" for d in negs) and len(negs) == 4
    good_ok = judge_deferral(base, None)["verdict"] == "PASS"
    expired = dict(base); expired["deferred_at_session_index"] = 10
    exp_ok = judge_deferral(expired, 20)["verdict"] == "FAIL"  # age 10 > window 3
    ok = neg_ok and good_ok and exp_ok
    print(f"self-test: 4-missing-field-fail={neg_ok} complete-pass={good_ok} "
          f"expired-fail={exp_ok}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Deferral-Expiration Gate (Done #15f)")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--deferrals-json", default=None)
    ap.add_argument("--current-session-index", type=int, default=None)
    ap.add_argument("--run-id-prefix", default="s13_be_h_production_deferral_expiration")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return _self_test()
    return run_gate(os.path.abspath(a.project_dir), a.deferrals_json,
                    a.current_session_index, a.run_id_prefix)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
