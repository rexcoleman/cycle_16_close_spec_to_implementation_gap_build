#!/usr/bin/env python3
"""Faithful-target KG provenance capture — Cycle-16-S26 Build-Runner Step 2.

Past-era RECONSTRUCTION overlay: writes each spec's FAITHFUL committed-observable into
the Fuseki /cycle6 KG (the system-of-record) as a NEW property
  cycle16:faithfulCommittedObservable "<faithful_target>"
plus a prov:wasDerivedFrom edge to the named source artifact (the spec-of-record file),
and a reconstruction-disclosure marker
  cycle16:faithfulTargetReconstruction "past_era_disclosed_confidence" .

RECONSTRUCTION IS THE FALLBACK for already-authored specs (past-era). It is NOT the
forward authoring-time mechanism (#67, S27+). Every node carries the reconstruction
marker so the overlay is never mistaken for authoring-time-captured provenance.

Mechanism: SPARQL INSERT DATA via the EXISTING spec_registry_authoring `_sparql_post`
(NOT a forked client, NOT a hand-edited triple file), mirroring
reconcile_kernel_coach_spec_node.py. Provenance edges land in the provenance named
graph; the faithful-observable property + reconstruction marker land in the assertion
graph. Confirm by SPARQL READ-BACK (assert the edge + target present), never by
asserting success.

Refuse-on-missing-precondition (DP#44): if the faithful target map is absent, or a
spec's faithful_target is a DEFECT (untraceable), REFUSE to write a fabricated target.
DP#26 carve-outs DO get a faithful_target 'n/a' triple (honest n/a is a real faithful
target, not a fabrication).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
OUTPUTS = REPO / "outputs"
sys.path.insert(0, str(HERE))

from spec_registry_authoring import (  # noqa: E402
    _sparql_post,
    _emit,
    SPARQL_UPDATE_ENDPOINT,
    SPARQL_QUERY_ENDPOINT,
    ASSERTION_GRAPH,
    PROVENANCE_GRAPH,
)

MAP_JSON = OUTPUTS / "faithful_target_map.json"
READBACK_OUT = OUTPUTS / "faithful_target_kg_readback.json"

PREFIXES = """PREFIX c6: <http://cycle6.local/ontology#>
PREFIX cycle16: <http://cycle16.local/ontology#>
PREFIX prov: <http://www.w3.org/ns/prov#>
"""

RECONSTRUCTION_MARKER = "past_era_disclosed_confidence"


def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _short(spec_iri: str) -> str:
    # spec ids are already cycle16:spec_retroactive_<uuid> — usable as a SPARQL prefixed name.
    return spec_iri


def _write_one(member: dict) -> tuple[bool, dict]:
    spec_iri = member["spec_iri"]
    ft = member["faithful_target"]
    src = member.get("prov_wasDerivedFrom")
    if member.get("is_defect") or ft is None:
        return False, {"spec_iri": spec_iri, "skipped": True,
                       "reason": "DP#44 refuse: defect/untraceable — no faithful target to write"}
    src_iri = "file://" + os.path.expanduser(src) if src else None

    prov_clause = ""
    if src_iri:
        prov_clause = f"""  GRAPH <{PROVENANCE_GRAPH}> {{
    {spec_iri} prov:wasDerivedFrom <{src_iri}> .
  }}
"""
    update = f"""{PREFIXES}
INSERT DATA {{
  GRAPH <{ASSERTION_GRAPH}> {{
    {spec_iri} cycle16:faithfulCommittedObservable "{_esc(ft)}" ;
      cycle16:faithfulTargetReconstruction "{RECONSTRUCTION_MARKER}" ;
      cycle16:faithfulTargetExtractionDisposition "{_esc(member['disposition'])}" .
  }}
{prov_clause}}}
"""
    st, ms, _ = _sparql_post(SPARQL_UPDATE_ENDPOINT, update, op="update")
    return st in (200, 204), {"spec_iri": spec_iri, "http_status": st, "ms": ms,
                              "faithful_target": ft, "prov_src": src_iri}


def _readback(spec_iri: str) -> dict:
    """SPARQL READ-BACK: assert the faithful-observable + reconstruction marker (assertion
    graph) and the prov:wasDerivedFrom edge (provenance graph) are present."""
    q_assert = f"""{PREFIXES}
SELECT ?ft ?recon ?disp WHERE {{
  GRAPH <{ASSERTION_GRAPH}> {{
    {spec_iri} cycle16:faithfulCommittedObservable ?ft ;
      cycle16:faithfulTargetReconstruction ?recon ;
      cycle16:faithfulTargetExtractionDisposition ?disp .
  }}
}}"""
    _s1, _m1, b1 = _sparql_post(SPARQL_QUERY_ENDPOINT, q_assert, op="query")
    rows = json.loads(b1)["results"]["bindings"]
    assert_present = bool(rows)
    ft = rows[0]["ft"]["value"] if rows else None
    recon = rows[0]["recon"]["value"] if rows else None

    q_prov = f"""{PREFIXES}
