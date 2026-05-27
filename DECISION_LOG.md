# Decision Log

> Append-only record of key decisions. quality_loop.sh appends scoring results here.
> See `~/ml-governance-templates/templates/management/DECISION_LOG.tmpl.md` for template.

## D-S2-1 — KT-1 paradigm-ruling disposition (C) metric-revision-within-intent (Rex 2026-05-27)

**Decision.** KT-1 (substrate audit ≥80% mechanism scope coverage → narrow Cycle 16) DOES NOT FIRE under refined operational metric per Rex paradigm-ruling 2026-05-27 disposition (C). Refined metric: "≥80% of MECHANISM-LAYER scope, excluding pure substrate-layer inheritance (storage primitives + access-permission enum + provenance edges + endpoint substrate)." Net mechanism-layer coverage post-refinement ~75-85% — marginal at literal ≥80% reading; firmly DOES NOT FIRE under intent reading. **Cycle 16 proceeds with full SI scope (Branches 1-4 all in-scope).**

**Authority chain.** Rex 2026-05-27 paradigm-ruling disposition (C) per foundational threshold-metric pre-registration discipline §10 (i)+(ii) > Amendment 2026-05-27b (`badd749`) structurally encoded substrate-vs-mechanism distinction (Cycle 6 KG inherits STORAGE substrate; Cycle 16 authors SPEC-IMPLEMENTATION MECHANISM) > Cycle 16 SI ACTIVE 2026-05-27 + Amendments 27a + 27b LOCKED > Binding 7 + S155 (KT-trigger paradigm escalation discipline).

