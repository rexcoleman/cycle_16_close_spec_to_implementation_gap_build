# Requirements: Cycle 16 — Close the spec-to-implementation gap

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- stage: 3 -->
<!-- source: Cycle 16 SI ACTIVE 2026-05-27 + Amendment 2026-05-27a (deadline-tightening) + Amendment 2026-05-27b (KG-primary registry storage) + kc-44 PD §1.4 #1 + §3 + §6.1 -->

## Deliverables

10 deliverables tied to Cycle 16 SI done-criteria #1-#10:

1. **Spec inventory artifact** (Cycle 1-15 retroactive scan) — `outputs/spec_inventory_retroactive_run.json` materialized as nanopublication 3-graph triplet at Fuseki `/cycle6` endpoint; 4-spec-class enumeration covering agent contracts + schemas + design decisions + methodology commitments.
2. **Pattern analysis artifact** — `outputs/pattern_analysis_cycle_10_counterfactual.json` capturing Cycle 10 RUNTIME_EMIT_SPEC.md case study counterfactual reasoning (H4 binding) + 4-spec-class operational definitions (H2 binding) with per-class structural verifier sketch.
3. **Substrate audit artifact** — LA §6 addendum (this S2 RP authoring; surgical GPL-41 append-only to existing §6 body) + Coach R3 verification log entry capturing KT-1 disposition recommendation (pre vs post Cycle 6 KG inheritance) + KT-6 disposition recommendation.
4. **External research deliverable** — LA §1 LOCKED at Cycle-16-S1 close (`9300c86`): 7 disciplines × ≥3 verbatim quotes each (36 total per HC #43 ≥30 floor) + §1.2 cross-discipline convergence matrix + §1b adjacent field survey + §6b.1 cross-domain mechanism validity pre-check (5-import matrix).
5. **KG-primary 14-field registry schema** — RDF/SPARQL schema document at `docs/spec_registry_schema.ttl` (TTL serialization per Cycle 6 BE#1 contract) instantiating: `spec_id` + `spec_type` + `owner` + `acceptance_criteria` + `target_session` + `current_status` (5-state enum) + `cycle_authored` + `session_authored` + `cycle_implemented` (nullable) + `session_implemented` (nullable) + `runtime_emit_event_class` (or `n/a` with documented rationale per DP#26 carve-out) + `dormancy_detection_threshold_sessions` (default 3) + `deferral_reason` (nullable; required if status=dormant-with-explicit-deferral) + `rex_authorization_for_deferral_past_cycle_close` (nullable; required if target_session past cycle close) + `audit_trail_link` (PROV-O typed-edge per Cycle 6 BE#1). = 14 fields plus per-edge HC-11 access-permission enum {publishable, ip-private, ephemeral} + Wikidata `wikibase:rank` + `prov:wasRevisionOf` (HC-RP-S2-3 carry — author at Stage 5 BE#1 schema extension if absent at Cycle 6 BE#1 ground state) + nanopublication 3-graph triplet pattern (assertion + provenance + publicationInfo).
6. **SPARQL UPDATE authoring discipline spec** — `docs/spec_authoring_discipline.md` defining the gate body executed at spec-authoring boundary: SPARQL UPDATE INSERT DATA against `/cycle6` endpoint per the 14-field schema; BLOCKING discipline rejects authoring if any non-nullable field absent OR if `runtime_emit_event_class` claim of `n/a` lacks documented rationale per DP#26 carve-out.
7. **TWO-surface BLOCKING gate** — `scripts/spec_implementation_present_gate.sh` (cycle-close surface) + `scripts/spec_implementation_session_close_gate.sh` (session-close surface) — both invoke SPARQL ASK body against `/cycle6` endpoint per H6 binding; gate-script skeleton mirrors `k_register_present_gate.sh` (Cycle 14 four-gate pattern). Session-close gate scans for `current_status = 'dormant-silent'` rows where `(current_session - session_authored) ≥ dormancy_detection_threshold_sessions`.
8. **Retroactive scan one-time fire** — `outputs/retroactive_scan_cycle_1_15_run.json` capturing per-spec classification result; `current_status = 'dormant-silent'` count is the KT-2 firing surface (<3 → KT-2 fires).
9. **Forward-apply observation surface** — instrumentation enabled at Cycle 16 close such that Cycles 17 + 18 sessions emit `spec_authoring_event` + `spec_implementation_event` to `outputs/build_runner_events.jsonl` runtime sink; cross-cycle aggregation query at done-criterion #10 longitudinal verdict close.
10. **5-layer close FINDINGS + paired commit** — `FINDINGS.md` at Cycle 16 close with Layer 1 (artifacts shipped per deliverables 1-9) + Layer 2 (mechanism characterization per H1-H8 hypothesis resolutions) + Layer 3 (cell granularity per HR §3a Cycle 16 EXTENSION-3 across 4×4×5 = 80 cells) + Layer 4 (Cycle 10 counterfactual analysis + KT-1..KT-6 dispositions with evidence) + Layer 5 (honest gaps + HC-RP-S2-3 Wikidata supersedure PARTIAL forward dependency + HC-RP-S2-4 Cycle 7 substrate-viability forward dependency + any new HC discovered Stage 5).

## Per-Deliverable Acceptance Criteria

| Deliverable # | Acceptance criteria | Verification surface |
|---|---|---|
| 1 (Spec inventory) | ≥N specs enumerated where N≈90-100 per H1; 4-spec-class coverage complete; nanopublication 3-graph at `/cycle6` operational | SPARQL SELECT against `/cycle6`; Coach R3 cross-check |
| 2 (Pattern analysis) | Cycle 10 counterfactual reasoning at FINDINGS Layer 4; 4-class structural verifier sketch at HR §3c rows | DP#43 spot-read at FINDINGS Layer 4 |
| 3 (Substrate audit) | LA §6 addendum (this S2 dispatch); KT-1 disposition with evidence; KT-6 disposition with Coach probe evidence | T10 + T12 Coach R3 |
| 4 (External research) | LOCKED at S1; 36 quotes / 7 disciplines / ratio ≥0.79; preservation verified at S2 | T2 `git diff` empty for LA §1-§5 |
| 5 (KG-primary schema) | 14 fields + per-edge HC-11 enum + PROV-O 4 typed-edges + nanopublication 3-graph + Wikidata supersedure (HC-RP-S2-3 carry if PARTIAL); TTL at `docs/spec_registry_schema.ttl` | SPARQL schema introspection at `/cycle6` |
| 6 (Authoring discipline) | SPARQL UPDATE INSERT DATA gate body; BLOCKING rejection if required fields absent; DP#26 carve-out for methodology commitments documented | H7 forward-apply observation Cycle 16 itself |
| 7 (TWO-surface gate) | Both gate scripts present at canonical path; SPARQL ASK body; gate fires BLOCKING with --advisory-mode flag for opt-in WARN | H6 + KT-4 surface; gate script unit smoke at Stage 5 |
| 8 (Retroactive scan) | One-time fire at Cycle 16 mid-cycle; per-spec classification result JSON; ≥3 dormant-silent surfaced else KT-2 fires | H3 + KT-2; aggregate query at scan close |
| 9 (Forward-apply) | Runtime emit instrumentation enabled at Cycle 16 close; spec_authoring + spec_implementation event classes wired to `outputs/build_runner_events.jsonl` | H8 longitudinal; Cycles 17-18 sessions |
| 10 (Close FINDINGS) | 5-layer per Cycle 14 multi-layer precedent; paired commit with HR resolution log filled; all KT dispositions cited | Cycle 16 close Stage 5 BE-class final |

## Quality Requirements

- **Minimum verbatim quote density:** ≥30 quotes across 7 external disciplines at LA §1 (per HC #43 floor). **LOCKED at S1 close at 36 quotes (71% over floor); preserved.**
- **Minimum sources at LA:** 7 distinct external disciplines + 4 internal substrates (RIDE / research_depth_enforcement_automation / Cycle 14 four-gate / Cycle 6 unified KG). **LOCKED at S1 close.**
- **External body share ≥0.80 at LANDSCAPE_ASSESSMENT.md (Binding 1):** LA §6c.2 audit at S1 close measured ≈0.79-0.83 depending on Mixed-section classification methodology. **Verified at S1 close; preserved.**
- **0 placeholders in all 5 Stage 3-4 canonicals + LA §6 addendum** at S2 close (per Mechanical Check #22; Cycle 14 ALL_PASS precedent).
- **Cycle 6 KG substrate-viability primitives operational** — verified at Coach probe 2026-05-27: 246,048 quads / 46 named graphs + SPARQL latency ≤0.5s (10-256× margin) + PROV-O 4 typed-edges + HC-11 access-permission enum 11,223+ usages + nanopublication 3-graph pattern. (HC-RP-S2-3: Wikidata `wikibase:rank` + `prov:wasRevisionOf` PARTIAL — author at Stage 5 BE#1 schema extension.)
- **HC-11 partition strict** (kc-44 PD §3.7): PUBLISHABLE = research question + 4 branches + done-criteria + KT-1..KT-6 triggers + cycle shape + 5-state taxonomy + 14-field registry schema + Cycle 6 KG inheritance narrative. PIPELINE-IP-PRIVATE = agent-prompt internals + rubric algorithm bodies + dispatch substrate content + RT prompts + adversarial inputs (gitignored). All 5 Stage 3-4 canonicals + LA §6 addendum contain PUBLISHABLE content only.
- **DP#43 + DP#44 binding:** refuse-on-missing-precondition. If any input not readable, Cycle 6 substrate state not accessible, KT triggers not pre-registered → HALT + surface specific defect; do NOT fabricate.
- **Stage 0-2 LOCKED preservation** (Binding 7 + S155): no body modification to docs/{OBSERVATION_LOG.md, RESEARCH_QUESTION_SPEC.md}; only surgical §6 addendum permitted to docs/LANDSCAPE_ASSESSMENT.md per Cycle 14 Amendment 2026-05-24c precedent. `git diff` empty for OBS + RQS at R3 verify.

## Constraints

- **Single research cycle within wrapper-program EMABS envelope ≤6 sessions** (per disposed paradigm question #1 + Cycle 1 envelope cap).
- **Build-class research type** (per `governance.yaml`: profile=research-build; research_type=build). Stage 5 BE-class sessions (4-5 BE-A..BE-E per Cycle 14 multi-BE precedent).
- **Compute resources sufficient** for cycle scope: Azure (7.7 GiB) handles all SPARQL UPDATE/ASK + retroactive scan + gate-script invocation. Mac Mini (48GB) available via Tailscale if needed for larger-graph batched SPARQL (not anticipated; Coach probes confirm latency ≤0.5s at current 246K-quad scale).
- **No multi-session execution beyond ROADMAP plan** (per Discipline #11 paired-commit binding).
- **Stage 0-2 input artifacts read-only** at S2 (Cycle-16-S1 close immutable per Binding 7).
- **Forbidden language per `project.yaml.audit.prohibited_language`** (5 enumerated tokens listed in `project.yaml`; not re-quoted here to keep this requirements artifact itself compliant) — avoided in all 5 Stage 3-4 canonicals + LA §6 addendum.
- **Claim tags per `project.yaml.audit.claim_tags`:** DEMONSTRATED / SUGGESTED / PROJECTED / HYPOTHESIZED — applied at FINDINGS Layer 4 (not Stage 3-4 canonicals; pre-Stage-5 they are pre-registrations, not claims).
- **Stage gate path discipline** (HC-RP2 carry from S1): stage gates expect canonicals at project-root; build-class scaffold places stage 0-2 at docs/. Stage 3-4 canonicals (this S2) at project-root — gate-path expectation satisfied; HC #55 candidate carry for future-cycle refinement.

## Stage Inputs (Read-Only at S2 Stage 3-4 Dispatch)

Stage 0-2 LOCKED canonicals at `docs/` (Cycle-16-S1 close `9300c86`):

- `docs/OBSERVATION_LOG.md` (260L; 10 canonical markers; n=8 OBS + PAT-1..PAT-4 meta-patterns + §3b 21-category structured enumeration 100% coverage per GPL-90).
- `docs/RESEARCH_QUESTION_SPEC.md` (498L; 18 canonical markers; §0a paradigm challenge + Lakatos test + §1.1 question lineage 5-prior-work table + §3a H1-H8 hypothesis enumeration verbatim L242-L253 + KT-1..KT-5 pre-registration matrix).
- `docs/LANDSCAPE_ASSESSMENT.md` (565L; 24 canonical markers; 7 disciplines × ≥3 verbatim quotes each at §1 rows 1-7; §1.2 cross-discipline convergence matrix; §1b adjacent field survey 4-row; §1.1 benchmark; §2 5-gap map; §2b fragmentation diagnosis; §3 baseline knowledge + §3.1 uncertain/contested depth expansion; §4 frontier moat test; §5 v_landscape_inputs query 3,128 rows; §6 EDA readiness with 4-row data source sample verification; §6b handoff to hypothesis with 4 sub-elements + 2 bridge rows; §6b.1 cross-domain mechanism validity pre-check 5-import matrix; §6b.2 internal substrate cross-validation 6-row; §6c depth self-audit aggregate 8.5/10; §6c.1 verbatim quote density audit 36 quotes; §6c.2 body-share ratio audit ≈0.79-0.83 external).

Stage 2 augmentation permitted at S2 (this dispatch):

- `docs/LANDSCAPE_ASSESSMENT.md §6 addendum` — surgical GPL-41 append-only after existing §6.B internal substrate row per substrate §5; +35-60L addendum encoding Cycle 6 KG substrate row + revised aggregate coverage + KT-1 reassessment + KT-6 detection-threshold-disposition row.

## Verification Surfaces (Coach R3 mechanical tests T1-T13 per kc-44 §3.3 + substrate §9)

- **T1.** Per-file placeholder check (double-brace literal-token grep) across cycle_16/HR + ED + PROJECT + REQUIREMENTS + ROADMAP = 0/0/0/0/0 + LANDSCAPE §6 addendum =0.
- **T2.** Stage 0-2 LOCKED preservation (no body mod to OBS/RQS/LA; only LA §6 surgical addendum). `git diff` = empty for OBS + RQS.
- **T3.** HYBRID PRIMARY VERBATIM CARRY 4 LOCKED + Cycle 16 EXTENSION-3 auditable at HR §3a + ED §0a.
- **T4.** All 5 canonicals + LA §6 addendum within line bands per substrate §2.
- **T5.** H1-H8 carried to HR §3 with Cycle 16 specialization (statement + falsification + metric + field_surprise + resolution=OPEN + evidence per row).
- **T6.** KT-1..KT-6 pre-registered structurally at ED §Field 6 (detection-point + threshold + disposition).
- **T7.** HC-11 partition — no pipeline-IP-private content leaked into publishable artifacts.
- **T8.** DP#43 spot-read ≥4 primary content sections across HR + ED + REQUIREMENTS + ROADMAP.
- **T9.** Amendments 2026-05-27a + 27b structurally encoded at ED §Field 6 + §4a + REQUIREMENTS #5-#7 + ROADMAP Stage 5.
- **T10.** Cycle 6 substrate-viability evidence substantively at LA §6 addendum (DP#43 spot-read; Coach-probed 2026-05-27 evidence cited).
- **T11.** KG-primary 14-field schema reflected in HR + ED + REQUIREMENTS + ROADMAP; per-edge HC-11 + PROV-O + Wikidata + nanopub primitives explicit at ED §4a.
- **T12.** §6 aggregate coverage REVISED at addendum (pre vs post Cycle 6 KG) + KT-1 reassessment (DOES NOT FIRE under refined metric per Rex paradigm-ruling 2026-05-27 disposition (C) metric-revision-within-intent; DECISION_LOG D-S2-1).
- **T13.** H4 counterfactual: Cycle 10 BE#5+#6 hypothetical Cycle 16 mechanism — registry row + target_session=Cycle-10-close + runtime_emit_event_class wiring would surface dormancy at Cycle 10 close.

> All 13 mechanical tests run independently by Coach at R3 per `feedback_honest_evaluation.md`; RP self-report not load-bearing.

## Honest Carries Open (forward-cycle deliverables tracked at FINDINGS Layer 5)

| HC ID | Description | Carry surface |
|---|---|---|
| HC-RP-S2-3 (NEW at S2) | Wikidata supersedure pattern PARTIAL at Cycle 6 KG ground state: only `cycle6:rankingRationale` present; `wikibase:rank` + `prov:wasRevisionOf` absent at 2026-05-27 Coach probe | ED §4a constraint #4 + Stage 5 BE#1 schema extension OR FINDINGS Layer 4 honest gap |
| HC-RP-S2-4 (NEW at S2) | Cycle 6 PARTIAL-CLOSED + Cycle 7 substrate-viability research-class cycle OPEN per Rex Decisions 1-4 2026-05-14g (BE#4 BUILT-NOT-PROMOTED HOLD) | FINDINGS Layer 4 forward dependency carry; H5 KT-1 surface explicit acknowledgment; vendor-portable abstraction if Cycle 7 surfaces vendor pivot |
| HC-RP1 (S1 carry) | RQS §3a +38L over upper band — load-bearing 4-branch × KT decomposition non-truncable | FLAG+CARRY per Mechanical Check #22; future-cycle template refinement |
| HC #55 candidate (S1 carry) | Stage-gate file-path mismatch — Stage 3-4 canonicals at project-root resolve; Stage 0-2 at docs/; HC #55-class for kc-44 PD inheritance | Resolved at S2 by placing canonicals at root; refinement carry |
| HC-RP-S2-5 (NEW at S2 if applicable) | KG-primary `runtime_emit_event_class = 'n/a'` over-use risk for methodology commitments per DP#26 carve-out — KT-3 firing surface (per H7) if ≥30% of methodology commitments take `n/a` | Cycle 16 forward-apply observation + KT-3 disposition |
| HC-RP-S2-6 (NEW at S2 R3) | kc-44 calibration delta: Coach R3 anchoring-slip at KT-1 paradigm escalation 2026-05-27 — operationally-disposable per foundational threshold-metric pre-registration discipline §10 (i)+(ii); Rex disposition (C) corrected via metric-revision-within-intent (DECISION_LOG D-S2-1) | kc-45 PD inheritance — Discipline #10 anchoring-slip countermeasure refinement at kc-N inbound gate at Coach R3 paradigm escalation |

> Honest carries carried forward across Cycle 16 close into Cycles 17-18 forward-apply window per longitudinal verdict discipline.
