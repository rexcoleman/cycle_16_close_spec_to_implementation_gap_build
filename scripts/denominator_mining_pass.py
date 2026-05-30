#!/usr/bin/env python3
"""Cycle-16-S27 Hole 3 — ONE bounded denominator mining pass (Rex ruling 1: NOT an open chase).

Mine for commitments AGREED-but-never-written-into-a-spec that are NOT already in V's 206.
Sources (one pass each, no recursion):
  - root DECISION_LOG.md
  - git log commit messages (this repo)
  - memory corpus (~/.claude/projects/.../memory/MEMORY.md + that dir's *.md)

Extract candidate commitments (Done #N obligations, "we will build X", Rex rulings implying a
deliverable). Dedup against V's 206 spec_ids and against the spec corpus prose. Fold genuinely-
new recovered commitments into a recovered population. DISCLOSE the residual blind spot
(unrecorded-by-construction: things agreed only verbally / never written anywhere — name the
bound, do not chase it).

Output: outputs/denominator_mining_pass.json
ADDITIVE ONLY.
"""
import json
import os
import re
import subprocess
import sys
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")
HOME = os.path.expanduser("~")

DECISION_LOG = os.path.join(PROJECT_ROOT, "DECISION_LOG.md")
VALIDATED_SET = os.path.join(OUTPUTS, "validated_commitment_set.json")
SCAN = os.path.join(OUTPUTS, "retroactive_scan_cycle_1_15_run.json")
MEMORY_DIR = os.path.join(HOME, ".claude", "projects",
                          "-home-azureuser-Moonshots-Career-Thesis-v2", "memory")
OUT = os.path.join(OUTPUTS, "denominator_mining_pass.json")
EVENTS = os.path.join(OUTPUTS, "cycle_16_s27_sizing_events.jsonl")


def now():
    return datetime.now(timezone.utc).isoformat()


