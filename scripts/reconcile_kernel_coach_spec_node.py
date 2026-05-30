#!/usr/bin/env python3
"""Reconcile the kernel-coach spec node to EXECUTION reality + record provenance.

Cycle-16-S25 vertical slice T4 (#32 KG reconcile, prove node==fire) + T5 (#40
provenance retrofit). Uses the EXISTING spec_registry_authoring library functions
(`_sparql_post`, `_emit`, the graph constants) — NOT a hand-edited raw triple file
and NOT a forked SPARQL client. The Fuseki /cycle6 endpoint is live (HTTP 200; see
`read_spec_status`).

T4 — reconcile to reality:
  The node currently asserts cycle16:currentStatus = running, but carried ZERO
  execution-evidence triples (no run_id). That is precisely the asserted-status-
  without-execution-evidence gap this cycle exists to catch. We add EXECUTION
  evidence: cycle16:cycleImplemented, cycle16:sessionImplemented, and a NEW
  cycle16:implementationRunId carrying the REAL run_id from the T1 emit
  (outputs/kernel_coach_events.jsonl transition.fire). We then PROVE
  node-run_id == emit-run_id by reading both.

T5 — provenance retrofit:
  Record prov:wasDerivedFrom edges (the schema's provenance predicate; the
  cycle16:auditTrailLink is the prov:wasGeneratedBy subproperty, schema L182):
    spec -> kernel-coach.md (audit_tuple source)
    spec -> kernel_coach_workflow_primitive_spec.md (PRIMARY)

Mechanism: SPARQL INSERT DATA against the live endpoint via the authoring
library's `_sparql_post`, plus a `spec_registry.write.event` emit via `_emit`.
Refuse-on-missing-precondition: if the emit run_id can't be read, REFUSE.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from spec_registry_authoring import (  # noqa: E402
    _sparql_post,
    _emit,
    read_spec_status,
    SPARQL_UPDATE_ENDPOINT,
    SPARQL_QUERY_ENDPOINT,
    ASSERTION_GRAPH,
    PROVENANCE_GRAPH,
)

PROJECT_DIR = Path(__file__).resolve().parent.parent
SPEC_IRI = "cycle16:spec_retroactive_af3a918a"
SINK = PROJECT_DIR / "outputs" / "kernel_coach_events.jsonl"

# Absolute file:// URIs so the provenance edges resolve faithfully (a relative
# <~/...> IRI gets a server-base prefix from Fuseki).
KERNEL_COACH_MD = os.path.expanduser("~/Moonshots_Career_Thesis_v2/.claude/agents/kernel-coach.md")
PRIMITIVE_SPEC = os.path.expanduser("~/cycle_10_autonomous_cycle_apparatus_build/scripts/kernel_coach_workflow_primitive_spec.md")
KERNEL_COACH_MD_IRI = "file://" + KERNEL_COACH_MD
PRIMITIVE_SPEC_IRI = "file://" + PRIMITIVE_SPEC


def _emit_run_id() -> str:
    """Read the REAL run_id of the kernel_coach.transition.fire event from the sink."""
    if not SINK.exists():
        raise SystemExit("REFUSE: emission sink absent — cannot reconcile to fire (DP#44)")
    for line in SINK.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rec = json.loads(line)
        if rec.get("event_class") == "kernel_coach.transition.fire":
            rid = rec.get("run_id")
            if not rid:
                raise SystemExit("REFUSE: transition.fire has no run_id (DP#44)")
            return rid
    raise SystemExit("REFUSE: no kernel_coach.transition.fire in sink (DP#44)")


def main() -> int:
    emit_run_id = _emit_run_id()

    # --- BEFORE snapshot ---
    before = read_spec_status(SPEC_IRI)
    before_run_ids = [t for t in before["all_triples"] if "implementationRunId" in t[0]]
    print("=== T4 BEFORE ===")
    print(json.dumps({
        "status": before["status"],
        "triple_count": before["readback_triple_count"],
        "implementationRunId_triples": before_run_ids,
    }, indent=2))

    # --- T4 + T5 combined INSERT DATA (additive; node already running) ---
    # T4: execution evidence (run_id + cycle/session implemented).
    # T5: provenance derived-from edges.
    update = f"""
