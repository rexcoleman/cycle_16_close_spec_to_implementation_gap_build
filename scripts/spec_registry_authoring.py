#!/usr/bin/env python3
"""
spec_registry_authoring.py — Cycle 16 BE-B SPARQL UPDATE authoring discipline wrapper.

Wraps the 5 substrate-operations specified at
~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_authoring_discipline.md
into callable Python functions invokable from any research-build project.

Authority: Cycle 16 SI ACTIVE 2026-05-27 (a2f14d5) + Amendment 2026-05-27a (be54a97;
same-cycle deadline default + dormancy_detection_threshold_sessions=3) + Amendment
2026-05-27b (badd749; KG-primary registry at Cycle 6 /cycle6 endpoint) + Cycle-16-S3
close D-S3-1 (BE-A SHIPPED `6c7c62d`).

5 functions (one per substrate-operation):
  - register_spec(...)             — Operation 1: per-spec registry-write
  - read_spec_status(spec_id)      — Operation 2: per-spec registry-read
  - fire_cycle_close_gate(cycle_n) — Operation 3: cycle-close BLOCKING gate ASK
  - fire_session_close_gate(...)   — Operation 4: session-close BLOCKING gate ASK
  - supersede_spec(...)            — Operation 5: 3-atomic non-destructive supersedure

Structural enforcement at wrapper entry (Brief 2 operationalization):
  - 11 mandatory fields required (raises ValueError on missing)
  - DP#26 carve-out: if runtime_emit_event_class == 'n/a' OR starts 'n/a',
    n_a_rationale MANDATORY (non-empty string)
  - SHACL pre-validation via pyshacl against docs/spec_registry_shapes.shacl.ttl
    BEFORE SPARQL UPDATE fires (refuse-on-violation per DP#44)
  - 4-class refusal taxonomy per substrate §3 (a)/(b)/(c)/(d):
      (a) acceptance-criteria-unclear        → KT-3 candidate registry-refinement
      (b) backlog-from-same-cycle-default    → KT-3 candidate default-relaxation
      (c) dp44-honest-gap                    → NOT KT-3; operational signal
      (d) n_a-rationale-unclear              → KT-3 candidate registry-refinement
    Each refusal fires `spec_registry.author_refusal.event` JSONL row for
    Coach R3 KT-3 firing-surface evaluation.

Runtime emits to outputs/spec_registry_events.jsonl (per-project sink; refuse-on-violation
halt-and-surface per RUNTIME_EMIT_SPEC §3). Three event classes:
  - spec_registry.write.event           — successful UPDATE INSERT DATA
  - spec_registry.shacl_refusal.event   — SHACL pre-validation OR write-boundary refusal
  - spec_registry.author_refusal.event  — author-side refusal (4-class taxonomy)

HC-11 partition: this docstring + function signatures + 5-state taxonomy + DP#26
n_a_rationale field design + 3 event JSON schemas = c6:publishable. Internal
algorithm bodies (SHACL pre-validation invocation logic + author-refusal classification
heuristics) = c6:ip-private (project gitignored).
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import sys
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any

try:
    import rdflib
    import pyshacl
except ImportError as e:
    sys.stderr.write(
        "spec_registry_authoring.py: missing pyshacl or rdflib; "
        "install via `pip install pyshacl rdflib` per ARTIFACT_CONTRACT §1 pre-condition.\n"
    )
    raise

# --- Constants per spec_authoring_discipline.md §0-§4 ---

SPARQL_UPDATE_ENDPOINT = os.environ.get(
    "CYCLE6_UPDATE_ENDPOINT", "http://localhost:3030/cycle6/update"
)
SPARQL_QUERY_ENDPOINT = os.environ.get(
    "CYCLE6_QUERY_ENDPOINT", "http://localhost:3030/cycle6/query"
)
ASSERTION_GRAPH = "http://cycle16.local/registry/assertion"
PROVENANCE_GRAPH = "http://cycle16.local/registry/provenance"
PUBINFO_GRAPH = "http://cycle16.local/registry/publicationInfo"

# 11 mandatory fields per spec_authoring_discipline.md §4 Operation 1
MANDATORY_FIELDS = (
    "spec_type",
    "owner",
    "acceptance_criteria",
    "target_session",
    "current_status",
    "cycle_authored",
    "session_authored",
    "runtime_emit_event_class",
    "dormancy_detection_threshold_sessions",
    "audit_trail_link",
    "access_permission",  # c6:accessPermission per §1 per-edge HC-11 BIND
)

# 4 spec-type enum classes
SPEC_TYPES = {"AgentContract", "Schema", "DesignDecision", "MethodologyCommitment"}

# 5-state taxonomy per Amendment 2026-05-27a
STATUSES = {
    "running",
    "dormant-with-explicit-deferral",
    "dormant-silent",
    "killed",
    "long-running",
}

# 3-enum HC-11 access permission per Cycle 6 BE#1
ACCESS_PERMISSIONS = {"publishable", "ip-private", "ephemeral"}

# 4-class refusal taxonomy per substrate §3 Brief 4 KT-3 firing surface
REFUSAL_CLASSES = {
    "acceptance_criteria_unclear",  # (a)
    "backlog_from_same_cycle_default",  # (b)
    "dp44_honest_gap",  # (c)
    "n_a_rationale_unclear",  # (d)
}

# --- Helpers ---


def _iso_now() -> str:
    return (
        datetime.datetime.now(datetime.timezone.utc)
        .isoformat()
        .replace("+00:00", "Z")
    )


def _uuid7() -> str:
    """Approximate UUID v7 via UUID4 (Python stdlib lacks v7); deterministic IRI."""
    return uuid.uuid4().hex[:32]


def _sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def _emit(
    project_dir: Path, namespace: str, event_class: str, payload: dict[str, Any]
) -> None:
    """Append-only JSONL emit per RUNTIME_EMIT_SPEC §1 + §4."""
    sink = project_dir / "outputs" / "spec_registry_events.jsonl"
    sink.parent.mkdir(parents=True, exist_ok=True)
    event = {
        "schema_version": "0.1",
        "namespace": namespace,
        "event_class": event_class,
        "timestamp": _iso_now(),
        "run_id": payload.pop("_run_id", str(uuid.uuid4())),
        "payload": payload,
    }
    with sink.open("a") as f:
        f.write(json.dumps(event) + "\n")


def _sparql_post(endpoint: str, query_or_update: str, op: str = "update") -> tuple[int, int]:
    """Return (http_status_code, response_time_ms). op ∈ {'update', 'query'}."""
    start = datetime.datetime.now(datetime.timezone.utc)
    data = urllib.parse.urlencode({op: query_or_update}).encode()
    headers = {}
    if op == "query":
        headers["Accept"] = "application/sparql-results+json"
    req = urllib.request.Request(endpoint, data=data, headers=headers)
    resp = urllib.request.urlopen(req, timeout=30)
    body = resp.read()
    elapsed_ms = int(
        (datetime.datetime.now(datetime.timezone.utc) - start).total_seconds() * 1000
    )
    return resp.status, elapsed_ms, body


def _validate_mandatory_fields(spec: dict[str, Any]) -> list[str]:
    """Return list of missing-field error strings; empty = PASS."""
    missing = [f for f in MANDATORY_FIELDS if f not in spec or spec[f] in (None, "")]
    return missing


def _validate_dp26_carve_out(spec: dict[str, Any]) -> str | None:
    """DP#26 n_a-rationale enforcement per Brief 2.

    If runtime_emit_event_class is 'n/a' OR begins 'n/a' (e.g., 'n/a — citation-based...'),
    n_a_rationale MUST be present and non-empty. Returns error string OR None on PASS.
    """
    rec = spec.get("runtime_emit_event_class", "")
    if rec == "n/a" or (isinstance(rec, str) and rec.startswith("n/a")):
        if not spec.get("n_a_rationale"):
            return (
                "DP#26 carve-out violation: runtime_emit_event_class='n/a' "
                "REQUIRES non-empty n_a_rationale field per HC-07 every-claim-traces-to-evidence BINDING."
            )
    return None


def _validate_enums(spec: dict[str, Any]) -> list[str]:
    """Return list of enum-violation error strings; empty = PASS."""
    errors = []
    if spec.get("spec_type") not in SPEC_TYPES:
        errors.append(
            f"spec_type='{spec.get('spec_type')}' not in 4-class enum {SPEC_TYPES}."
        )
    if spec.get("current_status") not in STATUSES:
        errors.append(
            f"current_status='{spec.get('current_status')}' not in 5-state enum {STATUSES}."
        )
    if spec.get("access_permission") not in ACCESS_PERMISSIONS:
        errors.append(
            f"access_permission='{spec.get('access_permission')}' "
            f"not in 3-enum {ACCESS_PERMISSIONS}."
        )
    return errors


def _build_spec_ttl(spec: dict[str, Any], spec_uuid: str) -> tuple[str, str, str]:
    """Build the 3-graph TTL fragments per spec_authoring_discipline §3 + §4 Operation 1.

    Returns (assertion_ttl, provenance_ttl, publicationInfo_ttl) — string TTL bodies
    inside their respective GRAPH clauses (no graph wrapper here; caller wraps).
    """
    spec_iri = f"cycle16:spec_{spec_uuid}"
    st = spec.get("spec_type", "AgentContract")
    status = spec.get("current_status", "running")

    def esc(s: Any) -> str:
        if s is None:
            return ""
        return str(s).replace("\\", "\\\\").replace('"', '\\"')

    assertion_lines = [
        f"    {spec_iri} a cycle16:Spec ;",
        f"      cycle16:specType cycle16:{st} ;",
        f'      cycle16:owner "{esc(spec["owner"])}" ;',
        f'      cycle16:acceptanceCriteria "{esc(spec["acceptance_criteria"])}" ;',
        f'      cycle16:targetSession "{esc(spec["target_session"])}" ;',
        f"      cycle16:currentStatus cycle16:{status} ;",
        f'      cycle16:cycleAuthored {int(spec["cycle_authored"])} ;',
        f'      cycle16:sessionAuthored "{esc(spec["session_authored"])}" ;',
        f'      cycle16:runtimeEmitEventClass "{esc(spec["runtime_emit_event_class"])}" ;',
        f'      cycle16:dormancyDetectionThresholdSessions {int(spec["dormancy_detection_threshold_sessions"])} ;',
        f"      cycle16:auditTrailLink cycle16:{esc(spec['audit_trail_link'])} ;",
        f"      c6:accessPermission c6:{spec['access_permission']} ;",
        f'      c6:rank "{esc(spec.get("rank", "normal"))}"',
    ]
    # Optional / conditional fields
    if spec.get("cycle_implemented") is not None:
        assertion_lines[-1] += " ;"
        assertion_lines.append(
            f'      cycle16:cycleImplemented {int(spec["cycle_implemented"])}'
        )
    if spec.get("session_implemented"):
        assertion_lines[-1] += " ;"
        assertion_lines.append(
            f'      cycle16:sessionImplemented "{esc(spec["session_implemented"])}"'
        )
    if spec.get("deferral_reason"):
        assertion_lines[-1] += " ;"
        assertion_lines.append(
            f'      cycle16:deferralReason "{esc(spec["deferral_reason"])}"'
        )
    if spec.get("rex_authorization_for_deferral_past_cycle_close"):
        assertion_lines[-1] += " ;"
        assertion_lines.append(
            f'      cycle16:rexAuthorizationForDeferralPastCycleClose '
            f'"{esc(spec["rex_authorization_for_deferral_past_cycle_close"])}"'
        )
    if spec.get("n_a_rationale"):
        assertion_lines[-1] += " ;"
        assertion_lines.append(
            f'      cycle16:n_a_rationale "{esc(spec["n_a_rationale"])}"'
        )
    assertion_lines[-1] += " ."
    assertion = "\n".join(assertion_lines)

    provenance = "\n".join(
        [
            f"    {spec_iri} prov:wasGeneratedBy cycle16:session_{esc(spec['session_authored']).replace('-','_')} ;",
            f"      prov:wasAttributedTo cycle16:owner_{esc(spec['owner']).replace(' ','_').replace('-','_')} ;",
            f'      prov:generatedAtTime "{_iso_now()}"^^xsd:dateTime ;',
            f"      prov:wasInformedBy cycle16:disposition_{esc(spec.get('informed_by', 'amendment_27a'))} .",
        ]
    )

    pubinfo = "\n".join(
        [
            f'    {spec_iri} cycle16:publishedAtCycle {int(spec["cycle_authored"])} ;',
            f'      cycle16:nanopubSigner "{esc(spec.get("nanopub_signer", "cycle16-be-b"))}" .',
        ]
    )

    return assertion, provenance, pubinfo


def _build_shacl_data_graph(spec: dict[str, Any], spec_uuid: str) -> rdflib.Graph:
    """Build an rdflib Graph carrying the spec's assertion triples for pre-validation.

    Includes namespace bindings + the spec instance + accessPermission + rank
    so SHACL polymorphism via subclass inheritance can fire.
    """
    g = rdflib.Graph()
    CYCLE16 = rdflib.Namespace("http://cycle16.local/ontology#")
    C6 = rdflib.Namespace("http://cycle6.local/ontology#")
    g.bind("cycle16", CYCLE16)
    g.bind("c6", C6)
    spec_node = CYCLE16[f"spec_{spec_uuid}"]
    g.add((spec_node, rdflib.RDF.type, CYCLE16.Spec))
    g.add((spec_node, rdflib.RDF.type, C6.Statement))  # explicit superclass assert
    g.add((spec_node, CYCLE16.specType, CYCLE16[spec["spec_type"]]))
    g.add((spec_node, CYCLE16.owner, rdflib.Literal(str(spec["owner"]))))
    g.add(
        (
            spec_node,
            CYCLE16.acceptanceCriteria,
            rdflib.Literal(str(spec["acceptance_criteria"])),
        )
    )
    g.add(
        (
            spec_node,
            CYCLE16.targetSession,
            rdflib.Literal(str(spec["target_session"])),
        )
    )
    # currentStatus value is the IRI cycle16:<status-keyword>
    g.add((spec_node, CYCLE16.currentStatus, CYCLE16[spec["current_status"]]))
    g.add(
        (
            spec_node,
            CYCLE16.cycleAuthored,
            rdflib.Literal(
                int(spec["cycle_authored"]),
                datatype=rdflib.XSD.integer,
            ),
        )
    )
    g.add(
        (
            spec_node,
            CYCLE16.sessionAuthored,
            rdflib.Literal(str(spec["session_authored"])),
        )
    )
    g.add(
        (
            spec_node,
            CYCLE16.runtimeEmitEventClass,
            rdflib.Literal(str(spec["runtime_emit_event_class"])),
        )
    )
    g.add(
        (
            spec_node,
            CYCLE16.dormancyDetectionThresholdSessions,
            rdflib.Literal(
                int(spec["dormancy_detection_threshold_sessions"]),
                datatype=rdflib.XSD.integer,
            ),
        )
    )
    g.add(
        (
            spec_node,
            CYCLE16.auditTrailLink,
            CYCLE16[spec["audit_trail_link"]],
        )
    )
    g.add((spec_node, C6.accessPermission, C6[spec["access_permission"]]))
    g.add(
        (
            spec_node,
            C6["rank"],
            rdflib.Literal(str(spec.get("rank", "normal"))),
        )
    )
    return g


def _shacl_pre_validate(
    spec: dict[str, Any], spec_uuid: str, project_dir: Path
) -> tuple[bool, str]:
    """Pre-validate spec against SHACL shapes. Returns (conforms, message).

    Per spec_authoring_discipline §5: SHACL refusal at write boundary. Wrapper-side
    pre-validation prevents fabricated-PASS at downstream gates.
    """
    schema_path = (
        project_dir / "docs" / "spec_registry_schema.ttl"
    )
    shapes_path = (
        project_dir / "docs" / "spec_registry_shapes.shacl.ttl"
    )
    c6_shapes = Path(
        "/home/azureuser/cycle_6_unified_substrate_build/runtime/jena/shapes/access_permission.shacl.ttl"
    )

    data_graph = _build_shacl_data_graph(spec, spec_uuid)
    ont_graph = rdflib.Graph()
    if schema_path.exists():
        ont_graph.parse(str(schema_path), format="turtle")
    shapes_graph = rdflib.Graph()
    if shapes_path.exists():
        shapes_graph.parse(str(shapes_path), format="turtle")
    if c6_shapes.exists():
        shapes_graph.parse(str(c6_shapes), format="turtle")

    conforms, _g, msg = pyshacl.validate(
        data_graph, shacl_graph=shapes_graph, ont_graph=ont_graph, inference="rdfs"
    )
    return conforms, msg


# --- 5 substrate-operations ---


def register_spec(
    spec: dict[str, Any],
    project_dir: str | Path = ".",
    namespace: str = "cycle_16.be_b.spec_registry",
    skip_shacl: bool = False,
) -> dict[str, Any]:
    """Operation 1: per-spec registry-write at /cycle6/update.

    Structural enforcement at wrapper entry:
      1. 11 mandatory fields non-empty
      2. spec_type / current_status / access_permission in enum
      3. DP#26 n_a_rationale required if runtime_emit_event_class begins 'n/a'
      4. SHACL pre-validation (skippable for testing via skip_shacl=True)

    On structural-enforcement FAIL → refuse-on-violation per DP#44 → emit
    `spec_registry.shacl_refusal.event` → raise ValueError. No partial write.

    Returns dict {spec_iri, http_status, response_time_ms, success_bool, ...}.
    """
    project_dir = Path(project_dir).expanduser().resolve()

    # 1. Mandatory fields
    missing = _validate_mandatory_fields(spec)
    if missing:
        msg = f"Missing mandatory fields: {missing}"
        _emit(
            project_dir,
            namespace,
            "spec_registry.shacl_refusal.event",
            {
                "refusal_class": "missing_mandatory_fields",
                "missing_fields": missing,
                "spec_partial": {k: v for k, v in spec.items() if k != "_run_id"},
                "_run_id": spec.get("_run_id", str(uuid.uuid4())),
            },
        )
        raise ValueError(msg)

    # 2. Enum violations
    enum_errors = _validate_enums(spec)
    if enum_errors:
        msg = f"Enum violations: {enum_errors}"
        _emit(
            project_dir,
            namespace,
            "spec_registry.shacl_refusal.event",
            {
                "refusal_class": "enum_violation",
                "errors": enum_errors,
                "spec_partial": {k: v for k, v in spec.items() if k != "_run_id"},
                "_run_id": spec.get("_run_id", str(uuid.uuid4())),
            },
        )
        raise ValueError(msg)

    # 3. DP#26 n_a-rationale
    dp26_err = _validate_dp26_carve_out(spec)
    if dp26_err:
        _emit(
            project_dir,
            namespace,
            "spec_registry.shacl_refusal.event",
            {
                "refusal_class": "dp26_n_a_rationale_missing",
                "error": dp26_err,
                "spec_partial": {k: v for k, v in spec.items() if k != "_run_id"},
                "_run_id": spec.get("_run_id", str(uuid.uuid4())),
            },
        )
        raise ValueError(dp26_err)

    spec_uuid = spec.get("spec_uuid") or _uuid7()
    spec_iri = f"cycle16:spec_{spec_uuid}"

    # 4. SHACL pre-validation
    if not skip_shacl:
        conforms, shacl_msg = _shacl_pre_validate(spec, spec_uuid, project_dir)
        if not conforms:
            _emit(
                project_dir,
                namespace,
                "spec_registry.shacl_refusal.event",
                {
                    "refusal_class": "shacl_violation",
                    "shacl_report_excerpt": shacl_msg[:2000],
                    "spec_iri": spec_iri,
                    "_run_id": spec.get("_run_id", str(uuid.uuid4())),
                },
            )
            raise ValueError(f"SHACL pre-validation refused write: {shacl_msg[:500]}")

    # 5. Build TTL fragments + SPARQL UPDATE
    assertion, provenance, pubinfo = _build_spec_ttl(spec, spec_uuid)
    update_body = f"""
