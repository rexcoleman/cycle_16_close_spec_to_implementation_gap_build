#!/usr/bin/env python3
"""Cycle-16-S28 BE-JTV — accuracy harness: run the verifier BLIND over ground truth.

Design spec: docs/judgment_tier_verifier_mechanism.md §B/§C. This is the validate-the-validator
step: the judgment-tier verifier (judgment_tier_verifier.py) is an UNPROVEN instrument. S29+ will
SCALE off its verdicts, so its OWN accuracy against blind, powered, structurally-independent
ground truth is the whole point. We MEASURE it; we do NOT trust it because it agrees with itself.

TWO GT ARMS (the S27 two-arm shape, SCALED + POWERED + with the construct-validity residual named):

  Arm 1 — construct-by-design pairs (N=60; 30 implemented / 30 not), labels TRUE BY CONSTRUCTION,
    authored blind to the verifier (build_jtv_gt_arm1.py + labels.json). The verifier's judges run
    on the (prose, code) pair; labels.json is read ONLY AFTER all verdicts are collected and
    written to disk (blindness asserted by write-before-read ordering + verifier got NO label path).

  Arm 2 — independent partial INVOCATION oracle on a blind random sample (n=ARM2_N) of the REAL
    judgment-tier specs. The oracle uses a DIFFERENT logic than any verifier judge: is the
    embodiment's named symbol actually IMPORTED/REFERENCED/CALLED from another file in the
    codebase? It is PARTIAL — it labels confidently only on unambiguous invocation evidence and
    ABSTAINS otherwise (those specs excluded from Arm-2 accuracy, disclosed). Arm 2 is the
    construct-validity BRIDGE: does Arm-1 accuracy transfer to real specs? It shares NO code with
    any verifier judge (its own _arm2_invocation_oracle body).

S27 FLAG FIXES carried:
  F1 — the TRUE narrow invariant for THIS harness: it runs the instrument-under-test
       (judgment_tier_verifier) BY DESIGN, so importing it is CORRECT. The forbidden thing is
       letting GT LABELS depend on the verifier — labels.json is true-by-construction and the
       Arm-2 oracle shares no judge code. No false "imports nothing" docstring is copied.
  F2 — every metric is labelled with its operator: the verifier's VALIDATED-IMPLEMENTED verdict
       uses AND (unanimity); the accuracy here scores that AND-verdict. We do NOT mix in an OR
       "needs-a-look" number.

TRUST DECISION (pre-registered, FROZEN before the GT run): TRUSTWORTHY iff the lower bound of the
95% Wilson CI on implemented-class precision (Arm 1) is STRICTLY > 0.60 (beats the S27 0.6
baseline). Else NOT-YET-TRUSTWORTHY — an explicit PASSING honest outcome. Judges/quorum/thresholds
are NOT tuned to clear it (JTV-7; git-diff attestation field).

ADDITIVE ONLY. Output: outputs/judgment_tier_verifier_accuracy.json (+ events jsonl).
"""
from __future__ import annotations

import json
import math
import os
import pathlib
import random
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")
sys.path.insert(0, HERE)

import judgment_tier_verifier as jtv  # the instrument under test (BY DESIGN; F1)

GT_DIR = os.path.join(HERE, "structural_prevention", "fixtures", "judgment_tier_gt")
LABELS = os.path.join(GT_DIR, "labels.json")
PAIRS = os.path.join(GT_DIR, "pairs")
EVENTS = os.path.join(OUTPUTS, "judgment_tier_verifier_events.jsonl")
OUT = os.path.join(OUTPUTS, "judgment_tier_verifier_accuracy.json")
VERDICTS_BLIND = os.path.join(OUTPUTS, "judgment_tier_verifier_arm1_blind_verdicts.json")

NAMESPACE = "cycle_16.s28.judgment_tier_verifier"
SCHEMA_VERSION = "0.1"
ARM2_SEED = 28
ARM2_N = 30
S27_BASELINE = 0.60


