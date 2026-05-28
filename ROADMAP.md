# Roadmap: Cycle 16 — Close the spec-to-implementation gap

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- stage: 4 -->
<!-- source: Cycle 16 SI ACTIVE 2026-05-27 + Amendment 2026-05-27a (deadline-tightening) + Amendment 2026-05-27b (KG-primary registry storage) + substrate §7 ROADMAP scope + Cycle 14 multi-BE precedent -->
<!-- gate:roadmap phases:5 -->

> Authored by RP at Stage 4 (Dispatch 2). Stage 5 BE-class sessions dispatched by build-orchestrator per Cycle 14 multi-deliverable precedent. Per-phase acceptance + KT-N threshold encoded; Coach R3 close-eval at each BE close-eval.

## §0 Phase Overview + Authority Chain

5 phases mapped to Cycle 16 SI Branches 1-4 + close-arc:

| Phase | Scope | Branches | Sessions | Done-criteria reference |
|---|---|---|---|---|
| Phase 0 (closed) | Stage 0-2 RP scaffold + fill | n/a | Cycle-16-S1 (closed 2026-05-27) | Cycle-16-S1 close `9300c86` |
| Phase 1 (THIS) | Stage 3-4 RP fill + LA §6 addendum | All 4 branches design | Cycle-16-S2 | This dispatch |
| Phase 2 | Stage 5 BE-A schema/SPARQL write-boundary | Branch 4.1 | ~1 BE session | Done #5 |
| Phase 3 | Stage 5 BE-B authoring discipline + DP#26 carve-out | Branch 4.2 | ~1 BE session | Done #6 + H7 + KT-3 |
| Phase 4 | Stage 5 BE-C TWO-surface gate | Branch 4.3 | ~1 BE session | Done #7 + H6 + KT-4 |
| Phase 5 | Stage 5 BE-D retroactive scan | Branch 4.4 | ~1 BE session | Done #1 + #8 + H1 + H3 + KT-2 |
| Phase 6 | Stage 5 BE-E forward-apply instrumentation | Branch 4.5 | ~0.5 BE session | Done #9 + H8 + KT-5 |
| Phase 7 (close-arc) | FINDINGS authoring + paired commit | n/a | ~1-2 close session(s) | Done #2 + #10 |

Total Cycle 16 sessions estimate: 6-7 within the ≤6-session envelope per disposed paradigm question #1 (with Phase 7 close session as the 7th if scope-discipline-bounded slip is required and Rex authorizes).

## §1 Phase 2 — Stage 5 BE-A: KG-primary 14-field schema + SPARQL write-boundary

<!-- gate:roadmap phase_2 BE_A required -->

### §1.1 Tasks

