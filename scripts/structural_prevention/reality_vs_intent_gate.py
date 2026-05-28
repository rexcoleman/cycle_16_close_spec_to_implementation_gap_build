#!/usr/bin/env python3
"""Reality-vs-Intent Gate (Cycle 16 BE-H / Done #15b).

Forward gate at Stage 1 RQS R3 + Stage 4 ED R3. Requires a mandatory structured
table where EACH row (one per H / KT / acceptance criterion) carries 4 columns:

  1. pre_registered_intent       (what the RQ/H asked for)
  2. operational_metric_verbatim (the metric, quoted verbatim)
  3. probe_primitive_referenced  (the named BE-F probe that grounds the metric)
  4. implementation_baseline     (the probe-fire baseline result for that row)

A missing table OR an incomplete table (any row missing any of the 4 columns)
-> R3 FAIL. To make the probe-reference column load-bearing (KT-8), this gate
IMPORTS + subprocess-EXECUTES each referenced probe with --self-test and records
real probe-fire evidence; a row that names a probe which fails self-test FAILS.

DP#44 refuse-on-missing-precondition: missing table file -> refuse (exit non-zero).

Sink: outputs/structural_prevention_reality_vs_intent_events.jsonl

Usage:
  reality_vs_intent_gate.py --project-dir DIR --table-json FILE \
      [--surface stage1_rqs_r3|stage4_ed_r3] [--probes-dir DIR]
  reality_vs_intent_gate.py --self-test
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import uuid

REQUIRED_COLS = [
    "pre_registered_intent",
    "operational_metric_verbatim",
    "probe_primitive_referenced",
    "implementation_baseline",
]


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _emit(sink: str, ec: str, run_id: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(sink), exist_ok=True)
    ev = {"schema_version": "0.1",
          "namespace": "cycle_16.be_h.reality_vs_intent_gate",
          "event_class": ec, "predicateType": "cycle16:reality_vs_intent_v1",
          "timestamp": _utc(), "run_id": run_id, "payload": payload}
    with open(sink, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")


def _probe_path(probes_dir: str, name: str) -> str | None:
    for cls in ("a", "b", "c", "d", "e", "f"):
        cand = os.path.join(probes_dir, cls, f"{name}.py")
        if os.path.exists(cand):
            return cand
    return None


def _self_test(probe_path: str) -> tuple[bool, int]:
    try:
        r = subprocess.run([sys.executable, probe_path, "--self-test"],
                           capture_output=True, text=True, timeout=120)
        return (r.returncode == 0, r.returncode)
    except Exception:
        return (False, -1)


def judge_table(rows: list[dict], probes_dir: str) -> dict:
    incomplete = []
    probe_failures = []
    for i, row in enumerate(rows):
        missing = [c for c in REQUIRED_COLS if not str(row.get(c, "")).strip()]
        if missing:
            incomplete.append({"row": i, "missing_cols": missing})
            continue
        # KT-8: the probe-reference column is load-bearing — execute it.
        name = str(row["probe_primitive_referenced"]).strip()
        pp = _probe_path(probes_dir, name)
        if not pp:
            probe_failures.append({"row": i, "probe": name, "reason": "not_found"})
            continue
        ok, rc = _self_test(pp)
        if not ok:
            probe_failures.append({"row": i, "probe": name,
                                   "reason": "self_test_failed", "exit": rc})
    ok = (not incomplete) and (not probe_failures) and len(rows) >= 1
    return {"verdict": "PASS" if ok else "FAIL",
            "rows": len(rows), "incomplete_rows": incomplete,
            "probe_failures": probe_failures}


def run_gate(project_dir, table_path, surface, run_id_prefix, probes_dir) -> int:
    sink = os.path.join(project_dir, "outputs",
                        "structural_prevention_reality_vs_intent_events.jsonl")
    if not table_path or not os.path.exists(table_path):
        _emit(sink, "reality_vs_intent_gate.refuse.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"surface": surface, "reason": "table_absent",
               "table_path": table_path, "refuse": True})
        print(f"REFUSE: reality-vs-intent table absent ({table_path})", file=sys.stderr)
        return 3
    with open(table_path) as f:
        rows = json.load(f)
    res = judge_table(rows, probes_dir)
    ec = ("reality_vs_intent_gate.pass.event" if res["verdict"] == "PASS"
          else "reality_vs_intent_gate.refuse.event")
    _emit(sink, ec, f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
          {"surface": surface, **res, "refuse": res["verdict"] == "FAIL"})
    print(f"Reality-vs-Intent [{surface}]: {res['verdict']} "
          f"({res['rows']} rows; {len(res['incomplete_rows'])} incomplete; "
          f"{len(res['probe_failures'])} probe-fail)")
    return 0 if res["verdict"] == "PASS" else 1


def _self_test_gate(probes_dir: str) -> int:
    """Known-good full table PASSES; remove one row's column -> FAILS."""
    good = [{"pre_registered_intent": "agents observed invoking",
             "operational_metric_verbatim": "implemented iff >=1 Agent invocation",
             "probe_primitive_referenced": "probe_agent_contract",
             "implementation_baseline": "20 fires implemented=true"}]
    bad = [dict(good[0])]
    bad[0].pop("implementation_baseline")  # remove 1 column from known-good fixture
    g = judge_table(good, probes_dir)
    b = judge_table(bad, probes_dir)
    ok = g["verdict"] == "PASS" and b["verdict"] == "FAIL"
    print(f"self-test: complete-table-pass={g['verdict']=='PASS'} "
          f"incomplete-table-fail={b['verdict']=='FAIL'}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Reality-vs-Intent Gate (Done #15b)")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--table-json", default=None)
    ap.add_argument("--surface", default="stage1_rqs_r3",
                    choices=["stage1_rqs_r3", "stage4_ed_r3"])
    ap.add_argument("--run-id-prefix", default="s13_be_h_production_reality_vs_intent")
    ap.add_argument("--probes-dir", default=None)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    project_dir = os.path.abspath(a.project_dir)
    probes_dir = a.probes_dir or os.path.join(project_dir, "scripts", "probes")
    if a.self_test:
        return _self_test_gate(probes_dir)
    return run_gate(project_dir, a.table_json, a.surface, a.run_id_prefix, probes_dir)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
