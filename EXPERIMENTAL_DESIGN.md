# Experimental Design: Cycle 16 — Close the spec-to-implementation gap

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- stage: 3 -->
<!-- source: Cycle 16 SI ACTIVE 2026-05-27 + Amendment 2026-05-27a (deadline-tightening) + Amendment 2026-05-27b (KG-primary registry storage) + substrate §7 ED scope + RP agent spec L324-L437 -->
<!-- gate:experimental_design §0-§4 required -->
<!-- gate:experimental_design §0a hybrid_primary_carry required -->
<!-- REQUIREMENT: KT-1..KT-6 binding into §4 Kill Shots + §Field 6 structural per substrate §4 STRUCTURAL BINDING -->
<!-- REQUIREMENT: §5+ filled by Build-Runner at Stage 5 (NOT in Dispatch 2 scope) -->

## §0 Authority Chain + Stage 3-4 Scope

Authority: Rex 2026-05-27 mid-Cycle-15 pivot + 2nd-pass deadline-tightening + 3rd-pass KG-primary storage authorization > Cycle 16 SI ACTIVE 2026-05-27 (`a2f14d5` + `be54a97` + `badd749`) > Cycle-16-S1 close `9300c86` (Stage 0-2 LOCKED + KT-1 DOES NOT FIRE ≈70%) > Cycle 6 substrate-as-governance-kernel PRIMARY thesis + Q-γ Option 2 unification 2026-05-13b > kc-44 PD §1.4 #1 + §3 + §6.1.

Stage 3-4 RP scope (this S2 dispatch): §0a + §0 Gate -1 + §1 Project Identity + §2 Novelty Claim + §3 Comparison Baselines + §4 Kill Shots + §4a Constraint-Driven Design Check + §Field 6 KT-1..KT-6 + §5 Statistical Plan + §6 Threats to Validity + §7 Pre-emptive Criticism + §8 Novelty/Impact/Generalization + §9 Cross-Domain. §5 Experimental Plan (Build-Runner per BE-class) + §6 Procedure + §7-§11 (Stage 5 fill) NOT in this Dispatch 2 scope per RP agent spec.

## §0a HYBRID PRIMARY VERBATIM CARRY (Source 1+2+3+4 LOCKED + Cycle 16 EXTENSION-3)

<!-- source: substrate §6 5-source CARRY chain by reference per HC #48 (c) compression discipline -->
<!-- gate:experimental_design §0a hybrid_primary_carry source_count:5 -->

**HYBRID PRIMARY is the binding pre-registration of EXPECTED-OUTCOME SHAPE** for this research line. Per Source 4 (Cycle 5 ED §0a L97-99+L113) CARRY DISCIPLINE VERBATIM: "no re-authoring; preserve HYBRID PRIMARY pre-registration. Semantic fidelity > stylistic edit."

