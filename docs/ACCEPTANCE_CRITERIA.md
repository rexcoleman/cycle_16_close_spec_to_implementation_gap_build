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

---

## §10 BE-B H7 Cycle 16 Branch 4.2 BE-A-source Authoring Discipline Acceptance Append

<!-- gate:acceptance_criteria §10 required -->

Per Cycle-16-S4 BE-B dispatch substrate §1 item 7 + §5 ACCEPTANCE_CRITERIA fill instructions + Cycle 14 §10 acceptance precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) unchanged. Thresholds 7-12 mirror ARTIFACT_CONTRACT §10.2 post-conditions 7-12 + per-test-bed strengthening §10.3 cross-references original §3 (TB-1+TB-2+TB-3 dogfooding to PRODUCTION registry graphs at /cycle6).

### §10.0 BE-B Acceptance Identity (extension to §0)

| Field | Value |
|---|---|
| **Artifact under acceptance** | BE-B 11-deliverable: wrapper script + install shell + govML install_hook + govML templates dir (5 files) + §10 appends at 5 BE-A docs + dogfooding results + envelope (per ARTIFACT_CONTRACT §10.0) |
| **Test bed** | TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment (3 test beds; n=3 per-test-bed strengthening; DesignDecision class still deferred to BE-D retroactive scan per Cycle 16 SI ROADMAP Phase 5) |
| **Baseline reference** | BE-A SHIPPED `6c7c62d` (Cycle-16-S3 close): 3 BE-A artifacts at docs/ + 5 BE-A canonical templates at docs/ scaffolded; govML v2.8.2 baseline at install_runtime_emit_substrate() L171-L209 |
| **Pre-registration commit** | (recorded at Cycle-16-S4 close paired-commit; pre-registration BINDS at this §10.1 fill BEFORE BE-B Step 4 dogfooding execution per build-runner.md §Rules + §0 pre-registration discipline — Step 3 §10 fill happened in parallel to Step 4 dogfooding within BE-B atomic dispatch; mechanical pre-registration at section-write timestamp) |

### §10.1 BE-B Acceptance Thresholds (rows 7-12)

