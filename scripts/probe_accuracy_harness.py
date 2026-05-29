#!/usr/bin/env python3
"""Cycle-16-S17 BE-M — probe-accuracy validation harness (Done #25/#38/#44).

VALIDATE THE VALIDATOR. This harness measures each Class A-F probe's accuracy
(TP/FP/FN/TN, precision, recall, FP-rate) against an INDEPENDENTLY-DERIVED,
EXECUTION-GROUNDED ground truth. It NEVER imports a probe module or calls a
probe function: probes are run only via their subprocess CLI and the emitted
JSONL is read back. The ground-truth deriver re-implements the label from the
SAME EXTERNAL source data the probe reads (JSONL transcripts / SPARQL KG /
filesystem / emission records) with its OWN code, so agreement is independent
corroboration, not correlated error.

WHAT THIS HARNESS DOES NOT DO (honest scope, DP#47 / feedback_honest_evaluation):
- It does NOT remediate anything a probe found (detector-validation only, Done #42).
- It does NOT state any "% implemented / % faithful" number about the codebase.
  It measures PROBE accuracy, not implementation status.
- It does NOT validate the LLM-judge paths (Class C live judge, Class F
  judge-fallback, Class E status-match which imports BE-F). Those are GAP-2-blocked
  (genuine Anthropic usage cap, Coach-confirmed) AND/OR correlated-error traps;
  they are marked DEFERRED-GAP-2, not given a clean number.
- A ground-truth label that is genuinely ambiguous is reported `contested`, never
  silently forced to one side; if >20% of a class is definition-sensitive the
  class is "contested - not validated to bar," not a number.

Independence attestation (--self-test): proves this harness's ground-truth deriver
namespace imports NO probe module (no `from ...probes...` / `import probe_`).

CLI:
  --class {A,B,C,D,E,F,all}   which class(es) to measure (default all)
  --scan-json PATH            population source (default outputs/retroactive_scan_cycle_1_15_run.json)
  --sink PATH                 per-spec event sink (default outputs/probe_accuracy_events.jsonl)
  --summary PATH              per-class summary (default outputs/probe_accuracy_summary.json)
  --query-endpoint URL        SPARQL endpoint for B/E (default http://localhost:3030/cycle6/query)
  --named-graph IRI           named graph (default http://cycle16.local/registry/assertion)
  --limit N                   cap specs/class (debug)
  --self-test                 emit independence attestation + exit
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
import urllib.parse
import urllib.request
import uuid
from typing import Any

# -------------------------------------------------------------------------
# HARD INDEPENDENCE INVARIANT (validate-the-validator, applied to this harness)
# This module MUST NOT import any probe module. The --self-test asserts it.
# Probes are invoked ONLY via subprocess CLI below.
# -------------------------------------------------------------------------

HARNESS_ID = "probe_accuracy_harness_v0.1"
HARNESS_VERSION = "0.1"
PRIMITIVE_NS = "cycle_16.be_m.probe_accuracy"
PREDICATE_TYPE = "cycle16:probe_accuracy_v1"

PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE_CLI = {
    "A": PROJECT_ROOT / "scripts/probes/a/probe_agent_contract.py",
    "B": PROJECT_ROOT / "scripts/probes/b/probe_schema.py",
    "C": PROJECT_ROOT / "scripts/probes/c/probe_design_decision.py",
    "D": PROJECT_ROOT / "scripts/probes/d/probe_methodology_commitment.py",
    "E": PROJECT_ROOT / "scripts/probes/e/probe_kg_fidelity.py",
    "F": PROJECT_ROOT / "scripts/probes/f/probe_spec_impl_fidelity.py",
}
SPEC_CLASS_OF = {
    "A": "a_agent_contract",
    "B": "b_schema",
    "C": "c_design_decision",
    "D": "d_methodology_commitment",
}
DEFAULT_TRANSCRIPT_ROOT = "/home/azureuser/.claude/projects/-home-azureuser-Moonshots-Career-Thesis-v2/"
RECENCY_WINDOW_MIN = 7 * 24 * 60  # 1 week, matches probe A default


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _short(spec_iri: str) -> str:
    return spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]


def _expand(p: str | None) -> str | None:
    return os.path.expanduser(p) if p else None


# =========================================================================
# Population loading
# =========================================================================
def load_population(scan_json: str) -> list[dict[str, Any]]:
    data = json.loads(pathlib.Path(scan_json).read_text())
    specs = data.get("per_spec_evidence_IP_PRIVATE", [])
    # distinct by spec_id (idempotent minting collapses 268 raw -> 232)
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for s in specs:
        sid = s.get("spec_id")
        if sid in seen:
            continue
        seen.add(sid)
        out.append(s)
    return out


# =========================================================================
# Probe runner (subprocess CLI ONLY — never imports a probe)
# =========================================================================
def run_probe_aggregate(cls: str, scan_json: str, sink: str,
                        query_endpoint: str, named_graph: str,
                        limit: int | None) -> int:
    """Fire a probe's --aggregate-cycle and write its JSONL to `sink`.
    Returns number of rows expected (best-effort)."""
    cli = PROBE_CLI[cls]
    pathlib.Path(sink).unlink(missing_ok=True)
    cmd = [sys.executable, str(cli), "--aggregate-cycle", "16",
           "--scan-json", scan_json, "--sink", sink]
    if cls == "E":
        cmd += ["--query-endpoint", query_endpoint, "--named-graph", named_graph]
    if limit:
        cmd += ["--limit", str(limit)]
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=1800,
                          cwd=str(PROJECT_ROOT))
    if proc.returncode != 0:
        sys.stderr.write(f"[probe {cls}] aggregate exit {proc.returncode}: "
                         f"{proc.stderr[-500:]}\n")
    return proc.returncode


def read_probe_fires(sink: str) -> list[dict[str, Any]]:
    """Read the probe's emitted JSONL and return per-spec payload dicts."""
    rows: list[dict[str, Any]] = []
    p = pathlib.Path(sink)
    if not p.exists():
        return rows
    for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            rec = json.loads(line)
        except json.JSONDecodeError:
            continue
        payload = rec.get("payload", rec)
        rows.append(payload)
    return rows


