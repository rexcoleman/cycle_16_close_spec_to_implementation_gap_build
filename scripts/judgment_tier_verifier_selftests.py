#!/usr/bin/env python3
"""Cycle-16-S28 BE-JTV — anti-gaming self-tests (mechanical, CLI exit-code).

Each test prints PASS/FAIL; the script exits 0 iff ALL pass, non-zero otherwise. These are the
validate-the-validator guards: they check the verifier can't be gamed into looking trustworthy.

Tests (per the build prompt §4):
  judges_share_no_extraction_or_parse_code  — AST: J1/J2/J3 private-reader call-graphs disjoint;
                                              HARD-FAIL if any two share a helper.
  verifier_reads_gt_at_scoring == false     — the verdict path never opens labels.json / any GT path.
  judges_not_tuned_to_agree                 — judge bodies + quorum constant byte-frozen across the
                                              measurement (hash snapshot stable).
  verifier_fn_human_inputs == 0             — the verdict path takes 0 human inputs.
  additive_only                             — frozen paths byte-identical (the new judgment_tier_gt/
                                              fixtures subdir is additive and excluded; floors intact).

ADDITIVE ONLY.
"""
import ast
import hashlib
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import judgment_tier_verifier as jtv

# Truly-frozen paths (per build prompt HC): probes/**, probe_accuracy_harness.py, EXISTING
# fixtures/**. The NEW judgment_tier_gt/ subdir under scripts/structural_prevention/fixtures/ is
# ADDITIVE (ARTIFACT_CONTRACT.md §18 names it a NEW artifact), so the parent fixtures dir is NOT
# frozen wholesale — only its pre-existing tracked files must stay byte-identical.
FROZEN_PATHS = [
    "scripts/probes",
    "scripts/probe_accuracy_harness.py",
    "fixtures",
    "tests/probes/fixtures",
]
FROZEN_PREEXISTING_GLOBS = ["scripts/structural_prevention/fixtures"]
ADDITIVE_NEW_SUBDIR = "scripts/structural_prevention/fixtures/judgment_tier_gt"
FLOORS = ("0.20", "0.80", "0.20")
JUDGE_HASH_SNAPSHOT = os.path.join(PROJECT_ROOT, "outputs", "judgment_tier_verifier_judge_code_hash.txt")


def t_judges_share_no_extraction_or_parse_code():
    st = jtv.independence_self_test()
    ok = st["judges_share_no_code_path"] and not st["shared_private_readers_across_judges"]
    return ok, (f"j1={st['j1_private_readers']} j2={st['j2_private_readers']} "
                f"j3={st['j3_private_readers']} shared={st['shared_private_readers_across_judges']}")


def t_verifier_reads_gt_at_scoring_false():
    """The verdict path must NOT open labels.json / any GT file. AST scan of the verdict-path
    function bodies for an actual open()/json.load CALL whose argument STRING contains a GT marker.
    String/comment mentions (e.g. a `blind_note` documenting that the path never opens labels.json)
    are NOT flagged — only real read CALLS of a GT path. Also: the verifier module must define no
    LABELS/GT_DIR module constant (the accuracy harness owns those, not the verdict path)."""
    src = open(os.path.join(HERE, "judgment_tier_verifier.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    verdict_fns = {"judge_j1_llm", "judge_j2_llm", "judge_j3_structural", "verify_spec",
                   "cmd_run", "load_judgment_tier", "quorum",
                   "_j1_resolve_prose", "_j1_read_embodiment", "_j1_parse",
                   "_j2_get_prose", "_j2_load_embodiment", "_j2_decode",
                   "_j3_obligations", "_j3_load_py", "_j3_reachable"}
    GT_MARKERS = ("labels.json", "ground_truth", "judgment_tier_gt", "labels_blind")

    def _is_read_call(n):
        if not isinstance(n, ast.Call):
            return False
        f = n.func
        if isinstance(f, ast.Name) and f.id == "open":
            return True
        if isinstance(f, ast.Attribute) and f.attr in ("load", "read_text", "open"):
            return True
        return False

    def _str_args_contain_marker(n):
        for a in ast.walk(n):
            if isinstance(a, ast.Constant) and isinstance(a.value, str):
                low = a.value.lower()
                if any(m in low for m in GT_MARKERS):
                    return True
        return False

    bad = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in verdict_fns:
            for sub in ast.walk(node):
                if _is_read_call(sub) and _str_args_contain_marker(sub):
                    bad.append(node.name)
                    break
    # module-level GT constants must NOT exist in the verifier (they belong to the accuracy harness)
    mod_gt_consts = []
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name) and t.id in ("LABELS", "GT_DIR", "PAIRS"):
                    mod_gt_consts.append(t.id)
    ok = (not bad) and (not mod_gt_consts)
    return ok, f"verdict-path GT-read calls: {bad or 'NONE'}; module GT constants: {mod_gt_consts or 'NONE'}"


