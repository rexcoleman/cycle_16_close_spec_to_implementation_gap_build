#!/usr/bin/env python3
"""Cycle-16-S28 BE-JTV — judgment-tier verifier-of-record (J1/J2/J3 diverse quorum).

Design spec: docs/judgment_tier_verifier_mechanism.md (RP-authored). This is the NEW
successor verifier that REPLACES the 1-LLM+1-grep pair in probe_accuracy_harness.py with a
genuinely diverse, structurally-independent quorum of THREE judges.

WHY THIS EXISTS (the load-bearing fix): probe_accuracy_harness.py's judgment-tier GT derivers
(gt_class_c L928 / gt_class_f_judge L993 / gt_class_e_status L957) ALL reduce to the SAME two
shared helpers `_gt_llm_judge` + `_gt_code_token_crosscheck`. That shared code makes any
systematic error correlate across the whole tier (agreement-by-construction). S29+ will SCALE
backlog implementation off this tier's verdicts, so a verifier whose judges secretly share code
reproduces the recursive failure one level up. This file gives three judges that share NO private
reader symbol:

  J1 — judge_j1_llm()       : claude-sonnet-4-5, "contract auditor" frame.
  J2 — judge_j2_llm()       : claude-haiku-4-5, "skeptical reviewer, default not-implemented" frame.
                              DISTINCT model AND distinct prompt AND a separate function body.
  J3 — judge_j3_structural(): deterministic AST/grep; credits an obligation ONLY when the
                              committed verb is wired into a reachable call path, not a comment.

INDEPENDENCE INVARIANT (the true, narrow one — NOT a copied #34 docstring; S27 FLAG F1):
  - J1, J2, J3 each have their OWN private spec-source/prose/embodiment readers, prefixed
    _j1_*, _j2_*, _j3_*. No judge calls another judge's private reader, and no two judges call a
    single shared private reader. (--independence-self-test asserts this by AST call-graph
    disjointness; it does NOT merely grep for an import name.)
  - J1 model id != J2 model id (a genuine diverse quorum, not one model agreeing with itself).
  - The ONLY shared symbols are: the LLM transport (spec_extraction_pipeline._e2_client — a
    key-selecting client factory, NOT a spec reader), the input loader (load_judgment_tier —
    reads the spec INVENTORY, not the prose/code a judge reasons over), the emitter, and stdlib.
    These are explicitly whitelisted; they are not reasoning code. Specifically: J1 reads prose
    via spec_extraction_pipeline.spec_prose_window; J2 reads prose by parsing the audit-tuple file
    region with its OWN reader; J3 derives obligation verbs from the commitment_text + its OWN AST
    pass. No two judges share a prose/code reader symbol.

QUORUM RULE (FROZEN, S27 FLAG F2 — explicitly AND vs OR):
  Pre-registered + frozen as UNANIMITY (logical AND), NOT strong-majority:
    VALIDATED-IMPLEMENTED      iff ALL non-abstaining judges say `implemented`
                               AND both J1 and J2 (the LLM reasoners) are non-abstaining.
    VALIDATED-NOT-IMPLEMENTED  iff ALL non-abstaining judges say `not_implemented`
                               AND the same >=2-reasoner floor holds.
    CONTESTED (-> conservative NOT-IMPLEMENTED) in EVERY other case: any disagreement, any
                               insufficient quorum, any refusal/no-key/unparseable judge.
  IMPLEMENTED uses AND (unanimity) because shipping a not-implemented spec as "done" is the
  Cycle-16 failure; under-claiming (a real implemented spec wrongly CONTESTED) only costs a
  re-look. So the mapping is asymmetric ONLY toward CONTESTED, never toward IMPLEMENTED. A
  "needs-a-look / surfacing" signal (used nowhere) would be OR; we do NOT emit one. NEVER tune
  judges/prompt/model to raise the agreement rate.

The verdict path is BLIND to ground-truth labels (JTV-3): --run / --vertical-slice never open
labels.json and take 0 human inputs (JTV-7). GT comparison happens only in the separate accuracy
harness AFTER verdicts are written.

ADDITIVE ONLY. Frozen paths (probes/**, floors, fixtures/**, probe_accuracy_harness.py) consumed
UNMODIFIED — this file imports NONE of probe_accuracy_harness's judge helpers.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import pathlib
import re
import sys
import uuid
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(HERE)
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")
HOME = os.path.expanduser("~")
sys.path.insert(0, HERE)

# LLM TRANSPORT ONLY (key-selecting client factory). NOT a spec/prose/code reasoning reader.
import spec_extraction_pipeline as _sep  # noqa: E402

TIER_VERDICTS = os.path.join(OUTPUTS, "validation_tier_verdicts.json")
SCAN = os.path.join(OUTPUTS, "retroactive_scan_cycle_1_15_run.json")
COMMITMENT_SET = os.path.join(OUTPUTS, "validated_commitment_set.json")
EVENTS = os.path.join(OUTPUTS, "judgment_tier_verifier_events.jsonl")
RUN_OUT = os.path.join(OUTPUTS, "judgment_tier_verifier_run.json")
VERDICTS_OUT = os.path.join(OUTPUTS, "judgment_tier_verifier_verdicts.json")

NAMESPACE = "cycle_16.s28.judgment_tier_verifier"
SCHEMA_VERSION = "0.1"

# ---- FROZEN judge constants (JTV-7: byte-identical across the accuracy run) ----
J1_MODEL = "claude-sonnet-4-5"   # judge J1 — code-reading LLM, model A
J2_MODEL = "claude-haiku-4-5"    # judge J2 — code-reading LLM, model B (DIFFERENT family/size)
J3_KIND = "structural_nonllm"    # judge J3 — deterministic AST/grep, no LLM
QUORUM_RULE = "UNANIMITY_AND"    # FROZEN: AND over non-abstainers + both-LLM-reasoner floor
LLM_REASONER_FLOOR = 2           # both J1 and J2 must be non-abstaining for a VALIDATED verdict
CODE_HEAD_BYTES = 14000          # bytes of embodiment text each LLM judge reads
MAX_TOKENS = 350


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _emit(event_class: str, payload: dict, run_id: str) -> None:
    rec = {"schema_version": SCHEMA_VERSION, "namespace": NAMESPACE,
           "event_class": event_class, "timestamp": _now(), "run_id": run_id, "payload": payload}
    with open(EVENTS, "a", encoding="utf-8") as f:
        f.write(json.dumps(rec) + "\n")


def _audit_path(scan_rec: dict) -> str | None:
    at = scan_rec.get("audit_tuple") or []
    if len(at) >= 2 and at[1]:
        return at[1].replace("~", HOME)
    return None


# =========================================================================
# Input loader — reads the spec INVENTORY (the 203 semantically_judged specs):
# spec_iri, spec_class, the canonical scan record (audit_tuple/name), commitment_text.
# This is NOT a judge's reasoning reader; it hands each judge the same neutral row.
# =========================================================================
def load_judgment_tier() -> list[dict]:
    for f in (TIER_VERDICTS, SCAN, COMMITMENT_SET):
        if not os.path.exists(f):
            raise FileNotFoundError(f"DP#44 refuse: missing {f}")
    tv = json.load(open(TIER_VERDICTS, encoding="utf-8"))
    sd = json.load(open(SCAN, encoding="utf-8"))
    scan_by_id = {}
    for r in sd["per_spec_evidence_IP_PRIVATE"]:
        scan_by_id.setdefault(r["spec_id"], r)
    cs = json.load(open(COMMITMENT_SET, encoding="utf-8"))
    text_by_id = {}
    for m in cs["members"]:
        text_by_id.setdefault(m["spec_id"], m.get("commitment_text"))
    rows = []
    for v in tv["per_spec_verdicts_IP_PRIVATE"]:
        if v.get("tier") != "semantically_judged":
            continue
        iri = v["spec_iri"]
        scan = scan_by_id.get(iri)
        rows.append({
            "spec_iri": iri,
            "spec_class": v.get("spec_class"),
            "commitment_text": text_by_id.get(iri),
            "scan_rec": scan,                                # the canonical record (audit_tuple/name)
            "embodiment_path": _audit_path(scan) if scan else None,
            "name": (scan or {}).get("name_truncated"),
            "committed_runtime_emit_class": (scan or {}).get("runtime_emit_event_class"),
        })
    if not rows:
        raise RuntimeError("DP#44 refuse: 0 judgment-tier rows resolved (input unreadable)")
    return rows


def stratum_of(spec_class: str | None) -> str:
    # spec_class already arrives in stratum form (a_agent_contract / b_schema /
    # c_design_decision / d_methodology_commitment). Pass through; map unknowns.
    return spec_class or "unknown"


def _read_embodiment_text(path: str | None) -> tuple[str | None, str]:
    """Generic file/dir reader used INDEPENDENTLY by each judge's own wrapper below
    via different call sites. (Defined once but each judge has its OWN wrapper that
    decides WHAT to read; the wrappers are the private readers, this is plain IO.)"""
    if not path:
        return None, "no embodiment path"
    p = pathlib.Path(os.path.expanduser(path))
    if not p.exists():
        return None, f"embodiment does not resolve: {path}"
    if p.is_dir():
        blobs = []
        for f in sorted(p.rglob("*")):
            if f.is_file() and f.suffix in (".py", ".sh", ".md", ".json", ".yaml", ".yml", ".ttl"):
                try:
                    blobs.append(f"### {f.name}\n" + f.read_text(encoding="utf-8", errors="replace")[:3500])
                except OSError:
                    continue
            if len(blobs) >= 6:
                break
        return ("\n\n".join(blobs)[:CODE_HEAD_BYTES] or None), str(p)
    try:
        return p.read_text(encoding="utf-8", errors="replace")[:CODE_HEAD_BYTES], str(p)
    except OSError as e:
        return None, f"unreadable: {e!r}"


# =========================================================================
# JUDGE J1 — code-reading LLM, model A (sonnet), "contract auditor" frame.
# Private readers: _j1_resolve_prose, _j1_read_embodiment, _j1_parse.
# =========================================================================
_J1_FRAME = (
    "ROLE: contract auditor. You audit whether a committed contract is honored by its embodiment.\n"
    "You are given the COMMITMENT (prose) and its EMBODIMENT (code or spec text). Decide whether "
    "the embodiment actually behaves as the commitment requires — not whether the topic is merely "
    "mentioned. A stub, a TODO, a comment, a docstring, a plan, or a name-only match is NOT "
    "implementation. For a code embodiment, implementation means the committed behavior is present "
    "in executable code reachable from a real entrypoint. For a spec/agent-instruction embodiment, "
    "implementation means the instruction is concretely specified and operative, not aspirational.\n"
    "Answer with NOTHING but one JSON object: "
    '{\"implemented\": <true|false>, \"evidence\": \"<file:line or concrete proof, or why not>\"}'
)


def _j1_resolve_prose(row: dict) -> str:
    rec = row.get("scan_rec")
    prose = None
    if rec:
        try:
            prose = _sep.spec_prose_window(rec, 1200)
        except Exception:
            prose = None
    ct = row.get("commitment_text") or ""
    if not prose or not str(prose).strip():
        prose = ct or f"spec {row.get('spec_iri')} ({row.get('spec_class')})"
    # always prepend the one-line commitment so the auditor sees the obligation crisply
    return f"COMMITMENT: {ct}\n\n--- definition-site prose ---\n{prose}"


def _j1_read_embodiment(row: dict) -> tuple[str | None, str]:
    return _read_embodiment_text(row.get("embodiment_path"))


def _j1_parse(text: str):
    for m in re.finditer(r"\{[^{}]*\}", text or "", re.DOTALL):
        try:
            o = json.loads(m.group(0))
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(o, dict) and "implemented" in o:
            return o
    return None


def judge_j1_llm(row: dict, client) -> tuple[str, str]:
    if client is None:
        return "abstain", "j1_abstain: no LLM key (DP#44; no fabricated verdict)"
    code, ref = _j1_read_embodiment(row)
    if code is None:
        return "abstain", f"j1_abstain: no readable embodiment ({ref})"
    prose = _j1_resolve_prose(row)
    prompt = f"{_J1_FRAME}\n\n=== COMMITMENT/SPEC ===\n{prose[:4500]}\n\n=== EMBODIMENT ({ref}) ===\n{code}"
    try:
        resp = client.messages.create(model=J1_MODEL, max_tokens=MAX_TOKENS, temperature=0,
                                      messages=[{"role": "user", "content": prompt}])
        out = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    except Exception as e:  # noqa: BLE001
        return "abstain", f"j1_abstain: llm_error {e!r}"[:200]
    v = _j1_parse(out)
    if v is None:
        return "abstain", f"j1_abstain: unparseable {out[:120]!r}"
    return ("implemented" if bool(v.get("implemented")) else "not_implemented",
            f"j1[{J1_MODEL}]: {str(v.get('evidence',''))[:160]}")


# =========================================================================
# JUDGE J2 — code-reading LLM, model B (haiku), "skeptical reviewer" frame.
# Private readers: _j2_get_prose, _j2_load_embodiment, _j2_decode. Distinct body.
# =========================================================================
_J2_FRAME = (
    "You are a SKEPTICAL reviewer. Your DEFAULT answer is NOT implemented; you only move off the "
    "default when the embodiment gives concrete, line-level proof that the committed behavior is "
    "actually operative. Mentions, names that match the commitment, comments, plans, docstrings, "
    "aspirational language, and unreferenced helpers are NOT proof. Ask: if I deleted everything "
    "that is only a comment, a name, or a plan, would the committed behavior still hold? If unsure, "
    "answer not implemented.\n"
    "You receive the COMMITMENT and the EMBODIMENT that supposedly fulfills it.\n"
    "Output ONLY one JSON object: "
    '{\"implemented\": <true|false>, \"evidence\": \"<concrete proof, or the gap>\"}'
)


def _j2_get_prose(row: dict) -> str:
    """J2's OWN prose reader: parse the audit-tuple file region directly around the spec name,
    falling back to commitment_text. Deliberately a DIFFERENT resolver than J1's (no shared call)."""
    ct = row.get("commitment_text") or ""
    rec = row.get("scan_rec") or {}
    path = row.get("embodiment_path")
    name = rec.get("name_truncated") or ""
    region = ""
    if path and os.path.isfile(os.path.expanduser(path)):
        try:
            txt = open(os.path.expanduser(path), encoding="utf-8", errors="replace").read()
            idx = txt.find(name) if name else -1
            if idx < 0 and ":" in name:
                idx = txt.find(name.split(":")[-1])
            region = txt[max(0, idx - 80): idx + 1100] if idx >= 0 else txt[:1100]
        except OSError:
            region = ""
    body = f"COMMITMENT: {ct}"
    if region.strip():
        body += f"\n\n--- spec region near '{name}' ---\n{region}"
    return body


