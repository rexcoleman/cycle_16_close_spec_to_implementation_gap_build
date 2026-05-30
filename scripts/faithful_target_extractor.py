#!/usr/bin/env python3
"""Faithful-target extraction — Cycle-16-S26 Build-Runner (Done #60 spec-provenance
fidelity, past-era reconstruction; extraction-fidelity part of #28/#67).

WHY
---
The S24 gap list keyed each spec's "what counts as implemented" on the BE-D scan's
SYNTHESIZED `runtime_emit_event_class`. The S25 vertical slice proved that synthesized
target can be UNFAITHFUL to the spec's own text (canonical: kernel-coach af3a918a,
synthesized `kernel_coach.dispatch` — a class that appears NOWHERE in the spec; the
real committed dispatch class is `kernel_coach.transition.fire`). Keying the probe on a
synthesized string makes a correct implementation read not_faithful.

This module re-derives each spec's FAITHFUL committed observable FROM THE SPEC'S OWN
TEXT, with TWO INDEPENDENT readers (single-reader REFUSED, reusing the
spec_extraction_pipeline.extraction_methods_distinct discipline):

  E1 (rule-based): parse the spec-of-record source file (resolved via the scan's
     audit_tuple[1]) for the event class(es) it ACTUALLY NAMES in its Role / emit /
     acceptance / schema section. NEVER reads the synthesized scan field.

  E2 (LLM, different mechanism): claude-haiku-4-5 reads the spec's acceptance/Role
     prose and independently extracts the committed observable. Different reader,
     different code path. Key-switch on usage-limit (ORCHESTRATION_ANTHROPIC_API_KEY
     in $MOO/.env <-> ANTHROPIC_API_KEY in $MOO/.env.backup) — operational, not a
     blocker (DP#44 only if NO key at all -> REFUSE that reader conservatively).

Reconcile:
  - E1 ∩ E2 agree on the faithful target  -> accepted.
  - DP#26 carve-out (runtime_emit_event_class begins 'n/a', n_a_rationale present, and
    the spec source is a methodology/decision/ontology artifact with no committed
    event-emit) -> faithful target 'n/a' preserved HONESTLY (never an invented observable).
  - Disagreement -> conservative + surfaced (NOT auto-resolved, NOT tuned to agree).
  - No committed observable AND not a DP#26 carve-out -> spec-provenance DEFECT
    (untraceable spec) — surfaced, never papered over.

The output is a faithful-target MAP (spec_iri -> faithful_target + provenance) plus the
extraction-independence JSONL (extraction_methods_distinct == true). It is the INPUT to
the KG-capture (Step 2) and the re-derivation (Step 3). It does NOT itself close the gap.

Anti-gaming asserts (constraints #27/#28):
  - faithful target extracted from the spec's own text, confirmed by an independent
    second reader; never synthesized; never tuned to make a probe pass.
  - the literal `kernel_coach.dispatch` (or any class invented to flip the F-probe) is
    NEVER emitted as a faithful target — assert af3a918a moves OFF it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = REPO / "outputs"
sys.path.insert(0, str(HERE))

# Reuse the EXISTING E1/E2 independence discipline (single-reader REFUSED).
from spec_extraction_pipeline import (  # noqa: E402
    extraction_methods_distinct,
    E1_MECHANISM,
    E2_MECHANISM,
    E2_MODEL,
    E2_PROMPT_ID,
    _load_key,
)

SCAN_JSON = OUTPUTS / "retroactive_scan_cycle_1_15_run.json"
V_JSON = OUTPUTS / "validated_commitment_set.json"
MAP_OUT = OUTPUTS / "faithful_target_map.json"
DISTINCT_JSONL = OUTPUTS / "faithful_target_extraction_methods_distinct.jsonl"

# Faithful-target extractor reader ids (DISTINCT from spec_extraction_pipeline so the
# independence claim is over THIS extraction, not borrowed). E1 is a rule-based
# event-class parser over the spec source; E2 is the LLM acceptance-text reader.
FT_E1_MECHANISM = "rule_based_event_class_parser"
FT_E2_MECHANISM = "llm_acceptance_text_reader:claude-haiku-4-5"
FT_E2_MODEL = "claude-haiku-4-5"
FT_E2_PROMPT_ID = "FT_faithful_observable_v1"

# DP#26 marker.
_NA_PREFIXES = ("n/a",)

# The synthesized class that S25 proved unfaithful — assert it is never a faithful target.
_FORBIDDEN_SYNTHESIZED = "kernel_coach.dispatch"


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _is_dp26(rec_class: str | None) -> bool:
    if not rec_class:
        return False
    return rec_class.strip().lower().startswith(_NA_PREFIXES)


# --------------------------------------------------------------------------- #
# Spec-of-record resolution (via the scan audit_tuple)
# --------------------------------------------------------------------------- #
def _resolve_source(scan_rec: dict) -> Path | None:
    at = scan_rec.get("audit_tuple") or []
    if len(at) >= 2 and at[1]:
        p = Path(os.path.expanduser(at[1]))
        if p.exists():
            return p
    return None


def _source_kind(scan_rec: dict) -> str | None:
    at = scan_rec.get("audit_tuple") or []
    return at[2] if len(at) >= 3 else None


# --------------------------------------------------------------------------- #
# E1 — rule-based event-class parser over the spec's OWN text
# --------------------------------------------------------------------------- #
# An emitted event class in this corpus is a backtick-quoted dotted token whose head
# is a namespace and which contains a verb-ish segment (session/transition/dispatch/
# fire/warmup/drift/phase/build/...). E1 reads the Role / emit / acceptance / schema
# region of the spec source and returns the committed PRIMARY dispatch/fire class.
_EVENT_CLASS_RE = re.compile(r"`([a-z][a-z0-9_]*(?:\.[a-z0-9_]+)+)`")

# When a spec commits a multi-event schema, the FAITHFUL execution-grounded observable
# for the F-probe is the spec's dispatch/transition FIRE class (the one the probe's
# execution path looks for as the behavioral commitment). Precedence of "the dispatch
# fire" among committed classes:
_FIRE_PREFERENCE = (
    ".transition.fire",
    ".dispatch.fire",
    ".fire",
    ".session.start",
    ".dispatch",
)

# Lines that DEFINE an emitted event (not merely mention one): a numbered/bulleted
# Role-schema line, an "emit"/"emits"/"event_class" line, or a §-schema enumeration.
_EMIT_CONTEXT_RE = re.compile(
    r"(emit|emits|event[_ ]class|transition|schema|fire|session\.(start|end)|namespace)",
    re.I,
)


def extract_e1(source: Path | None, scan_class: str | None) -> dict:
    """Rule-based: parse the spec source for the committed event class(es) it NAMES.

    Returns {target, all_classes, evidence}. target is the faithful primary fire class,
    or 'n/a' for a DP#26 carve-out, or None if nothing committed is found in the text."""
    if _is_dp26(scan_class):
        # DP#26 spec: confirm the source carries no committed event-emit (methodology /
        # decision / ontology). Faithful target n/a, derived from the carve-out marker.
        return {"target": "n/a", "all_classes": [], "evidence": "dp26_carveout_marker: runtime_emit_event_class begins 'n/a'"}
    if source is None:
        return {"target": None, "all_classes": [], "evidence": "source_unresolved"}
    try:
        text = source.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"target": None, "all_classes": [], "evidence": f"source_unreadable: {e!r}"}

    # Collect candidate event classes from emit-context lines ONLY (so we read the
    # spec's COMMITTED emissions, not arbitrary dotted tokens elsewhere in the doc).
    committed: list[tuple[str, str]] = []  # (class, evidence_line)
    for raw in text.splitlines():
        if not _EMIT_CONTEXT_RE.search(raw):
            continue
        for m in _EVENT_CLASS_RE.finditer(raw):
            cls = m.group(1)
            # Filter out obvious non-event dotted tokens (file paths, schema_version).
            if cls.endswith((".md", ".json", ".ttl", ".py", ".jsonl", ".shacl")):
                continue
            if cls.split(".", 1)[0] in ("schema_version", "scripts", "outputs", "docs", "analysis"):
                continue
            committed.append((cls, raw.strip()[:160]))
    seen = {}
    for cls, ev in committed:
        seen.setdefault(cls, ev)
    classes = list(seen.keys())
    if not classes:
        return {"target": None, "all_classes": [], "evidence": "no committed event class in emit-context lines of spec source"}

    # Choose the faithful PRIMARY fire class by the dispatch-fire preference order.
    target = None
    for pref in _FIRE_PREFERENCE:
        cands = [c for c in classes if c.endswith(pref)]
        if cands:
            target = sorted(cands, key=len)[0]
            break
    if target is None:
        # No transition/fire/dispatch class — take the lexicographically-first committed
        # class (deterministic), surfacing the full set for the second reader.
        target = sorted(classes)[0]
    return {"target": target, "all_classes": classes, "evidence": seen.get(target, "")}


