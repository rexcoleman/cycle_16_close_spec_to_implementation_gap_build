#!/usr/bin/env python3
"""Probe Class E — KG-fidelity check ("does the KG tell the truth about reality?").

Per Cycle-16-S15 BE-J dispatch substrate §0-§7 + Done #23 (three integration
surfaces: write-time hook, periodic audit, cycle-close gate) + Done #41 (autonomy
floor: NO mandatory human step; conservative fail-safe disposition on ambiguity)
+ Done #39 (non-re-derivable fields reported `unverifiable` on their own line,
NEVER silently passed) + HC #72 anti-substitution discipline + KT-8 import+execute
discipline + the validate-the-validator cross-check (status-match is a
structurally-independent second derivation, a different code path from the KG
record).

WHAT CLASS E IS (and is NOT):
    Class E proves KG-RECORD-vs-reality fidelity — does the knowledge graph's
    recorded value match what is actually true in the source/world? It does NOT
    prove implementation-fidelity of the spec (that is Class F / BE-K), and BE-J
    does NOT prove Class E's population-level ACCURACY (that is the later
    probe-accuracy validation step, Done #25, against diverse independent
    automated ground truth). No "KG is 100% faithful" claim from BE-J alone.

THE NAIVE DESIGN IS FORBIDDEN (substrate §2):
    Checking a KG self-asserted flag (`source_present: true`, `validated: true`,
    or string-matching a `current_status` enum) is the EXACT proxy substitution
    Cycle 16 exists to kill. Class E MUST IMPORT+EXECUTE the real comparison:
      (1) Source-traceability — resolve the spec's source reference and READ it
          (git object via `git cat-file -e/-p`, OR filesystem path via
          os.path.exists + readable). NEVER trust a `source_present` field.
      (2) Field-match — for the mechanically re-derivable subset of fields,
          re-extract from the REAL source and DIFF against the KG value. A field
          that is NOT mechanically re-derivable is reported `unverifiable`
          per-field (its own line). Any DIFF mismatch → infidelity.
      (3) Status-match — dispatch to the matching BE-F probe by spec_type
          (A/B/C/D), RUN it live (import + execute), and compare its live
          `implemented` result to the KG's recorded `current_status`. Mismatch →
          KG infidelity. This is a structurally-independent second derivation.

CONSERVATIVE DISPOSITION (Done #41 + #39):
    Any spec the probe cannot verify (source unresolvable, probe error,
    ambiguous) → classed infidelity/unverified (fail-safe), surfaced in evidence
    + routed to the remediation queue; NEVER counted faithful. No human step
    anywhere in the path — ambiguity yields a conservative after-the-fact report
    line, never a block-on-Rex.

Version-lock per Done #13: PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned;
modifications require Builder-ARCH paradigm dispatch (HC #74 BINDING).
"""
from __future__ import annotations

import argparse
import datetime
import importlib.util
import json
import os
import pathlib
import subprocess
import sys
import urllib.parse
import urllib.request
import uuid
from typing import Any

PROBE_VERSION = "0.1"
# Build-time admission lock commit — reuses the BE-F probe-library admission
# lock-commit constant pattern (pinned at admission_v1 first PASS); bumps require
# Builder-ARCH paradigm dispatch (HC #74 BINDING).
PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"
PROBE_ID = "probe_kg_fidelity_v0.1"
PRIMITIVE_CLASS = "E"
PREDICATE_TYPE_FIRE = "cycle16:probe_fire_v1"
PREDICATE_TYPE_SELF_TEST = "cycle16:probe_self_test_v1"

DEFAULT_QUERY_ENDPOINT = os.environ.get(
    "CYCLE6_QUERY_ENDPOINT", "http://localhost:3030/cycle6/query"
)
ASSERTION_GRAPH = "http://cycle16.local/registry/assertion"
ONTOLOGY_NS = "http://cycle16.local/ontology#"