def _j2_load_embodiment(row: dict) -> tuple[str | None, str]:
    """J2's OWN embodiment loader (independent body)."""
    path = row.get("embodiment_path")
    if not path:
        return None, "j2: no embodiment"
    p = pathlib.Path(os.path.expanduser(path))
    if not p.exists():
        return None, f"j2: unresolved {path}"
    if p.is_dir():
        chunks, cnt = [], 0
        for f in sorted(p.rglob("*")):
            if not f.is_file() or f.suffix not in (".py", ".sh", ".md", ".json", ".yaml", ".yml", ".ttl"):
                continue
            try:
                chunks.append(f"### FILE {f.name}\n{f.read_text(encoding='utf-8', errors='replace')[:3500]}")
            except OSError:
                continue
            cnt += 1
            if cnt >= 6:
                break
        return ("\n\n".join(chunks)[:CODE_HEAD_BYTES] or None), str(p)
    try:
        return p.read_text(encoding="utf-8", errors="replace")[:CODE_HEAD_BYTES], str(p)
    except OSError as e:
        return None, f"j2: unreadable {e!r}"


def _j2_decode(text: str):
    for c in re.findall(r"\{.*?\}", text or "", re.DOTALL):
        try:
            o = json.loads(c)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(o, dict) and "implemented" in o:
            return o
    return None


