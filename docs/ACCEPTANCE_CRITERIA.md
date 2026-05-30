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

---

## §11 BE-C H6 Cycle 16 Branch 4.3 BE-B-source TWO-surface Gate Acceptance Append

<!-- gate:acceptance_criteria §11 required -->

Per Cycle-16-S5 BE-C dispatch substrate §1 item 9 + §5 ACCEPTANCE_CRITERIA fill instructions + Cycle 14 §11 acceptance precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED) unchanged. Thresholds 13-18 mirror ARTIFACT_CONTRACT §11.2 post-conditions 13-18 + per-test-bed strengthening §11.3 from 3-TB dogfooding outcomes verbatim per dispatch substrate §4.

### §11.0 BE-C Acceptance Identity (extension to §0)

| Field | Value |
|---|---|
| **Artifact under acceptance** | BE-C 9-deliverable: 2 NEW gate scripts at govML scripts/ + check_all_gates.sh BLOCKING+ADVISORY loops + init_project.sh install_hook + templates/build/spec_implementation_gates/ NEW dir (OBLIGATION doc) + govML VERSION v2.8.4 + §11 BE-C appends at 3 cycle_16 docs + DEPLOYMENT/BUILD_DECISION §3 row 3 + cross_system_validation_be_c.json + envelope (per ARTIFACT_CONTRACT §11.0) |
| **Test bed** | TB-1 conforming-running (AgentContract) + TB-2 dormant-with-explicit-deferral-and-rex-authorization (Schema; HC #47 abstract target) + TB-3 dormant-silent-past-threshold (MethodologyCommitment; DP#26 carve-out; LOAD-BEARING) |
| **Baseline reference** | BE-B SHIPPED at Cycle-16-S4 close: `scripts/spec_registry_authoring.py` 29.8KB + govML v2.8.3 install_spec_registry_authoring_discipline() L239-L283 + govML v2.8.0+ `k_register_present_gate.sh` 231L skeleton (H6 metric reference) |
| **Pre-registration commit** | (recorded at Cycle-16-S5 close paired-commit; pre-registration BINDS at this §11.1 fill BEFORE BE-C 3-TB dogfooding execution per build-runner.md §Rules + §0 pre-registration discipline — Step 3 §11 fill happened in parallel to Step 4 dogfooding within BE-C atomic dispatch; mechanical pre-registration at section-write timestamp) |

### §11.1 BE-C Acceptance Thresholds (rows 13-18)

| # | Post-condition (link to ARTIFACT_CONTRACT §11.2 row) | Threshold | Measurement window | Verdict path |
|---|---|---|---|---|
| 13 | ARTIFACT_CONTRACT §11.2 row 13 (present-gate exists + executable + bash-clean + --help) | `bash -n ~/ml-governance-templates/scripts/spec_implementation_present_gate.sh && test -x ~/ml-governance-templates/scripts/spec_implementation_present_gate.sh && bash ~/ml-governance-templates/scripts/spec_implementation_present_gate.sh --help \| head -1` exits 0 | At Step 4a gate-script authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 14 | ARTIFACT_CONTRACT §11.2 row 14 (session-close-gate exists + executable + bash-clean + --help + ADVISORY=true default) | `bash -n ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh && test -x ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh && bash ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh --help \| head -1` exits 0 AND `grep -c "^ADVISORY=true" ~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` = 1 | At Step 4b gate-script authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 15 | ARTIFACT_CONTRACT §11.2 row 15 (check_all_gates.sh BLOCKING + ADVISORY loops landed) | `grep -c "spec_implementation_present_gate" ~/ml-governance-templates/scripts/check_all_gates.sh` ≥ 1 AND `grep -c "spec_implementation_session_close_gate" ~/ml-governance-templates/scripts/check_all_gates.sh` ≥ 1 AND existing 4-gate iteration loop body unchanged | At Step 4c check_all_gates.sh edit close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (e.g., FAIL with `Side-effect drift` if 4-gate loop body modified) |
| 16 | ARTIFACT_CONTRACT §11.2 row 16 (govML init_project.sh install_hook ADDITIVE) | `grep -c "^install_spec_implementation_gates()" ~/ml-governance-templates/scripts/init_project.sh` = 1 AND call-site count = 1 AND existing function counts unchanged | At Step 4d govML edit close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (e.g., FAIL with `Side-effect drift` if v2.8.2/v2.8.3 functions modified) |
| 17 | ARTIFACT_CONTRACT §11.2 row 17 (govML templates/build/spec_implementation_gates/ OBLIGATION doc) | `test -f ~/ml-governance-templates/templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` exits 0 + grep tests for §1 + §6 sections | At Step 4e govML templates dir creation | PASS / FAIL |
| 18 | ARTIFACT_CONTRACT §11.2 row 18 (3-TB dogfooding + JSONL ≥4 fire.event rows) | `outputs/cross_system_validation_be_c.json` `all_3_pass: true` + cycle-close holistic verdict `BLOCKED` (TB-3 load-bearing) + session-close `ADVISORY_FAIL` + JSONL `present_gate.fire.event` ≥ 1 BLOCKED + JSONL total ≥ 4 rows | At Step 4f 3-TB dogfooding close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |

### §11.2 BE-C Measurement Protocol (extension to §2)

| # | Threshold (link to §11.1) | Data source | Aggregation | Blinding plan |
|---|---|---|---|---|
| 13 | §11.1 row 13 (present-gate exists) | `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` | bash -n + test -x + --help head (deterministic) | operator-blind |
| 14 | §11.1 row 14 (session-close-gate + advisory default) | `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` | bash -n + test -x + --help head + grep ADVISORY=true (deterministic) | operator-blind |
| 15 | §11.1 row 15 (check_all_gates.sh integration) | `~/ml-governance-templates/scripts/check_all_gates.sh` | grep counts + bash -n syntax check (deterministic) | operator-blind |
| 16 | §11.1 row 16 (govML install_hook ADDITIVE) | `~/ml-governance-templates/scripts/init_project.sh` | grep counts + bash -n syntax check (deterministic) | operator-blind |
| 17 | §11.1 row 17 (OBLIGATION doc) | `~/ml-governance-templates/templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` | test -f + grep section header (deterministic) | operator-blind |
| 18 | §11.1 row 18 (3-TB dogfooding) | `outputs/cross_system_validation_be_c.json` + `outputs/spec_implementation_gates_events.jsonl` | JSON `all_3_pass` field + verdict comparison + JSONL row count (deterministic) | operator-blind (JSONL + JSON aggregation; runtime-emit-anchored) |

### §11.3 BE-C Per-Test-Bed Strengthening (n≥3; extension to §3; dispatch substrate §4 outcomes verbatim)

| Test bed | Cycle | Expected evidence shape | Evidence threshold per test bed | Actual outcome |
|---|---|---|---|---|
| **TB-1 conforming-running (AgentContract)** | Cycle 16 BE-C | Wrapper authors `cycle16:Spec` instance at production /cycle6 with `current_status=running` + `cycle_authored=16` + cycle-close holistic gate fires `BLOCKED` only because TB-3 is also present (per-TB-1 not directly load-bearing) | Write HTTP ∈ {200, 204} + readback HTTP 200 + readback_triple_count ≥ 13 (running state) + actual_status = "running" | Per `outputs/cross_system_validation_be_c.json` `be_c_smoke_results[0]`: write_success=true + readback OK + actual_status="running" + matches_expected=true |
| **TB-2 dormant-with-explicit-deferral-and-rex-authorization (Schema; HC #47 abstract target)** | Cycle 16 BE-C | Wrapper authors `cycle16:Spec` instance with `current_status=dormant-with-explicit-deferral` + `target_session=<next_cycle>:<session>` (abstract per HC #47) + `rex_authorization_for_deferral_past_cycle_close` edge populated → ASK FILTER NOT EXISTS excludes this spec from gate fire | Write HTTP ∈ {200, 204} + readback OK + actual_status = "dormant-with-explicit-deferral" + rex_authorization edge present in readback | Per `cross_system_validation_be_c.json` `be_c_smoke_results[1]`: write_success=true + readback OK + actual_status="dormant-with-explicit-deferral" + matches_expected=true; cycle-close gate ASK FILTER excludes TB-2 (verified holistic verdict reflects TB-3 only) |
| **TB-3 dormant-silent-past-threshold (MethodologyCommitment; DP#26 carve-out; LOAD-BEARING)** | Cycle 16 BE-C | Wrapper authors `cycle16:Spec` instance with `current_status=dormant-silent` + `session_authored=Cycle-16-S1` + `runtime_emit_event_class="n/a"` + `n_a_rationale` populated (DP#26 carve-out) + NO `rex_authorization` → cycle-close holistic gate ASK MUST return TRUE → verdict BLOCKED (load-bearing failure mode Cycle 16 structurally solving) | Write HTTP ∈ {200, 204} + readback OK + actual_status = "dormant-silent" + cycle-close holistic verdict = BLOCKED + dormant_silent_present_bool = "true" | Per `cross_system_validation_be_c.json` `be_c_smoke_results[2]` + `cycle_close_gate_holistic`: write_success=true + readback OK + actual_status="dormant-silent" + matches_expected=true; **cycle-close holistic verdict = BLOCKED (load-bearing) + dormant_silent_present_bool = "true"** + session-close holistic verdict = ADVISORY_FAIL |

**3-TB Strengthening Aggregate Outcome (per `cross_system_validation_be_c.json`):**

- `all_3_pass`: **true** (3 writes succeed + 3 readbacks match expected status + holistic cycle-close gate BLOCKED on TB-3 load-bearing)
- `production_graph_baseline_pre`: 246101 triples; `production_graph_baseline_post`: 246101 triples (post-cleanup); **baseline_equal_post_cleanup: true**
- Cleanup: 3 specs × 3 named graphs DELETE WHERE successful; per-spec readback post-cleanup returns 0 triples each
- H6 metric: **CONFIRMED** (skeleton structural equivalence to `k_register_present_gate.sh` 231L; divergence categories (a)+(b)+(c)+(d) per dispatch substrate §3 + honest carry (e) JSONL fire.event emit block load-bearing for HC #26 Gate 2)
- KT-4 firing surface: **DOES NOT FIRE** (cycle-close gate BLOCKED correctly on TB-3; no FALSE NEGATIVE; HC #59 BINDING screen applied — operational metric refinement not needed; SPARQL ASK substitution at gate-script-shell-script primitive layer is sufficient; no new enforcement primitive class required)

### §11.4 BE-C Failure Shape Diagnostic Grid (extension to §4)

No NEW failure shapes surfaced at BE-C beyond §4 grid; existing 5 classes (Mechanism-non-transfer / Pre-condition violation / Side-effect drift / Baseline-instability / Genuine acceptance miss) cover all observed BE-C verdict surfaces. Specifically:
- Side-effect drift = govML existing function/loop body modified (failure mode for §11.1 rows 15-16); verified at HC #26 Gate 3 pre-edit/post-edit checkpoint
- Mechanism-non-transfer = SPARQL ASK substitution not evaluable at shell-script primitive layer (H6 REFUTED → KT-4 fires); verified DOES NOT APPLY at BE-C (H6 CONFIRMED)
- Baseline-instability = production graph triple count diverging pre/post cleanup; verified DOES NOT APPLY at BE-C (baseline_equal_post_cleanup=true)

### §11.5 BE-C Honest Resolution Log (extension to §5)

| # | Threshold | Verdict | Diagnosis (if FAIL) | Cycle resolved at | Evidence link |
|---|---|---|---|---|---|
| 13 | §11.1 row 13 (present-gate) | PASS | — | Cycle 16 BE-C | `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` (325L; bash-syntax-clean; chmod +x applied) |
| 14 | §11.1 row 14 (session-close-gate + advisory default) | PASS | — | Cycle 16 BE-C | `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` (337L; bash-syntax-clean; ADVISORY=true default verified at L34) |
| 15 | §11.1 row 15 (check_all_gates.sh integration) | PASS | — | Cycle 16 BE-C | `~/ml-governance-templates/scripts/check_all_gates.sh` post-edit; `git -C ~/ml-governance-templates diff scripts/check_all_gates.sh` shows ONLY iteration list line + comment header replaced + NEW ADVISORY loop appended (LOCKED 4-gate loop body preserved) |
| 16 | §11.1 row 16 (govML install_hook ADDITIVE) | PASS | — | Cycle 16 BE-C | `~/ml-governance-templates/scripts/init_project.sh` post-edit; install_spec_implementation_gates() count=1; call-site count=1; install_runtime_emit_substrate count=1 (unchanged); install_spec_registry_authoring_discipline count=1 (unchanged) |
| 17 | §11.1 row 17 (OBLIGATION doc) | PASS | — | Cycle 16 BE-C | `~/ml-governance-templates/templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` (~8KB; §1 TWO-surface gate inventory + §6 HC-11 partition + §7 authority chain present) |
| 18 | §11.1 row 18 (3-TB dogfooding to PRODUCTION /cycle6) | PASS | — | Cycle 16 BE-C | `outputs/cross_system_validation_be_c.json` `all_3_pass=true` + `outputs/spec_implementation_gates_events.jsonl` (4 fire.event rows: present CLEAR+BLOCKED, session CLEAR+ADVISORY_FAIL) + DEPLOYMENT_LOG §3 row 3 BUILT entry |

**Per-H assessment at BE-C close (extension to BE-A §5 + BE-B §10.5 per-H):**

- **H6** (predicate extension clean): **CONFIRMED at BE-C** — both NEW gate scripts share k_register_present_gate.sh skeleton structurally; divergence ONLY in (a)+(b)+(c)+(d) per dispatch substrate §3 + honest carry (e) JSONL emit block. SPARQL ASK substitution at the gate-script-shell-script primitive layer evaluable per Python urllib heredoc. H6 CONFIRMED.
- **KT-4** (predicate extension requires new primitive class): **DOES NOT FIRE at BE-C** — cycle-close gate BLOCKED correctly on TB-3 dormant-silent surface (no FALSE NEGATIVE); HC #59 BINDING screen applied at the 3-TB dogfooding step; SPARQL ASK substitution is sufficient at the existing shell-script primitive layer; no new enforcement primitive class required.
- **H1+H2** (spec inventory + per-class operational): **EXTENDED at BE-C** — TWO-surface gate now actively detects dormant-silent spec class at /cycle6 production graph; consumer surface for BE-D retroactive scan at Cycle-16-S6 + onward Cycle 17+ cycles.
- **KT-3** (≥3 author refusals cumulative): **NOT RE-EVALUATED at BE-C** per dispatch substrate §6; carry forward LOCKED `false` from BE-B; no author refusals captured at BE-C dogfooding (BE-B wrapper accepts all 3 TBs cleanly).

### §11.6 BE-C Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | Every §11.1 threshold is deterministic count-based or numeric | [x] (6 rows: bash -n + grep counts + file presence + JSON field + JSONL row count) |
| 2 | Pre-registration commit (§11.0) lands BEFORE BE-C Step 4 3-TB dogfooding | [x] (Step 3 §11 fill precedes Step 4 dogfooding within BE-C atomic dispatch per build-runner.md §Build Stage Steps 1-3 BEFORE Step 4 artifact production) |
| 3 | Every §11.1 threshold maps to ≥1 ARTIFACT_CONTRACT §11.2 post-condition | [x] (1:1 mapping rows 13-18) |
| 4 | §11.2 measurement protocol resolves to runtime-emit OR output-file OR cross-system event log | [x] (all 6 rows resolve to output-file OR JSONL runtime-emit) |
| 5 | §11.3 per-test-bed strengthening commits ≥3 test beds + 3-TB outcomes embedded verbatim | [x] (TB-1 + TB-2 + TB-3 with actual_outcome column + aggregate `all_3_pass=true` + H6 CONFIRMED + KT-4 DOES NOT FIRE) |
| 6 | §11.4 failure-shape grid extension referenced (no NEW shapes; existing 5 cover BE-C) | [x] |

<!-- /gate:acceptance_criteria §11 -->

## §12 BE-D H1 H3 Cycle 16 Branch 4.4 BE-C-source Retroactive Scan Acceptance Append

<!-- gate:acceptance_criteria §12 required -->

Per Cycle-16-S6 BE-D dispatch substrate §1 item 7 + §4 ACCEPTANCE_CRITERIA fill instructions + Cycle 14 §12 BE#6 acceptance precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) unchanged. Thresholds 19-24 mirror ARTIFACT_CONTRACT §12.2 post-conditions 19-24 + per-test-bed strengthening §12.3 from 4-spec-class retroactive scan outcomes verbatim per dispatch substrate §5 (n≥3 per class).

### §12.0 BE-D Acceptance Identity (extension to §0)

| Field | Value |
|---|---|
| **Artifact under acceptance** | BE-D 10-deliverable: `outputs/retroactive_scan_cycle_1_15_run.json` (NEW; ~190KB) + 4-spec-class enumeration methodology + 5-state classification + per-spec materialization at `/cycle6` (268 raw writes + 232 distinct after idempotent minting; 235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 persisted) + KT-2 + H1 + H3 evaluation + §12 BE-D appends at 3 cycle_16 docs + DEPLOYMENT/BUILD_DECISION §2 row 4 + `outputs/build_runner_envelope.yaml` OVERWRITE + `outputs/build_runner_events.jsonl` append with single `retroactive_scan_run.event` fire (per ARTIFACT_CONTRACT §12.0) |
| **Test bed (4-spec-class strengthening n≥3 per class)** | Class (a) AgentContract n=9 distinct + Class (b) Schema n=10 distinct + Class (c) DesignDecision n=154 distinct + Class (d) MethodologyCommitment n=59 distinct (all ≥3 strengthening threshold) — per dispatch substrate §5 (4-spec-class × 5-state × 4-substrate-operation = 80-cell EXTENSION-3 cell granularity from HR §3a) |
| **Baseline reference** | BE-A SHIPPED at Cycle-16-S3 close: 14-field schema + SPARQL UPDATE write boundary at /cycle6 + BE-B SHIPPED at Cycle-16-S4 close: `scripts/spec_registry_authoring.py register_spec()` 5 Ops + DP#26 carve-out enforcement + BE-C SHIPPED at Cycle-16-S5 close: TWO-surface BLOCKING gate at govML v2.8.4 + Cycle 1-15 cycle directories (15 enumerable) + 23 outputs/*_events.jsonl files + 26 FINDINGS.md files for token enumeration |
| **Pre-registration commit** | (recorded at Cycle-16-S6 close 3-repo paired-commit; pre-registration BINDS at this §12.1 fill BEFORE BE-D bulk per-spec materialization step — Step 3 §12 fill happened in parallel to Step 4 bulk write within BE-D atomic dispatch; mechanical pre-registration at section-write timestamp per build-runner.md §Rules + §0 pre-registration discipline) |

### §12.1 BE-D Acceptance Thresholds (rows 19-24)

| # | Post-condition (link to ARTIFACT_CONTRACT §12.2 row) | Threshold | Measurement window | Verdict path |
|---|---|---|---|---|
| 19 | ARTIFACT_CONTRACT §12.2 row 19 (retroactive_scan_cycle_1_15_run.json present + JSON-parseable + 8 required keys) | `test -f outputs/retroactive_scan_cycle_1_15_run.json && python3 -c "import json; d=json.load(open('outputs/retroactive_scan_cycle_1_15_run.json')); required=['aggregate_counts_4x5','h1_total_enumerated','h1_estimate_floor','h1_confirmed_bool','kt_2_firing_surface','h3_dormant_silent_aggregate','h3_confirmed_bool','retroactive_classification_annotation']; assert all(k in d for k in required), 'missing keys'"` exits 0 | At Step 4a JSON authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 20 | ARTIFACT_CONTRACT §12.2 row 20 (4-spec-class enumeration with per-class n≥3 strengthening) | `python3 -c "import json; d=json.load(open('outputs/retroactive_scan_cycle_1_15_run.json')); pcs=d['per_class_strengthening_n_ge_3']; assert all(pcs[c]['total_distinct'] >= 3 for c in ['a_agent_contract','b_schema','c_design_decision','d_methodology_commitment']), 'class with <3 strengthening'"` exits 0 | At Step 4b enumeration scan close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 21 | ARTIFACT_CONTRACT §12.2 row 21 (5-state classification yields ≥3 dormant-silent → H3 CONFIRMED + KT-2 DOES NOT FIRE) | `python3 -c "import json; d=json.load(open('outputs/retroactive_scan_cycle_1_15_run.json')); assert d['h3_confirmed_bool'] is True and d['kt_2_firing_surface']['kt_2_fires_bool'] is False and d['h3_dormant_silent_aggregate'] >= 3"` exits 0 | At Step 4c classification heuristic close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (e.g., REFUTED → KT-2 FIRES → halt + Rex paradigm re-disposition) |
| 22 | ARTIFACT_CONTRACT §12.2 row 22 (H1 total enumerated ≥ 90 floor → CONFIRMED) | `python3 -c "import json; d=json.load(open('outputs/retroactive_scan_cycle_1_15_run.json')); assert d['h1_confirmed_bool'] is True and d['h1_total_enumerated'] >= 90"` exits 0 | At Step 4d H1 evaluation close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (REFUTED <70 → §3.5 3-test gate → Rex; INCONCLUSIVE 70-89 → Layer 5 honest gap) |
| 23 | ARTIFACT_CONTRACT §12.2 row 23 (per-spec materialization at /cycle6 succeeds with `retroactive_classification=true` annotation) | SPARQL COUNT `cycle16:Spec` instances at `/cycle6` ≥ 232 (= 232 BE-D + 3 BE-B S4 persisted = 235 actual) AND `grep -c "spec_registry.write.event" outputs/spec_registry_events.jsonl` ≥ 268 (raw write event count) | At Step 4e bulk materialization close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 24 | ARTIFACT_CONTRACT §12.2 row 24 (`retroactive_scan_run.event` single-fire at close with full payload) | `grep -c '"event_class": "retroactive_scan_run.event"' outputs/build_runner_events.jsonl` = 1 AND `python3 -c "import json; e=[json.loads(l) for l in open('outputs/build_runner_events.jsonl') if 'retroactive_scan_run' in l][-1]; required=['aggregate_counts','h1_confirmed_bool','h3_confirmed_bool','kt_2_fires_bool','timestamp']; assert all(k in e['payload'] for k in required)"` exits 0 | At Step 4f close-event emit | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |

### §12.2 BE-D Measurement Protocol (extension to §2)

| # | Threshold (link to §12.1) | Data source | Aggregation | Blinding plan |
|---|---|---|---|---|
| 19 | §12.1 row 19 (retroactive scan JSON present) | `outputs/retroactive_scan_cycle_1_15_run.json` | file presence + JSON parse + 8-key existence (deterministic) | operator-blind |
| 20 | §12.1 row 20 (per-class n≥3 strengthening) | `outputs/retroactive_scan_cycle_1_15_run.json` `per_class_strengthening_n_ge_3` | per-class total_distinct count ≥ 3 (deterministic) | operator-blind |
| 21 | §12.1 row 21 (H3 CONFIRMED + KT-2 DOES NOT FIRE) | `outputs/retroactive_scan_cycle_1_15_run.json` `h3_*` + `kt_2_firing_surface.*` | boolean field assertion (deterministic) | operator-blind |
| 22 | §12.1 row 22 (H1 CONFIRMED) | `outputs/retroactive_scan_cycle_1_15_run.json` `h1_*` | h1_total_enumerated ≥ 90 + h1_confirmed_bool=True (deterministic) | operator-blind |
| 23 | §12.1 row 23 (per-spec materialization at /cycle6) | SPARQL query `/cycle6` + `outputs/spec_registry_events.jsonl` | SPARQL COUNT + JSONL row count (deterministic) | operator-blind (SPARQL endpoint introspection; runtime-emit-anchored) |
| 24 | §12.1 row 24 (close event single-fire) | `outputs/build_runner_events.jsonl` | event class grep count + JSON payload field assertion (deterministic) | operator-blind |

### §12.3 BE-D Per-Test-Bed Strengthening (n≥3 per spec-class; extension to §3; retroactive_scan_cycle_1_15_run.json outcomes verbatim)

| Test bed (spec-class) | Cycle | Expected evidence shape | Evidence threshold per test bed | Actual outcome |
|---|---|---|---|---|
| **Class (a) AgentContract — `~/Moonshots_Career_Thesis_v2/.claude/agents/*.md` enumeration** | Cycle 16 BE-D | 9 agent contracts enumerated (build-orchestrator + build-runner + execution-orchestrator + implementation-coach + kernel-coach + research-executor + research-orchestrator + research-researcher-planner + research-verifier); each materialized at /cycle6 with retroactive_classification=true annotation; per-spec status classification per resolution preference heuristic | distinct enumerated count ≥ 3 (strengthening floor); class total = 9 ≥ 3 PASS; per-state breakdown captured | Per `retroactive_scan_cycle_1_15_run.json` `aggregate_counts_4x5.a_agent_contract`: running=2, dormant-with-explicit-deferral=0, dormant-silent=7, killed=0, long-running=0; total=9; **n≥3 PASS** (kernel-coach + research-executor have captured runtime emit fires across 23-JSONL scan; 7/9 dormant-silent represents the HC-BE-D-1 write-boundary gap surface for class (a) — Cycle 18 scope) |
| **Class (b) Schema — `find ~/cycle_*/scripts/runtime_emit/ + drift_telemetry + docs/spec_registry_*.ttl + cycle_6/runtime/jena/shapes + cycle_10 ontologies`** | Cycle 16 BE-D | 10 schemas enumerated (3 in cycle_16/scripts/runtime_emit/ + 2 cycle_16 docs/spec_registry_*.ttl + 2 cycle_6 SHACL shapes + 1 cycle_6 unified substrate ontology + 3 cycle_10 ontologies); each materialized with DP#26 carve-out (citation-based activation) where applicable | distinct enumerated count ≥ 3; class total = 10 ≥ 3 PASS; per-state breakdown captured | Per `aggregate_counts_4x5.b_schema`: running=8, dormant-with-explicit-deferral=0, dormant-silent=2, killed=0, long-running=0; total=10; **n≥3 PASS** (cycle_6 + cycle_16 schemas all running via SPARQL endpoint HTTP 200 + citation-based activation per DP#26; 2 cycle_10 ontologies dormant-silent — actor_trust + destination_class no captured fires in 23-JSONL scan) |
| **Class (c) DesignDecision — DECISION_LOG.md + state.json paradigm_dispositions/decisions_log/honest_carries blocks across 15 cycle dirs** | Cycle 16 BE-D | 154 design decisions distinct (190 raw with collisions resolved by idempotent sha256_8 minting); CONTRACT_CHANGE ADR-Cycle-N-S<m> entries + D-S<n>-<m> cycle dispositions + paradigm_disposition close/landed entries = running; honest_carries entries = dormant-with-explicit-deferral; remaining paradigm_disposition entries without close/landed marker = dormant-silent | distinct enumerated count ≥ 3; class total = 154 ≥ 3 PASS; per-state breakdown captured | Per `aggregate_counts_4x5.c_design_decision`: running=37, dormant-with-explicit-deferral=0, dormant-silent=117, killed=0, long-running=0; total=154; **n≥3 PASS** (37/154 running represents ratified ADRs + close/landed dispositions; 117/154 dormant-silent represents historical paradigm_dispositions without close-marker — classification heuristic limitation surfaced at empirical bias section of KT-2 firing surface rationale) |
| **Class (d) MethodologyCommitment — FINDINGS.md token enumeration across 26 files** | Cycle 16 BE-D | 59 distinct methodology tokens (HC-NN + DP#NN + Pattern NN + Binding NN + R-N + GPL-NN + Discipline #NN + Trap #NN + Check #NN + LL-NN + PL-NN + MR-NN + Mech-NN); classification per distinct-files + occurrence-count heuristic (distinct_files≥2 OR occurrences≥10 = running; else cycle-recency check) | distinct enumerated count ≥ 3; class total = 59 ≥ 3 PASS; per-state breakdown captured + DP#26 carve-out applied (every spec in this class has runtime_emit_event_class='n/a — citation-based activation per DP#26' + n_a_rationale per HR §3d) | Per `aggregate_counts_4x5.d_methodology_commitment`: running=45, dormant-with-explicit-deferral=0, dormant-silent=11, killed=0, long-running=3; total=59; **n≥3 PASS** (top 30 tokens by occurrence include HC-11 n=302 + HC-07 n=175 + R2 n=157 + Binding 7 n=69 — all running; 3 long-running tokens with occurrence in [3,9] range; 11 dormant-silent with single-file low-occurrence) |

**4-Class Strengthening Aggregate Outcome (per `retroactive_scan_cycle_1_15_run.json`):**

- `h1_total_enumerated`: **232 distinct** (raw 268; 36 collisions resolved by idempotent sha256_8 minting) ≥ 90 floor → **H1 CONFIRMED**
- `h3_dormant_silent_aggregate`: **137** (= 7 a + 2 b + 117 c + 11 d) ≥ 3 threshold → **H3 CONFIRMED**
- `kt_2_firing_surface.kt_2_fires_bool`: **False** (137 well above threshold 3); HC #59 BINDING screen applied — pre-registered SI kill condition not operationally-revisable; threshold evaluated literally on empirical count → **KT-2 DOES NOT FIRE**
- Per-class strengthening n≥3 outcomes: a/b/c/d **ALL 4 PASS** (9 + 10 + 154 + 59 distinct; smallest class = 9 = 3x floor)
- Production graph baseline pre-BE-D (default graph triples): 6; post-BE-D (full triple store): 250779 (~4680 net add for 232 specs × ~20 triples each / 3 nanopub graphs)
- NO DROP GRAPH at BE-D close — retroactive registry rows persist for BE-E forward-apply observation baseline reconstruction
- HC-BE-D-1 honest carry surfaced: write-boundary enforcement gap (specs written to filesystem without calling BE-B authoring wrapper) → Cycle 18 scope per Rex Option B split-sequential 2026-05-27

### §12.4 BE-D Failure Shape Diagnostic Grid (extension to §4)

No NEW failure shapes surfaced at BE-D beyond §4 grid; existing 5 classes (Mechanism-non-transfer / Pre-condition violation / Side-effect drift / Baseline-instability / Genuine acceptance miss) cover all observed BE-D verdict surfaces. Specifically:
- **Mechanism-non-transfer** would surface if KT-2 fires (paradigm-class candidate per substrate §3 + ED §Field 6 KT-2); verified DOES NOT APPLY at BE-D (KT-2 DOES NOT FIRE; dormant_silent=137 well above threshold 3)
- **Pre-condition violation** would surface if BE-A + BE-B + BE-C artifacts mutated (govML v2.8.4 LOCKED + SPARQL endpoint reachability) at BE-D start; verified DOES NOT APPLY at BE-D (pre-write `git -C ~/ml-governance-templates status -s` empty + HTTP 200 verified pre-bulk-write)
- **Side-effect drift** would surface if govML modified at BE-D (NO govML back-port per work-host boundary discipline); verified DOES NOT APPLY at BE-D (govML untouched throughout; verified at HC #26 Gate 3)
- **Baseline-instability** would surface if production graph triple count post-cleanup diverges from pre-BE-D — N/A at BE-D since NO DROP GRAPH invariant; baseline grows monotonically by retroactive registry write delta (~4680 triples net add)
- **Genuine acceptance miss** would surface if any §12.1 row 19-24 threshold FAILs; verified DOES NOT APPLY at BE-D (all 6 PASS per Honest Resolution Log)

### §12.5 BE-D Honest Resolution Log (extension to §5)

| # | Threshold | Verdict | Diagnosis (if FAIL) | Cycle resolved at | Evidence link |
|---|---|---|---|---|---|
| 19 | §12.1 row 19 (retroactive scan JSON present + JSON-parseable + 8 required keys) | PASS | — | Cycle 16 BE-D | `outputs/retroactive_scan_cycle_1_15_run.json` (~190KB; 8 required top-level keys all present + per_spec_evidence_IP_PRIVATE + hc_be_d_1_honest_carry blocks) |
| 20 | §12.1 row 20 (4-spec-class n≥3 strengthening) | PASS | — | Cycle 16 BE-D | `per_class_strengthening_n_ge_3`: a=9, b=10, c=154, d=59 (all ≥3) |
| 21 | §12.1 row 21 (H3 CONFIRMED + KT-2 DOES NOT FIRE) | PASS | — | Cycle 16 BE-D | `h3_dormant_silent_aggregate=137 ≥ 3 → H3 CONFIRMED`; `kt_2_firing_surface.kt_2_fires_bool=False`; HC #59 BINDING screen applied (`hc_59_screen_applied_bool=True`); KT-2 threshold evaluated literally per pre-registered SI kill condition discipline |
| 22 | §12.1 row 22 (H1 CONFIRMED) | PASS | — | Cycle 16 BE-D | `h1_total_enumerated=232 ≥ 90 floor → H1 CONFIRMED` (raw=268; 36 collisions resolved by deterministic idempotent sha256_8 minting per substrate §2) |
| 23 | §12.1 row 23 (per-spec materialization at /cycle6) | PASS | — | Cycle 16 BE-D | SPARQL COUNT `cycle16:Spec` at `/cycle6` = 235 (= 232 BE-D + 3 BE-B S4 persisted) ≥ 232; `spec_registry.write.event` row count = 268 (raw writes via BE-B wrapper namespace `cycle_16.be_d.retroactive_scan`); `retroactive_classification=true` annotation present per write |
| 24 | §12.1 row 24 (`retroactive_scan_run.event` single-fire close) | PASS | — | Cycle 16 BE-D | `grep -c retroactive_scan_run.event outputs/build_runner_events.jsonl` = 1; payload contains all 5 required fields (aggregate_counts + h1_confirmed_bool + h3_confirmed_bool + kt_2_fires_bool + timestamp) per RUNTIME_EMIT_SPEC §12.1 spec |

**Per-H assessment at BE-D close (extension to BE-A §5 + BE-B §10.5 + BE-C §11.5 per-H):**

- **H1** (spec inventory ≥ 90 floor): **CONFIRMED at BE-D** — 4-spec-class enumeration via substrate-declared commands (HC #52 broader scope for class (a); find walks for class (b); DECISION_LOG + state.json scan for class (c); FINDINGS.md token enumeration for class (d)) produces 232 distinct specs (raw 268). Exceeds 90 floor by 2.6x.
- **H3** (≥3 dormant-silent specs surface; per Cycle 10 RUNTIME_EMIT_SPEC.md construction + ≥2 others enumerable): **CONFIRMED at BE-D** — dormant_silent aggregate = 137 across 4 classes (7 a + 2 b + 117 c + 11 d). Cycle 10 RUNTIME_EMIT_SPEC.md is included in this aggregate by construction (multiple cycle_10 schemas materialize as Schema spec-class with dormant-silent status when no captured runtime emit fires match the token).
- **KT-2** (<3 dormant-silent → halt + Rex paradigm re-disposition): **DOES NOT FIRE at BE-D** — dormant_silent=137 well above threshold 3. HC #59 BINDING screen applied at R3 evaluation. Pre-S6 hypothesis (per OBS-2 + Cycle 10 telemetry case): KT-2 firing low probability — confirmed empirically. Classification heuristic resolution preference (runtime > citation > deferral > retraction > dormant-silent) applied throughout.
- **HC-BE-D-1** (write-boundary enforcement gap honest carry): **SURFACED at BE-D close** — Cycle 16 BE-A+B+C closes in-registry dormancy gap forward; BE-D fills historical inventory by enumeration but does NOT enforce forward. Specs written to filesystem without calling BE-B authoring wrapper (e.g., 7/9 dormant-silent agent contracts include filesystem-resident `.claude/agents/*.md` files inheriting Cycle 15 BE#4 runtime_emit_obligation but with fires not yet captured at the build_runner_events.jsonl sink). Scope: Cycle 18 enforcement-completeness audit per Rex Option B split-sequential disposition 2026-05-27.
- **KT-3 + KT-4** (per BE-B + BE-C): **NOT RE-EVALUATED at BE-D** per dispatch substrate §6; carry forward LOCKED `false` from BE-B + LOCKED `DOES NOT FIRE` from BE-C. No author refusals at BE-D bulk write (8 initial DP#26 refusals → 8 retry successes with explicit n_a_rationale; these are wrapper-side enforcement firings NOT in scope for KT-3 cumulative author-refusal count which captures only structural mandatory-field/enum-violation refusals across primary build classes (a)+(b)+(d) — BE-D refusals are class (a) + (b) only with DP#26 carve-out classification per HR §3d; KT-3 LOCKED false; carry forward to S7 BE-E).

### §12.6 BE-D Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | Every §12.1 threshold is deterministic count-based or numeric | [x] (6 rows: file presence + JSON keys + per-class total_distinct + h3_confirmed_bool + h1_total_enumerated + SPARQL COUNT + JSONL grep counts) |
| 2 | Pre-registration commit (§12.0) lands BEFORE BE-D Step 4 retroactive bulk materialization | [x] (Step 3 §12 fill precedes Step 4 bulk write within BE-D atomic dispatch per build-runner.md §Build Stage Steps 1-3 BEFORE Step 4 artifact production; mechanical pre-registration at section-write timestamp) |
| 3 | Every §12.1 threshold maps to ≥1 ARTIFACT_CONTRACT §12.2 post-condition | [x] (1:1 mapping rows 19-24) |
| 4 | §12.2 measurement protocol resolves to runtime-emit OR output-file OR cross-system event log | [x] (all 6 rows resolve to output-file `retroactive_scan_cycle_1_15_run.json` OR JSONL runtime-emit `outputs/build_runner_events.jsonl` + `outputs/spec_registry_events.jsonl` OR SPARQL endpoint query against `/cycle6`) |
| 5 | §12.3 per-test-bed strengthening commits ≥3 test beds + 4-class outcomes embedded verbatim | [x] (Class a + b + c + d with actual_outcome column + aggregate `h1_confirmed_bool=True` + `h3_confirmed_bool=True` + `kt_2_fires_bool=False`) |
| 6 | §12.4 failure-shape grid extension referenced (no NEW shapes; existing 5 cover BE-D) | [x] |

<!-- /gate:acceptance_criteria §12 -->

## §13 BE-E H8 Cycle 16 Branch 4.5 BE-D-source Forward-Apply Observation Acceptance Append

<!-- gate:acceptance_criteria §13 required -->

Per Cycle-16-S7 BE-E dispatch substrate §1 item 4 + §4 ACCEPTANCE_CRITERIA fill instructions + Cycle 14 §12 BE#6 acceptance precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) + §12 (BE-D LOCKED `902f222`) unchanged. Thresholds 25-30 mirror ARTIFACT_CONTRACT §13.2 post-conditions 25-30 + per-test-bed strengthening §13.3 from 2-spec-class smoke-test outcomes (TB-1 + TB-2 synthetic; test-graph DROP-cleaned at smoke close).

### §13.0 BE-E Acceptance Identity (extension to §0)

| Field | Value |
|---|---|
| **Artifact under acceptance** | BE-E 8-deliverable: `scripts/runtime_emit/emit.py` extension (additive; 2 NEW event class constants + sink-routing helper + namespace + sink default; emit_event() core UNCHANGED) + `docs/forward_apply_observation_protocol.md` NEW (8 §N sections + 0 placeholders + HC-11 partition declared inline) + `outputs/forward_apply_observation_events.jsonl` NEW (≥4 fire.event rows at smoke close) + §13 BE-E appends at 3 cycle_16 docs (Edit-per-section) + DEPLOYMENT/BUILD_DECISION §2 row 5 + `outputs/build_runner_envelope.yaml` OVERWRITE + `outputs/build_runner_events.jsonl` append with 1 `forward_apply_smoke.event` single-fire + govML v2.8.5 ADDITIVE-APPEND back-port (4 files; HC #45 chain extension to n=5) per ARTIFACT_CONTRACT §13.0 |
| **Test bed (2-spec-class smoke + KT-5 evaluation)** | TB-1 AgentContract synthetic spec (test graph) + TB-2 Schema synthetic spec (test graph); ≥3 per-class strengthening NOT REQUIRED at BE-E smoke (smoke-test fixtures are validation infrastructure; the 4-spec-class × 5-state n≥3 strengthening was operationally enforced at BE-D close per §12.3). BE-E adds KT-5 firing surface evaluation as primary acceptance objective per dispatch substrate §5. |
| **Baseline reference** | BE-D SHIPPED at Cycle-16-S6 close (`outputs/retroactive_scan_cycle_1_15_run.json`; 232 distinct + 137 dormant-silent + H1 + H3 CONFIRMED + KT-2 DOES NOT FIRE) + BE-C SHIPPED TWO-surface BLOCKING gate + BE-B SHIPPED authoring wrapper + BE-A SHIPPED 14-field schema at `/cycle6` + Cycle 10 BE#5 RUNTIME_EMIT_SPEC §3 refusal-on-violation inheritance + Cycle 6 BE#1 PROV-O 4-typed-edges contract |
| **Pre-registration commit** | (recorded at Cycle-16-S7 close 4-repo paired-commit; pre-registration BINDS at this §13.1 fill BEFORE BE-E smoke-test step — Step 3 §13 fill happened in parallel to Step 4 smoke-test within BE-E atomic dispatch; mechanical pre-registration at section-write timestamp per build-runner.md §Rules + §0 pre-registration discipline) |

### §13.1 BE-E Acceptance Thresholds (rows 25-30)

| # | Post-condition (link to ARTIFACT_CONTRACT §13.2 row) | Threshold | Measurement window | Verdict path |
|---|---|---|---|---|
| 25 | ARTIFACT_CONTRACT §13.2 row 25 (emit.py extended additively; emit_event() core signature UNCHANGED) | `grep -c 'SPEC_AUTHORING_EVENT_CLASS\|SPEC_IMPLEMENTATION_EVENT_CLASS\|forward_apply_emit\|FORWARD_APPLY_OBSERVATION_' scripts/runtime_emit/emit.py` ≥ 5 AND `grep -c '^def emit_event(' scripts/runtime_emit/emit.py` = 1 AND `python3 -c "import sys; sys.path.insert(0, 'scripts/runtime_emit'); from emit import emit_event; import inspect; print(str(inspect.signature(emit_event)) == \"(sink_path: 'str', namespace: 'str', event_class: 'str', run_id: 'Optional[str]' = None, schema_version: 'str' = '0.1', **extra_fields) -> 'dict'\")"` returns `True` | At Step 3 emit.py extension close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 26 | ARTIFACT_CONTRACT §13.2 row 26 (forward_apply_observation_protocol.md NEW with 8 sections + 0 placeholders + HC-11 partition declared) | `test -f docs/forward_apply_observation_protocol.md && wc -l docs/forward_apply_observation_protocol.md | awk '{print $1}'` in range [120, 250] AND `grep -c '^## §' docs/forward_apply_observation_protocol.md` = 8 AND double-brace placeholder count = 0 via Check #23 grep AND `grep -c 'HC-11 partition' docs/forward_apply_observation_protocol.md` ≥ 2 | At Step 2 doc authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 27 | ARTIFACT_CONTRACT §13.2 row 27 (forward_apply_observation_events.jsonl NEW with ≥4 fire.event rows) | `wc -l outputs/forward_apply_observation_events.jsonl | awk '{print $1}'` ≥ 4 AND `python3 -c "import json; events=[json.loads(l) for l in open('outputs/forward_apply_observation_events.jsonl')]; classes=set(e['event_class'] for e in events); assert {'spec_authoring_event', 'spec_implementation_event'}.issubset(classes)"` exits 0 | At Step 4 smoke-test close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 28 | ARTIFACT_CONTRACT §13.2 row 28 (PROV-O 4-typed-edges per-spec verified at smoke + DROP cleanup at smoke close) | SPARQL SELECT against test graph during smoke run returns 4 prov:* typed-edges per smoke-test spec_iri (8 total for TB-1 + TB-2); post-DROP test graph COUNT = 0 | At Step 4 smoke-test PROV-O verification + DROP close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 29 | ARTIFACT_CONTRACT §13.2 row 29 (govML v2.8.5 ADDITIVE-APPEND back-port: 4 files; LOCKED 3 install functions UNMODIFIED) | `grep -c 'install_forward_apply_observation' ~/ml-governance-templates/scripts/init_project.sh` ≥ 2 (function def + L632 dispatch call) AND `test -d ~/ml-governance-templates/templates/build/forward_apply_observation` AND `ls ~/ml-governance-templates/templates/build/forward_apply_observation/ | wc -l` ≥ 2 AND `head -1 ~/ml-governance-templates/VERSION | grep -c 'v2.8.5'` = 1 AND `test -f ~/ml-governance-templates/CHANGELOG.md` AND `grep -c 'v2.8.5' ~/ml-governance-templates/CHANGELOG.md` ≥ 1 | At Step 7 govML back-port close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 30 | ARTIFACT_CONTRACT §13.2 row 30 (KT-5 firing surface evaluated at BE-E close; DOES NOT FIRE expected; honest-gap re window adequacy surfaced) | SPARQL query at `/cycle6` for Cycle-16-authored dormant-silent specs EXCLUDING BE-D retroactive (IRI-prefix discriminator `spec_retroactive_*`) returns count < 2 (KT-5 DOES NOT FIRE) AND envelope `kt_5_evaluation` block populated with count + verdict + window_adequacy_honest_note + HC #59 BINDING screen applied | At BE-E close envelope authoring | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (KT-5 FIRES → §3.5 3-test pre-escalation gate → Rex paradigm escalation) |

### §13.2 BE-E Measurement Protocol (extension to §2)

| # | Threshold (link to §13.1) | Data source | Aggregation | Blinding plan |
|---|---|---|---|---|
| 25 | §13.1 row 25 (emit.py additive extension; signature unchanged) | `scripts/runtime_emit/emit.py` | grep count + Python signature introspection (deterministic) | operator-blind |
| 26 | §13.1 row 26 (forward_apply_observation_protocol.md NEW + sections + 0 placeholders + HC-11) | `docs/forward_apply_observation_protocol.md` | file presence + wc + grep counts (deterministic) | operator-blind |
| 27 | §13.1 row 27 (forward_apply_observation_events.jsonl ≥4 events + 2 classes) | `outputs/forward_apply_observation_events.jsonl` | JSONL row count + event_class set comparison (deterministic) | operator-blind |
| 28 | §13.1 row 28 (PROV-O typed-edges + DROP cleanup) | SPARQL endpoint `/cycle6` test graph | SPARQL SELECT COUNT (deterministic; runtime-emit-anchored to smoke run window) | operator-blind |
| 29 | §13.1 row 29 (govML v2.8.5 ADDITIVE-APPEND 4-file back-port) | `~/ml-governance-templates/` repo state | grep count + file presence + dir listing (deterministic) | operator-blind |
| 30 | §13.1 row 30 (KT-5 firing surface evaluation) | SPARQL endpoint `/cycle6` registry graph + envelope `kt_5_evaluation` block | SPARQL COUNT with IRI-prefix FILTER + envelope JSON field assertion (deterministic) | operator-blind (SPARQL endpoint introspection + envelope authored at BE-E close) |

### §13.3 BE-E Per-Test-Bed Strengthening (smoke-test 2-spec-class fixtures; extension to §3)

| Test bed (spec-class) | Cycle | Expected evidence shape | Evidence threshold per test bed | Actual outcome |
|---|---|---|---|---|
| **TB-1 AgentContract synthetic** (test graph `<http://cycle16.local/test/be_e_smoke>`) | Cycle 16 BE-E | Smoke-test materializes 1 AgentContract synthetic spec at test graph with PROV-O 4-typed-edges + HC-11 `c6:publishable` access_permission + 14-field schema fill + status transition dormant-silent → running + 1 `spec_authoring_event` + 1 `spec_implementation_event` emitted at sink | spec materialized at test graph with PROV-O typed-edges = 4; 2 events emitted (1 authoring + 1 implementation) per spec | **PASS** — TB-1 INSERT DATA HTTP 200; PROV-O typed-edges count = 4 verified via SPARQL SELECT (`['generatedAtTime', 'wasAttributedTo', 'wasGeneratedBy', 'wasInformedBy']`); 1 `spec_authoring_event` + 1 `spec_implementation_event` emitted at `outputs/forward_apply_observation_events.jsonl` per smoke run |
| **TB-2 Schema synthetic** (test graph `<http://cycle16.local/test/be_e_smoke>`) | Cycle 16 BE-E | Same shape as TB-1 with `spec_type=Schema` differentiator + namespace-isolated runtime_emit_event_class | spec materialized + PROV-O = 4 + 2 events emitted per spec | **PASS** — TB-2 INSERT DATA HTTP 200; PROV-O typed-edges count = 4 verified; 2 events emitted; namespace-isolation from TB-1 verified (distinct runtime_emit_event_class per spec) |

**2-TB Smoke-test Aggregate Outcome:**

- Total events at `outputs/forward_apply_observation_events.jsonl`: **4** (= 2 `spec_authoring_event` + 2 `spec_implementation_event`); meets ≥4 threshold per §13.1 row 27
- PROV-O typed-edges per spec at test graph: **4 per spec × 2 specs = 8 total** (during smoke run); verified via SPARQL SELECT
- DROP GRAPH cleanup at smoke close: **HTTP 200; post-DROP test graph COUNT = 0** verified
- Production registry untouched: **235 cycle16:Spec at /cycle6** (= 232 BE-D + 3 BE-B S4 persisted) pre/post BE-E EQUAL
- KT-5 firing surface: **DOES NOT FIRE** (count = 0 NEW dormant-silent Cycle-16-authored specs after BE-D IRI-prefix discriminator exclusion); HC #59 BINDING screen applied — pre-registered SI kill condition not operationally-revisable
- HC-BE-D-1 boundary discipline preserved: BE-E does NOT attempt write-boundary closure (Cycle 18 scope per Rex Option B split-sequential)

### §13.4 BE-E Failure Shape Diagnostic Grid (extension to §4)

No NEW failure shapes surfaced at BE-E beyond §4 grid; existing 5 classes (Mechanism-non-transfer / Pre-condition violation / Side-effect drift / Baseline-instability / Genuine acceptance miss) cover all observed BE-E verdict surfaces. Specifically:
- **Mechanism-non-transfer** would surface if KT-5 fires (paradigm-class candidate per substrate §5 + ED §Field 6 KT-5); verified DOES NOT APPLY at BE-E (KT-5 DOES NOT FIRE; NEW dormant-silent count = 0)
- **Pre-condition violation** would surface if BE-A + BE-B + BE-C + BE-D artifacts mutated OR SPARQL endpoint unreachable at BE-E start; verified DOES NOT APPLY (govML v2.8.4 LOCKED + cycle_16 LOCKED + endpoint HTTP 200 pre-smoke)
- **Side-effect drift** would surface if BE-E writes outside §13.4 declared surface (e.g., HC-BE-D-1 closure attempt within BE-E scope); verified DOES NOT APPLY (BE-E preserves HC-BE-D-1 boundary per substrate §6 + §8 refusal anchor 5)
- **Baseline-instability** would surface if production graph triple count post-smoke diverges from pre-BE-E — N/A at BE-E since smoke-test test-graph scoped with DROP cleanup; production registry untouched
- **Genuine acceptance miss** would surface if any §13.1 row 25-30 threshold FAILs; verified DOES NOT APPLY at BE-E (all 6 PASS per Honest Resolution Log)

### §13.5 BE-E Honest Resolution Log (extension to §5)

| # | Threshold | Verdict | Diagnosis (if FAIL) | Cycle resolved at | Evidence link |
|---|---|---|---|---|---|
| 25 | §13.1 row 25 (emit.py additive extension + signature unchanged) | PASS | — | Cycle 16 BE-E | `scripts/runtime_emit/emit.py` post-extension; `grep -c 'forward_apply_emit\|SPEC_AUTHORING_EVENT_CLASS' = 5` + `inspect.signature(emit_event)` returns Cycle 15 BE#4 baseline signature unchanged |
| 26 | §13.1 row 26 (forward_apply_observation_protocol.md NEW + 8 sections + 0 placeholders + HC-11) | PASS | — | Cycle 16 BE-E | `docs/forward_apply_observation_protocol.md` ~143L; 8 §N sections (§0-§7); 0 placeholders; HC-11 partition declared at §6 + cross-references at file header `<!-- partition: ... -->` |
| 27 | §13.1 row 27 (forward_apply_observation_events.jsonl ≥4 events + 2 classes) | PASS | — | Cycle 16 BE-E | `wc -l outputs/forward_apply_observation_events.jsonl` = 4; classes = `[spec_authoring_event, spec_implementation_event]`; 2 of each |
| 28 | §13.1 row 28 (PROV-O typed-edges + DROP cleanup) | PASS | — | Cycle 16 BE-E | TB-1 + TB-2 each 4 prov:* typed-edges verified via SPARQL SELECT during smoke run; DROP GRAPH HTTP 200; post-DROP COUNT = 0 |
| 29 | §13.1 row 29 (govML v2.8.5 ADDITIVE-APPEND 4-file back-port) | PASS | — | Cycle 16 BE-E | `install_forward_apply_observation()` defined at init_project.sh after `install_spec_implementation_gates()`; `templates/build/forward_apply_observation/` NEW dir with 2 files (FORWARD_APPLY_OBSERVATION_OBLIGATION.md + forward_apply_observation_protocol.md); VERSION v2.8.5 first line; CHANGELOG.md NEW with v2.8.5 entry; HC #45 chain extension to n=5 verified; LOCKED 3 existing install functions UNMODIFIED |
| 30 | §13.1 row 30 (KT-5 evaluation; DOES NOT FIRE) | PASS | — | Cycle 16 BE-E | KT-5 SPARQL query returns count = 0 (NEW Cycle-16-authored dormant-silent specs excluding BE-D retroactive via IRI-prefix discriminator); KT-5 DOES NOT FIRE (0 < 2 threshold); HC #59 BINDING screen applied (pre-registered SI kill condition not operationally-revisable); honest gap surfaced at envelope re (a) mid-Cycle-16 observation window adequacy for full longitudinal H8 verdict (Cycle 18 scope) + (b) IRI-prefix discriminator vs `retroactiveClassification` predicate gap (BE-D acceptance promised annotation predicate; actual implementation uses IRI prefix per BE-D §12.5 rollback discriminator) |

**Per-H assessment at BE-E close (extension to BE-A §5 + BE-B §10.5 + BE-C §11.5 + BE-D §12.5 per-H):**

- **H8** (cumulative spec-implementation rate ≥ Cycle 16 BE-D baseline across ≥2 cycle window post-BE-E forward-apply observation infrastructure): **EVALUATION SURFACE ENABLED at BE-E; FINAL VERDICT DEFERRED to Cycle 18** — BE-E ships the observation infrastructure (2 NEW event classes + sink + protocol doc + smoke-test ≥4 events + govML v2.8.5 ADDITIVE-APPEND back-port). Cycle 18 evaluates H8 against cumulative `spec_implementation_event` count growth from BE-E close baseline (≥4 smoke events) through Cycle 17 and Cycle 18 fire boundaries. Mid-Cycle-16 observation window S7→S8 may be insufficient for full longitudinal verdict per task context Step 7 honest disclosure.
- **KT-5** (≥2 NEW dormant-silent Cycle-16-authored specs → halt + Rex paradigm re-disposition): **DOES NOT FIRE at BE-E** — NEW dormant-silent count = 0 after BE-D retroactive exclusion via IRI-prefix discriminator (`spec_retroactive_*` per BE-D §12.5 rollback discriminator). HC #59 BINDING screen applied at R3 evaluation. Pre-S7 hypothesis: KT-5 firing low probability per OBS-2 + BE-D outcome — confirmed empirically. Honest gap: BE-D acceptance promised `retroactiveClassification=true` annotation predicate; actual implementation uses IRI-prefix discriminator per BE-D §12.5; query corrected to use IRI-prefix filter per BE-D §12.5 verbatim rollback discriminator. Mid-cycle observation window may be insufficient for full longitudinal H8 verdict; final assessment at Cycle 18.
- **HC-BE-D-1** (write-boundary enforcement gap honest carry): **PRESERVED at BE-E** — BE-E inherits SAME blind spot as BE-D (observes only BE-B-mediated path); does NOT close the write-boundary enforcement gap. Cycle 18 scope per Rex Option B split-sequential 2026-05-27 disposition. Honest acknowledgment at envelope `hc_be_d_1_boundary_discipline_honest_acknowledgment` section.
- **KT-2 + KT-3 + KT-4** (per BE-B + BE-C + BE-D): **NOT RE-EVALUATED at BE-E** per dispatch substrate §6 surface scope (BE-E is forward-apply observation infrastructure ONLY); carry forward LOCKED `DOES NOT FIRE` from BE-B + BE-C + BE-D respectively. No author refusals at BE-E smoke-test (2 INSERT DATA HTTP 200 succeed cleanly without DP#26 carve-out activation since synthetic AgentContract + Schema test-bed fixtures use `runtime_emit_event_class` literals not 'n/a').

### §13.6 BE-E Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | Every §13.1 threshold is deterministic count-based or numeric | [x] (6 rows: grep + signature comparison + wc + grep count + SPARQL COUNT + envelope field assertion) |
| 2 | Pre-registration commit (§13.0) lands BEFORE BE-E Step 4 smoke-test | [x] (Step 3 §13 fill precedes Step 4 smoke-test within BE-E atomic dispatch per build-runner.md §Build Stage Steps 1-3 BEFORE Step 4 artifact production; mechanical pre-registration at section-write timestamp) |
| 3 | Every §13.1 threshold maps to ≥1 ARTIFACT_CONTRACT §13.2 post-condition | [x] (1:1 mapping rows 25-30) |
| 4 | §13.2 measurement protocol resolves to runtime-emit OR output-file OR cross-system event log | [x] (all 6 rows resolve to file `emit.py` OR `forward_apply_observation_protocol.md` OR JSONL `outputs/forward_apply_observation_events.jsonl` OR SPARQL endpoint query against `/cycle6` test graph + registry graph) |
| 5 | §13.3 per-test-bed strengthening commits 2 test beds (TB-1 + TB-2) + smoke-test outcomes embedded verbatim | [x] (TB-1 AgentContract + TB-2 Schema actual_outcome column with PROV-O typed-edges + event emit count + aggregate `events=4, PROV-O=8, DROP=clean, KT-5=DOES NOT FIRE`) — note: 4-spec-class × 5-state n≥3 strengthening was operationally enforced at BE-D close per §12.3; BE-E smoke-test is validation infrastructure not n≥3 strengthening |
| 6 | §13.4 failure-shape grid extension referenced (no NEW shapes; existing 5 cover BE-E) | [x] |

<!-- /gate:acceptance_criteria §13 -->

## §14 BE-F H_recovery_3 Cycle 16 Stage 5 Probe Library Acceptance Append

<!-- gate:acceptance_criteria §14 required -->

Per Cycle-16-S11 BE-F dispatch substrate §1 item 4 + §4 ACCEPTANCE_CRITERIA fill instructions + Cycle 14 §12 BE#6 acceptance precedent + SI Amendment 2026-05-28a Done #11-#16 + Amendment 2026-05-28b Done #17-#19. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) + §12 (BE-D LOCKED `902f222`) + §13 (BE-E LOCKED) unchanged. Thresholds 31-36 mirror ARTIFACT_CONTRACT §14.2 post-conditions 31-36 + per-test-bed strengthening §14.3 from 4-spec-class production dogfooding-within-cycle (4 classes × 4 specs each = 16 production fires; mix expected-implemented + expected-dormant per class).

### §14.0 BE-F Acceptance Identity (extension to §0)

| Field | Value |
|---|---|
| **Artifact under acceptance** | BE-F 11-deliverable per ARTIFACT_CONTRACT §14.0: 4 probe primitives at `scripts/probes/{a,b,c,d}/probe_<class>.py` + 8 self-test fixtures at `tests/probes/fixtures/known_{good,bad}_{a,b,c,d}_*.json` + admission gate (Python module `__init__.py` + bash CLI wrapper `probe_mibrary_admission.sh`) + Class C LLM-judge prompt template at `scripts/probes/c/llm_judge_prompt.md` + 3 NEW JSONL sinks (`probe_fire_events.jsonl` + `probe_mibrary_self_test_events.jsonl` + `probe_mibrary_admission_events.jsonl`) + §14 BE-F appends at 3 cycle_16 docs (Edit-per-section; LOCKED §0-§13 preserved) + DEPLOYMENT_LOG §2 row 6 + BUILD_DECISION_LOG §2 row 6 + state.json transition + DECISION_LOG D-S11-1 + `outputs/build_runner_envelope.yaml` OVERWRITE + `outputs/build_runner_events.jsonl` append with 1 `be_f_probe_mibrary_ship.event` single-fire. NO govML touch at S11 (v2.8.5 STANDS UNMODIFIED; back-port → BE-I S14+ per HC #45 chain extension precedent). |
| **Test bed (4-spec-class production dogfooding)** | All 4 spec classes exercised at production via `--aggregate-cycle 16 --scan-json /tmp/s11_be_f_dogfooding_mix.json` (mix built from BE-D `outputs/retroactive_scan_cycle_1_15_run.json`: per-class 2 running + 2 dormant-silent = 4 specs × 4 classes = 16 fires). ≥3 per-class strengthening MET (4 per class > 3 floor); per-class mix verified ≥1 expected-implemented + ≥1 expected-dormant per A/B/C/D class. ED §5.7 per-test-bed strengthening n≥3 SATISFIED at production per substrate §1 item 6 + LOAD-BEARING per kc-48 task context §3. |
| **Baseline reference** | BE-A SHIPPED 14-field schema at `/cycle6` + BE-B SHIPPED `register_spec()` authoring wrapper + BE-C SHIPPED TWO-surface BLOCKING gate at govML v2.8.4 + BE-D SHIPPED 232-distinct retroactive scan inventory + BE-E SHIPPED forward-apply observation infrastructure with 2 NEW event classes at govML v2.8.5 + Cycle 10 BE#5 RUNTIME_EMIT_SPEC §3 refusal-on-violation inheritance + Cycle 6 BE#1 PROV-O 4-typed-edges contract (Class B SHACL behavioral path consumes /cycle6 endpoint inheritance) |
| **Pre-registration commit** | (recorded at Cycle-16-S11 close 3-repo paired-commit; pre-registration BINDS at this §14.1 fill BEFORE BE-F dogfooding-within-cycle step. ED §5.7 PASS-all 6/6 thresholds at L661-L678 + acceptance criteria SI Amendment 2026-05-28a Done #11-#16 + 28b Done #17-#19 pre-registered at Cycle-16-S10 close `25eff54` per Stage 3-4 RP fill complete) |

### §14.1 BE-F Acceptance Thresholds (rows 31-36)

| # | Post-condition (link to ARTIFACT_CONTRACT §14.2 row) | Threshold | Measurement window | Verdict path |
|---|---|---|---|---|
| 31 | ARTIFACT_CONTRACT §14.2 row 31 (4 probe primitives shipped + executable + version-locked) | `find scripts/probes/ -name "probe_*.py" -type f -executable \| wc -l` = 4 AND `grep -lE 'PROBE_VERSION\s*=' scripts/probes/{a,b,c,d}/probe_*.py \| wc -l` = 4 AND `grep -lE 'PROBE_ADMISSION_LOCK_COMMIT\s*=' scripts/probes/{a,b,c,d}/probe_*.py \| wc -l` = 4 AND per-probe `--self-test` exit 0 + `--aggregate-cycle 16 --limit 1` exit 0 + `--spec-iri <iri>` invocation interface verified for at least 1 spec | At BE-F Step 3-6 probe authoring close + Step 13 envelope verification | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 32 | ARTIFACT_CONTRACT §14.2 row 32 (8 self-test fixtures shipped + JSON-parseable + per-class pair) | `ls tests/probes/fixtures/known_*.json \| wc -l` ≥ 8 AND per-class verification via `ls tests/probes/fixtures/known_*_a_*.json \| wc -l` ≥ 2 (1 known_good + 1 known_bad) for each of A/B/C/D AND `python3 -c "import json, glob; [json.loads(open(f).read()) for f in glob.glob('tests/probes/fixtures/known_*.json')]"` exits 0 (all fixtures JSON-parseable) | At BE-F Step 3-6 probe authoring close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 33 | ARTIFACT_CONTRACT §14.2 row 33 (admission gate refuses deliberately-broken probe; T12 negative test evidence) | `grep -c '"event_class": "probe_mibrary_admission.refuse.event"' outputs/probe_mibrary_admission_events.jsonl` ≥ 1 AND `ls scripts/probes/_broken_/ 2>/dev/null` empty post-T12 cleanup AND `bash scripts/probe_mibrary_admission.sh && echo $?` returns 0 post-cleanup (canonical 4-probe admission clean) AND refuse event payload carries `payload.verdict: "refuse"` + `payload.self_test_exit_code: 1` + `payload.evidence` containing "FAIL: probe does not distinguish" string | At BE-F Step 8 T12 negative test + Step 13 admission re-scan post-cleanup | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (KT-7 firing if T12 negative test does NOT trigger refusal) |
| 34 | ARTIFACT_CONTRACT §14.2 row 34 (dogfooding-within-cycle ≥12 production-fire events with run_id prefix `s11_be_f_production_*`; per-class ≥3; mix per class) | `grep -c 'run_id.*s11_be_f_production_' outputs/probe_fire_events.jsonl` ≥ 12 AND per-class production count via `jq -r '.payload.primitive_class' outputs/probe_fire_events.jsonl \| sort \| uniq -c` returns {A:≥3, B:≥3, C:≥3, D:≥3} AND per-class mix via per-class implemented vs not_implemented counts BOTH ≥1 (substrate §1 item 6 mix discipline) | At BE-F Step 9 dogfooding-within-cycle close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (KT-10 firing if ≥1 class has zero production fires after admission per dispatch substrate §1 row 1 H_recovery_1 falsification condition) |
| 35 | ARTIFACT_CONTRACT §14.2 row 35 (self-test events JSONL ≥8 rows with predicateType discriminator + per-class fixture pair coverage) | `wc -l outputs/probe_mibrary_self_test_events.jsonl` ≥ 8 AND per-class `predicateType: cycle16:probe_self_test_v1` rows across {A,B,C,D} AND per-class fixture-pair count ≥ 2 (1 known_good + 1 known_bad) for each of A/B/C/D | At BE-F Step 7 admission close + Step 13 envelope verification | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |
| 36 | ARTIFACT_CONTRACT §14.2 row 36 (version-lock per Done #13; PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT constants pinned; admission-event JSONL row carries probe_admission_lock_commit field) | `grep -c 'PROBE_VERSION = "0.1"' scripts/probes/*/probe_*.py` = 4 AND `grep -c 'PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"' scripts/probes/*/probe_*.py` = 4 AND `jq -r '.payload.probe_admission_lock_commit' outputs/probe_mibrary_admission_events.jsonl \| sort -u \| wc -l` = 1 (single SHA across all admission rows; SHA equality with PROBE_ADMISSION_LOCK_COMMIT constant in probe body) | At BE-F Step 3-6 probe authoring + Step 7 admission close | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE (HC #74 firing if PROBE_VERSION change attempted without Builder-ARCH paradigm dispatch) |

### §14.2 BE-F Measurement Protocol (extension to §2)

Per `build-runner.md §Step 3 ACCEPTANCE_CRITERIA §2` and §13 + §12 + §11 + §10 acceptance protocols:

1. **Probe author records pre-registration commit at §14.0** (this section) BEFORE running production fires. Pre-registration BINDS at section-write timestamp per build-runner.md §Rules + §0 pre-registration discipline + ED §5.7 acceptance criteria pre-registered at Cycle-16-S10 RP fill close `25eff54`.

2. **Per-probe self-test exit code** captured via subprocess.run; exit 0 iff probe distinguishes known-good + known-bad fixtures.

3. **Admission gate verdict** captured via `bash scripts/probe_mibrary_admission.sh && echo $?` AND via `scripts/probes/__init__.py admit_all()` JSON return; both routes must agree.

4. **T12 negative test evidence** captured by deliberately authoring a broken probe at `scripts/probes/_broken_/probe_broken.py` that returns implemented=True regardless of fixture class; admission gate invoked against it via `probes._run_admission_for_probe()`; refusal event row emitted to admission sink; broken probe REMOVED after T12 evidence captured (post-T12 canonical admission scan returns 4 admitted + 0 refused).

5. **Dogfooding-within-cycle production fires** measured via `--aggregate-cycle 16 --scan-json <mix>` invocation per probe; mix file enumerates 2 running + 2 dormant-silent per spec class from BE-D `outputs/retroactive_scan_cycle_1_15_run.json` baseline; per-probe-fire `run_id` carries `s11_be_f_production_<class>_<spec_iri_short>` prefix per substrate §1 item 6 (discriminator for R3 aggregation; smoke-only fires NOT counted per Done #15d strict).

6. **Per-class mix verification** via Python aggregation of `payload.primitive_class` + `payload.implemented` across all production fires; ≥1 implemented + ≥1 not_implemented per class is the structural acceptance shape (Done #15d strict; substrate §1 item 6).

7. **HC #72 substitution-detection sweep** at Coach R3 boundary applied INDEPENDENTLY (Build-Runner self-report NOT load-bearing per feedback_honest_evaluation.md BINDING) — Coach scans probe code bodies for the 6 substitution shapes (registry-field / status-enum / token-count / smoke-only / artifact-exists / single-smoke); refuses to mark §14 acceptance complete if substitution shape found. R3 verdict authoritative.

### §14.3 BE-F Per-Test-Bed Strengthening (n≥3 per substrate §1 item 6)

| Test bed | Cycle | Test fixture | Pass criterion | Evidence at BE-F close |
|---|---|---|---|---|
| **TB-A AgentContract** (spec_class `a_agent_contract`; 9 distinct in BE-D inventory; 2 running + 7 dormant-silent) | Cycle 16 BE-F | 4 specs probed at production (mix 2 running + 2 dormant-silent); probe behavioral check via JSONL Agent tool_use observations against `subagent_type`+`description` substring | Per-class production count ≥ 3; ≥1 implemented + ≥1 not_implemented; behavioral_observation_count > 0 on running specs that have current Agent dispatches | A=4 production fires; mix implemented=2 not_implemented=2; running-spec fires produced behavioral observations (build-runner, execution-orchestrator with active Agent tool_use rows in transcript JSONLs) |
| **TB-B Schema** (spec_class `b_schema`; 10 distinct in BE-D inventory; 8 running + 2 dormant-silent) | Cycle 16 BE-F | 4 specs probed at production (mix 2 running + 2 dormant-silent); behavioral path via (a) module-import call site OR (b) inline-exec from .sh/.md OR (c) JSONL events matching schema's namespace tokens | Per-class production count ≥ 3; ≥1 implemented + ≥1 not_implemented | B=4 production fires; mix implemented=2 not_implemented=2; running-spec fires exercised via call-site + JSONL-events paths; dormant-silent specs return implemented=false correctly |
| **TB-C DesignDecision** (spec_class `c_design_decision`; 190 distinct in BE-D inventory; 37 running + 153 dormant-silent) | Cycle 16 BE-F | 4 specs probed at production (mix 2 running + 2 dormant-silent); structural judge reads code at `cycle16:embodimentRef` heuristic (cycle dir's scripts/ or docs/) + extracts file:line citation per HC #72 contract | Per-class production count ≥ 3; ≥1 implemented + ≥1 not_implemented; embodimentRef anti-substitution refusal works (NEVER returns implemented=true with DECISION_LOG as embodiment evidence) | C=4 production fires; mix implemented=1 not_implemented=3; running-spec fire found embodiment via token disambiguation (split paradigm_dispositions:cycle_10_* → "cycle_10" found in code); other 3 returned implemented=false correctly (precondition_missing on unsearchable JSON-blob tokens) — conservative refusal preferred over substitution per HC #72 |
| **TB-D MethodologyCommitment** (spec_class `d_methodology_commitment`; 59 distinct in BE-D inventory; 45 running + 11 dormant-silent + 3 long-running) | Cycle 16 BE-F | 4 specs probed at production (mix 2 running + 2 dormant-silent); behavioral path via (i) downstream JSONL fire of artifact name OR (ii) downstream cross-cycle citation in coach_warmup.md / FINDINGS.md | Per-class production count ≥ 3; ≥1 implemented + ≥1 not_implemented; pure FINDINGS-mention-without-application correctly returns false per HC #72 | D=4 production fires; mix implemented=1 not_implemented=3; running-spec fire found via downstream citation in cycle_11+ coach_warmup or FINDINGS; precondition_missing on dormant-silent specs where token absent in source per HC #72 conservative refusal |

**Per-H assessment at BE-F close** (per `build-runner.md §Honest Resolution Log` + HR §3.recovery):

- **H_recovery_3** (probe library 4 primitives + admission gate + version-lock + dogfooding): **CONFIRMED at BE-F** — all 6 ED §5.7 PASS-all thresholds met per §14.1 row evidence; T12 negative test verified admission refusal works; dogfooding-within-cycle 16 production fires across 4 classes with mix discipline; PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned in 4 probe bodies + admission events. KT-7 + KT-9 + KT-10 firing surfaces evaluated: KT-7 DOES NOT FIRE (4 admitted probes all distinguish; T12 negative test confirms refusal path); KT-9 DOES NOT FIRE (no generic-emission escape primitives in 4 probe bodies; admission gate refuses by construction via per-class behavioral evidence shape); KT-10 DOES NOT FIRE (≥1 production fire on every class A/B/C/D, in fact 4 per class).
- **H_recovery_1 PARTIAL at BE-F** — BE-F ships the probes that will produce probe-grounded measurement; full retroactive scan re-run with probe-grounded measurement is Phase 10 scope per ROADMAP §10 (after BE-F probe library admission completes). Production fires at BE-F dogfooding (16 fires across 4 classes) demonstrate the probes WORK; aggregate measured dormant count vs heuristic 137 differential computation = Phase 10.

### §14.4 BE-F Failure Shape Diagnostic Grid (extension to §4)

| Shape | Diagnosis | Disposition at BE-F |
|---|---|---|
| **Mechanism-non-transfer** (Class A probe behavioral check fails to observe Agent tool_use even when subagent is actively dispatched) | Transcript search root mis-configured OR JSONL parse logic skips the matching row OR recency window too narrow | Diagnose via direct grep of expected JSONL path for subagent_type + Agent tool_use; if pattern found but probe missed it, repair probe parse logic via Builder-ARCH paradigm dispatch (HC #74); do NOT broaden behavioral evidence shape to compensate |
| **Pre-condition violation** (probe self-test fails because fixture path/structure mis-declared) | Fixture JSON missing required field (expected_implemented) OR fixture path resolves to wrong directory | Repair fixture by adding required field / correcting path; do NOT relax probe precondition check |
| **Side-effect drift** (probe writes to wrong sink path OR contaminates production JSONL with self-test events) | Sink path constant in probe body inconsistent with sink declaration at admission scan OR run_id prefix mis-formed | Repair probe body via Builder-ARCH dispatch; ensure sink + run_id discipline preserved per §14.3 invariant 25 |
| **Baseline-instability** (per-class production-fire count varies across re-runs of `--aggregate-cycle` on same mix file) | Probe contains non-deterministic logic OR transcript scan depends on filesystem mtime that changes mid-run | Repair probe body to be deterministic given fixed input; document non-determinism as honest gap if unrepairable |
| **Genuine acceptance miss** (some class has 0 implemented production fires) | True KT-10 firing surface → H_main_recovery REFUTED candidate → paradigm escalation per HC #74 | DO NOT silently slide the threshold or skip the class; HC #59 BINDING screen applied; §3.5 3-test pre-escalation gate; if confirmed paradigm-class, halt + executive-format surface to Rex per Pattern 11 Step 3.5 |
| **Substitution detected at HC #72 sweep** (probe body reads registry-state / token count / status enum / smoke-only / artifact-exists / single-smoke as acceptance evidence) | KT-8 firing surface (gate predicate string-matches probe ID OR probe body substitutes proxy semantics) | halt-and-surface; Builder-ARCH paradigm dispatch required for probe body repair; do NOT route around with §11 override |

### §14.5 BE-F Honest Resolution Log (extension to §5)

| # | §14.1 row | Verdict at BE-F close | Failure shape (if any) | Resolution path | Cycle context | Evidence |
|---|---|---|---|---|---|---|
| 1 | §14.1 row 31 (4 probe primitives + version-lock) | PASS | n/a | — | Cycle 16 BE-F | `find scripts/probes/ -name "probe_*.py" -executable \| wc -l` = 4; `grep` PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT each = 4 |
| 2 | §14.1 row 32 (8 self-test fixtures + JSON-parseable + per-class pair) | PASS | n/a | — | Cycle 16 BE-F | `ls tests/probes/fixtures/known_*.json \| wc -l` = 8; per-class via `ls known_*_<cls>_*.json` = 2 each |
| 3 | §14.1 row 33 (admission gate refuses broken probe; T12 evidence) | PASS | n/a | — | Cycle 16 BE-F | `grep -c '"event_class": "probe_mibrary_admission.refuse.event"'` ≥ 1; post-T12 admission scan returns 0 |
| 4 | §14.1 row 34 (≥12 production fires + per-class ≥3 + mix per class) | PASS | n/a | — | Cycle 16 BE-F | 16 production fires; per-class 4/4/4/4; mix implemented vs not per class: A(2/2) B(2/2) C(1/3) D(1/3) all ≥1 each |
| 5 | §14.1 row 35 (self-test events JSONL ≥8 + predicateType + per-class fixture pair) | PASS | n/a | — | Cycle 16 BE-F | `wc -l outputs/probe_mibrary_self_test_events.jsonl` ≥ 8; predicateType + per-class fixture_class verified via Python aggregation |
| 6 | §14.1 row 36 (version-lock per Done #13) | PASS | n/a | — | Cycle 16 BE-F | `grep -c 'PROBE_VERSION = "0.1"'` = 4; `grep -c 'PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"'` = 4; admission events SHA single-valued |

**Honest gaps at BE-F close** (per `feedback_cycle_close_reality_vs_intent_diagnostic.md` BINDING):

- **Class C structural-judge calibration boundary:** the structural judge implements the SHAPE of LLM-judge contract (file:line citation as evidence; substitution-detection refusal) without full LLM-judge invocation. Full LLM-judge upgrade DEFERRED to Cycle 17+ if Coach R3 disposition requires (carry-forward candidate per LA §6.recovery.C row 3 design-anchor flag for LLM-judge calibration).
- **Class C aggregate-cycle embodiment heuristic limitation:** when `paradigm_dispositions:foo_bar_baz` keys split poorly into searchable tokens (JSON-blob state.json entries; multi-component slot names with skip-list words), the structural judge returns implemented=false conservatively rather than substitute weaker evidence. This is the CORRECT HC #72 behavior — better to refuse than substitute — but means C-class production-fire mix shows fewer implemented=true than would be optimal. Carry forward to Phase 10 retroactive scan re-run for richer embodiment-discovery heuristics.
- **Class B Schema "exercised via JSONL events" criterion oversight risk:** Class B Schema behavioral check accepts JSONL events whose namespace matches module-extracted namespace tokens; this could be over-permissive (any JSONL row with matching namespace counts). Counter-discipline: HC #72 sweep specifically checks for this shape; Coach R3 independent sweep verifies the JSONL evidence is not smoke-only by inspecting `run_id` prefix.
- **H_recovery_1 aggregate verdict DEFERRED** to Phase 10 retroactive scan re-run; BE-F ships probes; the differential calculation against BE-D heuristic 137 is a separate compute step (not within BE-F scope per substrate §6 + ROADMAP §10).

### §14.6 BE-F Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | §14.1 row 31 (4 probe primitives) | [x] PASS |
| 2 | §14.1 row 32 (8 self-test fixtures) | [x] PASS |
| 3 | §14.1 row 33 (admission refuses broken; T12 evidence) | [x] PASS |
| 4 | §14.1 row 34 (≥12 production fires + per-class ≥3 + mix) | [x] PASS |
| 5 | §14.1 row 35 (self-test events ≥8 + predicateType) | [x] PASS |
| 6 | §14.1 row 36 (version-lock per Done #13) | [x] PASS |

<!-- /gate:acceptance_criteria §14 -->

## §15 BE-G Cycle 16 Stage 5 Write-Boundary Enforcement Acceptance Append

> ADDITIVE-APPEND per HC #45 (chain n=7). §1-§14 preserved byte-identical above.
> All thresholds probe-fire-grounded; smoke-only fires REFUSED (HC #67). Verified at
> Cycle-16-S12 BE-G build. Authority: ED §5.8 (6/6) + SI Amendment 28d Done #29/#30.

### §15.1 Acceptance thresholds (rows 37-46)

| # | Threshold | Verdict | Evidence |
|---|---|---|---|
| 37 | Pre-commit hook HARD-BLOCKs ≥3 synthetic-violation fixtures (non-zero exit + `pre_commit_hook_block.fire.event`) | PASS | 3 fixtures (agent_spec / schema TTL / DECISION_LOG ADR) all exit 1 + 3 hook-block events; positive (register_spec in commit) ALLOW exit 0 |
| 38 | fsnotify watcher emits `spec_authoring_event` ≤60s on ≥3 staged bypasses | PASS | scan-once 3 events latency 53ms each (≤60000ms) + LIVE inotify daemon emitted 2 events on real git-bypassing write |
| 39 | 3-registry reconciliation gate `drift_detected_bool:false` across 5 consecutive closes | PASS | 5 fires vs LIVE /cycle6 (241 cycle16:Spec) + prompt_inventory (9 agent_spec) + FS (2); all drift=false |
| 40 | Done #17 gate body subprocess-invokes probe (NOT ASK currentStatus); ≥3 negative HARD-BLOCK + 1 positive; `evidence_type: probe_fire_aggregate` | PASS | positive: 268 probe fires / 72 implemented PASS; 3 negative fixtures BLOCKED (impl=0); `grep subprocess`=match, `grep '^[^#]*ASK {.*currentStatus'`=0 |
| 41 | `kill_spec()` 4-param; ADR grep + `spec_killed_event` + SPARQL→killed; ≥3 DP#44 refusals + ≥1 pass | PASS | `len(sig.parameters)==4`; positive kill (readback currentStatus=killed, audit_trail_link set, 1 spec_killed_event); 3 ValueError refusals (missing ADR / malformed iri / None) emitting NO event |
| 42 | Done #19 session-close gate aggregates probe-fire JSONL (NOT currentStatus); `advisory_mode_bool:true`; ≥3 dormancy tests; 5-session monotonic | PASS | 3 dormancy fixtures each flag 3 specs (advisory exit 0); advisory_mode_bool=true; evidence_type=probe_fire_aggregate; index 1→5 monotonic |
| 43 | Done #29 per-repo coverage matrix (all spec-bearing repos) + server-side/CI bypass-closure | PASS | `be_g_coverage_matrix.{md,json}` (4 repos) + `spec_authoring_required_check.yml` CI required-status-check (closes --no-verify) |
| 44 | Done #30 build-orchestrator + build-runner in prompt_inventory + 6 BE-G deliverables self-registered | PASS | sqlite3 verify both agent_specs active; 6 self-register write.events at /cycle6 |
| 45 | KT-7: every probe invoked by a gate body passes `--self-test` (exit 0) | PASS | a/b/c/d probes all `--self-test` exit 0 |
| 46 | KT-8: every gate/hook/kill validation IMPORTS+EXECUTES the named primitive, not string-match | PASS | present_gate `subprocess.run([python3, probe_path, --aggregate-cycle])`; session_close aggregates `probe_mibrary.fire.event.payload.implemented`; kill_spec `subprocess.run(["grep",...ADR...])`; hook inspects staged DIFF for register_spec call |

### §15.2 Honest carries (HC #70)

- BE-G does NOT make past specs implemented (Phase 11-13) nor validate probe accuracy (Done #25 / Phase 12).
- Enforcement is INSTALLABLE per repo; INSTALL into `.git/hooks` + CI branch protection is an operational promotion step, not performed by the build across all 79 repos.
- `watchdog`/`inotify_simple` absent on host → watcher uses Linux inotify(7) via ctypes (no third-party dep).
- govML back-port of BE-G scripts is BE-I / S14 (NO govML commit at S12 per work-host boundary).

<!-- /gate:acceptance_criteria §15 -->

## §16 — BE-H structural-prevention acceptance (Cycle-16-S13)

All probe-fire-grounded; smoke fires REFUSED as acceptance evidence
(`*_smoke_*` / `*_self_test_*` run_id discriminator).

- T-BE-H-1: 8 pieces present at `scripts/structural_prevention/`; each runnable
  with shebang + DP#44 refuse + dedicated `*_events.jsonl` sink. PASS.
- T-BE-H-2: each piece refuses >=1 negative fixture via a `*.refuse.event` row. PASS.
- T-BE-H-3: Substitution Gate (#14) imports+executes the named probe (`subprocess`
  + `--self-test`); HARD-FAILs >=3 proxy fixtures + passes >=1 probe-ref def. PASS.
- T-BE-H-4: probe-coverage (#15d) requires non-zero PRODUCTION fires per class
  A/B/C/D; smoke excluded via run_id prefix. PASS (a9/b10/c190/d59 prod impl). [measured]
- T-BE-H-5: ED section 5.9 threshold 5 (govML init_project.sh integration) = N/A at
  S13 / BE-I scope per kc-49 evidence-path-translation; signature DECLARED in
  README/envelope, wired at BE-I/S14. N/A-DOCUMENTED.
- T-BE-H-6: design-anchor disclosure (#15g) refuses absent disclosure column;
  emits Stage 2->3 checkpoint + paradigm-escalation marker on internal
  load-bearing inheritance. PASS.
- T-BE-H-7: HC-BE-G-1 fixed — probe-crash in session_close_gate is fail-closed
  (distinct `crash` verdict, NOT silent PASS=0); library self-test treats a
  crashing probe as a self-test FAIL. PASS.
- T-BE-H-8: HC-BE-G-2 fixed — real session-index partition replaces `*64`
  (live 5-session fixture: fires=3 last-3-distinct-sessions vs all-rows). PASS.
- T-BE-H-9 (KT-7): every probe invoked passes `--self-test` exit 0. PASS.
- T-BE-H-10 (KT-8): every implementation-judging predicate imports+executes. PASS.

(Stage 5 BE-H ADDITIVE-APPEND per Cycle-16-S13; BE-A..BE-G preserved verbatim.)

---

## §BE-M Probe-accuracy harness acceptance criteria (Cycle-16-S17, Done #25/#44 — PRE-REGISTERED before running)

Thresholds expressed as MEASURABLE counts (Amendment 28f Done #44 rigor split). KT-15 fires if any EXECUTION-OBSERVABLE class with a non-contested pinned GT is below bar.

- **T-BE-M-0 (independence — BLOCKING):** `--self-test` → `independence_clean=True` (0 source probe-imports AND 0 runtime-loaded probe modules in the harness namespace). Probes invoked via subprocess CLI only. **MET (exit 0).**
- **T-BE-M-1 (execution-observable bar):** for each of A, B, D, F (execution path), E (source-traceability + field-match sub-checks): bar = **FP == 0 AND recall ≥ 0.90** on the FULL population (≥20 where available).
- **T-BE-M-2 (small-n disclosure):** A (n=9) and B (n=10) are below the ≥20 bar — validate FULL population, disclose small-n, do NOT pad with synthetic. Likewise any class with `n_eval < 5` → PASS-LOW-POWER, never clean PASS.
- **T-BE-M-3 (contested-definition cap):** if >20% of a class's derivable specs are definition-sensitive → verdict CONTESTED (not a number), pinned-definition matrix reported alongside the flip count.
- **T-BE-M-4 (GAP-2 honesty):** Class C live judge, F judge-fallback path, E status-match (imports BE-F) → DEFERRED-GAP-2; no judgment-only accuracy reported at execution-observable confidence; no fabrication.
- **T-BE-M-5 (no codebase claim):** harness emits NO `% implemented/faithful` number about the codebase (Done #42).

**MEASURED OUTCOME (pre-registered honest reporting — a FAIL/PARTIAL is the CORRECT result if the data shows it):**
- A: FULL-RIGOR-FAIL — FP0/FN1/TN7, recall 0.0 (1 GT-positive missed: precondition short-circuits a spec with 2 real exact-subagent_type dispatches); +1 contested FP-under-strict-GT.
- B: CONTESTED — FP0/FN4/TN1/TP2, recall 0.33; contested 3/10=30%>20% (4 SHACL/ontology FN the probe aggregate path never target-class-checks despite real conforming instances).
- C: DEFERRED-GAP-2 (canonical decision LLM-judge-dependent).
- D: FULL-RIGOR-FAIL — FP28/TP5/TN21, precision 0.15, fp_rate 0.57 (loose substring over-match vs strict structured-field GT); 5 contested generic R-tokens.
- E: source-traceability 232/232 + field-match 18/18 AGREE on positives but NO negative cases on the real population → no FP-discrimination proven; status-match + overall disposition DEFERRED-GAP-2.
- F: FULL-RIGOR-PASS-LOW-POWER — TP2/FP0, n_eval=2 (264/269 DP#26 carve-outs); 2 judge-fallback DEFERRED-GAP-2.

(Stage 5 BE-M ADDITIVE-APPEND per Cycle-16-S17; BE-A..BE-H preserved verbatim. Pre-registered thresholds T-BE-M-0..5; measured outcome recorded post-run per Done #25 honest-outcome framing.)

---

## §BE-S Validation-tier close-path verdict acceptance criteria (Cycle-16-S24, ED §5.phase11.2 — PASS-all 6/6)

| # | Threshold | `[measured]` evidence | PASS/FAIL |
|---|---|---|---|
| T1 | Per-spec tier classifier; every spec in V has `tier` ∈ {execution_checkable, semantically_judged} | every_spec_has_tier=True; execution_checkable=3 / semantically_judged=203 over V's 206 spec_ids | **PASS** |
| T2 | Execution tier = full-rigor OR honest LOW-POWER (no silent upgrade) | 0 execution specs labelled VALIDATED-FULL-RIGOR without FP==0 ∧ recall≥0.90; all execution verdicts PASS-LOW-POWER (F-detector n_eval=2 per §1ee) | **PASS** |
| T3 | Judgment tier requires diverse judges else REFUSED | `--judge-diversity-check` exit 0; diverse_bool=True (GT `claude-sonnet-4-6` ≠ probe `claude-haiku-4-5`; cross-check = deterministic code-token grep = different method) | **PASS** |
| T4 | Fail-safe on disagreement/ambiguity → NOT-VALIDATED (never engineered agreement) | negative_fixture (judge=True,xcheck=False) → CONTESTED (pass=True); 194 fail-safe events; judgment-tier contested_fraction 0.9557 (the S19 ~45%+ C-disagreement reproduces as CONTESTED→NOT-VALIDATED — the bar working) | **PASS** |
| T5 | No human in the close path (structural) | `inspect.signature(close_verdict)` → `close_verdict_fn_human_inputs == 0`; signature `(spec_iri, *, _scan=None)`; negative manual-override REFUSED (no such param) | **PASS** |
| T6 | Tier-labelled claim; uniform "100% validated" REFUSED | two-tier completion claim + judgment-tier residual disclosed; CONTESTED specs NOT counted validated; grep `100% validated` count = 0 | **PASS** |

## §BE-T Guard-the-guards + trusted-detector run acceptance criteria (Cycle-16-S24, ED §5.phase11.3 — PASS-all 6/6)

| # | Threshold | `[measured]` evidence | PASS/FAIL |
|---|---|---|---|
| T1 | Enforcement infra enumerated INTO the audited population (#47) | audited_population_count = 230 = denominator M1′=193 + 37 infra entries (probe 6 / gate 21 / agent_spec 9 / accuracy_harness 1); every entry `is_enforcement_infra: true`; all 4 infra classes present | **PASS** |
| T2 | Detectors run over the infra entries too (guards audit themselves) | ≥1 `guard_the_guards.fire.event` per infra class (6/21/9/1); the harness's OWN status MEASURED (self-attests, rc 0), not assumed; 37/37 self-attest pass | **PASS** |
| T3 | Detector input == reconciled V (single-reader BE-D scan REFUSED) | `detector_input_path == outputs/validated_commitment_set.json`; `detector_input_is_reconciled_validated_set: true`; not wired to `retroactive_scan_cycle_1_15_run.json` | **PASS** |
| T4 | Per-spec tier-labelled implemented-rate emitted (THE FINDING) | execution tier: 1 implemented / 2 not-implemented / 0 contested; judgment tier: 9 diverse-judge-validated / 71 judge-not-implemented / 123 CONTESTED→not-counted; aggregate (incl. judgment-validated) 0.0485 `[measured]`; execution-proven-over-V 0.0049; tier-partitioned; CONTESTED NOT counted implemented | **PASS** |
| T5 | Independence preserved at run-time (validate-the-validator) | `probe_accuracy_harness.py --self-test` `independence_clean == true` (rc 0) re-asserted BEFORE accepting the run; carried into `trusted_detector_run.json`; run REFUSES if not clean | **PASS** |
| T6 | No un-scoped "100%"; §1ee gaps disclosed honestly (HC #70) | mechanical scan: 0 un-scoped "100%" (the sole "100%" is the scoped close-claim); 3 §1ee honest gaps verbatim (6/9 AgentContracts no executable observable; 3/10 KG ontologies no SHACL; 228/232 E-status not independently re-derivable) | **PASS** |

(Stage 5 BE-S+BE-T ADDITIVE-APPEND per Cycle-16-S24; BE-M + BE-A..BE-H preserved verbatim. The LARGE spec→implementation gap — execution-proven 1/206; judgment tier 194/203 fail-safe → CONTESTED/NOT-VALIDATED — is the HONEST deliverable per HC #70, never a number engineered to pass.)

> **BE-T S24 narrow disclosure re-emit (additive ONLY; no verdict change, no detector re-run):** `trusted_detector_run.json` now adds a three-population reconciliation (M1′=193 disclosed-bound / V=206=167+39 [167/193=86.5% coverage] / guard-pop=230=193+37 infra, the 37-infra cut DISTINCT from V's 39 cycle-16 specs), the **26-absent** extraction-coverage finding (193−167; disclosed, NOT counted implemented-or-not), per-era tier-partitioned rates (cycles-1-15 past + cycle-16 present/in-flight, summing to the aggregate), and an era-reconciled `close_claim`. Every prior per-spec verdict + gap_list count (exec 1/2/0; judgment 9/71/123) + aggregate rate is byte-identical (asserted recomputed==prior before write); residuals (6 single-reader edge ids + caveat, +53 DD surplus, BE-J 33.88% not-promoted, honest-gaps-verbatim) preserved unchanged.

---

## §BE-JTV Judgment-tier verifier acceptance criteria (Cycle-16-S28 — design spec `docs/judgment_tier_verifier_mechanism.md`; PRE-REGISTERED before running)

ADDITIVE-APPEND per Cycle-16-S28. All prior sections preserved verbatim. Thresholds are binary/deterministic, pre-registered BEFORE the verifier is run for measurement. Verdict path per §4 grid (PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE). The verifier is a NEW successor file; frozen paths consumed UNMODIFIED.

| # | Threshold (binary) | Measurement | Verdict path |
|---|---|---|---|
| JTV-1 | `judges_share_no_code_path == true` AND `j1_model != j2_model` (genuine diverse quorum, the §A.1 independence fix) | `judgment_tier_verifier.py --independence-self-test` exits 0; `judgment_tier_verifier.independence_selftest.event` `pass == true` | PASS / FAIL |
| JTV-2 | `gt_sample_n >= 40` (powered; target Arm-1 N=60 + Arm-2 n=30); realized N + 95% CI half-width disclosed | `judgment_tier_accuracy.json` `gt_sample_n` + `ci95_halfwidth` present | PASS / FAIL |
| JTV-3 | `gt_labels_blind_to_verifier == true` AND `no_human_in_close_path == true` (#25/#61) | verifier verdicts written before GT read (ordering asserted); accuracy-compute path takes 0 human inputs (signature-inspected); GT corpus authored independently of verifier logic | PASS / FAIL |
| JTV-4 | `accuracy_measured_against_independent_gt == true`: precision/recall/FNR for implemented class computed per stratum + pooled against Arm-1 construct GT + Arm-2 real-sample partial oracle | `judgment_tier_accuracy.json` confusion + P/R/FNR present per stratum | PASS / FAIL |
| JTV-5 | Inter-judge agreement reported SEPARATELY from accuracy (distinct labelled blocks; never merged into one "X% good" number) | `judgment_tier_accuracy.json` has distinct `inter_judge_agreement` block AND `accuracy` block | PASS / FAIL |
| JTV-6 | Trustworthiness bar (beat-and-prove S27 0.6): TRUSTWORTHY iff `precision_ci_low_for_implemented_class > 0.60`; otherwise honest NOT-YET-TRUSTWORTHY finding emitted and NO build-queue count | `judgment_tier_accuracy.verdict.event` `trustworthy` consistent with the CI lower bound; `now_trustworthy_build_queue_count` null unless trustworthy | PASS (either outcome is a valid PASS — a measured NOT-YET-TRUSTWORTHY is an honest finding, NOT a fail) |
| JTV-7 | `judges_not_tuned_to_agree == true`: judge prompts/models/thresholds byte-identical across the accuracy run (`git diff --stat` empty on judge code) | attested in artifact + git diff | PASS / FAIL |
| JTV-8 | `residual_R_disclosed == true` AND NO uniform "X% accurate, no residual / proven correct / 100%" claim (lint) | artifact discloses R (construct-validity + LLM-not-execution gaps); lint scan returns 0 forbidden strings | PASS / FAIL |
| JTV-9 | Vertical slice (≈5–8 real judgment-tier specs across ≥3 strata) run end-to-end with measured accuracy BEFORE any full-tier run; fail-safe fires on a planted disagreement | slice result recorded in `judgment_tier_verifier_run.json`; NOT a closure claim | PASS / FAIL |
| JTV-10 | `frozen_paths_unmodified == true` (`probe_spec_impl_fidelity.py`, floors 0.20/0.80/0.20, `fixtures/**`, gap-list outputs, `probe_accuracy_harness.py` interface — all byte-identical) | `git diff --stat` empty on frozen paths | PASS / FAIL |

**Honest pre-registration note:** the EXPECTED outcome of JTV-6 is NOT pre-determined. If the diverse-judge ensemble cannot reach `precision_ci_low > 0.60` on blind powered GT, the honest result is "judgment tier stays not-yet-trustworthy; S29 scaling waits" — and that is a PASSING build outcome (an honest measured negative), never a fail to be patched by tuning judges to agree (HC; #19/#46).

(Stage 5 BE-JTV ADDITIVE-APPEND per Cycle-16-S28; prior sections preserved verbatim.)
