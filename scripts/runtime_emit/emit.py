#!/usr/bin/env python3
"""Runtime emit primitive — JSONL append-only event emitter for research-build projects.

Lifted+adapted from Cycle 10 BE#7 apparatus_dispatch_shim.py emit primitive
(`_emit_event()` + `_utc_ts()` + run_id UUID + namespace + schema_version).
Auto-installed by `init_project.sh --profile research-build` per Cycle-15-S7 govML
v2.8.2 wire-in (`install_runtime_emit_substrate()` function).

Roles supported (per Cycle 10 PRIMARY workflow primitive specs at
`~/cycle_10_autonomous_cycle_apparatus_build/scripts/`):

  * kernel-coach (5 baseline event classes per kernel_coach_workflow_primitive_spec.md §2:
    session.start / warmup.complete / transition.fire / drift.signal / session.end)
  * impl-coach (7 baseline event classes per implementation_coach_workflow_primitive_spec.md §2:
    session.start / warmup.complete / handoff.inbound / transition.fire / drift.signal /
    handoff.outbound / session.end)
  * build-runner (5 baseline event classes per Moonshots .claude/agents/build-runner.md
    runtime_emit_obligation §: session.start / dispatch.received / build.phase.start /
    build.phase.complete / session.end + 1 drift class build_runner_runtime_failure)

Drift telemetry: vendored copy of Cycle 10 BE#5 drift_telemetry_signal_schema.json
v0.1 (4-class baseline per ROADMAP §2.5; namespace-append extension hook per
Item 2 (a) BINDING) at `scripts/runtime_emit/drift_telemetry_signal_schema.json`.

HC-11 partition (PUBLISHABLE): emit interface + namespace + schema_version + sink-path
convention + role enumeration + JSONL append-only invariant.
HC-11 partition (PIPELINE-IP-PRIVATE): per-event content payload bodies + drift-detection
algorithm bodies + agent-internal state — NEVER inlined in this module.

Refusal-on-violation per Cycle 10 BE#5 RUNTIME_EMIT_SPEC §3 = halt-and-surface:
if the artifact cannot record the boundary it just crossed, it cannot proceed.

Usage as library:

    from runtime_emit.emit import emit_event
    emit_event(
        sink_path="outputs/kernel_coach_events.jsonl",
        namespace="<project>.kernel_coach",
        event_class="kernel_coach.session.start",
        run_id="<uuid>",
        cycle_id="<cycle_id>",
        session_label="<S-N>",
        handoff_source="prior_kc_pd",
    )

Usage as CLI smoke test:

    python3 emit.py --help
    python3 emit.py --sink outputs/build_runner_events.jsonl \\
                    --namespace cycle_15.build_runner \\
                    --event-class build_runner.session.start \\
                    --cycle-id cycle_15 --session-label S7

Authority: Cycle-15-S7 BE#4 Branch 2.2 runtime emit deployment + Rex Step 3.5
Option B disposition 2026-05-27 (Pattern 11 STANDING) + govML v2.8.2 wire-in.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


SCHEMA_VERSION_DEFAULT = "0.1"


# --- Cycle 16 BE-E forward-apply observation event class registration constants -------
#
# Added per Cycle-16-S7 BE-E dispatch substrate §1 item 1 (additive extension;
# emit.py core `emit_event()` signature UNCHANGED per Cycle 10 §0 schema_version=0.1
# LOCKED). Two NEW event classes wired into the existing emit primitive — call sites
# pass these constants as `event_class` argument; no API break.
#
# Namespace: `cycle_16.be_e.forward_apply_observation` (per-pipeline + per-cycle
# + per-BE scope; namespace-isolated from BE-A/B/C/D namespaces per Cycle 10
# rule_6/8/10/12 invariants). Sink: `outputs/forward_apply_observation_events.jsonl`
# (NEW; empty at scaffold; refuse-on-violation per RUNTIME_EMIT_SPEC §3 if absent).
#
# Authority: Cycle-16-S7 BE-E dispatch substrate + Rex disposition (C) D-S2-1 +
# kc-46 R1 PASS task-context dispatch authorization 2026-05-27.
SPEC_AUTHORING_EVENT_CLASS = "spec_authoring_event"
SPEC_IMPLEMENTATION_EVENT_CLASS = "spec_implementation_event"

# Cycle 16 BE-E sink-routing convention (publishable per HC-11 partition;
# per-host enforcement routing internals are IP-private per forward_apply_observation_protocol.md §6)
FORWARD_APPLY_OBSERVATION_NAMESPACE = "cycle_16.be_e.forward_apply_observation"
FORWARD_APPLY_OBSERVATION_SINK_DEFAULT = "outputs/forward_apply_observation_events.jsonl"


def forward_apply_emit(
    sink_path: str = FORWARD_APPLY_OBSERVATION_SINK_DEFAULT,
    event_class: str = SPEC_AUTHORING_EVENT_CLASS,
    **extra_fields,
) -> dict:
    """Cycle 16 BE-E sink-routing helper for forward-apply observation events.

    Convenience wrapper around `emit_event()` with BE-E namespace + sink defaults
    bound. Accepts either `SPEC_AUTHORING_EVENT_CLASS` or `SPEC_IMPLEMENTATION_EVENT_CLASS`
    (validated; refuses other strings per refuse-on-missing-precondition discipline).
    Required payload fields per forward_apply_observation_protocol.md §1 are
    caller-provided via `**extra_fields` merged into the event payload.

    Refusal-on-violation: per RUNTIME_EMIT_SPEC §3 + BE-E §5, if event_class is
    not in the 2 BE-E classes, raise ValueError (halt-and-surface). Do NOT
    swallow the failure — orphan event class fires are evidence of write-boundary
    bypass per HC-BE-D-1 (Cycle 18 scope).
    """
    if event_class not in (SPEC_AUTHORING_EVENT_CLASS, SPEC_IMPLEMENTATION_EVENT_CLASS):
        raise ValueError(
            f"forward_apply_emit: event_class must be one of "
            f"{{{SPEC_AUTHORING_EVENT_CLASS!r}, {SPEC_IMPLEMENTATION_EVENT_CLASS!r}}}, "
            f"got {event_class!r} (refuse-on-missing-precondition per RUNTIME_EMIT_SPEC §3 + BE-E §5)"
        )
    return emit_event(
        sink_path=sink_path,
        namespace=FORWARD_APPLY_OBSERVATION_NAMESPACE,
        event_class=event_class,
        **extra_fields,
    )


def _utc_ts() -> str:
    """ISO 8601 UTC timestamp with microseconds (per Cycle 10 RUNTIME_EMIT_SPEC §4 row 2)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def emit_event(
    sink_path: str,
    namespace: str,
    event_class: str,
    run_id: Optional[str] = None,
    schema_version: str = SCHEMA_VERSION_DEFAULT,
    **extra_fields,
) -> dict:
    """Append a single event to JSONL sink_path.

    Required fields per Cycle 10 BE#5 RUNTIME_EMIT_SPEC §1:
        run_id, timestamp, namespace, schema_version, event_class.

    Auto-fills run_id if not provided; auto-fills timestamp at write time.
    Extra fields are merged into the event dict (per-event optional fields
    declared in role-specific schemas at agent specs).

    Returns the emitted event dict (for in-process verification / chaining).

    Refusal-on-violation: per RUNTIME_EMIT_SPEC §3, if sink_path is unwritable
    OR required field is null, raise an exception (halt-and-surface). Do NOT
    swallow the failure — silent emit-absent failures are exactly the Pattern G
    failure shape this primitive prevents.
    """
    if run_id is None:
        run_id = str(uuid.uuid4())
    if not namespace:
        raise ValueError("emit_event: namespace required (publishable per HC-11 partition)")
    if not event_class:
        raise ValueError("emit_event: event_class required (per RUNTIME_EMIT_SPEC §1)")

    event = {
        "run_id": run_id,
        "timestamp": _utc_ts(),
        "namespace": namespace,
        "schema_version": schema_version,
        "event_class": event_class,
    }
    # Merge extra fields without overwriting required fields
    for k, v in extra_fields.items():
        if k not in event:
            event[k] = v

    sink = Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(event) + "\n")
    return event