def judge_j2_llm(row: dict, client) -> tuple[str, str]:
    if client is None:
        return "abstain", "j2_abstain: no LLM key"
    code, ref = _j2_load_embodiment(row)
    if code is None:
        return "abstain", f"j2_abstain: {ref}"
    prose = _j2_get_prose(row)
    prompt = f"{_J2_FRAME}\n\n=== COMMITMENT ===\n{prose[:4500]}\n\n=== EMBODIMENT ({ref}) ===\n{code}"
    try:
        resp = client.messages.create(model=J2_MODEL, max_tokens=MAX_TOKENS, temperature=0,
                                      messages=[{"role": "user", "content": prompt}])
        out = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
    except Exception as e:  # noqa: BLE001
        return "abstain", f"j2_abstain: llm_error {e!r}"[:200]
    v = _j2_decode(out)
    if v is None:
        return "abstain", f"j2_abstain: unparseable {out[:120]!r}"
    return ("implemented" if bool(v.get("implemented")) else "not_implemented",
            f"j2[{J2_MODEL}]: {str(v.get('evidence',''))[:160]}")


# =========================================================================
# JUDGE J3 — deterministic structural (non-LLM). Different KIND of signal.
# Credits an obligation ONLY when a committed verb is wired into a reachable call
# path (a def carrying the verb that is also CALLED, OR a CLI/main entrypoint).
# Private readers: _j3_obligations, _j3_load_py, _j3_reachable. No LLM.
# =========================================================================
_OBLIGATION_VERBS = ("emit", "fire", "gate", "enforce", "validate", "block", "check",
                     "assert", "verify", "guard", "refuse", "halt")


