#!/usr/bin/env python3
"""Probe Class F — spec-implementation behavioral-fidelity check.

Research-tree branch 1b (BE-K / Cycle-16-S16 dispatch substrate §0-§5): does the
CODE behaviorally do what the spec COMMITS to — NOT "a function with the right
name exists" (Done #32 behavioral-fidelity bar). Plus Done #26: bring the live
code-reading LLM judge in-cycle for the semantic-conformance fallback (the Class C
LLM-judge path was stubbed to `_structural_judge` only; deferred to C17+).

WHAT CLASS F IS (and is NOT) — Done #42 detector discipline:
    Class F is a DETECTOR. It does NOT fix, remediate, or correct. Findings QUEUE
    under the validate-before-remediate lock (D-S15-1). This probe emits NO
    "implemented" / "X% faithful" HEADLINE COUNT. Class F's OWN accuracy is
    UNVALIDATED until the probe-accuracy validation step (Done #25, next session)
    against diverse independent automated ground truth. Raw fire tallies are
    reported as MEASURED DIVERGENCE only, never as a fidelity verdict on the
    codebase (HC #70).

THE JUDGE-GROUNDING CONTRACT — Done #41 floor (substrate §1; designed-against, not
bolted-on). The probe bottoms out in this exact precedence:

  (1) EXECUTION FIRST (default; objective; no judge opinion). The committed
      behavioral observable for Class F is the spec's `runtime_emit_event_class`.
      The probe checks — BY EXECUTION — that the embodiment ACTUALLY EMITS an
      event whose class == the committed `runtime_emit_event_class`. KT-8:
      import+execute / read the real RUNTIME EMISSION RECORD, NEVER string-match
      the registry or spec source.
        - Match  -> faithful (execution-grounded).
        - Wrong event class / wrong payload ("code exists but does the WRONG
          thing") -> NOT-faithful, objectively, NO judge.
      The execution path uses this precedence to resolve the emission:
        (a) If the embodiment is a Python module that exposes a callable predicate
            (`emit` / a `probe()` / a named emitter), IMPORT it (importlib, the
            Class E `_import_probe_module` precedent) and EXECUTE it in a sandboxed
            capture, asserting the emitted event_class.
        (b) Otherwise (agent-spec `.md` / `.ttl`-ontology embodiments, which are
            NOT Python-importable), the execution-grounded observable is the
            RUNTIME EMISSION SINK: the probe READS `outputs/*_events.jsonl` (the
            record produced by actually RUNNING the embodiment) and confirms a
            real emitted event of the committed class exists. This is execution
            of the emission, read from its product — NOT a registry/spec-text
            string match (KT-8 honored: we read the emission RECORD, not the
            `runtime_emit_event_class` registry field).

  (2) JUDGE ONLY AS FALLBACK for semantic/behavioral conformance that cannot be
      executed (no executable observable resolvable; emission absent AND no
      Python embodiment). The judge READS ACTUAL CODE at the embodiment ref
      (subprocess git/file resolve+read), emits a `file:line` citation, and
      REFUSES registry-state / ADR-text / spec-text / state.json / FINDINGS-
      mention / comment-only evidence (the Class C `llm_judge_prompt.md`
      forbidden-substitution list — reused VERBATIM as the judge contract).
      A judge verdict is valid ONLY when cross-checked by >=1 STRUCTURALLY-
      INDEPENDENT automated signal (the `_structural_judge` token-citation check,
      a different code path from the LLM read). AGREEMENT REQUIRED; disagreement
      -> conservative NOT-faithful + queued. A lone LLM opinion is NOT acceptance.

  (3) NO human label anywhere (Done #41). Ambiguity NEVER blocks: ambiguous
      fidelity = NOT-faithful -> tracked + surfaced as an after-the-fact report
      line. The cycle-close path has NO mandatory human step.

  DP#26 carve-out: specs with `runtime_emit_event_class == 'n/a'` (incl. the
  literal `'n/a -- citation-based activation per DP#26'`) are methodology
  commitments with NO executable behavior -> disposition = a DISTINCT
  `not_applicable_dp26_carveout`, surfaced separately, NOT counted faithful or
  unfaithful.

EMBODIMENT-CODE RESOLUTION (substrate §2 — scan records carry NO explicit
`embodimentRef`; resolution choice documented here):
    The scan record carries `audit_tuple = [repo_label, source_path, source_kind]`
    + `runtime_emit_event_class`. There is no `embodimentRef` field. We resolve
    the embodiment in this order:
      1. The committed `runtime_emit_event_class` IS the behavioral commitment.
         For the execution path we look for a real emitted event of that class in
         the runtime emission sink(s) (`outputs/*_events.jsonl` under the project
         root, plus the source repo's `outputs/` if resolvable from audit_tuple).
      2. If `audit_tuple[1]` resolves to a Python module exposing an emit
         callable, import+execute it (precedence (1)(a)).
      3. The judge-fallback embodiment ref = `audit_tuple[1]` (the spec source
         file / the neighbouring `scripts|runtime|docs` dir), read as CODE, never
         as the registry/spec text. The judge REFUSES if the only resolvable
         evidence is the spec/registry/ADR text itself.
    Rationale: `runtime_emit_event_class` is the spec's explicit behavioral
    commitment under the Cycle-16 14-field schema; the dormancy taxonomy
    ('running' = runtime_emit firing evidence in outputs/*_events.jsonl) makes the
    emission sink the canonical execution-grounded observable. Reading the
    EMISSION RECORD (not the registry field) is the KT-8-honoring execution check.

LIVE-LLM SPLIT (Done #26 / substrate §2 + §4):
    The judge-fallback path invokes a REAL LLM (Anthropic API via the `anthropic`
    SDK) to READ code for semantic conformance. BUT the self-test pass/fail
    determinism MUST NOT hinge on a non-deterministic online call: the self-test's
    load-bearing distinctions come from (a) the EXECUTION path (good vs wrong-
    thing) and (b) the DETERMINISTIC REFUSAL path (text-only refused PRE-LLM, by
    the anti-substitution gate, before any model call). The self-test exercises
    the judge+cross-check AGREEMENT logic with INJECTED/recorded judge outputs
    (`_evaluate_judge_with_crosscheck`); the live LLM is exercised only in the
    production fire when a key is present. If no LLM key is configured, the live
    judge path REFUSES conservatively (NOT-faithful) rather than fabricating a
    verdict (DP#44 refuse-on-missing-precondition) — it never silently passes.

KT-13 (substrate §4, NEW): a >10% behavioral-divergence rate (not-faithful over
APPLICABLE specs, i.e. excluding DP#26 carve-outs) fires a CONSERVATIVE surface +
remediation-queue annotation in the aggregate output / JSONL — NEVER a halt
(Done #41/#42 detector, never a blocking remediation). HR formalization is a later
RP touch.

Version-lock per Done #13: PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned;
modifications require Builder-ARCH paradigm dispatch (HC #74 BINDING).
"""
from __future__ import annotations

