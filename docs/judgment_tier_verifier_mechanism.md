# Judgment-Tier Verifier Mechanism — Cycle-16-S28 build-element design spec (additive)

RP-authored per Binding 6 (RP designs; Build-Runner implements; Coach verifies). ADDITIVE-ONLY
(DP#42): this is a NEW `docs/` artifact. It edits NO locked Stage 0-4 artifact and modifies NO
frozen path. It SPECIFIES the verifier-of-record for the judgment tier + its blind, powered,
structurally-independent accuracy-validation process. The Build-Runner builds the code from this
spec; this document writes no code.

Authority: Cycle-16-S28 transition prompt (`~/Moonshots_Career_Thesis_v2/.claude/workspace/cycle_16_s28_transition_prompt.md`)
First action SETTLED = "build + accuracy-validate the JUDGMENT-TIER VERIFIER (Hole 1)" per the
holes-disposition (`cycle_16_holes_disposition_rex_2026-05-30.md` §Re-sequenced plan S28) + Rex
close-bar rulings 2026-05-30. Disciplines anchored: #19/#25/#34/#38/#46/#61 (validate-the-validator;
no human in close path; independent 2nd instrument; diverse judges must agree + residual disclosed).
HC #74 BINDING (probe / harness / floors / fixtures version-locked — consumed UNMODIFIED).

---

## 0. The problem this instrument is for (and what makes it judgment-tier)

S24's two-tier partition (`scripts/validation_tier_verdict.py` + `outputs/validation_tier_verdicts.json`,
read live 2026-05-30) is:

| Tier | Count | Source |
|---|---|---|
| execution_checkable | 3 | `validation_tier_verdicts.json` `T1_tier_counts.execution_checkable` |
| semantically_judged (= judgment-tier) | 203 | `validation_tier_verdicts.json` `T1_tier_counts.semantically_judged` |
| — of which CONTESTED→NOT-VALIDATED (fail-safe) | 194 | `T4_failsafe.judgment_tier_contested` |
| — of which diverse-judge VALIDATED | 9 | 203 − 194 |

The judgment tier is the **~194–203 specs with no execution oracle**: there is no committed
runtime-emit class to fire and observe, so "is this spec implemented?" reduces to "does the code
behave as the prose intended?" — a judgment, not a measurement. That is precisely why no trustworthy
instrument exists for them yet. S27 proved the danger empirically: its n/a re-derivation instrument
measured **precision 0.6 / cross-instrument agreement 0.64** (`outputs/na_rederivation_accuracy.json`),
which is what an *unvalidated* judgment instrument looks like — too low to assert any count.

**Why S28 is on the critical path:** S29+ will SCALE backlog implementation off this tier's verdicts.
An unvalidated verifier whose agreement is *asserted* but not *measured against blind ground truth*
reproduces the exact recursive failure Cycle 16 exists to kill — one level up. At S24/S27 a falsely-high
agreement was harmless because the conclusion was the safe "don't trust it" direction. At S28 agreement
will be used to SCALE, so falsely-high agreement propagates straight into the backlog. **Independence
and measured accuracy are load-bearing now.**

### 0.1 The existing instrument and its two real defects (verified from source)

`scripts/probe_accuracy_harness.py` (consumed UNMODIFIED per HC #74; the Build-Runner may build a
hardened SUCCESSOR, not edit this file) contains the current judgment-tier GT derivers:
`gt_class_c`, `gt_class_f_judge`, `gt_class_e_status`. Its own docstring states it measures inter-judge
*agreement*, NOT *accuracy*, and that accuracy-vs-blind-GT is S28's job.

**Defect 1 — there is no J1/J2/J3 trio of independent judges; there are two judges and they are SHARED.**
Every judgment-tier GT entry point (`gt_class_c` L928, `gt_class_f_judge` L993, `gt_class_e_status` L957)
agrees via the SAME two functions:
- `_gt_llm_judge` (L788) — ONE LLM, `GT_JUDGE_MODEL = "claude-sonnet-4-6"` (L61).
- `_gt_code_token_crosscheck` (L855) — ONE deterministic token grep.