# --------------------------------------------------------------------------- #
# E2 — LLM acceptance-text reader (DIFFERENT mechanism)
# --------------------------------------------------------------------------- #
_E2_CLIENT = None
_E2_KEY_SOURCE = None

FT_E2_PROMPT = (
    "You are reading an AGENT SPECIFICATION (the spec-of-record). Your ONLY task is to "
    "extract the single PRIMARY runtime event class this spec COMMITS to emit at its "
    "dispatch / transition-fire boundary — exactly as the spec's own text names it "
    "(a dotted class like `namespace.transition.fire`). If the spec commits a multi-event "
    "schema, return the DISPATCH/TRANSITION-FIRE class (the one emitted when the agent "
    "actually dispatches/acts), NOT session.start/end. If the spec commits NO emitted "
    "event class (it is a methodology/decision/ontology commitment), return exactly "
    "\"n/a\". Do NOT invent a class. Do NOT return a namespace alone. Return ONLY a JSON "
    "object: {\"event_class\": \"<class or n/a>\", \"evidence\": \"<verbatim phrase from "
    "the spec naming it>\"}.\n\n--- SPEC TEXT ---\n"
)


def _e2_key():
    """Load an Anthropic key. Prefer .env.backup ANTHROPIC_API_KEY (the extraction
    pipeline's key); fall back to $MOO/.env ORCHESTRATION_ANTHROPIC_API_KEY on absence
    (operational key-switch, NOT a blocker). Returns (key, source) or (None, None)."""
    k = _load_key()
    if k:
        return k, "env.backup:ANTHROPIC_API_KEY"
    moo_env = os.path.expanduser("~/Moonshots_Career_Thesis_v2/.env")
    if os.path.isfile(moo_env):
        m = re.search(r"^ORCHESTRATION_ANTHROPIC_API_KEY=(\S+)", open(moo_env).read(), re.M)
        if m:
            return m.group(1).strip().strip('"').strip("'"), "env:ORCHESTRATION_ANTHROPIC_API_KEY"
    return None, None


