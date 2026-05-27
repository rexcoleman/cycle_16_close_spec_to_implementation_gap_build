# Known Boundaries — {{CYCLE_ID}} {{BE_ID}}

<!-- version: 0.1 -->
<!-- created: {{DATE}} -->
<!-- profile: build -->
<!-- stage: 5 -->
<!-- methodology_status: skeleton — back-ported from `~/cycle_14_fix_cycle_13_issues_build/docs/known_boundaries.md` 613L canonical per Cycle-14-S10 substrate §2 Item 4 -->
<!-- source: K register §N.1.M out-of-scope clauses + ADR §"Distinction" mechanism-discipline anchor + per-BE dispatch substrate NOT-applies clauses -->

> **Purpose:** Register surfaces NOT-applies under {{BE_ID}} closure scope per
> DP#26 Permission-to-Disagree + HR H-class NOT-applies discipline. These
> boundaries are NOT design defects in the patched build artifact — they are
> KNOWN regions of design-space the mechanism does NOT cover, with K register
> section reference + ADR §"Distinction" L-line mechanism-discipline anchor
> for each.
>
> **Out-of-scope at {{CYCLE_ID}} build-class scope (per upstream cycle SI directive
> + ADR L-line forward-carry):** {{out-of-scope summary — what is deferred to
> Cycle N+M enforcement scope vs Cycle N+P cross-substrate query dogfood scope}}.

### Companion Contracts

**Upstream (this boundaries register depends on):**
- See [K_REGISTER](K_REGISTER.tmpl.md) §N.1 for H disconfirmation patterns whose out-of-scope clauses register here
- See [BUILD_DECISION_LOG](BUILD_DECISION_LOG.tmpl.md) §3 for boundary-condition cross-system-validation decisions
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §4 for boundary-shape failure diagnoses

## Customization Guide

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{{CYCLE_ID}}` | Cycle this boundaries register lives in | `Cycle 14` |
| `{{BE_ID}}` | Specific BE (build-event) this register scopes to | `BE#1 Branch 1` |
| `{{DATE}}` | Register-creation date | `2026-05-24` |
| `{{SURFACE_TITLE}}` | One-line title of out-of-scope surface | `Functional TypedDict("Foo", {...})` |
| `{{K_SECTION_CITE}}` | K register cross-reference | `K §10.1.3` |
| `{{FORWARD_CARRY_CYCLE}}` | Cycle N+M scope for forward-carry | `Cycle 15` |

> Delete this section once the boundaries register is filled.

---

## §1 Runtime-only surfaces (K §N.1.M; static-AST uncovered)

<!-- gate:known_boundaries §1 required -->

Per K register out-of-scope clause: the following surfaces produce mechanism-
relevant behavior at Python runtime but are INVISIBLE to the static-AST
walker the patched build artifact uses.

### §1.M {{SURFACE_TITLE}}

**Surface:** {{verbatim code example showing the construction shape}}

**Why uncovered:** {{mechanism-level explanation — name the AST node class / regex grammar / call-site shape that the static-AST walker does NOT traverse}}

**Disposition:** BOUNDARY-DOCUMENTED. Per ADR §"Distinction" L-line: static-AST coverage at {{CYCLE_ID}} + runtime DbC instrumentation candidate at {{FORWARD_CARRY_CYCLE}}+ in-vivo enforcement scope.

**K register cite:** {{K_SECTION_CITE}} — verbatim quote: "{{K-register-row quote}}".

<!-- /gate:known_boundaries §1 -->

---

## §2 Out-of-scope syntactic forms ({{K_SECTION_CITE}} detection-form scope)

<!-- gate:known_boundaries §2 required -->

Syntactic constructions that produce class-form-equivalent runtime behavior
but are NOT detected at static-AST grain by the patched walker.

### §2.M {{SURFACE_TITLE}}

**Surface:** {{verbatim code example}}

**Why uncovered:** {{mechanism-level explanation per K register detection-form scope}}

**Disposition:** BOUNDARY-DOCUMENTED. {{FORWARD_CARRY_CYCLE}}+ enforcement scope may extend via {{recommended walker extension}} if needed; {{CYCLE_ID}} {{BE_ID}} scopes to {{covered detection forms}} per dispatch substrate enumeration.

<!-- /gate:known_boundaries §2 -->

---

## §3 Runtime DbC instrumentation surfaces ({{FORWARD_CARRY_CYCLE}}+ enforcement scope)

<!-- gate:known_boundaries §3 required -->

Surfaces where runtime validation IS the enforcement layer (e.g., `__post_init__`
method bodies; pydantic `@field_validator` decorators; attrs `field(validator=...)`
runtime validators); the patched build artifact does NOT inspect these at
static-AST grain.

### §3.M {{SURFACE_TITLE}}

**Surface:** {{verbatim code example}}

**Why uncovered:** {{mechanism-level explanation per static-AST analysis scope}}