PREFIX c6: <http://cycle6.local/ontology#>
PREFIX cycle16: <http://cycle16.local/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

INSERT DATA {{
  GRAPH <{ASSERTION_GRAPH}> {{
{assertion}
  }}
  GRAPH <{PROVENANCE_GRAPH}> {{
{provenance}
  }}
  GRAPH <{PUBINFO_GRAPH}> {{
{pubinfo}
  }}
}}
"""

    http_status, ms, body = _sparql_post(
        SPARQL_UPDATE_ENDPOINT, update_body, op="update"
    )
    success = http_status == 200 or http_status == 204

    payload = {
        "spec_id": spec_iri,
        "graph_iri": ASSERTION_GRAPH,
        "sparql_query_hash": _sha256(update_body),
        "http_status_code": http_status,
        "response_time_ms": ms,
        "triple_count_delta": assertion.count(";") + assertion.count(".")
        + provenance.count(";") + provenance.count(".")
        + pubinfo.count(";") + pubinfo.count("."),
        "accessPermission_value_set": spec["access_permission"],
        "success_bool": success,
        "test_bed_id": spec.get("test_bed_id"),
        "_run_id": spec.get("_run_id", str(uuid.uuid4())),
    }
    _emit(project_dir, namespace, "spec_registry.write.event", payload)

    return {
        "spec_iri": spec_iri,
        "spec_uuid": spec_uuid,
        "http_status_code": http_status,
        "response_time_ms": ms,
        "success_bool": success,
        "sparql_query_hash": payload["sparql_query_hash"],
        "triple_count_delta": payload["triple_count_delta"],
    }


def read_spec_status(spec_iri: str) -> dict[str, Any]:
    """Operation 2: per-spec registry-read SELECT.

    Returns dict {status, target_session, runtime_emit_event_class, http_status,
    response_time_ms, readback_triple_count}. Caller checks readback_triple_count
    matches expected per current_status (11 + 1 audit_trail_link + N conditional).
    """
    if spec_iri.startswith("cycle16:"):
        spec_iri_full = f"http://cycle16.local/ontology#{spec_iri[len('cycle16:'):]}"
    else:
        spec_iri_full = spec_iri

    query_body = f"""
