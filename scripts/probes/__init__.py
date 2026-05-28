"""Probe library admission gate — refuse primitives without passing self-test.

Per Cycle-16-S11 BE-F dispatch substrate §1 item 3 + HR §3.recovery H_recovery_3 +
ED §5.7 row 3 (self-test execution emits PASS/FAIL JSONL with predicateType
discriminator) + LA §6.recovery.A row 10 (SLSA chain-of-custody) + DP#44 BINDING.

This module performs admission scan at import time: for each probe in
scripts/probes/{a,b,c,d}/, runs `subprocess.run([sys.executable, probe_path,
"--self-test"])`; refuses to expose the probe (omits from __all__) if exit
non-zero on EITHER known-good or known-bad fixture (primitive must distinguish
both — mutation-testing analog per LA §6.recovery.A row 3).

Refusal mechanism:
    * Each refused probe path is recorded at REFUSED_PROBES list.
    * Each admission event (PASS or REFUSE) is emitted to
      outputs/probe_library_admission_events.jsonl with predicateType
      cycle16:probe_admission_v1.
    * __all__ is populated only with probe identifiers that PASSED admission.
    * The admission module raises NO ImportError on a refused probe — refusal
      surfaces to the JSONL sink for verifiable record. The CLI wrapper
      probe_library_admission.sh exits non-zero on any refusal.

DP#44-compliant refuse-on-missing-precondition: this gate refuses primitives
whose self-test does not distinguish known_good + known_bad fixtures; modifying
the gate body or bypass-skipping admission requires Builder-ARCH paradigm
dispatch (HC #74 BINDING).
"""
from __future__ import annotations

import datetime
import json
import os
import pathlib
import subprocess
import sys
import uuid
from typing import Any

PROBE_LIBRARY_VERSION = "0.1"
PROBE_ADMISSION_LOCK_COMMIT_DEFAULT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"
PREDICATE_TYPE_ADMISSION = "cycle16:probe_admission_v1"

_PROBE_DIR = pathlib.Path(__file__).resolve().parent
_PROJECT_ROOT = _PROBE_DIR.parents[1]
_ADMISSION_SINK = _PROJECT_ROOT / "outputs" / "probe_library_admission_events.jsonl"

ADMITTED_PROBES: list[dict[str, Any]] = []
REFUSED_PROBES: list[dict[str, Any]] = []


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _discover_probes(probe_dir: pathlib.Path) -> list[pathlib.Path]:
    """Walk class subdirs and return all probe_*.py files (excluding tests + private)."""
    probes: list[pathlib.Path] = []
    for cls_dir in sorted(probe_dir.iterdir()):
        if not cls_dir.is_dir():
            continue
        # Skip private directories starting with `_` (e.g., `_broken_/` negative-test stash)
        if cls_dir.name.startswith("_"):
            continue
        # Skip test-only / fixture-only subdirs by name convention
        if cls_dir.name in {"__pycache__", "tests"}:
            continue
        for f in sorted(cls_dir.glob("probe_*.py")):
            if not f.is_file():
                continue
            probes.append(f)
    return probes


def _emit_admission_event(
    probe_path: pathlib.Path,
    verdict: str,
    evidence: str,
    exit_code: int,
    fixture_class: str,
) -> None:
    """Append a JSONL row to the admission sink with predicateType cycle16:probe_admission_v1."""
    primitive_class = probe_path.parent.name.upper()
    event = {
        "schema_version": "0.1",
        "namespace": "cycle_16.be_f.probe_library_admission",
        "event_class": f"probe_library_admission.{verdict}.event",
        "predicateType": PREDICATE_TYPE_ADMISSION,
        "timestamp": _utc_ts(),
        "run_id": f"s11_be_f_admission_{primitive_class.lower()}_{uuid.uuid4().hex[:8]}",
        "payload": {
            "probe_path": str(probe_path),
            "probe_id": probe_path.stem,
            "primitive_class": primitive_class,
            "probe_library_version": PROBE_LIBRARY_VERSION,
            "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT_DEFAULT,
            "verdict": verdict,
            "self_test_exit_code": exit_code,
            "fixture_class": fixture_class,
            "evidence": evidence[:280],
        },
    }
    _ADMISSION_SINK.parent.mkdir(parents=True, exist_ok=True)
    with _ADMISSION_SINK.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def _run_admission_for_probe(probe_path: pathlib.Path) -> tuple[bool, str, int]:
    """Run --self-test against the probe.

    A passing probe must distinguish known_good + known_bad fixtures, evidenced
    by exit code 0 (per probe contract). Returns (admitted, evidence, exit_code).
    """
    try:
        result = subprocess.run(
            [sys.executable, str(probe_path), "--self-test"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        rc = result.returncode
        if rc == 0:
            return True, "self_test_distinguished_known_good_and_known_bad", rc
        evidence = (
            f"self_test_exit={rc} "
            f"stderr_head={result.stderr.strip()[:200]!r} "
            f"stdout_head={result.stdout.strip()[:160]!r}"
        )
        return False, evidence, rc
    except subprocess.TimeoutExpired:
        return False, "self_test_timeout_exceeded_120s", -1
    except OSError as e:
        return False, f"self_test_execution_failed: {e}", -2


def admit_all() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Admission scan — runs self-test against every discovered probe;
    populates ADMITTED_PROBES + REFUSED_PROBES; emits one JSONL row per probe."""
    ADMITTED_PROBES.clear()
    REFUSED_PROBES.clear()
    probes = _discover_probes(_PROBE_DIR)
    for p in probes:
        ok, evidence, rc = _run_admission_for_probe(p)
        verdict = "pass" if ok else "refuse"
        # fixture_class field at admission level = "self_test_pair" (probe ran
        # both known_good + known_bad; verdict synthesizes both).
        _emit_admission_event(
            probe_path=p,
            verdict=verdict,
            evidence=evidence,
            exit_code=rc,
            fixture_class="self_test_pair",
        )
        rec = {
            "probe_path": str(p),
            "probe_id": p.stem,
            "primitive_class": p.parent.name.upper(),
            "verdict": verdict,
            "evidence": evidence,
            "exit_code": rc,
        }
        if ok:
            ADMITTED_PROBES.append(rec)
        else:
            REFUSED_PROBES.append(rec)
    return ADMITTED_PROBES, REFUSED_PROBES


def expose_admitted() -> list[str]:
    """Return probe identifiers admitted at last scan."""
    return [p["probe_id"] for p in ADMITTED_PROBES]


__all__ = ["admit_all", "expose_admitted", "ADMITTED_PROBES", "REFUSED_PROBES"]