def main(argv: list[str]) -> int:
    """CLI smoke-test entry point.

    Usage:
        python3 emit.py --help
        python3 emit.py --sink <path> --namespace <ns> --event-class <cls> [--run-id <uuid>] [...]
    """
    parser = argparse.ArgumentParser(
        prog="emit.py",
        description=(
            "Runtime emit primitive for research-build projects (Cycle 10 PRIMARY adapter). "
            "Appends a single JSONL event to sink. Refusal-on-violation per RUNTIME_EMIT_SPEC §3."
        ),
    )
    parser.add_argument("--sink", required=True, help="JSONL sink path (e.g., outputs/kernel_coach_events.jsonl)")
    parser.add_argument("--namespace", required=True, help="Event namespace (e.g., cycle_15.kernel_coach)")
    parser.add_argument("--event-class", required=True, help="Event class (e.g., kernel_coach.session.start)")
    parser.add_argument("--run-id", default=None, help="UUID (auto-generated if absent)")
    parser.add_argument("--schema-version", default=SCHEMA_VERSION_DEFAULT, help=f"Schema version (default {SCHEMA_VERSION_DEFAULT})")
    parser.add_argument("--cycle-id", default=None, help="Optional cycle_id (e.g., cycle_15)")
    parser.add_argument("--session-label", default=None, help="Optional session_label (e.g., S7)")
    parser.add_argument("--verdict", default=None, help="Optional verdict field for end-class events")
    parser.add_argument("--drift-class", default=None, help="Optional drift_class field for drift.signal events")
    parser.add_argument("--severity", default=None, help="Optional severity (INFO|WARN|HALT) for drift events")

    args = parser.parse_args(argv[1:])

    extras = {}
    for f in ("cycle_id", "session_label", "verdict", "drift_class", "severity"):
        v = getattr(args, f.replace("-", "_"), None)
        if v is not None:
            extras[f] = v

    event = emit_event(
        sink_path=args.sink,
        namespace=args.namespace,
        event_class=args.event_class,
        run_id=args.run_id,
        schema_version=args.schema_version,
        **extras,
    )
    print(json.dumps(event), file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
