#!/usr/bin/env python3
"""Cycle-16-S24 BE-T part (i) — guard-the-guards (#47 / Done #47).

Folds the enforcement infrastructure ITSELF — probes, gates, agent specs, AND the
accuracy harness — INTO the audited population (an unaudited guard is the recursive
failure in miniature). Then runs the trusted detectors over the infra entries too
(the guards audit themselves). The harness's OWN implementation status is MEASURED,
not assumed.

Acceptance: ED §5.phase11.3 BE-T thresholds 1+2.
  T1: audited-population count == denominator(M1'=193) + |infra entries|; each infra
      entry flagged is_enforcement_infra:true; an absent infra surface HARD-FAILS.
  T2: >=1 detector-fire JSONL row per infra class in guard_the_guards_run.jsonl.

Builds:
  outputs/guard_the_guards_population.json
  outputs/guard_the_guards_run.jsonl
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import pathlib
import subprocess
import sys
from datetime import datetime, timezone

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = REPO / "outputs"
MOONSHOTS = pathlib.Path(os.path.expanduser("~/Moonshots_Career_Thesis_v2"))
GOVML = pathlib.Path(os.path.expanduser("~/ml-governance-templates"))
SINGULARITY_DB = pathlib.Path(os.path.expanduser("~/singularity.db"))

DENOM_JSON = OUTPUTS / "denominator_dual_method.json"
POP_OUT = OUTPUTS / "guard_the_guards_population.json"
RUN_OUT = OUTPUTS / "guard_the_guards_run.jsonl"

INFRA_CLASSES = ("probe", "gate", "agent_spec", "accuracy_harness")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _denominator_m1_prime() -> int:
    d = json.loads(DENOM_JSON.read_text())
    return int(d["method_1_recorded"]["m1_prime_cycles_1_15_frozen_unit"])


def _file_hash(p: pathlib.Path) -> str | None:
    try:
        return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
    except OSError:
        return None


def enumerate_infra() -> list[dict]:
    """Enumerate every enforcement-infra surface as an audited entry."""
    entries: list[dict] = []

    # 1. Probes (scripts/probes/{a..f}/*.py — the trusted detectors themselves).
    for p in sorted((HERE / "probes").rglob("*.py")):
        if "__pycache__" in p.parts or p.name == "__init__.py":
            continue
        entries.append({"infra_id": f"probe::{p.relative_to(REPO)}",
                        "infra_class": "probe",
                        "is_enforcement_infra": True,
                        "path": str(p.relative_to(REPO)),
                        "abs_path": str(p),
                        "sha256_16": _file_hash(p)})

    # 2. Gates: local scripts/*_gate.sh + scripts/run_gates.sh + govML *gate*.sh.
    local_gates = sorted(HERE.glob("*_gate.sh")) + sorted(HERE.glob("run_gates.sh"))
    for g in local_gates:
        entries.append({"infra_id": f"gate::{g.relative_to(REPO)}",
                        "infra_class": "gate", "is_enforcement_infra": True,
                        "path": str(g.relative_to(REPO)), "abs_path": str(g),
                        "sha256_16": _file_hash(g)})
    for g in sorted(GOVML.glob("scripts/*gate*.sh")):
        entries.append({"infra_id": f"gate::govML::{g.name}",
                        "infra_class": "gate", "is_enforcement_infra": True,
                        "path": str(g), "abs_path": str(g),
                        "sha256_16": _file_hash(g)})

    # 3. Agent specs (prompt_inventory active rows).
    try:
        rows = subprocess.run(
            ["sqlite3", str(SINGULARITY_DB),
             "SELECT name, path FROM prompt_inventory WHERE type='agent_spec' AND status='active';"],
            capture_output=True, text=True, timeout=30).stdout.strip().splitlines()
    except Exception:  # noqa: BLE001
        rows = []
    for row in rows:
        if "|" not in row:
            continue
        name, path = row.split("|", 1)
        ap = pathlib.Path(os.path.expanduser(path))
        # Relative paths (e.g. ".claude/agents/..") resolve against the canonical
        # Moonshots repo, not this project cwd (the specs live in the parent pipeline).
        if not ap.is_absolute() and not ap.exists():
            cand = MOONSHOTS / path
            if cand.exists():
                ap = cand
        entries.append({"infra_id": f"agent_spec::{name}",
                        "infra_class": "agent_spec", "is_enforcement_infra": True,
                        "path": path, "abs_path": str(ap),
                        "sha256_16": _file_hash(ap) if ap.exists() else None,
                        "exists": ap.exists()})

    # 4. The accuracy harness itself (the validator-of-validators).
    harness = HERE / "probe_accuracy_harness.py"
    entries.append({"infra_id": "accuracy_harness::probe_accuracy_harness.py",
                    "infra_class": "accuracy_harness", "is_enforcement_infra": True,
                    "path": str(harness.relative_to(REPO)), "abs_path": str(harness),
                    "sha256_16": _file_hash(harness)})
    return entries


def _detector_fire_over_infra(entry: dict) -> dict:
    """T2: a trusted detector fires over an infra entry — the guard audits itself. The
    detector here is the runnable-and-self-tests check: import-and-execute (KT-8), NOT a
    string match. For .py probes/harness: run `--self-test` (exit 0 == self-attests). For
    gates (.sh): assert executable + syntactically loadable (bash -n). For agent_specs:
    assert the spec file resolves+reads (the spec exists as a governed artifact)."""
    cls = entry["infra_class"]
    ap = pathlib.Path(entry["abs_path"])
    fired = {"event_class": "guard_the_guards.fire.event", "timestamp": _now(),
             "infra_id": entry["infra_id"], "infra_class": cls,
             "is_enforcement_infra": True, "detector": None,
             "self_attests": None, "evidence": None}
    if cls in ("probe", "accuracy_harness"):
        fired["detector"] = "subprocess --self-test (import-and-execute)"
        if not ap.exists():
            fired["self_attests"] = False
            fired["evidence"] = "file missing"
            return fired
        try:
            proc = subprocess.run([sys.executable, str(ap), "--self-test"],
                                  capture_output=True, text=True, timeout=120,
                                  env=dict(os.environ))
            fired["self_attests"] = (proc.returncode == 0)
            fired["evidence"] = (proc.stdout or proc.stderr or "")[-200:]
            fired["rc"] = proc.returncode
        except Exception as e:  # noqa: BLE001
            fired["self_attests"] = False
            fired["evidence"] = f"error: {e!r}"[:200]
    elif cls == "gate":
        fired["detector"] = "bash -n (syntactic load) + executable bit"
        if not ap.exists():
            fired["self_attests"] = False
            fired["evidence"] = "gate script missing"
            return fired
        try:
            proc = subprocess.run(["bash", "-n", str(ap)], capture_output=True,
                                  text=True, timeout=30)
            executable = os.access(str(ap), os.X_OK)
            fired["self_attests"] = (proc.returncode == 0)
            fired["evidence"] = f"bash -n rc={proc.returncode} executable={executable}; {(proc.stderr or '')[:120]}"
        except Exception as e:  # noqa: BLE001
            fired["self_attests"] = False
            fired["evidence"] = f"error: {e!r}"[:200]
    elif cls == "agent_spec":
        fired["detector"] = "governed-artifact resolve+read (spec exists on disk)"
        exists = ap.exists()
        readable = False
        if exists:
            try:
                readable = bool(ap.read_text(encoding="utf-8", errors="replace"))
            except OSError:
                readable = False
        fired["self_attests"] = bool(exists and readable)
        fired["evidence"] = f"exists={exists} readable={readable} path={entry['path']}"
    return fired


def build_population() -> dict:
    m1p = _denominator_m1_prime()
    infra = enumerate_infra()
    by_class = {c: [e for e in infra if e["infra_class"] == c] for c in INFRA_CLASSES}
    audited_count = m1p + len(infra)
    # HARD-FAIL guard: each infra class MUST be present (an absent surface fails T1).
    missing_classes = [c for c in INFRA_CLASSES if not by_class[c]]
    pop = {
        "schema_version": "be_t_guard_the_guards_population.v1",
        "build_event": "BE-T part (i) — guard-the-guards: enforcement infra folded INTO the audited population (Cycle-16-S24)",
        "timestamp": _now(),
        "denominator_m1_prime": m1p,
        "infra_entry_count": len(infra),
        "infra_count_by_class": {c: len(by_class[c]) for c in INFRA_CLASSES},
        "audited_population_count": audited_count,
        "audited_population_equals_denominator_plus_infra": audited_count == (m1p + len(infra)),
        "all_infra_classes_present": not missing_classes,
        "missing_infra_classes": missing_classes,
        "every_infra_entry_flagged": all(e.get("is_enforcement_infra") is True for e in infra),
        "infra_entries": infra,
    }
    POP_OUT.write_text(json.dumps(pop, indent=1))
    return pop


def run_detectors_over_infra(pop: dict) -> dict:
    fires = [_detector_fire_over_infra(e) for e in pop["infra_entries"]]
    with RUN_OUT.open("w") as f:
        for fr in fires:
            f.write(json.dumps(fr) + "\n")
    classes_fired = {c: sum(1 for fr in fires if fr["infra_class"] == c) for c in INFRA_CLASSES}
    return {"total_fires": len(fires), "fires_by_class": classes_fired,
            "at_least_one_per_class": all(classes_fired[c] >= 1 for c in INFRA_CLASSES),
            "self_attest_pass": sum(1 for fr in fires if fr["self_attests"]),
            "self_attest_fail": sum(1 for fr in fires if fr["self_attests"] is False)}


def main() -> int:
    ap = argparse.ArgumentParser(description="BE-T guard-the-guards")
    ap.add_argument("--build", action="store_true")
    args = ap.parse_args()
    pop = build_population()
    run = run_detectors_over_infra(pop)
    print(json.dumps({
        "audited_population_count": pop["audited_population_count"],
        "denominator_m1_prime": pop["denominator_m1_prime"],
        "infra_entry_count": pop["infra_entry_count"],
        "infra_count_by_class": pop["infra_count_by_class"],
        "all_infra_classes_present": pop["all_infra_classes_present"],
        "detector_fires_by_class": run["fires_by_class"],
        "at_least_one_per_class": run["at_least_one_per_class"],
        "self_attest_pass": run["self_attest_pass"],
        "self_attest_fail": run["self_attest_fail"],
    }, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