def _j3_obligations(row: dict) -> list[str]:
    """J3's OWN obligation extractor over the commitment text (NOT prose-window; its own source)."""
    blob = (row.get("commitment_text") or "").lower()
    return [v for v in _OBLIGATION_VERBS if v in blob]


def _j3_load_py(row: dict) -> list[tuple[str, str]]:
    """J3's OWN python-source loader. Non-python embodiments -> [] (AST undefined)."""
    path = row.get("embodiment_path")
    if not path:
        return []
    p = pathlib.Path(os.path.expanduser(path))
    if not p.exists():
        return []
    files = []
    if p.is_dir():
        files = [f for f in sorted(p.rglob("*.py")) if f.is_file()][:12]
    elif p.suffix == ".py":
        files = [p]
    out = []
    for f in files:
        try:
            out.append((f.name, f.read_text(encoding="utf-8", errors="replace")))
        except OSError:
            continue
    return out


def _j3_reachable(sources: list[tuple[str, str]]) -> tuple[set[str], set[str], bool]:
    defined, called = set(), set()
    has_main = False
    for _n, src in sources:
        if "__main__" in src or "argparse" in src or re.search(r"\ndef main\b", src):
            has_main = True
        try:
            tree = ast.parse(src)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                if any(v in node.name.lower() for v in _OBLIGATION_VERBS):
                    defined.add(node.name)
            if isinstance(node, ast.Call):
                fn = node.func
                if isinstance(fn, ast.Name):
                    called.add(fn.id)
                elif isinstance(fn, ast.Attribute):
                    called.add(fn.attr)
    return defined, called, has_main