# 5-state status enum → boolean "should reality show this implemented?"
# running / long-running → an active/implemented spec → BE-F implemented expected True.
# dormant-silent / dormant-with-explicit-deferral / killed → NOT active → expected False.
STATUS_IMPLIES_IMPLEMENTED = {
    "running": True,
    "long-running": True,
    "dormant-silent": False,
    "dormant-with-explicit-deferral": False,
    "killed": False,
}

# spec_type → matching BE-F probe module path + the scan spec_class key.
_PROBE_DIR = pathlib.Path(__file__).resolve().parent.parent  # scripts/probes
BE_F_PROBES = {
    "AgentContract": (_PROBE_DIR / "a" / "probe_agent_contract.py", "a_agent_contract"),
    "Schema": (_PROBE_DIR / "b" / "probe_schema.py", "b_schema"),
    "DesignDecision": (_PROBE_DIR / "c" / "probe_design_decision.py", "c_design_decision"),
    "MethodologyCommitment": (
        _PROBE_DIR / "d" / "probe_methodology_commitment.py",
        "d_methodology_commitment",
    ),
}


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_iri(spec_iri: str) -> str:
    tail = spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail.replace("spec_retroactive_", "").replace("-", "_")[:24] or "anon"


def _sparql_query(endpoint: str, query: str) -> tuple[int, Any]:
    """Stdlib SPARQL query (mirrors spec_registry_authoring._sparql_post op='query').
    Returns (http_status, parsed_json_or_None). DO NOT add requests/SPARQLWrapper."""
    data = urllib.parse.urlencode({"query": query}).encode()
    req = urllib.request.Request(
        endpoint, data=data, headers={"Accept": "application/sparql-results+json"}
    )
    resp = urllib.request.urlopen(req, timeout=30)
    body = resp.read()
    parsed = None
    if resp.status == 200:
        try:
            parsed = json.loads(body)
        except json.JSONDecodeError:
            parsed = None
    return resp.status, parsed


def _read_kg_node(spec_iri: str, endpoint: str, named_graph: str) -> dict[str, str]:
    """Read all predicate/object pairs for a spec node from the NAMED GRAPH.
    EVERY query uses a GRAPH clause (default-graph query returns 0)."""
    if spec_iri.startswith("cycle16:"):
        full = f"{ONTOLOGY_NS}{spec_iri[len('cycle16:'):]}"
    elif spec_iri.startswith("http"):
        full = spec_iri
    else:
        full = f"{ONTOLOGY_NS}{spec_iri}"
    query = f"""
PREFIX cycle16: <{ONTOLOGY_NS}>
SELECT ?p ?o WHERE {{
  GRAPH <{named_graph}> {{
    <{full}> ?p ?o .
  }}
}}
"""
    status, parsed = _sparql_query(endpoint, query)
    fields: dict[str, str] = {}
    if status == 200 and parsed:
        for b in parsed.get("results", {}).get("bindings", []):
            pred = b["p"]["value"].rsplit("#", 1)[-1].rsplit("/", 1)[-1]
            obj = b["o"]["value"]
            # Map currentStatus / specType IRIs to their local keyword.
            if pred in ("currentStatus", "specType") and obj.startswith("http"):
                obj = obj.rsplit("#", 1)[-1].rsplit("/", 1)[-1]
            fields[pred] = obj
    fields["_http_status"] = str(status)
    fields["_spec_iri_full"] = full
    return fields


# --- scan-JSON source-of-record join (the source-truth carrier) ---------------


