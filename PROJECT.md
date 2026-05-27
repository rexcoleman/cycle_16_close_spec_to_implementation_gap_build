# Project: Cycle 16 — Close the spec-to-implementation gap

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- stage: 3 -->
<!-- source: Cycle 16 SI ACTIVE 2026-05-27 (Moonshots a2f14d5) + Amendment 2026-05-27a (be54a97) + Amendment 2026-05-27b (badd749; KG-primary registry storage) -->

## Wrapper Program Context

This cycle is one build-class research cycle within the `engineering_methodology_for_agent_built_systems` wrapper program (EMABS). The wrapper program is the longer-arc paradigm investigation under which Cycles 13-15 attacked rubric-refinement (downstream symptom) and Rex 2026-05-27 pivoted the program at mid-Cycle-15-S7 to close the upstream gap that the wrapper was created to address but had not structurally engaged. Cycle 16 is the initial cycle to engage that upstream gap with a structural mechanism rather than discipline binding alone.

## Research Question (verbatim from Cycle 16 SI L11 + Amendment 2026-05-27a)

How do we structurally guarantee that every spec our pipeline writes — agent contracts, schemas, design decisions, methodology commitments — becomes implemented running code by the close of the authoring cycle (default), or gets explicitly deferred to a named target session with audit trail (exception requiring authorization for deferral past the authoring cycle close), or gets explicitly killed with audit trail — with structural detection of dormancy within ≤3 sessions of authoring via the runtime emit mechanism, and no silent drift?

## Scope

