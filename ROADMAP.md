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

<!-- amendment_2026_05_28a_extension_start -->

## §8 Phase 8 — External grounding (SHIPPED at S9) + Stage 3-4 RP fill (S10 this session) — Done definition extended per SI Amendment 2026-05-28a + 2026-05-28b walk-back of S8 FORMAL CLOSE

<!-- source: dispatch substrate §3.d Cycle-16-S10 RP fill scope — §8 Phase 8 + §9 Phase 9 + §10 Phase 10 -->
<!-- source: SI Amendment 2026-05-28a (Rex paradigm ruling walking back S8 FORMAL CLOSE: "if we move to a new cycle the problem will persist... should we keep it to cycle 16 so we actually solve the fucking problem") + SI Amendment 2026-05-28b (Rex "proceed" directive post-kc-47 self-audit) -->
<!-- source: S8 phase-checkpoint FINDINGS 481L LOCKED at `fb3a0fe` + `25eff54` + `6c80afb` per DP#42 non-destructive supersedure pattern -->
<!-- source: S9 Stage 0-2 RP fill close `d10e32a` (OBSERVATION_LOG §1.recovery + RESEARCH_QUESTION_SPEC §3.recovery + LANDSCAPE_ASSESSMENT §6.recovery; 3 artifacts +206/-0; HC-AUDIT-1 UPSTREAM CONFIRMED with 6 refinements; Cycle 6 KG 235 MATCH CORRECTED IRI; HC #72 sweep CLEAN; R3 PASS-WITH-FLAG+CARRY) -->
<!-- source: S10 Stage 3-4 RP fill (this session) — HR §3.recovery 9 H_recovery rows + 5 KT-7..KT-11 evidence schemata + ED §5.recovery 4 BE-N blocks (BE-F + BE-G + BE-H + BE-I) + REQUIREMENTS Done #11-#19 verbatim + this ROADMAP §8 + §9 + §10 -->
<!-- gate:roadmap §8 phase_8 required -->

**Framing per Amendment 28b.** Cycle 16 stays OPEN. Done definition extended via Done #11-#19. S8 FINDINGS 481L stands as phase-checkpoint Layer 1-5 retrospective per DP#42 non-destructive supersedure; Cycle 16 TRUE close-arc 5-layer FINDINGS at Phase 10 (per §10 below) supersedes via non-destructive supersedure pattern. "Recovery scope" is NOT the dominant frame; "fulfilling SI's research question structurally" / "Done definition extended" / "completion criteria" is.

### §8.1 Phase 8 Status: SHIPPED at S9 + Stage 3-4 RP fill at S10 (this session)

| Sub-phase | Status | Session | Close evidence |
|---|---|---|---|
| **Phase 8.0** — kc-47 audit forensic record at handoff §1dq + kc-47 self-audit §1dr (6 refinements; HC-AUDIT-1 honest carry) | ✓ COMPLETE | Mid-S8→pre-S9 (kc-47 lifecycle close `94befe8` + follow-up `f66714f` + paired `aa9191b`) | Handoff §1dq + §1dr; Moonshots paired commits; HC-AUDIT-1 NEW honest carry; HC #74 BINDING introduced |
| **Phase 8.1** — Stage 0-2 RP fill: OBSERVATION_LOG §1.recovery + RESEARCH_QUESTION_SPEC §3.recovery + LANDSCAPE_ASSESSMENT §6.recovery (10 probe-class disciplines × 30 verbatim quotes) | ✓ SHIPPED | Cycle-16-S9 (close `d10e32a`) | 3 artifacts +206/-0; HC-AUDIT-1 UPSTREAM CONFIRMED with 6 refinements; Cycle 6 KG 235 MATCH CORRECTED IRI named-graph-scoped; HC #72 sweep CLEAN; R3 PASS-WITH-FLAG+CARRY |
| **Phase 8.2** — Stage 3-4 RP fill: HR §3.recovery 9 H_recovery rows + 5 KT-7..KT-11 evidence schemata + ED §5.recovery 4 BE-N blocks (BE-F + BE-G + BE-H + BE-I) + REQUIREMENTS Done #11-#19 verbatim + this ROADMAP §8 + §9 + §10 | ✓ SHIPPED (THIS S10 session; Coach R3 verifies at close) | Cycle-16-S10 (close in-progress) | 4 canonical artifacts ADDITIVELY APPENDED via `<!-- amendment_2026_05_28a_extension_start -->`..`_end -->` markers; LOCKED-body discipline strict per `git diff` zero on pre-marker line ranges; HC #72 substitution-detection self-scan CLEAN at all 4 fill targets |

### §8.2 Phase 8 close criteria — already met at this S10 session close

- 4 canonical artifacts ADDITIVELY APPENDED with HC #72 substitution-detection CLEAN at fill composition.
- LOCKED-body discipline verified: `git diff --stat` zero deletions on pre-marker line ranges for HR / ED / REQUIREMENTS / ROADMAP.
- 0 placeholders across all 4 fill targets.
- 9 H_recovery rows × 9 Done# items (Done #11-#19) full coverage at HR §3.recovery.1.
- 5 KT-7..KT-11 evidence schemata × 5 fields each at HR §3.recovery.2.
- 4 BE-N blocks (BE-F + BE-G + BE-H + BE-I) × 6 PASS-all acceptance thresholds at ED §5.recovery; each threshold probe-fire-evidence grounded per Done #15d; smoke-only fires REFUSED.
- Done #11-#19 verbatim from SI Amendments 28a + 28b at REQUIREMENTS extension; Amendment 28b framing preserved.
- Phase 9 + Phase 10 sequencing + close criteria documented in §9 + §10 below.

**S10 reality-vs-intent diagnostic (per memory binding `feedback_cycle_close_reality_vs_intent_diagnostic.md`).** This S10 RP fill ships RESEARCH-SHAPE acceptance criteria + hypothesis pre-registration, NOT Stage 5 runtime mechanisms. The 4 BE-N blocks (§5.recovery at ED) name what BE-F + BE-G + BE-H + BE-I must ship; they do NOT ship those mechanisms. NO probes yet exist; NO write-boundary enforcement yet exists; NO Substitution Gate yet exists; NO structural-prevention layer yet exists; NO govML v2.8.6 yet exists. Cycle 16 TRUE close-arc happens at Phase 10 (per §10 below) after Phases 9.1-9.4 ship the runtime mechanisms.

<!-- /gate:roadmap §8 phase_8 -->

## §9 Phase 9 — Stage 5 BE-F + BE-G + BE-H + BE-I builds (Cycle-16-S11+ subsequent sessions; dispatched per dispatch substrate §3.d sequencing)

<!-- gate:roadmap §9 phase_9 required -->

### §9.1 Phase 9.1 — BE-F: 4 probe primitives Class A/B/C/D + admission gate (closes Done #13 + H_recovery_3)

**Scope.** Ship 4 code-active probe primitives at `~/ml-governance-templates/scripts/probes/{a,b,c,d}/<primitive_id>.py` per ED §5.7 BE-F PASS-all 6/6 acceptance thresholds. Class A AgentContract = Agent-tool invocation observer keyed by subagent_type (LA §6.recovery.A row 1 Pact + row 4 OTEL + row 8 eBPF uprobe). Class B Schema = property-based check at validation call site (LA §6.recovery.A row 2 + row 9 BX). Class C DesignDecision = ADR-to-code embodiment scanner with `git grep` of must-clauses + LLM-judge component calibrated against known-good/known-bad ADR fixtures (LA §6.recovery.A row 5 Bazel Skyframe + row 9 BX; design-anchor flag re LLM-judge calibration per §6.recovery.C row 3). Class D MethodologyCommitment = citation-and-application scanner with trace_id linkage (LA §6.recovery.A row 4 OTEL + row 10 SLSA). Library admission gate refuses primitives without passing self-test (DP#44 BINDING).

**Sequencing dependencies.** Phase 8 RP fill closed (this S10). Cycle 6 KG substrate-viability primitives operational. govML upstream accessible (Coach handles 3-repo paired commit; Builder-ARCH dispatches 4th-repo govML commit per HC #45 chain extension precedent).

**Expected sessions.** Cycle-16-S11+ (single session minimum; possibly 2 sessions if LLM-judge calibration per Class C requires Builder-ARCH paradigm dispatch).

**Close criteria.** ED §5.7 BE-F PASS-all (6/6 thresholds) at Coach R3 close-eval per kc-49 PD §3.3 T1-T13 mechanical tests. KT-7 + KT-9 + KT-10 evaluated.

### §9.2 Phase 9.2 — BE-G: Write-boundary enforcement + Done #17 cycle-close gate upgrade + Done #18 kill discipline + Done #19 ≤3-session dormancy preservation (closes Done #12 + #17 + #18 + #19 + H_recovery_2 + H_recovery_7 + H_recovery_8 + H_recovery_9)

**Scope.** Ship 4-component composite per ED §5.8 BE-G: (i) pre-commit hook + fsnotify watcher + `forward_apply_emit()` wired into production `register_spec()` + 3-registry reconciliation gate at session close (closing HC-BE-D-1 per kc-47 audit refinement #2 — BE-A 283 events confirm `register_spec()` works WHEN called; bypass unenforced); (ii) Done #17 cycle-close BLOCKING gate predicate UPGRADED from registry-field SPARQL ASK to probe-fire-evidence aggregation invoking named probe primitive via Python subprocess (per kc-47 audit refinement #1: BE-C 8 production-fires confirm prior predicate IS SPARQL ASK on registry-field; upgrade REPLACES predicate body); (iii) Done #18 `kill_spec(spec_iri, adr_retraction_ref, killing_session, kill_reason)` function with ADR retraction validation + `spec_killed_event` emit + SPARQL UPDATE state transition; (iv) Done #19 ≤3-session dormancy threshold preservation on probe-fire evidence (NOT registry-field).

**Sequencing dependencies.** Phase 9.1 BE-F closed (probe primitives must exist for cycle-close gate body to invoke them).

**Expected sessions.** Cycle-16-S12+ (1-2 sessions; composite 4-component scope may require sequential builds).

**Close criteria.** ED §5.8 BE-G PASS-all (6/6 thresholds) at Coach R3 close-eval. KT-7 + KT-8 evaluated.

### §9.3 Phase 9.3 — BE-H: Structural-prevention layer 7 components (closes Done #15a-g + H_recovery_5)

**Scope.** Ship 7 distinct runnable mechanisms at `~/ml-governance-templates/scripts/structural_prevention/` per ED §5.9 BE-H: (a) Stage 0 probe-presence check; (b) reality-vs-intent gate forward to Stage 1+4 R3 close-evals; (c) number-tagging gate at Rex-facing surfaces; (d) probe-coverage check at FINDINGS close; (e) probe library self-test at session close with 2-consecutive-fail auto-deprecate; (f) deferral expiration enforcement; (g) design-anchor disclosure at LANDSCAPE close. Each piece integrates into govML `init_project.sh` install path. Composition pattern PARTIALLY inherits from Cycle 14 four-gate skeleton (substrate-layer per §6.X.2 refined-metric); individual piece predicates externally grounded per LA §6.recovery.A.

**Sequencing dependencies.** Phase 9.1 BE-F closed (probe library required for piece (d) probe-coverage check + piece (e) library self-test gate). Phase 9.2 BE-G closed (write-boundary enforcement required for piece (f) deferral expiration integration).

**Expected sessions.** Cycle-16-S13+ (single session).

**Close criteria.** ED §5.9 BE-H PASS-all (6/6 thresholds) at Coach R3 close-eval. KT-7 + KT-8 + KT-10 evaluated.

### §9.4 Phase 9.4 — BE-I: govML v2.8.6 ADDITIVE-APPEND chain n=5→6 back-port (closes Done #14 + #16 + H_recovery_4 + H_recovery_6)

**Scope.** Back-port probe library (BE-F output) + Operational-Definition Substitution Gate (Done #14 implementation; Substitution Gate as runnable script at Stages 1+4 closes per H_recovery_4) + structural-prevention 7-piece layer (BE-H output) into govML upstream per ED §5.10 BE-I. 3 NEW install functions: `install_probe_library_canonical_vocabulary()` + `install_operational_definition_substitution_gate()` + `install_structural_prevention_layer()`. templates/build/probes/ + templates/build/structural_prevention/ NEW directories. VERSION v2.8.5 → v2.8.6 + CHANGELOG entry. **LOCKED bodies of v2.8.2 + v2.8.3 + v2.8.4 + v2.8.5 install functions UNMODIFIED** per HC #45 ADDITIVE-APPEND precedent class strict (KT-11 firing on any modification → halt for re-do). Freshly-scaffolded build-type projects inherit at scaffolding time.

**Sequencing dependencies.** Phases 9.1 + 9.2 + 9.3 closed. 4-repo paired commit expected (cycle_16 + EMABS + Moonshots + govML) per HC #45 chain extension precedent (Coach handles 3-repo Moonshots+EMABS+cycle_16 paired commit; Builder-ARCH dispatches 4th-repo govML back-port commit). Note: Done #14 Substitution Gate scripts ship at BE-I (govML upstream) since their canonical install path is govML `init_project.sh` install function `install_operational_definition_substitution_gate()`.

**Expected sessions.** Cycle-16-S14+ (single session; 4-repo paired commit).

**Close criteria.** ED §5.10 BE-I PASS-all (6/6 thresholds) at Coach R3 close-eval. KT-11 BINDING strict (LOCKED-body modification = halt for re-do).

### §9.5 Phase 9 aggregate close criteria

- All 4 BE-N close-evals PASS at Coach R3.
- 0 of 5 KT-7..KT-11 fires across BE-F + BE-G + BE-H + BE-I closes (KT-10 firing = H_main_recovery REFUTED candidate → paradigm escalation per HC #74; KT-11 firing = LOCKED-body violation halt for re-do per HC #45).
- HC #50 zero-Rex-escalation baseline MAINTAINED.
- Pattern 19 STANDING density-class discipline applies (cross-system back-port density profile at BE-I).
- Coach R3 independently verifies each BE close per kc-49/50/51 PD §3.3 T1-T13 mechanical tests.

<!-- /gate:roadmap §9 phase_9 -->

## §10 Phase 10 — Probe-grounded retroactive scan re-run + owner triage + TRUE close-arc 5-layer FINDINGS authoring (supersedes S8 phase-checkpoint via DP#42 non-destructive supersedure)

<!-- gate:roadmap §10 phase_10 required -->

### §10.1 Phase 10.1 — Probe-grounded retroactive scan re-run (closes Done #11 + H_recovery_1)

**Scope.** Re-run retroactive scan against the 235 production cycle16:Spec entries (per LA §6.recovery.B P3 named-graph-scoped count) using the 4 probe primitives shipped at BE-F. Replace BE-D heuristic 137 dormant-silent count with per-class measured count + confidence bounds. Per-class probe-fire aggregation across ≥3 distinct production specs per class (NOT smoke fixtures); `run_id` prefix tagged `prod_*`. Per-class confidence bounds (±CI from probe self-test against known-good + known-bad fixtures) reported alongside class skew (Gini concentration coefficient).

**Sequencing dependencies.** Phase 9.1 BE-F closed (4 probe primitives shipped + admission gate operational).

**Acceptance threshold (per H_recovery_1).** Probe-fire-evidence aggregation across ≥3 distinct production specs per class yields {d_A, d_B, d_C, d_D} measured dormant counts; aggregate measured count |d_A + d_B + d_C + d_D - 137| / 137 ≥ 0.10 (forensic discriminator demonstrating measurement is non-degenerate vs heuristic). Substitution-detection countermeasure: rows with `evidence_type: citation_density` / `evidence_type: token_match` / `evidence_type: status_enum_read` REJECTED at aggregation gate.

**Expected sessions.** Cycle-16-S15+ (single session; one-time retroactive fire).

**Close evidence.** `outputs/probe_grounded_retroactive_scan_run.json` (per-class measured counts + confidence bounds + class skew Gini coefficient + comparison to heuristic 137) + `outputs/probes/{a,b,c,d}/*.jsonl` (per-class production probe-fire JSONL logs ≥3 fires per class).

### §10.2 Phase 10.2 — Owner triage for measured-dormant specs

**Scope.** For each measured-dormant spec surfaced at Phase 10.1, owner triage routes to one of 3 dispositions: (a) implement (wire `runtime_emit_event_class` at the spec's intended runtime emit event); (b) defer with named target session + reason + Rex authorization (if past current cycle close) + re-activation condition + maximum dormancy window per Done #15f; (c) kill with ADR retraction via `kill_spec()` per Done #18 (H_recovery_8).

**Sequencing dependencies.** Phase 10.1 retroactive scan re-run complete + measured-dormant spec list populated.

**Expected sessions.** Cycle-16-S15+ (overlapping with Phase 10.1 or sequential).

**Close evidence.** `outputs/owner_triage_dispositions.json` (per-spec disposition + audit trail) + DECISION_LOG entries for kill dispositions (ADR-style retractions) + SPARQL UPDATE events for state transitions to `running` / `dormant-with-explicit-deferral` / `killed`.

### §10.3 Phase 10.3 — Cycle 16 TRUE close-arc 5-layer FINDINGS authoring (supersedes S8 phase-checkpoint via DP#42 non-destructive supersedure)

**Scope.** Author Cycle 16 TRUE close-arc 5-layer FINDINGS per Cycle 11/12/13/14 precedent (480-590-line band). Layer 1 (artifacts shipped per Phases 9.1-9.4 + Phase 10.1+10.2) + Layer 2 (mechanism characterization per H_recovery_1..9 hypothesis resolutions; Done #11-#19 closure verdicts) + Layer 3 (cell granularity per HR §3a Cycle 16 EXTENSION-3 across 4×4×5 = 80 cells; populated subset with PROBE-FIRE evidence now NOT heuristic) + Layer 4 (counterfactual analysis updated post-probe-grounded measurement + KT-7..KT-11 dispositions with evidence + per-discipline boundary-condition map; Cycle 10 RUNTIME_EMIT_SPEC.md counterfactual revisited with probe-fire evidence) + Layer 5 (honest gaps + HC carries forward to Cycles 17-18; reality-vs-intent diagnostic per memory binding `feedback_cycle_close_reality_vs_intent_diagnostic.md`: name what mechanism actually does vs what research question asked; tag numbers measured vs heuristic vs anecdotal).

**Per DP#42 non-destructive supersedure pattern.** S8 phase-checkpoint FINDINGS (481L LOCKED at `fb3a0fe` + `25eff54` + `6c80afb`) is NOT deleted, edited, or rewritten. It stands as historical phase-checkpoint Layer 1-5 retrospective honest about its narrow framing (in-registry dormancy portion only per Rex Option A 2026-05-27). Cycle 16 TRUE close-arc 5-layer FINDINGS is a NEW artifact (file path: `FINDINGS.md` if S8 FINDINGS is renamed to `FINDINGS_S8_phase_checkpoint.md` per Coach disposition; OR `FINDINGS_TRUE_CLOSE.md` if S8 FINDINGS retains canonical name) with supersedure annotation at Layer 0 referencing S8 phase-checkpoint as superseded predecessor.

**Framing discipline mandatory (Amendment 28b).** "Done definition extended" / "completion criteria" / "fulfilling SI's research question structurally" framing throughout. AVOID "recovery scope" as dominant frame.

**Sequencing dependencies.** Phases 10.1 + 10.2 complete. All Done #11-#19 closure evidence available.

**Expected sessions.** Cycle-16-S16+ (single session; close-arc authoring).

**Close evidence.** Cycle 16 TRUE close-arc 5-layer FINDINGS (480-590-line band) + supersedure annotation referencing S8 phase-checkpoint FINDINGS + 11-criterion close-gate ALL_PASS verification (per REQUIREMENTS §Done #11-#19 close gate criteria) + 3-or-4-repo paired commit (4-repo if BE-I govML back-port at Phase 9.4 hasn't already landed; 3-repo if it has).

### §10.4 Phase 10 aggregate close criteria — Cycle 16 TRUE close-arc FORMAL CLOSE

- All 9 H_recovery rows resolved (CONFIRMED / REFUTED / INCONCLUSIVE per HR §3.recovery.1 Resolution Log fill at FINDINGS close).
- All 9 Done #11-#19 items closed in-cycle per REQUIREMENTS §Done Definition Extended close gate criteria.
- 0 of 5 KT-7..KT-11 fires across Phases 9 + 10 (KT-10 firing = H_main_recovery REFUTED → paradigm escalation per HC #74).
- 5-layer FINDINGS authored per Cycle 11/12/13/14 precedent 480-590-line band; supersedes S8 phase-checkpoint via DP#42 non-destructive supersedure.
- Paired commit lands HR + ED + REQUIREMENTS + ROADMAP + FINDINGS + Stage 5 BE-class artifacts atomically (3-or-4-repo per phase 9.4 / phase 10.3 BE-I closing status).
- Coach R3 close-eval mechanical tests ALL_PASS or honest carry surfaced per `feedback_honest_evaluation.md` BINDING.
- HC #50 zero-Rex-escalation baseline MAINTAINED cumulative across kc-43..kc-N lifecycle.
- Honest reality-vs-intent diagnostic at FINDINGS Layer 5 per memory binding `feedback_cycle_close_reality_vs_intent_diagnostic.md`.

**Cycle 16 TRUE close-arc FORMAL CLOSE** = Phase 10 close criteria ALL_PASS. Until then, Cycle 16 stays OPEN per Rex 2026-05-28 paradigm ruling.

<!-- /gate:roadmap §10 phase_10 -->

<!-- amendment_2026_05_28a_extension_end -->

> Cycle 16 Phase 8 + Phase 9 + Phase 10 sequencing per dispatch substrate §3.d. Per `feedback_honest_evaluation.md` BINDING + `feedback_cycle_close_reality_vs_intent_diagnostic.md` BINDING: Coach R3 independent verification at every BE close + close-arc reality-vs-intent diagnostic mandatory at FINDINGS Layer 5; Build-Runner self-report NOT load-bearing. Per HC #74 BINDING cycle-management disposition is paradigm-class: any new-cycle / reopen / fold / close-timing / scope-re-sequencing candidate emerging from Phase 9 or 10 surfaces via Pattern 11 Step 3.5 to Rex — does NOT dispose operationally.

<!-- amendment_2026_05_29_phase11_start -->

## §11 Phase 11 — Denominator honesty (#50) + spec-extraction completeness (#49) + validation-tier close-path verdict (#51) + guard-the-guards (#47) (Cycle-16-S21+ subsequent sessions; per SI Amendment 2026-05-29g (28g) ruling (a))

<!-- source: SI Amendment 2026-05-29g (28g) Done #49/#50/#51 + ruling (a) + sequencing block ("Done #51 binds from S18 detector re-validation onward; Done #49 + #50 are preconditions for the enumeration phase (Phase 11), AFTER S18 makes detectors trustworthy per Done #42 validate-before-remediate") -->
<!-- source: cycle_16_s20_phase11_rp_dispatch_substrate §3.d ROADMAP authoring scope + §0 (Phase 11 FINDS + CERTIFIES; does NOT implement; Phase 12 verify → Phase 13 build/kill/defer) -->
<!-- source: HR §3.phase11 + ED §5.phase11 BE-R/BE-S/BE-T (this same S20 RP fill) -->
<!-- source: handoff §1ee S19 close — execution tier trustworthy; judgment tier CONTESTED -->
<!-- gate:roadmap §11 phase_11 required -->

**Framing.** Phase 11 FINDS and CERTIFIES the spec→implementation gaps; it does NOT implement the missing spec code (that is Phase 12 verify → Phase 13 build/kill/defer). The §10 "Phase 10" close-arc is SUPERSEDED as the close target by the extended Done bar (SI Amendment 28g TRUE-close item (i) = REQUIREMENTS close-gate criterion 12); per DP#42 non-destructive supersedure, §10 is NOT deleted — it stands as the prior close target and its Phase-10.1 probe-grounded retroactive scan re-run now feeds Phase 11 (the trusted detectors it produces are run over the validated set V at BE-T). Per Done #42 validate-before-remediate: Phase 11 lands AFTER S18 made the execution-observable detectors trustworthy (per §1ee); the CONTESTED judgment tier is NOT force-certified.

### §11.1 Phase 11.1 — BE-R: Denominator honesty (#50) + spec-extraction completeness (#49) (closes Done #50 + #49 + H_phase11_50 + H_phase11_49)

**Scope.** (i) Authored-intent scan (Method 2) over sources DISJOINT from Method 1 + `methods_read_disjoint_sources` independence assertion (dual-scan-of-recorded REFUSED) + `authored_but_unrecorded` divergence finding with per-spec provenance + disclosed residual R (never 0). (ii) Second-independent-extraction pipeline (E1 rule-based + E2 different-mechanism) + `extraction_methods_distinct` assertion (single-reader-twice REFUSED) + per-spec/aggregate Jaccard completeness + `E1 △ E2` adjudication ledger + reconciled validated set V (single-reader-as-detector-input REFUSED).

**Sequencing dependencies.** S18 detector re-validation complete (per §1ee — execution tier trustworthy). Within BE-R: denominator (#50) → extraction (#49). BE-R V is a precondition for BE-T's trusted-detector run.

**Acceptance threshold (per H_phase11_50 + H_phase11_49 / ED §5.phase11.1).** PASS-all 6 of 6: dual-scan REFUSED (independence assertion) + divergence with provenance + residual disclosed + distinct-mechanism extraction + measured Jaccard with surfaced symmetric difference + detector input = reconciled V.

**Expected sessions.** Cycle-16-S21+ (1-2 sessions; denominator then extraction).

**Close evidence.** `scripts/authored_intent_scan.py` + `scripts/spec_extraction_pipeline.py` + `outputs/denominator_dual_method.json` + `outputs/extraction_completeness.json` + `outputs/validated_commitment_set.json` + independence-check JSONL + DECISION_LOG `D-S{N}-{M}`.

### §11.2 Phase 11.2 — BE-S: Validation-tier close-path verdict mechanism (#51) (closes Done #51 + H_phase11_51)

**Scope.** Productionize the S19 diverse-agreeing-judge + tier-disclosure machinery (`gt_class_c`/`_status`/`_f_judge` in `probe_accuracy_harness.py`) into a per-spec CLOSE-PATH VERDICT function: execution-checkable → full-rigor verdict; semantically-judged → diverse-agreeing-judge verdict with fail-safe; per-spec tier label in the completion claim; 0 human inputs in the close path (ruling (a)). Does NOT re-build the judges; wires them into the close-path verdict + proves 0-human-in-close-path + emits the tier-labelled claim. Do NOT engineer agreement; do NOT force-certify the CONTESTED judgment tier.

**Sequencing dependencies.** Binds from S18 detector re-validation onward (per Amendment 28g sequencing). Consumes BE-R's validated set V (tier-classifies the specs in V). Its verdicts tier-label the BE-T run.

**Acceptance threshold (per H_phase11_51 / ED §5.phase11.2).** PASS-all 6 of 6: per-spec tier classifier + execution full-rigor-or-honest-LOW-POWER + diverse judges (different model/method) else REFUSED + fail-safe on disagreement (never engineered) + 0 human in close path + tier-labelled claim (uniform "100% validated" REFUSED).

**Expected sessions.** Cycle-16-S22+ (single session; productionizes existing machinery).

**Close evidence.** `scripts/validation_tier_verdict.py` + `outputs/validation_tier_verdicts.json` + `outputs/judge_diversity_check.jsonl` + `outputs/validation_tier_failsafe_events.jsonl` + reference to UNMODIFIED harness `gt_class_*` + `--self-test` + DECISION_LOG `D-S{N}-{M}`.

### §11.3 Phase 11.3 — BE-T: Guard-the-guards (#47) + trusted-detector run over the validated set (closes Done #47; consumes BE-R V + BE-S verdicts)

**Scope.** (i) Fold the enforcement infrastructure itself — probes, gates, agent specs, AND the accuracy harness — INTO the audited population (`is_enforcement_infra: true`); run the trusted detectors over the infra too (the guards audit themselves). (ii) Run the trusted execution-tier detectors over the reconciled validated commitment set V (NOT a single-reader extraction), tier-labelling each verdict per BE-S. The implemented-rate it yields IS the finding (likely large gaps per §1ee — 6/9 AgentContracts with no executable observable, 3/10 KG ontologies with no SHACL shapes); never a number to engineer; the CONTESTED judgment tier is NOT force-certified.

**Sequencing dependencies.** Guard-the-guards folds infra into the denominator BEFORE the detector run. The run consumes BE-R's V + BE-S's tier verdicts. Re-asserts harness `--self-test` `independence_clean==true` before accepting the run.

**Acceptance threshold (per ED §5.phase11.3).** PASS-all 6 of 6: enforcement infra in audited population + detectors fire over infra + detector input = reconciled V (single-reader REFUSED) + per-spec tier-labelled implemented-rate + independence preserved + no un-scoped "100%", gaps disclosed (HC #70).

**Expected sessions.** Cycle-16-S23+ (single session; guard-the-guards then run).

**Close evidence.** `outputs/guard_the_guards_population.json` + `outputs/guard_the_guards_run.jsonl` + `outputs/trusted_detector_run.json` (per-spec tier-labelled rate over V + independence attestation) + DECISION_LOG `D-S{N}-{M}`.

### §11.4 Phase 11 aggregate close criteria — Cycle 16 TRUE-close item (i) (Amendment 28g; REQUIREMENTS close-gate criterion 12)

- All 3 H_phase11 rows resolved (CONFIRMED / REFUTED / INCONCLUSIVE per HR §3.phase11 Resolution Log fill at FINDINGS close).
- Done #50 + #49 + #51 + #47 closed in-cycle per REQUIREMENTS §Done #47/#49/#50/#51 acceptance criteria.
- Denominator dual-method with `methods_read_disjoint_sources==True` + `authored_but_unrecorded` surfaced + residual R disclosed (never 0).
- Extraction completeness measured (Jaccard) + detectors run on reconciled V (single-reader REFUSED).
- Validation-tier verdict per-spec tier-labelled + diverse-agreeing judges + fail-safe + 0 human in close path; uniform "100% validated" REFUSED.
- Guard-the-guards: enforcement infra folded into the audited population + detectors fire over it + independence re-asserted.
- The close "100%" claim is TWO-TIER + RESIDUAL-DISCLOSED; a bare/uniform "100%" is REFUSED.
- Honest reality-vs-intent diagnostic at FINDINGS Layer 5 per `feedback_cycle_close_reality_vs_intent_diagnostic.md`; large implemented-rate gaps disclosed (HC #70), never engineered.

### §11.5 Route forward — Phase 12 (100% probe-fire verification) → Phase 13 (build/kill/defer)

Phase 11 certifies the spec→implementation gaps against a trusted denominator + validated commitment set + tier-disclosed verdicts. It does NOT implement the missing spec code. Route forward:

- **Phase 12 — 100% probe-fire verification.** Verify every spec in the discoverable population (recorded ∪ authored-intent) has a probe-fire verdict (implemented / not-implemented / contested) over the validated set V, tier-labelled; 100% coverage of the discoverable population with residual R disclosed (NOT a bare 100%).
- **Phase 13 — build / kill / defer the missing code.** For each certified gap: implement (wire the missing runtime observable) / kill (ADR retraction via `kill_spec()` per Done #18) / defer (named target session + reason + Rex authorization + re-activation condition + maximum dormancy window per Done #15f). This is where the missing spec code is actually built — NOT Phase 11.

**Cycle 16 TRUE-close** = REQUIREMENTS close-gate criteria 1-11 (Amendments 28a/28b/28e/28f) AND criterion 12 (Amendment 28g item (i)) ALL_PASS. Until then, Cycle 16 stays OPEN per Rex 2026-05-28 + 2026-05-29 paradigm rulings. Per HC #74 BINDING cycle-management disposition is paradigm-class: any new-cycle / reopen / fold / close-timing candidate emerging from Phase 11/12/13 surfaces via Pattern 11 Step 3.5 to Rex — does NOT dispose operationally.

<!-- /gate:roadmap §11 phase_11 -->

<!-- amendment_2026_05_29_phase11_end -->