def _load_scan_index(scan_json_path: str | None) -> dict[str, dict[str, Any]]:
    """Build {scan_spec_id_short -> scan_record} from the retroactive scan JSON.

    The KG retroactive node IRIs (spec_retroactive_<hex8>) join EXACTLY to the
    scan-JSON spec_id (cycle16:spec_retroactive_<hex8>). The scan record carries
    audit_tuple — [repo_label, real_source_path, source_kind/token] — which is the
    SOURCE-OF-RECORD for re-derivation (the KG auditTrailLink is an opaque activity
    IRI, not a path). Empty dict if scan JSON absent (probe still fires; field-match
    + source-traceability degrade to unverifiable, conservative-fail-safe)."""
    idx: dict[str, dict[str, Any]] = {}
    if not scan_json_path:
        return idx
    p = pathlib.Path(scan_json_path)
    if not p.exists():
        return idx
    try:
        data = json.loads(p.read_text())
    except (OSError, json.JSONDecodeError):
        return idx
    for rec in data.get("per_spec_evidence_IP_PRIVATE", []):
        sid = rec.get("spec_id", "")
        short = sid.rsplit(":", 1)[-1]
        idx[short] = rec
    return idx


# --- (1) source-traceability ---------------------------------------------------


def _resolve_and_read_source(source_ref: str | None) -> tuple[bool, str]:
    """RESOLVE the source reference and READ it. Reachable+readable → pass.

    A git SHA → `git cat-file -e <sha>` (object exists) then `git cat-file -p`.
    A filesystem path → os.path.exists + readable (open one byte).
    NEVER trust a `source_present` field — we EXECUTE the resolve+read."""
    if not source_ref:
        return False, "source_traceability_FAIL: no source reference on record"
    ref = os.path.expanduser(source_ref.strip())
    # Git-SHA shape: 7-40 hex chars, no path separators.
    is_sha = (
        7 <= len(ref) <= 40
        and all(c in "0123456789abcdef" for c in ref.lower())
        and "/" not in ref
    )
    if is_sha:
        try:
            exists = subprocess.run(
                ["git", "cat-file", "-e", ref], capture_output=True, timeout=20
            )
            if exists.returncode != 0:
                return False, f"source_traceability_FAIL: git object {ref[:12]} unreachable"
            show = subprocess.run(
                ["git", "cat-file", "-p", ref],
                capture_output=True,
                timeout=20,
            )
            if show.returncode == 0 and show.stdout:
                return True, f"source_traceability_OK: git object {ref[:12]} read ({len(show.stdout)}B)"
            return False, f"source_traceability_FAIL: git object {ref[:12]} unreadable"
        except (OSError, subprocess.SubprocessError) as e:
            return False, f"source_traceability_FAIL: git resolve error {e!r}"
    # Filesystem path.
    path = pathlib.Path(ref)
    if not path.exists():
        return False, f"source_traceability_FAIL: path does not exist: {ref}"
    if path.is_dir():
        # A directory source is reachable if listable + non-empty.
        try:
            listed = any(path.iterdir())
            return (
                (True, f"source_traceability_OK: dir reachable+non-empty: {ref}")
                if listed
                else (False, f"source_traceability_FAIL: dir empty: {ref}")
            )
        except OSError as e:
            return False, f"source_traceability_FAIL: dir unreadable {e!r}"
    try:
        with path.open("rb") as f:
            f.read(1)
        return True, f"source_traceability_OK: file reachable+readable: {ref}"
    except OSError as e:
        return False, f"source_traceability_FAIL: file unreadable {e!r}: {ref}"


# --- (2) field-match (re-derive + diff) ----------------------------------------

# Spec-type classification by source kind / file extension — mechanically
# re-derived from the REAL source, NOT read from the KG.
def _rederive_spec_type(scan_rec: dict[str, Any] | None, source_ref: str | None) -> str | None:
    """Re-derive spec_type from the source's kind/extension (a different code path
    from the KG specType field). Returns the re-derived spec_type or None if not
    mechanically re-derivable."""
    if scan_rec:
        kind = (scan_rec.get("audit_tuple") or [None, None, None])
        source_kind = kind[2] if len(kind) >= 3 else None
        # source_kind tokens: 'agent_spec' -> AgentContract, 'schema_json'/'schema' -> Schema,
        # 'paradigm_dispositions:...' -> DesignDecision, 'R#@L#'/methodology -> MethodologyCommitment.
        sk = (source_kind or "").lower()
        if "agent_spec" in sk or sk == "agent":
            return "AgentContract"
        if "schema" in sk:
            return "Schema"
        if "paradigm_disposition" in sk or "decision" in sk or "adr" in sk:
            return "DesignDecision"
        if "@l" in sk or "methodology" in sk or sk.startswith("r"):
            return "MethodologyCommitment"
    # Fall back to extension-based classification of the source path.
    if source_ref:
        low = source_ref.lower()
        if low.endswith(".md") and "/agents/" in low:
            return "AgentContract"
        if low.endswith((".json", ".ttl", ".shacl.ttl")) and "schema" in low:
            return "Schema"
    return None