PREFIX c6: <http://cycle6.local/ontology#>
PREFIX cycle16: <http://cycle16.local/ontology#>

SELECT ?p ?o WHERE {{
  GRAPH <{ASSERTION_GRAPH}> {{
    <{spec_iri_full}> ?p ?o .
  }}
}}
"""
    http_status, ms, body = _sparql_post(
        SPARQL_QUERY_ENDPOINT, query_body, op="query"
    )
    triples = []
    if http_status == 200:
        results = json.loads(body)
        for binding in results.get("results", {}).get("bindings", []):
            triples.append((binding["p"]["value"], binding["o"]["value"]))

    status_val = None
    target_session_val = None
    rec_val = None
    for p, o in triples:
        if p.endswith("currentStatus"):
            status_val = o
        if p.endswith("targetSession"):
            target_session_val = o
        if p.endswith("runtimeEmitEventClass"):
            rec_val = o

    return {
        "spec_iri": spec_iri,
        "http_status_code": http_status,
        "response_time_ms": ms,
        "readback_triple_count": len(triples),
        "status": status_val,
        "target_session": target_session_val,
        "runtime_emit_event_class": rec_val,
        "all_triples": triples,
    }


def fire_cycle_close_gate(cycle_n: int) -> dict[str, Any]:
    """Operation 3: cycle-close BLOCKING gate ASK.

    Returns dict {http_status, response_time_ms, dormant_silent_specs_present_bool,
    verdict: 'BLOCKING' | 'PASS'}. BLOCKING fires if ASK returns TRUE.
    """
    query_body = f"""