def _now():
    return datetime.now(timezone.utc).isoformat()


def _emit(event_class, payload, run_id):
    rec = {"schema_version": SCHEMA_VERSION, "namespace": NAMESPACE,
           "event_class": event_class, "timestamp": _now(), "run_id": run_id, "payload": payload}
    with open(EVENTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def wilson_ci(k, n, z=1.96):
    """95% Wilson score interval. Returns (low, high, halfwidth)."""
    if n == 0:
        return (None, None, None)
    p = k / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = (z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n))) / denom
    return (max(0.0, center - margin), min(1.0, center + margin), margin)


def metrics(cell):
    tp, fp, fn, tn = cell["tp"], cell["fp"], cell["fn"], cell["tn"]
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    fnr = fn / (tp + fn) if (tp + fn) else None
    p_low, p_high, p_hw = wilson_ci(tp, tp + fp) if (tp + fp) else (None, None, None)
    r_low, r_high, r_hw = wilson_ci(tp, tp + fn) if (tp + fn) else (None, None, None)
    return {"tp": tp, "fp": fp, "fn": fn, "tn": tn, "precision": precision, "recall": recall,
            "fnr": fnr, "precision_ci_95": [p_low, p_high], "precision_ci_halfwidth": p_hw,
            "recall_ci_95": [r_low, r_high], "recall_ci_halfwidth": r_hw}


# =========================================================================
# Arm 1 — run the verifier's judges BLIND over the construct-by-design pairs.
# A synthetic verifier-row is built per pair (prose=spec.md content, embodiment=code.py).
# The verifier never sees labels.json.
# =========================================================================
def run_arm1_blind(run_id):
    client = jtv._client()
    listing = sorted(os.listdir(PAIRS))  # listed from FILESYSTEM, not from labels
    bases = sorted({f.rsplit(".spec.md", 1)[0].rsplit(".code.py", 1)[0]
                    for f in listing if f.endswith((".spec.md", ".code.py"))})
    verdicts = {}
    for base in bases:
        spec_path = os.path.join(PAIRS, base + ".spec.md")
        code_path = os.path.join(PAIRS, base + ".code.py")
        if not (os.path.exists(spec_path) and os.path.exists(code_path)):
            continue
        prose = open(spec_path, encoding="utf-8").read()
        m = re.search(r"_(a_agent_contract|b_schema|c_design_decision|d_methodology_commitment)_", base)
        stratum = m.group(1) if m else "unknown"
        # row shaped exactly like a real verifier row: scan_rec=None (so judges use commitment_text),
        # embodiment_path=the pair code file, commitment_text=the spec prose.
        row = {"spec_iri": f"GT:{base}", "spec_class": stratum, "commitment_text": prose,
               "scan_rec": None, "embodiment_path": code_path, "name": base,
               "committed_runtime_emit_class": None}
        j1, j1ev = jtv.judge_j1_llm(row, client)
        j2, j2ev = jtv.judge_j2_llm(row, client)
        j3, j3ev = jtv.judge_j3_structural(row)
        qv, failsafe, n_reasoners = jtv.quorum(j1, j2, j3)
        verdicts[base] = {"stratum": stratum, "j1": j1, "j2": j2, "j3": j3,
                          "quorum_verdict": qv, "failsafe_fired": failsafe,
                          "n_reasoners_nonabstain": n_reasoners,
                          "j1ev": j1ev, "j2ev": j2ev, "j3ev": j3ev}
    json.dump({"run_id": run_id, "generated": _now(), "verdicts": verdicts,
               "note": "written BEFORE labels.json read (blindness ordering proof); verifier got NO label path"},
              open(VERDICTS_BLIND, "w", encoding="utf-8"), indent=2)
    return verdicts, os.path.getmtime(VERDICTS_BLIND)