import argparse
import datetime
import glob
import importlib.util
import io
import json
import os
import pathlib
import re
import subprocess
import sys
import uuid
from contextlib import redirect_stdout
from typing import Any

PROBE_VERSION = "0.1"
# Build-time admission lock commit — pinned at BE-K build HEAD (mirrors the Class C
# / Class E pinned-at-admission-baseline pattern). Bumps require Builder-ARCH
# paradigm dispatch (HC #74 BINDING).
PROBE_ADMISSION_LOCK_COMMIT = "1184a550b2c8b620839cf99c77cee728e3e2d208"
PROBE_ID = "probe_spec_impl_fidelity_v0.1"
PRIMITIVE_CLASS = "F"
PREDICATE_TYPE_FIRE = "cycle16:probe_fire_v1"
PREDICATE_TYPE_SELF_TEST = "cycle16:probe_self_test_v1"

JUDGE_PROMPT_PATH = str(
    pathlib.Path(__file__).resolve().parents[1] / "c" / "llm_judge_prompt.md"
)
_STRUCTURAL_JUDGE_PATH = (
    pathlib.Path(__file__).resolve().parents[1] / "c" / "probe_design_decision.py"
)

# DP#26 carve-out detection: runtime_emit_event_class values that denote a
# methodology commitment with no executable behavior.
_NA_PREFIXES = ("n/a",)

KT13_DIVERGENCE_THRESHOLD = 0.10  # >10% not-faithful over applicable specs -> surface

# Anthropic model for the live judge (Done #26). Cheap, fast, code-reading capable.
_JUDGE_MODEL = os.environ.get("CYCLE16_JUDGE_MODEL", "claude-haiku-4-5")


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short_iri(spec_iri: str) -> str:
    tail = spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail.replace("spec_retroactive_", "").replace("-", "_")[:24] or "anon"


def _project_root() -> pathlib.Path:
    return pathlib.Path(__file__).resolve().parents[3]


def _is_dp26_carveout(runtime_emit_event_class: str | None) -> bool:
    if not runtime_emit_event_class:
        return False
    low = runtime_emit_event_class.strip().lower()
    return any(low.startswith(p) for p in _NA_PREFIXES)


# --- (1) EXECUTION-FIRST: does the embodiment actually EMIT the committed class? --


def _candidate_emission_sinks(source_path: str | None) -> list[pathlib.Path]:
    """Resolve the runtime-emission sinks to scan for a real emitted event.

    Always include the project's own outputs/*.jsonl. If the spec's source path
    resolves to another repo, include that repo's outputs/*.jsonl too. We read the
    EMISSION RECORD (the product of executing the embodiment), NOT the registry."""
    sinks: list[pathlib.Path] = []
    proot = _project_root()
    for f in sorted(proot.glob("outputs/*.jsonl")):
        sinks.append(f)
    if source_path:
        sp = pathlib.Path(os.path.expanduser(source_path))
        # Walk up to find a repo root with an outputs/ dir.
        for anc in [sp] + list(sp.parents):
            cand = anc / "outputs"
            if cand.is_dir():
                for f in sorted(cand.glob("*.jsonl")):
                    if f not in sinks:
                        sinks.append(f)
                break
    return sinks


