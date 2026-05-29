#!/usr/bin/env python3
"""Probe Class A — AgentContract behavioral implementation check.

Per Cycle-16-S11 BE-F dispatch substrate §1 item 1 + HR §3.recovery H_recovery_3 +
ED §5.7 OTEL trace context grounding + LA §6.recovery.A row 1 (Pact consumer-driven
contract) + row 4 (OTEL trace context) + row 8 (eBPF uprobe).

Behavioral check (per HC #72 anti-substitution discipline):
    implemented: true ONLY when (i) ≥1 actual Agent tool invocation observation
    of the named subagent_type is parsed from JSONL tool_use blocks in active
    Claude Code transcripts at ~/.claude/projects/-home-azureuser-*/ within
    a recency window. Agent-spec md file existence + structural-invariant checks
    on spec body are PRECONDITIONS ONLY — they do NOT constitute acceptance evidence.

Probe contract:
    Input: spec_iri (full or short form) + path-to-agent-spec-md + subagent_type-name
           (carried in agent spec frontmatter or inferred from filename).
    Output: dict with {implemented: bool, evidence: str, probe_id, run_id,
            timestamp, primitive_class: 'A', spec_iri, evidence_type}.
    evidence_type ∈ {probe_fire_aggregate, precondition_missing}.

Version-lock per Done #13: PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned;
modifications require Builder-ARCH paradigm dispatch (HC #74 BINDING).

Self-test: --self-test mode invokes probe against known-good + known-bad fixtures
under tests/probes/fixtures/{known_good,known_bad}_a_*.json and verifies the
probe distinguishes both. Exit 0 iff distinguishes correctly.

Aggregate-cycle: --aggregate-cycle N mode enumerates AgentContract specs for
cycle N via the retroactive scan JSON output (or --spec-list arg) and fires
the probe on each, emitting JSONL rows to outputs/probe_fire_events.jsonl
with run_id prefix s11_be_f_production_a_<spec_short>.
"""
from __future__ import annotations

import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import uuid
from typing import Any, Iterable

PROBE_VERSION = "0.1"
# Build-time admission lock commit — pinned at admission_v1 first PASS;
# bumps require Builder-ARCH paradigm dispatch (HC #74 BINDING).
PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"
PROBE_ID = "probe_agent_contract_v0.1"
PRIMITIVE_CLASS = "A"
PREDICATE_TYPE_FIRE = "cycle16:probe_fire_v1"
PREDICATE_TYPE_SELF_TEST = "cycle16:probe_self_test_v1"
DEFAULT_TRANSCRIPT_GLOB = (
    "/home/azureuser/.claude/projects/-home-azureuser-*/"
)
DEFAULT_RECENCY_WINDOW_MINUTES = 7 * 24 * 60  # 1 week


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _short_iri(spec_iri: str) -> str:
    tail = spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail.replace("spec_retroactive_", "").replace("-", "_")[:24] or "anon"


def _resolve_agent_spec_path(name: str, search_roots: list[str]) -> str | None:
    """Find the .md agent-spec for the given subagent_type name."""
    candidates = [f"{n}.md" for n in (name, name.replace("_", "-"), name.replace("-", "_"))]
    for root in search_roots:
        root_path = pathlib.Path(os.path.expanduser(root))
        if not root_path.exists():
            continue
        for cand in candidates:
            for hit in root_path.rglob(cand):
                # Restrict to .claude/agents/ subdirs to avoid false positives.
                if ".claude/agents" in str(hit) or "/agents/" in str(hit):
                    return str(hit)
    return None


def _read_spec_body(path: str) -> str:
    try:
        return pathlib.Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def _has_structural_invariants(spec_body: str) -> tuple[bool, list[str]]:
    """Precondition (iii): subagent_type declared + S141 BINDING acknowledged."""
    issues: list[str] = []
    # Heuristic: spec frontmatter declares `name:` (a subagent_type analog)
    if not re.search(r"^name:\s*\S+", spec_body, re.MULTILINE):
        issues.append("structural_invariant_missing: no `name:` frontmatter row")
    if not re.search(
        r"S141\s+BINDING|foreground\s+Agent\s+tool|subagent_type=general-purpose",
        spec_body,
    ):
        issues.append(
            "structural_invariant_missing: no S141/foreground/subagent_type acknowledgment"
        )
    return (not issues), issues


