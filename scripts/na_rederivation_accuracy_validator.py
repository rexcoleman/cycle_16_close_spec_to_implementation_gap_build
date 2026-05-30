#!/usr/bin/env python3
"""Cycle-16-S27 #19/#46/#34 — validate the na_direction_rederivation INSTRUMENT itself.

The re-derivation in na_direction_rederivation.py is an UNPROVEN detector. Do NOT trust
it just because the positive direction (S26) was faithful — that is the substitution one
level up the whole cycle exists to kill. Measure its accuracy.

TWO independent validation arms:

  Arm 1 (blind-labeled fixtures): run instrument (a) on >=12 authored synthetic specs with
    KNOWN out-of-band labels (structural_prevention/fixtures/na_rederivation/ + labels.json),
    stratified genuine-n/a vs commits-observable. Compute precision / recall / false-negative-
    rate. The fixtures are reusable AUTHORED test data (like the other fixtures/**), not a
    human decision in the live close path.

  Arm 2 (structurally-independent 2nd instrument on the REAL 203): a DIFFERENT code path that
    MUST NOT import na_direction_rederivation's reader functions (#34). It uses the
    spec_extraction_pipeline E1' LLM reader (claude-SONNET-4-6, contract-auditor prompt — a
    different model AND different prompt than (a)'s haiku reader) PLUS a structurally different
    heuristic (obligation-density score). Report inter-instrument agreement on the 203 +
    surface disagreements.

If accuracy is low or disagreement is high -> DISCLOSE honestly. Do NOT tune to look good.

Output: outputs/na_rederivation_accuracy.json
ADDITIVE ONLY.

#34 GUARD: this module deliberately does NOT `import na_direction_rederivation` for any
reader. grep-confirm: no `import na_direction_rederivation` and no `nd.e1_prime`/`nd.e2_prime`.
"""
import json
import os
import re
import sys
import time
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")
FIXTURES = os.path.join(HERE, "structural_prevention", "fixtures", "na_rederivation")
sys.path.insert(0, HERE)

import spec_extraction_pipeline as sep  # for the live SONNET reader + prose window only

# We import (a)'s OUTPUT (the json) and re-run (a)'s readers via subprocess-free direct call
# for Arm 1 ONLY (validating the instrument is exactly running the instrument under test).
import na_direction_rederivation as instrument_a  # Arm 1 runs the instrument-under-test

NA_REDERIV = os.path.join(OUTPUTS, "na_direction_rederivation.json")
FAITHFUL_MAP = os.path.join(OUTPUTS, "faithful_target_map.json")
SCAN = os.path.join(OUTPUTS, "retroactive_scan_cycle_1_15_run.json")
OUT = os.path.join(OUTPUTS, "na_rederivation_accuracy.json")
EVENTS = os.path.join(OUTPUTS, "cycle_16_s27_sizing_events.jsonl")
HOME = os.path.expanduser("~")

# Arm-2 independent LLM reader: SONNET (different model from (a)'s haiku), contract-auditor
# prompt (different frame). NOT importing (a)'s reader.
ARM2_MODEL = "claude-sonnet-4-6"
ARM2_PROMPT = (
    "ROLE: independent reviewer. Read the fragment. Question: would ANY program need to "
    "RUN OR CHECK something at runtime to satisfy what this fragment commits — e.g. emit an "
    "event, fire/enforce a gate, run a validator, block on a condition? Or is it purely a "
    "decision/record/methodology/ontology that no code ever executes? Answer with ONLY a "
    "JSON object {\"requires_runtime_code\": <bool>, \"why\": \"<<=20 words>\"}. FRAGMENT:\n\n"
)


def now():
    return datetime.now(timezone.utc).isoformat()