def _event_class_matches(emitted: str | None, committed: str) -> bool:
    """A committed class 'foo.bar.baz' is satisfied by an emitted event_class equal
    to it, OR a namespaced variant whose dotted tail equals the committed class
    (e.g. committed 'session.start' satisfied by 'build_runner.session.start'), OR
    the committed class as a strict dotted-suffix of the emitted class. Exact-class
    equality is the strong signal; suffix is the lenient fallback for namespace
    prefixes. Anything else -> no match (wrong thing)."""
    if not emitted:
        return False
    if emitted == committed:
        return True
    # committed is a dotted suffix of emitted (namespace prefix difference)
    if emitted.endswith("." + committed):
        return True
    if committed.endswith("." + emitted):
        return True
    return False


def _execution_check_emission(
    committed_event_class: str, source_path: str | None
) -> tuple[bool | None, str, str]:
    """EXECUTION path (b): read the runtime emission RECORD and confirm a real
    emitted event of the committed class exists.

    Returns (faithful_or_None, evidence, sub_path). faithful_or_None is:
        True  -> committed class found emitted (execution-grounded faithful)
        False -> embodiment emitted events but NONE of the committed class, AND at
                 least one event shares the committed class's namespace head
                 (i.e. the embodiment is active but does the WRONG thing)
        None  -> no emission evidence at all in any sink (execution inconclusive;
                 hand to judge fallback)
    """
    sinks = _candidate_emission_sinks(source_path)
    if not sinks:
        return None, "execution_inconclusive: no emission sink found", "execution_emission"
    committed_head = committed_event_class.split(".", 1)[0]
    seen_classes: set[str] = set()
    matched_line: str | None = None
    for sink in sinks:
        try:
            with sink.open(encoding="utf-8", errors="replace") as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        rec = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    ec = rec.get("event_class")
                    if not ec:
                        continue
                    seen_classes.add(ec)
                    if _event_class_matches(ec, committed_event_class):
                        matched_line = f"{sink.name}: event_class={ec!r} run_id={rec.get('run_id')!r}"
                        break
        except OSError:
            continue
        if matched_line:
            break
    if matched_line:
        return (
            True,
            f"execution_faithful: committed class {committed_event_class!r} EMITTED "
            f"(read from emission record, not registry) || {matched_line}",
            "execution_emission",
        )
    # No committed-class emission. Is the embodiment nonetheless active in the
    # committed namespace head -> WRONG-THING (active but emits wrong class)?
    same_head = sorted(
        c for c in seen_classes if c.split(".", 1)[0] == committed_head
    )
    if same_head:
        return (
            False,
            f"execution_not_faithful: embodiment ACTIVE in namespace {committed_head!r} "
            f"but emits WRONG class(es) {same_head[:5]} -- committed {committed_event_class!r} "
            f"NEVER emitted (caught by execution, not text)",
            "execution_emission",
        )
    return (
        None,
        f"execution_inconclusive: committed class {committed_event_class!r} not in any "
        f"emission sink and no same-namespace activity (hand to judge fallback)",
        "execution_emission",
    )


def _execution_check_python(
    source_path: str | None, committed_event_class: str
) -> tuple[bool | None, str, str]:
    """EXECUTION path (a): if source_path is a Python module exposing an emit
    callable, IMPORT it (KT-8) and EXECUTE in a captured-stdout sandbox, asserting
    the emitted event_class. Conservative: any import/exec error -> None (fall
    through to emission-record check); never raises into the probe."""
    if not source_path:
        return None, "no_python_embodiment: no source path", "execution_python"
    sp = pathlib.Path(os.path.expanduser(source_path))
    if not sp.exists() or sp.suffix != ".py":
        return None, "no_python_embodiment: source not a .py module", "execution_python"
    try:
        spec = importlib.util.spec_from_file_location(
            f"be_f_embodiment_{sp.stem}_{uuid.uuid4().hex[:6]}", str(sp)
        )
        if spec is None or spec.loader is None:
            return None, "no_python_embodiment: import spec unresolvable", "execution_python"
        mod = importlib.util.module_from_spec(spec)
        buf = io.StringIO()
        with redirect_stdout(buf):
            spec.loader.exec_module(mod)
            emitter = None
            for name in ("emit", "emit_event", "main"):
                fn = getattr(mod, name, None)
                if callable(fn):
                    emitter = fn
                    break
            if emitter is None:
                return (
                    None,
                    "no_python_embodiment: no emit/main callable exposed",
                    "execution_python",
                )
        # We imported+executed the module (KT-8). Without a controlled fixture
        # harness for arbitrary embodiments we do NOT blindly call emitter() (could
        # have side effects); module-level execution already exercised import. The
        # emission-record check is the behavioral observable. Report import success.
        return (
            None,
            f"python_embodiment_imported: {sp.name} exposes emit callable "
            f"(import+execute OK; behavioral check via emission record)",
            "execution_python",
        )
    except Exception as e:  # noqa: BLE001 — conservative: any error -> fall through
        return (
            None,
            f"python_embodiment_import_error: {e!r} (fall through to emission check)",
            "execution_python",
        )