**Disposition:** BOUNDARY-DOCUMENTED. {{FORWARD_CARRY_CYCLE}}+ enforcement-layer candidate: {{recommended instrumentation approach}}. Out-of-scope at {{CYCLE_ID}} {{BE_ID}}.

**K register cite:** {{K_SECTION_CITE}} forward-carry mechanism: "{{K-register-row quote}}".

<!-- /gate:known_boundaries §3 -->

---

## §4 MRO ancestry across imports (static-AST name-match boundary)

<!-- gate:known_boundaries §4 required -->

Multi-level inheritance traversal across multiple ClassDef nodes (potentially
across files) that the static-AST name-match walker does NOT trace beyond
the immediate base position.

**Surface:** {{verbatim example showing transitive inheritance pattern}}

**Why uncovered:** {{static-AST name-match operates on immediate base name; MRO ancestry across multiple ClassDef nodes is N+M enforcement scope}}

**Disposition:** BOUNDARY-DOCUMENTED. Common case (direct inheritance from base class via documented import) IS covered; transitive inheritance via intermediate user-defined classes is {{FORWARD_CARRY_CYCLE}}+ scope.

**K register cite:** {{K_SECTION_CITE}} + ADR L-line + dispatch substrate detection-form enumeration scope.

<!-- /gate:known_boundaries §4 -->

---

## §5 ADR mechanism-discipline anchor (L-line verbatim)

<!-- gate:known_boundaries §5 required -->

Per ADR §"Distinction from voided {{VOIDED_PRECEDENT}}":

> "{{verbatim ADR quote}}"

**Mechanism discipline at {{CYCLE_ID}} {{BE_ID}}:** the boundaries documented
in this file are upstream-authorized via ADR + cycle SI ACTIVE entry. These
NOT-applies registrations are structural cover-discipline — they do NOT
soften the patched artifact's coverage claim; they HONESTLY name the region
of design-space the patch covers vs the region deferred to {{FORWARD_CARRY_CYCLE}}+
enforcement scope.

<!-- /gate:known_boundaries §5 -->

---

## §6 Honest evidence + DP#19 observation/interpretation discipline

<!-- gate:known_boundaries §6 required -->

Per DP#19 Observation ≠ Conclusion + DP#26 Permission-to-disagree boundary
discipline:

| Section | OBSERVATION (measurement) | INTERPRETATION (boundary disposition) |
|---|---|---|
| §1.M | {{observable measurement: "walker produces N attach targets on surface X"}} | {{interpretation: "runtime-only surface; static-AST cannot cover; FORWARD_CARRY_CYCLE+ enforcement scope"}} |
| §2.M | {{observable}} | {{interpretation}} |
| §3.M | {{observable}} | {{interpretation}} |
| §4 | {{observable}} | {{interpretation}} |

All measurements above are reproducible from {{aggregate JSON path}} + {{per-fixture raw JSONL emit path}}. All interpretations are sourced to K register sections + ADR + dispatch substrate per DP#26 boundary-binding discipline.

<!-- /gate:known_boundaries §6 -->

---

## §7 NOT-applies clauses (per-BE coverage gap declarations)

<!-- gate:known_boundaries §7 required -->

Per-BE explicit NOT-applies clauses bound to upstream K register sections +
ADR inheritance pattern. Each clause is a structural cover-discipline
declaration: "this BE does NOT claim coverage of surface X; surface X is
deferred to {{FORWARD_CARRY_CYCLE}}+".

### §7.M {{NOT_APPLIES_TITLE}}

**Pattern:** {{verbatim pattern shape}}

**{{BE_ID}} disposition:** NOT in {{N-patch}} scope per dispatch substrate explicit. {{Cycle baseline behavior}} PRESERVED in patched artifact.

**Forward-carry:** {{FORWARD_CARRY_CYCLE}}+ enforcement-layer per renumber {{DATE}}. Recommended: {{recommended approach}}.

**K register cite:** {{K_SECTION_CITE}}.

<!-- /gate:known_boundaries §7 -->

---

## §N Self-test (BEFORE classifying boundaries register as COMPLETE for cycle close)

| # | Check | Status |
|---|---|---|
| 1 | Every §1.M / §2.M / §3.M / §7.M row has verbatim K-register cite (no `{{PLACEHOLDER}}`) | [ ] |
| 2 | Every interpretation row in §6 cites OBSERVATION evidence path | [ ] |
| 3 | §5 ADR-anchor quote is verbatim (matches ADR source) | [ ] |
| 4 | All forward-carry cells name specific Cycle N+M (not "future" / "later") | [ ] |
| 5 | No softening language ("usually" / "mostly" / "should") in disposition cells | [ ] |
| 6 | All authority anchors resolve (SI line + ADR section + lock_commit) | [ ] |

> If any check is `[ ]`, halt-and-surface; do NOT close the BE.
