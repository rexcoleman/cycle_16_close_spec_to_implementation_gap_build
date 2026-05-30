#!/usr/bin/env python3
"""Cycle-16-S27 Hole 8 — well-formedness + dependency consistency for each spec in V (+ recovered).

Well-formedness (per spec):
  - non-vague: has a CHECKABLE commitment (an obligation anchor with a predicate, or a
    committed observable) OR an explicit n/a rationale (n_a_rationale_present / DP#26
    carve-out language in the text).
  - not internally contradictory: does not both assert an obligation AND disclaim it as
    needing-no-code in a way that conflicts (heuristic contradiction scan).

Dependency consistency (per spec):
  - resolve explicit dependency references in the spec text (other spec ids / 'depends on' /
    'requires <X>'); a violation = a spec claimed implemented while a spec it depends on is
    killed/deferred. NOTE: this corpus carries NO killed/deferred status (statuses are
    dormant-silent / running / long-running) — so the killed/deferred-dependency violation
    class is reported as 0 by construction, disclosed honestly (not asserted as 'no problem').

Output: outputs/spec_wellformedness_verdicts.json
ADDITIVE ONLY.
"""
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")
HOME = os.path.expanduser("~")
sys.path.insert(0, HERE)
import spec_extraction_pipeline as sep

FAITHFUL_MAP = os.path.join(OUTPUTS, "faithful_target_map.json")
SCAN = os.path.join(OUTPUTS, "retroactive_scan_cycle_1_15_run.json")
MINING = os.path.join(OUTPUTS, "denominator_mining_pass.json")
OUT = os.path.join(OUTPUTS, "spec_wellformedness_verdicts.json")
EVENTS = os.path.join(OUTPUTS, "cycle_16_s27_sizing_events.jsonl")

# statuses in this corpus that mean "not a live implemented spec"
_KILLED_DEFERRED = {"killed", "deferred", "dropped", "superseded", "withdrawn"}

_ANCHOR_RE = re.compile(
    r"\b(MUST|SHALL|REQUIRED|BINDING|enforce[ds]?|refus(e|es|ed)|gate[ds]?|emit[s]?|"
    r"fire[s]?|halt[s]?|block[s]?|assert[s]?|validat(e|es|ed))\b", re.I)
_NA_RATIONALE_RE = re.compile(
    r"(no\s+code|design\s+decision|methodology|ontology|citation-based|DP#?26|"
    r"carve[- ]?out|needs\s+no\s+(code|implementation)|documentation\s+only|record\s+only|"
    r"narrative)", re.I)
# spec dependency references in prose
_DEP_RE = re.compile(
    r"\b(?:depends on|depend on|requires|built on|relies on|predicated on|after)\s+"
    r"([A-Za-z0-9_#.\-:]{3,60})", re.I)
_SPEC_ID_RE = re.compile(r"\bspec_retroactive_[0-9a-f]{8}\b")
# contradiction heuristic: same window both commits an obligation AND disclaims runtime code
_CONTRA_OBLIG = re.compile(r"\b(MUST emit|MUST fire|MUST enforce|MUST validate|gate MUST)\b", re.I)
_CONTRA_DISCLAIM = re.compile(r"\b(needs no code|no implementation|never executes|binds no code)\b", re.I)


def now():
    return datetime.now(timezone.utc).isoformat()


