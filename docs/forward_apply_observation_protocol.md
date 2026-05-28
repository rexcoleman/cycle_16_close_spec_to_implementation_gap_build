# Forward-Apply Observation Protocol — Cycle 16 BE-E

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- profile: build -->
<!-- methodology_status: BE-E authored — Cycle 16 Stage 5 BE-E forward-apply observation infrastructure (Branch 4.5 BE-D-source closure per ROADMAP Phase 6) -->
<!-- source: dispatch substrate §1 item 2 + Cycle 16 SI Amendment 27a (≤3-session runtime emit detection threshold per spec) + Branch 4.5 + Done #9 + H8 + KT-5 firing surface -->
<!-- partition: c6:publishable (observation surface design + event-class taxonomy + session-close hook semantic + cycle-close aggregate hook + longitudinal verdict surface + refusal discipline + HC-11 partition + self-test); IP-private (per-host enforcement routing internal implementation + agent-prompt details + per-spec evidence trail at JSONL row content — referenced not inlined per HC-11 partition §6) -->

> **Authority chain.** Cycle 16 SI ACTIVE 2026-05-27 (`a2f14d5`) + Amendment 27a (`be54a97`; same-cycle deadline + ≤3-session runtime emit detection per spec) + Amendment 27b (`badd749`; KG-primary `/cycle6`) + Rex disposition (C) D-S2-1 + S3-S6 BE-A/B/C/D close dispositions + Rex 2026-05-27 Option A (Cycle 16 narrow; HC-BE-D-1 write-boundary enforcement gap → Cycle 18 scope per Option B split-sequential) + kc-46 R1 PASS task-context dispatch 2026-05-27 via Cycle-16-S7 Coach → Build-Runner BE-E. Cycle 10 BE#5 RUNTIME_EMIT_SPEC §3 inheritance (refusal-on-violation = halt-and-surface).

> **Companion documents.** ARTIFACT_CONTRACT.md §13 BE-E append (pre-conditions + post-conditions + invariants + side effects + versioning + change control + self-test) + RUNTIME_EMIT_SPEC.md §13 BE-E append (2 NEW event class schemas + measurement hook + refusal-on-violation extension + append-only + calibration hook + self-test) + ACCEPTANCE_CRITERIA.md §13 BE-E append (thresholds 25-30 + measurement protocol + per-test-bed strengthening n≥3 + failure shape grid + honest resolution log + self-test) + spec_authoring_discipline.md §4 Operations 1-5 (BE-A canonical write-boundary primitives that THIS observation surface measures) + spec_registry_authoring.py (BE-B Python wrapper consumed at every `spec_authoring_event` fire). BE-D `retroactive_scan_cycle_1_15_run.json` is the inventory baseline at /cycle6 against which forward-apply increments are observed.

---

## §0 Scope

Forward-apply observation infrastructure for the Cycle 16 spec-implementation gap closure mechanism. Observes the BE-B-mediated authoring path and the BE-C-mediated implementation-status transition path across the Cycle 17 → Cycle 18 → Cycle N+ longitudinal window. Two new runtime emit event classes wire observation into the existing `scripts/runtime_emit/emit.py` primitive (additive extension; `emit_event()` core signature UNCHANGED per Cycle 10 §0 schema_version=0.1 LOCKED).

**In scope:** (a) `spec_authoring_event` fires at every BE-B `register_spec()` SPARQL UPDATE write boundary; (b) `spec_implementation_event` fires when a spec's `cycle16:currentStatus` transitions to `cycle16:running` via the spec's `cycle16:runtimeEmitEventClass` first firing within the ≤3-session dormancy threshold per Amendment 2026-05-27a; (c) session-close hook consumes the events to drive `spec_implementation_session_close_gate.sh` ADVISORY surface; (d) cycle-close aggregate hook emits a SPARQL `SELECT COUNT(*) ?spec_type ?current_status` rollup per BE-B/BE-C; (e) longitudinal verdict at Cycle 18 close evaluates H8 cumulative ≥2-cycle window per HR §3 H8 (BE-E enables the surface; Cycle 18 evaluates the verdict).

**Out of scope.** Write-boundary enforcement closure for specs that bypass the BE-B wrapper entirely — that is HC-BE-D-1 write-boundary enforcement gap → Cycle 18 scope per Rex 2026-05-27 Option B split-sequential. BE-E inherits the SAME blind spot as BE-D: it can only observe what is registered via the BE-B-mediated authoring path. Filesystem-scan + spec-class-discriminator + work-host routing belongs to a different primitive class than what BE-E ships.