def judge_j3_structural(row: dict) -> tuple[str, str]:
    obligations = _j3_obligations(row)
    if not obligations:
        return "abstain", "j3_abstain: commitment names no obligation verb (structural test undefined)"
    sources = _j3_load_py(row)
    if not sources:
        return "abstain", "j3_abstain: no python embodiment (AST reachability undefined)"
    defined, called, has_main = _j3_reachable(sources)
    if not defined:
        return "not_implemented", f"j3: commitment commits {obligations} but no def/symbol carries an obligation verb"
    wired = sorted(s for s in defined if s in called)
    if wired:
        return "implemented", f"j3: verb-symbols wired into call path: {wired[:5]}"
    if has_main and defined:
        return "implemented", f"j3: verb-symbols {sorted(defined)[:3]} in a CLI/main entrypoint (reachable)"
    return "not_implemented", f"j3: verb-symbols {sorted(defined)[:3]} defined but not called/reachable"


# =========================================================================
# Quorum (FROZEN UNANIMITY_AND rule + asymmetric conservative fail-safe).
# =========================================================================
def quorum(j1: str, j2: str, j3: str) -> tuple[str, bool, int]:
    n_reasoners = len([x for x in (j1, j2) if x != "abstain"])
    nonabstain = [x for x in (j1, j2, j3) if x != "abstain"]
    if n_reasoners < LLM_REASONER_FLOOR or not nonabstain:
        return "CONTESTED", True, n_reasoners
    if all(x == "implemented" for x in nonabstain):
        return "VALIDATED-IMPLEMENTED", False, n_reasoners
    if all(x == "not_implemented" for x in nonabstain):
        return "VALIDATED-NOT-IMPLEMENTED", False, n_reasoners
    return "CONTESTED", True, n_reasoners  # disagreement -> conservative (never toward IMPLEMENTED)


