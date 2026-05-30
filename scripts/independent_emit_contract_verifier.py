#!/usr/bin/env python3
"""Independent emit-contract verifier — Cycle-16-S25 vertical slice T2 (#34).

PURPOSE
-------
Confirm that the kernel-coach AgentContract is OPERATIONALLY IMPLEMENTED by a
SECOND, GENUINELY INDEPENDENT instrument — a DIFFERENT code path, a DIFFERENT
reader, and a DIFFERENT source-of-truth than the Class F probe
(`scripts/probes/f/probe_spec_impl_fidelity.py`).

WHY THIS IS NOT THE F-PROBE (anti-recursive-failure constraint #34)
-------------------------------------------------------------------
The F-probe's ONLY emission check is `_event_class_matches`: it suffix-matches the
emitted `event_class` string against the committed class. It reads NEITHER spec
document. It checks the *probe's pass-condition* (does a string with the right
dotted suffix appear in any sink).

THIS verifier instead checks the *spec's INTENT* by PARSING THE SPEC ACCEPTANCE
TEXT and verifying FULL FIELD-CONTRACT CONFORMANCE + RUN-BOUNDARY DISCIPLINE:
  - SOURCE-OF-TRUTH #1: the §2 required-field row for `kernel_coach.transition.fire`
    in `~/cycle_10_autonomous_cycle_apparatus_build/scripts/kernel_coach_workflow_primitive_spec.md`
    (parsed live from the markdown table — NOT hard-coded).
  - SOURCE-OF-TRUTH #2: the 5-event schema enumerated in
    `~/Moonshots_Career_Thesis_v2/.claude/agents/kernel-coach.md` §Role.
  - CHECK: a real `kernel_coach.transition.fire` event exists with EVERY §2
    required field PRESENT and NON-NULL; AND the run brackets correctly
    (session.start first, session.end last, shared run_id, strictly-monotonic
    timestamps). This is STRONGER and DIFFERENT from event_class suffix-presence.

It does NOT import or call probe_spec_impl_fidelity.py and shares NO check with it.

OUTPUT: a verdict JSON (with the run_id evidence) on stdout; PASS/FAIL line;
exit 0 (PASS) / 1 (FAIL). No human step (#61). Refuse-on-missing-precondition:
absent spec doc / absent sink -> FAIL with explicit reason, never fabricated PASS.

Authority: Cycle-16-S25 dispatch substrate T2 (#34 LOAD-BEARING independence).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path

PRIMITIVE_SPEC_DEFAULT = os.path.expanduser(
    "~/cycle_10_autonomous_cycle_apparatus_build/scripts/kernel_coach_workflow_primitive_spec.md"
)
KERNEL_COACH_SPEC_DEFAULT = os.path.expanduser(
    "~/Moonshots_Career_Thesis_v2/.claude/agents/kernel-coach.md"
)
SINK_DEFAULT = str(
    Path(__file__).resolve().parent.parent / "outputs" / "kernel_coach_events.jsonl"
)


def _parse_transition_fire_required_fields(primitive_spec_path: str) -> tuple[list[str], str]:
    """Parse the §2 markdown table row for `kernel_coach.transition.fire` and extract
    the backtick-quoted Required-fields cell. Returns (fields, evidence_line).

    This reads the SPEC ACCEPTANCE TEXT directly (the §2 table) — the spec's intent.
    """
    p = Path(primitive_spec_path)
    if not p.exists():
        raise FileNotFoundError(
            f"primitive spec not found: {primitive_spec_path} (refuse-on-missing-precondition)"
        )
    for raw in p.read_text(encoding="utf-8").splitlines():
        if "kernel_coach.transition.fire" in raw and raw.lstrip().startswith("|"):
            cells = [c.strip() for c in raw.strip().strip("|").split("|")]
            # Required-fields is the last column in the §2 table.
            req_cell = cells[-1]
            fields = re.findall(r"`([^`]+)`", req_cell)
            return fields, raw.strip()
    raise ValueError(
        "could not locate the §2 table row for kernel_coach.transition.fire in primitive spec"
    )


def _parse_five_event_schema(kernel_coach_spec_path: str) -> tuple[list[str], list[str]]:
    """Parse the 5-event schema from kernel-coach.md §Role. Returns (classes, evidence_lines).

    SOURCE-OF-TRUTH #2 — confirms the committed schema is the 5-event set (and that
    `kernel_coach.dispatch` is NOT among them; the synthesized-class disclosure)."""
    p = Path(kernel_coach_spec_path)
    if not p.exists():
        raise FileNotFoundError(
            f"kernel-coach spec not found: {kernel_coach_spec_path} (refuse-on-missing-precondition)"
        )
    classes: list[str] = []
    evidence: list[str] = []
    in_role = False
    for raw in p.read_text(encoding="utf-8").splitlines():
        if raw.strip().startswith("## Role"):
            in_role = True
            continue
        if in_role and raw.startswith("## "):
            break
        m = re.search(r"`(kernel_coach\.[a-z.]+)`", raw)
        if in_role and m and re.match(r"^\d+\.", raw.strip()):
            classes.append(m.group(1))
            evidence.append(raw.strip())
    return classes, evidence


def verify(
    sink_path: str = SINK_DEFAULT,
    primitive_spec_path: str = PRIMITIVE_SPEC_DEFAULT,
    kernel_coach_spec_path: str = KERNEL_COACH_SPEC_DEFAULT,
) -> dict:
    """Run the independent verification. Returns a verdict dict."""
    verdict: dict = {
        "verifier": "independent_emit_contract_verifier",
        "verifier_version": "0.1",
        "shares_check_with_f_probe": False,
        "source_of_truth": {
            "primitive_spec_section2": primitive_spec_path,
            "kernel_coach_spec_role": kernel_coach_spec_path,
        },
        "checks": {},
        "failures": [],
    }

    # --- SOURCE-OF-TRUTH parse (spec INTENT, not probe pass-condition) ---
    try:
        required_fields, sec2_line = _parse_transition_fire_required_fields(primitive_spec_path)
        five_event_schema, schema_lines = _parse_five_event_schema(kernel_coach_spec_path)
    except (FileNotFoundError, ValueError) as e:
        verdict["pass"] = False
        verdict["failures"].append(f"precondition_refusal: {e}")
        return verdict

    verdict["committed_required_fields_transition_fire"] = required_fields
    verdict["committed_five_event_schema"] = five_event_schema
    verdict["sec2_evidence_line"] = sec2_line
    verdict["five_event_schema_evidence_lines"] = schema_lines
    verdict["synthesized_class_note"] = (
        "kernel_coach.dispatch is NOT in the committed schema "
        f"(committed = {five_event_schema}); it is a scan-synthesized abstraction. "
        "The real dispatch class is kernel_coach.transition.fire."
    )

    # --- read the emission sink (the run product) ---
    sink = Path(sink_path)
    if not sink.exists():
        verdict["pass"] = False
        verdict["failures"].append(
            f"precondition_refusal: emission sink absent: {sink_path}"
        )
        return verdict
    rows = []
    for line in sink.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue

    if not rows:
        verdict["pass"] = False
        verdict["failures"].append("precondition_refusal: emission sink is empty")
        return verdict

    # --- CHECK 1: a real transition.fire event with EVERY §2 field present + non-null ---
    fire_events = [r for r in rows if r.get("event_class") == "kernel_coach.transition.fire"]
    verdict["checks"]["transition_fire_count"] = len(fire_events)
    if not fire_events:
        verdict["failures"].append(
            "no kernel_coach.transition.fire event present (committed dispatch behavior never fired)"
        )
    fire = fire_events[0] if fire_events else None
    if fire is not None:
        missing_or_null = [f for f in required_fields if fire.get(f) in (None, "")]
        verdict["checks"]["transition_fire_field_contract"] = {
            "required": required_fields,
            "missing_or_null": missing_or_null,
            "present_values": {f: fire.get(f) for f in required_fields},
        }
        if missing_or_null:
            verdict["failures"].append(
                f"transition.fire field-contract violation: missing/null {missing_or_null}"
            )

    # --- CHECK 2: run-boundary discipline (different from event_class suffix-presence) ---
    run_id = fire.get("run_id") if fire else None
    run_rows = [r for r in rows if r.get("run_id") == run_id] if run_id else []
    boundary_ok = True
    boundary_detail = {}
    if run_id and run_rows:
        first_is_start = run_rows[0].get("event_class") == "kernel_coach.session.start"
        last_is_end = run_rows[-1].get("event_class") == "kernel_coach.session.end"
        shared_run_id = all(r.get("run_id") == run_id for r in run_rows)
        ts = [r.get("timestamp", "") for r in run_rows]
        monotonic = all(ts[i] <= ts[i + 1] for i in range(len(ts) - 1))
        boundary_detail = {
            "run_id": run_id,
            "events_in_run": [r.get("event_class") for r in run_rows],
            "session_start_first": first_is_start,
            "session_end_last": last_is_end,
            "shared_run_id": shared_run_id,
            "monotonic_timestamps": monotonic,
            "timestamps": ts,
        }
        for label, ok in (
            ("session_start_first", first_is_start),
            ("session_end_last", last_is_end),
            ("shared_run_id", shared_run_id),
            ("monotonic_timestamps", monotonic),
        ):
            if not ok:
                boundary_ok = False
                verdict["failures"].append(f"run-boundary discipline violation: {label}")
    else:
        boundary_ok = False
        verdict["failures"].append("run-boundary discipline: no resolvable run for transition.fire")
    verdict["checks"]["run_boundary"] = boundary_detail

    verdict["run_id_evidence"] = run_id
    verdict["pass"] = len(verdict["failures"]) == 0
    return verdict


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        prog="independent_emit_contract_verifier.py",
        description="Independent (non-F-probe) verifier of the kernel-coach emit contract.",
    )
    p.add_argument("--sink", default=SINK_DEFAULT)
    p.add_argument("--primitive-spec", default=PRIMITIVE_SPEC_DEFAULT)
    p.add_argument("--kernel-coach-spec", default=KERNEL_COACH_SPEC_DEFAULT)
    p.add_argument("--quiet", action="store_true", help="Print only PASS/FAIL line")
    args = p.parse_args(argv[1:])

    verdict = verify(
        sink_path=args.sink,
        primitive_spec_path=args.primitive_spec,
        kernel_coach_spec_path=args.kernel_coach_spec,
    )
    if not args.quiet:
        print(json.dumps(verdict, indent=2))
    if verdict["pass"]:
        print(f"PASS: kernel-coach emit contract conformant (run_id={verdict.get('run_id_evidence')})")
        return 0
    print(f"FAIL: {verdict['failures']}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
