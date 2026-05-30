# DECISION LOG

<!-- version: 2.0 -->
<!-- created: 2026-02-20 -->
<!-- last_validated_against: CS_7641_Machine_Learning_OL_Report -->

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
- None — decisions may reference any contract but have no structural dependency.

**Downstream (depends on this contract):**
- See [CHANGELOG](CHANGELOG.tmpl.md) for CONTRACT_CHANGE entries triggered by decisions (cross-reference ADR IDs)
- See [RISK_REGISTER](RISK_REGISTER.tmpl.md) for risk entries mitigated by decisions
- See [IMPLEMENTATION_PLAYBOOK](IMPLEMENTATION_PLAYBOOK.tmpl.md) §5 for change control procedure referencing ADR entries

## Purpose

This log records architectural and methodological decisions for the **{{PROJECT_NAME}}** project using a lightweight ADR (Architecture Decision Record) format. Each decision captures the context, alternatives, rationale, and consequences so that future changes are informed rather than accidental.

**Relationship to CHANGELOG:** When a decision triggers a `CONTRACT_CHANGE` commit, the change MUST also be logged in CHANGELOG with a cross-reference to the ADR ID.

---

## When to Create an ADR

Create a new ADR when:
- A decision affects multiple contracts or specs
- A decision resolves an ambiguity in authority documents
- A decision involves tradeoffs that future contributors need to understand
- A `CONTRACT_CHANGE` commit is triggered by a methodological choice
- A risk mitigation strategy is selected from multiple options

Do NOT create an ADR for routine implementation choices that follow directly from a single contract requirement with no alternatives.

---

## Status Lifecycle

```
Proposed → Accepted → [Superseded by ADR-YYYY]
```

- **Proposed:** Under discussion; not yet binding.
- **Accepted:** Binding; implementation may proceed.
- **Superseded:** Replaced by a newer ADR. MUST cite the superseding ADR ID. Do NOT delete superseded entries.

---

## Decision Record Template

Copy this block for each new decision:

```markdown
## ADR-XXXX: [Short title]

- **Date:** YYYY-MM-DD
- **Status:** Proposed | Accepted | Superseded by ADR-YYYY

### Context
[Problem statement and constraints. Cite authority documents by tier and section.]

### Decision
[The chosen approach. Be specific enough that someone can implement it without ambiguity.]

### Alternatives Considered

| Option | Description | Verdict | Reason |
|--------|-------------|---------|--------|
| A (chosen) | [approach] | **Accepted** | [why best] |
| B | [approach] | Rejected | [why not] |
| C | [approach] | Rejected | [why not] |

### Rationale
[Why this approach is best given the project constraints. Cite authority documents.]

### Consequences
[Tradeoffs and risks. Reference RISK_REGISTER entries if applicable.]

### Contracts Affected

| Contract | Section | Change Required |
|----------|---------|----------------|
| [contract name] | §N | [what changes] |

### Evidence Plan

| Validation | Command / Artifact | Expected Result |
|------------|-------------------|-----------------|
| [what to verify] | [command or file path] | [pass criteria] |
```

---

## Decisions

*(Record decisions below. Number sequentially: ADR-0001, ADR-0002, etc.)*

---

## ADR-0001: [First decision title]

- **Date:** YYYY-MM-DD
- **Status:** Proposed

### Context
*(Describe the problem and constraints. Cite authority documents by tier and section.)*

### Decision
*(State the chosen approach with enough specificity to implement.)*

### Alternatives Considered

| Option | Description | Verdict | Reason |
|--------|-------------|---------|--------|
| A (chosen) | *(approach)* | **Accepted** | *(why best)* |
| B | *(approach)* | Rejected | *(why not)* |

### Rationale
*(Why this is the best choice given project constraints.)*

### Consequences
*(Tradeoffs, risks, downstream effects. Reference RISK_REGISTER entries.)*

### Contracts Affected

| Contract | Section | Change Required |
|----------|---------|----------------|
| *(contract)* | §N | *(what changes)* |

### Evidence Plan

| Validation | Command / Artifact | Expected Result |
|------------|-------------------|-----------------|
| *(what to verify)* | *(command or file)* | *(pass criteria)* |

## Landscape Gate — 2026-05-27T12:17:03Z

**Verdict:** CLEAR (11 PASS, 0 FAIL, 2 WARN)

Gate passed. Stage 0-2 complete. Next action: formulate (Stage 3).

| Check | Result |
|---|---|
| LANDSCAPE_ASSESSMENT exists | PASS |
| Search Protocol filled | PASS |
| ≥5 prior works | PASS (count: 20) |
| ≥1 gaps identified | PASS (count: 5) |
| Baseline Knowledge filled | PASS |
| Frontier Moat 3 checks | PASS (count: 3) |
| Cross-Engine Context filled | PASS |
| EDA Readiness (type unknown) | PASS |
| DB cross-check | PASS (count: 9) |
| Citation verification | WARN (count: 0) |
| Search strategy documentation | PASS (count: 4) |
| Characterization source | WARN (count: 0) |
| Placeholder residue | PASS (count: 0) |

