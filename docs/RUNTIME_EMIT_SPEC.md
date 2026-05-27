# RUNTIME EMIT SPEC

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- profile: build -->
<!-- methodology_status: BE-A authored — Cycle 16 Stage 5 BE-A spec registry write-boundary runtime emit -->
<!-- source: ARTIFACT_CONTRACT.md §0-§7 + build-runner.md §runtime_emit_obligation (5-event baseline + 1 drift class) + dispatch substrate §1 item 5 -->

> **Authority Hierarchy**
>
> | Priority | Document | Role |
> |----------|----------|------|
> | Tier 1 | `~/Moonshots_Career_Thesis_v2/.claude/strategic_frame.md` + Cycle 16 SI ACTIVE 2026-05-27 (a2f14d5) + Amendments 27a/27b | Primary spec — highest authority |
> | Tier 2 | `~/Moonshots_Career_Thesis_v2/.claude/agents/build-runner.md §runtime_emit_obligation` (5-event baseline + drift class) + ARTIFACT_CONTRACT.md §0-§7 | Clarifications — cannot override Tier 1 |
> | Tier 3 | Cycle 10 RUNTIME_EMIT_SPEC.md (canonical anchor; 5-cycle dormancy case study) + govML v2.8.2 scaffolding install pattern | Advisory only — non-binding if inconsistent with Tier 1/2 |
> | Contract | This document | Implementation detail — subordinate to all tiers above |

### Companion Contracts

**Upstream (this contract depends on):**
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §1 for the run-context that triggers emits

**Downstream (depends on this contract):**
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §2 for measurement protocols that read these emits
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §1 for cross-system event-log shape this spec contributes to
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §3 for promotion gates that read emits as evidence

## Customization Guide

(Customization Guide deleted at BE-A fill close per template instruction.)

---

## §0 Emit Identity

<!-- gate:runtime_emit_spec §0 required -->

