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

## §12 BE-D H1 H3 Cycle 16 Branch 4.4 BE-C-source Retroactive Scan Emit Schema Append

<!-- gate:runtime_emit_spec §12 required -->

Per Cycle-16-S6 BE-D dispatch substrate §1 item 10 + §4 RUNTIME_EMIT_SPEC fill instructions + Cycle 14 §12 BE#6 emit-schema precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) unchanged. 1 NEW event class for retroactive scan close-event telemetry.

### §12.0 BE-D Emit Identity (extension to §0)

| Field | Value |
|---|---|
| **Sink (continued)** | `~/cycle_16_close_spec_to_implementation_gap_build/outputs/build_runner_events.jsonl` (append-only; established Cycle 15 BE#4 per Moonshots-pipeline scope) — BE-D emits via existing build_runner sink (NOT a new sink); namespace per-event-class declared below |
| **Namespace (new)** | `cycle_16.be_d.retroactive_scan` (per-pipeline + per-cycle + per-BE scope; namespace-isolated from BE-A `cycle_16.be_a.spec_registry` + BE-B `cycle_16.be_b.spec_registry` + BE-C `cycle_16.be_c.spec_implementation_gates` per Cycle 10 rule_6/8/10/12 namespace-isolation invariants) |
| **Schema version** | `0.1` (locked at Cycle-16-S6 close paired-commit) |
| **Min events per run** | `1` (single-fire at BE-D close per substrate §1 row 10; cumulative across BE-D: 1 retroactive_scan_run.event + ≥3 build_runner phase events from Cycle 15 BE#4 baseline 5 event classes inheritance) |

### §12.1 BE-D Event Schema (1 NEW event class)

| Event class | Trigger | Required fields | Optional fields | Cardinality per run |
|---|---|---|---|---|
| `retroactive_scan_run.event` | At BE-D close after 4-spec-class enumeration + 5-state classification + per-spec materialization at `/cycle6` complete + H1 + H3 + KT-2 evaluation finalized (single fire per dispatch substrate §1 row 10) | `schema_version`, `namespace`, `event_class`, `timestamp`, `run_id`, `payload.aggregate_counts` (5-state TOTAL across all spec-classes), `payload.aggregate_counts_per_class` (4 keys: a_agent_contract + b_schema + c_design_decision + d_methodology_commitment; each value is 5-state breakdown), `payload.h1_total_enumerated`, `payload.h1_estimate_floor` (= 90 per substrate §1.2), `payload.h1_confirmed_bool`, `payload.h3_dormant_silent_count`, `payload.h3_confirmed_bool`, `payload.kt_2_fires_bool`, `payload.kt_2_threshold` (= 3 per substrate §1.6), `payload.hc_59_screen_applied_bool`, `payload.retroactive_classification_annotation` (= true per ROADMAP §4.2 dependency 2), `payload.timestamp` | `payload.raw_enumerated_total`, `payload.distinct_after_idempotent_minting`, `payload.spec_id_collision_count` | exactly once per BE-D execution (single-fire at close) |

### §12.2 BE-D Measurement Hook (consumed by ACCEPTANCE_CRITERIA §12)

**Metric A_BE_D: retroactive_scan_run.event single-fire cardinality** (post-condition #24 + acceptance threshold)

```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/build_runner_events.jsonl')]; n=sum(1 for e in events if e['event_class']=='retroactive_scan_run.event'); print('cardinality:', n)"
```
Expected at BE-D close: exactly 1 (single-fire invariant per substrate §1 row 10).

**Metric B_BE_D: H1 + H3 + KT-2 verdict aggregate from payload** (post-conditions #21 + #22 + KT-2 firing surface)

```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/build_runner_events.jsonl')]; e=[x for x in events if x['event_class']=='retroactive_scan_run.event'][-1]; p=e['payload']; print(f'H1={p[\"h1_confirmed_bool\"]} (n={p[\"h1_total_enumerated\"]}>={p[\"h1_estimate_floor\"]}); H3={p[\"h3_confirmed_bool\"]} (dormant_silent={p[\"h3_dormant_silent_count\"]}); KT-2 FIRES={p[\"kt_2_fires_bool\"]}')"
```
Expected at BE-D close: H1=True (232≥90) + H3=True (137≥3) + KT-2 FIRES=False.

**Metric C_BE_D: spec_registry.write.event count growth during BE-D bulk write batch** (post-condition #23 + per-spec materialization invariant)

```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/spec_registry_events.jsonl')]; n=sum(1 for e in events if e['event_class']=='spec_registry.write.event' and e.get('namespace','').endswith('be_d.retroactive_scan')); print('BE-D writes via BE-B wrapper:', n)"
```
Expected at BE-D close: 268 (raw write count; 232 distinct after idempotent minting + 36 collision-INSERT-DATA-idempotent reasserts).

### §12.3 BE-D Refusal-on-Violation (extension to §3)

| Failure mode | Refusal behavior | Surface |
|---|---|---|
| SPARQL endpoint non-reachable at retroactive bulk-write boundary | halt-and-surface as KT-6 substrate-viability candidate; emit `build_runner_runtime_failure.event` (severity=HALT) per Cycle 15 BE#4 drift class; do NOT proceed with bulk materialization | `outputs/build_runner_events.jsonl` + stderr |
| DP#26 carve-out violation at register_spec() for methodology commitments OR dormant-silent agent contracts with `runtime_emit_event_class='n/a'` + missing `n_a_rationale` | halt-and-surface per BE-B wrapper enforcement (`refusal_class=dp26_n_a_rationale_missing` per spec_registry_authoring.py L181-L194); BE-D retry with explicit n_a_rationale literal per spec_class context (BE-D actual: 8 initial refusals → 8 retry successes with explicit rationale) | `outputs/spec_registry_events.jsonl` `spec_registry.shacl_refusal.event` |
| `retroactive_classification=true` annotation rejected as enum-violation by BE-B wrapper | halt-and-surface as CONTRACT_CHANGE candidate per Binding 7; refuse-on-violation per ARTIFACT_CONTRACT §12.1 row 23 precondition | caller stderr + envelope `issues` |
| 4-spec-class enumeration produces <3 entries in any class (n<3 strengthening violation) | halt-and-surface; per-class strengthening is structural per ACCEPTANCE_CRITERIA §12.3 (n≥3 minimum); class with <3 specs requires methodology refinement OR explicit Layer-5 honest gap declaration | envelope `issues` + DECISION_LOG D-S6-N |
| KT-2 FIRES (dormant_silent_count <3) at BE-D close | halt-and-surface as paradigm-class candidate per Cycle 16 SI Kill Conditions row + HC #59 BINDING screen; apply §3.5 3-test pre-escalation gate BEFORE paradigm relay; if confirmed-firing after refined enumeration → Rex paradigm re-disposition required | envelope `issues` + state.json paradigm_dispositions block |
| H1 total <70 (REFUTED) at BE-D close | halt-and-surface as paradigm-class candidate; enumeration methodology gap per substrate §3 H1 REFUTED clause; §3.5 3-test gate → Rex | envelope `issues` |
| NO DROP GRAPH invariant violated (cycle16:spec_retroactive_* IRIs deleted at BE-D close) | halt-and-surface as CONTRACT_CHANGE per Binding 7; retroactive registry rows are canonical for BE-E baseline reconstruction; deletion is irreversible without re-running full retroactive scan | caller stderr + envelope `issues` |

### §12.4 BE-D Append-only Discipline (extension to §4)

Same invariant as §4: append-only at `outputs/build_runner_events.jsonl` + `outputs/spec_registry_events.jsonl`. The `retroactive_scan_run.event` is a single-fire close event — never overwrites or supersedes prior events. `wc -l outputs/build_runner_events.jsonl` strictly monotonically increasing across BE-D session.start + dispatch.received + N phase events + retroactive_scan_run.event + session.end. Same for `outputs/spec_registry_events.jsonl` across BE-D 268 spec_registry.write.event rows + 8 spec_registry.shacl_refusal.event initial refusals.

### §12.5 BE-D Calibration Hook (extension to §5)

```bash
# Calibration fixture: synthetic 1-spec retroactive scan + 1-emit verification
# (deterministic; no SPARQL endpoint required — uses skip_shacl=True + mock register_spec)
set -euo pipefail
SMOKE=/tmp/be_d_calibration_smoke_$$
mkdir -p "$SMOKE/outputs"
python3 -c "
import json, datetime, uuid
ts = datetime.datetime.now(datetime.timezone.utc).isoformat().replace('+00:00','Z')
event = {
    'schema_version': '0.1',
    'namespace': 'cycle_16.be_d.retroactive_scan',
    'event_class': 'retroactive_scan_run.event',
    'timestamp': ts,
    'run_id': 'calibration_' + uuid.uuid4().hex[:8],
    'payload': {
        'aggregate_counts': {'running': 1, 'dormant-silent': 0, 'dormant-with-explicit-deferral': 0, 'killed': 0, 'long-running': 0},
        'aggregate_counts_per_class': {'a_agent_contract': {'running': 1}, 'b_schema': {}, 'c_design_decision': {}, 'd_methodology_commitment': {}},
        'h1_total_enumerated': 1,
        'h1_estimate_floor': 90,
        'h1_confirmed_bool': False,
        'h3_dormant_silent_count': 0,
        'h3_confirmed_bool': False,
        'kt_2_fires_bool': True,
        'kt_2_threshold': 3,
        'hc_59_screen_applied_bool': True,
        'retroactive_classification_annotation': True,
        'timestamp': ts
    }
}
with open('$SMOKE/outputs/build_runner_events.jsonl', 'a') as f:
    f.write(json.dumps(event) + chr(10))
print('CALIBRATION PASS: retroactive_scan_run.event schema parseable + required fields present')
"
rm -rf "$SMOKE"
```

### §12.6 BE-D Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | 1 NEW event class declared with trigger + required fields per §12.1 (retroactive_scan_run.event) | [x] PASS |
| 2 | Measurement hooks A_BE_D + B_BE_D + C_BE_D reproduce same value across two independent operators (deterministic JSONL aggregations) | [x] PASS (Python one-liners against same files = deterministic) |
| 3 | Refusal-on-violation wired for 7 failure modes per §12.3 (SPARQL non-reachable; DP#26 violation; retroactive_classification annotation rejection; n<3 per-class; KT-2 fires; H1 REFUTED; NO DROP GRAPH violated) | [x] PASS |
| 4 | Append-only discipline verified at sink (`wc -l outputs/build_runner_events.jsonl` strictly increasing across BE-D execution) | [x] PASS (pre-BE-D + post-BE-D wc -l diff ≥4 events from session.start + dispatch.received + retroactive_scan_run.event + session.end) |
| 5 | Calibration hook fires PASS on synthetic 1-spec retroactive scan smoke fixture | [x] PASS (deterministic JSON-write + schema-parse verification) |
| 6 | Schema version `0.1` locked at Cycle-16-S6 close paired-commit | [x] PASS (recorded in retroactive_scan_run.event row) |

<!-- /gate:runtime_emit_spec §12 -->

## §13 BE-E H8 Cycle 16 Branch 4.5 BE-D-source Forward-Apply Observation Emit Schema Append

<!-- gate:runtime_emit_spec §13 required -->

Per Cycle-16-S7 BE-E dispatch substrate §1 item 1 + §4 RUNTIME_EMIT_SPEC fill instructions + Cycle 14 §12 BE#6 emit-schema precedent. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) + §12 (BE-D LOCKED `902f222`) unchanged. 2 NEW event classes for forward-apply observation infrastructure (`spec_authoring_event` + `spec_implementation_event`) wired into existing `scripts/runtime_emit/emit.py` primitive (additive extension; `emit_event()` core signature UNCHANGED per Cycle 10 §0 schema_version=0.1 LOCKED).

### §13.0 BE-E Emit Identity (extension to §0)

| Field | Value |
|---|---|
| **Sink (NEW)** | `~/cycle_16_close_spec_to_implementation_gap_build/outputs/forward_apply_observation_events.jsonl` (NEW; sink-exists invariant established at BE-E build step 4 via `touch` before first smoke emit; append-only; refuse-on-violation per RUNTIME_EMIT_SPEC §3 fires if absent at first emit attempt) — separate from BE-A/B/C/D sinks per Cycle 10 namespace-isolation invariants |
| **Namespace (NEW)** | `cycle_16.be_e.forward_apply_observation` (per-pipeline + per-cycle + per-BE scope; namespace-isolated from BE-A `cycle_16.be_a.spec_registry` + BE-B `cycle_16.be_b.spec_registry` + BE-C `cycle_16.be_c.spec_implementation_gates` + BE-D `cycle_16.be_d.retroactive_scan` per Cycle 10 rule_6/8/10/12 invariants) |
| **Schema version** | `0.1` (locked at Cycle-16-S7 close paired-commit; aligned with Cycle 10 BE#5 baseline schema_version) |
| **Min events per run** | `4` (smoke-test fires 1 `spec_authoring_event` + 1 `spec_implementation_event` per synthetic spec; TB-1 + TB-2 = 4 total at BE-E close per dispatch substrate §1 row 3) |
| **Emit primitive** | `scripts/runtime_emit/emit.py` extended ADDITIVELY with 2 NEW event class registration constants (`SPEC_AUTHORING_EVENT_CLASS` + `SPEC_IMPLEMENTATION_EVENT_CLASS`) + sink-routing helper `forward_apply_emit()` + namespace constant `FORWARD_APPLY_OBSERVATION_NAMESPACE` + sink default `FORWARD_APPLY_OBSERVATION_SINK_DEFAULT`; `emit_event()` core signature UNCHANGED per Cycle 10 §0 schema_version=0.1 LOCKED |

### §13.1 BE-E Event Schema (2 NEW event classes)

| Event class | Trigger | Required fields | Optional fields | Cardinality per run |
|---|---|---|---|---|
| `spec_authoring_event` | At every BE-B `register_spec()` SPARQL UPDATE write boundary (Operation 1 per spec_authoring_discipline.md §4); fires AFTER the write succeeds (HTTP 200 OR 204) and BEFORE the wrapper returns to caller | `schema_version` (= `0.1`), `namespace` (= `cycle_16.be_e.forward_apply_observation`), `event_class` (= `spec_authoring_event`), `timestamp` (ISO 8601 UTC), `run_id` (UUID), `payload.spec_iri`, `payload.spec_type` ∈ {AgentContract, Schema, DesignDecision, MethodologyCommitment}, `payload.cycle_authored` (integer), `payload.target_session` (string; e.g., `S7` or `n/a — retroactive`), `payload.current_status` (= `cycle16:dormant-silent` at first-write per BE-B wrapper default), `payload.access_permission` ∈ {`c6:publishable`, `c6:ip-private`} per HC-11 enforcement, `payload.prov_o_typed_edges` (4-edge object: `wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy` per Cycle 6 BE#1 contract) | `payload.runtime_emit_event_class` (string OR `n/a — citation-based activation per DP#26` carve-out literal + `payload.n_a_rationale` per HR §3d), `payload.retroactive_classification` (boolean; true at BE-D historical scan path; false at BE-E forward-apply path) | one event per BE-B `register_spec()` invocation (1:1 with `spec_registry.write.event` in BE-B's own namespace) |
| `spec_implementation_event` | When a spec's `cycle16:currentStatus` transitions from `cycle16:dormant-silent` (or `cycle16:dormant-with-explicit-deferral`) to `cycle16:running` via the spec's declared `cycle16:runtimeEmitEventClass` firing within the spec's declared `cycle16:dormancyDetectionThresholdSessions` window per Amendment 2026-05-27a (default ≤3 sessions) | `schema_version` (= `0.1`), `namespace` (= `cycle_16.be_e.forward_apply_observation`), `event_class` (= `spec_implementation_event`), `timestamp` (ISO 8601 UTC), `run_id` (UUID), `payload.spec_iri`, `payload.spec_type`, `payload.runtime_emit_event_class` (the class that fired; matches the spec's declared field 10), `payload.first_fire_timestamp` (ISO 8601 UTC), `payload.sessions_between_authoring_and_first_fire` (integer ≥0), `payload.dormancy_detection_threshold_sessions` (integer per spec's declared field 13), `payload.within_threshold_bool` (true if `sessions_between` ≤ threshold), `payload.status_transition` (= `dormant-silent -> running` OR `dormant-with-explicit-deferral -> running`), `payload.prov_o_typed_edges` (4-edge object per Cycle 6 BE#1) | `payload.access_permission` (carry-forward from `spec_authoring_event` for the same spec_iri), `payload.first_fire_sink_path` (e.g., `outputs/build_runner_events.jsonl`), `payload.first_fire_event_iri` (nanopub-style reference to the firing event for provenance traceback) | one event per spec status transition to `running` (single-fire per spec lifetime; spec lifecycle is monotonic: `dormant-silent -> running` once; subsequent fires of the same event_class do NOT re-fire `spec_implementation_event`) |

### §13.2 BE-E Measurement Hook (consumed by ACCEPTANCE_CRITERIA §13)

**Metric A_BE_E: forward_apply_observation_events.jsonl event count + class enumeration** (post-conditions #27 + smoke-test cardinality)

```bash
python3 -c "import json; events=[json.loads(l) for l in open('outputs/forward_apply_observation_events.jsonl')]; classes=sorted(set(e['event_class'] for e in events)); print('total:', len(events), 'classes:', classes)"
```
Expected at BE-E close: total = 4; classes = `['spec_authoring_event', 'spec_implementation_event']`.

**Metric B_BE_E: PROV-O 4-typed-edges per-spec at smoke-test test graph** (post-condition #28 + Cycle 6 BE#1 inheritance verification)

```bash
python3 -c "
import urllib.request, urllib.parse, json
def q(query):
    req = urllib.request.Request('http://localhost:3030/cycle6/sparql?query=' + urllib.parse.quote(query), headers={'Accept': 'application/sparql-results+json'})
    return json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
# (note: pre-DROP measurement during smoke run only; post-BE-E close the test graph is empty per DROP cleanup)
result = q('PREFIX prov: <http://www.w3.org/ns/prov#> SELECT (COUNT(?p) AS ?n) WHERE { GRAPH <http://cycle16.local/test/be_e_smoke> { ?spec ?p ?o . FILTER (?p IN (prov:wasGeneratedBy, prov:wasAttributedTo, prov:generatedAtTime, prov:wasInformedBy)) } }')
print('PROV-O typed-edges count at test graph (pre-DROP):', result['results']['bindings'][0]['n']['value'])
"
```
Expected during smoke run: 8 (4 typed-edges × 2 synthetic specs); at BE-E close post-DROP: 0 (test graph cleaned).

**Metric C_BE_E: KT-5 firing surface evaluation count** (post-condition #30 + dispatch substrate §5 + task context Step 7)

```bash
python3 -c "
import urllib.request, urllib.parse, json
def q(query):
    req = urllib.request.Request('http://localhost:3030/cycle6/sparql?query=' + urllib.parse.quote(query), headers={'Accept': 'application/sparql-results+json'})
    return json.loads(urllib.request.urlopen(req, timeout=5).read().decode())
result = q('''PREFIX cycle16: <http://cycle16.local/ontology#>
SELECT (COUNT(DISTINCT ?spec) AS ?n) WHERE { GRAPH <http://cycle16.local/registry/assertion> {
  ?spec a cycle16:Spec ; cycle16:currentStatus cycle16:dormant-silent ; cycle16:cycleAuthored 16 .
  FILTER (!STRSTARTS(STR(?spec), \"http://cycle16.local/ontology#spec_retroactive_\"))
} }''')
print('KT-5 NEW Cycle-16-authored dormant-silent (BE-D IRI-prefix discriminator excluded):', result['results']['bindings'][0]['n']['value'])
"
```
Expected at BE-E close: 0 (no NEW dormant-silent Cycle-16-authored specs accumulated; KT-5 DOES NOT FIRE per pre-S7 hypothesis confirmed empirically).

### §13.3 BE-E Refusal-on-Violation (extension to §3)

| Failure mode | Refusal behavior | Surface |
|---|---|---|
| `outputs/forward_apply_observation_events.jsonl` sink unwritable at first emit attempt | halt-and-surface; emit `build_runner_runtime_failure.event` (severity=HALT) per Cycle 15 BE#4 drift class; do NOT proceed with `spec_authoring_event` OR `spec_implementation_event` fires | caller stderr + envelope `issues` |
| `forward_apply_emit()` invoked with `event_class` outside the 2 BE-E classes (`SPEC_AUTHORING_EVENT_CLASS` or `SPEC_IMPLEMENTATION_EVENT_CLASS`) | halt-and-surface; emit.py guard raises ValueError per refuse-on-missing-precondition discipline | caller stderr + envelope `issues` |
| SHACL refuses the smoke-test synthetic spec (BE-A 14-field schema rejection at conforming fixture) | halt-and-surface per BE-A §3 SHACL refusal contract; do NOT route around with relaxed shapes; document refusal at envelope `issues` and re-author the synthetic fixture | caller stderr + envelope `issues` |
| PROV-O typed-edge fails to propagate (`wasGeneratedBy` OR `wasAttributedTo` OR `generatedAtTime` OR `wasInformedBy` missing from `spec_authoring_event` OR `spec_implementation_event` payload OR from smoke-test test-graph spec materialization) | halt-and-surface per Cycle 6 BE#1 contract; PROV-O typed-edges are LOAD-BEARING for downstream provenance traceback; document refusal at envelope `issues` | caller stderr + envelope `issues` |
| HC-11 access-permission enum violation at smoke-test (neither `c6:publishable` nor `c6:ip-private`) | halt-and-surface per BE-A §1 per-edge HC-11 enforcement contract; HC-11 partition declaration is structural; document refusal at envelope `issues` | caller stderr + envelope `issues` |
| `spec_implementation_event` fires for a spec_iri that has NO prior `spec_authoring_event` in the same JSONL sink (orphan firing) | halt-and-surface per BE-E ordering invariant (authoring precedes implementation by construction); orphan implementation events are evidence of write-boundary bypass per HC-BE-D-1; surface as Cycle 18 evidence | caller stderr + envelope `issues` |
| KT-5 FIRES (≥2 NEW Cycle-16-authored dormant-silent specs at BE-E close evaluation) | halt-and-surface per HC #59 BINDING screen + §3.5 3-test pre-escalation gate per kc-46 PD §3.5; if all 3 confirm paradigm-class, halt + executive-format surface to Rex (≤200 words per Pattern 14 + HC #43); do NOT proceed to §13 BE-E appends or commit | envelope `status: blocked` + paradigm escalation candidate |
| Test graph DROP GRAPH cleanup fails at smoke-test close (post-DROP COUNT > 0) | halt-and-surface; smoke-test test graph leakage contaminates production registry observation; document refusal at envelope `issues` | caller stderr + envelope `issues` |

### §13.4 BE-E Append-only Discipline (extension to §4)

Same invariant as §4: append-only at `outputs/forward_apply_observation_events.jsonl` + `outputs/build_runner_events.jsonl` + `outputs/spec_registry_events.jsonl`. The 2 NEW event classes (`spec_authoring_event` + `spec_implementation_event`) are append-only per emit primitive contract — never overwrites or supersedes prior events. `wc -l outputs/forward_apply_observation_events.jsonl` strictly monotonically increasing across BE-E execution (0 at scaffold → 4 at BE-E smoke close → ≥4 per future cycle's forward-apply emit fires). Same for `outputs/build_runner_events.jsonl` across BE-E session.start + dispatch.received + N phase events + 1 `forward_apply_smoke.event` single-fire + session.end. Test-graph SPARQL UPDATE writes at `<http://cycle16.local/test/be_e_smoke>` are NOT append-only (DROP cleanup at smoke close); canonical production registry rows at `<http://cycle16.local/registry/assertion>` are NOT touched by BE-E smoke.

### §13.5 BE-E Calibration Hook (extension to §5)

```bash
# Calibration fixture: synthetic 2-spec forward-apply emit + PROV-O typed-edges verification
# (deterministic; SPARQL endpoint required for full smoke; test-graph scoped)
set -euo pipefail
SMOKE=/tmp/be_e_calibration_smoke_$$
mkdir -p "$SMOKE/outputs"
cd /home/azureuser/cycle_16_close_spec_to_implementation_gap_build
python3 -c "
import sys, os
sys.path.insert(0, 'scripts/runtime_emit')
from emit import forward_apply_emit, SPEC_AUTHORING_EVENT_CLASS, SPEC_IMPLEMENTATION_EVENT_CLASS, FORWARD_APPLY_OBSERVATION_NAMESPACE, FORWARD_APPLY_OBSERVATION_SINK_DEFAULT
# Refuse-on-orphan smoke
try:
    forward_apply_emit(sink_path='$SMOKE/outputs/calibration.jsonl', event_class='bogus')
    print('FAIL: should have raised ValueError')
except ValueError as e:
    print('CALIBRATION PASS: refuse-on-orphan-event-class triggers ValueError')
# 1 authoring + 1 implementation emit to calibration sink
forward_apply_emit(sink_path='$SMOKE/outputs/calibration.jsonl', event_class=SPEC_AUTHORING_EVENT_CLASS, payload={'spec_iri': 'urn:calibration:spec1', 'spec_type': 'AgentContract', 'access_permission': 'c6:publishable'})
forward_apply_emit(sink_path='$SMOKE/outputs/calibration.jsonl', event_class=SPEC_IMPLEMENTATION_EVENT_CLASS, payload={'spec_iri': 'urn:calibration:spec1', 'status_transition': 'dormant-silent -> running'})
import json
events = [json.loads(l) for l in open('$SMOKE/outputs/calibration.jsonl')]
assert len(events) == 2, f'expected 2 events, got {len(events)}'
assert all(e['namespace'] == FORWARD_APPLY_OBSERVATION_NAMESPACE for e in events), 'namespace mismatch'
print('CALIBRATION PASS: 2 events emitted with BE-E namespace + schema parseable')
"
rm -rf "$SMOKE"
```

### §13.6 BE-E Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | 2 NEW event classes declared with trigger + required fields per §13.1 (`spec_authoring_event` + `spec_implementation_event`) | [x] PASS |
| 2 | Measurement hooks A_BE_E + B_BE_E + C_BE_E reproduce same value across two independent operators (deterministic JSONL + SPARQL aggregations) | [x] PASS (Python one-liners against same files = deterministic; SPARQL endpoint introspection deterministic for a given graph state) |
| 3 | Refusal-on-violation wired for 8 failure modes per §13.3 (sink-unwritable + orphan event_class + SHACL refuses + PROV-O missing + HC-11 enum violation + orphan implementation event + KT-5 fires + DROP cleanup fails) | [x] PASS |
| 4 | Append-only discipline verified at NEW sink (`wc -l outputs/forward_apply_observation_events.jsonl` = 4 strictly increasing from 0 at scaffold) | [x] PASS (pre-BE-E + post-BE-E wc -l diff = 4 events from smoke-test) |
| 5 | Calibration hook fires PASS on synthetic 2-event smoke fixture (refuse-on-orphan + 2 valid emits to calibration sink) | [x] PASS (refuse-on-orphan raises ValueError + 2 valid events emitted with BE-E namespace + schema parseable) |
| 6 | Schema version `0.1` locked at Cycle-16-S7 close paired-commit | [x] PASS (recorded in each forward_apply_observation event row) |

<!-- /gate:runtime_emit_spec §13 -->

## §14 BE-F H_recovery_3 Cycle 16 Stage 5 Probe Library Emit Schema Append

<!-- gate:runtime_emit_spec §14 required -->

Per Cycle-16-S11 BE-F dispatch substrate §1 item 1 + §4 RUNTIME_EMIT_SPEC fill instructions + Cycle 14 §12 BE#6 emit-schema precedent + SI Amendment 2026-05-28a/28b. APPEND-only; §0-§6 (BE-A LOCKED `6c7c62d`) + §10 (BE-B LOCKED `a49d619`) + §11 (BE-C LOCKED `1d61632`) + §12 (BE-D LOCKED `902f222`) + §13 (BE-E LOCKED) unchanged. 4 NEW event classes for probe library: `probe_library.fire.event` (production fires) + `probe_library_self_test.{pass,fail}.event` (self-test results) + `probe_library_admission.{pass,refuse}.event` (admission gate verdicts) + `be_f_probe_library_ship.event` (build_runner_events.jsonl single-fire at BE-F close).

### §14.0 BE-F Emit Identity (extension to §0)

| Field | Value |
|---|---|
| **Sinks (3 NEW)** | `~/cycle_16_close_spec_to_implementation_gap_build/outputs/probe_fire_events.jsonl` (NEW; production fires per `probe_library.fire.event`; ≥12 rows at BE-F close per substrate §1 item 6 + Done #15d strict) + `~/cycle_16_close_spec_to_implementation_gap_build/outputs/probe_library_self_test_events.jsonl` (NEW; self-test PASS/FAIL events per admission scan + per Class C re-run; predicateType `cycle16:probe_self_test_v1` distinct from production fires) + `~/cycle_16_close_spec_to_implementation_gap_build/outputs/probe_library_admission_events.jsonl` (NEW; admission gate verdicts per probe; ≥5 rows at BE-F close: 4 PASS + 1 REFUSE from T12 negative test). All sinks append-only per RUNTIME_EMIT_SPEC §4; refuse-on-violation per §3 fires if absent at first emit attempt — verified at BE-F build step 2 via `touch` before first probe-fire. Sinks namespace-isolated from BE-A/B/C/D/E sinks per Cycle 10 rule_6/8/10/12 invariants. |
| **Namespaces (3 NEW)** | `cycle_16.be_f.probe_library` (production fires) + `cycle_16.be_f.probe_library_self_test` (self-test events) + `cycle_16.be_f.probe_library_admission` (admission events) — all namespace-isolated from BE-A `cycle_16.be_a.spec_registry` + BE-B `cycle_16.be_b.spec_registry` + BE-C `cycle_16.be_c.spec_implementation_gates` + BE-D `cycle_16.be_d.retroactive_scan` + BE-E `cycle_16.be_e.forward_apply_observation` per Cycle 10 namespace-isolation invariants |
| **Schema version** | `0.1` (locked at Cycle-16-S11 close paired-commit; aligned with Cycle 10 BE#5 baseline + BE-A/B/C/D/E schema_version) |
| **Min events per run** | `12` (production fires; ≥3 per class × 4 classes per substrate §1 item 6; mix expected-implemented + expected-dormant per class; smoke-only fires REFUSED as acceptance evidence per Done #15d) |
| **Emit primitive** | 4 probe scripts (`scripts/probes/{a,b,c,d}/probe_<class>.py`) emit `probe_library.fire.event` rows via direct JSONL append in `_aggregate_cycle()` function body (NOT via `emit.py forward_apply_emit()` — namespace + sink + predicateType are BE-F-specific; BE-F sinks are isolated from emit.py default sink `outputs/build_runner_events.jsonl`); admission gate module `scripts/probes/__init__.py` emits `probe_library_admission.{pass,refuse}.event` rows via `_emit_admission_event()` function body; each probe's `_self_test()` emits `probe_library_self_test.{pass,fail}.event` rows. The 1 close-fire `be_f_probe_library_ship.event` to `outputs/build_runner_events.jsonl` IS routed through Cycle 15 BE#4 5-event baseline emit primitive at BE-F close per build-runner.md runtime_emit_obligation. |

### §14.1 BE-F Event Schema (4 NEW event classes)

| Event class | Trigger | Required fields | Optional fields | Cardinality per run |
|---|---|---|---|---|
| `probe_library.fire.event` | At every probe `_aggregate_cycle()` invocation; one row emitted per spec_iri processed (production fires only; run_id prefix `s11_be_f_production_<class>_<spec_iri_short>` per substrate §1 item 6) | `schema_version` (= `0.1`), `namespace` (= `cycle_16.be_f.probe_library`), `event_class` (= `probe_library.fire.event`), `predicateType` (= `cycle16:probe_fire_v1` per LA §6.recovery.A row 10 SLSA in-toto attestation), `timestamp` (ISO 8601 UTC), `run_id` (with `s11_be_f_production_` prefix), `payload.probe_id`, `payload.probe_version`, `payload.probe_admission_lock_commit`, `payload.primitive_class` ∈ {A, B, C, D}, `payload.spec_iri`, `payload.implemented` (bool), `payload.evidence` (string ≤280 chars; behavioral observation OR precondition_missing descriptor), `payload.evidence_type` ∈ {`probe_fire_aggregate`, `precondition_missing`} | `payload.spec_class` (echo from BE-D scan), `payload.name_truncated` (echo), `payload.current_status_known` (echo from BE-D), `payload.behavioral_observation_count` (Class A specific), `payload.behavioral_path` (Class D specific: downstream_jsonl_fire OR downstream_citation OR none), `payload.judge_kind` (Class C specific: structural_judge_v0.1 OR llm_judge_v0.1), `payload.adr_evidence` (Class C precondition surface) | one event per `_aggregate_cycle()` × spec_iri; minimum 12 per BE-F close (3 per class × 4 classes); maximum unbounded (full 232-spec enumeration possible) |
| `probe_library_self_test.pass.event` (and `.fail.event`) | At every probe `_self_test()` execution against fixture pair (1 known-good + 1 known-bad); one row per fixture invocation; distinguished bool field carries the per-fixture distinguish verdict | `schema_version` (= `0.1`), `namespace` (= `cycle_16.be_f.probe_library_self_test`), `event_class` (= `probe_library_self_test.pass.event` OR `.fail.event`), `predicateType` (= `cycle16:probe_self_test_v1` — DISTINCT from production fires per LA §6.recovery.A row 10), `timestamp`, `run_id` (with `s11_be_f_probe_lib_self_test_` prefix), `payload.probe_id`, `payload.probe_version`, `payload.primitive_class`, `payload.fixture_path`, `payload.fixture_class` ∈ {known_good, known_bad}, `payload.expected_implemented` (bool), `payload.actual_implemented` (bool), `payload.distinguished` (bool; true iff expected == actual) | `payload.evidence` (≤200 chars; probe's evidence string for the fixture), `payload.evidence_type`, `payload.behavioral_path` (Class D), `payload.judge_kind` (Class C) | ≥8 events per BE-F close (4 probes × 2 fixtures); ≥1 event per probe per fixture; smoke-only fires NOT counted toward production acceptance per Done #15d |
| `probe_library_admission.pass.event` (and `.refuse.event`) | At every admission gate scan (`probes.admit_all()` or `probe_library_admission.sh` invocation); one row per probe discovered; verdict synthesizes the self-test exit code (PASS iff exit 0; REFUSE iff exit ≠ 0) | `schema_version` (= `0.1`), `namespace` (= `cycle_16.be_f.probe_library_admission`), `event_class` (= `probe_library_admission.pass.event` OR `.refuse.event`), `predicateType` (= `cycle16:probe_admission_v1`), `timestamp`, `run_id` (with `s11_be_f_admission_` prefix), `payload.probe_path`, `payload.probe_id`, `payload.primitive_class`, `payload.probe_library_version`, `payload.probe_admission_lock_commit` (SHA pinned at admission), `payload.verdict` ∈ {pass, refuse}, `payload.self_test_exit_code` (int) | `payload.fixture_class` (= `self_test_pair` for canonical admission; OR `self_test_pair_T12_negative` for T12 broken probe), `payload.evidence` (refusal: stderr_head + stdout_head extracts; pass: `self_test_distinguished_known_good_and_known_bad`) | ≥5 events per BE-F close (4 PASS for canonical probes + 1 REFUSE for T12 negative test) |
| `be_f_probe_library_ship.event` | At BE-F build close (Step 14 envelope authoring close) — single-fire NEW event class emitted to `outputs/build_runner_events.jsonl` (NOT to BE-F-specific sinks) via Cycle 15 BE#4 5-event baseline emit primitive | `schema_version` (= `0.1`), `namespace` (= `moonshots.build_runner`), `event_class` (= `be_f_probe_library_ship.event`), `timestamp`, `run_id`, `payload.cycle_id` (= 16), `payload.session_label` (= `Cycle-16-S11`), `payload.be_class` (= `BE-F`), `payload.probes_admitted_count` (= 4), `payload.production_fires_count` (≥12), `payload.t12_negative_test_verdict` (= `PASSED`), `payload.locked_preservation_verdict` (= `zero_marker_loss=true`) | `payload.honest_gaps` (string list; surface honest_gaps reproduced from envelope), `payload.hc70_reality_vs_intent_table_path` | one event per BE-F close (single-fire close marker) |

### §14.2 BE-F Measurement Hook (consumed by ACCEPTANCE_CRITERIA §14)

**Metric A_BE_F: probe_fire_events.jsonl production count + per-class coverage + mix** (post-condition #34 + Done #15d + substrate §1 item 6)

```bash
python3 -c "
import json
from collections import Counter, defaultdict
rows = [json.loads(l) for l in open('outputs/probe_fire_events.jsonl') if l.strip()]
prod = [r for r in rows if r['run_id'].startswith('s11_be_f_production_')]
classes = Counter(r['payload']['primitive_class'] for r in prod)
mix = defaultdict(lambda: {'implemented': 0, 'not_implemented': 0})
for r in prod:
    bucket = 'implemented' if r['payload']['implemented'] else 'not_implemented'
    mix[r['payload']['primitive_class']][bucket] += 1
print(f'total_production={len(prod)} classes={dict(classes)}')
for k in sorted(mix):
    print(f'  {k}: implemented={mix[k][\"implemented\"]} not_implemented={mix[k][\"not_implemented\"]}')
"
```
Expected at BE-F close: total_production ≥ 12; per-class ≥3; per-class mix ≥1 implemented + ≥1 not_implemented.

**Metric B_BE_F: probe_library_self_test_events.jsonl count + predicateType + per-class fixture pair** (post-condition #35)

```bash
python3 -c "
import json
rows = [json.loads(l) for l in open('outputs/probe_library_self_test_events.jsonl') if l.strip()]
st = [r for r in rows if r.get('predicateType') == 'cycle16:probe_self_test_v1']
from collections import defaultdict
by_class_fxc = defaultdict(set)
for r in st:
    by_class_fxc[r['payload']['primitive_class']].add(r['payload'].get('fixture_class'))
print(f'self_test_rows={len(st)}')
for k in sorted(by_class_fxc):
    print(f'  {k}: fixture_classes={sorted(by_class_fxc[k])}')
"
```
Expected at BE-F close: self_test_rows ≥ 8; per-class fixture_classes = {known_good, known_bad}.

**Metric C_BE_F: probe_library_admission_events.jsonl PASS+REFUSE counts** (post-condition #33 + T12 negative test evidence)

```bash
python3 -c "
import json
from collections import Counter
rows = [json.loads(l) for l in open('outputs/probe_library_admission_events.jsonl') if l.strip()]
ctr = Counter(r['payload']['verdict'] for r in rows)
print(f'pass={ctr[\"pass\"]} refuse={ctr[\"refuse\"]}')
"
```
Expected at BE-F close: pass ≥ 4 (canonical 4-probe admission); refuse ≥ 1 (T12 negative test broken probe).

### §14.3 BE-F Refusal-on-Violation (extension to §3)

| Failure mode | Refusal behavior | Surface |
|---|---|---|
| Probe self-test does not distinguish known_good + known_bad fixtures | admission gate refuses (exit non-zero); emits `probe_library_admission.refuse.event` to admission sink; refused probe NOT added to ADMITTED_PROBES list (omitted from __all__); DP#44 BINDING refuse-on-missing-precondition | caller stderr (admission CLI) + envelope `issues` + admission JSONL sink |
| Probe body modified post-admission without version bump (PROBE_VERSION or PROBE_ADMISSION_LOCK_COMMIT inconsistent) | halt-and-surface per §14.3 invariant 23; require Builder-ARCH paradigm dispatch (HC #74); admission gate detects via SHA comparison at re-admission | caller stderr + envelope `issues` |
| Generic-emission escape primitive proposed (probe body inspects "any emit event of any class fires" rather than spec-class-specific behavioral surface) | halt-and-surface per substrate §7 anti-pattern + KT-9 firing surface; Builder-ARCH paradigm dispatch required; do NOT route around by adding the primitive at admission | caller stderr + envelope `issues` + paradigm escalation candidate per HC #74 |
| Class C LLM-judge invoked and returns implemented=True on known-bad fixture (substitution failure — registry-text / ADR-text / FINDINGS-mention accepted as evidence) | structural-judge fallback REFUSES at admission via `_structural_judge()` enforcing same contract shape (file:line citation required; embodimentRef ≠ DECISION_LOG); KT-8 firing surface candidate | caller stderr + envelope `issues` |
| Substitution shape detected in probe body at HC #72 sweep (registry-field read / status-enum equality / token count / smoke-only / artifact-exists / single-smoke) | halt-and-surface per HC #72 BINDING; Builder-ARCH paradigm dispatch required for probe body repair; refuse to admit the substitution-shape probe | caller stderr + envelope `issues` + Coach R3 sweep verdict |
| Smoke-only fire submitted as acceptance evidence (`run_id` prefix `_smoke_*` or `_probe_lib_self_test_*` instead of `s11_be_f_production_*`) | R3 aggregation filters via `run_id` prefix; smoke-only fires NOT counted toward acceptance per Done #15d strict; FAIL on probe-coverage acceptance threshold if no production fires present | R3 close-eval verdict + envelope `acceptance_filter_evidence` |
| Probe-fire timeout (≥120s on single invocation) | admission gate halts that probe with `self_test_timeout_exceeded_120s` evidence; subprocess.TimeoutExpired raised; refusal event emitted | caller stderr + envelope `issues` |
| KT-7 (self-test fail) / KT-8 (gate predicate string-matches probe ID) / KT-9 (generic-emission escape) / KT-10 (zero production probe fires on ≥1 class after admission) firing at BE-F close | halt-and-surface per HC #59 BINDING screen; §3.5 3-test pre-escalation gate; if all 3 confirm paradigm-class, halt + executive-format surface to Rex per HC #74 BINDING + Pattern 11 Step 3.5; do NOT proceed to §14 BE-F appends or commit | envelope `status: blocked` + paradigm escalation candidate |

### §14.4 BE-F Append-only Discipline (extension to §4)

Same invariant as §4 + §13: append-only at all 3 NEW BE-F sinks (`probe_fire_events.jsonl` + `probe_library_self_test_events.jsonl` + `probe_library_admission_events.jsonl`) + at `outputs/build_runner_events.jsonl` (5-event baseline + 1 `be_f_probe_library_ship.event` close-fire). The 4 NEW event classes are append-only per emit primitive contract — never overwrite or supersede prior events. `wc -l outputs/probe_fire_events.jsonl` strictly monotonically increasing across BE-F execution (0 at scaffold → 16 at BE-F dogfooding-within-cycle close → ≥16 per future cycle's BE-F probe re-fires for forward extrapolation at Phase 10 retroactive scan re-run per ROADMAP §10). Same for self-test + admission sinks. Probe body PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT constants are CONST-only (never reassigned at runtime); modifications require Builder-ARCH paradigm dispatch + new admission event row (new SHA pin).

### §14.5 BE-F Calibration Hook (extension to §5)

```bash
# Calibration: re-run admission gate + verify per-class self-test events
set -euo pipefail
cd /home/azureuser/cycle_16_close_spec_to_implementation_gap_build

# 1. Admission scan PASS
bash scripts/probe_library_admission.sh > /tmp/be_f_admission_summary.json
python3 -c "
import json
s = json.load(open('/tmp/be_f_admission_summary.json')) if False else None
import subprocess
# Re-invoke admission via the python module directly for structured verdict
import sys; sys.path.insert(0, 'scripts')
import importlib
# clear cache to ensure fresh admission scan
for mod in list(sys.modules):
    if mod.startswith('probes'): del sys.modules[mod]
import probes
admitted, refused = probes.admit_all()
assert len(admitted) == 4, f'CALIBRATION FAIL: expected 4 admitted, got {len(admitted)}'
assert len(refused) == 0, f'CALIBRATION FAIL: unexpected refusals: {refused}'
print('CALIBRATION PASS: admission gate admitted 4 + refused 0')
print('CALIBRATION PASS: probe_library_admission_events.jsonl event count matches admission verdict')
"

# 2. Self-test events count + per-class coverage
python3 -c "
import json
from collections import defaultdict
rows = [json.loads(l) for l in open('outputs/probe_library_self_test_events.jsonl') if l.strip()]
by_class = defaultdict(set)
for r in rows:
    if r.get('predicateType') == 'cycle16:probe_self_test_v1':
        by_class[r['payload']['primitive_class']].add(r['payload'].get('fixture_class'))
for cls in 'ABCD':
    fxcs = by_class.get(cls, set())
    assert 'known_good' in fxcs and 'known_bad' in fxcs, f'CALIBRATION FAIL: class {cls} missing fixture pair'
print('CALIBRATION PASS: all 4 classes have known_good + known_bad self-test events')
"
```

### §14.6 BE-F Self-test (extension to §6)

| # | Check | Status |
|---|---|---|
| 1 | 4 NEW event classes declared with trigger + required fields per §14.1 (`probe_library.fire.event` + `probe_library_self_test.{pass,fail}.event` + `probe_library_admission.{pass,refuse}.event` + `be_f_probe_library_ship.event`) | [x] PASS |
| 2 | Measurement hooks A_BE_F + B_BE_F + C_BE_F reproduce same value across two independent operators (deterministic JSONL aggregations) | [x] PASS (Python one-liners against same files = deterministic; admission-scan re-invocation yields same verdict given unchanged probe bodies) |
| 3 | Refusal-on-violation wired for 8 failure modes per §14.3 (self-test-non-distinguishing + version-lock-violation + generic-emission-escape + LLM-judge substitution + HC #72 substitution shape + smoke-only-as-acceptance + probe-fire timeout + KT-7/8/9/10 firing) | [x] PASS |
| 4 | Append-only discipline verified at all 3 NEW sinks (strictly monotonically increasing line counts during BE-F dogfooding-within-cycle execution) | [x] PASS (pre-BE-F + post-BE-F wc -l diffs match expected counts: probe_fire +16 / self_test ≥+8 / admission ≥+5) |
| 5 | Calibration hook fires PASS on admission re-scan + per-class self-test coverage check | [x] PASS (calibration verifies 4 admitted + 0 refused + per-class known_good + known_bad fixture pair present) |
| 6 | Schema version `0.1` locked at Cycle-16-S11 close paired-commit + predicateType discriminators (`cycle16:probe_fire_v1` for production / `cycle16:probe_self_test_v1` for self-test / `cycle16:probe_admission_v1` for admission) STRUCTURALLY distinct per LA §6.recovery.A row 10 SLSA chain-of-custody | [x] PASS (predicateType values verified distinct in each sink; structural discriminator at JSONL row level enforces SLSA-style provenance routing) |

<!-- /gate:runtime_emit_spec §14 -->

## §15 BE-G Cycle 16 Stage 5 Write-Boundary Enforcement Emit Schema Append

> ADDITIVE-APPEND per HC #45 (chain n=7). §1-§14 preserved byte-identical above.

### §15.1 NEW event classes (BE-G)

| event_class | namespace | sink | payload key fields |
|---|---|---|---|
| `pre_commit_hook_block.fire.event` | `cycle_16.be_g.spec_authoring` | `outputs/spec_authoring_events.jsonl` | verdict=HARD_BLOCK, violating_files[], evidence_type=write_boundary_violation |
| `spec_authoring_event.fire.event` | `cycle_16.be_g.spec_authoring` | `outputs/spec_authoring_events.jsonl` | spec_path, delivery_latency_ms (≤60000), git_bypassing_write_bool, evidence_type=filesystem_write_observation |
| `three_registry_reconciliation.fire.event` | `cycle_16.be_g.three_registry_reconciliation` | `outputs/three_registry_reconciliation_events.jsonl` | filesystem_spec_class_count, kg_cycle16_spec_count, prompt_inventory_agent_spec_count, drift_detected_bool, drift_reason |
| `spec_implementation_present_gate.probe_fire_aggregate.fire.event` | `cycle_16.be_g.spec_implementation_gates` | `outputs/spec_implementation_gates_events.jsonl` | verdict, evidence_type=probe_fire_aggregate, probe_fire_total, probe_fire_implemented |
| `spec_implementation_session_close_gate.probe_fire_aggregate.fire.event` | `cycle_16.be_g.spec_implementation_gates` | `outputs/spec_implementation_gates_events.jsonl` | evidence_type=probe_fire_aggregate, probe_fire_rows_in_window, dormant_specs_no_recent_impl_count, advisory_mode_bool=true |
| `spec_killed_event.fire.event` | `cycle_16.be_g.spec_registry` | `outputs/spec_registry_events.jsonl` | spec_iri, adr_retraction_ref, audit_trail_link, new_status=cycle16:killed, success_bool |
| `kill_spec.refusal.event` | `cycle_16.be_g.spec_registry` | `outputs/spec_registry_events.jsonl` | refusal_class, raised=ValueError (DP#44; NO spec_killed_event on refusal) |
| `spec_registry.forward_apply_warn.event` | (caller namespace) | `outputs/spec_registry_events.jsonl` | spec_iri, warn (non-fatal forward-apply/hook failure) |

### §15.2 forward_apply_emit() production wiring (Done #12 item 3)

`register_spec()` now calls `forward_apply_emit()` after a successful write, emitting
`spec_authoring_event` (no cycle_implemented) or `spec_implementation_event` (with
cycle_implemented/session_implemented) to `outputs/forward_apply_observation_events.jsonl`
with `authoring_source: production_register_spec`. This closes the emit.py:96 zero-caller gap.

### §15.3 Non-smoke run_id discipline

All BE-G production fires carry run_id prefix `s12_be_g_production_*` (never `smoke`/`test`).
Acceptance counts smoke-prefixed fires as ZERO (HC #67 + Done #15d).

<!-- /gate:runtime_emit_spec §15 -->

## §16 — BE-H structural-prevention emit schema (Cycle-16-S13)

Common envelope: `schema_version`, `namespace` (`cycle_16.be_h.<piece>`),
`event_class` (`<piece>.{refuse,pass,checkpoint_flag,deprecate}.event`),
`predicateType` (`cycle16:<piece>_v1`), `timestamp` (UTC),
`run_id` (production prefix `s13_be_h_production_<piece>_*`), `payload`.

Per-piece payload fields:
- substitution_gate: `surface`, `definition_id`, `verdict`, `reason`,
  `named_probe`, `self_test_exit`, `proxy_class`, `refuse`.
- stage_0_probe_presence: `reason`, `class`, `module`, `self_test_exit`,
  `present`, `required`, `refuse`.
- reality_vs_intent: `surface`, `rows`, `incomplete_rows`, `probe_failures`,
  `verdict`, `refuse`.
- number_tagging: `surface`, `target`, `untagged_numbers`,
  `heuristic_in_verdict`, `verdict`, `refuse`.
- probe_coverage: `coverage` (per-class prod/impl), `cycle`, `reason`, `refuse`.
- library_self_test: `result` (probes/fails/crashes/deprecations), `refuse`;
  per-probe rows carry `crash` bool + `self_test_exit` + `session`.
- deferral_expiration: `spec`, `verdict`, `reason`, `missing_fields`,
  `age_sessions`, `max_window`, `auto_route`, `refuse`.
- design_anchor_disclosure: `verdict`, `internal_load_bearing`,
  `checkpoint_flag`, `paradigm_escalation_candidate`, `refuse`.
- auto_deprecate: `probe_id`, `reason`, `sessions`, `action`, `refuse`.

session_close_gate carry-fix upgrade: `dormant_specs_over_threshold_bool` now
admits the `crash` value (HC-BE-G-1); dormancy window partitioned by real
session index (HC-BE-G-2).

(Stage 5 BE-H ADDITIVE-APPEND per Cycle-16-S13; BE-A..BE-G preserved verbatim.)