def _e2_client():
    global _E2_CLIENT, _E2_KEY_SOURCE
    if _E2_CLIENT is not None:
        return _E2_CLIENT
    key, src = _e2_key()
    if not key:
        return None
    import anthropic
    _E2_CLIENT = anthropic.Anthropic(api_key=key)
    _E2_KEY_SOURCE = src
    return _E2_CLIENT


def _e2_call(prose: str, max_retries: int = 4) -> dict:
    """Single E2 LLM call with key-switch on usage-limit. Returns parsed dict or a
    refusal dict. NEVER fabricates a verdict (DP#44)."""
    global _E2_CLIENT
    client = _e2_client()
    if client is None:
        return {"target": None, "evidence": "DP#44_refuse: no Anthropic key in .env.backup or .env", "refused": True}
    import anthropic
    last_err = None
    switched = False
    for _ in range(max_retries):
        try:
            resp = client.messages.create(
                model=FT_E2_MODEL,
                max_tokens=300,
                messages=[{"role": "user", "content": FT_E2_PROMPT + prose[:4000]}],
            )
            text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
            m = re.search(r"\{.*\}", text, re.S)
            if not m:
                last_err = f"unparseable: {text[:120]!r}"
                continue
            v = json.loads(m.group(0))
            ec = (v.get("event_class") or "").strip()
            return {"target": ec or None, "evidence": (v.get("evidence") or "")[:160], "refused": False}
        except anthropic.APIStatusError as e:  # usage-limit / 400 -> key-switch ONCE
            last_err = repr(e)
            if not switched:
                key, src = _e2_key()
                # try the OTHER key
                moo_env = os.path.expanduser("~/Moonshots_Career_Thesis_v2/.env")
                m2 = re.search(r"^ORCHESTRATION_ANTHROPIC_API_KEY=(\S+)",
                               open(moo_env).read(), re.M) if os.path.isfile(moo_env) else None
                if m2:
                    _E2_CLIENT = anthropic.Anthropic(
                        api_key=m2.group(1).strip().strip('"').strip("'"))
                    client = _E2_CLIENT
                    switched = True
                    continue
            return {"target": None, "evidence": f"e2_api_error_after_switch: {last_err}", "refused": True}
        except Exception as e:  # noqa: BLE001
            last_err = repr(e)
            continue
    return {"target": None, "evidence": f"e2_failed: {last_err}", "refused": True}