def _field_match(
    kg_fields: dict[str, str],
    scan_rec: dict[str, Any] | None,
    source_ref: str | None,
    source_ok: bool,
) -> tuple[bool, list[str], list[str]]:
    """Re-derive the mechanically-derivable field subset from the REAL source and
    DIFF against the KG value. Returns (all_match, mismatches, unverifiable_lines).

    Re-derivable subset: spec_type (from source kind), source-existence-vs-KG
    (the KG asserts an auditTrailLink; reality = does a source resolve?). Fields
    that are NOT mechanically re-derivable (acceptanceCriteria prose, owner label,
    targetSession intent, dormancy threshold) are reported `unverifiable` per-field
    (Done #39 — own line, NEVER silently passed)."""
    mismatches: list[str] = []
    unverifiable: list[str] = []

    # Re-derivable #1: spec_type. KG specType keyword vs source-classified.
    kg_spec_type = kg_fields.get("specType")
    rederived = _rederive_spec_type(scan_rec, source_ref)
    if rederived is None:
        unverifiable.append(
            f"unverifiable: spec_type not mechanically re-derivable (kg={kg_spec_type!r}; no source-kind signal)"
        )
    elif kg_spec_type != rederived:
        mismatches.append(
            f"MISMATCH spec_type: kg={kg_spec_type!r} re-derived-from-source={rederived!r}"
        )

    # Re-derivable #2: source-existence. KG asserts auditTrailLink (a source link);
    # reality = did the source actually resolve+read (source_ok from check (1))?
    kg_audit = kg_fields.get("auditTrailLink")
    if kg_audit and not source_ok:
        mismatches.append(
            f"MISMATCH source_existence: KG asserts auditTrailLink={kg_audit.rsplit('#',1)[-1]!r} "
            f"but the source-of-record does not resolve+read (KG claims a traceable source that reality lacks)"
        )

    # Non-re-derivable fields → unverifiable per-field (Done #39).
    for fld in ("acceptanceCriteria", "owner", "targetSession", "dormancyDetectionThresholdSessions"):
        if fld in kg_fields:
            unverifiable.append(
                f"unverifiable: {fld} is prose/intent — not mechanically re-derivable from source"
            )

    all_match = len(mismatches) == 0
    return all_match, mismatches, unverifiable


# --- (3) status-match (live BE-F probe import+execute) --------------------------