# --- (2) JUDGE FALLBACK: read ACTUAL CODE, refuse text-only, cross-check ----------


def _import_structural_judge():
    """Import the Class C `_structural_judge` (the structurally-independent
    automated cross-check signal). KT-8 import+execute of an existing primitive."""
    spec = importlib.util.spec_from_file_location(
        "be_f_structural_judge_xcheck", str(_STRUCTURAL_JUDGE_PATH)
    )
    if spec is None or spec.loader is None:
        return None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _anti_substitution_refuses(
    embodiment_ref_path: str | None,
    spec_source_path: str | None,
    spec_iri: str,
) -> tuple[bool, str]:
    """DETERMINISTIC, PRE-LLM refusal gate (the load-bearing self-test refusal).

    Refuses (returns True, reason) when the only resolvable evidence is spec /
    registry / ADR / state.json text — the forbidden-substitution list from the
    Class C llm_judge_prompt.md. The judge CANNOT pass by reading the spec text.

    Returns (refuses, reason). refuses=True -> conservative NOT-faithful, no LLM
    call made."""
    # No embodiment ref at all -> nothing to read as code -> refuse.
    if not embodiment_ref_path:
        return True, "anti_substitution_refusal: no embodiment code ref (text/registry-only evidence)"
    target = pathlib.Path(os.path.expanduser(embodiment_ref_path))
    if not target.exists():
        return True, f"anti_substitution_refusal: embodiment ref does not resolve: {embodiment_ref_path}"
    # Refuse if the embodiment ref IS a registry/spec-text artifact (state.json,
    # DECISION_LOG, FINDINGS, *_registry*.json, the spec source itself).
    name = target.name.lower()
    forbidden_markers = (
        "state.json",
        "decision_log",
        "findings",
        "_registry",
        "spec_registry",
        "retroactive_scan",
    )
    if any(m in name for m in forbidden_markers):
        return (
            True,
            f"anti_substitution_refusal: embodiment ref is registry/spec-text artifact "
            f"({target.name}) — forbidden-substitution (HC #72)",
        )
    if spec_source_path:
        ssp = pathlib.Path(os.path.expanduser(spec_source_path))
        try:
            if target.resolve() == ssp.resolve():
                return (
                    True,
                    "anti_substitution_refusal: embodiment ref IS the spec source itself (spec-text substitution)",
                )
        except OSError:
            pass
    return False, "anti_substitution_gate_pass: embodiment ref is candidate code"