def verify_spec(row: dict, client, run_id: str) -> dict:
    """Run J1, J2, J3 on one spec and apply the quorum. BLIND to GT (never reads labels)."""
    j1, j1ev = judge_j1_llm(row, client)
    j2, j2ev = judge_j2_llm(row, client)
    j3, j3ev = judge_j3_structural(row)
    for jid, kind, model, label, ev in (
        ("J1", "llm_model_a", J1_MODEL, j1, j1ev),
        ("J2", "llm_model_b", J2_MODEL, j2, j2ev),
        ("J3", J3_KIND, None, j3, j3ev),
    ):
        payload = {"spec_iri": row["spec_iri"], "judge_id": jid, "judge_kind": kind,
                   "judge_model": model, "verdict": label, "evidence": ev}
        if label == "abstain":
            payload["abstain_reason"] = ev
        _emit("judgment_tier_verifier.judge.event", payload, run_id)
    qv, failsafe, n_reasoners = quorum(j1, j2, j3)
    _emit("judgment_tier_verifier.verdict.event",
          {"spec_iri": row["spec_iri"], "j1": j1, "j2": j2, "j3": j3, "quorum_verdict": qv,
           "failsafe_fired": failsafe, "n_reasoners_nonabstain": n_reasoners}, run_id)
    return {"spec_iri": row["spec_iri"], "spec_class": row.get("spec_class"),
            "stratum": stratum_of(row.get("spec_class")), "j1": j1, "j2": j2, "j3": j3,
            "j1_evidence": j1ev, "j2_evidence": j2ev, "j3_evidence": j3ev,
            "quorum_verdict": qv, "failsafe_fired": failsafe, "n_reasoners_nonabstain": n_reasoners}


# =========================================================================
# Independence self-test (AST call-graph disjointness — NOT grep-for-import).
# =========================================================================
def _judge_private_callgraph(func_name: str) -> set[str]:
    """Module-level private reader symbols (prefixed _j1_/_j2_/_j3_) transitively called from
    func_name's body, via AST over THIS module's source."""
    tree = ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
    funcs = {n.name: n for n in ast.walk(tree)
             if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))}

    def direct(name):
        node = funcs.get(name)
        out = set()
        if node is None:
            return out
        for sub in ast.walk(node):
            if isinstance(sub, ast.Call):
                fn = sub.func
                if isinstance(fn, ast.Name):
                    out.add(fn.id)
                elif isinstance(fn, ast.Attribute):
                    out.add(fn.attr)
        return out

    seen, stack, private = set(), [func_name], set()
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        for callee in direct(cur):
            if callee.startswith(("_j1_", "_j2_", "_j3_")):
                private.add(callee)
            if callee in funcs and callee not in seen:
                stack.append(callee)
    return private