def _import_probe_module(probe_path: pathlib.Path):
    """Import a BE-F probe module by file path (KT-8 import+execute, not string-match)."""
    spec = importlib.util.spec_from_file_location(
        f"be_f_probe_{probe_path.parent.name}_{probe_path.stem}", str(probe_path)
    )
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _build_be_f_kwargs(
    spec_type: str, spec_iri: str, scan_rec: dict[str, Any] | None, source_ref: str | None
) -> dict[str, Any]:
    """Build per-class kwargs for the BE-F probe.probe() call from the scan record's
    audit_tuple, mirroring each BE-F probe's _aggregate_cycle arg-prep."""
    audit = (scan_rec or {}).get("audit_tuple") or [None, None, None]
    src = os.path.expanduser(audit[1]) if len(audit) >= 2 and audit[1] else (
        os.path.expanduser(source_ref) if source_ref else None
    )
    token = audit[2] if len(audit) >= 3 and audit[2] else None
    name_trunc = (scan_rec or {}).get("name_truncated")
    if spec_type == "AgentContract":
        return {"agent_spec_path": src, "subagent_type_name": name_trunc}
    if spec_type == "Schema":
        return {"schema_path": src}
    if spec_type == "DesignDecision":
        clean = (token or name_trunc or _short_iri(spec_iri))
        clean = clean.split(":", 1)[-1] if clean and ":" in clean else clean
        embodiment = None
        if src:
            cdir = pathlib.Path(src).parent
            for c in (cdir / "scripts", cdir / "docs"):
                if c.is_dir():
                    embodiment = str(c)
                    break
        return {
            "decision_token": clean,
            "decision_log_path": src,
            "embodiment_ref_path": embodiment,
        }
    if spec_type == "MethodologyCommitment":
        tok = (token or "").split("@")[0] or name_trunc
        return {"commitment_source_path": src, "commitment_token": tok}
    return {}


def _status_match(
    spec_iri: str,
    spec_type: str | None,
    kg_status: str | None,
    scan_rec: dict[str, Any] | None,
    source_ref: str | None,
) -> tuple[bool, str, bool | None]:
    """Dispatch to the matching BE-F probe by spec_type, RUN it live (import+execute),
    compare its live `implemented` to the KG's recorded current_status.

    Returns (status_ok, evidence, live_implemented). status_ok=False on mismatch
    OR on any inability to run (conservative fail-safe per Done #41 — NEVER counted
    faithful when unverifiable)."""
    if not spec_type or spec_type not in BE_F_PROBES:
        return False, f"status_match_UNVERIFIABLE: unknown spec_type={spec_type!r} (conservative-fail)", None
    if kg_status not in STATUS_IMPLIES_IMPLEMENTED:
        return False, f"status_match_UNVERIFIABLE: KG status={kg_status!r} not in 5-state enum (conservative-fail)", None
    probe_path, _scan_class = BE_F_PROBES[spec_type]
    if not probe_path.exists():
        return False, f"status_match_UNVERIFIABLE: BE-F probe missing at {probe_path} (conservative-fail)", None
    try:
        mod = _import_probe_module(probe_path)
        if mod is None or not hasattr(mod, "probe"):
            return False, f"status_match_UNVERIFIABLE: cannot import BE-F probe.probe() (conservative-fail)", None
        kwargs = _build_be_f_kwargs(spec_type, spec_iri, scan_rec, source_ref)
        result = mod.probe(spec_iri=spec_iri, **kwargs)
        live_impl = bool(result.get("implemented"))
    except Exception as e:  # noqa: BLE001 — any probe error → conservative fail-safe
        return False, f"status_match_UNVERIFIABLE: live BE-F probe error {e!r} (conservative-fail)", None
    expected_impl = STATUS_IMPLIES_IMPLEMENTED[kg_status]
    if live_impl == expected_impl:
        return (
            True,
            f"status_match_OK: live BE-F({spec_type}) implemented={live_impl} "
            f"consistent with KG status={kg_status!r}",
            live_impl,
        )
    return (
        False,
        f"status_match_INFIDELITY: live BE-F({spec_type}) implemented={live_impl} "
        f"CONTRADICTS KG status={kg_status!r} (expected implemented={expected_impl})",
        live_impl,
    )


# --- the probe -----------------------------------------------------------------