1. **Author `docs/spec_registry_schema.ttl`** — TTL serialization of 14-field schema per Cycle 6 BE#1 contract: `spec_id` IRI (UUID v7 or canonical hash) + `rdf:type cycle16:Spec` + `spec_type` ∈ {AgentContract, Schema, DesignDecision, MethodologyCommitment} + `owner` + `acceptance_criteria` + `target_session` + `current_status` ∈ {running, dormant-with-explicit-deferral, dormant-silent, killed, long-running} + `cycle_authored` + `session_authored` + `cycle_implemented` + `session_implemented` (nullable) + `runtime_emit_event_class` + `dormancy_detection_threshold_sessions` (default 3) + `deferral_reason` (nullable; required if status=dormant-with-explicit-deferral) + `rex_authorization_for_deferral_past_cycle_close` (nullable; required if target_session > cycle_authored close) + `audit_trail_link` (PROV-O typed-edge target). PROV-O 4 typed-edges materialized at write: `prov:wasGeneratedBy` (the spec-authoring session) + `prov:wasAttributedTo` (the owner) + `prov:generatedAtTime` (session timestamp) + `prov:wasInformedBy` (upstream spec or paradigm disposition).
2. **Author per-edge HC-11 access-permission enum** — annotate every materialized edge with `cycle6:hcAccessPermission` ∈ {publishable, ip-private, ephemeral} per Cycle 6 BE#1 contract (11,223 ip-private + 1 publishable + 1 ephemeral usages observed at 2026-05-27 Coach probe; pattern operational).
3. **Author Wikidata supersedure predicates** — `wikibase:rank` (preferred / normal / deprecated) + `prov:wasRevisionOf` (predicate linking superseded spec). **HC-RP-S2-3 binding:** if absent at Cycle 6 BE#1 ground state at Stage 5 BE-A entry, author here at schema extension and surface to Coach for verification against Cycle 6 BE#1 contract upstream extension OR FINDINGS Layer 4 honest gap.
4. **Author nanopublication 3-graph pattern** — for every `cycle16:Spec` instance, materialize 3 named graphs at `/cycle6` endpoint: `<spec_iri>:assertion` + `<spec_iri>:provenance` + `<spec_iri>:publicationInfo` (per Cycle 6 BE#1 contract; 46-graph operational at 2026-05-27 probe).
5. **SPARQL UPDATE write-boundary spec** — author body of the SPARQL UPDATE INSERT DATA query that the spec-authoring-discipline gate body (Phase 3 BE-B) will use; smoke-test against `/cycle6` endpoint with synthetic test spec.

### §1.2 Dependencies

- Phase 1 (this RP fill) closed at R3 PASS.
- Cycle 6 KG substrate-viability primitives operational per Coach probe 2026-05-27 (verified at LA §6 addendum).
- govML scaffold lock_commit `efaf6ae6` (captured at Cycle-16-S1 scaffold per `governance.yaml`).

### §1.3 Verification

- `curl http://localhost:3030/cycle6/sparql --data-urlencode 'query=ASK { ?spec a cycle16:Spec }'` returns TRUE for ≥1 test spec materialized end-to-end.
- 14-field schema introspection via SPARQL DESCRIBE returns all 14 predicates per test spec.
- HC-RP-S2-3 disposition surfaced to Coach: Wikidata predicates present (cleanly) OR carried as honest gap to FINDINGS Layer 4.

## §2 Phase 3 — Stage 5 BE-B: Spec-authoring discipline + DP#26 carve-out

### §2.1 Tasks

1. **Author `docs/spec_authoring_discipline.md`** — define the gate body executed at spec-authoring boundary: SPARQL UPDATE INSERT DATA against `/cycle6` endpoint per the 14-field schema; BLOCKING discipline rejects if any non-nullable field absent.
2. **Author DP#26 carve-out spec** — methodology commitments at Layer-5 may take `runtime_emit_event_class = 'n/a — citation-based activation per DP#26'` with documented rationale; carve-out reviewed at Coach R3 per DP#26 BINDING.
3. **Wire authoring-discipline into scaffold + RP/Coach/Builder workflows** — `scripts/spec_authoring_check.sh` invoked at session-init for any session authoring a spec; emits to `outputs/build_runner_events.jsonl` per Cycle 10 RUNTIME_EMIT_SPEC.md inheritance.
4. **Forward-apply during Cycle 16 itself** — every new spec authored at Phases 2-7 (this ROADMAP) must pass authoring-discipline gate; refusals tracked as KT-3 firing surface (per H7).

### §2.2 Dependencies

- Phase 2 BE-A complete (`/cycle6` endpoint with 14-field schema operational).
- DP#26 BINDING + DP#43 BINDING + DP#44 BINDING all UNMODIFIED at this S2.

### §2.3 Verification

- Forward-apply dogfooding: ≥4 specs authored at Phases 2-7 (the registry schema itself + Phase 3 authoring discipline spec + Phase 4 gate spec + Phase 5 retroactive scan spec + Phase 6 instrumentation spec) all pass authoring-discipline gate cleanly = H7 CONFIRMED.
- KT-3 firing surface: n=3+ author rejections during Cycle 16 → registry refinement OR same-cycle default relaxation.

## §3 Phase 4 — Stage 5 BE-C: TWO-surface BLOCKING gate

### §3.1 Tasks

1. **Author `scripts/spec_implementation_present_gate.sh`** — cycle-close surface; mirrors `k_register_present_gate.sh` skeleton (Cycle 14 four-gate pattern); predicate body = SPARQL ASK against `/cycle6`: `ASK { ?spec a cycle16:Spec . ?spec cycle16:registry_row_exists true . ?spec cycle16:target_session ?ts . ?spec cycle16:runtime_emit_event_class ?ec . FILTER (?spec.current_status IN (cycle16:running, cycle16:dormant-with-explicit-deferral, cycle16:killed, cycle16:long-running) OR (?spec.session_authored + ?spec.dormancy_threshold ≥ current_session)) }`.
2. **Author `scripts/spec_implementation_session_close_gate.sh`** — session-close surface; same skeleton; predicate body specifically scans for `current_status = 'dormant-silent'` rows where `(current_session - session_authored) ≥ dormancy_detection_threshold_sessions`.
3. **Wire both gates into `check_all_gates.sh`** — at cycle-close (single fire) + at session-close (each session); BLOCKING by default with `--advisory-mode` opt-in WARN flag per Cycle 14 four-gate precedent.
4. **H6 + KT-4 evaluation** — assess at BE-C close whether predicate extension is clean (gate-script skeleton hosts SPARQL ASK without primitive-class extension) OR requires new enforcement primitive class (KT-4 fires).

### §3.2 Dependencies

- Phase 2 BE-A complete.
- Phase 3 BE-B complete.

### §3.3 Verification

- Both gate scripts present at canonical path with bash shebang + DP#44-compliant refuse-on-missing-precondition behavior.
- BE-C close-eval: run gate scripts against `/cycle6` with synthetic test specs covering all 5 states → expected BLOCKING fires on `dormant-silent` test fixture; expected PASS fires on `running` + `dormant-with-explicit-deferral` + `killed` + `long-running` test fixtures.
- H6 CONFIRMED if gate-script skeleton mirrors `k_register_present_gate.sh` cleanly without primitive-class extension; KT-4 fires otherwise.

## §4 Phase 5 — Stage 5 BE-D: Retroactive scan against Cycles 1-15

### §4.1 Tasks

1. **Enumerate 4 spec-classes across Cycles 1-15:** (a) agent contracts via `ls ~/Moonshots_Career_Thesis_v2/.claude/agents/*.md` direct (NOT `git ls-files` per HC #52 broader scope per OBS-2; 6-of-9 gitignored); (b) schemas via `find ~/cycle_*/scripts/runtime_emit/ -name '*.json' -o -name '*.py'` + drift_telemetry_signal_schema.json class enumeration; (c) design decisions via DECISION_LOG.md across all 15 cycle directories + paradigm-disposition records; (d) methodology commitments via FINDINGS.md Layer-5 sections across all 15 cycle directories.
2. **Classify each spec per 5-state taxonomy** — running / dormant-with-explicit-deferral / dormant-silent / killed / long-running. Classification heuristic: search for `runtime_emit_event_class` runtime emit firing evidence in `outputs/*_events.jsonl` OR cite at downstream session warmup OR retraction ADR.
3. **Materialize per-spec rows at `/cycle6` endpoint** via SPARQL UPDATE INSERT DATA + retroactive `cycle_authored` + `session_authored` assignment.
4. **Emit `outputs/retroactive_scan_cycle_1_15_run.json`** with aggregate counts per spec-class × per-state.
5. **KT-2 evaluation:** `current_status = 'dormant-silent'` aggregate count. If <3, KT-2 FIRES → halt + Rex paradigm re-disposition. If ≥3, H3 CONFIRMED + per-spec owner-triage workflow surfaces.
6. **H1 evaluation:** total enumerated spec count vs N≈90-100 estimate per RQS §3a; CONFIRMED if total ≥ estimate floor.

### §4.2 Dependencies

- Phase 2 BE-A complete (schema operational at `/cycle6`).
- Phase 3 BE-B complete (authoring-discipline gate retroactively bypassed for Cycles 1-15 with explicit `retroactive_classification = true` annotation per audit trail).

### §4.3 Verification

- Aggregate query: `SELECT (COUNT(*) AS ?n) ?spec_type ?current_status WHERE { ?spec a cycle16:Spec ; cycle16:spec_type ?spec_type ; cycle16:current_status ?current_status } GROUP BY ?spec_type ?current_status` returns 4×5 = 20-cell breakdown.
- DP#43 spot-read at BE-D close-eval: ≥3 dormant-silent specs identified with verbatim citation surface (per-spec evidence link to cycle directory + session-authored + missing runtime emit event class firing record).

## §5 Phase 6 — Stage 5 BE-E: Forward-apply instrumentation

### §5.1 Tasks

1. **Wire spec_authoring_event + spec_implementation_event classes** into `scripts/runtime_emit/emit.py` + `outputs/build_runner_events.jsonl` sink per Cycle 10 RUNTIME_EMIT_SPEC.md inheritance.
2. **Author `docs/forward_apply_observation_protocol.md`** — define observation surface across Cycles 17-18: session-close gate fires at every session close; aggregate query at each cycle close; longitudinal verdict at Cycle 18 close.
3. **Smoke-test forward-apply** — emit 1 synthetic spec_authoring_event + 1 synthetic spec_implementation_event during Phase 6 BE-E session; verify JSONL sink received both events with PROV-O typed-edges.
4. **KT-5 evaluation surface enabled** — H_main REFUTED if ≥2 NEW dormant-silent specs accumulate mid-Cycle-16 OR across Cycles 17-18.

### §5.2 Dependencies

- Phases 2-5 complete.
- Cycle 10 runtime_emit infrastructure operational (verified at Cycle-16-S1 scaffold).

### §5.3 Verification

- `tail outputs/build_runner_events.jsonl` shows synthetic events with all PROV-O typed-edges + HC-11 access-permission enum.
- Forward-apply observation enabled at Cycle 16 close; Cycles 17 + 18 session-close gates fire on registry state.

## §6 Phase 7 — Close-arc: FINDINGS authoring + paired commit

### §6.1 Tasks

1. **Synthesize FINDINGS.md Layer 1** (artifacts shipped per deliverables 1-9 at REQUIREMENTS).
2. **FINDINGS Layer 2** — mechanism characterization per H1-H8 hypothesis resolutions; cross-reference HR §4 Resolution Log.
3. **FINDINGS Layer 3** — cell granularity per HR §3a Cycle 16 EXTENSION-3 across 4×4×5 = 80 cells; empirically populated subset reported.
4. **FINDINGS Layer 4** — Cycle 10 counterfactual analysis (H4); KT-1..KT-6 dispositions with evidence; per-discipline boundary-condition map.
5. **FINDINGS Layer 5** — honest gaps: HC-RP-S2-3 Wikidata supersedure forward dependency + HC-RP-S2-4 Cycle 7 substrate-viability forward dependency + any new HC discovered Phase 2-6 + forward-cycle carries to Cycles 17-18.
6. **Paired commit** — HR §4 Resolution Log filled + ED §5+ Stage 5 fill (Build-Runner authored across Phases 2-6) + this ROADMAP §7 closure annotation + FINDINGS.md + paired-commit binding per Discipline #11.
7. **Coach R3 close-eval** — mechanical tests T1-T13 + DP#43 spot-read across FINDINGS layers; close-disposition emitted.

### §6.2 Verification

- 5-layer FINDINGS present per Cycle 14 multi-layer precedent.
- All 10 done-criteria addressed (CONFIRMED / REFUTED / INCONCLUSIVE per HR §4).
- Paired commit lands HR + ED + PROJECT + REQUIREMENTS + ROADMAP + FINDINGS + LA §6 addendum + Stage 5 BE-class artifacts atomically.

## §7 Estimated Source Plan

| Source | Type | Access Method | Priority |
|---|---|---|---|
| Cycle 6 BE#1 contract + schema docs at `~/cycle_6_unified_substrate_build/docs/` | Internal spec | Read | HIGH |
| Apache Jena Fuseki `/cycle6` endpoint (localhost:3030) | KG substrate | curl SPARQL UPDATE/ASK | HIGH |
| `~/cycle_10_autonomous_cycle_apparatus_build/scripts/runtime_emit/` + drift_telemetry_signal_schema.json | Runtime emit infra | Read + reference | HIGH |
| `~/ml-governance-templates/scripts/k_register_present_gate.sh` (Cycle 14 skeleton) | Gate-script template | Read + adapt | HIGH |
| `~/Moonshots_Career_Thesis_v2/.claude/agents/*.md` (9 agent specs) | Retroactive scan input | ls direct | HIGH |
| `~/cycle_*/FINDINGS.md` Layer-5 sections (Cycles 1-15) | Methodology commitments | Read | MEDIUM |
| `~/cycle_*/DECISION_LOG.md` (Cycles 1-15) | Design decisions | Read | MEDIUM |
| `singularity.db` v_observation_inputs + v_question_inputs + v_landscape_inputs | Cross-engine DB | sqlite3 query | LOW (S1 close) |

## §8 Risk Register

| Risk | Probability | Mitigation |
|---|---|---|
| Cycle 6 KG substrate-viability shift mid-Cycle-16 (Cycle 7 vendor pivot lands during Phases 2-6) | LOW (Cycle 7 OPEN; not closed within Cycle 16 envelope) | HC-RP-S2-4 explicit carry; vendor-portable abstraction layer above Fuseki-specific SPARQL if Cycle 7 surfaces pivot |
| Wikidata supersedure predicates not addable cleanly at Stage 5 BE-A | MEDIUM (HC-RP-S2-3 PARTIAL at 2026-05-27 probe) | ED §4a constraint #4 binds Stage 5 BE#1 schema extension OR FINDINGS Layer 4 honest gap |
| KT-2 fires at retroactive scan (<3 dormant-silent) | LOW (Cycle 10 case is canonical 1-of-3; OBS-2 6-of-9 gitignored agent specs surface ≥2-3 additional candidates) | Halt + Rex paradigm re-disposition per substrate §4 KT-2 disposition row |
| KT-3 fires at forward-apply dogfooding (n=3+ author refusals mid-cycle) | MEDIUM (registry-row-required is heavyweight at per-session cadence) | Registry refinement OR same-cycle default relaxation per substrate §4 KT-3 disposition row |
| KT-4 fires at predicate extension (Cycle 14 skeleton requires new primitive class) | LOW (preliminary disposition at LA §6b.2: predicate extends cleanly via SPARQL ASK substitution) | New enforcement primitive class warranted; surface as paradigm-class scope expansion candidate OR proceed within cycle if scope still bounded |
| KT-5 fires (≥2 NEW dormant-silent specs mid-Cycle-16 OR Cycles 17-18) | LOW initially; MEDIUM longitudinal (forward-apply observation enabled at Cycle 16 close) | H_main REFUTED; paradigm escalation to RQS §4.1 Alternative 2 (specs ARE code) candidate |
| KT-6 fires (Cycle 6 substrate-viability blocker) | LOW (Coach probe 2026-05-27 confirmed 246K quads + ≤0.5s latency + PROV-O + HC-11 + nanopub operational) | Fall back to SQL/YAML per pre-Amendment-27b binary framing + Step 3.5 escalation gate |
| Cycle 16 envelope ≤6 sessions exceeded | LOW (5-7 sessions estimated; close session may slip to 7th) | Rex authorization required for past-envelope slip per disposed paradigm question #1 |

## §9 Close Definition

Cycle 16 closes when:

- All 10 done-criteria (per REQUIREMENTS §Deliverables 1-10) addressed: CONFIRMED / REFUTED / INCONCLUSIVE per HR §4 Resolution Log + FINDINGS Layer 4.
- OR KT-1..KT-6 disposition fires with halt + Rex paradigm re-disposition surface (KT-1 narrows scope; KT-2 + KT-6 halts; KT-3..KT-5 surfaces honest gap + paradigm escalation candidate).
- Paired commit of HR + ED + PROJECT + REQUIREMENTS + ROADMAP + FINDINGS + LA §6 addendum + Stage 5 BE-class artifacts lands atomically.
- Coach R3 close-eval mechanical tests T1-T13 ALL PASS or honest carry surfaced per `feedback_honest_evaluation.md` BINDING.

> Forward-apply observation across Cycles 17-18 begins at Cycle 16 close; longitudinal verdict at Cycle 18 close (per done-criterion #10).

---

## §7 Close-arc Annotation (Cycle-16-S8 close FINDINGS authoring; Build-Runner fill per kc-46 PD §3.3 + REQUIREMENTS §Verification Surfaces + substrate §3 OUTPUT #4)

<!-- source: Cycle-16-S8 close-arc per dispatch substrate §3 OUTPUT #4 + DECISION_LOG D-S3-1..D-S7-1 + FINDINGS §2 Done Definition outcome table -->
<!-- gate:roadmap phase_7 closure_annotation required -->

### §7.1 Phase 0-7 Final Status (per Cycle 16 SI ACTIVE 2026-05-27 + Amendments 27a + 27b)

| Phase | Status | Session | Close evidence |
|---|---|---|---|
| **Phase 0** (Stage 0-2 RP scaffold + fill) | ✓ CLOSED | Cycle-16-S1 | `9300c86`; OBS 260L + RQS 498L + LA 565L; 36 verbatim quotes / 7 disciplines; T1-T8 ALL PASS at S1 R3 |
| **Phase 1** (Stage 3-4 RP fill + LA §6 addendum) | ✓ CLOSED | Cycle-16-S2 | 5 canonicals at project root 0 placeholders (HR 148L + ED 576L + PROJECT 79L + REQUIREMENTS 101L + ROADMAP 184L) + LA §6 addendum +47L surgical GPL-41 append; Rex paradigm-ruling D-S2-1 disposition (C); T1-T13 ALL PASS at S2 R3 |
| **Phase 2** (Stage 5 BE-A schema + SPARQL write-boundary) | ✓ CLOSED | Cycle-16-S3 | 13 artifacts + 3-TB SPARQL UPDATE smoke ALL_PASS at PROD /cycle6; HC-RP-S2-3 RESOLVED via Path α; H6+H7 CONFIRMATION CANDIDATES; KT-4+KT-6 DO NOT FIRE; DECISION_LOG D-S3-1 |
| **Phase 3** (Stage 5 BE-B authoring discipline + DP#26 carve-out + govML v2.8.3) | ✓ CLOSED | Cycle-16-S4 | 11+ artifacts + 3-TB dogfooding to PROD /cycle6 ALL_PASS; KT-3 DOES NOT FIRE; **Done #6 SHIPPED**; HC #45 ADDITIVE-APPEND chain n=3; DECISION_LOG D-S4-1 |
| **Phase 4** (Stage 5 BE-C TWO-surface BLOCKING gate + govML v2.8.4) | ✓ CLOSED | Cycle-16-S5 | 11+ artifacts + 3-TB dogfooding all_3_pass=true; **H6 CONFIRMED** with HC-BE-C-1 op carry; **KT-4 DOES NOT FIRE**; HC #45 chain n=4; DECISION_LOG D-S5-1 |
| **Phase 5** (Stage 5 BE-D retroactive scan + 5-state classification) | ✓ CLOSED | Cycle-16-S6 | 10 deliverables + 232 distinct cycle16:Spec at PROD /cycle6; **H1 + H3 CONFIRMED**; **KT-2 DOES NOT FIRE** (137 >> 3; 45x); **HC-BE-D-1 SURFACED** → Cycle 18 scope per Rex Option B; 3-repo paired commit NO govML; DECISION_LOG D-S6-1 |
| **Phase 6** (Stage 5 BE-E forward-apply observation + govML v2.8.5) | ✓ CLOSED | Cycle-16-S7 | 8 deliverables + 4 smoke-test fire.event rows at /cycle6 test graph; **H8 evaluation surface ENABLED** (FINAL VERDICT DEFERRED to Cycle 18); **KT-5 DOES NOT FIRE** count=0 IRI-prefix discriminator; HC-BE-D-1 PRESERVED at BE-E; HC #45 chain n=5 (4-install_hook chain at govML v2.8.5); 4-repo paired commit; DECISION_LOG D-S7-1 |
| **Phase 7** (Close-arc FINDINGS authoring + paired commit) | ✓ CLOSED at S8 (THIS) | Cycle-16-S8 | 5-layer FINDINGS.md NEW at project root + HR §4 Resolution Log fill (8H + 6KT) + ED §5+ Stage 5 acceptance fill (5 BE rows) + this ROADMAP §7 closure annotation + state.json transition + 3-repo paired commit (cycle_16 + EMABS + Moonshots; NO govML per close-arc precedent Cycle 11/12/13/14) |

### §7.2 Done Definition #1-#10 Final Status (per REQUIREMENTS §Deliverables 1-10 + FINDINGS §2)

| # | Done criterion | Status | Closing session | Evidence pointer |
|---|---|---|---|---|
| **#1** | Spec inventory (Cycle 1-15 retroactive scan) — 4-spec-class enumeration via KG materialization | ✓ CLOSED | S6 BE-D | `outputs/retroactive_scan_cycle_1_15_run.json` 232 distinct + per-class 9a + 10b + 154c + 59d |
| **#2** | Pattern analysis — Cycle 10 counterfactual + 4-class operational definitions | ✓ CLOSED | S8 (THIS) | FINDINGS Layer 4 §7.2 item (ix) H4 counterfactual reasoning chain + HR §3c per-class rows |
| **#3** | Substrate audit — LA §6 addendum with KT-1 + KT-6 dispositions | ✓ CLOSED | S2 | LA §6.X.1+§6.X.2+§6.X.3 + DECISION_LOG D-S2-1 paradigm-ruling entry |
| **#4** | External research — 7 disciplines × ≥3 verbatim quotes (LA §1 LOCKED at S1) | ✓ CLOSED | S1 (preserved through S8) | LA §1 rows 1-7 (IETF / PEP / OpenAPI / DbC / feature-flag governance / ADR / Parnas); 36 quotes ≥30 floor per HC #43 |
| **#5** | KG-primary 14-field registry schema — TTL + SHACL + materialization at /cycle6 | ✓ CLOSED | S3 BE-A | `docs/spec_registry_schema.ttl` + `spec_registry_shapes.shacl.ttl` + 3-TB smoke ALL_PASS + Path α HC-RP-S2-3 RESOLVED |
| **#6** | SPARQL UPDATE authoring discipline + DP#26 carve-out + scripts/spec_registry_authoring.py | ✓ CLOSED | S4 BE-B | `scripts/spec_registry_authoring.py` 29.8KB + 3-TB dogfooding all_3_pass=true + KT-3 DOES NOT FIRE; govML v2.8.3 ADDITIVE-APPEND |
| **#7** | TWO-surface BLOCKING gate — cycle-close + session-close gate scripts | ✓ CLOSED | S5 BE-C | 2 NEW gate scripts at govML scripts/ + 3-TB dogfooding all_3_pass=true + H6 CONFIRMED with HC-BE-C-1 op carry + KT-4 DOES NOT FIRE; govML v2.8.4 ADDITIVE-APPEND |
| **#8** | Retroactive scan fires (≥3 dormant-silent surfaces else KT-2) | ✓ CLOSED | S6 BE-D | 137 dormant-silent >> 3 floor (45x); KT-2 DOES NOT FIRE; per-class breakdown 7a+2b+117c+11d |
| **#9** | Forward-apply observation enabled — runtime emit instrumentation Cycle 17-18 ready | ✓ CLOSED | S7 BE-E | 2 NEW event classes wired into emit.py ADDITIVELY (Cycle 10 schema_version=0.1 LOCKED); 4 smoke-test events at `outputs/forward_apply_observation_events.jsonl`; KT-5 DOES NOT FIRE count=0; govML v2.8.5 ADDITIVE-APPEND chain n=5 |
| **#10** | 5-layer close FINDINGS + paired commit + H8 longitudinal verdict | **PARTIAL at S8** (5-layer FINDINGS + paired commit CLOSED THIS S8; **H8 longitudinal final verdict DEFERRED to Cycle 18 close** per HR §3 H8 design; ≥2-cycle window per Amendment 27a) | S8 (5-layer + paired commit); Cycle 18 close (H8 longitudinal) | this FINDINGS + S8 paired commit + state.json transition + H8 OPEN forward Cycle 18 |

### §7.3 Close-arc Completion Annotation

**Cycle 16 closes with 9 of 10 SI Done Definition items CLOSED in-cycle at S8; Item #10 partial (5-layer FINDINGS + paired commit CLOSED THIS S8; H8 longitudinal final verdict DEFERRED to Cycle 18 close per HR §3 H8 design).** Item #10 deferral is by design, not a gap — H8 requires ≥2-cycle longitudinal window per kc-44 PD Amendment 27a deadline-tightening (Cycles 17 + 18 forward-apply post-Cycle-16 close).

**KT firing aggregate at Cycle 16 close: 0 of 6 KT triggers fire** (KT-1 + KT-2 + KT-3 + KT-4 + KT-5 + KT-6 ALL DOES NOT FIRE per per-BE evidence + HC #59 BINDING screen at KT-1 + KT-2 + KT-5).

**Hypothesis resolutions at Cycle 16 close:** H1 + H3 + H6 + H7 + H4 (counterfactual) CONFIRMED; H2 + H5 CONFIRMED-WITH-CAVEAT (H5 under refined metric per D-S2-1); H8 OPEN forward Cycle 18 by design.

**Honest carries forward Cycle 17/18+:** HC-BE-D-1 PRESERVED → Cycle 18 scope per Rex Option B split-sequential 2026-05-27 (write-boundary enforcement gap closure with filesystem-scan + spec-class-discriminator + work-host-routing gate primitive class — different than what Cycle 16 ships); HC-BE-E-1 NEW documentation-only Layer 4 surface (BE-D §12 doc-vs-implementation discriminator gap; future-cycle BE-D §12 amendment candidate); HC-BE-A-3 STANDING (docs/ scaffolding-path divergence); HC #55 + HC #56 + HC #63 + HC #64 STANDING from S1 carry. HC #50 zero-Rex-escalation baseline MAINTAINED cumulative kc-45+46 across 10 close-eval rounds.

**Framing discipline mandatory (Rex Option A 2026-05-27 BINDING per `feedback_honest_evaluation.md`):** Cycle 16 closes the **"in-registry dormancy portion"** of the spec-implementation gap — NOT "spec-to-implementation gap closure" unqualified. **Cycle 17 inherits in-registry mechanism as DEFAULT via govML rail HC #45 ADDITIVE-APPEND chain n=5** (v2.8.5 ADDITIVE; existing 3 install_hooks LOCKED). **Cycle 18 absorbs HC-BE-D-1 write-boundary enforcement gap closure** per Rex Option B split-sequential 2026-05-27.

<!-- /gate:roadmap phase_7 closure_annotation -->

> Cycle 16 close-arc complete at Cycle-16-S8. Per `feedback_honest_evaluation.md` BINDING: Coach R3 independent verification at S8 close-eval; Build-Runner self-report NOT load-bearing. Per Pattern 14 STANDING: close summary direct to Rex in executive format ≤200 words fires post-commit. Per Pattern 9 BINDING: kc-47 PD authoring at kc-46 terminal close fires AFTER this S8 commit as Moonshots-paired follow-up (out-of-scope this S8 Coach per kc-46 PD §6.3).
