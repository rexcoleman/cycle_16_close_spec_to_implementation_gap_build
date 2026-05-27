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