def probe(
    spec_iri: str,
    query_endpoint: str = DEFAULT_QUERY_ENDPOINT,
    named_graph: str = ASSERTION_GRAPH,
    scan_rec: dict[str, Any] | None = None,
    scan_json_path: str | None = None,
    source_ref_override: str | None = None,
    expected_fidelity: bool | None = None,
) -> dict[str, Any]:
    """Class E KG-fidelity probe.

    fidelity_ok: true ONLY when all three execution-grounded sub-checks pass
    (source resolves+reads; re-derived fields DIFF-match; live BE-F probe status
    is consistent with the KG record). Any sub-check FAIL or any UNVERIFIABLE
    inability → fidelity_ok False + classed infidelity/unverified (conservative
    fail-safe, Done #41) → NEVER counted faithful. No human step in this path."""
    run_id = f"s15_be_j_production_e_{_short_iri(spec_iri)}_{uuid.uuid4().hex[:6]}"
    ts = _utc_ts()

    # Read the KG node from the NAMED GRAPH (GRAPH clause mandatory).
    try:
        kg_fields = _read_kg_node(spec_iri, query_endpoint, named_graph)
    except Exception as e:  # noqa: BLE001
        return _build_result(
            spec_iri, run_id, ts, False, "infidelity_or_unverified",
            f"probe_error: KG read failed {e!r} (conservative-fail-safe)",
            {"source_traceability": False, "field_match": False, "status_match": False},
            [], [],
        )
    if kg_fields.get("_http_status") != "200" or "specType" not in kg_fields:
        return _build_result(
            spec_iri, run_id, ts, False, "infidelity_or_unverified",
            f"probe_error: KG node not found / endpoint http={kg_fields.get('_http_status')} "
            f"(named_graph={named_graph}; conservative-fail-safe)",
            {"source_traceability": False, "field_match": False, "status_match": False},
            [], [],
        )

    # Resolve the source-of-record: scan record audit_tuple[1] is the real source
    # path (the KG auditTrailLink is an opaque activity IRI). Join scan_rec by IRI.
    if scan_rec is None and scan_json_path:
        idx = _load_scan_index(scan_json_path)
        short = spec_iri.rsplit(":", 1)[-1]
        scan_rec = idx.get(short)
    source_ref = source_ref_override
    if source_ref is None and scan_rec:
        audit = scan_rec.get("audit_tuple") or [None, None, None]
        source_ref = audit[1] if len(audit) >= 2 else None

    # (1) Source-traceability — resolve + READ.
    source_ok, source_ev = _resolve_and_read_source(source_ref)

    # (2) Field-match — re-derive + DIFF.
    field_ok, mismatches, unverifiable = _field_match(
        kg_fields, scan_rec, source_ref, source_ok
    )

    # (3) Status-match — live BE-F probe import+execute.
    status_ok, status_ev, live_impl = _status_match(
        spec_iri,
        kg_fields.get("specType"),
        kg_fields.get("currentStatus"),
        scan_rec,
        source_ref,
    )

    sub_checks = {
        "source_traceability": source_ok,
        "field_match": field_ok,
        "status_match": status_ok,
    }
    fidelity_ok = source_ok and field_ok and status_ok
    disposition = "faithful" if fidelity_ok else "infidelity_or_unverified"

    evidence_parts = [source_ev, status_ev]
    if mismatches:
        evidence_parts.extend(mismatches)
    evidence = " || ".join(evidence_parts)

    return _build_result(
        spec_iri, run_id, ts, fidelity_ok, disposition, evidence, sub_checks,
        mismatches, unverifiable,
        extra={
            "kg_current_status": kg_fields.get("currentStatus"),
            "kg_spec_type": kg_fields.get("specType"),
            "live_be_f_implemented": live_impl,
            "source_ref": source_ref,
            "scan_joined": scan_rec is not None,
        },
    )


def _build_result(
    spec_iri: str,
    run_id: str,
    ts: str,
    fidelity_ok: bool,
    disposition: str,
    evidence: str,
    sub_checks: dict[str, bool],
    mismatches: list[str],
    unverifiable: list[str],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "probe_id": PROBE_ID,
        "probe_version": PROBE_VERSION,
        "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
        "primitive_class": PRIMITIVE_CLASS,
        "spec_iri": spec_iri,
        "run_id": run_id,
        "timestamp": ts,
        "predicateType": PREDICATE_TYPE_FIRE,
        "fidelity_ok": fidelity_ok,
        "disposition": disposition,  # faithful | infidelity_or_unverified
        "evidence": evidence,
        "evidence_type": "probe_fire_aggregate",
        "sub_checks": sub_checks,
        "mismatches": mismatches,
        "unverifiable_fields": unverifiable,  # Done #39 — own line, never silently passed
    }
    if extra:
        result.update(extra)
    return result