PREFIX c6: <http://cycle6.local/ontology#>
PREFIX cycle16: <http://cycle16.local/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>

INSERT DATA {{
  GRAPH <{ASSERTION_GRAPH}> {{
    {SPEC_IRI} cycle16:cycleImplemented 16 ;
      cycle16:sessionImplemented "Cycle-16-S25" ;
      cycle16:implementationRunId "{emit_run_id}" .
  }}
  GRAPH <{PROVENANCE_GRAPH}> {{
    {SPEC_IRI} prov:wasDerivedFrom <{KERNEL_COACH_MD_IRI}> ;
      prov:wasDerivedFrom <{PRIMITIVE_SPEC_IRI}> .
  }}
}}
"""
    http_status, ms, body = _sparql_post(SPARQL_UPDATE_ENDPOINT, update, op="update")
    success = http_status in (200, 204)
    print(f"\n=== SPARQL UPDATE (mechanism: live Fuseki /cycle6 via authoring lib _sparql_post) ===")
    print(f"http_status={http_status} response_time_ms={ms} success={success}")
    if not success:
        raise SystemExit(f"REFUSE: SPARQL update failed http={http_status} (DP#44 halt-and-surface)")

    # Emit a spec_registry.write.event recording the reconciliation (via authoring lib _emit).
    _emit(
        PROJECT_DIR,
        "cycle_16.be_b.spec_registry",
        "spec_registry.write.event",
        {
            "spec_id": SPEC_IRI,
            "graph_iri": ASSERTION_GRAPH,
            "reconcile_kind": "implementation_evidence_plus_provenance",
            "implementation_run_id": emit_run_id,
            "cycle_implemented": 16,
            "session_implemented": "Cycle-16-S25",
            "prov_wasDerivedFrom": [KERNEL_COACH_MD_IRI, PRIMITIVE_SPEC_IRI],
            "http_status_code": http_status,
            "response_time_ms": ms,
            "success_bool": success,
            "_run_id": emit_run_id,
        },
    )

    # --- AFTER snapshot + PROOF node-run_id == emit-run_id ---
    after = read_spec_status(SPEC_IRI)
    node_run_id_triples = [t for t in after["all_triples"] if "implementationRunId" in t[0]]
    node_run_id = node_run_id_triples[0][1] if node_run_id_triples else None
    # Provenance lives in the provenance named graph; read_spec_status reads only
    # the assertion graph, so query the provenance graph directly.
    prov_q = f"""
PREFIX cycle16: <http://cycle16.local/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>
SELECT ?o WHERE {{ GRAPH <{PROVENANCE_GRAPH}> {{ {SPEC_IRI} prov:wasDerivedFrom ?o }} }}
"""
    _st, _ms, prov_body = _sparql_post(SPARQL_QUERY_ENDPOINT, prov_q, op="query")
    prov_triples = [
        ["prov:wasDerivedFrom", b["o"]["value"]]
        for b in json.loads(prov_body)["results"]["bindings"]
    ]
    cycle_impl = [t for t in after["all_triples"] if t[0].endswith("cycleImplemented")]
    sess_impl = [t for t in after["all_triples"] if t[0].endswith("sessionImplemented")]

    print("\n=== T4 AFTER ===")
    print(json.dumps({
        "status": after["status"],
        "triple_count": after["readback_triple_count"],
        "cycleImplemented": cycle_impl,
        "sessionImplemented": sess_impl,
        "implementationRunId_triples": node_run_id_triples,
    }, indent=2))

    print("\n=== T4 PROOF: node-run_id == emit-run_id (read from BOTH, not asserted) ===")
    match = node_run_id == emit_run_id
    print(json.dumps({
        "emit_run_id (from outputs/kernel_coach_events.jsonl)": emit_run_id,
        "node_run_id (from Fuseki /cycle6 readback)": node_run_id,
        "MATCH": match,
    }, indent=2))

    print("\n=== T5 PROVENANCE triples written (read back from KG) ===")
    print(json.dumps(prov_triples, indent=2))

    if not match:
        raise SystemExit("REFUSE: node-run_id != emit-run_id — reconciliation not proven (DP#44)")
    print("\nRECONCILE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