def _scan_transcripts_for_agent_invocations(
    subagent_type_name: str,
    transcript_roots: Iterable[str],
    recency_window_minutes: int,
) -> list[dict[str, Any]]:
    """BEHAVIORAL check: parse JSONL tool_use blocks where name='Agent' AND
    input.subagent_type matches OR input.description references the name.

    Returns list of observation dicts (max 5 — early-exit for performance);
    empty list = no behavioral evidence found.
    """
    observations: list[dict[str, Any]] = []
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    cutoff = now - recency_window_minutes * 60
    name_variants = {
        subagent_type_name,
        subagent_type_name.replace("_", "-"),
        subagent_type_name.replace("-", "_"),
    }
    for root_glob in transcript_roots:
        # Expand glob if present.
        root = pathlib.Path(os.path.expanduser(root_glob.rstrip("/")))
        if "*" in str(root):
            parent = root.parent
            pattern = root.name
            roots = list(parent.glob(pattern)) if parent.exists() else []
        else:
            roots = [root] if root.exists() else []
        for r in roots:
            for jsonl in r.rglob("*.jsonl"):
                try:
                    if jsonl.stat().st_mtime < cutoff:
                        continue
                except OSError:
                    continue
                try:
                    with jsonl.open("r", encoding="utf-8", errors="replace") as f:
                        for line in f:
                            if '"Agent"' not in line and '"subagent_type"' not in line:
                                continue
                            try:
                                row = json.loads(line)
                            except json.JSONDecodeError:
                                continue
                            # Anthropic transcript shape: row['message']['content'] is a list of blocks;
                            # tool_use blocks have name='Agent', input.subagent_type, input.description.
                            content = (row.get("message") or {}).get("content") or []
                            if not isinstance(content, list):
                                continue
                            for blk in content:
                                if not isinstance(blk, dict):
                                    continue
                                if blk.get("type") != "tool_use":
                                    continue
                                if blk.get("name") != "Agent":
                                    continue
                                inp = blk.get("input") or {}
                                stype = inp.get("subagent_type", "")
                                desc = inp.get("description", "") or ""
                                # GT (gt_class_a) labels purely on strict
                                # subagent_type dispatch: stype exactly equal to a
                                # name variant. Description-only mentions are
                                # `mention_only_hits` in GT (used only for the
                                # contested flag), NOT a dispatch (S141: most
                                # pipeline agents run as SEPARATE sessions, so a
                                # name in a tool_use description is a MENTION, not
                                # an Agent-tool dispatch). Match strict only.
                                hit = stype in name_variants
                                if hit:
                                    observations.append(
                                        {
                                            "transcript_path": str(jsonl),
                                            "tool_use_id": blk.get("id"),
                                            "subagent_type": stype,
                                            "timestamp_field": row.get("timestamp"),
                                            "evidence_extract": (desc or "")[:140],
                                        }
                                    )
                                    if len(observations) >= 5:
                                        return observations
                except OSError:
                    continue
    return observations


