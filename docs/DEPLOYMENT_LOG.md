# DEPLOYMENT LOG

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- profile: build -->
<!-- methodology_status: BE-A authored — Cycle 16 Stage 5 BE-A build event row appended -->
<!-- source: ARTIFACT_CONTRACT §5 promotion gates + build-runner.md §Step 5 build-event row template + dispatch substrate §1 item 7 -->

> **Authority Hierarchy**
>
> | Priority | Document | Role |
> |----------|----------|------|
> | Tier 1 | Cycle 16 SI ACTIVE 2026-05-27 + Amendments 27a/27b | Primary spec — highest authority |
> | Tier 2 | ARTIFACT_CONTRACT.md §5 promotion authority + rollback procedure | Clarifications — cannot override Tier 1 |
> | Tier 3 | Cycle 14 BE precedent DEPLOYMENT_LOG §2 build-event row format | Advisory only — non-binding if inconsistent with Tier 1/2 |
> | Contract | This document | Implementation detail — subordinate to all tiers above |

### Companion Contracts

**Upstream (this contract depends on):**
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §5 for promotion authority and rollback procedure
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §1 for thresholds the promotion gate consults

**Downstream (depends on this contract):**
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §3 for cross-test-bed deployment evidence
- See [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §1 for the decisions recorded at each promotion event

## Customization Guide

(Customization Guide deleted at BE-A fill close per template instruction.)

---

## §0 Deployment Identity

<!-- gate:deployment_log §0 required -->

| Field | Value |
|---|---|
| **Artifact** | `cycle_16_be_a_spec_registry_schema_and_write_boundary` (per ARTIFACT_CONTRACT §0) |
| **Test bed** | TB-1 AgentContract + TB-2 Schema + TB-3 MethodologyCommitment (3 test beds; n=3 per-test-bed strengthening) |
| **Deploy target** | azure-vm-7gb (Apache Jena Fuseki PID 479112; `/cycle6` SPARQL endpoint at http://localhost:3030/cycle6) |
| **First promotion commit** | (recorded post-fill at Cycle-16-S3 close paired-commit per Discipline #11 + PC #100) |
| **Promotion authority** | build-runner BUILT at BE-A (Cycle-16-S3) → Coach R3 evaluation → build-orchestrator promotion at Cycle-16-S4 BE-B consumer integration → Rex paradigm ruling on CONTRACT_CHANGE OR KT-6 firing per Binding 7 |

<!-- /gate:deployment_log §0 -->

---

## §1 Promotion Gate Stack

<!-- gate:deployment_log §1 entries:1 -->

The promotion gate stack runs in declared order at every promotion attempt.
A FAIL on any gate halts promotion; the artifact stays at its prior
production version until the gate PASSes (or a CONTRACT_CHANGE adjusts the gate).

| # | Gate name | Gate script (path) | What it checks | FAIL behavior |
|---|---|---|---|---|
| 1 | build_pipeline_gate | `~/ml-governance-templates/scripts/build_pipeline_gate.sh` | ARTIFACT_CONTRACT §0-§7 + RUNTIME_EMIT_SPEC §0-§6 + ACCEPTANCE_CRITERIA §0-§6 filled with 0 placeholders + canonical markers preserved | halt-promotion |
| 2 | production_deployment_gate | `~/ml-governance-templates/scripts/production_deployment_gate.sh` | DEPLOYMENT_LOG §2 build event row exists + §4 rollback procedure tested end-to-end | halt-promotion |
| 3 | cross_system_validation_gate | `~/ml-governance-templates/scripts/cross_system_validation_gate.sh` | ACCEPTANCE_CRITERIA §3 per-test-bed strengthening n≥3 PASS verdicts | halt-promotion |
| 4 | hc26_internal_smoke_gate | `~/ml-governance-templates/scripts/hc26_internal_smoke_gate.sh` | N≥3 PASS rows in BUILD_DECISION_LOG §N.5 internal-smoke subsection (fresh-scaffold findability + per-artifact CLI cleanliness + backwards-compatibility preservation) | halt-promotion |
| 5 | k_register_present_gate | `~/ml-governance-templates/scripts/k_register_present_gate.sh` | Cycle 14 inheritance: docs/k_register.md exists + placeholder zero + ≥1 §N.1.M H-disconfirmation subsection | halt-promotion (advisory-mode opt-in via --advisory-mode) |

<!-- /gate:deployment_log §1 -->

> [SEED: min_gates=1]
> The build-class gate stack mirrors the research-class `check_all_gates.sh`
> wrapper pattern: a single composite invocation runs the full stack and
> emits per-gate verdicts. Gate scripts ship at
> `~/ml-governance-templates/scripts/build_*.sh` (parallel to the research-class
> `landscape_depth_gate*.sh` / `pre_compute_check.sh`).

---

## §2 Promotion Event Log (append-only)

| # | Timestamp | Commit | Gate stack verdict | Promotion verdict | Operator | Notes |
|---|---|---|---|---|---|---|
| 1 | 2026-05-27T19:30:00Z | (recorded at Cycle-16-S3 close paired-commit) | N/A (build event; gate stack verdicts at promotion event at Cycle-16-S4 BE-B consumer integration) | BUILT (not yet PROMOTED) | build-runner | BE-A build artifact stack produced: docs/spec_registry_schema.ttl (112 triples) + docs/spec_registry_shapes.shacl.ttl (103 triples) + docs/spec_authoring_discipline.md (5 operations + HC-11 + PROV-O + nanopub) + 3-test-bed live SPARQL UPDATE smoke ALL_PASS (TB-1 HTTP 200 257ms readback 13 triples; TB-2 HTTP 200 222ms readback 13 triples; TB-3 HTTP 200 222ms readback 14 triples; DROP GRAPH cleanup HTTP 200 186ms). SHACL polymorphism via subclass inheritance VERIFIED (conforming fixture conforms=True; non-conforming fixture 8 violations ≥4 threshold). Pending Cross-System-Validator at Workflow step 4 + Promotion-Gate Stack at Workflow step 5. |
| 2 | 2026-05-27T19:55:00Z | (recorded at Cycle-16-S4 close paired-commit; 4-repo: cycle_16 + EMABS + Moonshots + govML per Rex back-port directive) | N/A (build event; gate stack verdicts at promotion event at Cycle-16-S5 BE-C consumer integration) | BUILT (not yet PROMOTED) | build-runner | BE-B build artifact stack produced: scripts/spec_registry_authoring.py (29.8KB; 5 Ops + record_author_refusal helper; SHACL pre-validation + DP#26 n_a_rationale wrapper-side enforcement + 4-class refusal taxonomy) + scripts/install_spec_registry_authoring_discipline.sh (3.4KB; bash-syntax-clean; idempotent) + govML init_project.sh install_hook ADDITIVE-APPEND (NEW install_spec_registry_authoring_discipline function L210+ + call-site at research-build profile branch AFTER install_runtime_emit_substrate) + govML templates/build/spec_registry/ NEW directory (5 files: spec_registry_authoring.py + 3 BE-A artifacts copied verbatim + SPEC_AUTHORING_DISCIPLINE.md obligation doc authored) + govML VERSION bump v2.8.2 → v2.8.3 + 3-TB dogfooding to PRODUCTION /cycle6 registry graphs ALL_PASS (TB-1 AgentContract HTTP 200 244ms readback 13 triples; TB-2 Schema HTTP 200 218ms readback 13 triples; TB-3 MethodologyCommitment DP#26 HTTP 200 200ms readback 15 triples + n_a_rationale present). Fresh-scaffold govML smoke `/tmp/be_b_smoke_<ts>` ships 7 expected files cleanly + wrapper imports + 11 mandatory fields + 4 spec-classes + 5 statuses + 4 refusal classes resolved. Brief 4 KT-3 firing surface evaluation: 0 author refusals captured at BE-B dogfooding; (a)+(b)+(d) cumulative = 0 < threshold 3 → KT-3 DOES NOT FIRE. Pending Cycle-16-S5 BE-C TWO-surface BLOCKING gate build + Cross-System-Validator + Promotion-Gate Stack. |
| 3 | 2026-05-27T21:10:00Z | (recorded at Cycle-16-S5 close paired-commit; 4-repo: cycle_16 + EMABS + Moonshots + govML per Rex back-port directive STANDING) | N/A (build event; gate stack verdicts at promotion event at Cycle-16-S6 BE-D consumer integration + Cycle 17+ retroactive scan) | BUILT (not yet PROMOTED) | build-runner | BE-C build artifact stack produced: `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` (325L; cycle-close BLOCKING per Operation 3; mirrors k_register_present_gate.sh 231L skeleton per H6 metric; SPARQL ASK via Python urllib substituted at predicate body) + `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` (337L; session-close ADVISORY default per Operation 4; --blocking-mode opt-in; same skeleton structure; SESSIONS_BETWEEN pre-computed at shell layer via grep -c) + check_all_gates.sh BLOCKING loop extended to 5 gates (5th-gate append) + NEW ADVISORY loop appended for session-close-gate with --advisory-mode explicit (LOCKED 4-gate loop body preserved) + govML init_project.sh install_hook ADDITIVE-APPEND (NEW install_spec_implementation_gates function L284+ + call-site at research-build profile branch AFTER install_spec_registry_authoring_discipline; existing v2.8.2 + v2.8.3 functions UNCHANGED) + govML templates/build/spec_implementation_gates/ NEW directory (1 file: SPEC_IMPLEMENTATION_GATES_OBLIGATION.md ~8KB declaring TWO-surface gate interface + HC-11 partition + authority chain) + govML VERSION bump v2.8.3 → v2.8.4 + 3-TB dogfooding to PRODUCTION /cycle6 registry graphs ALL_3_PASS (TB-1 conforming-running write_success+readback_match; TB-2 dormant-with-explicit-deferral-and-rex-authorization write_success+readback_match+ASK FILTER NOT EXISTS excludes; TB-3 dormant-silent-past-threshold write_success+readback_match+cycle-close holistic verdict BLOCKED load-bearing+dormant_silent_present_bool=true). Fresh-scaffold govML smoke `/tmp/be_c_smoke_<ts>` ships docs/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md + outputs/spec_implementation_gates_events.jsonl + 5 prior install outputs all present (cumulative install_hook chain: runtime_emit + spec_registry + spec_implementation_gates all operational). H6 metric CONFIRMED (skeleton structural equivalence verified via diff vs k_register_present_gate.sh; divergence categories (a)+(b)+(c)+(d) per dispatch substrate §3 + honest carry (e) JSONL fire.event emit block at script close — load-bearing for HC #26 internal smoke Gate 2; not present in k_register skeleton). KT-4 firing surface: DOES NOT FIRE (cycle-close gate BLOCKED correctly on TB-3 dormant-silent surface; no FALSE NEGATIVE; HC #59 BINDING screen applied; SPARQL ASK substitution at gate-script-shell-script primitive layer sufficient; no new enforcement primitive class required). Production graph baseline pre/post equal (246101 triples both sides; DROP cleanup verified per dispatch substrate §4). JSONL fire.event sink ≥4 rows (present_gate CLEAR + present_gate BLOCKED + session_close_gate CLEAR + session_close_gate ADVISORY_FAIL). Pending Cycle-16-S6 BE-D retroactive scan + Cross-System-Validator + Promotion-Gate Stack. |
| 4 | 2026-05-27T22:40:00Z | (recorded at Cycle-16-S6 close 3-repo paired-commit; cycle_16 + EMABS + Moonshots; NO govML at BE-D per work-host boundary discipline per dispatch substrate §0 + §9) | N/A (build event; gate stack verdicts at promotion event at Cycle-16-S7 BE-E forward-apply observation consumer integration) | BUILT (not yet PROMOTED) | build-runner | BE-D build artifact stack produced: `outputs/retroactive_scan_cycle_1_15_run.json` (~190KB; aggregate_counts_4x5 + per_spec_evidence_IP_PRIVATE + h1/h3/kt_2 verdicts + per_class_strengthening_n_ge_3 outcomes + hc_be_d_1_honest_carry + production_graph_baseline_pre/post + retroactive_classification_annotation=true) + 4-spec-class enumeration via substrate-declared commands (Class (a) AgentContract `ls .claude/agents/*.md` n=9 distinct; Class (b) Schema `find scripts/runtime_emit + cycle_6 shapes + cycle_10 ontologies + cycle_16 spec_registry` n=10 distinct; Class (c) DesignDecision `DECISION_LOG.md + state.json paradigm_dispositions/decisions_log/honest_carries across 15 cycle dirs` n=154 distinct (190 raw with 36 idempotent-minting collisions resolved); Class (d) MethodologyCommitment `FINDINGS.md token enumeration across 26 files` n=59 distinct) + 5-state classification per dispatch substrate §1.3 verbatim (running / dormant-with-explicit-deferral / dormant-silent / killed / long-running) + classification heuristic resolution preference (structural runtime emit > citation evidence > deferral edge > retraction ADR > dormant-silent default) + DP#26 carve-out applied to MethodologyCommitment + dormant-silent AgentContract + cycle_10 Schemas (runtime_emit_event_class='n/a — citation-based activation per DP#26' + n_a_rationale per HR §3d) + per-spec materialization at PRODUCTION /cycle6 via BE-B `register_spec()` (268 raw writes; 232 distinct after deterministic idempotent sha256_8 minting; 235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 persisted; 8 initial DP#26 refusals → 8 retry successes with explicit n_a_rationale; `retroactive_classification=true` annotation per write per ROADMAP §4.2 dependency 2; bulk write namespace `cycle_16.be_d.retroactive_scan` namespace-isolated from BE-A/B/C namespaces per Cycle 10 namespace-isolation invariants) + §12 BE-D appends at 3 cycle_16 docs (ARTIFACT_CONTRACT §12 + RUNTIME_EMIT_SPEC §12 with 1 NEW event class `retroactive_scan_run.event` + ACCEPTANCE_CRITERIA §12) + DEPLOYMENT_LOG §2 row 4 + BUILD_DECISION_LOG §2 row 4 (this row) + `outputs/build_runner_envelope.yaml` OVERWRITE + `outputs/build_runner_events.jsonl` append with single `retroactive_scan_run.event` close-fire. H1 metric **CONFIRMED** (h1_total_enumerated=232 distinct ≥ 90 floor; raw=268 with 36 collisions; 2.6x floor multiplier). H3 metric **CONFIRMED** (h3_dormant_silent_aggregate=137 ≥ 3 threshold; per-class breakdown: 7 a + 2 b + 117 c + 11 d). KT-2 firing surface: **DOES NOT FIRE** (dormant_silent count 137 well above threshold 3; HC #59 BINDING screen applied — pre-registered SI kill condition not operationally-revisable; threshold evaluated literally per HC #59 disambiguation). HC-BE-D-1 honest carry SURFACED: write-boundary enforcement gap (specs written to filesystem without calling BE-B authoring wrapper) → Cycle 18 scope per Rex 2026-05-27 Option A disposition + Option B split-sequential framing; BE-D retroactive scan fills historical inventory by enumeration but does NOT enforce forward. NO DROP GRAPH at BE-D close (retroactive registry rows persist for BE-E forward-apply observation baseline reconstruction; unlike BE-A/B/C smoke specs). NO govML back-port at BE-D (one-time within-cycle artifact per work-host boundary discipline per dispatch substrate §0 + §9). Production graph baseline pre-BE-D (default graph triples) = 6; post-BE-D full triple store = 250779 (~4680 net add for 232 specs × ~20 triples each / 3 nanopub graphs). Pending Cycle-16-S7 BE-E forward-apply observation (`spec_authoring_event` + `spec_implementation_event` classes into runtime_emit/emit.py + `docs/forward_apply_observation_protocol.md` authoring + smoke-test per ROADMAP §5) + Cross-System-Validator + Promotion-Gate Stack. |
| 5 | 2026-05-28T00:30:00Z | (recorded at Cycle-16-S7 close 4-repo paired-commit; cycle_16 + EMABS + Moonshots + govML per Rex back-port directive STANDING 2026-05-27; HC #45 ADDITIVE-APPEND chain extension to n=5) | N/A (build event; gate stack verdicts at promotion event at Cycle-16-S8 close FINDINGS authoring) | BUILT (not yet PROMOTED) | build-runner | BE-E build artifact stack produced: `scripts/runtime_emit/emit.py` extended ADDITIVELY (2 NEW event class registration constants `SPEC_AUTHORING_EVENT_CLASS` + `SPEC_IMPLEMENTATION_EVENT_CLASS` + sink-routing helper `forward_apply_emit()` + namespace constant `FORWARD_APPLY_OBSERVATION_NAMESPACE` + sink default `FORWARD_APPLY_OBSERVATION_SINK_DEFAULT`; `emit_event()` core signature UNCHANGED per Cycle 10 §0 schema_version=0.1 LOCKED — verified via Python `inspect.signature(emit_event)` returns Cycle 15 BE#4 baseline signature) + `docs/forward_apply_observation_protocol.md` NEW (~143L; 8 §N sections covering §0 scope + §1 event-class taxonomy + §2 session-close hook + §3 cycle-close aggregate hook + §4 longitudinal verdict surface (Cycle 18 + KT-5 evaluation) + §5 refusal-on-violation discipline + §6 HC-11 partition + §7 self-test; 0 placeholders; HC-11 partition declared inline per Binding 8 BIND) + `outputs/forward_apply_observation_events.jsonl` NEW (sink-exists invariant established via touch at BE-E build step 4; 4 fire.event rows emitted at BE-E smoke close: 2 `spec_authoring_event` + 2 `spec_implementation_event` for TB-1 AgentContract synthetic + TB-2 Schema synthetic with PROV-O 4-typed-edges (`wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy` per Cycle 6 BE#1 contract) + HC-11 `c6:publishable` access_permission enum) + §13 BE-E appends at 3 cycle_16 docs (ARTIFACT_CONTRACT §13 + RUNTIME_EMIT_SPEC §13 with 2 NEW event classes + ACCEPTANCE_CRITERIA §13) + DEPLOYMENT_LOG §2 row 5 (this row) + BUILD_DECISION_LOG §2 row 5 + `outputs/build_runner_envelope.yaml` OVERWRITE (BE-D → BE-E envelope) + `outputs/build_runner_events.jsonl` append with 1 `forward_apply_smoke.event` single-fire NEW event class at BE-E close + `outputs/spec_registry_events.jsonl` append-only growth (smoke-test SPARQL INSERT DATA write events at test graph, DROP-cleaned at smoke close) + govML v2.8.5 ADDITIVE-APPEND back-port (4 files: `~/ml-governance-templates/scripts/init_project.sh` NEW `install_forward_apply_observation()` function defined after `install_spec_implementation_gates()` + function added to research-build profile dispatch list ADDITIVE + `~/ml-governance-templates/templates/build/forward_apply_observation/` NEW dir with 2 files FORWARD_APPLY_OBSERVATION_OBLIGATION.md + forward_apply_observation_protocol.md + VERSION v2.8.4 → v2.8.5 (new header line prepended; v2.8.4 header preserved verbatim) + CHANGELOG.md NEW with v2.8.5 entry citing Cycle-16-S7 BE-E + 4-repo paired commit + HC #45 ADDITIVE-APPEND chain n=5; LOCKED bodies of `install_runtime_emit_substrate` + `install_spec_registry_authoring_discipline` + `install_spec_implementation_gates` UNMODIFIED — `git diff` 0 on those function line ranges verified at R3). H8 evaluation surface ENABLED at BE-E (FINAL VERDICT DEFERRED to Cycle 18 cumulative ≥2-cycle window per HR §3 H8). KT-5 firing surface evaluated at BE-E close per `forward_apply_observation_protocol.md` §4 + dispatch substrate §5 + task context Step 7: SPARQL query at `/cycle6` for Cycle-16-authored dormant-silent specs EXCLUDING BE-D retroactive (IRI-prefix discriminator `spec_retroactive_*` per BE-D §12.5 rollback discriminator) returns count = 0 → **KT-5 DOES NOT FIRE** (0 < 2 threshold); HC #59 BINDING screen applied — pre-registered SI kill condition not operationally-revisable. Honest gap surfaced re (a) mid-Cycle-16 observation window S7→S8 may be insufficient for full longitudinal verdict (cumulative ≥2-cycle window evaluation deferred to Cycle 18) + (b) IRI-prefix discriminator vs `retroactiveClassification` predicate gap (BE-D acceptance promised `retroactiveClassification=true` annotation predicate; actual implementation uses IRI prefix per BE-D §12.5 rollback discriminator — query corrected to use IRI-prefix filter per BE-D §12.5 verbatim). HC-BE-D-1 write-boundary enforcement gap PRESERVED as honest carry at BE-E (BE-E inherits SAME blind spot as BE-D; observes only BE-B-mediated path; closure → Cycle 18 scope per Rex 2026-05-27 Option B split-sequential). DROP GRAPH cleanup at BE-E smoke close HTTP 200 verified; post-DROP test graph COUNT = 0 verified; production registry untouched (235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 persisted EQUAL pre/post BE-E). Pending Cycle-16-S8 Cycle 16 close 5-layer FINDINGS authoring (ROADMAP Phase 7) + Cross-System-Validator + Promotion-Gate Stack. |
| 6 | 2026-05-28T17:30:00Z | (recorded at Cycle-16-S11 close 3-repo paired-commit; cycle_16 + EMABS + Moonshots; NO govML at S11 per dispatch substrate §1 item 11 + ED §5.7 evidence-path translation; v2.8.5 STANDS UNMODIFIED; govML upstream probe library + Operational-Definition Substitution Gate + structural-prevention layer back-port at v2.8.6 ADDITIVE-APPEND chain extension to n=6 lands at BE-I S14+ per HC #45 chain extension precedent) | N/A (build event; gate stack verdicts at promotion event at Cycle-16-S12 BE-G consumer integration) | BUILT (not yet PROMOTED) | build-runner | BE-F build artifact stack produced: 4 probe primitives at `scripts/probes/{a,b,c,d}/probe_<class>.py` (Class A AgentContract behavioral via OTEL JSONL tool_use scan + Class B Schema behavioral via call-site/inline-exec/JSONL exercise + Class C DesignDecision structural-judge with file:line citation per HC #72 anti-substitution + Class D MethodologyCommitment behavioral via downstream JSONL fire OR cross-cycle citation; each executable + each carries PROBE_VERSION = "0.1" + PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae" per Done #13 version-lock) + `scripts/probes/c/llm_judge_prompt.md` (HC #72 anti-substitution language explicit forbidding registry-text-only / ADR-text-only / FINDINGS-mention-only as acceptance evidence; calibration fixtures referenced) + `scripts/probes/__init__.py` (admission-gate Python module exposing `admit_all()` + `expose_admitted()` + ADMITTED_PROBES + REFUSED_PROBES; DP#44-compliant refuse-on-self-test-fail) + `scripts/probe_library_admission.sh` (bash CLI/CI wrapper; exit 0 iff all admitted; exit 1 on any refusal; emits per-probe admission events) + 8 self-test fixtures at `tests/probes/fixtures/known_{good,bad}_{a,b,c,d}_1.json` (1 known-good + 1 known-bad per class A/B/C/D) + 3 NEW JSONL sinks (`outputs/probe_fire_events.jsonl` + `outputs/probe_library_self_test_events.jsonl` + `outputs/probe_library_admission_events.jsonl`) + §14 BE-F appends at 3 cycle_16 docs (ARTIFACT_CONTRACT §14 with 6 post-conditions rows 31-36 + 4 invariants rows 22-25 + 12-row §14.7 self-test all PASS; RUNTIME_EMIT_SPEC §14 with 4 NEW event classes + 6 §14.6 self-test all PASS; ACCEPTANCE_CRITERIA §14 with 6 thresholds rows 31-36 + per-test-bed strengthening at 4 spec classes + Honest Resolution Log + 6 §14.6 self-test all PASS) + DEPLOYMENT_LOG §2 row 6 (this row) + BUILD_DECISION_LOG §2 row 6 + state.json transition + DECISION_LOG D-S11-1 + `outputs/build_runner_envelope.yaml` OVERWRITE (BE-E → BE-F envelope) + `outputs/build_runner_events.jsonl` append with 1 `be_f_probe_library_ship.event` single-fire NEW event class at BE-F close. All 6 ACCEPTANCE_CRITERIA §14.1 thresholds **PASS-all** (rows 31-36): row 31 = 4 probes shipped executable + version-locked; row 32 = 8 fixtures parseable + per-class pair; row 33 = T12 negative test verified admission refusal (synthetic broken probe rejected with exit code 1 + refuse event emitted; broken probe removed post-T12; canonical 4-probe admission scan returns exit 0); row 34 = 16 production fires (4 per class A/B/C/D; mix implemented vs not_implemented: A(2/2) B(2/2) C(1/3) D(1/3) all classes ≥1 each); row 35 = ≥8 self-test events with predicateType `cycle16:probe_self_test_v1` distinct from production `cycle16:probe_fire_v1`; row 36 = version-lock verified (PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned in 4 probe bodies + admission events SHA single-valued). KT-7 + KT-9 + KT-10 firing surfaces evaluated: KT-7 DOES NOT FIRE (4 admitted probes distinguish + T12 negative refusal verified); KT-9 DOES NOT FIRE (no generic-emission escape primitives in 4 probe bodies; admission refuses by construction via per-class behavioral evidence shape); KT-10 DOES NOT FIRE (≥1 production fire on every class A/B/C/D; in fact 4 per class). KT-8 firing surface evaluated structurally at Class C structural-judge anti-substitution refusal (embodimentRef IS DECISION_LOG → refuse with HC #72 evidence; KT-8 anti-substitution discipline verified in known_bad_c_1 fixture). HC-BE-D-1 boundary discipline PRESERVED (BE-F probes consume `/cycle6` SPARQL endpoint via SELECT/ASK only — no INSERT/UPDATE/DELETE/DROP from probe bodies; canonical production registry untouched). govML v2.8.5 STANDS UNMODIFIED at BE-F (NO govML touch at S11; back-port v2.8.6 → BE-I S14+). LOCKED preservation verified: BE-A §1-§3 + BE-B §10 + BE-C §11 + BE-D §12 + BE-E §13 byte-identical via md5 head-N comparison per file (lines 1-594 of ARTIFACT_CONTRACT.md / 1-647 of RUNTIME_EMIT_SPEC.md / 1-566 of ACCEPTANCE_CRITERIA.md all md5-match HEAD baseline). Pending Cycle-16-S12 BE-G Operational-Definition Substitution Gate (Done #14 + H_recovery_4) + Cross-System-Validator + Promotion-Gate Stack. |

> Promotion event log is APPEND-ONLY. Rollback events emit new rows with
> `verdict=ROLLED_BACK` referencing the superseded promotion. Edits to
> prior rows are forbidden; corrections emit new rows with explicit
> supersede references.

---

## §3 Per-Test-Bed Deployment Roll-up

<!-- gate:deployment_log §3 entries:1 -->

A build-class artifact's deployment story is read across test beds. Roll-up
the per-test-bed promotion verdicts and verdict count toward the n≥3 threshold.

| Test bed | Cycle | Promotion verdict | Production duration | Acceptance verdict at this bed | Cross-system evidence row link |
|---|---|---|---|---|---|
| TB-1 AgentContract | Cycle 16 BE-A | HELD (BUILT not PROMOTED at BE-A; PROMOTED at BE-B consumer integration target) | 0 sessions (BE-A close-smoke only; test graph DROP GRAPH cleanup at close) | PASS — UPDATE HTTP 200 257ms + readback 13 triples + SHACL conforms=True | `outputs/cross_system_validation_be_a.json` row `be_a_smoke_results[0]` |
| TB-2 Schema | Cycle 16 BE-A | HELD | 0 sessions | PASS — UPDATE HTTP 200 222ms + readback 13 triples + SHACL conforms=True | `outputs/cross_system_validation_be_a.json` row `be_a_smoke_results[1]` |
| TB-3 MethodologyCommitment (DP#26 carve-out) | Cycle 16 BE-A | HELD | 0 sessions | PASS — UPDATE HTTP 200 222ms + readback 14 triples (including deferral_reason) + SHACL accepts `n/a` runtime_emit_event_class literal | `outputs/cross_system_validation_be_a.json` row `be_a_smoke_results[2]` |

<!-- /gate:deployment_log §3 -->

> [SEED: min_test_beds=3]
> Until n≥3 test beds have at least PROMOTED+ACCEPTED verdict, the artifact's
> deployment story is INCONCLUSIVE at the program level (single-test-bed
> success is INCONCLUSIVE evidence per the build-class evidence grammar).

---

## §4 Rollback Procedure (referenced from ARTIFACT_CONTRACT §5)

| Step | Command / hook | Expected outcome | Verification |
|---|---|---|---|
| 1 | `python3 -c "import urllib.request, urllib.parse; data=urllib.parse.urlencode({'update':'DROP GRAPH <http://cycle16.local/test/be_a_smoke>'}).encode(); print(urllib.request.urlopen('http://localhost:3030/cycle6/update', data=data).status)"` | HTTP 200; test graph triples removed | Tested end-to-end at BE-A smoke close 2026-05-27 — DROP GRAPH cleanup HTTP 200 186ms verified (see §2 row 1 Notes) |
| 2 | `rm docs/spec_registry_schema.ttl docs/spec_registry_shapes.shacl.ttl docs/spec_authoring_discipline.md outputs/cross_system_validation_be_a.json outputs/be_a_smoke_fixture_*.ttl outputs/build_runner_envelope.yaml` | All BE-A NEW artifact files deleted | Tested via `ls` of canonical paths post-delete returns "no such file" |
| 3 | `git -C ~/cycle_16_close_spec_to_implementation_gap_build checkout docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA,DEPLOYMENT_LOG,BUILD_DECISION_LOG}.md` | Scaffolded template Edits reverted to pre-BE-A baseline | Tested via `git diff` post-revert returns empty for those 5 files |
| 4 | `git -C ~/cycle_6_unified_substrate_build diff runtime/jena/` returns empty | Confirms Cycle 6 LOCKED body UNMODIFIED throughout BE-A (Path γ FORBIDDEN per Binding 7) | Verified at HC #26 internal smoke gate 3 (backwards-compat preservation) — see BUILD_DECISION_LOG §1.5 |

> Rollback MUST be tested (executed end-to-end on a non-production test bed)
> BEFORE the artifact's first production promotion. A documented-but-untested
> rollback is documentation-active discipline (the failure shape Cycle 1
> Pattern B catalogs).

---

## §5 Promotion-FAIL Diagnostic Path

When the gate stack returns FAIL_AT_GATE_<N>, classify per this grid before
recording in [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §2:

| Shape | Diagnosis | Disposition |
|---|---|---|
| **Acceptance threshold miss** | A row in [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §1 returned FAIL or FAILS-WITH-DIAGNOSED-SHAPE | Halt promotion; record diagnosed shape in BUILD_DECISION_LOG |
| **Pre-condition violation** | A row in [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §1 was not held during measurement | Restore pre-condition; re-run gate; do NOT promote |
| **Runtime-emit absent / malformed** | A row in [RUNTIME_EMIT_SPEC](RUNTIME_EMIT_SPEC.tmpl.md) §1 was missing required field or schema version | Halt promotion; surface the missing field; do NOT route around |
| **Side-effect drift** | The artifact wrote outside [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §4 declared surface | Restore surface; tighten contract; re-run |
| **Gate-script defect** | The gate script itself failed for reasons unrelated to the artifact (e.g., dependency missing) | Fix the gate; re-run; do NOT classify as artifact failure |

> The diagnostic path mirrors [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §4
> failure-shape grid. The shared structural rule: a FAIL is *diagnosed*
> before it is repaired; "tighter threshold" or "skip the gate this round"
> are forbidden repair shapes.

---

## §6 Self-test (BEFORE first production promotion)

| # | Check | Status |
|---|---|---|
| 1 | §1 promotion gate stack lists ≥1 gate with a script path that exists and is executable | [x] (5 gates: build_pipeline_gate.sh + production_deployment_gate.sh + cross_system_validation_gate.sh + hc26_internal_smoke_gate.sh + k_register_present_gate.sh; all at canonical `~/ml-governance-templates/scripts/` paths) |
| 2 | §1 gates resolve to load-bearing rows of [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) and [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) (not "advisory only") | [x] (gates 1-4 BLOCKING per AC §1 thresholds + AC §3 test beds; gate 5 advisory-mode-opt-in only) |
| 3 | §4 rollback was executed end-to-end on a non-production target with VERIFIED column populated | [x] (rollback step 1 DROP GRAPH `<http://cycle16.local/test/be_a_smoke>` executed at BE-A smoke close: HTTP 200 186ms; non-production test graph) |
| 4 | §3 per-test-bed roll-up has rows pre-allocated for each ROADMAP-committed test bed (rows MAY be empty awaiting promotion) | [x] (TB-1 + TB-2 + TB-3 rows populated with BE-A close-smoke verdict PASS for all 3) |
| 5 | §0 promotion authority is a named role/operator (not "TBD") | [x] (build-runner → Coach R3 → build-orchestrator → Rex on CONTRACT_CHANGE) |

> If any check is `[ ]`, halt-and-surface; do NOT promote.