**4 LOCKED canonical sources (reference by path; do NOT re-quote per HC #48 (c)):**

- Source 1: `/home/azureuser/cycle_1_engineering_methodology_for_agent_built_systems_research/docs/HYPOTHESIS_REGISTRY.md` §3a L105 — Rex S2 sharpening 2026-05-07 ORIGINAL.
- Source 2: `/home/azureuser/cycle_4_*/docs/RESEARCH_QUESTION_SPEC.md` §0a L45 — EXTENSION-1.
- Source 3: `/home/azureuser/cycle_5_*/docs/RESEARCH_QUESTION_SPEC.md` §0a L43 — EXTENSION-2.
- Source 4: `/home/azureuser/cycle_5_*/docs/EXPERIMENTAL_DESIGN.md` §0a L97-99 + L113 — CARRY DISCIPLINE (references Sources 1+2+3 explicitly).

**Cycle 16 EXTENSION-3 NEW (this S2 RP authoring; cross-ref HR §3a):**

HYBRID PRIMARY: BOTH satisfied → boundary-condition map per discipline AND per failure mode AND **per-spec × per-substrate-operation (registry-write / registry-read / cycle-close-gate-fire / session-close-gate-fire) × per-discipline-state (5-state taxonomy: running / dormant-with-explicit-deferral / dormant-silent / killed / long-running)** cell granularity — PRIMARY EXPECTED outcome shape per Rex S2 sharpening 2026-05-07 BINDING CARRY VERBATIM from 4 LOCKED sources + Cycle 4/5/6 extensions. Cycle 16 success metric = BOUNDARY-CONDITION-MAP RICHNESS at per-spec × per-substrate-operation × per-discipline-state cell granularity across 4 spec-classes × 4 substrate-operations × 5 discipline-states = up to 80 cells.

**Cell-granularity axes:**

- 4 spec-classes (Branch 1.2): agent contracts / schemas / design decisions / methodology commitments.
- 4 substrate-operations (Cycle 6 BE#1 KG-primary contract; Amendment 2026-05-27b): registry-write (SPARQL UPDATE INSERT DATA against `/cycle6` per nanopublication 3-graph triplet) / registry-read (SPARQL SELECT) / cycle-close-gate-fire (SPARQL ASK at cycle-close gate boundary) / session-close-gate-fire (SPARQL ASK at session-close gate boundary; ≤3-session dormancy threshold).
- 5 discipline-states (Amendment 2026-05-27a): running / dormant-with-explicit-deferral / dormant-silent / killed / long-running.

Total cell space = 80. Empirical sparsity acceptable; framework discriminative capacity for populated cells is the load-bearing measurement at FINDINGS Layer 3.

**Binding 2 strict:** Cycle 6 KG inheritance is mechanism-class inheritance (Q-γ Option 2 carried from BE#1 ship state) — NOT design anchor. Cell granularity derived from RQ + 4 branches + 5-state taxonomy + 4-substrate-operation enumeration; NOT mirror of Cycle 6 BE#1-#4 sequencing.

<!-- /gate:experimental_design §0a hybrid_primary_carry -->

## §0 Problem Selection Gate (Gate -1)

<!-- gate:experimental_design §0 problem_selection_gate required -->

| # | Criterion | Answer |
|---|---|---|
| 1 | **Research question** | Verbatim from Cycle 16 SI L11 + Amendment 2026-05-27a: "How do we structurally guarantee that every spec our pipeline writes — agent contracts, schemas, design decisions, methodology commitments — becomes implemented running code by the close of the authoring cycle (default), or gets explicitly deferred to a named target session with audit trail, or gets explicitly killed with audit trail — with structural detection of dormancy within ≤3 sessions of authoring via the runtime emit mechanism, and no silent drift?" |
| 2 | **Practitioner pain** | The wrapper-program EMABS pipeline itself — operating with 9 agent specs + ~100 cross-cycle methodology commitments + ~30+ design decisions + ~5 schemas across 15 cycles — has empirically observed the failure mode at canonical case (Cycle 10 RUNTIME_EMIT_SPEC.md: 5-cycle gap between BE#5+BE#6 authoring and Cycle-15-S7 runtime emission). Specific audience: AI-agent-built-systems engineering teams operating pipelines with ≥10 cycles' standing carrying ≥50 methodology specifications without per-spec lifecycle registry. Magnitude: at canonical case, 5-cycle dormancy = ~2.5 months pipeline cadence. |
| 3 | **Novel gap** | Per LA §1 LOCKED 7-discipline grounding: each discipline (IETF / Python PEP / OpenAPI / DbC / feature-flag governance / ADR / Parnas) encodes some variant of spec→implementation lifecycle tracking but NONE at AI-agent-built-systems engineering grain. LaunchDarkly is closest (LA §1 row 5) — per-flag lifecycle states + 30d/7d stale-flag detection at user-traffic-firing grain — but operates at runtime-active-flag grain, not at spec-emits-structural-event grain. RFC 6982/7942 carries implementation-status as voluntary peer-pressure; Cycle 16 makes it STRUCTURAL BLOCKING. Cycle 14 four-gate fires at cycle-close on artifact-EXISTS predicate; Cycle 16 extends to TWO surfaces (cycle-close + session-close) at spec-IMPLEMENTED predicate. The composition of all 7 disciplines into a unified 14-field schema (per kc-44 corrected count) targeting AI-agent-engineering-methodology grain is the cross-disciplinary contribution candidate. |
| 4 | **Feasibility** | yes — single research cycle ≤6 sessions per disposed paradigm question #1 envelope. Cycle 14 multi-BE precedent established 4-5 BE-class sessions for similar mechanism-class build. Stages 0-2 closed at S1; Stage 3-4 RP fill at S2 (this dispatch); Stage 5 BE-A..BE-E across S3-S6; close FINDINGS at S7 if needed (7th session requires Rex authorization for past-envelope slip per disposed paradigm question #1). |
| 5 | **Falsifiability** | KT-1..KT-6 pre-registered with full reversal disposition (per HR §3 + §Field 6). H_main REFUTED iff KT-5 fires (≥2 NEW dormant-silent specs mid-cycle OR Cycles 17-18 forward-apply). H1 REFUTED iff <N specs enumerable. H2 REFUTED iff ≥1 spec class lacks structural verifier (KT-4 surface). H3 REFUTED iff <3 dormant-silent at retroactive scan (KT-2 fires). H4 REFUTED iff counterfactual analysis at FINDINGS Layer 4 shows Cycle 16 mechanism would NOT have caught Cycle 10 case. H5 REFUTED iff substrate coverage <80% post Cycle 6 KG addendum (KT-1 inverse — disposition unchanged). H6 REFUTED iff gate predicate substitution requires new primitive class (KT-4 fires). H7 REFUTED iff ≥3 author refusals mid-cycle (KT-3 fires). H8 REFUTED iff ≥2 NEW dormant-silent specs mid-cycle OR Cycles 17-18 (KT-5 fires). |
| 6 | **Data availability** | LOCKED at S1 per LA §6 EDA Readiness data source sample verification: 9 agent specs at Moonshots `.claude/agents/*.md` (HC #52 broader scope per OBS-2 ls direct); ~5 schemas + 3 scripts/runtime_emit/ + 4 outputs/ JSONL sinks at scaffold; design decisions cross-cycle at DECISION_LOG.md (~30+); methodology commitments cross-cycle at FINDINGS Layer-5 (~50+ items); Cycle 6 KG substrate operational at `/cycle6` endpoint (246,048 quads / 46 graphs verified at 2026-05-27 Coach probe). |
| 7 | **Scope boundary** | Out-of-scope per Cycle 16 SI L91-L98: (a) new rubric dimensions beyond Cycle 13's five (Cycle 13 LOCKED); (b) modification of Cycle 13/14/15 LOCKED bodies (Binding 7); (c) deferred rubric-refinement scope from Cycle 15 Items 5-10 (Cycles 17-18 absorb per kc-44 renumbering); (d) full paradigm-class reversal of spec-vs-code duality (RQS §4.1 Alternative 2 — KT-5 paradigm escalation surface only); (e) ≤6-session envelope per disposed paradigm question #1. |
| 8 | **Success criteria** | 10 done-criteria per REQUIREMENTS §Deliverables 1-10: spec inventory (Cycle 1-15 retroactive) + pattern analysis (Cycle 10 counterfactual) + substrate audit (LA §6 addendum) + external research (S1 LOCKED) + KG-primary 14-field schema + SPARQL UPDATE authoring discipline + TWO-surface BLOCKING gate + retroactive scan fires (≥3 dormant-silent surfaces else KT-2) + forward-apply observation enabled + 5-layer close FINDINGS + paired commit. CONFIRMED / REFUTED / INCONCLUSIVE per HR §4. |
| 9 | **Kill conditions** | KT-1 (substrate ≥80%) → narrow to gap-filling only; KT-2 (<3 dormant-silent) → halt + Rex re-disposition; KT-3 (≥3 author refusals) → registry refinement OR same-cycle default relaxation; KT-4 (predicate requires new primitive class) → new enforcement primitive class warranted; KT-5 (≥2 NEW dormant-silent mid-cycle OR Cycles 17-18) → H_main REFUTED + paradigm escalation; KT-6 (Cycle 6 KG substrate-viability blocker) → fall back to SQL/YAML + Step 3.5 escalation. |
| 10 | **Prior art check** | LA §1 LOCKED 7 disciplines × ≥3 verbatim quotes each (36 total) + LA §1.2 cross-discipline convergence matrix + LA §1b 4-row adjacent field survey + LA §1.1 benchmark + LA §2 5-gap map + LA §6b.1 5-import cross-domain mechanism validity pre-check + LA §6b.2 6-row internal substrate cross-validation. |
| 11 | **Significance** | If H1-H8 collectively CONFIRMED + KT-1..KT-6 do not fire negatively + ≥2-cycle forward-apply shows 0 NEW dormant-silent specs, the wrapper-program EMABS gains its structural answer to the documentation-active-vs-code-active gap framed at AAEM cycle 1 closure. Per-spec KG registry schema (14 fields) becomes a candidate cross-disciplinary benchmark schema for spec-implementation governance in AI-agent-built systems. If REFUTED (KT-5 fires), RQS §4.1 Alternative 2 (specs ARE code; spec/code single source of truth) becomes the candidate forward-cycle paradigm escalation surface. |
| 12 | **Disconfirming evidence** | Per RQS §4 Assumption Challenge: searched WebSearch 2026-05-27 for evidence AGAINST the per-spec-registry-with-stale-detection mechanism class (search terms: "feature flag registry failure mode at enterprise scale" + "RFC 6982 implementation status section ineffective adoption" + "ADR governance registry overhead too heavy practitioner pushback"). Results: feature-flag stale-detection criticism exists at "noise / false-positive" level but not at "mechanism class invalid" level; RFC 6982 adoption is voluntary peer-pressure (which Cycle 16 makes BLOCKING — addressing the criticism not validating it); ADR adoption pushback exists at "ADR-of-ADRs meta-overhead" surface (informs ED §4 Kill Shot #3 — registry overhead risk). No disconfirming evidence at "mechanism class invalid" level found. |
| 13 | **Time-to-outcome feasibility** | Primary outcome (Cycle 16 close): 5-7 sessions = ~3 weeks at pipeline cadence (per-session ~2-3 days typical). Intermediate outcomes per phase: Phase 2 BE-A schema close = ~1 week; Phase 3 BE-B authoring discipline = ~1 week; Phase 4 BE-C gate = ~1 week; Phases 5-7 close-arc = ~1 week. Longitudinal verdict (done-criterion #10): ≥2 subsequent cycles post-Cycle-16-close (Cycles 17-18 forward-apply window) = ~6-8 weeks total to longitudinal verdict close. |

<!-- /gate:experimental_design §0 problem_selection_gate -->

**Gate -1 verdict:** PASS — all 13 criteria filled with specific evidence; Coach R3 verification at substrate §9 T8 DP#43 spot-read.

### Assumption challenge (A8)

What does the field currently believe that might be wrong? Per RQS §4 row 1 verbatim: AI-agent-engineering-methodology common practice (wrapper-program Bindings 1+2 implicit) assumes that author-time discipline + periodic cycle-close-review = implementation guarantee for authored specs. The Cycle 10 telemetry case study refutes this empirically: spec was well-authored at BE#5+BE#6 by disciplined process; Cycles 11-14 close-reviews all occurred; runtime wiring did not happen until Cycle-15-S7 only because Rex explicitly disposed govML back-port. Five cycles of close-reviews failed to close the gap. The challenge: without a per-spec registry binding "authored" to "runtime emit event class fired" via a structural BLOCKING gate that fires at both cycle-close AND session-close with ≤3-session dormancy threshold, no amount of author-time care or close-review attention catches dormant-silent specs at the source. 7-of-7 external disciplines surveyed at LA §1 independently arrived at compensating mechanisms (per-spec lifecycle tracking + structural detection of dormancy) — strong cross-discipline convergence evidence that the assumption is field-broadly known-insufficient.

### Artifact-first design

What artifact will practitioners use? **A 14-field per-spec registry schema (per kc-44 corrected count; Amendment 2026-05-27b) materialized at Apache Jena Fuseki `/cycle6` endpoint as nanopublication 3-graph triplets** per Cycle 6 BE#1 contract. Practitioner-facing artifacts: (a) `docs/spec_registry_schema.ttl` — TTL serialization of the 14-field schema for reproducibility; (b) `scripts/spec_implementation_present_gate.sh` + `scripts/spec_implementation_session_close_gate.sh` — TWO-surface BLOCKING gate scripts mirroring Cycle 14 four-gate skeleton; (c) `scripts/spec_authoring_check.sh` — spec-authoring-time gate body invoking SPARQL UPDATE against `/cycle6`; (d) `outputs/retroactive_scan_cycle_1_15_run.json` — empirical retroactive scan result; (e) `outputs/build_runner_events.jsonl` runtime emit sink with spec_authoring + spec_implementation event classes. Cycle 17-18 sessions inherit the mechanism via warmup auto-load; per-spec registry queryable via SPARQL endpoint.

### Surprise pre-registration

Expected finding: H1-H8 collectively CONFIRMED at Cycle 16 close with KT-1 + KT-3 + KT-4 + KT-6 NOT firing (DOES NOT FIRE per S2 RP analysis); KT-2 + KT-5 OPEN at empirical fire surface (retroactive scan + forward-apply dogfooding). Surprises: (a) KT-1 FIRES at LA §6 addendum (substrate coverage ≥80% post Cycle 6 KG inheritance) → Cycle 16 narrows to gap-filling + retroactive inventory only — RP authoring at this S2 will reassess; (b) KT-2 fires at retroactive scan (<3 dormant-silent specs across 15 cycles is surprisingly low — would suggest pipeline is structurally more disciplined than feature-flag governance norm at adjacent scale); (c) KT-4 fires (Cycle 14 skeleton requires structurally different primitive — surprising given LA §6b.2 preliminary disposition of clean extension); (d) KT-5 fires mid-Cycle-16 (≥2 NEW dormant-silent specs during the cycle authoring the mechanism itself — would refute H_main + paradigm-escalate). Most surprising outcome: KT-2 + KT-5 fire simultaneously (<3 historical dormant-silent AND ≥2 NEW Cycle 16 dormant-silent) — would indicate dormancy is freshly accumulating at Cycle 16 cadence faster than the historical baseline.

### Cross-domain bridge

Analogous problem in another domain: DevOps feature-flag governance (LaunchDarkly + GrowthBook + Optimizely; LA §1 row 5 + LA §1b row 1). Specific parallel: feature flags accumulate as silent technical debt — created during experiments / launches, never cleaned up, code paths persist forever, runtime branches never observed in production but never deleted from code. Direct structural parallel to: methodology specs accumulate as silent technical debt — authored during cycle planning, never wired to runtime, documentation persists forever, code paths never emit runtime events but spec remains in the artifact base. Mechanism import: per-flag lifecycle state machine (LaunchDarkly: Live / Ready for code removal / Ready to archive / Archived / Deprecated) + automated stale-flag detection at temporal thresholds (30d-created + 7d-inactive). Adaptation: replace "flag is firing in user traffic" with "spec's runtime_emit_event_class fires to JSONL sink at session cadence"; replace 30d with ≤3-session (sessions are pipeline's natural cadence). 5-state taxonomy at Amendment 2026-05-27a directly mirrors LaunchDarkly's 5-state lifecycle. PRIMARY adjacent-field import per LA §6b method import ranking.

## §1 Project Identity

- **Title:** Cycle 16 — Close the spec-to-implementation gap (build-class research within `engineering_methodology_for_agent_built_systems` wrapper program).
- **Target venue:** Internal pipeline (Stage 5 BE-class build artifacts) + FINDINGS.md at Cycle 16 close + cross-cycle reference at Cycles 17-18 forward-apply.
- **Lock commit:** Set at Cycle-16-S2 transition close — commits this ED + HR + PROJECT + REQUIREMENTS + ROADMAP + LA §6 addendum as paired set per Discipline #11.
- **Research type:** build (per `governance.yaml: research_type: build`; profile `research-build`).
- **Domain:** AI-agent-built-systems engineering methodology — spec-implementation governance via KG-primary substrate.

## §2 Novelty Claim

Per HC #34 ≤25 words: KG-primary 14-field per-spec registry composing 7 external disciplines + TWO-surface BLOCKING gate + ≤3-session dormancy detection at AI-agent-engineering-methodology grain.

Extended claim (per LA §6b landscape signals): the cross-discipline composition unifies 7 previously-incomparable mechanisms (IETF + PEP + OpenAPI + DbC + feature-flag governance + ADR + Parnas) into a single 14-field schema applied at AI-agent-built-systems engineering grain where this composition has not been applied before. Differentiation from 7 prior works at LA §1 rows 1-7 LOCKED.

## §3 Comparison Baselines

<!-- gate:experimental_design §3 baselines required -->

| # | Baseline | Source | What it covers | What it misses |
|---|---|---|---|---|
| 1 | **LaunchDarkly Flag Health metrics** (commercial precedent) | LA §1 row 5; 8 verbatim quotes (LaunchDarkly Flag Health docs + GrowthBook Stale Feature Flag Detection + Optimizely Flag Statuses + FlagShark cleanup tooling) | Per-flag lifecycle state machine (5 states: Live / Ready for code removal / Ready to archive / Archived / Deprecated) + automated stale-flag detection at 30d/7d threshold + Code References auto-linking flag-key → file:line + commercial deployment >1000 enterprises | Operates at runtime-active-flag grain (user traffic firing) not at spec-emits-structural-event grain (session-cadence JSONL emit). Adaptation per H5 import #1: replace "flag fires in user traffic" with "spec's runtime_emit_event_class fires to JSONL sink"; replace 30d/7d with ≤3-session threshold. |
| 2 | **IETF RFC 6982/7942 Implementation Status Section adoption** (social-process precedent) | LA §1 row 2; 4 verbatim quotes | Per-spec implementation-status field carried as canonical-class field through standards-development lifecycle; "running code" philosophy (Clark 1992); reference-implementation requirement at standards-track promotion (IESG discretionary); 30+ year operational history | Voluntary peer-pressure adoption ("highly desirable" not BLOCKING). Cycle 16 mechanism makes it STRUCTURAL BLOCKING at TWO surfaces (cycle-close + session-close). Cultural anchor borrowed; enforcement modality stricter. |
| 3 | **Cycle 14 four-gate methodology** (lock_commit `efaf6ae6` captured at scaffold) | LA §6b.2 row 3 + Moonshots `~/ml-governance-templates/scripts/k_register_present_gate.sh` source-inspected at S1 | Template-class structural-gate predicate body (`artifact_exists($spec) ∧ placeholder_count($spec) == 0 ∧ H_disconfirmation_subsection_count($spec) ≥ 1`); gate-script skeleton + `check_all_gates.sh` invocation + profile-build conditional firing + BLOCKING mode default; HC #45 + HC #23 closures verified-in-vivo at Cycle-16-S1 scaffold | Fires at cycle-close only (one surface). Predicate is artifact-EXISTS not spec-IMPLEMENTED. Cycle 16 extends to TWO surfaces via SPARQL UPDATE/ASK substitution targeting `/cycle6` endpoint per Cycle 6 BE#1 contract. H6 + KT-4 evaluation at Phase 4 BE-C. |
| 4 | **Cycle 6 unified KG substrate** (Apache Jena Fuseki `/cycle6` endpoint operational since 2026-05-14) | LA §6 addendum (Cycle 16 EXTENSION) + Coach probe 2026-05-27 evidence: PID 479112 RUNNING; 246,048 quads / 46 named graphs; top: be4:signals:assertion=93,297 + be4:claims:assertion=40,810 + be4:signals:publicationInfo=20,976 + be4:signals:provenance=15,733 + be4:claims:provenance=11,901 + be2:assertion=8,543 + be3:pipeline_experiments_ranking_events:assertion=6,201 + cycle6:ontology=181; SPARQL latency: COUNT(*)=0.139s + per-graph agg=0.495s + predicate enum=0.082s + HC-11 enum=0.066s (all ≤5s threshold by 10-256× margin) | Cycle 6 PARTIAL-CLOSED at S7 2026-05-14h per Rex Decisions 1-4: 3-of-4 BEs PROMOTED + BE#4 BUILT-NOT-PROMOTED HOLD pending Cycle 7 substrate-viability research-class cycle (HC-RP-S2-4 forward dependency carry). Wikidata supersedure PARTIAL — only `cycle6:rankingRationale` present; `wikibase:rank` + `prov:wasRevisionOf` absent at 2026-05-27 ground state (HC-RP-S2-3 carry; ED §4a constraint #4 binds Stage 5 BE-A schema extension). |
| 5 | **Wrapper-program Bindings 1-7** (behavioral discipline baseline) | strategic_frame.md 8 Bindings ACTIVE 2026-05-07 + HC-03 amendment `debdf2f` UNMODIFIED | Coach NEVER fills Stage 0-4 templates (Binding 6); ≥80% external research at LANDSCAPE (Binding 1); cross-validation surface NOT design anchor (Binding 2); no §11 overrides (Binding 7) | Operates at coarse per-cycle grain via author-time discipline + close-review attention; Cycle 10 telemetry case study refutes empirically (5-cycle gap despite high author discipline + 5 close-reviews). Cycle 16 supplements with structural per-spec registry + ≤3-session dormancy detection. |

≥1 baseline required from the prior works engaged at LA §1 — exceeded; 5 baselines (3 external + 2 internal/inheritance).

<!-- /gate:experimental_design §3 baselines -->

## §4 Kill Shots

<!-- gate:experimental_design §4 kill_shots required -->
<!-- REQUIREMENT: KT-1..KT-6 verbatim from substrate §4 STRUCTURAL BINDING (each KT-N also at HR §3 surprise criteria) -->

≥2 specific criticisms a hostile reviewer would make, with mitigations. KT-1..KT-6 reversal triggers bind into Kill Shot surprise criteria per substrate §4 STRUCTURAL BINDING.

| # | Criticism | Severity | Mitigation | Evidence mitigation works |
|---|---|---|---|---|
| 1 | **KT-1 firing — substrate ≥80%:** "Internal substrate already covers ≥80% of Cycle 16 mechanism scope per LA §6 addendum revised aggregate coverage post Cycle 6 KG inheritance (~90-95%); Cycle 16 is over-building when narrowing to gap-filling + retroactive inventory would suffice." | HIGH (substrate viability surface; pre-Amendment-27b coverage was ≈70%; post-27b may shift) | LA §6 addendum captures Cycle 6 KG mechanism-class inheritance at this S2 RP authoring + Coach R3 verification at substrate §9 T12. If KT-1 FIRES at revised ≥80%, Cycle 16 narrows Branch 4 to retroactive scan + spec-class RDF schema extensions only (NOT full registry framework). | LA §6b.2 6-row matrix at S1 measured ≈70%; Cycle 6 KG adds ~20-25% per S2 addendum estimation. KT-1 disposition surface intentionally lives at LA §6 addendum per substrate §5 task; Coach R3 mechanical test T12. |
| 2 | **KT-2 firing — <3 dormant-silent:** "The retroactive Cycle 1-15 scan surfaces <3 dormant-silent specs across 4 spec-classes; the Cycle 10 anecdote was the outlier not the pattern; the mechanism is over-built for the problem size." | MED (retroactive scan empirical surface; H3 binding) | KT-2 disposition: halt + Rex paradigm re-disposition per substrate §4. Phase 5 BE-D retroactive scan is the empirical surface; if <3 dormant-silent surfaces, Cycle 16 halts before forward-apply build (Phases 6-7 not authored). | OBS-2 (6-of-9 agent specs gitignored; HC #52 broader scope) suggests ≥3 candidates: Cycle 10 RUNTIME_EMIT_SPEC.md + ≥2 of 6 gitignored agent specs whose runtime invocation cannot be verified absent enumeration. Pre-S5 hypothesis: ≥3 dormant-silent likely; KT-2 firing low probability. |
| 3 | **KT-3 firing — n=3+ author refusals:** "Registry-row-required at authoring boundary is too heavyweight at per-session pipeline cadence; ≥3 author refusals during Cycle 16 itself force same-cycle backlog OR registry shape refinement." | MED (forward-apply dogfooding surface; H7 binding) | KT-3 disposition: registry shape needs structural refinement OR same-cycle default needs relaxation for specific spec types per substrate §4. DP#26 carve-out (per HR §3d) allows methodology commitments to take `runtime_emit_event_class = 'n/a'` with documented rationale — mitigates heavyweight risk at Layer-5 methodology spec class. | LaunchDarkly enterprise customer engineers operate per-flag tagging-at-creation discipline at >1000-flag scale without refusal cascade (LA §1 row 5); per-spec authoring at AI-agent-engineering cadence is heavier but pipeline session cadence (per ~2-3 days) gives more authoring time than LaunchDarkly per-feature-launch cadence (hours). Per H7 forward-apply dogfooding during Cycle 16 itself. |
| 4 | **KT-4 firing — predicate extension requires new primitive class:** "The Cycle 14 four-gate gate-script-shape (artifact_exists ∧ placeholder_count == 0 ∧ H_disconfirmation_subsection ≥ 1) does not extend cleanly to the spec-implementation predicate via SPARQL ASK substitution; the new predicate requires structurally different gate primitive (e.g., maintaining per-spec state across invocations rather than per-invocation stateless query)." | MED (Branch 2.3 surface; H6 binding) | KT-4 disposition: new enforcement primitive class warranted; surface as paradigm-class scope expansion candidate OR proceed within cycle if scope still bounded per substrate §4. Phase 4 BE-C is the empirical surface (gate-script implementation). | LA §6b.2 row 3 preliminary disposition: predicate extends cleanly — same double-brace-placeholder-zero + ≥1-H-disconfirmation-subsection shape, with new conditions added via SPARQL ASK body against `/cycle6` endpoint per Cycle 6 BE#1 contract. KT-4 firing low probability per preliminary assessment. |
| 5 | **KT-5 firing — ≥2 NEW dormant-silent specs:** "Forward-apply during Cycle 16 itself OR across Cycles 17-18 produces ≥2 NEW dormant-silent specs — the mechanism's structural BLOCKING surface is insufficient under pipeline cadence; H_main REFUTED." | HIGH (H_main REFUTED + paradigm escalation; H8 binding) | KT-5 disposition: H_main REFUTED → FINDINGS Layer 5 honest-gap + paradigm escalation candidate per substrate §4. RQS §4.1 Alternative 2 (specs ARE code; spec/code single source of truth) becomes candidate forward-cycle escalation surface. | Forward-apply observation enabled at Cycle 16 close (Phase 6 BE-E); longitudinal verdict at Cycle 18 close (done-criterion #10). KT-5 firing is the H_main reversal surface — intentionally pre-registered, not mitigated. |
| 6 | **KT-6 firing — Cycle 6 KG substrate-viability blocker:** "Apache Jena Fuseki `/cycle6` endpoint fails substrate-viability (RDF schema mismatch / SPARQL latency >5s / HC-11/PROV-O/Wikidata primitives absent / Cycle 7 consumer migration stalled blocking onboarding) — Cycle 16 must fall back to SQL/YAML per pre-Amendment-27b binary framing." | HIGH (NEW KT per Amendment 2026-05-27b; substrate-viability surface) | KT-6 disposition: fall back to SQL/YAML + Step 3.5 escalation gate + evidence at FINDINGS Layer 4. Coach pre-disposed DOES NOT FIRE per 2026-05-27 probe; RP independently verifies + reports at LA §6 addendum. | Coach probe 2026-05-27: 246,048 quads / 46 named graphs operational; SPARQL latency 0.066-0.495s (10-256× margin to ≤5s threshold); PROV-O 4 typed-edges operational; HC-11 enum 11,223+ usages operational; nanopublication 3-graph pattern operational across 46 graphs. KT-6 DOES NOT FIRE per all 4 substrate-viability primitives operational. HC-RP-S2-3 (Wikidata supersedure PARTIAL) is sub-KT-6 candidate that does NOT fire main KT-6. |

<!-- /gate:experimental_design §4 kill_shots -->

### §4a Constraint-Driven Design Check

<!-- source: substrate §7 §4a 6 BINDING constraints anchor + LA §3 + §4 contested/uncertain feed-forward -->

6 BINDING constraints from substrate authority + LA §3 §4 contested-items + §6 addendum carry that shaped Cycle 16 design choices:

1. **Registry write = SPARQL UPDATE INSERT DATA to Fuseki `/cycle6` endpoint per Cycle 6 BE#1 contract.** Per Amendment 2026-05-27b 3rd-pass Rex authorization: KG-primary storage substrate (NOT pre-27b binary "SQL table at singularity.db OR YAML registry at govML scaffolding" framing). SQL/YAML fallback only on KT-6 substrate-viability blocker firing.
2. **Per-edge HC-11 access-permission enum required at every write boundary.** Each materialized predicate annotated with `cycle6:hcAccessPermission` ∈ {publishable, ip-private, ephemeral} per Cycle 6 BE#1 contract (operational at 2026-05-27 probe: 11,223 ip-private + 1 publishable + 1 ephemeral usages).
3. **PROV-O 4 typed-edges required at every spec materialization:** `prov:wasGeneratedBy` (the session) + `prov:wasAttributedTo` (the owner) + `prov:generatedAtTime` (timestamp) + `prov:wasInformedBy` (upstream spec). Per Cycle 6 BE#1 contract orphan-refusal discipline.
4. **Wikidata supersedure pattern (`wikibase:rank` + `prov:wasRevisionOf`) author at Stage 5 BE-A schema extension if absent.** HC-RP-S2-3 binding: at 2026-05-27 Coach probe, only `cycle6:rankingRationale` predicate present; `wikibase:rank` + `prov:wasRevisionOf` absent at Cycle 6 BE#1 ground state. Stage 5 BE-A authors at schema extension OR FINDINGS Layer 4 honest gap.
5. **Substrate viability verified at LA §6 addendum + Coach-probed evidence.** Coach probe 2026-05-27 raw evidence cited at LA §6 addendum + ED §3 row 4 + ED §Field 6 KT-6 row. KT-6 disposition recommendation: DOES NOT FIRE per all 4 substrate-viability primitives operational.
6. **Cycle 14 four-gate skeleton extended to spec-implementation predicate via SPARQL UPDATE/ASK body substitution.** Per H6 binding + Branch 2.3 + Phase 4 BE-C verification surface. Same `scripts/<name>_present_gate.sh` skeleton + `check_all_gates.sh` invocation + `--advisory-mode` opt-in WARN flag + BLOCKING default. New predicate body: SPARQL ASK against `/cycle6`.

Additional contested-item carry from LA §3.1:

- **LA §3.1 Contested item (4):** `spec_registry` substrate choice (SQL OR YAML OR KG). **RESOLVED at S2 by Amendment 2026-05-27b:** KG-primary per Cycle 6 BE#1 contract; SQL/YAML fallback only on KT-6 firing.
- **LA §3.1 Contested item (5):** `runtime_emit_event_class` MANDATORY for all specs OR allow documented `n/a`. **RESOLVED at S2:** allow documented `n/a` per DP#26 carve-out for methodology commitments (HR §3d) — over-use risk is KT-3 firing surface (per H7).
- **LA §3.1 Contested item (6):** KT-1 disposition reversibility at Stage 3-4. **RESOLVED at S2:** KT-1 reassessment lives at LA §6 addendum (this S2 RP authoring) per substrate §5; pre-registration locks OPERATIONAL disposition; Rex paradigm-ruling required if Stage 3-4 evidence substantially changes outcome shape per Binding 7.

### Related Work

Per LA §1 LOCKED + §6b prior work frontier: 7 external disciplines surveyed cover spec→implementation lifecycle tracking at field scale (IETF / Python PEP / OpenAPI / DbC / feature-flag governance / ADR / Parnas; LA §1 rows 1-7 with 36 verbatim quotes total). LaunchDarkly is closest direct precedent at adjacent grain (per-flag lifecycle states + automated stale-flag detection); IETF + PEP provide cultural anchor (running code philosophy); Cycle 14 four-gate is internal template precedent; Cycle 10 RUNTIME_EMIT_SPEC.md is canonical failure-mode case study. The composition of all 7 into a unified 14-field schema applied at AI-agent-engineering-methodology grain is the cross-disciplinary contribution candidate.

### Threats to Validity

1. **K register spec defects deferred forward** — the 14-field schema is authored at Stage 3-4 RP (this dispatch) as a pre-registration; actual implementation at Stage 5 BE-A may surface schema defects (e.g., field constraint conflicts, IRI namespacing collisions with existing `cycle6:` predicates). Threat: schema-authored ≠ schema-shippable. Mitigation: Phase 2 BE-A smoke-test against `/cycle6` endpoint with synthetic test spec end-to-end (REQUIREMENTS §Verification Surfaces).
2. **HC-RP-S2-3 Wikidata supersedure PARTIAL forward dependency** — only `cycle6:rankingRationale` present at 2026-05-27 ground state; `wikibase:rank` + `prov:wasRevisionOf` absent. Threat: Stage 5 BE-A schema extension may surface that Cycle 6 BE#1 contract upstream requires extension rather than just Cycle 16 schema annotation. Mitigation: ED §4a constraint #4 binds Stage 5 BE-A to surface to Coach for verification; FINDINGS Layer 4 honest gap if extension is upstream-blocked.
3. **HC-RP-S2-4 Cycle 7 substrate-viability research-class cycle OPEN forward dependency** — Cycle 6 PARTIAL-CLOSED at S7 2026-05-14h per Rex Decisions 1-4; BE#4 BUILT-NOT-PROMOTED HOLD; if Cycle 7 surfaces vendor pivot (Fuseki → alternative KG), Cycle 16 mechanism would need vendor-portable abstraction layer. Mitigation: FINDINGS Layer 4 forward dependency carry; vendor-portable abstraction layer authored at Stage 5 BE-A if Cycle 7 surfaces pivot during Cycle 16 envelope.
4. **Dogfooding bias** — Cycle 16 mechanism is authored within the cycle that tests it; forward-apply observation during Cycle 16 itself may be artificially constrained (RP/Coach/Builder are aware of the mechanism and may unconsciously avoid the dormancy modes the mechanism is designed to detect). Mitigation: KT-5 firing surface explicitly pre-registered to catch this — if ≥2 NEW dormant-silent specs accumulate mid-Cycle-16 OR Cycles 17-18, H_main REFUTED + paradigm escalation candidate. Longitudinal forward-apply across Cycles 17-18 (post-Cycle-16-close) less subject to dogfooding bias.
5. **Per-spec-class operational definition variance** — 4 spec-classes have structurally different "implemented" semantics (agent contract = invocation; schema = validation firing; design decision = code embodiment OR retraction ADR; methodology commitment = downstream citation OR explicit deferral per DP#26 carve-out). Threat: variance may require per-class bespoke verifier logic rather than unified gate-predicate skeleton. Mitigation: H2 + H6 + KT-4 explicitly pre-registered to surface this — Phase 4 BE-C gate-script implementation tests "clean skeleton extension" vs "new primitive class warranted."

### Statistical Plan (computational research conditional)

This Cycle 16 is build-class research; the central artifacts are structural (registry schema + gate scripts + retroactive scan output) not statistical. No primary hypothesis test (chi-squared / t-test / regression) is computed at Cycle 16 close. **Aggregate retroactive scan counts** (per-spec-class × per-state breakdown; 4×5 = 20-cell aggregate) are deterministic enumeration results — counted not tested. **KT-2 firing surface** is a deterministic threshold: if `count(current_status = 'dormant-silent') < 3`, KT-2 FIRES — no statistical test applied. **KT-3 firing surface** is a deterministic count: n=3+ author refusals = KT-3 fires. **KT-5 firing surface** is similarly deterministic.

The closest statistical-equivalent surface is the **per-cell HYBRID PRIMARY boundary-condition map richness** at FINDINGS Layer 3 (HR §3a EXTENSION-3): empirical sparsity across 80 cells is reported as cell-count populated / total; no inferential statistic computed. Per kc-44 PD §3.3: discrete reversal-disposition surfaces (KT-N) replace continuous-statistical surfaces in build-class research.

### Ablation Plan (computational research conditional)

This Cycle 16 is build-class research; not all ablations apply at the same granularity as compute-bound experimental design. Two ablation-class sensitivity analyses:

1. **Per-spec-class ablation:** retroactive scan disaggregated per spec-class (4 classes); per-class dormant-silent count reported separately at FINDINGS Layer 3. If aggregate KT-2 fires (<3 dormant-silent) but per-class breakdown shows class imbalance (e.g., 3 dormant-silent ALL in methodology commitments; 0 in agent contracts), the mechanism may be load-bearing only for some classes.
2. **DP#26 carve-out usage ablation:** at Cycle 16 close, count of methodology commitments with `runtime_emit_event_class = 'n/a'` documented vs without. If ≥30% of methodology commitments take `n/a`, KT-3 firing surface narrows mechanism applicability to subset-of-spec-classes only — surface at FINDINGS Layer 4.

### Adaptive Adversary Analysis (security-domain conditional)

Cycle 16 is governance-class research (AI-agent-built-systems engineering methodology); NOT directly security-domain. Adversary surface analysis nonetheless applies at the meta-level: how would a motivated adversary exploit the Cycle 16 mechanism findings?

- **Adversary exploits mechanism completeness gap:** if Cycle 16 ships with `runtime_emit_event_class = 'n/a'` carve-out, an adversary could (in theory) author specs with intentionally-vague `n/a` claims to evade the dormancy detection while degrading pipeline output quality. Mitigation: DP#26 carve-out requires documented rationale; Coach R3 spot-check at close-eval.
- **Adversary exploits HC-RP-S2-3 schema gap:** Wikidata supersedure PARTIAL means superseded specs may not have structural retraction trail until Stage 5 BE-A schema extension. Adversary could (in theory) supersede a spec without leaving audit trail in the brief window. Mitigation: HC-RP-S2-3 binding to Stage 5 BE-A; FINDINGS Layer 4 honest gap if extension is upstream-blocked.
- **Responsible disclosure:** N/A (research-class artifacts; no external-facing system).

<!-- /gate:experimental_design §0-§4 -->

## §Field 6 KT-1..KT-6 Pre-Registration Matrix (structural binding; cross-ref HR §3 + LA §6 addendum)

<!-- source: substrate §4 KT-1..KT-6 matrix + Cycle 16 SI L98-L110 + Amendment 2026-05-27b -->
<!-- gate:experimental_design §Field_6 kt_matrix required -->

| KT | Detection point | Threshold | Disposition |
|---|---|---|---|
| **KT-1** | LANDSCAPE §6 addendum close (Stage 2 augmentation; this S2 RP authoring + Coach R3 verification + Rex paradigm-ruling 2026-05-27 disposition (C) metric-revision-within-intent per foundational threshold-metric pre-registration discipline §10 (i)+(ii)) | RIDE + research_depth_enforcement_automation + Cycle 14 four-gate + Cycle 6 unified KG (added via §6 addendum per Amendment 2026-05-27b) collectively cover **≥80% of MECHANISM-LAYER scope, excluding pure substrate-layer inheritance (storage primitives + access-permission enum + provenance edges + endpoint substrate)** per refined operational metric (Rex disposition (C) 2026-05-27; substrate availability ≠ mechanism redundancy) | **DOES NOT FIRE under refined metric** (post-refinement mechanism-layer coverage ~75-85%; HC-11 partition semantics + PROV-O orphan-refusal discipline counted as mechanism-class; storage + endpoint + nanopublication 3-graph + raw HC-11 enum + raw PROV-O edges counted as substrate-layer excluded). **Cycle 16 proceeds with full SI scope (Branches 1-4 all in-scope).** Originally would fire under literal ≥80% reading of unrefined "any inheritance" metric (~90-95% pre-refinement); foundational threshold-metric pre-registration discipline §10 (i)+(ii) anchors literal-vs-intent disambiguation operationally rather than via paradigm escalation. |
| **KT-2** | Phase 5 BE-D retroactive Cycle 1-15 scan close | <3 dormant-silent specs surfaced at aggregate count | Halt + Rex paradigm re-disposition; problem may be lower-leverage than Cycle 10 anecdote suggested |
| **KT-3** | Forward-apply dogfooding during Cycle 16 itself (Phases 2-7) | n=3+ author rejections (acceptance criteria unclear OR same-cycle backlog unmanageable) | Either (a) registry shape needs structural refinement, OR (b) same-cycle default needs relaxation for specific spec types per DP#26 carve-out |
| **KT-4** | Phase 4 BE-C gate-script implementation | "spec implemented" predicate requires structurally different gate primitive than "artifact exists" via SPARQL ASK substitution | New enforcement primitive class warranted; surface as paradigm-class scope expansion candidate OR proceed within cycle if scope still bounded |
| **KT-5** | Cycle 16 mid-cycle forward-apply observation + Cycles 17-18 longitudinal | ≥2 NEW dormant-silent specs accumulate during Cycle 16 itself OR forward-apply window | H_main REFUTED → FINDINGS Layer 5 honest-gap + paradigm escalation candidate (RQS §4.1 Alternative 2: specs ARE code, no spec/code separation) |
| **KT-6 NEW** | LA §6 addendum (Stage 2 augmentation) OR Stage 3-4 RP fill pre-dispatch (this S2) | Substantive Cycle 6 substrate-viability blocker (RDF schema mismatch / SPARQL latency >5s / HC-11/PROV-O/Wikidata primitives absent / Cycle 7 consumer migration stalled blocking onboarding) | Fall back to SQL/YAML per pre-Amendment-27b binary framing + Step 3.5 escalation gate + evidence at FINDINGS Layer 4 |

**KT-6 disposition recommendation (this S2 RP authoring):** **DOES NOT FIRE.** Coach probe 2026-05-27 substrate evidence: 246,048 quads + 46 named graphs operational; SPARQL latency 0.066-0.495s (10-256× margin to ≤5s threshold); PROV-O 4 typed-edges operational; HC-11 access-permission enum 11,223+ usages operational; nanopublication 3-graph pattern operational across 46 named graphs. All 4 substrate-viability primitives operational. HC-RP-S2-3 (Wikidata supersedure PARTIAL — only `cycle6:rankingRationale` present) is sub-KT-6 candidate that does NOT fire main KT-6. HC-RP-S2-4 (Cycle 7 substrate-viability research-class cycle OPEN; BE#4 BUILT-NOT-PROMOTED HOLD per Rex Decisions 1-4 2026-05-14g) is FORWARD DEPENDENCY carry, NOT current-state substrate-viability blocker.

**KT-1 reassessment disposition (Rex paradigm-ruling 2026-05-27 disposition (C) metric-revision-within-intent):** evidence at LA §6 addendum; pre-Amendment-27b ~70% mechanism-layer coverage (RIDE F-D Hybrid ~30% + research_depth_enforcement_automation ~20% + Cycle 14 four-gate ~20%); Cycle 6 KG mechanism-layer inheritance ~5-15% (HC-11 partition semantics + PROV-O orphan-refusal discipline; raw storage + endpoint + nanopublication 3-graph excluded as substrate-layer per refined metric). **Net mechanism-layer coverage post-refinement ~75-85% — marginal at literal threshold (≥80%); firmly DOES NOT FIRE under intent reading per Rex disposition (C) anchoring foundational threshold-metric pre-registration discipline §10 (i)+(ii).** Cycle 16 proceeds with full SI scope (Branches 1-4 all in-scope). The pre-Rex-ruling literal reading (~90-95% under unrefined "any inheritance" metric) conflated substrate availability with mechanism redundancy; refined metric (mechanism-LAYER scope only) measures intent faithfully and resolves operationally without paradigm escalation.

<!-- /gate:experimental_design §Field_6 kt_matrix -->

## §7 Pre-emptive Criticism (substrate §7 + kc-44 PD §3.3)

Beyond §4 Kill Shots (which bind KT-1..KT-6 structurally), 3 additional pre-emptive criticisms a hostile reviewer might raise:

1. **"7-discipline cross-discipline composition is over-citation; the mechanism is essentially LaunchDarkly transplanted to a different application surface."** Response: LA §6b.1 cross-domain mechanism validity pre-check 5-import matrix shows that each of 5 imports (LaunchDarkly + IETF/PEP + DbC + ADR + Parnas) contributes a structurally distinct mechanism element (per-spec lifecycle state machine + implementation-status field as canonical-class field + runtime-boundary contract assertion + supersedure-tracking + authoring-time precision discipline). Composition is the load-bearing contribution; per LA §2b fragmentation diagnosis: "Is making evidence comparable the real contribution? yes — this is a methodology contribution." Cycle 16's 14-field schema unifies 7 incomparable mechanisms into a single comparison surface — that act of unification is what LaunchDarkly alone does not provide (LaunchDarkly handles 1 of 7 mechanism elements; Cycle 16 handles 7).
2. **"The wrapper-program scope is too narrow; cycle 16 only matters for AI-agent-built-systems engineering methodology — niche audience."** Response: ED §0 Gate -1 #2 practitioner pain quantifies the audience at AI-agent-built-systems engineering teams operating pipelines with ≥10 cycles' standing carrying ≥50 methodology specifications. The 7-discipline cross-discipline grounding at LA §1 LOCKED demonstrates that the failure mode is field-broadly known (each of 7 source domains independently invented compensating mechanisms); Cycle 16's composition makes the mechanism applicable to a new application surface that did not have it. The application surface (AI-agent-built-systems) is growing rapidly (per OBS-8 cross-engine signals on agent frameworks); audience size scales with field growth.
3. **"ED §0 #12 disconfirming evidence search was insufficient; only 3 search terms used."** Response: search terms covered the 3 most-cited criticism surfaces for the mechanism class (feature-flag stale-detection false-positive criticism + RFC 6982 voluntary peer-pressure adoption criticism + ADR registry-overhead practitioner pushback). Per RQS §4 row 1 contradiction search: each source domain independently arrived at the mechanism class, suggesting cross-discipline convergence is the strongest available evidence. Additional disconfirming-evidence search at FINDINGS Layer 4 close if Coach R3 surfaces this as gap.

## §8 Novelty / Impact / Generalization

**Novelty Assessment (per `project.yaml.audit.prohibited_language` constraint — no "novel" / "first" tokens):** The cross-discipline composition unifying 7 mechanism elements (per-spec registry + lifecycle state machine + implementation-status field + owner attribution + temporal-threshold detection + audit-trail/supersedure + authoring-time discipline) into a single 14-field schema applied at AI-agent-built-systems engineering methodology grain is a composition that has not been performed at this application surface per LA §1.2 cross-discipline convergence matrix + §6 KT-1 disposition assessment. Each component is field-mature in its source domain; the COMPOSITION at this application surface is the discriminating contribution.

**Practitioner Impact:** if H1-H8 collectively CONFIRMED + KT-1..KT-6 do not fire negatively + ≥2-cycle forward-apply shows 0 NEW dormant-silent specs, the per-spec KG registry schema becomes a candidate cross-disciplinary benchmark schema for spec-implementation governance in AI-agent-built systems. Per LA §1.1 Benchmark as Landscape: "At AI-agent-built-systems-engineering-methodology grain, NO benchmark exists because the field itself is nascent (~2024-2026 emergence). Cycle 16's per-spec registry schema (13 fields per SI §4.1; 14 per kc-44 corrected count) IS a candidate benchmark schema for the field." Practitioner action path: pipeline teams at this scope can adopt the schema + gate-script pattern in ~1 cycle by adapting `/cycle6` endpoint pattern to local KG substrate.

**Generalization Analysis (failure modes with thresholds):** mechanism generalizes within AI-agent-built-systems engineering methodology grain (cycle-cadence pipelines authoring ≥50 cross-cycle methodology specifications). Mechanism does NOT generalize to: (a) per-day-cadence operational systems (use LaunchDarkly directly; Cycle 16's session-cadence threshold is too coarse); (b) protocol-standardization processes (IETF/PEP timeline is multi-year; same-cycle default is too aggressive); (c) safety-critical systems requiring formal verification (use DbC + Eiffel-class runtime checking; Cycle 16's structural BLOCKING gate is not formal-verification-grade). Per FINDINGS Layer 4 boundary statement at Cycle 16 close.

## §9 Cross-Domain Connections (proactive at design time; reflective at FINDINGS Layer 4)

Per LA §1b 4-row adjacent field survey + LA §6b.1 5-import matrix:

- **DevOps feature-flag governance (LaunchDarkly + GrowthBook + Optimizely + FlagShark):** PRIMARY adjacent-field import. Per-flag lifecycle state machine + automated stale-detection at temporal threshold. Adaptation: session-cadence ≤3 instead of 30d/7d days; per-spec-emit-event instead of per-flag-fires-in-traffic.
- **Standards-development (IETF + Python PEP):** SECONDARY import. Per-spec implementation-status as canonical-class field through lifecycle; PEP-Delegate owner attribution. Adaptation: SPARQL ASK against `/cycle6` instead of social-process tracking; STRUCTURAL BLOCKING instead of voluntary peer-pressure.
- **ADR governance (Nygard 2011 + Tyree & Akerman 2005):** TERTIARY import. 4-state lifecycle + supersedure-tracking via two-way "Supersedes / Superseded By" relations + immutable-post-acceptance. Adaptation: 5-state taxonomy adds `long-running` for multi-cycle planned implementations (Amendment 2026-05-27a 5th state); supersedure via Wikidata `wikibase:rank` + `prov:wasRevisionOf` predicates (HC-RP-S2-3 carry).
- **Enterprise agent/data registries** (Prefactor 2026 + lakeFS + MCP enterprise registry literature; LA §1b row 4): QUATERNARY import. Identity + ownership + framework + capability + status fields per enterprise-registry best-practice. Adaptation: 14-field schema directly maps to enterprise-registry pattern; per-spec rows instead of per-agent-runtime rows.
- **Design by Contract (Meyer 1992 + Eiffel + icontract/deal/beartype):** Cross-discipline anchor. Runtime contract assertion at code boundaries. Adaptation: gate-script-as-contract-assertion at spec-lifecycle boundaries (cycle-close + session-close); SPARQL ASK body fires at gate-invocation time.
- **Parnas precise documentation + tabular notations:** Cultural anchor. Documentation as canonical-class engineering artifact maintained DURING development. Adaptation: 14-field registry row IS the precise documentation in Parnas-style structured form (per-field-required at authoring time).

Reflective cross-domain connections (discovered DURING analysis) reported at FINDINGS Layer 4 close.

## §10 Per-BE Stage 5 Scope Binding (forward to Build-Runner)

<!-- source: substrate §7 ROADMAP Stage 5 BE-class + Cycle 14 multi-BE precedent -->
<!-- gate:experimental_design §10 stage_5_be_scope required -->

Stage 5 BE-class sessions decompose into 4-5 BE per Cycle 14 multi-BE precedent. Each BE has a discrete deliverable + acceptance criteria + KT-N evaluation surface. ROADMAP §1-§6 phases bind into BE-class scope as follows:

### §10.1 BE-A: KG-primary 14-field schema + SPARQL write-boundary (ROADMAP Phase 2)

**Scope:** author `docs/spec_registry_schema.ttl` + materialize 14-field RDF schema at Fuseki `/cycle6` endpoint + smoke-test against synthetic test spec + author per-edge HC-11 access-permission enum + author PROV-O 4 typed-edges + author Wikidata supersedure predicates (or HC-RP-S2-3 carry) + author nanopublication 3-graph pattern.

**Acceptance criteria (per REQUIREMENTS §Per-Deliverable #5):**

- 14 fields + per-edge HC-11 enum + PROV-O 4 typed-edges + nanopublication 3-graph + Wikidata supersedure (HC-RP-S2-3 carry if PARTIAL).
- TTL serialization at canonical path.
- `curl http://localhost:3030/cycle6/sparql --data-urlencode 'query=ASK { ?spec a cycle16:Spec }'` returns TRUE for ≥1 test spec materialized end-to-end.
- SPARQL DESCRIBE on test spec returns all 14 predicates.

**KT-N evaluation surface:** none directly; KT-6 (substrate-viability) re-verifiable at BE-A close (sanity-check that `/cycle6` endpoint is operational and SPARQL UPDATE/ASK end-to-end works).

**Threats to validity at BE-A:** schema field constraint conflicts; IRI namespacing collisions with existing `cycle6:` predicates; HC-RP-S2-3 Wikidata supersedure PARTIAL forward dependency.

### §10.2 BE-B: Spec-authoring discipline + DP#26 carve-out (ROADMAP Phase 3)

**Scope:** author `docs/spec_authoring_discipline.md` defining gate body executed at spec-authoring boundary (SPARQL UPDATE INSERT DATA against `/cycle6`); author DP#26 carve-out spec (methodology commitments allow `runtime_emit_event_class = 'n/a'` with documented rationale); author `scripts/spec_authoring_check.sh` invoked at session-init for spec-authoring sessions.

**Acceptance criteria (per REQUIREMENTS §Per-Deliverable #6):**

- SPARQL UPDATE INSERT DATA gate body defined.
- BLOCKING discipline rejects if required (non-nullable) fields absent.
- DP#26 carve-out for methodology commitments documented with rationale requirement.
- `scripts/spec_authoring_check.sh` present at canonical path with DP#44-compliant refuse-on-missing-precondition behavior.

**KT-N evaluation surface:** KT-3 forward-apply observation enabled (every new spec authored at Phases 2-7 must pass authoring-discipline gate; refusal count tracked).

**Threats to validity at BE-B:** spec-authoring authoring overhead may produce refusal cascade in same session (KT-3 firing); DP#26 carve-out may be over-used (defeating mechanism — KT-3 surface narrower variant).

### §10.3 BE-C: TWO-surface BLOCKING gate (ROADMAP Phase 4)

**Scope:** author `scripts/spec_implementation_present_gate.sh` (cycle-close surface) + `scripts/spec_implementation_session_close_gate.sh` (session-close surface); both invoke SPARQL ASK against `/cycle6` per H6 binding; both wire into `check_all_gates.sh` wrapper per Cycle 14 four-gate pattern; H6 + KT-4 evaluation.

**Acceptance criteria (per REQUIREMENTS §Per-Deliverable #7):**

- Both gate scripts present at canonical path with bash shebang + DP#44-compliant refuse-on-missing-precondition behavior.
- BE-C close-eval: synthetic test specs covering all 5 states → expected BLOCKING fires on `dormant-silent` test fixture; expected PASS fires on 4 other states.
- Gate-script skeleton mirrors `k_register_present_gate.sh` cleanly without primitive-class extension = H6 CONFIRMED; KT-4 fires otherwise.

**KT-N evaluation surface:** KT-4 firing — predicate extension requires structurally different gate primitive than SPARQL ASK body substitution at the gate-script-shell-script primitive layer.

**Threats to validity at BE-C:** gate-script invocation cadence (per-session vs per-cycle); SPARQL endpoint availability at gate-fire time (network/process dependency); per-spec state maintenance across invocations (if required, may surface KT-4 as primitive-class boundary).

### §10.4 BE-D: Retroactive Cycle 1-15 scan (ROADMAP Phase 5)

**Scope:** enumerate 4 spec-classes across Cycles 1-15 (agent contracts via `ls` direct per HC #52; schemas via `find` + drift_telemetry; design decisions via DECISION_LOG cross-cycle; methodology commitments via FINDINGS Layer-5 cross-cycle) + classify per 5-state taxonomy + materialize per-spec rows at `/cycle6` via SPARQL UPDATE INSERT DATA + emit `outputs/retroactive_scan_cycle_1_15_run.json` + H1 + H3 + KT-2 evaluation.

**Acceptance criteria (per REQUIREMENTS §Per-Deliverable #1 + #8):**

- ≥N specs enumerated (N≈90-100 per H1).
- 4-spec-class coverage complete.
- Aggregate query: `SELECT (COUNT(*) AS ?n) ?spec_type ?current_status WHERE { ?spec a cycle16:Spec ; cycle16:spec_type ?spec_type ; cycle16:current_status ?current_status } GROUP BY ?spec_type ?current_status` returns 4×5 = 20-cell breakdown.
- ≥3 dormant-silent specs identified with verbatim citation surface (per-spec evidence link to cycle directory + session-authored + missing runtime emit event class firing record).

**KT-N evaluation surface:** KT-2 fires iff <3 dormant-silent specs at retroactive scan close → halt + Rex paradigm re-disposition.

**Threats to validity at BE-D:** retroactive `cycle_authored` + `session_authored` assignment is approximation (git log + cycle close timestamp); per-class operational-definition variance may surface false-positive/false-negative dormant-silent classifications (per H2 + per-class structural verifier sketch at HR §3c).

### §10.5 BE-E: Forward-apply instrumentation (ROADMAP Phase 6)

**Scope:** wire spec_authoring_event + spec_implementation_event classes into `scripts/runtime_emit/emit.py` + `outputs/build_runner_events.jsonl` sink + author `docs/forward_apply_observation_protocol.md` + smoke-test forward-apply + KT-5 evaluation surface enabled.

**Acceptance criteria (per REQUIREMENTS §Per-Deliverable #9):**

- Runtime emit instrumentation enabled at Cycle 16 close.
- 1 synthetic spec_authoring_event + 1 synthetic spec_implementation_event emitted at BE-E session; JSONL sink received both events with PROV-O typed-edges + HC-11 access-permission enum.
- Forward-apply observation enabled at Cycle 16 close; Cycles 17 + 18 session-close gates fire on registry state.

**KT-N evaluation surface:** KT-5 firing surface enabled (H_main REFUTED if ≥2 NEW dormant-silent specs accumulate mid-Cycle-16 OR Cycles 17-18 forward-apply window).

**Threats to validity at BE-E:** instrumentation may not capture all spec-authoring surfaces (e.g., specs authored via Coach handoff edit may bypass `scripts/spec_authoring_check.sh`); longitudinal verdict (Cycles 17-18) depends on continued mechanism inheritance at subsequent scaffold.

<!-- /gate:experimental_design §10 stage_5_be_scope -->

## §11 5-Layer FINDINGS Authoring Scope (forward to close-arc Phase 7)

<!-- source: substrate §7 close-arc scope + Cycle 14 5-layer FINDINGS precedent -->

5-layer FINDINGS per Cycle 14 close precedent. Each layer addresses distinct evidence surface; cross-references between layers preserve traceability.

### §11.1 Layer 1 — Artifacts shipped

Per REQUIREMENTS §Deliverables 1-9: spec inventory artifact + pattern analysis artifact + substrate audit artifact (LA §6 addendum) + external research deliverable (LA §1 LOCKED) + KG-primary 14-field registry schema + SPARQL UPDATE authoring discipline + TWO-surface BLOCKING gate scripts + retroactive scan one-time fire JSON + forward-apply observation surface. Each artifact cited by canonical path + lock_commit.

### §11.2 Layer 2 — Mechanism characterization

Per H1-H8 hypothesis resolutions at HR §4 Resolution Log. Each resolution: CONFIRMED / REFUTED / INCONCLUSIVE / SUPERSEDED with evidence path. Cross-reference KT-1..KT-6 dispositions; surface honest carries (HC-RP-S2-3 + HC-RP-S2-4 + any new at Stage 5).

### §11.3 Layer 3 — Cell granularity (HYBRID PRIMARY EXTENSION-3)

Per HR §3a Cycle 16 EXTENSION-3 across 4×4×5 = 80 cells. Populated cells reported with empirical evidence; sparse cells acknowledged. Framework discriminative capacity for populated cells = load-bearing measurement (per Source 4 CARRY DISCIPLINE: "success metric = BOUNDARY-CONDITION-MAP RICHNESS").

### §11.4 Layer 4 — Hypothesis resolutions + Cycle 10 counterfactual + KT dispositions

Detailed evidence layer. Cycle 10 counterfactual analysis (H4) — apply Cycle 16 mechanism to Cycle 10 BE#5+BE#6 substrate state; observe whether the gate would have FAILED at Cycle 10 close (5-cycle dormancy surfaced). Per KT-1..KT-6 row: fired Y/N + evidence path + downstream implication.

### §11.5 Layer 5 — Honest gaps + KT firings + forward-cycle carries

Per `feedback_honest_evaluation.md` BINDING: honest gaps surfaced explicitly with quantified evidence. HC-RP-S2-3 (Wikidata supersedure PARTIAL) + HC-RP-S2-4 (Cycle 7 substrate-viability OPEN) + any KT firings + carries to Cycles 17-18 longitudinal verdict (done-criterion #10).

## §12 Cross-Reference Map (substrate §9 mechanical tests T1-T13)

<!-- source: kc-44 PD §3.3 mechanical tests T1-T13 + substrate §9 -->

| Test | Verification surface | Section |
|---|---|---|
| T1 | Placeholder count = 0 across all 5 Stage 3-4 canonicals + LA §6 addendum | REQUIREMENTS §Verification Surfaces |
| T2 | Stage 0-2 LOCKED preservation (`git diff` empty for OBS + RQS) | REQUIREMENTS §Constraints + this ED §1 Lock commit |
| T3 | HYBRID PRIMARY VERBATIM CARRY auditable | HR §3a + this ED §0a |
| T4 | All 5 canonicals + LA §6 addendum within line bands | Substrate §2 + per-artifact wc -l |
| T5 | H1-H8 carried to HR §3 with Cycle 16 specialization | HR §3 |
| T6 | KT-1..KT-6 pre-registered structurally | This ED §Field 6 + HR §3 surprise criteria |
| T7 | HC-11 partition (no IP-private content leaked) | REQUIREMENTS §Quality Requirements |
| T8 | DP#43 spot-read ≥4 sections across HR + ED + REQUIREMENTS + ROADMAP | Coach R3 |
| T9 | Amendments 2026-05-27a + 27b structurally encoded | This ED §Field 6 + §4a + REQUIREMENTS #5-#7 + ROADMAP Stage 5 |
| T10 | Cycle 6 substrate-viability evidence at LA §6 addendum | LA §6 addendum (this S2 RP authoring) |
| T11 | KG-primary 14-field schema reflected in HR + ED + REQUIREMENTS + ROADMAP | HR §3 + this ED §3 row 4 + §4a + REQUIREMENTS #5 + ROADMAP §1 |
| T12 | §6 aggregate coverage REVISED + KT-1 reassessment | LA §6 addendum |
| T13 | H4 counterfactual at FINDINGS Layer 4 | This ED §11.4 + HR §3 H4 row |

> Coach independent verifies all 13 mechanical tests at R3 close-eval per `feedback_honest_evaluation.md` BINDING; RP self-report not load-bearing.

## §13 Discipline + Constraint Summary

Bindings 1+2+6+7 (strategic_frame.md) + S155 + HC #34/#48/#51 + HC-11 partition (kc-44 PD §3.7) + DP#43/#44 all apply. Key Stage 3-4 deltas at this S2:

- **Binding 1 (≥80% external):** LA §1-§5 36 quotes already met at S1; LA §6 addendum is internal cross-validation NOT new external (per Binding 2 strict).
- **Binding 2 (internal as cross-validation NOT design anchor):** Cycle 6 KG inheritance is mechanism-class inheritance (Q-γ Option 2 unification carried from Cycle 6 BE#1 ship state) NOT design anchor; cell granularity at §0a EXTENSION-3 derived from RQ + 4 branches + 5-state taxonomy + 4-substrate-operation enumeration NOT mirror of Cycle 6 BE#1-#4 sequencing.
- **Binding 6 (RP authors all 5 canonicals + LA §6 addendum):** Coach composes substrate + dispatches + validates at R3; does NOT fill Stage 3-4 templates.
- **Binding 7 + S155:** no §11 overrides; no Coach-direct gate-script or canonical edits; KT fire → halt + surface to Rex; no Coach-direct Stage 5 fill.
- **HC #34 cap ≤20,000B decimal at substrate composition** (already satisfied at S2 dispatch substrate compose 19,937B).
- **HC #48 (a)+(b)+(c):** (a) single Write S7 pattern at compose + multi-round compression-via-Edit; (b) §1-§13 scope-split; (c) §0a 5-source CARRY by reference (not re-quoted).
- **HC-11 partition:** PUBLISHABLE in this ED = research question + branches + done-criteria + KT-1..KT-6 + cycle shape + 5-state taxonomy + 14-field schema + Cycle 6 KG inheritance narrative. PIPELINE-IP-PRIVATE excluded = agent-prompt internals + rubric algorithm bodies + dispatch substrate content + RT prompts + adversarial inputs (gitignored).
- **DP#44 refuse-on-missing-precondition** binding for Stage 5 Build-Runner: HALT + surface specific defect; do NOT fabricate.

## §14 Honest Carries (cross-ref REQUIREMENTS §Honest Carries Open + HR §5)

- **HC-RP1 (S1 carry):** RQS §3a +38L over upper band — load-bearing 4-branch × KT decomposition non-truncable per DP#44 + substrate §6+§8 T5+T8 mandate. NOT blocking; FLAG+CARRY per Mechanical Check #22.
- **HC #55 candidate (S1 carry):** stage-gate file-path mismatch (gate expects project-root; scaffold places stage 0-2 at docs/). Stage 3-4 canonicals at project-root resolve at S2; HC #55-class refinement carry for kc-44 PD inheritance.
- **HC #56 candidate (S1 carry):** question_gate §0 regex artifact (advisory non-academic citation heuristic). NOT blocking.
- **HC-RP-S2-3 NEW:** Wikidata supersedure PARTIAL (only `cycle6:rankingRationale` present; `wikibase:rank` + `prov:wasRevisionOf` absent at 2026-05-27 Coach probe). ED §4a constraint #4 binds Cycle 16 to author at Stage 5 BE-A schema extension OR detect at close as honest gap. Sub-KT-6 candidate; does NOT fire main KT-6 (4-PROV-O typed-edges + per-edge HC-11 enum + nanopub primitives operational).
- **HC-RP-S2-4 NEW:** Cycle 6 PARTIAL-CLOSED + Cycle 7 substrate-viability research-class cycle OPEN per Rex Decisions 1-4 2026-05-14g (BE#4 BUILT-NOT-PROMOTED HOLD). FINDINGS Layer 4 forward dependency carry; H5 KT-1 surface explicit acknowledgment; vendor-portable abstraction if Cycle 7 surfaces vendor pivot during Cycle 16 envelope.
- **HC-RP-S2-5 candidate:** KG-primary `runtime_emit_event_class = 'n/a'` over-use risk for methodology commitments per DP#26 carve-out — KT-3 firing surface (per H7) if ≥30% of methodology commitments take `n/a`. Cycle 16 forward-apply observation + KT-3 disposition.
- **HC-RP-S2-6 NEW (kc-44 calibration delta; S2 R3 anchoring-slip):** Coach R3 paradigm escalation of KT-1 literal-vs-intent ambiguity to Rex 2026-05-27 was operationally-disposable per foundational threshold-metric pre-registration discipline §10 (i)+(ii) — Amendment 2026-05-27b structural encoding (substrate-layer vs mechanism-layer distinction) already supplied the refinement substrate; Coach should have refined operational metric structurally rather than relay paradigm verdict. kc-44 inbound gate at Coach R3 paradigm escalation rubber-stamped Coach paradigm verdict instead of disposing per Discipline #10. Rex disposition (C) 2026-05-27 corrected operationally via metric-revision-within-intent. Surface to kc-45 PD inheritance for Discipline #10 anchoring-slip countermeasure refinement: kc-N inbound gate at Coach R3 paradigm escalation should screen literal-vs-intent threshold-metric ambiguity class for operational metric-refinement disposition BEFORE relaying paradigm verdict to Rex. Future cycles inherit refined-metric framing at ED §Field 6 + LA §6 to prevent recurrence.

> All honest carries surface explicitly at FINDINGS Layer 5; KT firings auto-route to paradigm escalation surface per substrate §4 + RQS §4.1 Alternative 2 reservoir.

## §15 Per-Discipline External-Grounding → Cycle 16 Mechanism Mapping (detailed)

<!-- source: LA §1 LOCKED 7 disciplines + LA §1.2 cross-discipline convergence matrix + LA §6b.1 5-import matrix -->

Per-discipline detailed mapping from LA §1 source quotes to Cycle 16 14-field schema element + structural verifier surface:

### §15.1 IETF (RFC 7322 + RFC 6982/7942) → Cycle 16

**Source mechanism:** Per-RFC Implementation Status section (RFC 6982 / RFC 7942) carrying implementation inventory as canonical-class field through standards-development lifecycle. Cultural anchor: "rough consensus and running code" (Clark 1992).

**Cycle 16 mapping:**

- `current_status` (5-state enum) ← per-RFC implementation-status field as canonical-class lifecycle citizen.
- `audit_trail_link` ← RFC supersedure tracking ("Obsoletes / Obsoleted by" headers; RFC 7942 obsoletes RFC 6982 example).
- `owner` ← per-RFC author + working-group chair + Area Director hierarchy → Cycle 16 owner attribution.
- Adaptation: voluntary peer-pressure → STRUCTURAL BLOCKING at TWO surfaces (cycle-close + session-close).

**Structural verifier surface:** SPARQL ASK against `/cycle6` for `?spec cycle16:current_status ?status` where status ∈ acceptable_set. The cultural framing (running code = evidence of maturity) is mechanized at gate-fire boundary.

### §15.2 Python PEP (PEP 1 + PEP 12) → Cycle 16

**Source mechanism:** Per-PEP 8-state lifecycle (Draft / Active / Accepted / Final / Provisional / Deferred / Rejected / Withdrawn / Superseded) + PEP-Delegate per-PEP human owner tracking implementation status.

**Cycle 16 mapping:**

- `current_status` (5-state) extends PEP state vocabulary (running ≈ PEP Active+Final; dormant-with-explicit-deferral ≈ PEP Deferred; killed ≈ PEP Rejected+Withdrawn; long-running = NEW state per Amendment 2026-05-27a for multi-cycle planned implementations; dormant-silent = NEW failure-mode state).
- `owner` ← PEP-Delegate per-PEP ownership.
- Adaptation: human social process → SPARQL ASK structural query at gate-fire time.

**Structural verifier surface:** Per-spec owner assignment is REQUIRED at registry write boundary (per §4a constraint #1); PEP-Delegate analog encoded at `owner` field.

### §15.3 OpenAPI / Swagger → Cycle 16

**Source mechanism:** Contract-first API design + spec-as-single-source-of-truth + tooling-generated code (openapi-generator, swagger-codegen) + CI-integrated drift detection (Dredd, Schemathesis, oasdiff).

**Cycle 16 mapping:**

- `runtime_emit_event_class` ← spec-binds-to-runtime-emit (analog to OpenAPI spec-binds-to-generated-code).
- TWO-surface BLOCKING gate ← CI-integrated drift detection on PR (analog: gate fires at cycle-close + session-close not at PR boundary).
- Adaptation: code-generation by tooling (template-driven) → SPARQL UPDATE INSERT DATA writes registry row at authoring time (not code generation; spec materialization as KG row).

**Structural verifier surface:** TWO-surface BLOCKING gate fires SPARQL ASK against `/cycle6` per Cycle 14 four-gate skeleton extension (H6 binding).

### §15.4 Design by Contract (Meyer 1992 + Eiffel + icontract/deal/beartype) → Cycle 16

**Source mechanism:** Preconditions + postconditions + invariants enforced at code boundaries via compiler-emitted assertion checks; assertion violation fires exception at exact frame where contract was breached.

**Cycle 16 mapping:**

- Gate-script-as-contract-assertion at spec-lifecycle boundaries (cycle-close + session-close) ← runtime contract assertion at code boundaries.
- Spec dormancy fires gate FAIL at exact session-close where dormancy threshold exceeded ← contract violation surfaces at exact frame.
- Adaptation: DbC compilation-options-enable/disable → gate `--advisory-mode` opt-in WARN flag (analog).

**Structural verifier surface:** SPARQL ASK body in gate script encodes the per-spec contract; gate fires per-invocation at gate-time mechanically.

### §15.5 Feature-flag governance (LaunchDarkly + GrowthBook + Optimizely + FlagShark) → Cycle 16

**Source mechanism:** Per-flag lifecycle states (5: Live / Ready for code removal / Ready to archive / Archived / Deprecated) + automated stale-flag detection at temporal thresholds (LaunchDarkly 30d-created + 7d-inactive; GrowthBook 14d-unchanged + uniform-value-serve; Optimizely 30d-no-modify + no-traffic) + Code References scanning flag-key → file:line.

**Cycle 16 mapping:**

- `current_status` 5-state taxonomy directly mirrors LaunchDarkly 5-state lifecycle (vocabulary adapted to spec-implementation grain).
- `dormancy_detection_threshold_sessions` (default 3) is session-cadence-scaled analog of LaunchDarkly's 30d/7d days.
- INFRASTRUCTURE_INDEX.md auto-link spec → project artifact ← LaunchDarkly Code References auto-link flag-key → file:line.
- Adaptation: per-flag-firing-in-user-traffic → per-spec-runtime-emit-event-firing-to-JSONL-sink.

**Structural verifier surface:** PRIMARY adjacent-field import per LA §6b method import ranking + LA §6b.1 row 1 cross-domain mechanism validity pre-check (domain distance 3; YES with adaptation).

### §15.6 ADR governance (Nygard 2011 + Tyree & Akerman 2005) → Cycle 16

**Source mechanism:** Per-decision 4-state lifecycle (Proposed → Accepted → Deprecated / Superseded) + immutable-post-acceptance + "Supersedes / Superseded By" two-way relations.

**Cycle 16 mapping:**

- `current_status` 5-state extends ADR 4-state (adds `long-running` per Amendment 2026-05-27a).
- `audit_trail_link` ← ADR two-way supersedure relation.
- Wikidata `wikibase:rank` + `prov:wasRevisionOf` (HC-RP-S2-3 carry) ← ADR supersedure-link discipline.
- Adaptation: process-discipline → gate-script-mechanical.

**Structural verifier surface:** SPARQL ASK against `/cycle6` queries per-spec supersedure chain; ADR's immutable-post-acceptance preserved via Binding 7 ("LOCKED bodies").

### §15.7 Parnas precise documentation + tabular notations → Cycle 16

**Source mechanism:** Documentation as canonical-class engineering artifact maintained DURING development (not after); tabular notations enumerating function behavior under all conditions to eliminate ambiguity.

**Cycle 16 mapping:**

- 14-field registry row IS the precise documentation in Parnas-style structured form (per-field-required at authoring time).
- Spec-authoring-time discipline (Branch 4.2 + REQUIREMENTS §Per-Deliverable #6) directly inherits Parnas's "document-during-development" framing.
- Adaptation: per-function mathematically-precise spec → per-spec structurally-required field tuple at KG row.

**Structural verifier surface:** SPARQL UPDATE INSERT DATA at registry write boundary requires all non-nullable fields present; "incomplete documentation" surfaces structurally at authoring time, not at downstream read.

## §16 Cycle 10 Counterfactual Analysis Pre-Registration (H4 forward-binding)

<!-- source: substrate §9 T13 + Cycle 10 RUNTIME_EMIT_SPEC.md substrate at ~/cycle_10_autonomous_cycle_apparatus_build/ -->

Counterfactual analysis surface at FINDINGS Layer 4 (H4 binding): apply proposed Cycle 16 mechanism to Cycle 10 BE#5+BE#6 substrate state. Pre-registered counterfactual reasoning:

### §16.1 Cycle 10 BE#5+BE#6 substrate state (factual)

- **BE#5+BE#6 authoring** (Cycle 10; circa 2026-04): RUNTIME_EMIT_SPEC.md authored at `~/cycle_10_autonomous_cycle_apparatus_build/docs/RUNTIME_EMIT_SPEC.md` defining `drift_telemetry` event class + per-event schema; lock_commit at BE#5+BE#6.
- **Cycles 11-14:** runtime emission did NOT wire into runtime; spec remained at "documentation" state across 4 cycles of close-reviews.
- **Cycle 15-S7 (2026-05-27):** runtime emission finally wired into govML scaffold (`scripts/runtime_emit/` + `outputs/*_events.jsonl`) only because Rex explicitly disposed govML back-port at that surface.
- **Gap:** 5 cycles dormant (BE#5+BE#6 ~ Cycle 10 close → Cycle 15-S7 ~5 cycles ~ 2.5 months at pipeline cadence).

### §16.2 Counterfactual Cycle 16 mechanism application

If Cycle 16 mechanism had been in place at Cycle 10 BE#5+BE#6 authoring:

1. **Authoring-time gate (Branch 4.2):** RUNTIME_EMIT_SPEC.md authoring would have triggered `scripts/spec_authoring_check.sh`. Required fields: `spec_id` (e.g., `cycle10:drift_telemetry_spec`) + `spec_type` (Schema) + `owner` (Coach Cycle 10) + `target_session` (Cycle 10 close) + `runtime_emit_event_class` (`drift_telemetry`) + `dormancy_detection_threshold_sessions` (3) — all 14 fields enumerable at authoring time.
2. **SPARQL UPDATE INSERT DATA** at `/cycle6` materializes the registry row + nanopublication 3-graph triplet + PROV-O typed-edges + HC-11 enum.
3. **Cycle 10 close gate (Branch 4.3):** `scripts/spec_implementation_present_gate.sh` SPARQL ASK against `/cycle6` → query: `ASK { ?spec cycle16:spec_id "cycle10:drift_telemetry_spec" . ?spec cycle16:current_status ?status . FILTER(?status IN (cycle16:running, cycle16:dormant-with-explicit-deferral, cycle16:killed, cycle16:long-running)) }`. At Cycle 10 close, the actual state was: spec authored + no runtime emit event firing observed yet. `current_status` would have been `dormant-silent` (no explicit deferral; runtime emit not firing). Gate would have FAILED at Cycle 10 close → BLOCKING → Cycle 10 cannot close until status transitioned to acceptable_set.
4. **Cycle 10 close blocked by gate** → Cycle 10 close would have required either (a) wiring runtime emission inside Cycle 10 (transitioning status to `running`), OR (b) explicit deferral to a named target_session with Rex authorization (transitioning to `dormant-with-explicit-deferral`), OR (c) explicit kill (transitioning to `killed`). Default would have been (a) wire runtime emission — closing the gap at Cycle 10 close, NOT Cycle 15-S7.

### §16.3 Counterfactual evaluation surface

- **H4 CONFIRMED** if counterfactual analysis demonstrates Cycle 16 mechanism would have closed the 5-cycle gap at Cycle 10 close (per §16.2 reasoning chain).
- **H4 REFUTED** if counterfactual surfaces that the mechanism would NOT have caught the case (e.g., because `runtime_emit_event_class = 'n/a'` would have been a defensible disposition for RUNTIME_EMIT_SPEC.md at authoring time — note: this is implausible since the spec IS the runtime emit specification, so `n/a` would be self-contradictory; H4 CONFIRMED hypothesis preliminarily strong).
- **DP#26 carve-out interaction:** Cycle 10 RUNTIME_EMIT_SPEC.md is `spec_type = Schema` (not methodology commitment); DP#26 carve-out for `n/a` applies to methodology commitments only. Schemas MUST have non-null `runtime_emit_event_class`. Counterfactual reinforces H4 CONFIRMED preliminary.

## §17 KT-1 Disposition Recommendation Detail (defer to LA §6 addendum)

<!-- source: substrate §5 KT-1 reassessment task at LA §6 addendum + Coach R3 mechanical test T12 -->

KT-1 disposition is OPERATIONALLY locked at LA §6 addendum per substrate §5 task. This ED §17 surfaces the reasoning chain that RP applies at LA §6 addendum authoring:

### §17.1 Pre-27b coverage (LA §6b.2 at S1 close)

- RIDE F-D Hybrid composition: ~30% (discoverability + enforcement framework at infrastructure-USE scope).
- research_depth_enforcement_automation: ~20% (enforcement primitive class + LLM-judge primitive).
- Cycle 14 four-gate: ~20% (template-class structural-gate pattern at artifact-EXISTS predicate scope).
- **Total ≈ 70% per LA §6b.2 aggregate coverage assessment.**
- **KT-1 disposition at S1 close: DOES NOT FIRE** (< 80% threshold).

### §17.2 Cycle 6 KG addition (S2 addendum estimation)

- Cycle 6 KG mechanism-class inheritance (Q-γ Option 2 unification): adds ~20-25% mechanism inheritance per Amendment 2026-05-27b.
  - Per-edge HC-11 access-permission enum: inherits from BE#1 contract (11,223+ usages operational).
  - PROV-O 4 typed-edges orphan-refusal discipline: inherits from BE#1 contract.
  - Wikidata supersedure pattern: PARTIAL (HC-RP-S2-3 carry; full inheritance pending Stage 5 BE-A extension).
  - Nanopublication 3-graph pattern: operational across 46 named graphs.
  - SPARQL query endpoint substrate: operational at 246K-quad scale with ≤0.5s latency.

### §17.3 Post-27b revised coverage assessment + Rex paradigm-ruling 2026-05-27 disposition (C) metric-revision-within-intent

**Pre-Rex-ruling raw aggregate estimate (S2 RP initial authoring):** Pre-27b ≈70% + Cycle 6 KG ~20-25% = ≈90-95% revised aggregate coverage under unrefined "any inheritance" metric. RP surfaced KT-1 as paradigm-class question to Coach R3 + Rex per Binding 7 (literal-vs-intent ambiguity at substrate-layer vs mechanism-layer distinction).

**Coach R3 paradigm escalation to Rex 2026-05-27** per 3-test pre-escalation gate (end-state convergence + gotcha #16 + S176) returning 3/3 PARADIGM. Rex disposition (C) 2026-05-27: **metric-revision-within-intent per foundational threshold-metric pre-registration discipline §10 (i)+(ii)** — Amendment 2026-05-27b already encoded the substrate-vs-mechanism distinction structurally (Cycle 6 KG inherits STORAGE substrate; Cycle 16 authors SPEC-IMPLEMENTATION MECHANISM); KT-1 literal-vs-intent ambiguity resolves operationally by refining operational metric to measure intent faithfully.

**Refined operational metric (Rex disposition (C)):** "≥80% of MECHANISM-LAYER scope, excluding pure substrate-layer inheritance (storage primitives + access-permission enum + provenance edges + endpoint substrate)."

**Refined coverage recalculation:**

- Pre-Amendment-27b ~70% mechanism-layer coverage (RIDE F-D Hybrid + research_depth_enforcement_automation + Cycle 14 four-gate; unchanged under refined metric since these substrates ARE mechanism-class at composition + enforcement + structural-gate respectively).
- Cycle 6 KG mechanism-layer inheritance ~5-15% (HC-11 partition semantics + PROV-O orphan-refusal discipline at write boundary; storage + endpoint + nanopublication 3-graph + raw HC-11 enum primitive + raw PROV-O typed-edge primitive excluded as substrate-layer per refined metric).
- **Net mechanism-layer coverage post-inheritance ~75-85%.**
- **KT-1 disposition under refined metric: DOES NOT FIRE.** Marginal at literal ≥80% reading; firmly DOES NOT FIRE under intent reading. **Cycle 16 proceeds with full SI scope** (Branches 1-4 all in-scope; not narrowed to gap-filling only).

### §17.4 Counter-considerations (HC-RP-S2-3 + HC-RP-S2-4 bound the inheritance)

- HC-RP-S2-3 (Wikidata supersedure PARTIAL): only `cycle6:rankingRationale` present; `wikibase:rank` + `prov:wasRevisionOf` absent. Reduces full mechanism inheritance from Cycle 6 KG by ~5-10% (supersedure-tracking is one of the 7 mechanism dimensions at LA §1.2; PARTIAL inheritance).
- HC-RP-S2-4 (Cycle 7 substrate-viability OPEN): if Cycle 7 surfaces vendor pivot, mechanism inheritance becomes conditional. Does NOT reduce S2 RP authoring decision (Cycle 7 OPEN does not block Cycle 16 mechanism design); FINDINGS Layer 4 forward dependency carry.

### §17.5 RP disposition recommendation + Rex paradigm-ruling (C) operationalization

RP at S2 authoring surfaced KT-1 as paradigm-class question to Coach R3 + Rex per Binding 7. Coach R3 3-test pre-escalation gate returned 3/3 PARADIGM; surfaced to Rex 2026-05-27. **Rex disposition (C) 2026-05-27: metric-revision-within-intent** per foundational threshold-metric pre-registration discipline §10 (i)+(ii). Operationalization: KT-1 row at §Field 6 refined to mechanism-LAYER scope (substrate-layer inheritance excluded); LA §6.X.1 + §6.X.2 + ED §17.3 + DECISION_LOG entry encode disposition (C) at all surfaces. Refined-metric coverage ~75-85% mechanism-layer; KT-1 DOES NOT FIRE; Cycle 16 proceeds with full SI scope.

**Calibration delta carried forward (HC-RP-S2-5):** Coach R3 paradigm escalation was operationally-disposable per threshold-metric pre-registration discipline §10 (i)+(ii) — Amendment 2026-05-27b structural encoding (substrate-layer vs mechanism-layer) already supplied refinement substrate; Coach should have refined operational metric structurally rather than relay paradigm verdict. kc-44 inbound gate at Coach R3 paradigm escalation should catch this class going forward. Surface to kc-45 PD inheritance for Discipline #10 anchoring-slip countermeasure refinement.

## §18 Cycle 16 Compute + Resource Plan

<!-- source: REQUIREMENTS §Constraints + compute_resources DB + Cycle 6 substrate access -->

| Resource | Allocation | Use surface |
|---|---|---|
| Azure VM (7.7 GiB) | Primary host | All SPARQL UPDATE/ASK at `/cycle6` endpoint; retroactive scan; gate-script invocation; RP/Coach/Builder session compute |
| Apache Jena Fuseki PID 479112 | Local on Azure (localhost:3030 `/cycle6`) | KG substrate; 246K quads / 46 named graphs at S2 entry |
| Mac Mini M4 Pro (48GB / 16-core GPU) via Tailscale | Reserve for larger-graph batched SPARQL if needed | Not anticipated; Coach probe latency ≤0.5s at current scale |
| `singularity.db` | Cross-engine state substrate | Read-only at Stage 3-4 (S1 close DB queries locked) |
| Disk: `~/cycle_16_*` | Project root | ~50KB for stage 0-2 + ~150KB at S2 close after Stage 3-4 + ~500KB-1MB at Stage 5 BE-class close |

> No GPU or large-dataset dependency at this cycle scope. Compute envelope well within Azure VM capacity per Cycle 14 multi-BE precedent.

---

## §5 Stage 5 Acceptance Verdicts (Build-Runner fill at Cycle 16 close-arc S8 per kc-46 PD §3.3 + REQUIREMENTS §Verification Surfaces)

<!-- source: Cycle-16-S8 close-arc Stage 5 fill per substrate §3 OUTPUT #3 + DECISION_LOG D-S3-1..D-S7-1 -->
<!-- gate:experimental_design §5 stage_5_acceptance required -->

Per-BE Stage 5 acceptance verdicts + per-BE close evidence + D-S3-1..D-S7-1 paradigm disposition references. ED §0-§4 + §0a + §Field 6 + §4a + §10 + §11 + §15 + §16 + §17 + §18 LOCKED at S2 close per Binding 7; ED §5+ Stage 5 fill permitted at this S8 per kc-46 PD §3.3 + REQUIREMENTS §Verification Surfaces.

### §5.1 BE-A Acceptance (Phase 2; ROADMAP §1; Done #5)

**Acceptance verdict: PASS-all (6 of 6 thresholds per ACCEPTANCE_CRITERIA §1).** Per `outputs/cross_system_validation_be_a.json` be_a_smoke_results array: 14-field schema TTL materialized at `docs/spec_registry_schema.ttl` + SHACL shapes at `spec_registry_shapes.shacl.ttl`; 3-TB SPARQL UPDATE smoke ALL_PASS at PROD `/cycle6` (TB-1 AgentContract HTTP 200 / TB-2 Schema HTTP 200 / TB-3 MethodologyCommitment HTTP 200; DROP cleanup HTTP 200; readback returns 13-14 triples per spec); pyshacl conforms=True for conforming fixture + 8 violations ≥4 threshold for non-conforming fixture; SPARQL DESCRIBE returns all 14 predicates per test spec.

**Close evidence:** `outputs/cross_system_validation_be_a.json` + `outputs/build_runner_events.jsonl` write.event rows + 5 BE-class templates filled to 0 placeholders + 3 NEW docs/ artifacts + 5 NEW outputs/ supporting + DECISION_LOG D-S3-1 BUILT verdict.

**Paradigm disposition reference: D-S3-1.** HC-RP-S2-3 RESOLVED-VIA-NAMESPACE-EQUIVALENCE via Path α (`cycle16:Spec rdfs:subClassOf c6:Statement` SHACL polymorphism accepts `c6:rank` + `c6:supersedesRef` predicates; Cycle 6 LOCKED ontology UNMODIFIED via `git -C ~/cycle_6_unified_substrate_build diff runtime/jena/` = 0); Path γ NOT TAKEN per Binding 7. H6 + H7 CONFIRMATION CANDIDATES surfaced; KT-4 + KT-6 DO NOT FIRE; D-S2-1 refined-metric KT-1 disposition preserved. 3 HC-BE-A NEW honest carries (HC-BE-A-1 §1 row 4 wording — RESOLVED at S4 §10.3 5-row per-state conditional-readback table; HC-BE-A-2 Path α inheritance carry; HC-BE-A-3 docs/ scaffolding-path divergence STANDING). HC #50 baseline MAINTAINED.

### §5.2 BE-B Acceptance (Phase 3; ROADMAP §2; Done #6)

**Acceptance verdict: PASS-all (6 of 6 thresholds per ACCEPTANCE_CRITERIA §10.1 rows 7-12).** Per `outputs/be_b_dogfooding_results.json` all_3_pass=true: 3-TB dogfooding to PRODUCTION `/cycle6` registry graphs ALL PASS (TB-1 AgentContract HTTP 200 244ms write 9ms readback 13 triples; TB-2 Schema HTTP 200 218ms write 5ms readback 13 triples; TB-3 MethodologyCommitment HTTP 200 200ms write 8ms readback 15 triples + DP#26 n_a_rationale literal present). `scripts/spec_registry_authoring.py` 29.8KB Python wrapper at canonical path with DP#44-compliant refuse-on-missing-precondition behavior; SPARQL UPDATE INSERT DATA gate body defined; BLOCKING rejects if required (non-nullable) fields absent.

**Close evidence:** `outputs/be_b_dogfooding_results.json` + `outputs/spec_registry_events.jsonl` 3 spec_registry.write.event rows + `~/ml-governance-templates/VERSION` v2.8.3 + `~/ml-governance-templates/scripts/init_project.sh` `install_spec_registry_authoring_discipline()` ADDITIVE-APPEND function L211+ + `~/ml-governance-templates/templates/build/spec_registry/` NEW dir 5 files + DEPLOYMENT_LOG §2 row 2 + BUILD_DECISION_LOG §2 row 2 + DECISION_LOG D-S4-1 BUILT verdict.

**Paradigm disposition reference: D-S4-1.** KT-3 firing surface evaluation: 0 author refusals captured across all 4 classes; cumulative (a)+(b)+(d) = 0 < threshold 3 → KT-3 DOES NOT FIRE; HC #59 BINDING countermeasure NOT TRIGGERED. Done #6 SHIPPED. Rex back-port directive 2026-05-27 4-repo paired commit operationalized 1st time (cycle_16 + EMABS + Moonshots + govML); without back-port Cycle 17+ fresh-scaffolded projects do NOT inherit authoring discipline. HC-BE-A-1 RESOLVED at §10.3; 2 NEW HC-BE-B honest carries (HC-BE-B-1 Pattern 19 first-arc BREAK cross-system back-port density n=26; HC-BE-B-2 production registry graphs without DROP-GRAPH cleanup intentional per "no spec lands without registry row" discipline). Pattern 19 BREAK at n=26 recovered via 6-Edit-round second-pass to 19,591B WITHIN-CAP. HC #45 ADDITIVE-APPEND precedent class extended to n=3 (Cycle-15-S3 init_project.sh array fix + Cycle-15-S7 install_runtime_emit_substrate + Cycle-16-S4 install_spec_registry_authoring_discipline). HC #50 baseline MAINTAINED.

### §5.3 BE-C Acceptance (Phase 4; ROADMAP §3; Done #7)

**Acceptance verdict: PASS-all (6 of 6 thresholds per ACCEPTANCE_CRITERIA §11.1 rows 13-18).** Per `outputs/cross_system_validation_be_c.json` all_3_pass=true: 3-TB dogfooding cycle_close_gate_holistic + session_close_gate_holistic ALL PASS; cycle_close_gate_holistic verdict=BLOCKED matches_expected=true on TB-3 dormant-silent load-bearing surface; baseline_equal_post_cleanup=true at 246101 triples (DROP cleanup verified per dispatch substrate §4); JSONL fire.event sink ≥4 rows (4 present_gate + 4 session_close_gate). 2 NEW gate scripts at govML scripts/ at canonical path with bash shebang + DP#44-compliant refuse-on-missing-precondition behavior.

**Close evidence:** `outputs/cross_system_validation_be_c.json` + `outputs/spec_implementation_gates_events.jsonl` 8 fire.event rows + `~/ml-governance-templates/VERSION` v2.8.4 + `~/ml-governance-templates/scripts/init_project.sh` `install_spec_implementation_gates()` ADDITIVE-APPEND + L632 call-site + `~/ml-governance-templates/scripts/check_all_gates.sh` build-class branch BLOCKING-loop 5th-gate + ADVISORY-loop append + `~/ml-governance-templates/templates/build/spec_implementation_gates/SPEC_IMPLEMENTATION_GATES_OBLIGATION.md` NEW + DEPLOYMENT_LOG §2 row 3 + BUILD_DECISION_LOG §2 row 3 + DECISION_LOG D-S5-1 BUILT verdict.

**Paradigm disposition reference: D-S5-1.** H6 CONFIRMED (skeleton structural equivalence to `k_register_present_gate.sh` 231L); divergence categories (a)+(b)+(c)+(d) trivial naming/predicate-body/output-filename/ADVISORY-default; **divergence (e) JSONL fire.event emit block OPERATIONAL ACCEPT per HC #59 BINDING literal-vs-intent metric-revision-within-intent** (later-evolved runtime emit discipline applied to NEW gate NOT primitive-class extension; H6 intent preserved). HC-BE-C-1 op carry. KT-4 DOES NOT FIRE (all 3 firing-surface signals negative). KT-3 carry-forward LOCKED `false`. Rex back-port directive STANDING operationalized 2nd time; HC #45 ADDITIVE-APPEND precedent class extended to n=4. Pattern 19 BREAK at n=27 recovered via 6-Edit-round second-pass to 19,733B WITHIN-CAP. 3 NEW HC-BE-C honest carries (HC-BE-C-1 H6 divergence (e); HC-BE-C-2 audit-only TB-2 abstract reference; HC-BE-C-3 audit-only per-TB holistic verdict granularity). HC #50 baseline MAINTAINED.

### §5.4 BE-D Acceptance (Phase 5; ROADMAP §4; Done #1 + Done #8)

**Acceptance verdict: PASS-all (6 of 6 thresholds per ACCEPTANCE_CRITERIA §12.1 rows 19-24).** Per `outputs/retroactive_scan_cycle_1_15_run.json`: h1_total_enumerated=232 distinct cycle16:Spec ≥ 90 floor (2.6x multiplier); h3_dormant_silent_aggregate=137 ≥ 3 threshold (45x floor); per_class_strengthening_n_ge_3 ALL 4 PASS (a=9 + b=10 + c=154 + d=59 distinct; smallest class = 9 = 3x floor); per-spec materialization at PROD `/cycle6` via BE-B `register_spec()` with `retroactive_classification=true` annotation per ROADMAP §4.2 dependency 2 (IRI-prefix `spec_retroactive_*` per §12.5 rollback discriminator — see HC-BE-E-1 documentation-only carry at FINDINGS Layer 4); aggregate 4×5 = 20-cell breakdown via SPARQL SELECT GROUP BY returns 92 running + 0 dormant-with-explicit-deferral + 137 dormant-silent + 0 killed + 3 long-running; 8 initial DP#26 carve-out refusals → 8 retry successes with explicit n_a_rationale per spec-class context; NO DROP GRAPH at BE-D close (retroactive registry rows persist for BE-E forward-apply observation baseline reconstruction). Production graph baseline pre-BE-D = 6 default graph triples; post-BE-D full triple store = 250,773 triples.

**Close evidence:** `outputs/retroactive_scan_cycle_1_15_run.json` ~190KB + `outputs/spec_registry_events.jsonl` 283 rows (= 6 BE-B baseline + 268 BE-D writes + 8 SHACL refusal events + 1 retry-related) + `outputs/build_runner_events.jsonl` retroactive_scan_run.event single-fire + DEPLOYMENT_LOG §2 row 4 + BUILD_DECISION_LOG §2 row 4 + 3 §12 BE-D appends at docs/{ARTIFACT_CONTRACT,RUNTIME_EMIT_SPEC,ACCEPTANCE_CRITERIA}.md +307/0 insertions + DECISION_LOG D-S6-1 BUILT verdict.

**Paradigm disposition reference: D-S6-1.** H1 CONFIRMED + H3 CONFIRMED + KT-2 DOES NOT FIRE at empirical threshold (literal 137 >> 3; HC #59 BINDING screen N/A no literal-vs-intent ambiguity). **HC-BE-D-1 NEW SURFACED**: write-boundary enforcement gap (specs written to filesystem without calling BE-B authoring wrapper) → Cycle 18 scope per Rex 2026-05-27 Option A disposition + Option B split-sequential framing. Cycle 16 closes in-registry dormancy gap; does NOT close write-boundary discoverability gap; BE-E inherits SAME blind spot. KT-3 + KT-4 NOT RE-EVALUATED at BE-D (carry-forward LOCKED). HC #45 ADDITIVE-APPEND precedent class does NOT apply at BE-D (NO govML touch per work-host boundary discipline; BE-D is one-time within-cycle artifact). 3-repo paired commit at S6 close (NO govML). Pattern 19 BREAK at n=28 recovered via 3-Edit-round to 19,967B WITHIN-CAP. HC #48 (d) sub-cycle scope-decomposition refinement candidate STANDING refined empirically at n=3 — within-cycle BE-class artifact density profile distinguishes from cross-system back-port BE-class density profile. HC #50 baseline MAINTAINED.

### §5.5 BE-E Acceptance (Phase 6; ROADMAP §5; Done #9 + Done #10 partial H8 evaluation surface)

**Acceptance verdict: PASS-all (6 of 6 thresholds per ACCEPTANCE_CRITERIA §13.1 rows 25-30).** Per `outputs/forward_apply_observation_events.jsonl`: 4 fire.event rows (2 spec_authoring_event + 2 spec_implementation_event for TB-1 AgentContract synthetic + TB-2 Schema synthetic; PROV-O 4 typed-edges per spec — `wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy` per Cycle 6 BE#1 contract; HC-11 `c6:publishable` access_permission enum; DROP GRAPH cleanup HTTP 200 + post-DROP test graph COUNT=0 verified). `scripts/runtime_emit/emit.py` extended ADDITIVELY (2 NEW event class constants `SPEC_AUTHORING_EVENT_CLASS` + `SPEC_IMPLEMENTATION_EVENT_CLASS` + sink-routing helper `forward_apply_emit()` + namespace constant `FORWARD_APPLY_OBSERVATION_NAMESPACE` + sink default `FORWARD_APPLY_OBSERVATION_SINK_DEFAULT`; `emit_event()` core signature UNCHANGED per Cycle 10 §0 schema_version=0.1 LOCKED — Python `inspect.signature(emit_event)` returns Cycle 15 BE#4 baseline signature). `docs/forward_apply_observation_protocol.md` NEW ~143L 8 §N sections; 0 placeholders; HC-11 partition declared inline per Binding 8 BIND. Forward-apply observation enabled at Cycle 16 close; Cycles 17 + 18 session-close gates fire on registry state.

**Close evidence:** `outputs/forward_apply_observation_events.jsonl` 4 fire.event rows + `outputs/build_runner_events.jsonl` forward_apply_smoke.event single-fire + `outputs/spec_registry_events.jsonl` append-only growth (smoke-test test-graph DROP-cleaned at smoke close) + `~/ml-governance-templates/VERSION` v2.8.5 + `~/ml-governance-templates/CHANGELOG.md` NEW v2.8.5 entry + DEPLOYMENT_LOG §2 row 5 + BUILD_DECISION_LOG §2 row 5 + ARTIFACT_CONTRACT §13 + RUNTIME_EMIT_SPEC §13 (2 NEW event class schemas) + ACCEPTANCE_CRITERIA §13 BE-E appends + `docs/forward_apply_observation_protocol.md` NEW + `scripts/runtime_emit/emit.py` ADDITIVE extension + DECISION_LOG D-S7-1 BUILT verdict.

**Paradigm disposition reference: D-S7-1.** H8 evaluation surface ENABLED at BE-E (FINAL VERDICT DEFERRED to Cycle 18 cumulative ≥2-cycle window per HR §3 H8). KT-5 DOES NOT FIRE empirical count=0 at BE-E close (IRI-prefix discriminator `spec_retroactive_*` per BE-D §12.5 rollback discriminator; naive ASK against `retroactiveClassification=true` predicate returned false-alarm 28 → IRI-prefix corrected to 0; HC #59 BINDING screen applied — pre-registered SI kill condition not operationally-revisable). HC-BE-D-1 PRESERVED at BE-E (same blind spot — observes only what's registered). HC-BE-E-1 NEW documentation-only carry (BE-D §12 ARTIFACT_CONTRACT promised `retroactiveClassification=true` annotation predicate; §12.5 rollback uses IRI-prefix — documentation-only correction; BE-D output stands). Honest gap re mid-Cycle-16 observation window S7→S8 adequacy for H8 longitudinal verdict (DEFERRED to Cycle 18 per design per HR §3 H8). KT-2 + KT-3 + KT-4 NOT RE-EVALUATED at BE-E (carry-forward LOCKED `false` from BE-B + BE-C + BE-D). govML v2.8.5 ADDITIVE-APPEND back-port: HC #45 chain extension to n=5 (v2.8.2 runtime_emit + v2.8.3 spec_registry + v2.8.4 spec_implementation_gates + v2.8.5 forward_apply_observation); LOCKED bodies of 3 existing install functions UNMODIFIED via `git diff` 0 on those function line ranges. 4-repo paired commit at S7 close per Rex back-port directive STANDING (cycle_16 `2adf319` + EMABS `e0c5ad0` + Moonshots + govML `72a039a`). Pattern 19 n=29 first-arc WITHIN-CAP (19,596B/0.9798× + 19,886B/0.9943× for protocol artifact); 2-pass compression NOT INVOKED. HC #50 baseline MAINTAINED.

### §5.6 Aggregate Stage 5 close ledger (S3-S7 + S8 close-arc)

| BE | Session | Verdict | Done items | KT evaluation | HC NEW |
|---|---|---|---|---|---|
| BE-A | S3 | PASS-all (6/6) | #5 SHIPPED | KT-4 + KT-6 DO NOT FIRE | HC-BE-A-1 RESOLVED at S4 / HC-BE-A-2 Path α / HC-BE-A-3 docs/ scaffolding STANDING |
| BE-B | S4 | PASS-all (6/6) | #6 SHIPPED | KT-3 DOES NOT FIRE | HC-BE-B-1 Pattern 19 cross-system back-port density / HC-BE-B-2 production registry without DROP-cleanup intentional |
| BE-C | S5 | PASS-all (6/6) | #7 SHIPPED | KT-4 DOES NOT FIRE; H6 CONFIRMED with HC-BE-C-1 op carry | HC-BE-C-1 H6 divergence (e) / HC-BE-C-2 audit-only abstract reference / HC-BE-C-3 audit-only holistic verdict |
| BE-D | S6 | PASS-all (6/6) | #1 + #8 SHIPPED | KT-2 DOES NOT FIRE; H1 + H3 CONFIRMED | **HC-BE-D-1 write-boundary enforcement gap → Cycle 18 scope per Rex Option B** |
| BE-E | S7 | PASS-all (6/6) | #9 SHIPPED + #10 partial H8 evaluation surface ENABLED | KT-5 DOES NOT FIRE empirical count=0; H8 evaluation surface ENABLED (DEFERRED to Cycle 18) | HC-BE-E-1 NEW documentation-only BE-D doc-vs-implementation discriminator gap |
| Close | S8 (THIS) | 9 of 10 Done items CLOSED; #10 partial H8 forward Cycle 18 by design | 5-layer FINDINGS + HR §4 fill + ED §5+ fill + ROADMAP §7 annotation + state.json transition + 3-repo paired commit | 0 of 6 KT fire aggregate | n/a (close-arc audit-only; no new BE-class artifacts per §10 refusal anchor 7) |

**Aggregate decision rule.** 9 of 10 SI Done Definition items CLOSED in-cycle at S8; Item #10 partial (5-layer FINDINGS + paired commit CLOSED THIS S8; H8 longitudinal final verdict DEFERRED to Cycle 18 close per HR §3 H8 design). 0 of 6 KT triggers fire. H1 + H3 + H6 + H7 + H4 (counterfactual) CONFIRMED; H2 + H5 CONFIRMED-WITH-CAVEAT (H5 under refined metric per D-S2-1); H8 OPEN forward Cycle 18 by design. HC-BE-D-1 PRESERVED → Cycle 18 scope per Rex Option B split-sequential; HC-BE-E-1 NEW documentation-only Layer 4 surface. HC #50 zero-Rex-escalation baseline MAINTAINED cumulative kc-45+46 across 10 close-eval rounds.

<!-- /gate:experimental_design §5 stage_5_acceptance -->

> Per `feedback_honest_evaluation.md` BINDING: Build-Runner self-report NOT load-bearing; Coach R3 independent verification at every BE close per kc-46 PD §3.3 T1-T13 mechanical tests is the authoritative verdict. All 5 BE close-evals PASSED Coach independent verification at corresponding actual-fire commits (S3 + S4 + S5 + S6 + S7).

<!-- amendment_2026_05_28a_extension_start -->

## §5.recovery Stage 5 Acceptance Criteria — BE-F + BE-G + BE-H + BE-I (Cycle-16-S10 Stage 3-4 RP fill per SI Amendment 2026-05-28a + 2026-05-28b; Done definition extended for fulfilling SI's research question structurally)

<!-- source: dispatch substrate §3.b Cycle-16-S10 RP fill scope — 4 BE-N blocks §5.7 BE-F + §5.8 BE-G + §5.9 BE-H + §5.10 BE-I -->
<!-- source: SI Amendment 2026-05-28a Done #11-#16 + Amendment 2026-05-28b Done #17-#19 verbatim — BE-F..BE-I new BE-class scope -->
<!-- source: HR §3.recovery.1 H_recovery_1..H_recovery_9 + §3.recovery.2 KT-7..KT-11 evidence schemata (this same S10 RP fill) -->
<!-- source: docs/LANDSCAPE_ASSESSMENT.md §6.recovery.A 10 probe-class disciplines × 30 verbatim quotes (S9 RP fill) -->
<!-- source: memory binding `feedback_operational_definition_substitution.md` detection — code-active probe-fire as acceptance evidence per Done #15d; smoke-only fires REFUSED -->
<!-- gate:experimental_design §5.recovery stage_5_recovery_acceptance required -->

**Discipline.** Per dispatch substrate §4 + Done #15d + memory binding `feedback_operational_definition_substitution.md`: each BE-N acceptance threshold below names a probe primitive class + specifies probe-fire-evidence aggregation against PRODUCTION specs (NOT smoke-only fires; NOT registry-field reads / status-enum equality / token-count / citation-density / artifact-exists-at-path / single-smoke-event). Smoke-only fires REFUSED at acceptance verdict per Done #15d. HC-11 partition declared per block. HC #72 substitution-detection self-scanned at every threshold draft before write; 0 substitution candidates retained.

**Acceptance verdict pattern.** Each BE-N requires PASS-all on 6 acceptance thresholds (mirrors §5.1-5.5 BE-A..BE-E `PASS-all (6 of 6)` precedent at BE close-evals). Coach R3 independently re-verifies at BE close-eval per kc-48+kc-49+kc-50 PD §3.3 T1-T13 mechanical tests.

**LOCKED-body discipline (Binding 7 + DP#42 strict).** §5.1-§5.6 LOCKED at S8 phase-checkpoint close per `fb3a0fe` + `25eff54` + `6c80afb`; §5.recovery is ADDITIVE-APPEND only. Verify via `git diff --stat` zero deletions on pre-marker line ranges.

### §5.7 BE-F Acceptance Criteria (Probe library 4 primitives Class A/B/C/D; closes Done #13 + H_recovery_3)

**Scope statement.** BE-F ships 4 probe primitives at `~/ml-governance-templates/scripts/probes/{a,b,c,d}/<primitive_id>.py` as canonical vocabulary (code, NOT markdown). Each primitive includes passing self-test against ≥1 known-good fixture + ≥1 known-bad fixture; library admission gate refuses primitives without passing self-test; version-lock at creation; modifications require Builder-ARCH paradigm dispatch (paradigm-class per kc-48 PD §5; HC #74 BINDING). Generic-emission escape primitives ABSENT (KT-9 firing on proposal).

**PASS-all (6 of 6) acceptance thresholds (each probe-fire-evidence grounded; smoke-only fires REFUSED per Done #15d):**

1. **Primitive count + class coverage.** `find ~/ml-governance-templates/scripts/probes/{a,b,c,d}/ -name "*.py" -type f -not -name "self_test_*"` returns ≥4 primitive files (one per Class A/B/C/D); each in correct subdirectory; admission script `~/ml-governance-templates/scripts/probe_library_admission.sh` exists with bash shebang + DP#44-compliant refuse-on-missing-precondition behavior.
2. **Self-test fixture pair per primitive.** `find ~/ml-governance-templates/scripts/probes/{a,b,c,d}/ -name "self_test_known_good_*.py" -o -name "self_test_known_bad_*.py"` returns ≥8 fixture files (≥1 known-good + ≥1 known-bad per primitive); fixtures structurally distinguished per LA §6.recovery.A row 3 mutation-testing killed-vs-survived discipline.
3. **Self-test execution emits PASS/FAIL JSONL event with predicateType discriminator.** For each primitive, `subprocess.run([sys.executable, primitive_path, "--self-test"])` exits 0 on known-good fixture AND exits 0 on known-bad fixture (i.e., primitive distinguishes both); execution emits `event_class: probe_library_self_test.pass.event` OR `.fail.event` to sink `outputs/probe_library_self_test_events.jsonl` with `predicateType: cycle16:probe_self_test_v1` (DISTINCT from production `cycle16:probe_fire_v1` per LA §6.recovery.A row 10 SLSA chain-of-custody discipline). Verify via JSONL tail showing 4 PASS events post-admission.
4. **Admission gate refuses primitives with failing self-test (≥3 negative-fixture refusals).** `probe_library_admission.sh` invoked against ≥3 deliberately-broken fixtures (e.g., primitive that passes on known-bad fixture by always returning success) returns non-zero exit code AND emits `event_class: probe_library_admission.refuse.event`. Verify via test-harness invocation against 3 broken fixtures all rejected.
5. **Production probe-fire on ≥1 spec per class (HC #72 anti-substitution; Done #15d).** Each of 4 primitives fires AT LEAST ONCE on a production cycle16:Spec (NOT smoke fixtures): `run_id` prefix `prod_*` (NOT `be_e_smoke_*` / `probe_lib_self_test_*`); per-class production-probe-fire JSONL row emitted with `predicateType: cycle16:probe_fire_v1` + `evidence_type: probe_fire_aggregate` field. Smoke-only fires explicitly REFUSED as acceptance evidence per Done #15d. Per-class verification: `grep "prod_" outputs/probe_library_events.jsonl | jq '.payload.primitive_class' | sort -u` returns 4 distinct class values {A, B, C, D}.
6. **Version-lock at creation; paradigm-class modification discipline.** Each primitive carries a version constant (e.g., `__primitive_version__ = "1.0"`) + lock_commit reference; modifications to primitive body require Builder-ARCH paradigm dispatch (HC #74 BINDING). Generic-emission escape primitives ABSENT at admission scan (KT-9 fires on proposal — paradigm escalation). Verify via design-review checklist at admission boundary.

**HC-11 partition.** Probe library = PUBLISHABLE (canonical vocabulary at ~/ml-governance-templates/ govML upstream; inherited by all freshly-scaffolded build-type projects). Self-test events = PUBLISHABLE. Production probe-fire events = PIPELINE-IP-PRIVATE (spec content from internal cycles).

**Close evidence file paths.** `~/ml-governance-templates/scripts/probes/{a,b,c,d}/<primitive_id>.py` (4 primitive files) + `~/ml-governance-templates/scripts/probes/{a,b,c,d}/self_test_known_{good,bad}_*.py` (≥8 fixtures) + `~/ml-governance-templates/scripts/probe_library_admission.sh` (admission script) + `outputs/probe_library_self_test_events.jsonl` (≥4 PASS events) + `outputs/probe_library_admission_events.jsonl` (≥3 refusal events) + `outputs/probe_library_events.jsonl` (production fires ≥4 events tagged `run_id: prod_*`) + DECISION_LOG entry `D-S{N}-{M}` at BE-F close.

**KT cross-binding.** KT-7 (self-test fail at admission → halt-and-surface for repair) + KT-9 (generic-emission escape primitive proposed → paradigm escalation per HC #74) + KT-10 (zero production fires on any class at FINDINGS → H_main_recovery REFUTED candidate).

### §5.8 BE-G Acceptance Criteria (Write-boundary enforcement + Done #17 cycle-close gate upgrade + Done #18 kill discipline + Done #19 ≤3-session dormancy preservation; closes Done #12 + #17 + #18 + #19 + H_recovery_2 + H_recovery_7 + H_recovery_8 + H_recovery_9)

**Scope statement.** BE-G ships 4-component composite: (i) write-boundary closure (pre-commit hook + fsnotify watcher + `forward_apply_emit()` wired into production `register_spec()` + 3-registry reconciliation gate at session close — closing HC-BE-D-1 per kc-47 audit refinement #2); (ii) Done #17 cycle-close BLOCKING gate predicate UPGRADED from registry-field SPARQL ASK to probe-fire-evidence aggregation invoking named probe primitive via Python subprocess; HARD-BLOCK on missing probe fire for any spec authored in-cycle; accepts `killed` (Done #18) OR `dormant-with-explicit-deferral` with Rex authorization + named target session + re-activation condition + maximum dormancy window (Done #15f); (iii) Done #18 `kill_spec(spec_iri, adr_retraction_ref, killing_session, kill_reason)` function with ADR retraction validation + `spec_killed_event` emit + SPARQL UPDATE state transition + audit trail recording; (iv) Done #19 ≤3-session dormancy threshold preservation on probe-fire evidence (NOT registry-field).

**PASS-all (6 of 6) acceptance thresholds (each probe-fire-evidence grounded; smoke-only fires REFUSED):**

1. **Pre-commit hook HARD-BLOCKs ≥3 synthetic-violation fixtures.** Pre-commit hook script at `~/ml-governance-templates/scripts/spec_authoring_pre_commit_hook.sh` (or equivalent canonical path) installed via `~/.git/hooks/pre-commit` symlink OR pre-commit framework config; invoked against ≥3 curated synthetic-violation fixtures (direct file edit of agent_spec.md without `register_spec()` in same commit + temp-path schema materialization + DECISION_LOG ADR entry without `register_spec()` call) returns non-zero exit code AND emits `event_class: pre_commit_hook_block.fire.event` to `outputs/spec_authoring_events.jsonl`. Verify via test-harness invocation across 3 fixtures all HARD-BLOCKed.
2. **fsnotify watcher emits `spec_authoring_event` within ≤60s on staged bypasses.** fsnotify-based watcher at `~/ml-governance-templates/scripts/spec_authoring_watcher.py` (or equivalent canonical path) monitoring spec-class paths emits `event_class: spec_authoring_event.fire.event` JSONL row within ≤60 seconds delivery latency on ≥3 staged-but-unregistered fixtures (per fsnotify v1.9.0 delivery semantics "When a file is removed a Remove event won't be emitted until all file descriptors are closed" — implementation accounts for write-then-close ordering). Verify via test-harness staging file + awaiting JSONL row arrival across 3 fixtures.
3. **3-registry reconciliation gate at session close detects zero drift across 5 consecutive sessions.** `~/ml-governance-templates/scripts/three_registry_reconciliation_gate.sh` at session-close hook reads (a) filesystem spec-class file inventory + (b) Fuseki `/cycle6` cycle16:Spec count via SPARQL SELECT + (c) `prompt_inventory` SQLite table; emits `event_class: three_registry_reconciliation.fire.event` with `drift_detected_bool: false` across 5 consecutive session closes. Verify via JSONL log scan post-5-session window.
4. **Done #17 cycle-close gate body UPGRADED: invokes probe primitive via subprocess (NOT SPARQL ASK on registry).** `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` body shows `python3 ~/ml-governance-templates/scripts/probes/<class>/<primitive>.py --aggregate-cycle <N>` invocation chain AND prior `SPARQL ASK { ?spec cycle16:currentStatus ?status }` invocation REMOVED or commented; gate emits `event_class: spec_implementation_present_gate.probe_fire_aggregate.fire.event` (NEW class) with payload `evidence_type: probe_fire_aggregate`. Verify (a) `grep -E 'subprocess\|python3.*probes' spec_implementation_present_gate.sh` returns match; (b) `grep -E '^[^#]*ASK \{.*currentStatus' spec_implementation_present_gate.sh` returns 0 active matches; (c) ≥3 negative-fixture test cases (cycle 16 spec-class fixture set with simulated missing probe fires) all HARD-BLOCK; (d) positive fixture (complete probe fires + 1 spec in `killed` state per Done #18 + 1 spec in `dormant-with-explicit-deferral` state with all 4 required fields per Done #15f) passes.
5. **Done #18 `kill_spec()` function shipped with ADR validation + emit + SPARQL UPDATE + DP#44 refusal.** `scripts/spec_registry_authoring.py` contains `def kill_spec(spec_iri, adr_retraction_ref, killing_session, kill_reason):` — verify via `python3 -c "from scripts.spec_registry_authoring import kill_spec; import inspect; sig = inspect.signature(kill_spec); assert len(sig.parameters) == 4"`. Function body executes (a) `subprocess.run(["grep", "-E", f"^## ADR-{adr_retraction_ref}", "docs/DECISION_LOG.md"]).returncode == 0` ADR validation; (b) emits `event_class: spec_killed_event.fire.event` JSONL row to `outputs/spec_registry_events.jsonl`; (c) executes SPARQL UPDATE setting `cycle16:currentStatus` → `cycle16:killed` AND `cycle16:auditTrailLink` to ADR reference (verify via SPARQL SELECT post-call); (d) raises `ValueError` on ≥3 negative-fixture tests (missing ADR + malformed spec_iri + None args) per DP#44 BINDING + emits NO event on refusal. ≥3 negative-fixture refusals + ≥1 positive-fixture pass verified.
6. **Done #19 ≤3-session dormancy threshold preserved on probe-fire evidence.** `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` body shows aggregation step against probe-fire JSONL log across last 3 sessions (NOT SPARQL ASK on `cycle16:currentStatus`); emits `event_class: spec_implementation_session_close_gate.probe_fire_aggregate.fire.event` with `evidence_type: probe_fire_aggregate` field; `current_session_index` advances correctly per session-close (verified via 5-session trace shows monotonic increment); ≥3 dormancy-firing test cases verified (negative fixture: 3 specs across ≥2 classes with simulated dormant probe-fire history → gate flags all 3; positive fixture: 3 specs with recent production probe fires → gate flags 0); `advisory_mode_bool: true` preserved at Cycle 16 (BLOCKING transition at Cycle 17+ per kc-44 Amendment 2026-05-27a).

**HC-11 partition.** Pre-commit hook + watcher + reconciliation gate + upgraded gate body + `kill_spec()` function = PUBLISHABLE (govML upstream substrate). Spec-class file contents inspected by hook = PIPELINE-IP-PRIVATE (per-cycle spec content). Three-registry reconciliation event payloads = PIPELINE-IP-PRIVATE.

**Close evidence file paths.** `~/ml-governance-templates/scripts/spec_authoring_pre_commit_hook.sh` + `~/ml-governance-templates/scripts/spec_authoring_watcher.py` + `~/ml-governance-templates/scripts/three_registry_reconciliation_gate.sh` + `~/ml-governance-templates/scripts/spec_implementation_present_gate.sh` (UPGRADED) + `~/ml-governance-templates/scripts/spec_implementation_session_close_gate.sh` (UPGRADED on Done #19 surface) + `scripts/spec_registry_authoring.py` (with `kill_spec()` function ADDITIVELY appended) + `outputs/spec_authoring_events.jsonl` (≥3 hook-block + ≥3 watcher events) + `outputs/three_registry_reconciliation_events.jsonl` (≥5 reconciliation events) + `outputs/spec_implementation_gates_events.jsonl` (≥3 cycle-close negative-fixture HARD-BLOCK + ≥3 session-close dormancy-firing events) + `outputs/spec_registry_events.jsonl` (≥1 `spec_killed_event` + ≥3 refusal records) + DECISION_LOG entry `D-S{N}-{M}` at BE-G close.

**KT cross-binding.** KT-7 (probe primitives invoked by gate body must pass self-test) + KT-8 (gate body / hook predicate / kill_spec validation must IMPORT and EXECUTE the named primitive, NOT string-match — applies broadly across all 6 thresholds).

### §5.9 BE-H Acceptance Criteria (Structural-prevention layer 7 components; closes Done #15a-g + H_recovery_5)

**Scope statement.** BE-H ships structural-prevention layer as 7 distinct runnable mechanisms at `~/ml-governance-templates/scripts/structural_prevention/`: (a) Stage 0 probe-presence check; (b) reality-vs-intent gate forward to Stage 1+4 R3 close-evals; (c) number-tagging gate at Rex-facing surfaces; (d) probe-coverage check at FINDINGS close; (e) probe library self-test at session close with 2-consecutive-fail auto-deprecate; (f) deferral expiration enforcement; (g) design-anchor disclosure at LANDSCAPE close. Each piece fires mechanically at its declared surface with ≥1 negative-fixture refusal; each integrates into govML `init_project.sh` install path. Per LA §6.recovery.C row 8 design-anchor: composition pattern (gate-script-per-piece + invoke from `check_all_gates.sh`) PARTIALLY inherits from Cycle 14 four-gate skeleton (substrate-layer per §6.X.2 refined-metric Rex disposition (C)); individual piece predicates externally grounded per LA §6.recovery.A.

**PASS-all (6 of 6) acceptance thresholds (each probe-fire-evidence grounded; smoke-only fires REFUSED):**

1. **All 7 pieces present at canonical path as runnable mechanisms.** `find ~/ml-governance-templates/scripts/structural_prevention/ -type f -name "*.sh" -o -name "*.py"` returns ≥7 runnable scripts; each with shebang + DP#44-compliant refuse-on-missing-precondition behavior; each emits to dedicated JSONL sink at `outputs/structural_prevention_<piece>_events.jsonl`.
2. **Each piece refuses on ≥1 negative fixture (mechanical halt-and-surface).** Test harness invokes each of 7 pieces against ≥1 negative fixture: (a) Stage 0 probe-presence script exits non-zero on negative-fixture (probe primitives absent in project tree); (b) reality-vs-intent gate refuses close when mandatory structured table absent or incomplete (remove 1 row from known-good RQS §3.recovery.1 fixture → gate fails); (c) number-tagging gate refuses close when ≥1 primary number lacks `[measured]` / `[heuristic]` / `[anecdotal]` tag AND BLOCKS if `[heuristic]`-tagged number appears in Done-criterion verdict (verified via 2 fixtures: missing tag + heuristic in verdict); (d) probe-coverage check refuses close when per-class production-probe-fire count = 0 for any class (smoke fires explicitly rejected via `run_id` prefix discriminator); (e) library self-test gate auto-deprecates primitive after 2 consecutive session failures (verified via deliberately broken primitive across 2 session-close fires); (f) deferral expiration gate refuses close when deferred spec lacks named target session OR reason OR re-activation condition OR maximum dormancy window (4 negative fixtures covering each missing field); (g) design-anchor disclosure gate refuses close when LANDSCAPE close artifact lacks load-bearing-mechanism design-anchor disclosure column. Each negative-fixture refusal verified via JSONL `*.refuse.event` row.
3. **Probe-coverage check (d) requires non-zero PRODUCTION fires per class (Done #15d strict).** `~/ml-governance-templates/scripts/structural_prevention/probe_coverage_check.sh` predicate: `for class in A B C D; do production_count=$(grep -c "prod_" outputs/probes/<class>/*.jsonl); [ "$production_count" -gt 0 ] || exit 1; done`. Smoke fires identified via `run_id` prefix `be_e_smoke_*` / `probe_lib_self_test_*` and NOT counted toward production count. Verify via JSONL run_id-prefix discriminator + per-class aggregation against ≥4 production fixtures.
4. **Library self-test gate (e) auto-deprecates after 2 consecutive fails.** Test scenario: deliberately break a known-good primitive at session N; observe `event_class: probe_library_self_test.fail.event` at session N+1 close; observe `event_class: probe_library_self_test.fail.event` AGAIN at session N+2 close; observe `event_class: probe_library_auto_deprecate.fire.event` at session N+2 close emitting `consecutive_failure_count: 2`; observe session N+3 close HARD-BLOCK until repair via Builder-ARCH dispatch OR removal via paradigm disposition. JSONL log trace across 3-session window verified.
5. **govML `init_project.sh` integration path declared.** `~/ml-governance-templates/scripts/init_project.sh` contains `install_structural_prevention_layer()` ADDITIVE-APPEND function call (verified mechanically via `grep -E '^install_structural_prevention_layer\(\)' init_project.sh` + call-site in install_project() body); freshly-scaffolded build-type project at `scaffold_research_project.py --research-type build --profile research-build --dest /tmp/test_scaffold` materializes all 7 structural-prevention pieces under `/tmp/test_scaffold/scripts/structural_prevention/` (verified via `find` returning ≥7 files).
6. **Composition-pattern design-anchor disclosed at acceptance close.** Per LA §6.recovery.C row 8 + Binding 2 design-anchor enforcement: BE-H close evidence file explicitly states composition pattern PARTIALLY inherits from Cycle 14 four-gate skeleton (substrate-layer per §6.X.2 refined-metric); individual piece predicates externally grounded per LA §6.recovery.A discipline mapping (a)←row 1+2+9; (b)←row 3; (c)←row 10 chain-of-custody for number provenance; (d)←row 8 production-vs-smoke discriminator; (e)←row 3 mutation-testing auto-deprecate; (f)←row 5+6 admission control + dependency tracking; (g)←row 9 BX drift-detection. Design-anchor disclosure JSONL row emitted at BE-H close.

**HC-11 partition.** Structural-prevention scripts + JSONL sinks (gate-fire events) + composition-pattern design-anchor disclosure = PUBLISHABLE (govML upstream). Per-cycle production probe-fire content inspected = PIPELINE-IP-PRIVATE (cycle 16 spec inventory).

**Close evidence file paths.** `~/ml-governance-templates/scripts/structural_prevention/{stage_0_probe_presence_check.sh, reality_vs_intent_gate.py, number_tagging_gate.py, probe_coverage_check.sh, library_self_test_gate.sh, deferral_expiration_gate.py, design_anchor_disclosure_gate.py}` (7 pieces) + `outputs/structural_prevention_<piece>_events.jsonl` (7 sinks; ≥1 refusal event per piece + ≥1 PASS event per piece) + `outputs/probe_library_auto_deprecate_events.jsonl` (≥1 deprecation event) + DECISION_LOG entry `D-S{N}-{M}` at BE-H close.

**KT cross-binding.** KT-7 + KT-8 + KT-10 collectively cross-bind (any piece shipping with self-test failure / string-match substitution / zero production coverage fires the relevant KT).

### §5.10 BE-I Acceptance Criteria (govML v2.8.6 ADDITIVE-APPEND chain n=5→6 back-port; closes Done #16 + H_recovery_6)

**Scope statement.** BE-I back-ports probe library + Operational-Definition Substitution Gate + structural-prevention 7-piece layer into govML at scripts/init_project.sh as 3 NEW install functions: `install_probe_library_canonical_vocabulary()` + `install_operational_definition_substitution_gate()` + `install_structural_prevention_layer()`; templates/build/probes/ NEW directory + templates/build/structural_prevention/ NEW directory; VERSION v2.8.5 → v2.8.6; CHANGELOG.md v2.8.6 entry. Freshly-scaffolded build-type projects inherit at scaffolding time. **LOCKED bodies of prior install functions UNMODIFIED** (v2.8.2 `install_runtime_emit_substrate` + v2.8.3 `install_spec_registry_authoring_discipline` + v2.8.4 `install_spec_implementation_gates` + v2.8.5 `install_forward_apply_observation`) per HC #45 ADDITIVE-APPEND precedent class strict. Cross-system 4-repo paired commit expected (cycle_16 + EMABS + Moonshots + govML) per HC #45 chain extension precedent.

**PASS-all (6 of 6) acceptance thresholds (each probe-fire-evidence grounded; smoke-only fires REFUSED):**

1. **VERSION transition + CHANGELOG entry.** `~/ml-governance-templates/VERSION` reads `v2.8.6`; `~/ml-governance-templates/CHANGELOG.md` contains `v2.8.6` entry with timestamp + ADDITIVE-APPEND chain extension annotation (n=5→6) + ship-commit SHA + Done #16 closure reference. Mechanical: `grep -E '^v2\.8\.6' CHANGELOG.md` returns match; `cat VERSION` returns `v2.8.6`.
2. **3 NEW install functions ADDITIVELY APPENDED to init_project.sh.** `grep -cE '^install_(probe_library_canonical_vocabulary|operational_definition_substitution_gate|structural_prevention_layer)\(\)' ~/ml-governance-templates/scripts/init_project.sh` returns 3 (function definitions) AND `grep -cE '^[[:space:]]+install_(probe_library_canonical_vocabulary|operational_definition_substitution_gate|structural_prevention_layer)$' init_project.sh` returns 3 (call-sites in install_project() body). Functions defined AND invoked.
3. **LOCKED bodies of prior install functions UNMODIFIED (KT-11 strict; HC #45 precedent class).** `git diff <v2.8.5_lock_commit>..HEAD -- ~/ml-governance-templates/scripts/init_project.sh` filtered to prior install_function line ranges (v2.8.2 + v2.8.3 + v2.8.4 + v2.8.5 install function bodies) returns **0 modification lines**. Mechanical verification via line-range bracketed diff: for each prior install function, line-range diff returns "0 changes." KT-11 fires immediately on any non-zero modification line count (halt for re-do).
4. **templates/build/probes/ + templates/build/structural_prevention/ NEW directories materialized.** `ls ~/ml-governance-templates/templates/build/probes/` returns non-empty (≥4 primitive templates a/+b/+c/+d/); `ls ~/ml-governance-templates/templates/build/structural_prevention/` returns non-empty (≥7 piece templates matching BE-H surface). Template files contain placeholder substitution markers per govML scaffolding convention (NOT hardcoded paths).
5. **Freshly-scaffolded project inherits v2.8.6 components (smoke test on real scaffold).** Run `scaffold_research_project.py --research-type build --profile research-build --dest /tmp/test_scaffold_v286` against the v2.8.6 govML state; verify (a) `/tmp/test_scaffold_v286/scripts/probes/` exists with ≥4 primitive files; (b) `/tmp/test_scaffold_v286/scripts/structural_prevention/` exists with ≥7 piece files; (c) `/tmp/test_scaffold_v286/VERSION` includes v2.8.6 reference; (d) `find /tmp/test_scaffold_v286 -name "*.py" -o -name "*.sh"` returns counts consistent with v2.8.6 manifest. Smoke test against fresh tmpfs scaffold; NOT against running cycle 16 project (Coach handles cycle 16 inheritance separately).
6. **4-repo paired commit + push verify per HC #45 chain extension precedent.** Cross-system paired commit lands cycle_16 (this project) + EMABS wrapper (paired Moonshots-wrapper update) + Moonshots (handoff / coach_warmup updates) + govML (v2.8.6 chain extension); each repo's commit SHA referenced in BE-I close evidence; `git log --oneline -1 ~/ml-governance-templates/` shows v2.8.6 commit; cross-repo paired-commit ledger emitted at `outputs/cross_system_paired_commit_v2_8_6.json` (govML SHA + cycle_16 SHA + EMABS SHA + Moonshots SHA + timestamp). Coach handles 3-repo Moonshots+EMABS+cycle_16 paired commit; Builder-ARCH dispatches the 4th-repo govML back-port commit per HC #45 precedent.

**HC-11 partition.** VERSION + CHANGELOG + init_project.sh (all 3 new install functions + LOCKED bodies UNMODIFIED) + templates/build/probes/ + templates/build/structural_prevention/ = PUBLISHABLE (govML upstream). Smoke-test scaffold artifacts = EPHEMERAL (test-bed only). 4-repo paired commit ledger = PUBLISHABLE.

**Close evidence file paths.** `~/ml-governance-templates/VERSION` (v2.8.6) + `~/ml-governance-templates/CHANGELOG.md` (v2.8.6 entry) + `~/ml-governance-templates/scripts/init_project.sh` (3 new install functions ADDITIVELY APPENDED + 3 call-sites in install_project() body; prior install function bodies UNMODIFIED) + `~/ml-governance-templates/templates/build/probes/` directory + `~/ml-governance-templates/templates/build/structural_prevention/` directory + `outputs/cross_system_paired_commit_v2_8_6.json` (4-repo paired-commit ledger) + `/tmp/test_scaffold_v286/` (smoke-test scaffold; ephemeral) + DECISION_LOG entry `D-S{N}-{M}` at BE-I close + 4-repo paired-commit SHA references (cycle_16 + EMABS + Moonshots + govML).

**KT cross-binding.** KT-11 BINDING strict (LOCKED-body modification halts for re-do per HC #45 precedent class). Pattern 19 STANDING density-class discipline applies (cross-system back-port density profile).

### §5.recovery aggregate ledger forward

| BE | Closing Done# | Closing H_recovery | KT cross-binding | HC-11 partition | Expected Cycle 16 session |
|---|---|---|---|---|---|
| BE-F | #13 | H_recovery_3 | KT-7 + KT-9 + KT-10 | Library = PUBLISHABLE; production fires = PIPELINE-IP-PRIVATE | Cycle-16-S11+ Stage 5 |
| BE-G | #12 + #17 + #18 + #19 | H_recovery_2 + H_recovery_7 + H_recovery_8 + H_recovery_9 | KT-7 + KT-8 | Hook/watcher/gates/kill_spec = PUBLISHABLE; spec content = PIPELINE-IP-PRIVATE | Cycle-16-S12+ Stage 5 (1-2 sessions; composite) |
| BE-H | #15a-g | H_recovery_5 | KT-7 + KT-8 + KT-10 | 7 pieces + sinks = PUBLISHABLE; production-fire payloads = PIPELINE-IP-PRIVATE | Cycle-16-S13+ Stage 5 |
| BE-I | #16 | H_recovery_6 | KT-11 strict | govML chain = PUBLISHABLE; 4-repo paired commit ledger = PUBLISHABLE | Cycle-16-S14+ Stage 5 (4-repo paired commit) |

**Aggregate decision rule for §5.recovery.** Each BE-N requires PASS-all on 6 thresholds at Coach R3 close-eval per kc-49/50/51 PD §3.3 T1-T13 mechanical tests. 0 of 5 KT-7..KT-11 fires across BE-F..BE-I closes is the success condition for Cycle 16 TRUE close-arc. KT-10 firing at any BE close = H_main_recovery REFUTED candidate → paradigm escalation per HC #74. Smoke-only fires as acceptance evidence REFUSED per Done #15d strict. Done #11 (probe-grounded measurement replaces heuristic 137) closes at Phase 10 retroactive scan re-run (per ROADMAP §10 below) after BE-F probe library admission completes.

<!-- /gate:experimental_design §5.recovery stage_5_recovery_acceptance -->

<!-- amendment_2026_05_28a_extension_end -->

> Per `feedback_honest_evaluation.md` BINDING: Build-Runner self-report NOT load-bearing; Coach R3 independent verification at every BE-F..BE-I close per kc-49+50+51 PD §3.3 T1-T13 mechanical tests is the authoritative verdict. Each BE-N close-eval reproduces the §5.1-§5.6 BE-A..BE-E pattern (PASS-all 6/6 thresholds; HC #50 zero-Rex-escalation baseline preservation; HC #72 substitution-detection self-scan at every threshold draft).