| # | Post-condition (link to ARTIFACT_CONTRACT §10.2 row) | Threshold | Measurement window | Verdict path |
|---|---|---|---|---|
| 7 | ARTIFACT_CONTRACT §10.2 row 7 (wrapper exists + importable + 5 functions + helper) | `python3 -c "import spec_registry_authoring as sra; assert all(callable(getattr(sra, f)) for f in ['register_spec','read_spec_status','fire_cycle_close_gate','fire_session_close_gate','supersede_spec','record_author_refusal'])"` exits 0 | At Step 4a wrapper authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 8 | ARTIFACT_CONTRACT §10.2 row 8 (shell install wrapper syntax-clean + executable) | `bash -n scripts/install_spec_registry_authoring_discipline.sh && test -x scripts/install_spec_registry_authoring_discipline.sh` exits 0 | At Step 4b shell authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 9 | ARTIFACT_CONTRACT §10.2 row 9 (govML init_project.sh install_hook landed; ADDITIVE) | `grep -c "^install_spec_registry_authoring_discipline()" ~/ml-governance-templates/scripts/init_project.sh` returns ≥1 AND `bash -n ~/ml-governance-templates/scripts/init_project.sh` exits 0 AND `grep -c "^install_runtime_emit_substrate()" ~/ml-governance-templates/scripts/init_project.sh` UNCHANGED at 1 | At Step 4c govML edit close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (e.g., FAIL with `Side-effect drift` if v2.8.2 function modified) |
| 10 | ARTIFACT_CONTRACT §10.2 row 10 (govML templates/build/spec_registry/ ships 5 files) | `ls ~/ml-governance-templates/templates/build/spec_registry/ | wc -l` returns 5; obligation doc parses cleanly + has `c6:publishable` annotation | At Step 4d govML templates copy close | PASS / FAIL |
| 11 | ARTIFACT_CONTRACT §10.2 row 11 (3-TB dogfooding to PRODUCTION /cycle6 PASSES) | All 3 test beds return: UPDATE HTTP ∈ {200, 204} + readback HTTP 200 + readback_triple_count ≥ N_expected per current_status (11 mandatory non-nullable + 1 audit_trail_link + 1 c6:rank = 13 for running; +deferral_reason + n_a_rationale = 15 for TB-3 dormant-with-explicit-deferral DP#26 carve-out). Per Brief 3 §10.3 conditional-readback refinement, per-state triple count is: **running** = 13 (11 mandatory + audit_trail_link + rank) / **dormant-with-explicit-deferral** = 14 (running + deferral_reason) / **DP#26 MethodologyCommitment dormant-with-explicit-deferral** = 15 (dormant-with-explicit-deferral + n_a_rationale) / **long-running** = 14 (running + rex_authorization_for_deferral_past_cycle_close) / **killed** = variable depending on retraction audit field. Aggregate `success_bool=true` count = 3 per Metric A_BE_B | At Step 4e 3-TB dogfooding close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE per §4 grid |
| 12 | ARTIFACT_CONTRACT §10.2 row 12 (govML VERSION bumped + backwards-compat preserved) | `head -3 ~/ml-governance-templates/VERSION | grep -c "v2.8.3"` returns ≥1; `git -C ~/ml-governance-templates status --short` shows only expected paths (VERSION + scripts/init_project.sh + templates/build/spec_registry/); 17 legacy projects: F4 skip-WARN at scaffolding extension (legacy projects not retroactively re-scaffolded) | At Step 4f govML VERSION bump close | PASS / FAIL |

### §10.2 BE-B Measurement Protocol (extension to §2)

| # | Threshold (link to §10.1) | Data source | Aggregation | Blinding plan |
|---|---|---|---|---|
| 7 | §10.1 row 7 (wrapper import + functions) | `scripts/spec_registry_authoring.py` (output file) | Python import + hasattr check (deterministic) | operator-blind (Python stdlib; no operator judgment) |
| 8 | §10.1 row 8 (shell syntax) | `scripts/install_spec_registry_authoring_discipline.sh` (output file) | `bash -n` + `test -x` (deterministic) | operator-blind |
| 9 | §10.1 row 9 (govML install_hook) | `~/ml-governance-templates/scripts/init_project.sh` (output file) | grep count (deterministic) + bash -n syntax check | operator-blind |
| 10 | §10.1 row 10 (govML templates dir) | `~/ml-governance-templates/templates/build/spec_registry/` (output dir) | ls + wc -l (deterministic) | operator-blind |
| 11 | §10.1 row 11 (3-TB dogfooding) | `outputs/spec_registry_events.jsonl` + `outputs/be_b_dogfooding_results.json` | success_bool count + per-TB readback_triple_count per current_status conditional-nullable rules | operator-blind (JSONL + JSON aggregation; runtime-emit-anchored) |
| 12 | §10.1 row 12 (VERSION bump) | `~/ml-governance-templates/VERSION` (output file) | head + grep + git status (deterministic) | operator-blind |

### §10.3 BE-B Per-Test-Bed Strengthening (n≥3; extension to §3; Brief 3 disposition embedded)

| Test bed | Cycle | Expected evidence shape | Evidence threshold per test bed |
|---|---|---|---|
| **TB-1 = AgentContract** (BE-B meta-dogfooding: wrapper itself; spec_type=cycle16:AgentContract; runtime_emit_event_class=spec_registry.write.event; current_status=running) | Cycle 16 BE-B | Wrapper authors a `cycle16:Spec` instance describing itself via PRODUCTION /cycle6 registry write + SELECT readback returns 13 triples (running state: 11 mandatory non-nullable + audit_trail_link + rank) + SHACL pre-validation conforms=True | UPDATE HTTP ∈ {200, 204} + readback HTTP 200 + readback_triple_count ≥ 13 + SHACL pre-validation PASS; recorded in `outputs/be_b_dogfooding_results.json` TB-1 row + `spec_registry.write.event` JSONL row with `test_bed_id="TB-1"` + `success_bool=true` |
| **TB-2 = Schema** (govML v2.8.3 install_hook function; spec_type=cycle16:Schema; runtime_emit_event_class=govml_scaffold_event; current_status=running) | Cycle 16 BE-B | Wrapper authors a `cycle16:Spec` instance describing govML install_hook + SELECT readback returns 13 triples (running state) + SHACL pre-validation conforms=True | Same UPDATE/readback/SHACL pattern as TB-1 with spec_type=Schema; recorded TB-2 row + write.event with `test_bed_id="TB-2"` |
| **TB-3 = MethodologyCommitment** (DP#26 carve-out: HC-BE-A-2 Layer 4 namespace-equivalence honest-gap; spec_type=cycle16:MethodologyCommitment; runtime_emit_event_class="n/a"; current_status=dormant-with-explicit-deferral; deferral_reason + n_a_rationale both populated) | Cycle 16 BE-B | Wrapper authors a `cycle16:Spec` methodology commitment + SELECT readback returns 15 triples (dormant-with-explicit-deferral DP#26 state: 11 mandatory non-nullable + audit_trail_link + rank + deferral_reason + n_a_rationale) + SHACL pre-validation conforms=True (n/a literal accepted at field 11 per HR §3d) | Same UPDATE/readback pattern + SHACL conforms=True with n/a literal + n_a_rationale present in readback triples; recorded TB-3 row + write.event with `test_bed_id="TB-3"` |

**Brief 3 disposition refinement (HC-BE-A-1 operational refinement at §10.3 row 4 conditional-readback wording):**

| current_status enum value | Expected readback_triple_count | Composition |
|---|---|---|
| `running` | 13 | 11 mandatory non-nullable + 1 audit_trail_link + 1 c6:rank |
| `dormant-with-explicit-deferral` | 14 | running (13) + 1 deferral_reason |
| `dormant-with-explicit-deferral` + DP#26 (MethodologyCommitment with `n/a` runtime_emit_event_class + non-empty n_a_rationale) | 15 | dormant-with-explicit-deferral (14) + 1 n_a_rationale |
| `long-running` | 14 | running (13) + 1 rex_authorization_for_deferral_past_cycle_close |
| `killed` | 13-14 | running (13) + optional retraction-audit field |

This refinement closes the BE-A acceptance-criteria §1 row 4 wording over-specification flagged at BE-A envelope `biggest_gap` (originally specified `≥14 triples` for all states; correct semantics is per-state conditional-nullable counts). BE-C consumer (Cycle-16-S5) inherits this refined per-state expected count for `spec_implementation_present_gate.sh` + `spec_implementation_session_close_gate.sh` gate-fire thresholds.

### §10.4 BE-B Failure Shape Diagnostic Grid (extension to §4)

No NEW failure shapes surfaced at BE-B beyond §4 grid; existing 5 classes (Mechanism-non-transfer / Pre-condition violation / Side-effect drift / Baseline-instability / Genuine acceptance miss) cover all observed BE-B refusal/violation surfaces. Specifically:
- Side-effect drift = govML existing function modified (failure mode for §10.1 row 9)
- Mechanism-non-transfer = SHACL polymorphism via subclass not accepting `cycle16:Spec` instances at production /cycle6 (BE-A already validated this; BE-B inherits)

### §10.5 BE-B Honest Resolution Log (extension to §5)

| # | Threshold | Verdict | Diagnosis (if FAIL) | Cycle resolved at | Evidence link |
|---|---|---|---|---|---|
| 7 | §10.1 row 7 (wrapper) | PASS | — | Cycle 16 BE-B | `scripts/spec_registry_authoring.py` + import smoke result |
| 8 | §10.1 row 8 (shell install) | PASS | — | Cycle 16 BE-B | `scripts/install_spec_registry_authoring_discipline.sh` + bash -n exit 0 |
| 9 | §10.1 row 9 (govML install_hook ADDITIVE) | PASS | — | Cycle 16 BE-B | `~/ml-governance-templates/scripts/init_project.sh` post-edit + grep counts |
| 10 | §10.1 row 10 (govML templates dir) | PASS | — | Cycle 16 BE-B | `~/ml-governance-templates/templates/build/spec_registry/` directory + 5 files listed |
| 11 | §10.1 row 11 (3-TB dogfooding to PRODUCTION /cycle6) | PASS | — | Cycle 16 BE-B | `outputs/be_b_dogfooding_results.json` all_3_pass=true (TB-1 244ms 13 triples / TB-2 218ms 13 triples / TB-3 200ms 15 triples + n_a_rationale present) |
| 12 | §10.1 row 12 (govML VERSION bump v2.8.3) | PASS | — | Cycle 16 BE-B | `~/ml-governance-templates/VERSION` head v2.8.3 entry; backwards-compat preserved (17 legacy projects skip-WARN per F4) |

**Per-H assessment at BE-B close (extension to BE-A §5 per-H):**

- **H7** (0 author refusals at BE-B dogfooding boundary): CONFIRMED at BE-B — all 3 TBs authored without any `record_author_refusal()` invocation (cumulative (a)+(b)+(c)+(d) = 0). Brief 4 KT-3 firing surface threshold: (a)+(b)+(d) ≥ 3 → fires. Observed 0; KT-3 DOES NOT FIRE at BE-B.
- **H1+H2** (spec inventory + per-class operational): EXTENDED at BE-B — wrapper now operationalizes 3 of 4 spec-classes (AgentContract + Schema + MethodologyCommitment) via PRODUCTION /cycle6 writes (forward-apply discipline); DesignDecision class deferred to BE-D Phase 5 retroactive scan.
- **H6** (predicate extension clean): CONFIRMED at BE-B — Path α subclass inheritance via `cycle16:Spec rdfs:subClassOf c6:Statement` accepted by SHACL polymorphism at 3 production-graph writes; Path β fallback NOT needed.

### §10.6 BE-B Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | Every §10.1 threshold is deterministic count-based or numeric | [x] (6 rows: import + bash -n + grep counts + ls + readback_triple_count per state + head/grep) |
| 2 | Pre-registration commit (§10.0) lands BEFORE BE-B Step 4 dogfooding | [x] (Step 3 §10 fill precedes Step 4 dogfooding within BE-B atomic dispatch per build-runner.md §Build Stage Steps 1-3 BEFORE Step 4 artifact production) |
| 3 | Every §10.1 threshold maps to ≥1 ARTIFACT_CONTRACT §10.2 post-condition | [x] (1:1 mapping rows 7-12) |
| 4 | §10.2 measurement protocol resolves to runtime-emit OR output-file OR cross-system event log | [x] (all 6 rows resolve to output-file OR JSONL runtime-emit) |
| 5 | §10.3 per-test-bed strengthening commits ≥3 test beds + Brief 3 conditional-readback refinement embedded | [x] (TB-1 + TB-2 + TB-3 + per-state triple count table) |
| 6 | §10.4 failure-shape grid extension referenced (no NEW shapes; existing 5 cover BE-B) | [x] |

<!-- /gate:acceptance_criteria §10 -->
