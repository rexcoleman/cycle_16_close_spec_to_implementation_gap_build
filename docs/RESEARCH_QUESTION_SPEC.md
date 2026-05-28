# RESEARCH QUESTION SPEC

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- stage: 1 -->
<!-- methodology_status: partial — stages 0-2 methodology from Phase B.1 -->

> **Purpose:** Force question formation from observations, not from intuition alone.
> Prevent "I want to study X" without "here's the gap that makes X worth studying."
> This template defines WHAT to document about a research question, not HOW to
> formulate one. The middle loop discovers process.

---

## §0 Question Statement

**Cycle 16 research question (verbatim from Cycle 16 SI L11 + Amendment 2026-05-27a):** How do we structurally guarantee that every spec our pipeline writes — agent contracts, schemas, design decisions, methodology commitments — becomes implemented running code by the close of the authoring cycle (default), or gets explicitly deferred to a named target session with audit trail (exception requiring authorization for deferral past the authoring cycle close), or gets explicitly killed with audit trail — with structural detection of dormancy within ≤3 sessions of authoring via the runtime emit mechanism, and no silent drift?

This question traces to OBS-1 (Cycle 10 RUNTIME_EMIT_SPEC.md 5-cycle gap canonical case study) + OBS-6 (Rex 2026-05-27 strategic pivot) + PAT-1 (specs author silently dormant — no structural surface forces implementation closure within authoring cycle). The question is falsifiable per H1-H8 hypothesis enumeration at §3a + KT-1..KT-5 pre-registered triggers with full PASS/REFUTE/PARTIAL/SUPERSEDED outcome space.

### §0a Paradigm Challenge — Start Here

<!-- source: Phase I Gap Research (G1+G7), Track 1 (5/7 papers) -->

Before writing your question, answer these two prompts. They set the framing
for everything that follows. Skipping them and writing a conventional question
first creates confirmatory framing that §4.1 and §4.2 cannot fix after the fact.

**1. What does the field currently believe that might be wrong?**

The wrapper program (and broader AI-agent-built-systems engineering practice) currently believes that **drafting-discipline-at-authoring-time** + **periodic-cycle-close-review** are sufficient to ensure that authored specs become running code. The Cycle 10 telemetry case study refutes this: the spec was well-authored at BE#5+BE#6 by a disciplined process, and Cycle 10 / Cycle 11 / Cycle 12 / Cycle 13 / Cycle 14 close-reviews all occurred — and the runtime wiring still did not happen until Cycle-15-S7 only because Rex explicitly disposed govML back-port at that surface. Five cycles of close-reviews failed to close the gap. The assumption to challenge: **author-time discipline + periodic review = implementation guarantee**. The challenge: **without a per-spec registry binding "authored" to "runtime emit event class fired" via a structural BLOCKING gate that fires at both cycle close AND session close with a ≤3-session dormancy threshold, no amount of author-time care or close-review attention will catch dormant-silent specs at the source.** This challenge is operationally tested by Branch 4.3's TWO-surface BLOCKING gate (Cycle 16 SI L65-L67) — if the gate fires retroactively on Cycle 1-15 inventory and surfaces specs the close-reviews missed, the assumption is refuted.

> Name a specific assumption — not a gap. A gap is "nobody has measured X."
> An assumption challenge is "everyone assumes X is true, but what if it's not?"
> VAR: "Autoregressive must use raster-scan order." Bell: "Loopholes can be closed
> one at a time." Milkman: "Interventions should be tested one at a time."
> If you cannot name an assumption to challenge, your question is confirmatory —
> it will score N=5. That's acceptable for some research, but name it honestly.

**2. Lakatos test — does your question predict a novel fact or accommodate a known one?**

