# ACCEPTANCE CRITERIA

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- profile: build -->
<!-- methodology_status: BE-A authored — Cycle 16 Stage 5 BE-A acceptance pre-registered BEFORE measurement at Step 3 per build-runner.md Rules + §0 pre-registration discipline -->
<!-- source: ARTIFACT_CONTRACT §2 post-conditions 1-6 + RUNTIME_EMIT_SPEC §1 event schema + dispatch substrate §1 item 6 + HR §3 H1+H2+H5+H6+H7 + HYBRID PRIMARY 4×4×5 cell granularity per ED §0a + HR §3a -->

> **Authority Hierarchy**
>
> | Priority | Document | Role |
> |----------|----------|------|
> | Tier 1 | `~/Moonshots_Career_Thesis_v2/.claude/strategic_frame.md` + Cycle 16 SI ACTIVE 2026-05-27 (a2f14d5) + Amendments 27a/27b | Primary spec — highest authority |
> | Tier 2 | ARTIFACT_CONTRACT.md §2 post-conditions (this artifact's outward-facing promise) + HYPOTHESIS_REGISTRY.md §3 H1+H2+H5+H6+H7 (BE-A surface evidence binding) + ED §0a HYBRID PRIMARY cell granularity | Clarifications — cannot override Tier 1 |
> | Tier 3 | Cycle 14 BE precedent ACCEPTANCE_CRITERIA per-test-bed strengthening n≥3 (build-class evidence grammar floor) | Advisory only — non-binding if inconsistent with Tier 1/2 |
> | Contract | This document | Implementation detail — subordinate to all tiers above |

### Companion Contracts

**Upstream (this contract depends on):**
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §2 for post-conditions this acceptance verifies
- See [RUNTIME_EMIT_SPEC](RUNTIME_EMIT_SPEC.tmpl.md) §2 for the emitted events this acceptance reads

**Downstream (depends on this contract):**
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 for the promotion gate that consumes acceptance
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §2 for the n≥3 cross-system measurement strengthening
- See [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §2 for build-decisions that resolved against acceptance verdicts

## Customization Guide

(Customization Guide deleted at BE-A fill close per template instruction.)

---

## §0 Acceptance Identity

<!-- gate:acceptance_criteria §0 required -->

| Field | Value |
|---|---|
| **Artifact under acceptance** | `cycle_16_be_a_spec_registry_schema_and_write_boundary` (per ARTIFACT_CONTRACT §0) |
| **Test bed** | TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment (3 test beds per §3 per-test-bed strengthening; Branch 3 → DesignDecision deferred to BE-D retroactive scan per ROADMAP Phase 5) |
| **Baseline reference** | Cycle 6 BE#1 ontology TTL ground state at lock_commit (10,765B; 261L; Coach-verified 2026-05-27 read VERBATIM) + Coach probe 2026-05-27 ~19:00 UTC SPARQL UPDATE/SELECT/DROP latency measurements (0.621s / 0.035s / 0.055s; all ≤5s threshold by 8-100× margin) |
| **Baseline metric value** | Cycle 6 BE#1: 246,048 quads + 46 named graphs operational; SPARQL latency p95 ≤0.621s; HC-11 access-permission enum 11,223+ usages; PROV-O 4 typed-edges operational; nanopublication 3-graph operational across 46 named graphs |
| **Pre-registration commit** | (recorded at Cycle-16-S3 close paired-commit; pre-registration BINDS at this Step 3 fill BEFORE Step 4 artifact production — per build-runner.md §Rules + §0 pre-registration discipline + ACCEPTANCE_CRITERIA self-test #2) |

<!-- /gate:acceptance_criteria §0 -->

> Acceptance verifies post-conditions (§2 of [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md))
> against a pre-registered baseline. Pre-registration commit MUST be set BEFORE
> the artifact is run for measurement. If pre-registration commit lands AFTER
> measurement, the acceptance is post-hoc and cannot be classified as PASSED.

---

## §1 Acceptance Thresholds (per post-condition)

<!-- gate:acceptance_criteria §1 entries:1 -->

For each post-condition in [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §2,
state a measurable acceptance threshold. Thresholds MUST be deterministic
count-based or numeric (no "improves substantially" — declare a number).

| # | Post-condition (link to ARTIFACT_CONTRACT §2 row) | Threshold | Measurement window | Verdict path |
|---|---|---|---|---|
| 1 | ARTIFACT_CONTRACT §2 row 1 (`docs/spec_registry_schema.ttl` exists + parseable) | rdflib parse returns ≥40 triples + 0 errors AND `cycle16:Spec rdfs:subClassOf c6:Statement` triple present | At Step 4a TTL authoring close + at BE-A close-smoke | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (e.g., FAIL with `Mechanism-non-transfer` shape if subclass inheritance not accepted by parser) |
| 2 | ARTIFACT_CONTRACT §2 row 2 (`docs/spec_registry_shapes.shacl.ttl` exists + parseable) | rdflib parse returns ≥30 triples + 0 errors AND 3 named shapes present (`cycle16:SpecShape` + `cycle16:SpecTypeShape` + `cycle16:CurrentStatusShape`) | At Step 4b SHACL authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 3 | ARTIFACT_CONTRACT §2 row 3 (`docs/spec_authoring_discipline.md` exists with 5 substrate-operations) | `grep -c "^### Operation" docs/spec_authoring_discipline.md` returns ≥5 AND HC-11 + PROV-O + nanopub sections present | At Step 4c discipline doc authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 4 | ARTIFACT_CONTRACT §2 row 4 (SPARQL UPDATE smoke test PASSES for 3 test beds) | All 3 test beds (TB-1/TB-2/TB-3) return: UPDATE HTTP 200 + readback SELECT returns ≥14 field predicates per spec + DROP GRAPH HTTP 200; aggregate `success_bool=true` count = 3 per Metric A | At Step 4d smoke test close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE per §4 grid |
| 5 | ARTIFACT_CONTRACT §2 row 5 (SHACL refuses non-conforming specs) | pyshacl validate on non-conforming fixture: conforms=False AND violation count ≥4 (one per: missing owner + invalid spec_type + dormant-silent without target session + missing accessPermission) | At Step 4d smoke test close + §5 calibration hook fire | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 6 | ARTIFACT_CONTRACT §2 row 6 (`outputs/build_runner_events.jsonl` has ≥6 events) | `wc -l outputs/build_runner_events.jsonl` returns ≥6 AND 0 JSON parse errors AND ≥1 of each baseline event class + ≥3 write.event rows | At BE-A close-yield + before YAML envelope authored | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |

<!-- /gate:acceptance_criteria §1 -->

> [SEED: min_thresholds=1; pre-registration window: SET BEFORE artifact run]
> Verdict path includes `FAILS-WITH-DIAGNOSED-SHAPE` (not just FAIL) per
> the build-class acceptance grammar: "artifact ships and meets contract
> OR fails-with-diagnosed-shape." The latter is a valid build-class outcome
> when the failure shape is structurally legible (i.e., "artifact missed
> threshold T because mechanism M did not transfer; diagnosed and recorded
> in BUILD_DECISION_LOG").

---

## §2 Measurement Protocol

<!-- gate:acceptance_criteria §2 required -->

State exactly how each threshold is measured. Measurement is read from the
runtime-emit stream (per [RUNTIME_EMIT_SPEC](RUNTIME_EMIT_SPEC.tmpl.md) §2)
or from artifact output, NOT from operator self-assessment.

| # | Threshold (link to §1) | Data source | Aggregation | Blinding plan |
|---|---|---|---|---|
| 1 | §1 row 1 (TTL parseable) | `docs/spec_registry_schema.ttl` (output file) | rdflib triple count (deterministic) + targeted triple-existence check | operator-blind (rdflib library; no operator judgment) |
| 2 | §1 row 2 (SHACL parseable + 3 shapes) | `docs/spec_registry_shapes.shacl.ttl` (output file) | rdflib triple count + IRI presence count | operator-blind |
| 3 | §1 row 3 (discipline doc structure) | `docs/spec_authoring_discipline.md` (output file) | `grep -c "^### Operation"` count + section presence | operator-blind (grep; no operator judgment) |
| 4 | §1 row 4 (3-test-bed smoke PASS) | `outputs/build_runner_events.jsonl` per Metric A (`success_bool=true` write.event count) + `outputs/cross_system_validation_be_a.json` per-test-bed records | count (deterministic; 3 = PASS) | operator-blind (JSONL aggregation; runtime-emit-anchored per build-runner.md §RE quality dimension) |
| 5 | §1 row 5 (SHACL refuses ≥4 violations) | `outputs/be_a_smoke_fixture_nonconforming.ttl` + pyshacl validation output | violation count (deterministic) | operator-blind (pyshacl library) |
| 6 | §1 row 6 (JSONL ≥6 events) | `outputs/build_runner_events.jsonl` | `wc -l` count + per-event-class count | operator-blind (wc + json.loads; no judgment) |

<!-- /gate:acceptance_criteria §2 -->

> Self-assessment is permitted ONLY when no runtime-emit surface exists for
> the threshold AND the assessor declares operator-bias risk explicitly.
> When self-assessment is used, an external verifier role (or independent
> measurement at a second test bed) is required before the verdict can
> be classified PASSED rather than SUGGESTED.

---

## §3 Per-Test-Bed Strengthening (n≥3)

<!-- gate:acceptance_criteria §3 entries:1 -->

A build-class artifact's acceptance is INCONCLUSIVE at n=1 test bed; the
ROADMAP commits the artifact to ≥3 test beds for cross-system multi-instance
evidence. Pre-register per-test-bed evidence here.

| Test bed | Cycle | Expected evidence shape | Evidence threshold per test bed |
|---|---|---|---|
| **TB-1 = AgentContract** (spec_type `cycle16:AgentContract`; e.g., owner=`research-orchestrator`; runtime_emit_event_class=`agent_dispatch_event`; current_status=`cycle16:running`; representative of 9-spec agent_specs surface per OBS-2/HC #52) | Cycle 16 BE-A | Synthetic `cycle16:Spec` written to test graph + SELECT readback returns all 14 fields + SHACL `c6:StatementAccessPermissionShape` polymorphism via subclass inheritance accepts `c6:accessPermission c6:publishable` annotation | UPDATE HTTP 200 + readback HTTP 200 with all 14 field predicates + SHACL conforms=True; recorded in `outputs/cross_system_validation_be_a.json` TB-1 row + `be_a_spec_registry.write.event` row with `test_bed_id="TB-1"` + `success_bool=true` |
| **TB-2 = Schema** (spec_type `cycle16:Schema`; e.g., owner=`cycle_16_be_a_authoring`; runtime_emit_event_class=`validation_event`; current_status=`cycle16:running`; representative of ~5-spec schemas surface per HR §3 H1) | Cycle 16 BE-A | Synthetic `cycle16:Spec` schema written + SELECT readback all 14 fields + SHACL accepts + Wikidata `c6:rank "normal"` annotation accepted via inherited shape | Same UPDATE/readback/SHACL pattern as TB-1 with spec_type=Schema; recorded TB-2 row + write.event with `test_bed_id="TB-2"` |
| **TB-3 = MethodologyCommitment** (DP#26 carve-out test; spec_type `cycle16:MethodologyCommitment`; e.g., owner=`cycle_16_methodology_layer_5`; runtime_emit_event_class=`"n/a — citation-based activation per DP#26"`; current_status=`cycle16:dormant-with-explicit-deferral`; deferral_reason set; representative of ~50+ Layer-5 methodology commitments surface per HR §3 H1) | Cycle 16 BE-A | Synthetic `cycle16:Spec` methodology commitment written + SELECT readback all 14 fields INCLUDING `runtime_emit_event_class = 'n/a — citation-based activation per DP#26'` literal + `deferral_reason` literal + SHACL accepts the `n/a` runtime_emit_event_class value (verify SHACL does NOT enforce specific event class value beyond MIN_COUNT 1 on field 11; carve-out preserved structurally per HR §3d) | Same UPDATE/readback pattern + SHACL conforms=True with `n/a` value accepted; recorded TB-3 row + write.event with `test_bed_id="TB-3"` |

<!-- /gate:acceptance_criteria §3 -->

> [SEED: min_test_beds=3]
> n≥3 test beds is the cross-system multi-instance evidence floor; n=1
> SUPPORTS but is INCONCLUSIVE per the build-class evidence grammar.
> Single-test-bed PASS does NOT close acceptance at the program level.

---

## §4 Failure Shape Diagnostic Grid

When a threshold FAILs, classify the failure shape per this grid:

| Shape | Diagnosis | Disposition path |
|---|---|---|
| **Mechanism-non-transfer** | The mechanism that the artifact imports from external source does not operate the same way in target domain | Refute the import; record in [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md); do NOT propose a "tighter threshold" patch |
| **Pre-condition violation** | Acceptance ran with a pre-condition not held; measurement is uninterpretable | Re-run with pre-condition restored; do NOT classify the FAIL as evidence |
| **Side-effect drift** | Artifact had effects outside [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §4 declared surface | Tighten contract; re-run acceptance; record drift in BUILD_DECISION_LOG |
| **Baseline-instability** | Baseline reference (§0) was not stable during measurement window | Restore baseline-stability or expand measurement window; record |
| **Genuine acceptance miss** | All above ruled out; artifact did not meet threshold | Classify FAILS-WITH-DIAGNOSED-SHAPE with which mechanism missed; record in BUILD_DECISION_LOG |

> The diagnostic grid prevents "we'll loosen the threshold" repair shape.
> When acceptance FAILs, a *diagnosed* failure is the build-class deliverable;
> a relaxed threshold is a patch that hides the failure.

---

## §5 Honest Resolution Log

| # | Threshold | Verdict | Diagnosis (if FAIL) | Cycle resolved at | Evidence link |
|---|---|---|---|---|---|
| 1 | §1 row 1 (TTL parseable) | (filled at BE-A close-smoke; PASS expected) | — | Cycle 16 BE-A | `docs/spec_registry_schema.ttl` + BUILD_DECISION_LOG §1 verdict row |
| 2 | §1 row 2 (SHACL parseable) | (filled at BE-A close-smoke; PASS expected) | — | Cycle 16 BE-A | `docs/spec_registry_shapes.shacl.ttl` + BUILD_DECISION_LOG §1 verdict row |
| 3 | §1 row 3 (discipline doc) | (filled at BE-A close-smoke; PASS expected) | — | Cycle 16 BE-A | `docs/spec_authoring_discipline.md` + BUILD_DECISION_LOG §1 verdict row |
| 4 | §1 row 4 (3-test-bed smoke) | (filled at BE-A close-smoke) | — | Cycle 16 BE-A | `outputs/cross_system_validation_be_a.json` + JSONL write.event rows |
| 5 | §1 row 5 (SHACL refuses ≥4) | (filled at BE-A close-smoke) | — | Cycle 16 BE-A | `outputs/be_a_smoke_fixture_nonconforming.ttl` + pyshacl violation output |
| 6 | §1 row 6 (JSONL ≥6 events) | (filled at BE-A close-yield) | — | Cycle 16 BE-A | `outputs/build_runner_events.jsonl` |

**Per-H assessment at BE-A close** (per `build-runner.md §Honest Resolution Log` + HR §3):

- **H1** (spec inventory enumeration): PARTIAL at BE-A — only 3 synthetic test specs written (TB-1+TB-2+TB-3); full inventory ≥N≈90-100 is BE-D Phase 5 retroactive scan scope. BE-A surfaces the WRITE-PATH operational; H1 enumeration evidence DEFERRED to BE-D.
- **H2** (per-class operational definitions): PARTIAL at BE-A — 3 of 4 spec-classes covered as test beds (AgentContract + Schema + MethodologyCommitment); DesignDecision class operational definition DEFERRED to BE-D retroactive scan + H6 BE-C gate-script. BE-A surfaces that 3-of-4 classes operationally accept the 14-field schema via SHACL.
- **H5** (substrate coverage): REVISED per Rex disposition (C) D-S2-1 2026-05-27 — KT-1 DOES NOT FIRE under refined mechanism-layer metric (substrate availability ≠ mechanism redundancy). BE-A inherits Cycle 6 BE#1 substrate primitives operationally (Path α RECOMMENDED per substrate §3); inheritance surface verified at smoke (SHACL polymorphism via subclass).
- **H6** (predicate extension clean): CONFIRMATION CANDIDATE at BE-A IF subclass inheritance accepts polymorphism via `cycle16:Spec rdfs:subClassOf c6:Statement` — surface verifiable at TB-1+TB-2+TB-3 smoke test. If Path β fallback required (SHACL polymorphism rejects), H6 PARTIAL at BE-A; KT-4 candidate surface for BE-C disposition.
- **H7** (0 author refusals): CONFIRMATION CANDIDATE at BE-A IF this BE-A authoring itself produces 0 refusals at the spec-authoring discipline gate body (forward-apply dogfooding: BE-A is the first spec authored under the discipline). BE-A close-smoke fires write.event with success_bool=true ≥3 times = 0 refusals at the AUTHORING boundary for BE-A's own 3 synthetic test specs.

> Resolution log is APPEND-ONLY. Verdicts are never edited; corrections
> emit new rows that supersede prior verdicts (with explicit supersede ref).

---

## §6 Self-test (BEFORE running acceptance)

| # | Check | Status |
|---|---|---|
| 1 | Every §1 threshold is deterministic count-based or numeric (no qualitative "improves") | [x] (6 rows: all deterministic — triple count + parse error count + grep count + HTTP status + violation count + line count) |
| 2 | Pre-registration commit (§0) lands BEFORE artifact run for measurement | [x] (Step 3 ACCEPTANCE_CRITERIA fill BINDS at this Step 3 BEFORE Step 4 artifact production per build-runner.md §Rules + §0 pre-registration discipline; commit recorded at Cycle-16-S3 close paired-commit) |
| 3 | Every §1 threshold maps to ≥1 [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §2 post-condition | [x] (1:1 mapping: §1 rows 1-6 ↔ ARTIFACT_CONTRACT §2 rows 1-6) |
| 4 | §2 measurement protocol resolves to runtime-emit OR output-file OR cross-system event log (NOT operator self-assessment alone) | [x] (all 6 rows resolve to output-file OR JSONL runtime-emit — no operator judgment) |
| 5 | §3 per-test-bed strengthening commits ≥3 test beds | [x] (TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment per HYBRID PRIMARY cell granularity 4×4×5; 4th spec-class DesignDecision deferred to BE-D per ROADMAP Phase 5) |
| 6 | §4 failure-shape grid is referenced (not absent) when any §1 threshold has VERDICT=FAIL | [x] (5-class grid pre-populated; per-class disposition path documented; BE-A close-smoke verdicts will reference grid if FAIL) |

> If any check is `[ ]`, halt-and-surface; do NOT proceed to acceptance verdict.