SELECT ?o WHERE {{ GRAPH <{PROVENANCE_GRAPH}> {{ {spec_iri} prov:wasDerivedFrom ?o }} }}"""
    _s2, _m2, b2 = _sparql_post(SPARQL_QUERY_ENDPOINT, q_prov, op="query")
    prov = [r["o"]["value"] for r in json.loads(b2)["results"]["bindings"]]
    return {
        "spec_iri": spec_iri,
        "faithful_observable_present": assert_present,
        "faithful_target_readback": ft,
        "reconstruction_marker_readback": recon,
        "prov_wasDerivedFrom_readback": prov,
        "prov_edge_present": len(prov) > 0,
    }


def run(limit: int | None = None) -> dict:
    if not MAP_JSON.exists():
        raise SystemExit("REFUSE: faithful_target_map.json absent — run faithful_target_extractor.py first (DP#44).")
    m = json.loads(MAP_JSON.read_text())
    members = m["members"]
    if limit:
        members = members[:limit]

    written = skipped = 0
    write_log = []
    for mem in members:
        ok, detail = _write_one(mem)
        if detail.get("skipped"):
            skipped += 1
        elif ok:
            written += 1
        else:
            raise SystemExit(f"REFUSE: SPARQL write failed for {mem['spec_iri']}: {detail} (DP#44 halt).")
        write_log.append(detail)

    # READ-BACK verify a representative + the worked-case af3a918a + every concrete-class spec.
    concrete = [x["spec_iri"] for x in members
                if x["synthesized_runtime_emit_event_class"]
                and not str(x["synthesized_runtime_emit_event_class"]).lower().startswith("n/a")]
    sample_dp26 = next((x["spec_iri"] for x in members if x["disposition"] == "dp26_carveout_preserved"), None)
    to_readback = list(dict.fromkeys(concrete + ([sample_dp26] if sample_dp26 else [])
                                     + ["cycle16:spec_retroactive_af3a918a"]))
    readbacks = [_readback(s) for s in to_readback if any(x["spec_iri"] == s for x in members)]

    # Assert the worked case reads back the FAITHFUL class (not the synthesized one).
    af = next((r for r in readbacks if r["spec_iri"] == "cycle16:spec_retroactive_af3a918a"), None)
    if af is not None:
        assert af["faithful_target_readback"] == "kernel_coach.transition.fire", \
            f"READ-BACK FAIL: af3a918a faithful target = {af['faithful_target_readback']!r} (expected kernel_coach.transition.fire)"
        assert af["faithful_target_readback"] != "kernel_coach.dispatch", "READ-BACK FAIL: af3a918a still on synthesized class"
        assert af["prov_edge_present"], "READ-BACK FAIL: af3a918a missing prov:wasDerivedFrom edge"
        assert af["reconstruction_marker_readback"] == RECONSTRUCTION_MARKER, "READ-BACK FAIL: af3a918a missing reconstruction marker"

    out = {
        "schema_version": "faithful_target_kg_capture.v1",
        "build_event": "Cycle-16-S26 faithful-target KG provenance capture (past-era reconstruction)",
        "reconstruction_marker": RECONSTRUCTION_MARKER,
        "reconstruction_note": (
            "Past-era RECONSTRUCTION overlay (the FALLBACK for already-authored specs). "
            "NOT the forward authoring-time mechanism (#67, S27+). Every node carries "
            f"cycle16:faithfulTargetReconstruction = {RECONSTRUCTION_MARKER!r}."
        ),
        "endpoint": SPARQL_UPDATE_ENDPOINT,
        "assertion_graph": ASSERTION_GRAPH,
        "provenance_graph": PROVENANCE_GRAPH,
        "n_members": len(members),
        "written": written,
        "skipped_defect": skipped,
        "readback_verified": readbacks,
        "worked_case_af3a918a_readback": af,
    }
    READBACK_OUT.write_text(json.dumps(out, indent=1))

    # Emit a spec_registry.write.event recording the reconstruction overlay (via authoring lib).
    _emit(REPO, "cycle_16.s26.faithful_target", "spec_registry.write.event", {
        "reconcile_kind": "faithful_target_reconstruction_overlay",
        "written": written, "skipped_defect": skipped,
        "reconstruction_marker": RECONSTRUCTION_MARKER,
        "worked_case_af3a918a": af["faithful_target_readback"] if af else None,
    })
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Faithful-target KG provenance capture (reconstruction)")
    ap.add_argument("--limit", type=int, default=None)
    args = ap.parse_args()
    out = run(limit=args.limit)
    print(f"KG capture: written={out['written']} skipped_defect={out['skipped_defect']} of n={out['n_members']}")
    af = out["worked_case_af3a918a_readback"]
    if af:
        print(f"  af3a918a READ-BACK: faithful={af['faithful_target_readback']!r} "
              f"prov_edge={af['prov_edge_present']} recon={af['reconstruction_marker_readback']!r}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