PREFIX cycle16: <http://cycle16.local/ontology#>

ASK {{
  GRAPH <{ASSERTION_GRAPH}> {{
    ?spec cycle16:currentStatus cycle16:dormant-silent ;
          cycle16:cycleAuthored {int(cycle_n)} .
  }}
}}
"""
    http_status, ms, body = _sparql_post(
        SPARQL_QUERY_ENDPOINT, query_body, op="query"
    )
    dormant_silent = False
    if http_status == 200:
        dormant_silent = json.loads(body).get("boolean", False)
    return {
        "http_status_code": http_status,
        "response_time_ms": ms,
        "dormant_silent_specs_present_bool": dormant_silent,
        "verdict": "BLOCKING" if dormant_silent else "PASS",
        "cycle_n": cycle_n,
    }


def fire_session_close_gate(
    current_session_index: int,
    session_authored_index: int,
    threshold: int = 3,
) -> dict[str, Any]:
    """Operation 4: session-close BLOCKING gate ASK.

    Per spec_authoring_discipline §4 Operation 4 + Amendment 2026-05-27a default 3.
    Returns dict {http_status, response_time_ms, dormant_specs_over_threshold_bool,
    verdict: 'BLOCKING' | 'PASS'}.
    """
    sessions_between = current_session_index - session_authored_index
    if sessions_between < threshold:
        return {
            "http_status_code": None,
            "response_time_ms": 0,
            "sessions_between": sessions_between,
            "threshold": threshold,
            "dormant_specs_over_threshold_bool": False,
            "verdict": "PASS",
        }
    query_body = f"""