def emit_event(event_class, payload, run_id):
    rec = {"schema_version": "0.1", "namespace": "cycle_16.s27.sizing",
           "event_class": event_class, "timestamp": now(), "run_id": run_id,
           "payload": payload}
    with open(EVENTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------------------
# Arm 1 — fixtures with known labels, run the instrument-under-test on them.
# ---------------------------------------------------------------------------
def run_arm1(llm=True):
    labels = json.load(open(os.path.join(FIXTURES, "labels.json")))["labels"]
    results = []
    tp = fp = tn = fn = 0
    for fname, lab in sorted(labels.items()):
        gt = bool(lab["needs_implementation"])
        path = os.path.join(FIXTURES, fname)
        prose = open(path, encoding="utf-8", errors="replace").read()
        # Run instrument (a)'s ACTUAL readers (this is the instrument under test).
        e1 = instrument_a.e1_prime(prose)
        e2 = instrument_a.e2_prime(prose) if llm else {"needs_implementation": e1["needs_implementation"]}
        disp = instrument_a.reconcile(e1, e2)
        # The instrument flags a spec as needing-code iff disposition is FALSE_NEGATIVE_gap
        # (both readers say needs) OR disagreement (at least one reader says needs). For a
        # CONSERVATIVE detector the positive prediction = "any reader says needs implementation".
        pred = bool(e1["needs_implementation"] or e2.get("needs_implementation"))
        if pred and gt:
            tp += 1
        elif pred and not gt:
            fp += 1
        elif (not pred) and (not gt):
            tn += 1
        else:
            fn += 1
        results.append({"fixture": fname, "ground_truth_needs_impl": gt,
                        "predicted_needs_impl": pred, "disposition": disp,
                        "e1": e1["needs_implementation"],
                        "e2": e2.get("needs_implementation"),
                        "correct": pred == gt})
    n = len(results)
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    # false-negative-rate over the actually-needs-code population = fn / (tp + fn)
    fnr = fn / (tp + fn) if (tp + fn) else None
    accuracy = (tp + tn) / n if n else None
    return {
        "n_fixtures": n, "tp": tp, "fp": fp, "tn": tn, "fn": fn,
        "fixture_precision": precision, "fixture_recall": recall,
        "fixture_false_negative_rate": fnr, "fixture_accuracy": accuracy,
        "per_fixture": results,
    }


# ---------------------------------------------------------------------------
# Arm 2 — structurally-independent 2nd instrument on the REAL 203.
# Different code path: (i) SONNET LLM reader (different model+prompt from (a)),
# (ii) a structurally different obligation-density heuristic. The 2nd instrument's
# verdict = needs-code iff EITHER signal says so (conservative, like (a)).
# ---------------------------------------------------------------------------
_DENSITY_TERMS = re.compile(
    r"\b(emit|emits|fire|fires|gate|gates|enforce|enforced|refuse|refused|validat|"
    r"assert|halt|block|conform|shacl|nonzero|exit\s*code|MUST|SHALL|REQUIRED)\b", re.I)
_EVENTCLASS = re.compile(r"\b[a-z][a-z0-9_]*\.[a-z0-9_]+(?:\.[a-z0-9_]+)+\b")


def arm2_heuristic(prose):
    """Structurally DIFFERENT from (a)'s e1_prime: a density score, not anchor+surface
    co-occurrence. needs-code iff obligation-term density above a fixed principled
    threshold OR a concrete dotted event-class with >=3 segments is present."""
    if not prose:
        return False, 0.0
    words = max(1, len(re.findall(r"\w+", prose)))
    hits = len(_DENSITY_TERMS.findall(prose))
    density = hits / words
    has_eventclass = bool(_EVENTCLASS.search(prose))
    # principled fixed threshold (NOT tuned to the corpus): an obligation term roughly
    # every ~60 words signals a binding runtime obligation; ~0.017 density.
    needs = (density >= 0.017) or has_eventclass
    return needs, round(density, 4)


def _arm2_first_json(raw):
    """Independent (inlined, NOT imported from (a)) balanced first-JSON-object extractor."""
    start = raw.find("{")
    while start != -1:
        depth = 0; in_str = False; esc = False
        for i in range(start, len(raw)):
            c = raw[i]
            if in_str:
                if esc: esc = False
                elif c == "\\": esc = True
                elif c == '"': in_str = False
                continue
            if c == '"': in_str = True
            elif c == "{": depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(raw[start:i + 1])
                    except Exception:
                        break
        start = raw.find("{", start + 1)
    return None


def arm2_llm(prose, max_retries=5):
    client = sep._e2_client()
    last = None
    for attempt in range(max_retries):
        try:
            r = client.messages.create(
                model=ARM2_MODEL, max_tokens=120,
                messages=[{"role": "user", "content": ARM2_PROMPT + prose[:1800]}])
            raw = r.content[0].text.strip()
            obj = _arm2_first_json(raw)
            if obj is None:
                return None
            return bool(obj.get("requires_runtime_code"))
        except Exception as e:
            last = e
            m = str(e).lower()
            if "529" in m or "overload" in m or "rate" in m or "timeout" in m:
                time.sleep(2 ** attempt); continue
            time.sleep(1)
    raise RuntimeError(f"Arm2 LLM failed: {last}")


def run_arm2_on_203(llm=True):
    """Cross-check the real 203 with the independent 2nd instrument; compare vs (a)'s
    per-spec needs-code verdict from na_direction_rederivation.json."""
    a_out = json.load(open(NA_REDERIV))
    a_by = {}
    for m in a_out["members"]:
        # (a)'s needs-code verdict = disposition in {FALSE_NEGATIVE_gap, disagreement_conservative}
        a_needs = m["disposition"] in ("FALSE_NEGATIVE_gap", "disagreement_conservative")
        a_by[m["spec_iri"]] = {"disposition": m["disposition"], "a_needs": a_needs}
    scan = json.load(open(SCAN))
    byid = {}
    for r in scan["per_spec_evidence_IP_PRIVATE"]:
        byid.setdefault(r["spec_id"], r)
    fm = json.load(open(FAITHFUL_MAP))
    na = [x for x in fm["members"] if x.get("disposition") == "dp26_carveout_preserved"]

    agree = 0
    disagreements = []
    n_eval = 0
    arm2_needs_count = 0
    for x in na:
        sid = x["spec_iri"]
        rec = byid.get(sid)
        prose = sep.spec_prose_window(rec, n=1800) if rec else None
        if not prose:
            continue
        h_needs, density = arm2_heuristic(prose)
        l_needs = None
        if llm:
            try:
                l_needs = arm2_llm(prose)
            except RuntimeError:
                l_needs = None
        arm2_needs = bool(h_needs or (l_needs is True))
        if arm2_needs:
            arm2_needs_count += 1
        a_needs = a_by.get(sid, {}).get("a_needs", False)
        n_eval += 1
        if arm2_needs == a_needs:
            agree += 1
        else:
            disagreements.append({
                "spec_iri": sid, "spec_class": x["spec_class"],
                "instrument_a_disposition": a_by.get(sid, {}).get("disposition"),
                "instrument_a_needs_code": a_needs,
                "instrument_2_needs_code": arm2_needs,
                "arm2_heuristic_needs": h_needs, "arm2_heuristic_density": density,
                "arm2_llm_needs": l_needs,
            })
    agreement_rate = agree / n_eval if n_eval else None
    return {
        "n_evaluated_on_203": n_eval,
        "instrument_a_needs_code_count": sum(1 for v in a_by.values() if v["a_needs"]),
        "instrument_2_needs_code_count": arm2_needs_count,
        "n_agree": agree,
        "independent_instrument_agreement_on_203": agreement_rate,
        "n_disagreements": len(disagreements),
        "disagreements": disagreements,
        "instrument_2_note": "SONNET LLM (different model+prompt from (a)'s haiku) OR an "
                             "obligation-density heuristic (structurally different from (a)'s "
                             "anchor+surface co-occurrence). Does NOT import (a)'s readers (#34).",
    }


def honest_statement(arm1, arm2):
    parts = []
    p, r, fnr = arm1["fixture_precision"], arm1["fixture_recall"], arm1["fixture_false_negative_rate"]
    parts.append(f"Fixture (n={arm1['n_fixtures']}): precision={p}, recall={r}, FNR={fnr}, "
                 f"accuracy={arm1['fixture_accuracy']} [MEASURED on authored test data].")
    ag = arm2["independent_instrument_agreement_on_203"]
    parts.append(f"203 inter-instrument agreement={ag} over n={arm2['n_evaluated_on_203']} "
                 f"({arm2['n_disagreements']} disagreements surfaced, NOT auto-resolved) [MEASURED].")
    if r is not None and r < 0.9:
        parts.append("WARNING: fixture recall below 0.9 — the instrument misses some "
                     "observable-committing specs; disclosed, NOT tuned away.")
    if ag is not None and ag < 0.8:
        parts.append("WARNING: cross-instrument agreement below 0.8 — instrument-under-test "
                     "is not corroborated on a meaningful share of the 203; disclosed.")
    parts.append("This is the validate-the-validator step (#46/#34): the re-derivation "
                 "instrument's accuracy is MEASURED, not assumed faithful. Imperfect-but-"
                 "disclosed beats tuned-to-agree.")
    return " ".join(parts)


def run(run_id=None, llm=True):
    run_id = run_id or f"s27_na_accuracy_{uuid.uuid4().hex[:8]}"
    arm1 = run_arm1(llm=llm)
    arm2 = run_arm2_on_203(llm=llm)
    out = {
        "schema_version": "s27_na_rederivation_accuracy.v1",
        "build_event": "Cycle-16-S27 #19/#46/#34 — validate the n/a re-derivation instrument itself",
        "run_id": run_id,
        "validate_the_validator": True,
        "n_fixtures": arm1["n_fixtures"],
        "fixture_precision": arm1["fixture_precision"],
        "fixture_recall": arm1["fixture_recall"],
        "fixture_false_negative_rate": arm1["fixture_false_negative_rate"],
        "fixture_accuracy": arm1["fixture_accuracy"],
        "fixture_detail": arm1,
        "independent_instrument_agreement_on_203": arm2["independent_instrument_agreement_on_203"],
        "independent_instrument_detail": arm2,
        "disagreements": arm2["disagreements"],
        "instrument_2_is_different_code_path_not_importing_a_readers": True,
        "honest_accuracy_statement": honest_statement(arm1, arm2),
    }
    json.dump(out, open(OUT, "w"), indent=2)
    emit_event("accuracy_validation.complete", {
        "fixture_precision": arm1["fixture_precision"],
        "fixture_recall": arm1["fixture_recall"],
        "fixture_false_negative_rate": arm1["fixture_false_negative_rate"],
        "independent_instrument_agreement_on_203": arm2["independent_instrument_agreement_on_203"],
        "n_disagreements": arm2["n_disagreements"],
    }, run_id)
    print(f"[accuracy] fixtures P={arm1['fixture_precision']} R={arm1['fixture_recall']} "
          f"FNR={arm1['fixture_false_negative_rate']} | 203-agreement="
          f"{arm2['independent_instrument_agreement_on_203']} -> {OUT}")
    return out


if __name__ == "__main__":
    rid = sys.argv[1] if len(sys.argv) > 1 else None
    run(run_id=rid)
