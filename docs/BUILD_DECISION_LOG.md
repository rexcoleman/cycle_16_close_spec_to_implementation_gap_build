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