def emit_event(event_class, payload, run_id):
    rec = {"schema_version": "0.1", "namespace": "cycle_16.s27.sizing",
           "event_class": event_class, "timestamp": now(), "run_id": run_id,
           "payload": payload}
    with open(EVENTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


def assess_spec(rec, faithful_member):
    """Return per-spec well-formedness + dependency verdict."""
    sid = rec["spec_id"]
    prose = sep.spec_prose_window(rec, n=1800) or ""
    has_anchor = bool(_ANCHOR_RE.search(prose))
    na_rationale_field = bool(rec.get("n_a_rationale_present"))
    has_na_rationale = na_rationale_field or bool(_NA_RATIONALE_RE.search(prose))
    # checkable commitment: an obligation anchor with substantive text around it
    has_checkable = has_anchor and len(prose.strip()) >= 40

    wellformed = bool(has_checkable or has_na_rationale)
    reason_parts = []
    if has_checkable:
        reason_parts.append("has_checkable_commitment")
    if has_na_rationale:
        reason_parts.append("has_explicit_na_rationale")
    if not wellformed:
        reason_parts.append("VAGUE: no checkable commitment AND no explicit n/a rationale")

    contradictory = bool(_CONTRA_OBLIG.search(prose) and _CONTRA_DISCLAIM.search(prose))
    if contradictory:
        reason_parts.append("INTERNALLY_CONTRADICTORY: commits an obligation AND disclaims code")
        wellformed = False

    # dependency resolution from prose
    depends_on = sorted(set(_SPEC_ID_RE.findall(prose)))
    dep_phrases = [m.group(1) for m in _DEP_RE.finditer(prose)][:8]

    return {
        "spec_iri": sid,
        "spec_class": rec.get("spec_class"),
        "current_status": rec.get("current_status"),
        "wellformed": wellformed,
        "reason": "; ".join(reason_parts) or "no_signal",
        "has_checkable_commitment": has_checkable,
        "has_explicit_na_rationale": has_na_rationale,
        "internally_contradictory": contradictory,
        "depends_on_spec_ids": depends_on,
        "dependency_phrases": dep_phrases,
    }


def run(run_id=None):
    run_id = run_id or f"s27_wellformed_{uuid.uuid4().hex[:8]}"
    fm = json.load(open(FAITHFUL_MAP))
    fm_by = {x["spec_iri"]: x for x in fm["members"]}
    scan = json.load(open(SCAN))
    byid = {}
    for r in scan["per_spec_evidence_IP_PRIVATE"]:
        byid.setdefault(r["spec_id"], r)
    # V = the 206 in faithful map
    v_ids = [x["spec_iri"] for x in fm["members"]]

    # status index for dependency-consistency
    status_by = {sid: byid[sid].get("current_status") for sid in v_ids if sid in byid}

    per_spec = []
    n_vague = n_contra = 0
    for sid in v_ids:
        rec = byid.get(sid)
        if rec is None:
            per_spec.append({"spec_iri": sid, "wellformed": False,
                             "reason": "scan record missing", "depends_on_spec_ids": [],
                             "dependency_consistent": True})
            n_vague += 1
            continue
        v = assess_spec(rec, fm_by.get(sid))
        if not v["wellformed"]:
            n_vague += 1
        if v["internally_contradictory"]:
            n_contra += 1
        # dependency consistency: is this spec "claimed implemented" while a depended-on
        # spec is killed/deferred? "claimed implemented" approximated by current_status
        # being 'running'/'long-running' (a live spec). killed/deferred set is empty in
        # this corpus -> 0 violations by construction (disclosed).
        dep_violation = False
        dep_detail = []
        claimed_impl = (v.get("current_status") in ("running", "long-running"))
        for dep in v["depends_on_spec_ids"]:
            dep_status = status_by.get(dep)
            if dep_status in _KILLED_DEFERRED and claimed_impl:
                dep_violation = True
                dep_detail.append({"dep": dep, "dep_status": dep_status})
        v["dependency_consistent"] = (not dep_violation)
        v["dependency_violation_detail"] = dep_detail
        per_spec.append(v)

    n_dep_viol = sum(1 for v in per_spec if not v.get("dependency_consistent", True))
    n_wellformed = sum(1 for v in per_spec if v.get("wellformed"))
    out = {
        "schema_version": "s27_spec_wellformedness_verdicts.v1",
        "build_event": "Cycle-16-S27 Hole 8 — well-formedness + dependency consistency",
        "run_id": run_id,
        "n_specs": len(v_ids),
        "summary": {
            "n_wellformed": n_wellformed,
            "n_vague": n_vague,
            "n_contradictory": n_contra,
            "n_dependency_violations": n_dep_viol,
        },
        "killed_deferred_status_present_in_corpus": any(
            s in _KILLED_DEFERRED for s in status_by.values()),
        "dependency_consistency_note": (
            "This corpus carries NO killed/deferred/dropped status (only dormant-silent / "
            "running / long-running). The killed/deferred-dependency violation class is "
            "therefore 0 BY CONSTRUCTION, not because dependency hygiene was independently "
            "proven sound. Disclosed honestly. Explicit inter-spec dependency references in "
            "prose are extracted and reported regardless."),
        "per_spec": per_spec,
    }
    json.dump(out, open(OUT, "w"), indent=2)
    emit_event("wellformedness.complete", {
        "n_specs": len(v_ids), "n_wellformed": n_wellformed, "n_vague": n_vague,
        "n_contradictory": n_contra, "n_dependency_violations": n_dep_viol,
    }, run_id)
    print(f"[wellformedness] n={len(v_ids)} wellformed={n_wellformed} vague={n_vague} "
          f"contradictory={n_contra} dep_violations={n_dep_viol} -> {OUT}")
    return out


if __name__ == "__main__":
    rid = sys.argv[1] if len(sys.argv) > 1 else None
    run(run_id=rid)