PREFIX cycle16: <http://cycle16.local/ontology#>

ASK {{
  GRAPH <{ASSERTION_GRAPH}> {{
    ?spec cycle16:currentStatus cycle16:dormant-silent ;
          cycle16:dormancyDetectionThresholdSessions ?t .
    FILTER ({sessions_between} >= ?t)
  }}
}}
"""
    http_status, ms, body = _sparql_post(
        SPARQL_QUERY_ENDPOINT, query_body, op="query"
    )
    over_threshold = False
    if http_status == 200:
        over_threshold = json.loads(body).get("boolean", False)
    return {
        "http_status_code": http_status,
        "response_time_ms": ms,
        "sessions_between": sessions_between,
        "threshold": threshold,
        "dormant_specs_over_threshold_bool": over_threshold,
        "verdict": "BLOCKING" if over_threshold else "PASS",
    }


def supersede_spec(
    new_spec: dict[str, Any],
    old_spec_iri: str,
    project_dir: str | Path = ".",
    namespace: str = "cycle_16.be_b.spec_registry",
) -> dict[str, Any]:
    """Operation 5: 3-atomic non-destructive supersedure.

    Per spec_authoring_discipline §4 Operation 5: new spec → preferred + supersedesRef
    link + old spec rank → deprecated. Both queryable post-supersedure.
    """
    project_dir = Path(project_dir).expanduser().resolve()
    new_spec_for_write = dict(new_spec)
    new_spec_for_write["rank"] = "preferred"
    result = register_spec(
        new_spec_for_write, project_dir=project_dir, namespace=namespace
    )
    new_spec_iri = result["spec_iri"]
    old_iri_full = (
        old_spec_iri
        if not old_spec_iri.startswith("cycle16:")
        else f"http://cycle16.local/ontology#{old_spec_iri[len('cycle16:'):]}"
    )
    new_iri_full = f"http://cycle16.local/ontology#{new_spec_iri[len('cycle16:'):]}"

    link_body = f"""
