# BUILD DECISION LOG

<!-- version: 0.1 -->
<!-- created: 2026-05-27 -->
<!-- profile: build -->
<!-- methodology_status: BE-A authored — Cycle 16 Stage 5 BE-A decision log with §1.4 architectural-choice subsection (Path α inheritance choice per substrate §3) -->
<!-- source: ARTIFACT_CONTRACT §6 change control + ACCEPTANCE_CRITERIA §4 failure-shape grid + DEPLOYMENT_LOG §5 promotion-FAIL diagnostic + dispatch substrate §3 Wikidata supersedure Path α/β/γ decision space -->

> **Authority Hierarchy**
>
> | Priority | Document | Role |
> |----------|----------|------|
> | Tier 1 | Cycle 16 SI ACTIVE 2026-05-27 + Amendments 27a/27b | Primary spec — highest authority |
> | Tier 2 | ARTIFACT_CONTRACT.md §6 change control triggers + ACCEPTANCE_CRITERIA.md §4 failure-shape grid + DEPLOYMENT_LOG.md §5 promotion-FAIL diagnostic | Clarifications — cannot override Tier 1 |
> | Tier 3 | Cycle 14 BE precedent BUILD_DECISION_LOG §1.4 architectural-choice subsection pattern | Advisory only — non-binding if inconsistent with Tier 1/2 |
> | Contract | This document | Implementation detail — subordinate to all tiers above |

### Companion Contracts