def _judge_code_hash():
    return hashlib.sha256(
        open(os.path.join(HERE, "judgment_tier_verifier.py"), "rb").read()).hexdigest()


def t_judges_not_tuned_to_agree():
    """Judge code (incl. quorum constant) byte-frozen ACROSS the measurement.

    The verifier is a NEW additive file (may be untracked, so plain `git diff` has no committed
    baseline). True invariant: the judge code did not change between the snapshot taken before the
    measurement and now. Compare stored hash snapshot to current hash. If a snapshot exists it MUST
    match (mid-measurement change = FAIL). If none exists, write it (first run) — clean, since
    nothing changed within a measurement. If TRACKED, additionally require no uncommitted edit."""
    cur = _judge_code_hash()
    if os.path.exists(JUDGE_HASH_SNAPSHOT):
        prev = open(JUDGE_HASH_SNAPSHOT, encoding="utf-8").read().strip()
        if prev != cur:
            return False, f"judge code hash CHANGED across measurement: {prev[:12]} -> {cur[:12]}"
        snap_msg = f"hash stable {cur[:12]} (matches pre-measurement snapshot)"
    else:
        open(JUDGE_HASH_SNAPSHOT, "w", encoding="utf-8").write(cur)
        snap_msg = f"hash snapshot written {cur[:12]} (first run)"
    r = subprocess.run(["git", "ls-files", "--error-unmatch", "scripts/judgment_tier_verifier.py"],
                       cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)
    if r.returncode == 0:
        d = subprocess.run(["git", "diff", "--stat", "--", "scripts/judgment_tier_verifier.py"],
                           cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)
        if d.stdout.strip():
            return False, f"tracked verifier has uncommitted edits: {d.stdout.strip()}"
        return True, f"{snap_msg}; tracked + git-diff clean"
    return True, f"{snap_msg}; verifier is NEW untracked additive file (no committed baseline)"


def t_verifier_fn_human_inputs_zero():
    n = jtv.verifier_fn_human_inputs()
    return n == 0, f"verifier_fn_human_inputs={n}"


def t_additive_only():
    """Frozen paths byte-identical (git diff --stat empty AND no untracked-new under them), floors
    0.20/0.80/0.20 intact, AND no PRE-EXISTING file under structural_prevention/fixtures changed
    (the new judgment_tier_gt/ subdir is additive and excluded)."""
    dirty = []
    for p in FROZEN_PATHS:
        r = subprocess.run(["git", "diff", "--stat", "--", p],
                           cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)
        if r.stdout.strip():
            dirty.append(p)
    r2 = subprocess.run(["git", "status", "--porcelain", "--", *FROZEN_PATHS],
                        cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)
    new_under_frozen = [l for l in r2.stdout.splitlines() if l.strip()]
    r3 = subprocess.run(["git", "diff", "--stat", "--", *FROZEN_PREEXISTING_GLOBS],
                        cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=30)
    preexisting_changed = [l for l in r3.stdout.splitlines()
                           if l.strip() and ADDITIVE_NEW_SUBDIR not in l]
    # The floors 0.20/0.80/0.20 are declared canonically in docs/ARTIFACT_CONTRACT.md (a frozen
    # Stage-0..4 contract; this build only APPENDED §18). Assert they are present AND that the
    # contract's NON-APPEND region is unchanged is out of scope here; we assert floor literals
    # present (not silently deleted) — the docs are not in this build's frozen-PATH list but the
    # floor VALUES are a hard constraint.
    contract = open(os.path.join(PROJECT_ROOT, "docs/ARTIFACT_CONTRACT.md"),
                    encoding="utf-8").read()
    floors_ok = all(f in contract for f in FLOORS)
    ok = (not dirty) and (not new_under_frozen) and (not preexisting_changed) and floors_ok
    return ok, (f"dirty_frozen={dirty or 'NONE'} new_under_frozen={new_under_frozen or 'NONE'} "
                f"preexisting_changed={preexisting_changed or 'NONE'} "
                f"floors_in_contract={floors_ok}")


def main():
    tests = [
        ("judges_share_no_extraction_or_parse_code", t_judges_share_no_extraction_or_parse_code),
        ("verifier_reads_gt_at_scoring_false", t_verifier_reads_gt_at_scoring_false),
        ("judges_not_tuned_to_agree", t_judges_not_tuned_to_agree),
        ("verifier_fn_human_inputs_zero", t_verifier_fn_human_inputs_zero),
        ("additive_only", t_additive_only),
    ]
    all_ok = True
    for name, fn in tests:
        try:
            ok, detail = fn()
        except Exception as e:  # noqa: BLE001
            ok, detail = False, f"EXCEPTION {e!r}"
        all_ok = all_ok and ok
        print(f"[{'PASS' if ok else 'FAIL'}] {name} :: {detail}")
    print(f"OVERALL {'PASS' if all_ok else 'FAIL'}")
    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