## Landscape Gate — 2026-05-27T12:17:56Z

**Verdict:** CLEAR (11 PASS, 0 FAIL, 2 WARN)

Gate passed. Stage 0-2 complete. Next action: formulate (Stage 3).

| Check | Result |
|---|---|
| LANDSCAPE_ASSESSMENT exists | PASS |
| Search Protocol filled | PASS |
| ≥5 prior works | PASS (count: 20) |
| ≥1 gaps identified | PASS (count: 5) |
| Baseline Knowledge filled | PASS |
| Frontier Moat 3 checks | PASS (count: 3) |
| Cross-Engine Context filled | PASS |
| EDA Readiness (type unknown) | PASS |
| DB cross-check | PASS (count: 9) |
| Citation verification | WARN (count: 0) |
| Search strategy documentation | PASS (count: 4) |
| Characterization source | WARN (count: 0) |
| Placeholder residue | PASS (count: 0) |

## Landscape Gate — 2026-05-27T13:45:05Z

**Verdict:** CLEAR (11 PASS, 0 FAIL, 2 WARN)

Gate passed. Stage 0-2 complete. Next action: formulate (Stage 3).

| Check | Result |
|---|---|
| LANDSCAPE_ASSESSMENT exists | PASS |
| Search Protocol filled | PASS |
| ≥5 prior works | PASS (count: 20) |
| ≥1 gaps identified | PASS (count: 5) |
| Baseline Knowledge filled | PASS |
| Frontier Moat 3 checks | PASS (count: 3) |
| Cross-Engine Context filled | PASS |
| EDA Readiness (type unknown) | PASS |
| DB cross-check | PASS (count: 9) |
| Citation verification | WARN (count: 0) |
| Search strategy documentation | PASS (count: 4) |
| Characterization source | WARN (count: 0) |
| Placeholder residue | PASS (count: 0) |

---

## ADR-S12-1-KILL: Retract obsolete BE-G dogfood spec (Cycle-16-S12 kill_spec() dogfood)

- **Date:** 2026-05-28
- **Status:** Accepted

### Context
BE-G Done #18 ships `kill_spec(spec_iri, adr_retraction_ref, killing_session, kill_reason)`.
Acceptance (ED §5.8 threshold 5) requires ≥1 positive kill exercised from a real ADR
retraction record. This ADR is the retraction record that authorizes the positive
`kill_spec()` dogfood against a synthetic spec written to `/cycle6` at S12.

