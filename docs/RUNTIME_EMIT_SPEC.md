# RUNTIME EMIT SPEC

<!-- version: 0.1 -->
<!-- created: {{DATE}} -->
<!-- profile: build -->
<!-- methodology_status: skeleton — first-cycle build-class formalization -->

> **Authority Hierarchy**
>
> | Priority | Document | Role |
> |----------|----------|------|
> | Tier 1 | `{{TIER1_DOC}}` | Primary spec — highest authority |
> | Tier 2 | `{{TIER2_DOC}}` | Clarifications — cannot override Tier 1 |
> | Tier 3 | `{{TIER3_DOC}}` | Advisory only — non-binding if inconsistent with Tier 1/2 |
> | Contract | This document | Implementation detail — subordinate to all tiers above |

### Companion Contracts

**Upstream (this contract depends on):**
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §1 for the run-context that triggers emits

**Downstream (depends on this contract):**
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §2 for measurement protocols that read these emits
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §1 for cross-system event-log shape this spec contributes to
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §3 for promotion gates that read emits as evidence

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{ARTIFACT_NAME}}` | Artifact emitting the events | `signal-pipeline-v1` |
| `{{EVENT_TABLE_NAME}}` | Event sink (DB table / log file / event bus topic) | `engml_enforcement_events` |
| `{{EVENT_NAMESPACE}}` | Namespace for events from this artifact | `signal_pipeline.poll` |
| `{{MIN_PER_RUN_EVENTS}}` | Minimum number of structured events per run | `3` |

> Delete this section once the contract is filled.

---

## §0 Emit Identity

<!-- gate:runtime_emit_spec §0 required -->

| Field | Value |
|---|---|
| **Artifact** | {{ARTIFACT_NAME}} |
| **Event sink** | {{EVENT_TABLE_NAME}} |
| **Event namespace** | {{EVENT_NAMESPACE}} |
| **Schema version** | {{SCHEMA_VERSION}} |
| **Min events per run** | {{MIN_PER_RUN_EVENTS}} |

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
| {{EVENT_CLASS}} | {{when emitted (entry / exit / boundary / refusal / verdict)}} | {{run_id, timestamp, namespace, ...}} | {{...}} | {{exactly-once / at-least-once / count-bounded}} |

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

```
{{MEASUREMENT_QUERY_OR_HOOK}}
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
| {{FAILURE_MODE}} | {{halt-and-exit-nonzero / fall-back-to-local-buffer / refuse-to-start}} | {{stderr / status_file / event_bus DLQ}} |

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
{{CALIBRATION_COMMAND}}
```

| Calibration check | What it asserts | Run frequency |
|---|---|---|
| {{CALIBRATION_NAME}} | {{e.g., "every required field in §1 is non-null on a fixture run"}} | {{every commit / pre-promotion / weekly}} |

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
| 1 | Every §1 event class has a trigger AND required-field set | [ ] |
| 2 | §2 measurement hook reproduces the same value across two independent operators on the same emit log | [ ] |
| 3 | §3 refusal-on-violation is wired (not "TBD") for at least one failure mode | [ ] |
| 4 | §4 append-only discipline is verified by inspection of the event sink | [ ] |
| 5 | §5 calibration hook runs to PASS on a fixture before first production run | [ ] |
| 6 | Schema version (§0) is locked at promotion commit | [ ] |

> If any check is `[ ]`, halt-and-surface; do NOT promote to production.