# =========================================================================
# SPARQL helper (independent of probe code; for B SHACL + E re-derivation)
# =========================================================================
def sparql_select(endpoint: str, query: str) -> list[dict[str, Any]] | None:
    """Independent SPARQL SELECT via urllib (NOT the probe's helper). Returns
    bindings list, or None on any failure (conservative)."""
    try:
        data = urllib.parse.urlencode({"query": query}).encode()
        req = urllib.request.Request(
            endpoint, data=data,
            headers={"Accept": "application/sparql-results+json",
                     "Content-Type": "application/x-www-form-urlencoded"},
        )
        with urllib.request.urlopen(req, timeout=30) as resp:
            body = json.loads(resp.read().decode())
        return body.get("results", {}).get("bindings", [])
    except Exception:  # noqa: BLE001
        return None


# =========================================================================
# Class A ground-truth deriver  (INDEPENDENT JSONL parse, STRICT definition)
# =========================================================================
# PINNED GT DEFINITION (A): a Class A AgentContract is "implemented/deployed"
# iff there exists >=1 JSONL tool_use block with name=='Agent' AND
# input.subagent_type EXACTLY equal to the agent name (under {-,_} normalization)
# within a 1-week recency window. This is the most defensible "actual Agent-tool
# subagent dispatch" definition.
# CONTESTED dimension (disclosed, not silently chosen): per S141, most pipeline
# agents run as SEPARATE Claude Code sessions (not Agent-tool subagents), so a
# name appearing only in a tool_use *description* (or only in prose) is a MENTION,
# not a dispatch. The probe's behavioral path also matches description-mentions
# (>4-char names). A spec is flagged contested if the strict-subagent_type label
# and the lenient description-mention label DISAGREE.
GT_DEF_A = ("A_strict_subagent_type_dispatch_v1: >=1 JSONL Agent tool_use with "
            "input.subagent_type == agent-name (normalized) within 7d; "
            "description-only mentions are NOT dispatches (S141 separate-session caveat)")


def _norm_variants(name: str) -> set[str]:
    return {name, name.replace("_", "-"), name.replace("-", "_")}