def emit_event(event_class, payload, run_id):
    rec = {"schema_version": "0.1", "namespace": "cycle_16.s27.sizing",
           "event_class": event_class, "timestamp": now(), "run_id": run_id,
           "payload": payload}
    with open(EVENTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


# Commitment-bearing patterns. Conservative: require a deliverable/obligation verb so we
# do not mint noise from narrative. A "candidate commitment" is a clause that names a thing
# that was agreed to be BUILT / DONE / DELIVERED.
_COMMIT_PATTERNS = [
    re.compile(r"\bDone\s+#\d+[a-z]?\b[^.\n]{0,140}", re.I),
    re.compile(r"\bwe (?:will|shall|must|are going to) (?:build|implement|add|ship|deliver|create|wire|land)\b[^.\n]{0,140}", re.I),
    re.compile(r"\b(?:Rex ruling|paradigm ruling|directive)\b[^.\n]{0,140}", re.I),
    re.compile(r"\b(?:commit(?:s|ment|ted)? to|deliverable[:=]|MUST (?:build|deliver|ship|emit|implement))\b[^.\n]{0,140}", re.I),
    re.compile(r"\bFORWARD\s+#\d+\b[^.\n]{0,140}", re.I),
]

# Tokens that mark a candidate as a build/runtime deliverable rather than a pure decision.
_DELIVERABLE_HINT = re.compile(
    r"\b(build|implement|script|gate|emit|fire|probe|validator|enforce|wire|deliver|"
    r"ship|pipeline|harness|detector|schema|runtime|code)\b", re.I)

_STOP = set("the a an of to and or for in on at by with is are be must shall should not this "
            "that it its as per via into done #".split())


def _sig(text):
    toks = re.findall(r"[a-z0-9]+", text.lower())
    out = []
    for t in toks:
        if t in _STOP or len(t) <= 2:
            continue
        out.append(t[:-1] if (len(t) > 4 and t.endswith("s")) else t)
    return frozenset(out)


def load_V_signatures():
    """V's spec corpus: build a token-signature index of all 206 specs' commitment text so
    we can dedup recovered candidates against what is already a spec."""
    v = json.load(open(VALIDATED_SET))
    spec_ids = set()
    sigs = []
    for m in v["members"]:
        spec_ids.add(m["spec_id"])
        txt = m.get("commitment_text") or ""
        if txt:
            sigs.append(_sig(txt))
    # also fold in scan names for breadth
    scan = json.load(open(SCAN))
    for r in scan["per_spec_evidence_IP_PRIVATE"]:
        nm = r.get("name_truncated") or ""
        if nm:
            sigs.append(_sig(nm))
    return spec_ids, sigs


def _already_in_V(cand_sig, v_sigs, min_overlap=3, jaccard=0.5):
    """A candidate is already-a-spec iff its token signature strongly overlaps an existing
    spec commitment signature (>=min_overlap shared tokens AND Jaccard>=jaccard)."""
    if not cand_sig:
        return True  # empty signature -> noise, treat as dedup-drop
    for s in v_sigs:
        inter = cand_sig & s
        if len(inter) >= min_overlap and (len(inter) / len(cand_sig | s)) >= jaccard:
            return True
    return False


def gather_decision_log():
    if not os.path.isfile(DECISION_LOG):
        return []
    txt = open(DECISION_LOG, encoding="utf-8", errors="replace").read()
    cands = []
    for pat in _COMMIT_PATTERNS:
        for m in pat.finditer(txt):
            cands.append(("DECISION_LOG.md", m.group(0).strip()[:200]))
    return cands


def gather_git_log():
    try:
        out = subprocess.run(["git", "-C", PROJECT_ROOT, "log", "--format=%s%n%b"],
                             capture_output=True, text=True, timeout=60).stdout
    except Exception:
        return []
    cands = []
    for pat in _COMMIT_PATTERNS:
        for m in pat.finditer(out):
            cands.append(("git_log", m.group(0).strip()[:200]))
    return cands


def gather_memory():
    cands = []
    paths = []
    if os.path.isdir(MEMORY_DIR):
        for fn in sorted(os.listdir(MEMORY_DIR)):
            if fn.endswith(".md"):
                paths.append(os.path.join(MEMORY_DIR, fn))
    for p in paths:
        try:
            txt = open(p, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for pat in _COMMIT_PATTERNS:
            for m in pat.finditer(txt):
                cands.append((os.path.basename(p), m.group(0).strip()[:200]))
    return cands


def run(run_id=None):
    run_id = run_id or f"s27_mining_{uuid.uuid4().hex[:8]}"
    spec_ids, v_sigs = load_V_signatures()
    raw = gather_decision_log() + gather_git_log() + gather_memory()

    # dedup candidates among themselves (by signature) and vs V
    seen_sigs = set()
    recovered = []
    deduped_against_V = 0
    self_dup = 0
    for source, text in raw:
        sig = _sig(text)
        key = sig
        if key in seen_sigs:
            self_dup += 1
            continue
        seen_sigs.add(key)
        if _already_in_V(sig, v_sigs):
            deduped_against_V += 1
            continue
        # keep only candidates that look like a BUILD/RUNTIME deliverable (not a pure
        # decision record) — these are the ones that would ADD to the build denominator
        is_deliverable = bool(_DELIVERABLE_HINT.search(text))
        recovered.append({
            "source": source, "text": text,
            "looks_like_runtime_deliverable": is_deliverable,
            "needs_code_candidate": is_deliverable,
        })

    n_runtime = sum(1 for r in recovered if r["needs_code_candidate"])
    out = {
        "schema_version": "s27_denominator_mining_pass.v1",
        "build_event": "Cycle-16-S27 Hole 3 — ONE bounded denominator mining pass (Rex ruling 1)",
        "run_id": run_id,
        "one_pass": True,
        "sources_scanned": ["DECISION_LOG.md", "git_log", "memory/*.md"],
        "n_raw_candidates": len(raw),
        "n_self_duplicates": self_dup,
        "n_deduped_against_V": deduped_against_V,
        "deduped_against_V": True,
        "V_spec_count": len(spec_ids),
        "recovered_specs": recovered,
        "n_recovered": len(recovered),
        "n_recovered_runtime_deliverable_candidates": n_runtime,
        "new_population_size": len(spec_ids) + len(recovered),
        "residual_disclosure": (
            "BLIND SPOT (unrecorded-by-construction, NOT chased per Rex ruling 1): "
            "commitments agreed only verbally in conversation and never written into "
            "DECISION_LOG.md, a commit message, or memory are invisible to this pass by "
            "construction. This ONE bounded pass cannot recover them; the bound is the set "
            "of WRITTEN artifacts (DECISION_LOG + git log + memory). Recovered candidates are "
            "heuristic text-pattern matches (Done #N / 'we will build' / rulings / FORWARD #N) "
            "and may themselves restate existing specs missed by the dedup; they are surfaced "
            "as candidates, NOT asserted as confirmed new specs."),
    }
    json.dump(out, open(OUT, "w"), indent=2)
    emit_event("mining_pass.complete", {
        "n_raw_candidates": len(raw), "n_recovered": len(recovered),
        "n_recovered_runtime_deliverable_candidates": n_runtime,
        "new_population_size": out["new_population_size"],
    }, run_id)
    print(f"[mining] raw={len(raw)} deduped_vs_V={deduped_against_V} recovered={len(recovered)} "
          f"runtime_deliverable={n_runtime} -> {OUT}")
    return out


if __name__ == "__main__":
    rid = sys.argv[1] if len(sys.argv) > 1 else None
    run(run_id=rid)
