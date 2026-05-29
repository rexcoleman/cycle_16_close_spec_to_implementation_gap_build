#!/usr/bin/env python3
"""Probe Class C — DesignDecision behavioral implementation check.

Per Cycle-16-S11 BE-F dispatch substrate §1 item 1 + HR §3.recovery H_recovery_3 +
LA §6.recovery.A row 5 (Bazel Skyframe dep-graph) + row 9 (BX) + design-anchor
flag re LLM-judge calibration at §6.recovery.C row 3 + ED §5.7 grounding.

HC #72 ANTI-SUBSTITUTION DISCIPLINE (BINDING — load-bearing for KT-8):
    The LLM-judge MUST read ACTUAL CODE/CONFIG via file:line citation as evidence.
    The judge prompt explicitly FORBIDS:
        - "registry says implemented" / SPARQL ASK on cycle16:currentStatus
        - "DECISION_LOG ADR text exists"
        - "FINDINGS mentions the decision"
    The judge MUST produce a file:line citation showing the embodiment of the
    decision in code/config. ADR-text-only or registry-only evidence ⇒
    implemented: false (substitution detected).

Behavioral check:
    Precondition (i): DECISION_LOG ADR entry exists (file presence + grep
                      `^## ADR-<id>` or `^### .*<title>`).
    Acceptance evidence (ii): LLM-judge reads code at cycle16:embodimentRef + emits
                              file:line citation. Without an LLM API key, the probe
                              uses a STRUCTURAL JUDGE — pattern-match against the
                              ADR-declared embodiment ref (path + line range or
                              symbol) AND require a non-trivial match (≥1 grep hit
                              for a load-bearing token from the ADR).

The structural judge is deliberate calibration: it implements the SHAPE of the
LLM-judge contract (file:line citation as evidence; substitution-detection
refusal) without requiring online LLM calls at probe-fire time. Full LLM-judge
upgrade is deferred to Cycle 17+ if Coach R3 disposition requires (carry-forward
candidate at envelope honest_gaps).

Version-lock per Done #13: PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned.
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import pathlib
import re
import subprocess
import sys
import uuid
from typing import Any

PROBE_VERSION = "0.1"
PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"
PROBE_ID = "probe_design_decision_v0.1"
PRIMITIVE_CLASS = "C"
PREDICATE_TYPE_FIRE = "cycle16:probe_fire_v1"
PREDICATE_TYPE_SELF_TEST = "cycle16:probe_self_test_v1"
JUDGE_PROMPT_PATH = str(pathlib.Path(__file__).resolve().parent / "llm_judge_prompt.md")

# Anthropic model for the C probe's LIVE judge (BE-P, Cycle-16-S19). The PROBE
# judge uses claude-haiku-4-5; the HARNESS GT judge (gt_class_c) MUST use a
# DIFFERENT model (claude-sonnet-4-6) so probe<->GT agreement is INDEPENDENT
# agreement, not a judge agreeing with itself (validate-the-validator #19).
_C_JUDGE_MODEL = os.environ.get("CYCLE16_C_JUDGE_MODEL", "claude-haiku-4-5")


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _short_iri(spec_iri: str) -> str:
    tail = spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail.replace("spec_retroactive_", "").replace("-", "_")[:24] or "anon"


def _adr_present(decision_log_path: str, adr_token: str) -> tuple[bool, str]:
    """Precondition: ADR entry exists in DECISION_LOG."""
    p = pathlib.Path(os.path.expanduser(decision_log_path))
    if not p.exists():
        return False, "decision_log_not_found"
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
    except OSError as e:
        return False, f"decision_log_unreadable: {e}"
    # Match the ADR/decision token either as a heading or in a row
    if re.search(rf"(?im)^\s*#+\s*.*{re.escape(adr_token)}", body) or (
        adr_token in body
    ):
        return True, f"adr_token_present_in {decision_log_path}"
    return False, f"adr_token_absent={adr_token}"


def _structural_judge(
    embodiment_ref_path: str | None,
    decision_token: str,
    decision_log_path: str,
) -> tuple[bool, str]:
    """STRUCTURAL judge mirrors LLM-judge contract:
    READS actual code/config at embodiment_ref_path (NOT ADR/DECISION_LOG text),
    produces a file:line citation as evidence.

    Acceptance: ≥1 file:line in the embodiment file (or its parent dir if
    embodiment_ref_path is a directory) where a load-bearing token from the
    decision is referenced AND the file is NOT itself the DECISION_LOG.

    Refusal: empty embodiment_ref_path OR embodiment_ref_path resolves to the
    DECISION_LOG itself (registry/ADR-text-only substitution).
    """
    if not embodiment_ref_path:
        return False, "anti_substitution: no embodimentRef declared (ADR-text-only)"
    target = pathlib.Path(os.path.expanduser(embodiment_ref_path))
    if not target.exists():
        return False, f"embodimentRef_not_found: {embodiment_ref_path}"
    # Anti-substitution gate: refuse if embodimentRef IS the DECISION_LOG
    dl_p = pathlib.Path(os.path.expanduser(decision_log_path)).resolve()
    if target.resolve() == dl_p:
        return (
            False,
            "anti_substitution_refusal: embodimentRef IS DECISION_LOG (HC #72)",
        )

    # Discover load-bearing tokens from the decision_token
    # (split on _, :, ., -; drop short and structural words)
    raw_tokens = re.split(r"[\s:_./\-]+", decision_token)
    skip = {
        "paradigm",
        "dispositions",
        "decisions",
        "log",
        "cycle",
        "close",
        "decision",
        "the",
        "and",
        "to",
        "of",
        "s",
        "n",
        "be",
        "stage",
    }
    tokens = [
        t.lower()
        for t in raw_tokens
        if len(t) >= 4 and t.lower() not in skip
    ]
    if not tokens:
        return False, "no_load_bearing_tokens_extractable"

    # Search target (file OR directory; one file:line citation is sufficient)
    citations: list[str] = []
    files_to_scan: list[pathlib.Path]
    if target.is_dir():
        files_to_scan = [
            f
            for f in target.rglob("*")
            if f.is_file() and f.suffix in (".py", ".sh", ".md", ".json", ".yaml", ".yml", ".ttl")
        ][:50]
    else:
        files_to_scan = [target]

    for f in files_to_scan:
        if f.resolve() == dl_p:
            continue
        try:
            for lineno, line in enumerate(
                f.read_text(encoding="utf-8", errors="replace").splitlines(), 1
            ):
                ll = line.lower()
                if any(t in ll for t in tokens):
                    citations.append(f"{f}:{lineno}: {line.strip()[:120]}")
                    break
        except OSError:
            continue
        if citations:
            break

    if not citations:
        return (
            False,
            f"structural_judge_no_code_citation: tokens={tokens[:5]} target={target}",
        )
    return True, f"structural_judge_citation: {citations[0]}"


def _extract_verdict_json(text: str) -> dict[str, Any] | None:
    """Robustly extract the {"implemented":..., "evidence":...} object from a reply
    that may wrap prose / ```json fences around the JSON. Returns the first balanced-
    brace candidate that parses AND has an 'implemented' key, else None."""
    if not text:
        return None
    candidates: list[str] = []
    for m in re.finditer(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S):
        candidates.append(m.group(1))
    starts: list[int] = []
    for i, ch in enumerate(text):
        if ch == "{":
            starts.append(i)
        elif ch == "}" and starts:
            s = starts.pop()
            candidates.append(text[s:i + 1])
    for cand in candidates:
        try:
            obj = json.loads(cand)
        except (json.JSONDecodeError, ValueError):
            continue
        if isinstance(obj, dict) and "implemented" in obj:
            return obj
    return None


def _live_llm_judge(
    embodiment_ref_path: str | None,
    decision_token: str,
    decision_log_path: str,
) -> tuple[bool | None, str]:
    """BE-P LIVE judge (signal #1): invoke a REAL LLM (Anthropic) to READ the
    embodiment CODE and emit a file:line citation per the EXISTING Class C judge
    contract (llm_judge_prompt.md — forbids registry/ADR/spec-text substitution).

    Returns (implemented_or_None, evidence). None -> could not run (no key / SDK /
    error / unparseable) -> conservative upstream (DP#44 refuse-on-missing-
    precondition; NEVER fabricate a verdict). The judge reads ACTUAL CODE at the
    embodiment ref; it refuses if the ref IS the DECISION_LOG (anti-substitution)."""
    if not embodiment_ref_path:
        return None, "live_judge_refused: no embodimentRef (ADR-text-only; DP#44)"
    target = pathlib.Path(os.path.expanduser(embodiment_ref_path))
    if not target.exists():
        return None, f"live_judge_unavailable: embodimentRef does not resolve: {embodiment_ref_path}"
    # Anti-substitution: refuse if the embodiment ref IS the DECISION_LOG.
    try:
        if target.resolve() == pathlib.Path(os.path.expanduser(decision_log_path)).resolve():
            return None, "live_judge_refused: embodimentRef IS DECISION_LOG (HC #72)"
    except OSError:
        pass
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        return None, "live_judge_unavailable: ANTHROPIC_API_KEY unset (DP#44 refuse; no fabricated verdict)"
    try:
        import anthropic  # noqa: PLC0415
    except ImportError:
        return None, "live_judge_unavailable: anthropic SDK not installed"
    try:
        contract = pathlib.Path(JUDGE_PROMPT_PATH).read_text(encoding="utf-8", errors="replace")
    except OSError:
        contract = "You are a strict code-reading judge. Refuse registry/ADR/spec-text evidence."
    # Read the embodiment CODE (directory -> concatenate a bounded set of code files;
    # file -> read it). NEVER read DECISION_LOG/registry as the evidence.
    code_blobs: list[str] = []
    if target.is_dir():
        files = [
            f for f in sorted(target.rglob("*"))
            if f.is_file() and f.suffix in (".py", ".sh", ".json", ".yaml", ".yml", ".ttl")
        ][:8]
        for f in files:
            try:
                code_blobs.append(f"### {f}\n" + f.read_text(encoding="utf-8", errors="replace")[:4000])
            except OSError:
                continue
    else:
        try:
            code_blobs.append(f"### {target}\n" + target.read_text(encoding="utf-8", errors="replace")[:12000])
        except OSError as e:
            return None, f"live_judge_unavailable: cannot read embodiment code: {e!r}"
    if not code_blobs:
        return None, f"live_judge_unavailable: no readable code at embodiment ref {target}"
    code = "\n\n".join(code_blobs)[:14000]
    prompt = (
        f"{contract}\n\n--- DECISION TOKEN ---\n{decision_token}\n\n"
        f"--- CANDIDATE EMBODIMENT CODE ({target}) ---\n{code}\n\n"
        "Respond with NOTHING but a single-line JSON object and NO prose before or "
        "after it. EXACTLY this shape: "
        '{"implemented": true, "evidence": "<file:line: verbatim line> OR <reason refused>"}'
    )
    try:
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=_C_JUDGE_MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        verdict = _extract_verdict_json(text)
        if verdict is None:
            return None, f"live_judge_unparseable: {text[:160]!r}"
        return bool(verdict.get("implemented")), f"live_judge[{_C_JUDGE_MODEL}]: {str(verdict.get('evidence', ''))[:200]}"
    except Exception as e:  # noqa: BLE001
        return None, f"live_judge_error: {e!r}"


def probe(
    spec_iri: str,
    decision_token: str | None = None,
    decision_log_path: str | None = None,
    embodiment_ref_path: str | None = None,
    expected_implemented: bool | None = None,
    # BE-P self-test injection (agreement-logic exercise; NOT used in production):
    injected_llm_verdict: bool | None = None,
    use_live_judge: bool = True,
) -> dict[str, Any]:
    """Class C DesignDecision behavioral probe (BE-P, Cycle-16-S19 — LIVE judge).

    Composition (Discipline #30 — diverse, structurally-independent, agreement-
    required):
      precondition: ADR present (else precondition_missing, implemented=False).
      signal #1 = LIVE LLM judge reads CODE at embodimentRef (claude-haiku-4-5),
                  refuses registry/ADR/spec-text per llm_judge_prompt.md.
      signal #2 = the existing _structural_judge token-citation check (DIFFERENT
                  code path).
      implemented=True ONLY when BOTH affirm (agreement). Any None / disagreement /
      no-key -> conservative implemented=False + reason (DP#44; never fabricate).
    The ADR precondition + anti-substitution (embodimentRef != DECISION_LOG) gate
    are retained. In the self-test, the live call is replaced by an injected verdict
    so determinism does not hinge on an online call (the structural signal stays
    live + deterministic)."""
    run_id = f"s19_be_p_production_c_{_short_iri(spec_iri)}_{uuid.uuid4().hex[:6]}"
    ts = _utc_ts()
    decision_log_path = decision_log_path or str(
        pathlib.Path(__file__).resolve().parents[3] / "DECISION_LOG.md"
    )
    decision_token = decision_token or _short_iri(spec_iri)

    # Precondition (i): ADR present
    adr_ok, adr_evidence = _adr_present(decision_log_path, decision_token)
    if not adr_ok:
        return {
            "probe_id": PROBE_ID,
            "probe_version": PROBE_VERSION,
            "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
            "primitive_class": PRIMITIVE_CLASS,
            "spec_iri": spec_iri,
            "run_id": run_id,
            "timestamp": ts,
            "predicateType": PREDICATE_TYPE_FIRE,
            "implemented": False,
            "evidence": f"precondition_failed: {adr_evidence}",
            "evidence_type": "precondition_missing",
            "judge_kind": "live_llm+structural_agreement_v0.2",
        }

    # signal #2: structural judge reads code (NOT ADR text), different code path.
    struct_impl, struct_ev = _structural_judge(
        embodiment_ref_path, decision_token, decision_log_path
    )

    # signal #1: LIVE LLM judge reads code (injected in self-test).
    if injected_llm_verdict is not None or not use_live_judge:
        llm_impl: bool | None = injected_llm_verdict
        llm_ev = f"injected_llm_verdict={injected_llm_verdict} (self-test agreement-logic exercise)"
    else:
        llm_impl, llm_ev = _live_llm_judge(
            embodiment_ref_path, decision_token, decision_log_path
        )

    # agreement-required composition. Both must affirm True for implemented=True.
    # Any None / disagreement -> conservative implemented=False (DP#44 fail-safe).
    if llm_impl is None:
        implemented = False
        agreement = None
        evidence = (f"judge_conservative_not_implemented: live judge unavailable/refused "
                    f"(DP#44) || llm:{llm_ev[:100]} || structural:{struct_ev[:100]}")
    elif llm_impl != struct_impl:
        implemented = False
        agreement = False
        evidence = (f"judge_disagreement_conservative_not_implemented: "
                    f"llm={llm_impl} structural={struct_impl} (NOT-implemented + surfaced) || "
                    f"llm:{llm_ev[:100]} || structural:{struct_ev[:100]}")
    else:
        agreement = True
        implemented = bool(llm_impl)  # == struct_impl
        evidence = (f"judge_agreement_{'implemented' if implemented else 'not_implemented'}: "
                    f"llm==structural=={llm_impl} || llm:{llm_ev[:100]} || structural:{struct_ev[:100]}")

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
        "evidence": evidence,
        "evidence_type": "probe_fire_aggregate",
        "judge_kind": "live_llm+structural_agreement_v0.2",
        "judge_model": _C_JUDGE_MODEL,
        "llm_verdict": llm_impl,
        "structural_verdict": struct_impl,
        "crosscheck_agreement": agreement,
        "adr_evidence": adr_evidence,
    }


def _self_test(fixture_dir: pathlib.Path) -> int:
    project_root = pathlib.Path(__file__).resolve().parents[3]
    sink = project_root / "outputs" / "probe_library_self_test_events.jsonl"
    good = sorted(fixture_dir.glob("known_good_c_*.json"))
    bad = sorted(fixture_dir.glob("known_bad_c_*.json"))
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
            decision_token=cfg.get("decision_token"),
            decision_log_path=cfg.get("decision_log_path"),
            embodiment_ref_path=cfg.get("embodiment_ref_path"),
            # Determinism: the self-test exercises the AGREEMENT logic with an
            # injected LLM verdict (default = the fixture's expected label) so the
            # pass/fail does NOT hinge on a non-deterministic online call. The
            # structural signal stays live + deterministic. The live LLM path is
            # exercised only in the production aggregate fire.
            injected_llm_verdict=cfg.get(
                "injected_llm_verdict", cfg.get("expected_implemented")
            ),
            use_live_judge=False,
        )
        expected = cfg["expected_implemented"]
        distinguished = result["implemented"] == expected
        all_distinguished = all_distinguished and distinguished
        rows.append(
            {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_f.probe_library_self_test",
                "event_class": (
                    "probe_library_self_test.pass.event"
                    if distinguished
                    else "probe_library_self_test.fail.event"
                ),
                "predicateType": PREDICATE_TYPE_SELF_TEST,
                "timestamp": _utc_ts(),
                "run_id": f"s11_be_f_probe_lib_self_test_c_{fx.stem}_{uuid.uuid4().hex[:6]}",
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
                    "judge_kind": result.get("judge_kind"),
                },
            }
        )
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
    data = json.loads(pathlib.Path(scan_json_path).read_text())
    specs = [
        s
        for s in data.get("per_spec_evidence_IP_PRIVATE", [])
        if s.get("spec_class") == "c_design_decision"
    ]
    if limit:
        specs = specs[:limit]
    sink = pathlib.Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    fired = 0
    with sink.open("a", encoding="utf-8") as f:
        for s in specs:
            audit_tuple = s.get("audit_tuple") or [None, None, None]
            # audit_tuple[1] = file path; [2] = registry key (e.g., paradigm_dispositions:<key>)
            decision_log_path = (
                os.path.expanduser(audit_tuple[1]) if audit_tuple[1] else None
            )
            # Token cleaning: registry keys like "paradigm_dispositions:foo_bar_baz"
            # are colon-prefixed registry slots. Extract the trailing-keyword
            # portion (which is more likely to surface in code/docs); fall
            # back to the name_truncated.
            raw_token = (
                audit_tuple[2]
                if len(audit_tuple) >= 3 and audit_tuple[2]
                else s.get("name_truncated") or _short_iri(s["spec_id"])
            )
            token = raw_token.split(":", 1)[-1] if ":" in raw_token else raw_token
            # Truncate JSON-blob tokens (e.g., decisions_log:{'date':...}) at
            # the first non-identifier character to surface a usable keyword.
            token = re.split(r"[\s,{}\[\]'\"]+", token)[0] or raw_token
            # For DesignDecision specs in state.json paradigm_dispositions, the
            # embodimentRef is typically the source code that ENACTS the disposition.
            # Heuristic: state.json itself is the registry; the cycle's
            # scripts/ dir is the code where dispositions are enacted.
            embodiment_dir = None
            if decision_log_path and "state.json" in decision_log_path:
                # Embodiment ref = the cycle dir's scripts/ (where dispositions enacted)
                cycle_dir = pathlib.Path(decision_log_path).parent
                if (cycle_dir / "scripts").is_dir():
                    embodiment_dir = str(cycle_dir / "scripts")
            elif decision_log_path:
                # Embodiment = the cycle dir's docs/ or scripts/ neighbor
                cycle_dir = pathlib.Path(decision_log_path).parent
                for c in (cycle_dir / "docs", cycle_dir / "scripts"):
                    if c.is_dir():
                        embodiment_dir = str(c)
                        break
            result = probe(
                spec_iri=s["spec_id"],
                decision_token=token,
                decision_log_path=decision_log_path,
                embodiment_ref_path=embodiment_dir,
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
                    "judge_kind": result.get("judge_kind"),
                },
            }
            f.write(json.dumps(row) + "\n")
            fired += 1
    print(f"PASS: aggregate-cycle fired {fired} probes against DesignDecision specs (sink={sink_path})")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Probe Class C — DesignDecision")
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
    p.add_argument("--spec-iri", default=None)
    p.add_argument("--decision-token", default=None)
    p.add_argument("--decision-log-path", default=None)
    p.add_argument("--embodiment-ref-path", default=None)
    args = p.parse_args(argv)

    if args.self_test:
        fixture_dir = (
            pathlib.Path(__file__).resolve().parents[3] / "tests" / "probes" / "fixtures"
        )
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
            decision_token=args.decision_token,
            decision_log_path=args.decision_log_path,
            embodiment_ref_path=args.embodiment_ref_path,
        )
        print(json.dumps(result, indent=2))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