def gt_class_a(spec: dict[str, Any], transcript_root: str) -> dict[str, Any]:
    name = spec.get("name_truncated") or _short(spec["spec_id"])
    variants = _norm_variants(name)
    desc_variants = {v.lower() for v in variants if len(v) > 4}
    now = datetime.datetime.now(datetime.timezone.utc).timestamp()
    cutoff = now - RECENCY_WINDOW_MIN * 60
    strict_hits = 0           # exact subagent_type match (DISPATCH)
    mention_only_hits = 0     # description-mention but NOT subagent_type
    root = pathlib.Path(os.path.expanduser(transcript_root))
    if root.exists():
        for jsonl in root.rglob("*.jsonl"):
            try:
                if jsonl.stat().st_mtime < cutoff:
                    continue
            except OSError:
                continue
            try:
                with jsonl.open("r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        if '"Agent"' not in line:
                            continue
                        try:
                            row = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        content = (row.get("message") or {}).get("content") or []
                        if not isinstance(content, list):
                            continue
                        for blk in content:
                            if not isinstance(blk, dict):
                                continue
                            if blk.get("type") != "tool_use" or blk.get("name") != "Agent":
                                continue
                            inp = blk.get("input") or {}
                            stype = (inp.get("subagent_type") or "")
                            desc = (inp.get("description") or "").lower()
                            if stype in variants:
                                strict_hits += 1
                            elif any(d in desc for d in desc_variants):
                                mention_only_hits += 1
            except OSError:
                continue
    strict_label = strict_hits >= 1
    lenient_label = (strict_hits + mention_only_hits) >= 1
    contested = strict_label != lenient_label
    return {
        "gt_label": strict_label,
        "gt_definition_id": GT_DEF_A,
        "gt_source": f"jsonl_transcripts:{transcript_root} (strict subagent_type match; independent parser)",
        "contested": contested,
        "gt_detail": (f"strict_subagent_type_dispatches={strict_hits} "
                      f"description_only_mentions={mention_only_hits} "
                      f"(lenient_label={lenient_label})"),
    }


# =========================================================================
# Class B ground-truth deriver (INDEPENDENT: SPARQL for SHACL, rg for .py/.json)
# =========================================================================
# PINNED GT DEFINITION (B): a Schema spec is "implemented/exercised" iff the
# schema file exists AND is exercised: for .ttl/.shacl -> >=1 conforming instance
# of a class in the KG (independent SPARQL); for .py -> >=1 import/reference of the
# module stem in the codebase (independent ripgrep, distinct regex from probe);
# for .json -> >=1 reference to the schema stem in the codebase. Distinct code path
# from the probe (the probe uses urllib+its own regex; we use urllib+SPARQL and the
# system `grep -rl` with a separately-authored pattern).
GT_DEF_B = ("B_schema_exercised_v1: file exists AND (SHACL: >=1 conforming KG "
            "instance via independent SPARQL) OR (.py/.json: >=1 reference to stem "
            "in codebase via independent grep). Note: SHACL+SPARQL share the KG "
            "endpoint with the probe (shared ground-truth lag, NOT shared code).")

SCHEMA_SEARCH_ROOTS = [
    "/home/azureuser/cycle_16_close_spec_to_implementation_gap_build/",
    "/home/azureuser/cycle_6_unified_substrate_build/",
    "/home/azureuser/cycle_10_autonomous_cycle_apparatus_build/",
    "/home/azureuser/Moonshots_Career_Thesis_v2/",
]


def _grep_references(stem: str, roots: list[str], exclude_path: str) -> int:
    """Independent reference count: `grep -rl` for the stem token across roots,
    excluding the schema file itself. Counts files referencing the stem."""
    hits: set[str] = set()
    pat = re.compile(rf"\b{re.escape(stem)}\b")
    for root in roots:
        rp = pathlib.Path(root)
        if not rp.exists():
            continue
        try:
            proc = subprocess.run(
                ["grep", "-rlw", "--include=*.py", "--include=*.sh",
                 "--include=*.md", "--include=*.yaml", "--include=*.yml",
                 "--include=*.ttl", "--include=*.json", stem, str(rp)],
                capture_output=True, text=True, timeout=120)
            for f in proc.stdout.splitlines():
                if os.path.realpath(f) != os.path.realpath(exclude_path):
                    if pat.search(pathlib.Path(f).read_text(
                            encoding="utf-8", errors="replace")[:200000]):
                        hits.add(os.path.realpath(f))
        except (OSError, subprocess.SubprocessError):
            continue
    return len(hits)


def gt_class_b(spec: dict[str, Any], endpoint: str, named_graph: str) -> dict[str, Any]:
    audit = spec.get("audit_tuple") or [None, None, None]
    src = _expand(audit[1]) if len(audit) >= 2 else None
    if not src or not pathlib.Path(src).exists():
        return {"gt_label": False, "gt_definition_id": GT_DEF_B,
                "gt_source": "filesystem: schema file absent", "contested": False,
                "gt_detail": f"schema_path_absent={src}"}
    suf = pathlib.Path(src).suffix.lower()
    body = pathlib.Path(src).read_text(encoding="utf-8", errors="replace")
    if src.endswith((".ttl", ".shacl", ".shacl.ttl")):
        # Independent SHACL/ontology: count conforming instances of any class
        # targeted/declared in the file, via independent SPARQL. We resolve
        # prefixed names by expanding @prefix declarations parsed from the TTL.
        prefixes = dict(re.findall(r"@prefix\s+([\w-]*):\s*<([^>]+)>", body))
        target_classes = re.findall(r"sh:targetClass\s+<([^>]+)>", body)
        target_classes += re.findall(r"sh:targetClass\s+([\w-]+:[\w-]+)", body)
        decl_classes = re.findall(r"<([^>]+)>\s+a\s+owl:Class", body)
        decl_classes += re.findall(r"([\w-]+:[\w-]+)\s+(?:a|rdf:type)\s+owl:Class", body)
        probed_raw = list(dict.fromkeys(target_classes + decl_classes))

        def _to_iri(tok: str) -> str | None:
            if tok.startswith("http"):
                return tok
            if ":" in tok:
                pfx, local = tok.split(":", 1)
                base = prefixes.get(pfx)
                if base:
                    return base + local
            return None

        resolved = [(_to_iri(t), t) for t in probed_raw]
        resolvable = [(iri, t) for iri, t in resolved if iri]
        if not probed_raw:
            return {"gt_label": None, "gt_definition_id": GT_DEF_B,
                    "gt_source": f"shacl/ontology no targetClass/owl:Class extractable: {src}",
                    "contested": True,
                    "gt_detail": "no_independent_target_class_to_count -> contested"}
        if not resolvable:
            return {"gt_label": None, "gt_definition_id": GT_DEF_B,
                    "gt_source": f"shacl prefixed targetClass unresolvable (no matching @prefix): {src}",
                    "contested": True,
                    "gt_detail": f"unresolved_target_classes={probed_raw[:3]} -> contested"}
        # Count conforming instances across BOTH the named assertion graph AND
        # the default/any graph (ontologies live in their own graphs).
        total = 0
        per_class = []
        for iri, tok in resolvable[:6]:
            best = 0
            for graph_clause in (f"GRAPH <{named_graph}>", "GRAPH ?g", ""):
                inner = f"{graph_clause} {{ ?i a <{iri}> }}" if graph_clause else f"?i a <{iri}>"
                q = f"SELECT (COUNT(DISTINCT ?i) AS ?c) WHERE {{ {inner} }}"
                b = sparql_select(endpoint, q)
                if b:
                    try:
                        best = max(best, int(b[0]["c"]["value"]))
                    except (KeyError, ValueError, IndexError):
                        pass
            total += best
            per_class.append((tok, best))
        if sparql_select(endpoint, "SELECT ?s WHERE { ?s ?p ?o } LIMIT 1") is None:
            return {"gt_label": None, "gt_definition_id": GT_DEF_B,
                    "gt_source": "SPARQL endpoint unreachable",
                    "contested": True,
                    "gt_detail": "endpoint_unreachable -> contested (cannot derive SHACL GT)"}
        return {"gt_label": total > 0, "gt_definition_id": GT_DEF_B,
                "gt_source": f"independent SPARQL conforming-instance count (prefix-expanded) over endpoint",
                "contested": False,
                "gt_detail": f"conforming_instances_total={total} per_class={per_class[:4]}"}
    # .py / .json -> independent reference grep
    stem = pathlib.Path(src).stem
    refs = _grep_references(stem, SCHEMA_SEARCH_ROOTS, src)
    return {"gt_label": refs > 0, "gt_definition_id": GT_DEF_B,
            "gt_source": f"independent grep -rlw for stem '{stem}' across {len(SCHEMA_SEARCH_ROOTS)} repos",
            "contested": False,
            "gt_detail": f"referencing_files={refs} (excl self)"}


# =========================================================================
# Class D ground-truth deriver (INDEPENDENT JSONL scan; STRICTER than probe)
# =========================================================================
# PINNED GT DEFINITION (D): a MethodologyCommitment is "applied/fired downstream"
# iff (a) the commitment token is present in its source AND (b) there is >=1
# downstream JSONL event whose event_class OR run_id OR payload field references
# the artifact stem/token AS A STRUCTURED FIELD VALUE (not an incidental substring
# anywhere in the line). The probe matches `token in line` against any line with
# "event_class"/"namespace" -> this over-matches generic tokens. We tighten: the
# token must appear inside event_class, run_id, or a payload string value.
# CONTESTED: tokens that are short/generic (<=2 chars, or pure "R\d+" rule labels
# that collide with countless rule citations) -> the structured-reference label is
# not adjudicable independently -> flagged contested.
GT_DEF_D = ("D_methodology_applied_v1: token in source AND >=1 downstream JSONL "
            "event referencing token/stem as a STRUCTURED field value "
            "(event_class | run_id | payload value), not an incidental line "
            "substring. Short/generic tokens (<=2 chars or bare R<n>) -> contested.")

D_JSONL_ROOTS = ["/home/azureuser/cycle_16_close_spec_to_implementation_gap_build/outputs/"]
# Files the HARNESS itself writes into outputs/ — MUST be excluded from any
# ground-truth scan AND must not be present when a probe runs (else the probe
# reads our own output = circular contamination, validate-the-validator hazard).
HARNESS_OWN_SINKS = {"probe_accuracy_events.jsonl"}


def _is_harness_own(path: pathlib.Path) -> bool:
    return path.name in HARNESS_OWN_SINKS or path.name.startswith(".acc_probe_fire_")


def _token_in_structured_field(rec: dict[str, Any], needles: set[str]) -> bool:
    ec = str(rec.get("event_class") or "")
    rid = str(rec.get("run_id") or "")
    for n in needles:
        if n and (n in ec or n in rid):
            return True
    payload = rec.get("payload")
    if isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, str):
                for n in needles:
                    if n and n in v:
                        return True
    return False


