# ACCEPTANCE CRITERIA

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
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §2 for post-conditions this acceptance verifies
- See [RUNTIME_EMIT_SPEC](RUNTIME_EMIT_SPEC.tmpl.md) §2 for the emitted events this acceptance reads

**Downstream (depends on this contract):**
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 for the promotion gate that consumes acceptance
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §2 for the n≥3 cross-system measurement strengthening
- See [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §2 for build-decisions that resolved against acceptance verdicts

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{ARTIFACT_NAME}}` | Name of the artifact under acceptance | `signal-pipeline-v1` |
| `{{BASELINE_REFERENCE}}` | Baseline this artifact is measured against | `pre-build manual signal-poll, n=30 sessions` |
| `{{BASELINE_METRIC_VALUE}}` | Baseline numeric value | `operator-correction rate per session = 0.42` |
| `{{ACCEPTANCE_THRESHOLD}}` | Threshold the artifact must clear | `correction rate ≤ 0.20 over 5 consecutive sessions` |
| `{{TEST_BED_ID}}` | Test bed where acceptance is evaluated | `TB-1 signal pipeline` |

> Delete this section once the contract is filled.

---

## §0 Acceptance Identity

<!-- gate:acceptance_criteria §0 required -->

| Field | Value |
|---|---|
| **Artifact under acceptance** | {{ARTIFACT_NAME}} |
| **Test bed** | {{TEST_BED_ID}} |
| **Baseline reference** | {{BASELINE_REFERENCE}} |
| **Baseline metric value** | {{BASELINE_METRIC_VALUE}} |
| **Pre-registration commit** | {{LOCK_COMMIT}} |

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
| 1 | {{POSTCONDITION_LINK}} | {{ACCEPTANCE_THRESHOLD}} | {{MEASUREMENT_WINDOW}} | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE |

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
| 1 | {{THRESHOLD_LINK}} | {{runtime-emit table / output file / cross-system event log}} | {{mean / median / count / rate}} | {{operator-blind / self-assessment-with-honesty-disclosure}} |

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
| {{TEST_BED_1}} | {{CYCLE_N}} | {{evidence shape}} | {{per-bed threshold (e.g., ≥1 catch per primitive class; PASS verdict required)}} |
| {{TEST_BED_2}} | {{CYCLE_N+1}} | {{evidence shape}} | {{per-bed threshold}} |
| {{TEST_BED_3}} | {{CYCLE_N+2}} | {{per-bed threshold}} |

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
| 1 | {{THRESHOLD_LINK}} | {{PASS / FAIL / INCONCLUSIVE / FAILS-WITH-DIAGNOSED-SHAPE}} | {{shape from §4}} | {{CYCLE_N}} | {{file path or runtime-emit ref}} |

> Resolution log is APPEND-ONLY. Verdicts are never edited; corrections
> emit new rows that supersede prior verdicts (with explicit supersede ref).

---

## §6 Self-test (BEFORE running acceptance)

| # | Check | Status |
|---|---|---|
| 1 | Every §1 threshold is deterministic count-based or numeric (no qualitative "improves") | [ ] |
| 2 | Pre-registration commit (§0) lands BEFORE artifact run for measurement | [ ] |
| 3 | Every §1 threshold maps to ≥1 [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §2 post-condition | [ ] |
| 4 | §2 measurement protocol resolves to runtime-emit OR output-file OR cross-system event log (NOT operator self-assessment alone) | [ ] |
| 5 | §3 per-test-bed strengthening commits ≥3 test beds | [ ] |
| 6 | §4 failure-shape grid is referenced (not absent) when any §1 threshold has VERDICT=FAIL | [ ] |

> If any check is `[ ]`, halt-and-surface; do NOT proceed to acceptance verdict.