def score_arm1(verdicts, blind_mtime):
    """Read labels.json (AFTER verdicts written) and score implemented-class P/R/FNR."""
    label_read_time = datetime.now(timezone.utc).timestamp()
    blind_ordering_ok = (blind_mtime <= label_read_time)
    lab = json.load(open(LABELS, encoding="utf-8"))["labels"]

    def pred_impl(qv):
        return qv == "VALIDATED-IMPLEMENTED"

    strata, pooled, rows = {}, {"tp": 0, "fp": 0, "fn": 0, "tn": 0}, []
    for base, meta in sorted(lab.items()):
        v = verdicts.get(base)
        if v is None:
            continue
        gt = meta["true_label"] == "implemented"
        pred = pred_impl(v["quorum_verdict"])
        st = meta["stratum"]
        cell = strata.setdefault(st, {"tp": 0, "fp": 0, "fn": 0, "tn": 0})
        k = "tp" if (pred and gt) else "fp" if (pred and not gt) else "fn" if (not pred and gt) else "tn"
        cell[k] += 1
        pooled[k] += 1
        rows.append({"base": base, "stratum": st, "gt": meta["true_label"],
                     "quorum_verdict": v["quorum_verdict"], "pred_implemented": pred,
                     "correct": pred == gt, "j1": v["j1"], "j2": v["j2"], "j3": v["j3"]})
    return pooled, strata, rows, bool(blind_ordering_ok)


def inter_judge_agreement(verdicts):
    """Agreement (how often J1==J2==J3 / J1==J2 among non-abstainers) — reported SEPARATELY
    from accuracy (JTV-5). Conflating them is the S24/S27 error this cycle exists to kill."""
    full3 = pair12 = tot3 = totp = 0
    for v in verdicts.values():
        nonab = [x for x in (v["j1"], v["j2"], v["j3"]) if x != "abstain"]
        if len(nonab) == 3:
            tot3 += 1
            if len(set(nonab)) == 1:
                full3 += 1
        if v["j1"] != "abstain" and v["j2"] != "abstain":
            totp += 1
            if v["j1"] == v["j2"]:
                pair12 += 1
    return {"unanimous_3judge_agreement_rate": (full3 / tot3) if tot3 else None,
            "n_specs_all3_nonabstain": tot3,
            "j1_j2_reasoner_agreement_rate": (pair12 / totp) if totp else None,
            "n_specs_both_reasoners_nonabstain": totp,
            "NOTE": "agreement is reported SEPARATELY from accuracy; it is NOT a quality number"}


# =========================================================================
# Arm 2 — blind random real-sample + independent partial INVOCATION oracle.
# =========================================================================
def _arm2_blind_sample(seed, n):
    rows = jtv.load_judgment_tier()
    embodied = [r for r in rows if r.get("embodiment_path")
                and os.path.exists(os.path.expanduser(r["embodiment_path"]))]
    ids = sorted(r["spec_iri"] for r in embodied)
    rng = random.Random(seed)
    rng.shuffle(ids)
    chosen = set(ids[:min(n, len(ids))])
    by = {r["spec_iri"]: r for r in embodied}
    return [by[i] for i in sorted(chosen)], seed, len(embodied)


_SEARCH_ROOTS = [os.path.join(os.path.expanduser("~"), "Moonshots_Career_Thesis_v2"), PROJECT_ROOT]