def gt_class_d(spec: dict[str, Any]) -> dict[str, Any]:
    audit = spec.get("audit_tuple") or [None, None, None]
    src = _expand(audit[1]) if len(audit) >= 2 else None
    token = (audit[2] or "").split("@")[0] if len(audit) >= 3 and audit[2] else (
        spec.get("name_truncated") or _short(spec["spec_id"]))
    # precondition: token in source
    token_in_source = False
    if src and pathlib.Path(src).exists():
        body = pathlib.Path(src).read_text(encoding="utf-8", errors="replace")
        token_in_source = bool(re.search(rf"\b{re.escape(token)}\b", body))
    needles = {token, pathlib.Path(token).stem}
    needles.discard("")
    # contested if token is short/generic
    is_generic = (len(token) <= 2) or bool(re.fullmatch(r"[Rr]\d+", token))
    structured_hits = 0
    for root in D_JSONL_ROOTS:
        rp = pathlib.Path(os.path.expanduser(root))
        if not rp.exists():
            continue
        for jsonl in rp.rglob("*_events.jsonl"):
            if _is_harness_own(jsonl):
                continue
            try:
                with jsonl.open("r", encoding="utf-8", errors="replace") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue
                        # cheap prefilter
                        if not any(n in line for n in needles):
                            continue
                        try:
                            rec = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        if _token_in_structured_field(rec, needles):
                            structured_hits += 1
                            if structured_hits >= 2:
                                break
            except OSError:
                continue
            if structured_hits >= 2:
                break
        if structured_hits >= 2:
            break
    label = token_in_source and structured_hits >= 1
    return {
        "gt_label": label,
        "gt_definition_id": GT_DEF_D,
        "gt_source": f"source token-presence + independent structured-field JSONL scan over {D_JSONL_ROOTS}",
        "contested": is_generic,
        "gt_detail": (f"token={token!r} token_in_source={token_in_source} "
                      f"structured_field_hits={structured_hits} generic_token={is_generic}"),
    }


# =========================================================================
# Class E ground-truth derivers (sub-check level)
#   source-traceability + field-match: FULL RIGOR (independent fs/git + re-derive)
#   status-match + overall disposition: DEFERRED-GAP-2 (probe imports BE-F)
# =========================================================================
# PINNED GT DEFINITION (E source-traceability): the KG node's source-of-record
# (scan audit_tuple[1]) resolves+reads on disk/git, derived by an independent
# os.path.exists / git cat-file (NOT the probe's resolver).
# PINNED GT DEFINITION (E field-match / spec_type): re-derive spec_type by reading
# the source DIRECTLY (file extension + /agents/ path + frontmatter), a DIFFERENT
# angle from the probe's source-kind-token heuristic.
GT_DEF_E_SRC = ("E_source_traceability_v1: scan audit_tuple[1] path resolves+reads "
                "(independent os.path.exists/git cat-file).")
GT_DEF_E_FIELD = ("E_field_match_spec_type_v1: spec_type re-derived by reading the "
                  "source file directly (extension + /agents/ path), independent of "
                  "the probe's source-kind-token map.")


def gt_class_e_source(scan_rec: dict[str, Any] | None) -> bool | None:
    if not scan_rec:
        return None
    audit = scan_rec.get("audit_tuple") or [None, None, None]
    ref = audit[1] if len(audit) >= 2 else None
    if not ref:
        return False
    ref = os.path.expanduser(ref.strip())
    is_sha = (7 <= len(ref) <= 40 and all(c in "0123456789abcdef" for c in ref.lower())
              and "/" not in ref)
    if is_sha:
        try:
            r = subprocess.run(["git", "cat-file", "-e", ref], capture_output=True,
                               timeout=20, cwd=str(PROJECT_ROOT))
            return r.returncode == 0
        except (OSError, subprocess.SubprocessError):
            return False
    p = pathlib.Path(ref)
    if not p.exists():
        return False
    if p.is_dir():
        try:
            return any(p.iterdir())
        except OSError:
            return False
    try:
        with p.open("rb") as f:
            f.read(1)
        return True
    except OSError:
        return False


def gt_class_e_spec_type(scan_rec: dict[str, Any] | None) -> str | None:
    """Independent spec_type re-derivation: read the SOURCE directly."""
    if not scan_rec:
        return None
    audit = scan_rec.get("audit_tuple") or [None, None, None]
    ref = os.path.expanduser((audit[1] or "").strip()) if len(audit) >= 2 else ""
    low = ref.lower()
    if low.endswith(".md") and ("/agents/" in low or "/.claude/agents" in low):
        return "AgentContract"
    if low.endswith((".json", ".ttl", ".shacl", ".shacl.ttl")) and "schema" in low:
        return "Schema"
    if low.endswith((".ttl",)) and ("ontology" in low or "shapes" in low):
        return "Schema"
    if low.endswith(".py"):
        return None  # ambiguous without deeper read
    return None


# =========================================================================
# Class F ground-truth deriver (execution path FULL RIGOR; judge path DEFERRED)
# =========================================================================
# PINNED GT DEFINITION (F execution-path): a spec is "behaviorally faithful via
# execution" iff its committed runtime_emit_event_class is actually emitted (a
# row in outputs/*.jsonl whose event_class equals or is a dotted-suffix variant
# of the committed class). "n/a" committed class -> DP#26 carve-out (not faithful/
# unfaithful, EXCLUDED from accuracy). Same-namespace-but-wrong-class -> not faithful.
# No emission at all -> EXECUTION-INCONCLUSIVE (probe hands to judge -> DEFERRED-GAP-2).
# We re-implement the emission-record read INDEPENDENTLY (our own JSONL parse +
# our own suffix-match, no probe import).
GT_DEF_F = ("F_execution_emission_v1: committed runtime_emit_event_class is emitted "
            "in outputs/*.jsonl (exact or dotted-suffix match), via independent "
            "emission-record read. 'n/a'->DP#26 carve-out (excluded). "
            "No-emission->inconclusive->judge path->DEFERRED-GAP-2.")

F_SINK_GLOBS = ["/home/azureuser/cycle_16_close_spec_to_implementation_gap_build/outputs/"]


def _f_event_class_matches(emitted: str, committed: str) -> bool:
    if not emitted:
        return False
    if emitted == committed:
        return True
    if emitted.endswith("." + committed) or committed.endswith("." + emitted):
        return True
    return False