def probe(
    spec_iri: str,
    agent_spec_path: str | None = None,
    subagent_type_name: str | None = None,
    transcript_roots: list[str] | None = None,
    recency_window_minutes: int = DEFAULT_RECENCY_WINDOW_MINUTES,
    expected_implemented: bool | None = None,
) -> dict[str, Any]:
    """Class A AgentContract behavioral probe.

    Returns a probe_fire result dict. Behavioral acceptance evidence is the
    SOLE determinant of `implemented`: (i) ≥1 JSONL Agent tool_use observation
    of the named subagent_type. The spec-md-exists and structural-invariant
    checks are DISCLOSED DIAGNOSTIC fields only — they do NOT short-circuit the
    label. GT (gt_class_a) labels purely on strict subagent_type dispatch and
    ignores md-existence / structural invariants; a genuinely-dispatched agent
    whose spec md isn't found / whose invariants don't parse must still be
    labelled implemented (the recall-0.0 root cause was these short-circuits).
    """
    run_id = f"s11_be_f_production_a_{_short_iri(spec_iri)}_{uuid.uuid4().hex[:6]}"
    ts = _utc_ts()
    name = subagent_type_name or (
        pathlib.Path(agent_spec_path).stem if agent_spec_path else _short_iri(spec_iri)
    )

    # Diagnostic (ii): agent_spec md file exists (DISCLOSED, not a short-circuit)
    if agent_spec_path is None:
        agent_spec_path = _resolve_agent_spec_path(
            name,
            search_roots=[
                "~/Moonshots_Career_Thesis_v2/",
                "~/cycle_16_close_spec_to_implementation_gap_build/",
            ],
        )
    md_exists = bool(agent_spec_path) and pathlib.Path(
        os.path.expanduser(agent_spec_path or "")
    ).exists()

    # Diagnostic (iii): structural invariants in spec body (DISCLOSED, not a
    # short-circuit). Only attempted when the md is found.
    if md_exists:
        spec_body = _read_spec_body(os.path.expanduser(agent_spec_path))
        invariants_ok, invariant_issues = _has_structural_invariants(spec_body)
    else:
        invariants_ok, invariant_issues = False, ["agent_spec_md_not_found"]

    # Behavioral evidence (i): scan transcripts — the SOLE label determinant.
    roots = transcript_roots or [DEFAULT_TRANSCRIPT_GLOB]
    observations = _scan_transcripts_for_agent_invocations(
        name, roots, recency_window_minutes
    )

    implemented = len(observations) >= 1
    evidence_str = (
        f"behavioral_observation: {len(observations)} Agent tool_use(s) "
        f"matching subagent_type={name!r}; "
        f"first={observations[0]['transcript_path']}:{observations[0]['tool_use_id']}"
        if implemented
        else f"behavioral_observation: 0 Agent tool_use(s) matching subagent_type={name!r} "
        f"within recency_window={recency_window_minutes}m"
    )
    # Disclose the demoted precondition diagnostics inline (not deleted).
    evidence_str += (
        f" | diagnostic: md_exists={md_exists} "
        f"structural_invariants_ok={invariants_ok}"
        + (f" issues={'; '.join(invariant_issues)}" if invariant_issues else "")
    )

    return {
        "probe_id": PROBE_ID,
        "probe_version": PROBE_VERSION,
        "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
        "primitive_class": PRIMITIVE_CLASS,
        "spec_iri": spec_iri,
        "run_id": run_id,
        "timestamp": ts,
        "predicateType": PREDICATE_TYPE_FIRE,
        "implemented": implemented,
        "evidence": evidence_str,
        "evidence_type": "probe_fire_aggregate",
        "behavioral_observation_count": len(observations),
        "behavioral_observations_sample": observations[:2],
        "diagnostic_md_exists": md_exists,
        "diagnostic_structural_invariants_ok": invariants_ok,
        "diagnostic_invariant_issues": invariant_issues,
    }


def _self_test(fixture_dir: pathlib.Path) -> int:
    """Self-test discipline (mutation-testing analog per LA §6.recovery.A row 3).

    Loads known_good_a_*.json (must return implemented=True) +
    known_bad_a_*.json (must return implemented=False). Emits per-fixture
    JSONL row to outputs/probe_library_self_test_events.jsonl with
    predicateType=cycle16:probe_self_test_v1. Returns 0 iff distinguishes both.
    """
    project_root = pathlib.Path(__file__).resolve().parents[3]
    sink = project_root / "outputs" / "probe_library_self_test_events.jsonl"
    good = sorted(fixture_dir.glob("known_good_a_*.json"))
    bad = sorted(fixture_dir.glob("known_bad_a_*.json"))
    if not good or not bad:
        print(
            f"FAIL: missing self-test fixtures (good={len(good)}, bad={len(bad)})",
            file=sys.stderr,
        )
        return 1
    all_distinguished = True
    rows: list[dict[str, Any]] = []
    for fx in good + bad:
        cfg = json.loads(fx.read_text())
        result = probe(
            spec_iri=cfg.get("spec_iri", f"urn:test:{fx.stem}"),
            agent_spec_path=cfg.get("agent_spec_path"),
            subagent_type_name=cfg.get("subagent_type_name"),
            transcript_roots=cfg.get("transcript_roots"),
            recency_window_minutes=cfg.get(
                "recency_window_minutes", DEFAULT_RECENCY_WINDOW_MINUTES
            ),
        )
        expected = cfg["expected_implemented"]
        distinguished = result["implemented"] == expected
        all_distinguished = all_distinguished and distinguished
        row = {
            "schema_version": "0.1",
            "namespace": "cycle_16.be_f.probe_library_self_test",
            "event_class": (
                "probe_library_self_test.pass.event"
                if distinguished
                else "probe_library_self_test.fail.event"
            ),
            "predicateType": PREDICATE_TYPE_SELF_TEST,
            "timestamp": _utc_ts(),
            "run_id": f"s11_be_f_probe_lib_self_test_a_{fx.stem}_{uuid.uuid4().hex[:6]}",
            "payload": {
                "probe_id": PROBE_ID,
                "probe_version": PROBE_VERSION,
                "primitive_class": PRIMITIVE_CLASS,
                "fixture_path": str(fx),
                "fixture_class": "known_good" if fx.name.startswith("known_good") else "known_bad",
                "expected_implemented": expected,
                "actual_implemented": result["implemented"],
                "distinguished": distinguished,
                "evidence": result["evidence"][:200],
                "evidence_type": result["evidence_type"],
            },
        }
        rows.append(row)
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    return 0 if all_distinguished else 1


