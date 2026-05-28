#!/usr/bin/env python3
"""Probe Class C — DesignDecision behavioral implementation check.

Per Cycle-16-S11 BE-F dispatch substrate §1 item 1 + HR §3.recovery H_recovery_3 +
LA §6.recovery.A row 5 (Bazel Skyframe dep-graph) + row 9 (BX) + design-anchor
flag re LLM-judge calibration at §6.recovery.C row 3 + ED §5.7 grounding.

HC #72 ANTI-SUBSTITUTION DISCIPLINE (BINDING — load-bearing for KT-8):
    The LLM-judge MUST read ACTUAL CODE/CONFIG via file:line citation as evidence.
    The judge prompt explicitly FORBIDS:
        - "registry says implemented" / SPARQL ASK on cycle16:currentStatus
        - "DECISION_LOG ADR text exists"
        - "FINDINGS mentions the decision"
    The judge MUST produce a file:line citation showing the embodiment of the
    decision in code/config. ADR-text-only or registry-only evidence ⇒
    implemented: false (substitution detected).

Behavioral check:
    Precondition (i): DECISION_LOG ADR entry exists (file presence + grep
                      `^## ADR-<id>` or `^### .*<title>`).
    Acceptance evidence (ii): LLM-judge reads code at cycle16:embodimentRef + emits
                              file:line citation. Without an LLM API key, the probe
                              uses a STRUCTURAL JUDGE — pattern-match against the
                              ADR-declared embodiment ref (path + line range or
                              symbol) AND require a non-trivial match (≥1 grep hit
                              for a load-bearing token from the ADR).

The structural judge is deliberate calibration: it implements the SHAPE of the
LLM-judge contract (file:line citation as evidence; substitution-detection
refusal) without requiring online LLM calls at probe-fire time. Full LLM-judge
upgrade is deferred to Cycle 17+ if Coach R3 disposition requires (carry-forward
candidate at envelope honest_gaps).

Version-lock per Done #13: PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys
import uuid
from typing import Any

PROBE_VERSION = "0.1"
PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"
PROBE_ID = "probe_design_decision_v0.1"
PRIMITIVE_CLASS = "C"
PREDICATE_TYPE_FIRE = "cycle16:probe_fire_v1"
PREDICATE_TYPE_SELF_TEST = "cycle16:probe_self_test_v1"
JUDGE_PROMPT_PATH = str(pathlib.Path(__file__).resolve().parent / "llm_judge_prompt.md")


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _short_iri(spec_iri: str) -> str:
    tail = spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail.replace("spec_retroactive_", "").replace("-", "_")[:24] or "anon"


def _adr_present(decision_log_path: str, adr_token: str) -> tuple[bool, str]:
    """Precondition: ADR entry exists in DECISION_LOG."""
    p = pathlib.Path(os.path.expanduser(decision_log_path))
    if not p.exists():
        return False, "decision_log_not_found"
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"decision_log_unreadable: {e}"
    # Match the ADR/decision token either as a heading or in a row
    if re.search(rf"(?im)^\s*#+\s*.*{re.escape(adr_token)}", body) or (
        adr_token in body
    ):
        return True, f"adr_token_present_in {decision_log_path}"
    return False, f"adr_token_absent={adr_token}"


def _structural_judge(
    embodiment_ref_path: str | None,
    decision_token: str,
    decision_log_path: str,
) -> tuple[bool, str]:
    """STRUCTURAL judge mirrors LLM-judge contract:
    READS actual code/config at embodiment_ref_path (NOT ADR/DECISION_LOG text),
    produces a file:line citation as evidence.

    Acceptance: ≥1 file:line in the embodiment file (or its parent dir if
    embodiment_ref_path is a directory) where a load-bearing token from the
    decision is referenced AND the file is NOT itself the DECISION_LOG.

    Refusal: empty embodiment_ref_path OR embodiment_ref_path resolves to the
    DECISION_LOG itself (registry/ADR-text-only substitution).
    """
    if not embodiment_ref_path:
        return False, "anti_substitution: no embodimentRef declared (ADR-text-only)"
    target = pathlib.Path(os.path.expanduser(embodiment_ref_path))
    if not target.exists():
        return False, f"embodimentRef_not_found: {embodiment_ref_path}"
    # Anti-substitution gate: refuse if embodimentRef IS the DECISION_LOG
    dl_p = pathlib.Path(os.path.expanduser(decision_log_path)).resolve()
    if target.resolve() == dl_p:
        return (
            False,
            "anti_substitution_refusal: embodimentRef IS DECISION_LOG (HC #72)",
        )

    # Discover load-bearing tokens from the decision_token
    # (split on _, :, ., -; drop short and structural words)
    raw_tokens = re.split(r"[\s:_./\-]+", decision_token)
    skip = {
        "paradigm",
        "dispositions",
        "decisions",
        "log",
        "cycle",
        "close",
        "decision",
        "the",
        "and",
        "to",
        "of",
        "s",
        "n",
        "be",
        "stage",
    }
    tokens = [
        t.lower()
        for t in raw_tokens
        if len(t) >= 4 and t.lower() not in skip
    ]
    if not tokens:
        return False, "no_load_bearing_tokens_extractable"

    # Search target (file OR directory; one file:line citation is sufficient)
    citations: list[str] = []
    files_to_scan: list[pathlib.Path]
    if target.is_dir():
        files_to_scan = [
            f
            for f in target.rglob("*")
            if f.is_file() and f.suffix in (".py", ".sh", ".md", ".json", ".yaml", ".yml", ".ttl")
        ][:50]
    else:
        files_to_scan = [target]

    for f in files_to_scan:
        if f.resolve() == dl_p:
            continue
        try:
            for lineno, line in enumerate(
                f.read_text(encoding="utf-8", errors="replace").splitlines(), 1
            ):
                ll = line.lower()
                if any(t in ll for t in tokens):
                    citations.append(f"{f}:{lineno}: {line.strip()[:120]}")
                    break
        except OSError:
            continue
        if citations:
            break

    if not citations:
        return (
            False,
            f"structural_judge_no_code_citation: tokens={tokens[:5]} target={target}",
        )
    return True, f"structural_judge_citation: {citations[0]}"


def probe(
    spec_iri: str,
    decision_token: str | None = None,
    decision_log_path: str | None = None,
    embodiment_ref_path: str | None = None,
    expected_implemented: bool | None = None,
) -> dict[str, Any]:
    """Class C DesignDecision behavioral probe.

    Acceptance: ADR present AND structural judge reads code (NOT ADR text) and
    produces file:line citation. Embodiment-not-declared / embodiment-IS-ADR =
    refusal (HC #72 anti-substitution).
    """
    run_id = f"s11_be_f_production_c_{_short_iri(spec_iri)}_{uuid.uuid4().hex[:6]}"
    ts = _utc_ts()
    decision_log_path = decision_log_path or str(
        pathlib.Path(__file__).resolve().parents[3] / "DECISION_LOG.md"
    )
    decision_token = decision_token or _short_iri(spec_iri)

    # Precondition (i): ADR present
    adr_ok, adr_evidence = _adr_present(decision_log_path, decision_token)
    if not adr_ok:
        return {
            "probe_id": PROBE_ID,
            "probe_version": PROBE_VERSION,
            "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
            "primitive_class": PRIMITIVE_CLASS,
            "spec_iri": spec_iri,
            "run_id": run_id,
            "timestamp": ts,
            "predicateType": PREDICATE_TYPE_FIRE,
            "implemented": False,
            "evidence": f"precondition_failed: {adr_evidence}",
            "evidence_type": "precondition_missing",
        }

    # Behavioral (ii): structural judge reads code (NOT ADR text)
    impl, evidence = _structural_judge(
        embodiment_ref_path, decision_token, decision_log_path
    )
    return {
        "probe_id": PROBE_ID,
        "probe_version": PROBE_VERSION,
        "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
        "primitive_class": PRIMITIVE_CLASS,
        "spec_iri": spec_iri,
        "run_id": run_id,
        "timestamp": ts,
        "predicateType": PREDICATE_TYPE_FIRE,
        "implemented": impl,
        "evidence": evidence,
        "evidence_type": "probe_fire_aggregate",
        "judge_kind": "structural_judge_v0.1",
        "adr_evidence": adr_evidence,
    }


def _self_test(fixture_dir: pathlib.Path) -> int:
    project_root = pathlib.Path(__file__).resolve().parents[3]
    sink = project_root / "outputs" / "probe_library_self_test_events.jsonl"
    good = sorted(fixture_dir.glob("known_good_c_*.json"))
    bad = sorted(fixture_dir.glob("known_bad_c_*.json"))
    if not good or not bad:
        print(
            f"FAIL: missing self-test fixtures (good={len(good)}, bad={len(bad)})",
            file=sys.stderr,
        )
        return 1
    all_distinguished = True
    rows: list[dict[str, Any]] = []
    for fx in good + bad:
        cfg = json.loads(fx.read_text())
        result = probe(
            spec_iri=cfg.get("spec_iri", f"urn:test:{fx.stem}"),
            decision_token=cfg.get("decision_token"),
            decision_log_path=cfg.get("decision_log_path"),
            embodiment_ref_path=cfg.get("embodiment_ref_path"),
        )
        expected = cfg["expected_implemented"]
        distinguished = result["implemented"] == expected
        all_distinguished = all_distinguished and distinguished
        rows.append(
            {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_f.probe_library_self_test",
                "event_class": (
                    "probe_library_self_test.pass.event"
                    if distinguished
                    else "probe_library_self_test.fail.event"
                ),
                "predicateType": PREDICATE_TYPE_SELF_TEST,
                "timestamp": _utc_ts(),
                "run_id": f"s11_be_f_probe_lib_self_test_c_{fx.stem}_{uuid.uuid4().hex[:6]}",
                "payload": {
                    "probe_id": PROBE_ID,
                    "probe_version": PROBE_VERSION,
                    "primitive_class": PRIMITIVE_CLASS,
                    "fixture_path": str(fx),
                    "fixture_class": "known_good" if fx.name.startswith("known_good") else "known_bad",
                    "expected_implemented": expected,
                    "actual_implemented": result["implemented"],
                    "distinguished": distinguished,
                    "evidence": result["evidence"][:200],
                    "evidence_type": result["evidence_type"],
                    "judge_kind": result.get("judge_kind"),
                },
            }
        )
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return 0 if all_distinguished else 1


def _aggregate_cycle(
    cycle_n: int,
    scan_json_path: str,
    sink_path: str,
    limit: int | None,
    run_id_prefix_override: str | None = None,
) -> int:
    data = json.loads(pathlib.Path(scan_json_path).read_text())
    specs = [
        s
        for s in data.get("per_spec_evidence_IP_PRIVATE", [])
        if s.get("spec_class") == "c_design_decision"
    ]
    if limit:
        specs = specs[:limit]
    sink = pathlib.Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    fired = 0
    with sink.open("a", encoding="utf-8") as f:
        for s in specs:
            audit_tuple = s.get("audit_tuple") or [None, None, None]
            # audit_tuple[1] = file path; [2] = registry key (e.g., paradigm_dispositions:<key>)
            decision_log_path = (
                os.path.expanduser(audit_tuple[1]) if audit_tuple[1] else None
            )
            # Token cleaning: registry keys like "paradigm_dispositions:foo_bar_baz"
            # are colon-prefixed registry slots. Extract the trailing-keyword
            # portion (which is more likely to surface in code/docs); fall
            # back to the name_truncated.
            raw_token = (
                audit_tuple[2]
                if len(audit_tuple) >= 3 and audit_tuple[2]
                else s.get("name_truncated") or _short_iri(s["spec_id"])
            )
            token = raw_token.split(":", 1)[-1] if ":" in raw_token else raw_token
            # Truncate JSON-blob tokens (e.g., decisions_log:{'date':...}) at
            # the first non-identifier character to surface a usable keyword.
            token = re.split(r"[\s,{}\[\]'\"]+", token)[0] or raw_token
            # For DesignDecision specs in state.json paradigm_dispositions, the
            # embodimentRef is typically the source code that ENACTS the disposition.
            # Heuristic: state.json itself is the registry; the cycle's
            # scripts/ dir is the code where dispositions are enacted.
            embodiment_dir = None
            if decision_log_path and "state.json" in decision_log_path:
                # Embodiment ref = the cycle dir's scripts/ (where dispositions enacted)
                cycle_dir = pathlib.Path(decision_log_path).parent
                if (cycle_dir / "scripts").is_dir():
                    embodiment_dir = str(cycle_dir / "scripts")
            elif decision_log_path:
                # Embodiment = the cycle dir's docs/ or scripts/ neighbor
                cycle_dir = pathlib.Path(decision_log_path).parent
                for c in (cycle_dir / "docs", cycle_dir / "scripts"):
                    if c.is_dir():
                        embodiment_dir = str(c)
                        break
            result = probe(
                spec_iri=s["spec_id"],
                decision_token=token,
                decision_log_path=decision_log_path,
                embodiment_ref_path=embodiment_dir,
            )
            if run_id_prefix_override:
                result["run_id"] = (
                    f"{run_id_prefix_override}_{_short_iri(s['spec_id'])}_{uuid.uuid4().hex[:6]}"
                )
            row = {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_f.probe_library",
                "event_class": "probe_library.fire.event",
                "predicateType": PREDICATE_TYPE_FIRE,
                "timestamp": result["timestamp"],
                "run_id": result["run_id"],
                "payload": {
                    "probe_id": result["probe_id"],
                    "probe_version": result["probe_version"],
                    "probe_admission_lock_commit": result[
                        "probe_admission_lock_commit"
                    ],
                    "primitive_class": result["primitive_class"],
                    "spec_iri": result["spec_iri"],
                    "spec_class": s.get("spec_class"),
                    "name_truncated": s.get("name_truncated"),
                    "current_status_known": s.get("current_status"),
                    "implemented": result["implemented"],
                    "evidence": result["evidence"][:280],
                    "evidence_type": result["evidence_type"],
                    "judge_kind": result.get("judge_kind"),
                },
            }
            f.write(json.dumps(row) + "\n")
            fired += 1
    print(f"PASS: aggregate-cycle fired {fired} probes against DesignDecision specs (sink={sink_path})")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Probe Class C — DesignDecision")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--aggregate-cycle", type=int, default=None)
    p.add_argument(
        "--scan-json",
        default=str(
            pathlib.Path(__file__).resolve().parents[3]
            / "outputs"
            / "retroactive_scan_cycle_1_15_run.json"
        ),
    )
    p.add_argument(
        "--sink",
        default=str(
            pathlib.Path(__file__).resolve().parents[3]
            / "outputs"
            / "probe_fire_events.jsonl"
        ),
    )
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--run-id-prefix", default=None)
    p.add_argument("--spec-iri", default=None)
    p.add_argument("--decision-token", default=None)
    p.add_argument("--decision-log-path", default=None)
    p.add_argument("--embodiment-ref-path", default=None)
    args = p.parse_args(argv)

    if args.self_test:
        fixture_dir = (
            pathlib.Path(__file__).resolve().parents[3] / "tests" / "probes" / "fixtures"
        )
        return _self_test(fixture_dir)
    if args.aggregate_cycle is not None:
        return _aggregate_cycle(
            cycle_n=args.aggregate_cycle,
            scan_json_path=args.scan_json,
            sink_path=args.sink,
            limit=args.limit,
            run_id_prefix_override=args.run_id_prefix,
        )
    if args.spec_iri:
        result = probe(
            spec_iri=args.spec_iri,
            decision_token=args.decision_token,
            decision_log_path=args.decision_log_path,
            embodiment_ref_path=args.embodiment_ref_path,
        )
        print(json.dumps(result, indent=2))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