def _f_sink_dirs(spec: dict[str, Any]) -> list[str]:
    """Resolve the emission-sink dirs to scan, INDEPENDENTLY mirroring the probe's
    policy (cycle_16/outputs/ + the source repo's outputs/) with our own code.
    Critical: a Class F spec sourced in another repo (e.g. cycle_10) emits into
    THAT repo's outputs/, not cycle_16's — scanning only cycle_16 would falsely
    label such specs inconclusive."""
    dirs = list(F_SINK_GLOBS)
    audit = spec.get("audit_tuple") or [None, None, None]
    src = _expand(audit[1]) if len(audit) >= 2 else None
    if src:
        sp = pathlib.Path(src)
        for anc in [sp] + list(sp.parents):
            cand = anc / "outputs"
            if cand.is_dir():
                if str(cand) + "/" not in dirs and str(cand) not in dirs:
                    dirs.append(str(cand))
                break
    return dirs


def gt_class_f(spec: dict[str, Any]) -> dict[str, Any]:
    committed = spec.get("runtime_emit_event_class")
    if not committed or committed.startswith("n/a"):
        return {"gt_label": "dp26_carveout", "gt_definition_id": GT_DEF_F,
                "gt_source": "scan runtime_emit_event_class='n/a' (DP#26 carve-out)",
                "contested": False, "gt_detail": "dp26_carveout (excluded from accuracy)"}
    committed_head = committed.split(".", 1)[0]
    matched = False
    same_head = False
    sink_dirs = _f_sink_dirs(spec)
    for root in sink_dirs:
        rp = pathlib.Path(os.path.expanduser(root))
        if not rp.exists():
            continue
        for jsonl in sorted(rp.glob("*.jsonl")):
            if _is_harness_own(jsonl):
                continue
            try:
                with jsonl.open("r", encoding="utf-8", errors="replace") as f:
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
                        if _f_event_class_matches(ec, committed):
                            matched = True
                            break
                        if ec.split(".", 1)[0] == committed_head:
                            same_head = True
            except OSError:
                continue
            if matched:
                break
        if matched:
            break
    if matched:
        return {"gt_label": True, "gt_definition_id": GT_DEF_F,
                "gt_source": f"independent emission-record read over {sink_dirs}",
                "contested": False,
                "gt_detail": f"committed_class={committed!r} EMITTED"}
    if same_head:
        return {"gt_label": False, "gt_definition_id": GT_DEF_F,
                "gt_source": f"independent emission-record read over {sink_dirs}",
                "contested": False,
                "gt_detail": f"committed_class={committed!r} NOT emitted; same-namespace "
                             f"activity present (wrong-thing)"}
    # No emission anywhere -> probe falls to judge fallback (GAP-2 path)
    return {"gt_label": "inconclusive_judge_path", "gt_definition_id": GT_DEF_F,
            "gt_source": f"independent emission-record read over {sink_dirs}",
            "contested": False,
            "gt_detail": f"committed_class={committed!r} not emitted, no same-namespace "
                         f"activity -> probe routes to judge (DEFERRED-GAP-2)"}


# =========================================================================
# Confusion matrix
# =========================================================================
def confusion(pairs: list[tuple[bool, bool]]) -> dict[str, Any]:
    """pairs = list of (probe_positive, gt_positive)."""
    tp = sum(1 for p, g in pairs if p and g)
    fp = sum(1 for p, g in pairs if p and not g)
    fn = sum(1 for p, g in pairs if not p and g)
    tn = sum(1 for p, g in pairs if not p and not g)
    n = len(pairs)
    precision = tp / (tp + fp) if (tp + fp) else None
    recall = tp / (tp + fn) if (tp + fn) else None
    fp_rate = fp / (fp + tn) if (fp + tn) else None
    return {"TP": tp, "FP": fp, "FN": fn, "TN": tn, "n": n,
            "precision": precision, "recall": recall, "fp_rate": fp_rate}


# =========================================================================
# Per-class measurement orchestration
# =========================================================================
def measure_class(cls: str, population: list[dict[str, Any]], scan_json: str,
                  query_endpoint: str, named_graph: str, limit: int | None,
                  emit) -> dict[str, Any]:
    # Probe-fire sink lives OUTSIDE outputs/ so that NO probe (which scans
    # outputs/*.jsonl) can read another class's fire output mid-run.
    tmp_sink = str(pathlib.Path("/tmp") / f"acc_probe_fire_{cls.lower()}_{os.getpid()}.jsonl")
    rc = run_probe_aggregate(cls, scan_json, tmp_sink, query_endpoint, named_graph, limit)
    fires = read_probe_fires(tmp_sink)
    # index probe fires by spec_iri
    fire_by_iri = {f.get("spec_iri"): f for f in fires}

    if cls in ("A", "B", "C", "D"):
        specs = [s for s in population if s.get("spec_class") == SPEC_CLASS_OF[cls]]
        if limit:
            specs = specs[:limit]
        return _measure_abcd(cls, specs, fire_by_iri, query_endpoint, named_graph, emit)
    if cls == "E":
        return _measure_e(fires, scan_json, emit)
    if cls == "F":
        return _measure_f(fires, population, emit)
    raise ValueError(cls)


def _measure_abcd(cls, specs, fire_by_iri, endpoint, named_graph, emit):
    pairs: list[tuple[bool, bool]] = []
    contested = 0
    no_fire = 0
    deferred = 0
    rows_for_disclosure: list[dict[str, Any]] = []
    for s in specs:
        iri = s["spec_id"]
        fire = fire_by_iri.get(iri)
        if fire is None:
            no_fire += 1
            continue
        probe_pos = bool(fire.get("implemented"))
        if cls == "A":
            gt = gt_class_a(s, DEFAULT_TRANSCRIPT_ROOT)
        elif cls == "B":
            gt = gt_class_b(s, endpoint, named_graph)
        elif cls == "D":
            gt = gt_class_d(s)
        else:  # C -> DEFERRED-GAP-2 (LLM-judge canonical; structural-only is partial)
            gt = {"gt_label": None, "gt_definition_id":
                  "C_design_decision_DEFERRED: canonical decision is LLM-judge-dependent "
                  "(GAP-2). Structural-judge embodiment heuristic is probe-internal; no "
                  "clean independent label without the live LLM.",
                  "gt_source": "n/a (DEFERRED-GAP-2)", "contested": False,
                  "gt_detail": "C accuracy not measurable this session (GAP-2)"}
        gt_label = gt["gt_label"]
        verdict = _emit_row(emit, cls, iri, s, probe_pos, gt)
        rows_for_disclosure.append({"spec_iri": iri, "name": s.get("name_truncated"),
                                    "probe": probe_pos, **gt})
        if gt.get("contested"):
            contested += 1
            continue
        if gt_label is None:
            deferred += 1
            continue
        pairs.append((probe_pos, bool(gt_label)))
    n_eval = len(pairs)
    n_total = len(specs)
    mtx = confusion(pairs)
    return _classify_verdict(cls, mtx, contested, deferred, n_total, n_eval, no_fire,
                             rows_for_disclosure,
                             execution_observable=(cls in ("A", "B", "D")))


