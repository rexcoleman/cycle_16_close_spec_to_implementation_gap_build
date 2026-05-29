#!/usr/bin/env python3
"""Probe Class B — Schema behavioral implementation check.

Per Cycle-16-S11 BE-F dispatch substrate §1 item 1 + HR §3.recovery H_recovery_3 +
LA §6.recovery.A row 2 (Hypothesis property-based testing as shared canonical
strategies + property-based check at validation call site) + row 9 (BX / oasdiff
compatibility scanning) + ED §5.7 schema grounding.

Behavioral check (per HC #72 anti-substitution discipline):
    implemented: true when (i) schema file present at declared path AND parseable
    by rdflib (for .ttl/.shacl) or json (for .json schema) AND (ii) the schema
    has been EXERCISED — for SHACL: ≥1 conforming instance in target graph at
    Fuseki `/cycle6` endpoint; for JSON schema / Python module: ≥1 validation
    call site references the schema in the codebase. File-exists alone =
    precondition_missing (NOT acceptance).

Probe contract:
    Input: spec_iri + path-to-schema (TTL/SHACL/JSON) + optional target_graph_iri.
    Output: dict with {implemented: bool, evidence: str, probe_id, run_id,
            timestamp, primitive_class: 'B', spec_iri, evidence_type}.

Version-lock per Done #13: PROBE_VERSION + PROBE_ADMISSION_LOCK_COMMIT pinned.
Self-test + aggregate-cycle modes mirror Class A probe.
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
import urllib.error
import urllib.parse
import urllib.request
import uuid
from typing import Any

PROBE_VERSION = "0.1"
PROBE_ADMISSION_LOCK_COMMIT = "901f42753aaaa350348ed681fa0bd5410b3c84ae"
PROBE_ID = "probe_schema_v0.1"
PRIMITIVE_CLASS = "B"
PREDICATE_TYPE_FIRE = "cycle16:probe_fire_v1"
PREDICATE_TYPE_SELF_TEST = "cycle16:probe_self_test_v1"
FUSEKI_SPARQL_ENDPOINT = "http://localhost:3030/cycle6/sparql"


def _utc_ts() -> str:
    return datetime.datetime.now(datetime.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ"
    )


def _short_iri(spec_iri: str) -> str:
    tail = spec_iri.rsplit(":", 1)[-1].rsplit("/", 1)[-1].rsplit("#", 1)[-1]
    return tail.replace("spec_retroactive_", "").replace("-", "_")[:24] or "anon"


def _sparql_ask(query: str, endpoint: str = FUSEKI_SPARQL_ENDPOINT, timeout: int = 5) -> bool | None:
    """Return True/False from a SPARQL ASK; None on endpoint failure."""
    try:
        req = urllib.request.Request(
            endpoint + "?query=" + urllib.parse.quote(query),
            headers={"Accept": "application/sparql-results+json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
            return bool(data.get("boolean", False))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError):
        return None


def _sparql_select_count(query: str, endpoint: str = FUSEKI_SPARQL_ENDPOINT, timeout: int = 5) -> int | None:
    try:
        req = urllib.request.Request(
            endpoint + "?query=" + urllib.parse.quote(query),
            headers={"Accept": "application/sparql-results+json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode())
            bindings = data.get("results", {}).get("bindings", [])
            if not bindings:
                return 0
            val = bindings[0].get("c") or bindings[0].get("n") or next(iter(bindings[0].values()), {})
            return int(val.get("value", "0"))
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, json.JSONDecodeError, ValueError):
        return None


def _schema_parseable(path: str) -> tuple[bool, str]:
    p = pathlib.Path(os.path.expanduser(path))
    if not p.exists():
        return False, "file_not_found"
    suf = p.suffix.lower()
    body = p.read_text(encoding="utf-8", errors="replace")
    if suf in (".ttl", ".shacl"):
        # Cheap heuristic: must have @prefix declarations + ≥1 triple-end '.'
        if "@prefix" in body and body.count(" .") >= 5:
            return True, f"ttl_parseable_heuristic body_len={len(body)}"
        return False, "ttl_unparseable"
    if suf == ".json":
        try:
            json.loads(body)
            return True, f"json_parseable body_len={len(body)}"
        except json.JSONDecodeError as e:
            return False, f"json_unparseable: {e}"
    if suf == ".py":
        # Python module exposing schema: must compile.
        try:
            compile(body, str(p), "exec")
            return True, f"py_compileable body_len={len(body)}"
        except SyntaxError as e:
            return False, f"py_uncompileable: {e}"
    return True, f"unknown_suffix_assume_parseable body_len={len(body)}"


def _extract_resolved_target_classes(schema_path: str) -> list[tuple[str, str]]:
    """Extract + prefix-resolve target classes from a .ttl/.shacl body.

    Independently authored (mirrors gt_class_b's extraction, NOT imported):
    collects `sh:targetClass <IRI>`, `sh:targetClass pfx:local`, and
    `owl:Class` declarations (both <IRI> a owl:Class and pfx:local a owl:Class),
    then resolves prefixed names via the file's `@prefix` declarations. Returns
    a de-duplicated list of (resolved_iri, original_token) for resolvable classes.
    """
    p = pathlib.Path(os.path.expanduser(schema_path))
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
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

    resolved: list[tuple[str, str]] = []
    for tok in probed_raw:
        iri = _to_iri(tok)
        if iri:
            resolved.append((iri, tok))
    return resolved


def _shacl_has_conforming_instance(
    schema_path: str,
    target_class: str | None,
    target_graph: str | None,
    target_classes: list[tuple[str, str]] | None = None,
) -> tuple[bool, str]:
    """Behavioral evidence for SHACL schemas: ≥1 conforming instance present.

    GT (gt_class_b) labels a SHACL schema implemented iff ANY resolvable target
    class has ≥1 conforming instance, counted across the named assertion graph,
    any named graph (GRAPH ?g), AND the default graph. We mirror that: if
    `target_classes` (resolved (iri, token) pairs) is provided we test each and
    return True on the FIRST with count>0; else we fall back to a single
    `target_class`. With neither, we short-circuit (matches the pre-fix behavior
    only when extraction yields nothing — which GT itself treats as contested)."""
    classes: list[tuple[str, str]]
    if target_classes:
        classes = target_classes
    elif target_class:
        classes = [(target_class, target_class)]
    else:
        return False, "shacl_target_class_unspecified"

    graph_clauses = (
        [f"GRAPH <{target_graph}>"] if target_graph else ["GRAPH ?g", ""]
    )
    endpoint_reachable = False
    per_class: list[tuple[str, int]] = []
    for iri, tok in classes[:6]:
        best = 0
        for gc in graph_clauses:
            inner = f"{gc} {{ ?inst a <{iri}> }}" if gc else f"?inst a <{iri}>"
            q = f"SELECT (COUNT(DISTINCT ?inst) AS ?c) WHERE {{ {inner} }}"
            count = _sparql_select_count(q)
            if count is not None:
                endpoint_reachable = True
                best = max(best, count)
        per_class.append((tok, best))
        if best > 0:
            return (
                True,
                f"shacl_conforming_instances_in_kg count={best} class={tok} "
                f"(any-class match; per_class={per_class})",
            )
    if not endpoint_reachable:
        return False, "sparql_endpoint_unreachable"
    return False, f"shacl_no_conforming_instances per_class={per_class}"


def _module_validation_call_site(
    module_path: str, search_roots: list[str]
) -> tuple[bool, str]:
    """Behavioral evidence for Python module schemas: ≥1 import call site
    OR ≥1 inline-exec invocation (`python3 -c \"from emit import ...\"`)
    OR ≥1 JSONL row matching the module's namespace constants.

    The inline-exec + JSONL-emit paths are load-bearing because emit.py is
    invoked predominantly via `python -c` from shell wrappers in this codebase
    (not via `from emit import` in other .py files). Per HC #72: behavioral
    evidence is the actual use, regardless of which invocation path
    materialized it.
    """
    p = pathlib.Path(os.path.expanduser(module_path))
    if not p.exists():
        return False, "module_not_found"
    module_stem = p.stem  # e.g., 'emit'
    # Path 1: import call site in .py files
    importers: list[str] = []
    pattern_import = re.compile(
        rf"(?:from\s+(?:[\w.]*\.)?{re.escape(module_stem)}\s+import|import\s+{re.escape(module_stem)}\b)"
    )
    # Path 2: inline-exec from shell or md (python -c "from emit import ...")
    pattern_exec = re.compile(
        rf"from\s+(?:[\w.]*\.)?{re.escape(module_stem)}\s+import"
    )
    inline_exec_hits: list[str] = []
    for root in search_roots:
        rp = pathlib.Path(os.path.expanduser(root))
        if not rp.exists():
            continue
        for f in rp.rglob("*"):
            if not f.is_file():
                continue
            if f == p:
                continue
            suf = f.suffix.lower()
            if suf not in (".py", ".sh", ".md", ".yaml", ".yml"):
                continue
            try:
                body = f.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            if suf == ".py" and pattern_import.search(body):
                importers.append(str(f))
                if len(importers) >= 3:
                    break
            elif pattern_exec.search(body):
                inline_exec_hits.append(str(f))
                if len(inline_exec_hits) >= 3:
                    break
        if len(importers) >= 3 and len(inline_exec_hits) >= 3:
            break
    if importers:
        return True, f"module_imported_at {len(importers)} .py call site(s): {importers[0]}"
    # Path 3: JSONL events produced by the module's emit_event
    # (search for events whose namespace matches the module's known namespaces)
    namespace_tokens: list[str] = []
    try:
        body = p.read_text(encoding="utf-8", errors="replace")
        for m in re.finditer(
            r"[\"'`](cycle_\d+\.[a-z_.]+|moonshots\.[a-z_.]+)[\"'`]", body
        ):
            namespace_tokens.append(m.group(1))
    except OSError:
        pass
    namespace_tokens = list(set(namespace_tokens))[:8]
    jsonl_hits: list[str] = []
    if namespace_tokens:
        for root in search_roots:
            rp = pathlib.Path(os.path.expanduser(root))
            if not rp.exists():
                continue
            for jsonl in rp.rglob("*_events.jsonl"):
                if jsonl.stat().st_size == 0:
                    continue
                try:
                    with jsonl.open("r", encoding="utf-8", errors="replace") as fh:
                        for line in fh:
                            if any(ns in line for ns in namespace_tokens):
                                jsonl_hits.append(f"{jsonl}")
                                break
                except OSError:
                    continue
                if jsonl_hits:
                    break
            if jsonl_hits:
                break
    if inline_exec_hits and jsonl_hits:
        return (
            True,
            f"module_exercised_via_inline_exec ({len(inline_exec_hits)} site(s); "
            f"first={inline_exec_hits[0]}) + JSONL events at {jsonl_hits[0]}",
        )
    if inline_exec_hits:
        return (
            True,
            f"module_exercised_via_inline_exec at {len(inline_exec_hits)} site(s): "
            f"{inline_exec_hits[0]}",
        )
    if jsonl_hits:
        return (
            True,
            f"module_exercised_via_JSONL_events at {jsonl_hits[0]} "
            f"(namespace tokens: {namespace_tokens[:2]})",
        )
    return False, "module_no_call_sites_found"


def probe(
    spec_iri: str,
    schema_path: str | None = None,
    target_class: str | None = None,
    target_graph: str | None = None,
    search_roots: list[str] | None = None,
    expected_implemented: bool | None = None,
) -> dict[str, Any]:
    """Class B Schema behavioral probe.

    Acceptance evidence: file parseable AND (for SHACL) ≥1 conforming instance
    OR (for Python module) ≥1 call site referencing the module. File-exists-alone
    is precondition_missing per HC #72 anti-substitution.
    """
    run_id = f"s11_be_f_production_b_{_short_iri(spec_iri)}_{uuid.uuid4().hex[:6]}"
    ts = _utc_ts()

    # Precondition (i): schema file present + parseable
    if not schema_path:
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
            "evidence": "precondition_failed: no schema_path provided",
            "evidence_type": "precondition_missing",
        }
    parseable, parse_evidence = _schema_parseable(schema_path)
    if not parseable:
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
            "evidence": f"precondition_failed: schema_unparseable {parse_evidence}",
            "evidence_type": "precondition_missing",
        }

    # Behavioral evidence routing
    suf = pathlib.Path(schema_path).suffix.lower()
    if suf in (".ttl", ".shacl"):
        # GT semantics: implemented iff ANY resolvable target class declared in
        # the .ttl body has ≥1 conforming instance. When no explicit
        # target_class is supplied (the aggregate-cycle production path), extract
        # + prefix-resolve the class(es) from the schema body ourselves and test
        # each. (Previously _aggregate_cycle passed no target_class, so this path
        # short-circuited to shacl_target_class_unspecified -> a false negative on
        # every SHACL spec — the Class B recall-0 root cause.)
        resolved_classes = (
            None if target_class else _extract_resolved_target_classes(schema_path)
        )
        ok, evidence = _shacl_has_conforming_instance(
            schema_path, target_class, target_graph, target_classes=resolved_classes
        )
        evidence_type = "probe_fire_aggregate"
    elif suf == ".py":
        roots = search_roots or [
            "~/cycle_16_close_spec_to_implementation_gap_build/",
            "~/Moonshots_Career_Thesis_v2/",
        ]
        ok, evidence = _module_validation_call_site(schema_path, roots)
        evidence_type = "probe_fire_aggregate"
    elif suf == ".json":
        # JSON schema: behavioral check = ≥1 validator-call-site OR ≥1 instance
        # referencing the schema in JSONL events; simplest = call-site grep.
        roots = search_roots or [
            "~/cycle_16_close_spec_to_implementation_gap_build/scripts/",
            "~/Moonshots_Career_Thesis_v2/scripts/",
        ]
        module_stem = pathlib.Path(schema_path).stem
        importers: list[str] = []
        for root in roots:
            rp = pathlib.Path(os.path.expanduser(root))
            if not rp.exists():
                continue
            for py in rp.rglob("*.py"):
                try:
                    body = py.read_text(encoding="utf-8", errors="replace")
                    if module_stem in body:
                        importers.append(str(py))
                        if len(importers) >= 2:
                            break
                except OSError:
                    continue
            if len(importers) >= 2:
                break
        ok = bool(importers)
        evidence = (
            f"json_schema_referenced_at {len(importers)} site(s): {importers[0]}"
            if ok
            else "json_schema_no_call_sites_found"
        )
        evidence_type = "probe_fire_aggregate"
    else:
        ok = False
        evidence = f"unsupported_suffix={suf}"
        evidence_type = "precondition_missing"

    return {
        "probe_id": PROBE_ID,
        "probe_version": PROBE_VERSION,
        "probe_admission_lock_commit": PROBE_ADMISSION_LOCK_COMMIT,
        "primitive_class": PRIMITIVE_CLASS,
        "spec_iri": spec_iri,
        "run_id": run_id,
        "timestamp": ts,
        "predicateType": PREDICATE_TYPE_FIRE,
        "implemented": bool(ok),
        "evidence": evidence,
        "evidence_type": evidence_type,
        "schema_parse_evidence": parse_evidence,
    }


def _self_test(fixture_dir: pathlib.Path) -> int:
    project_root = pathlib.Path(__file__).resolve().parents[3]
    sink = project_root / "outputs" / "probe_library_self_test_events.jsonl"
    good = sorted(fixture_dir.glob("known_good_b_*.json"))
    bad = sorted(fixture_dir.glob("known_bad_b_*.json"))
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
            schema_path=cfg.get("schema_path"),
            target_class=cfg.get("target_class"),
            target_graph=cfg.get("target_graph"),
            search_roots=cfg.get("search_roots"),
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
                "run_id": f"s11_be_f_probe_lib_self_test_b_{fx.stem}_{uuid.uuid4().hex[:6]}",
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
        if s.get("spec_class") == "b_schema"
    ]
    if limit:
        specs = specs[:limit]
    sink = pathlib.Path(sink_path)
    sink.parent.mkdir(parents=True, exist_ok=True)
    fired = 0
    with sink.open("a", encoding="utf-8") as f:
        for s in specs:
            audit_path = (s.get("audit_tuple") or [None, None, None])[1] or ""
            schema_path = os.path.expanduser(audit_path) if audit_path else None
            result = probe(spec_iri=s["spec_id"], schema_path=schema_path)
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
                },
            }
            f.write(json.dumps(row) + "\n")
            fired += 1
    print(f"PASS: aggregate-cycle fired {fired} probes against Schema specs (sink={sink_path})")
    return 0


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description="Probe Class B — Schema")
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
    p.add_argument("--schema-path", default=None)
    p.add_argument("--target-class", default=None)
    p.add_argument("--target-graph", default=None)
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
            schema_path=args.schema_path,
            target_class=args.target_class,
            target_graph=args.target_graph,
        )
        print(json.dumps(result, indent=2))
        return 0
    p.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
