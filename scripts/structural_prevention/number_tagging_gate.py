#!/usr/bin/env python3
"""Number-Tagging Gate (Cycle 16 BE-H / Done #15c).

At every Rex-facing surface (FINDINGS / close summaries / transition prompts /
handoffs), every PRIMARY number must carry one of the provenance tags:
    [measured]   — produced by a probe-fire / executed measurement
    [heuristic]  — estimate / proxy (citation density, ls+grep count, etc.)
    [anecdotal]  — single-instance observation

BLOCKING RULES:
  (1) Any primary number with NO tag -> FAIL (missing-tag).
  (2) Any [heuristic]-tagged number that appears inside a Done-criterion verdict
      line -> FAIL (a heuristic number must never stand as a Done verdict; the
      Cycle-9 substitution pattern was heuristic estimates booked as measured
      completion).

DP#44 refuse-on-missing-precondition: target file absent -> refuse (exit non-zero).

Sink: outputs/structural_prevention_number_tagging_events.jsonl

Usage:
  number_tagging_gate.py --project-dir DIR --target FILE \
      [--surface findings|close_summary|transition_prompt|handoff] [--run-id-prefix PFX]
  number_tagging_gate.py --self-test
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import sys
import uuid

TAG_RE = re.compile(r"\[(measured|heuristic|anecdotal)\]", re.I)
# A "primary number": an integer/decimal/percent token, optionally with a unit,
# that is NOT part of a tag, a citation marker [N], a date, a section ref (§N,
# L123), a commit hash, or a markdown list ordinal.
NUMBER_RE = re.compile(r"(?<![\w§Ll#.\-/])(\d+(?:\.\d+)?)\s*(%|x|×|specs?|fires?|sessions?)?\b")
DONE_VERDICT_RE = re.compile(r"\bdone\s*#?\d+\b.*\b(complete|confirmed|shipped|pass|done|closed)\b", re.I)
SKIP_LINE_RE = re.compile(r"^\s*(\||#{1,6}\s|>|```|\d+\.\s)")  # tables/headers handled per-token


def _utc() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _emit(sink: str, ec: str, run_id: str, payload: dict) -> None:
    os.makedirs(os.path.dirname(sink), exist_ok=True)
    ev = {"schema_version": "0.1",
          "namespace": "cycle_16.be_h.number_tagging_gate",
          "event_class": ec, "predicateType": "cycle16:number_tagging_v1",
          "timestamp": _utc(), "run_id": run_id, "payload": payload}
    with open(sink, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")


def _is_excluded(line: str, start: int, num: str) -> bool:
    """Exclude tokens that are not 'primary numbers' (dates, refs, hashes, list ords)."""
    pre = line[max(0, start - 2):start]
    if "§" in pre or pre.endswith("L") or pre.endswith("#"):
        return True
    if re.match(r"^\d{4}-\d{2}-\d{2}", line[start:start + 10]):  # ISO date
        return True
    # Inside a [..N..] citation/tag bracket
    bidx = line.rfind("[", 0, start)
    if bidx != -1 and "]" in line[start:start + 12] and not TAG_RE.search(line[bidx:start + 12]):
        return True
    return False


def scan_text(text: str) -> dict:
    untagged = []
    heuristic_in_verdict = []
    for ln, line in enumerate(text.splitlines(), 1):
        line_has_tag = TAG_RE.search(line)
        is_verdict = DONE_VERDICT_RE.search(line)
        for m in NUMBER_RE.finditer(line):
            num = m.group(1)
            if _is_excluded(line, m.start(1), num):
                continue
            # Primary number must carry a tag somewhere on its line.
            if not line_has_tag:
                untagged.append({"line": ln, "number": num, "context": line.strip()[:120]})
            else:
                tag = line_has_tag.group(1).lower()
                if tag == "heuristic" and is_verdict:
                    heuristic_in_verdict.append(
                        {"line": ln, "number": num, "context": line.strip()[:120]})
    ok = (not untagged) and (not heuristic_in_verdict)
    return {"verdict": "PASS" if ok else "FAIL",
            "untagged_numbers": untagged,
            "heuristic_in_verdict": heuristic_in_verdict}


def run_gate(project_dir, target, surface, run_id_prefix) -> int:
    sink = os.path.join(project_dir, "outputs",
                        "structural_prevention_number_tagging_events.jsonl")
    if not target or not os.path.exists(target):
        _emit(sink, "number_tagging_gate.refuse.event",
              f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
              {"surface": surface, "reason": "target_absent",
               "target": target, "refuse": True})
        print(f"REFUSE: target absent ({target})", file=sys.stderr)
        return 3
    with open(target) as f:
        res = scan_text(f.read())
    ec = ("number_tagging_gate.pass.event" if res["verdict"] == "PASS"
          else "number_tagging_gate.refuse.event")
    _emit(sink, ec, f"{run_id_prefix}_{uuid.uuid4().hex[:8]}",
          {"surface": surface, "target": target, **res,
           "refuse": res["verdict"] == "FAIL"})
    print(f"Number-Tagging [{surface}]: {res['verdict']} "
          f"(untagged={len(res['untagged_numbers'])}, "
          f"heuristic-in-verdict={len(res['heuristic_in_verdict'])})")
    return 0 if res["verdict"] == "PASS" else 1


def _self_test() -> int:
    """Fixture 1: untagged number -> FAIL. Fixture 2: heuristic-in-verdict -> FAIL.
    Fixture 3: properly tagged measured number -> PASS."""
    f1 = "We enumerated 232 specs across the cycle."          # untagged
    f2 = "Done #11 complete: 137 [heuristic] dormant specs."  # heuristic in verdict
    f3 = "We measured 20 [measured] implemented fires."       # tagged, not verdict
    r1, r2, r3 = scan_text(f1), scan_text(f2), scan_text(f3)
    ok = (r1["verdict"] == "FAIL" and len(r1["untagged_numbers"]) >= 1
          and r2["verdict"] == "FAIL" and len(r2["heuristic_in_verdict"]) >= 1
          and r3["verdict"] == "PASS")
    print(f"self-test: untagged-fail={r1['verdict']=='FAIL'} "
          f"heuristic-in-verdict-fail={r2['verdict']=='FAIL'} "
          f"tagged-measured-pass={r3['verdict']=='PASS'}")
    return 0 if ok else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Number-Tagging Gate (Done #15c)")
    ap.add_argument("--project-dir", default=".")
    ap.add_argument("--target", default=None)
    ap.add_argument("--surface", default="findings",
                    choices=["findings", "close_summary", "transition_prompt", "handoff"])
    ap.add_argument("--run-id-prefix", default="s13_be_h_production_number_tagging")
    ap.add_argument("--self-test", action="store_true")
    a = ap.parse_args(argv)
    if a.self_test:
        return _self_test()
    return run_gate(os.path.abspath(a.project_dir), a.target, a.surface, a.run_id_prefix)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