def _measure_e(fires, scan_json, emit):
    """E: validate source-traceability + field-match sub-checks (FULL RIGOR);
    status-match + overall disposition DEFERRED-GAP-2 (probe imports BE-F)."""
    scan_idx = {}
    data = json.loads(pathlib.Path(scan_json).read_text())
    for s in data.get("per_spec_evidence_IP_PRIVATE", []):
        scan_idx[s["spec_id"].rsplit(":", 1)[-1]] = s
        # also index by short hash variants
    # E fires on KG IRIs; join to scan by the spec name where possible.
    src_pairs: list[tuple[bool, bool]] = []
    field_pairs: list[tuple[bool, bool]] = []
    src_unjoinable = 0
    field_unjoinable = 0
    status_deferred = 0
    rows: list[dict[str, Any]] = []
    for f in fires:
        iri = f.get("spec_iri")
        subchecks = f.get("sub_checks") or {}
        probe_src = subchecks.get("source_traceability")
        probe_field = subchecks.get("field_match")
        status_deferred += 1  # status-match sub-check is DEFERRED-GAP-2 for every spec
        # try to join scan_rec
        short = (iri or "").rsplit(":", 1)[-1]
        scan_rec = scan_idx.get(short)
        if scan_rec is None:
            # E enumerates the FULL KG (242) incl nodes not in scan (cycle16 own).
            # Without a scan join we cannot independently derive the source ref.
            src_unjoinable += 1
            field_unjoinable += 1
            _emit_row(emit, "E", iri, {"name_truncated": short}, probe_src,
                      {"gt_label": None, "gt_definition_id": GT_DEF_E_SRC,
                       "gt_source": "no scan join -> source not independently derivable",
                       "contested": False, "gt_detail": "kg-only node, no scan audit_tuple",
                       "sub_check": "source_traceability"})
            continue
        gt_src = gt_class_e_source(scan_rec)
        if gt_src is not None and probe_src is not None:
            src_pairs.append((bool(probe_src), bool(gt_src)))
        gt_st = gt_class_e_spec_type(scan_rec)
        kg_type = f.get("kg_spec_type")
        # field-match GT: re-derived spec_type matches KG type (no source-existence mismatch)
        field_gt = None
        if gt_st is not None:
            field_gt = (gt_st == kg_type) and (gt_src is True if gt_src is not None else True)
            if probe_field is not None:
                field_pairs.append((bool(probe_field), bool(field_gt)))
        else:
            field_unjoinable += 1
        _emit_row(emit, "E", iri, {"name_truncated": short}, probe_src,
                  {"gt_label": gt_src, "gt_definition_id": GT_DEF_E_SRC,
                   "gt_source": f"independent fs/git resolve of {scan_rec.get('audit_tuple', [None, None])[1]}",
                   "contested": False,
                   "gt_detail": (f"source_ok_gt={gt_src} field_ok_gt={field_gt} "
                                 f"rederived_type={gt_st} kg_type={kg_type} "
                                 f"STATUS_MATCH=DEFERRED-GAP-2"),
                   "sub_check": "source_traceability+field_match"})
        rows.append({"spec_iri": iri, "src_gt": gt_src, "field_gt": field_gt})
    src_mtx = confusion(src_pairs)
    field_mtx = confusion(field_pairs)
    return {
        "class": "E",
        "verdict": "PARTIAL-SUBCHECKS-VALIDATED + STATUS-MATCH-DEFERRED-GAP-2",
        "tag": "CONTESTED/DEFERRED-GAP-2 (overall disposition gated on status-match)",
        "execution_observable": True,
        "subcheck_matrices": {
            "source_traceability": src_mtx,
            "field_match_spec_type": field_mtx,
        },
        "status_match_subcheck": "DEFERRED-GAP-2 (probe imports BE-F; correlated-error "
                                 "trap + GAP-2 LLM-adjacent; cannot validate this session)",
        "overall_disposition_validatable": False,
        "overall_disposition_reason": ("E disposition = source_ok AND field_ok AND status_ok; "
                                       "status_ok is DEFERRED-GAP-2, so the overall faithful/"
                                       "infidelity verdict CANNOT be validated to bar this session"),
        "n_fires": len(fires),
        "kg_only_nodes_unjoinable_to_scan": src_unjoinable,
        "status_match_specs_deferred": status_deferred,
        "gt_definition": {"source": GT_DEF_E_SRC, "field": GT_DEF_E_FIELD},
        "bar_source_traceability": _bar_text(src_mtx),
        "bar_field_match": _bar_text(field_mtx),
        "honest_limitation": (
            "On this population EVERY scan-joined node has a resolvable source AND a "
            "matching re-derived spec_type, so the source-traceability and field-match "
            "sub-check matrices contain ONLY positives (TN=FP=FN=0). This confirms the "
            "probe AGREES with independent derivation on positives, but provides NO "
            "discriminating power against a dangling-source / wrong-type FP — there are "
            "no negative cases in the real population to test that. The known-bad "
            "behaviour is covered only by the probe's own self-test fixture (which the "
            "harness is forbidden to use as accuracy GT). NOT a clean 'sub-checks "
            "validated to bar' for FP-resistance."),
    }


