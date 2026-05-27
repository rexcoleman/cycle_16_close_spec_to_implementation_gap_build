# ARTIFACT CONTRACT

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
>
> **Conflict rule:** When a higher-tier document and this contract disagree, the higher tier wins.
> Update this contract via `CONTRACT_CHANGE` or align implementation to the higher tier.

### Companion Contracts

**Upstream (this contract depends on):**
- See [ENVIRONMENT_CONTRACT](../core/ENVIRONMENT_CONTRACT.tmpl.md) §8 for determinism and runtime defaults
- See [DATA_CONTRACT](../core/DATA_CONTRACT.tmpl.md) §3 for input data contracts (when build consumes data)

**Downstream (depends on this contract):**
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §1 for the pass/fail thresholds this contract is measured against
- See [RUNTIME_EMIT_SPEC](RUNTIME_EMIT_SPEC.tmpl.md) §2 for the structured-emit shape this artifact MUST produce
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §1 for promotion gates this contract is verified at
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §1 for cross-system-validation event surfaces

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{ARTIFACT_NAME}}` | Name of the build artifact | `signal-pipeline-v1` |
| `{{ARTIFACT_KIND}}` | Service / library / pipeline / cli / agent-spec | `cli` |
| `{{INVOCATION_INTERFACE}}` | How consumers invoke the artifact | `python -m signal_pipeline poll <source>` |
| `{{RUNTIME_TARGETS}}` | Runtime environments the artifact ships to | `azure-vm-7gb`, `mac-mini-m4-pro-48gb` |
| `{{CONTRACT_OWNER}}` | Operator or agent role responsible for contract upkeep | `<role-name>` |
| `{{TIER1_DOC}}` | Tier 1 authority document | `PROJECT.md §Acceptance` |
| `{{TIER2_DOC}}` | Tier 2 authority document | `EXPERIMENTAL_DESIGN.md §4a` |
| `{{TIER3_DOC}}` | Tier 3 authority document | `external standards reference` |

> Delete this section once the contract is filled.

---

## §0 Artifact Identity

<!-- gate:artifact_contract §0 required -->

| Field | Value |
|---|---|
| **Artifact name** | {{ARTIFACT_NAME}} |
| **Artifact kind** | {{ARTIFACT_KIND}} |
| **Repository path** | {{REPO_PATH}} |
| **Lock commit** | {{LOCK_COMMIT}} |
| **Build cycle** | {{CYCLE_ID}} |
| **Test bed binding** | {{TEST_BED_ID}} |
| **Contract owner** | {{CONTRACT_OWNER}} |

<!-- /gate:artifact_contract §0 -->

> The artifact identity row is the structural index every downstream gate
> resolves against. If any field is `{{PLACEHOLDER}}` or `TBD` at the
> production-deployment gate, the gate FAILs by construction.

---

## §1 Pre-conditions

<!-- gate:artifact_contract §1 entries:1 -->

State the conditions that MUST hold before this artifact runs. Pre-conditions
are checked structurally at invocation; a failed pre-condition refuses the run
(per design-by-contract; Hoare/Meyer pattern).

| # | Pre-condition | How verified at runtime | Refusal behavior on FAIL |
|---|---|---|---|
| 1 | {{PRECONDITION}} | {{VERIFICATION_HOOK}} | {{REFUSAL_BEHAVIOR}} |

<!-- /gate:artifact_contract §1 -->

> [SEED: min_preconditions=1]
> Pre-conditions are NOT defensive null checks — they are the contract
> the consumer commits to before invocation. Examples: "input file exists at
> path X with schema Y", "auth token is non-empty and valid for scope Z",
> "upstream artifact A is at lock commit B".

---

## §2 Post-conditions

<!-- gate:artifact_contract §2 entries:1 -->

State the conditions the artifact GUARANTEES on successful completion. Post-conditions
are what consumers depend on; ACCEPTANCE_CRITERIA tests them.

| # | Post-condition | How verified after run | What CROSS_SYSTEM_VALIDATION measures against |
|---|---|---|---|
| 1 | {{POSTCONDITION}} | {{VERIFICATION_HOOK}} | {{CROSS_SYSTEM_LINK}} |

<!-- /gate:artifact_contract §2 -->

> [SEED: min_postconditions=1]
> Post-conditions are the artifact's outward-facing promise. They are what
> downstream consumers wire against. A post-condition that cannot be verified
> by inspection of the artifact's output (or runtime-emit) is not a contract;
> it is a wish.

---

## §3 Invariants

<!-- gate:artifact_contract §3 entries:1 -->

State the invariants the artifact preserves across its lifecycle (between
invocations, across versions, across deployment targets).

| # | Invariant | When checked | If violated |
|---|---|---|---|
| 1 | {{INVARIANT}} | {{CHECKPOINT}} | {{VIOLATION_HANDLING}} |

<!-- /gate:artifact_contract §3 -->

> Invariants distinguish a build-class artifact from a one-shot script.
> Examples: "schema X is preserved across versions ≥1.0", "output ordering
> is deterministic across runtime targets", "no side effects outside paths
> declared in §4".

---

## §4 Side Effects and Resource Footprint

| Surface | Effect | Bounds |
|---|---|---|
| Filesystem writes | {{PATHS_WRITTEN}} | {{MAX_BYTES_OR_FILES}} |
| Database writes | {{TABLES_AND_TABLES_VS_VIEWS}} | {{ROW_BOUNDS_OR_NONE}} |
| Network egress | {{HOSTS_OR_NONE}} | {{REQUEST_RATE_OR_NONE}} |
| Process / thread footprint | {{PROCESSES_OR_NONE}} | {{MAX_CONCURRENT}} |
| Energy / GPU / memory | {{RESOURCE_PROFILE}} | {{CEILING}} |

> A build-class artifact ships into production runtime; its resource
> footprint MUST be declared so cross-system-validation can measure
> against it. "It's small" is not a footprint — declare numbers.

---

## §5 Versioning and Promotion Hooks

| Field | Value |
|---|---|
| **Version scheme** | {{semver / cycle-id / commit-hash}} |
| **Promotion authority** | {{WHO_AUTHORIZES_PROMOTION}} |
| **Promotion gates** | {{GATE_LIST}} |
| **Rollback procedure** | {{ROLLBACK_HOOK}} |

> See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 for the promotion
> gate stack this artifact passes through. Rollback procedure MUST
> be tested (not just documented) before first production promotion.

---

## §6 Change Control Triggers

The following changes require a `CONTRACT_CHANGE` commit:

- Pre-conditions or post-conditions (any §1 / §2 row)
- Invariants (any §3 row)
- Side-effect surfaces (any new §4 row)
- Version scheme or promotion authority (§5)
- Runtime targets (top-of-document `{{RUNTIME_TARGETS}}`)

> **Refusal authority binding (refuse-on-missing-precondition; design-by-contract refusal pattern):** if the artifact's running
> behavior diverges from this contract WITHOUT an accompanying CONTRACT_CHANGE,
> the cross-system-validation gate FAILs structurally. Re-aligning runtime
> to contract is the only repair path; routing around the contract is forbidden.

---

## §7 Self-test (BEFORE shipping the artifact)

| # | Check | Status |
|---|---|---|
| 1 | Every §1 pre-condition has a runtime verification hook (§1 col 3) | [ ] |
| 2 | Every §2 post-condition is verifiable from artifact output OR runtime-emit | [ ] |
| 3 | Every §3 invariant has a checkpoint AND a violation-handling row | [ ] |
| 4 | §4 side effects enumerate every path/table/host the artifact touches | [ ] |
| 5 | §5 promotion gates resolve to ≥1 gate script in [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 | [ ] |
| 6 | §6 change control triggers list every load-bearing field above | [ ] |

> If any check is `[ ]` unchecked, this contract is not ready for
> ACCEPTANCE_CRITERIA verification. Halt-and-surface (per refuse-on-missing-precondition).