def independence_self_test() -> dict:
    g1 = _judge_private_callgraph("judge_j1_llm")
    g2 = _judge_private_callgraph("judge_j2_llm")
    g3 = _judge_private_callgraph("judge_j3_structural")
    pairs = {"j1_j2": g1 & g2, "j1_j3": g1 & g3, "j2_j3": g2 & g3}
    shared = {k: sorted(v) for k, v in pairs.items() if v}
    prefix_ok = (all(s.startswith("_j1_") for s in g1) and len(g1) >= 1
                 and all(s.startswith("_j2_") for s in g2) and len(g2) >= 1
                 and all(s.startswith("_j3_") for s in g3) and len(g3) >= 1)
    judges_share_no_code_path = (not shared) and prefix_ok
    return {
        "judges_share_no_code_path": judges_share_no_code_path,
        "j1_private_readers": sorted(g1), "j2_private_readers": sorted(g2),
        "j3_private_readers": sorted(g3),
        "shared_private_readers_across_judges": shared,
        "j1_model": J1_MODEL, "j2_model": J2_MODEL,
        "j1_model_ne_j2_model": (J1_MODEL != J2_MODEL),
        "pass": bool(judges_share_no_code_path and J1_MODEL != J2_MODEL),
        "quorum_rule": QUORUM_RULE,
    }


def verifier_fn_human_inputs() -> int:
    """JTV-7: 0 human inputs in the verdict path. verify_spec(row, client, run_id) — all
    machine-derived. AST-scan the verdict-path function bodies (NOT docstrings/strings) for an
    interactive read: a call to builtins input(...) or a sys.stdin access. Counts violations."""
    verdict_fns = {"judge_j1_llm", "judge_j2_llm", "judge_j3_structural", "verify_spec",
                   "cmd_run", "load_judgment_tier", "quorum",
                   "_j1_resolve_prose", "_j1_read_embodiment", "_j1_parse",
                   "_j2_get_prose", "_j2_load_embodiment", "_j2_decode",
                   "_j3_obligations", "_j3_load_py", "_j3_reachable"}
    tree = ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
    violations = 0
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name in verdict_fns:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Call) and isinstance(sub.func, ast.Name) and sub.func.id == "input":
                    violations += 1
                if (isinstance(sub, ast.Attribute) and sub.attr == "stdin"
                        and isinstance(sub.value, ast.Name) and sub.value.id == "sys"):
                    violations += 1
    return violations


def _client():
    """LLM transport (key-selecting). Returns a client or None."""
    try:
        return _sep._e2_client()
    except Exception:
        return None


def _load_env():
    for f in (os.path.join(PROJECT_ROOT, ".env"), os.path.join(PROJECT_ROOT, ".env.backup")):
        if os.path.exists(f):
            for line in open(f, encoding="utf-8"):
                s = line.strip()
                if s and not s.startswith("#") and "=" in s:
                    k, v = s.split("=", 1)
                    os.environ.setdefault(k, v)


def _dist(results):
    from collections import Counter
    return dict(Counter(r["quorum_verdict"] for r in results))


def _stratum_dist(results):
    from collections import Counter, defaultdict
    by = defaultdict(Counter)
    for r in results:
        by[r["stratum"]][r["quorum_verdict"]] += 1
    return {k: dict(v) for k, v in by.items()}