- **In scope:** 4 branches per Cycle 16 SI L15-L72: (1) retroactive Cycle 1-15 spec inventory across 4 spec-classes + per-class operational definition + 5-state taxonomy classification; (2) substrate audit (RIDE + research_depth_enforcement_automation + Cycle 14 four-gate + Cycle 6 unified KG per Amendment 2026-05-27b) for ≥80% mechanism scope (KT-1 disposition surface); (3) external grounding from 7 disciplines (IETF / Python PEP / OpenAPI / Design by Contract / feature-flag governance / ADR / Parnas) per LA §1 LOCKED; (4) build per-spec KG-primary registry at Fuseki `/cycle6` endpoint with 14-field schema (per kc-44 corrected count) + per-edge HC-11 access-permission enum + PROV-O 4 typed-edges + Wikidata supersedure pattern + nanopublication 3-graph triplet + spec-authoring-time discipline + TWO-surface BLOCKING gate at cycle-close + session-close + retroactive scan + forward-apply observation across Cycles 17-18.
- **Out of scope** (per Cycle 16 SI L91-L98 + disposed paradigm question #1): (a) new rubric dimensions beyond Cycle 13's five — Cycle 13 LOCKED; (b) modification of Cycle 13/14/15 LOCKED bodies — preserved per Binding 7; (c) the deferred rubric-refinement scope from Cycle 15 Items 5-10 — moved to Cycles 17-18 per kc-44 Amendment 2026-05-27a renumbering; (d) full paradigm-class reversal of spec-vs-code duality (RQS §4.1 Alternative 2) — reserved as KT-5 paradigm escalation surface if Cycle 16 structural mechanism fails; (e) ≤6 sessions per disposed paradigm question #1 envelope.
- **Kill conditions:** KT-1 fires (substrate coverage ≥80% per LA §6 addendum) → Cycle 16 narrows to gap-filling + retroactive inventory only. KT-2 fires (<3 dormant-silent specs at retroactive scan) → halt + Rex paradigm re-disposition. KT-6 fires (substantive Cycle 6 KG substrate-viability blocker) → fall back to SQL/YAML per pre-Amendment-27b binary framing + escalate per Step 3.5 gate. KT-5 fires (≥2 NEW dormant-silent specs mid-cycle OR cross-cycle) → H_main REFUTED + paradigm escalation candidate.

## Success Criteria (per Cycle 16 SI L75-L88 done-criteria #1-#10)

1. **Spec inventory complete:** every spec across Cycles 1-15 enumerated at retroactive scan close, classified per 5-state taxonomy, owner-attributed.
2. **Pattern analysis:** Cycle 10 case study counterfactual analysis (H4) + 4-spec-class per-type operational definitions (H2) authored.
3. **Substrate audit:** LA §6 addendum encodes Cycle 6 KG inheritance evidence + KT-1 disposition recommendation + KT-6 disposition recommendation; Coach independent verification at R3.
4. **External research:** 7 disciplines × ≥3 verbatim quotes each LOCKED at LA §1 (36 quotes total; HC #43 ≥30 floor exceeded per S1 close).
5. **KG-primary 14-field registry:** schema authored + materialized at Fuseki `/cycle6` endpoint as nanopublication 3-graph triplet per Cycle 6 BE#1 contract.
6. **SPARQL UPDATE authoring discipline:** spec-authoring-time gate body forces complete registry row + target_session + runtime_emit_event_class (or documented `n/a` per DP#26 carve-out for methodology commitments).
7. **TWO-surface BLOCKING gate:** `scripts/spec_implementation_present_gate.sh` at cycle-close + session-close fires SPARQL ASK against `/cycle6`; predicate body extends Cycle 14 four-gate skeleton via SPARQL UPDATE substitution.
8. **Retroactive scan fires:** one-time fire against Cycles 1-15 inventory at Cycle 16 mid-cycle; ≥3 dormant-silent specs surfaced (else KT-2 fires).
9. **Forward apply:** infrastructure observation across Cycles 17-18 begins (≥2 subsequent cycles required for #10 longitudinal verdict).
10. **5-layer FINDINGS + paired commit:** Layer 1 (artifacts), Layer 2 (mechanism), Layer 3 (cell granularity per HR §3a EXTENSION-3), Layer 4 (hypothesis resolutions + Cycle 10 counterfactual), Layer 5 (honest gaps + KT firings + forward-cycle carries).

## Forbidden Proxies

- High word count does not count as thoroughness.
- Many citations does not count as cross-discipline composition (per LA §1 7-discipline grounding LOCKED — composition not citation count is the load-bearing surface).
- Internal consistency does not count as correctness (per Cycle 6 KG mechanism-class inheritance: empirical Coach probe is load-bearing; not internal claim).
- LLM self-assessment does not count as validation — Coach independent verification at R3 mechanical tests T1-T13 per kc-44 §3.3.
- "Mechanism shipped" does not count as "mechanism works" — KT-N empirical firing surface at FINDINGS Layer 4 + longitudinal forward-apply across Cycles 17-18 is the operational test.

## Gap Analysis

Per LA §2 Gap Map + §6b Handoff: 5 gaps span mixed types (3 method-innovation + 2 feasibility-demonstration + 1 domain-transfer). No per-spec registry exists at AI-agent-built-systems-engineering-methodology grain across the 7 external disciplines surveyed; sub-cycle (session-grain) TWO-surface BLOCKING gate has not been attempted in any source domain; retroactive scan mechanism cannot fire absent per-spec registry; spec-authoring-time discipline at registry-row-required boundary is operationally compatible at LaunchDarkly enterprise scale but untested at AI-agent-engineering-methodology cadence. Gap was confirmed by searching 7 external disciplines (LA §1 LOCKED 36 verbatim quotes) + 4 internal substrates (LA §6b.2 + Cycle 6 KG addendum) + 3 cross-engine DB views (7,560 + 126 + 3,128 rows; no spec-implementation-gap entry).

## Significance

If the mechanism works (H1-H8 collectively CONFIRMED + KT-1..KT-6 do not fire negatively + ≥2-cycle forward-apply with 0 NEW dormant-silent specs), the wrapper-program EMABS gains its structural answer to the documentation-active-vs-code-active gap framed at AAEM cycle 1 closure. Downstream practitioner impact: the per-spec KG registry schema (14 fields) becomes a candidate cross-disciplinary benchmark schema for spec-implementation governance in AI-agent-built systems, composed from 7 field-mature discipline sources but unified at an application surface (AI-agent-engineering-methodology) where it has not been composed before. If the mechanism is REFUTED (KT-5 fires), the paradigm-class question reservoir (RQS §4.1 Alternative 2: specs ARE code, no spec/code separation) becomes the candidate forward-cycle escalation surface.

## Prior Work Engaged (minimum 3; full 7-discipline grounding at LA §1)

1. **LaunchDarkly + GrowthBook + Optimizely commercial feature-flag governance** (LA §1 row 5; 8 verbatim quotes): per-flag lifecycle states (Live / Ready for code removal / Ready to archive / Archived / Deprecated) + automated stale-flag detection at temporal thresholds (LaunchDarkly: 30d-created + 7d-inactive; GrowthBook: 14d-unchanged + uniform-value-serve; Optimizely: 30d-no-modify + no-traffic) + Code References scanning auto-linking flag-key → file:line + commercial deployment at >1000 enterprise customers. **Relevance:** PRIMARY adjacent-field import — Cycle 16 5-state taxonomy directly mirrors LaunchDarkly's lifecycle vocabulary; ≤3-session dormancy threshold is the session-cadence-scaled analog of LaunchDarkly's 30d/7d heuristic.
2. **IETF RFC 6982/7942 Implementation Status Section + Python PEP 1 PEP-Delegate** (LA §1 rows 1+2; 4+3 verbatim quotes): per-spec implementation-status field carried as canonical-class field through standards-development lifecycle; "running code" philosophy (Clark 1992); reviewers "assign due consideration to documents that have the benefit of running code." **Relevance:** SECONDARY import providing the social-process anchor (PEP-Delegate) and the cultural framing (running code = implementation evidence) that Cycle 16 mechanizes via SPARQL ASK against `/cycle6` endpoint at gate-fire time.
3. **Cycle 14 four-gate methodology** (LA §6b.2 row 3; lock_commit `efaf6ae6` captured at Cycle-16-S1 scaffold per `governance.yaml`): template-class structural-gate predicate body `artifact_exists($spec) ∧ placeholder_count($spec) == 0 ∧ H_disconfirmation_subsection_count($spec) ≥ 1`; gate-script skeleton + `check_all_gates.sh` invocation + profile-build conditional firing + BLOCKING mode default. **Relevance:** TEMPLATE inheritance — Cycle 16 extends predicate body via SPARQL UPDATE substitution targeting Fuseki `/cycle6` endpoint per Cycle 6 BE#1 contract; same gate-script skeleton; H6 hypothesis explicitly tests "clean extension" vs "new primitive class warranted" (KT-4 firing surface).

## Cycle 6 KG Substrate Inheritance (per Amendment 2026-05-27b)

Apache Jena Fuseki PID 479112 RUNNING since 2026-05-14; TDB store at `runtime/jena/tdb/`; config `runtime/jena/run/cycle6.ttl`. Coach-probed at S2 entry 2026-05-27: **246,048 quads / 46 named graphs.** Top: be4:signals:assertion=93,297; be4:claims:assertion=40,810; be4:signals:publicationInfo=20,976; be4:signals:provenance=15,733; be4:claims:provenance=11,901; be2:assertion=8,543; be3:pipeline_experiments_ranking_events:assertion=6,201; cycle6:ontology=181. SPARQL latency: COUNT(*)=0.139s; per-graph aggregate=0.495s; predicate enum=0.082s; HC-11 access-permission enum=0.066s (all ≤5s threshold by 10-256× margin). PROV-O 4 typed-edges operational. HC-11 access-permission enum operational (11,223 ip-private + 1 publishable + 1 ephemeral usages). Nanopublication 3-graph pattern operational across 46 named graphs. Wikidata supersedure PARTIAL: only `cycle6:rankingRationale` predicate; `wikibase:rank` + `prov:wasRevisionOf` absent — HC-RP-S2-3 honest gap (ED §4a constraint #4 binds Stage 5 BE#1 schema extension OR detect at close).

## 4-Branch Decomposition (per Cycle 16 SI L15-L72)

- **Branch 1 — Retroactive enumeration:** 1.1 spec inventory across Cycles 1-15 (4 spec-classes) → 1.2 per-class operational "implemented" definition → 1.3 5-state taxonomy classification → 1.4 dormant-silent identification → 1.5 Cycle 10 case study counterfactual analysis (H1-H4 binding).
- **Branch 2 — Substrate audit:** 2.1 RIDE F-D Hybrid composition coverage → 2.2 research_depth_enforcement_automation primitive class coverage → 2.3 Cycle 14 four-gate predicate-extension assessment (H6 + KT-4) → 2.4 Cycle 6 unified KG inheritance per Amendment 2026-05-27b (H5 + KT-1 + KT-6 binding; LA §6 addendum surface).
- **Branch 3 — External grounding:** 7 disciplines × ≥3 verbatim quotes each LOCKED at LA §1 + LA §1.2 cross-discipline convergence matrix + LA §1b adjacent field survey (3 ranked imports for ED §9a External Validation).
- **Branch 4 — Mechanism build:** 4.1 KG-primary 14-field schema (per kc-44 corrected count; per Cycle 6 BE#1 contract with PROV-O 4 typed-edges + per-edge HC-11 enum + Wikidata supersedure + nanopublication 3-graph triplet) → 4.2 spec-authoring-time SPARQL UPDATE discipline (H7 + KT-3) → 4.3 TWO-surface BLOCKING gate (cycle-close + session-close + ≤3-session dormancy threshold per Amendment 2026-05-27a) → 4.4 retroactive scan one-time fire mid-cycle (H3 + KT-2) → 4.5 forward-apply observation across Cycles 17-18 (H8 + KT-5).

## KT-1..KT-6 Pre-Registration Summary (per HR §3 + ED §Field 6 + LA §6 addendum)

- **KT-1** (substrate ≥80%) — DISPOSITION at LA §6 addendum + Coach R3 verification; DOES NOT FIRE recommendation per ≈70% pre-27b coverage; may shift to ≈90-95% with Cycle 6 KG inheritance — RP reassesses at addendum.
- **KT-2** (<3 dormant-silent at retroactive scan) — halt + Rex paradigm re-disposition.
- **KT-3** (n=3+ author refusals mid-cycle) — registry refinement OR same-cycle default relaxation.
- **KT-4** (predicate extension requires new primitive class) — new enforcement primitive class warranted.
- **KT-5** (≥2 NEW dormant-silent specs mid-cycle OR Cycles 17-18) — H_main REFUTED; paradigm escalation candidate.
- **KT-6 NEW** (Cycle 6 KG substrate-viability blocker per Amendment 2026-05-27b) — fall back to SQL/YAML per pre-27b binary framing + escalate via Step 3.5 gate. Coach pre-disposed DOES NOT FIRE per 2026-05-27 probe; RP independently verifies + reports.

## Pipeline-Internal Status

Build-class research cycle (per `governance.yaml`: profile=research-build; research_type=build). Stages 0-2 LOCKED at Cycle-16-S1 close (`9300c86`); Stage 3-4 RP fill in progress at this S2. Stage 5 = BE-class sessions (Cycle 14 multi-BE precedent: 4-5 BE-A..BE-E covering schema/SPARQL write-boundary + authoring discipline + TWO-surface gate + retroactive scan + forward-apply). Cycle close = 10/10 done-criteria OR KT-1..KT-6 disposition with FINDINGS Layer 4-5 honest carry.