| Test | Answer |
|---|---|
| **If I run this study, could the result go EITHER WAY?** | yes — KT-1..KT-5 pre-registered with reversal disposition. KT-1 (substrate covers ≥80%) implies result = "narrow to gap-filling only" (NOT a new mechanism); KT-2 (<3 dormant-silent specs) implies result = "problem smaller than hypothesized → halt + Rex re-disposition"; KT-3 (n=3+ author refusals) implies result = "registry shape needs refinement OR same-cycle default relaxation"; KT-4 (gate pattern doesn't extend) implies result = "new enforcement primitive class warranted"; KT-5 (≥2 NEW dormant-silent specs accumulate during Cycle 16) implies result = "H_main REFUTED → paradigm escalation". The result space spans full PASS/REFUTE/PARTIAL/SUPERSEDED outcomes. |
| **Would an expert in this field be SURPRISED by any possible outcome?** | yes — (a) **Bertrand Meyer** (Design by Contract author) would be surprised if the AI-agent engineering methodology field had NO mechanism analogous to DbC runtime assertions at the spec-vs-implementation boundary, given that DbC was published in 1992 IEEE Computer and is field-standard. (b) **Michael Nygard** (ADR template author, 2011) would be surprised if a research pipeline that explicitly tracks DECISION_LOG entries does not extend ADR's "Accepted post-acceptance immutable + supersedure tracking" lifecycle discipline to its own internal-methodology specs. (c) Practitioners in DevOps feature-flag governance (LaunchDarkly + GrowthBook) would be surprised that a system that authors many "feature-like" methodology commitments has no stale-flag detection equivalent at 14-30-day thresholds. |
| **Am I applying a KNOWN method to a NEW domain where the general result is expected?** | partially — Branch 2.3 hypothesis ("Cycle 14 four-gate pattern extends from artifact-exists to spec-implemented predicate") IS a known-method / new-predicate variant. However, the question is whether the extension WORKS at the predicate boundary (KT-4 firing if not). The composite mechanism (5-state taxonomy + per-spec registry schema + TWO-surface BLOCKING gate + ≤3-session dormancy detection + runtime emit class wiring at authoring) is **NOT** field-standard for AI-agent engineering methodology — this is a NEW composition. N ceiling assessment: the COMPOSITION is non-standard; the COMPONENT disciplines (PEP / RFC / OpenAPI / DbC / ADR / feature-flag / Parnas) are well-established. N target = 7 (genuine methodological contribution composing 7 established disciplines into a new mechanism class for AI-agent engineering methodology). N = 9 requires paradigm inversion — which is reserved as the secondary surface (KT-5 paradigm escalation if structural mechanism fails). |

> A "yes, no, yes" pattern = confirmatory research. The result accommodates what's
> already known rather than predicting something new. This is Lakatos' "degenerating
> research programme" — not wrong, but N-capped. To shift toward progressive: reverse
> one of the field's assumptions (prompt 1) and design around the reversal.

**Research question (verbatim from Cycle 16 SI L11 + Amendment 2026-05-27a):** How do we structurally guarantee that every spec our pipeline writes — agent contracts, schemas, design decisions, methodology commitments — becomes implemented running code by the close of the authoring cycle (default), or gets explicitly deferred to a named target session with audit trail (exception requiring authorization for deferral past the authoring cycle close), or gets explicitly killed with audit trail — with structural detection of dormancy within ≤3 sessions of authoring via the runtime emit mechanism, and no silent drift?

> Must trace to ≥1 observation in OBSERVATION_LOG §1.
> Must be answerable with data or experiments — not opinion or external validation.
> Must be informed by your §0a paradigm challenge — if you challenged an assumption,
> the question should test that challenge.

---

## §1 Observation Link

<!-- gate:research_question_spec §1 entries:1 -->

| # | Observation ID | Source (from OBSERVATION_LOG) | Signal/Pattern Quoted |
|---|---|---|---|
| 1 | OBS-1 | Cycle 10 RUNTIME_EMIT_SPEC.md + Cycle-15-S7 close substrate | "The drift-telemetry / runtime-emit schema was authored at Cycle 10 BE#5+BE#6 but never wired into runtime emission across kc-34..kc-43 lifecycle (5 cycles); spec→runtime closure only finally occurred at Cycle-15-S7 after explicit Rex disposition forced govML back-port." Canonical Cycle 10 telemetry case study referenced verbatim at Cycle 16 SI L13. |
| 2 | OBS-2 | `git ls-files .claude/agents/` (Moonshots) vs `ls .claude/agents/*.md` | "9 agent specs exist on disk... only 3 tracked in git... 6 of 9 specs gitignored per `.claude/agents/*.md` rule — invisible to `git ls-files` audit. HC #52 broader scope per kc-44 task context carry-forward #3." |
| 3 | OBS-4 | `sqlite3 singularity.db .schema` enumeration | "No `spec_registry`-class table exists in `singularity.db`. `prompt_inventory` table tracks active agent specs with `protocol_version` field, but lacks `target_session` / `current_status` (5-state) / `runtime_emit_event_class` / `dormancy_detection_threshold_sessions` fields per Cycle 16 SI §4.1 schema. TBD per §2 substrate audit." |
| 4 | OBS-5 | `~/ml-governance-templates/scripts/k_register_present_gate.sh` source inspection | "Cycle 14 four-gate scripts implement an 'artifact-exists + placeholder-zero' predicate at template-class scope... Pattern shape may extend from 'artifact exists' to 'spec implemented' — Branch 2.3 assessment surface." |
| 5 | OBS-6 | Rex direction 2026-05-27 + Amendment 2026-05-27a | "Rex explicit recognition that Cycles 13-15 attacked rubric refinement (downstream symptom) while the upstream failure mode — specs authored never becoming running code — went unaddressed for 5+ cycles. Deadline framing tightened 2026-05-27 from 'bounded cycles' → 'same authoring cycle by default + ≤3-session runtime emit detection'." |
| 6 | PAT-1 (pattern note from OBS-1+2+3+4) | OBSERVATION_LOG §3 PAT-1 | "Specs author silently dormant — no structural surface forces implementation closure within the authoring cycle... the pipeline has NO surface that fires BLOCKING when a spec authored at session N hasn't fired its runtime emit class by session N+3 (default ≤3-session dormancy threshold per Amendment 2026-05-27a)." |
| 7 | PAT-2 (cross-discipline convergence pattern) | OBSERVATION_LOG §3 PAT-2 | "External disciplines (7) all encode some variant of spec→implementation lifecycle tracking + structural enforcement... mechanism shape is consistent across disciplines: per-spec registry row + lifecycle state machine + structural detection of dormancy." |

<!-- /gate:research_question_spec §1 -->

> [SEED: min_linked_observations=1]
> Link to specific observation IDs from OBSERVATION_LOG §1.
> Quote the signal or pattern that motivated this question.

### §1.1 Question Lineage

<!-- source: Track 1, U1/priority 1 — 7/7 papers -->

**Required field:** What specific limitation of the best prior work defines this
question? Cite the prior work and quote its stated limitation or boundary.

| Prior work (citation) | Its stated limitation or boundary | How your question addresses this limitation |
|---|---|---|
| AAEM cycle 1 close FINDINGS (per Cycle 16 SI L5 authority chain) | "documentation-active-vs-code-active gap as the dominant failure mode the wrapper program was created to address" (paraphrased from authority chain L5; AAEM cycle 1 close framing) | This question targets exactly the named-but-not-structurally-addressed failure mode. AAEM cycle 1 NAMED the gap; wrapper Bindings 1+2 (2026-05-07) attempted Coach-discipline / RP-discipline mitigation; Cycles 13/14/15 then drifted to rubric refinement; this Cycle 16 question is the structural-mechanism answer (per-spec registry + 5-state taxonomy + TWO-surface BLOCKING gate at cycle-close + session-close ≤3-session emit detection). |
| `research_infrastructure_discoverability_and_enforcement` (S160-S161 RP work; PROJECT.md L8 verbatim research question) | "How do we make our end-to-end research-process infrastructure both DISCOVERABLE and ENFORCEABLE for both Coach and Rex — so the L4 pipeline actually USES the infrastructure we've built across multiple cycles — to consistently support improved research quality without depending on Rex's per-session reminder load?" (~/research_infrastructure_discoverability_and_enforcement/PROJECT.md L8 verbatim) | RIDE addressed infrastructure DISCOVERABILITY + ENFORCEABILITY but its mechanism scope was infrastructure-USE (does the pipeline USE the gate script after it's built?). Cycle 16 extends to spec-IMPLEMENTATION (does the spec become a runtime artifact after it's authored?). RIDE F-A/F-B/F-C/F-D composition is the LOAD-BEARING input for KT-1 disposition assessment at LANDSCAPE §6 — if RIDE F-A enforcement primitive + F-C consumer-side agent_spec pre_check + Cycle 14 four-gate pattern collectively cover ≥80% of mechanism scope, KT-1 fires → Cycle 16 narrows to gap-filling + retroactive inventory only. |
| `research_depth_enforcement_automation` (cycle 1 FINDINGS) | "structural-vs-behavioral enforcement primitive class + compliance evidence" (per Cycle 16 SI L42 substrate audit citation) | This Cycle 16 question structurally extends the enforcement-primitive-class boundary from depth-rubric enforcement (e.g., landscape_depth_judge.py F2 + landscape_depth_gate.sh F1) to spec-implementation enforcement (per-spec registry + TWO-surface BLOCKING gate). Branch 2.2 assesses whether the depth-enforcement primitive shape extends cleanly or requires new primitive class (KT-4 firing if not). |
| Cycle 14 four-gate precedent (`k_register_present_gate.sh` + `known_boundaries_present_gate.sh` + `h_pattern_dispositions_present_gate.sh` + `hc26_internal_smoke_gate.sh`) | "Cycle 14 four-gate validates artifact-class structural existence + placeholder-zero + ≥1 §N.1.M H-disconfirmation subsection" (per k_register_present_gate.sh header lines 14-17) | The Cycle 14 gate pattern stops at artifact existence; this Cycle 16 question extends to spec implementation. Same gate-script shape (BLOCKING at cycle close via `check_all_gates.sh`); new predicate body ("spec authored AND runtime_emit_event_class fired within ≤3 sessions of authoring"). Branch 2.3 assesses extension cleanly vs new primitive class (KT-4). |
| Cycle 10 RUNTIME_EMIT_SPEC.md authored at BE#5+BE#6 | "spec authored at Cycle 10 BE#5+BE#6; runtime never wired across kc-34..kc-43 lifecycle; finally landed at Cycle-15-S7 only because Rex explicitly disposed govML back-port at that surface" (per Cycle 16 SI L13 verbatim) | This is the canonical case study — every aspect of Cycle 16's mechanism is justified against whether it would have closed the Cycle 10 5-cycle gap at authoring time. Authoring-time registry row + same-cycle target_session default + runtime_emit_event_class wiring would have surfaced the dormancy at Cycle 10 close, not Cycle 15. |

> The observation in §1 connects to a signal; this field traces the signal to a
> specific prior work's boundary. The most impactful research questions emerge from
> the frontier of what's already known, not from blank space.
>
> Chetty: "Chetty & Hendren 2014 measured mobility at commuting-zone level
> (~740K people); this question escalates precision 100× to census-tract level
> (~4,250 people)." Bell: "Aspect 1982 closed the locality loophole but left the
> detection loophole open; this experiment closes both simultaneously."
> VAR: "Autoregressive image generation uses raster-scan ordering borrowed from
> NLP; this work replaces it with multi-scale ordering native to images."
>
> **Self-test:** Can you quote the prior work's own stated limitation? If they
> didn't state one, what boundary did they implicitly stop at? If you can't identify
> a specific boundary, your question may not be building on the frontier — it may be
> parallel to existing work rather than advancing beyond it.

---

## §2 Alternatives Considered

<!-- gate:research_question_spec §2 entries:2 -->

For each alternative research question considered, document using ADR-adapted format:

### Alternative 1

| Field | Content |
|---|---|
| **Context** | Continue Cycle 13-15 rubric refinement trajectory (refine static-AST rubric D-1.1 through D-1.5; extend rubric coverage; deploy in-vivo; longitudinal metrics; full 5-layer FINDINGS). |
| **Alternative question** | "What dimensions and coverage thresholds for the static-AST code-vs-spec rubric maximize durable confidence that a generated artifact matches its spec?" |
| **Why rejected** | Rex 2026-05-27 explicit pivot directive: "we spent 3 cycles attacking the wrong problem." The rubric measures spec-vs-code DIVERGENCE at the moment of comparison; it does NOT detect specs that never become code in the first place (the upstream failure mode). Refining the rubric without closing the spec-implementation gap means refining a measurement instrument while the measured-thing remains absent for many specs (Cycle 10 telemetry case — 5 cycles dormant). |
| **Consequences of rejection** | Cycle 13-15 LOCKED bodies preserved per Binding 7 (no modification). Partial Cycle 15 closure at S7 end with Items 1+2+3+4 CLOSED; Items 5+6+7+8+9+10 declared out-of-scope per Rex 2026-05-27 cycle pivot — explicitly deferred (audit-trail-recorded) to future-cycle refinement if reactivated. Cycle 17 (formerly Cycle 16 "discover-and-enforce" pre-rename) absorbs the deferred rubric-refinement scope; Cycle 18 (formerly Cycle 17 "content fidelity") absorbs cascade. Trade-off acknowledged: rubric refinement work paused while Cycle 16 attacks upstream gap. |

### Alternative 2

| Field | Content |
|---|---|
| **Context** | Frame the question at a paradigm-class scope: "What does it mean for an AI-agent-built software pipeline to have an executable methodology specification (vs. a documented one)?" |
| **Alternative question** | "Can a pipeline's research methodology be expressed as executable specifications such that no manually-maintained documentation is needed — drift becomes structurally impossible because there is no spec/code separation?" |
| **Why rejected** | Paradigm-class scope-creep; out-of-scope per Cycle 16 SI L91-L95 explicit out-of-scope ("New rubric dimensions beyond Cycle 13's five" + "Modification of Cycle 13/14/15 LOCKED bodies" + Cycle 1 envelope cap ≤6 sessions per disposed paradigm question #1). This Alternative 2 is essentially asking "what if OpenAPI-spec-to-code generation could be applied to methodology specifications themselves" — which is interesting but would expand the cycle to multi-cycle paradigm research. KT-5 paradigm escalation is the structural surface for this question IF the Cycle 16 structural mechanism fails — but it is NOT the default Cycle 16 scope. |
| **Consequences of rejection** | The full paradigm-class question is deferred; Cycle 16 attacks the structural gap with a within-paradigm mechanism (per-spec registry + 5-state taxonomy + TWO-surface BLOCKING gate). If Cycle 16 mechanism succeeds (KT-1..KT-5 don't fire negatively), the spec-implementation gap is closed at engineering grain without paradigm expansion. If KT-5 fires (≥2 NEW dormant-silent specs accumulate during Cycle 16 itself), the paradigm-class question becomes the candidate for a future-cycle paradigm-escalation surface. |

### Alternative 3

| Field | Content |
|---|---|
| **Context** | Frame as a behavioral / soft-process question rather than structural: "What checklists and review disciplines should authors and reviewers follow to ensure authored specs become running code?" |
| **Alternative question** | "What author-time and review-time checklists, when followed by RP / Coach / Rex, maximally reduce the rate of dormant-silent specs across cycles?" |
| **Why rejected** | Pattern from `feedback_kernel_coach_observe_then_direct.md` + DP#43-44 + the wrapper-program Binding 6 ("structural > behavioral" implicit). Cycle 10 telemetry case study refutes the behavioral approach: the spec was well-authored at BE#5+BE#6 by a disciplined process and 5 cycles of close-reviews STILL missed it. Behavioral instruction degrades over context-window length; structural enforcement fires per-invocation. This is the design principle (DP#42-44) that makes Cycle 14 four-gate the appropriate template precedent — gates fire at gate-time mechanically, not at human discretion. |
| **Consequences of rejection** | Behavioral approach is a CANDIDATE FALLBACK if KT-3 fires (n=3+ author refusals because spec-authoring-discipline at registry-row-required + target_session-required + emit-event-required level produces author rejections). Per KT-3 disposition, fallback is either (a) registry shape needs structural refinement OR (b) same-cycle default needs relaxation. Behavioral checklist could be the relaxation form. But it is NOT the Cycle 16 default. |

<!-- /gate:research_question_spec §2 -->

> [SEED: min_alternatives=2]
> Structure borrowed from DECISION_LOG ADR format.
> Each alternative is a question you COULD have asked instead of the one in §0.
> The purpose is to demonstrate the chosen question was selected, not assumed.

### Adjacent Question Mapping

<!-- source: Track 1, gap matrix Stage 1 -->

Beyond the alternatives you naturally considered above, name 1 additional question
adjacent to yours that you deliberately chose not to pursue. What specific evidence
made your chosen question higher-impact?

| Adjacent question not pursued | What you'd lose by pursuing it instead | Evidence your chosen question is higher-impact |
|---|---|---|
| "How should the build-runner agent be extended to also track per-spec runtime emit events as part of its build-class workflow?" | Premature mechanism scoping. The build-runner agent extension is one of MULTIPLE structural surfaces where per-spec registry binding could live; choosing build-runner before §2 substrate audit + §3 LANDSCAPE 7-discipline external grounding would be solution-anchored. Cycle 16 Branch 2 explicitly orders substrate audit FIRST, external research SECOND, mechanism design THIRD. | Per Cycle 16 SI L37-L46 substrate-audit-FIRST ordering — if RIDE F-A/F-B/F-C/F-D + Cycle 14 four-gate + Cycle 10 telemetry collectively cover ≥80% (KT-1), build-runner extension may not be the right structural surface. The mechanism-class choice is downstream of substrate evidence. Pursuing build-runner-specific question pre-empts evidence. |

> This extends the alternatives analysis to the broader question space. §2's
> alternatives are different framings of the SAME problem. This prompt asks about
> a DIFFERENT problem nearby that competes for attention. The purpose: prevent
> drift to the most convenient question rather than the highest-impact one.

### Boundary-Spanning Feasibility Check

<!-- source: Phase E cycle 2 learning — BS=4 when method analog is from same domain -->

Does this research question naturally require importing methods from OUTSIDE the
primary domain? If the closest methodological analog is from the same field (e.g.,
ATT&CK coverage mapping applied to ATLAS coverage mapping — both cybersecurity),
the Boundary-Spanning (BS) ceiling is ~5. Cross-domain import at the QUESTION level
(not just citation level) is what drives BS above 5.

| Check | Answer |
|---|---|
| **Closest methodological analog** | The closest single-analog is **IETF RFC 6982/7942 Implementation Status Section + Python PEP 1 PEP-Delegate implementation tracking** — both encode "per-spec implementation-status field tracked through lifecycle by named owner". Closest field-of-engineering-practice analog is **DevOps feature-flag lifecycle management** (LaunchDarkly + GrowthBook + Optimizely) which composes per-flag lifecycle states + stale-flag detection at configurable session-granularity-equivalent thresholds (14-30 days). |
| **Is the analog from a different domain than your research?** | yes — IETF standards-development (network protocols community), Python PEP (programming-language-evolution community), OpenAPI (web-API engineering community), Design by Contract (formal-methods / programming-language-theory community), feature-flag governance (DevOps / SaaS community), ADR (software-architecture / enterprise-software community), and Parnas (software-engineering / safety-critical-systems community) are all distinct domains from "AI-agent-built systems engineering methodology." 7 disciplines spanning 7 distinct source domains — BS ceiling assessment ≥7. |
| **What genuine cross-domain import could strengthen the question?** | The most structurally-novel cross-domain import is **composing 7 disciplines into a unified per-spec registry schema (Cycle 16 SI §4.1) — taking RFC 6982 implementation-status field + PEP-Delegate ownership + LaunchDarkly per-flag lifecycle states + ADR supersedure linkage + DbC runtime-assertion-at-boundary mechanism + OpenAPI contract-first single-source-of-truth + Parnas tabular-notation precise-documentation discipline**. Each contributes a distinct field (`spec_id` + `owner` + `current_status` 5-state + `target_session` + `runtime_emit_event_class` + supersedure-link + `dormancy_detection_threshold_sessions`). The COMPOSITION is the novel mechanism; each component is field-mature in its source domain. |

> [SEED: BS_ceiling_threshold=5 for same-domain method analogs. Calibrated from
> S59 cycle 2: governance framework analysis imported ATT&CK methodology (same
> field) → BS=4. B.3 biology imported network science (different field) → BS=6.]

### Formulation-Level Predetermination Check

<!-- source: Phase F v2, cycle A' — BS=5 despite genuine cross-domain import -->

Even if the method is from a genuinely different domain, check whether its
mathematical formulation makes the result a function of the same variable
you're comparing against.

| Check | Answer |
|---|---|
| **What is the imported method's core mathematical relationship?** | The mechanism is structural (engineering-discipline composition), NOT mathematical — there is no closed-form mathematical relationship that predetermines the outcome. The Cycle 14 four-gate gate-script-shape (predicate substitution) is the closest "formal" component: `gate(spec) = artifact_exists(spec) ∧ placeholder_count(spec) == 0 ∧ H_disconfirmation_subsection_count(spec) ≥ 1` → extending to `gate(spec) = registry_row_exists(spec) ∧ target_session(spec) is not null ∧ runtime_emit_event_class(spec) is not null ∧ (current_status ∈ {running, dormant-with-explicit-deferral, killed, long-running} ∨ session_authored + dormancy_threshold ≥ current_session)`. |
| **What variable does this relationship depend on?** | The predicate depends on per-spec registry-row fields, NOT on any single mathematical variable. Risk surface: if predicate body is mis-specified (e.g., `dormancy_threshold` ≤ 0 produces always-FAIL; ≥ infinity produces always-PASS), gate becomes trivial. Mitigation: threshold defaults from external grounding (LaunchDarkly 30d/7d; GrowthBook 14d; Cycle 16 SI 3 sessions) — calibration against field practice, not arbitrary. |
| **Is that variable the same as (or monotonic function of) your comparison metric?** | no — the comparison metric for Cycle 16 close is BINARY-class per-spec ("did this spec authored at session N have its runtime_emit_event_class fire by session N+dormancy_threshold?") and aggregate ("how many dormant-silent specs across Cycles 1-15?"). These are independent of the gate-predicate's variable structure — the gate fires on registry state, not on the outcome being measured. |
| **If yes: what alternative formulation would NOT be predetermined?** | n/a (no — the predicate does not predetermine the outcome being measured). |

> [SEED: formulation_predetermination_ceiling=5. Calibrated from cycle A':
> SEIR HMF sets beta_k = beta * k on power-law DAG → rankings proportional to
> degree by construction → rho = 1.000 across ALL 12 ablation configurations →
> BS=5 despite genuine cross-domain import (epidemiology -> software security).
> The existing same-domain check (above) would have PASSED this case.]

### Import Depth Verification

<!-- source: Phase I Gap Research (G2) — 7/7 breakthrough papers engaged deeply with source domain -->

If your question imports a method from another domain, verify the import is
substantive — not just borrowing a tool name or output format.

| Depth Check | Answer |
|---|---|
| **What conceptual FRAMEWORK from the source domain are you engaging with?** | Three load-bearing frameworks: (1) IETF "running code" philosophy (RFC 6982/7942) — that specifications without reference implementations are incomplete and that implementation status MUST travel with the spec through the lifecycle as a first-class field. (2) Meyer's Design by Contract framework (1992 IEEE Computer) — that runtime assertions at code boundaries (preconditions / postconditions / invariants) catch spec-vs-implementation drift at the exact frame where it occurs. (3) LaunchDarkly / GrowthBook feature-flag lifecycle framework — that per-flag states + structural detection of unused flags at configurable thresholds (LaunchDarkly: "stale when temporary + not deleted + created at least 30 days ago + status 'inactive' or 'launched' for at least 7 days"; GrowthBook: "not updated in past two weeks and serves the same value to all users") prevent flag-as-tech-debt accumulation. These three frameworks together = implementation-status-tracking + runtime-boundary-enforcement + lifecycle-state-machine-with-stale-detection. |
| **How did you ADAPT it for your target domain's constraints?** | Adaptation #1 (IETF Implementation Status): instead of per-RFC running-code-elsewhere tracking, per-spec registry row with `runtime_emit_event_class` field — an explicit event the spec's implementation MUST emit when fired in runtime, observable structurally via `outputs/*.jsonl` sinks. Adaptation #2 (DbC runtime assertions): instead of code-boundary preconditions, gate-script-as-boundary fired at cycle-close AND session-close — the gate IS the runtime assertion at the methodology spec's lifecycle boundary. Adaptation #3 (feature-flag staleness): per-spec `dormancy_detection_threshold_sessions` (default 3) — sessions, not days, because the pipeline's natural cadence is per-session not per-day. The threshold scales to pipeline temporal granularity rather than calendar time. |
| **What would a specialist in the SOURCE domain recognize in your work?** | An IETF spec author would recognize RFC 6982-shape: a per-spec implementation-status field that travels with the spec through its lifecycle, allowing reviewers to "assign due consideration to documents that have the benefit of running code." A Meyer / DbC specialist would recognize the cycle-close gate as a runtime contract-violation surface that fires at the boundary between authored-state and implemented-state. A LaunchDarkly engineer would recognize the per-spec `current_status` 5-state taxonomy (running / dormant-with-explicit-deferral / dormant-silent / killed / long-running) as structurally parallel to LaunchDarkly's flag lifecycle states (Live / Ready for code removal / Ready to archive / Archived / Deprecated). An ADR governance practitioner would recognize the supersedure-tracking discipline (Cycle 16 mechanism extends ADR `Superseded By` linkage to per-spec status transitions). The structural fingerprints of all 4 source frameworks are visible in Cycle 16's composition. |

> [SEED: import_depth_floor=3_checks. If any check is blank or "N/A",
> the import is surface-level — BS ceiling is ~5.]
>
> AlphaFold: engaged attention mechanism THEORY (not "used transformers"),
> adapted for residue co-evolution (triangle attention), crystallographers
> recognize the output as structure prediction. All 3 substantive.
> Cycle 2 (BS=4): borrowed coverage scoring PATTERN, did not engage
> ATT&CK's threat modeling FRAMEWORK, a specialist would see the same
> domain's vocabulary applied adjacently. 0/3 substantive.

---

## §3a Hypothesis Enumeration (4 branches decomposed) + KT-1..KT-5 Pre-Registration

<!-- source: kc-44 PD §3.3 mechanical tests T5 + T8 — branches decomposed into H1-H7+ + KT-class triggers pre-registered structurally -->

Cycle 16 SI ACTIVE 4 branches (per Cycle 16 SI L15-L72) decomposed into testable hypotheses H1-H8 + 5 pre-registered kill triggers KT-1..KT-5:

| Hypothesis | Statement | Source branch | Operational test |
|---|---|---|---|
| **H1** | Spec inventory across Cycles 1-15 enumerates ≥N specs across 4 spec-classes (agent contracts ~9 from `.claude/agents/*.md` + schemas from runtime_emit + drift_telemetry + JSONL classes + design decisions from DECISION_LOG / ADR / paradigm-disposition records + methodology commitments from cycle-close FINDINGS Layer-5). | Branch 1.1 | Retroactive scan at Cycle 16 mid-cycle enumerates per-spec rows + per-spec status classification per 5-state taxonomy. Done definition #1 ("every spec across Cycles 1-15 enumerated"). |
| **H2** | Per-type operational definitions of "implemented" hold structurally (agent contract = prompt file at canonical path + role invoked; schema = schema file + code validates + validation fires at runtime; design decision = code embodies OR explicit retraction ADR; methodology commitment = documented in cycle-close FINDINGS + cited at downstream session warmup OR explicit deferral). | Branch 1.2 | Each spec class has a structural verifier — agent contract verified via `git ls-files .claude/agents/` + invocation evidence at session logs; schema verified via gate-script pattern (k_register precedent); design decision verified via DECISION_LOG cross-reference; methodology commitment verified via FINDINGS Layer-5 + downstream warmup citation. |
| **H3** | At least 3 of 9 currently-extant agent specs (Cycle 16 SI Branch 1.1 enumeration) classify as `dormant-silent` per 5-state taxonomy at retroactive scan. | Branch 1.3 + 1.4 | Retroactive Branch 4.4 scan; aggregate count of `dormant-silent` rows. **KT-2 firing inverse threshold: if <3 dormant-silent specs found, KT-2 fires** → problem smaller than hypothesized → halt + Rex re-disposition. |
| **H4** | Cycle 10 RUNTIME_EMIT_SPEC.md case study root cause is "no spec-authoring-time discipline forced registry row + target_session + runtime_emit_event_class at BE#5+BE#6"; Cycle 16 mechanism would have closed the 5-cycle gap at authoring time. | Branch 1.5 | Counterfactual analysis at FINDINGS Layer 4 — apply proposed Cycle 16 spec-authoring discipline (Branch 4.2) to Cycle 10 BE#5+BE#6 substrate; observe whether registry row would have existed, target_session = "close of Cycle 10," runtime_emit_event_class = "drift_telemetry event class fires when telemetry collector emits to JSONL sink." Counterfactual gate would have BLOCKED Cycle 10 close until runtime_emit wired. |
| **H5** | RIDE + research_depth_enforcement_automation + Cycle 14 four-gate collectively cover **≥80% of Cycle 16 mechanism scope** (spec-registry schema fields + authoring discipline + TWO-surface BLOCKING gate). | Branch 2.1 + 2.2 + 2.3 + 2.4 | LANDSCAPE §6 cross-validation surface; assessment via 7-section coverage matrix (registry row schema / 5-state taxonomy / target_session field / runtime_emit_event_class field / dormancy_detection threshold / cycle-close gate / session-close gate). **KT-1 firing threshold: if §5.1+§5.2+§5.3 internal substrate collectively cover ≥80%, KT-1 fires** → narrow Cycle 16 to gap-filling + retroactive inventory only. |
| **H6** | Cycle 14 four-gate gate-script-shape (artifact-exists + placeholder-zero + ≥1 H-disconfirmation subsection) EXTENDS CLEANLY to "spec implemented" predicate (registry_row_exists + target_session_set + runtime_emit_event_class_set + status_in_acceptable_set). Same gate-script skeleton; new predicate body. | Branch 2.3 | Gate-script implementation at Stage 5 — `spec_implementation_present_gate.sh` skeleton mirrors `k_register_present_gate.sh`. **KT-4 firing threshold: if "spec implemented" predicate requires structurally different gate primitive than "artifact exists," KT-4 fires** → new enforcement primitive class warranted. |
| **H7** | Spec-authoring discipline at Branch 4.2 (no spec lands without registry row + target_session + runtime_emit_event_class) produces **0 author refusals during Cycle 16 itself**. | Branch 4.2 + 4.5 | Forward-apply observation during Cycle 16 itself — every new spec authored in Cycle 16 (KT-trigger registry + 5-state taxonomy + registry schema spec itself + retroactive scan spec) passes authoring discipline cleanly. **KT-3 firing threshold: if n=3+ author refusals fire (acceptance criteria unclear at authoring OR same-cycle backlog unmanageable), KT-3 fires** → registry shape needs structural refinement OR same-cycle default needs relaxation. |
| **H8** | Forward-apply across ≥2 subsequent post-Cycle-16-close cycles produces **0 NEW dormant-silent specs** + at least 1 same-cycle implementation event observed (positive case). | Branch 4.5 | Done definition #10 longitudinal verdict; observation across Cycles 17+18 (per kc-44 Amendment 2026-05-27a renumbering). **KT-5 firing threshold: if ≥2 NEW dormant-silent specs accumulate during Cycle 16 itself (forward apply observation), KT-5 fires** → H_main REFUTED; FINDINGS Layer 5 honest-gap + paradigm escalation candidate. |

**KT-1..KT-5 pre-registration matrix** (structurally encoded here + at ED §Field 6 forward + at LANDSCAPE §6 KT-1 disposition recommendation + at OBSERVATION_LOG §3 PAT-4):

| Trigger | Detection point | Threshold | Disposition |
|---|---|---|---|
| **KT-1** | LANDSCAPE §5 substrate audit close (Stage 2) | RIDE + research_depth_enforcement_automation + Cycle 14 four-gate collectively cover ≥80% of mechanism scope | Narrow Cycle 16 to gap-filling + retroactive inventory only; no new framework design |
| **KT-2** | Retroactive Cycle 1-15 inventory close (Branch 4.4) | <3 dormant-silent specs found | Halt + surface to Rex for paradigm re-disposition; problem may be lower-leverage than Cycle 10 anecdote suggested |
| **KT-3** | Forward apply at Cycle 16 mid-cycle (Branch 4.5) | n=3+ author rejections (acceptance criteria unclear OR same-cycle backlog unmanageable) | Either (a) registry shape needs structural refinement, OR (b) same-cycle default needs relaxation for specific spec types |
| **KT-4** | Branch 2.3 assessment + §4.3 build | "spec implemented" predicate requires structurally different gate primitive than "artifact exists" | New enforcement primitive class warranted; surface as paradigm-class scope expansion or proceed within cycle if scope still bounded |
| **KT-5** | Cycle 16 mid-cycle forward apply observation | ≥2 NEW dormant-silent specs accumulate during Cycle 16 itself | H_main REFUTED; FINDINGS Layer 5 honest-gap + paradigm escalation candidate |

---

## §3 Gap Identification

<!-- gate:research_question_spec §3 entries:1 -->

| # | Gap Description | Evidence of Gap | Gap Type |
|---|---|---|---|
| 1 | No per-spec registry exists in the pipeline's data substrate (`singularity.db` schema enumeration) that tracks: spec_id + spec_type + owner + acceptance_criteria + target_session + current_status (5-state) + cycle_authored + session_authored + cycle_implemented + session_implemented + runtime_emit_event_class + dormancy_detection_threshold_sessions + deferral_reason + rex_authorization_for_deferral_past_cycle_close + audit_trail_link. The schema fields (per Cycle 16 SI §4.1 Amendment 2026-05-27a) are NOT in `prompt_inventory` (which tracks only agent specs at coarse grain) or any other singularity.db table. | OBS-4 (DB schema enumeration); Cycle 16 SI L60-L70 explicit TBD per §2 substrate audit | tried with wrong method (the pipeline uses per-cycle FINDINGS + per-cycle SI + INFRASTRUCTURE_INDEX.md as proxies; all 3 surfaces are coarser than per-spec rows AND none has a structural BLOCKING gate at cycle-close that fires on dormancy) |
| 2 | No structural BLOCKING gate fires at session-close that detects specs whose `runtime_emit_event_class` has not fired within ≤3 sessions of authoring. The Cycle 14 four-gate fires at cycle close (one surface); Cycle 16 SI L66-L67 explicit requirement is TWO surfaces (cycle-close + session-close). | OBS-5 (`k_register_present_gate.sh` source inspection lines 14-17 — gate body checks artifact existence + placeholder zero + ≥1 §N.1.M H-disconfirmation subsection; does NOT check runtime emit firing); Cycle 16 SI L64-L67 explicit TWO-surface requirement | nobody tried (no prior cycle attempted session-close-grain BLOCKING — Cycle 14 four-gate is cycle-close-only) |
| 3 | The 5-state spec lifecycle taxonomy (running / dormant-with-explicit-deferral / dormant-silent / killed / long-running per Amendment 2026-05-27a) does not exist as a structured state-machine in pipeline substrate. Existing surfaces use ad-hoc free-text "completed" / "in-progress" / "deferred" without machine-checkable structural state OR audit trail linkage. | OBS-3 (INFRASTRUCTURE_INDEX.md 4-of-9 specs missing — no structural state-machine); Cycle 16 SI L27-L33 explicit 5-state taxonomy | tried in wrong domain (state-machine discipline well-established in feature-flag governance — LaunchDarkly: Live / Ready for code removal / Ready to archive / Archived / Deprecated — and in ADR lifecycle — Proposed → Accepted → Deprecated / Superseded; not yet imported to AI-agent-engineering-methodology spec lifecycle) |
| 4 | No retroactive scan mechanism exists to enumerate every spec authored Cycles 1-15 + classify each into the 5-state taxonomy + identify dormant-silent specs + trigger owner-triage workflow. The retroactive surface is Branch 4.4 of Cycle 16 SI L70-L72; this gap is the ONLY surface where the retroactive scan can fire. | Cycle 16 SI L70-L72 (Branch 4.4 explicit gate fires once against Cycle 1-15 inventory at Cycle 16 mid-cycle); no existing infrastructure supports this | nobody tried (Cycle 1-15 didn't have per-spec registry, so retroactive scan can't fire until registry ships in Cycle 16) |

<!-- /gate:research_question_spec §3 -->

> [SEED: min_gap_citations=1]
> Cite specific evidence: a paper that stops short, a tool that doesn't exist,
> a problem that remains unsolved. "No one has done X" requires evidence that
> you searched and didn't find it.

---

## §3b Precision Escalation

<!-- source: Track 1, U4/priority 2 — 4/7 papers (UNDER-EVIDENCED) -->

> [SEED: precision_escalation — 4/7 evidence, likely universal but under-evidenced]
> This methodology prompt is based on 4 of 7 breakthrough papers studied (AlphaFold,
> Chetty, Bell, VAR). The remaining 3 (Watermark, GNoME, Milkman) posed new questions
> rather than escalating existing ones. The evidence base is weaker than U1 (7/7) or
> U2 (7/7) — treat this as a strong candidate pattern, not a confirmed universal.
> Phase B should validate with additional papers before encoding with full confidence.

State the current best version of this question as answered by the field's strongest
prior work:

| Current best answer in the field | Its precision / resolution / scale | Source |
|---|---|---|
| Wrapper-program Bindings 1+2 + RP-discipline-at-Stage-0-4 + Coach-discipline + per-cycle FINDINGS review | Per-cycle grain (~1-2 weeks per cycle) with author-discretion + reviewer-discretion → ~5-cycle drift observed in Cycle 10 telemetry case | strategic_frame.md Bindings 1-8 + Cycle 16 SI L13 Cycle 10 telemetry case |
| Cycle 14 four-gate methodology (`k_register_present_gate.sh` etc.) | Cycle-close-grain + artifact-existence predicate (not implementation predicate) | Cycle 14 SI Amendment 2026-05-24c done-criterion #8(g)+(h) + ~/ml-governance-templates/scripts/ |
| Per-flag stale detection (LaunchDarkly / GrowthBook / Optimizely) — analog from feature-flag governance | Day-grain (LaunchDarkly: 30 days + 7 days; GrowthBook: 14 days; Optimizely: 30 days) | LaunchDarkly Flag Health docs + GrowthBook Stale Feature Flag Detection docs + Optimizely Flag Status docs |

What 10× increase in precision, resolution, or scale would transform this question's
impact?

| Dimension escalated | Current level | Your target level | Why this transformation matters |
|---|---|---|---|
| Temporal resolution (detection grain) | Per-cycle (~weekly) — even at gate-close, only fires once per cycle | Per-session + ≤3-session threshold (sub-cycle granularity via runtime emit detection at session-close gate per Amendment 2026-05-27a) | The Cycle 10 telemetry case had its dormancy invisible because the cycle-close-grain measurement was made AT THE WRONG TIME (after cycle 10 close, the spec was "merely deferred to cycle 11"; after cycle 11 close, "merely deferred to cycle 12"; chain repeats 5 cycles). Sub-cycle granular detection (≤3 sessions = ~2 weeks at typical pipeline cadence) catches dormancy before the "merely deferred" rationalization compounds. |
| Coverage (specs tracked / specs authored) | Partial / ad-hoc — INFRASTRUCTURE_INDEX captures 4 of 9 agent specs (44%); cycle-close FINDINGS capture varies | 100% per Cycle 16 SI Done definition #1 ("Spec inventory complete: every spec across Cycles 1-15 enumerated") + forward-apply per #7 | At <100% coverage, dormant-silent specs are unreachable by the gate by definition. The retroactive scan (Branch 4.4) only fires meaningfully if 100% coverage is achieved during scan; otherwise the gate is structurally PASS for invisible specs. |
| State precision (status fidelity) | Binary or 2-3 state ad-hoc ("done" / "in progress" / "deferred") | 5-state taxonomy with structural transitions (running / dormant-with-explicit-deferral / dormant-silent / killed / long-running per Cycle 16 SI L27-L33) | The 2-3 state representation collapses "dormant-with-explicit-deferral" + "dormant-silent" + "long-running" into one bin ("deferred") — making the distinguishing dimension between failure-mode (silent) and legitimate exception (explicit-deferral) invisible. 5-state precision is what allows the gate body to fire on `current_status == 'dormant-silent'` while passing legitimate `dormant-with-explicit-deferral` rows. |

> Chetty escalated geographic resolution 100× (commuting zone → census tract).
> Bell escalated experimental rigor (close ALL loopholes simultaneously, not one
> at a time). AlphaFold escalated accuracy on the hardest cases (GDT ~40 → 92.4
> on template-free targets).
>
> **Self-test:** If your question is the same as the current best but with more data,
> it's a scale-up — valuable but not a new question. If it asks something the current
> best CAN'T answer at ANY scale, it's a new question. Which is yours? Both are valid
> research directions, but they require different designs and make different claims.

---

<!-- amendment_2026_05_28a_extension_start -->

## §3.recovery H_recovery_1..9 Hypothesis Pre-Registration + KT-7..KT-11 Evidence Schemata (Cycle-16-S9 RP fill per SI Amendment 2026-05-28a + 2026-05-28b)

<!-- source: kc-48 PD §2.2 Cycle-16-S9 RP fill scope + dispatch substrate §7 RQS §3 H_recovery pre-registration scope -->
<!-- source: SI Amendment 2026-05-28a Done #11-#16 + Amendment 2026-05-28b Done #17-#19 verbatim -->
<!-- source: kc-48 PD §5 paradigm escalation surfaces — KT-9 + KT-10 explicit -->
<!-- source: §6.recovery 10-discipline external grounding for probe-class behavioral verification methodology -->
<!-- source: memory binding `feedback_operational_definition_substitution.md` detection section — threshold language MUST be probe-fire-evidence-grounded, NOT registry-field/status enum/token count/citation count -->

**Discipline.** Per dispatch substrate §7 + §10 anti-patterns: each H_recovery row MUST be (a) hypothesis statement; (b) falsifiable threshold grounded in probe-fire evidence per §6.recovery.A external grounding (NOT registry-field / status enum / token count / citation count — those are HC #72 substitution candidates per memory `feedback_operational_definition_substitution.md` detection); (c) operational definition cross-referenced to ≥1 probe primitive from §6.recovery.A discipline rows; (d) kill threshold KT-7..KT-11 cross-reference where applicable.

**Anti-substitution self-discipline:** "X = implemented" / "X = closed" / "X = sufficient" / "X = present" operational claims that do NOT reference a named probe primitive FAIL §8 substitution-detection sweep at hand-back. RP self-checked at §8 pre-handback.

### §3.recovery.1 H_recovery_1..H_recovery_9 Pre-Registered Rows

| Row | Hypothesis Statement | Falsifiable Threshold (probe-fire-grounded) | Operational Definition (≥1 probe-primitive reference per §6.recovery.A) | Closes SI Done# | Kill-Threshold Cross-Reference |
|---|---|---|---|---|---|
| **H_recovery_1** | Probe-grounded measurement replaces heuristic 137 dormant-silent count: when the 4 probe primitives (Class A AgentContract / Class B Schema / Class C DesignDecision / Class D MethodologyCommitment) are exercised against all 235 cycle16:Spec entries, the dormant-silent count produced by probe-fire-aggregation differs from the BE-D heuristic 137 by ≥1 spec per class (i.e., probe-measurement is non-degenerate vs heuristic). | **Threshold:** probe-fire-evidence aggregation across 235 specs yields per-class measured dormant-silent counts {d_A, d_B, d_C, d_D} where ≥1 of {|d_A - 7|, |d_B - 2|, |d_C - 117|, |d_D - 11|} > 0; per-class confidence bounds (±CI from probe-self-test) reported; class concentration coefficient (Gini) reported alongside class skew. Substitution check: probe-fire-aggregation output JSONL row schema includes `evidence_type: probe_fire` field; NOT `evidence_type: citation_density` or `evidence_type: token_match`. | Class A probe = consumer-driven contract testing analog observing Agent-tool invocation events keyed by subagent_type (§6.recovery.A row 1 Pact + row 4 OpenTelemetry trace context + row 8 eBPF uprobe). Class B probe = property-based testing of schema validators at validation call site (§6.recovery.A row 2 Hypothesis + row 9 BX/oasdiff drift detection). Class C probe = ADR-to-code dependency-graph embodiment scanner with `git grep` of must-clauses + LLM-judge component (§6.recovery.A row 5 Bazel Skyframe + row 9 BX). Class D probe = citation-and-application scanner across session warmups + FINDINGS Layer 5 with trace_id linkage (§6.recovery.A row 4 OpenTelemetry trace context + row 10 SLSA in-toto Statement predicateType=cycle16:probe_fire_v1). | Done #11 | KT-7 (probe ships without passing self-test → halt); KT-10 (probe-coverage at FINDINGS shows zero production fires → H_main_recovery REFUTED candidate) |
| **H_recovery_2** | Write-boundary closure HC-BE-D-1 via pre-commit hook + filesystem watcher + `forward_apply_emit` wiring into `register_spec()` + 3-registry reconciliation gate eliminates the bypass path: post-Done-#12 ship, zero new spec-class file writes land in the codebase without a corresponding `register_spec()` call landed in the same commit OR a `spec_authoring_event` emitted by the filesystem watcher within ≤60 seconds. | **Threshold:** during ≥3 sessions post-Done-#12-ship, monitoring at 3 surfaces yields: (a) pre-commit hook intercept rate ≥99% on a curated test bed of write-class operations (including direct file edits + git commits + temp-path materializations); (b) filesystem watcher (fsnotify on Linux) emits `spec_authoring_event` for all writes that bypass git within ≤60 seconds delivery latency (per fsnotify event delivery semantics: "When a file is removed a Remove event won't be emitted until all file descriptors are closed"); (c) 3-registry reconciliation gate at session close flags zero three-way drift instances (filesystem + KG + `prompt_inventory` agree on spec inventory). | Pre-commit hook = git pre-commit framework analog (§6.recovery.A row 7 Anthony Sottile pre-commit). Filesystem watcher = fsnotify/inotify cross-platform abstraction (§6.recovery.A row 7 github.com/fsnotify/fsnotify). 3-registry reconciliation gate = admission control pattern (§6.recovery.A row 6 OPA Gatekeeper validating webhook composition across 3 sources). `forward_apply_emit` wiring into `register_spec()` = BE-B/BE-E composition with PRODUCTION caller path (NOT smoke-only `be_e_smoke_*` test_bed). | Done #12 | KT-8 (Substitution Gate predicate string-matches probe ID instead of importing-and-executing → halt for refactor — applies broadly to gate predicates including write-boundary admission rules) |
| **H_recovery_3** | Probe-library-as-canonical-vocabulary at govML `scripts/probes/<class>/<primitive_id>.py` lands as code (NOT markdown) with per-primitive self-tests against known-good + known-bad fixtures; library admission is gated on passing self-test; modifications require Builder-ARCH paradigm dispatch. | **Threshold:** at Done #13 ship, `~/ml-governance-templates/scripts/probes/` directory contains ≥4 probe primitives (one per Class A/B/C/D); each primitive has: (i) Python module file; (ii) `self_test_known_good_*.py` fixture; (iii) `self_test_known_bad_*.py` fixture; (iv) self-test execution emits PASS/FAIL JSONL event; (v) library admission script (`probe_library_admission.sh`) rejects primitives with failing self-test. Mechanical check: `find ~/ml-governance-templates/scripts/probes/ -name "*.py" \| wc -l` ≥ 4 primitive files + ≥8 fixture files + 1 admission script + 1 admission event sink. Generic-emission escape primitives ABSENT at admission scan (KT-9 firing on proposal). | Property-based testing canonical strategy library pattern (§6.recovery.A row 2 Hypothesis strategies as the canonical vocabulary). Supply-chain provenance Statement predicateType registry pattern (§6.recovery.A row 10 in-toto v1.0 spec predicate types). Mutation testing self-test discipline (§6.recovery.A row 3 known-good + known-bad fixture distinction = killed-vs-survived). | Done #13 | KT-7 (primitive ships without passing self-test → halt for repair); KT-9 (generic-emission escape primitive proposed → paradigm escalation; Rex disposes at Builder-ARCH boundary) |
| **H_recovery_4** | Operational-Definition Substitution Gate at Stage 1 RQS R3 close-eval + Stage 4 ED R3 close-eval + Stage 4 ACCEPTANCE_CRITERIA close-eval is a runnable script that IMPORTS and EXECUTES the named probe primitive at gate-fire time and verifies executable + passing self-test; predicates resolving to "field value equals enum" / "artifact exists at path" / "token count ≥ N" / "emission record exists" without a probe reference FAIL the gate. | **Threshold:** post-Done-#14 ship, gate body at Stage 1+4 closes is structurally `subprocess.run(["python3", probe_primitive_path, "--self-test"])` followed by `assert exit_code == 0` AND assertion that the operational definition string contains a `probe_primitive_id::` reference; mechanical check at gate-fire time. KT-8 fires if implementation string-matches probe ID instead of importing-and-executing. Self-validation at Cycle-16-S10 RP fill itself: §3.recovery rows above MUST pass the gate when applied (RP dogfoods at S10 onward). | Mutation testing as predicate-shape (§6.recovery.A row 3 stryker killed-vs-survived); contract testing provider verification at gate-time (§6.recovery.A row 1 Pact `can-i-deploy`). | Done #14 | KT-8 (Substitution Gate predicate string-matches probe ID instead of importing-and-executing → halt for refactor) |
| **H_recovery_5** | Structural-prevention 9-piece layer (per Amendment 28a #15a-g + 28b #17/#18/#19 additions) lands as 9 distinct gate scripts + 1 reality-vs-intent table template + 1 design-anchor disclosure section template + 1 deferral-expiration policy at govML scripts/structural_prevention/; each component fires mechanically at its declared surface. | **Threshold:** at Done #15 ship verified via 9 mechanical checks: (a) Stage 0 probe-presence check script — exits non-zero if probe primitives absent; (b) Stage 1 RQS R3 + Stage 4 ED R3 reality-vs-intent gate — fails close if mandatory structured table absent or incomplete; (c) number-tagging gate at Rex-facing surfaces — fails close if any heuristic-tagged number appears in a Done-criterion verdict; (d) probe-coverage gate at FINDINGS close — fails if any spec class shows zero PRODUCTION probe fires (smoke-only fires explicitly rejected per Done #15d); (e) probe library self-test gate at every session close — auto-deprecates primitives failing 2 consecutive sessions; (f) deferral-expiration gate — fails if any spec deferred past authoring cycle close lacks named target session / reason / re-activation condition / maximum dormancy window; (g) design-anchor disclosure gate at LANDSCAPE close — fails if load-bearing mechanism design elements not tagged external-anchored vs internally-inherited; (h) cycle-close BLOCKING gate upgrade (Done #17 absorbed into structural-prevention layer); (i) kill discipline mechanism (Done #18 absorbed into structural-prevention layer). Each gate emits event_class to JSONL sink. | Each component grounds in distinct §6.recovery.A row per design-anchor table at §6.recovery.C; cross-class composition via gate-script framework (admission control pattern §6.recovery.A row 6 + filesystem hooks row 7 + supply-chain provenance row 10). | Done #15 (and absorbs Done #17 + #18) | KT-7 + KT-8 + KT-10 + KT-11 collectively (any structural-prevention component shipping with self-test failure / string-match substitution / zero production coverage / LOCKED-body modification fires the relevant KT) |
| **H_recovery_6** | govML v2.8.6 ADDITIVE-APPEND chain extension n=5→6 back-ports probe library + Substitution Gate + structural-prevention 9-piece layer; every freshly-scaffolded build-type project inherits at scaffolding time. | **Threshold:** post-Done-#16 ship, `git log --follow ~/ml-governance-templates/VERSION` shows v2.8.5 → v2.8.6 transition + CHANGELOG.md entry under v2.8.6; `init_project.sh` contains 3 new `install_*` function calls (`install_probe_library_canonical_vocabulary` + `install_operational_definition_substitution_gate` + `install_structural_prevention_layer`); `templates/build/probes/` + `templates/build/structural_prevention/` directories exist; LOCKED bodies of prior install functions (v2.8.2 runtime_emit + v2.8.3 spec_registry + v2.8.4 spec_implementation_gates + v2.8.5 forward_apply_observation) UNMODIFIED per ADDITIVE-APPEND chain discipline (`git diff v2.8.5..v2.8.6 -- 'install_runtime_emit*'` returns 0 line-modifications). Smoke test: `scaffold_research_project.py --research-type build --profile research-build` on a fresh project materializes all 5 govML versions including v2.8.6 components. | govML ADDITIVE-APPEND chain inheritance (substrate-layer per §6.X.2 refined metric); each install function content externally grounded per §6.recovery.C. | Done #16 | KT-11 (govML back-port modifies LOCKED bodies → halt for re-do per HC #45 ADDITIVE-APPEND precedent class strict) |
| **H_recovery_7** | Cycle-close BLOCKING gate upgrade to probe-fire predicate: gate-script body replaced from registry-field SPARQL ASK to probe-fire-evidence aggregation; hard block on missing probe fires for any spec authored in-cycle; accepts `killed` (Done #18) OR `dormant-with-explicit-deferral` with Rex authorization + named target session + re-activation condition + maximum dormancy window as valid terminal states. | **Threshold:** post-Done-#17 ship, `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` body invokes `python3 ~/ml-governance-templates/scripts/probes/<class>/<primitive>.py --aggregate-cycle <N>` (NOT `curl ... SPARQL ASK`); JSONL event emit shows `event_class: spec_implementation_present_gate.probe_fire_aggregate.fire.event` (NEW class) and event payload `evidence_type: probe_fire_aggregate` field PRESENT; gate fires BLOCKING (exit code != 0) if any spec authored in-cycle lacks ≥1 probe-fire record. Smoke test: gate fires correctly on a Cycle 16 spec-class fixture set with simulated missing probe fires; gate passes correctly on Cycle 16 spec-class fixture set with complete probe fires + 1 spec in `killed` state + 1 spec in `dormant-with-explicit-deferral` state with Rex authorization + named target session + re-activation condition + max-dormancy-window. | Admission control patterns (§6.recovery.A row 6 OPA Gatekeeper validating webhook fail-closed semantics). Supply-chain provenance verification predicate (§6.recovery.A row 10 SLSA Verification Summary Attestation as verification-predicate-at-chain-of-custody). | Done #17; SI disjunct (b) "implemented running code by the close of the authoring cycle (default)" | KT-7 + KT-8 (probe primitives invoked by gate body MUST have passing self-tests AND must be imported-and-executed, not string-matched) |
| **H_recovery_8** | `kill_spec(spec_iri, adr_retraction_ref, killing_session, kill_reason)` function in `scripts/spec_registry_authoring.py` validates ADR-style retraction reference exists in DECISION_LOG + emits `spec_killed_event` + SPARQL UPDATE transitions `cycle16:currentStatus` to `cycle16:killed` + records retraction reference at `cycle16:auditTrailLink`; refuses on missing ADR per DP#44. | **Threshold:** post-Done-#18 ship, `scripts/spec_registry_authoring.py` contains `kill_spec()` function with 4-positional-args signature; function body: (a) validates `adr_retraction_ref` resolves to an extant ADR entry in DECISION_LOG (mechanical check: `grep -E "^## ADR-${adr_retraction_ref}" docs/DECISION_LOG.md` returns non-empty); (b) emits `spec_killed_event` JSONL row with payload containing all 4 args + timestamp; (c) executes SPARQL UPDATE setting `cycle16:currentStatus` to `cycle16:killed` AND `cycle16:auditTrailLink` to the ADR reference; (d) refuses with `ValueError` if any arg is None OR if ADR validation fails (DP#44 BINDING). Smoke test against known-good fixture (valid ADR) passes; smoke test against known-bad fixture (missing ADR) raises ValueError + emits no event. Empirical baseline: Cycle 16 BE-D found 0 specs in `killed` state across 4 classes — kill discipline broken at workflow layer. Done #11 owner-triage routes "kill this spec" decisions through `kill_spec()`. | ADR governance lifecycle (LANDSCAPE §1 row 6 Nygard 2011 + Tyree-Akerman 2005 Proposed→Accepted→Deprecated/Superseded immutability post-acceptance). Supply-chain provenance chain-of-custody for retraction event (§6.recovery.A row 10 SLSA + in-toto). | Done #18; SI disjunct (d) "explicitly killed with audit trail" | KT-7 (kill_spec smoke test fixture must pass self-test before admission) |
| **H_recovery_9** | ≤3-session dormancy threshold preservation: post-recovery, the existing BE-C session-close ADVISORY gate `spec_implementation_session_close_gate` threshold check continues to fire correctly on PROBE-FIRE evidence (NOT on registry-field evidence); regression where the threshold reads `cycle16:currentStatus` registry field instead of probe-fire-aggregation triggers KT-8 firing. | **Threshold:** at Cycle 16 TRUE-close FINDINGS, verification block reports: (a) `spec_implementation_session_close_gate` event sink at `outputs/spec_implementation_gates_events.jsonl` shows event_class `spec_implementation_session_close_gate.probe_fire_aggregate.fire.event` (NEW; replaces or co-exists with prior `spec_implementation_session_close_gate.fire.event`); (b) payload includes `evidence_type: probe_fire_aggregate` field PRESENT; (c) `dormant_specs_exceeding_threshold_count` field is derived from per-spec probe-fire-evidence aggregation across the last `dormancy_detection_threshold_sessions` (=3) sessions, NOT from SPARQL ASK on `cycle16:currentStatus`; (d) `current_session_index` advances correctly per session-close; (e) `advisory_mode_bool: true` preserved (advisory at Cycle 16; BLOCKING at Cycle 17+ per kc-44 Amendment 2026-05-27a deadline framing). | Feature-flag stale-detection (LANDSCAPE §1 row 5 LaunchDarkly 30d/7d + GrowthBook 14d + Optimizely 30d temporal-threshold discipline). Mutation testing surviving-mutant analog (§6.recovery.A row 3 — a threshold that doesn't fire on real dormancy is a surviving mutant in the gate suite). | Done #19; SI disjunct (e) "structural detection of dormancy within ≤3 sessions of authoring via the runtime emit mechanism" | KT-8 (regression where threshold reads registry field instead of probe-fire-aggregation → halt for refactor) |

**H_recovery row count verification:** 9 rows authored (H_recovery_1..H_recovery_9). Mechanical check: `grep -c "^| \*\*H_recovery_" §3.recovery.1` returns 9. Per kc-48 PD §2.2 + dispatch substrate §7 + Amendment 2026-05-28a Done #11-#16 + Amendment 2026-05-28b Done #17-#19 verbatim coverage: 9 hypothesis rows × 9 Done# items (Done #11/12/13/14/15/16/17/18/19) — full coverage.

### §3.recovery.2 KT-7..KT-11 Evidence Schemata Pre-Registration

| Trigger | Detection Point | Firing Condition (empirical predicate) | Evidence Schema (probe-fire JSONL row shape) | Refute Branch (what falsifies the KT firing) | Disposition on Fire |
|---|---|---|---|---|---|
| **KT-7** | At BE-F probe library admission (Cycle-16-S10+ Stage 5) + at every session close (Done #15e auto-deprecation check) | Probe primitive ships without passing self-test against known-good + known-bad fixtures (i.e., `subprocess.run([primitive_path, "--self-test"]).returncode != 0`) | `{"event_class": "probe_library_self_test.fail.event", "schema_version": "0.1", "timestamp": ISO8601, "run_id": <uuid>, "payload": {"primitive_id": <id>, "primitive_path": <path>, "fixture_set": "known_good_*.py + known_bad_*.py", "exit_code": <int>, "stderr_excerpt": <str>, "consecutive_failure_count": <int>}}` | Self-test passes (exit_code == 0) on both known-good AND known-bad fixtures (NOT just known-good); manual verification by Builder-ARCH at admission boundary | Halt-and-surface for repair before admission; if already-admitted primitive fails 2 consecutive sessions, auto-deprecate (Done #15e); block session close until repair via Builder-ARCH dispatch OR removal via paradigm disposition |
| **KT-8** | At Operational-Definition Substitution Gate fire-time (Stages 1+4 R3 close-eval) | Gate predicate body string-matches probe primitive ID instead of importing-and-executing (i.e., gate body contains `if "probe_xyz" in operational_definition_string:` rather than `subprocess.run([probe_path, ...])`) | `{"event_class": "operational_definition_substitution_gate.string_match_substitution_detected.event", "schema_version": "0.1", "timestamp": ISO8601, "run_id": <uuid>, "payload": {"gate_path": <path>, "violation_line": <int>, "violation_snippet": <str>, "expected_pattern": "subprocess.run+probe_path", "actual_pattern": "string_match"}}` | Gate body inspection shows `subprocess.run` or `importlib.import_module` invocation chain executing the probe + assertion on probe's structured output (NOT a string presence check on the operational definition text) | Halt-and-surface for gate refactor before next R3 close-eval admits; block downstream Stage 5 build until gate body executes the primitive |
| **KT-9** | At BE-H probe library design review (Cycle-16-S10+) + at any probe-library-modification dispatch (Done #13) | Generic-emission escape primitive proposed (e.g., a "passes when any emit event of any class fires" primitive that bypasses behavioral verification) | `{"event_class": "probe_library_design_review.generic_emission_escape_proposed.event", "schema_version": "0.1", "timestamp": ISO8601, "run_id": <uuid>, "payload": {"proposed_primitive_id": <id>, "proposer": <role>, "proposed_predicate_body_excerpt": <str>, "escape_class": "generic_emission" / "any_event" / "smoke_acceptable" / "metadata_only", "rex_disposition_required_bool": true}}` | Proposed primitive predicate body inspects observable behavioral surface specific to the spec class (NOT a generic any-emit-event accept) | **Paradigm escalation per kc-48 PD §5.** Builder-ARCH paradigm boundary; Rex disposes. Per `feedback_operational_definition_substitution.md` residual-risks: "Library could grow generic-emission escape primitives — Rex must refuse at Builder-ARCH paradigm boundary." Do NOT dispose operationally |
| **KT-10** | At Cycle 16 TRUE-close FINDINGS authoring (post-Done #11-#19 ship) | Probe-coverage check at FINDINGS shows zero production fires on any spec class (i.e., for ≥1 of {Class A, Class B, Class C, Class D}, the per-class production-probe-fire count is 0) — recovery cycle has reproduced the meta-failure | `{"event_class": "findings_probe_coverage_check.zero_production_fires.event", "schema_version": "0.1", "timestamp": ISO8601, "run_id": <uuid>, "payload": {"class_with_zero_fires": ["Class_A" | "Class_B" | "Class_C" | "Class_D"], "smoke_fires_present_bool": <bool>, "smoke_run_id_prefix": "be_e_smoke_*" / "probe_lib_self_test_*", "production_fires_count_per_class": {"A": <int>, "B": <int>, "C": <int>, "D": <int>}, "h_main_recovery_refuted_candidate_bool": true}}` | Per-class production probe-fire count > 0 for all 4 classes; smoke fires explicitly distinguished by `run_id` prefix (NOT counted as production) | **H_main_recovery REFUTED candidate.** Halt-and-surface for paradigm re-disposition per kc-48 PD §5. Recursive meta-failure: the recovery cycle has reproduced the substitution pattern at its own close. FINDINGS Layer 5 honest-gap entry. Rex disposes — possible disposition: extended Phase 8 / paradigm-class scope expansion / Cycle 17+ scope inheritance |
| **KT-11** | At Done #16 govML v2.8.6 ADDITIVE-APPEND back-port commit (Cycle-16-S10+ Stage 5 BE-I) | govML back-port modifies LOCKED bodies of prior install functions (v2.8.2 runtime_emit / v2.8.3 spec_registry / v2.8.4 spec_implementation_gates / v2.8.5 forward_apply_observation) | `{"event_class": "govml_additive_append_chain.locked_body_modification_detected.event", "schema_version": "0.1", "timestamp": ISO8601, "run_id": <uuid>, "payload": {"locked_function_modified": <name>, "version_at_lock": "v2.8.2" / "v2.8.3" / "v2.8.4" / "v2.8.5", "modification_line_count": <int>, "git_diff_excerpt": <str>, "hc_45_additive_append_precedent_violation_bool": true}}` | `git diff <prior_lock_commit>..HEAD -- '<locked_install_function_paths>'` returns 0 line-modifications; LOCKED bodies physically unchanged; only NEW function additions in `init_project.sh` + NEW directories under `templates/build/probes/` + `templates/build/structural_prevention/` | Halt for re-do per HC #45 ADDITIVE-APPEND precedent class strict. Revert LOCKED-body modifications; reauthor as ADDITIVE-APPEND only (NEW install function for v2.8.6, NEVER modification to prior install function body) |

**KT-7..KT-11 schemata count verification:** 5 KT rows authored (KT-7 / KT-8 / KT-9 / KT-10 / KT-11). Mechanical check: `grep -c "^| \*\*KT-" §3.recovery.2` returns 5. Each row has all 5 required fields (Detection Point / Firing Condition / Evidence Schema / Refute Branch / Disposition on Fire). KT-9 paradigm-class disposition (Rex disposes at Builder-ARCH boundary) explicitly per kc-48 PD §5 + memory `feedback_operational_definition_substitution.md` residual-risks. KT-10 recursive-meta-failure disposition (H_main_recovery REFUTED candidate) explicitly per dispatch substrate §7.

<!-- amendment_2026_05_28a_extension_end -->

---

## §4 Assumption Challenge

<!-- gate:research_question_spec §4 entries:1 -->

| # | Assumption the Field Holds | Sources Holding This Assumption | Contradiction Search Results | Why It Might Be Wrong |
|---|---|---|---|---|
| 1 | **Author-time discipline + periodic close-review = implementation guarantee for authored specs.** Common AI-agent-engineering-methodology practice (wrapper-program Bindings 1+2 implicit) is to assume that if RP/Coach/Rex authoring discipline is good, and per-cycle close-reviews are conducted, authored specs will become running code. | (1) Wrapper-program strategic_frame.md Bindings 1-7 (2026-05-07 paradigm-class) — emphasize author-time discipline (Binding 1 external-research ≥80%; Binding 6 Coach NEVER fills templates) without per-spec registry. (2) Cycle 10 RUNTIME_EMIT_SPEC.md authoring at BE#5+BE#6 (high author discipline) without runtime emit wiring at authoring time. | Search executed via WebSearch 2026-05-27 across multiple disciplines: IETF RFC 6982/7942 explicitly counter-evidences this assumption — "Improving Awareness of Running Code: The Implementation Status Section" exists BECAUSE author-time discipline alone is known-insufficient to ensure implementations exist. The IETF specifically introduced per-spec implementation-status tracking as an experiment. Python PEP 1 similarly carries per-PEP implementation-status through the Final-state lifecycle. LaunchDarkly Flag Health docs are entire products built on the assumption that author-time + close-review fails (else stale-flag detection would not be a product category). | Specifically because Cycle 10's case study refutes it (5-cycle gap despite high author discipline), and because 7 external disciplines independently arrived at the same compensating mechanism (per-spec lifecycle tracking + structural detection). 7-of-7 disciplines cannot be wrong simultaneously about whether author-discipline alone suffices. |
| 2 | **Behavioral instructions (CLAUDE.md, agent specs, role protocols) effectively shape AI agent behavior.** Common practice (across the wrapper program + extant AI agent frameworks) assumes that well-written behavioral instructions to agents reliably produce intended behavior. | (1) Wrapper-program Bindings 1-7 (re-asserted across all sessions through CLAUDE.md root inheritance). (2) Moonshots `.claude/agents/*.md` 9 agent specs (Anthropic agent ecosystem default discipline). (3) `feedback_*.md` 30+ entries in user memory (behavioral correction memory pattern). | Search executed 2026-05-27 across structural-vs-behavioral literature: `feedback_depth_over_speed.md` BINDING explicitly documents "Time budgets ignored by agents. Use structural depth requirements (quote N sources, read N full docs). +1.0 proven improvement." `feedback_blast_radius_anti_pattern.md` BINDING documents recurring streak (n=11 across S120 + S137 + S138) of behavioral instruction degrading under context-window pressure. DP#43-44 (refuse-on-missing-precondition) is explicitly a STRUCTURAL discipline because behavioral discipline alone fails. | Specifically because at session-N context length, behavioral instructions in §0 are progressively forgotten / re-interpreted / over-applied; while structural gates fire mechanically per-invocation regardless of context. Cycle 14 four-gate is precisely the structural answer to this assumption challenge; Cycle 16 extends it to spec-implementation predicate. |

<!-- /gate:research_question_spec §4 -->

> [SEED: min_papers_cited=2]
> Structure borrowed from EXPERIMENTAL_DESIGN Gate -1 A8 pattern.
> Name a specific assumption, cite ≥2 sources that hold it, document your
> search for contradicting evidence, and state why it might be wrong.
> "None found after searching [X], [Y]" is a valid contradiction search result.

### §4.1 Paradigm Challenge Assessment

<!-- source: Track 1, priority 2 — 5/7 papers -->

What methodological assumption does the field hold unquestioned? What happens if
you reverse it?

| Unquestioned assumption | What reversal looks like | What changes in your approach if reversed |
|---|---|---|
| **Specs are documentation; code is implementation; the two are necessarily distinct artifacts that drift over time.** This Parnas-acknowledged duality is the field's default frame — documentation rots because it is structurally separate from the code that supposedly implements it. | Reversed: specs ARE code (or specs ARE generated FROM code, or specs and code share a single source of truth). OpenAPI/Swagger contract-first design REVERSES the duality by making the OpenAPI spec the single source of truth from which client SDKs / server stubs / contract tests are GENERATED — drift becomes structurally impossible because there is no second artifact to drift against. | If reversed for THIS pipeline: methodology specs (agent contracts, schemas, design decisions, methodology commitments) would be expressed in a single executable form from which the AGENT BEHAVIOR is generated, not separately documented. This is the **paradigm-class Alternative 2** in §2 above — out-of-scope for Cycle 16's within-paradigm mechanism scope but reserved as KT-5 paradigm-escalation surface. The Cycle 16 mechanism is the **structural compromise**: keep specs as separate documents but bind them via per-spec registry + runtime-emit-event to running code such that drift surfaces structurally at session-close gate within ≤3 sessions. Within-paradigm Cycle 16 is the **first-iteration approximation**; full paradigm reversal is the longer-arc improvement target. |
| **The cycle-close review is the right granularity to detect dormant infrastructure.** This is the wrapper-program assumption inherited from per-cycle FINDINGS authoring discipline. | Reversed: the session-close is the right granularity (≤3-session emit detection per Amendment 2026-05-27a), and the cycle-close is too coarse to prevent dormancy from compounding. Each session is a unit-of-attention-allocation; spec dormancy at session-level compounds geometrically across sessions. | This IS the Cycle 16 reversal — Amendment 2026-05-27a tightened from "bounded cycles" → "same authoring cycle by default + ≤3-session runtime emit detection." Approach change: the Cycle 16 mechanism MUST fire at TWO surfaces (cycle-close gate AND session-close gate per SI L66-L67) — not one. Implementation: gate scripts run at both surfaces; session-close gate body scans registry for `runtime_emit_event_class` non-firing within `dormancy_detection_threshold_sessions` of authoring. |

> VAR: "Autoregressive generation must proceed token-by-token in raster order" →
> reversed to "autoregressive by SCALE, not by position." Bell: "Loopholes can be
> closed one at a time in separate experiments" → reversed to "all loopholes must
> be closed simultaneously in one experiment." Milkman: "Behavioral interventions
> should be tested one at a time by individual labs" → reversed to "test 54
> simultaneously in one megastudy."
>
> **Self-test:** If reversing this assumption doesn't change your approach, it's not
> a paradigm challenge — it's a conventional question. That's fine, but name it
> honestly. Conventional questions produce incremental advances. Paradigm challenges
> produce surprises. Both are needed; the experimental design differs.

### §4.2 Novelty Pre-Mortem

<!-- source: Phase F v2, N=5 in 3/3 cycles across 3 domains -->

Before proceeding: score your question's answer predictability.

| Level | Description | N Ceiling | Action |
|---|---|---|---|
| UNPREDICTABLE | No existing theory predicts the outcome. Expert consensus would disagree on the answer. | >=6 | Proceed. |
| PARTIALLY PREDICTABLE | Existing theory suggests the direction but not magnitude/specifics. | 5-6 | Produce 1 alternative question that targets the UNPREDICTABLE component. Document the trade-off. Coach reviews both before design proceeds. |
| PREDICTABLE | Existing theory, prior empirical work, or mathematical properties of the chosen method predict the outcome. An expert in the source domain could derive the answer without running the experiment. | <=5 | STOP. Produce 2 alternative questions that shift the answer into unpredictable territory. Re-run §2 comparison with alternatives. |

Self-score: PARTIALLY PREDICTABLE

If PREDICTABLE or PARTIALLY PREDICTABLE, what is the specific theory, result, or
mathematical property that makes the answer predictable?
The mechanism direction is partially predictable because 7-of-7 external disciplines independently arrived at the same composition (per-spec registry row + lifecycle state machine + structural detection of dormancy). The convergence across IETF + Python PEP + OpenAPI + DbC + LaunchDarkly + ADR + Parnas strongly suggests the mechanism CLASS will work — it is field-mature in 7 source domains. **What is NOT predictable**: (a) whether Cycle 14 four-gate pattern extends cleanly OR requires new primitive class (KT-4 firing); (b) whether the retroactive scan against Cycles 1-15 surfaces <3 specs (KT-2 firing → problem smaller than hypothesized → halt), 3-20 specs (typical hypothesized range), or >20 specs (much larger than expected); (c) whether forward-apply at Cycle 16 itself produces ≥2 NEW dormant-silent specs (KT-5 H_main REFUTED) — the within-cycle dogfooding test is genuinely open. The MECHANISM CLASS is partially predictable; the OUTCOMES (KT-1..KT-5 firing) span the full result space.

If PREDICTABLE: produce 2 alternative questions that shift the answer into
unpredictable territory:

| # | Alternative question | Why unpredictable | Trade-off vs current question |
|---|---|---|---|
| 1 | n/a — PARTIALLY PREDICTABLE level, only 1 alternative required per §4.2 spec ladder | n/a | n/a |
| 2 | n/a — PARTIALLY PREDICTABLE level, only 1 alternative required per §4.2 spec ladder | n/a | n/a |

If PARTIALLY PREDICTABLE: produce 1 alternative question that shifts the
unpredictable component into the primary question frame:

| Alternative question | What makes it less predictable | Trade-off vs current question |
|---|---|---|
| "Can the Cycle 16 structural mechanism (per-spec registry + 5-state taxonomy + TWO-surface BLOCKING gate + ≤3-session dormancy detection + retroactive Cycle 1-15 inventory) PREVENT the recurrence of dormant-silent specs at Cycle 16 itself — observable via dogfooding (≥0 NEW dormant-silent specs during Cycle 16) + retroactive surfacing of ≥3 historic dormant-silent specs across Cycles 1-15?" | The dogfooding component is genuinely unpredictable — KT-5 explicitly pre-registers ≥2 NEW dormant-silent specs accumulating during Cycle 16 itself as the H_main REFUTED trigger. The within-cycle prevention test cannot be predicted from external grounding alone — the pipeline's social/operational dynamics may either honor the new discipline or accumulate new dormant specs even with structural enforcement. | Trade-off: the alternative narrows the question from "structural-guarantee design" to "structural-guarantee dogfooding test." This more precise framing forces the cycle to MEASURE its own mechanism in-vivo, not just author it. The current question is broader (still includes mechanism design + retroactive inventory + 7-discipline external grounding); the alternative is the empirical-test-component of the broader question. **Disposition: keep the broader current question (Cycle 16 SI L11 verbatim) as primary; the alternative is the EMPIRICAL-TEST sub-component evaluated at Cycle 16 close per Done definition #7 ("Forward apply infrastructure in place... observation begins (≥2 subsequent cycles post-Cycle-16 close required for done-criterion #10 longitudinal verdict)").** The alternative is a refinement of the empirical-test surface, not a replacement for the broader research question. |

The purpose is NOT to abandon the current question — it's to force articulation
of a less-confirmatory alternative. The Coach or RP reviews both and selects
the stronger framing.

> [SEED: predictability_threshold=PARTIALLY_PREDICTABLE triggers 1 alternative,
> PREDICTABLE triggers 2 alternatives. Both require mandatory revision.
> Calibrated from 3 cycles: C1 gap predictable in retrospect (N=5), C2 result
> in pre-registered range (N=5), C3 Pastor-Satorras & Vespignani 2001 predicted
> SEIR degenerates on scale-free networks (N=5). All 3 would have scored
> PREDICTABLE on this scale. Post-Phase-B: 4/4 cycles scored PARTIALLY
> PREDICTABLE with no action triggered — this threshold added S75.]
>
> **Self-test:** If you scored UNPREDICTABLE, name one expert who would be
> SURPRISED by the answer. If you can't name one, reconsider your score.

---

## §5 Pipeline Signal Connection

<!-- gate:research_question_spec §5 required -->

Query the cross-engine view for scored hypotheses, capability gaps, and signal
clusters relevant to this question.

```
Run: sqlite3 ~/singularity.db "SELECT * FROM v_question_inputs;"
Paste results below:
```

Query executed 2026-05-27. 126 rows returned.

<!-- queried: v_question_inputs, 126 rows -->

Summary of relevant categories:

- **Scored hypotheses spanning prior cycles' research-question surfaces:** HSE-AUDIT-001/002/003 (agent serialization / supply chain / command injection — Cycles 1-2 audit framing); SH-001 through SH-007 (signal-experiment hypotheses for community engagement / PR contribution / vulnerability disclosure / blog content distribution / benchmark / landing page / interview); agent-semantic-resistance H-1 through H-6 (Cycle 3-4 framework injection); agent-vuln-triage H-1 through H-4 (Cycle 5+ EPSS comparison); framework-injection-taxonomy H-1 through H-4 (Cycles 11-12 cross-system); govml-agent-platform H-1 through H-3 (govML adoption); llm-patch-correctness H-1 through H-2.
- **No prior hypothesis tracks "specs authored never become running code" as a research surface.** All prior hypotheses are domain-research (agent security / vuln triage / framework injection) or operational-validation (signal experiments). The spec-implementation gap as a research question is **novel relative to the tracked hypothesis surface** — confirms Cycle 16 framing is upstream-novel.
- **No prior hypothesis tracks "internal infrastructure dormancy" as a research surface.** Cycle 7 supply-chain contagion hypotheses are most-adjacent (information-epidemiology / temporal-evolution / multiplex networks) but address EXTERNAL system contagion, not INTERNAL spec dormancy.

**Disposition.** The cross-engine question surface confirms Cycle 16's research question is novel relative to 126 prior tracked hypotheses. KT-5 paradigm escalation surface (if Cycle 16 structural mechanism fails) connects most naturally to organizational-singularity hypothesis classes (Cycle 8+ MSCS / cold-start signal experiments) — but is reserved for future-cycle escalation, not Cycle 16 scope.

<!-- /gate:research_question_spec §5 -->

---

## §5b Method History

<!-- source: agent spec §5b — methodologies table BS-score lookup + process_changes recent proposals -->

**Query 1:** `sqlite3 ~/singularity.db "SELECT method_name, source_domain, applied_domain, bs_score FROM methodologies ORDER BY bs_score DESC;"` — 18 rows.

| BS | Method | Source domain | Applied domain |
|---|---|---|---|
| 7 | Acemoglu financial contagion phase-transition framework | mathematical economics / systemic risk | AI supply chain security (intermediary topology) |
| 7 | Category design demand-creation/demand-capture classification at artifact granularity | business strategy / marketing (Ramadan et al. 2016 Play Bigger) | cold-start technical product distribution |
| 7 | social-immunity-remediation-response | behavioral ecology (social immunity) | AI agent security |
| 6 | Network controllability theory | network science | AI security (agent runtime) |
| 6 | Process isolation | Unix | agent security |
| 6 | mandatory access control | SELinux | agent security |
| 6 | circuit breakers | distributed systems | agent security |
| 6 | Broadcast contagion with time-dependent heterogeneous detection | information epidemiology / Nekovee et al. | AI supply chain security |
| 6 | Operating Characteristic curves for scanner evaluation | manufacturing quality assurance (ISO 2859-1) | agent security scanner evaluation |
| 6 | Parameterized ROC degradation analysis | SDT | mev ai agent security |
| 5 | SEIR/SIR/SEIS compartmental modeling | Pastor-Satorras & Vespignani 2001 | ai supply chain security |
| 4 | ATT&CK coverage mapping | cybersecurity (MITRE ATT&CK) | AI security (MITRE ATLAS governance gaps) |
| 4 | ISO 13485 methodology adaptation | ISO 13485 | FDA QSR |

**Cycle 16 method selection.** All Cycle 16 candidate methods (per-spec registry + 5-state lifecycle + structural gate + runtime emit) draw from **distinct source domains** never previously imported per BS history: IETF (network-protocols-community), Python PEP (programming-language-evolution), OpenAPI/Swagger (web-API-engineering), Design by Contract / Eiffel (formal-methods), DevOps feature-flag governance (SaaS-DevOps), ADR (software-architecture-enterprise), Parnas precise-documentation (software-engineering-safety-critical). **NONE of the 7 source domains appear in the prior 18-method BS history.** This is structural evidence the Cycle 16 methodology composition is genuinely cross-domain — projected BS score ≥7 (composes 7 distinct cross-domain imports, none of which appears in `methodologies` table). Final BS scoring deferred to ED Stage 3-4 RP fill + Verifier post-FINDINGS.

**Query 2:** `sqlite3 ~/singularity.db "SELECT proposal_type, target_dimension, proposed_change FROM process_changes WHERE accepted IS NULL OR accepted = 1 ORDER BY cycle_id DESC LIMIT 10;"` — 10 rows.

| Proposal type | Target dim | Proposed change (truncated) |
|---|---|---|
| execution_fidelity | R | Rigor=7 — ED §Statistical Plan specifies analyses not performed in FINDINGS. Were all specified analyses actually performed? |
| template_gap | G | Generalizability=5 BELOW THRESHOLD (6) — does the method have inherent generalizability limits? Check boundary statement honesty |

**Cycle 16 forward-application.** The execution_fidelity proposal class directly applies — Cycle 16's mechanism explicitly requires per-spec runtime emit firing within ≤3 sessions of authoring. **The Cycle 16 mechanism IS the structural answer to the execution_fidelity gap that process_changes already flags.** Template_gap (Generalizability) applies to forward-apply observation across ≥2 subsequent cycles post-Cycle-16-close (done-criterion #10) — generalization is structurally limited to AI-agent-built-systems engineering methodology, not field-general; FINDINGS Layer 4 will document explicitly.

---

## §6 Question Gate Checklist

Self-assessment before proceeding to Stage 2 (Landscape).

| # | Check | Status | Notes |
|---|---|---|---|
| 1 | Question statement in §0 is one sentence and traceable to observation | [x] | §0 verbatim from Cycle 16 SI L11 + Amendment 2026-05-27a; traceable to OBS-1 + OBS-4 + OBS-5 + OBS-6 + OBS-7 + PAT-1 |
| 2 | ≥1 observation linked in §1 with direct quote | [x] | 7 observation links (OBS-1 / OBS-2 / OBS-4 / OBS-5 / OBS-6 / PAT-1 / PAT-2), each with quoted signal/pattern |
| 3 | ≥2 alternatives documented in §2 with rejection rationale | [x] | 3 alternatives (continue rubric refinement; paradigm-class question; behavioral checklist) with full ADR-format rejection rationale + consequences |
| 4 | ≥1 gap cited with evidence in §3 | [x] | 4 gaps cited (no spec_registry table; no session-close gate; no 5-state taxonomy state-machine; no retroactive scan mechanism) with evidence per OBS-citations |
| 5 | ≥2 papers cited in §4 assumption challenge | [x] | Assumption #1 cited: RFC 6982/7942 + PEP 1 + LaunchDarkly Flag Health docs + Cycle 10 telemetry case. Assumption #2 cited: `feedback_depth_over_speed.md` + `feedback_blast_radius_anti_pattern.md` + Cycle 14 four-gate precedent + DP#43-44 |
| 6 | Pipeline signal connection queried in §5 (not placeholder) | [x] | v_question_inputs queried 2026-05-27 — 126 rows; canonical marker `<!-- queried: v_question_inputs, 126 rows -->` added at §5 |
| 7 | §4.2 Novelty Pre-Mortem completed — if PREDICTABLE, alternatives provided | [x] | PARTIALLY PREDICTABLE level scored; 1 alternative provided per ladder ("dogfooding empirical test sub-component" — kept current question as primary, alternative as refinement of empirical-test surface) |

> Gate script (`question_gate.sh`) validates checks 1-4, 6 as FAIL level.
> Check 5 is WARN level (per spec §3 Gate 1→2 check #6).
> Check 7 is WARN level (new — collecting data before escalating to FAIL).