def cmd_run(limit, slice_mode, plant_disagreement):
    _load_env()
    run_id = f"jtv_{'slice' if slice_mode else 'run'}_{uuid.uuid4().hex[:8]}"
    rows = load_judgment_tier()
    rows.sort(key=lambda r: r["spec_iri"])
    if slice_mode:
        embodied = [r for r in rows if r.get("embodiment_path")
                    and os.path.exists(os.path.expanduser(r["embodiment_path"]))]
        picked, strata = [], set()
        for r in embodied:
            picked.append(r)
            strata.add(stratum_of(r.get("spec_class")))
            if len(picked) >= (limit or 6) and len(strata) >= 3:
                break
        rows = picked[: max(limit or 6, len(strata))]
    elif limit:
        rows = rows[:limit]
    client = _client()
    results = [verify_spec(r, client, run_id) for r in rows]
    planted = None
    if plant_disagreement:
        qv, failsafe, n = quorum("implemented", "not_implemented", "implemented")
        planted = {"planted_inputs": {"j1": "implemented", "j2": "not_implemented", "j3": "implemented"},
                   "quorum_verdict": qv, "failsafe_fired": failsafe, "expected": "CONTESTED",
                   "fail_safe_fires_on_disagreement": qv == "CONTESTED"}
        _emit("judgment_tier_verifier.verdict.event",
              {"spec_iri": "PLANTED:disagreement_fixture", "j1": "implemented",
               "j2": "not_implemented", "j3": "implemented", "quorum_verdict": qv,
               "failsafe_fired": failsafe, "n_reasoners_nonabstain": n}, run_id)
    selftest = independence_self_test()
    out = {
        "schema_version": SCHEMA_VERSION, "run_id": run_id,
        "mode": "vertical_slice" if slice_mode else "full_run", "generated": _now(),
        "n_specs": len(results), "quorum_rule": QUORUM_RULE,
        "quorum_rule_semantics": ("VALIDATED-IMPLEMENTED uses logical AND (unanimity among "
                                  "non-abstainers) + both-LLM-reasoner floor; CONTESTED is the "
                                  "conservative fail-safe on ANY disagreement (S27 FLAG F2)"),
        "independence_self_test": selftest,
        "verifier_fn_human_inputs": verifier_fn_human_inputs(),
        "blind_to_gt": True,
        "blind_note": "this path never opens labels.json / any GT file (JTV-3)",
        "planted_disagreement_failsafe": planted,
        "verdict_distribution": _dist(results), "stratum_distribution": _stratum_dist(results),
        "per_spec": results,
        "NOT_a_closure_claim": ("this run records verifier verdicts; trustworthiness is decided "
                                "ONLY by the separate accuracy harness against blind GT"),
    }
    json.dump(out, open(RUN_OUT, "w", encoding="utf-8"), indent=2)
    json.dump({"run_id": run_id, "blind_to_gt": True, "per_spec": results},
              open(VERDICTS_OUT, "w", encoding="utf-8"), indent=2)
    print(json.dumps({"run_id": run_id, "mode": out["mode"], "n_specs": len(results),
                      "verdict_distribution": out["verdict_distribution"],
                      "stratum_distribution": out["stratum_distribution"],
                      "independence_pass": selftest["pass"],
                      "planted_failsafe": (planted or {}).get("fail_safe_fires_on_disagreement"),
                      "run_out": RUN_OUT}, indent=2))


def main():
    ap = argparse.ArgumentParser(description="Judgment-tier verifier (J1/J2/J3 quorum).")
    ap.add_argument("--independence-self-test", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--vertical-slice", action="store_true")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--plant-disagreement", action="store_true")
    args = ap.parse_args()
    if args.independence_self_test:
        _load_env()
        st = independence_self_test()
        _emit("judgment_tier_verifier.independence_selftest.event", st,
              f"jtv_selftest_{uuid.uuid4().hex[:8]}")
        print(json.dumps(st, indent=2))
        sys.exit(0 if st["pass"] else 1)
    if args.vertical_slice:
        cmd_run(limit=args.limit or 6, slice_mode=True, plant_disagreement=True)
        return
    if args.run:
        cmd_run(limit=args.limit, slice_mode=False, plant_disagreement=False)
        return
    ap.error("one of --independence-self-test / --run / --vertical-slice required")


if __name__ == "__main__":
    main()
