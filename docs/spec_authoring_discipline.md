# Spec Authoring Discipline — Cycle 16 BE-A

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- profile: build -->
<!-- methodology_status: BE-A authored — Cycle 16 Stage 5 BE-A SPARQL UPDATE write-boundary protocol -->
<!-- source: ARTIFACT_CONTRACT §0 + dispatch substrate §4 5-substrate-operations + Cycle 6 BE#1 contract -->

## §0 Scope and Authority

Authority: Cycle 16 SI ACTIVE 2026-05-27 (a2f14d5) + Amendment 2026-05-27a (be54a97; same-cycle deadline default + ≤3-session emit detection) + Amendment 2026-05-27b (badd749; KG-primary registry at Cycle 6 `/cycle6` endpoint).

This document specifies the spec-authoring discipline for materializing `cycle16:Spec` instances at the Cycle 6 unified knowledge-graph substrate via SPARQL UPDATE INSERT DATA against `http://localhost:3030/cycle6/update`. Consumed at Cycle-16-S4 BE-B (authoring discipline operationalization) + Cycle-16-S5 BE-C (TWO-surface BLOCKING gate fires).

**Substrate inheritance chain (Path α RECOMMENDED per substrate §3 HC-RP-S2-3 disposition):** `cycle16:Spec rdfs:subClassOf c6:Statement` inherits Cycle 6 BE#1 predicates (`c6:accessPermission` + `c6:rank` + `c6:supersedesRef` + PROV-O 4 typed-edges + nanopublication 3-graph pattern). Path γ (modifying Cycle 6 LOCKED ontology body) is FORBIDDEN per Binding 7. Path β (additive `cycle16:` namespace predicates) is acceptable only if smoke test surfaces SHACL polymorphism rejection.

## §1 Per-edge HC-11 enforcement contract (BIND)

Every `cycle16:Spec` instance materialization MUST declare `c6:accessPermission` per `c6:StatementAccessPermissionShape` inheritance via subclass polymorphism. Allowed values per Cycle 6 BE#1 ontology:

- `c6:publishable` — content may be exposed to public surfaces (e.g., schema definitions, methodology rationale narratives)
- `c6:ip-private` — pipeline IP; HC-11 retrieval REFUSED to unauthenticated queries (e.g., per-spec runtime emit details, internal drift-detection algorithm bodies)
- `c6:ephemeral` — transient working memory (e.g., session-scoped spec drafts pre-promotion)

**Default at BE-A:** `c6:publishable` for the 3 BE-A test bed synthetic specs (TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment); future BE-B + BE-C may use mixed enum per spec class.

**SHACL refusal at write boundary:** SHACL `c6:StatementAccessPermissionShape` MUST refuse writes missing `c6:accessPermission` OR with value outside the 3-enum. No silent partial-fill at write boundary per DP#44 BINDING.

## §2 PROV-O 4-typed-edges contract (BIND)

Every `cycle16:Spec` instance materialization MUST declare 4 PROV-O typed-edges in the `<spec_iri>:provenance` named graph per nanopublication 3-graph pattern:

1. **`prov:wasGeneratedBy`** — links spec to the spec-authoring session activity (`cycle16:session_<id>` activity IRI)
2. **`prov:wasAttributedTo`** — links spec to the owner agent/role (`cycle16:owner_<role>` agent IRI)
3. **`prov:generatedAtTime`** — `xsd:dateTime` timestamp of spec authoring
4. **`prov:wasInformedBy`** — links spec to upstream spec OR paradigm disposition (`cycle16:spec_<upstream_id>` OR `cycle16:disposition_<id>`)

Per Cycle 6 BE#1 contract orphan-refusal discipline: if `cycle16:Spec` instance also asserts `c6:Claim` (claim-class spec; subset; not all specs are claims), `c6:ClaimProvenanceShape` enforces `c6:wasDerivedFrom` MIN_COUNT 1 additionally.

## §3 Nanopublication 3-graph pattern (per spec type)

Materialization at `/cycle6` endpoint writes to 3 named graphs per `cycle16:Spec` instance:

- **`<spec_iri>:assertion`** — the field triples themselves (14 fields + audit_trail_link)
- **`<spec_iri>:provenance`** — PROV-O 4 typed-edges per §2
- **`<spec_iri>:publicationInfo`** — signer + publishedAtCycle + nanopub metadata

**Optional path per spec type:** ephemeral specs (e.g., session-scoped drafts) MAY skip the publicationInfo graph; assertion + provenance are MANDATORY for every spec.

## §4 5 Substrate-Operations (write boundary primitives)

### Operation 1: Registry-write (per-spec materialization at authoring boundary)

