# {{ARTIFACT_NAME}} Blindspot Register ({{CYCLE_ID}} §K BINDING)

<!-- version: 0.1 -->
<!-- created: {{DATE}} -->
<!-- profile: build -->
<!-- methodology_status: skeleton — back-ported from Cycle 13 `~/cycle_13_build_cycle_shift_left_build/docs/be1_blindspot_register.md` 1,461L canonical per Cycle-14-S10 substrate §2 Item 3 -->

> **Authority Hierarchy**
>
> | Priority | Document | Role |
> |----------|----------|------|
> | Tier 1 | `{{TIER1_DOC}}` | Primary spec — highest authority |
> | Tier 2 | `{{TIER2_DOC}}` | Clarifications — cannot override Tier 1 |
> | Tier 3 | `{{TIER3_DOC}}` | Advisory only — non-binding if inconsistent with Tier 1/2 |
> | K register | This document | Cumulative cross-BE blindspot ledger — append-only |

### Companion Contracts

**Upstream (this register depends on):**
- See [HYPOTHESIS_REGISTRY](../HYPOTHESIS_REGISTRY.tmpl.md) §3 for H-class hypotheses whose disconfirmation patterns this register absorbs
- See [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §4 for CONTRACT_CHANGE rows tied to K-register sections
- See [KNOWN_BOUNDARIES](KNOWN_BOUNDARIES.tmpl.md) §N for NOT-applies dispositions of K-register surfaces

> The K register is the **cumulative cross-BE blindspot ledger** for a build-
> class research cycle. Every H disconfirmation pattern, RED team finding,
> T12 bounded-evidence carry, and cross-BE pattern count lands here with
> verbatim source cite + per-row lock_commit. Per ADR-Cycle-13-S3 (c)
> bounded-evidence inheritance pattern: evidence claims MUST cite verbatim
> source (rubric file+line OR JSONL aggregate cite) for DP#43 paired
> structural+content verification.

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{ARTIFACT_NAME}}` | Artifact this register is scoped to (BE# or cycle) | `BE#1` / `Cycle 13` |
| `{{CYCLE_ID}}` | Cycle this register lives in | `Cycle 14` |
| `{{DATE}}` | Register-creation date (ISO-8601) | `2026-05-24` |
| `{{BE_ID}}` | Specific BE (build-event) this section scopes to | `BE#5` |
| `{{PATTERN_TITLE}}` | One-line title of disconfirmation pattern | `@dataclass field annotations invisible to FunctionDef AST inspection` |
| `{{HIGH_MEDIUM_LOW}}` | Severity classification | `HIGH` |
| `{{TYPE_A_B}}` | Type A (defect-in-rubric) vs Type B (out-of-scope-but-honest) | `Type A` |
| `{{K_SECTION_CITE}}` | §X.Y.Z cross-reference | `§10.1.2` |
| `{{LOCK_COMMIT}}` | git lock_commit for this row's evidence | `d8512b8` |

> Delete this section once the register is filled.

---

## §N.1 H disconfirmation patterns (per H-class hypothesis)

<!-- gate:k_register §N.1 required -->

For each H-class hypothesis disconfirmed during the build cycle, register the
disconfirmation pattern with verbatim source cite + recommended closure
mechanism.

### §N.1.M {{PATTERN_TITLE}} (H{{HYP_NUM}}-retro {{FALSIFY|CONFIRM}} direct cause; {{HIGH_MEDIUM_LOW}} priority per LA §6b.1 Gap N)

**Pattern (verbatim source cite):** {{verbatim quote from rubric file:line OR retroactive simulation evidence}}

**Why uncovered (mechanism level):** {{mechanism-discipline anchor — name the AST node class / regex grammar / call-site shape that the rubric did NOT cover}}

**Disposition:** CONTRACT_CHANGE candidate / BOUNDARY-DOCUMENTED / RT-class patch (RT-N at §N.2)

**Recommended closure mechanism:** {{e.g., "extend ClassDef walker to traverse AnnAssign field declarations via strategy (iii)"}}

