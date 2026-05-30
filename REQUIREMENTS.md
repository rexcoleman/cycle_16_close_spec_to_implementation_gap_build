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

<!-- amendment_2026_05_28a_extension_start -->

## Done Definition Extended — Done #11-#19 (Cycle-16-S10 Stage 3-4 RP fill per SI Amendment 2026-05-28a + 2026-05-28b verbatim; fulfilling SI's research question structurally)

<!-- source: dispatch substrate §3.c Cycle-16-S10 RP fill scope — Done #11-#19 verbatim + close gate criteria -->
<!-- source: Cycle 16 SI Amendment 2026-05-28a body (Moonshots `5b1e8d6` + paired) Done #11-#16 + Amendment 2026-05-28b body (Moonshots `f66714f`; wrapper `3e5907a`) Done #17-#19 -->
<!-- source: Rex 2026-05-28 paradigm ruling walking back S8 FORMAL CLOSE — Cycle 16 stays OPEN — and Rex 2026-05-28 "proceed" directive post-kc-47 self-audit -->
<!-- gate:requirements done_definition_extended #11..#19 required -->

**Framing per SI Amendment 2026-05-28b.** Done #1-#10 above stand as audit-trail of original under-spec'd pre-registration. **Done #11-#19 are what fulfilling SI's research question structurally requires** — not "recovery" in the sense of correcting a failure, but **completion in the sense of finishing the cycle's actual intent**. The S8 5-layer FINDINGS (481L LOCKED at `fb3a0fe` + `25eff54` + `6c80afb`) stands as a phase-checkpoint Layer 1-5 retrospective per DP#42 non-destructive supersedure; Cycle 16 TRUE close-arc FINDINGS at Phase 10 supersedes via non-destructive supersedure pattern.