---

## §1 Event-class taxonomy (2 NEW classes; extends Cycle 15 BE#4 build-runner 5-event baseline)

| Event class | Trigger boundary | Required fields | Optional fields | Cardinality |
|---|---|---|---|---|
| `spec_authoring_event` | At every BE-B `register_spec()` SPARQL UPDATE write boundary (Operation 1 per spec_authoring_discipline.md §4); fires AFTER the write succeeds (HTTP 200 OR 204) and BEFORE the wrapper returns to caller | `schema_version` (= `0.1`), `namespace` (= `cycle_16.be_e.forward_apply_observation`), `event_class` (= `spec_authoring_event`), `timestamp` (ISO 8601 UTC), `run_id` (UUID), `payload.spec_iri`, `payload.spec_type` ∈ {AgentContract, Schema, DesignDecision, MethodologyCommitment}, `payload.cycle_authored` (integer), `payload.target_session` (string; e.g., `S7` or `n/a — retroactive`), `payload.current_status` (= `cycle16:dormant-silent` at first-write per BE-B wrapper default), `payload.access_permission` ∈ {`c6:publishable`, `c6:ip-private`} per HC-11 enforcement, `payload.prov_o_typed_edges` (4-edge object: `wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy` per Cycle 6 BE#1 contract) | `payload.runtime_emit_event_class` (string OR `n/a — citation-based activation per DP#26` carve-out literal + `payload.n_a_rationale` per HR §3d), `payload.retroactive_classification` (boolean; true at BE-D historical scan path; false at BE-E forward-apply path) | one event per BE-B `register_spec()` invocation (1:1 with `spec_registry.write.event` in BE-B's own namespace) |
| `spec_implementation_event` | When a spec's `cycle16:currentStatus` transitions from `cycle16:dormant-silent` (or `cycle16:dormant-with-explicit-deferral`) to `cycle16:running` via the spec's declared `cycle16:runtimeEmitEventClass` firing within the spec's declared `cycle16:dormancyDetectionThresholdSessions` window per Amendment 2026-05-27a (default ≤3 sessions) | `schema_version` (= `0.1`), `namespace` (= `cycle_16.be_e.forward_apply_observation`), `event_class` (= `spec_implementation_event`), `timestamp` (ISO 8601 UTC), `run_id` (UUID), `payload.spec_iri`, `payload.spec_type`, `payload.runtime_emit_event_class` (the class that fired; matches the spec's declared field 10), `payload.first_fire_timestamp` (ISO 8601 UTC), `payload.sessions_between_authoring_and_first_fire` (integer ≥0), `payload.dormancy_detection_threshold_sessions` (integer per spec's declared field 13), `payload.within_threshold_bool` (true if `sessions_between` ≤ threshold), `payload.status_transition` (= `dormant-silent → running` OR `dormant-with-explicit-deferral → running`), `payload.prov_o_typed_edges` (4-edge object per Cycle 6 BE#1) | `payload.access_permission` (carry-forward from `spec_authoring_event` for the same spec_iri), `payload.first_fire_sink_path` (e.g., `outputs/build_runner_events.jsonl`), `payload.first_fire_event_iri` (nanopub-style reference to the firing event for provenance traceback) | one event per spec status transition to `running` (single-fire per spec lifetime; spec lifecycle is monotonic: `dormant-silent → running` once; subsequent fires of the same event_class do NOT re-fire `spec_implementation_event`) |

**Sink:** `~/cycle_16_close_spec_to_implementation_gap_build/outputs/forward_apply_observation_events.jsonl` (NEW; empty at scaffold; refuse-on-violation per RUNTIME_EMIT_SPEC §3 fires if absent at first emit attempt).

**Namespace isolation invariant** (per Cycle 10 rule_6 + rule_8 + rule_10 + rule_12): BE-E namespace `cycle_16.be_e.forward_apply_observation` is namespace-isolated from BE-A `cycle_16.be_a.spec_registry` + BE-B `cycle_16.be_b.spec_registry` + BE-C `cycle_16.be_c.spec_implementation_gates` + BE-D `cycle_16.be_d.retroactive_scan`. The 2 NEW classes do NOT co-exist with BE-A/B/C/D classes in the same JSONL sink; cross-namespace coordination is via SPARQL query at `/cycle6` (BE-B writes the registry rows; BE-E observes the writes via emit at the SAME wrapper call boundary).

---

## §2 Session-close hook (consumes BE-C `spec_implementation_session_close_gate.sh` ADVISORY surface)

At every session close (kernel-coach `kernel_coach.session.end` + build-runner `build_runner.session.end` + impl-coach `impl_coach.session.end` per Cycle 15 BE#4 baseline), the session-close hook performs the following sequence:

1. Read `~/<project>/outputs/forward_apply_observation_events.jsonl` and aggregate `spec_implementation_event` rows whose `payload.first_fire_timestamp` falls within the current session window (bounded by the matching `*.session.start` and `*.session.end` events in the same `outputs/<role>_events.jsonl` sink).
2. For each spec with status transition `dormant-silent → running` (or `dormant-with-explicit-deferral → running`) within the session window, emit a session-scoped roll-up event (no new event class; this is read-side aggregation, not write-side emit).
3. Invoke `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh --advisory-mode` per BE-C Operation 4 contract. The gate queries `/cycle6` for dormant-silent specs exceeding their `dormancyDetectionThresholdSessions` field and emits ADVISORY WARN if any are present.
4. The session-close hook does NOT BLOCK the session close on ADVISORY WARN (per BE-C default mode); the WARN surfaces at session handoff for the next session to address (per session-close-gate ADVISORY semantics).

**Honest gap.** BE-E session-close hook observes only specs that flowed through the BE-B authoring wrapper. Specs filesystem-resident WITHOUT BE-B wrapper invocation (HC-BE-D-1 write-boundary enforcement gap) are NOT observed at this hook. Cycle 18 scope per Rex Option B split-sequential closes the write-boundary enforcement gap; until then, this hook's observation is bounded by BE-B authoring coverage.

---

## §3 Cycle-close aggregate hook (consumes BE-C `spec_implementation_present_gate.sh` BLOCKING surface)

At every cycle close (build-orchestrator promotion event at DEPLOYMENT_LOG §2), the cycle-close aggregate hook performs the following sequence:

1. Query `/cycle6` with the BE-B/BE-C aggregate SPARQL:

    ```sparql
    PREFIX cycle16: <http://cycle16.local/ontology#>
    SELECT ?spec_type ?current_status (COUNT(DISTINCT ?spec) AS ?n)
    WHERE {
      GRAPH <http://cycle16.local/registry/assertion> {
        ?spec a cycle16:Spec ;
              cycle16:specType ?spec_type ;
              cycle16:currentStatus ?current_status ;
              cycle16:cycleAuthored ?ca .
        FILTER (?ca >= 16)
      }
    }
    GROUP BY ?spec_type ?current_status
    ORDER BY ?spec_type ?current_status
    ```

2. Aggregate the 4-spec-class × 5-state breakdown for specs authored Cycle 16 onward (excludes BE-D historical inventory via `FILTER (?ca >= 16)`). Compare against the BE-D baseline at `outputs/retroactive_scan_cycle_1_15_run.json` `aggregate_counts_4x5` for trend.
3. Invoke `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` (BLOCKING by default). Gate FAILs if any Cycle-16-onward dormant-silent specs lack `cycle16:rexAuthorizationForDeferralPastCycleClose` edges per BE-C Operation 3 contract.
4. Cycle-close aggregate values feed Cycle 18 H8 longitudinal verdict per §4 below.

---

## §4 Longitudinal verdict surface (Cycle 18 evaluation; BE-E enables, Cycle 18 evaluates)

H8 per HR §3 H8: "Cumulative spec-implementation rate ≥ Cycle 16 BE-D baseline across ≥2 cycle window post-BE-E forward-apply observation infrastructure." H8 evaluation is NOT performed at BE-E close (mid-cycle observation window S7→S8 may be insufficient for full longitudinal verdict per task context Step 7 honest disclosure); Cycle 18 evaluates H8 against the cumulative `spec_implementation_event` count growth from BE-E close baseline (≥4 smoke events) through Cycle 17 and Cycle 18 fire boundaries.

**KT-5 firing surface evaluation at BE-E close (PRIMARY OBJECTIVE per dispatch substrate §5; task context Step 7).** KT-5 IS pre-registered SI kill condition per ED §Field 6 KT-5 + HR §3 H8 + Cycle 16 SI §K-conditions; NOT operationally-revisable per HC #59 BINDING (HC #59 metric-revision-within-intent applies to OPERATIONAL metrics, NOT pre-registered SI kill conditions). Threshold: ≥2 NEW dormant-silent specs accumulated DURING Cycle 16 itself (NOT retroactive — only specs authored at Cycle-16-S1..S7 timeline; the 137 BE-D retroactive dormant-silent are Cycles 1-15 inventory excluded). KT-5 evaluation at BE-E close queries `/cycle6` via SPARQL:

```sparql
PREFIX cycle16: <http://cycle16.local/ontology#>
SELECT (COUNT(DISTINCT ?spec) AS ?n) WHERE {
  GRAPH <http://cycle16.local/registry/assertion> {
    ?spec a cycle16:Spec ;
          cycle16:currentStatus cycle16:dormant-silent ;
          cycle16:cycleAuthored 16 .
    FILTER NOT EXISTS { ?spec cycle16:retroactiveClassification true }
  }
}
```

KT-5 FIRES if count ≥ 2 → H_main REFUTED → FINDINGS Layer 5 honest-gap + paradigm escalation candidate per dispatch substrate §5 KT-5 disposition row. KT-5 DOES NOT FIRE if count < 2 → record honest-gap re window adequacy per task context Step 7; S8 transition prompt routes to Cycle 16 close 5-layer FINDINGS authoring (ROADMAP Phase 7).

---

## §5 Refusal-on-violation discipline (per RUNTIME_EMIT_SPEC §3 inheritance + DP#44 BINDING)

Halt-and-surface defaults inherited from Cycle 10 BE#5 RUNTIME_EMIT_SPEC §3 + Cycle 16 BE-A RUNTIME_EMIT_SPEC §3 + BE-B `spec_authoring_discipline.md §5`:

| Failure mode | Refusal behavior | Surface |
|---|---|---|
| `outputs/forward_apply_observation_events.jsonl` sink unwritable at first emit attempt | halt-and-surface; emit `build_runner_runtime_failure.event` (severity=HALT) per Cycle 15 BE#4 drift class; do NOT proceed with `spec_authoring_event` OR `spec_implementation_event` fires | caller stderr + envelope `issues` |
| SHACL refuses the smoke-test synthetic spec (BE-A 14-field schema rejection) | halt-and-surface per BE-A §3 SHACL refusal contract; do NOT route around with relaxed shapes; document refusal at envelope `issues` and re-author the synthetic fixture | caller stderr + envelope `issues` |
| PROV-O typed-edge fails to propagate (`wasGeneratedBy` OR `wasAttributedTo` OR `generatedAtTime` OR `wasInformedBy` missing from `spec_authoring_event` OR `spec_implementation_event` payload) | halt-and-surface per Cycle 6 BE#1 contract; PROV-O typed-edges are LOAD-BEARING for downstream provenance traceback; document refusal at envelope `issues` | caller stderr + envelope `issues` |
| HC-11 access-permission enum violation at smoke-test (neither `c6:publishable` nor `c6:ip-private`) | halt-and-surface per BE-A §1 per-edge HC-11 enforcement contract; HC-11 partition declaration is structural; document refusal at envelope `issues` | caller stderr + envelope `issues` |
| `spec_implementation_event` fires for a spec_iri that has NO prior `spec_authoring_event` in the same JSONL sink (orphan firing) | halt-and-surface per BE-E ordering invariant (authoring precedes implementation by construction); orphan implementation events are evidence of write-boundary bypass per HC-BE-D-1; surface as Cycle 18 evidence | caller stderr + envelope `issues` |
| KT-5 FIRES (≥2 NEW Cycle-16-authored dormant-silent specs at BE-E close evaluation) | halt-and-surface per HC #59 BINDING screen + §3.5 3-test pre-escalation gate per kc-46 PD §3.5; if all 3 confirm paradigm-class, halt + executive-format surface to Rex (≤200 words per Pattern 14 + HC #43); do NOT proceed to §13 BE-E appends or commit | envelope `status: blocked` + paradigm escalation candidate |

DP#44 BINDING on FAIL → halt-and-surface; do NOT route around with §11/§12/§13 override addendum or Coach-direct edit of LOCKED canonicals or gate scripts (per substrate §8 refusal anchor 4 + Binding 7 + S155).

---

## §6 HC-11 partition (per BE-A §1 + Binding 8 BIND across wrapper)

**PUBLISHABLE (`c6:publishable`) — this document, in full + the 2 NEW event class schemas + sink-path convention + namespace + ≤3-session dormancy threshold semantic + session-close + cycle-close hook interface + KT-5 SPARQL evaluation query + refusal-on-violation taxonomy + 4-repo paired commit precedent extension to Cycle 16 BE-E + govML v2.8.5 ADDITIVE-APPEND framing + 14-field schema reflection at smoke-test PROV-O typed-edges.**

**IP-PRIVATE (`c6:ip-private`) — referenced not inlined per Binding 8 BIND + HC-11 partition + BUILD_DECISION_LOG §7 verbatim:** per-host enforcement routing internal implementation; agent-prompt details (kernel-coach + build-runner + impl-coach internal task contexts that fire `spec_authoring_event` via BE-B wrapper); per-spec evidence trail at JSONL row content (specific spec_iri values; per-row provenance authority chain internals); session-close + cycle-close internal aggregation algorithm bodies; per-role checklist contents at `~/ml-governance-templates/checklists/*.checklist`.

Per-edge HC-11 annotation per BE-A §1-§3 LOCKED at every NEW materialization (smoke-test specs + `forward_apply_observation_events.jsonl` row content). The 2 NEW event classes carry `payload.access_permission` field as structural enforcement of per-edge HC-11 annotation; SHACL shape inherits BE-A SpecShape constraint (`sh:in (c6:publishable c6:ip-private)`).

---

## §7 Self-test (BEFORE shipping the BE-E artifact stack)

| # | Check | Status |
|---|---|---|
| 1 | `outputs/forward_apply_observation_events.jsonl` sink exists (empty at scaffold; refuse-on-violation per RUNTIME_EMIT_SPEC §3 if absent at first emit) | [x] PASS — sink created at BE-E build step 4 via `touch` before first smoke emit |
| 2 | 2 NEW event classes declared with trigger + required fields per §1 (`spec_authoring_event` + `spec_implementation_event`) | [x] PASS — schema documented at §1; matches RUNTIME_EMIT_SPEC §13.1 BE-E append schema; smoke-test fires both classes against synthetic specs |
| 3 | Refusal-on-violation wired for 6 failure modes per §5 (sink-unwritable + SHACL refuses + PROV-O missing + HC-11 enum violation + orphan implementation event + KT-5 fires) | [x] PASS — all 6 modes documented with refusal behavior + surface destination |
| 4 | HC-11 partition declared per §6 (publishable interface + IP-private internals per Binding 8) | [x] PASS — per-edge HC-11 annotation structural at `payload.access_permission` field; SHACL inherits BE-A `SpecShape` enum constraint |
| 5 | Smoke-test ≥4 events fired against synthetic specs (TB-1 + TB-2; each emits 1 `spec_authoring_event` + 1 `spec_implementation_event` for total ≥4) at `outputs/forward_apply_observation_events.jsonl` | [x] PASS — verified at BE-E smoke-test step 4 per dispatch substrate §1 item 3; DROP GRAPH cleanup on test graph `<http://cycle16.local/test/be_e_smoke>` at smoke-test close (canonical production registry rows persist) |
| 6 | PROV-O 4-typed-edges (`wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy`) per-spec verified at smoke-test via SPARQL DESCRIBE against test graph | [x] PASS — DESCRIBE returns 4-typed-edge graph per smoke-test spec; Cycle 6 BE#1 contract inherited |
| 7 | KT-5 firing surface evaluated at BE-E close per §4 + dispatch substrate §5 + task context Step 7 (count + verdict + window adequacy honest note) | [x] PASS — KT-5 evaluation query executed at BE-E close; verdict recorded at envelope `kt_5_evaluation` block; honest gap on mid-Cycle-16 observation window adequacy surfaced |

---

End of forward_apply_observation_protocol.md. Cycle-16-S7 Stage 5 BE-E forward-apply observation infrastructure. Build-Runner foreground via Agent tool `subagent_type=general-purpose`. Architecture-1 §2 seed+Edit. HC #34 cap ≤20,000B decimal. NEVER `run_in_background`. Per dispatch substrate §1 item 2.