def _arm2_invocation_oracle(row):
    """Independent PARTIAL behavioral oracle. ('implemented'|'not_implemented'|'abstain', ev).
    Logic DIFFERENT from every verifier judge: is the embodiment's symbol IMPORTED/CALLED from a
    DIFFERENT file? Confident only on code embodiments; abstains on docs/agent-spec/schema where
    'invocation' is not a code call."""
    emb = row.get("embodiment_path")
    if not emb:
        return "abstain", "arm2_abstain: no embodiment"
    p = pathlib.Path(os.path.expanduser(emb))
    if not p.exists():
        return "abstain", "arm2_abstain: embodiment unresolved"
    if p.suffix not in (".py", ".sh"):
        return "abstain", f"arm2_abstain: non-code embodiment ({p.suffix}); invocation undefined"
    stem = p.stem
    name = row.get("name") or stem
    targets = {t for t in {stem, name} if t and len(t) >= 4}
    if not targets:
        return "abstain", "arm2_abstain: no load-bearing symbol name"
    hits = []
    for root in _SEARCH_ROOTS:
        for t in targets:
            try:
                r = subprocess.run(
                    ["grep", "-rIl", "-e", f"import {t}", "-e", f"{t}(", "-e", f"from {t}",
                     "--include=*.py", "--include=*.sh", root],
                    capture_output=True, text=True, timeout=30)
            except (subprocess.TimeoutExpired, OSError):
                continue
            for line in r.stdout.splitlines():
                if os.path.abspath(line) != os.path.abspath(str(p)):
                    hits.append(line)
    hits = sorted(set(hits))
    if hits:
        return "implemented", f"arm2: symbol {stem!r} imported/called from {len(hits)} other file(s)"
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return "abstain", "arm2_abstain: unreadable"
    if "__main__" in body and ("def main" in body or "argparse" in body):
        return "abstain", "arm2_abstain: runnable script, no external ref (invocation ambiguous)"
    if re.search(r"^def \w+", body, re.M):
        return "not_implemented", f"arm2: {stem!r} defines functions but referenced/called nowhere (dead)"
    return "abstain", "arm2_abstain: no clear invocation signal"


def run_arm2(run_id):
    sample, seed, n_embodied = _arm2_blind_sample(ARM2_SEED, ARM2_N)
    client = jtv._client()
    cell = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    abstained, rows = 0, []
    for r in sample:
        oracle, oev = _arm2_invocation_oracle(r)
        if oracle == "abstain":
            abstained += 1
            rows.append({"spec_iri": r["spec_iri"], "oracle": "abstain", "oracle_ev": oev, "scored": False})
            continue
        j1, _ = jtv.judge_j1_llm(r, client)
        j2, _ = jtv.judge_j2_llm(r, client)
        j3, _ = jtv.judge_j3_structural(r)
        qv, _fs, _n = jtv.quorum(j1, j2, j3)
        pred, gt = (qv == "VALIDATED-IMPLEMENTED"), (oracle == "implemented")
        k = "tp" if (pred and gt) else "fp" if (pred and not gt) else "fn" if (not pred and gt) else "tn"
        cell[k] += 1
        rows.append({"spec_iri": r["spec_iri"], "oracle": oracle, "oracle_ev": oev[:120],
                     "quorum_verdict": qv, "pred_implemented": pred, "correct": pred == gt,
                     "j1": j1, "j2": j2, "j3": j3, "scored": True})
    return {"seed": seed, "n_embodied_in_tier": n_embodied, "sample_n": len(sample),
            "scored_n": sum(1 for x in rows if x["scored"]), "abstained_n": abstained,
            "cell": cell, "metrics": metrics(cell), "rows": rows}


def git_diff_judge_code():
    try:
        r = subprocess.run(["git", "diff", "--stat", "--", "scripts/judgment_tier_verifier.py"],
                           cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)
        return (r.stdout.strip() == ""), r.stdout.strip()
    except (subprocess.TimeoutExpired, OSError) as e:
        return False, f"git_error: {e!r}"