```sparql
PREFIX c6: <http://cycle6.local/ontology#>
PREFIX cycle16: <http://cycle16.local/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

INSERT DATA {
  GRAPH <http://cycle16.local/registry/assertion> {
    cycle16:spec_<UUID7> a cycle16:Spec ;
      cycle16:specType cycle16:AgentContract ;
      cycle16:owner "research-orchestrator" ;
      cycle16:acceptanceCriteria "Role invoked at >=1 session; agent_dispatch_event runtime emit observed within 3 sessions of authoring" ;
      cycle16:targetSession "Cycle-16-S5" ;
      cycle16:currentStatus cycle16:running ;
      cycle16:cycleAuthored 16 ;
      cycle16:sessionAuthored "Cycle-16-S3" ;
      cycle16:runtimeEmitEventClass "agent_dispatch_event" ;
      cycle16:dormancyDetectionThresholdSessions 3 ;
      cycle16:auditTrailLink cycle16:activity_be_a_authoring ;
      c6:accessPermission c6:publishable ;
      c6:rank "normal" .
  }
  GRAPH <http://cycle16.local/registry/provenance> {
    cycle16:spec_<UUID7> prov:wasGeneratedBy cycle16:session_Cycle_16_S3 ;
      prov:wasAttributedTo cycle16:owner_research_orchestrator ;
      prov:generatedAtTime "2026-05-27T19:00:00Z"^^xsd:dateTime ;
      prov:wasInformedBy cycle16:disposition_amendment_27a .
  }
  GRAPH <http://cycle16.local/registry/publicationInfo> {
    cycle16:spec_<UUID7> cycle16:publishedAtCycle 16 ;
      cycle16:nanopubSigner "cycle16-be-a" .
  }
}
```

**Invocation pattern (Python urllib; harness curl-fallback per build-runner.md §Tool Fallback Chains):**

```python
import urllib.request, urllib.parse
update_body = """<INSERT DATA query body verbatim above>"""
data = urllib.parse.urlencode({'update': update_body}).encode()
req = urllib.request.Request('http://localhost:3030/cycle6/update', data=data)
resp = urllib.request.urlopen(req, timeout=10)
assert resp.status == 200, f"UPDATE failed: HTTP {resp.status}"
```

### Operation 2: Registry-read (per-spec status enum)

```sparql
PREFIX cycle16: <http://cycle16.local/ontology#>

SELECT ?status ?targetSession ?runtimeEmitEventClass
WHERE {
  GRAPH <http://cycle16.local/registry/assertion> {
    cycle16:spec_<UUID7> cycle16:currentStatus ?status ;
                         cycle16:targetSession ?targetSession ;
                         cycle16:runtimeEmitEventClass ?runtimeEmitEventClass .
  }
}
```

### Operation 3: Cycle-close-gate-fire (BLOCKING discipline per H6 KT-4 surface)

Gate FAILS (BLOCKING) at cycle-close boundary if ASK returns TRUE for any spec authored at the closing cycle in dormant-silent state:

```sparql
PREFIX cycle16: <http://cycle16.local/ontology#>

ASK {
  GRAPH <http://cycle16.local/registry/assertion> {
    ?spec cycle16:currentStatus cycle16:dormant-silent ;
          cycle16:cycleAuthored <CYCLE_N> .
  }
}
```

Wired into `scripts/spec_implementation_present_gate.sh` at Cycle-16-S5 BE-C per ROADMAP Phase 4.

### Operation 4: Session-close-gate-fire (≤3-session dormancy threshold per Amendment 2026-05-27a)

Gate FAILS (BLOCKING) at session-close boundary if ASK returns TRUE for any spec exceeding dormancy threshold:

```sparql
PREFIX cycle16: <http://cycle16.local/ontology#>

ASK {
  GRAPH <http://cycle16.local/registry/assertion> {
    ?spec cycle16:currentStatus cycle16:dormant-silent ;
          cycle16:sessionAuthored ?sa ;
          cycle16:dormancyDetectionThresholdSessions ?threshold .
    # SESSIONS_BETWEEN primitive (count-of-JSONL-session-markers fallback):
    # operationally implemented at gate-script-shell layer (per BE-C wrap) as:
    #   sessions_between=$(grep -c '"event_class":"session.start"' outputs/*_events.jsonl)
    # then injected into ASK as literal
    FILTER (<CURRENT_SESSION_INDEX> - <SESSION_AUTHORED_INDEX> >= ?threshold)
  }
}
```

`SESSIONS_BETWEEN` is a SPARQL custom-function-equivalent primitive defined at BE-A as: count of `session.start` event markers in `outputs/*_events.jsonl` sinks between two session identifiers. Implemented as shell pre-computation at gate-script wrap layer (Operation 4 SPARQL ASK receives session indices as bound literals; no SPARQL custom-function dependency required). Wired into `scripts/spec_implementation_session_close_gate.sh` at Cycle-16-S5 BE-C.

### Operation 5: Spec-supersedure (non-destructive per Wikidata pattern via c6:supersedesRef)

3 atomic writes per supersedure event:

