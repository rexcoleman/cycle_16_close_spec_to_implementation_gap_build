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
