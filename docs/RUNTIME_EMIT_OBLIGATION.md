# Runtime Emit Obligation (auto-installed by govML v2.8.2 scaffolding)

> Auto-installed by `init_project.sh --profile research-build` per Cycle-15-S7 BE#4
> Branch 2.2 runtime emit deployment + Rex Step 3.5 Option B disposition 2026-05-27.
> Closes HC #23 BINDING (runtime emit obligation NOT wired across kc-34..kc-42 lifecycle).

## Authority chain

- Cycle 10 PRIMARY workflow primitive specs at `~/cycle_10_autonomous_cycle_apparatus_build/scripts/`:
  - `kernel_coach_workflow_primitive_spec.md` (91L; §2 5-event schema; §3 3-seam; §5 drift; §7 Item 2)
  - `implementation_coach_workflow_primitive_spec.md` (125L; §2 7-event schema; §3 3-seam classes; §5 4-drift; §7 Item 2)
- Cycle 10 BE#5 RUNTIME_EMIT_SPEC at `~/cycle_10_autonomous_cycle_apparatus_build/docs/be5/RUNTIME_EMIT_SPEC.md` (266L; §0 emit identity + §1 per-event required fields + §2 measurement hooks + §3 refusal-on-violation + §4 append-only + §5 calibration hook)
- Cycle 10 BE#5 drift schema v0.1 at `~/cycle_10_autonomous_cycle_apparatus_build/scripts/drift_telemetry_signal_schema.json` (vendored copy at `scripts/runtime_emit/drift_telemetry_signal_schema.json`)
- Cycle 15 SI Branch 2.2 + ROADMAP Phase 3 task 2
- govML v2.8.2 wire-in at `~/ml-governance-templates/scripts/init_project.sh` `install_runtime_emit_substrate()` function

## 4-namespace per-role schema (PUBLISHABLE per HC-11 partition Binding 8)

| Role | Sink path | Namespace pattern | Schema version | Event-class count |
|---|---|---|---|---|
| kernel-coach | `outputs/kernel_coach_events.jsonl` | `<project>.kernel_coach.*` | `0.1` | 5 (session.start / warmup.complete / transition.fire / drift.signal / session.end) |
| impl-coach | `outputs/impl_coach_events.jsonl` | `<project>.impl_coach.*` | `0.1` | 7 (session.start / warmup.complete / handoff.inbound / transition.fire / drift.signal / handoff.outbound / session.end) |
| coach | `outputs/coach_events.jsonl` | `<project>.coach.*` | `0.1` | DEFERRED (coach-class is session-role-class per coach_core.md, not Agent-tool spec; sink reserved; population deferred to coach_core.md edit per HC #45 explicit Rex authorization discipline at kc-44+ PD inheritance) |
| build-runner | `outputs/build_runner_events.jsonl` | `<project>.build_runner.*` | `0.1` | 5 (session.start / dispatch.received / build.phase.start / build.phase.complete / session.end) + 1 drift (build_runner_runtime_failure) |

## Drift telemetry baseline (4-class per ROADMAP §2.5; v0.1)

Per `scripts/runtime_emit/drift_telemetry_signal_schema.json` vendored copy:

1. `content_fidelity_drift` (severity_default=WARN) — content diverges from upstream artifact citation
2. `scope_drift` (severity_default=HALT) — work drifts beyond cycle SI §3 IN into §3 OUT
3. `paradigm_misclassification` (severity_default=HALT) — operational classified as paradigm or vice versa
4. `phase_scope_violation` (severity_default=HALT) — work crosses phase scope (e.g., Stage 3-4 RP authoring drifts into Stage 5 build authoring)

Plus 4 BE#6 impl-coach + 4 BE#3 actor-trust + 4 BE#2 action-class + 4 BE#4 destination-class + 4 BE#7 integrated-apparatus drift classes (namespace-isolated; see vendored schema for full taxonomy).

## Refusal-on-violation default (per RUNTIME_EMIT_SPEC §3)

Halt-and-surface: if the artifact cannot record the boundary it just crossed, it cannot proceed. Per Cycle 10 BE#5 RUNTIME_EMIT_SPEC §3 row 1: emit sink unwritable → refuse-to-start. Per row 2: drift class outside schema → halt-and-surface (emit refusal event with drift_class=schema_violation_attempt). Per row 3: required field null → halt-and-surface. Per row 4: monotonic timestamp violation → halt-and-surface.

## Append-only discipline (per RUNTIME_EMIT_SPEC §4)

- Events are append-only (no deletion or edit; corrections emit new event with `supersedes:` field)
- Timestamps monotonic per `run_id` within a single run
- `schema_version` recorded per event
- Run boundary brackets: `session.start` MUST precede every other event in a run; `session.end` MUST be the last event

## HC-11 partition (Binding 8 BIND across wrapper)

- **PUBLISHABLE:** schema + integration patterns + role contracts + sink-path convention + 4-namespace enumeration + drift-class taxonomy names + severities + detection cadences + Rex Step 3.5 authority anchor
- **PIPELINE-IP-PRIVATE:** pre-escalation gate state-machine internals + drift-detection algorithm bodies + per-event content payload bodies + agent-internal state + Round 1/3 validation logic source — NEVER inlined here

## Item 2 (a)(b)(c) BINDING per Cycle 10 ROADMAP §2.5 + §2.6 verbatim

- **(a) Extension mechanism live:** new drift class added by namespace-append (no spec edit required per namespace-driven dispatch); new role added by namespace-append to this 4-namespace table
- **(b) Hypothetical-extension test passes:** new cycle's worked-example asserts emit ≥1 event of new class through wired infrastructure (vendored schema preserves Cycle 11 first-run worked-example test references)
- **(c) v0.1→v0.2 migration path:** base 4 drift classes preserved + new additive (append-only enum positions) + deprecation policy (`rank=deprecated` Wikidata pattern; classes kept in schema; emit only by legacy versions)

## Usage

```bash
# Library import (Python)
from runtime_emit.emit import emit_event
emit_event(
    sink_path="outputs/kernel_coach_events.jsonl",
    namespace="<project_id>.kernel_coach",
    event_class="kernel_coach.session.start",
    cycle_id="<cycle_id>",
    session_label="<S-N>",
    handoff_source="prior_kc_pd",
)

# CLI smoke test
python3 scripts/runtime_emit/emit.py --help
python3 scripts/runtime_emit/emit.py \
    --sink outputs/build_runner_events.jsonl \
    --namespace cycle_15.build_runner \
    --event-class build_runner.session.start \
    --cycle-id cycle_15 --session-label S7
```

## Why scaffolding-time install (vs runtime-import-only)

Per Cycle-15-S7 LESSONS_LEARNED (govML companion edit §3.2): emit-as-scaffolding-time-install ensures auto-inheritance + zero per-project ceremony. Behavioral instruction "remember to add emit hooks per project" would have shipped n=4-6 forgotten across kc-34..kc-42 lifecycle (HC #23 BINDING observed gap). Structural enforcement via scaffolding is DP#1 meta-scale (structural > behavioral).