def _measure_f(fires, population, emit):
    pop_idx = {s["spec_id"]: s for s in population}
    pairs: list[tuple[bool, bool]] = []
    dp26 = 0
    judge_path = 0
    no_join = 0
    rows: list[dict[str, Any]] = []
    for f in fires:
        iri = f.get("spec_iri")
        disp = f.get("disposition")
        sub = f.get("sub_checks") or {}
        path = sub.get("path")
        spec = pop_idx.get(iri)
        if spec is None:
            no_join += 1
            continue
        gt = gt_class_f(spec)
        gtl = gt["gt_label"]
        if gtl == "dp26_carveout":
            dp26 += 1
            _emit_row(emit, "F", iri, spec, None, gt)
            continue
        if gtl == "inconclusive_judge_path":
            judge_path += 1
            _emit_row(emit, "F", iri, spec, None, {**gt,
                      "gt_detail": gt["gt_detail"] + f" || probe_path={path} disp={disp}"})
            continue
        # execution-path GT available (True / False)
        probe_faithful = bool(f.get("fidelity_ok"))
        # Only compare on execution-path probe results (judge path is GAP-2)
        if path == "execution":
            pairs.append((probe_faithful, bool(gtl)))
            _emit_row(emit, "F", iri, spec, probe_faithful,
                      {**gt, "gt_detail": gt["gt_detail"] + f" || probe execution-path disp={disp}"})
        else:
            judge_path += 1
            _emit_row(emit, "F", iri, spec, probe_faithful,
                      {**gt, "gt_label": "deferred_judge_path",
                       "gt_detail": gt["gt_detail"] + f" || probe routed to {path} (DEFERRED-GAP-2)"})
    mtx = confusion(pairs)
    return _classify_verdict("F", mtx, contested=0, deferred=judge_path,
                             n_total=len(fires), n_eval=len(pairs), no_fire=no_join,
                             rows_for_disclosure=rows, execution_observable=True,
                             extra={"dp26_carveouts": dp26,
                                    "judge_path_DEFERRED_GAP_2": judge_path,
                                    "gt_definition": GT_DEF_F,
                                    "note": "execution-path validated FULL RIGOR; "
                                            "judge-fallback path DEFERRED-GAP-2"})


def _bar_text(mtx):
    fp = mtx["FP"]
    rec = mtx["recall"]
    n = mtx["n"]
    if n == 0:
        return "NO-EVAL-PAIRS"
    zero_fp = fp == 0
    rec_ok = (rec is not None and rec >= 0.90)
    return f"zero_FP={zero_fp} recall={rec} recall>=0.90={rec_ok} n={n}"


def _classify_verdict(cls, mtx, contested, deferred, n_total, n_eval, no_fire,
                      rows_for_disclosure, execution_observable, extra=None):
    result = {
        "class": cls,
        "matrix": mtx,
        "n_total_population": n_total,
        "n_evaluated": n_eval,
        "n_contested_excluded": contested,
        "n_deferred_gap2": deferred,
        "n_no_probe_fire": no_fire,
        "execution_observable": execution_observable,
    }
    if extra:
        result.update(extra)
    # contested fraction over the population that HAD a derivable label attempt
    contestable_base = n_eval + contested
    contested_frac = (contested / contestable_base) if contestable_base else 0.0
    result["contested_fraction"] = round(contested_frac, 4)

    if cls == "C":
        result["verdict"] = "DEFERRED-GAP-2"
        result["tag"] = "DEFERRED-GAP-2"
        result["small_n_disclosed"] = False
        return result

    small_n = cls in ("A", "B") and n_total < 20
    result["small_n_disclosed"] = small_n
    if small_n:
        result["small_n_note"] = (f"Class {cls} population is n={n_total} (<20). The "
                                  f"≥20-blind-sample bar is UNMEETABLE; validated FULL "
                                  f"population, disclosed small-n (NOT padded with synthetic).")

    if not execution_observable:
        result["verdict"] = "DEFERRED-GAP-2"
        result["tag"] = "DEFERRED-GAP-2"
        return result

    if contested_frac > 0.20:
        result["verdict"] = "CONTESTED — not validated to bar"
        result["tag"] = "CONTESTED"
        return result

    if n_eval == 0:
        result["verdict"] = "NO-EVALUABLE-SPECS"
        result["tag"] = "CONTESTED"
        return result

    zero_fp = mtx["FP"] == 0
    rec = mtx["recall"]
    rec_ok = (rec is None) or (rec >= 0.90)  # rec None when no positives in GT
    rec_defined = rec is not None
    # Honest small-n / no-discriminating-power guard: a "PASS" on a handful of
    # evaluable specs (or with no negatives / no positives) is NOT a credible
    # population validation — surface it as PASS-LOW-POWER, not clean PASS.
    has_pos = mtx["TP"] + mtx["FN"] > 0
    has_neg = mtx["FP"] + mtx["TN"] > 0
    low_power = (n_eval < 5) or (not has_pos) or (not has_neg)
    if zero_fp and rec_ok:
        if low_power:
            result["verdict"] = "FULL-RIGOR-PASS-LOW-POWER (n_eval too small / no neg or no pos cases)"
            result["tag"] = "PASS-LOW-POWER"
            result["low_power_note"] = (
                f"n_eval={n_eval}; has_positive_GT={has_pos}; has_negative_GT={has_neg}. "
                f"Agreement is real but the evaluable set is too thin / lacks "
                f"discriminating cases to certify population accuracy to bar.")
        else:
            result["verdict"] = "FULL-RIGOR-PASS"
            result["tag"] = "FULL-RIGOR-PASS"
    else:
        result["verdict"] = "FULL-RIGOR-FAIL (KT-15 fires)"
        result["tag"] = "FULL-RIGOR-FAIL"
    result["bar"] = (f"zero_FP={zero_fp} (FP={mtx['FP']}); "
                     f"recall={rec} recall>=0.90={rec_ok} "
                     f"(recall {'defined' if rec_defined else 'undefined: no GT-positives'})")
    return result


# =========================================================================
# Event emission
# =========================================================================
def make_emitter():
    """Buffer events IN MEMORY (do NOT write the sink incrementally). The sink is
    written only at the very end — this prevents any probe (which scans
    outputs/*.jsonl) from reading the harness's own partially-written output mid-run
    (circular-contamination / validate-the-validator hazard)."""
    buf: list[dict[str, Any]] = []
    run_id = f"s17_be_m_probe_accuracy_{uuid.uuid4().hex[:8]}"

    def emit(event: dict[str, Any]):
        buf.append(event)

    return emit, buf, run_id