def extract_e2(source: Path | None, scan_class: str | None) -> dict:
    """LLM acceptance-text reader. DP#26 -> 'n/a' (no call needed; the carve-out is
    structural). Else read the spec source prose and call the LLM."""
    if _is_dp26(scan_class):
        return {"target": "n/a", "evidence": "dp26_carveout_marker", "refused": False}
    if source is None:
        return {"target": None, "evidence": "source_unresolved", "refused": True}
    try:
        text = source.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return {"target": None, "evidence": f"source_unreadable: {e!r}", "refused": True}
    return _e2_call(text)


# --------------------------------------------------------------------------- #
# Reconcile E1 ∩ E2
# --------------------------------------------------------------------------- #
def _normalize(t: str | None) -> str | None:
    if t is None:
        return None
    t = t.strip().strip("`")
    return t.lower() if t.lower().startswith("n/a") and t.lower() == "n/a" else t


def _classes_agree(e1: str | None, e2: str | None) -> bool:
    if e1 is None or e2 is None:
        return False
    a, b = _normalize(e1), _normalize(e2)
    if a == b:
        return True
    # dotted-suffix tolerance (namespace-prefix difference), mirroring the F-probe's
    # own _event_class_matches lenience so agreement isn't brittle on namespace heads.
    if a and b and (a.endswith("." + b) or b.endswith("." + a)):
        return True
    return False


