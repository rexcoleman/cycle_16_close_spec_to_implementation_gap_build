#!/usr/bin/env python3
"""Independent verifier of the FAITHFUL re-derivation — Cycle-16-S26 Build-Runner Step 4
(anti-recursive-failure constraint #34/#27).

The re-derived gap list (outputs/trusted_detector_run_faithful.json) MUST be verified by
an instrument INDEPENDENT of the extraction that produced it: a DIFFERENT code path, a
DIFFERENT reader, reading the spec acceptance text DIRECTLY, with:
  - NO import of faithful_target_extractor (the producer of the faithful targets), and
  - NO import of probe_spec_impl_fidelity (the F-probe).
(independent_emit_contract_verifier.py is the precedent for "independent" = different
path / reader / source-of-truth.)

WHAT THIS VERIFIES (independently, for each execution-tier spec whose target the faithful
re-derivation MOVED, plus the worked case af3a918a):
  1. The faithful target in the re-derived gap list is ACTUALLY NAMED in the spec's own
     acceptance/Role text (re-parsed HERE, with a hand-rolled regex distinct from the
     extractor's) — i.e. the faithful target is text-grounded, not synthesized.
  2. The synthesized target the gap list moved OFF is NOT a fabrication we re-introduced:
     for af3a918a, assert `kernel_coach.dispatch` is NOT in the spec text.
  3. The implemented/not-implemented verdict is INDEPENDENTLY corroborated by reading the
     emission sink DIRECTLY (does the faithful class actually appear emitted?) — a direct
     JSONL read, NOT the F-probe's _event_class_matches.

Exit 0 (all corroborated) / 1 (any divergence). No human step. Refuse-on-missing-
precondition: absent spec/sink/gap-list -> FAIL with reason, never a fabricated PASS.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = REPO / "outputs"

FAITHFUL_RUN = OUTPUTS / "trusted_detector_run_faithful.json"
MAP_JSON = OUTPUTS / "faithful_target_map.json"
SCAN_JSON = OUTPUTS / "retroactive_scan_cycle_1_15_run.json"

# Independent event-class regex (DELIBERATELY a different pattern than the extractor's
# _EVENT_CLASS_RE: this one requires a backtick-bounded class with >=2 dotted segments
# AND a known verb segment, parsed from the WHOLE doc — a different reading procedure).
_VERB_SEGMENTS = ("start", "end", "fire", "dispatch", "transition", "warmup",
                  "drift", "signal", "complete", "received", "phase", "handoff",
                  "build", "session")
_INDEP_CLASS_RE = re.compile(r"`([a-z][a-z0-9_]*(?:\.[a-z0-9_]+){1,4})`")


def _spec_named_classes(source_path: str) -> set[str]:
    """Independently re-parse the spec's OWN text for every backtick dotted class whose
    LAST segment is a known event verb. Different procedure from the extractor."""
    p = Path(os.path.expanduser(source_path))
    if not p.exists():
        raise FileNotFoundError(f"spec source absent: {source_path}")
    text = p.read_text(encoding="utf-8", errors="replace")
    out = set()
    for m in _INDEP_CLASS_RE.finditer(text):
        cls = m.group(1)
        if cls.split(".")[-1] in _VERB_SEGMENTS:
            out.add(cls)
    return out


def _sink_emitted_classes() -> set[str]:
    """Direct read of every event_class present in any outputs/*.jsonl emission sink.
    A plain JSONL scan — NOT the F-probe's suffix-matcher."""
    classes = set()
    for f in sorted((REPO / "outputs").glob("*.jsonl")):
        try:
            for line in f.open(encoding="utf-8", errors="replace"):
                line = line.strip()
                if not line:
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                ec = rec.get("event_class")
                if ec:
                    classes.add(ec)
        except OSError:
            continue
    return classes


def _emitted_match(committed: str, emitted: set[str]) -> bool:
    """Independent emitted-class check (exact OR dotted-suffix), re-implemented HERE
    (not imported from the probe)."""
    if committed in emitted:
        return True
    for e in emitted:
        if e.endswith("." + committed) or committed.endswith("." + e):
            return True
    return False


def verify() -> dict:
    failures = []
    if not FAITHFUL_RUN.exists():
        return {"pass": False, "failures": ["precondition_refusal: trusted_detector_run_faithful.json absent"]}
    fai = json.loads(FAITHFUL_RUN.read_text())
    fmap = {m["spec_iri"]: m for m in json.loads(MAP_JSON.read_text())["members"]}
    scan = {}
    for p in json.loads(SCAN_JSON.read_text())["per_spec_evidence_IP_PRIVATE"]:
        scan.setdefault(p["spec_id"], p)
    fai_ps = {p["spec_iri"]: p for p in fai["per_spec_gap_list_IP_PRIVATE"]}
    emitted = _sink_emitted_classes()

    # The execution-tier specs whose target moved substantively + the worked case.
    targets = list(fai["faithful_overlay_replacements"].keys())
    if "cycle16:spec_retroactive_af3a918a" not in targets:
        targets.append("cycle16:spec_retroactive_af3a918a")

    checks = []
    for sid in targets:
        mem = fmap.get(sid)
        rec = scan.get(sid)
        gap = fai_ps.get(sid)
        if not (mem and rec and gap):
            failures.append(f"{sid}: missing map/scan/gap entry")
            continue
        src = mem.get("source_path") or (rec.get("audit_tuple") or [None, None])[1]
        try:
            named = _spec_named_classes(src)
        except FileNotFoundError as e:
            failures.append(f"{sid}: {e}")
            continue
        faithful = mem["faithful_target"]
        # CHECK 1: faithful target is named in the spec's OWN text (independent parse).
        ft_text_grounded = faithful in named or any(
            n.endswith("." + faithful) or faithful.endswith("." + n) for n in named)
        if not ft_text_grounded:
            failures.append(f"{sid}: faithful target {faithful!r} NOT independently found in spec text (named={sorted(named)})")
        # CHECK 2: the synthesized target moved OFF is NOT in the spec text (was a fabrication).
        synth = mem["synthesized_runtime_emit_event_class"]
        synth_in_text = synth in named
        # CHECK 3: independent emitted-class corroboration of the gap-list verdict.
        emit_present = _emitted_match(faithful, emitted)
        verdict_implemented = gap["implemented"]
        verdict_corroborated = (emit_present == verdict_implemented)
        if not verdict_corroborated:
            failures.append(
                f"{sid}: gap-list implemented={verdict_implemented} but independent sink read "
                f"emitted_present={emit_present} for faithful {faithful!r}")
        checks.append({
            "spec_iri": sid,
            "name": mem.get("name"),
            "synthesized_target": synth,
            "faithful_target": faithful,
            "faithful_text_grounded_independent": ft_text_grounded,
            "synthesized_in_spec_text": synth_in_text,
            "spec_named_classes_independent": sorted(named),
            "faithful_emitted_in_sink_independent": emit_present,
            "gap_list_implemented": verdict_implemented,
            "verdict_independently_corroborated": verdict_corroborated,
        })

    # Worked-case specific assertions (af3a918a).
    af = next((c for c in checks if c["spec_iri"] == "cycle16:spec_retroactive_af3a918a"), None)
    if af:
        if af["faithful_target"] != "kernel_coach.transition.fire":
            failures.append("af3a918a faithful target is not kernel_coach.transition.fire")
        if af["synthesized_in_spec_text"]:
            failures.append("af3a918a synthesized kernel_coach.dispatch UNEXPECTEDLY found in spec text")
        if not af["faithful_emitted_in_sink_independent"]:
            failures.append("af3a918a faithful class NOT independently found emitted in sink")
        if not af["gap_list_implemented"]:
            failures.append("af3a918a gap-list still not-implemented after faithful re-derivation")

    return {
        "verifier": "faithful_rederivation_independent_verifier",
        "independence": "different code path; reads spec acceptance text directly; "
                        "NO import of faithful_target_extractor, NO import of probe_spec_impl_fidelity",
        "imports_faithful_extractor": False,
        "imports_f_probe": False,
        "checks": checks,
        "failures": failures,
        "pass": len(failures) == 0,
    }


def main() -> int:
    argparse.ArgumentParser(description="Independent verifier of the faithful re-derivation").parse_args()
    v = verify()
    print(json.dumps(v, indent=2))
    if v["pass"]:
        print("PASS: faithful re-derivation independently corroborated "
              "(faithful targets text-grounded; verdicts match direct sink read)")
        return 0
    print(f"FAIL: {v['failures']}")
    return 1


# Hard guard: this module must NOT import the producer or the probe (assert at import-time).
assert "faithful_target_extractor" not in sys.modules or __name__ != "__main__", \
    "independence violation: faithful_target_extractor imported"

if __name__ == "__main__":
    raise SystemExit(main())
