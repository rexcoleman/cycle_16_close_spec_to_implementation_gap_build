#!/usr/bin/env python3
"""Operational-Definition Substitution Gate (Cycle 16 BE-H / Done #14).

Fires at Stage 1 RQS close + Stage 4 ED close + Stage 4 ACCEPTANCE_CRITERIA close.

PREDICATE (KT-8 BINDING — NO string-match of a probe ID):
  For each operational definition supplied, the definition MUST name a probe
  primitive by name (e.g. "probe_agent_contract") AND this gate IMPORTS +
  subprocess-EXECUTES that probe with `--self-test`, confirming exit 0
  (executable + passing self-test). The gate physically runs the probe; it
  never accepts a probe-ID substring as evidence.

  A definition whose acceptance predicate resolves to a PROXY —
    * "field value == enum"        (registry-state substitution)
    * "artifact exists at path"    (presence substitution)
    * "token count >= N"           (citation-density substitution)
    * "emission record exists"     (emission-record substitution)
  WITH NO probe reference, OR naming a probe that fails self-test —
  HARD-FAILs (exit non-zero) and emits a refuse.event.

DP#44 refuse-on-missing-precondition: if the probes dir is absent OR no
definitions are supplied, the gate REFUSES (exit non-zero) rather than passing.

Sink: outputs/structural_prevention_substitution_gate_events.jsonl
  >=1 refuse.event + >=1 pass.event per the BE-H acceptance contract.

Usage:
  operational_definition_substitution_gate.py --project-dir DIR \
      --definitions-json FILE [--surface stage1_rqs|stage4_ed|stage4_acceptance] \
      [--run-id-prefix PFX] [--probes-dir DIR]
  operational_definition_substitution_gate.py --self-test
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import subprocess
import sys
import uuid

PROXY_PATTERNS = [
    # (label, regex)  — proxy semantics this gate must REFUSE when no probe is named.
    ("field_equals_enum", re.compile(r"\b(field|currentStatus|status|registry[ _-]?state)\b.*==|==\s*(cycle16:\w+|['\"]?\w+['\"]?)\s*$", re.I)),
    ("artifact_exists_at_path", re.compile(r"\b(exists?\s+at\s+path|file\s+exists|os\.path\.exists|artifact\s+(is\s+)?present)\b", re.I)),
    ("token_count_threshold", re.compile(r"\b(token[ _-]?count|word[ _-]?count|citation[ _-]?density|>=\s*\d+\s*(tokens|words|citations|mentions))\b", re.I)),
    ("emission_record_exists", re.compile(r"\b(emission\s+record\s+(exists|present)|>=\s*\d+\s*emit|emit[ _-]?row\s+exists)\b", re.I)),
]
PROBE_NAME_RE = re.compile(r"\bprobe_[a-z_]+\b")


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _emit(sink: str, event_class: str, run_id: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(sink), exist_ok=True)
    ev = {
        "schema_version": "0.1",
        "namespace": "cycle_16.be_h.operational_definition_substitution_gate",
        "event_class": event_class,
        "predicateType": "cycle16:substitution_gate_v1",
        "timestamp": _utc(),
        "run_id": run_id,
        "payload": payload,
    }
    with open(sink, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")


def _probe_path(probes_dir: str, probe_name: str) -> str | None:
    """Resolve probe_name -> class subdir path. Probes live at probes/<cls>/<probe_name>.py."""
    for cls in ("a", "b", "c", "d", "e", "f"):
        cand = os.path.join(probes_dir, cls, f"{probe_name}.py")
        if os.path.exists(cand):
            return cand
    return None


def _run_self_test(probe_path: str) -> tuple[bool, int, str]:
    """IMPORT + SUBPROCESS-EXECUTE the named probe with --self-test (KT-8)."""
    try:
        r = subprocess.run(
            [sys.executable, probe_path, "--self-test"],
            capture_output=True, text=True, timeout=120,
        )
        return (r.returncode == 0, r.returncode, (r.stderr or r.stdout or "")[:200])
    except subprocess.TimeoutExpired:
        return (False, -1, "self_test_timeout_120s")
    except OSError as e:
        return (False, -2, f"exec_failed:{e}")


def judge_definition(defn: dict, probes_dir: str) -> dict:
    """Return verdict dict for one operational definition.

    PASS iff: definition names a probe primitive AND that probe is executable
    AND passes self-test (exit 0). Otherwise FAIL with the proxy class detected.
    """
    text = (defn.get("operational_metric") or defn.get("text") or "")
    name = defn.get("id") or defn.get("hypothesis") or "(unnamed)"
    named_probe = defn.get("probe_primitive")
    if not named_probe:
        m = PROBE_NAME_RE.search(text)
        named_probe = m.group(0) if m else None

    proxy_hits = [label for (label, rx) in PROXY_PATTERNS if rx.search(text)]

    if not named_probe:
        return {
            "definition_id": name, "verdict": "FAIL",
            "reason": "no_probe_primitive_referenced",
            "proxy_class": proxy_hits or ["unspecified_proxy"],
            "named_probe": None,
        }
    probe_path = _probe_path(probes_dir, named_probe)
    if not probe_path:
        return {
            "definition_id": name, "verdict": "FAIL",
            "reason": "named_probe_not_found_on_disk",
            "named_probe": named_probe, "proxy_class": proxy_hits,
        }
    # KT-8: physically execute the probe's self-test — never string-match the ID.
    ok, rc, ev = _run_self_test(probe_path)
    if not ok:
        return {
            "definition_id": name, "verdict": "FAIL",
            "reason": "named_probe_self_test_failed",
            "named_probe": named_probe, "self_test_exit": rc,
            "evidence": ev,
        }
    return {
        "definition_id": name, "verdict": "PASS",
        "reason": "probe_executed_and_self_test_passed",
        "named_probe": named_probe, "probe_path": probe_path,
        "self_test_exit": rc,
    }


def run_gate(project_dir: str, definitions: list[dict], surface: str,
             run_id_prefix: str, probes_dir: str) -> int:
    sink = os.path.join(project_dir, "outputs",
                        "structural_prevention_substitution_gate_events.jsonl")
    # DP#44: refuse-on-missing-precondition.
    if not os.path.isdir(probes_dir):
        _emit(sink, "operational_definition_substitution_gate.refuse.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"surface": surface, "reason": "probes_dir_absent",
               "probes_dir": probes_dir, "refuse": True})
        print(f"REFUSE: probes_dir absent ({probes_dir})", file=sys.stderr)
        return 3
    if not definitions:
        _emit(sink, "operational_definition_substitution_gate.refuse.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"surface": surface, "reason": "no_definitions_supplied", "refuse": True})
        print("REFUSE: no operational definitions supplied", file=sys.stderr)
        return 3

    results = [judge_definition(d, probes_dir) for d in definitions]
    fails = [r for r in results if r["verdict"] == "FAIL"]
    passes = [r for r in results if r["verdict"] == "PASS"]

    for r in results:
        ec = ("operational_definition_substitution_gate.refuse.event"
              if r["verdict"] == "FAIL"
              else "operational_definition_substitution_gate.pass.event")
        _emit(sink, ec, f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"surface": surface, **r, "refuse": r["verdict"] == "FAIL"})

    print(f"Substitution Gate [{surface}]: {len(passes)} PASS, {len(fails)} FAIL")
    for r in fails:
        print(f"  FAIL {r['definition_id']}: {r['reason']} "
              f"(proxy={r.get('proxy_class')})", file=sys.stderr)
    return 1 if fails else 0


def _self_test(project_dir: str, probes_dir: str) -> int:
    """Distinguish known-bad (proxy) defs from known-good (probe-referencing) def.

    >=3 proxy negative fixtures must FAIL; >=1 probe-referencing def must PASS.
    """
    bad = [
        {"id": "kb_field_enum",
         "operational_metric": "spec.currentStatus == cycle16:implemented"},
        {"id": "kb_artifact_exists",
         "operational_metric": "the gate file exists at path scripts/x.sh"},
        {"id": "kb_token_count",
         "operational_metric": "citation density >= 5 mentions in FINDINGS"},
        {"id": "kb_emission_record",
         "operational_metric": "an emit row exists in outputs/x_events.jsonl"},
    ]
    good = [{"id": "kg_probe_ref",
             "operational_metric": "implemented iff probe_agent_contract fires implemented=true",
             "probe_primitive": "probe_agent_contract"}]
    bad_res = [judge_definition(d, probes_dir) for d in bad]
    good_res = [judge_definition(d, probes_dir) for d in good]
    bad_ok = all(r["verdict"] == "FAIL" for r in bad_res) and len(bad_res) >= 3
    good_ok = all(r["verdict"] == "PASS" for r in good_res) and len(good_res) >= 1
    print(f"self-test: proxy-fixtures-fail={bad_ok} ({len(bad_res)}) "
          f"probe-fixture-pass={good_ok}")
    return 0 if (bad_ok and good_ok) else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Operational-Definition Substitution Gate (Done #14)")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--definitions-json", default=None,
                    help="JSON file: list of {id, operational_metric, [probe_primitive]}")
    ap.add_argument("--surface", default="stage1_rqs",
                    choices=["stage1_rqs", "stage4_ed", "stage4_acceptance"])
    ap.add_argument("--run-id-prefix", default="s13_be_h_production_substitution_gate")
    ap.add_argument("--probes-dir", default=None)
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)

    project_dir = os.path.abspath(a.project_dir)
    probes_dir = a.probes_dir or os.path.join(project_dir, "scripts", "probes")

    if a.self_test:
        return _self_test(project_dir, probes_dir)

    definitions: list[dict] = []
    if a.definitions_json and os.path.exists(a.definitions_json):
        with open(a.definitions_json) as f:
            definitions = json.load(f)
    return run_gate(project_dir, definitions, a.surface, a.run_id_prefix, probes_dir)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