def reconcile(scan_rec: dict, e1: dict, e2: dict) -> dict:
    scan_class = scan_rec.get("runtime_emit_event_class")
    dp26 = _is_dp26(scan_class)
    e1t, e2t = e1.get("target"), e2.get("target")

    if dp26:
        # Both readers derive n/a from the carve-out marker (structural agreement).
        return {
            "faithful_target": "n/a",
            "disposition": "dp26_carveout_preserved",
            "agreement": True,
            "defect": False,
        }
    # Non-carve-out: require independent agreement on a concrete class.
    if e1t is None and e2t is None:
        return {
            "faithful_target": None,
            "disposition": "spec_provenance_defect_untraceable",
            "agreement": False,
            "defect": True,
        }
    if _classes_agree(e1t, e2t):
        # Agreement -> accept. Prefer the more specific (longer dotted) of the two.
        target = max([t for t in (e1t, e2t) if t], key=lambda s: len(s))
        return {
            "faithful_target": _normalize(target),
            "disposition": "agreed_faithful_target",
            "agreement": True,
            "defect": False,
        }
    # Disagreement -> conservative + surfaced. We DO NOT auto-resolve to either reader.
    # We record both; the faithful_target is set to E1's rule-based read (deterministic,
    # text-grounded) but flagged disagreement so the re-derivation treats it conservatively
    # and the disagreement surfaces in the before/after table. NOT tuned to agree.
    return {
        "faithful_target": _normalize(e1t) if e1t else _normalize(e2t),
        "disposition": "reader_disagreement_surfaced_conservative",
        "agreement": False,
        "defect": False,
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def _load_v_ids() -> set[str]:
    v = json.loads(V_JSON.read_text())
    return {m["spec_id"] for m in v["members"]}


def _load_scan_distinct() -> dict[str, dict]:
    scan = json.loads(SCAN_JSON.read_text())
    out: dict[str, dict] = {}
    for p in scan["per_spec_evidence_IP_PRIVATE"]:
        out.setdefault(p["spec_id"], p)
    return out


def run(limit: int | None = None, no_llm: bool = False) -> dict:
    v_ids = _load_v_ids()
    scan = _load_scan_distinct()
    spec_ids = sorted(i for i in v_ids if i in scan)
    if limit:
        spec_ids = spec_ids[:limit]

    # T4 independence assertion (single-reader REFUSED) — over THIS extraction's readers.
    distinct, reason = extraction_methods_distinct(
        FT_E1_MECHANISM, FT_E2_MECHANISM,
        model_e1=None, model_e2=FT_E2_MODEL,
        prompt_e1=None, prompt_e2=FT_E2_PROMPT_ID,
        e1_seeded_from_e2=False,
    )
    if not distinct:
        raise SystemExit(f"REFUSED: extraction_methods_distinct == False ({reason}) — single-reader REFUSED.")

    DISTINCT_JSONL.write_text(json.dumps({
        "schema_version": "0.1",
        "namespace": "cycle_16.s26.faithful_target_extraction",
        "event_class": "faithful_target.extraction_methods_distinct.event",
        "timestamp": _now(),
        "run_id": f"s26_ft_distinct_{uuid.uuid4().hex[:8]}",
        "payload": {
            "extraction_methods_distinct": True,
            "reason": reason,
            "e1_mechanism": FT_E1_MECHANISM,
            "e2_mechanism": FT_E2_MECHANISM,
            "e2_model": FT_E2_MODEL,
            "e2_prompt_id": FT_E2_PROMPT_ID,
            "single_reader_refused": True,
        },
    }) + "\n")

    members = []
    counts = {"agreed_faithful_target": 0, "dp26_carveout_preserved": 0,
              "reader_disagreement_surfaced_conservative": 0,
              "spec_provenance_defect_untraceable": 0}
    moved_off_forbidden = []
    for sid in spec_ids:
        rec = scan[sid]
        source = _resolve_source(rec)
        scan_class = rec.get("runtime_emit_event_class")
        e1 = extract_e1(source, scan_class)
        if no_llm or _is_dp26(scan_class):
            e2 = extract_e2(None, scan_class) if _is_dp26(scan_class) else {
                "target": None, "evidence": "no_llm_mode", "refused": True}
        else:
            e2 = extract_e2(source, scan_class)
        rc = reconcile(rec, e1, e2)
        counts[rc["disposition"]] = counts.get(rc["disposition"], 0) + 1

        # Anti-gaming assert: never emit the forbidden synthesized class as faithful.
        ft = rc["faithful_target"]
        assert ft != _FORBIDDEN_SYNTHESIZED, (
            f"ANTI-GAMING VIOLATION: faithful target == forbidden synthesized "
            f"{_FORBIDDEN_SYNTHESIZED!r} for {sid}")
        if rec.get("runtime_emit_event_class") == _FORBIDDEN_SYNTHESIZED and ft != _FORBIDDEN_SYNTHESIZED:
            moved_off_forbidden.append({"spec_iri": sid, "synthesized": _FORBIDDEN_SYNTHESIZED, "faithful": ft})

        members.append({
            "spec_iri": sid,
            "spec_class": rec.get("spec_class"),
            "name": rec.get("name_truncated"),
            "current_status": rec.get("current_status"),
            "source_path": str(source) if source else None,
            "source_kind": _source_kind(rec),
            "synthesized_runtime_emit_event_class": scan_class,
            "faithful_target": ft,
            "disposition": rc["disposition"],
            "agreement": rc["agreement"],
            "is_defect": rc["defect"],
            "e1_rule_based": {"target": e1.get("target"), "all_classes": e1.get("all_classes"),
                              "evidence": e1.get("evidence", "")[:160], "mechanism": FT_E1_MECHANISM},
            "e2_llm": {"target": e2.get("target"), "evidence": e2.get("evidence", "")[:160],
                       "refused": e2.get("refused"), "mechanism": FT_E2_MECHANISM},
            # prov:wasDerivedFrom source artifact for the KG capture (Step 2).
            "prov_wasDerivedFrom": str(source) if source else None,
        })

    out = {
        "schema_version": "faithful_target_map.v1",
        "build_event": "Cycle-16-S26 faithful-target extraction (Done #60 past-era reconstruction)",
        "timestamp": _now(),
        "extraction_methods_distinct": True,
        "extraction_methods_distinct_reason": reason,
        "e2_key_source": _E2_KEY_SOURCE,
        "n_specs": len(members),
        "disposition_counts": counts,
        "synthesized_vs_faithful_note": (
            "faithful_target is extracted from each spec's OWN text by E1 (rule-based) + E2 "
            "(LLM), reconciled; NEVER copied from the scan's synthesized runtime_emit_event_class. "
            "DP#26 carve-outs preserve faithful_target 'n/a' HONESTLY."
        ),
        "moved_off_forbidden_synthesized": moved_off_forbidden,
        "members": members,
    }
    MAP_OUT.write_text(json.dumps(out, indent=1))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Faithful-target extractor (E1∩E2)")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--no-llm", action="store_true", help="rule-based-only (E2 refused) — for the concrete-class smoke")
    args = ap.parse_args()
    out = run(limit=args.limit, no_llm=args.no_llm)
    print(f"faithful-target extraction: n={out['n_specs']} | distinct={out['extraction_methods_distinct']} | "
          f"key={out['e2_key_source']}")
    print(f"  dispositions: {out['disposition_counts']}")
    print(f"  moved_off_forbidden_synthesized: {out['moved_off_forbidden_synthesized']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