So the "diverse, structurally-independent agreeing judges" are exactly **1 LLM + 1 grep**, and all three
class derivers call the identical two functions. The LLM judge and the grep cross-check do read
different code paths (good), but: (a) it is a *pair*, not a *quorum*; (b) the grep cross-check is a weak
signal (token-presence, not behavioral); (c) the two functions are shared verbatim across c/e/f, so any
systematic error in `_gt_llm_judge` correlates across the whole tier. At S24 this was immaterial because
the verdict direction was the safe one (CONTESTED→NOT-VALIDATED). For S28-as-scaling-input it is the
independence defect to fix. **The Build-Runner MUST replace the 1-LLM+1-grep pair with a genuinely
diverse quorum (§A).**

**Defect 2 (carries the S27 FLAG, §F).** `scripts/na_rederivation_accuracy_validator.py` is the
validate-the-validator EXEMPLAR (balanced labeled fixtures authored independently of the detector →
classify → P/R/FNR → independent 2nd instrument, different model+method → agreement → emit json).
Its construct is correct and reusable, but it has two flaws the S28 harness must not inherit (see §F).
Critically it used **only n=12 fixtures** (`run_arm1`, `labels.json`) — too few to power an accuracy
estimate (§B).

---

## A. The verifier-of-record (judgment tier)

The Build-Runner builds a NEW successor verifier (e.g. `scripts/judgment_tier_verifier.py`) that does
NOT edit the frozen harness. It MAY consume the harness's UNMODIFIED helpers where they are genuinely
independent, but it MUST provide a genuine quorum, not the 1-LLM+1-grep pair.

### A.1 The diverse-judge ensemble (genuine independence — different models AND different code paths)

The ensemble is **three structurally-independent judges**, J1/J2/J3, each rendering an
implemented / not-implemented / abstain verdict for one judgment-tier spec from its spec-of-record text
+ its embodiment code:

- **J1 — code-reading LLM judge, model A** (e.g. `claude-sonnet-4-6`). Reads the embodiment code +
  the spec's acceptance prose; answers "does this code behave as the prose intends?" Distinct prompt
  authored for this judge. (May reuse the harness's `_gt_llm_judge` UNMODIFIED as J1 — it is already
  the sonnet code-reader.)
- **J2 — code-reading LLM judge, model B** (a DIFFERENT model family/version than J1, e.g.
  `claude-haiku-4-5` or `claude-opus-*`; model id pinned + disclosed). A SEPARATELY authored prompt
  (different framing than J1 — e.g. contract-auditor frame vs. behavioral-intent frame). **Different
  model AND different prompt AND a separate function body** — it must NOT call J1's function.
- **J3 — non-LLM structural judge** (different *kind* of signal entirely): a deterministic analyzer
  over the embodiment — e.g. obligation-token + control-flow presence in the named embodiment files
  (does the code contain the verbs the prose commits: emit/fire/gate/enforce/validate/block, wired into
  a call path, not just a comment), authored as its own function (the existing
  `_gt_code_token_crosscheck` is the seed but should be strengthened from token-presence to
  call-path-presence). J3 shares NO code with J1/J2.

