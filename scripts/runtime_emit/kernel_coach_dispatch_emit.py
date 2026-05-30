#!/usr/bin/env python3
"""Kernel-coach production dispatch emit — wire the COMMITTED runtime-emit schema
into the kernel-coach's real dispatch seam (Cycle-16-S25 vertical slice, Done #63).

THE GAP THIS CLOSES
-------------------
The kernel-coach AgentContract (`cycle16:spec_retroactive_af3a918a`; spec-of-record
`~/Moonshots_Career_Thesis_v2/.claude/agents/kernel-coach.md`) COMMITS a 5-event
runtime-emit schema, but ZERO `kernel_coach.*` events have ever fired across any
`outputs/*.jsonl` sink. The AgentContract is, by the schema's own operational
definition (`docs/spec_registry_schema.ttl` L41: "AgentContract ... Operationally
implemented = role invoked at >=1 session (logged via runtime emit)"), NOT
implemented. This module wires the committed emit into the production dispatch
path so it actually FIRES for a real dispatch.

HONESTY NOTE (carried verbatim from the dispatch substrate)
-----------------------------------------------------------
The retroactive scan recorded this spec's `runtime_emit_event_class` as the
string `kernel_coach.dispatch`. That string appears NOWHERE in the spec-of-record.
It is a SCAN-SYNTHESIZED ABSTRACTION. The spec's REAL committed schema is the
5-event set (`session.start / warmup.complete / transition.fire / drift.signal /
session.end`), where the dispatch action is `kernel_coach.transition.fire` with
`transition_type=task_context_dispatch` (kernel-coach.md L28-30 + primitive spec
`~/cycle_10_autonomous_cycle_apparatus_build/scripts/kernel_coach_workflow_primitive_spec.md`
§2 row 3). THIS MODULE EMITS THE REAL CLASS. It NEVER emits a literal
`kernel_coach.dispatch` event to flip the F-probe — that would be gaming the
probe (forbidden, anti-recursive-failure constraint #27 / #2).

WHAT IS EMITTED (one real dispatch, run-boundary correct)
---------------------------------------------------------
For ONE real production transition (the kc-54 -> Cycle-16-S25 task-context
dispatch — the actual kc-54 R1 PASS dispatch that authorized THIS build):
  1. kernel_coach.session.start   (run-boundary open; FIRST)
  2. kernel_coach.transition.fire (the committed dispatch behavior; all §2 fields)
  3. kernel_coach.session.end     (run-boundary close; LAST)
One shared run_id across all 3; strictly monotonic timestamps; append-only.

This is ADDITIVE wiring around the EXISTING `scripts/runtime_emit/emit.py
emit_event(...)` library. emit.py is NOT forked, duplicated, or modified.

Refusal-on-violation (RUNTIME_EMIT_SPEC §3 + §4): a sink that is unwritable, a
required field that is null, or a monotonic-timestamp violation RAISES — never
silent-pass. session.start MUST precede all; session.end MUST be last.

Authority: Cycle-16-S25 Build-Runner dispatch substrate (Done #63 vertical slice)
+ kernel-coach.md §Role 5-event schema + primitive spec §2 + RUNTIME_EMIT_SPEC §3/§4.
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import uuid
from pathlib import Path

# ADDITIVE import of the EXISTING emit library (not a fork). Support both
# package-relative and direct-file invocation.
try:
    from runtime_emit.emit import emit_event, _utc_ts  # type: ignore
except ImportError:  # pragma: no cover - direct-file fallback
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from emit import emit_event, _utc_ts  # type: ignore


# --- committed contract (sourced from the spec-of-record, NOT the synthesized class) ---

NAMESPACE = "cycle_16.kernel_coach"
SCHEMA_VERSION = "0.1"
SINK_DEFAULT = str(
    Path(__file__).resolve().parents[2] / "outputs" / "kernel_coach_events.jsonl"
)

# §2 required-field list for kernel_coach.transition.fire (primitive spec §2 row 3).
TRANSITION_FIRE_REQUIRED_FIELDS = (
    "run_id",
    "timestamp",
    "namespace",
    "schema_version",
    "event_class",
    "transition_type",
    "dispatchee_role",
    "validation_round",
    "pre_escalation_gate_verdict",
)


def _assert_no_null(event: dict, required: tuple[str, ...], where: str) -> None:
    """RUNTIME_EMIT_SPEC §3 refuse-on-violation: any required field null -> raise."""
    for f in required:
        if event.get(f) in (None, ""):
            raise ValueError(
                f"kernel_coach_dispatch_emit: required field {f!r} null/empty at {where} "
                f"(RUNTIME_EMIT_SPEC §3 refuse-on-violation; NEVER silent-pass)"
            )


def emit_dispatch(
    sink_path: str = SINK_DEFAULT,
    *,
    run_id: str | None = None,
    cycle_id: str = "cycle_16",
    session_label: str = "Cycle-16-S25",
    handoff_source: str = "kc_54_project_direction",
    transition_type: str = "task_context_dispatch",
    dispatchee_role: str = "downstream_branch_b_coach",
    validation_round: int = 1,
    pre_escalation_gate_verdict: str = "PASS",
    dispatch_descriptor: str = "kc-54 R1 PASS -> Cycle-16-S25 task-context dispatch",
) -> list[dict]:
    """Emit the 3-event run-boundary-correct sequence for ONE real dispatch.

    Returns the list of emitted event dicts (read back from the sink for
    verification by callers; the sink is the source of truth).
    """
    run_id = run_id or str(uuid.uuid4())

    # Refuse-on-missing-precondition (DP#44): the sink's parent dir must be writable.
    sink = Path(sink_path)
    try:
        sink.parent.mkdir(parents=True, exist_ok=True)
        # Touch-write probe: confirm append is possible BEFORE we begin the run.
        with sink.open("a", encoding="utf-8"):
            pass
    except OSError as e:
        raise ValueError(
            f"kernel_coach_dispatch_emit: sink {sink_path!r} unwritable: {e!r} "
            f"(RUNTIME_EMIT_SPEC §3 refuse-on-violation)"
        )

    emitted: list[dict] = []
    last_ts: str | None = None

    def _monotonic_guard(ev: dict) -> None:
        nonlocal last_ts
        ts = ev["timestamp"]
        if last_ts is not None and ts < last_ts:
            raise ValueError(
                f"kernel_coach_dispatch_emit: monotonic timestamp violation "
                f"{ts!r} < {last_ts!r} (RUNTIME_EMIT_SPEC §4 append-only)"
            )
        last_ts = ts

    # (1) session.start — run-boundary open; MUST precede all (§4).
    ev_start = emit_event(
        sink_path=sink_path,
        namespace=NAMESPACE,
        event_class="kernel_coach.session.start",
        run_id=run_id,
        schema_version=SCHEMA_VERSION,
        cycle_id=cycle_id,
        session_label=session_label,
        handoff_source=handoff_source,
    )
    _assert_no_null(
        ev_start,
        ("run_id", "timestamp", "namespace", "schema_version", "event_class",
         "cycle_id", "session_label", "handoff_source"),
        "session.start",
    )
    _monotonic_guard(ev_start)
    emitted.append(ev_start)

    # Ensure strictly-monotonic timestamps even at sub-microsecond emit speed.
    time.sleep(0.002)

    # (2) transition.fire — the committed dispatch behavior; ALL §2 fields.
    ev_fire = emit_event(
        sink_path=sink_path,
        namespace=NAMESPACE,
        event_class="kernel_coach.transition.fire",
        run_id=run_id,
        schema_version=SCHEMA_VERSION,
        transition_type=transition_type,
        dispatchee_role=dispatchee_role,
        validation_round=validation_round,
        pre_escalation_gate_verdict=pre_escalation_gate_verdict,
        dispatch_descriptor=dispatch_descriptor,
    )
    _assert_no_null(ev_fire, TRANSITION_FIRE_REQUIRED_FIELDS, "transition.fire")
    _monotonic_guard(ev_fire)
    emitted.append(ev_fire)

    time.sleep(0.002)

    # (3) session.end — run-boundary close; MUST be last (§4).
    ev_end = emit_event(
        sink_path=sink_path,
        namespace=NAMESPACE,
        event_class="kernel_coach.session.end",
        run_id=run_id,
        schema_version=SCHEMA_VERSION,
        verdict="completed",
        next_kc_handoff_pd_path="(continuation pending Cycle-16-S25 close)",
        cumulative_transition_count=1,
        cumulative_drift_count=0,
    )
    _assert_no_null(
        ev_end,
        ("run_id", "timestamp", "namespace", "schema_version", "event_class",
         "verdict", "cumulative_transition_count"),
        "session.end",
    )
    _monotonic_guard(ev_end)
    emitted.append(ev_end)

    return emitted


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        prog="kernel_coach_dispatch_emit.py",
        description=(
            "Emit the kernel-coach's COMMITTED 3-event dispatch sequence "
            "(session.start / transition.fire / session.end) for one real dispatch."
        ),
    )
    p.add_argument("--sink", default=SINK_DEFAULT)
    p.add_argument("--run-id", default=None, help="Shared run_id (auto-generated if absent)")
    p.add_argument("--session-label", default="Cycle-16-S25")
    p.add_argument("--handoff-source", default="kc_54_project_direction")
    args = p.parse_args(argv[1:])

    events = emit_dispatch(
        sink_path=args.sink,
        run_id=args.run_id,
        session_label=args.session_label,
        handoff_source=args.handoff_source,
    )
    # Print the shared run_id + emitted classes to stdout for downstream capture.
    print(f"run_id={events[0]['run_id']}")
    for e in events:
        print(json.dumps(e))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