### Decision
Retract the synthetic dogfood spec `cycle16:spec_be_g_kill_dogfood_s12`; transition its
`cycle16:currentStatus` → `cycle16:killed` with `cycle16:auditTrailLink` → this ADR.
Kill discipline is ADR-gated: no kill without a recorded retraction (DP#44).

| D-S13-1 | BE-H structural-prevention layer ships at cycle_16 scripts/structural_prevention/; ED section 5.9 govML paths translated to cycle_16 first-arc; threshold 5 (init_project.sh) N/A at S13, signature declared for BE-I; HC-BE-G-1/HC-BE-G-2 fixed in cycle_16 mirror, govML canonical copy carry flagged for BE-I | 2026-05-28 | Coach R3 |

---

## ADR-S21-1: BE-R built but denominator HOLD (not-yet-trustworthy); denominator scope disposed Option-1

- **Date:** 2026-05-29
- **Status:** Accepted (Coach S21 R3 verdict; kc-53 Round-2 affirmed HOLD + disposed scope)

### Context
S21 fired the BE-R Build-Runner (one foreground general-purpose Agent, S141). BE-R built the
two foundational Phase-11 mechanisms — `scripts/authored_intent_scan.py` (#50 denominator,
Method 2) + `scripts/spec_extraction_pipeline.py` (#49 E1+E2 → reconciled set V) — and
self-reported 6/6 thresholds + "PROMOTED-candidate, pending Coach R3." Coach ran the
independent third-method verification the dispatch + #18/#29 + Amendment 28h require.

### Decision — BE-R = HOLD (honest not-yet) at the Coach-verification gate
The **mechanisms are valid** (all four predicates import-and-execute real logic, not the KT-8
string-match/status-read mode; Coach independently re-ran all three guards: independence
`exit=0`, methods-distinct `exit=0`, detector-input `exit=0` with the single-reader negative
fixture correctly REFUSED; additive only — harness/probes/fixtures/gates/templates UNTOUCHED;
no fudging — the Build-Runner disclosed its findings honestly). But the **numbers they produce
are NOT yet trustworthy**. Verdict corrected from "PROMOTED-candidate" to **HOLD-not-trusted**.
Mechanisms committed; outputs recorded as untrusted, NOT promoted. BE-S/BE-T NOT run (they
consume the untrusted denominator/V). #53 (KG reconcile to V) stays BLOCKED until V is trusted.

### Three findings (the validate-the-validator catch, one level up)
1. **Denominator not method-stable — #18 ±5% cross-method check FAILS.** M1 (recorded 4-class
   audit) = 232; M1∪M2 (dual-method discoverable) = 354; Coach third method (identifier census
   across 15 cycle repos, dedup by repo+token) = 898 distinct (repo,id) pairs. ~3.5× spread.
   Root cause: "distinct spec" has no method-stable operational definition
   (operational-definition-substitution one level up).
2. **The "122 authored_but_unrecorded" is contaminated** — not a missing-specs measure. 122
   entries from only 69 distinct tokens, dominated by DP#41/DP#30/DP#7… (46 DP#N
   design-principle REFERENCES) + Cycle-16's own Done #N (54); ~8 are naming-mismatch
   false-positives (present in M1's FINDINGS corpus, missed by the token-substring name test).
   Method 2's absence-test conflates references-to-principles with authored specs.
3. **Reconciled set V is ~97.6% one reader.** Aggregate Jaccard 0.0134 (∩=22/∪=1638): E1
   (rule-based) nearly inert → V (|V|=1637, admit-on-either-reader) ≈ the E2 LLM extraction;
   the T6 guard checks V's label/path, not its composition. "Two-independent-reader V" is
   currently one reader.

### Denominator scope — disposed OPERATIONALLY by kc-53 (Round 2): Option 1
The denominator population = the **four RQS spec classes only** (agent contracts / schemas /
design decisions / methodology commitments per RQS L17/L53 + H1 L246 + probe-library Class
A/B/C/D). **DP#/HC#/GPL/Pattern/Binding are pipeline-governance principles** enforced
continuously via the gate stack + agent specs (and audited by guard-the-guards #47) — they are
**references, not denominator members**; counting them is a category error (the contamination
finding #2 above is the proof). NOT presented to Rex: resolved by the SI's own RQS; Rex's
architectural judgment does not change it (gotcha #16 NO / S176 protocol-supersedes YES).

### S22 carry — RP-authored refinement (Binding 6; NOT Coach-direct), all 3 findings as inputs
- (a) Make spec-class definition method-stable: scope enumeration to the four RQS classes;
  exclude DP/HC/GPL principle-references AND current-cycle (Cycle 16) Done-items from the
  cycles-1-15 denominator; reconcile granularity across methods to the same class definition.
- (b) Fix E1 (inert at Jaccard 0.0134) so it materially contributes before V is "reconciled."
- (c) Strengthen the #49 acceptance criterion (T6): require both readers to materially
  contribute (per-reader contribution floor / non-trivial Jaccard) — RP re-authors the criterion
  to match spec intent (#27), reported to kc-53; NOT a Coach-direct gate edit (Binding 7).
- (d) ANTI-GAMING (#28/#29): re-verify ±5% must EMERGE from independent methods applying the
  same principled definition — NOT from tuning the definition until the numbers agree (that
  would Goodhart the ±5% gate — the substitution one level up). Residual disclosed, never zeroed.

| D-S21-1 | BE-R mechanisms BUILT + valid (4 predicates import-and-execute, 3 guards re-run exit 0, additive); denominator/V HOLD (not-trusted): #18 ±5% FAILS (232/354/898), "122" contaminated (DP#N refs + Cycle-16 Done#N + naming-mismatch), V ~97.6% E2-only (Jaccard 0.0134, E1 inert). Scope disposed Option-1 (four RQS classes; principles = references not members). BE-S/BE-T NOT run; #53 blocked. S22 RP refinement carry (a-d). | 2026-05-29 | Coach S21 R3 + kc-53 R2 |

## ADR-S22-1: spec-class definition FROZEN (a) + V-composition guard strengthened (c) + E1 fixed/re-run (b) — Coach R3 = HOLD-AGAIN (honest not-yet)

- **Date:** 2026-05-30
- **Status:** Accepted (Coach S22 R3 verdict; freeze-before-count honored; nothing tuned-to-pass)

### Context
Per S21 carry + S22 task context (kc-53 R1 PASS, Rex-authorized 2026-05-30). Goal: a method-stable denominator + a genuine two-reader V, OR an honest HOLD with residual disclosed. Work split per Binding 6: RP authored (a) the frozen spec-class definition (`docs/spec_class_frozen_definition.md`, committed FIRST at `1e43a04`) + (c) strengthened ED §5.phase11.1-R threshold 6′/7/8; Build-Runner then implemented (b) the E1 fix + frozen-exclusions/unit + composition guard + re-run. Coach independently re-verified (DP#43).

### Decision — HOLD-AGAIN (honest not-yet); both #50 and #49 IMPROVED but not-yet-trustworthy
- **#50 denominator:** contamination fixed (authored_but_unrecorded 122→17 [measured]); Coach-re-derived M1'=193 [measured]. But independent 3rd-method census lands 63→424 vs 193/210 — DesignDecision "ADR row OR state.json block" sub-predicate not grain-pinned → ±5% does NOT emerge (disclosed per threshold 8, not engineered). Most-defensible denominator = M1'=193, residual disclosed.
- **#49 V:** E1 genuinely fixed 2.4%→11.8% [measured] (NOT tuned to mimic E2; methods-distinct True) but V (1818) still FAILS 6′ (e1_share 0.1177<0.20, e2_solo 0.8823>0.80, Jaccard 0.0655<0.20). Strengthened guard correctly REFUSES it (CLI exit 0: negative+live REFUSED, positive PASS) — the composition floor is now a structural HARD-FAIL, not a Coach judgment call.

### Honest residuals (never zeroed)
(i) DesignDecision count-grain unpinned (state.json-block vs ADR-row vs classifier); (ii) rule-based E1 under-contributes vs LLM on prose-heavy specs — fix the extractor/reconciliation-unit, NOT the floor; (iii) BE-S/BE-T + #53 stay BLOCKED on the untrusted V/denominator; BE-J 33.88% SUSPECT. Durable gains: frozen def + strengthened guard + contamination exclusion + 5× E1 survive to S23. See root D-S22 + BUILD_DECISION_LOG row 14-S22.


## ADR-S23-1: Denominator RESOLVED disclosed-bound (M1'=193) + V TRUSTED — grain-pin (a') + form-appropriate second reader (b') succeeded; disclosed-bound exit confirmed (kc-53 R2)

- **Date:** 2026-05-30
- **Status:** Accepted (Coach S23 R3 verdict; kc-53 R2 confirmed the disclosed-bound exit operationally; freeze-before-count honored; nothing tuned-to-pass)

### Context
S22 HOLD-AGAIN localized two residuals: DesignDecision count-grain unpinned (63->424 spread) + V single-reader-on-prose. S23 task context (kc-53 R1 PASS, Rex-authorized) split per Binding 6: RP authored (a') the decision-identity grain-pin (frozen def §7, committed FIRST `d50b6e9`) + (b') threshold 6'' (form-appropriate second reader; floors UNCHANGED); Build-Runner implemented both + re-ran. Coach independently re-verified (DP#43); kc-53 R2 disposed the verdict.

### Decision — denominator RESOLVED disclosed-bound; V TRUSTED
- **V TRUSTED:** live V PASSES 6' (e1_share 0.4333 / e2_solo 0.5667 / Jaccard 0.269 — all floors clear, UNCHANGED; S22 was 0.1177/0.8823/0.0655). Second reader genuinely independent (E1'=claude-sonnet-4-6/alt-prompt != E2=claude-haiku-4-5 on model AND prompt; not seeded from E2). Guard fixtures intact (negative REFUSED, positive PASS); #49 methods-distinct + #50 disjoint PASS. 6-spec structured edge (E1 solo=0) flagged lower-confidence.
- **Denominator RESOLVED disclosed-bound = M1'=193:** grain-pin collapsed within-method ambiguity by construction (23/445 -> 172 decision-identities). pm5% cross-method does NOT emerge (M1=119 classified / M3=172 raw-census) because the methods apply different inclusion criteria — irreducible classify-vs-census difference; forcing convergence destroys cross-method independence. No method-independent "true count" exists; disclosed per discipline #29, not engineered.

### kc-53 R2 guard refinement (recorded)
Exit criterion is **reducibility, not size**: a large residual that is irreducible + demonstrated is the disclosed-bound finding (not a HOLD). kc-53 carries the refined wording into durable surfaces (kc-54 transition).

### Residuals (DISCLOSED, carried forward, never zeroed)
(1) +53 DesignDecision classification-surplus (M3 raw-census 172 vs M1 classified 119) — carried into BE-T gap list / #53 / FINDINGS. (2) 6-spec V edge (2 bare-date degenerate + 4 at p~=0.44) — lower extraction confidence. Close claim: "100% of the disclosed-bound discoverable population, residual R disclosed."

### Consequences
UNBLOCKS BE-S (#51) / BE-T (#47 + trusted-detector run -> honest gap list) / #53 (KG reconcile to V) / Phase 12. Done #42 BE-J 33.88% lock holds (re-derive on the trusted denominator downstream). NO govML this session. See root D-S23 + BUILD_DECISION_LOG row 14-S23.
