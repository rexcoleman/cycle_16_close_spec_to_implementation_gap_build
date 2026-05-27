# DEPLOYMENT LOG

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
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §5 for promotion authority and rollback procedure
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §1 for thresholds the promotion gate consults

**Downstream (depends on this contract):**
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §3 for cross-test-bed deployment evidence
- See [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §1 for the decisions recorded at each promotion event

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{ARTIFACT_NAME}}` | Artifact whose deployment is logged | `signal-pipeline-v1` |
| `{{DEPLOY_TARGET}}` | Runtime target deployed to | `azure-vm-7gb`, `mac-mini-m4-pro-48gb` |
| `{{PROMOTION_AUTHORITY}}` | Operator/agent role that authorizes promotion | `<orchestrator-role> + <builder-role>; <upper-tier-operator> on KILL fire` |

> Delete this section once the contract is filled.

---

## §0 Deployment Identity

<!-- gate:deployment_log §0 required -->

| Field | Value |
|---|---|
| **Artifact** | {{ARTIFACT_NAME}} |
| **Test bed** | {{TEST_BED_ID}} |
| **Deploy target** | {{DEPLOY_TARGET}} |
| **First promotion commit** | {{LOCK_COMMIT}} |
| **Promotion authority** | {{PROMOTION_AUTHORITY}} |

<!-- /gate:deployment_log §0 -->

---

## §1 Promotion Gate Stack

<!-- gate:deployment_log §1 entries:1 -->

The promotion gate stack runs in declared order at every promotion attempt.
A FAIL on any gate halts promotion; the artifact stays at its prior
production version until the gate PASSes (or a CONTRACT_CHANGE adjusts the gate).

| # | Gate name | Gate script (path) | What it checks | FAIL behavior |
|---|---|---|---|---|
| 1 | {{GATE_NAME}} | {{path/to/build_*_gate.sh}} | {{which contract row(s) it verifies}} | {{halt-promotion / advisory-warn / refuse-and-rollback}} |

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
| 1 | {{ISO_TIMESTAMP}} | {{COMMIT_HASH}} | PASS / FAIL_AT_GATE_<N> | PROMOTED / HELD / ROLLED_BACK | {{OPERATOR}} | {{1-line note or evidence link}} |

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
| {{TEST_BED_1}} | {{CYCLE_N}} | PROMOTED / HELD | {{wall-clock or session count}} | PASS / FAIL / FAILS-WITH-DIAGNOSED-SHAPE | {{CROSS_SYSTEM_VALIDATION row}} |

<!-- /gate:deployment_log §3 -->

> [SEED: min_test_beds=3]
> Until n≥3 test beds have at least PROMOTED+ACCEPTED verdict, the artifact's
> deployment story is INCONCLUSIVE at the program level (single-test-bed
> success is INCONCLUSIVE evidence per the build-class evidence grammar).

---

## §4 Rollback Procedure (referenced from ARTIFACT_CONTRACT §5)

| Step | Command / hook | Expected outcome | Verification |
|---|---|---|---|
| 1 | {{ROLLBACK_STEP_1}} | {{OUTCOME}} | {{HOW_VERIFIED}} |
| 2 | {{ROLLBACK_STEP_2}} | {{OUTCOME}} | {{HOW_VERIFIED}} |

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
| 1 | §1 promotion gate stack lists ≥1 gate with a script path that exists and is executable | [ ] |
| 2 | §1 gates resolve to load-bearing rows of [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) and [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) (not "advisory only") | [ ] |
| 3 | §4 rollback was executed end-to-end on a non-production target with VERIFIED column populated | [ ] |
| 4 | §3 per-test-bed roll-up has rows pre-allocated for each ROADMAP-committed test bed (rows MAY be empty awaiting promotion) | [ ] |
| 5 | §0 promotion authority is a named role/operator (not "TBD") | [ ] |

> If any check is `[ ]`, halt-and-surface; do NOT promote.