# --- self-test -----------------------------------------------------------------


def _self_test(fixture_dir: pathlib.Path) -> int:
    """Self-test: load known_good_e_*.json (must return fidelity_ok=True) +
    known_bad_e_*.json (must return fidelity_ok=False). Emits per-fixture JSONL
    to outputs/probe_library_self_test_events.jsonl with predicateType
    cycle16:probe_self_test_v1. Exit 0 iff distinguishes BOTH."""
    project_root = pathlib.Path(__file__).resolve().parents[3]
    sink = project_root / "outputs" / "probe_library_self_test_events.jsonl"
    good = sorted(fixture_dir.glob("known_good_e_*.json"))
    bad = sorted(fixture_dir.glob("known_bad_e_*.json"))
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
            query_endpoint=cfg.get("query_endpoint", DEFAULT_QUERY_ENDPOINT),
            named_graph=cfg.get("named_graph", ASSERTION_GRAPH),
            scan_rec=cfg.get("scan_rec"),
            scan_json_path=cfg.get("scan_json_path"),
            source_ref_override=cfg.get("source_ref_override"),
            expected_fidelity=cfg.get("expected_fidelity"),
        )
        expected = cfg["expected_fidelity"]
        distinguished = result["fidelity_ok"] == expected
        all_distinguished = all_distinguished and distinguished
        rows.append(
            {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_j.kg_fidelity_self_test",
                "event_class": (
                    "probe_library_self_test.pass.event"
                    if distinguished
                    else "probe_library_self_test.fail.event"
                ),
                "predicateType": PREDICATE_TYPE_SELF_TEST,
                "timestamp": _utc_ts(),
                "run_id": f"s15_be_j_probe_lib_self_test_e_{fx.stem}_{uuid.uuid4().hex[:6]}",
                "payload": {
                    "probe_id": PROBE_ID,
                    "probe_version": PROBE_VERSION,
                    "primitive_class": PRIMITIVE_CLASS,
                    "fixture_path": str(fx),
                    "fixture_class": "known_good" if fx.name.startswith("known_good") else "known_bad",
                    "expected_fidelity": expected,
                    "actual_fidelity_ok": result["fidelity_ok"],
                    "distinguished": distinguished,
                    "disposition": result["disposition"],
                    "sub_checks": result["sub_checks"],
                    "evidence": result["evidence"][:240],
                    "unverifiable_fields": result["unverifiable_fields"][:6],
                },
            }
        )
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    if not all_distinguished:
        print(
            "FAIL: self-test did not distinguish known_good (fidelity_ok must be True) "
            "+ known_bad (fidelity_ok must be False)",
            file=sys.stderr,
        )
    return 0 if all_distinguished else 1


# --- aggregate-cycle (periodic audit / production dogfood) ----------------------


