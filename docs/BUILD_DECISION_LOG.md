# BUILD DECISION LOG

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
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §6 for change-control triggers that must emit decisions here
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §4 for failure-shape diagnoses that emit decisions here
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §5 for promotion-FAIL diagnoses that emit decisions here
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §4 for negative-result decisions

> The build-class decision log is the cross-cutting append-only ledger
> for every load-bearing decision the build cycle makes. ARTIFACT_CONTRACT
> changes, ACCEPTANCE_CRITERIA verdicts with FAIL/FAILS-WITH-DIAGNOSED-SHAPE,
> DEPLOYMENT_LOG promotions/rollbacks, and CROSS_SYSTEM_VALIDATION refute-import
> rows ALL emit a row here.

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{ARTIFACT_NAME}}` | Artifact this log is scoped to | `signal-pipeline-v1` |
| `{{DECISION_OWNER}}` | Default decision owner role | `<orchestrator-role> + <builder-role>; <upper-tier-operator> on KILL fire` |
| `{{CYCLE_ID}}` | Research-build cycle this log scopes to | `Cycle 14` |
| `{{DATE}}` / `{{ISO_TIMESTAMP}}` | Timestamps in cycle close + per-row events | `2026-05-24` / `2026-05-24T14:00:00Z` |

> **§N.4 Architectural-Choice subsections (recommended).** When Build-Runner faces ≥2 candidate architectures for a build event (e.g., additive-edit vs new-layered-file; imported-library vs reference-by-shim; ClassDef.body walk vs ast.walk traversal), append `### §N.4 Architectural-Choice` to the event-§N block recording (a) candidates ≥2 enumerated, (b) selected choice + verbatim rationale, (c) reversibility (LOW / MODERATE / HIGH), (d) backwards-compat evidence. Precedents: **Cycle-14-S8 BE#6** (additive-edit vs new-layered rubric file — chose additive; LOW reversibility; backwards-compat preserved by extending existing rubric rather than introducing parallel-file class) + **Cycle-14-S9 ARCH** (imported-library + reference-by-shim vs file-copy duplication — chose imported-library at govML; MODERATE reversibility; per-project reproducibility preserved via `governance.yaml.govml_lock_commit`). Per Cycle-14-S10 substrate §2 Item 6: this §N.4 pattern is methodology back-ported to govML at template-class scope (no new gate; verification = read Customization Guide post-edit; pattern lives in this template for forward-cycle Build-Runner consumption).
>
> Delete this section once the contract is filled.

---

## §0 Log Identity

<!-- gate:build_decision_log §0 required -->

| Field | Value |
|---|---|
| **Artifact** | {{ARTIFACT_NAME}} |
| **Cycle** | {{CYCLE_ID}} |
| **Default decision owner** | {{DECISION_OWNER}} |
| **Append-only** | YES (edits are forbidden; corrections emit new rows with `supersedes` ref) |

<!-- /gate:build_decision_log §0 -->

---

## §1 Promotion Decisions (mirror [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 with rationale)

<!-- gate:build_decision_log §1 entries:1 -->

| # | Timestamp | Decision | Rationale (1-3 sentences) | Owner | Evidence link | Supersedes |
|---|---|---|---|---|---|---|
| 1 | {{ISO_TIMESTAMP}} | PROMOTE / HOLD / ROLLBACK / DEFER / KILL | {{rationale}} | {{OWNER}} | {{path / event_id}} | {{prior decision row N or N/A}} |

<!-- /gate:build_decision_log §1 -->