def main():
    jtv._load_env()
    run_id = f"jtv_acc_{uuid.uuid4().hex[:8]}"
    if not os.path.exists(LABELS):
        print(json.dumps({"DP44_refuse": f"missing {LABELS}"}))
        sys.exit(2)

    selftest = jtv.independence_self_test()
    if not selftest["pass"]:
        _emit("judgment_tier_verifier.runtime_failure.event",
              {"failure_class": "independence_self_test_fail", "evidence": selftest,
               "recovery_path": "fix judge code-path disjointness before scoring"}, run_id)
        print(json.dumps({"HALT": "independence self-test failed", "selftest": selftest}))
        sys.exit(1)

    arm1_verdicts, blind_mtime = run_arm1_blind(run_id)
    pooled, strata, arm1_rows, blind_ok = score_arm1(arm1_verdicts, blind_mtime)
    pooled_m = metrics(pooled)
    strata_m = {st: metrics(c) for st, c in strata.items()}
    agreement = inter_judge_agreement(arm1_verdicts)
    arm2 = run_arm2(run_id)

    p_ci = pooled_m["precision_ci_95"]
    p_ci_low = p_ci[0] if p_ci and p_ci[0] is not None else None
    trustworthy = bool(p_ci_low is not None and p_ci_low > S27_BASELINE)
    trust_decision = "TRUSTWORTHY" if trustworthy else "NOT-YET-TRUSTWORTHY"

    judge_clean, judge_diff = git_diff_judge_code()
    human_inputs = jtv.verifier_fn_human_inputs()
    arm1_n = pooled["tp"] + pooled["fp"] + pooled["fn"] + pooled["tn"]
    total_gt_n = arm1_n + arm2["scored_n"]

    residual_R = (
        "R (DISCLOSED, irreducible): accuracy is measured on {a1} constructed Arm-1 pairs (labels "
        "true by construction) + {a2} real-sample Arm-2 partial-oracle agreements. Constructed "
        "near-misses are authored to be adjudicable; the real ~194 judgment-tier specs are messier "
        "(vaguer prose, markdown/multi-file embodiments, partial impls — and ~190 of 203 have NO "
        "code embodiment at all, only decision-log/findings text). Arm 2 abstained on {ab} of {an} "
        "sampled real specs (invocation ambiguous / non-code embodiment), so transfer is tested but "
        "NOT proven equal across the full tier. Judgment-tier specs have NO execution oracle by "
        "definition: 'implemented' here = diverse judges agree + measured above the bar, NOT proven "
        "correct."
    ).format(a1=arm1_n, a2=arm2["scored_n"], ab=arm2["abstained_n"], an=arm2["sample_n"])

    if trustworthy:
        build_queue_count = {
            "note": "range, CI-bounded; requires a full --run over the 203 to populate the point",
            "method": "verifier VALIDATED-IMPLEMENTED count on full tier x [precision_ci_low, precision_ci_high]",
            "precision_ci_95": p_ci, "full_tier_run_required": True}
    else:
        build_queue_count = {
            "value": None,
            "reason": (f"NOT-YET-TRUSTWORTHY: implemented-class precision CI lower bound {p_ci_low} "
                       f"<= {S27_BASELINE}; no count emitted (S27 lesson: do not re-introduce a "
                       f"point count the accuracy does not support)")}

    headline = (
        f"trust_decision={trust_decision}: judgment-tier verifier implemented-class precision "
        f"(Arm-1, N={arm1_n} construct GT) = {pooled_m['precision']} with 95% Wilson CI {p_ci} "
        f"(halfwidth {pooled_m['precision_ci_halfwidth']}); recall={pooled_m['recall']}, "
        f"FNR={pooled_m['fnr']}. Bar: precision_ci_low > {S27_BASELINE} -> "
        f"{'MET' if trustworthy else 'NOT MET'}. Inter-judge agreement is reported SEPARATELY "
        f"(not merged into this number)."
    )

    out = {
        "schema_version": SCHEMA_VERSION, "run_id": run_id, "generated": _now(),
        # ---- HEADLINE (leads with range/CI, not a bare point; §G.1) ----
        "trust_decision": trust_decision, "honest_statement": headline,
        "implemented_class_precision": pooled_m["precision"], "precision_ci_95": p_ci,
        "precision_ci_low_for_implemented_class": p_ci_low, "recall": pooled_m["recall"],
        "fnr": pooled_m["fnr"], "gt_sample_n": total_gt_n, "ci95_halfwidth": pooled_m["precision_ci_halfwidth"],
        # ---- inter-judge agreement: SEPARATE block (JTV-5) ----
        "inter_judge_agreement": agreement,
        # ---- accuracy: SEPARATE block ----
        "accuracy": {
            "arm1_construct": {"n": arm1_n, "pooled": pooled_m, "per_stratum": strata_m,
                               "gt_labels_blind_to_verifier": True, "blind_ordering_ok": blind_ok,
                               "blind_proof": "verifier verdicts written to disk BEFORE labels.json read; verifier received NO label path"},
            "arm2_real_sample_partial_oracle": {
                "seed": arm2["seed"], "n_embodied_in_tier": arm2["n_embodied_in_tier"],
                "sample_n": arm2["sample_n"], "scored_n": arm2["scored_n"],
                "abstained_n": arm2["abstained_n"], "metrics": arm2["metrics"],
                "oracle_logic": "behavioral invocation oracle (import/call reference); shares NO code with any verifier judge"},
        },
        # ---- binary contract assertions (§H / JTV) ----
        "judges_share_no_code_path": selftest["judges_share_no_code_path"],
        "j1_model": jtv.J1_MODEL, "j2_model": jtv.J2_MODEL,
        "j1_model_ne_j2_model": selftest["j1_model_ne_j2_model"],
        "accuracy_measured_against_independent_gt": True,
        "inter_judge_agreement_reported_separately_from_accuracy": True,
        "residual_R_disclosed": True, "residual_R": residual_R,
        "no_human_in_close_path": human_inputs == 0, "verifier_fn_human_inputs": human_inputs,
        "judges_not_tuned_to_agree": judge_clean,
        "judge_code_git_diff_stat": judge_diff or "(empty — byte-identical)",
        "quorum_rule": jtv.QUORUM_RULE,
        "quorum_rule_operator": "AND (unanimity among non-abstainers) for VALIDATED-IMPLEMENTED; CONTESTED is conservative fail-safe (S27 FLAG F2)",
        "now_trustworthy_build_queue_count": build_queue_count,
        "s27_baseline_precision": S27_BASELINE,
        # ---- raw rows below the headline (§G.1) ----
        "arm1_rows": arm1_rows, "arm2_rows": arm2["rows"],
        "NOT_a_closure_claim": ("this measures ONE instrument for ONE tier; it does NOT close the "
                                "spec->implementation gap and claims no done/100%/gap-closed"),
    }
    json.dump(out, open(OUT, "w", encoding="utf-8"), indent=2)

    _emit("judgment_tier_accuracy.measure.event",
          {"arm": "arm1_construct", "stratum": "pooled", **{k: pooled[k] for k in ("tp", "fp", "fn", "tn")},
           "precision": pooled_m["precision"], "recall": pooled_m["recall"], "fnr": pooled_m["fnr"],
           "gt_sample_n": total_gt_n, "ci95_halfwidth": pooled_m["precision_ci_halfwidth"],
           "precision_ci_low_for_implemented_class": p_ci_low,
           "gt_labels_blind_to_verifier": True, "judges_not_tuned_to_agree": judge_clean}, run_id)
    _emit("judgment_tier_accuracy.verdict.event",
          {"trustworthy": trustworthy, "honest_statement": headline,
           "inter_judge_agreement": agreement["j1_j2_reasoner_agreement_rate"],
           "residual_R_disclosed": True,
           "now_trustworthy_build_queue_count": (None if not trustworthy else "range_pending_full_run"),
           "no_human_in_close_path": human_inputs == 0}, run_id)

    print(json.dumps({"trust_decision": trust_decision, "implemented_class_precision": pooled_m["precision"],
                      "precision_ci_95": p_ci, "recall": pooled_m["recall"], "fnr": pooled_m["fnr"],
                      "gt_sample_n": total_gt_n, "arm1_n": arm1_n, "arm2_scored_n": arm2["scored_n"],
                      "arm2_abstained": arm2["abstained_n"],
                      "inter_judge_agreement_j1j2": agreement["j1_j2_reasoner_agreement_rate"],
                      "judges_share_no_code_path": selftest["judges_share_no_code_path"],
                      "judges_not_tuned_to_agree": judge_clean, "out": OUT}, indent=2))


if __name__ == "__main__":
    main()
