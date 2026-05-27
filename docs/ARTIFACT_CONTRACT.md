# ARTIFACT CONTRACT

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- profile: build -->
<!-- methodology_status: BE-A authored — Cycle 16 Stage 5 BE-A (KG-resident 14-field spec registry schema + SPARQL UPDATE write-boundary primitives at Cycle 6 /cycle6 endpoint) -->
<!-- source: Cycle 16 SI ACTIVE 2026-05-27 (a2f14d5) + Amendment 2026-05-27a (be54a97) + Amendment 2026-05-27b (badd749) + kc-45 R1 PASS task-context dispatch via Cycle-16-S3 Coach + dispatch substrate ~/Moonshots_Career_Thesis_v2/.claude/workspace/cycle_16_s3_be_a_dispatch_substrate.md -->

> **Authority Hierarchy**
>
> | Priority | Document | Role |
> |----------|----------|------|
> | Tier 1 | `~/Moonshots_Career_Thesis_v2/.claude/strategic_frame.md` (8 Bindings ACTIVE) + Cycle 16 SI ACTIVE 2026-05-27 (a2f14d5) + Amendments 2026-05-27a (be54a97) + 2026-05-27b (badd749) | Primary spec — highest authority |
> | Tier 2 | `~/Moonshots_Career_Thesis_v2/.claude/identity/pipeline_identity.md` (hard constraints) + `~/cycle_16_close_spec_to_implementation_gap_build/EXPERIMENTAL_DESIGN.md` §0a + §4a + §Field 6 (paradigm + constraint surfaces) | Clarifications — cannot override Tier 1 |
> | Tier 3 | `~/cycle_6_unified_substrate_build/runtime/jena/ontology/cycle_6_unified_substrate.ttl` (LOCKED parent ontology; Path γ FORBIDDEN per Binding 7) + LANDSCAPE_ASSESSMENT.md §6 addendum (Coach-verified 2026-05-27 substrate-viability) | Advisory only — non-binding if inconsistent with Tier 1/2 |
> | Contract | This document | Implementation detail — subordinate to all tiers above |
>
> **Conflict rule:** When a higher-tier document and this contract disagree, the higher tier wins.
> Update this contract via `CONTRACT_CHANGE` or align implementation to the higher tier.

### Companion Contracts

**Upstream (this contract depends on):**
- See [ENVIRONMENT_CONTRACT](../core/ENVIRONMENT_CONTRACT.tmpl.md) §8 for determinism and runtime defaults
- See [DATA_CONTRACT](../core/DATA_CONTRACT.tmpl.md) §3 for input data contracts (when build consumes data)

**Downstream (depends on this contract):**
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §1 for the pass/fail thresholds this contract is measured against
- See [RUNTIME_EMIT_SPEC](RUNTIME_EMIT_SPEC.tmpl.md) §2 for the structured-emit shape this artifact MUST produce
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §1 for promotion gates this contract is verified at
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §1 for cross-system-validation event surfaces

## Customization Guide

(Customization Guide deleted at BE-A fill close per template instruction.)

---

## §0 Artifact Identity

<!-- gate:artifact_contract §0 required -->