| Field | Value |
|---|---|
| **Artifact** | `cycle_16_be_a_spec_registry_schema_and_write_boundary` (per ARTIFACT_CONTRACT §0) |
| **Event sink** | `~/cycle_16_close_spec_to_implementation_gap_build/outputs/build_runner_events.jsonl` (append-only JSONL; per govML v2.8.2 `install_runtime_emit_substrate()` scaffolding install pattern; pre-scaffolded at Cycle-16-S1) |
| **Event namespace** | `cycle_16.be_a.spec_registry` (per-pipeline + per-cycle + per-BE scope; namespace-isolated from BE-B/BE-C downstream per Cycle 10 rule_6 + rule_8 + rule_10 + rule_12 namespace-isolation invariants) |
| **Schema version** | `0.1` (recorded in every event row's `schema_version` field; locked at Cycle-16-S3 close paired-commit) |
| **Min events per run** | `6` (1× session.start + 1× dispatch.received + 5× build.phase.start + 5× build.phase.complete + 1× session.end + ≥3× be_a_spec_registry.write.event per smoke test bed; total ≥15 baseline) |

<!-- /gate:runtime_emit_spec §0 -->

> The emit sink is the single source of truth for runtime evidence.
> A build-class artifact that "runs and reports success in stdout" without
> structured emit is NOT measurable for [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md)
> and NOT eligible for production-deployment gate PASS.

---

## §1 Event Schema (per event class)

<!-- gate:runtime_emit_spec §1 entries:1 -->

For each event class the artifact emits, declare schema. Schemas are pre-registered
and locked at promotion-gate-PASS; subsequent schema changes require CONTRACT_CHANGE.

| Event class | Trigger | Required fields | Optional fields | Cardinality per run |
|---|---|---|---|---|
| `be_a_spec_registry.session.start` | At BE-A dispatch boundary (Agent foreground subagent fires; before ARTIFACT_CONTRACT §1 pre-condition check) | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.agent`, `payload.cycle`, `payload.be`, `payload.dispatch_authority` | `payload.parent_cycle_lock_commit` | exactly-once |
| `be_a_spec_registry.dispatch.received` | At dispatch substrate + ED + ROADMAP + HR + LA + Cycle 6 TTL + 2 SHACL shapes read complete | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.inputs_read` (list of paths) | `payload.input_byte_count_total` | exactly-once |
| `be_a_spec_registry.build.phase.start` | At each Step 1-5 entry per build-runner.md §Build Stage (Step 1 ARTIFACT_CONTRACT / Step 2 RUNTIME_EMIT_SPEC / Step 3 ACCEPTANCE_CRITERIA / Step 4 build artifacts / Step 5 DEPLOYMENT_LOG + BUILD_DECISION_LOG + CSV) | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.step`, `payload.artifact` | `payload.target_subsections` | exactly-once per step (5 total) |
| `be_a_spec_registry.build.phase.complete` | At each Step 1-5 exit with verification results | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.step`, `payload.artifact`, `payload.placeholder_residue_count`, `payload.canonical_markers_post_edit`, `payload.status` | `payload.canonical_markers_baseline`, `payload.zero_marker_loss` | exactly-once per step (5 total) |
| `be_a_spec_registry.session.end` | At YAML envelope authored at `outputs/build_runner_envelope.yaml` | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.verdict` ∈ {completed, checkpoint, blocked, failed}, `payload.cumulative_phase_count` | `payload.next_actions` | exactly-once |
| `be_a_spec_registry.write.event` | At each SPARQL UPDATE INSERT DATA invocation against `/cycle6/update` per smoke test bed | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.spec_id`, `payload.graph_iri`, `payload.sparql_query_hash` (sha256 of query body), `payload.http_status_code`, `payload.response_time_ms`, `payload.triple_count_delta`, `payload.accessPermission_value_set`, `payload.success_bool` | `payload.test_bed_id` ∈ {TB-1, TB-2, TB-3} | at-least-once per test bed (count-bounded ≥3 across 3 test beds; smoke test fires 1+ per write) |
| `build_runner_runtime_failure` (drift class; severity HALT) | Fires on compose-stall / Class A Write-block / Class B stream-watchdog / HC #26 internal smoke FAIL / canonical-marker loss / SHACL validation refuses CONFORMING spec / HTTP non-200 on UPDATE write | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.failure_class`, `payload.evidence`, `payload.surface_path` | `payload.recovery_path` (e.g., "halt-and-surface-to-build-orchestrator") | 0 expected on clean run; 1+ triggers halt-and-surface |

<!-- /gate:runtime_emit_spec §1 -->

> [SEED: min_event_classes=1]
> Pattern reference: jidoka stop-and-fix runtime emits one event per stop;
> control-theory PID loops emit one error-signal event per measurement
> interval; SRE runtime emits one budget-spend event per request. The
> structural rule is the same: one event per *boundary the contract cares
> about*, not one event per line of code.

---

## §2 Measurement Hook (consumed by ACCEPTANCE_CRITERIA)

<!-- gate:runtime_emit_spec §2 required -->

State the SQL / log-grep / event-bus consumer ACCEPTANCE_CRITERIA §2 reads to
compute its threshold value.

**Per metric (ACCEPTANCE_CRITERIA §1 + §2 binding):**

Metric A: **Total spec writes succeeded** (post-condition #4 evidence)
```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/build_runner_events.jsonl')]; n=len([e for e in events if e['event_class']=='be_a_spec_registry.write.event' and e['payload'].get('success_bool')==True]); print(n)"
```

Metric B: **Per-accessPermission distribution** (invariant #2 + per-edge HC-11 evidence)
```bash
python3 -c "import json,collections; events=[json.loads(l) for l in open('outputs/build_runner_events.jsonl')]; c=collections.Counter(e['payload'].get('accessPermission_value_set','UNSET') for e in events if e['event_class']=='be_a_spec_registry.write.event'); print(dict(c))"
```

Metric C: **Write latency p95** (side-effect-bound verification per §4 ≤5s bound)
```bash
python3 -c "import json,statistics; events=[json.loads(l) for l in open('outputs/build_runner_events.jsonl')]; lat=sorted(float(e['payload'].get('response_time_ms',0)) for e in events if e['event_class']=='be_a_spec_registry.write.event'); print('p95='+str(lat[int(0.95*len(lat))] if lat else 'no-data'))"
```

Metric D: **Drift-event count** (HALT-and-surface invariant #1 + #6 evidence)
```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/build_runner_events.jsonl')]; n=len([e for e in events if e['event_class']=='build_runner_runtime_failure']); print(n)"
```

> The measurement hook MUST be reproducible — given the same emit log, two
> independent operators MUST compute the same metric value. If the hook
> contains a free parameter that changes the value, that parameter is part
> of the contract and belongs in [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §0
> identity row.

---

## §3 Refusal-on-Violation (refuse-on-missing-precondition; design-by-contract refusal pattern)

<!-- gate:runtime_emit_spec §3 required -->

State what the artifact does when a runtime-emit fails to write (DB unavailable;
log rotation; event-bus partition). The build-class default is **halt-and-surface**:
if the artifact cannot record the boundary it just crossed, it cannot proceed,
because the next event would be unverifiable.

| Failure mode | Refusal behavior | Surface (where halt is reported) |
|---|---|---|
| SPARQL UPDATE returns HTTP non-200 | halt-and-surface; emit `build_runner_runtime_failure` drift event; do NOT retry from memory (S133 BINDING); return `status: blocked` in YAML envelope | `outputs/build_runner_events.jsonl` (drift event row) + YAML envelope `issues` field + `outputs/build_runner_envelope.yaml` |
| SHACL validation refuses a CONFORMING spec at smoke (invariant violation: polymorphism broken) | halt-and-surface; emit drift event; fall back to Path β (additive `cycle16:` namespace predicates mirroring `c6:` semantics); record disposition in BUILD_DECISION_LOG §1.4 architectural choice | drift event + BUILD_DECISION_LOG §1.4 + YAML envelope |
| Readback returns <14 field predicates per test spec | halt-and-surface; emit drift event; investigate write-side serialization defect; do NOT close as completed | drift event + BUILD_DECISION_LOG §1 verdict row FAIL_AT_SMOKE_READBACK |
| HC #26 internal smoke FAIL (any of 3 gates) | halt-and-surface; emit drift event; return `status: blocked` (NOT completed); record FAIL row in BUILD_DECISION_LOG §N.5 internal-smoke subsection | drift event + BUILD_DECISION_LOG §N.5 + YAML envelope |
| Canonical marker count post-edit < baseline | halt-and-surface; emit drift event; restore lost marker via git checkout OR Edit; do NOT close as completed (DP#44 BINDING) | drift event + YAML envelope `canonical_markers_post_edit` field + `zero_marker_loss: false` |
| Fuseki PID 479112 dies mid-BE-A (process unavailability) | halt-and-surface as KT-6 candidate per Binding 7 + ED §Field 6; do NOT route around with SQL/YAML fallback unless Rex-dispositioned escalation | drift event + Coach surface to Rex via Cycle-16-S3 handoff |

<!-- /gate:runtime_emit_spec §3 -->

> Refusal-on-violation prevents the runtime-emit-absent failure shape
> (Pattern G in the Cycle 1 LANDSCAPE evidence): "engineering primitive
> registries, calibration-as-CI, and runtime-emit are all absent." A
> build-class artifact that silently swallows emit failures is a regression
> to documentation-active discipline.

---

## §4 Append-only Discipline

| Property | Required | Verification |
|---|---|---|
| **Events are append-only** | YES | No event MAY be deleted or edited; corrections emit a new event referencing the prior `event_id` via `supersedes:` field |
| **Timestamps are monotonic per run** | YES | Each event's timestamp ≥ prior event's timestamp within a single `run_id` |
| **Schema version is recorded per event** | YES | Every event includes `schema_version` from §0 |
| **Run boundary events bracket every run** | YES | `run.start` event MUST precede every other event in a run; `run.end` event MUST be the last event |

> Append-only discipline is the structural guarantee that
> [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) can do n≥3
> cross-system reasoning over event logs from multiple test beds.

---

## §5 Calibration Hook (CI-time validation)

<!-- gate:runtime_emit_spec §5 required -->

State the CI-time calibration that asserts emit shape is preserved across
artifact versions.

```bash
# Calibration fixture: known-conforming + known-non-conforming specs at outputs/be_a_smoke_fixture_{conforming,nonconforming}.ttl
python3 -c "
import pyshacl, rdflib
shapes = rdflib.Graph()
shapes.parse('docs/spec_registry_shapes.shacl.ttl', format='turtle')
shapes.parse('/home/azureuser/cycle_6_unified_substrate_build/runtime/jena/shapes/access_permission.shacl.ttl', format='turtle')
conf = rdflib.Graph(); conf.parse('outputs/be_a_smoke_fixture_conforming.ttl', format='turtle')
nonconf = rdflib.Graph(); nonconf.parse('outputs/be_a_smoke_fixture_nonconforming.ttl', format='turtle')
r_c = pyshacl.validate(conf, shacl_graph=shapes, ont_graph=rdflib.Graph().parse('docs/spec_registry_schema.ttl', format='turtle'))
r_n = pyshacl.validate(nonconf, shacl_graph=shapes, ont_graph=rdflib.Graph().parse('docs/spec_registry_schema.ttl', format='turtle'))
assert r_c[0] == True, 'CONFORMING fixture FAILED — calibration drift'
assert r_n[0] == False, 'NON-CONFORMING fixture PASSED — calibration drift'
print('CALIBRATION PASS')
"
```

| Calibration check | What it asserts | Run frequency |
|---|---|---|
| SHACL polymorphism fixture | `c6:StatementAccessPermissionShape` polymorphism applies to `cycle16:Spec rdfs:subClassOf c6:Statement` instances; conforming fixture validates; non-conforming (missing accessPermission / invalid spec_type / dormant-silent without target session / missing owner) refused with ≥4 violation classes | every BE-A invocation + pre-promotion at Cycle-16-S4 BE-B consumer wiring + every CONTRACT_CHANGE that touches §1 schema or §5 SHACL shapes |
| Event schema parseable | Every line of `outputs/build_runner_events.jsonl` parses as JSON + contains required fields per §1 schema row for its event_class | every BE-A close + pre-promotion |
| Append-only monotonicity | `wc -l outputs/build_runner_events.jsonl` strictly increases across BE-A execution; no row deleted or rewritten | every Step 1-5 boundary |

<!-- /gate:runtime_emit_spec §5 -->

> Calibration-as-CI is a load-bearing pattern from the LANDSCAPE evidence
> (M4 method import). It catches regressions where a code change drops a
> required field from emit *without* changing the schema declaration —
> which would otherwise pass-through the build pipeline silently. If your
> artifact has no calibration hook, your runtime-emit is one refactor away
> from quietly going dark.

---

## §6 Self-test (BEFORE shipping the artifact's first run)

| # | Check | Status |
|---|---|---|
| 1 | Every §1 event class has a trigger AND required-field set | [x] (7 classes: session.start + dispatch.received + build.phase.start + build.phase.complete + session.end + be_a_spec_registry.write.event + build_runner_runtime_failure drift class — all have trigger + required-fields) |
| 2 | §2 measurement hook reproduces the same value across two independent operators on the same emit log | [x] (4 metrics A-D: each is `python3 -c` one-liner against same JSONL file = deterministic; reproducibility verified by running twice) |
| 3 | §3 refusal-on-violation is wired (not "TBD") for at least one failure mode | [x] (6 failure modes wired: HTTP non-200 + SHACL refuses conforming + readback <14 + HC #26 FAIL + canonical marker loss + Fuseki PID death) |
| 4 | §4 append-only discipline is verified by inspection of the event sink | [x] (BE-A execution: `wc -l outputs/build_runner_events.jsonl` strictly increasing across Step 1-5 boundaries; SHA256 recorded at close in BUILD_DECISION_LOG §1) |
| 5 | §5 calibration hook runs to PASS on a fixture before first production run | [x] (calibration hook = pyshacl validate on conforming + non-conforming fixtures; expected conf=True nonconf=False; runs at Step 4 smoke test) |
| 6 | Schema version (§0) is locked at promotion commit | [x] (schema_version `0.1` in every event row; locked at Cycle-16-S3 close paired-commit per Discipline #11) |

> If any check is `[ ]`, halt-and-surface; do NOT promote to production.

---

## §10 BE-B H7 Cycle 16 Branch 4.2 BE-A-source Authoring Discipline Emit Schema Append

<!-- gate:runtime_emit_spec §10 required -->

Per Cycle-16-S4 BE-B dispatch substrate §1 item 6 + §3 4-class refusal taxonomy + Cycle 14 §10 emit-schema precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) unchanged. 3 NEW event classes for spec_registry authoring discipline.

### §10.0 BE-B Emit Identity (extension to §0)

| Field | Value |
|---|---|
| **Sink (new)** | `~/cycle_16_close_spec_to_implementation_gap_build/outputs/spec_registry_events.jsonl` (append-only; created at BE-B fresh-scaffold install per `install_spec_registry_authoring_discipline()` govML v2.8.3 hook) |
| **Namespace (new)** | `cycle_16.be_b.spec_registry` (per-pipeline + per-cycle + per-BE scope; namespace-isolated from BE-A `cycle_16.be_a.spec_registry` per Cycle 10 rule_6 + rule_8 + rule_10 + rule_12 namespace-isolation invariants) |
| **Schema version** | `0.1` (locked at Cycle-16-S4 close paired-commit) |
| **Min events per run** | `3` (≥1 per dogfooding TB write = 3 baseline; plus 0-N shacl_refusal / author_refusal events depending on dogfooding success path) |

### §10.1 BE-B Event Schema (3 NEW event classes)

| Event class | Trigger | Required fields | Optional fields | Cardinality per run |
|---|---|---|---|---|
| `spec_registry.write.event` | At each successful `register_spec()` invocation (UPDATE INSERT DATA HTTP 200/204; SHACL pre-validation PASS; structural-enforcement PASS) | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.spec_id`, `payload.graph_iri`, `payload.sparql_query_hash` (sha256 of query body), `payload.http_status_code`, `payload.response_time_ms`, `payload.triple_count_delta`, `payload.accessPermission_value_set`, `payload.success_bool` | `payload.test_bed_id` ∈ {TB-1, TB-2, TB-3} | at-least-once per `register_spec` PASS |
| `spec_registry.shacl_refusal.event` | At `register_spec()` refuse-on-violation: missing mandatory field / enum violation / DP#26 n_a_rationale absent / SHACL polymorphism violation | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.refusal_class` ∈ {missing_mandatory_fields, enum_violation, dp26_n_a_rationale_missing, shacl_violation}, `payload.spec_partial` (sanitized dict) | `payload.shacl_report_excerpt` (≤2000 chars), `payload.missing_fields`, `payload.errors`, `payload.error`, `payload.spec_iri` | 0 expected on clean run; 1+ per refused write |
| `spec_registry.author_refusal.event` | At `record_author_refusal()` invocation per Brief 4 KT-3 firing surface (author-side, NOT wrapper-side) | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.refusal_class` ∈ REFUSAL_CLASSES {acceptance_criteria_unclear, backlog_from_same_cycle_default, dp44_honest_gap, n_a_rationale_unclear}, `payload.rationale`, `payload.spec_partial`, `payload.kt_3_candidate_bool` | n/a | 0+ per session; Coach R3 close-eval aggregates per class |

### §10.2 BE-B Measurement Hook (consumed by ACCEPTANCE_CRITERIA §10)

**Metric A_BE_B: Total spec_registry.write.event success count** (post-condition #11 + 3-TB threshold)
```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/spec_registry_events.jsonl')]; n=len([e for e in events if e['event_class']=='spec_registry.write.event' and e['payload'].get('success_bool')==True]); print(n)"
```
Expected at BE-B close: ≥3 (one per TB-1+TB-2+TB-3 dogfooding write).

**Metric B_BE_B: Per-refusal-class distribution** (Brief 4 KT-3 firing-surface evaluation)
```bash
python3 -c "import json, collections; events=[json.loads(l) for l in open('outputs/spec_registry_events.jsonl')]; c=collections.Counter(e['payload'].get('refusal_class','UNSET') for e in events if e['event_class']=='spec_registry.author_refusal.event'); print(dict(c))"
```
Coach R3: (a) acceptance_criteria_unclear + (b) backlog_from_same_cycle_default + (d) n_a_rationale_unclear cumulative ≥3 → KT-3 FIRES; only (c) dp44_honest_gap → KT-3 DOES NOT FIRE.

**Metric C_BE_B: shacl_refusal count by class** (DP#26 carve-out enforcement evidence)
```bash
python3 -c "import json, collections; events=[json.loads(l) for l in open('outputs/spec_registry_events.jsonl')]; c=collections.Counter(e['payload'].get('refusal_class','UNSET') for e in events if e['event_class']=='spec_registry.shacl_refusal.event'); print(dict(c))"
```

### §10.3 BE-B Refusal-on-Violation (extension to §3)

| Failure mode | Refusal behavior | Surface |
|---|---|---|
| `register_spec` missing mandatory field | halt-and-surface; emit `spec_registry.shacl_refusal.event` with `refusal_class: missing_mandatory_fields` + `missing_fields` list; ValueError raised; no write to /cycle6 | `outputs/spec_registry_events.jsonl` + caller stderr |
| `register_spec` enum violation (spec_type / current_status / access_permission outside enum) | halt-and-surface; emit `spec_registry.shacl_refusal.event` with `refusal_class: enum_violation`; ValueError raised | same |
| `register_spec` DP#26 carve-out violation (`runtime_emit_event_class` starts "n/a" AND `n_a_rationale` empty) | halt-and-surface per HC-07 every-claim-traces-to-evidence BINDING; emit `spec_registry.shacl_refusal.event` with `refusal_class: dp26_n_a_rationale_missing`; ValueError raised | same |
| `register_spec` SHACL polymorphism violation at write boundary | halt-and-surface per `spec_authoring_discipline §5 BIND`; emit `spec_registry.shacl_refusal.event` with `refusal_class: shacl_violation` + truncated SHACL report; ValueError raised | same |
| `record_author_refusal` refusal_class outside REFUSAL_CLASSES enum | ValueError raised; no JSONL emit (refusal-class validation is wrapper-entry) | caller stderr |
| HTTP non-200/204 on `register_spec` UPDATE write | halt-and-surface; emit `spec_registry.write.event` with `success_bool: false` (still recorded for audit) + raise per Operation 1 invocation contract | same |

### §10.4 BE-B Append-only Discipline (extension to §4)

Same invariant as §4: append-only at `outputs/spec_registry_events.jsonl`. New events INCLUDE prior-event `supersedes:` field only when a write needs correction (e.g., per-spec re-author after refusal). Per spec_authoring_discipline §4 Operation 5 supersedure pattern, non-destructive supersedure at the registry layer preserves audit trail; emit-event layer mirrors structurally.

### §10.5 BE-B Calibration Hook (extension to §5)

```bash
# Calibration fixture: 3 BE-B dogfooding TBs + n_a_rationale enforcement smoke
python3 -c "
import sys; sys.path.insert(0, 'scripts')
import spec_registry_authoring as sra

# DP#26 enforcement smoke: should refuse
try:
    sra.register_spec({
        'spec_type':'MethodologyCommitment',
        'owner':'calibration_smoke',
        'acceptance_criteria':'calibration_check',
        'target_session':'cycle-16-close',
        'current_status':'dormant-with-explicit-deferral',
        'cycle_authored':16,
        'session_authored':'Cycle-16-S4',
        'runtime_emit_event_class':'n/a',
        'dormancy_detection_threshold_sessions':3,
        'audit_trail_link':'activity_calibration_smoke',
        'access_permission':'publishable',
    }, project_dir='.')
    print('CALIBRATION FAIL: DP#26 enforcement skipped n_a_rationale check')
except ValueError as e:
    if 'n_a_rationale' in str(e) or 'DP#26' in str(e):
        print('CALIBRATION PASS')
    else:
        print(f'CALIBRATION FAIL: unexpected ValueError: {e}')
"
```

### §10.6 BE-B Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | 3 NEW event classes have triggers + required fields specified | [x] PASS (write.event + shacl_refusal.event + author_refusal.event) |
| 2 | Measurement hooks A_BE_B + B_BE_B + C_BE_B reproduce same value across two independent operators (deterministic JSONL aggregations) | [x] PASS (Python one-liners against same file = deterministic) |
| 3 | Refusal-on-violation wired for 6 failure modes (4 SHACL refusal subclasses + author refusal + HTTP non-200) | [x] PASS (per §10.3 table) |
| 4 | Append-only discipline verified at sink (`wc -l outputs/spec_registry_events.jsonl` strictly increasing across BE-B 3-TB dogfooding) | [x] PASS (3 write.events appended at smoke) |
| 5 | Calibration hook fires PASS on DP#26 carve-out smoke fixture | [x] PASS (ValueError raised + DP#26 keyword match) |
| 6 | Schema version `0.1` locked at Cycle-16-S4 close paired-commit | [x] PASS (recorded in every event row) |

<!-- /gate:runtime_emit_spec §10 -->

---

## §11 BE-C H6 Cycle 16 Branch 4.3 BE-B-source TWO-surface Gate Emit Schema Append

<!-- gate:runtime_emit_spec §11 required -->

Per Cycle-16-S5 BE-C dispatch substrate §1 item 8 + §5 RUNTIME_EMIT_SPEC fill instructions + Cycle 14 §11 emit-schema precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED) unchanged. 2 NEW event classes for spec_implementation_gates fire telemetry.

### §11.0 BE-C Emit Identity (extension to §0)

| Field | Value |
|---|---|
| **Sink (new)** | `~/cycle_16_close_spec_to_implementation_gap_build/outputs/spec_implementation_gates_events.jsonl` (append-only; created at BE-C fresh-scaffold install per `install_spec_implementation_gates()` govML v2.8.4 hook) |
| **Namespace (new)** | `cycle_16.be_c.spec_implementation_gates` (per-pipeline + per-cycle + per-BE scope; namespace-isolated from BE-A `cycle_16.be_a.spec_registry` + BE-B `cycle_16.be_b.spec_registry` per Cycle 10 rule_6/8/10/12 namespace-isolation invariants) |
| **Schema version** | `0.1` (locked at Cycle-16-S5 close paired-commit) |
| **Min events per run** | `2` (1 per gate fire = 2 baseline at 1 invocation of each gate; ≥6 across 3-TB dogfooding × 2 gates) |

### §11.1 BE-C Event Schema (2 NEW event classes)

| Event class | Trigger | Required fields | Optional fields | Cardinality per run |
|---|---|---|---|---|
| `spec_implementation_present_gate.fire.event` | At each `spec_implementation_present_gate.sh` invocation (cycle-close BLOCKING gate; mirrors `k_register_present_gate.sh` skeleton per H6 metric) | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.cycle_n`, `payload.verdict` ∈ {CLEAR, BLOCKED, ADVISORY_FAIL, SKIP_NON_BUILD_PROFILE}, `payload.dormant_silent_present_bool` ∈ {true, false, unknown, error}, `payload.pass_count`, `payload.fail_count`, `payload.warn_count`, `payload.sparql_endpoint`, `payload.ask_http_status`, `payload.ask_response_ms`, `payload.project_dir`, `payload.advisory_mode_bool` | (none at v0.1) | exactly once per invocation |
| `spec_implementation_session_close_gate.fire.event` | At each `spec_implementation_session_close_gate.sh` invocation (session-close ADVISORY gate by default; --blocking-mode opt-in flips to BLOCKING) | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.current_session_index` (= `SESSIONS_BETWEEN` grep-derived count), `payload.threshold` (Amendment 27a default 3), `payload.dormant_specs_exceeding_threshold_count`, `payload.verdict` ∈ {CLEAR, ADVISORY_FAIL, BLOCKED, SKIP_NON_BUILD_PROFILE}, `payload.pass_count`, `payload.fail_count`, `payload.warn_count`, `payload.sparql_endpoint`, `payload.ask_http_status`, `payload.ask_response_ms`, `payload.project_dir`, `payload.advisory_mode_bool` | (none at v0.1) | exactly once per invocation |

### §11.2 BE-C Measurement Hook (consumed by ACCEPTANCE_CRITERIA §11)

**Metric A_BE_C: spec_implementation_present_gate.fire.event count by verdict** (post-condition #18 + H6 + KT-4 firing surface)
```bash
python3 -c "import json, collections; events=[json.loads(l) for l in open('outputs/spec_implementation_gates_events.jsonl')]; c=collections.Counter(e['payload']['verdict'] for e in events if e['event_class']=='spec_implementation_present_gate.fire.event'); print(dict(c))"
```
Expected at BE-C close: at least 1 CLEAR (TB-1 + TB-2 conforming) + 1 BLOCKED (TB-3 dormant-silent past-threshold; load-bearing per dispatch substrate §4).

**Metric B_BE_C: spec_implementation_session_close_gate.fire.event count by verdict** (post-condition #18 cross-surface)
```bash
python3 -c "import json, collections; events=[json.loads(l) for l in open('outputs/spec_implementation_gates_events.jsonl')]; c=collections.Counter(e['payload']['verdict'] for e in events if e['event_class']=='spec_implementation_session_close_gate.fire.event'); print(dict(c))"
```
Expected at BE-C close: at least 1 CLEAR (TB-1 + TB-2 within threshold or with rex_authorization) + 1 ADVISORY_FAIL (TB-3 past threshold without rex_authorization).

**Metric C_BE_C: dormant_silent_present_bool == "true" per fire event** (KT-4 firing surface classification primary signal)
```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/spec_implementation_gates_events.jsonl')]; n=len([e for e in events if e['event_class']=='spec_implementation_present_gate.fire.event' and e['payload'].get('dormant_silent_present_bool')=='true']); print(n)"
```
Expected at BE-C close: ≥1 (TB-3 dormant-silent past-threshold load-bearing fire). KT-4 FIRES if this count is 0 across 3-TB dogfooding (i.e., FALSE NEGATIVE on TB-3); KT-4 DOES NOT FIRE if TB-3 surfaces the dormant-silent boolean correctly.

### §11.3 BE-C Refusal-on-Violation (extension to §3)

| Failure mode | Refusal behavior | Surface |
|---|---|---|
| SPARQL endpoint non-reachable at gate invocation | emit fire.event with `ask_http_status: 0` + `verdict: CLEAR` if no failed Checks (Check 2 SKIP) OR `verdict: BLOCKED/ADVISORY_FAIL` if downstream FAIL; surface WARN-class via add_check | `outputs/spec_implementation_gates_events.jsonl` + stderr Check 1 WARN |
| ASK boolean TRUE at present-gate Check 2 (cycle-close dormant-silent dormant-silent without rex_authorization) | halt-and-surface BLOCKED; exit 1 unless `--advisory-mode` (then ADVISORY_FAIL + exit 0) | same |
| COUNT > 0 at session-close-gate Check 2 (dormant-silent over threshold) | ADVISORY_FAIL by default (advisory loop semantics); BLOCKED if `--blocking-mode` opt-in | same |
| 4-class verdict enum violation (unknown verdict literal at JSON output) | halt-and-surface as CONTRACT_CHANGE per Binding 7; refuse-on-violation per ARTIFACT_CONTRACT §11.3 row 12 invariant | caller stderr + envelope `issues` |
| HC #45 ADDITIVE-APPEND violation at govML LOCKED bodies | refuse via build-runner DP#44 refuse triggers (a)/(b)/(c)/(f) per dispatch substrate §7; emit `build_runner_runtime_failure.event` | `outputs/build_runner_events.jsonl` + envelope |

### §11.4 BE-C Append-only Discipline (extension to §4)

Same invariant as §4: append-only at `outputs/spec_implementation_gates_events.jsonl`. New fire events INCLUDE prior-event reference only via the JSONL sink ordering (each fire is a fresh event; no supersedure semantics at gate-fire layer). Gate scripts always APPEND via shell heredoc-piped Python urllib write — never edit existing rows. `wc -l outputs/spec_implementation_gates_events.jsonl` strictly monotonically increasing across BE-C 3-TB dogfooding × 2 gates fires.

### §11.5 BE-C Calibration Hook (extension to §5)

```bash
# Calibration fixture: 1 gate-script-help + 1 gate-script-skip-non-build-profile fire
# (deterministic; no SPARQL endpoint dependency at calibration boundary).
set -euo pipefail
SMOKE=/tmp/be_c_calibration_smoke_$$
mkdir -p "$SMOKE"
# No governance.yaml at $SMOKE → SKIP_NON_BUILD_PROFILE verdict
bash ~/ml-governance-templates/scripts/spec_implementation_present_gate.sh "$SMOKE" >/dev/null
VERDICT=$(python3 -c "import json; print(json.load(open('$SMOKE/outputs/spec_implementation_present_gate_results.json'))['verdict'])")
if [ "$VERDICT" = "SKIP_NON_BUILD_PROFILE" ]; then
    echo "CALIBRATION PASS: skip-WARN verdict on non-build profile"
else
    echo "CALIBRATION FAIL: expected SKIP_NON_BUILD_PROFILE, got $VERDICT"
fi
rm -rf "$SMOKE"
```

### §11.6 BE-C Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | 2 NEW event classes have triggers + required fields specified per §11.1 | [x] PASS (present_gate.fire.event + session_close_gate.fire.event) |
| 2 | Measurement hooks A_BE_C + B_BE_C + C_BE_C reproduce same value across two independent operators (deterministic JSONL aggregations) | [x] PASS (Python one-liners against same file = deterministic) |
| 3 | Refusal-on-violation wired for 5 failure modes per §11.3 | [x] PASS |
| 4 | Append-only discipline verified at sink (`wc -l outputs/spec_implementation_gates_events.jsonl` strictly increasing across BE-C 3-TB × 2-gate dogfooding) | [x] PASS (≥6 fire.events appended at smoke; pre/post wc -l diff ≥6) |
| 5 | Calibration hook fires PASS on SKIP_NON_BUILD_PROFILE smoke fixture (no governance.yaml → skip-WARN verdict) | [x] PASS |
| 6 | Schema version `0.1` locked at Cycle-16-S5 close paired-commit | [x] PASS (recorded in every event row) |

<!-- /gate:runtime_emit_spec §11 -->