**Upstream (this contract depends on):**
- See [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §6 for change-control triggers that must emit decisions here
- See [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §4 for failure-shape diagnoses that emit decisions here
- See [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §5 for promotion-FAIL diagnoses that emit decisions here
- See [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §4 for negative-result decisions

> The build-class decision log is the cross-cutting append-only ledger
> for every load-bearing decision the build cycle makes. ARTIFACT_CONTRACT
> changes, ACCEPTANCE_CRITERIA verdicts with FAIL/FAILS-WITH-DIAGNOSED-SHAPE,
> DEPLOYMENT_LOG promotions/rollbacks, and CROSS_SYSTEM_VALIDATION refute-import
> rows ALL emit a row here.

## Customization Guide

(Customization Guide deleted at BE-A fill close per template instruction.)

> **§N.4 Architectural-Choice subsections (recommended).** When Build-Runner faces ≥2 candidate architectures for a build event (e.g., additive-edit vs new-layered-file; imported-library vs reference-by-shim; ClassDef.body walk vs ast.walk traversal), append `### §N.4 Architectural-Choice` to the event-§N block recording (a) candidates ≥2 enumerated, (b) selected choice + verbatim rationale, (c) reversibility (LOW / MODERATE / HIGH), (d) backwards-compat evidence. Precedents: **Cycle-14-S8 BE#6** (additive-edit vs new-layered rubric file — chose additive; LOW reversibility; backwards-compat preserved by extending existing rubric rather than introducing parallel-file class) + **Cycle-14-S9 ARCH** (imported-library + reference-by-shim vs file-copy duplication — chose imported-library at govML; MODERATE reversibility; per-project reproducibility preserved via `governance.yaml.govml_lock_commit`). Per Cycle-14-S10 substrate §2 Item 6: this §N.4 pattern is methodology back-ported to govML at template-class scope (no new gate; verification = read Customization Guide post-edit; pattern lives in this template for forward-cycle Build-Runner consumption).
>
> Delete this section once the contract is filled.

---

## §0 Log Identity

<!-- gate:build_decision_log §0 required -->

| Field | Value |
|---|---|
| **Artifact** | `cycle_16_be_a_spec_registry_schema_and_write_boundary` (per ARTIFACT_CONTRACT §0) |
| **Cycle** | Cycle 16 (Stage 5 BE-A) |
| **Default decision owner** | build-runner (BE-A authoring) → Coach R3 (close-eval) → build-orchestrator (BE-B+ consumer integration) → Rex (CONTRACT_CHANGE OR KT-N firing per Binding 7) |
| **Append-only** | YES (edits are forbidden; corrections emit new rows with `supersedes` ref) |

<!-- /gate:build_decision_log §0 -->

---

## §1 Promotion Decisions (mirror [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 with rationale)

<!-- gate:build_decision_log §1 entries:1 -->

| # | Timestamp | Decision | Rationale (1-3 sentences) | Owner | Evidence link | Supersedes |
|---|---|---|---|---|---|---|
| 1 | 2026-05-27T19:30:00Z | BUILT (not yet PROMOTED) | BE-A build artifact stack produced + 3-test-bed live SPARQL UPDATE smoke ALL_PASS at /cycle6 Fuseki endpoint. Cycle 6 BE#1 substrate primitives operationally inherited via Path α (subclass polymorphism `cycle16:Spec rdfs:subClassOf c6:Statement` accepted by SHACL conforming fixture; non-conforming fixture 8 violations ≥4 threshold). HC-RP-S2-3 Wikidata supersedure RESOLVED-VIA-NAMESPACE-EQUIVALENCE (c6:rank ≡ wikibase:rank semantically; c6:supersedesRef ≡ prov:wasRevisionOf semantically). Pending Cycle-16-S4 BE-B consumer integration + Cross-System-Validator + Promotion-Gate Stack. | build-runner | `outputs/cross_system_validation_be_a.json` + `outputs/build_runner_events.jsonl` write.event rows + DEPLOYMENT_LOG §2 row 1 | N/A |

### §1.4 Architectural Choice (BE-A Wikidata supersedure path)

**Decision space (per substrate §3):** Path α (reuse `c6:rank` + `c6:supersedesRef` predicates via subclass inheritance) vs Path β (additive `cycle16:specRank` + `cycle16:supersedesSpec` predicates mirroring semantics) vs Path γ (modify Cycle 6 LOCKED ontology body — FORBIDDEN per Binding 7).

| Candidate | Selected | Rationale | Reversibility | Backwards-compat evidence |
|---|---|---|---|---|
| Path α: reuse `c6:rank` + `c6:supersedesRef` via subclass inheritance | ✓ SELECTED | Cleanest inheritance; no namespace pollution; SHACL polymorphism via `cycle16:Spec rdfs:subClassOf c6:Statement` accepts conforming fixture at smoke (verified 2026-05-27). HC-RP-S2-3 documented as RESOLVED-VIA-NAMESPACE-EQUIVALENCE at FINDINGS Layer 4 honest gap (Wikidata-canonical-namespace-absence is documentation-class not function-class). | LOW (cleanest path; revert = re-author with Path β additive predicates) | Cycle 6 LOCKED ontology body UNMODIFIED throughout BE-A (verified via `git -C ~/cycle_6_unified_substrate_build diff runtime/jena/` returns empty post-BE-A; HC #26 internal smoke gate 3 PASS — see §1.5 row 3) |
| Path β: additive `cycle16:specRank` + `cycle16:supersedesSpec` mirroring c6: semantics | NOT SELECTED | Acceptable fallback if Path α smoke surfaces SHACL polymorphism rejection; preserves Wikidata-canonical-naming option for future migration; marginal namespace pollution. Not needed because Path α smoke PASSED. | MODERATE | n/a (not exercised) |
| Path γ: append predicates to c6: LOCKED ontology body | FORBIDDEN | Modifies Cycle 6 LOCKED body; violates Binding 7. Build-Runner refuses-and-surfaces per DP#44 if forced. | n/a | n/a (forbidden) |

**Decision authority:** build-runner per dispatch substrate §3 + Binding 7 BIND. Records this architectural choice per Cycle-14-S9 ARCH precedent (imported-library + reference-by-shim at govML; analogous to subclass-inheritance + reuse-by-polymorphism here).

### §1.5 HC #26 Internal Smoke (3 gates per build-runner.md §Internal Smoke)

| Gate | Verdict | Evidence | Timestamp |
|---|---|---|---|
| 1: Fresh-scaffold findability (TTL files discoverable via `ls docs/*.ttl` ≥2 files) | PASS | `ls docs/*.ttl` returns 2 files: `spec_registry_schema.ttl` + `spec_registry_shapes.shacl.ttl` | 2026-05-27T19:35:00Z |
| 2: Per-artifact CLI cleanliness (double-brace-placeholder count = 0 + spot-read ≥3 sections substantive across 5 templates + 3 new artifacts) | PASS | All 5 scaffolded templates (ARTIFACT_CONTRACT + RUNTIME_EMIT_SPEC + ACCEPTANCE_CRITERIA + DEPLOYMENT_LOG + BUILD_DECISION_LOG) return placeholder count = 0 per Check #23 grep; all 3 NEW artifacts (spec_registry_schema.ttl + spec_registry_shapes.shacl.ttl + spec_authoring_discipline.md) parse cleanly per rdflib + structural section count ≥5 | 2026-05-27T19:35:00Z |
| 3: Backwards-compatibility preservation (Cycle 6 BE#1 ontology TTL UNMODIFIED + govML v2.8.2 UNMODIFIED + Cycle 16 Stage 0-4 LOCKED canonicals UNMODIFIED) | PASS | `git -C ~/cycle_6_unified_substrate_build diff runtime/jena/` returns empty post-BE-A + `git status` reports "nothing to commit, working tree clean"; Cycle 16 Stage 0-2 LOCKED canonicals at expected line counts post-BE-A (EXPERIMENTAL_DESIGN.md=576 + HYPOTHESIS_REGISTRY.md=148 + PROJECT.md=79 + REQUIREMENTS.md=101 + ROADMAP.md=184 + LANDSCAPE_ASSESSMENT.md=612 per `wc -l` 2026-05-27T19:35:00Z; baseline preserved per Stage 0-2 LOCKED at Cycle-16-S1 close `9300c86` + Stage 3-4 at Cycle-16-S2 close) | 2026-05-27T19:35:00Z |

**N=3 PASS rows = structural acceptance criterion met per `build-runner.md §HC#26 Internal Smoke`.**

<!-- /gate:build_decision_log §1 -->

> Each promotion decision in [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2
> emits a corresponding row here with rationale. The DEPLOYMENT_LOG row
> is the *event*; this row is the *reasoning*. They are kept in two
> places to honor append-only discipline at both the deployment surface
> and the decision surface.

---

## §2 Acceptance-Verdict Decisions

<!-- gate:build_decision_log §2 entries:1 -->

For every ACCEPTANCE_CRITERIA threshold that emits FAIL or FAILS-WITH-DIAGNOSED-SHAPE,
record the disposition decision.

| # | Threshold (link to [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §1 row) | Verdict | Failure shape (from §4 grid) | Decision | Owner | Evidence link |
|---|---|---|---|---|---|---|
| — | (no FAIL or FAILS-WITH-DIAGNOSED-SHAPE rows at BE-A close — all 6 ACCEPTANCE_CRITERIA §1 thresholds PASS per 3-test-bed smoke + pyshacl conforming/non-conforming verdicts) | PASS-all | n/a | n/a | build-runner | `outputs/cross_system_validation_be_a.json` |
| 2 | ACCEPTANCE_CRITERIA §10.1 rows 7-12 (BE-B 6 thresholds) | PASS-all | n/a (all 6 PASS; no FAIL diagnosed) | BE-B BUILT verdict at Cycle-16-S4 paired-commit; ROADMAP Phase 3 task 2 closed; Branch 4.2 BE-A-source closure landed; Brief 4 KT-3 firing surface 0 refusals → DOES NOT FIRE; Brief 3 HC-BE-A-1 refined at §10.3 (per-state conditional-readback table); govML v2.8.3 install_hook lands via fresh-scaffold smoke (7-file install per /tmp/be_b_smoke_<ts>). Pending Cycle-16-S5 BE-C TWO-surface BLOCKING gate consumer integration. | build-runner | `outputs/be_b_dogfooding_results.json` (all_3_pass=true) + `outputs/spec_registry_events.jsonl` (≥3 spec_registry.write.event rows) + `~/ml-governance-templates/VERSION` v2.8.3 + DEPLOYMENT_LOG §2 row 2 BUILT entry |
| 3 | ACCEPTANCE_CRITERIA §11.1 rows 13-18 (BE-C 6 thresholds) | PASS-all | n/a (all 6 PASS; no FAIL diagnosed) | BE-C BUILT verdict at Cycle-16-S5 paired-commit; ROADMAP Phase 4 closed; Branch 4.3 BE-B-source closure landed; H6 metric CONFIRMED (skeleton structural equivalence to k_register_present_gate.sh; divergence (a)+(b)+(c)+(d) per dispatch substrate §3 + honest carry (e) JSONL fire.event emit block at script close — load-bearing for HC #26 Gate 2; surfaced explicitly per feedback_honest_evaluation.md BINDING); KT-4 firing surface DOES NOT FIRE (cycle-close gate BLOCKED correctly on TB-3 dormant-silent load-bearing surface; HC #59 BINDING screen applied; SPARQL ASK substitution at shell-script primitive layer sufficient; no new enforcement primitive class required); govML v2.8.4 install_hook lands via fresh-scaffold smoke (`/tmp/be_c_smoke_<ts>` ships OBLIGATION doc + empty JSONL sink + 5 prior install outputs all operational); production graph baseline_pre/post EQUAL (246101 triples both sides; DROP cleanup verified at smoke close per dispatch substrate §4); JSONL fire.event sink ≥4 rows. KT-3 NOT RE-EVALUATED at BE-C per dispatch substrate §6 (carry forward LOCKED false from BE-B). Pending Cycle-16-S6 BE-D retroactive scan + Cross-System-Validator + Promotion-Gate Stack. | build-runner | `outputs/cross_system_validation_be_c.json` (all_3_pass=true; cycle_close_gate_holistic.verdict=BLOCKED matches_expected=true; baseline_equal_post_cleanup=true) + `outputs/spec_implementation_gates_events.jsonl` (≥4 fire.event rows: 2 present_gate + 2 session_close_gate) + `~/ml-governance-templates/VERSION` v2.8.4 + DEPLOYMENT_LOG §2 row 3 BUILT entry + ARTIFACT_CONTRACT §11 + RUNTIME_EMIT_SPEC §11 + ACCEPTANCE_CRITERIA §11 BE-C appends |
| 4 | ACCEPTANCE_CRITERIA §12.1 rows 19-24 (BE-D 6 thresholds) | PASS-all | n/a (all 6 PASS; no FAIL diagnosed) | BE-D BUILT verdict at Cycle-16-S6 3-repo paired-commit (cycle_16 + EMABS + Moonshots; NO govML at BE-D per work-host boundary discipline per dispatch substrate §0 + §9); ROADMAP Phase 5 closed; Branch 4.4 BE-C-source closure landed; H1 metric **CONFIRMED** (h1_total_enumerated=232 distinct after deterministic idempotent sha256_8 minting; raw=268 with 36 collisions resolved by INSERT-DATA idempotency; ≥ 90 floor; 2.6x multiplier; per substrate §3 H1 metric); H3 metric **CONFIRMED** (h3_dormant_silent_aggregate=137 ≥ 3 threshold; per-class breakdown: 7 a + 2 b + 117 c + 11 d); KT-2 firing surface **DOES NOT FIRE** (dormant_silent count 137 well above threshold 3; HC #59 BINDING screen applied — pre-registered SI kill condition not operationally-revisable; threshold evaluated literally per HC #59 disambiguation; substrate §3 + ED §Field 6 KT-2 + ROADMAP §4.1 task 5 surface); per-class strengthening n≥3 outcomes **ALL 4 PASS** (a=9 distinct + b=10 distinct + c=154 distinct + d=59 distinct; smallest class = 9 = 3x floor); per-spec materialization at PRODUCTION /cycle6 via BE-B `register_spec()` **268 raw writes; 232 distinct cycle16:Spec instances**; SPARQL COUNT cycle16:Spec at /cycle6 = 235 (= 232 BE-D + 3 BE-B S4 persisted); 8 initial DP#26 carve-out refusals (`spec_registry.shacl_refusal.event` rows with refusal_class=dp26_n_a_rationale_missing) → 8 retry successes with explicit n_a_rationale per spec-class context; `retroactive_classification=true` annotation present on every BE-D-written spec per ROADMAP §4.2 dependency 2; NO DROP GRAPH at BE-D close per substrate §1 row 4 + §2 (retroactive registry rows persist for BE-E forward-apply observation baseline reconstruction); production graph baseline pre-BE-D (default graph triples) = 6; post-BE-D full triple store = 250779 (~4680 net add for 232 specs × ~20 triples each / 3 nanopub graphs); HC-BE-D-1 honest carry SURFACED: write-boundary enforcement gap (specs written to filesystem without calling BE-B authoring wrapper) → Cycle 18 scope per Rex 2026-05-27 Option A disposition + Option B split-sequential framing; BE-D retroactive scan fills historical inventory by enumeration of 4 spec classes (one-time gap-fill) but does NOT enforce forward; BE-E forward-apply observation (S7) has the same blind spot — can only observe what's registered; closure of write-boundary gap requires different gate primitive class (filesystem scan + spec-class discriminator + work-host routing) than what Cycle 16 ships (SPARQL query against /cycle6). KT-3 NOT RE-EVALUATED at BE-D per dispatch substrate §6 (carry forward LOCKED `false` from BE-B; 8 BE-D DP#26 refusals are wrapper-side carve-out classification per HR §3d, NOT in scope for primary classes (a)+(b)+(d) author-refusal cumulative count which captures structural mandatory-field/enum-violation refusals only). KT-4 NOT RE-EVALUATED at BE-D per dispatch substrate §6 (carry forward LOCKED `DOES NOT FIRE` from BE-C). Pending Cycle-16-S7 BE-E forward-apply observation (`spec_authoring_event` + `spec_implementation_event` classes into runtime_emit/emit.py + `docs/forward_apply_observation_protocol.md` authoring + smoke-test per ROADMAP §5) + Cross-System-Validator + Promotion-Gate Stack. | build-runner | `outputs/retroactive_scan_cycle_1_15_run.json` (h1_confirmed_bool=true + h3_confirmed_bool=true + kt_2_firing_surface.kt_2_fires_bool=false + per_class_strengthening_n_ge_3 all 4 PASS + aggregate_counts_4x5 5-state breakdown + per_spec_evidence_IP_PRIVATE + hc_be_d_1_honest_carry + production_graph_baseline_pre/post) + `outputs/spec_registry_events.jsonl` (≥268 spec_registry.write.event rows from BE-D namespace `cycle_16.be_d.retroactive_scan` + 8 initial spec_registry.shacl_refusal.event rows) + `outputs/build_runner_events.jsonl` (1 retroactive_scan_run.event single-fire at close + Cycle 15 BE#4 5-event baseline class fires) + DEPLOYMENT_LOG §2 row 4 BUILT entry + ARTIFACT_CONTRACT §12 + RUNTIME_EMIT_SPEC §12 + ACCEPTANCE_CRITERIA §12 BE-D appends |
| 5 | ACCEPTANCE_CRITERIA §13.1 rows 25-30 (BE-E 6 thresholds) | PASS-all | n/a (all 6 PASS; no FAIL diagnosed) | BE-E BUILT verdict at Cycle-16-S7 4-repo paired-commit (cycle_16 + EMABS + Moonshots + govML per Rex back-port directive STANDING 2026-05-27; HC #45 ADDITIVE-APPEND chain extension to n=5); ROADMAP Phase 6 closed; Branch 4.5 BE-D-source closure landed; Done #9 H8 evaluation surface ENABLED (FINAL VERDICT DEFERRED to Cycle 18 cumulative ≥2-cycle window per HR §3 H8); 2 NEW event classes (`spec_authoring_event` + `spec_implementation_event`) wired into `scripts/runtime_emit/emit.py` ADDITIVELY (sink-routing helper `forward_apply_emit()` + namespace constant `FORWARD_APPLY_OBSERVATION_NAMESPACE` + sink default `FORWARD_APPLY_OBSERVATION_SINK_DEFAULT`; `emit_event()` core signature UNCHANGED per Cycle 10 §0 schema_version=0.1 LOCKED — verified via Python `inspect.signature(emit_event)` returns Cycle 15 BE#4 baseline signature); `docs/forward_apply_observation_protocol.md` NEW (~143L; 8 §N sections; 0 placeholders; HC-11 partition declared inline per Binding 8 BIND); smoke-test ≥4 fire.event rows at `outputs/forward_apply_observation_events.jsonl` (2 `spec_authoring_event` + 2 `spec_implementation_event` for TB-1 AgentContract synthetic + TB-2 Schema synthetic; test graph `<http://cycle16.local/test/be_e_smoke>` with PROV-O 4-typed-edges (`wasGeneratedBy` + `wasAttributedTo` + `generatedAtTime` + `wasInformedBy` per Cycle 6 BE#1 contract) + HC-11 `c6:publishable` access_permission enum; DROP GRAPH cleanup HTTP 200 + post-DROP test graph COUNT = 0 verified; canonical production registry rows preserved: 235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 persisted EQUAL pre/post BE-E). KT-5 firing surface evaluated at BE-E close per `forward_apply_observation_protocol.md` §4 + dispatch substrate §5: SPARQL query at `/cycle6` for Cycle-16-authored dormant-silent specs EXCLUDING BE-D retroactive (IRI-prefix discriminator `spec_retroactive_*` per BE-D §12.5 rollback discriminator) returns count = 0 → **KT-5 DOES NOT FIRE** (0 < 2 threshold); HC #59 BINDING screen applied — pre-registered SI kill condition not operationally-revisable. Honest gap surfaced re (a) mid-Cycle-16 observation window S7→S8 may be insufficient for full longitudinal verdict (cumulative ≥2-cycle window evaluation deferred to Cycle 18) + (b) IRI-prefix discriminator vs `retroactiveClassification` predicate gap (BE-D acceptance promised `retroactiveClassification=true` annotation predicate; actual implementation uses IRI prefix per BE-D §12.5 rollback discriminator — query corrected to use IRI-prefix filter per BE-D §12.5 verbatim). HC-BE-D-1 write-boundary enforcement gap PRESERVED as honest carry at BE-E (BE-E inherits SAME blind spot as BE-D; observes only BE-B-mediated path; closure → Cycle 18 scope per Rex 2026-05-27 Option B split-sequential). govML v2.8.5 ADDITIVE-APPEND back-port verified: NEW `install_forward_apply_observation()` function at init_project.sh after `install_spec_implementation_gates()` + function added to research-build profile dispatch list ADDITIVE + NEW dir `templates/build/forward_apply_observation/` with 2 files (FORWARD_APPLY_OBSERVATION_OBLIGATION.md + forward_apply_observation_protocol.md) + VERSION v2.8.4 → v2.8.5 (new header line prepended; v2.8.4 header preserved verbatim) + CHANGELOG.md NEW with v2.8.5 entry; LOCKED bodies of `install_runtime_emit_substrate` + `install_spec_registry_authoring_discipline` + `install_spec_implementation_gates` UNMODIFIED — `git diff` 0 on those function line ranges verified at R3. KT-2 + KT-3 + KT-4 NOT RE-EVALUATED at BE-E per dispatch substrate §6 (carry forward LOCKED `DOES NOT FIRE` from BE-B + BE-C + BE-D). Pending Cycle-16-S8 Cycle 16 close 5-layer FINDINGS authoring (ROADMAP Phase 7) + Cross-System-Validator + Promotion-Gate Stack. | build-runner | `outputs/forward_apply_observation_events.jsonl` (4 fire.event rows: 2 `spec_authoring_event` + 2 `spec_implementation_event`) + `outputs/build_runner_events.jsonl` (1 `forward_apply_smoke.event` single-fire at BE-E close + Cycle 15 BE#4 5-event baseline class fires) + `outputs/spec_registry_events.jsonl` append-only (smoke-test write events at test graph; DROP-cleaned at smoke close) + `~/ml-governance-templates/VERSION` v2.8.5 + `~/ml-governance-templates/CHANGELOG.md` v2.8.5 entry + DEPLOYMENT_LOG §2 row 5 BUILT entry + ARTIFACT_CONTRACT §13 + RUNTIME_EMIT_SPEC §13 (2 NEW event classes) + ACCEPTANCE_CRITERIA §13 BE-E appends + `docs/forward_apply_observation_protocol.md` NEW + `scripts/runtime_emit/emit.py` ADDITIVE extension |
| 6 | ACCEPTANCE_CRITERIA §14.1 rows 31-36 (BE-F 6 thresholds) | PASS-all | n/a (all 6 PASS; no FAIL diagnosed) | BE-F BUILT verdict at Cycle-16-S11 3-repo paired-commit (cycle_16 + EMABS + Moonshots; NO govML at S11 per dispatch substrate §1 item 11 + ED §5.7 evidence-path translation; v2.8.5 STANDS UNMODIFIED; govML upstream probe library back-port at v2.8.6 ADDITIVE-APPEND chain extension to n=6 lands at BE-I S14+ per HC #45 chain extension precedent); ROADMAP Phase 8 BE-F closed; Done #13 + H_recovery_3 closed; SI Amendment 2026-05-28a Done #11-#16 Done #13 mechanically verified; 4 probe primitives at `scripts/probes/{a,b,c,d}/probe_<class>.py` shipped + executable + version-locked (PROBE_VERSION = "0.1" + PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae" in 4 probe bodies); admission gate (Python `scripts/probes/__init__.py` + bash `scripts/probe_library_admission.sh`) DP#44-compliant refuse-on-self-test-fail; 8 self-test fixtures shipped (1 known-good + 1 known-bad per class A/B/C/D); T12 negative test verified admission refusal (synthetic broken probe rejected with exit code 1 + refuse event emitted to `outputs/probe_library_admission_events.jsonl`; broken probe REMOVED post-T12; canonical 4-probe admission scan returns exit 0); dogfooding-within-cycle 16 production fires across 4 classes (per-class 4 each; mix expected-implemented vs not_implemented: A(2/2) B(2/2) C(1/3) D(1/3) all ≥1 each per substrate §1 item 6 Done #15d strict; smoke-only fires NOT counted toward acceptance per Done #15d). KT-7 firing surface DOES NOT FIRE (4 admitted probes all distinguish + T12 refusal verified); KT-9 firing surface DOES NOT FIRE (no generic-emission escape primitives in 4 probe bodies; admission refuses by construction via per-class behavioral evidence shape); KT-10 firing surface DOES NOT FIRE (≥1 production fire on every class A/B/C/D; in fact 4 per class — well above 1 floor per H_recovery_1 falsification condition). KT-8 firing surface evaluated structurally at Class C `_structural_judge()` anti-substitution refusal (embodimentRef IS DECISION_LOG → refuse with HC #72 evidence; KT-8 anti-substitution discipline verified in known_bad_c_1 fixture). Class C LLM-judge prompt template at `scripts/probes/c/llm_judge_prompt.md` explicitly forbids registry-text-only / ADR-text-only / FINDINGS-mention-only as acceptance evidence (HC #72 BINDING language; calibration fixtures referenced); structural-judge fallback in `probe_design_decision.py` enforces same contract shape without online LLM at probe-fire time (full LLM-judge upgrade DEFERRED to Cycle 17+ per honest gap at §14.5). HC-BE-D-1 boundary discipline PRESERVED (BE-F probes consume `/cycle6` SPARQL endpoint via SELECT/ASK only; no INSERT/UPDATE/DELETE/DROP from probe bodies; canonical production registry untouched; 235 cycle16:Spec at /cycle6 = 232 BE-D + 3 BE-B S4 EQUAL pre/post BE-F). govML v2.8.5 STANDS UNMODIFIED at BE-F (NO govML touch at S11 per substrate §1 item 11 + ED §5.7 evidence-path translation; v2.8.6 ADDITIVE-APPEND DEFERRED to BE-I S14+ per HC #45 chain extension precedent strict). LOCKED preservation VERIFIED: BE-A §1-§3 + BE-B §10 + BE-C §11 + BE-D §12 + BE-E §13 byte-identical via md5 head-N comparison per file (ARTIFACT_CONTRACT.md lines 1-594 / RUNTIME_EMIT_SPEC.md lines 1-647 / ACCEPTANCE_CRITERIA.md lines 1-566 all md5-match HEAD baseline 901f427). KT-2 + KT-3 + KT-4 + KT-5 NOT RE-EVALUATED at BE-F per dispatch substrate §6 (carry forward LOCKED `DOES NOT FIRE` from BE-B + BE-C + BE-D + BE-E). HC #74 cycle-management surfacing: no operational cycle-management dispositions encountered during BE-F build; no Pattern 11 Step 3.5 surface required. HC #72 substrate-compose substitution-detection self-applied at every primitive design moment (Class A behavioral via OTEL JSONL tool_use NOT registry-state; Class B via call-site/inline-exec/JSONL exercise NOT just file-exists; Class C structural-judge with file:line citation NOT registry-text; Class D downstream JSONL fire OR cross-cycle citation NOT FINDINGS-mention-only); Coach R3 independent HC #72 sweep verdict authoritative per `feedback_honest_evaluation.md` BINDING. Pending Cycle-16-S12 BE-G Operational-Definition Substitution Gate (Done #14 + H_recovery_4) + Cross-System-Validator + Promotion-Gate Stack. | build-runner | `outputs/probe_fire_events.jsonl` (16 production-fire rows with run_id prefix `s11_be_f_production_*`; 4 per class A/B/C/D) + `outputs/probe_library_self_test_events.jsonl` (≥8 self-test rows + T12 row + Class C re-run row with predicateType `cycle16:probe_self_test_v1`) + `outputs/probe_library_admission_events.jsonl` (5 events: 4 PASS + 1 REFUSE for T12 negative test) + `outputs/build_runner_events.jsonl` (1 `be_f_probe_library_ship.event` single-fire at BE-F close + Cycle 15 BE#4 5-event baseline class fires) + `scripts/probes/{a,b,c,d}/probe_*.py` (4 probes; executable; version-locked) + `scripts/probes/__init__.py` (admission gate) + `scripts/probes/c/llm_judge_prompt.md` (Class C LLM-judge contract template) + `scripts/probe_library_admission.sh` (bash CLI wrapper) + `tests/probes/fixtures/known_*.json` (8 fixtures) + DEPLOYMENT_LOG §2 row 6 BUILT entry + ARTIFACT_CONTRACT §14 + RUNTIME_EMIT_SPEC §14 (4 NEW event classes) + ACCEPTANCE_CRITERIA §14 BE-F appends + state.json transition + DECISION_LOG D-S11-1 |
| 7 | ACCEPTANCE_CRITERIA §15.1 rows 37-46 (BE-G 10 thresholds) | PASS-all | n/a (all 10 PASS; no FAIL diagnosed) | BE-G BUILT verdict at Cycle-16-S12 3-repo paired-commit (cycle_16 + EMABS + Moonshots; NO govML at S12 per work-host boundary — BE-G scripts authored at canonical `~/ml-governance-templates/scripts/` AND mirrored at `scripts/be_g_mirror/`; govML back-port + v2.8.6 ADDITIVE-APPEND is BE-I/S14 per HC #45 chain extension); ROADMAP Phase 9.2 BE-G closed; Done #12 + #17 + #18 + #19 + #29 + #30 + H_recovery_2/7/8/9 closed. 10 deliverables PASS: (1) pre-commit hook 3 HARD-BLOCK fixtures + 3 pre_commit_hook_block.fire.event; (2) inotify-ctypes watcher 3 scan-once @53ms ≤60s + LIVE daemon 2 fires on real bypass write; (3) forward_apply_emit() wired into production register_spec():547+ closing emit.py:96 zero-caller gap (6 production fires); (4) 3-registry reconciliation 5 closes drift=false vs LIVE /cycle6 241 + prompt_inventory 9 + FS 2; (5) Done #17 present_gate UPGRADED — subprocess `probes/<class>/probe_<class>.py --aggregate-cycle 16` + aggregate payload.implemented (positive 268 fires/72 impl PASS; 3 negative BLOCKED; ASK-currentStatus REMOVED, `grep '^[^#]*ASK {.*currentStatus'`=0; KT-8 PASS); (6) kill_spec() 4-param (sig==4) ADR-grep-subprocess + spec_killed_event + SPARQL→killed readback-verified + 3 DP#44 ValueError refusals NO-event; (7) Done #19 session_close_gate UPGRADED — last-3-session probe-fire JSONL aggregate NOT currentStatus; advisory_mode_bool=true; 3 dormancy fixtures each flag 3; monotonic 1→5 (pipefail-hardening `|| true` on SESSIONS_BETWEEN grep -c — BE-G-scoped one-token additive fix on the BE-C-authored count primitive, behavior unchanged for ≥1 match); (8) Done #29 coverage matrix .md+.json (4 repos) + CI required-status-check spec_authoring_required_check.yml closing --no-verify; (9) Done #30 build-orchestrator+build-runner registered (HC #64; confirmed ABSENT pre-S12) + 6 deliverables self-registered; (10) Class E/F integration-hook STUBS (return None; live BE-J/S15 + BE-K/S16; NO probe impl). KT-7 (4 --self-test exit 0) + KT-8 (4 predicates subprocess/import-execute named primitive) PASS. HC #70 honest scope: present+future spine; does NOT make past specs implemented (Phase 11-13) NOR validate probe accuracy (Done #25/Phase 12); HC-BE-D-1 closed for forward/present path only. govML v2.8.5 UNMODIFIED at S12. LOCKED preservation VERIFIED: BE-A..BE-F §1-§14 byte-identical (md5 head-694 ARTIFACT / head-798 RUNTIME_EMIT / head-666 ACCEPTANCE unchanged). KT-1..KT-6 + KT-9/KT-10 NOT RE-EVALUATED at BE-G (carry forward LOCKED from prior BEs). HC #74 cycle-management surfacing: none encountered. Pending Cycle-16-S13 BE-H structural-prevention layer + Cross-System-Validator + Promotion-Gate Stack. | build-runner | `outputs/spec_authoring_events.jsonl` (8: 3 hook-block + 5 watcher) + `outputs/three_registry_reconciliation_events.jsonl` (5) + `outputs/spec_implementation_gates_events.jsonl` (8: 4 present-gate incl 3 BLOCKED + 4 session-close incl 3 dormancy) + `outputs/spec_registry_events.jsonl` (1 spec_killed_event + 11 refusals + 7 write.event incl 6 self-register) + `outputs/forward_apply_observation_events.jsonl` (7 production fires) + `outputs/be_g_coverage_matrix.{md,json}` + `outputs/spec_authoring_required_check.yml` + `~/ml-governance-templates/scripts/{spec_authoring_pre_commit_hook.sh,spec_authoring_watcher.py,three_registry_reconciliation_gate.sh,spec_implementation_present_gate.sh,spec_implementation_session_close_gate.sh}` (+ `scripts/be_g_mirror/` mirrors) + `scripts/spec_registry_authoring.py` (kill_spec + forward_apply wiring + Class E/F hooks) + prompt_inventory build-orchestrator+build-runner rows + ARTIFACT_CONTRACT §15 + RUNTIME_EMIT_SPEC §15 + ACCEPTANCE_CRITERIA §15 + DEPLOYMENT_LOG §2 row 7 + DECISION_LOG D-S12-1 + state.json transition |

<!-- /gate:build_decision_log §2 -->

> Forbidden decision shape: "loosen the threshold." Per [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §4
> diagnostic grid, a FAIL is *diagnosed*, not relaxed. If the threshold
> was wrong by construction, that is itself a finding (record as
> CONTRACT_CHANGE; recompute baseline; do NOT silently slide the threshold).

---

## §3 Cross-System-Validation Decisions

<!-- gate:build_decision_log §3 entries:1 -->

For every CROSS_SYSTEM_VALIDATION result that produces a refute-import or
boundary-condition decision.

| # | Primitive (link to [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §3 row) | Cross-bed verdict | Decision | Rationale | Evidence link |
|---|---|---|---|---|---|
| 1 | 14-field schema + SHACL polymorphism via subclass inheritance (Path α) | YES across 3 test beds (TB-1 + TB-2 + TB-3 all PASS) | LOAD_BEARING | Path α inheritance accepted by SHACL at 3 spec-classes (AgentContract + Schema + MethodologyCommitment); 4th class DesignDecision deferred to BE-D Phase 5 retroactive scan per ROADMAP. | `outputs/cross_system_validation_be_a.json` `be_a_smoke_results` array |
| 2 | DP#26 carve-out for MethodologyCommitment (runtime_emit_event_class = 'n/a — citation-based activation per DP#26' literal accepted by SHACL) | YES at TB-3 (1 test bed; carve-out is class-specific) | LOAD_BEARING | SHACL `cycle16:SpecShape` `sh:minCount 1` on field 11 accepts the 'n/a' literal as a valid xsd:string value; no enum constraint on field 11 (only MIN_COUNT 1). DP#26 BINDING preserved structurally per HR §3d. | `outputs/cross_system_validation_be_a.json` `be_a_smoke_results[2]` (TB-3) + pyshacl conforming-fixture validation |

<!-- /gate:build_decision_log §3 -->

---

## §4 Contract-Change Decisions

<!-- gate:build_decision_log §4 entries:0 -->

For every CONTRACT_CHANGE that updates [ARTIFACT_CONTRACT](ARTIFACT_CONTRACT.tmpl.md) §1-§6
or other build-class contract surfaces.

| # | Timestamp | Contract section changed | Old → New | Rationale | Authority | Commit hash |
|---|---|---|---|---|---|---|
| — | (no CONTRACT_CHANGE rows at BE-A close — BE-A operates within ED §0a + §4a + Amendments 27a/27b paradigm bindings authored at Cycle-16-S1+S2; no §1/§2/§3 row revision needed for BE-A) | n/a | n/a | n/a | n/a | n/a |

<!-- /gate:build_decision_log §4 -->

> CONTRACT_CHANGE decisions REQUIRE a Tier 1 authority reference (per
> Authority Hierarchy at top). Operator-direct or sub-tier CONTRACT_CHANGE
> without Tier 1 authority is forbidden (the strict-process-rail discipline:
> no override addenda; no operator-direct edit of canonical templates to
> make a gate pass; applies symmetrically to build-class).

---

## §5 KILL-Trigger Decisions

When a build-class KILL trigger fires (artifact contract drift; baseline
instability >threshold; cross-system mechanism refute; scope creep beyond
cycle envelope), record the KILL decision and disposition.

| # | KILL trigger | Fired at | Disposition | Surface (where halt was reported) | Upper-tier paradigm ruling required? |
|---|---|---|---|---|---|
| — | KT-6 (Cycle 6 substrate-viability blocker) | NOT FIRED at BE-A (Coach pre-verified 2026-05-27; Build-Runner re-verified at smoke: Fuseki PID alive + /cycle6 ASK HTTP 200 + UPDATE HTTP 200 + readback HTTP 200 + DROP GRAPH HTTP 200) | n/a | n/a | NO (DOES NOT FIRE) |
| — | KT-4 (predicate extension requires new primitive class) | NOT FIRED at BE-A (Path α subclass inheritance accepted by SHACL polymorphism at 3 test beds; H6 CONFIRMATION CANDIDATE for BE-C evaluation surface) | n/a | n/a | NO (DOES NOT FIRE; H6 evidence surface at BE-C) |
| — | (no other KT triggers in scope at BE-A; KT-1/KT-2/KT-3/KT-5 evaluation surfaces are downstream BE-B/BE-D/BE-E or Cycle 17-18 longitudinal) | n/a | n/a | n/a | n/a |

> KILL triggers fire structurally; routing-around via operator-direct edit
> of the gate or canonical artifact to make the trigger PASS is forbidden
> (the strict-process-rail discipline binds symmetrically to build-class).
> On any KILL fire requiring upper-tier paradigm ruling, halt-and-surface;
> do NOT auto-route.

---

## §6 Self-test (BEFORE classifying decision log as COMPLETE for cycle close)

| # | Check | Status |
|---|---|---|
| 1 | Every [DEPLOYMENT_LOG](DEPLOYMENT_LOG.tmpl.md) §2 row has a corresponding §1 decision row with rationale | [x] (DEPLOYMENT_LOG §2 row 1 BUILT verdict ↔ BUILD_DECISION_LOG §1 row 1 BUILT decision) |
| 2 | Every [ACCEPTANCE_CRITERIA](ACCEPTANCE_CRITERIA.tmpl.md) §5 FAIL or FAILS-WITH-DIAGNOSED-SHAPE row has a §2 decision row | [x] (no FAIL rows at BE-A close; §2 marked "no FAIL or FAILS-WITH-DIAGNOSED-SHAPE rows") |
| 3 | Every [CROSS_SYSTEM_VALIDATION](CROSS_SYSTEM_VALIDATION.tmpl.md) §3 PARTIAL or NO row has a §3 decision row | [x] (§3 LOAD_BEARING decisions for Path α inheritance + DP#26 carve-out — 2 rows for BE-A cross-bed evidence) |
| 4 | Every CONTRACT_CHANGE in the cycle commits has a §4 row referencing the commit hash | [x] (no CONTRACT_CHANGE at BE-A close; §4 marked "no CONTRACT_CHANGE rows") |
| 5 | Every KILL trigger fire has a §5 row with disposition (no silent KILL) | [x] (no KT fires at BE-A close; §5 marked NOT FIRED for KT-6 + KT-4 with evidence; KT-1/KT-2/KT-3/KT-5 are downstream BE evaluation surfaces) |
| 6 | All rows have non-placeholder evidence links (or explicit "no evidence; deferred" with justification) | [x] (all populated rows have file-path evidence links to outputs/ + docs/ artifacts; empty rows explicitly marked "no fires at BE-A close" with downstream BE deferral) |

> If any check is `[ ]`, halt-and-surface; do NOT close the cycle.

---

## §7 Pre-check Interface (for build-class agent specs)

<!-- gate:build_decision_log §7 advisory -->

Build-class agent specs invoke a pre-execution checklist before primary task
execution (extends F-C composition from RIDE: checklist-with-refusal-authority,
PASS/FAIL/WARN per item). The interface contract is publishable; the checklist
contents and runner orchestration internals are pipeline IP and live at internal
paths NOT inlined here.

| Field | Value |
|---|---|
| **Pre-check ID** | `build_runner` (per `build-runner.md §pre_check` invocation pattern) |
| **Invocation** | `bash ~/ml-governance-templates/scripts/agent_pre_check_runner.sh --role build_runner --project-dir ~/cycle_16_close_spec_to_implementation_gap_build` |
| **Refusal authority** | Refuse-on-missing-precondition: any FAIL-level item halts primary execution with explicit callout per `build-runner.md §pre_check DP#44 refusal-authority binding` |
| **Mode** | Conditional invocation: F-C runner fires ONLY when `governance.yaml` has `f_c_checklist: enabled` (BLOCKING) or `f_c_checklist: advisory` (WARN-only). Default at Cycle 16: SKIP (governance.yaml does not enable F-C checklist; preserves all 17 existing projects per F4 fix discipline). |
| **Checklist contents** | (pipeline IP — referenced not inlined; lives at `~/ml-governance-templates/checklists/build_runner.checklist` per `build-runner.md §pre_check` + BUILD_DECISION_LOG §7 L180-L181 verbatim) |
| **Runner orchestration internals** | (pipeline IP — referenced not inlined; lives at internal-only path per HC-11 partition) |

<!-- /gate:build_decision_log §7 -->

> The interface (pre-check ID, invocation, refusal authority, mode) is
> publishable build-class methodology. The checklist contents and runner
> orchestration are pipeline-private IP (publishable-vs-private partition); a separate internal
> agent-spec for build-class is dispositioned at the next build-class cycle
> bootstrap, NOT inlined into this template.

| 8 | BE-H | Ship structural-prevention layer at cycle_16 first-arc (govML untouched; BE-I back-port); every implementation-judging predicate subprocess-executes a named BE-F probe (KT-8); fix HC-BE-G-1 fail-open->fail-closed crash verdict + HC-BE-G-2 magic-64->real session-index partition in be_g_mirror session_close_gate | S13 |

(Stage 5 BE-H section 2 row 8 ADDITIVE per Cycle-16-S13; rows 1-7 LOCKED.)

| 9 | BE-J | Ship Class E KG-fidelity probe (Done #23) at cycle_16 first-arc (NO govML; later-BE back-port). VERDICT: BUILT. The probe IMPORTs+EXECUTEs the real KG-vs-reality comparison — resolves+reads the source-of-record, re-derives+diffs fields, fires the live BE-F probe for status-match (KT-8). A status-enum string-match or KG self-assert-flag trust is the FORBIDDEN proxy this cycle exists to kill (substrate §2). Done #41 autonomy floor: conservative fail-safe disposition (infidelity_or_unverified, never faithful) on any ambiguity; KT-12 (>10% fidelity-fail → SURFACE + remediation queue, NOT a halt) — no mandatory human step in the probe/gate/close path. 3 Done #23 surfaces live-wired; real /cycle6 dogfood (242 nodes, faithful=160/infidelity=72/unverifiable=10). HC #70 HONEST: BE-J does NOT prove Class E population-level ACCURACY (that is Done #25) — no "KG is 100% faithful" claim. | S15 |

(Stage 5 BE-J section 2 row 9 ADDITIVE per Cycle-16-S15; rows 1-8 LOCKED.)

| 10 | BE-K | Ship Class F spec-implementation fidelity probe + live code-reading judge (Done #24/#26) at cycle_16 first-arc (NO govML; later-BE back-port). VERDICT: **BUILT-NOT-FULLY-PROMOTED (partial).** "Does the code behaviorally do what the spec commits to" (Done #32), NOT name-presence. Done #41 floor PROVEN: execution-first (import+execute embodiment, check emitted event_class vs committed — wrong-thing caught by execution, KT-8); live LLM judge ONLY as fallback, READS code + file:line citation, REFUSES registry/ADR/spec-text, valid ONLY with ≥1 independent automated cross-check (Class C `_structural_judge`) agreeing — lone-LLM ≠ acceptance; no human label. Coach R3 drove a real live fire: judge genuinely invoked Anthropic API; under HTTP-400-usage-limit failure the probe returned conservative not_faithful (missing independent signal), NOT fabricated, NOT crash — the floor held under real failure. Self-test exit 0 (good-exec/wrong-thing-exec/text-only-refuse); admission exit 0 (6 admitted). Dogfood NON-smoke: 268 fired / 4 applicable / 264 DP#26 carve-outs / divergence 0.50 over n=4 (MEASURED, not a verdict); KT-13 (>10% divergence → surface+queue, NOT halt). **Done #26 NOT fully met: 0 successful live verdicts → LIVENESS is a BLOCKING carry to S17 (≥1 real-code→real-verdict), NOT folded into "done."** GAP-1 fixed (model repin claude-3-5-haiku-20241022 EOL → claude-haiku-4-5). GAP-2 BLOCKING (Rex infra): Anthropic account usage-limit blocks live verdict + Done #25; likely degrades T3/classify crons now. HC #70 HONEST: does NOT prove judge correctness or Class F accuracy (Done #25). | S16 |

(Stage 5 BE-K section 2 row 10 ADDITIVE per Cycle-16-S16; rows 1-9 LOCKED.)