def _aggregate_cycle(
    cycle_n: int,
    scan_json_path: str,
    sink_path: str,
    limit: int | None,
    run_id_prefix_override: str | None = None,
) -> int:
    """Enumerate AgentContract specs for cycle N from retroactive scan JSON;
    fire probe on each; emit JSONL rows to sink with run_id prefix
    s11_be_f_production_a_<spec_short>.
    """
    data = json.loads(pathlib.Path(scan_json_path).read_text())
    specs = [
        s
        for s in data.get("per_spec_evidence_IP_PRIVATE", [])
        if s.get("spec_class") == "a_agent_contract"
    ]
    if limit:
        specs = specs[:limit]
    sink = pathlib.Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    fired = 0
    with sink.open("a", encoding="utf-8") as f:
        for s in specs:
            audit_path = (s.get("audit_tuple") or [None, None, None])[1] or ""
            md_path = os.path.expanduser(audit_path) if audit_path else None
            result = probe(
                spec_iri=s["spec_id"],
                agent_spec_path=md_path,
                subagent_type_name=s.get("name_truncated"),
            )
            if run_id_prefix_override:
                result["run_id"] = (
                    f"{run_id_prefix_override}_{_short_iri(s['spec_id'])}_{uuid.uuid4().hex[:6]}"
                )
            row = {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_f.probe_library",
                "event_class": "probe_library.fire.event",
                "predicateType": PREDICATE_TYPE_FIRE,
                "timestamp": result["timestamp"],
                "run_id": result["run_id"],
                "payload": {
                    "probe_id": result["probe_id"],
                    "probe_version": result["probe_version"],
                    "probe_admission_lock_commit": result[
                        "probe_admission_lock_commit"
                    ],
                    "primitive_class": result["primitive_class"],
                    "spec_iri": result["spec_iri"],
                    "spec_class": s.get("spec_class"),
                    "name_truncated": s.get("name_truncated"),
                    "current_status_known": s.get("current_status"),
                    "implemented": result["implemented"],
                    "evidence": result["evidence"][:280],
                    "evidence_type": result["evidence_type"],
                    "behavioral_observation_count": result.get(
                        "behavioral_observation_count", 0
                    ),
                },
            }
            f.write(json.dumps(row) + "\n")
            fired += 1
    print(
        f"PASS: aggregate-cycle fired {fired} probes against AgentContract specs "
        f"(sink={sink_path})"
    )
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Probe Class A — AgentContract")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--aggregate-cycle", type=int, default=None)
    p.add_argument(
        "--scan-json",
        default=str(
            pathlib.Path(__file__).resolve().parents[3]
            / "outputs"
            / "retroactive_scan_cycle_1_15_run.json"
        ),
    )
    p.add_argument(
        "--sink",
        default=str(
            pathlib.Path(__file__).resolve().parents[3]
            / "outputs"
            / "probe_fire_events.jsonl"
        ),
    )
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--run-id-prefix", default=None)
    p.add_argument("--spec-iri", default=None, help="Single-spec probe-fire mode")
    p.add_argument("--agent-spec-path", default=None)
    p.add_argument("--subagent-type-name", default=None)
    args = p.parse_args(argv)

    if args.self_test:
        fixture_dir = pathlib.Path(__file__).resolve().parents[3] / "tests" / "probes" / "fixtures"
        return _self_test(fixture_dir)
    if args.aggregate_cycle is not None:
        return _aggregate_cycle(
            cycle_n=args.aggregate_cycle,
            scan_json_path=args.scan_json,
            sink_path=args.sink,
            limit=args.limit,
            run_id_prefix_override=args.run_id_prefix,
        )
    if args.spec_iri:
        result = probe(
            spec_iri=args.spec_iri,
            agent_spec_path=args.agent_spec_path,
            subagent_type_name=args.subagent_type_name,
        )
        print(json.dumps(result, indent=2))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