```sparql
PREFIX c6: <http://cycle6.local/ontology#>
PREFIX cycle16: <http://cycle16.local/ontology#>

# Atomic write 1: new spec materialization (per Operation 1)
INSERT DATA {
  GRAPH <http://cycle16.local/registry/assertion> {
    cycle16:spec_<NEW_UUID7> a cycle16:Spec ;
      # ... 14 fields per Operation 1 ...
      c6:rank "preferred" .
  }
}

# Atomic write 2: supersedesRef link from new -> old
INSERT DATA {
  GRAPH <http://cycle16.local/registry/assertion> {
    cycle16:spec_<NEW_UUID7> c6:supersedesRef cycle16:spec_<OLD_UUID7> .
  }
}

# Atomic write 3: old spec rank transition to deprecated
DELETE { GRAPH <http://cycle16.local/registry/assertion> { cycle16:spec_<OLD_UUID7> c6:rank ?old_rank . } }
INSERT { GRAPH <http://cycle16.local/registry/assertion> { cycle16:spec_<OLD_UUID7> c6:rank "deprecated" . } }
WHERE  { GRAPH <http://cycle16.local/registry/assertion> { cycle16:spec_<OLD_UUID7> c6:rank ?old_rank . } }
```

Both old + new specs remain queryable per Cycle 6 BE#1 contract: non-destructive supersedure preserves audit trail. Per HC-RP-S2-3 disposition: `c6:supersedesRef` ≡ `prov:wasRevisionOf` semantically (RESOLVED-VIA-NAMESPACE-EQUIVALENCE at FINDINGS Layer 4 honest gap).

## §5 Refuse-on-missing-precondition discipline (DP#44 BINDING)

SHACL validation MUST refuse non-conforming writes at the write boundary; no silent partial-fill. Specifically:

- **Missing owner (Field 3):** SHACL `cycle16:SpecShape` `sh:minCount 1` on `cycle16:owner` fires Violation.
- **Invalid spec_type (Field 2):** SHACL `cycle16:SpecTypeShape` `sh:in` 4-class enum fires Violation if value outside enum.
- **Dormant-silent without target_session (Field 5):** SHACL `cycle16:SpecShape` `sh:minCount 1` on `cycle16:targetSession` fires Violation (target_session is non-nullable regardless of state).
- **Missing accessPermission (HC-11 inherited):** Inherited `c6:StatementAccessPermissionShape` `sh:minCount 1` fires Violation via subclass polymorphism.
- **Invalid current_status (Field 6):** SHACL `cycle16:CurrentStatusShape` `sh:in` 5-state enum fires Violation if value outside enum.
- **Invalid rank (inherited):** Inherited `c6:StatementRankShape` `sh:in` {preferred, normal, deprecated} fires Violation.

At write boundary: any Violation halts the write; `build_runner_runtime_failure` drift event fires per RUNTIME_EMIT_SPEC §3; no partial fill propagates. Recovery: fix the spec body + re-author per Operation 1; do NOT route around via §11 override per S155 BINDING.

## §6 Test bed binding (3 test beds at BE-A per ACCEPTANCE_CRITERIA §3)

BE-A smoke test exercises Operation 1 via 3 test beds (TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment) against test graph `<http://cycle16.local/test/be_a_smoke>` (NOT production registry graphs). Per-test-bed write fires `be_a_spec_registry.write.event` per RUNTIME_EMIT_SPEC §1 schema. DROP GRAPH cleanup at BE-A close.

Per HYBRID PRIMARY (ED §0a + HR §3a): per-test-bed cell granularity within the 4×4×5 = 80-cell envelope (4 spec-classes × 4 substrate-operations × 5 discipline-states). BE-A populates 3 cells of the 4-spec-class × 1-substrate-operation (Operation 1 registry-write) × 1-state (running OR dormant-with-explicit-deferral per TB-3) projection = honest sparsity acceptable per HR §3a; full cell-coverage extends across BE-B + BE-C + BE-D + BE-E.

## §7 HC-11 partition (PUBLISHABLE vs IP-PRIVATE)

This document is `c6:publishable` per project gitignored-root convention (Cycle 16 SI scope; explicit ip-private tag required for any pipeline-IP content per Binding 8 HC-11 defensive depth).

- **PUBLISHABLE here:** 14-field schema narrative + 5-state taxonomy + Wikidata supersedure disposition + SPARQL UPDATE template body + per-edge HC-11 enforcement contract + PROV-O 4-typed-edges contract + nanopublication 3-graph pattern + 5 substrate-operation enumeration + SHACL refusal narrative.
- **IP-PRIVATE (referenced not inlined):** Per-role checklist contents at `~/ml-governance-templates/checklists/build_runner.checklist` (BUILD_DECISION_LOG §7 L180-L181); drift-detection internal algorithm bodies; pre-escalation gate state-machine internals; agent-prompt internals.

End of spec-authoring discipline document.
