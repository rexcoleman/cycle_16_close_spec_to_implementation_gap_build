# Faithful-Target Mechanism — Cycle-16-S26 build-element spec (additive)

RP-authored per Binding 6. ADDITIVE-ONLY (DP#42): this is a NEW docs/ artifact; it
edits NO locked Stage 0-4 artifact and modifies NO existing phase section. It describes
the faithful-target measurement-fidelity mechanism built + run at Cycle-16-S26, its
acceptance criteria, and the anti-gaming asserts.

Authority: kc-54 R1 PASS; Done #60 (spec-provenance fidelity, past-era) corrected per
SI Amendment 28k; extraction-fidelity part of #28/#67. HC #74 BINDING (probe/harness/
floors/fixtures version-locked).

## 0. The defect this fixes

The S24 spec→implementation gap list (`outputs/trusted_detector_run.json`) keyed each
spec's "what counts as implemented" on the BE-D scan's SYNTHESIZED
`runtime_emit_event_class`. The S25 vertical slice proved that synthesized per-spec
target can be UNFAITHFUL to the spec's OWN text. Canonical worked example:

- `cycle16:spec_retroactive_af3a918a` (kernel-coach AgentContract). The scan synthesized
  `runtime_emit_event_class = kernel_coach.dispatch`. The spec-of-record
  (`~/Moonshots_Career_Thesis_v2/.claude/agents/kernel-coach.md` §Role) commits a 5-event
  schema whose dispatch class is `kernel_coach.transition.fire`. `kernel_coach.dispatch`
  appears NOWHERE in the spec — it is a scan-synthesized abstraction.
- Consequence: the F-probe keyed on the synthesized string reports `not_faithful` EVEN
  for a correct implementation (execution path: "embodiment ACTIVE in namespace
  kernel_coach but emits WRONG class"). Re-running the gap detector could not confirm an
  honest fix — which is why S25 needed an independent instrument.

Scaling implementation against synthesized targets would build ~200 specs to a detector,
not to the specs — the recursive failure Cycle 16 exists to stop. So: make the per-spec
targets FAITHFUL to each spec's own text, then re-derive the gap list. THIS IS THE
MEASUREMENT-FIDELITY FIX. It does NOT itself close the gap.

## 1. Mechanism

### 1.1 Faithful-target extraction (`scripts/faithful_target_extractor.py`)

Two INDEPENDENT readers (single-reader REFUSED; reuses
`spec_extraction_pipeline.extraction_methods_distinct`):

- **E1 (rule-based, `rule_based_event_class_parser`)**: parses the spec-of-record source
  (resolved via the scan `audit_tuple[1]`) for the event class(es) it ACTUALLY NAMES in
  its Role / emit / acceptance / schema region. Chooses the dispatch/transition-fire
  class by a fixed preference order. NEVER reads the synthesized scan field.
- **E2 (LLM, `llm_acceptance_text_reader:claude-haiku-4-5`)**: independently reads the
  spec acceptance prose and extracts the committed observable. Key-switch on usage-limit
  (`ANTHROPIC_API_KEY` in `.env.backup` ↔ `ORCHESTRATION_ANTHROPIC_API_KEY` in `.env`) —
  operational, not a blocker. No key at all → REFUSE conservatively (DP#44), never fabricate.

Reconcile: E1∩E2 agree → faithful target accepted. DP#26 carve-out (`runtime_emit_event
_class` begins `n/a`) → faithful target `n/a` preserved HONESTLY (never an invented
observable). Disagreement → conservative + surfaced (NOT auto-resolved, NOT tuned to
agree). No committed observable AND not a DP#26 carve-out → spec-provenance DEFECT.

### 1.2 KG provenance capture (`scripts/faithful_target_kg_capture.py`)

Past-era RECONSTRUCTION overlay into the Fuseki /cycle6 KG (system-of-record), via the
EXISTING `spec_registry_authoring._sparql_post` (not a forked client). Writes, per spec:
`cycle16:faithfulCommittedObservable`, `cycle16:faithfulTargetReconstruction =
"past_era_disclosed_confidence"`, and a `prov:wasDerivedFrom` edge to the named source
artifact. Confirmed by SPARQL READ-BACK (assert edge + target present), never by
asserting success. Reconstruction is the FALLBACK for already-authored specs; it is NOT
the forward authoring-time mechanism (#67, S27+).

### 1.3 Re-derivation (`scripts/trusted_detector_run_faithful.py`)

Writes a faithful-overlay scan (each spec's `runtime_emit_event_class` → faithful target)
and re-runs the UNMODIFIED detector against it. Output → NEW file
`outputs/trusted_detector_run_faithful.json` (does NOT overwrite the synthesized run).
Judgment-tier verdicts are INVARIANT (no DP#26 spec's target changed substantively —
faithful `n/a` ≡ synthesized `n/a — citation-based…`) so the cached judgment verdicts are
reused verbatim; only the execution tier is re-fired against faithful targets.

### 1.4 Independent verification (`scripts/faithful_rederivation_independent_verifier.py`)

Verifies the re-derived gap list via a DIFFERENT code path: re-parses spec acceptance
text with a distinct regex and reads the emission sink DIRECTLY, with NO import of the
faithful-target extractor and NO import of the F-probe. Exit 0 (corroborated) / 1.

## 2. Acceptance criteria

- AC-1: `extraction_methods_distinct == true` (single-reader REFUSED).
- AC-2: every faithful target is extracted from the spec's own text + confirmed by an
  independent second reader OR is an honest DP#26 `n/a`; none synthesized.
- AC-3: af3a918a worked case: synthesized `kernel_coach.dispatch` → faithful
  `kernel_coach.transition.fire`, captured in the KG with a `prov:wasDerivedFrom` edge,
  confirmed by SPARQL read-back.
- AC-4: re-derived gap list verified by an instrument independent of the producer
  (different path/reader/source-of-truth); exit 0.
- AC-5: probe / harness / floors / fixtures byte-identical (`git diff --stat` empty);
  `trusted_detector_run.json` not overwritten.
- AC-6: before/after movement table emitted; old vs new aggregate rate disclosed with
  residuals carried.

## 3. Anti-gaming asserts (HARD)

1. Targets from the spec's own text + independent second reader; never synthesized,
   never tuned to make a probe pass (#27/#28).
2. Re-derived gap list verified by a DIFFERENT instrument than the one that produced it
   (#34).
3. NO human in the verification/close path; NOTHING tuned (floors/probes/harness/fixtures
   byte-identical — proven by `git diff --stat`).
4. The literal `kernel_coach.dispatch` (or any class invented to flip the F-probe) is
   NEVER emitted as a faithful target — asserted in-code (`_FORBIDDEN_SYNTHESIZED`).
5. Additive-only (DP#42): no locked Stage 0-4 artifact edited.

## 4. Honest disclosure

This is the MEASUREMENT-FIDELITY fix. It does NOT close the spec→implementation gap. ONE
spec (kernel-coach af3a918a) was implemented at S25; ~the rest remain. The re-derivation
moved exactly ONE verdict (af3a918a False→True — a correct implementation the synthesized
target falsely flagged); implementation-coach stayed not-implemented under its faithful
target (genuinely dormant), proving the fix does not inflate. Aggregate moved 10/206
(4.85%) → 11/206 (5.34%). Carried residuals (disclosed, not resolved): +53 DesignDecision
classification-surplus; 6 single-reader edge specs; 26-absent extraction-coverage gap
(M1'=193 disclosed-bound); BE-J 33.88% NOT promoted.