**LOCKED-body discipline (Binding 7 + DP#42 strict).** Done #1-#10 (Deliverables list §1-§10 above) LOCKED at S2 RP fill + S8 phase-checkpoint close per `9300c86` + `fb3a0fe`; Done #11-#19 ADDITIVELY APPENDED here are extension to the Done definition. Verify via `git diff --stat` zero deletions on pre-marker line ranges (Done #1-#10 + Per-Deliverable Acceptance + Quality Requirements + Constraints + Stage Inputs + Verification Surfaces T1-T13 + Honest Carries Open + closing quote).

### Done #11-#19 verbatim from SI Amendments 28a + 28b

**Done #11 — Past: probe-grounded measurement.** Four code-active probe primitives shipped (Class A AgentContract = Agent-tool invocation observer keyed by subagent_type; Class B Schema = per-schema validator emit at validation call site; Class C DesignDecision = ADR-to-code embodiment scanner combining `git grep` of must-clauses with LLM-judge; Class D MethodologyCommitment = citation-and-application scanner across downstream warmups + FINDINGS). Each probe ships with passing self-test against known-good and known-bad fixtures before library admission. Retroactive scan re-runs with probes. Heuristic 137 replaced by measured count per class with confidence bounds. Owner triage complete for every measured-dormant spec — implement / defer with named target session + reason + Rex authorization + re-activation condition / kill with ADR retraction.

**Done #12 — Present: write-boundary closure (HC-BE-D-1 closure).** Pre-commit hook scans staged files for new spec-class artifacts (agent_spec markdown / schema files / DECISION_LOG ADR entries / FINDINGS Layer 5 commitment markers); blocks commit unless corresponding `register_spec()` landed in the same commit. Filesystem watcher (fsnotify) on the same paths emits `spec_authoring_event` on writes that bypass git. `forward_apply_emit()` wired into `register_spec()` in production — BE-E observation surface fires on real authoring events, not synthetic smoke. Three-registry reconciliation gate at every session close (filesystem + KG + `prompt_inventory`); three-way drift becomes forbidden state that blocks close.

**Done #13 — Future: probe-library-as-canonical-vocabulary.** Probe library lives as code at `~/ml-governance-templates/scripts/probes/<class>/<primitive_id>.py`. Each primitive specifies behavioral surface verified, input fixture, execution method, observable success criterion, and a self-test against known-good + known-bad fixtures. Library documentation index generated from code state. Probe primitives version-lock at creation; modifications require Builder-ARCH dispatch (paradigm-class; Rex disposition). New probe classes for new problem domains require Builder-ARCH dispatch. Generic-emission escape primitives forbidden at library design — refused at Builder-ARCH paradigm boundary.

**Done #14 — Future: Operational-Definition Substitution Gate.** Gate at Stage 1 RQS close + Stage 4 ED close + Stage 4 ACCEPTANCE_CRITERIA close. Predicate is a runnable script that IMPORTS the named probe primitive at gate-fire time and verifies executable + has a passing self-test. Definitions resolving to "field value equals enum" / "artifact exists at path" / "token count ≥ N" / "emission record exists" without a probe reference FAIL the gate. Hard block. The check is structural — the gate physically cannot pass on a string-match proxy because it executes the named primitive.

**Done #15 — Future: structural-prevention layer 7 additional pieces.** (a) Stage 0 probe-presence check — kernel-coach + RP inventory required probe primitives BEFORE Stage 1 entry; halt-and-surface for Builder-ARCH dispatch if primitives absent; no "proceed with temporary citation density" escape hatch. (b) Reality-vs-intent gate moved forward from FINDINGS close to Stage 1 RQS R3 close-eval + Stage 4 ED R3 close-eval; mandatory structured table per H / KT / acceptance row with pre-registered intent + operational metric verbatim + probe primitive referenced + implementation-artifact baseline check result; missing or incomplete table = R3 FAIL. (c) Number-tagging structural gate at every Rex-facing surface (FINDINGS / close summaries / transition prompts / handoffs); every primary number carries a measured / heuristic / anecdotal tag; close gate BLOCKS if any number tagged "heuristic" appears in a Done-criterion verdict. (d) Probe-coverage check at FINDINGS close — for every spec class the cycle claims to govern, FINDINGS must show ≥1 probe firing per class with non-zero production count; smoke-only fires accepted only for the probe library's own self-test, never as cycle-deliverable evidence. (e) Probe library self-test at every session close — library exercises every primitive against its fixtures and emits results to a self-test event sink; primitives whose self-test fails for 2 consecutive sessions auto-deprecate; auto-deprecation blocks session close until repair via Builder-ARCH dispatch or removal via paradigm disposition. (f) Deferral expiration — specs deferred past authoring cycle close must specify named target session + reason + re-activation condition + maximum dormancy window; deferrals exceeding window auto-route to kill or Rex re-disposition; silent deferral persistence is forbidden state. (g) Design-anchor disclosure at LANDSCAPE close — new mandatory enumeration of load-bearing mechanism design elements tagged external-anchored or internally-inherited; internal-inheritance of load-bearing design (not just substrate primitives) triggers Stage 2→3 checkpoint review + surfaces as paradigm escalation candidate flag (extends Binding 2 enforcement from ratio check to design-anchor check).

**Done #16 — Forward inheritance: govML v2.8.6 ADDITIVE-APPEND chain extension to n=6.** Probe library + Operational-Definition Substitution Gate + 7 structural-prevention pieces back-port to govML at scripts/init_project.sh `install_probe_library_canonical_vocabulary()` + `install_operational_definition_substitution_gate()` + `install_structural_prevention_layer()` + templates/build/probes/ NEW dir + templates/build/structural_prevention/ NEW dir + VERSION v2.8.5 → v2.8.6 + CHANGELOG.md v2.8.6 entry. LOCKED bodies of prior install functions UNMODIFIED (v2.8.2 runtime_emit + v2.8.3 spec_registry + v2.8.4 spec_implementation_gates + v2.8.5 forward_apply_observation). Every freshly-scaffolded build-type project inherits at scaffolding time.

**Done #17 — Cycle-close BLOCKING gate predicate UPGRADED to probe-fire evidence (SI Amendment 2026-05-28b).** Gate-script predicate body invokes named probe primitive via Python subprocess at gate-fire time per Done #14 import-and-execute discipline; hard block on missing probe fires for any spec authored in-cycle; accepts `killed` with ADR retraction OR `dormant-with-explicit-deferral` with Rex authorization + named target session + re-activation condition + maximum dormancy window as valid terminal states; closes SI disjunct (b) "implemented running code by the close of the authoring cycle (default)."

**Done #18 — Kill discipline mechanism (SI Amendment 2026-05-28b).** NEW function `kill_spec(spec_iri, adr_retraction_ref, killing_session)` in `scripts/spec_registry_authoring.py` validates ADR-style retraction in DECISION_LOG + emits `spec_killed_event` + SPARQL UPDATE transitions `cycle16:currentStatus` to `cycle16:killed` + records retraction reference at `cycle16:auditTrailLink`; empirical baseline Cycle 16 BE-D found 0 killed across 4 classes — kill discipline broken at workflow layer; Done #11 owner-triage routes "kill this spec" decisions through this mechanism; closes SI disjunct (d) "explicitly killed with audit trail."

**Done #19 — ≤3-session dormancy threshold preservation made explicit (SI Amendment 2026-05-28b).** Existing BE-C session-close ADVISORY gate threshold check preserved post-recovery; FINDINGS close verification that threshold continues to fire correctly on probe-fire evidence not registry-field evidence; closes SI disjunct (e) "structural detection of dormancy within ≤3 sessions of authoring via the runtime emit mechanism."

### Close Gate Criteria — Cycle 16 TRUE close-arc FORMAL CLOSE

Cycle 16 TRUE close-arc FORMAL CLOSE happens when ALL of the following land:

1. **Probe-grounded measurement replaces heuristic 137** (Done #11; H_recovery_1) — 4 probe primitives Class A/B/C/D exercised against production specs (NOT smoke); per-class measured dormant counts reported with confidence bounds; heuristic 137 replaced.
2. **Write-boundary closed** (Done #12; H_recovery_2) — pre-commit hook + fsnotify watcher + 3-registry reconciliation gate composition ships and fires on production write paths.
3. **Cycle-close gate upgraded to probe-fire predicate** (Done #17; H_recovery_7) — `spec_implementation_present_gate.sh` body invokes probe primitive via subprocess; SPARQL ASK on `cycle16:currentStatus` removed/commented; HARD-BLOCK on missing probe fire.
4. **Kill discipline mechanism shipped** (Done #18; H_recovery_8) — `kill_spec(spec_iri, adr_retraction_ref, killing_session, kill_reason)` function with ADR validation + `spec_killed_event` emit + SPARQL UPDATE state transition + DP#44 refusal.
5. **≤3-session dormancy threshold verified on probe-fire evidence** (Done #19; H_recovery_9) — session-close gate evidence schema shows `evidence_type: probe_fire_aggregate` (NOT `registry_field_read`); ≥3 dormancy-firing test cases verified on probe-fire.
6. **Structural-prevention 7-piece layer ships in govML v2.8.6** (Done #15a-g + #16; H_recovery_5 + H_recovery_6) — all 7 pieces materialized + integrated into `init_project.sh` install path; v2.8.5 → v2.8.6 transition; LOCKED bodies of prior install functions UNMODIFIED per HC #45 ADDITIVE-APPEND precedent class.
7. **Probe library canonical vocabulary ships** (Done #13; H_recovery_3) — ≥4 primitives Class A/B/C/D at `~/ml-governance-templates/scripts/probes/` with passing self-tests + admission gate refusing primitives without self-test.
8. **Operational-Definition Substitution Gate ships at Stages 1+4 closes** (Done #14; H_recovery_4) — gate body IMPORTS and EXECUTES named primitive via subprocess; ≥3 negative-fixture refusals; RP self-dogfooded.
9. **TRUE close-arc 5-layer FINDINGS authored per Cycle 11/12/13/14 precedent (480-590-line band)** — supersedes S8 phase-checkpoint FINDINGS via DP#42 non-destructive supersedure; Layer 1-5 structure preserved; honest reality-vs-intent diagnostic per memory binding `feedback_cycle_close_reality_vs_intent_diagnostic.md`.
10. **0 of 5 KT-7..KT-11 fires** at BE-F + BE-G + BE-H + BE-I close-evals (KT-10 firing = H_main_recovery REFUTED candidate → paradigm escalation per HC #74; KT-11 firing = LOCKED-body violation halt for re-do per HC #45).
11. **4-repo paired commit + push verify** per HC #45 chain extension precedent (cycle_16 + EMABS + Moonshots + govML); cross-system paired-commit ledger emitted.

Done #11-#19 completion + 11-criterion close-gate ALL_PASS = Cycle 16 TRUE close-arc FORMAL CLOSE. Until then, Cycle 16 stays OPEN per Rex 2026-05-28 paradigm ruling walking back S8 FORMAL CLOSE designation; "if we move to a new cycle the problem will persist... should we keep it to cycle 16 so we actually solve the fucking problem."

### Cycle 16 close-state at S10 (this RP fill)

- **9 of 10 SI Done Definition items CLOSED** at S8 phase-checkpoint (per S8 ROADMAP §7.3 closure annotation; LOCKED at `fb3a0fe`+`25eff54`+`6c80afb`).
- **Done #11-#19 OPEN; Stage 3-4 RP fill complete at S10 (this session)**; Stage 5 BE-F + BE-G + BE-H + BE-I builds queued for Cycle-16-S11+.
- **Phase 10 retroactive scan re-run + owner triage + TRUE close-arc 5-layer FINDINGS authoring** queued post-BE-F admission.

<!-- /gate:requirements done_definition_extended -->

<!-- amendment_2026_05_28a_extension_end -->

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

<!-- amendment_2026_05_29_phase11_start -->

## Done Definition Extended — Done #47 + #49 + #50 + #51 Per-Deliverable Acceptance Criteria (Cycle-16-S20 Phase-11 RP fill per SI Amendment 2026-05-29g (28g) ruling (a); verbatim-faithful to 28g + dispatch §2 bars)

<!-- source: SI Amendment 2026-05-29g (28g) Done #49/#50/#51 + ruling (a) verbatim — `.claude/workspace/cycle_16_si_amendment_2026_05_29g.md` -->
<!-- source: cycle_16_s20_phase11_rp_dispatch_substrate §2 (the substitution traps as falsifiable thresholds) + §3.3 REQUIREMENTS authoring scope -->
<!-- source: HR §3.phase11 H_phase11_49/50/51 + ED §5.phase11 BE-R/BE-S/BE-T (this same S20 RP fill) -->
<!-- gate:requirements done_definition_phase11 -->

**LOCKED-body discipline (Binding 7 + DP#42 strict).** Done #1-#19 + Close Gate Criteria 1-11 + Per-Deliverable Acceptance + Quality Requirements + Constraints + Stage Inputs + Verification Surfaces + Honest Carries LOCKED at prior closes; Done #47 + #49 + #50 + #51 ADDITIVELY APPENDED here. Verify via `git diff` zero change on pre-marker line ranges.

### Done #47 + #49 + #50 + #51 verbatim-faithful per-deliverable criteria

**Done #50 — Denominator honesty (found ≠ all).** The cycles-1–16 spec denominator is derived by ≥2 GENUINELY INDEPENDENT discovery methods (not the registry/recorded set alone): Method 1 = the BE-D recorded-artifact scan (232 distinct [measured]); Method 2 = an authored-intent scan reading sources Method 1 does NOT read (git history of spec-bearing commits + DECISION_LOG/handoff/SI-amendment prose + session transcripts). A dual-scan of recorded artifacts (registry + KG + canonical docs) is ONE method with one blind spot — REFUSED; the methods MUST be provably reading different sources (`methods_read_disjoint_sources` independence assertion). The divergence `authored_but_unrecorded = |authored_intent ∖ recorded|` is surfaced as a finding with per-spec provenance. The residual blind spot (intentions never written down anywhere) is explicitly bounded and disclosed, never rounded to zero. Every "100%" completion claim is scoped to the discoverable population (recorded ∪ authored-intent) with the residual stated; a bare "100%" is REFUSED. Closes hole #2; implements general discipline #29; sharpens Done #43 + #37.

**Done #49 — Spec-extraction completeness validated.** For each cycles-1–16 spec, the set of checkable commitments extracted from its prose is validated by a SECOND INDEPENDENT extraction (different method / different reader): E1 (rule-based parser) + E2 (independent mechanism at a different model/reader); `extraction_methods_distinct` asserts the mechanisms differ (a re-run of one reader is REFUSED). Extraction-completeness = per-spec + aggregate `jaccard = |E1∩E2|/|E1∪E2|` [measured] + disclosed; the symmetric difference `E1 △ E2` is surfaced for adjudication, never dropped. Detectors run against the reconciled VALIDATED commitment set V, never a single-reader extraction (a guard HARD-FAILS a detector wired to E1-alone or E2-alone). Closes hole #1; implements general discipline #28.

**Done #51 — Validation-tier disclosure (ruling (a); no human in close path).** No uniform "100% validated." Execution-checkable specs validate at full rigor (`FP==0 AND recall≥0.90` vs blind ground truth) OR explicit honest PASS-LOW-POWER with `n_eval` disclosed. Semantically-judged specs validate ONLY by diverse, structurally-independent automated judges that must AGREE — `judge_uses_different_model_or_method` asserts diversity (GT=`claude-sonnet-4-6` ≠ probe=`claude-haiku-4-5`; the harness `_gt_code_token_crosscheck` is a different code path); a single judge or a judge agreeing with itself is REFUSED; NEVER a human in the close path (`close_verdict_fn_human_inputs == 0`). Disagreement / ambiguity / missing-signal fails safe (NOT-VALIDATED) and is surfaced for the human's after-the-fact audit — agreement is NEVER engineered (the S19 ~45% [measured] judge disagreement correctly yielding CONTESTED is the bar working). The completion claim declares, per spec, which tier validated it, and the judgment-tier residual confidence gap is disclosed. Closes hole #3; implements general discipline #30.

**Done #47 — Guard-the-guards.** The enforcement infrastructure itself — the probes, the gates, the agent specs, AND the accuracy harness — is enumerated INTO the audited population (an unaudited guard is the recursive failure in miniature). The Build-Runner pulls the infra into the denominator (`is_enforcement_infra: true` entries) and runs the trusted detectors over it too; the harness's own implementation status is measured, not assumed. Run-time independence is re-asserted (`probe_accuracy_harness.py --self-test` `independence_clean == true`) before the run is accepted (the prober may not be its own proxy).

### Per-Deliverable Acceptance Criteria — Phase 11

| Deliverable # | Acceptance criteria | Verification surface |
|---|---|---|
| 50 (Denominator honesty) | `methods_read_disjoint_sources(S1,S2)==True` [measured, boolean] (dual-scan REFUSED); `authored_but_unrecorded` [measured] with per-spec provenance; residual R bounded + disclosed (never 0); every "100%" scoped to discoverable population | BE-R §5.phase11.1 thresholds 1-3; Coach R3 mechanical re-check of independence assertion + `outputs/denominator_dual_method.json` |
| 49 (Extraction completeness) | `extraction_methods_distinct==True` [measured, boolean] (single-reader-twice REFUSED); per-spec + aggregate Jaccard [measured]; `E1 △ E2` adjudication ledger (no silent drops); `detector_input_is_reconciled_validated_set==True` (single-reader-as-input REFUSED) | BE-R §5.phase11.1 thresholds 4-6; Coach R3 re-check of `outputs/extraction_completeness.json` + `validated_commitment_set.json` |
| 51 (Validation-tier disclosure) | per-spec tier label; execution = `FP==0 AND recall≥0.90` OR honest PASS-LOW-POWER(`n_eval`); judgment = diverse judges (`judge_uses_different_model_or_method==True`) AGREE else fail-safe NOT-VALIDATED; `close_verdict_fn_human_inputs==0`; uniform "100% validated" REFUSED | BE-S §5.phase11.2 thresholds 1-6; Coach R3 re-check of `outputs/validation_tier_verdicts.json` + judge-diversity + fail-safe events |
| 47 (Guard-the-guards) | probes + gates + agent specs + accuracy harness enumerated INTO audited population (`is_enforcement_infra: true`); detectors fire over infra; detector input = reconciled V; `independence_clean==true` re-asserted; no un-scoped "100%" | BE-T §5.phase11.3 thresholds 1-6; Coach R3 re-check of `outputs/guard_the_guards_population.json` + `trusted_detector_run.json` |

### Close Gate Criteria — TRUE-close extension item (i) (SI Amendment 28g)

Per Amendment 28g TRUE-close extension: Cycle 16 closes ONLY when (a)-(h) per Amendments 28e+28f hold AND **(i) Done #49–#51 land** — spec-extraction completeness validated + denominator derived dual-method with residual disclosed + every completion claim tier-labelled with the judgment tier validated by agreeing diverse automated judges (no human in the close path), with guard-the-guards (#47) folding the enforcement infra into the audited population. The "100%" claim at close is explicitly TWO-TIER and RESIDUAL-DISCLOSED; a uniform "100% validated" is REFUSED. This item (i) is appended to the 11-criterion close gate above as criterion 12.

**Close gate criterion 12 (NEW; Amendment 28g item (i)).** Done #50 (denominator dual-method, residual disclosed) + Done #49 (extraction completeness validated, detectors on V) + Done #51 (per-spec tier-labelled verdict, diverse-agreeing judges, fail-safe, 0 human in close path) + Done #47 (guard-the-guards) ALL land; the close "100%" claim is two-tier + residual-disclosed; a uniform "100% validated" is REFUSED at close. Until criterion 12 holds (alongside criteria 1-11), Cycle 16 stays OPEN.

### Cycle 16 close-state at S20 (this Phase-11 RP fill)

- **Done #49 + #50 + #51 + #47 OPEN; Stage 3-4 RP fill complete at S20 (this session)**; Stage 5 BE-R + BE-S + BE-T builds queued for Cycle-16-S21+.
- **Reality-vs-intent baseline (HR §3.phase11.2):** Method 2 (authored-intent scan) DOES NOT EXIST today (denominator is single-method); the second extraction DOES NOT EXIST today (detectors consume single-reader BE-D scan); the diverse-judge machinery EXISTS (S19) but is NOT yet productionized as a close-path verdict with per-spec tier labels + proven 0-human-in-close-path. Phase 11 builds/productionizes these; the gaps are the work, not regressions.
- **Phase 11 FINDS + CERTIFIES the gaps; Phase 12 (100% probe-fire verification) → Phase 13 (build/kill/defer the missing spec code)** is the route-forward (NOT this phase).

<!-- /gate:requirements done_definition_phase11 -->

<!-- amendment_2026_05_29_phase11_end -->

<!-- amendment_2026_05_30_s22_refinement_start -->

## Per-Deliverable Acceptance Criteria — S22 refinement (a) frozen spec-class definition + (c) two-reader V composition (Cycle-16-S22 RP refinement; root fix of the S21 HOLD)

<!-- source: S21 Coach R3 HOLD findings 1-3 (cycle_16 01a165d, ADR-S21-1, BUILD_DECISION_LOG row 14-R3) -->
<!-- source: docs/spec_class_frozen_definition.md + ED §5.phase11.1-R threshold 6′/7/8 + HR §3.phase11.1-R rows (this same S22 RP fill) -->
<!-- source: cycle_16_s22_rp_refinement_dispatch_substrate §3 (anti-gaming guards) + §4 (frozen def) + §5 (T6′) -->
<!-- source: .claude/strategic_frame.md Binding 6 (RP authors, Coach does not) + Binding 7 (process-guided; no Coach-direct gate edit) + Binding 8 (HC-07/HC-11) -->
<!-- gate:requirements done_definition_phase11_refinement -->

**Scope LOCKED (four RQS spec classes ONLY; substrate §1).** The denominator population is AgentContract + Schema + DesignDecision + MethodologyCommitment. `DP#N / HC#N / GPL / Pattern / Binding` are references, NOT denominator members. This is the RQS's own answer; it is NOT a Rex question and is NOT reopened.

**Deliverable (a) — the frozen spec-class definition (RP authors this S22; the freeze-before-count artifact).** Acceptance:
1. Canonical artifact `docs/spec_class_frozen_definition.md` exists and specifies, for the cycles-1-15 denominator: (i) ONE method-stable counting unit (one distinct spec = one `(spec_class, canonical-definition-site)` tuple, deduped by `sha256(repo|realpath|spec_class)`); (ii) a per-class membership predicate for all four classes, each derived top-down from the `cycle16:SpecType` `rdfs:comment` + HR §3c/H2 verifier; (iii) the three exclusions — `DP#N/HC#N/GPL/Pattern/Binding` principle-references, Cycle-16-own `Done #N` items, naming-FP substring matches (removed by canonical-identity dedup); (iv) the cycles-1-15 scope rule (`cycle_authored ∈ {1..15}`; Cycle-16 authorship excluded); (v) a one-sentence derivation rationale per boundary + per exclusion, grounded in class semantics NOT a target count.
2. **Freeze-before-count (the order is the whole point; substrate §3.1).** The artifact is committed FIRST, BEFORE any re-count. The Build-Runner re-run (deliverable (b), next dispatch) cites it by path + commit SHA; the cited commit is an ancestor of the re-run commit (`git merge-base --is-ancestor` exits 0). A re-run that does not cite a prior-committed frozen definition is REFUSED.
3. **±5% must EMERGE, never tuned-to-agree (substrate §3.2).** Under the frozen definition the three-method spread is MEASURED. If the methods STILL diverge beyond ±5%, that is an HONEST FINDING, disclosed — the definition is NOT loosened/redrawn to force agreement (a stable-because-tuned number is REFUSED). On residual divergence, the most-defensible single denominator is stated as "100% of the discoverable population, residual R disclosed"; R is disclosed, never zeroed.

**Deliverable (c) — the strengthened #49 T6 acceptance criterion (RP authors this S22 as threshold 6′; Build-Runner implements the code).** Acceptance:
1. ED §5.phase11.1-R threshold 6′ checks V's COMPOSITION, not its label: per-reader contribution share `e1_share, e2_share` each ≥ 0.20 AND neither solo share > 0.80; aggregate Jaccard ≥ 0.20. The floors are derived from what two-reader validation MEANS (a reader contributing < 1/5 of V is a garnish; 0.20 = 1/(readers+3) lenient principled minimum) — NOT set to any number the current run passes.
2. The guard HARD-FAILS on a single-reader-dominated V: the S21 state (Jaccard 0.0134 / E1 share 2.4% / E2_only 97.6% `[measured]`) MUST FAIL 6′. Negative fixture (artificially single-reader-dominated V) REFUSED; positive fixture (genuine two-reader V, both shares ≥ 0.20, Jaccard ≥ 0.20) PASSES.
3. E1 and E2 stay genuinely independent (threshold 4 `extraction_methods_distinct` preserved). The Build-Runner fixes the inert E1 by making it read the spec's definition-site prose COMPETENTLY, NOT by tuning it to mimic E2. A 6′ PASS achieved by collapsing E1 into E2 is REFUSED.
4. **Binding 7 boundary:** RP authors the CRITERION (this S22). The Build-Runner (deliverable (b), next dispatch) extends `scripts/spec_extraction_pipeline.py::assert_detector_input` from label-check to composition-check + authors the two fixtures. This is RP spec work reported to kc-53, NOT a Coach-direct gate edit.

**BE-R close-eval becomes PASS-all (8 of 8):** original thresholds 1-5 + threshold 6 superseded-by-6′ + new threshold 7 (freeze-before-count binding) + new threshold 8 (±5%-must-emerge / residual-disclosed). Coach R3 independently re-verifies after the Build-Runner re-run.

**Reality-vs-intent baseline (HR §3.phase11.1-R):** at S21 the denominator is method-unstable (232/354/898 spread `[measured]`) and V is single-reader (E1 share 2.4% `[measured]`); the S22 refinement (a)+(c) is the ROOT fix of both HOLD findings; the Build-Runner re-runs under it. The S21 V FAILS 6′ — the guard working, not a regression.

**HC-11 partition (Binding 8).** The frozen definition + the composition-criterion methodology + the principled floors = PUBLISHABLE. Per-spec V contents + per-spec provenance + the divergence list = PIPELINE-IP-PRIVATE.

<!-- /gate:requirements done_definition_phase11_refinement -->

<!-- amendment_2026_05_30_s22_refinement_end -->