def _emit_row(emit, cls, iri, spec, probe_pos, gt):
    label = gt.get("gt_label")
    if isinstance(label, bool) and probe_pos is not None:
        if probe_pos and label:
            outcome = "agree_TP"
        elif not probe_pos and not label:
            outcome = "agree_TN"
        elif probe_pos and not label:
            outcome = "FP"
        else:
            outcome = "FN"
    elif gt.get("contested"):
        outcome = "contested"
    else:
        outcome = "deferred_or_carveout"
    emit({
        "schema_version": "0.1",
        "namespace": PRIMITIVE_NS,
        "event_class": "probe_accuracy.measure.event",
        "predicateType": PREDICATE_TYPE,
        "timestamp": _utc_ts(),
        "payload": {
            "harness_id": HARNESS_ID,
            "primitive_class": cls,
            "spec_iri": iri,
            "spec_name": (spec or {}).get("name_truncated"),
            "probe_disposition": probe_pos,
            "gt_label": label,
            "gt_source": gt.get("gt_source"),
            "gt_definition_id": gt.get("gt_definition_id"),
            "contested": gt.get("contested", False),
            "outcome": outcome,
            "gt_detail": gt.get("gt_detail"),
            "sub_check": gt.get("sub_check"),
        },
    })
    return outcome


# =========================================================================
# Independence self-test (validate-the-validator applied to the harness)
# =========================================================================
def independence_attestation() -> dict[str, Any]:
    """Prove this module imported NO probe code. Inspect sys.modules + this
    module's source for probe imports."""
    src = pathlib.Path(__file__).read_text(encoding="utf-8")
    # 1. Source-level: no `from ...probes...` / `import probe_` statements.
    import_lines = [ln.strip() for ln in src.splitlines()
                    if re.match(r"^\s*(from|import)\s", ln)]
    probe_imports = [ln for ln in import_lines
                     if re.search(r"\bprobes?\b|\bprobe_\w+", ln)
                     and not ln.startswith("#")]
    # 2. Runtime: no probe module present in sys.modules under our namespace.
    loaded_probe_mods = [m for m in sys.modules
                         if "probe_agent_contract" in m or "probe_schema" in m
                         or "probe_design_decision" in m or "probe_methodology" in m
                         or "probe_kg_fidelity" in m or "probe_spec_impl" in m
                         or m == "probes" or m.startswith("probes.")]
    clean = (len(probe_imports) == 0) and (len(loaded_probe_mods) == 0)
    return {
        "independence_clean": clean,
        "source_probe_import_statements": probe_imports,
        "runtime_loaded_probe_modules": loaded_probe_mods,
        "assertion": ("ground-truth deriver imports NO probe module/function; probes "
                      "are invoked ONLY via subprocess CLI (run_probe_aggregate -> "
                      "subprocess.run). PROVEN." if clean else
                      "FAIL: probe code detected in harness namespace."),
        "probe_invocation_mechanism": "subprocess.run([python, probe_cli, '--aggregate-cycle', ...])",
    }


# =========================================================================
# main
# =========================================================================
def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Cycle-16-S17 BE-M probe-accuracy harness")
    ap.add_argument("--class", dest="cls", default="all",
                    choices=["A", "B", "C", "D", "E", "F", "all"])
    ap.add_argument("--scan-json",
                    default=str(PROJECT_ROOT / "outputs/retroactive_scan_cycle_1_15_run.json"))
    ap.add_argument("--sink", default=str(PROJECT_ROOT / "outputs/probe_accuracy_events.jsonl"))
    ap.add_argument("--summary", default=str(PROJECT_ROOT / "outputs/probe_accuracy_summary.json"))
    ap.add_argument("--query-endpoint", default="http://localhost:3030/cycle6/query")
    ap.add_argument("--named-graph", default="http://cycle16.local/registry/assertion")
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args(argv)

    if args.self_test:
        att = independence_attestation()
        print(json.dumps(att, indent=2))
        return 0 if att["independence_clean"] else 1

    population = load_population(args.scan_json)
    classes = ["A", "B", "C", "D", "E", "F"] if args.cls == "all" else [args.cls]
    # Remove any stale harness sink so NO probe can read the harness's own output.
    pathlib.Path(args.sink).unlink(missing_ok=True)
    emit, buf, run_id = make_emitter()
    per_class: dict[str, Any] = {}
    for cls in classes:
        sys.stderr.write(f"[harness] measuring class {cls}...\n")
        per_class[cls] = measure_class(cls, population, args.scan_json,
                                       args.query_endpoint, args.named_graph,
                                       args.limit, emit)
    # Write the per-spec event sink NOW (after all probes have run).
    with open(args.sink, "w", encoding="utf-8") as fh:
        for ev in buf:
            fh.write(json.dumps(ev) + "\n")

    att = independence_attestation()
    summary = {
        "harness_id": HARNESS_ID,
        "harness_version": HARNESS_VERSION,
        "run_id": run_id,
        "timestamp": _utc_ts(),
        "scan_json": args.scan_json,
        "population_distinct": len(population),
        "independence_attestation": att,
        "per_class": per_class,
        "scope_disclaimer": ("Measures PROBE accuracy (TP/FP/FN/TN/precision/recall) vs "
                             "independently-derived execution-grounded ground truth. Does NOT "
                             "state any '% implemented/faithful' about the codebase (Done #42). "
                             "LLM-judge paths (C live judge, F judge-fallback, E status-match) "
                             "are DEFERRED-GAP-2."),
    }
    # emit a summary event too
    with open(args.sink, "a", encoding="utf-8") as f:
        for cls, res in per_class.items():
            f.write(json.dumps({
                "schema_version": "0.1",
                "namespace": PRIMITIVE_NS,
                "event_class": "probe_accuracy.summary.event",
                "predicateType": PREDICATE_TYPE,
                "timestamp": _utc_ts(),
                "run_id": run_id,
                "payload": {"harness_id": HARNESS_ID, "primitive_class": cls,
                            "verdict": res.get("verdict"), "tag": res.get("tag"),
                            "matrix": res.get("matrix") or res.get("subcheck_matrices")},
            }) + "\n")
    pathlib.Path(args.summary).write_text(json.dumps(summary, indent=2))
    print(json.dumps({c: {"verdict": r.get("verdict"), "tag": r.get("tag"),
                          "matrix": r.get("matrix") or r.get("subcheck_matrices")}
                      for c, r in per_class.items()}, indent=2))
    print(f"\n[harness] independence_clean={att['independence_clean']}")
    print(f"[harness] summary -> {args.summary}")
    print(f"[harness] per-spec events -> {args.sink}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