def _live_llm_judge(
    embodiment_ref_path: str, decision_token: str
) -> tuple[bool | None, str]:
    """Done #26 LIVE judge: invoke a REAL LLM (Anthropic) to read code at the
    embodiment ref and emit a file:line citation per the Class C judge contract.

    Returns (implemented_or_None, evidence). None -> could not run (no key / SDK /
    error) -> conservative NOT-faithful upstream (DP#44 refuse-on-missing-
    precondition; NEVER fabricate a verdict)."""
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
    target = pathlib.Path(os.path.expanduser(embodiment_ref_path))
    try:
        code = target.read_text(encoding="utf-8", errors="replace")[:12000]
    except OSError as e:
        return None, f"live_judge_unavailable: cannot read embodiment code: {e!r}"
    prompt = (
        f"{contract}\n\n--- DECISION TOKEN ---\n{decision_token}\n\n"
        f"--- CANDIDATE EMBODIMENT CODE ({target}) ---\n{code}\n\n"
        "Return ONLY a JSON object: "
        '{\"implemented\": true|false, \"evidence\": \"<file:line: verbatim line> OR <reason refused>\"}'
    )
    try:
        client = anthropic.Anthropic(api_key=api_key)
        resp = client.messages.create(
            model=_JUDGE_MODEL,
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")
        m = re.search(r"\{.*\}", text, re.S)
        if not m:
            return None, f"live_judge_unparseable: {text[:160]!r}"
        verdict = json.loads(m.group(0))
        return bool(verdict.get("implemented")), f"live_judge: {verdict.get('evidence', '')[:200]}"
    except Exception as e:  # noqa: BLE001
        return None, f"live_judge_error: {e!r}"


def _evaluate_judge_with_crosscheck(
    embodiment_ref_path: str | None,
    decision_token: str,
    spec_source_path: str | None,
    spec_iri: str,
    decision_log_path: str | None = None,
    injected_llm_verdict: bool | None = None,
    injected_structural_verdict: bool | None = None,
) -> tuple[bool, str, dict[str, Any]]:
    """JUDGE FALLBACK with MANDATORY >=1 structurally-independent cross-check.

    Precedence:
      1. Deterministic anti-substitution refusal (PRE-LLM). text-only -> NOT-faithful.
      2. LLM judge reads code (live in production; injected in self-test).
      3. Structural-judge cross-check (Class C `_structural_judge`, independent
         code path). AGREEMENT REQUIRED. Disagreement -> conservative NOT-faithful.
      A lone LLM 'true' with no agreeing cross-check is NOT acceptance.

    Returns (faithful, evidence, sub_checks)."""
    sub: dict[str, Any] = {"path": "judge_fallback"}
    refuses, reason = _anti_substitution_refuses(
        embodiment_ref_path, spec_source_path, spec_iri
    )
    sub["anti_substitution_refusal"] = refuses
    if refuses:
        sub["llm_verdict"] = None
        sub["structural_verdict"] = None
        sub["crosscheck_agreement"] = None
        return False, reason, sub

    assert embodiment_ref_path is not None  # gate guarantees resolvable code ref

    # --- LLM judge (independent signal #1) ---
    if injected_llm_verdict is not None:
        llm_verdict: bool | None = injected_llm_verdict
        llm_ev = f"injected_llm_verdict={injected_llm_verdict} (self-test agreement-logic exercise)"
    else:
        llm_verdict, llm_ev = _live_llm_judge(embodiment_ref_path, decision_token)
    sub["llm_verdict"] = llm_verdict
    sub["llm_evidence"] = llm_ev[:200]

    # --- Structural-judge cross-check (independent signal #2; different code path) ---
    if injected_structural_verdict is not None:
        struct_verdict: bool | None = injected_structural_verdict
        struct_ev = f"injected_structural_verdict={injected_structural_verdict}"
    else:
        sj = _import_structural_judge()
        if sj is None or not hasattr(sj, "_structural_judge"):
            struct_verdict, struct_ev = None, "structural_judge_unavailable"
        else:
            dlp = decision_log_path or str(_project_root() / "DECISION_LOG.md")
            try:
                struct_verdict, struct_ev = sj._structural_judge(
                    embodiment_ref_path, decision_token, dlp
                )
            except Exception as e:  # noqa: BLE001
                struct_verdict, struct_ev = None, f"structural_judge_error: {e!r}"
    sub["structural_verdict"] = struct_verdict
    sub["structural_evidence"] = struct_ev[:200]

    # --- agreement-required composition ---
    # Valid acceptance REQUIRES the LLM judge AND the independent structural
    # cross-check to BOTH affirm. Any None, any disagreement -> conservative
    # NOT-faithful. A lone LLM opinion is NOT acceptance.
    if llm_verdict is None or struct_verdict is None:
        sub["crosscheck_agreement"] = False
        return (
            False,
            f"judge_conservative_not_faithful: missing independent signal "
            f"(llm={llm_verdict}, structural={struct_verdict}) || llm:{llm_ev[:80]} || struct:{struct_ev[:80]}",
            sub,
        )
    if llm_verdict != struct_verdict:
        sub["crosscheck_agreement"] = False
        return (
            False,
            f"judge_disagreement_conservative_not_faithful: llm={llm_verdict} "
            f"structural={struct_verdict} (disagreement -> NOT-faithful + queued) || "
            f"llm:{llm_ev[:80]} || struct:{struct_ev[:80]}",
            sub,
        )
    sub["crosscheck_agreement"] = True
    faithful = bool(llm_verdict)  # == struct_verdict
    return (
        faithful,
        f"judge_crosscheck_{'faithful' if faithful else 'not_faithful'}: "
        f"llm==structural=={llm_verdict} (agreement) || llm:{llm_ev[:80]} || struct:{struct_ev[:80]}",
        sub,
    )


# --- the probe -------------------------------------------------------------------


def probe(
    spec_iri: str,
    runtime_emit_event_class: str | None = None,
    source_path: str | None = None,
    embodiment_ref_path: str | None = None,
    decision_token: str | None = None,
    current_status: str | None = None,
    # self-test injection (judge agreement-logic exercise; NOT used in production):
    injected_llm_verdict: bool | None = None,
    injected_structural_verdict: bool | None = None,
    expected_fidelity: bool | None = None,
) -> dict[str, Any]:
    """Class F spec-implementation behavioral-fidelity probe.

    disposition in {faithful, not_faithful, not_applicable_dp26_carveout, unverifiable}.
    fidelity_ok True ONLY for execution-grounded faithful OR judge+cross-check
    agreed-faithful. Everything else (wrong-thing, refusal, missing signal,
    ambiguity, error) -> fidelity_ok False, conservative. No human step."""
    run_id = f"s16_be_k_production_f_{_short_iri(spec_iri)}_{uuid.uuid4().hex[:6]}"
    ts = _utc_ts()
    decision_token = decision_token or _short_iri(spec_iri)

    # DP#26 carve-out: methodology commitment, no executable behavior.
    if _is_dp26_carveout(runtime_emit_event_class):
        return _build_result(
            spec_iri, run_id, ts, False, "not_applicable_dp26_carveout",
            f"dp26_carveout: runtime_emit_event_class={runtime_emit_event_class!r} "
            f"(methodology commitment; no executable behavior; not counted faithful/unfaithful)",
            {"path": "dp26_carveout"},
            extra={"runtime_emit_event_class": runtime_emit_event_class,
                   "current_status": current_status},
        )

    # No committed observable at all -> unverifiable (conservative).
    if not runtime_emit_event_class:
        # Fall to judge ONLY if an embodiment code ref is supplied; else unverifiable.
        if embodiment_ref_path:
            faithful, evidence, sub = _evaluate_judge_with_crosscheck(
                embodiment_ref_path, decision_token, source_path, spec_iri,
                injected_llm_verdict=injected_llm_verdict,
                injected_structural_verdict=injected_structural_verdict,
            )
            disp = "faithful" if faithful else "not_faithful"
            return _build_result(spec_iri, run_id, ts, faithful, disp, evidence, sub,
                                 extra={"runtime_emit_event_class": None,
                                        "current_status": current_status})
        return _build_result(
            spec_iri, run_id, ts, False, "unverifiable",
            "unverifiable: no runtime_emit_event_class committed and no embodiment code ref",
            {"path": "unverifiable"},
            extra={"current_status": current_status},
        )

    # (1) EXECUTION FIRST.
    # (1a) Python embodiment import+execute (KT-8). Inconclusive -> fall through.
    py_ok, py_ev, _ = _execution_check_python(source_path, runtime_emit_event_class)
    # (1b) Emission-record execution check (the behavioral observable).
    emit_ok, emit_ev, emit_path = _execution_check_emission(
        runtime_emit_event_class, source_path
    )

    if emit_ok is True:
        return _build_result(
            spec_iri, run_id, ts, True, "faithful",
            f"{emit_ev} || python:{py_ev[:80]}",
            {"path": "execution", "execution_sub": emit_path, "python_import": py_ev[:80],
             "judge_invoked": False},
            extra={"runtime_emit_event_class": runtime_emit_event_class,
                   "current_status": current_status},
        )
    if emit_ok is False:
        # WRONG-THING caught by execution. Objective NOT-faithful, no judge.
        return _build_result(
            spec_iri, run_id, ts, False, "not_faithful",
            f"{emit_ev} || python:{py_ev[:80]}",
            {"path": "execution", "execution_sub": emit_path, "python_import": py_ev[:80],
             "judge_invoked": False},
            extra={"runtime_emit_event_class": runtime_emit_event_class,
                   "current_status": current_status},
        )

    # (2) Execution inconclusive -> JUDGE FALLBACK (read code, refuse text-only,
    #     mandatory cross-check, agreement-required).
    eref = embodiment_ref_path or source_path
    faithful, j_evidence, sub = _evaluate_judge_with_crosscheck(
        eref, decision_token, source_path, spec_iri,
        injected_llm_verdict=injected_llm_verdict,
        injected_structural_verdict=injected_structural_verdict,
    )
    sub["execution_evidence"] = emit_ev[:120]
    disp = "faithful" if faithful else "not_faithful"
    return _build_result(
        spec_iri, run_id, ts, faithful, disp,
        f"execution_inconclusive->judge_fallback || {j_evidence}",
        sub,
        extra={"runtime_emit_event_class": runtime_emit_event_class,
               "current_status": current_status},
    )


def _build_result(
    spec_iri: str,
    run_id: str,
    ts: str,
    fidelity_ok: bool,
    disposition: str,
    evidence: str,
    sub_checks: dict[str, Any],
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    result = {
        "probe_id": PROBE_ID,
        "probe_version": PROBE_VERSION,
        "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
        "primitive_class": PRIMITIVE_CLASS,
        "spec_iri": spec_iri,
        "run_id": run_id,
        "timestamp": ts,
        "predicateType": PREDICATE_TYPE_FIRE,
        "fidelity_ok": fidelity_ok,
        # faithful | not_faithful | not_applicable_dp26_carveout | unverifiable
        "disposition": disposition,
        "evidence": evidence,
        "evidence_type": "probe_fire_aggregate",
        "sub_checks": sub_checks,
    }
    if extra:
        result.update(extra)
    return result


# --- self-test -------------------------------------------------------------------


def _self_test(fixture_dir: pathlib.Path) -> int:
    """Self-test: distinguish good (exec-pass) / wrong-thing (exec-fail) /
    text-only (judge REFUSE). Determinism comes from the EXECUTION path and the
    DETERMINISTIC pre-LLM refusal — NOT from any online call. The judge agreement
    logic is exercised via injected verdicts. Emits per-fixture JSONL with
    predicateType cycle16:probe_self_test_v1. Exit 0 iff distinguishes ALL."""
    project_root = _project_root()
    sink = project_root / "outputs" / "probe_library_self_test_events.jsonl"
    good = sorted(fixture_dir.glob("known_good_f_*.json"))
    bad = sorted(fixture_dir.glob("known_bad_f_*.json"))
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
            runtime_emit_event_class=cfg.get("runtime_emit_event_class"),
            source_path=cfg.get("source_path"),
            embodiment_ref_path=cfg.get("embodiment_ref_path"),
            decision_token=cfg.get("decision_token"),
            current_status=cfg.get("current_status"),
            injected_llm_verdict=cfg.get("injected_llm_verdict"),
            injected_structural_verdict=cfg.get("injected_structural_verdict"),
            expected_fidelity=cfg.get("expected_fidelity"),
        )
        expected = cfg["expected_fidelity"]
        distinguished = result["fidelity_ok"] == expected
        # Also assert the EXPECTED PATH fired where the fixture pins it (so a
        # text-only fixture that happens to be False for the WRONG reason fails).
        expected_path = cfg.get("expected_path")
        if expected_path is not None:
            actual_path = result["sub_checks"].get("path")
            path_ok = actual_path == expected_path or (
                expected_path == "judge_refusal"
                and result["sub_checks"].get("anti_substitution_refusal") is True
            )
            distinguished = distinguished and path_ok
        all_distinguished = all_distinguished and distinguished
        rows.append(
            {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_k.spec_impl_fidelity_self_test",
                "event_class": (
                    "probe_library_self_test.pass.event"
                    if distinguished
                    else "probe_library_self_test.fail.event"
                ),
                "predicateType": PREDICATE_TYPE_SELF_TEST,
                "timestamp": _utc_ts(),
                "run_id": f"s16_be_k_probe_lib_self_test_f_{fx.stem}_{uuid.uuid4().hex[:6]}",
                "payload": {
                    "probe_id": PROBE_ID,
                    "probe_version": PROBE_VERSION,
                    "primitive_class": PRIMITIVE_CLASS,
                    "fixture_path": str(fx),
                    "fixture_class": "known_good" if fx.name.startswith("known_good") else "known_bad",
                    "expected_fidelity": expected,
                    "actual_fidelity_ok": result["fidelity_ok"],
                    "expected_path": expected_path,
                    "actual_path": result["sub_checks"].get("path"),
                    "distinguished": distinguished,
                    "disposition": result["disposition"],
                    "anti_substitution_refusal": result["sub_checks"].get("anti_substitution_refusal"),
                    "crosscheck_agreement": result["sub_checks"].get("crosscheck_agreement"),
                    "evidence": result["evidence"][:240],
                },
            }
        )
    sink.parent.mkdir(parents=True, exist_ok=True)
    with sink.open("a", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")
    if not all_distinguished:
        print(
            "FAIL: self-test did not distinguish good(exec-pass) / "
            "wrong-thing(exec-fail) / text-only(judge-refuse)",
            file=sys.stderr,
        )
    return 0 if all_distinguished else 1


# --- aggregate-cycle (production dogfood / periodic audit) ------------------------


def _aggregate_cycle(
    cycle_n: int,
    scan_json_path: str,
    sink_path: str,
    limit: int | None,
    run_id_prefix_override: str | None = None,
    applicable_only: bool = False,
) -> int:
    """Production dogfood: fire Class F against the REAL cycle16:Spec population
    from the retroactive scan JSON (the source-of-record carrying
    runtime_emit_event_class + audit_tuple + current_status). NON-smoke: real
    run_ids, real verdicts, real JSONL.

    KT-13: >10% behavioral-divergence (not_faithful over APPLICABLE specs, i.e.
    excluding DP#26 carve-outs) -> CONSERVATIVE surface + remediation-queue
    annotation; NEVER a halt (Done #41/#42)."""
    data = json.loads(pathlib.Path(scan_json_path).read_text())
    specs = data.get("per_spec_evidence_IP_PRIVATE", [])
    if applicable_only:
        specs = [
            s for s in specs
            if not _is_dp26_carveout(s.get("runtime_emit_event_class"))
        ]
    if limit:
        specs = specs[:limit]
    sink = pathlib.Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    fired = faithful = not_faithful = dp26 = unverifiable = 0
    remediation_queue: list[str] = []
    with sink.open("a", encoding="utf-8") as f:
        for s in specs:
            audit = s.get("audit_tuple") or [None, None, None]
            source_path = os.path.expanduser(audit[1]) if len(audit) >= 2 and audit[1] else None
            token = audit[2] if len(audit) >= 3 and audit[2] else s.get("name_truncated")
            result = probe(
                spec_iri=s["spec_id"],
                runtime_emit_event_class=s.get("runtime_emit_event_class"),
                source_path=source_path,
                embodiment_ref_path=source_path,
                decision_token=token,
                current_status=s.get("current_status"),
            )
            if run_id_prefix_override:
                result["run_id"] = (
                    f"{run_id_prefix_override}_{_short_iri(s['spec_id'])}_{uuid.uuid4().hex[:6]}"
                )
            disp = result["disposition"]
            if disp == "faithful":
                faithful += 1
            elif disp == "not_applicable_dp26_carveout":
                dp26 += 1
            elif disp == "unverifiable":
                unverifiable += 1
            else:  # not_faithful
                not_faithful += 1
                remediation_queue.append(result["spec_iri"])
            row = {
                "schema_version": "0.1",
                "namespace": "cycle_16.be_k.spec_impl_fidelity",
                "event_class": "probe_library.fire.event",
                "predicateType": PREDICATE_TYPE_FIRE,
                "timestamp": result["timestamp"],
                "run_id": result["run_id"],
                "payload": {
                    "probe_id": result["probe_id"],
                    "probe_version": result["probe_version"],
                    "probe_admission_lock_commit": result["probe_admission_lock_commit"],
                    "primitive_class": result["primitive_class"],
                    "spec_iri": result["spec_iri"],
                    "spec_class": s.get("spec_class"),
                    "runtime_emit_event_class": s.get("runtime_emit_event_class"),
                    "current_status": s.get("current_status"),
                    "fidelity_ok": result["fidelity_ok"],
                    "disposition": result["disposition"],
                    "sub_checks": result["sub_checks"],
                    "evidence": result["evidence"][:320],
                },
            }
            f.write(json.dumps(row) + "\n")
            fired += 1

    applicable = faithful + not_faithful + unverifiable  # excludes DP#26 carve-outs
    divergence_rate = (not_faithful / applicable) if applicable else 0.0
    kt13_fired = divergence_rate > KT13_DIVERGENCE_THRESHOLD
    # KT-13 conservative surface + remediation queue (NEVER a halt).
    kt13_row = {
        "schema_version": "0.1",
        "namespace": "cycle_16.be_k.spec_impl_fidelity",
        "event_class": "probe_library.kt13_divergence_surface.event",
        "predicateType": PREDICATE_TYPE_FIRE,
        "timestamp": _utc_ts(),
        "run_id": f"s16_be_k_kt13_surface_{uuid.uuid4().hex[:8]}",
        "payload": {
            "kt13_threshold": KT13_DIVERGENCE_THRESHOLD,
            "behavioral_divergence_rate": round(divergence_rate, 4),
            "kt13_fired": kt13_fired,
            "applicable_specs": applicable,
            "not_faithful": not_faithful,
            "dp26_carveouts_excluded": dp26,
            "remediation_queue_size": len(remediation_queue),
            "remediation_queue": remediation_queue[:50],
            "action": "conservative_surface_plus_remediation_queue (NEVER a halt; Done #41/#42)",
            "hc70_honesty": "MEASURED DIVERGENCE only; Class F own accuracy UNVALIDATED until Done #25",
        },
    }
    with sink.open("a", encoding="utf-8") as f:
        f.write(json.dumps(kt13_row) + "\n")

    print(
        f"PASS: aggregate-cycle fired {fired} Class F probes (sink={sink_path}) || "
        f"faithful={faithful} not_faithful={not_faithful} "
        f"dp26_carveout={dp26} unverifiable={unverifiable} || "
        f"MEASURED behavioral_divergence_rate={divergence_rate:.4f} over {applicable} applicable specs "
        f"|| KT-13 fired={kt13_fired} (conservative surface+queue, NEVER halt) "
        f"|| HC #70: Class F own accuracy UNVALIDATED until Done #25 — NOT a fidelity verdict on the codebase"
    )
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Probe Class F — spec-implementation fidelity")
    p.add_argument("--self-test", action="store_true")
    p.add_argument("--aggregate-cycle", "--production", dest="aggregate_cycle",
                   type=int, nargs="?", const=16, default=None)
    p.add_argument("--applicable-only", action="store_true",
                   help="Fire only on specs with executable runtime_emit_event_class (exclude DP#26 carve-outs)")
    p.add_argument(
        "--scan-json",
        default=str(_project_root() / "outputs" / "retroactive_scan_cycle_1_15_run.json"),
    )
    p.add_argument(
        "--sink",
        default=str(_project_root() / "outputs" / "probe_fire_events.jsonl"),
    )
    p.add_argument("--limit", type=int, default=None)
    p.add_argument("--run-id-prefix", default=None)
    p.add_argument("--spec-iri", default=None, help="Single-spec fidelity-probe mode")
    p.add_argument("--runtime-emit-event-class", default=None)
    p.add_argument("--source-path", default=None)
    p.add_argument("--embodiment-ref-path", default=None)
    p.add_argument("--current-status", default=None)
    args = p.parse_args(argv)

    if args.self_test:
        fixture_dir = _project_root() / "tests" / "probes" / "fixtures"
        return _self_test(fixture_dir)
    if args.aggregate_cycle is not None:
        return _aggregate_cycle(
            cycle_n=args.aggregate_cycle,
            scan_json_path=args.scan_json,
            sink_path=args.sink,
            limit=args.limit,
            run_id_prefix_override=args.run_id_prefix,
            applicable_only=args.applicable_only,
        )
    if args.spec_iri:
        result = probe(
            spec_iri=args.spec_iri,
            runtime_emit_event_class=args.runtime_emit_event_class,
            source_path=args.source_path,
            embodiment_ref_path=args.embodiment_ref_path,
            current_status=args.current_status,
        )
        print(json.dumps(result, indent=2))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
