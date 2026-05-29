#!/usr/bin/env python3
"""Probe Class D — MethodologyCommitment behavioral implementation check.

Per Cycle-16-S11 BE-F dispatch substrate §1 item 1 + HR §3.recovery H_recovery_3 +
ED §5.7 trace_id linkage grounding + LA §6.recovery.A row 4 (OTEL trace context) +
row 10 (SLSA in-toto Statement with predicateType: cycle16:probe_fire_v1).

Behavioral check (per HC #72 anti-substitution discipline):
    implemented: true ONLY when (i) the runnable artifact named at
    cycle16:runnableArtifactRef has FIRED ≥1 time post-authoring (event in
    outputs/*_events.jsonl matching artifact-id within recency window), OR
    (ii) a downstream warmup transcript / FINDINGS Layer 5 cites the
    commitment by trace_id. Pure FINDINGS-mention WITHOUT downstream
    application evidence = implemented: false (citation-only is documentary
    not behavioral per HC #72).

Probe contract:
    Input: spec_iri + path-to-commitment-source (FINDINGS.md@LXX) +
           optional runnable_artifact_ref + optional trace_id.
    Output: dict with {implemented: bool, evidence: str, probe_id, run_id,
            timestamp, primitive_class: 'D', spec_iri, evidence_type}.
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
from typing import Any, Iterable

PROBE_VERSION = "0.1"
PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"
PROBE_ID = "probe_methodology_commitment_v0.1"
PRIMITIVE_CLASS = "D"
PREDICATE_TYPE_FIRE = "cycle16:probe_fire_v1"
PREDICATE_TYPE_SELF_TEST = "cycle16:probe_self_test_v1"


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _short_iri(spec_iri: str) -> str:
    tail = spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail.replace("spec_retroactive_", "").replace("-", "_")[:24] or "anon"


def _commitment_source_exists(path: str, token: str) -> tuple[bool, str]:
    """Precondition (i): the commitment is authored in a real source."""
    p = pathlib.Path(os.path.expanduser(path))
    if not p.exists():
        return False, "commitment_source_not_found"
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"commitment_source_unreadable: {e}"
    # token may be e.g. "R1" or "Binding 6"; permit either
    if re.search(rf"\b{re.escape(token)}\b", body):
        return True, f"commitment_token_present_in {p}"
    return False, f"commitment_token_absent={token}"


# Files the BE-M harness itself writes into outputs/ — EXCLUDED from the scan
# so the probe never reads the harness's own (or a sibling probe's) fire output
# = circular contamination (validate-the-validator hazard). Mirrors the harness's
# own exclusion set; independently authored here, NOT imported.
_HARNESS_OWN_SINKS = {"probe_accuracy_events.jsonl"}


def _is_harness_own_sink(path: pathlib.Path) -> bool:
    return path.name in _HARNESS_OWN_SINKS or path.name.startswith(".acc_probe_fire_")


def _token_in_structured_field(rec: dict, needles: set) -> bool:
    """Structured-field match (independently authored to mirror the GT's
    `_token_in_structured_field`, NOT imported): the token must appear inside a
    STRUCTURED field of the parsed JSON record — event_class OR run_id OR a
    string value of the payload dict — NOT as an incidental substring anywhere
    in the raw line."""
    ec = str(rec.get("event_class") or "")
    rid = str(rec.get("run_id") or "")
    for n in needles:
        if n and (n in ec or n in rid):
            return True
    payload = rec.get("payload")
    if isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, str):
                for n in needles:
                    if n and n in v:
                        return True
    return False


def _downstream_jsonl_fire(
    runnable_artifact_ref: str | None,
    jsonl_search_roots: Iterable[str],
    commitment_token: str,
    recency_window_minutes: int,
) -> tuple[bool, str]:
    """Behavioral evidence (i): runnable artifact has FIRED ≥1 time post-authoring.

    A fire is a downstream JSONL record where the artifact stem / commitment token
    appears as a STRUCTURED FIELD VALUE (event_class | run_id | payload string
    value) of the parsed record — NOT an incidental substring anywhere in the
    line (the raw-substring match over-counted generic tokens such as HC-11 /
    DP#44 / Binding 6/7 → 28 FPs). Harness-own sink files are excluded to avoid
    circular contamination.
    """
    if not runnable_artifact_ref:
        return False, "no_runnable_artifact_ref_declared"
    artifact_stem = pathlib.Path(runnable_artifact_ref).stem
    # Match either artifact_stem OR commitment_token in JSONL rows
    needles = {artifact_stem}
    if commitment_token:
        needles.add(commitment_token)
    needles.discard("")
    now_ts = datetime.datetime.now(datetime.timezone.utc).timestamp()
    cutoff = now_ts - recency_window_minutes * 60
    hits: list[str] = []
    for root in jsonl_search_roots:
        rp = pathlib.Path(os.path.expanduser(root))
        if not rp.exists():
            continue
        for jsonl in rp.rglob("*_events.jsonl"):
            if _is_harness_own_sink(jsonl):
                continue
            try:
                if jsonl.stat().st_mtime < cutoff:
                    continue
                with jsonl.open("r", encoding="utf-8", errors="replace") as f:
                    for lineno, line in enumerate(f, 1):
                        line = line.strip()
                        if not line:
                            continue
                        # cheap prefilter before JSON parse
                        if not any(n in line for n in needles):
                            continue
                        try:
                            rec = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if _token_in_structured_field(rec, needles):
                            hits.append(f"{jsonl}:{lineno}")
                            if len(hits) >= 2:
                                return (
                                    True,
                                    f"downstream_jsonl_fire (structured-field): {hits[0]}",
                                )
            except OSError:
                continue
    if hits:
        return True, f"downstream_jsonl_fire (structured-field): {hits[0]}"
    return False, "no_downstream_jsonl_fire_found"


def _warmup_transcript_citation(
    trace_id: str | None,
    commitment_token: str | None,
    md_search_roots: Iterable[str],
) -> tuple[bool, str]:
    """Behavioral evidence (ii): downstream warmup transcript / FINDINGS Layer 5
    cites the commitment by a STRUCTURED, collision-free trace_id ONLY.

    GT (gt_class_d) recognises NO md-citation path; it labels implemented purely
    on token-in-source AND a structured-field JSONL fire. A bare commitment_token
    substring in a downstream FINDINGS/warmup md is an incidental documentary
    mention (HC #72: citation-only is documentary, not behavioral) and collides
    with countless rule citations (HC-11 / DP#44 / Binding 6/7 / Pattern N) →
    28 FPs vs GT. We therefore restrict this fallback to a unique trace_id needle
    and DROP the generic commitment_token substring match, so the probe label
    matches GT semantics. With no trace_id (the aggregate-cycle default) this path
    does not fire, exactly mirroring GT's no-citation-path stance."""
    if not trace_id:
        return False, "no_trace_id_for_warmup_citation (token-only citation is documentary, not behavioral — GT-aligned)"
    needles = {trace_id}
    cycle_cites: list[str] = []
    for root in md_search_roots:
        rp = pathlib.Path(os.path.expanduser(root))
        if not rp.exists():
            continue
        targets = list(rp.rglob("coach_warmup.md"))
        targets += list(rp.rglob("FINDINGS.md"))
        for md in targets:
            try:
                body = md.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for n in needles:
                # The citation must be a structural reference (not the original auth)
                if re.search(rf"\b{re.escape(n)}\b", body):
                    cycle_cites.append(str(md))
                    if len(cycle_cites) >= 2:
                        return (
                            True,
                            f"downstream_citation: {cycle_cites[0]}",
                        )
    if cycle_cites:
        return True, f"downstream_citation: {cycle_cites[0]}"
    return False, "no_downstream_citation_found"


def probe(
    spec_iri: str,
    commitment_source_path: str | None = None,
    commitment_token: str | None = None,
    runnable_artifact_ref: str | None = None,
    trace_id: str | None = None,
    jsonl_search_roots: list[str] | None = None,
    md_search_roots: list[str] | None = None,
    recency_window_minutes: int = 60 * 24 * 60,  # 60 days
    expected_implemented: bool | None = None,
) -> dict[str, Any]:
    """Class D MethodologyCommitment behavioral probe.

    Acceptance: source-exists (precondition) AND (downstream_jsonl_fire OR
    downstream_citation). Pure FINDINGS-mention without downstream application
    or downstream citation = implemented: false (HC #72 anti-substitution).
    """
    run_id = f"s11_be_f_production_d_{_short_iri(spec_iri)}_{uuid.uuid4().hex[:6]}"
    ts = _utc_ts()
    commitment_token = commitment_token or _short_iri(spec_iri)

    # Precondition (i): commitment source present
    if not commitment_source_path:
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
            "evidence": "precondition_failed: no commitment_source_path provided",
            "evidence_type": "precondition_missing",
        }
    src_ok, src_evidence = _commitment_source_exists(
        commitment_source_path, commitment_token
    )
    if not src_ok:
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
            "evidence": f"precondition_failed: {src_evidence}",
            "evidence_type": "precondition_missing",
        }

    # Behavioral (i): downstream JSONL fire
    jsonl_roots = jsonl_search_roots or [
        "~/cycle_10_autonomous_cycle_apparatus_build/outputs/",
        "~/cycle_16_close_spec_to_implementation_gap_build/outputs/",
        "~/Moonshots_Career_Thesis_v2/.claude/runtime_emit/",
    ]
    fire_ok, fire_evidence = _downstream_jsonl_fire(
        runnable_artifact_ref,
        jsonl_roots,
        commitment_token,
        recency_window_minutes,
    )
    if fire_ok:
        return {
            "probe_id": PROBE_ID,
            "probe_version": PROBE_VERSION,
            "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
            "primitive_class": PRIMITIVE_CLASS,
            "spec_iri": spec_iri,
            "run_id": run_id,
            "timestamp": ts,
            "predicateType": PREDICATE_TYPE_FIRE,
            "implemented": True,
            "evidence": fire_evidence,
            "evidence_type": "probe_fire_aggregate",
            "behavioral_path": "downstream_jsonl_fire",
        }

    # Behavioral (ii): downstream citation
    md_roots = md_search_roots or [
        "~/cycle_11_capstone_signal_unification_build/",
        "~/cycle_12_evaluator_substrate_apparatus_build/",
        "~/cycle_13_build_cycle_shift_left_build/",
        "~/cycle_14_signal_unification_build/",
        "~/cycle_15_capstone_prioritizer_build/",
        "~/cycle_16_close_spec_to_implementation_gap_build/",
    ]
    cite_ok, cite_evidence = _warmup_transcript_citation(
        trace_id, commitment_token, md_roots
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
        "implemented": cite_ok,
        "evidence": cite_evidence if cite_ok else f"no_behavioral_evidence (fire: {fire_evidence}; cite: {cite_evidence})",
        "evidence_type": "probe_fire_aggregate",
        "behavioral_path": "downstream_citation" if cite_ok else "none",
    }


def _self_test(fixture_dir: pathlib.Path) -> int:
    project_root = pathlib.Path(__file__).resolve().parents[3]
    sink = project_root / "outputs" / "probe_library_self_test_events.jsonl"
    good = sorted(fixture_dir.glob("known_good_d_*.json"))
    bad = sorted(fixture_dir.glob("known_bad_d_*.json"))
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
            commitment_source_path=cfg.get("commitment_source_path"),
            commitment_token=cfg.get("commitment_token"),
            runnable_artifact_ref=cfg.get("runnable_artifact_ref"),
            trace_id=cfg.get("trace_id"),
            jsonl_search_roots=cfg.get("jsonl_search_roots"),
            md_search_roots=cfg.get("md_search_roots"),
            recency_window_minutes=cfg.get(
                "recency_window_minutes", 60 * 24 * 60
            ),
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
                "run_id": f"s11_be_f_probe_lib_self_test_d_{fx.stem}_{uuid.uuid4().hex[:6]}",
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
                    "behavioral_path": result.get("behavioral_path"),
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
        if s.get("spec_class") == "d_methodology_commitment"
    ]
    if limit:
        specs = specs[:limit]
    sink = pathlib.Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    fired = 0
    with sink.open("a", encoding="utf-8") as f:
        for s in specs:
            audit_tuple = s.get("audit_tuple") or [None, None, None]
            src_path = os.path.expanduser(audit_tuple[1]) if audit_tuple[1] else None
            # audit_tuple[2] = token like "R1@L4" -> extract token before @
            token = (
                (audit_tuple[2] or "").split("@")[0]
                if len(audit_tuple) >= 3 and audit_tuple[2]
                else s.get("name_truncated") or _short_iri(s["spec_id"])
            )
            # Heuristic runnable_artifact_ref: for methodology commitments,
            # the runnable artifact is typically a script/gate referenced
            # in the FINDINGS where the commitment lives; we pass the
            # token so the JSONL search finds matching event_class rows.
            result = probe(
                spec_iri=s["spec_id"],
                commitment_source_path=src_path,
                commitment_token=token,
                runnable_artifact_ref=token,
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
                    "behavioral_path": result.get("behavioral_path"),
                },
            }
            f.write(json.dumps(row) + "\n")
            fired += 1
    print(
        f"PASS: aggregate-cycle fired {fired} probes against MethodologyCommitment specs "
        f"(sink={sink_path})"
    )
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Probe Class D — MethodologyCommitment")
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
    p.add_argument("--commitment-source-path", default=None)
    p.add_argument("--commitment-token", default=None)
    p.add_argument("--runnable-artifact-ref", default=None)
    p.add_argument("--trace-id", default=None)
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
            commitment_source_path=args.commitment_source_path,
            commitment_token=args.commitment_token,
            runnable_artifact_ref=args.runnable_artifact_ref,
            trace_id=args.trace_id,
        )
        print(json.dumps(result, indent=2))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
