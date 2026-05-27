# CROSS SYSTEM VALIDATION

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
- See [RUNTIME_EMIT_SPEC](RUNTIME_EMIT_SPEC.tmpl.md) §1 for per-test-bed event schemas this validation aggregates
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §3 for the n≥3 strengthening requirement
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §3 for per-test-bed deployment roll-up

**Downstream (depends on this contract):**
- See [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §3 for cross-test-bed decisions resolved against validation evidence

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{ARTIFACT_NAME}}` | Artifact under cross-system validation | `signal-pipeline-v1` |
| `{{PRIMITIVE_CLASS}}` | Engineering primitive class measured (A-E from LANDSCAPE) | `closed-loop runtime catch` |
| `{{TEST_BED_LIST}}` | Test beds the validation runs across | `TB-1, TB-2, TB-3` |
| `{{CATCH_THRESHOLD}}` | Per-test-bed catch threshold | `≥1 catch per primitive class per test bed under cross-domain test` |

> Delete this section once the contract is filled.

---

## §0 Validation Identity

<!-- gate:cross_system_validation §0 required -->

| Field | Value |
|---|---|
| **Artifact** | {{ARTIFACT_NAME}} |
| **Test beds in scope** | {{TEST_BED_LIST}} |
| **Primitive classes measured** | {{PRIMITIVE_CLASS}} |
| **Cross-domain catch threshold** | {{CATCH_THRESHOLD}} |
| **Pre-registration commit** | {{LOCK_COMMIT}} |

<!-- /gate:cross_system_validation §0 -->

> Cross-system-validation is the build-class equivalent of n≥3
> generalization evidence. Its job is to surface whether the engineering
> primitive (closed-loop runtime catch / refusal-authority interface /
> calibration-as-CI / runtime-emit shape) holds at multiple test beds OR
> exhibits a per-test-bed boundary condition that the per-discipline
> falsification threshold catches.

---

## §1 Per-Test-Bed Catch Inventory

<!-- gate:cross_system_validation §1 entries:3 -->

For each test bed in scope, inventory the catches the artifact produced.

| Test bed | Cycle | Primitive class | Catch description | Real-vs-intentional-fire | Repair shape distribution (PATH A/B/C/D) | Evidence link |
|---|---|---|---|---|---|---|
| {{TEST_BED_1}} | {{CYCLE_N}} | {{PRIMITIVE_CLASS}} | {{1-line description}} | {{REAL / INTENTIONAL}} | {{PATH_A: N / PATH_B: N / PATH_C: N / PATH_D: N}} | {{event_id or runtime-emit ref}} |
| {{TEST_BED_2}} | {{CYCLE_N+1}} | {{PRIMITIVE_CLASS}} | {{...}} | {{...}} | {{...}} | {{...}} |
| {{TEST_BED_3}} | {{CYCLE_N+2}} | {{PRIMITIVE_CLASS}} | {{...}} | {{...}} | {{...}} | {{...}} |

<!-- /gate:cross_system_validation §1 -->

> [SEED: min_test_beds=3, min_real_catches_per_bed=1]
> The catch threshold is "≥1 catch per primitive class per test bed under
> cross-domain test, where each catch is REAL (not intentional fire)."
> Intentional-fire catches (where the artifact catches a fault the operator
> deliberately injected as a smoke test) do NOT count toward the threshold.
> Real catches are catches the operator did NOT plan in advance.

---

## §2 Boundary-Condition Map

<!-- gate:cross_system_validation §2 required -->

When per-test-bed catches diverge (one bed PASSES, another FAILs, a third
FAILS-WITH-DIAGNOSED-SHAPE), document the boundary condition that explains
the divergence. Boundary conditions are the build-class deliverable of
cross-system-validation; "the primitive transferred cleanly" is rare.

| Boundary condition | Test beds where condition triggers | Predicted-or-discovered | Disposition |
|---|---|---|---|
| {{BOUNDARY_CONDITION}} | {{TEST_BED_LIST}} | PREDICTED at design / DISCOVERED at deployment | {{tightening artifact contract / partition primitive class / refute import}} |

<!-- /gate:cross_system_validation §2 -->

> [SEED: boundary-condition-map richness over clean H-vs-B disposition]
> Per Cycle 1 paradigm framework: HYBRID with explicit boundary conditions
> per discipline AND per failure mode is the PRIMARY EXPECTED outcome shape,
> NOT fallback. Cross-system-validation that produces a rich boundary-condition
> map is more valuable than a binary "transfer / no-transfer" verdict.

---

## §3 Cross-Domain Mechanism Test (n≥3 strengthening)

<!-- gate:cross_system_validation §3 entries:1 -->

For each engineering primitive imported from external discipline (per
LANDSCAPE_ASSESSMENT §6b method-import-opportunities), test mechanism
transfer at n≥3 test beds.

| Primitive (source domain → target) | TB-1 mechanism transfer? | TB-2 mechanism transfer? | TB-3 mechanism transfer? | Boundary | Refuted? |
|---|---|---|---|---|---|
| {{PRIMITIVE_NAME}} (e.g., jidoka closed-loop runtime → agent stage runtime) | {{YES / PARTIAL / NO}} | {{YES / PARTIAL / NO}} | {{YES / PARTIAL / NO}} | {{BOUNDARY_LINK}} | {{YES (refute import) / NO (boundary-condition only)}} |

<!-- /gate:cross_system_validation §3 -->

> Mechanism transfer is the load-bearing signal: the primitive *operates the
> same way* in the target domain. PARTIAL is a valid (and often expected)
> outcome — record the boundary explicitly. NO triggers a refute-the-import
> path, recorded in [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §3.

---

## §4 Honest Negative Result Discipline

When cross-system-validation produces a negative result (the primitive does
not transfer; the artifact's contract holds at one bed but breaks at another),
the negative result is a valid build-class deliverable. Document per this
shape:

| Field | Value |
|---|---|
| **Negative result** | {{1-line description: which primitive, which bed(s), what failed}} |
| **Disposition** | {{refute import / partition primitive class / introduce new primitive class}} |
| **Pre-emptive criticism (1 sentence)** | {{the strongest reading of "this is just an artifact-defect, not a primitive-failure" — addressed honestly}} |
| **Recorded at** | [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §3 row {{N}} |

> Negative results are publishable per build-class evidence grammar.
> "Artifact ships and meets contract OR fails-with-diagnosed-shape" — the
> latter clause is half the contract.

---

## §5 Self-test (BEFORE classifying validation as COMPLETE)

| # | Check | Status |
|---|---|---|
| 1 | §1 catch inventory has rows for ≥3 test beds | [ ] |
| 2 | Each §1 catch is classified REAL or INTENTIONAL (not "TBD") | [ ] |
| 3 | §2 boundary-condition map has ≥1 entry OR explicit "no boundary observed" with evidence link | [ ] |
| 4 | §3 per-primitive mechanism transfer column is filled across all n≥3 test beds (not partial fill) | [ ] |
| 5 | If any §3 column is "NO", a refute-import row exists in [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) | [ ] |
| 6 | §4 negative-result discipline applied to any FAIL or PARTIAL transfer (not skipped) | [ ] |

> If any check is `[ ]`, the cross-system-validation is INCONCLUSIVE; do NOT
> classify primitive as load-bearing.