def _aggregate_cycle(
    cycle_n: int,
    query_endpoint: str,
    named_graph: str,
    scan_json_path: str,
    sink_path: str,
    limit: int | None,
    run_id_prefix_override: str | None = None,
) -> int:
    """Periodic-audit / dogfood mode: enumerate the REAL named-graph cycle16:Spec
    population, fire Class E on each, emit JSONL rows to sink with production
    run_ids. Joins the scan-JSON source-of-record by IRI for source/field/status
    re-derivation. NON-smoke: fires against the live /cycle6 population."""
    # Enumerate the REAL population from the named graph (GRAPH clause mandatory).
    enum_query = f"""
PREFIX cycle16: <{ONTOLOGY_NS}>
SELECT ?s WHERE {{
  GRAPH <{named_graph}> {{
    ?s a cycle16:Spec .
  }}
}}
"""
    status, parsed = _sparql_query(query_endpoint, enum_query)
    if status != 200 or not parsed:
        print(f"FAIL: could not enumerate population (http={status})", file=sys.stderr)
        return 1
    iris = [
        "cycle16:" + b["s"]["value"].rsplit("#", 1)[-1]
        for b in parsed.get("results", {}).get("bindings", [])
    ]
    if limit:
        iris = iris[:limit]
    scan_idx = _load_scan_index(scan_json_path)
    sink = pathlib.Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    fired = faithful = infidelity = unverifiable = 0
    with sink.open("a", encoding="utf-8") as f:
        for iri in iris:
            short = iri.rsplit(":", 1)[-1]
            scan_rec = scan_idx.get(short)
            result = probe(
                spec_iri=iri,
                query_endpoint=query_endpoint,
                named_graph=named_graph,
                scan_rec=scan_rec,
            )
            if run_id_prefix_override:
                result["run_id"] = (
                    f"{run_id_prefix_override}_{_short_iri(iri)}_{uuid.uuid4().hex[:6]}"
                )
            if result["fidelity_ok"]:
                faithful += 1
            elif not result["sub_checks"]["source_traceability"] or (
                "UNVERIFIABLE" in result["evidence"]
            ):
                unverifiable += 1
            else:
                infidelity += 1
            row = {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_j.kg_fidelity",
                "event_class": "probe_library.fire.event",
                "predicateType": PREDICATE_TYPE_FIRE,
                "timestamp": result["timestamp"],
                "run_id": result["run_id"],
                "payload": {
                    "probe_id": result["probe_id"],
                    "probe_version": result["probe_version"],
                    "probe_admission_lock_commit": result["probe_admission_lock_commit"],
                    "primitive_class": result["primitive_class"],
                    "spec_iri": result["spec_iri"],
                    "kg_spec_type": result.get("kg_spec_type"),
                    "kg_current_status": result.get("kg_current_status"),
                    "fidelity_ok": result["fidelity_ok"],
                    "disposition": result["disposition"],
                    "sub_checks": result["sub_checks"],
                    "live_be_f_implemented": result.get("live_be_f_implemented"),
                    "scan_joined": result.get("scan_joined"),
                    "evidence": result["evidence"][:320],
                    "unverifiable_fields_count": len(result["unverifiable_fields"]),
                },
            }
            f.write(json.dumps(row) + "\n")
            fired += 1
    print(
        f"PASS: aggregate-cycle fired {fired} Class E probes against the REAL "
        f"named-graph cycle16:Spec population (sink={sink_path}) || "
        f"faithful={faithful} infidelity={infidelity} unverifiable={unverifiable}"
    )
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Probe Class E — KG-fidelity")
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
    p.add_argument("--spec-iri", default=None, help="Single-spec fidelity-probe mode")
    p.add_argument("--query-endpoint", default=DEFAULT_QUERY_ENDPOINT)
    p.add_argument("--named-graph", default=ASSERTION_GRAPH)
    args = p.parse_args(argv)

    if args.self_test:
        fixture_dir = (
            pathlib.Path(__file__).resolve().parents[3] / "tests" / "probes" / "fixtures"
        )
        return _self_test(fixture_dir)
    if args.aggregate_cycle is not None:
        return _aggregate_cycle(
            cycle_n=args.aggregate_cycle,
            query_endpoint=args.query_endpoint,
            named_graph=args.named_graph,
            scan_json_path=args.scan_json,
            sink_path=args.sink,
            limit=args.limit,
            run_id_prefix_override=args.run_id_prefix,
        )
    if args.spec_iri:
        result = probe(
            spec_iri=args.spec_iri,
            query_endpoint=args.query_endpoint,
            named_graph=args.named_graph,
            scan_json_path=args.scan_json,
        )
        print(json.dumps(result, indent=2))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