**Independence requirement (BINDING, the load-bearing change):** J1, J2, J3 MUST share NO extraction,
prose-window, or spec-parsing code path. Each judge independently resolves the spec-of-record source,
reads its own prose window, and reads its own embodiment slice. A single shared "read the spec and
extract the window" helper feeding all three would make their agreement correlated-by-construction —
the exact trap. The Build-Runner provides a `--independence-self-test` that asserts (by AST/import
inspection, mirroring the harness's `--self-test` pattern) that J1's, J2's, and J3's function bodies do
not transitively call a shared extraction/parse function and that J1≠J2 model id. This self-test emits
`judges_share_no_code_path: true/false` and the acceptance gate (§H) BLOCKS on false.

### A.2 Agreement → verdict mapping + conservative fail-safe

Per spec, collect (J1, J2, J3) ∈ {implemented, not_implemented, abstain}³.

- **VALIDATED-IMPLEMENTED** iff **all three non-abstaining judges agree `implemented`** AND at least
  J1 and J2 (the two independent reasoners) are non-abstaining. (Unanimity among non-abstainers, with a
  ≥2-reasoner floor.)
- **VALIDATED-NOT-IMPLEMENTED** iff all non-abstaining judges agree `not_implemented` with the same
  ≥2-reasoner floor.
- **CONTESTED → NOT-VALIDATED (fail-safe)** in EVERY other case: any disagreement, any insufficient
  quorum (fewer than 2 reasoners non-abstaining), any unparseable/refused/no-key judge. This mirrors
  the existing harness fail-safe (`gt_class_c` returns CONTESTED on `judge_label != xcheck_label`). The
  fail-safe is conservative on the SCALING direction: an implemented spec wrongly CONTESTED costs a
  re-look; a not-implemented spec wrongly marked implemented ships an unbuilt spec into "done" — the
  Cycle-16 failure. So the verdict mapping is asymmetric only toward CONTESTED, never toward
  IMPLEMENTED.
- **NEVER tune the judges to agree.** No prompt, threshold, or model is changed to raise the agreement
  rate. Disagreement is surfaced and counted, not resolved (HC; §C, §G).

The verifier is run **blind to the ground-truth labels** (§B) — it produces verdicts from spec+code
alone; the GT comparison happens only afterward in the accuracy harness (§C).

---

## B. The blind, powered, structurally-independent ground-truth process (the heart of S28)

The verifier's accuracy is measured against ground-truth labels produced by a process **structurally
independent of the verifier** (different source, different logic) with **no human in the close path**
(#25/#61). The GT labels must NOT be fixtures written to make the verifier pass.

### B.1 Chosen GT mechanism: construct-by-design spec↔code pairs with labels known by construction
(primary), corroborated by an independent partial behavioral oracle on the real specs (secondary)

After weighing the three options the prompt offers, the design uses **two GT arms** — the same
two-arm shape as the S27 exemplar but SCALED and POWERED, and with the construct-validity limitation
named explicitly:

**GT Arm 1 — construct-by-design labeled pairs (powered; labels true by construction; blind to verifier).**
Author a balanced corpus of **N = 60** synthetic spec↔code pairs (justification below), each a
(spec-of-record prose fragment, embodiment code file) pair whose true label is **known by construction**
because the pair was *built* implemented or *built* not-implemented:
- **30 IMPLEMENTED pairs:** the embodiment code genuinely does what the prose commits (the behavior is
  present and wired into a call path).
- **30 NOT-IMPLEMENTED pairs:** the prose commits a behavior the embodiment plausibly *looks* like it
  addresses (same vocabulary, a stub/comment/wrong-thing) but does NOT actually do — i.e. adversarial
  near-misses, the case that defeats token-matching. This stratum is what forces the verifier to read
  behavior, not keywords.
- Stratify across the four spec classes present in the judgment tier (DesignDecision, MethodologyCommitment,
  AgentContract-without-emit, Schema-without-conforming-instance) so accuracy is reported per stratum,
  not just pooled.
- Labels live in a `labels.json` authored **independently of the verifier's logic** and the corpus is
  reusable authored test data (like the existing `fixtures/**`), NOT a human decision in the live close
  path. The verifier sees ONLY the (prose, code) pairs; it never sees `labels.json`. The harness reads
  `labels.json` only AFTER collecting verifier verdicts.

**GT Arm 2 — independent partial oracle on a blind random sample of the REAL judgment-tier specs
(construct-validity bridge).** Draw a **seeded, disclosed, blind random sample of n = 30** real
judgment-tier spec_iris (seeded shuffle over the sorted spec_id list, exactly the
`_c_blind_sample_ids` discipline already in the harness, L916). For each, derive an *independent
partial label* the verifier is NOT shown, using a DIFFERENT logic than any verifier judge — e.g. a
behavioral/usage oracle: does the embodiment's named symbol get *invoked* anywhere in the codebase or
test suite (call-graph / import-and-reference, not the verifier's intent-judgment)? This oracle is
partial (it labels confidently only where invocation evidence is unambiguous; elsewhere it abstains and
those specs are excluded from Arm-2 accuracy, disclosed). Arm 2 is the bridge that tests whether Arm-1
accuracy transfers to real specs (§D residual).

### B.2 Powering N (justify the sample + report resulting confidence)

The accuracy estimate is a proportion (precision / recall on the implemented class). For a binomial
proportion, the 95% Wald/Wilson half-width at the worst case p=0.5 is ≈ `0.98/√N`:

| N (per relevant denominator) | ≈95% CI half-width on a proportion |
|---|---|
| 12 (S27 — too low) | ±0.28 |
| 30 | ±0.18 |
| 60 | ±0.13 |
| 100 | ±0.10 |

S27's n=12 yields ±0.28 — so its 0.6 precision was indistinguishable from anything in [0.32, 0.88]:
**no power to assert a count**, which is exactly why S27 honestly refused one. S28 sets **Arm-1 N = 60**
(30 implemented / 30 not), giving ≈±0.13 on each of precision and recall — enough to *distinguish*
"clearly beats the 0.6 baseline" from "does not," which is the decision S28 must support, while staying
authorable by a Build-Runner in one session. Arm-2 n = 30 (±0.18) is the lower-powered transfer check,
disclosed as such; it tests *direction of transfer*, not a precise real-population accuracy. **If the
Build-Runner can author more Arm-1 pairs cheaply, N may rise (disclose actual N + recomputed CI); N
must NEVER fall below 40** (the gate, §H, asserts `gt_sample_n >= 40`). Report the realized N and the
realized CI half-width in the output artifact (§G).

### B.3 Blindness + no-human-in-close-path (structural)

- The verifier is executed and its per-spec verdicts written to disk BEFORE `labels.json` / the Arm-2
  oracle is read by the accuracy harness. The harness asserts ordering (verdicts file mtime/lock < GT
  read) and asserts the verifier process received no GT path argument — emitting
  `gt_labels_blind_to_verifier: true/false`.
- No interactive prompt, no Rex-disposition argument, no manual-override flag anywhere in the verify or
  accuracy-compute path (mirror `close_verdict`'s 0-human-input signature discipline,
  `validation_tier_verdict.py` L189 + `--inspect-human-inputs`). The accuracy harness emits
  `no_human_in_close_path: true/false`; the gate BLOCKS on false. Human audit is strictly after-the-fact
  and read-only.

### B.4 Named construct-validity limitation (the disclosed residual R — see also §D)

**Construct-validity limitation, stated explicitly:** accuracy measured on Arm-1's *constructed* pairs
may not transfer to the real ~194 judgment-tier specs, because constructed near-misses are authored to
be adjudicable and the real specs are messier (vaguer prose, multi-file embodiments, partial
implementations). Arm-2 partially bridges this but is itself partial (it abstains on ambiguous specs)
and lower-powered (n=30). **The residual R is: "verifier accuracy is measured on N constructed pairs +
n real-sample partial-oracle agreements; its accuracy on the full real judgment tier is bounded by
that, not proven equal to it."** R is disclosed in the output artifact and may NOT be silently dropped
(§D, §G).

---

## C. The accuracy harness

A NEW harness (e.g. `scripts/judgment_tier_accuracy.py`) that consumes the verifier's blind verdicts +
the GT (Arm 1 + Arm 2) and computes, for the **implemented** class:

- **precision** = TP / (TP+FP), **recall** = TP / (TP+FN), **FNR** = FN / (TP+FN), plus TN/FP-rate and
  raw confusion counts — reported per stratum (the 4 spec classes) AND pooled, with the realized 95% CI
  half-width per §B.2.
- **Inter-judge agreement reported SEPARATELY from accuracy** (a distinct field block). Agreement is a
  property of the ensemble (how often J1=J2=J3); accuracy is agreement-with-GT. Conflating them is the
  S24/S27 error this whole cycle exists to kill. The artifact carries both, clearly labelled, never
  merged into one "the verifier is X% good" number.
- The verifier is run **blind** to GT (§B.3).

**Trustworthiness bar (beat-and-prove the 0.6 baseline):** the judgment tier may be called
"now-trustworthy enough to gate scaling" ONLY if, on Arm 1, the lower bound of the 95% CI on
**precision for the implemented class exceeds the S27 baseline of 0.60** (i.e. `precision_CI_low > 0.60`,
not merely a point estimate above 0.6) AND recall is disclosed (a high-precision/low-recall verifier is
still usable for scaling — it under-claims implemented, which is the safe direction — but recall must be
stated so the un-adjudicated remainder is visible). **If the bar is not met, that is an honest finding:
the judgment tier stays NOT-YET-TRUSTWORTHY**, the artifact says so, and no build-queue count is emitted
(§G). **Never tune the judges to agree or to hit the bar** (HC). The harness re-runnable by an
independent operator must reproduce the same numbers (deterministic GT read; LLM nondeterminism handled
by pinning temperature=0 / disclosing any residual variance).

---

## D. The disclosed irreducible residual

Judgment-tier specs have NO execution oracle — that is the definition of the tier. Therefore:

- **"Validated" here means "diverse independent judges agree AND the verifier's accuracy is measured
  above the bar, residual R disclosed" — it does NOT mean "proven correct."** A judgment-tier
  VALIDATED-IMPLEMENTED verdict is a high-confidence judgment, not a proof.
- The output artifact MUST disclose R (the §B.4 construct-validity gap + the LLM-judgment-not-execution
  gap). The spec **FORBIDS** any uniform claim of the form "the verifier is X% accurate over the
  judgment tier with no residual." That uniform claim is the substitution one level up. The acceptance
  gate (§H) asserts `residual_R_disclosed: true` and a lint that no "X% accurate, no residual / proven
  correct / 100%" string is emitted.

---

## E. Vertical slice (prove it works small before trusting it on the full ~194–203)

Before the verifier is run/trusted on the full judgment tier, the Build-Runner runs a **small
end-to-end slice**: pick a handful (≈5–8) of real judgment-tier specs spanning ≥3 of the 4 strata, run
J1/J2/J3 → verdict mapping → accuracy comparison against whichever of those specs Arm-2's oracle can
confidently label (+ any that overlap Arm-1's construct pattern). Demonstrate end-to-end that: judges
fire independently, the agreement→verdict mapping produces sane verdicts, the fail-safe fires on a
planted disagreement, and the accuracy number is computed with its CI. This slice proves the machine
runs with its measured accuracy on real input BEFORE the full-tier run — the same "vertical slice
first" discipline used at S25 (1 spec, execution-proven, nothing tuned). The slice result is recorded;
it is NOT a closure claim.

---

## F. Carry the S27 FLAG fixes (if the accuracy-validator pattern is reused)

The S28 accuracy harness reuses the *pattern* of `scripts/na_rederivation_accuracy_validator.py`. If
that script (or its shape) is reused, the Build-Runner MUST fix:

- **F1 — docstring import claim must match actual imports.** The validator's `#34 GUARD` docstring
  (L28-29) states: *"this module deliberately does NOT `import na_direction_rederivation` for any
  reader … no `import na_direction_rederivation`."* But the module DOES `import na_direction_rederivation
  as instrument_a` (L49) and `import spec_extraction_pipeline as sep` (L45). The intended meaning is
  narrower — Arm 1 *deliberately runs the instrument-under-test* (so importing it is correct there), and
  Arm 2 must NOT import its *reader* functions. The docstring as written is false and self-contradicting.
  **Fix: rewrite the guard to state the true invariant — "Arm 1 runs instrument_a (the
  instrument-under-test, by design); Arm 2 imports NO reader function of instrument_a (`nd.e1_prime` /
  `nd.e2_prime` are never called in the Arm-2 path)" — and make the module's `--self-test` assert
  exactly that narrower invariant.** The S28 harness's own independence self-test (§A.1) must likewise
  state precisely which imports are intended and which are forbidden.
- **F2 — Arm-1 metric must be unambiguous AND-vs-OR.** The S27 Arm-1 prediction is
  `pred = e1.needs_implementation OR e2.needs_implementation` (L100) — an **OR** (conservative:
  positive if *any* reader flags it), but the surrounding comment and disposition vocabulary
  ("both readers say needs", "disagreement") blur whether the positive prediction is AND or OR.
  **For S28: state explicitly that the ensemble's VALIDATED verdict uses AND (unanimity among
  non-abstainers, §A.2) while a "needs-a-look / CONTESTED" surfacing uses OR — and label each metric
  with which operator produced it.** Do not report a single number whose AND/OR semantics is ambiguous.
- **F3 — mining noise (S27 Mining 79 = noisy candidates, not confirmed specs) is NOT in S28 scope.**
  Noted forward only; S28 does not consume or re-derive the mining list.

---

## G. Output-artifact discipline

The verifier's result artifact (`outputs/judgment_tier_verifier_run.json` + a human-facing summary)
MUST:

1. **Lead with an honest range/number, not a raw point field.** The first/headline field is a tier-level
   honest statement carrying the realized N, the precision CI (interval, not point), recall, the
   agreement-vs-accuracy distinction, and the trustworthiness verdict (TRUSTWORTHY / NOT-YET-TRUSTWORTHY).
   The raw per-spec verdicts and raw confusion counts live below the headline, not as the lead.
2. **Emit a "now-trustworthy build-queue count" ONLY if the measured accuracy clears the §C bar.** If the
   bar is not met, the artifact emits NO build-queue count — it emits the honest "judgment tier stays
   not-yet-trustworthy at precision_CI_low=<x> ≤ 0.60" finding. (This is the S27 lesson encoded: the
   Coach R3 BLOCKED the comfortable "144" point-number; the artifact must not re-introduce a point count
   the accuracy doesn't support.)
3. Carry inter-judge agreement and accuracy as **separate, clearly-labelled** blocks (§C).
4. Disclose residual R (§D) and forbid the uniform "X% accurate, no residual" claim (§D lint).

---

## H. Contract sections to fill (pointers; filled in the three contract files)

This build element's binary acceptance is encoded in `ARTIFACT_CONTRACT.md §13`,
`RUNTIME_EMIT_SPEC.md §13`, and `ACCEPTANCE_CRITERIA.md §13` (APPEND-only; prior BE sections
unchanged). The load-bearing binary assertions are:

- `gt_labels_blind_to_verifier == true`
- `judges_share_no_code_path == true` (the §A.1 independence fix)
- `gt_sample_n >= 40` (powered; §B.2 — target 60 Arm-1 + 30 Arm-2)
- `accuracy_measured_against_independent_gt == true`
- `precision_ci_low_for_implemented_class` reported (interval, not point) — TRUSTWORTHY iff `> 0.60`
- `inter_judge_agreement_reported_separately_from_accuracy == true`
- `residual_R_disclosed == true`
- `no_human_in_close_path == true`
- `judges_not_tuned_to_agree == true` (attested: judge prompts/models/thresholds byte-identical before
  and after the accuracy run; `git diff --stat` empty on judge code across the run)
- `frozen_paths_unmodified == true` (`scripts/probes/probe_spec_impl_fidelity.py`, floors 0.20/0.80/0.20,
  `fixtures/**`, gap-list outputs, `probe_accuracy_harness.py` consumed-by-others interface — all
  byte-identical; the verifier is a NEW successor file)

---

## I. Honest disclosure (what this design is and is NOT)

This is the design for ONE instrument for ONE tier. It does NOT implement any backlog spec; it does NOT
close the spec→implementation gap; it does NOT claim "done" / "100%" / "gap-closed." Its deliverable is
a judgment-tier verifier whose OWN accuracy is measured against blind, powered, structurally-independent
ground truth, with the residual disclosed — so that S29+ can decide whether the judgment-tier verdicts
are trustworthy enough to scale against, or whether (the honest alternative) the tier stays not-yet-
trustworthy and scaling waits. The biggest thing this design does NOT prove is that accuracy measured on
constructed/sampled ground truth transfers to the full real ~194 judgment-tier specs — that gap is the
disclosed residual R.