**K register cite:** §N.1.M (this row) → cross-references to §N.2 RT-class patch + §N.3 T12 bounded-evidence carry as applicable.

**Authority:** {{verbatim authority chain — SI L-line + ADR section + lock_commit}}

<!-- /gate:k_register §N.1 -->

---

## §N.2 RED team findings (per BE close batch)

<!-- gate:k_register §N.2 required -->

For each RED team attempt that surfaces a Type A defect at the patched rubric,
register the finding with severity + Type-A/B classification + patched-at
lock_commit.

| # | Attempt | Pattern | Severity | Type | Patched-at lock_commit | K § cite |
|---|---|---|---|---|---|---|
| 1 | `attempt_{{N}}` | {{1-line pattern}} | HIGH / MEDIUM / LOW | Type A / Type B | `{{lock_commit}}` | `{{K_SECTION_CITE}}` |

<!-- /gate:k_register §N.2 -->

> **HC-11 partition.** Probe corpora (the actual attack-fixture content) live at
> pipeline-private paths (e.g., `red_team_evidence/`); this register cites
> attempt IDs + verdicts + patch-attribution ONLY, not probe content.

---

## §N.3 T12 bounded-evidence inheritance (per ADR-Cycle-13-S3 (c))

<!-- gate:k_register §N.3 required -->

For each H-class finding whose evidence is bounded to a specific apparatus +
fixture scope per ADR-Cycle-13-S3 (c) bounded-evidence inheritance pattern,
register the bounded-evidence cite + scope limitation + forward-carry
disposition.

| # | Finding | Apparatus + fixture scope | Bounded evidence (verbatim cite) | Forward-carry (Cycle N+M scope) |
|---|---|---|---|---|
| 1 | {{H-class finding}} | `{{apparatus_path}}` + `{{fixture_class}}` | {{rubric file:line OR JSONL aggregate cite}} | {{Cycle N+M enforcement-layer disposition}} |

<!-- /gate:k_register §N.3 -->

> Per ADR-Cycle-13-S3 (c) bounded-evidence inheritance: a finding at one
> apparatus/fixture scope is NOT automatically claimed at all build-class
> apparatuses. Cross-substrate generalization requires explicit cross-bed
> validation (see [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §3).

---

## §N.4 Cumulative cross-BE count (running total + per-BE close lock_commit)

<!-- gate:k_register §N.4 required -->

| # | BE | Cumulative blindspots | New this BE | Patched this BE | Carried forward | Close lock_commit |
|---|---|---|---|---|---|---|
| 1 | {{BE_ID}} | {{cumulative_n}} | {{new_n}} | {{patched_n}} | {{carried_n}} | `{{lock_commit}}` |

<!-- /gate:k_register §N.4 -->

> The cumulative cross-BE count is the structural signal that the build
> cycle is **learning** at the per-BE rate predicted by ADR-Cycle-13-S3 (c).
> If `new_n` stays elevated across BEs without convergence, that is itself a
> finding — surface to BUILD_DECISION_LOG §5 as a KILL-trigger candidate
> (mechanism-non-transfer per ACCEPTANCE_CRITERIA §4 grid).

---

## §N.5 Self-test (BEFORE classifying register as COMPLETE for cycle close)

| # | Check | Status |
|---|---|---|
| 1 | Every §N.1 pattern row has verbatim source cite (no `{{PLACEHOLDER}}`) | [ ] |
| 2 | Every §N.2 RED team row has attempt ID + patched-at lock_commit | [ ] |
| 3 | Every §N.3 T12 row has bounded apparatus + fixture scope cite | [ ] |
| 4 | Every §N.4 cumulative row has close lock_commit | [ ] |
| 5 | HC-11 partition respected: no probe corpora content republished here | [ ] |
| 6 | All authority anchors resolve (SI line + ADR section + lock_commit) | [ ] |

> If any check is `[ ]`, halt-and-surface; do NOT close the BE.
