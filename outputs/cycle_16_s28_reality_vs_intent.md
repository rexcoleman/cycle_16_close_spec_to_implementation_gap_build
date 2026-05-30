# Cycle-16-S28 — reality-vs-intent diagnostic (judgment-tier verifier build)

**Date:** 2026-05-30. **Author:** Cycle-16-S28 downstream Coach (DP#43 R3; every check re-run independently per HC#75 — self-tests, accuracy harness, frozen-path diff, GT pairs hand-sampled, Arm-2 inspected). The Build-Runner this session RAN everything (unlike S27, which built but did not run).

## What was ASKED (intent)
Build + accuracy-validate the judgment-tier verifier for the ~194–203 non-probe-checkable specs, so its verdicts can be trusted to **SCALE backlog implementation in S29+**. Trustworthy = "multiple independent judges that must agree, whose OWN accuracy is measured against blind, powered, structurally-independent ground truth, beating the S27 0.6-precision baseline — or an honest NOT-YET."

## What was actually BUILT + MEASURED (reality)
- **A genuine 3-judge ensemble, verified independent.** J1 (claude-sonnet LLM, contract-auditor), J2 (claude-haiku LLM, skeptical-default — different model AND different prompt AND separate body), J3 (deterministic AST/structural). Coach re-ran `--independence-self-test` → `share_private_reader=False`, exit 0. This FIXES the real defect the RP found + Coach confirmed in source: the prior `probe_accuracy_harness` "diverse judges" were **1 sonnet LLM + 1 grep shared verbatim** across gt_class_c/e/f (L788/L855) — a pair, not a quorum, correlated by construction.
- **Quorum = UNANIMITY_AND** (VALIDATED-IMPLEMENTED iff all non-abstainers agree + ≥2 LLM reasoners; everything else → CONTESTED, asymmetric only toward the safe direction). F2 fixed (AND-vs-OR explicit). F1 fixed (false `#34 GUARD` docstring not copied; true narrow invariant stated).
- **It RAN end-to-end:** vertical slice (6 real specs, planted-disagreement fail-safe fires=True, human_inputs=0); full 203-spec run; accuracy harness over a powered GT.
- **Construct-GT accuracy (Arm-1, N=60, hand-verified genuine):** implemented-class precision **1.0**, 95% Wilson CI **[0.886, 1.0]**, recall 1.0, FNR 0.0; per-stratum all clean. Coach hand-read pairs — the adversarial near-misses are REAL (e.g., an `audit_logger` near-miss emits `audit.entry` with `prev_hash` present but hardcoded `"0"*64` so it never chains; a token-matcher passes it, a behavior-reading judge correctly fails it). So precision 1.0 means the judges read behavior, not keywords — a meaningful result.
- **Anti-gaming, all re-run by Coach, exit 0:** independence; blind-at-scoring (verdicts written before labels read); not-tuned-to-agree (judge code hash-frozen pre-GT); 0 human inputs; additive-only (frozen paths byte-identical — `git diff --quiet` exit 0). Forbidden-string lint clean.

## The GAP (reality minus intent) — the honest R3 finding
**The verifier's accuracy on the REAL judgment tier is UNMEASURED.** Arm-2 — the construct-validity bridge that was supposed to test transfer from synthetic pairs to real specs — **abstained on 30/30** sampled real specs, because its invocation/symbol-trace oracle needs a *code* embodiment, and the real judgment tier is by definition mostly non-code decision/methodology TEXT. So:
- precision 1.0 holds on **60 builder-authored construct pairs** (genuine, but same-session shared-author → construct-validity risk, disclosed);
- **zero** real judgment-tier specs received an independent ground-truth label;
- therefore the verifier's real-tier precision/recall is **not established**.

### Coach R3 CORRECTION (substantive — honest-accounting; same class as S27 C1)
The build artifact is internally honest (its `residual_R` and headline both state Arm-2 abstained 30/30 and real-tier transfer is UNMEASURED) but **internally contradictory** — it still sets `trust_decision=TRUSTWORTHY` and emits a `now_trustworthy_build_queue_count`. Corrected:

- **C1 — "TRUSTWORTHY" is qualified, not unconditional.** The verifier is **construct-GT-trustworthy** (precision CI low 0.886 > 0.60 on genuine adversarial pairs) but **NOT-YET-demonstrated on the real tier** (Arm-2 0/30). An unqualified TRUSTWORTHY would license S29 to scale against verdicts whose real-tier accuracy was never measured — the exact recursive failure one level up.
- **C2 — strike the "now-trustworthy build-queue count."** It is wrong twice: (a) `26` is the **IMPLEMENTED** count, not the build queue — the work-to-do set is the **~177 not-implemented (72 VALIDATED-NOT-IMPLEMENTED + 105 CONTESTED→conservative-not)**; (b) no count off the full 203 run is trust-validated, because real-tier accuracy is unmeasured. Report the full-run distribution **26 IMPLEMENTED / 72 NOT-IMPLEMENTED / 105 CONTESTED** explicitly tagged *real-tier-accuracy UNMEASURED*, not as a trustworthy build-queue size.
- **C3 — the real open problem S28 surfaced:** the chosen Arm-2 oracle is **structurally incapable** of labeling the real judgment tier (no code symbol on text-embodiment specs). Real-tier accuracy measurement is therefore **unsolved**, not merely "residual disclosed." S29 must build a real-tier GT that works on text embodiments (a different independent labeling method) **before** any scaling — scaling against the current verdicts is forbidden until then.

## Net
**BUILD PASS** (the apparatus is real, independent, behavior-reading, ran end-to-end, construct-validated at precision 1.0, all guards re-run clean) **with a substantive framing correction**: S28 produced a verifier that is **trustworthy on constructed adversarial pairs but whose real-judgment-tier accuracy is UNMEASURED** — an honest NOT-YET on the thing that gates scaling. Real apparatus progress; the scaling-readiness question is not yet answered. **NOT closed by deferral** (real code + real measurement this session). The S27 lesson held: the comfortable "TRUSTWORTHY → here's your build-queue count" was caught and corrected, exactly as the cycle is designed to do. Cycle 16 OPEN.

## Minor flags (FLAG+CARRY, non-blocking)
- F-S28-1: J1 model id is `claude-sonnet-4-5` (spec named sonnet-4-6); it resolved and produced verdicts (per-stratum precision computed on real J1+J2 output), so independence (sonnet≠haiku) holds; pin the intended id at S29 if reused.
- F-S28-2: contract section numbering — spec §H references "§13"; the RP appended as the next BE section. Cosmetic; the binary assertions are present and were re-checked.