PREFIX c6: <http://cycle6.local/ontology#>

INSERT DATA {{
  GRAPH <{ASSERTION_GRAPH}> {{
    <{new_iri_full}> c6:supersedesRef <{old_iri_full}> .
  }}
}}
"""
    link_http, link_ms, _ = _sparql_post(SPARQL_UPDATE_ENDPOINT, link_body, op="update")

    deprecate_body = f"""
PREFIX c6: <http://cycle6.local/ontology#>

DELETE {{ GRAPH <{ASSERTION_GRAPH}> {{ <{old_iri_full}> c6:rank ?old_rank . }} }}
INSERT {{ GRAPH <{ASSERTION_GRAPH}> {{ <{old_iri_full}> c6:rank "deprecated" . }} }}
WHERE  {{ GRAPH <{ASSERTION_GRAPH}> {{ <{old_iri_full}> c6:rank ?old_rank . }} }}
"""
    dep_http, dep_ms, _ = _sparql_post(
        SPARQL_UPDATE_ENDPOINT, deprecate_body, op="update"
    )

    return {
        "new_spec_iri": new_spec_iri,
        "old_spec_iri": old_spec_iri,
        "write_1_http_status": result["http_status_code"],
        "write_1_ms": result["response_time_ms"],
        "write_2_link_http_status": link_http,
        "write_2_link_ms": link_ms,
        "write_3_deprecate_http_status": dep_http,
        "write_3_deprecate_ms": dep_ms,
        "success_bool": all(
            s in (200, 204)
            for s in (result["http_status_code"], link_http, dep_http)
        ),
    }


def record_author_refusal(
    refusal_class: str,
    spec_partial: dict[str, Any],
    rationale: str,
    project_dir: str | Path = ".",
    namespace: str = "cycle_16.be_b.spec_registry",
) -> None:
    """Record an author-side refusal for Brief 4 KT-3 firing-surface evaluation.

    refusal_class ∈ REFUSAL_CLASSES:
      - acceptance_criteria_unclear (a) → KT-3 candidate
      - backlog_from_same_cycle_default (b) → KT-3 candidate
      - dp44_honest_gap (c) → NOT KT-3; operational signal
      - n_a_rationale_unclear (d) → KT-3 candidate
    """
    if refusal_class not in REFUSAL_CLASSES:
        raise ValueError(
            f"refusal_class='{refusal_class}' not in {REFUSAL_CLASSES}"
        )
    project_dir = Path(project_dir).expanduser().resolve()
    _emit(
        project_dir,
        namespace,
        "spec_registry.author_refusal.event",
        {
            "refusal_class": refusal_class,
            "rationale": rationale,
            "spec_partial": spec_partial,
            "kt_3_candidate_bool": refusal_class != "dp44_honest_gap",
        },
    )


# --- CLI ---


def _cli() -> int:
    parser = argparse.ArgumentParser(
        description="Cycle 16 BE-B spec_registry authoring wrapper",
    )
    sub = parser.add_subparsers(dest="op", required=False)

    sub_register = sub.add_parser("register", help="Operation 1: register a spec")
    sub_register.add_argument("--spec-json", required=True, help="Path to spec JSON")
    sub_register.add_argument("--project-dir", default=".")

    sub_read = sub.add_parser("read", help="Operation 2: read spec status")
    sub_read.add_argument("--spec-iri", required=True)

    sub_cycle = sub.add_parser("cycle-close-gate", help="Operation 3")
    sub_cycle.add_argument("--cycle-n", type=int, required=True)

    sub_session = sub.add_parser("session-close-gate", help="Operation 4")
    sub_session.add_argument("--current-index", type=int, required=True)
    sub_session.add_argument("--authored-index", type=int, required=True)
    sub_session.add_argument("--threshold", type=int, default=3)

    sub_help = sub.add_parser("help", help="Print extended help")

    args = parser.parse_args()
    if args.op == "register":
        with open(args.spec_json) as f:
            spec = json.load(f)
        r = register_spec(spec, project_dir=args.project_dir)
        print(json.dumps(r, indent=2))
        return 0 if r["success_bool"] else 1
    if args.op == "read":
        r = read_spec_status(args.spec_iri)
        print(json.dumps(r, indent=2))
        return 0
    if args.op == "cycle-close-gate":
        r = fire_cycle_close_gate(args.cycle_n)
        print(json.dumps(r, indent=2))
        return 0 if r["verdict"] == "PASS" else 1
    if args.op == "session-close-gate":
        r = fire_session_close_gate(
            args.current_index, args.authored_index, args.threshold
        )
        print(json.dumps(r, indent=2))
        return 0 if r["verdict"] == "PASS" else 1
    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(_cli())
