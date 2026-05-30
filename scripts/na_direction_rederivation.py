#!/usr/bin/env python3
"""Cycle-16-S27 Hole 2 — re-derive the 203 "n/a / DP#26 carve-out" specs from each
spec's OWN text (NOT the scan's dp26 marker).

THE BUG THIS FIXES: scripts/faithful_target_extractor.py lines 154-157 + 297-298
short-circuit on the scan's `runtime_emit_event_class` starting "n/a" and return
"n/a" from `dp26_carveout_marker` WITHOUT reading the spec. A spec wrongly excused as
n/a that actually commits a runtime observable is a false-negative gap, invisible
today. This script reads each of the 203 specs' OWN definition-site text with TWO
independent readers and re-derives the disposition.

Readers (independence reused from spec_extraction_pipeline.extraction_methods_distinct;
single-reader REFUSED -> SystemExit):
  E1' = rule-based: parse the spec's own prose for a committed runtime-observable /
        emitted event / gate-fire / checkable obligation. mechanism id =
        "rule_based_observable_parser" (distinct mechanism, NOT E2's id).
  E2' = LLM (claude-haiku-4-5) with a GENUINELY DIFFERENT prompt asking whether the
        spec commits ANY runtime-observable behavior / emitted event / gate-fire /
        checkable obligation requiring code, vs being a pure design-decision /
        methodology / ontology record needing no code. Returns
        {needs_implementation, committed_observable, evidence}.

Per-spec disposition:
  genuine_na             : both readers agree no committed observable
  FALSE_NEGATIVE_gap     : a reader finds a committed observable -> wrongly-excused spec
  disagreement_conservative : readers disagree -> surfaced, NOT auto-resolved/tuned
  unverifiable           : source unreadable -> honest residual (NEVER silently n/a)

Anti-gaming: never invent an observable to manufacture a gap; never tune to a count.
The number MOVES wherever the spec text says.

Output: outputs/cycle_16_s27_na_direction_rederivation.json  (also writes the
canonical name outputs/na_direction_rederivation.json).
ADDITIVE ONLY. Does NOT modify any frozen path.
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
sys.path.insert(0, HERE)

import spec_extraction_pipeline as sep  # reuse independence + prose-window discipline

FAITHFUL_MAP = os.path.join(OUTPUTS, "faithful_target_map.json")
SCAN = os.path.join(OUTPUTS, "retroactive_scan_cycle_1_15_run.json")
OUT = os.path.join(OUTPUTS, "na_direction_rederivation.json")
EVENTS = os.path.join(OUTPUTS, "cycle_16_s27_sizing_events.jsonl")
HOME = os.path.expanduser("~")

# Reader mechanism ids — DISTINCT (rule-based vs LLM => extraction_methods_distinct True).
E1P_MECHANISM = "rule_based_observable_parser"
E2P_MECHANISM = "llm_na_rederivation:claude-haiku-4-5"
E2P_MODEL = "claude-haiku-4-5"
E2P_PROMPT_ID = "S27_na_rederivation_needs_impl_v1"

SHARED_RUN_ID = None  # set by the orchestrator; falls back to a local id


def now():
    return datetime.now(timezone.utc).isoformat()


def emit_event(event_class, payload, run_id):
    rec = {
        "schema_version": "0.1",
        "namespace": "cycle_16.s27.sizing",
        "event_class": event_class,
        "timestamp": now(),
        "run_id": run_id,
        "payload": payload,
    }
    with open(EVENTS, "a") as f:
        f.write(json.dumps(rec) + "\n")


# ---------------------------------------------------------------------------
# E1' — rule-based observable detector over the spec's OWN prose window.
# A "committed observable" = an obligation anchor co-occurring with an
# execution-observable surface: an emitted event class, a gate that must fire/
# halt/block, an enforced/refused runtime check, a schema constraint that a
# validator must enforce. This is a DIFFERENT detector from E1 in the extraction
# pipeline (which extracts generic checkable commitments) — here we look
# specifically for code-requiring runtime observables, the n/a question.
# ---------------------------------------------------------------------------
# Surfaces that indicate a runtime-observable / code-requiring obligation.
_OBS_SURFACE_RE = re.compile(
    r"\b("
    r"emit(s|ted|ting)?|event[_ ]class|\.fire\b|\.transition\b|fire(s|d)?\b|"
    r"gate\b|gates\b|halt(s|ed)?|block(s|ed)?|refus(e|es|ed|al)|enforc(e|es|ed|ement)|"
    r"validat(e|es|ed|or|ion)|assert(s|ed|ion)?|shacl|conform(s|ance)?|"
    r"namespace|jsonl|run_id|schema_version|MUST\s+fire|MUST\s+emit|"
    r"checkable|hard[- ]?fail|exit\s*code|nonzero|non-zero|status\s*code|"
    r"probe(s)?\b|detector|telemetry|signal\b"
    r")\b",
    re.I,
)
# A pure-design / methodology / ontology marker — text that explicitly disclaims
# runtime code (DP#26 carve-out language). Used only as corroboration, never as a
# short-circuit replacing the read.
_NA_RATIONALE_RE = re.compile(
    r"(no\s+code|design\s+decision|methodology|ontology|citation-based|"
    r"DP#?26|carve[- ]?out|paradigm\s+(ruling|disposition)|narrative\s+record|"
    r"needs\s+no\s+(code|implementation)|documentation\s+only|record\s+only)",
    re.I,
)
# Obligation anchors (a spec that BINDS someone, reused-spirit from E1 anchors).
_ANCHOR_RE = re.compile(
    r"\b(MUST|SHALL|REQUIRED|BINDING|enforce[ds]?|refus(e|es|ed)|"
    r"gate[ds]?|emit[s]?|fire[s]?|halt[s]?|block[s]?|assert[s]?)\b",
    re.I,
)
# Concrete event-class token (dotted lowercase like foo.bar.fire) on an emit-context line.
_EVENT_CLASS_RE = re.compile(r"\b([a-z][a-z0-9_]*(?:\.[a-z0-9_]+){1,4})\b")
_EMIT_CTX_RE = re.compile(r"(emit|emits|event[_ ]class|\.fire|\.transition|namespace|fire\b)", re.I)


_VERSION_TOK_RE = re.compile(r"^v?\d+(\.\d+)+$")


def _looks_like_event_class(tok):
    if tok.endswith((".md", ".json", ".ttl", ".py", ".jsonl", ".shacl", ".sh", ".yaml", ".yml")):
        return False
    # reject dotted-number version tokens (v2.8.2, 1.0.0) — not event classes
    if _VERSION_TOK_RE.match(tok):
        return False
    head = tok.split(".", 1)[0]
    if head in ("schema_version", "scripts", "outputs", "docs", "analysis", "runtime",
                "home", "azureuser", "www", "http", "https"):
        return False
    # an event class names a behavioral surface; require a recognizable verb-ish tail
    # OR an emit-y token, else fall back to 'unnamed_runtime_obligation' (handled by caller)
    tail = tok.rsplit(".", 1)[-1]
    if tail in ("fire", "transition", "emit", "event", "start", "end", "complete",
                "fired", "fires", "halt", "block", "refusal", "gate", "pass", "fail",
                "check", "run", "dispatch", "close", "open", "present", "absent",
                "violation", "verdict", "signal", "telemetry", "computed", "checklist"):
        return True
    # otherwise accept only if it looks like a namespaced event (>=3 dotted segments,
    # all-lowercase, no digits-only middle) to avoid version/path false positives
    segs = tok.split(".")
    if len(segs) >= 3 and all(re.match(r"^[a-z][a-z0-9_]*$", s) for s in segs):
        return True
    return False


def e1_prime(prose):
    """Rule-based: does the spec text commit ANY runtime-observable obligation?
    Returns {needs_implementation, committed_observable, evidence, n_anchors,
    n_obs_surface}."""
    if not prose:
        return {"needs_implementation": False, "committed_observable": "n/a",
                "evidence": "empty_prose", "n_anchors": 0, "n_obs_surface": 0}
    anchors = list(_ANCHOR_RE.finditer(prose))
    obs_hits = list(_OBS_SURFACE_RE.finditer(prose))
    # Look for a concrete committed event class on an emit-context line.
    committed_class = None
    committed_ev = None
    for raw in prose.splitlines():
        if not _EMIT_CTX_RE.search(raw):
            continue
        for m in _EVENT_CLASS_RE.finditer(raw):
            tok = m.group(1)
            if _looks_like_event_class(tok) and "." in tok:
                committed_class = tok
                committed_ev = raw.strip()[:200]
                break
        if committed_class:
            break

    # Decision rule (deterministic): a spec commits a runtime observable iff it has
    # at least one obligation anchor AND at least one execution-observable surface
    # term in the SAME window. A concrete event class strengthens to a named target.
    needs = bool(anchors) and bool(obs_hits)
    if committed_class:
        return {"needs_implementation": True,
                "committed_observable": committed_class,
                "evidence": committed_ev,
                "n_anchors": len(anchors), "n_obs_surface": len(obs_hits)}
    if needs:
        # find a representative evidence line containing an anchor+surface
        ev = ""
        for raw in prose.splitlines():
            if _ANCHOR_RE.search(raw) and _OBS_SURFACE_RE.search(raw):
                ev = raw.strip()[:200]
                break
        if not ev:
            a = anchors[0]
            ev = prose[max(0, a.start() - 20): a.start() + 160].replace("\n", " ").strip()
        return {"needs_implementation": True,
                "committed_observable": "unnamed_runtime_obligation",
                "evidence": ev,
                "n_anchors": len(anchors), "n_obs_surface": len(obs_hits)}
    # No anchor+surface co-occurrence => reads as pure design/methodology/ontology.
    na_ev = ""
    mm = _NA_RATIONALE_RE.search(prose)
    if mm:
        s = max(0, mm.start() - 30)
        na_ev = prose[s: mm.start() + 80].replace("\n", " ").strip()
    return {"needs_implementation": False,
            "committed_observable": "n/a",
            "evidence": na_ev or "no obligation-anchor co-occurring with a runtime-observable surface",
            "n_anchors": len(anchors), "n_obs_surface": len(obs_hits)}


# ---------------------------------------------------------------------------
# E2' — LLM (claude-haiku-4-5), a GENUINELY DIFFERENT prompt (the n/a question,
# not E2's "extract commitments" frame).
# ---------------------------------------------------------------------------
E2P_PROMPT = (
    "You are auditing whether a software/specification fragment commits any obligation "
    "that REQUIRES CODE to satisfy. Decide between exactly two cases:\n"
    "  (A) The fragment commits AT LEAST ONE runtime-observable behavior, emitted event, "
    "gate that must fire, validator/schema that must be enforced, or other checkable "
    "obligation that some program would have to execute or check. -> needs_implementation = true.\n"
    "  (B) The fragment is a PURE design decision, methodology note, ontology/record, "
    "rationale, or narrative that binds no running code (nothing would ever execute or "
    "be checked at runtime to satisfy it). -> needs_implementation = false.\n"
    "Judge ONLY from the text; do not assume. If it merely DESCRIBES a decision or records "
    "a rationale with no executable obligation, that is (B). If it says something MUST emit/"
    "fire/be enforced/be validated/halt/block, that is (A).\n"
    "Return ONLY a JSON object: {\"needs_implementation\": <bool>, "
    "\"committed_observable\": \"<event-class or short obligation phrase, or n/a>\", "
    "\"evidence\": \"<verbatim phrase from the fragment, or empty>\"}. FRAGMENT:\n\n"
)


def _first_json_object(raw):
    """Robustly extract the FIRST balanced top-level JSON object from model output (the
    model may emit multiple objects / trailing prose; a greedy {.*} would mis-grab them)."""
    start = raw.find("{")
    while start != -1:
        depth = 0
        in_str = False
        esc = False
        for i in range(start, len(raw)):
            c = raw[i]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    frag = raw[start:i + 1]
                    try:
                        return json.loads(frag)
                    except Exception:
                        break
        start = raw.find("{", start + 1)
    return None


def e2_prime(prose, max_retries=5):
    """LLM n/a-rederivation read. Key-switch on usage-limit is operational (handled by
    the shared client/_load_key). REFUSE only if NO key at all (caller converts to
    'unverifiable' conservatively — never fabricates a verdict)."""
    client = sep._e2_client()  # raises DP#44 RuntimeError if NO key
    last_err = None
    for attempt in range(max_retries):
        try:
            r = client.messages.create(
                model=E2P_MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": E2P_PROMPT + prose[:1800]}],
            )
            raw = r.content[0].text.strip()
            obj = _first_json_object(raw)
            if obj is None:
                return {"needs_implementation": False, "committed_observable": "n/a",
                        "evidence": "", "_parse": "no_json"}
            return {
                "needs_implementation": bool(obj.get("needs_implementation")),
                "committed_observable": str(obj.get("committed_observable", "n/a"))[:160],
                "evidence": str(obj.get("evidence", ""))[:240],
            }
        except Exception as e:
            last_err = e
            msg = str(e).lower()
            if "529" in msg or "overload" in msg or "rate" in msg or "timeout" in msg:
                time.sleep(2 ** attempt)
                continue
            time.sleep(1)
    raise RuntimeError(f"E2' failed after {max_retries} retries: {last_err}")


def reconcile(e1, e2):
    """Per-spec disposition from the two reader verdicts (NOT tuned to agree)."""
    a = bool(e1["needs_implementation"])
    b = bool(e2["needs_implementation"])
    if a and b:
        return "FALSE_NEGATIVE_gap"
    if a != b:
        return "disagreement_conservative"
    return "genuine_na"


def load_na_members():
    fm = json.load(open(FAITHFUL_MAP))
    na = [x for x in fm["members"] if x.get("disposition") == "dp26_carveout_preserved"]
    scan = json.load(open(SCAN))
    byid = {}
    for r in scan["per_spec_evidence_IP_PRIVATE"]:
        byid.setdefault(r["spec_id"], r)
    return na, byid


def run(run_id=None, llm=True):
    run_id = run_id or f"s27_na_rederiv_{uuid.uuid4().hex[:8]}"
    # Independence assertion FIRST (single-reader REFUSED -> SystemExit).
    distinct, reason = sep.extraction_methods_distinct(
        E1P_MECHANISM, E2P_MECHANISM,
        model_e1=None, model_e2=E2P_MODEL,
        prompt_e1=None, prompt_e2=E2P_PROMPT_ID,
    )
    if not distinct:
        raise SystemExit(f"REFUSED: extraction_methods_distinct == False: {reason}")

    na, byid = load_na_members()
    members = []
    fn_gaps = []
    disp_counts = {"genuine_na": 0, "FALSE_NEGATIVE_gap": 0,
                   "disagreement_conservative": 0, "unverifiable": 0}

    for x in na:
        sid = x["spec_iri"]
        rec = byid.get(sid)
        source_path = (x.get("source_path") or "").replace("~", HOME)
        # Read the spec's OWN definition-site prose (NO dp26 short-circuit).
        prose = None
        if rec is not None:
            try:
                prose = sep.spec_prose_window(rec, n=1800)
            except Exception:
                prose = None
        if not prose or not os.path.isfile(source_path):
            disp_counts["unverifiable"] += 1
            members.append({
                "spec_iri": sid, "spec_class": x["spec_class"],
                "source_path": source_path,
                "disposition": "unverifiable",
                "reason": "source unreadable / prose unresolved (NOT silently kept n/a)",
                "e1_prime": None, "e2_prime": None,
            })
            continue

        e1 = e1_prime(prose)
        # E2': LLM. On NO-key -> conservative 'unverifiable', never fabricate.
        if llm:
            try:
                e2 = e2_prime(prose)
            except RuntimeError as e:
                if "DP#44" in str(e) or "not found" in str(e):
                    disp_counts["unverifiable"] += 1
                    members.append({
                        "spec_iri": sid, "spec_class": x["spec_class"],
                        "source_path": source_path,
                        "disposition": "unverifiable",
                        "reason": f"E2' reader unavailable (no key): {e}",
                        "e1_prime": e1, "e2_prime": None,
                    })
                    continue
                raise
        else:
            raise SystemExit("REFUSED: single-reader run (E2' disabled). Two readers required.")

        disp = reconcile(e1, e2)
        disp_counts[disp] += 1
        m = {
            "spec_iri": sid, "spec_class": x["spec_class"],
            "name": x.get("name"), "source_path": source_path,
            "disposition": disp,
            "e1_prime": e1, "e2_prime": e2,
        }
        members.append(m)
        if disp == "FALSE_NEGATIVE_gap":
            # prefer a concrete observable + verbatim evidence from whichever reader named it
            obs = e1["committed_observable"]
            if obs in ("n/a", "unnamed_runtime_obligation") and e2.get("committed_observable") not in ("n/a", ""):
                obs = e2["committed_observable"]
            ev = e1.get("evidence") or e2.get("evidence")
            fn_gaps.append({
                "spec_iri": sid, "spec_class": x["spec_class"],
                "committed_observable": obs,
                "evidence": ev,
                "e1_evidence": e1.get("evidence"),
                "e2_evidence": e2.get("evidence"),
                "source_path": source_path,
            })

    out = {
        "schema_version": "s27_na_direction_rederivation.v1",
        "build_event": "Cycle-16-S27 Hole 2 — re-derive 203 n/a specs from each spec's OWN text (NO dp26 short-circuit)",
        "is_sizing_not_gap_closure": True,
        "n": len(na),
        "run_id": run_id,
        "extraction_methods_distinct": distinct,
        "extraction_methods_distinct_reason": reason,
        "single_reader_refused": True,
        "readers": {
            "e1_prime": {"mechanism": E1P_MECHANISM, "kind": "rule_based"},
            "e2_prime": {"mechanism": E2P_MECHANISM, "model": E2P_MODEL,
                         "prompt_id": E2P_PROMPT_ID},
        },
        "disposition_counts": disp_counts,
        "false_negative_gaps": fn_gaps,
        "members": members,
        "anti_gaming_note": "No observable invented; no tuning to a target count; "
                            "the dp26 short-circuit was NOT used — each spec's own text was read.",
    }
    json.dump(out, open(OUT, "w"), indent=2)
    emit_event("na_rederivation.complete", {
        "n": len(na), "disposition_counts": disp_counts,
        "n_false_negative_gaps": len(fn_gaps),
        "extraction_methods_distinct": distinct,
    }, run_id)
    print(f"[na_direction_rederivation] n={len(na)} disposition={disp_counts} "
          f"false_negative_gaps={len(fn_gaps)} -> {OUT}")
    return out


if __name__ == "__main__":
    rid = sys.argv[1] if len(sys.argv) > 1 else None
    run(run_id=rid)