| Field | Value |
|---|---|
| **Artifact name** | `cycle_16_be_a_spec_registry_schema_and_write_boundary` |
| **Artifact kind** | schema-and-write-boundary-protocol (TTL schema + SHACL constraints + SPARQL UPDATE authoring discipline doc) |
| **Repository path** | `~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_registry_schema.ttl` (primary TTL); `~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_registry_shapes.shacl.ttl` (SHACL constraints); `~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_authoring_discipline.md` (write-boundary protocol) |
| **Invocation interface** | SPARQL UPDATE INSERT DATA against `http://localhost:3030/cycle6/update` per `docs/spec_authoring_discipline.md` Operation 1 template body; readback via SPARQL SELECT against `http://localhost:3030/cycle6/query` |
| **Runtime targets** | Apache Jena Fuseki PID 479112 on azure-vm-7gb (Coach-verified 2026-05-27 12d uptime; --config /home/azureuser/cycle_6_unified_substrate_build/runtime/jena/run/cycle6.ttl) |
| **Lock commit** | (recorded post-fill at Cycle-16-S3 close paired-commit per Discipline #11 + PC #100) |
| **Build cycle** | Cycle 16 (Stage 5 BE-A) |
| **Test bed binding** | TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment (per ACCEPTANCE_CRITERIA §3 per-test-bed strengthening n=3; ED §0a HYBRID PRIMARY 4-spec-class × 4-substrate-operation × 5-discipline-state cell granularity) |
| **Contract owner** | build-runner (BE-A authoring) → spec-authoring-discipline (BE-B consumer at Cycle-16-S4) → Coach R3 close-eval (Cycle-16-S3 close) |

<!-- /gate:artifact_contract §0 -->

> The artifact identity row is the structural index every downstream gate
> resolves against. If any field is an unfilled double-brace placeholder token or `TBD` at the
> production-deployment gate, the gate FAILs by construction.

---

## §1 Pre-conditions

<!-- gate:artifact_contract §1 entries:1 -->

State the conditions that MUST hold before this artifact runs. Pre-conditions
are checked structurally at invocation; a failed pre-condition refuses the run
(per design-by-contract; Hoare/Meyer pattern).

| # | Pre-condition | How verified at runtime | Refusal behavior on FAIL |
|---|---|---|---|
| 1 | **Fuseki `/cycle6` UPDATE write-boundary OPERATIONAL** (PID 479112 alive; HTTP 200 on SPARQL UPDATE INSERT DATA; readback HTTP 200 returns inserted triples verbatim). Coach-verified 2026-05-27 ~19:00 UTC: UPDATE 0.621s; SELECT readback 0.035s; DROP GRAPH cleanup HTTP 200. | `python3 -c "import urllib.request, urllib.parse; data=urllib.parse.urlencode({'query':'ASK { ?s ?p ?o }'}).encode(); req=urllib.request.Request('http://localhost:3030/cycle6/query', data=data, headers={'Accept':'application/sparql-results+json'}); print(urllib.request.urlopen(req,timeout=10).status)"` returns `200` | halt-and-surface as KT-6 candidate per Binding 7 + ED §Field 6; return `status: blocked` in YAML envelope; do NOT route around via SQL/YAML fallback unless KT-6 escalation Rex-dispositioned |
| 2 | **Cycle 6 BE#1 ontology TTL accessible + LOCKED** at canonical path `~/cycle_6_unified_substrate_build/runtime/jena/ontology/cycle_6_unified_substrate.ttl` with predicates `c6:Statement` + `c6:accessPermission` + `c6:AccessPermission` + `c6:rank` + `c6:supersedesRef` + `c6:wasDerivedFrom` + `c6:wasAttributedTo` + `c6:wasGeneratedBy` + `c6:wasInformedBy` + `c6:assertion` + `c6:provenance` + `c6:publicationInfo` available + namespace `c6:` = `http://cycle6.local/ontology#` resolvable | `python3 -c "import rdflib; g=rdflib.Graph(); g.parse('/home/azureuser/cycle_6_unified_substrate_build/runtime/jena/ontology/cycle_6_unified_substrate.ttl', format='turtle'); print(len(g))"` returns ≥200 triples + 0 parse errors | halt-and-surface; do NOT modify Cycle 6 LOCKED body (Path γ FORBIDDEN per Binding 7); fall back to Path β additive `cycle16:` namespace predicates if regression suspected |
| 3 | **SHACL `cycle16:Spec rdfs:subClassOf c6:Statement` inheritance accepted by Fuseki SHACL validator** — verify polymorphism at BE-A smoke test: `c6:StatementAccessPermissionShape` (sh:targetClass c6:Statement) constraint MUST fire on `cycle16:Spec` instances via subclass inheritance | Smoke test at BE-A close: write synthetic `cycle16:Spec` instance MISSING `c6:accessPermission` → pyshacl validation MUST report violation referencing `c6:StatementAccessPermissionShape`; write same instance WITH `c6:accessPermission c6:publishable` → MUST conform | halt-and-surface; fall back to Path β (additive `cycle16:specAccessPermission` mirroring `c6:accessPermission`); record disposition in BUILD_DECISION_LOG §1.4 |
| 4 | **`cycle16:` namespace `http://cycle16.local/ontology#` collision-free** at BE-A first write — no pre-existing triples in `/cycle6` using `cycle16:` predicates | `python3 -c "import urllib.request, urllib.parse; data=urllib.parse.urlencode({'query':'ASK { ?s ?p ?o FILTER STRSTARTS(STR(?p), \"http://cycle16.local/ontology#\") }'}).encode(); req=urllib.request.Request('http://localhost:3030/cycle6/query', data=data, headers={'Accept':'application/sparql-results+json'}); import json; print(json.loads(urllib.request.urlopen(req,timeout=10).read())['boolean'])"` returns `False` BEFORE BE-A first write | halt-and-surface; investigate collision source; do NOT proceed without namespace-clean ground state |
| 5 | **Parent-cycle FINDINGS substrate available** at ED §Field 6 KT-1..KT-6 matrix + HR §3 H1-H8 + LA §6 addendum (Cycle 6 substrate-viability evidence: 246,048 quads / 46 named graphs / SPARQL latency 0.066-0.495s; KT-6 DOES NOT FIRE; KT-1 DOES NOT FIRE under refined mechanism-layer metric per Rex disposition (C) D-S2-1 2026-05-27) | `wc -l ~/cycle_16_close_spec_to_implementation_gap_build/{EXPERIMENTAL_DESIGN.md,HYPOTHESIS_REGISTRY.md,docs/LANDSCAPE_ASSESSMENT.md}` returns ≥1700 + ≥140 + ≥600 lines + grep confirms §Field 6 + §3 + §6 sections present | halt-and-surface (under-spec'd dispatch); refuse-on-missing-precondition per DP#44 + S132 |

<!-- /gate:artifact_contract §1 -->

> [SEED: min_preconditions=1]
> Pre-conditions are NOT defensive null checks — they are the contract
> the consumer commits to before invocation. Examples: "input file exists at
> path X with schema Y", "auth token is non-empty and valid for scope Z",
> "upstream artifact A is at lock commit B".

---

## §2 Post-conditions

<!-- gate:artifact_contract §2 entries:1 -->

State the conditions the artifact GUARANTEES on successful completion. Post-conditions
are what consumers depend on; ACCEPTANCE_CRITERIA tests them.

| # | Post-condition | How verified after run | What CROSS_SYSTEM_VALIDATION measures against |
|---|---|---|---|
| 1 | **`docs/spec_registry_schema.ttl` EXISTS + PARSEABLE** as TTL with 0 errors AND declares `cycle16:Spec rdfs:subClassOf c6:Statement` + 4 spec-class enum (`cycle16:AgentContract` + `cycle16:Schema` + `cycle16:DesignDecision` + `cycle16:MethodologyCommitment`) + 5-state taxonomy enum + 14 field predicates per substrate §2 verbatim | `python3 -c "import rdflib; g=rdflib.Graph(); g.parse('~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_registry_schema.ttl', format='turtle'); print(len(g))"` returns ≥40 triples + 0 errors + `python3 -c "from rdflib import Graph,Namespace; g=Graph(); g.parse('...', format='turtle'); CY=Namespace('http://cycle16.local/ontology#'); print((CY.Spec, None, None) in g)"` returns True | CROSS_SYSTEM_VALIDATION TB-1+TB-2+TB-3 readback bindings — TTL is the schema CSV measures against |
| 2 | **`docs/spec_registry_shapes.shacl.ttl` EXISTS + PARSEABLE** with `cycle16:SpecShape` (sh:targetClass cycle16:Spec) + `cycle16:SpecTypeShape` (sh:in 4-class enum) + `cycle16:CurrentStatusShape` (sh:in 5-state enum) + inherited `c6:StatementAccessPermissionShape` polymorphism for `cycle16:Spec` instances via subclass inheritance | `python3 -c "import rdflib; g=rdflib.Graph(); g.parse('~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_registry_shapes.shacl.ttl', format='turtle'); print(len(g))"` returns ≥30 triples + 0 errors | CROSS_SYSTEM_VALIDATION SHACL acceptance verdicts per test bed (TB-1+TB-2+TB-3 conforming specs MUST PASS; ≥4 non-conforming fixture specs MUST FAIL with violation messages referencing specific shape) |
| 3 | **`docs/spec_authoring_discipline.md` EXISTS** with 5 substrate-operation templates (Operation 1 registry-write SPARQL UPDATE INSERT DATA + Operation 2 registry-read SELECT + Operation 3 cycle-close-gate-fire ASK + Operation 4 session-close-gate-fire ASK + Operation 5 spec-supersedure 3-write protocol) + per-edge HC-11 enforcement contract + PROV-O 4-typed-edges contract + nanopublication 3-graph optional path | `grep -c "^### Operation" ~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_authoring_discipline.md` returns ≥5 + grep confirms HC-11 + PROV-O + nanopub sections present | BUILD_DECISION_LOG §1 verdict references; consumer BE-B at Cycle-16-S4 reads this body |
| 4 | **SPARQL UPDATE smoke test PASSES end-to-end** for 3 test beds (TB-1 AgentContract / TB-2 Schema / TB-3 MethodologyCommitment) — write synthetic `cycle16:Spec` to test graph `<http://cycle16.local/test/be_a_smoke>` + SELECT readback returns all 14 field predicates per spec + DROP GRAPH cleanup HTTP 200 | Recorded in BUILD_DECISION_LOG §1 verdict row + DEPLOYMENT_LOG §2 build event row + `outputs/cross_system_validation_be_a.json` 3-test-bed results + smoke test fires `be_a_spec_registry.write.event` per write to `outputs/build_runner_events.jsonl` | CROSS_SYSTEM_VALIDATION §3 per-test-bed strengthening n=3 confirmation; H1+H2+H5+H6+H7 surface evidence per HR §3 |
| 5 | **SHACL refuses non-conforming specs** — write fixtures with ≥4 SHACL violation classes (missing owner / invalid spec_type / dormant-silent without target session / missing accessPermission) → pyshacl reports ≥4 violations referencing specific shape IRIs | `python3 -c "import pyshacl, rdflib; data=rdflib.Graph(); data.parse('outputs/be_a_smoke_fixture_nonconforming.ttl', format='turtle'); shapes=rdflib.Graph(); shapes.parse('docs/spec_registry_shapes.shacl.ttl', format='turtle'); shapes.parse('/home/azureuser/cycle_6_unified_substrate_build/runtime/jena/shapes/access_permission.shacl.ttl', format='turtle'); r=pyshacl.validate(data, shacl_graph=shapes); print('conforms='+str(r[0])+'; violations='+str(r[2].count('Violation')))"` returns conforms=False + violations≥4 | BUILD_DECISION_LOG §1 SHACL verdict row + HR §3 H6 (predicate extension clean) evidence |
| 6 | **`outputs/build_runner_events.jsonl` HAS ≥6 events** conforming to RUNTIME_EMIT_SPEC §1 schema: ≥1 session.start + ≥1 dispatch.received + ≥5 build.phase.start (one per Step 1-5) + ≥5 build.phase.complete + ≥1 session.end + ≥1 be_a_spec_registry.write.event per test bed write | `wc -l outputs/build_runner_events.jsonl` returns ≥6 + `python3 -c "import json; [json.loads(l) for l in open('outputs/build_runner_events.jsonl')]"` returns 0 parse errors | CROSS_SYSTEM_VALIDATION reads JSONL for write.event aggregation; runtime-emit evidence for ACCEPTANCE_CRITERIA §2 measurement protocol |

<!-- /gate:artifact_contract §2 -->

> [SEED: min_postconditions=1]
> Post-conditions are the artifact's outward-facing promise. They are what
> downstream consumers wire against. A post-condition that cannot be verified
> by inspection of the artifact's output (or runtime-emit) is not a contract;
> it is a wish.

---

## §3 Invariants

<!-- gate:artifact_contract §3 entries:1 -->

State the invariants the artifact preserves across its lifecycle (between
invocations, across versions, across deployment targets).

| # | Invariant | When checked | If violated |
|---|---|---|---|
| 1 | **Cycle 6 LOCKED ontology body UNMODIFIED throughout BE-A** (`git -C ~/cycle_6_unified_substrate_build diff runtime/jena/ontology/` returns empty post-BE-A) — Path γ FORBIDDEN per Binding 7 | HC #26 internal smoke gate 3 (backwards-compat preservation) at BE-A close before STOP/yield | CONTRACT_CHANGE = Rex paradigm ruling per Binding 7; halt-and-surface; rollback BE-A artifacts via §5 procedure |
| 2 | **Per-edge HC-11 `c6:accessPermission` declared on every `cycle16:Spec` instance materialized** — SHACL `c6:StatementAccessPermissionShape` polymorphism via subclass inheritance enforces structurally | At every SPARQL UPDATE INSERT DATA invocation against `/cycle6` per spec_authoring_discipline.md Operation 1; pre-write SHACL validation fires | refuse-on-violation per RUNTIME_EMIT_SPEC §3 halt-and-surface; emit `build_runner_runtime_failure` drift event |
| 3 | **PROV-O 4 typed-edges on every spec materialized** — `prov:wasGeneratedBy` + `prov:wasAttributedTo` + `prov:generatedAtTime` + `prov:wasInformedBy` written to `<spec_iri>:provenance` named graph per nanopublication 3-graph pattern | At every Operation 1 write (per nanopub assertion + provenance + publicationInfo graph triplet); BE-A smoke test SELECT readback verifies presence | halt-and-surface; orphan-spec without provenance = HC-07-equivalent at spec-class grain |
| 4 | **Wikidata rank IN {preferred, normal, deprecated} enforced via SHACL** — `c6:rank` predicate inherited from Cycle 6 BE#1 ontology via `cycle16:Spec rdfs:subClassOf c6:Statement`; `c6:StatementRankShape` polymorphism applies | At every Operation 1 write where `c6:rank` is set; default `c6:rank "normal"` at registry-write; transitions to "deprecated" at supersedure (Operation 5) | refuse-on-violation; SHACL rejects invalid rank value at write boundary |
| 5 | **5-state taxonomy `current_status` IN {running, dormant-with-explicit-deferral, dormant-silent, killed, long-running} enforced via SHACL** — `cycle16:CurrentStatusShape` with `sh:in` enum | At every Operation 1 write; at every Operation 2 read (consumer-side validation that state value matches enum) | refuse-on-violation; SHACL rejects invalid state value at write boundary |
| 6 | **Append-only DEPLOYMENT_LOG + BUILD_DECISION_LOG discipline** — no prior row edited; corrections via `supersedes:` reference; `git diff` post-fill shows ONLY new rows added | Pre-commit at Cycle-16-S3 close paired-commit per Discipline #11 | halt-and-surface; revert offending edit; re-apply via supersedes reference |

<!-- /gate:artifact_contract §3 -->

> Invariants distinguish a build-class artifact from a one-shot script.
> Examples: "schema X is preserved across versions ≥1.0", "output ordering
> is deterministic across runtime targets", "no side effects outside paths
> declared in §4".

---

## §4 Side Effects and Resource Footprint

| Surface | Effect | Bounds |
|---|---|---|
| Filesystem writes | `~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_registry_schema.ttl` (new); `~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_registry_shapes.shacl.ttl` (new); `~/cycle_16_close_spec_to_implementation_gap_build/docs/spec_authoring_discipline.md` (new); `~/cycle_16_close_spec_to_implementation_gap_build/outputs/build_runner_events.jsonl` (append-only); `~/cycle_16_close_spec_to_implementation_gap_build/outputs/cross_system_validation_be_a.json` (new); `~/cycle_16_close_spec_to_implementation_gap_build/outputs/be_a_smoke_fixture_conforming.ttl` (new); `~/cycle_16_close_spec_to_implementation_gap_build/outputs/be_a_smoke_fixture_nonconforming.ttl` (new); `~/cycle_16_close_spec_to_implementation_gap_build/outputs/build_runner_envelope.yaml` (new); Edits to `docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md` (scaffolded templates — Edit-per-section per build-runner.md §Canonical marker preservation) | ≤500KB cumulative across all new files; JSONL append-only growth ≤50KB at BE-A close |
| Database writes | SPARQL UPDATE INSERT DATA against Fuseki `/cycle6` SPARQL endpoint at `<http://cycle16.local/test/be_a_smoke>` named graph (test only; DROP GRAPH cleanup at BE-A close); NO production-registry writes at BE-A (production writes are BE-B scope per Cycle-16-S4 dispatch) | ≤50 triples per test spec × 3 test beds = ≤150 triples written + ≤150 triples dropped at cleanup; net zero persistent storage delta at BE-A close |
| Network egress | NONE (localhost-only: Fuseki at `http://localhost:3030/cycle6/update` + `http://localhost:3030/cycle6/query`) | 0 external requests; ≤10 localhost HTTP requests at smoke test |
| Process / thread footprint | python3 subprocess for rdflib parse + pyshacl validation + urllib.request POST; no daemon processes spawned | ≤2 concurrent python3 invocations; ≤30s wall-clock per invocation; ≤5s SPARQL response latency per call (Coach probe verified 0.066-0.621s; 10-75× margin) |
| Energy / GPU / memory | rdflib parse + pyshacl validation: ≤100MB RAM per invocation; no GPU; no inference cost | ≤500MB peak total across BE-A execution |

> A build-class artifact ships into production runtime; its resource
> footprint MUST be declared so cross-system-validation can measure
> against it. "It's small" is not a footprint — declare numbers.

---

## §5 Versioning and Promotion Hooks

| Field | Value |
|---|---|
| **Version scheme** | cycle-id-anchored: TTL declares `owl:versionInfo "0.1 (Cycle 16 BE-A)"`; promotion semver bumps at Cycle-16-S4 BE-B consumer wiring (0.2) + Cycle-16-S5 BE-C gate wiring (0.3) + Cycle 16 close (1.0 candidate per HR §3 H1-H8 disposition) |
| **Promotion authority** | build-runner BUILT (not yet PROMOTED) at BE-A close (Cycle-16-S3) → Coach R3 evaluation at Cycle-16-S3 close-eval → build-orchestrator promotion at Cycle-16-S4+ BE-B consumer integration → Rex paradigm ruling required on CONTRACT_CHANGE OR KT-6 firing (Binding 7 + S155) |
| **Promotion gates** | `build_pipeline_gate.sh` (`~/ml-governance-templates/scripts/build_pipeline_gate.sh`) + `production_deployment_gate.sh` + `cross_system_validation_gate.sh` per `build-runner.md §Dispatch Model`; plus Cycle 14 inherited gates `k_register_present_gate.sh` + `known_boundaries_present_gate.sh` + `h_pattern_dispositions_present_gate.sh` + `hc26_internal_smoke_gate.sh` per scaffold `outputs/*_gate_results.json` evidence |
| **Rollback procedure** | (1) `python3 -c "import urllib.request, urllib.parse; data=urllib.parse.urlencode({'update':'DROP GRAPH <http://cycle16.local/test/be_a_smoke>'}).encode(); print(urllib.request.urlopen('http://localhost:3030/cycle6/update', data=data).status)"` returns 200; (2) repeat for `<http://cycle16.local/registry/assertion>` + `<http://cycle16.local/registry/provenance>` + `<http://cycle16.local/registry/publicationInfo>` if BE-B has wired production registry graphs (BE-A only writes to test graph; BE-A rollback is graph-only); (3) `rm docs/spec_registry_schema.ttl docs/spec_registry_shapes.shacl.ttl docs/spec_authoring_discipline.md outputs/cross_system_validation_be_a.json outputs/be_a_smoke_fixture_*.ttl outputs/build_runner_envelope.yaml`; (4) revert scaffolded template Edits via `git checkout docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md`; rollback END-TO-END TESTED at BE-A close-smoke via DROP GRAPH `<http://cycle16.local/test/be_a_smoke>` cleanup (per Coach probe pattern 2026-05-27) — DEPLOYMENT_LOG §6 self-test #3 row checkable. |

> See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 for the promotion
> gate stack this artifact passes through. Rollback procedure MUST
> be tested (not just documented) before first production promotion.

---

## §6 Change Control Triggers

The following changes require a `CONTRACT_CHANGE` commit:

- Pre-conditions or post-conditions (any §1 / §2 row)
- Invariants (any §3 row) — particularly invariant #1 (Cycle 6 LOCKED body) which binds Path γ forbidden discipline per Binding 7
- Side-effect surfaces (any new §4 row) — particularly any promotion of test-graph writes to production-registry graph writes (BE-B scope per Cycle-16-S4)
- Version scheme or promotion authority (§5)
- Runtime targets (top-of-document Runtime targets row) — particularly any KT-6 firing requiring fall back to SQL/YAML per pre-Amendment-27b binary framing
- 14-field schema field count or constraints (Field 6 5-state taxonomy / Field 11 DP#26 carve-out / Field 12 ≤3-session threshold per Amendment 2026-05-27a)
- SPARQL UPDATE write-boundary template body or per-edge HC-11 enforcement contract

CONTRACT_CHANGE authority = Rex paradigm ruling per Binding 7 + S155 + BUILD_DECISION_LOG §4 verbatim. Do NOT route around via §11 override addendum or Coach-direct template edit per S155 BINDING.

> **Refusal authority binding (refuse-on-missing-precondition; design-by-contract refusal pattern):** if the artifact's running
> behavior diverges from this contract WITHOUT an accompanying CONTRACT_CHANGE,
> the cross-system-validation gate FAILs structurally. Re-aligning runtime
> to contract is the only repair path; routing around the contract is forbidden.

---

## §7 Self-test (BEFORE shipping the artifact)

| # | Check | Status |
|---|---|---|
| 1 | Every §1 pre-condition has a runtime verification hook (§1 col 3) | [x] (5 rows: ASK probe + rdflib parse + pyshacl polymorphism + namespace collision ASK + wc -l ED+HR+LA all wired) |
| 2 | Every §2 post-condition is verifiable from artifact output OR runtime-emit | [x] (6 rows: rdflib parse + SHACL parse + grep operations + BUILD_DECISION_LOG verdict row + pyshacl violations + wc -l JSONL all wired) |
| 3 | Every §3 invariant has a checkpoint AND a violation-handling row | [x] (6 rows: HC #26 smoke gate 3 + per-write SHACL + per-write provenance + SHACL rank enum + SHACL state enum + git diff append-only all wired) |
| 4 | §4 side effects enumerate every path/table/host the artifact touches | [x] (5 surfaces: filesystem + DB/SPARQL + network localhost-only + process + memory all bounded) |
| 5 | §5 promotion gates resolve to ≥1 gate script in [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 | [x] (build_pipeline_gate.sh + production_deployment_gate.sh + cross_system_validation_gate.sh per build-runner.md §Dispatch Model + Cycle 14 inherited gates at outputs/*_gate_results.json) |
| 6 | §6 change control triggers list every load-bearing field above | [x] (7 trigger classes: §1 + §2 + §3 + §4 + §5 + 14-field schema + SPARQL UPDATE template body) |

> If any check is `[ ]` unchecked, this contract is not ready for
> ACCEPTANCE_CRITERIA verification. Halt-and-surface (per refuse-on-missing-precondition).