> Each promotion decision in [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2
> emits a corresponding row here with rationale. The DEPLOYMENT_LOG row
> is the *event*; this row is the *reasoning*. They are kept in two
> places to honor append-only discipline at both the deployment surface
> and the decision surface.

---

## §2 Acceptance-Verdict Decisions

<!-- gate:build_decision_log §2 entries:1 -->

For every ACCEPTANCE_CRITERIA threshold that emits FAIL or FAILS-WITH-DIAGNOSED-SHAPE,
record the disposition decision.

| # | Threshold (link to [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §1 row) | Verdict | Failure shape (from §4 grid) | Decision | Owner | Evidence link |
|---|---|---|---|---|---|---|
| 1 | {{ACCEPTANCE_ROW}} | FAIL / FAILS-WITH-DIAGNOSED-SHAPE | {{shape}} | TIGHTEN_CONTRACT / RE-RUN_WITH_PRECONDITION / REFUTE_IMPORT / FAILS-WITH-DIAGNOSED-SHAPE_RECORDED / KILL | {{OWNER}} | {{evidence link}} |

<!-- /gate:build_decision_log §2 -->

> Forbidden decision shape: "loosen the threshold." Per [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §4
> diagnostic grid, a FAIL is *diagnosed*, not relaxed. If the threshold
> was wrong by construction, that is itself a finding (record as
> CONTRACT_CHANGE; recompute baseline; do NOT silently slide the threshold).

---

## §3 Cross-System-Validation Decisions

<!-- gate:build_decision_log §3 entries:1 -->

For every CROSS_SYSTEM_VALIDATION result that produces a refute-import or
boundary-condition decision.

| # | Primitive (link to [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §3 row) | Cross-bed verdict | Decision | Rationale | Evidence link |
|---|---|---|---|---|---|
| 1 | {{PRIMITIVE_LINK}} | YES / PARTIAL / NO across {{n}} test beds | LOAD_BEARING / BOUNDARY_CONDITIONED / REFUTED / DEFERRED_TO_NEXT_CYCLE | {{rationale}} | {{evidence link}} |

<!-- /gate:build_decision_log §3 -->

---

## §4 Contract-Change Decisions

<!-- gate:build_decision_log §4 entries:0 -->

For every CONTRACT_CHANGE that updates [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §1-§6
or other build-class contract surfaces.

| # | Timestamp | Contract section changed | Old → New | Rationale | Authority | Commit hash |
|---|---|---|---|---|---|---|
| 1 | {{ISO_TIMESTAMP}} | {{ARTIFACT_CONTRACT §N row M}} | {{old}} → {{new}} | {{rationale}} | {{authority chain}} | {{commit}} |

<!-- /gate:build_decision_log §4 -->

> CONTRACT_CHANGE decisions REQUIRE a Tier 1 authority reference (per
> Authority Hierarchy at top). Operator-direct or sub-tier CONTRACT_CHANGE
> without Tier 1 authority is forbidden (the strict-process-rail discipline:
> no override addenda; no operator-direct edit of canonical templates to
> make a gate pass; applies symmetrically to build-class).

---

## §5 KILL-Trigger Decisions

When a build-class KILL trigger fires (artifact contract drift; baseline
instability >threshold; cross-system mechanism refute; scope creep beyond
cycle envelope), record the KILL decision and disposition.

| # | KILL trigger | Fired at | Disposition | Surface (where halt was reported) | Upper-tier paradigm ruling required? |
|---|---|---|---|---|---|
| 1 | {{TRIGGER_NAME}} | {{ISO_TIMESTAMP}} | HALT-AND-SURFACE / RE-RUN-WITH-CORRECTION / DEFER-TO-NEXT-CYCLE | {{stderr / state.json / DLQ}} | YES / NO |

> KILL triggers fire structurally; routing-around via operator-direct edit
> of the gate or canonical artifact to make the trigger PASS is forbidden
> (the strict-process-rail discipline binds symmetrically to build-class).
> On any KILL fire requiring upper-tier paradigm ruling, halt-and-surface;
> do NOT auto-route.

---

## §6 Self-test (BEFORE classifying decision log as COMPLETE for cycle close)

| # | Check | Status |
|---|---|---|
| 1 | Every [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 row has a corresponding §1 decision row with rationale | [ ] |
| 2 | Every [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §5 FAIL or FAILS-WITH-DIAGNOSED-SHAPE row has a §2 decision row | [ ] |
| 3 | Every [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §3 PARTIAL or NO row has a §3 decision row | [ ] |
| 4 | Every CONTRACT_CHANGE in the cycle commits has a §4 row referencing the commit hash | [ ] |
| 5 | Every KILL trigger fire has a §5 row with disposition (no silent KILL) | [ ] |
| 6 | All rows have non-`{{PLACEHOLDER}}` evidence links (or explicit "no evidence; deferred" with justification) | [ ] |

> If any check is `[ ]`, halt-and-surface; do NOT close the cycle.

---

## §7 Pre-check Interface (for build-class agent specs)

<!-- gate:build_decision_log §7 advisory -->

Build-class agent specs invoke a pre-execution checklist before primary task
execution (extends F-C composition from RIDE: checklist-with-refusal-authority,
PASS/FAIL/WARN per item). The interface contract is publishable; the checklist
contents and runner orchestration internals are pipeline IP and live at internal
paths NOT inlined here.

| Field | Value |
|---|---|
| **Pre-check ID** | `{{pre_check_id}}` |
| **Invocation** | `{{path/to/agent_pre_check_runner.sh --role <role> --project-dir <project_dir>}}` |
| **Refusal authority** | Refuse-on-missing-precondition: any FAIL-level item halts primary execution with explicit callout |
| **Mode** | BLOCKING (default) or `--advisory-mode` (WARN-only; PASS-through) |
| **Checklist contents** | (pipeline IP — referenced not inlined; lives at internal-only path) |
| **Runner orchestration internals** | (pipeline IP — referenced not inlined) |

<!-- /gate:build_decision_log §7 -->

> The interface (pre-check ID, invocation, refusal authority, mode) is
> publishable build-class methodology. The checklist contents and runner
> orchestration are pipeline-private IP (publishable-vs-private partition); a separate internal
> agent-spec for build-class is dispositioned at the next build-class cycle
> bootstrap, NOT inlined into this template.