**Context.** S2 RP raw initial estimate ~90-95% aggregate coverage post-Amendment-27b + Cycle 6 KG inheritance under unrefined "any inheritance" metric. RP surfaced literal-vs-intent ambiguity (substrate-layer inheritance vs mechanism-layer redundancy) at LA §6.X.2 + ED §17. Coach R3 3-test pre-escalation gate (end-state convergence + gotcha #16 + S176) returned 3/3 PARADIGM; escalated to Rex via Pattern 14 executive format.

**Rex ruling rationale.** Per `feedback_protocol_supersedes_pre_registered_surface.md` + foundational threshold-metric pre-registration discipline §10 (i)+(ii): Amendment 2026-05-27b already encoded the substrate-vs-mechanism distinction structurally; KT-1 literal-vs-intent ambiguity resolves operationally by refining operational metric to measure intent faithfully — substrate availability ≠ mechanism redundancy. Coach R3 paradigm escalation was operationally-disposable; this is not a paradigm question. Refine metric structurally at ED §Field 6 + LA §6.X.1; proceed with full SI scope.

**Encoded surfaces (operationalization).**
- ED §Field 6 KT-1 row: refined threshold language + DOES NOT FIRE disposition (locked).
- ED §17.3 + §17.5: refined coverage recalculation + Coach-R3-paradigm-escalation-to-Rex audit-trail + Rex disposition (C) operationalization.
- LA §6.X.1: revised aggregate coverage under refined metric.
- LA §6.X.2: KT-1 reassessment disposition DOES NOT FIRE (Cycle 16 proceeds with full SI scope).
- This DECISION_LOG entry: paradigm-ruling audit trail per pipeline_identity.md L51-L56 Coach-direct fill exception for paradigm-ruling documentation.
- HC-RP-S2-6 NEW carry at ED §14: kc-44 calibration delta — Discipline #10 anchoring-slip countermeasure refinement candidate for kc-45 PD inheritance.

**Forward-cycle inheritance.** Future cycles inherit refined-metric framing at ED §Field 6 to prevent recurrence of literal-vs-intent threshold-metric ambiguity per foundational threshold-metric pre-registration discipline §10 (i)+(ii). FINDINGS Layer 4 forward carry HC-RP-S2-6 + Cycle 16 close FINDINGS layer-5 lesson-learned entry.

**Non-destructive supersedure pattern (Wikidata `rank`):** original KT-1 row literal-≥80%-coverage framing PRESERVED at substrate §4 + this DECISION_LOG entry as HISTORICAL RECORD; refined metric SUPERSEDES at OPERATIONAL surface (ED §Field 6 row); audit trail preserved per Binding 8 (HC-07) + Cycle 13/14 LOCKED non-destructive supersedure precedent.

## D-S3-1 — Cycle-16-S3 Stage 5 BE-A close: KG-resident 14-field schema + SPARQL write-boundary BUILT (Path α HC-RP-S2-3 RESOLVED-VIA-NAMESPACE-EQUIVALENCE)

**Decision.** BE-A close verdict = BUILT (not yet PROMOTED) per `build-runner.md §Step 5` template. 13 artifacts shipped at `~/cycle_16_close_spec_to_implementation_gap_build/` (5 scaffolded BE-class templates filled to 0 placeholders at `docs/` + 3 NEW build artifacts at `docs/{spec_registry_schema.ttl, spec_registry_shapes.shacl.ttl, spec_authoring_discipline.md}` + 5 NEW supporting artifacts at `outputs/{build_runner_events.jsonl, cross_system_validation_be_a.json, be_a_smoke_fixture_conforming.ttl, be_a_smoke_fixture_nonconforming.ttl, build_runner_envelope.yaml}`). H6 + H7 CONFIRMATION CANDIDATES surfaced; KT-4 + KT-6 DO NOT FIRE; KT-1 DOES NOT FIRE under D-S2-1 refined-metric inheritance preserved.

**Authority chain.** Rex 2026-05-27 disposition (C) D-S2-1 (KT-1 mechanism-layer metric refined; full SI scope proceeds) > kc-45 R1 PASS task-context dispatch via Rex paste-bridge 2026-05-27 19:00 UTC > Cycle-16-S3 Coach Build-Runner Agent foreground dispatch per S141 BINDING > Coach R3 close-eval per kc-44 PD §3.3 T1-T13 + DP#43 + Coach Check #23 + HC #26 3-gate ALL PASS.

**HC-RP-S2-3 disposition: RESOLVED-VIA-NAMESPACE-EQUIVALENCE (Path α).** Build-Runner Wikidata supersedure inheritance via `cycle16:Spec rdfs:subClassOf c6:Statement` accepts `c6:rank` + `c6:supersedesRef` predicates at SHACL polymorphism (verified at 3 test beds TB-1 + TB-2 + TB-3; pyshacl conforms=True for conforming + 8 violations for non-conforming fixture ≥4 threshold). Wikidata-canonical-namespace-absence (`wikibase:rank` + `prov:wasRevisionOf` not used in any predicate body at Cycle 6 BE#1 ontology TTL ground state) documented at BE-A BUILD_DECISION_LOG §1 + this entry as namespace-equivalence: function-class PRESENT under `c6:` namespace; documentation-class gap remains as FINDINGS Layer 4 honest-gap candidate (NOT a function gap). Path γ (modify Cycle 6 LOCKED ontology TTL body) NOT TAKEN per Binding 7; `git -C ~/cycle_6_unified_substrate_build diff runtime/jena/` = 0 lines verified.

**Live SPARQL UPDATE write-boundary smoke ALL_PASS.** Coach Brief 2 pre-verification (2026-05-27 19:00 UTC): ASK HTTP 200 in 0.055s + UPDATE INSERT HTTP 200 in 0.621s + readback HTTP 200 in 0.035s + DROP cleanup HTTP 200. Build-Runner re-verified at BE-A smoke ~19:25 UTC: TB-1+TB-2+TB-3 UPDATE HTTP 200 (222-257ms) + readback HTTP 200 (5-12ms) returning 13-14 triples per spec + DROP cleanup HTTP 200 (186ms). Fuseki PID 479112 alive + `/cycle6` endpoint operational throughout.

**Honest carries at BE-A close** (3 NEW; all non-blocking per Mechanical Check #22 FLAG+CARRY classifier):
- **HC-BE-A-1**: ACCEPTANCE_CRITERIA §1 row 4 wording over-specifies readback threshold to "≥14 triples"; actual is 13 (running specs without conditional-nullable cycle_implemented/session_implemented/deferral_reason) or 14 (dormant-with-explicit-deferral including deferral_reason). Structurally correct per nullable-field design; wording refinement candidate for BE-B contract amendment OR FINDINGS Layer 4 documentation.
- **HC-BE-A-2**: HC-RP-S2-3 RESOLVED-VIA-NAMESPACE-EQUIVALENCE (Path α chosen) — sub-KT-6 candidate disposed; main KT-6 DOES NOT FIRE; FINDINGS Layer 4 carry for namespace-canonicity documentation.
- **HC-BE-A-3**: Scaffolded BE-class templates at `docs/` vs Cycle 14 precedent at project root — Cycle 16 init_project.sh scaffolding path divergence; operationally correct (Build-Runner used canonical scaffolded location); architectural disclosure per `build-runner.md §Canonical marker preservation BINDING`.

**Forward inheritance.** BE-A ARTIFACT_CONTRACT §1 pre-conditions + §2 post-conditions + §3 invariants + RUNTIME_EMIT_SPEC §1 event schema + ACCEPTANCE_CRITERIA §3 per-test-bed strengthening are S4 BE-B inputs (no spec lands without registry row + target_session + emit-event wired). HC-RP-S2-6 (kc-44 calibration delta) + HC-BE-A-1+2+3 forward to FINDINGS Layer 4. HC-RP-S2-4 (Cycle 6 PARTIAL-CLOSED Cycle 7 OPEN) + Brief 3 (cross-engine DB registration gap) Coach-only forward-carry to FINDINGS Layer 4.

**HC #50 zero-Rex-escalation baseline MAINTAINED at S3.** 0 Rex paradigm escalations this session (Build-Runner BE-A close + R3 close-eval clean; no KT-trigger ambiguity surfaced; HC #59 BINDING countermeasure NOT triggered). Cumulative kc-45 lifecycle (S3 first session): 0 genuine paradigm escalations + 1 Rex Step 3.5 disposition (Path A approval for Brief 2 curl harness scope at S3 entry — operational decision, not paradigm).
