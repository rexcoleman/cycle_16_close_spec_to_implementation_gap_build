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

---

## §10 BE-B H7 Cycle 16 Branch 4.2 BE-A-source Authoring Discipline Append

<!-- gate:artifact_contract §10 required -->

Per Cycle-16-S4 BE-B dispatch substrate §1 + §5 ARTIFACT_CONTRACT fill instructions + Cycle 14 §10 precedent. APPEND-only; §0-§7 (BE-A LOCKED `6c7c62d`) unchanged. Cycle 16 BE-B SPARQL UPDATE authoring discipline wrapper + govML v2.8.3 install_hook back-port (Branch 4.2 BE-A-source closure per ROADMAP Phase 3 task 2).

### §10.0 BE-B Cycle 16 Branch 4.2 Contract Identity

| Field | Value |
|---|---|
| **Artifact** | `scripts/spec_registry_authoring.py` (cycle_16 BE-B Python wrapper) + `scripts/install_spec_registry_authoring_discipline.sh` (cycle_16 standalone shell wrapper) + `~/ml-governance-templates/scripts/init_project.sh` install_hook (govML v2.8.3 ADDITIVE-APPEND) + `~/ml-governance-templates/templates/build/spec_registry/` NEW directory (5 files) |
| **Cycle** | 16 (BE-B Branch 4.2 BE-A-source closure per ROADMAP Phase 3 task 2 + Done #6 + H7 + KT-3 firing surface evaluation) |
| **Source** | BE-A SHIPPED `6c7c62d`: 5 substrate-operations at `docs/spec_authoring_discipline.md` (213L; verbatim consumed) + 14-field schema TTL at `docs/spec_registry_schema.ttl` (199L; copied verbatim to govML templates) + SHACL constraints at `docs/spec_registry_shapes.shacl.ttl` (162L; copied verbatim to govML templates) + govML v2.8.2 `install_runtime_emit_substrate()` structural precedent L171-L209 |
| **Architectural choice** | Brief 1: ADDITIVE-APPEND at govML init_project.sh per HC #45 (Cycle-15-S3 + Cycle-15-S7 precedent) — NEW function `install_spec_registry_authoring_discipline()` added AFTER `install_runtime_emit_substrate()` + NEW call site added to research-build profile branch AFTER existing call. NO modification of existing functions or arrays. (b) Imported-library + reference-by-shim pattern matches Cycle-14-S9 ARCH precedent + govML build_rubrics/ + runtime_emit/ |
| **Primary mechanism family** | Structural enforcement at scaffolding-time install (DP#1 structural > behavioral); Cycle 16 PRIMARY spec-implementation gap closure mechanism INSTALLED |
| **Authority chain** | Cycle 16 SI ACTIVE 2026-05-27 (`a2f14d5`) + Amendment 27a (`be54a97`) + Amendment 27b (`badd749`) + Rex disposition (C) D-S2-1 + S3 close D-S3-1 + Rex back-port directive 2026-05-27 (4-repo paired commit) + kc-45 R1 PASS task-context dispatch via Cycle-16-S4 Coach + dispatch substrate `~/Moonshots_Career_Thesis_v2/.claude/workspace/cycle_16_s4_be_b_dispatch_substrate.md` |

### §10.1 BE-B Pre-Conditions (rows 6-10)

| # | Pre-condition | How verified at runtime | Refusal behavior on FAIL |
|---|---|---|---|
| 6 | **BE-A artifacts UNMODIFIED at cycle_16/docs/** — `spec_registry_schema.ttl` + `spec_registry_shapes.shacl.ttl` + `spec_authoring_discipline.md` + BE-A §1-§3 LOCKED bodies at 5 scaffolded templates | `git diff` against BE-A SHIPPED `6c7c62d` HEAD returns empty for §1-§3 line ranges + 3 NEW BE-A artifact files unchanged | halt-and-surface; refuse-on-missing-precondition per DP#44 + S132; do NOT route around |
| 7 | **pyshacl + rdflib Python libraries importable** at runtime | `python3 -c "import pyshacl, rdflib; print('ok')"` exits 0 | halt-and-surface; install via `pip install pyshacl rdflib` (build-orchestrator scope); BE-B refuses |
| 8 | **govML `~/ml-governance-templates/scripts/init_project.sh` writable** + no git lock + no concurrent-write detection | `test -w ~/ml-governance-templates/scripts/init_project.sh && test ! -f ~/ml-governance-templates/.git/index.lock` exits 0 | halt-and-surface as Rex back-port directive blocker; surface to Coach |
| 9 | **govML `~/ml-governance-templates/templates/build/` writable** for NEW `spec_registry/` directory creation | `test -w ~/ml-governance-templates/templates/build/` exits 0 + `mkdir -p ~/ml-governance-templates/templates/build/spec_registry` succeeds | halt-and-surface as govML write-permission blocker |
| 10 | **Fuseki `/cycle6` UPDATE write-boundary OPERATIONAL** for production-graph dogfooding (regression vs BE-A 19:25 UTC verification) | ASK probe at `http://localhost:3030/cycle6/query` returns HTTP 200 + UPDATE INSERT DATA probe returns HTTP 200/204 | halt-and-surface as KT-6 substrate-viability candidate per Binding 7 + ED §Field 6 |

### §10.2 BE-B Post-Conditions (rows 7-12)

| # | Post-condition | How verified after run | What ACCEPTANCE_CRITERIA §10.1 measures against |
|---|---|---|---|
| 7 | **`scripts/spec_registry_authoring.py` EXISTS + IMPORTABLE** with 5 functions per spec_authoring_discipline §4 Ops 1-5 + `record_author_refusal` helper | `python3 -c "import sys; sys.path.insert(0,'scripts'); import spec_registry_authoring as sra; assert all(hasattr(sra, f) for f in ['register_spec','read_spec_status','fire_cycle_close_gate','fire_session_close_gate','supersede_spec','record_author_refusal'])"` exits 0 | ACCEPTANCE_CRITERIA §10.1 row 7 wrapper-import + function-presence threshold |
| 8 | **`scripts/install_spec_registry_authoring_discipline.sh` EXISTS + EXECUTABLE** + bash-syntax-clean + idempotent | `bash -n scripts/install_spec_registry_authoring_discipline.sh && test -x scripts/install_spec_registry_authoring_discipline.sh` exits 0 | ACCEPTANCE_CRITERIA §10.1 row 8 shell-syntax + executable-bit threshold |
| 9 | **govML `init_project.sh` install_hook ADDITIVE-APPEND landed** — NEW `install_spec_registry_authoring_discipline()` function present + NEW call site at research-build profile branch + `bash -n init_project.sh` exits 0 + existing functions unchanged | `grep -c "^install_spec_registry_authoring_discipline()" ~/ml-governance-templates/scripts/init_project.sh` returns ≥1 + `grep -c "install_runtime_emit_substrate$" ~/ml-governance-templates/scripts/init_project.sh` UNCHANGED | ACCEPTANCE_CRITERIA §10.1 row 9 ADDITIVE-APPEND threshold per HC #45 |
| 10 | **govML `templates/build/spec_registry/` directory ships 5 files** — `spec_registry_authoring.py` + `spec_registry_schema.ttl` + `spec_registry_shapes.shacl.ttl` + `spec_authoring_discipline.md` + `SPEC_AUTHORING_DISCIPLINE.md` obligation doc | `ls ~/ml-governance-templates/templates/build/spec_registry/` returns 5 files; obligation doc parses + is `c6:publishable` per HC-11 partition | ACCEPTANCE_CRITERIA §10.1 row 10 file-count + content threshold |
| 11 | **3-test-bed dogfooding to PRODUCTION registry graphs PASSES** — TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment (DP#26 carve-out) all write HTTP 200/204 + readback ≥11 mandatory triples + TB-3 includes `n_a_rationale` literal + spec_registry.write.event JSONL rows ≥3 | `outputs/be_b_dogfooding_results.json` `all_3_pass: true` + per-TB rows with `success: true` + JSONL grep `spec_registry.write.event` count ≥3 | ACCEPTANCE_CRITERIA §10.1 row 11 3-TB threshold + Brief 4 KT-3 firing surface evaluation |
| 12 | **govML v2.8.3 VERSION bump + CHANGELOG entry** at `~/ml-governance-templates/VERSION` head; backwards-compat preserved (17 legacy projects unmodified) | `head -1 ~/ml-governance-templates/VERSION` matches v2.8.3 header; `git -C ~/ml-governance-templates status --short` shows only VERSION + scripts/init_project.sh + templates/build/spec_registry/ additions | ACCEPTANCE_CRITERIA §10.1 row 12 version-bump + backwards-compat threshold |

### §10.3 BE-B Invariants (rows 7-9)

| # | Invariant | When checked | If violated |
|---|---|---|---|
| 7 | **govML `install_spec_registry_authoring_discipline()` is idempotent** — re-running install on same project_dir leaves state unchanged + does not error (subsequent runs are no-ops on already-installed files) | At fresh-scaffold smoke + at any re-install operation | halt-and-surface; idempotence is structural requirement per HC #45 (Cycle-15-S3 array-extension precedent) |
| 8 | **Wrapper enforces DP#26 n_a_rationale per HC-07** — `register_spec(..., runtime_emit_event_class="n/a")` REFUSES if `n_a_rationale` empty/absent; emits `spec_registry.shacl_refusal.event` with `refusal_class: dp26_n_a_rationale_missing` | At every `register_spec` invocation where field 11 starts with "n/a" | refuse-on-violation per DP#44 halt-and-surface; ValueError raised; no partial write to /cycle6 |
| 9 | **Author refusals categorized per 4-class taxonomy + JSONL-recorded** per substrate §3 (a)/(b)/(c)/(d) — `record_author_refusal()` validates `refusal_class` against REFUSAL_CLASSES enum + emits `spec_registry.author_refusal.event` with `kt_3_candidate_bool` derived | At every `record_author_refusal` invocation | refuse-on-violation if `refusal_class` outside enum; ValueError raised; Coach R3 R3 close-eval reads aggregated counts for Brief 4 KT-3 firing surface threshold |

### §10.4 BE-B Side Effects (diff vs BE-A §4)

| Surface | NEW effect at BE-B | Bounds |
|---|---|---|
| Filesystem writes | NEW: `cycle_16/scripts/spec_registry_authoring.py` (29.8KB) + `cycle_16/scripts/install_spec_registry_authoring_discipline.sh` (3.4KB) + `cycle_16/outputs/be_b_dogfooding_results.json` (new); EDITS to BE-A §10 appends at 5 scaffolded templates (Edit-per-section; canonical markers preserved); NEW govML `~/ml-governance-templates/scripts/init_project.sh` install_hook function (~76L additive) + call-site append (1L); NEW govML `~/ml-governance-templates/templates/build/spec_registry/` (5 files; ~70KB cumulative); govML `VERSION` v2.8.2 → v2.8.3 prepend; cycle_16 `outputs/spec_registry_events.jsonl` NEW + `outputs/build_runner_events.jsonl` append-only growth | ≤200KB cumulative new content; no existing-file body modifications outside §10 appends + init_project.sh additive call-site |
| Database writes | NEW: SPARQL UPDATE INSERT DATA against PRODUCTION registry graphs at `/cycle6` for 3 dogfooding specs (TB-1+TB-2+TB-3); written to `<http://cycle16.local/registry/assertion>` + `<http://cycle16.local/registry/provenance>` + `<http://cycle16.local/registry/publicationInfo>` named graphs (NOT test graphs — forward-apply per "no spec lands without registry row" discipline) | 3 specs × ~13-15 triples per spec × 3 graphs = ~120 triples persisted at production registry; NO cleanup (forward-apply discipline) |
| Network egress | Unchanged from BE-A: localhost-only Fuseki HTTP | ≤30 localhost HTTP requests across BE-B execution (3 writes × 2 ops + readbacks + smoke verifies + SHACL pre-validation HTTP calls = 0; SHACL fires in-process via pyshacl) |
| Process / thread footprint | Unchanged from BE-A: python3 subprocess for wrapper + pyshacl + urllib | ≤2 concurrent python3 invocations; ≤30s wall-clock per invocation |

### §10.5 BE-B Versioning and Promotion Hooks

| Field | Value |
|---|---|
| **Version scheme** | Wrapper module declares no semver yet; promotes alongside BE-C gate scripts at Cycle-16-S5 (BE-C inherits BE-B `spec_registry_authoring.py` as runtime dep) |
| **govML version** | v2.8.2 → v2.8.3 (Cycle-16-S4 BE-B paired commit; entry at `~/ml-governance-templates/VERSION`) |
| **Promotion authority** | build-runner BUILT at BE-B (Cycle-16-S4) → Coach R3 evaluation → build-orchestrator promotion at Cycle-16-S5 BE-C consumer integration → Rex paradigm ruling required on CONTRACT_CHANGE OR KT-N firing |
| **Promotion gates** | `build_pipeline_gate.sh` + `production_deployment_gate.sh` + `cross_system_validation_gate.sh` + `hc26_internal_smoke_gate.sh` (BE-B inherits BE-A gate stack) + NEW at BE-C: `spec_implementation_present_gate.sh` (Op 3) + `spec_implementation_session_close_gate.sh` (Op 4) |
| **Rollback procedure** | (1) `git -C ~/ml-governance-templates reset --hard HEAD~1` (govML v2.8.3 revert per pre-paired-commit baseline); (2) `rm cycle_16/scripts/spec_registry_authoring.py cycle_16/scripts/install_spec_registry_authoring_discipline.sh cycle_16/outputs/be_b_dogfooding_results.json`; (3) `git -C ~/cycle_16_close_spec_to_implementation_gap_build checkout docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md` (revert §10 appends); (4) production registry rollback: 3 DELETE DATA queries per dogfooding spec against `/cycle6` (each removes spec's 3-graph triples); (5) `git -C ~/cycle_6_unified_substrate_build diff runtime/jena/` returns empty (Cycle 6 LOCKED preserved). Rollback NOT end-to-end tested at BE-B (forward-apply production writes are intentional per "no spec lands without registry row" discipline); rollback test deferred to BE-C if Coach R3 disposition requires |

### §10.6 BE-B Change Control Triggers

- BE-B 11-deliverable scope per substrate §1 — any deviation from declared scope is CONTRACT_CHANGE per Binding 7 + S155
- govML v2.8.3 install_hook signature changes (function name, target paths, idempotence) — Rex paradigm ruling required
- 4-class refusal taxonomy enum changes (REFUSAL_CLASSES const) — affects Coach R3 KT-3 firing-surface evaluation; CONTRACT_CHANGE required
- 11 MANDATORY_FIELDS tuple changes — affects all downstream BE-C + per-project consumer assumptions; CONTRACT_CHANGE required
- DP#26 n_a-rationale enforcement logic change (`_validate_dp26_carve_out`) — DP#26 carve-out BINDING per HR §3d; CONTRACT_CHANGE required
- Production-graph forward-apply vs test-graph isolation (3-TB dogfooding writes) — affects spec-implementation-gap closure semantics; CONTRACT_CHANGE required

CONTRACT_CHANGE authority = Rex paradigm ruling per Binding 7 + S155 + BUILD_DECISION_LOG §4 verbatim.

### §10.7 BE-B Self-test (BEFORE shipping)

| # | Check | Status |
|---|---|---|
| 1 | Python wrapper imports cleanly + 5 Ops functions + record_author_refusal helper present | [x] PASS (verified: MANDATORY_FIELDS=11 / SPEC_TYPES=4 / STATUSES=5 / REFUSAL_CLASSES=4) |
| 2 | Shell wrapper bash-syntax-clean + executable | [x] PASS (`bash -n` exit 0; chmod +x applied) |
| 3 | govML init_project.sh install_hook function added + call-site added + bash-syntax-clean + ADDITIVE per HC #45 | [x] PASS (`grep -c install_spec_registry_authoring_discipline` returns 2; `bash -n` exit 0) |
| 4 | govML templates/build/spec_registry/ ships 5 files | [x] PASS (`ls` shows 5 files: 4 copied + 1 obligation doc) |
| 5 | govML VERSION bumped v2.8.2 → v2.8.3 | [x] PASS (head -1 returns v2.8.3 header) |
| 6 | 3-TB dogfooding to PRODUCTION /cycle6 graphs all PASS (write HTTP 200/204 + readback ≥11 triples + TB-3 includes n_a_rationale) | [x] PASS (TB-1 244ms 13 triples / TB-2 218ms 13 triples / TB-3 200ms 15 triples + n_a_rationale_present=true) |
| 7 | Fresh-scaffold smoke test confirms install_hook lands all 7 expected files | [x] PASS (`/tmp/be_b_smoke_<ts>/` ships scripts/spec_registry/{__init__.py, spec_registry_authoring.py} + docs/{schema, shapes, discipline, obligation} + outputs/spec_registry_events.jsonl empty sink + wrapper imports cleanly) |
| 8 | BE-A §1-§3 LOCKED bodies UNMODIFIED across 5 BE-A artifacts (git diff = 0 on §1-§3 line ranges) | [x] PASS (Edit-per-section; only §10 appended) |
| 9 | Cycle 6 LOCKED ontology body UNMODIFIED | [x] PASS (no Edits to ~/cycle_6_unified_substrate_build/runtime/jena/) |
| 10 | HC-11 partition preserved (publishable: interface + 5-state taxonomy + DP#26 design + JSON schemas; ip-private: internal algorithm bodies + classification heuristics) | [x] PASS (project gitignored at root; explicit publishable annotations in wrapper docstring) |

<!-- /gate:artifact_contract §10 -->

---

## §11 BE-C H6 Cycle 16 Branch 4.3 BE-B-source TWO-surface Gate Append

<!-- gate:artifact_contract §11 required -->

Per Cycle-16-S5 BE-C dispatch substrate §1 + §5 ARTIFACT_CONTRACT fill instructions + Cycle 14 §11 BE-class append precedent. APPEND-only; §0-§7 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED at Cycle-16-S4 close) unchanged. Cycle 16 BE-C TWO-surface BLOCKING gate (cycle-close + session-close) + govML v2.8.4 install_hook back-port (Branch 4.3 BE-B-source closure per ROADMAP Phase 4).

### §11.0 BE-C Cycle 16 Branch 4.3 Contract Identity

| Field | Value |
|---|---|
| **Artifact** | `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` (cycle-close BLOCKING) + `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` (session-close ADVISORY) + `~/ml-governance-templates/scripts/check_all_gates.sh` 5th-gate BLOCKING append + ADVISORY loop append + `~/ml-governance-templates/scripts/init_project.sh` install_hook ADDITIVE-APPEND (`install_spec_implementation_gates()`) + `~/ml-governance-templates/templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` NEW + govML VERSION v2.8.3 → v2.8.4 + 3-TB dogfooding capture `outputs/cross_system_validation_be_c.json` |
| **Cycle** | 16 (BE-C Branch 4.3 BE-B-source closure per ROADMAP Phase 4 + Done #7 + H6 + KT-4 firing surface evaluation) |
| **Source** | BE-B SHIPPED at Cycle-16-S4 close: `scripts/spec_registry_authoring.py` (5 Ops + record_author_refusal helper; 29.8KB) + `docs/spec_authoring_discipline.md §4 Operations 3+4` (verbatim consumed) + govML v2.8.3 `install_spec_registry_authoring_discipline()` structural precedent L239-L283 + govML v2.8.0+ `k_register_present_gate.sh` 231L skeleton (verbatim mirrored per H6 metric) |
| **Architectural choice** | TWO-surface gate authoring with reference-by-shim install_hook (Cycle-14-S9 architectural choice (b) extended). Gate scripts live ONLY at govML canonical `scripts/`; install_hook layers OBLIGATION doc + empty JSONL sink at per-project `docs/` + `outputs/` only. ADDITIVE-APPEND per HC #45 (Cycle-15-S3 + Cycle-15-S7 + Cycle-16-S4 + **Cycle-16-S5** precedent class extended to 4 members) |
| **Primary mechanism family** | Structural enforcement at gate-fire boundary (consumer-side; cycle-close + session-close) complementing BE-B scaffolding-time install (authoring-side). Dual-surface DP#1 structural > behavioral; Cycle 16 PRIMARY spec-implementation gap closure mechanism INSTALLED at BOTH boundaries. |
| **Authority chain** | Cycle 16 SI ACTIVE 2026-05-27 (`a2f14d5`) + Amendments 27a/27b + Rex disposition (C) D-S2-1 + S3 D-S3-1 + S4 D-S4-1 + Rex back-port directive STANDING 2026-05-27 (4-repo paired commit) + kc-45 R1 PASS task-context dispatch authorization via Cycle-16-S5 Coach + dispatch substrate `~/Moonshots_Career_Thesis_v2/.claude/workspace/cycle_16_s5_be_c_dispatch_substrate.md` |

### §11.1 BE-C Pre-Conditions (rows 13-18)

| # | Pre-condition | How verified at runtime | Refusal behavior on FAIL |
|---|---|---|---|
| 13 | **BE-A + BE-B artifacts UNMODIFIED at cycle_16/** — BE-A §1-§3 LOCKED bodies + BE-B §10 LOCKED bodies at 3 docs/.md + `scripts/spec_registry_authoring.py` BE-B body unchanged | `git diff` against BE-B SHIPPED HEAD returns 0 line changes on §1-§10 line ranges of 3 docs; `git diff scripts/spec_registry_authoring.py` returns empty | halt-and-surface; refuse-on-missing-precondition per DP#44 + S132; do NOT route around |
| 14 | **SPARQL endpoint `http://localhost:3030/cycle6/sparql` reachable** for gate-fire dogfooding | `python3 -c "import urllib.request, urllib.parse; req=urllib.request.Request('http://localhost:3030/cycle6/sparql', data=urllib.parse.urlencode({'query':'ASK { ?s ?p ?o }'}).encode()); r=urllib.request.urlopen(req, timeout=5); assert r.status==200"` exits 0 | halt-and-surface as KT-6 substrate-viability candidate; gate scripts emit WARN-class verdict on Check 1 unreachability |
| 15 | **`k_register_present_gate.sh` skeleton at govML scripts/ UNMODIFIED** for H6 metric reference | `wc -l ~/ml-governance-templates/scripts/k_register_present_gate.sh` = 231L; `git -C ~/ml-governance-templates diff scripts/k_register_present_gate.sh` empty | halt-and-surface; H6 metric depends on skeleton stability; refuse-on-violation |
| 16 | **govML `~/ml-governance-templates/scripts/init_project.sh` writable** + `install_runtime_emit_substrate()` at L171-L209 + `install_spec_registry_authoring_discipline()` at L239-L283 ABSENT-MUTATION refused | `grep -c "^install_runtime_emit_substrate()" ~/ml-governance-templates/scripts/init_project.sh` = 1 AND `grep -c "^install_spec_registry_authoring_discipline()" ~/ml-governance-templates/scripts/init_project.sh` = 1 | halt-and-surface (Refuse trigger (a) or (b) per dispatch substrate §7); BE-C BUILD does NOT proceed |
| 17 | **govML `~/ml-governance-templates/scripts/check_all_gates.sh` L2042-L2069 build-class branch 4-gate BLOCKING loop intact** for ADDITIVE 5th-gate append | `grep -c "for gate in hc26_internal_smoke_gate k_register_present_gate" ~/ml-governance-templates/scripts/check_all_gates.sh` ≥1 pre-edit | halt-and-surface (Refuse trigger (f)) |
| 18 | **govML `templates/build/` writable** for NEW `spec_implementation_gates/` directory creation | `test -w ~/ml-governance-templates/templates/build/` exits 0 + `mkdir -p ~/ml-governance-templates/templates/build/spec_implementation_gates` succeeds | halt-and-surface as govML write-permission blocker |

### §11.2 BE-C Post-Conditions (rows 13-18)

| # | Post-condition | How verified after run | What ACCEPTANCE_CRITERIA §11.1 measures against |
|---|---|---|---|
| 13 | **`scripts/spec_implementation_present_gate.sh` EXISTS + EXECUTABLE + BASH-SYNTAX-CLEAN + `--help` clean exit** at govML canonical scripts/ | `bash -n ~/ml-governance-templates/scripts/spec_implementation_present_gate.sh && test -x ~/ml-governance-templates/scripts/spec_implementation_present_gate.sh && bash ~/ml-governance-templates/scripts/spec_implementation_present_gate.sh --help \| head -1` exits 0 | ACCEPTANCE_CRITERIA §11.1 row 13 syntax + executable + help threshold |
| 14 | **`scripts/spec_implementation_session_close_gate.sh` EXISTS + EXECUTABLE + BASH-SYNTAX-CLEAN + `--help` clean exit** with ADVISORY=true default | `bash -n ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh && test -x ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh && bash ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh --help \| head -1` exits 0 + `grep -c "^ADVISORY=true" ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` = 1 | ACCEPTANCE_CRITERIA §11.1 row 14 syntax + executable + help + advisory-default threshold |
| 15 | **`check_all_gates.sh` BLOCKING loop extended + ADVISORY loop NEW** — `for gate in ... spec_implementation_present_gate; do` present + `for gate in spec_implementation_session_close_gate; do ... --advisory-mode ...` present | `grep -c "spec_implementation_present_gate" ~/ml-governance-templates/scripts/check_all_gates.sh` ≥1 AND `grep -c "spec_implementation_session_close_gate" ~/ml-governance-templates/scripts/check_all_gates.sh` ≥1 AND existing 4-gate iteration list body unchanged (PASS/FAIL accumulators) | ACCEPTANCE_CRITERIA §11.1 row 15 ADDITIVE-APPEND threshold |
| 16 | **govML `init_project.sh` install_hook ADDITIVE-APPEND landed** — NEW `install_spec_implementation_gates()` function present + NEW call site at research-build profile branch AFTER `install_spec_registry_authoring_discipline` + existing functions unchanged | `grep -c "^install_spec_implementation_gates()" ~/ml-governance-templates/scripts/init_project.sh` = 1 + `grep -c "^        install_spec_implementation_gates$" ~/ml-governance-templates/scripts/init_project.sh` = 1 + `grep -c "^install_runtime_emit_substrate()" ~/ml-governance-templates/scripts/init_project.sh` = 1 (unchanged) + `grep -c "^install_spec_registry_authoring_discipline()" ~/ml-governance-templates/scripts/init_project.sh` = 1 (unchanged) | ACCEPTANCE_CRITERIA §11.1 row 16 ADDITIVE per HC #45 |
| 17 | **govML `templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` ships** with TWO-surface gate interface declared + HC-11 partition + authority chain | `test -f ~/ml-governance-templates/templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` exits 0 + grep tests for `## §1 TWO-surface gate inventory` + `## §6 HC-11 partition` | ACCEPTANCE_CRITERIA §11.1 row 17 file + content threshold |
| 18 | **3-test-bed dogfooding to PRODUCTION /cycle6 PASSES** — TB-1 conforming-running CLEAR / TB-2 dormant-with-explicit-deferral-and-rex-authorization CLEAR / TB-3 dormant-silent-past-threshold BLOCKING-FAIL (load-bearing) + spec_implementation_gates_events.jsonl ≥4 fire.event rows | `outputs/cross_system_validation_be_c.json` `all_3_pass: true` + per-TB verdict + JSONL `grep -c spec_implementation_present_gate.fire.event` ≥3 + `grep -c spec_implementation_session_close_gate.fire.event` ≥3 | ACCEPTANCE_CRITERIA §11.1 row 18 3-TB threshold + H6 + KT-4 firing surface evaluation |

### §11.3 BE-C Invariants (rows 10-13)

| # | Invariant | When checked | If violated |
|---|---|---|---|
| 10 | **SPARQL endpoint reachability per check OR skip-WARN** — gate scripts probe `$CYCLE6_QUERY_ENDPOINT` (default `http://localhost:3030/cycle6/sparql`) at Check 1; if HTTP non-200 OR timeout → WARN-class verdict + downstream Checks SKIP | At every gate-script invocation | halt-and-surface as KT-6 substrate-viability candidate per dispatch substrate §7 refuse trigger (d); gate scripts emit fire.event with `ask_http_status: 0` for downstream forensics |
| 11 | **Skeleton structural equivalence to `k_register_present_gate.sh` per H6 metric** — `set -euo pipefail` + while-loop arg-parse + DIR/ADVISORY init + `--help` block + governance.yaml profile-build check + skip-WARN JSON + `add_check()` helper + PASS/FAIL/WARN accumulators + verdict block + `mkdir -p outputs` + JSON writer + `exit $EXIT_CODE` | At gate-script authoring close + at any re-edit | H6 REFUTED → KT-4 fires → paradigm-class candidate per dispatch substrate §3 + ED §Field 6 KT-4 |
| 12 | **4-class verdict enum** per gate: `CLEAR / BLOCKED / ADVISORY_FAIL / SKIP_NON_BUILD_PROFILE` | At every gate-script invocation output JSON `verdict` field | halt-and-surface; verdict outside enum is contract violation requiring CONTRACT_CHANGE per Binding 7 |
| 13 | **`check_all_gates.sh` integration line present** — 5-gate BLOCKING iteration list contains `spec_implementation_present_gate` AND ADVISORY loop contains `spec_implementation_session_close_gate` invoked with `--advisory-mode` explicit | At post-edit verification + at every `check_all_gates.sh` invocation against build-class project | halt-and-surface; missing integration = F-D Discoverability sub-mechanism layer violation per RIDE ED L426-L434 |

### §11.4 BE-C Side Effects (diff vs §10)

| Surface | NEW effect at BE-C | Bounds |
|---|---|---|
| Filesystem writes | NEW: `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` (~325L) + `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` (~337L) + `~/ml-governance-templates/templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` (~8KB) + `outputs/cross_system_validation_be_c.json` (NEW); EDITS to govML `init_project.sh` (+44L additive function + 1L call-site) + `check_all_gates.sh` (+16/-2 iteration list extension + NEW ADVISORY loop; LOCKED 4-gate loop body preserved) + govML `VERSION` (+148L v2.8.4 head prepend); §11 BE-C appends at 3 cycle_16 docs (Edit-per-section); DEPLOYMENT_LOG + BUILD_DECISION_LOG §3 row 3 appends; `outputs/spec_implementation_gates_events.jsonl` NEW + `outputs/build_runner_events.jsonl` append-only growth | ≤200KB cumulative new content; no existing-file body modifications outside §11 appends + init_project.sh additive function/call-site + check_all_gates.sh additive iteration extension + VERSION head prepend |
| Database writes | NEW: SPARQL UPDATE INSERT DATA via BE-B `register_spec()` against PRODUCTION /cycle6 graphs for 3 BE-C dogfooding specs (TB-1 + TB-2 + TB-3); DROP GRAPH cleanup at smoke close per dispatch substrate §4 (analog to BE-A test-graph cleanup discipline; production graph baseline pre/post equal verified via SPARQL COUNT) | 3 specs × ~13-15 triples × 3 named graphs each = ~120 triples written then DROPped; production graph baseline pre/post COUNT-equal post-cleanup |
| Network egress | localhost-only Fuseki HTTP via Python urllib (BE-B wrapper + 2 NEW gate scripts) | ≤40 localhost HTTP requests across BE-C execution (3 writes × 2 ops + 2 gates × 3 TB × 2 checks + readbacks + smoke verifies + DROP GRAPH cleanup × 3) |
| Process / thread footprint | python3 subprocess for wrapper invocations + 2 gate scripts via bash + urllib | ≤3 concurrent python3 invocations; ≤30s wall-clock per invocation; gate scripts ≤10s |

### §11.5 BE-C Versioning and Promotion Hooks

| Field | Value |
|---|---|
| **Version scheme** | Gate scripts declare no semver yet; promote alongside Cycle 17+ retroactive-scan dispatchees that consume BE-C gates |
| **govML version** | v2.8.3 → v2.8.4 (Cycle-16-S5 BE-C paired commit; entry at `~/ml-governance-templates/VERSION` head) |
| **Promotion authority** | build-runner BUILT at BE-C (Cycle-16-S5) → Coach R3 evaluation → build-orchestrator promotion at Cycle 17+ consumer integration OR Cycle-16-S6 BE-D retroactive scan consumer integration → Rex paradigm ruling required on CONTRACT_CHANGE OR KT-N firing |
| **Promotion gates** | `build_pipeline_gate.sh` + `production_deployment_gate.sh` + `cross_system_validation_gate.sh` + `hc26_internal_smoke_gate.sh` (BE-C inherits BE-A/B gate stack) + NEW at BE-C: `spec_implementation_present_gate.sh` (Op 3) + `spec_implementation_session_close_gate.sh` (Op 4) — BE-C is the consumer **and** the artifact for the NEW gates |
| **Rollback procedure** | (1) `git -C ~/ml-governance-templates reset --hard HEAD~1` (govML v2.8.4 revert per pre-paired-commit baseline; 5 files affected: VERSION + 2 NEW gate scripts + init_project.sh + check_all_gates.sh + NEW templates dir); (2) DROP GRAPH cleanup at smoke close already performed (no production triples remain post-smoke); (3) `git -C ~/cycle_16_close_spec_to_implementation_gap_build checkout docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md` (revert §11 appends); (4) `rm cycle_16/outputs/cross_system_validation_be_c.json cycle_16/outputs/spec_implementation_gates_events.jsonl`; (5) `git -C ~/cycle_6_unified_substrate_build diff runtime/jena/` returns empty (Cycle 6 LOCKED preserved throughout). Rollback NOT end-to-end tested at BE-C (DROP GRAPH cleanup IS end-to-end tested at smoke close; full rollback test deferred to Cycle 17+ if Coach R3 disposition requires) |

### §11.6 BE-C Change Control Triggers

- BE-C 9-deliverable scope per dispatch substrate §1 — any deviation from declared scope is CONTRACT_CHANGE per Binding 7 + S155
- govML v2.8.4 install_hook signature changes (function name `install_spec_implementation_gates`, target paths under `${DOCS_DIR}/` + `${PROJECT_DIR}/outputs/`, idempotence) — Rex paradigm ruling required
- SPARQL ASK predicate body changes (Operation 3 or Operation 4 ASK structure) — affects H6 metric + KT-4 firing surface; CONTRACT_CHANGE required
- CYCLE_N resolution chain changes (governance.yaml → state.json → fallback JSONL) — affects per-project gate firing semantics; CONTRACT_CHANGE required
- SESSIONS_BETWEEN primitive implementation changes (grep-based shell pre-computation) — affects Operation 4 threshold semantics; CONTRACT_CHANGE required
- 4-class verdict enum changes (CLEAR / BLOCKED / ADVISORY_FAIL / SKIP_NON_BUILD_PROFILE) — affects JSONL emit schema + check_all_gates.sh accumulator semantics; CONTRACT_CHANGE required

CONTRACT_CHANGE authority = Rex paradigm ruling per Binding 7 + S155 + BUILD_DECISION_LOG §4 verbatim.

### §11.7 BE-C Self-test (BEFORE shipping)

| # | Check | Status |
|---|---|---|
| 1 | TWO gate scripts present at govML canonical scripts/ + executable + bash-syntax-clean + --help exits 0 | [x] PASS (`bash -n` exit 0 on both; chmod +x applied; --help returns first line cleanly) |
| 2 | check_all_gates.sh BLOCKING loop extended to 5 gates (4th-original-gate iteration body unchanged; PASS/FAIL accumulators preserved) + ADVISORY loop NEW appended after BLOCKING | [x] PASS (grep counts match; iteration body verified preserved via `git diff` showing only iteration list line + comment header replaced) |
| 3 | govML init_project.sh install_hook function added + call-site added + bash-syntax-clean + ADDITIVE per HC #45 (no modification of existing functions) | [x] PASS (`grep -c install_spec_implementation_gates()` returns 2 — function def + call-site; `bash -n` exit 0; install_runtime_emit_substrate count unchanged at 1; install_spec_registry_authoring_discipline count unchanged at 1) |
| 4 | govML templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md present | [x] PASS (file at canonical path; HC-11 partition declared in §6) |
| 5 | govML VERSION bumped v2.8.3 → v2.8.4 with substantive entry | [x] PASS (head v2.8.4 entry present; v2.8.3 + v2.8.2 + v2.8.1 + v2.8.0 + v2.7.1 entries preserved below) |
| 6 | 3-TB dogfooding via BE-B wrapper authors 3 specs at PRODUCTION /cycle6 → 2 NEW gates fire ≥6 fire.event rows → expected verdicts captured per TB | [x] PASS (TB-1 CLEAR + TB-2 CLEAR + TB-3 BLOCKING-FAIL; `outputs/cross_system_validation_be_c.json` `all_3_pass=true`; `outputs/spec_implementation_gates_events.jsonl` ≥6 rows from 3 TB × 2 gates) |
| 7 | Fresh-scaffold smoke test confirms install_hook lands OBLIGATION + JSONL sink (per-project layer) + 3 prior installs still operational | [x] PASS (`/tmp/be_c_smoke_<ts>/` ships docs/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md + outputs/spec_implementation_gates_events.jsonl + 5 prior install outputs all present) |
| 8 | BE-A §1-§3 LOCKED + BE-B §10 LOCKED bodies UNMODIFIED across 5 BE-A/BE-B artifacts | [x] PASS (Edit-per-section; only §11 appended; pre-write canonical-marker baseline preserved post-edit) |
| 9 | Cycle 6 LOCKED ontology body UNMODIFIED throughout BE-C | [x] PASS (`git -C ~/cycle_6_unified_substrate_build diff runtime/jena/ \| wc -l` = 0 pre + post BE-C) |
| 10 | HC-11 partition preserved (publishable: TWO-surface gate interface + cycle-close/session-close semantic + --advisory-mode/--blocking-mode conventions + 4-class verdict enum + JSONL emit schema + integration shape; ip-private: SPARQL ASK predicate body algorithm + FILTER variable-substitution + SESSIONS_BETWEEN internals + per-role checklists at govML internal-only paths) | [x] PASS (OBLIGATION doc §6 declares partition; project gitignored at root; explicit publishable annotations) |

<!-- /gate:artifact_contract §11 -->

## §12 BE-D H1 H3 Cycle 16 Branch 4.4 BE-C-source Retroactive Scan Append

<!-- gate:artifact_contract §12 required -->

Per Cycle-16-S6 BE-D dispatch substrate §1 + §4 ARTIFACT_CONTRACT fill instructions + Cycle 14 §12 BE#6 multi-BE append precedent. APPEND-only; §0-§7 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) unchanged. Cycle 16 BE-D one-time within-cycle retroactive scan + 4-spec-class enumeration + 5-state classification + per-spec materialization at `/cycle6` (Branch 4.4 BE-C-source closure per ROADMAP Phase 5). NO govML back-port at BE-D per work-host boundary discipline.

### §12.0 BE-D Cycle 16 Branch 4.4 Contract Identity

| Field | Value |
|---|---|
| **Artifact** | `~/cycle_16_close_spec_to_implementation_gap_build/outputs/retroactive_scan_cycle_1_15_run.json` (~190KB; aggregate counts + per-spec evidence trail + H1 + H3 + KT-2 verdicts + HC-BE-D-1 honest carry) + per-spec materialization at `/cycle6` via BE-B `scripts/spec_registry_authoring.py register_spec()` invocation with `retroactive_classification=true` annotation (268 raw writes; 232 distinct after idempotent minting; 235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 persisted) + `outputs/build_runner_events.jsonl` append with `retroactive_scan_run.event` single-fire NEW event class + `outputs/spec_registry_events.jsonl` append-only growth (268 `spec_registry.write.event` rows) + §12 BE-D appends at 3 cycle_16 docs (Edit-per-section) + DEPLOYMENT_LOG §2 row 4 + BUILD_DECISION_LOG §2 row 4 + `outputs/build_runner_envelope.yaml` OVERWRITE |
| **Cycle** | 16 (BE-D Branch 4.4 BE-C-source closure per ROADMAP Phase 5 + Done #8 + H1 + H3 + KT-2 firing surface evaluation; one-time within-cycle artifact) |
| **Source** | BE-C SHIPPED at Cycle-16-S5 close: TWO-surface BLOCKING gate (`scripts/spec_implementation_present_gate.sh` 325L + `scripts/spec_implementation_session_close_gate.sh` 337L) at govML v2.8.4 + BE-B `scripts/spec_registry_authoring.py register_spec()` (5 Ops + DP#26 carve-out enforcement) + BE-A 14-field schema at `/cycle6` (HTTP 200 SPARQL endpoint reachable; verified pre-BE-D) + Cycle 1-15 cycle directories (16 directories under `~/cycle_*` enumerated; cycle_1 absent by design — Moonshots root is the C1 wrapper; 15 cycle dirs verified per substrate §7 refuse trigger (e)) + 23 outputs/*_events.jsonl files across cycles for runtime emit firing evidence + 26 FINDINGS.md files (15 cycles + docs/ duplicates) for methodology commitment tokens |
| **Architectural choice** | Retroactive enumeration via 4-spec-class scan + 5-state classification heuristic (resolution preference: structural runtime emit > citation evidence > deferral edge > retraction ADR > dormant-silent default). Per-spec materialization via BE-B authoring wrapper (NOT direct SPARQL UPDATE) preserves single-source-of-truth registry-write boundary. `retroactive_classification=true` annotation per spec write per ROADMAP §4.2 dependency 2 (audit-trail discipline for authoring-discipline gate bypass). NO DROP GRAPH at BE-D close — these are canonical retroactive registry rows persistent for BE-E forward-apply observation. NO govML back-port — one-time cycle-local artifact per work-host boundary discipline. |
| **Primary mechanism family** | Inventory-class enumeration completing the historical gap-fill that BE-A+B+C structural-enforcement closes forward. BE-A schema + BE-B authoring discipline + BE-C TWO-surface gate close the in-registry dormancy gap forward; BE-D fills the historical registry by enumeration. HC-BE-D-1 write-boundary enforcement gap remains as Cycle 18 scope per Rex Option B split-sequential disposition. |
| **Authority chain** | Cycle 16 SI ACTIVE 2026-05-27 (`a2f14d5`) + Amendments 27a (`be54a97`) + 27b (`badd749`) + Rex disposition (C) D-S2-1 + S3 D-S3-1 + S4 D-S4-1 + S5 D-S5-1 + Rex 2026-05-27 Option A (Cycle 16 narrow; HC-BE-D-1 → Cycle 18 scope) + kc-46 R1 PASS task-context dispatch authorization via Cycle-16-S6 Coach + dispatch substrate `~/Moonshots_Career_Thesis_v2/.claude/workspace/cycle_16_s6_be_d_dispatch_substrate.md` |

### §12.1 BE-D Pre-Conditions (rows 19-24)

| # | Pre-condition | How verified at runtime | Refusal behavior on FAIL |
|---|---|---|---|
| 19 | **BE-A + BE-B + BE-C artifacts UNMODIFIED at cycle_16/** — BE-A §1-§3 LOCKED + BE-B §10 LOCKED + BE-C §11 LOCKED bodies at 3 docs/.md + BE-B `scripts/spec_registry_authoring.py` BE-B body unchanged + BE-C 2 gate scripts at govML scripts/ unchanged | `git diff` against BE-C SHIPPED HEAD `1d61632` returns 0 line changes on §1-§11 line ranges of 3 docs; `git diff scripts/spec_registry_authoring.py` returns empty; `git -C ~/ml-governance-templates diff scripts/spec_implementation_*_gate.sh` returns empty | halt-and-surface; refuse-on-missing-precondition per DP#44 + S132; do NOT route around |
| 20 | **SPARQL endpoint `http://localhost:3030/cycle6/sparql` reachable** for retroactive per-spec materialization writes | `python3 -c "import urllib.request, urllib.parse; req=urllib.request.Request('http://localhost:3030/cycle6/sparql?query=' + urllib.parse.quote('SELECT (COUNT(*) AS ?c) WHERE {?s ?p ?o}')); r=urllib.request.urlopen(req, timeout=5); assert r.status==200"` exits 0 | halt-and-surface as KT-6 substrate-viability candidate per dispatch substrate §7 refuse trigger (d) |
| 21 | **15 cycle directories at `~/cycle_*` enumerable** for 4-spec-class scan across Cycles 1-15 | `ls -d ~/cycle_*/ \| wc -l` returns 16 (cycle_1 wrapper at Moonshots root + 15 explicit cycle dirs) | halt-and-surface per substrate §7 refuse trigger (e); BE-D BUILD does NOT proceed |
| 22 | **`.claude/agents/*.md` enumeration non-empty** for Class (a) agent contract scan | `ls ~/Moonshots_Career_Thesis_v2/.claude/agents/*.md \| wc -l` returns 9 | halt-and-surface per substrate §7 refuse trigger (f) |
| 23 | **BE-B `register_spec()` accepts `retroactive_classification=true` annotation as additional optional field** without rejecting on enum-violation | smoke test: 1 retroactive AgentContract write succeeds + readback OK + 14-field schema accepts retroactive annotation; verified at BE-D pre-bulk smoke 2026-05-27 | halt-and-surface; route to BE-B amendment per CONTRACT_CHANGE Binding 7 |
| 24 | **DP#26 carve-out at BE-B wrapper for `runtime_emit_event_class='n/a'` literals** with `n_a_rationale` field required — methodology commitments + dormant-silent agent contracts + cycle_10 schemas all activate this enforcement | `register_spec()` raises ValueError with `dp26_n_a_rationale_missing` refusal class on missing n_a_rationale; verified at BE-D 8 initial failures + 8 retry successes with explicit rationale | halt-and-surface; DP#26 enforcement is structural per HR §3d |

### §12.2 BE-D Post-Conditions (rows 19-24)

| # | Post-condition | How verified after run | What ACCEPTANCE_CRITERIA §12.1 measures against |
|---|---|---|---|
| 19 | **`outputs/retroactive_scan_cycle_1_15_run.json` EXISTS + JSON-PARSEABLE + SCHEMA-CONFORMING** per substrate §1.1 (aggregate_counts + per_spec_evidence + h1_total_enumerated + h1_estimate_floor + h1_confirmed_bool + kt_2_firing_surface + h3_dormant_silent_aggregate + h3_confirmed_bool + retroactive_classification_annotation + baseline_pre/post + timestamp) | `python3 -c "import json; d=json.load(open('outputs/retroactive_scan_cycle_1_15_run.json')); assert 'aggregate_counts_4x5' in d and 'h1_confirmed_bool' in d and 'kt_2_firing_surface' in d"` exits 0 | ACCEPTANCE_CRITERIA §12.1 row 19 file presence + JSON validity + 8 required top-level keys threshold |
| 20 | **4-spec-class enumeration produces 4 non-empty class entries** in `aggregate_counts_4x5` per substrate §1.2 + ROADMAP §4.1 task 1 exact commands; each class has per-state breakdown + per-class strengthening n≥3 outcomes | per substrate §1.1 schema row count = 4 (a/b/c/d) + TOTAL aggregator; per-class `total_distinct ≥ 3` (BE-D outcomes: a=9, b=10, c=154, d=59) | ACCEPTANCE_CRITERIA §12.1 row 20 per-class n≥3 strengthening threshold |
| 21 | **5-state taxonomy classification produces ≥3 dormant-silent specs** (H3 CONFIRMED + KT-2 DOES NOT FIRE per substrate §3) | `outputs/retroactive_scan_cycle_1_15_run.json`.`aggregate_counts_4x5.TOTAL.dormant-silent` ≥ 3; BE-D actual: 137 | ACCEPTANCE_CRITERIA §12.1 row 21 H3 + KT-2 threshold |
| 22 | **H1 total enumerated count ≥ 90 floor** (CONFIRMED per substrate §3 H1 metric) | `outputs/retroactive_scan_cycle_1_15_run.json`.`h1_total_enumerated` ≥ 90; BE-D actual: 232 distinct after idempotent minting (268 raw) | ACCEPTANCE_CRITERIA §12.1 row 22 H1 threshold |
| 23 | **Per-spec materialization at `/cycle6` via BE-B wrapper succeeds for all enumerated specs** (268 raw writes; 232 distinct via idempotent sha256_8 minting) + `retroactive_classification=true` annotation present per write | SPARQL COUNT cycle16:Spec at `/cycle6` = 235 (= 232 BE-D + 3 BE-B S4 persisted); per-write http_status=200 OR 204 verified across `outputs/spec_registry_events.jsonl` `spec_registry.write.event` rows | ACCEPTANCE_CRITERIA §12.1 row 23 materialization threshold + idempotency invariant |
| 24 | **`outputs/build_runner_events.jsonl` includes single `retroactive_scan_run.event` at BE-D close** with payload `{aggregate_counts, h1_confirmed_bool, h3_confirmed_bool, kt_2_fires_bool, timestamp}` per RUNTIME_EMIT_SPEC §12 NEW event class spec | `grep -c "retroactive_scan_run.event" outputs/build_runner_events.jsonl` = 1; JSON parse succeeds on the event payload | ACCEPTANCE_CRITERIA §12.1 row 24 single-fire NEW event class threshold |

### §12.3 BE-D Invariants (rows 14-17)

| # | Invariant | When checked | If violated |
|---|---|---|---|
| 14 | **NO DROP GRAPH at BE-D close** — retroactive registry rows persist for BE-E forward-apply observation (unlike BE-A/B/C smoke specs); SPARQL DELETE WHERE NOT invoked on cycle16:spec_retroactive_* IRIs | At BE-D close + at every BE-D session re-run | halt-and-surface; deleting retroactive rows invalidates BE-E forward-apply observation baseline |
| 15 | **Deterministic + idempotent spec_id minting** per substrate §2 — `cycle16:spec_retroactive_<sha256_8_chars_of_audit_tuple>`; re-running scan with same audit tuples produces same spec_iris (verified empirically: 268 raw writes → 232 distinct + 36 collision-excess on duplicate audit_tuples; SPARQL INSERT DATA on duplicate IRI is idempotent — same triples re-asserted, no schema violation) | At every retroactive write batch; pre-write spec_id derivation step | CONTRACT_CHANGE per Binding 7 — idempotency is BE-D primary invariant; non-deterministic minting breaks BE-E forward-apply baseline reconstruction |
| 16 | **`retroactive_classification=true` annotation present on every BE-D-written spec** — BE-B wrapper accepts the annotation as additional optional field; ROADMAP §4.2 dependency 2 (audit-trail discipline for authoring-discipline gate bypass) | At every register_spec() invocation within BE-D scope | halt-and-surface as audit-trail violation; retroactive writes without annotation conflate with forward-applied BE-E writes |
| 17 | **NO govML back-port at BE-D** — work-host boundary discipline; BE-D is one-time within-cycle artifact; 3-repo paired commit (cycle_16 + EMABS + Moonshots) at S6 close; govML UNTOUCHED | At BE-D close + at 3-repo paired commit | halt-and-surface; govML mutation at BE-D scope violates work-host boundary per dispatch substrate §0 (line 7) and §9 (NO govML at BE-D) |

### §12.4 BE-D Side Effects (diff vs §11)

| Surface | NEW effect at BE-D | Bounds |
|---|---|---|
| Filesystem writes | NEW: `outputs/retroactive_scan_cycle_1_15_run.json` (~190KB; aggregate + per-spec evidence + H1 + H3 + KT-2 verdicts + HC-BE-D-1 honest carry); EDITS to 3 cycle_16 docs §12 BE-D appends (Edit-per-section; LOCKED §1-§11 preserved); EDITS to DEPLOYMENT_LOG §2 row 4 + BUILD_DECISION_LOG §2 row 4 (append-only); `outputs/build_runner_envelope.yaml` OVERWRITE (BE-C → BE-D envelope); `outputs/spec_registry_events.jsonl` append-only growth (268 spec_registry.write.event rows during BE-D bulk; 8 dp26_shacl_refusal events from initial failures + 8 retry write events); `outputs/build_runner_events.jsonl` append-only growth (1 session.start + 1 dispatch.received + 1 retroactive_scan_run.event + Step-N phase events) | ≤300KB cumulative new content at cycle_16/; no existing-file body modifications outside §12 appends + DEPLOYMENT/BUILD_DECISION row 4 append + envelope overwrite |
| Database writes | NEW: 268 SPARQL UPDATE INSERT DATA via BE-B `register_spec()` against PRODUCTION `/cycle6` graphs (assertion + provenance + publicationInfo per nanopub 3-graph pattern); 232 distinct spec_iris after idempotent minting (36 collisions resolved by INSERT-DATA idempotency); NO DROP GRAPH at close (persist for BE-E) | 232 distinct cycle16:Spec instances written; production graph baseline pre-BE-D = 6 triples in default + 246101 across named graphs; post-BE-D = ~250779 total triples (~4680 net add for 232 specs × ~20 triples each / 3 graphs) |
| Network egress | localhost-only Fuseki HTTP via Python urllib (BE-B wrapper batch invocations) | 268 writes × ~200ms each ≈ 52s wall-clock; readback queries during HC #26 verification ~10 add'l ops |
| Process / thread footprint | python3 subprocess for wrapper invocations + retry batch + verification queries | ≤2 concurrent python3 invocations; ≤60s wall-clock cumulative; per-spec write ≤500ms |

### §12.5 BE-D Versioning and Promotion Hooks

| Field | Value |
|---|---|
| **Version scheme** | Retroactive scan output declares no semver; promote alongside BE-E forward-apply observation at Cycle-16-S7 consumer integration |
| **govML version** | UNCHANGED at v2.8.4 (BE-D is one-time within-cycle artifact; NO back-port per work-host boundary discipline per dispatch substrate §0 + §9) |
| **Promotion authority** | build-runner BUILT at BE-D (Cycle-16-S6) → Coach R3 evaluation → build-orchestrator promotion at Cycle-16-S7 BE-E forward-apply observation consumer integration → Rex paradigm ruling required on CONTRACT_CHANGE OR KT-2 firing |
| **Promotion gates** | BE-A/B/C gate stack inherited (`build_pipeline_gate.sh` + `production_deployment_gate.sh` + `cross_system_validation_gate.sh` + `hc26_internal_smoke_gate.sh` + `spec_implementation_present_gate.sh` + `spec_implementation_session_close_gate.sh`) — BE-D does NOT add new gates; the 6 dormant-silent cohorts at /cycle6 surface to BE-C cycle-close gate at next Cycle 17+ fire |
| **Rollback procedure** | NO DROP GRAPH at BE-D close per substrate §1 row 4. If full BE-D rollback required at Cycle 17+ retroactive: (1) `git -C ~/cycle_16_close_spec_to_implementation_gap_build checkout docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md` (revert §12 appends); (2) `rm cycle_16/outputs/retroactive_scan_cycle_1_15_run.json`; (3) SPARQL DELETE WHERE for all `cycle16:spec_retroactive_*` IRIs across 3 nanopub graphs (deterministic via spec_iri prefix match — 232 distinct + 3 BE-B persisted preserved by IRI-prefix discriminator); (4) cycle_6 LOCKED preserved throughout (verified at HC #26 Gate 3). Rollback NOT end-to-end tested at BE-D (BE-D is one-time; per-spec materialization is canonical, NOT smoke-test); full rollback test deferred to Cycle 17+ if Coach R3 disposition requires |

### §12.6 BE-D Change Control Triggers

- BE-D 10-deliverable scope per dispatch substrate §1 — any deviation from declared scope is CONTRACT_CHANGE per Binding 7 + S155
- 4-spec-class enumeration methodology changes (commands at ROADMAP §4.1 task 1) — affects H1 inventory + downstream BE-E forward-apply baseline; CONTRACT_CHANGE required
- 5-state taxonomy changes (running / dormant-with-explicit-deferral / dormant-silent / killed / long-running) — affects H3 + KT-2 firing surface evaluation; CONTRACT_CHANGE required
- Classification heuristic changes (resolution preference: runtime > citation > deferral > retraction > dormant-silent) — affects per-spec status assignment + H3 + KT-2 firing surface; CONTRACT_CHANGE required
- DP#26 carve-out semantics changes for methodology commitments (`runtime_emit_event_class='n/a — citation-based activation per DP#26'` + n_a_rationale required) — affects BE-B wrapper enforcement boundary + KT-3 firing surface; CONTRACT_CHANGE required per HR §3d
- HC-BE-D-1 write-boundary enforcement gap closure mechanism changes — affects Cycle 18 scope; CONTRACT_CHANGE required at Cycle 18 ED + ROADMAP authoring
- Spec_id minting algorithm changes (`cycle16:spec_retroactive_<sha256_8_chars_of_audit_tuple>` deterministic + idempotent) — affects re-runnability + BE-E baseline reconstruction; CONTRACT_CHANGE required

CONTRACT_CHANGE authority = Rex paradigm ruling per Binding 7 + S155 + BUILD_DECISION_LOG §4 verbatim.

### §12.7 BE-D Self-test (BEFORE shipping)

| # | Check | Status |
|---|---|---|
| 1 | `outputs/retroactive_scan_cycle_1_15_run.json` present + JSON-parseable + 8 required top-level keys (aggregate_counts_4x5 + h1_total_enumerated + h1_estimate_floor + h1_confirmed_bool + kt_2_firing_surface + h3_dormant_silent_aggregate + h3_confirmed_bool + retroactive_classification_annotation) | [x] PASS (file 190KB; JSON parse OK; all required keys present + `per_spec_evidence_IP_PRIVATE` (HC-11 partition) + `enumeration_methodology` + `classification_heuristic` + `hc_be_d_1_honest_carry`) |
| 2 | 4-spec-class enumeration produces non-empty entries for a/b/c/d + per-class n≥3 strengthening | [x] PASS (a=9 distinct + b=10 distinct + c=154 distinct + d=59 distinct; all classes ≥3 threshold) |
| 3 | 5-state classification yields ≥3 dormant-silent specs (H3 CONFIRMED + KT-2 DOES NOT FIRE) | [x] PASS (dormant_silent=137; well above 3 threshold; HC #59 BINDING screen applied) |
| 4 | H1 total ≥ 90 floor (CONFIRMED) | [x] PASS (h1_total_enumerated=232 distinct; raw=268; CONFIRMED per substrate §3 H1 metric) |
| 5 | Per-spec materialization at `/cycle6` succeeds via BE-B register_spec() for all enumerated specs with `retroactive_classification=true` annotation | [x] PASS (268 raw writes; 232 distinct after idempotent minting; 235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 persisted; 8 initial DP#26 refusals → 8 retry successes with explicit n_a_rationale) |
| 6 | `retroactive_scan_run.event` NEW event class fires exactly once at BE-D close with required payload (aggregate_counts + h1_confirmed_bool + h3_confirmed_bool + kt_2_fires_bool + timestamp) | [x] PASS (`grep -c "retroactive_scan_run.event" outputs/build_runner_events.jsonl` = 1; payload contains all required fields per RUNTIME_EMIT_SPEC §12) |
| 7 | NO DROP GRAPH at BE-D close (retroactive rows persist for BE-E) | [x] PASS (no DELETE WHERE invoked on cycle16:spec_retroactive_* IRIs; SPARQL COUNT cycle16:Spec at /cycle6 = 235 stable post-BE-D close) |
| 8 | BE-A §1-§3 LOCKED + BE-B §10 LOCKED + BE-C §11 LOCKED bodies UNMODIFIED across 5 BE-A/BE-B/BE-C artifacts | [x] PASS (Edit-per-section; only §12 appended; `git diff` on §1-§11 line ranges of 3 docs = 0 line changes; canonical-marker baseline preserved post-edit) |
| 9 | govML v2.8.4 LOCKED UNMODIFIED throughout BE-D (`git -C ~/ml-governance-templates status -s` empty pre + post) | [x] PASS (NO govML back-port at BE-D per work-host boundary discipline; verified pre-write + post-write) |
| 10 | Cycle 6 LOCKED ontology body + Cycle 13/14/15-partial-close LOCKED bodies UNMODIFIED throughout BE-D | [x] PASS (`git -C ~/cycle_6_unified_substrate_build diff runtime/jena/ \| wc -l` = 0 pre + post BE-D) |
| 11 | HC-11 partition preserved (publishable: aggregate_counts_4x5 + 5-state taxonomy + H1/H3/KT-2 verdicts + per-class strengthening n≥3; ip-private: per_spec_evidence audit_tuple citations + retroactive classification audit trail) | [x] PASS (json explicit `hc_11_partition` section declares partition; `per_spec_evidence_IP_PRIVATE` array contains IP-PRIVATE citation tuples; project gitignored at root) |
| 12 | HC-BE-D-1 write-boundary enforcement gap surfaced as honest carry — state.json `honest_carries_open` prepend at S6 close (Coach scope); DECISION_LOG D-S6-1 row; §12 BE-D appends reference HC-BE-D-1 explicitly (this §12.0 + §12.4 + §12.5); S7 transition prompt + Cycle 16 close FINDINGS Layer 4 explicit gap section (Coach + future scope) | [x] PASS (HC-BE-D-1 surfaced at §12.0 mechanism family + §12.5 Versioning notes (rollback discriminator on cycle16:spec_retroactive_* prefix) + retroactive_scan_cycle_1_15_run.json `hc_be_d_1_honest_carry` block with Cycle 18 scope per Rex Option B split-sequential 2026-05-27) |

<!-- /gate:artifact_contract §12 -->

## §13 BE-E H8 Cycle 16 Branch 4.5 BE-D-source Forward-Apply Observation Append

<!-- gate:artifact_contract §13 required -->

Per Cycle-16-S7 BE-E dispatch substrate §1 + §4 ARTIFACT_CONTRACT fill instructions + Cycle 14 §12 BE#6 multi-BE append precedent. APPEND-only; §0-§7 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) + §12 (BE-D LOCKED `902f222`) unchanged. Cycle 16 BE-E forward-apply observation infrastructure: 2 NEW event classes (`spec_authoring_event` + `spec_implementation_event`) wired into `scripts/runtime_emit/emit.py` (additive; emit_event() core signature UNCHANGED per Cycle 10 §0 schema_version=0.1 LOCKED) + `docs/forward_apply_observation_protocol.md` NEW (8 sections; HC-11 partition declared inline) + smoke-test ≥4 events at `outputs/forward_apply_observation_events.jsonl` + govML v2.8.5 ADDITIVE-APPEND back-port (Branch 4.5 BE-D-source closure per ROADMAP Phase 6).

### §13.0 BE-E Cycle 16 Branch 4.5 Contract Identity

| Field | Value |
|---|---|
| **Artifact** | `~/cycle_16_close_spec_to_implementation_gap_build/scripts/runtime_emit/emit.py` ADDITIVE extension (2 NEW event class registration constants + `forward_apply_emit()` sink-routing helper; emit_event() core signature UNCHANGED) + `~/cycle_16_close_spec_to_implementation_gap_build/docs/forward_apply_observation_protocol.md` NEW (8 §N sections + 0 placeholders + HC-11 partition declared inline per Binding 8 BIND) + `~/cycle_16_close_spec_to_implementation_gap_build/outputs/forward_apply_observation_events.jsonl` NEW (sink-exists invariant + 4 smoke events emitted at BE-E close: 2 `spec_authoring_event` + 2 `spec_implementation_event` for TB-1 + TB-2 synthetic specs to test graph `<http://cycle16.local/test/be_e_smoke>` with PROV-O 4-typed-edges + HC-11 `c6:publishable` access_permission) + §13 BE-E appends at 3 cycle_16 docs (Edit-per-section) + DEPLOYMENT_LOG §2 row 5 + BUILD_DECISION_LOG §2 row 5 + `outputs/build_runner_envelope.yaml` OVERWRITE + `outputs/build_runner_events.jsonl` append with 1 `forward_apply_smoke.event` single-fire NEW event class + `outputs/spec_registry_events.jsonl` append with smoke-test write events (TB-1 + TB-2 synthetic, test-graph-scoped, DROP cleanup at smoke close) + govML v2.8.5 ADDITIVE-APPEND back-port (init_project.sh NEW `install_forward_apply_observation()` + templates/build/forward_apply_observation/ NEW dir + VERSION v2.8.5 + CHANGELOG v2.8.5 entry) |
| **Cycle** | 16 (BE-E Branch 4.5 BE-D-source closure per ROADMAP Phase 6 + Done #9 + H8 evaluation surface enabled + KT-5 firing surface evaluated at BE-E close per dispatch substrate §5; forward-apply observation infrastructure consumed across Cycle 17 → Cycle 18 longitudinal H8 verdict window) |
| **Source** | BE-D SHIPPED at Cycle-16-S6 close: `outputs/retroactive_scan_cycle_1_15_run.json` (232 distinct + 137 dormant-silent + H1 + H3 CONFIRMED + KT-2 DOES NOT FIRE; 4-spec-class × 5-state aggregate at /cycle6 as forward-apply baseline) + BE-C SHIPPED TWO-surface BLOCKING gate at govML v2.8.4 + BE-B SHIPPED `scripts/spec_registry_authoring.py register_spec()` consumed at every `spec_authoring_event` fire boundary + BE-A SHIPPED 14-field schema at `/cycle6` (HTTP 200 SPARQL endpoint verified pre-BE-E smoke; 6 default-graph triples baseline) + Cycle 10 BE#5 RUNTIME_EMIT_SPEC §3 refusal-on-violation inheritance + Cycle 6 BE#1 PROV-O 4-typed-edges contract + Cycle 15 BE#4 5-event baseline build_runner emit substrate |
| **Architectural choice** | 2 NEW event classes registered as named constants in emit.py + sink-routing helper `forward_apply_emit()` with BE-E namespace + sink defaults bound (refuses orphan event_class per RUNTIME_EMIT_SPEC §3); namespace-isolated from BE-A/B/C/D namespaces per Cycle 10 rule_6/8/10/12 invariants; sink path `outputs/forward_apply_observation_events.jsonl` separate from build_runner/spec_registry/spec_implementation_gates sinks per RUNTIME_EMIT_SPEC §4 append-only discipline. Smoke-test test-graph scoped DROP cleanup at close (canonical production registry rows persist; the 3 BE-B S4 + 232 BE-D rows preserved). NO HC-BE-D-1 write-boundary closure within BE-E (Cycle 18 scope per Rex 2026-05-27 Option B split-sequential). |
| **Primary mechanism family** | Forward-apply observation infrastructure completing the spec-implementation gap closure forward: BE-A schema + BE-B authoring wrapper + BE-C TWO-surface BLOCKING gate close the in-registry dormancy gap forward at write/gate boundaries; BE-D fills the historical registry by enumeration; BE-E adds observation hooks (`spec_authoring_event` at write boundary + `spec_implementation_event` at status-transition boundary) consumed by session-close + cycle-close hooks per `docs/forward_apply_observation_protocol.md` §2 + §3 (BE-E enables; Cycle 18 evaluates H8 longitudinal verdict). HC-BE-D-1 write-boundary enforcement gap remains as Cycle 18 scope per Rex Option B split-sequential disposition (BE-E inherits the same blind spot as BE-D — observes only BE-B-mediated path). |
| **Authority chain** | Cycle 16 SI ACTIVE 2026-05-27 (`a2f14d5`) + Amendments 27a (`be54a97`) + 27b (`badd749`) + Rex disposition (C) D-S2-1 + S3 D-S3-1 + S4 D-S4-1 + S5 D-S5-1 + S6 D-S6-1 + Rex 2026-05-27 Option A (Cycle 16 narrow; HC-BE-D-1 → Cycle 18 scope per Option B split-sequential) + kc-46 R1 PASS task-context dispatch authorization via Cycle-16-S7 Coach + dispatch substrate `~/Moonshots_Career_Thesis_v2/.claude/workspace/cycle_16_s7_be_e_dispatch_substrate.md` |

### §13.1 BE-E Pre-Conditions (rows 25-30)

| # | Pre-condition | How verified at runtime | Refusal behavior on FAIL |
|---|---|---|---|
| 25 | **BE-A + BE-B + BE-C + BE-D artifacts UNMODIFIED at cycle_16/** — BE-A §1-§3 LOCKED + BE-B §10 LOCKED + BE-C §11 LOCKED + BE-D §12 LOCKED bodies at 3 docs/.md + BE-B `scripts/spec_registry_authoring.py` BE-B body unchanged + BE-C 2 gate scripts at govML scripts/ unchanged + BE-D `outputs/retroactive_scan_cycle_1_15_run.json` unchanged | `git diff` against BE-D SHIPPED HEAD `902f222` returns 0 line changes on §1-§12 line ranges of 3 docs; `git diff scripts/spec_registry_authoring.py` returns empty; `git -C ~/ml-governance-templates diff scripts/spec_implementation_*_gate.sh` returns empty | halt-and-surface; refuse-on-missing-precondition per DP#44 + S132; do NOT route around |
| 26 | **SPARQL endpoint `http://localhost:3030/cycle6/sparql` reachable** for smoke-test write boundary + PROV-O typed-edge propagation verification + KT-5 evaluation query | `python3 -c "import urllib.request, urllib.parse; req=urllib.request.Request('http://localhost:3030/cycle6/sparql?query=' + urllib.parse.quote('SELECT (COUNT(*) AS ?c) WHERE {?s ?p ?o}')); r=urllib.request.urlopen(req, timeout=5); assert r.status==200"` exits 0 | halt-and-surface as KT-6 substrate-viability candidate per dispatch substrate §8 refusal anchor |
| 27 | **`scripts/runtime_emit/emit.py` present with `emit_event()` core signature at known def-site** (Cycle 15 BE#4 baseline; 175L; Path declared) | `grep -c '^def emit_event(' scripts/runtime_emit/emit.py` = 1; pre-extension byte count recorded for additive-diff verification | halt-and-surface; refuse-on-missing-precondition; emit.py is BE-E primary extension surface |
| 28 | **BE-D `outputs/retroactive_scan_cycle_1_15_run.json` present + readable** as forward-apply baseline (232 distinct + 137 dormant-silent inventory for KT-5 retroactive exclusion discrimination) | `test -f outputs/retroactive_scan_cycle_1_15_run.json && python3 -c "import json; d=json.load(open('outputs/retroactive_scan_cycle_1_15_run.json')); assert 'h3_dormant_silent_aggregate' in d"` exits 0 | halt-and-surface; BE-D baseline is structural precondition for BE-E forward-apply observation |
| 29 | **`outputs/forward_apply_observation_events.jsonl` sink writable at BE-E smoke-test boundary** (sink-exists invariant established at BE-E build step 4 via `touch` before first smoke emit; refuse-on-violation per RUNTIME_EMIT_SPEC §3 fires if absent) | `test -w outputs/forward_apply_observation_events.jsonl` exits 0; OR `touch outputs/forward_apply_observation_events.jsonl` succeeds | halt-and-surface; sink-unwritable surfaces upstream filesystem misconfiguration |
| 30 | **PROV-O 4-typed-edges contract honored at smoke-test fixture authoring** — every synthetic spec (TB-1 + TB-2) materialized at test graph carries `prov:wasGeneratedBy` + `prov:wasAttributedTo` + `prov:generatedAtTime` + `prov:wasInformedBy` triples per Cycle 6 BE#1 contract inheritance | SPARQL SELECT against test graph `<http://cycle16.local/test/be_e_smoke>` for the 4 prov:* predicates per smoke-test spec_iri returns ≥4 typed-edges per spec | halt-and-surface per BE-A §1 + Cycle 6 BE#1; PROV-O typed-edges are LOAD-BEARING for downstream provenance traceback |

### §13.2 BE-E Post-Conditions (rows 25-30)

| # | Post-condition | How verified after run | What ACCEPTANCE_CRITERIA §13.1 measures against |
|---|---|---|---|
| 25 | **`scripts/runtime_emit/emit.py` extended additively** — 2 NEW event class registration constants (`SPEC_AUTHORING_EVENT_CLASS` + `SPEC_IMPLEMENTATION_EVENT_CLASS`) + NEW sink-routing helper `forward_apply_emit()` + NEW namespace constant `FORWARD_APPLY_OBSERVATION_NAMESPACE` + NEW sink default `FORWARD_APPLY_OBSERVATION_SINK_DEFAULT`; `emit_event()` core signature UNCHANGED | `grep -c 'spec_authoring_event\|spec_implementation_event\|forward_apply_emit\|FORWARD_APPLY_OBSERVATION_' scripts/runtime_emit/emit.py` ≥ 5; existing `emit_event(` def-site `grep -c '^def emit_event('` = 1 (unchanged from baseline); `python3 -c "from emit import emit_event; import inspect; print(inspect.signature(emit_event))"` returns Cycle 15 BE#4 baseline signature | ACCEPTANCE_CRITERIA §13.1 row 25 additive-only invariant + signature-unchanged invariant |
| 26 | **`docs/forward_apply_observation_protocol.md` NEW** with 8 sections (§0 scope + §1 event-class taxonomy + §2 session-close hook + §3 cycle-close aggregate hook + §4 longitudinal verdict surface (Cycle 18 + KT-5 evaluation) + §5 refusal-on-violation discipline + §6 HC-11 partition + §7 self-test) + 0 placeholders + HC-11 partition declared inline | `wc -l docs/forward_apply_observation_protocol.md` in expected range (~140-220L); double-brace placeholder count = 0 via Check #23 grep; `grep -c '^## §' docs/forward_apply_observation_protocol.md` = 8 | ACCEPTANCE_CRITERIA §13.1 row 26 doc presence + section count + 0 placeholders |
| 27 | **`outputs/forward_apply_observation_events.jsonl` NEW sink with ≥4 fire.event rows** at BE-E smoke-test close (2 `spec_authoring_event` for TB-1 + TB-2 synthetic specs + 2 `spec_implementation_event` for TB-1 + TB-2 status transitions dormant-silent → running) with required payload fields per RUNTIME_EMIT_SPEC §13.1 | `wc -l outputs/forward_apply_observation_events.jsonl` ≥ 4; `jq -r '.event_class' outputs/forward_apply_observation_events.jsonl | sort -u` returns `[spec_authoring_event, spec_implementation_event]`; per-row payload field assertion succeeds | ACCEPTANCE_CRITERIA §13.1 row 27 smoke-test event count + class enumeration |
| 28 | **PROV-O 4-typed-edges per-spec verified at smoke-test** via SPARQL DESCRIBE against test graph `<http://cycle16.local/test/be_e_smoke>` for TB-1 + TB-2 synthetic specs | SPARQL SELECT against test graph per smoke-test spec_iri returns 4 prov:* predicates (`wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy`) per spec; DROP GRAPH cleanup at smoke close HTTP 200 + post-DROP COUNT = 0 verified | ACCEPTANCE_CRITERIA §13.1 row 28 PROV-O typed-edges threshold + DROP cleanup |
| 29 | **govML v2.8.5 ADDITIVE-APPEND back-port** at `~/ml-governance-templates/`: NEW `install_forward_apply_observation()` function in init_project.sh after `install_spec_implementation_gates()` (~L327) + templates/build/forward_apply_observation/ NEW dir (2 files: FORWARD_APPLY_OBSERVATION_OBLIGATION.md + forward_apply_observation_protocol.md) + VERSION v2.8.5 prepended (v2.8.4 header preserved verbatim) + CHANGELOG v2.8.5 entry; LOCKED bodies of `install_runtime_emit_substrate` + `install_spec_registry_authoring_discipline` + `install_spec_implementation_gates` UNMODIFIED (HC #45 ADDITIVE-APPEND chain extension to n=5) | `git -C ~/ml-governance-templates diff scripts/init_project.sh` shows ADDITIVE-ONLY at install_forward_apply_observation() body + L632 list extension; `git -C ~/ml-governance-templates diff scripts/init_project.sh -- '*install_runtime_emit_substrate*'` empty; VERSION grep for `v2.8.5` returns 1 line; CHANGELOG entry present | ACCEPTANCE_CRITERIA §13.1 row 29 govML 4-file ADDITIVE-APPEND verification |
| 30 | **KT-5 firing surface evaluated at BE-E close** per `forward_apply_observation_protocol.md` §4 + dispatch substrate §5 (count + verdict + window adequacy honest note) — DOES NOT FIRE expected per pre-S7 hypothesis; honest gap re mid-Cycle-16 observation window adequacy surfaced for Cycle 18 longitudinal H8 verdict | SPARQL query at `/cycle6` for Cycle-16-authored dormant-silent specs EXCLUDING BE-D retroactive (IRI-prefix discriminator `spec_retroactive_*` per BE-D §12.5 rollback discriminator); count + verdict recorded at envelope `kt_5_evaluation` block; HC #59 BINDING screen applied | ACCEPTANCE_CRITERIA §13.1 row 30 KT-5 evaluation + honest-gap surface |

### §13.3 BE-E Invariants (rows 18-21)

| # | Invariant | When checked | If violated |
|---|---|---|---|
| 18 | **`emit_event()` core signature UNCHANGED** per Cycle 10 §0 schema_version=0.1 LOCKED — extension adds NEW constants + helper but does NOT modify the canonical emit primitive contract | At BE-E close + at every `from emit import emit_event` consumer site | CONTRACT_CHANGE per Binding 7 — emit_event() is Cycle 10 BE#5 PRIMARY infrastructure inherited at Cycle 15 BE#4; signature change requires Rex paradigm ruling |
| 19 | **Namespace isolation** — BE-E namespace `cycle_16.be_e.forward_apply_observation` namespace-isolated from BE-A/B/C/D namespaces per Cycle 10 rule_6/8/10/12 invariants; sink path separate from build_runner/spec_registry/spec_implementation_gates sinks | At every `forward_apply_emit()` invocation; refuse on orphan event_class per emit.py guard | halt-and-surface; namespace contamination invalidates downstream SPARQL aggregations |
| 20 | **PROV-O 4-typed-edges propagation** per Cycle 6 BE#1 contract — every smoke-test spec materialized at test graph + every BE-E forward-apply event payload carries `wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy` | At every BE-E event emission + at smoke-test SPARQL DESCRIBE verification | halt-and-surface per BE-A §1; PROV-O typed-edges are LOAD-BEARING for downstream provenance traceback (Cycle 6 BE#1 cross-cycle contract) |
| 21 | **HC-BE-D-1 boundary discipline preserved** — BE-E does NOT attempt write-boundary enforcement closure (Cycle 18 scope per Rex 2026-05-27 Option B split-sequential); BE-E inherits the SAME blind spot as BE-D (observes only BE-B-mediated path) | At BE-E close + at envelope `hc_be_d_1_boundary_discipline_honest_acknowledgment` section | halt-and-surface; HC-BE-D-1 closure within BE-E scope is paradigm-class boundary violation per Rex Option A 2026-05-27 disposition |

### §13.4 BE-E Side Effects (diff vs §12)

| Surface | NEW effect at BE-E | Bounds |
|---|---|---|
| Filesystem writes | NEW: `docs/forward_apply_observation_protocol.md` (~20KB; 8 sections + HC-11 partition declared inline); EDITS to `scripts/runtime_emit/emit.py` (additive; 2 NEW constants + sink-routing helper + namespace constant + sink default; emit_event() core UNCHANGED); NEW: `outputs/forward_apply_observation_events.jsonl` sink (0B at scaffold; 4 smoke events at close); EDITS to 3 cycle_16 docs §13 BE-E appends (Edit-per-section; LOCKED §0-§12 preserved); EDITS to DEPLOYMENT_LOG §2 row 5 + BUILD_DECISION_LOG §2 row 5 (append-only); `outputs/build_runner_envelope.yaml` OVERWRITE (BE-D → BE-E envelope); `outputs/build_runner_events.jsonl` append (1 `forward_apply_smoke.event` single-fire NEW event class at BE-E close + Cycle 15 BE#4 5-event baseline class fires); `outputs/spec_registry_events.jsonl` append-only (smoke-test write events at test graph, DROP-cleaned at close) | ≤50KB cumulative new content at cycle_16/; no existing-file body modifications outside §13 appends + DEPLOYMENT/BUILD_DECISION row 5 append + envelope overwrite + emit.py additive extension |
| Database writes | NEW: smoke-test SPARQL INSERT DATA at test graph `<http://cycle16.local/test/be_e_smoke>` for 2 synthetic specs (TB-1 AgentContract + TB-2 Schema) with PROV-O 4-typed-edges + HC-11 `c6:publishable` access_permission + 14-field schema fill; DELETE + INSERT for status transition dormant-silent → running per spec; DROP GRAPH cleanup at BE-E smoke close (canonical production registry rows persist; the 3 BE-B S4 + 232 BE-D rows preserved) | 2 test-graph-scoped INSERT batches + 2 status transitions + 1 DROP GRAPH; production graph baseline pre/post EQUAL at BE-E close (test graph fully cleaned) |
| Network egress | localhost-only Fuseki HTTP via Python urllib (smoke-test invocations + KT-5 evaluation query) | ~6 SPARQL invocations × ~200ms each ≈ 1.2s wall-clock; HC #28 retry not required (single-shot smoke) |
| govML repo writes | NEW function `install_forward_apply_observation()` in `~/ml-governance-templates/scripts/init_project.sh` after `install_spec_implementation_gates()` (~L327); function added to build-profile dispatch list (~L632); NEW dir `~/ml-governance-templates/templates/build/forward_apply_observation/` with 2 files (FORWARD_APPLY_OBSERVATION_OBLIGATION.md + forward_apply_observation_protocol.md); VERSION v2.8.5 prepended (v2.8.4 header preserved verbatim); CHANGELOG v2.8.5 entry; LOCKED bodies of `install_runtime_emit_substrate` + `install_spec_registry_authoring_discipline` + `install_spec_implementation_gates` UNMODIFIED | 5 files modified at govML (init_project.sh + 2 NEW templates + VERSION + CHANGELOG); 0 deletions on existing 3 install function bodies; HC #45 ADDITIVE-APPEND chain extension to n=5 |
| Process / thread footprint | python3 subprocess for smoke-test (`/tmp/be_e_smoke_test.py` orchestrator) | ≤1 concurrent python3 invocation; ≤5s wall-clock cumulative; per-emit ≤50ms |

### §13.5 BE-E Versioning and Promotion Hooks

| Field | Value |
|---|---|
| **Version scheme** | BE-E forward-apply observation infrastructure declares no semver at cycle_16 surface; emit.py extension carried alongside BE-A/B/C/D atomic build; promote alongside BE-E at Cycle-16-S7 close paired commit |
| **govML version** | BUMP v2.8.4 → v2.8.5 (ADDITIVE-APPEND per HC #45 precedent class chain extension to n=5; LOCKED bodies of `install_runtime_emit_substrate` + `install_spec_registry_authoring_discipline` + `install_spec_implementation_gates` UNMODIFIED; NEW `install_forward_apply_observation()` function + NEW templates dir + VERSION + CHANGELOG ADDITIVE) |
| **Promotion authority** | build-runner BUILT at BE-E (Cycle-16-S7) → Coach R3 evaluation → build-orchestrator promotion at Cycle-16-S8 close FINDINGS authoring (ROADMAP Phase 7) → Rex paradigm ruling required on CONTRACT_CHANGE OR KT-5 firing |
| **Promotion gates** | BE-A/B/C/D gate stack inherited (`build_pipeline_gate.sh` + `production_deployment_gate.sh` + `cross_system_validation_gate.sh` + `hc26_internal_smoke_gate.sh` + `spec_implementation_present_gate.sh` + `spec_implementation_session_close_gate.sh`) — BE-E does NOT add new gates at scripts/ canonical layer; the observation infrastructure consumes existing BE-C TWO-surface gate at session-close + cycle-close hooks per `forward_apply_observation_protocol.md` §2 + §3 |
| **Rollback procedure** | If full BE-E rollback required: (1) `git -C ~/cycle_16_close_spec_to_implementation_gap_build checkout docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md scripts/runtime_emit/emit.py` (revert §13 appends + emit.py extension); (2) `rm docs/forward_apply_observation_protocol.md outputs/forward_apply_observation_events.jsonl`; (3) `git -C ~/ml-governance-templates checkout scripts/init_project.sh VERSION CHANGELOG.md && rm -rf templates/build/forward_apply_observation/` (revert govML v2.8.5 → v2.8.4); (4) NO production graph DROP required at /cycle6 (smoke-test test-graph DROP-cleaned at BE-E smoke close; canonical production rows untouched); (5) cycle_6 LOCKED preserved throughout (verified at HC #26 Gate 3). Rollback tested end-to-end via smoke-test DROP GRAPH (HTTP 200 verified at BE-E smoke close); full file-revert rollback NOT end-to-end tested at BE-E (defer to Cycle 17+ if Coach R3 disposition requires) |

### §13.6 BE-E Change Control Triggers

- BE-E 8-deliverable scope per dispatch substrate §1 — any deviation from declared scope is CONTRACT_CHANGE per Binding 7 + S155
- 2 NEW event class schema changes (`spec_authoring_event` + `spec_implementation_event` required/optional fields per RUNTIME_EMIT_SPEC §13.1) — affects forward-apply observation surface + Cycle 18 H8 longitudinal verdict; CONTRACT_CHANGE required
- ≤3-session dormancy threshold default per Amendment 2026-05-27a changes — affects spec_implementation_event firing window + session-close hook ADVISORY surface; CONTRACT_CHANGE required per Amendment 27a inheritance
- Namespace + sink path changes (`cycle_16.be_e.forward_apply_observation` + `outputs/forward_apply_observation_events.jsonl`) — affects cross-namespace SPARQL aggregations + session-close hook consumption; CONTRACT_CHANGE required per Cycle 10 namespace-isolation invariants
- HC-11 access_permission enum changes (`c6:publishable` + `c6:ip-private`) — affects per-edge HC-11 enforcement at smoke-test + BE-E event payload; CONTRACT_CHANGE required per BE-A §1
- PROV-O 4-typed-edges contract changes — affects Cycle 6 BE#1 cross-cycle inheritance contract; CONTRACT_CHANGE required at Cycle 6 BE#1 + cascade to BE-A + BE-B + BE-D + BE-E
- HC-BE-D-1 write-boundary enforcement gap closure mechanism changes — affects Cycle 18 scope; CONTRACT_CHANGE required at Cycle 18 ED + ROADMAP authoring (BE-E preserves HC-BE-D-1 boundary; do NOT attempt closure within BE-E scope)
- govML v2.8.5 ADDITIVE-APPEND framing changes (HC #45 chain extension to n=5) — affects scaffolding inheritance pattern for future BE-class additive-append cycles; CONTRACT_CHANGE required at HC #45 catalog

CONTRACT_CHANGE authority = Rex paradigm ruling per Binding 7 + S155 + BUILD_DECISION_LOG §4 verbatim.

### §13.7 BE-E Self-test (BEFORE shipping)

| # | Check | Status |
|---|---|---|
| 1 | `scripts/runtime_emit/emit.py` extended additively with 2 NEW event class constants + sink-routing helper + namespace/sink constants; `emit_event()` core signature UNCHANGED | [x] PASS (`grep -c 'SPEC_AUTHORING_EVENT_CLASS\|SPEC_IMPLEMENTATION_EVENT_CLASS\|forward_apply_emit' scripts/runtime_emit/emit.py` ≥ 4; `inspect.signature(emit_event)` returns Cycle 15 BE#4 baseline signature verified) |
| 2 | `docs/forward_apply_observation_protocol.md` NEW with 8 §N sections + 0 placeholders + HC-11 partition declared inline per Binding 8 | [x] PASS (`grep -c '^## §' docs/forward_apply_observation_protocol.md` = 8 covering §0-§7; double-brace placeholder count = 0 via Check #23 grep) |
| 3 | `outputs/forward_apply_observation_events.jsonl` NEW with ≥4 fire.event rows (2 `spec_authoring_event` + 2 `spec_implementation_event` for TB-1 + TB-2 synthetic specs) | [x] PASS (`wc -l outputs/forward_apply_observation_events.jsonl` = 4; class enumeration via `jq -r '.event_class'` returns both NEW classes) |
| 4 | PROV-O 4-typed-edges per-spec verified at smoke-test via SPARQL SELECT against test graph `<http://cycle16.local/test/be_e_smoke>` for TB-1 + TB-2 | [x] PASS (TB-1 + TB-2 each return 4 prov:* typed-edges: wasGeneratedBy + wasAttributedTo + generatedAtTime + wasInformedBy; verified at smoke-test 2026-05-27) |
| 5 | DROP GRAPH cleanup at smoke-test close — test graph triples post-DROP = 0; canonical production rows preserved | [x] PASS (`DROP GRAPH <http://cycle16.local/test/be_e_smoke>` HTTP 200; post-DROP COUNT = 0 verified; production registry untouched: 235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 persisted post-BE-E) |
| 6 | govML v2.8.5 ADDITIVE-APPEND back-port — 4 files (init_project.sh + 2 NEW templates + VERSION + CHANGELOG); LOCKED bodies of 3 existing install functions UNMODIFIED | [x] PASS (`install_forward_apply_observation` defined at init_project.sh after `install_spec_implementation_gates`; templates/build/forward_apply_observation/ NEW dir with 2 files; VERSION v2.8.5 line 1; CHANGELOG.md NEW with v2.8.5 entry; HC #45 chain extension to n=5 verified) |
| 7 | KT-5 firing surface evaluated at BE-E close per `forward_apply_observation_protocol.md` §4 + dispatch substrate §5 — DOES NOT FIRE expected; honest-gap re window adequacy surfaced | [x] PASS (SPARQL query at /cycle6 for Cycle-16-authored dormant-silent specs EXCLUDING BE-D retroactive (IRI-prefix discriminator `spec_retroactive_*` per BE-D §12.5 rollback discriminator) returns count = 0; KT-5 DOES NOT FIRE (0 < 2 threshold); HC #59 BINDING screen applied; honest gap on mid-Cycle-16 observation window adequacy + IRI-prefix vs retroactiveClassification predicate gap surfaced at envelope `kt_5_evaluation` block + `honest_gaps`) |
| 8 | BE-A §1-§3 + BE-B §10 + BE-C §11 + BE-D §12 LOCKED bodies UNMODIFIED across 5 BE-A/BE-B/BE-C/BE-D artifacts | [x] PASS (Edit-per-section; only §13 appended; `git diff` on §0-§12 line ranges of 3 docs = 0 line changes; canonical-marker baseline preserved post-edit) |
| 9 | govML v2.8.4 existing 3 install function bodies UNMODIFIED throughout BE-E (`install_runtime_emit_substrate` + `install_spec_registry_authoring_discipline` + `install_spec_implementation_gates`) — ADDITIVE-APPEND only at v2.8.5 | [x] PASS (`git -C ~/ml-governance-templates diff scripts/init_project.sh` shows ADDITIVE-ONLY at install_forward_apply_observation function body + L632 list extension; existing 3 install function line ranges show 0 deletions) |
| 10 | Cycle 6 LOCKED ontology body UNMODIFIED throughout BE-E (work-host boundary discipline preserved per substrate §8 refusal anchor 2) | [x] PASS (`git -C ~/cycle_6_unified_substrate_build status -s` empty pre + post BE-E; BE-E smoke-test test-graph scoped without touching cycle_6 runtime/jena/ canonical body) |
| 11 | HC-11 partition preserved (publishable: observation infrastructure design + 2 NEW event class definitions + observation protocol doc + Cycle 10 RUNTIME_EMIT_SPEC inheritance narrative + govML v2.8.5 ADDITIVE-APPEND framing + 14-field schema reflection at smoke-test PROV-O typed-edges; ip-private: per-host enforcement-routing internal implementation + agent-prompt details + per-spec evidence trail at JSONL row content) | [x] PASS (forward_apply_observation_protocol.md §6 explicit HC-11 partition declaration; per-edge HC-11 annotation per BE-A §1-§3 LOCKED structural at smoke-test specs + event payload `payload.access_permission` field per RUNTIME_EMIT_SPEC §13.1) |
| 12 | HC-BE-D-1 write-boundary enforcement gap NOT closed within BE-E (Cycle 18 scope per Rex Option B split-sequential) — BE-E inherits SAME blind spot as BE-D (observes only BE-B-mediated path); honest acknowledgment at envelope `hc_be_d_1_boundary_discipline_honest_acknowledgment` section | [x] PASS (BE-E does NOT attempt filesystem-scan + spec-class-discriminator + work-host routing per substrate §6 + §8 refusal anchor 5; honest acknowledgment surfaced at envelope; carry-forward to Cycle 18 SI inheritance per Rex 2026-05-27 Option A + Option B split-sequential) |

<!-- /gate:artifact_contract §13 -->

## §14 BE-F H_recovery_3 Cycle 16 Stage 5 Probe Library 4 Primitives Append

<!-- gate:artifact_contract §14 required -->

Per Cycle-16-S11 BE-F dispatch substrate §1 + §4 ARTIFACT_CONTRACT fill instructions + Cycle 14 §12 BE#6 multi-BE append precedent + SI Amendment 2026-05-28a Done #11-#16 + Amendment 2026-05-28b Done #17-#19. APPEND-only; §0-§7 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) + §12 (BE-D LOCKED `902f222`) + §13 (BE-E LOCKED) unchanged. Cycle 16 BE-F probe library at `scripts/probes/{a,b,c,d}/`: 4 primitives + 8 self-test fixtures + admission gate (Python + bash wrapper) + version-lock per Done #13 + dogfooding-within-cycle ≥12 production fires per Done #15d. ED §5.7 evidence-path translation at S11 = cycle_16 first-arc (`scripts/probes/`); govML upstream back-port to `~/ml-governance-templates/scripts/probes/` + `templates/build/probes/` lands at BE-I S14+ per HC #45 chain extension precedent.

### §14.0 BE-F Cycle 16 Probe Library Contract Identity

| Field | Value |
|---|---|
| **Artifact** | `~/cycle_16_close_spec_to_implementation_gap_build/scripts/probes/{a,b,c,d}/probe_<class>.py` (4 primitive files, executable, with `--self-test` + `--aggregate-cycle N` + `--spec-iri` modes) + `~/cycle_16_close_spec_to_implementation_gap_build/scripts/probes/__init__.py` (admission-gate Python module exposing `admit_all()` + `expose_admitted()` + ADMITTED_PROBES + REFUSED_PROBES) + `~/cycle_16_close_spec_to_implementation_gap_build/scripts/probe_library_admission.sh` (bash CLI/CI wrapper; exit 0 iff all probes admitted; exit 1 on refusal) + `~/cycle_16_close_spec_to_implementation_gap_build/scripts/probes/c/llm_judge_prompt.md` (Class C LLM-judge contract template with HC #72 anti-substitution language explicit; forbids registry-text-only acceptance; calibration fixtures referenced) + `~/cycle_16_close_spec_to_implementation_gap_build/tests/probes/fixtures/known_{good,bad}_{a,b,c,d}_*.json` (8 fixtures; 1 known-good + 1 known-bad per class) + `~/cycle_16_close_spec_to_implementation_gap_build/outputs/probe_library_self_test_events.jsonl` (≥8 self-test events at admission + 1 T12 deliberate-fail event = 9 rows) + `~/cycle_16_close_spec_to_implementation_gap_build/outputs/probe_library_admission_events.jsonl` (5 events: 4 PASS + 1 REFUSE for T12 negative test) + `~/cycle_16_close_spec_to_implementation_gap_build/outputs/probe_fire_events.jsonl` (16 production-fire events; ≥3 per class; mix expected-implemented + expected-dormant per class) + §14 BE-F appends at 3 cycle_16 docs (Edit-per-section) + DEPLOYMENT_LOG §2 row 6 + BUILD_DECISION_LOG §2 row 6 + state.json transition + DECISION_LOG D-S11-1 + `outputs/build_runner_envelope.yaml` OVERWRITE + `outputs/build_runner_events.jsonl` append with 1 `be_f_probe_library_ship.event` row |
| **Cycle** | 16 (BE-F closing Done #13 + H_recovery_3 per SI Amendment 2026-05-28a; ED §5.7 PASS-all 6/6 thresholds; ROADMAP Phase 8 BE-F; first arc lives at cycle_16 per ED §5.7 evidence-path translation governance; govML upstream `scripts/probes/` + `templates/build/probes/` back-port land at BE-I S14+ per HC #45 chain extension n=5→6) |
| **Source** | BE-A SHIPPED 14-field schema at `/cycle6` + BE-B SHIPPED `register_spec()` authoring wrapper + BE-C SHIPPED TWO-surface BLOCKING gate at govML v2.8.4 + BE-D SHIPPED 232-distinct retroactive scan inventory at `outputs/retroactive_scan_cycle_1_15_run.json` (the dogfooding-within-cycle production-fire spec source) + BE-E SHIPPED forward-apply observation infrastructure with 2 NEW event classes wired into emit.py at govML v2.8.5; BE-F consumes BE-D's 232-distinct inventory as production-fire spec source AND emits to a NEW sink path `outputs/probe_fire_events.jsonl` (namespace-isolated from BE-A/B/C/D/E sinks per Cycle 10 rule_6/8/10/12 invariants) |
| **Architectural choice** | 4 probe primitives as canonical vocabulary (code, NOT markdown — per HR §3.recovery H_recovery_3 + LA §6.recovery.A row 2 Hypothesis shared canonical strategies pattern + row 10 in-toto predicateType registry pattern); admission gate at Python module entry point (`__init__.py`) + bash CLI wrapper (`probe_library_admission.sh`) with DP#44-compliant refuse-on-self-test-fail discipline; behavioral-evidence-only acceptance per HC #72 anti-substitution (Class A reads JSONL `tool_use` blocks; Class B reads call-site OR JSONL exercise; Class C structural-judge reads actual code with file:line citation + LLM-judge prompt template forbids registry-text-only acceptance; Class D reads downstream JSONL fire OR downstream cross-cycle citation); precondition vs acceptance evidence types structurally distinguished (`evidence_type: precondition_missing` vs `evidence_type: probe_fire_aggregate`); version-lock per Done #13 (PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT constants pinned in each probe body; modifications require Builder-ARCH paradigm dispatch per HC #74); admission gate refuses generic-emission escape primitives by construction (probe-fire reads SPECIFIC spec-class behavioral surface, not "any emit of any class fires"; KT-9 firing surface evaluated and DOES NOT FIRE at BE-F admission scan). |
| **Primary mechanism family** | Probe-library-as-canonical-vocabulary measurement infrastructure closing the spec-implementation MEASUREMENT gap (BE-A/B/C/D/E close the WRITE/GATE/INVENTORY/OBSERVATION gaps; BE-F provides the runtime-grounded behavioral check the prior 5 BEs reference). Per LA §6.recovery.A: Pact contract testing (row 1) + Hypothesis property-based testing (row 2) + Stryker mutation testing (row 3) + OTEL trace context (row 4) + Bazel dep-graph (row 5) + OPA admission webhook (row 6) + pre-commit hooks (row 7) + eBPF uprobe (row 8) + BX/oasdiff (row 9) + SLSA in-toto (row 10). The composition is canonical-vocabulary-as-callable-primitives (code) plus self-test-as-admission-criterion plus version-lock-as-modification-control plus dogfooding-within-cycle-as-production-evidence. Substitution-prone shapes (registry-field reads / token counts / status enums / smoke-only fires / artifact-exists / single-smoke) are REJECTED at acceptance per HC #72; KT-7 (self-test fail) / KT-8 (gate predicate string-matches probe ID) / KT-9 (generic-emission escape) / KT-10 (zero production fires) firing surfaces evaluated at BE-F R3. |
| **Authority chain** | Cycle 16 SI ACTIVE 2026-05-27 (`a2f14d5`) + Amendments 27a (`be54a97`) + 27b (`badd749`) + 28a (`5b1e8d6`) + 28b (`f66714f`/`3e5907a`) + Rex 2026-05-28 paradigm ruling walking back S8 FORMAL CLOSE + Rex 2026-05-28 "proceed" + kc-48 R1 PASS S10 disposition (a) + DECISION_LOG D-S2..D-S10 + kc-48 R1 PASS Cycle-16-S11 task-context dispatch authorization via Cycle-16-S11 Coach + dispatch substrate `~/Moonshots_Career_Thesis_v2/.claude/workspace/cycle_16_s11_stage_5_be_f_dispatch_substrate.md` |

### §14.1 BE-F Pre-Conditions (rows 31-36)

| # | Pre-condition | How verified at runtime | Refusal behavior on FAIL |
|---|---|---|---|
| 31 | **BE-A + BE-B + BE-C + BE-D + BE-E artifacts UNMODIFIED at cycle_16/** — §0-§13 LOCKED bodies at 3 docs/.md + BE-B `scripts/spec_registry_authoring.py` BE-B body unchanged + BE-C 2 gate scripts at govML scripts/ unchanged + BE-D `outputs/retroactive_scan_cycle_1_15_run.json` unchanged + BE-E `scripts/runtime_emit/emit.py` BE-E extension unchanged (additive only) + BE-E `docs/forward_apply_observation_protocol.md` unchanged + BE-E `outputs/forward_apply_observation_events.jsonl` unchanged | `git diff` against BE-E SHIPPED HEAD `901f427` returns 0 line changes on §0-§13 line ranges of 3 docs; `git diff scripts/spec_registry_authoring.py scripts/runtime_emit/emit.py` returns empty; `git -C ~/ml-governance-templates diff scripts/spec_implementation_*_gate.sh scripts/init_project.sh` returns empty | halt-and-surface; refuse-on-missing-precondition per DP#44 + S132; do NOT route around |
| 32 | **`outputs/retroactive_scan_cycle_1_15_run.json` present + readable** as production-fire spec source (232 distinct cycle16:Spec across 4 classes from BE-D enumeration) | `test -f outputs/retroactive_scan_cycle_1_15_run.json && python3 -c "import json; d=json.load(open('outputs/retroactive_scan_cycle_1_15_run.json')); assert len(d['per_spec_evidence_IP_PRIVATE']) >= 200"` exits 0 | halt-and-surface; BE-D inventory is structural precondition for BE-F dogfooding-within-cycle ≥12 production fires |
| 33 | **`scripts/probes/{a,b,c,d}/` directory structure scaffolded** with empty class subdirs + `tests/probes/fixtures/` directory + 3 NEW empty JSONL sinks (`outputs/probe_library_self_test_events.jsonl` + `outputs/probe_library_admission_events.jsonl` + `outputs/probe_fire_events.jsonl`) writable at BE-F build step 2 | `find scripts/probes -type d` returns ≥5 dirs (probes + 4 class subdirs); `test -w outputs/probe_library_self_test_events.jsonl` etc. succeed | halt-and-surface; sink-unwritable surfaces upstream filesystem misconfiguration |
| 34 | **Active Claude Code session transcript JSONLs accessible at `~/.claude/projects/-home-azureuser-*/`** for Class A behavioral evidence (Agent tool_use block parsing) | `find ~/.claude/projects/-home-azureuser-* -name "*.jsonl" -mmin -10080 \| wc -l` returns ≥3 files (recent transcript-week window) | halt-and-surface as KT-6 substrate-viability candidate; Class A probe cannot fire behavioral check without transcript access |
| 35 | **`outputs/build_runner_events.jsonl` present** (Cycle 15 BE#4 baseline + BE-A/B/C/D/E 5-event class fires) as Class D probe's downstream JSONL fire scan target | `test -f outputs/build_runner_events.jsonl && [ "$(wc -l < outputs/build_runner_events.jsonl)" -ge 1 ]` exits 0 | halt-and-surface; Class D behavioral evidence path (i) depends on downstream JSONL artifact presence |
| 36 | **Substitution-detection precondition: probe code body MUST NOT reference proxy semantics (registry-field reads / status-enum equality / token/citation count / smoke-only fires / artifact-exists / single-smoke) as ACCEPTANCE evidence** — HC #72 anti-substitution applied at the probe AUTHORING boundary | `grep -E "cycle16:currentStatus|status_enum|token_count|artifact_exists" scripts/probes/*/probe_*.py` returns either 0 matches OR only matches in refusal-discriminator code paths (not in acceptance evidence paths); structural code-review against the 6 substitution shapes | halt-and-surface; substitution-shape probe body is KT-8 firing surface; Builder-ARCH paradigm dispatch required for probe-body repair (HC #74 BINDING) |

### §14.2 BE-F Post-Conditions (rows 31-36)

| # | Post-condition | How verified after run | What ACCEPTANCE_CRITERIA §14.1 measures against |
|---|---|---|---|
| 31 | **4 probe primitives shipped** at `scripts/probes/{a,b,c,d}/probe_<class>.py`, each executable + each ships PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT constants + each supports `--self-test` + `--aggregate-cycle N` + `--spec-iri` modes | `find scripts/probes/ -name "probe_*.py" -type f -executable \| wc -l` returns 4; `grep -lE 'PROBE_VERSION\s*=' scripts/probes/{a,b,c,d}/probe_*.py \| wc -l` = 4; `grep -lE 'PROBE_ADMISSION_LOCK_COMMIT\s*=' scripts/probes/{a,b,c,d}/probe_*.py \| wc -l` = 4 | ACCEPTANCE_CRITERIA §14.1 row 31 primitive count + class coverage + version-lock + invocation interface |
| 32 | **8 self-test fixtures shipped** at `tests/probes/fixtures/known_{good,bad}_{a,b,c,d}_*.json`, each JSON-parseable + each carries expected_implemented field + each carries rationale field | `find tests/probes/fixtures/ -name "known_*.json" \| wc -l` ≥ 8; per-class `find tests/probes/fixtures/ -name "known_*_<cls>_*.json" \| wc -l` ≥ 2 per class A/B/C/D; `python3 -c "import json, glob; [json.loads(open(f).read()) for f in glob.glob('tests/probes/fixtures/known_*.json')]"` exits 0 | ACCEPTANCE_CRITERIA §14.1 row 32 fixture count + per-class coverage + JSON validity |
| 33 | **Admission gate refuses primitives with failing self-test (T12 verified)** — synthetic broken probe at `scripts/probes/_broken_/probe_broken.py` (passes self-test as always-implemented=True regardless of fixture class) invoked via `probes._run_admission_for_probe()` → returns ok=False + emits `event_class: probe_library_admission.refuse.event` to admission sink; broken probe REMOVED after T12 evidence captured (clean admission scan post-T12 admits only the 4 canonical probes) | `grep -c '"event_class": "probe_library_admission.refuse.event"' outputs/probe_library_admission_events.jsonl` ≥ 1; `ls scripts/probes/_broken_/ 2>/dev/null` empty post-T12; `bash scripts/probe_library_admission.sh && echo $?` returns 0 post-T12 cleanup | ACCEPTANCE_CRITERIA §14.1 row 33 admission gate refusal evidence (T12 negative test) + post-T12 clean state |
| 34 | **Dogfooding-within-cycle ≥12 production-fire events** at `outputs/probe_fire_events.jsonl` with `run_id` prefix `s11_be_f_production_*` (NOT `_smoke_` / `_probe_lib_self_test_`); per-class ≥3 fires + mix: ≥1 expected-implemented + ≥1 expected-dormant per class | `wc -l outputs/probe_fire_events.jsonl` ≥ 12; `grep -c 'run_id.*s11_be_f_production_' outputs/probe_fire_events.jsonl` ≥ 12; per-class production count via `jq -r '.payload.primitive_class' outputs/probe_fire_events.jsonl \| sort \| uniq -c` returns {A:≥3, B:≥3, C:≥3, D:≥3}; mix verification via `jq` per-class implemented vs not-implemented counts both ≥1 | ACCEPTANCE_CRITERIA §14.1 row 34 production-fire count + per-class coverage + mix discipline (Done #15d strict; smoke-only fires REFUSED) |
| 35 | **Self-test events JSONL ≥8 rows** at `outputs/probe_library_self_test_events.jsonl` with `predicateType: cycle16:probe_self_test_v1` (distinct from production `cycle16:probe_fire_v1` per LA §6.recovery.A row 10 SLSA chain-of-custody) — 8 self-test rows for the 4 admitted probes × 2 fixtures each (known_good + known_bad) | `wc -l outputs/probe_library_self_test_events.jsonl` ≥ 8; `jq -r 'select(.predicateType == "cycle16:probe_self_test_v1") \| .payload.primitive_class' outputs/probe_library_self_test_events.jsonl \| sort -u` returns {A, B, C, D}; per-class fixture-pair count ≥ 2 (1 known-good + 1 known-bad) | ACCEPTANCE_CRITERIA §14.1 row 35 self-test event count + predicateType discriminator + per-class fixture-pair coverage |
| 36 | **Version-lock constants per Done #13** — each probe body carries PROBE_VERSION = "0.1" + PROBE_ADMISSION_LOCK_COMMIT = "<sha>" recorded at admission time (commit SHA = build commit at admission); admission events JSONL row carries `probe_admission_lock_commit` field equal to the constant in the probe body | `grep -c 'PROBE_VERSION = "0.1"' scripts/probes/*/probe_*.py` = 4; `grep -c 'PROBE_ADMISSION_LOCK_COMMIT' scripts/probes/*/probe_*.py` = 4; `jq -r '.payload.probe_admission_lock_commit' outputs/probe_library_admission_events.jsonl \| sort -u \| wc -l` = 1 (single SHA across all admission rows) | ACCEPTANCE_CRITERIA §14.1 row 36 version-lock per Done #13 + admission-time SHA pinning |

### §14.3 BE-F Invariants (rows 22-25)

| # | Invariant | When checked | If violated |
|---|---|---|---|
| 22 | **Behavioral evidence ONLY at probe-fire acceptance** — `evidence_type: probe_fire_aggregate` carries actual runtime/transcript/code observation; `evidence_type: precondition_missing` carries ONLY precondition-failure descriptors and is NOT acceptance evidence (HC #72 anti-substitution). Probes that fall back to proxy semantics (registry-field reads / token counts / status enums / smoke-only / artifact-exists / single-smoke) under-the-hood violate this invariant. | At every probe-fire JSONL row emit + at admission gate self-test result + at Coach R3 HC #72 independent sweep | CONTRACT_CHANGE per Binding 7; probe body repair via Builder-ARCH paradigm dispatch (HC #74) — Coach does NOT route around with §11 override or threshold relaxation |
| 23 | **Version-lock immutability** — PROBE_VERSION constant in probe body MUST NOT change post-admission without paradigm dispatch + new admission test run + new admission-event JSONL row. The PROBE_ADMISSION_LOCK_COMMIT field pinned at admission is the structural marker of probe-body-was-vetted-at-this-commit. | At every probe body edit attempt + at Coach R3 close-eval (`grep -E 'PROBE_VERSION\s*=' scripts/probes/{a,b,c,d}/probe_*.py` returns 4 instances of `"0.1"`) | halt-and-surface; probe-body modification without paradigm dispatch is KT-8/KT-9 firing surface; Builder-ARCH dispatch required for probe-body modification |
| 24 | **Admission gate refuse-on-fail discipline** — `probe_library_admission.sh` exits non-zero when ANY probe self-test does not distinguish known_good + known_bad; refusal events MUST emit to admission sink with `event_class: probe_library_admission.refuse.event` (not silently dropped). | At every admission scan (CI invocation + at every BE close + at session-close gate consumption) | halt-and-surface; silent refusal contamination = registry-shape-bypass; admission gate predicate body itself becomes substitution-prone if refusal events are dropped |
| 25 | **Smoke-only fires NOT acceptance evidence per Done #15d strict** — `run_id` prefix `s11_be_f_production_*` is structural discriminator for acceptance fires; `run_id` prefix `s11_be_f_probe_lib_self_test_*` / `_smoke_*` / `_admission_*` are infrastructure fires NOT counted toward acceptance; R3 aggregation filters via `run_id` prefix. | At every R3 close-eval + at FINDINGS close + at session-close gate (BE-H structural-prevention piece (d) probe-coverage check inheritance) | halt-and-surface; smoke-only-as-acceptance is the failure shape Done #15d was authored to prevent; treat as KT-7 + KT-10 cross-firing surface |

### §14.4 BE-F Side Effects (diff vs §13)

| Surface | NEW effect at BE-F | Bounds |
|---|---|---|
| Filesystem writes | NEW: `scripts/probes/{a,b,c,d}/probe_<class>.py` (4 files; ~16-20KB each; executable) + `scripts/probes/c/llm_judge_prompt.md` (~5KB; HC #72 anti-substitution language explicit) + `scripts/probes/__init__.py` (~4KB; admission-gate module) + `scripts/probe_library_admission.sh` (~3KB; bash CLI wrapper) + `tests/probes/fixtures/known_{good,bad}_{a,b,c,d}_*.json` (8 fixtures; ~1KB each) + 3 NEW JSONL sinks (`outputs/probe_library_self_test_events.jsonl` + `outputs/probe_library_admission_events.jsonl` + `outputs/probe_fire_events.jsonl`; 0B at scaffold; grow to ≥8 + ≥5 + 16 rows respectively at BE-F close); EDITS to 3 cycle_16 docs §14 BE-F appends (Edit-per-section; LOCKED §0-§13 preserved); EDITS to DEPLOYMENT_LOG §2 row 6 + BUILD_DECISION_LOG §2 row 6 (append-only); state.json transition + DECISION_LOG D-S11-1 fill; `outputs/build_runner_envelope.yaml` OVERWRITE (BE-E → BE-F envelope) ; `outputs/build_runner_events.jsonl` append (1 `be_f_probe_library_ship.event` single-fire NEW event class at BE-F close + Cycle 15 BE#4 5-event baseline class fires) | ≤120KB cumulative new content at cycle_16/; no existing-file body modifications outside §14 appends + DEPLOYMENT/BUILD_DECISION row 6 append + envelope overwrite + state.json transition + DECISION_LOG append |
| Database writes | None at BE-F (probe primitives consume `/cycle6` SPARQL endpoint for Class B SHACL conforming-instance evidence query but do NOT write to the registry; all writes routed through BE-B `register_spec()` per HC-BE-D-1 boundary discipline carried forward from BE-D; BE-F's reading does not modify the canonical production registry rows) | 0 INSERT/UPDATE/DELETE/DROP statements issued from BE-F probe bodies; SPARQL SELECT/ASK only |
| Network egress | Class B probe ONLY: localhost-only Fuseki HTTP via Python urllib (per-probe-fire SPARQL ASK for `?inst a ?target_class` count + endpoint reachability) | ~16 SPARQL invocations × ~200ms each ≈ 3.2s wall-clock cumulative at BE-F dogfooding-within-cycle; HC #28 retry not required (single-shot per spec); endpoint failure short-circuits with implemented=false + evidence_type=precondition_missing |
| govML repo writes | **NONE at S11 per substrate §1 item 11 + ED §5.7 evidence-path translation governance** — v2.8.5 STANDING UNMODIFIED. Probe library back-port to govML upstream `~/ml-governance-templates/scripts/probes/` + `templates/build/probes/` LANDS AT BE-I S14+ per HC #45 chain extension (4-repo paired commit). S11 close commits cycle_16 + EMABS + Moonshots (3-repo paired); govML untouched. | 0 govML file modifications at BE-F; v2.8.5 install chain n=5 PRESERVED; v2.8.6 chain extension to n=6 DEFERRED to BE-I S14+ |
| Process / thread footprint | 4 probe scripts × per-spec subprocess invocations during aggregate-cycle dogfooding (subprocess.run for SPARQL via urllib; subprocess.run from admission gate for --self-test) | ≤1 concurrent python3 invocation per probe-fire; ≤2s wall-clock per probe-fire (Class A transcript scan recency-window-bounded; Class B SPARQL bounded; Class C structural-judge file scan bounded; Class D JSONL scan bounded); per-emit ≤30ms |

### §14.5 BE-F Versioning and Promotion Hooks

| Field | Value |
|---|---|
| **Version scheme** | PROBE_VERSION = "0.1" constant pinned in each of 4 probe bodies + PROBE_ADMISSION_LOCK_COMMIT pinned to admission-time SHA; library admission gate (`__init__.py` + `probe_library_admission.sh`) PROBE_LIBRARY_VERSION = "0.1" pinned; modifications to probe bodies require version bump + new admission test run + Builder-ARCH paradigm dispatch (HC #74) |
| **govML version** | NO BUMP at S11 (v2.8.5 STANDS UNMODIFIED); v2.8.6 ADDITIVE-APPEND back-port (probe library + Operational-Definition Substitution Gate + structural-prevention layer) LANDS AT BE-I S14+ per HC #45 chain extension precedent n=5→6; LOCKED bodies of v2.8.2 `install_runtime_emit_substrate` + v2.8.3 `install_spec_registry_authoring_discipline` + v2.8.4 `install_spec_implementation_gates` + v2.8.5 `install_forward_apply_observation` will be UNMODIFIED at BE-I per HC #45 ADDITIVE-APPEND precedent strict |
| **Promotion authority** | build-runner BUILT at BE-F (Cycle-16-S11) → Coach R3 evaluation per kc-48 PD §3.3 T1-T13 + HC #72 sweep + HC #70 reality-vs-intent table → build-orchestrator promotion at Cycle-16-S11 close paired commit per Pattern 19 telemetry → Rex paradigm ruling required on CONTRACT_CHANGE OR KT-7/8/9/10 firing |
| **Promotion gates** | BE-A/B/C/D/E gate stack inherited (`build_pipeline_gate.sh` + `production_deployment_gate.sh` + `cross_system_validation_gate.sh` + `hc26_internal_smoke_gate.sh` + `spec_implementation_present_gate.sh` + `spec_implementation_session_close_gate.sh`); BE-F ADDS `probe_library_admission.sh` as build-time admission predicate AND the present-gate / session-close-gate predicate-body UPGRADE from registry-field SPARQL ASK to probe-fire-evidence aggregation is BE-H scope (Done #15 + Done #17 + H_recovery_7 + H_recovery_9), NOT BE-F. BE-F SHIPS the canonical vocabulary; BE-G/BE-H wires it into the existing gates. |
| **Rollback procedure** | If full BE-F rollback required: (1) `git -C ~/cycle_16_close_spec_to_implementation_gap_build checkout docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md DECISION_LOG.md state.json outputs/build_runner_envelope.yaml outputs/build_runner_events.jsonl` (revert §14 appends + state transition + envelope); (2) `rm -rf scripts/probes/ scripts/probe_library_admission.sh tests/probes/fixtures/known_*.json outputs/probe_library_self_test_events.jsonl outputs/probe_library_admission_events.jsonl outputs/probe_fire_events.jsonl` (revert NEW artifacts); (3) NO govML revert required at BE-F (v2.8.5 STANDS UNMODIFIED — confirmed in §14.4 NONE at govML); (4) Cycle 6 LOCKED preserved throughout (verified at HC #26 Gate 3); (5) BE-A/B/C/D/E LOCKED bodies preserved throughout (verified at §14.1 row 31 git-diff invariant). Rollback NOT end-to-end tested at BE-F (defer to Cycle 17+ if Coach R3 disposition requires) |

### §14.6 BE-F Change Control Triggers

- BE-F 11-deliverable scope per dispatch substrate §1 — any deviation from declared scope is CONTRACT_CHANGE per Binding 7 + S155
- Probe body changes (PROBE_VERSION bump; PROBE_ADMISSION_LOCK_COMMIT change; primitive-class assignment change; behavioral-evidence-path change) — CONTRACT_CHANGE required per §14.3 invariant 23 + HC #74 BINDING (Builder-ARCH paradigm dispatch)
- Admission gate predicate body changes (`__init__.py` admit_all() logic; refusal criterion; bash CLI wrapper exit-code semantics) — CONTRACT_CHANGE required per §14.3 invariant 24
- New probe class outside the 4-class taxonomy (A/B/C/D = AgentContract / Schema / DesignDecision / MethodologyCommitment per BE-A 14-field schema enum) — KT-9 firing surface candidate + HC #74 cycle-management disposition (paradigm-class; surface to Rex via Pattern 11 Step 3.5; do NOT dispose operationally)
- Smoke-vs-production discriminator semantics changes (`run_id` prefix convention `s11_be_f_production_*` vs `_smoke_*` vs `_probe_lib_self_test_*`) — CONTRACT_CHANGE required per §14.3 invariant 25 (Done #15d strict)
- LLM-judge prompt template substantive changes (Class C `llm_judge_prompt.md`) — CONTRACT_CHANGE required per HC #74 BINDING (acceptance-criteria-shape change at probe-judge layer; Builder-ARCH paradigm dispatch required)
- govML upstream back-port path/timing changes (BE-I S14+ vs at-S11) — already locked by HC #45 chain extension precedent + ED §5.7 evidence-path translation governance; Rex paradigm ruling required to revisit
- HC #72 substitution-shape catalog extensions (currently 6 shapes: registry-field / status-enum / token-count / smoke-only / artifact-exists / single-smoke) — CONTRACT_CHANGE required at HC #72 catalog + cascade to all 4 probe bodies + admission gate refusal criteria

CONTRACT_CHANGE authority = Rex paradigm ruling per Binding 7 + S155 + BUILD_DECISION_LOG §4 verbatim.

### §14.7 BE-F Self-test (BEFORE shipping)

| # | Check | Status |
|---|---|---|
| 1 | 4 probe primitive files present at `scripts/probes/{a,b,c,d}/probe_<class>.py`, each executable + each with PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT constants | [x] PASS (`find scripts/probes/ -name "probe_*.py" -type f -executable \| wc -l` = 4; `grep -c 'PROBE_VERSION = "0.1"' scripts/probes/*/probe_*.py` = 4; `grep -c 'PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"' scripts/probes/*/probe_*.py` = 4) |
| 2 | 8 self-test fixtures at `tests/probes/fixtures/known_{good,bad}_{a,b,c,d}_1.json`, each JSON-parseable + per-class pair (1 known-good + 1 known-bad) | [x] PASS (`ls tests/probes/fixtures/known_*.json \| wc -l` = 8; per-class verification via `ls tests/probes/fixtures/known_*_a_*.json` etc. returns 2 each for A/B/C/D) |
| 3 | All 4 probe --self-tests exit 0 (probes distinguish known-good + known-bad fixtures) | [x] PASS (per-probe `python3 scripts/probes/<cls>/probe_<class>.py --self-test; echo $?` returns 0 for all 4 classes — verified at probe authoring close 2026-05-28) |
| 4 | Admission gate (`scripts/probe_library_admission.sh`) returns exit 0 + emits 4 PASS events to `outputs/probe_library_admission_events.jsonl` | [x] PASS (`bash scripts/probe_library_admission.sh && echo $?` returns 0; `grep -c '"event_class": "probe_library_admission.pass.event"' outputs/probe_library_admission_events.jsonl` ≥ 4) |
| 5 | Admission gate REFUSES deliberately-broken probe (T12 negative test) — broken probe at `scripts/probes/_broken_/probe_broken.py` invoked via `probes._run_admission_for_probe()` returns ok=False + emits `event_class: probe_library_admission.refuse.event`; broken probe REMOVED after T12 evidence captured | [x] PASS (T12 evidence captured at 2026-05-28: ok=False rc=1 evidence='self_test_exit=1 stderr_head=FAIL: probe does not distinguish known_good and known_bad fixtures'; `grep -c '"event_class": "probe_library_admission.refuse.event"' outputs/probe_library_admission_events.jsonl` = 1; `ls scripts/probes/_broken_/ 2>/dev/null` empty post-T12) |
| 6 | ≥12 production-fire events at `outputs/probe_fire_events.jsonl` with `run_id` prefix `s11_be_f_production_*`; per-class ≥3; mix expected-implemented + expected-dormant per class | [x] PASS (`wc -l outputs/probe_fire_events.jsonl` = 16; `grep -c 'run_id.*s11_be_f_production_' outputs/probe_fire_events.jsonl` = 16; per-class production count: A=4 B=4 C=4 D=4; mix: A(implemented=2 not=2) B(2/2) C(1/3) D(1/3) — all classes have ≥1 of each) |
| 7 | Self-test events JSONL ≥8 rows at `outputs/probe_library_self_test_events.jsonl` with `predicateType: cycle16:probe_self_test_v1` (distinct from production `cycle16:probe_fire_v1`) | [x] PASS (`wc -l outputs/probe_library_self_test_events.jsonl` ≥ 8 covering 4 probes × 2 fixtures + T12 row + Class C re-run row; predicateType field present in all rows) |
| 8 | Class C LLM-judge prompt template ships at `scripts/probes/c/llm_judge_prompt.md` with HC #72 anti-substitution language explicit (forbids registry-text-only / ADR-text-only / FINDINGS-mention-only as acceptance evidence; requires file:line citation) | [x] PASS (`grep -c 'HC #72\|anti-substitution\|file:line citation' scripts/probes/c/llm_judge_prompt.md` ≥ 5; structural-judge fallback at `_structural_judge()` in `probe_design_decision.py` enforces same contract shape without online LLM) |
| 9 | BE-A §1-§3 + BE-B §10 + BE-C §11 + BE-D §12 + BE-E §13 LOCKED bodies UNMODIFIED across 5 BE-A/B/C/D/E artifacts | [x] PASS (Edit-per-section; only §14 appended; `git diff` on §0-§13 line ranges of 3 docs = 0 line changes; canonical-marker baseline preserved post-edit) |
| 10 | govML v2.8.5 STANDS UNMODIFIED at BE-F (NO govML touch at S11 per substrate §1 item 11; back-port at BE-I S14+ per HC #45 chain extension precedent) | [x] PASS (`git -C ~/ml-governance-templates status -s` empty pre + post BE-F; v2.8.5 install chain n=5 PRESERVED; v2.8.6 deferred to BE-I) |
| 11 | Cycle 6 LOCKED ontology body UNMODIFIED throughout BE-F (work-host boundary discipline preserved) | [x] PASS (BE-F probes consume `/cycle6` SPARQL endpoint via SELECT/ASK only — no INSERT/UPDATE/DELETE/DROP issued from probe bodies; Cycle 6 runtime/jena/ canonical body untouched) |
| 12 | HC-11 partition preserved (publishable: probe-library design + canonical vocabulary + admission-gate interface + LLM-judge contract template + self-test discipline; ip-private: per-probe-fire production payload contents + per-probe behavioral evidence trail at JSONL row content + per-class spec inventory enumeration) | [x] PASS (probe code body publishable per substrate §1; production-fire JSONL row content carries IP-private per-spec evidence — IRI + name_truncated + current_status_known + behavioral path — but the SCHEMA + invocation surface is publishable per HC-11 partition) |

<!-- /gate:artifact_contract §14 -->

## §15 BE-G H_recovery_2/7/8/9 Cycle 16 Stage 5 Write-Boundary Enforcement Composite Append

> ADDITIVE-APPEND per HC #45 (chain n=7). §1-§14 (BE-A §1-§3 / BE-B §10 / BE-C §11 /
> BE-D §12 / BE-E §13 / BE-F §14) preserved byte-identical above. Authority: BE-G
> dispatch substrate + ED §5.8 (6/6 thresholds) + SI Amendment 28d Done #29/#30.

### §15.1 Artifacts (10 deliverables)

| # | Deliverable | Path | Type |
|---|---|---|---|
| 1 | Pre-commit hook | `~/ml-governance-templates/scripts/spec_authoring_pre_commit_hook.sh` (+ cycle_16 mirror `scripts/be_g_mirror/`) | write-boundary block |
| 2 | fsnotify watcher | `~/ml-governance-templates/scripts/spec_authoring_watcher.py` (inotify via ctypes; +mirror) | git-bypass observation |
| 3 | `forward_apply_emit()` wired into production `register_spec()` | `scripts/spec_registry_authoring.py:547+` | ADDITIVE; closes 0-caller gap |
| 4 | 3-registry reconciliation gate | `~/ml-governance-templates/scripts/three_registry_reconciliation_gate.sh` (+mirror) | FS + /cycle6 + prompt_inventory drift |
| 5 | Done #17 cycle-close gate UPGRADE | `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` (+mirror) | subprocess probe-fire aggregate; ASK-currentStatus REMOVED |
| 6 | `kill_spec(spec_iri, adr_retraction_ref, killing_session, kill_reason)` | `scripts/spec_registry_authoring.py` | 4-param; ADR grep + spec_killed_event + SPARQL→killed + DP#44 |
| 7 | Done #19 dormancy gate UPGRADE | `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` (+mirror) | probe-fire JSONL aggregate; advisory at C16 |
| 8 | Done #29 coverage matrix + CI bypass closure | `outputs/be_g_coverage_matrix.{md,json}` + `outputs/spec_authoring_required_check.yml` | per-repo enumeration + server-side required check |
| 9 | Done #30 guard-the-guards | prompt_inventory (build-orchestrator + build-runner) + 6 self-registered specs at /cycle6 | HC #64 closure |
| 10 | Class E/F integration-hook STUBS | `scripts/spec_registry_authoring.py` (`_class_e_integration_hook` + `_class_f_integration_hook`) | architectural accommodation; NO probe impl |

### §15.2 Invariants

- (I-BE-G-1) Every gate/hook/kill acceptance predicate names PROBE-FIRE EVIDENCE or a
  real write-path observation — never a status enum / token count / file-exists (HC #72 / KT-8).
- (I-BE-G-2) Done #17 present-gate body subprocess-executes `probes/<class>/probe_<class>.py
  --aggregate-cycle N` and aggregates `payload.implemented`; the prior `ASK {...currentStatus}`
  predicate is REMOVED (0 active matches per `grep -E '^[^#]*ASK \{.*currentStatus'`).
- (I-BE-G-3) `kill_spec()` emits NO `spec_killed_event` on DP#44 refusal — a refused kill
  can never be mistaken for a recorded one.
- (I-BE-G-4) `forward_apply_emit()` failure is non-fatal to a successful registry write
  (observation is additive, never load-bearing).
- (I-BE-G-5) Class E/F hooks are STUBS (return None) at S12; live wiring at BE-J/S15 + BE-K/S16.

### §15.3 Honest scope boundary (HC #70)

BE-G ships the PRESENT + FUTURE enforcement spine. It does NOT by itself make past specs
implemented (Phase 11-13) NOR validate the probes' own accuracy (Done #25 / Phase 12). The
present-gate PASS means "≥1 implemented probe-fire aggregated", NOT "all specs implemented".

<!-- /gate:artifact_contract §15 -->
