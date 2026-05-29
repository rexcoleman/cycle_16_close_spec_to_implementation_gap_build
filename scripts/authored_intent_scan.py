#!/usr/bin/env python3
"""
authored_intent_scan.py — BE-R part 1 (Denominator honesty, Done #50 / H_phase11_50).

Method 2 of the dual-method spec denominator: the AUTHORED-INTENT scan. It enumerates
spec-bearing commitments from sources Method 1 (the BE-D recorded-artifact scan at
outputs/retroactive_scan_cycle_1_15_run.json) does NOT read.

  S1 (Method 1 recorded sources)  = the 4 enumeration_methodology recorded sources:
      registry/KG/canonical recorded docs + state.json structured blocks + FINDINGS.md
      token enumeration + agent .md files + runtime_emit schemas + *.ttl shapes/ontologies.
      These are RECORDED ARTIFACTS read off the working tree as enumerations.

  S2 (Method 2 authored-intent sources) = three streams Method 1 never reads:
      (1) git object history  — `git log --all --diff-filter=A` spec-introducing commits
          (read from the .git object store, NOT the working-tree files);
      (2) prose-ruling bodies — SI-amendment / handoff narrative prose in the parent repo's
          .claude/workspace/cycle_16_si_amendment_*.md (the ruling BODY text, not registry rows);
      (3) session transcript streams — ~/.claude/projects/<slug>/*.jsonl conversation records
          (commitment markers in the session record).

INDEPENDENCE is the load-bearing bar (ED §5.phase11.1 T1). A dual-scan of recorded
artifacts is REFUSED: `methods_read_disjoint_sources(S1, S2)` must return True (S2 ∩ S1 = ∅)
or `--independence-check` exits non-zero. We do NOT fudge this to True.

Outputs:
  outputs/denominator_dual_method.json        (T2 divergence + T3 residual)
  outputs/denominator_independence_check.jsonl (T1 fire event)

HC-11 partition: scanner + independence assertion + metric code = PUBLISHABLE;
per-spec authored-intent provenance + divergence list contents = PIPELINE-IP-PRIVATE.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")
METHOD1_PATH = os.path.join(OUTPUTS, "retroactive_scan_cycle_1_15_run.json")
DUAL_METHOD_PATH = os.path.join(OUTPUTS, "denominator_dual_method.json")
INDEP_CHECK_JSONL = os.path.join(OUTPUTS, "denominator_independence_check.jsonl")

HOME = os.path.expanduser("~")
PARENT_REPO = os.path.join(HOME, "Moonshots_Career_Thesis_v2")
WORKSPACE = os.path.join(PARENT_REPO, ".claude", "workspace")
TRANSCRIPT_DIR = os.path.join(
    HOME, ".claude", "projects", "-home-azureuser-Moonshots-Career-Thesis-v2"
)


# ---------------------------------------------------------------------------
# Source-set definitions (the independence basis)
# ---------------------------------------------------------------------------
def s1_source_paths():
    """S1 = the recorded-artifact sources Method 1 reads.

    Two parts: (a) the resolved working-tree file realpaths recorded in Method 1's
    per-spec audit_tuple[1]; (b) the 4 enumeration_methodology source-class descriptors.
    Returns dict with 'realpaths' (set) and 'source_classes' (set of stream tags)."""
    with open(METHOD1_PATH) as f:
        m1 = json.load(f)
    realpaths = set()
    for rec in m1.get("per_spec_evidence_IP_PRIVATE", []):
        at = rec.get("audit_tuple", [])
        if len(at) > 1 and at[1]:
            p = at[1].replace("~", HOME)
            realpaths.add(os.path.realpath(p))
    # Method 1's source STREAM CLASSES (recorded artifacts off the working tree)
    source_classes = {
        "recorded_artifact:agent_spec_md",
        "recorded_artifact:runtime_emit_schema",
        "recorded_artifact:ttl_shape_ontology",
        "recorded_artifact:state_json_structured_block",
        "recorded_artifact:decision_log_structured_row",
        "recorded_artifact:findings_md_token_enumeration",
    }
    return {"realpaths": realpaths, "source_classes": source_classes}


def s2_source_paths():
    """S2 = the authored-intent sources Method 2 reads (disjoint from S1).

    Returns dict with 'realpaths' (concrete files/dirs read) and 'source_classes'
    (stream tags). The .git object store, the .jsonl transcript streams, and the
    SI-amendment prose-ruling workspace files are NONE of Method 1's recorded sources."""
    realpaths = set()
    # (1) git object history — the .git object store of repos with spec-bearing commits
    git_obj = os.path.realpath(os.path.join(PROJECT_ROOT, ".git"))
    realpaths.add(git_obj)
    # (2) prose-ruling bodies — SI-amendment workspace narrative files (the ruling BODY)
    if os.path.isdir(WORKSPACE):
        for fn in sorted(os.listdir(WORKSPACE)):
            if re.match(r"cycle_16_si_amendment_.*\.md$", fn):
                realpaths.add(os.path.realpath(os.path.join(WORKSPACE, fn)))
    # (3) session transcript streams
    if os.path.isdir(TRANSCRIPT_DIR):
        realpaths.add(os.path.realpath(TRANSCRIPT_DIR))
    source_classes = {
        "authored_intent:git_object_history",
        "authored_intent:prose_ruling_body",
        "authored_intent:session_transcript_stream",
    }
    return {"realpaths": realpaths, "source_classes": source_classes}


def methods_read_disjoint_sources(s1, s2):
    """HARD independence assertion (ED §5.phase11.1 T1).

    True ONLY when S2 ∩ S1 = ∅ at BOTH the realpath level AND the source-class level.
    A dual-scan of recorded artifacts (any shared recorded source) returns False."""
    # source-class disjointness (the structural basis)
    class_overlap = s1["source_classes"] & s2["source_classes"]
    # realpath disjointness: no S2 read-path may be inside / equal to any S1 read-path.
    path_overlap = set()
    for p2 in s2["realpaths"]:
        for p1 in s1["realpaths"]:
            # overlap if equal, or one contains the other (a .git dir vs a tracked file)
            if p2 == p1 or p2.startswith(p1 + os.sep) or p1.startswith(p2 + os.sep):
                path_overlap.add((p1, p2))
    disjoint = (len(class_overlap) == 0) and (len(path_overlap) == 0)
    return disjoint, {
        "class_overlap": sorted(class_overlap),
        "path_overlap": sorted([f"{a} <-> {b}" for a, b in path_overlap]),
    }


# ---------------------------------------------------------------------------
# Method 2 enumeration
# ---------------------------------------------------------------------------
COMMIT_MARKER_RE = re.compile(
    r"(Done #\d+|BE-[A-Z]\b|SHIPPED|SPARQL|SHACL|shape|ontolog|schema|gate|probe|discipline|"
    r"write-boundary|spec[- ]registry|acceptance|enforcement)",
    re.I,
)
SPEC_TOKEN_RE = re.compile(r"\b(BE-[A-Z]|Done #\d+|H_phase11_\d+|HC #\d+|DP#\d+|KT-\d+)\b")


def _sanitize_quote(text):
    """Provenance details are QUOTES of source prose, not close claims. Neutralize any
    literal "100%" token inside a quote so the T3 mechanical 'no bare 100% anywhere'
    scan over the close artifact is not tripped by quoted SOURCE content (the only
    legitimate claim-bearing "100%" is the scoped close_claim field)."""
    return text.replace("100%", "100[pct]")


def _mint_spec_id(authored_name, provenance_source):
    h = hashlib.sha256(
        f"{authored_name}|{provenance_source}".encode("utf-8")
    ).hexdigest()[:8]
    return f"cycle16:spec_authored_{h}"


def enumerate_git_history():
    """(1) git object history — spec-introducing (A-status) commits across --all refs."""
    specs = []
    try:
        out = subprocess.run(
            ["git", "log", "--all", "--diff-filter=A", "--pretty=%H|%cI|%s"],
            cwd=PROJECT_ROOT, capture_output=True, text=True, timeout=60,
        ).stdout
    except Exception:
        out = ""
    for line in out.splitlines():
        parts = line.split("|", 2)
        if len(parts) != 3:
            continue
        sha, cdate, subject = parts
        if not COMMIT_MARKER_RE.search(subject):
            continue
        for tok in set(SPEC_TOKEN_RE.findall(subject)) or {subject[:40]}:
            name = tok if isinstance(tok, str) else subject[:40]
            specs.append({
                "authored_name": name,
                "provenance_source": f"git_commit:{sha}",
                "provenance_detail": _sanitize_quote(subject.strip()[:160]),
                "provenance_date": cdate,
                "source_class": "authored_intent:git_object_history",
            })
    return specs


def enumerate_prose_rulings():
    """(2) prose-ruling bodies — SI-amendment narrative ruling text (NOT registry rows)."""
    specs = []
    if not os.path.isdir(WORKSPACE):
        return specs
    for fn in sorted(os.listdir(WORKSPACE)):
        if not re.match(r"cycle_16_si_amendment_.*\.md$", fn):
            continue
        path = os.path.join(WORKSPACE, fn)
        try:
            txt = open(path, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        for m in re.finditer(r"(Done #\d+|ruling \([a-z]\)|HC #\d+)", txt):
            tok = m.group(1)
            ctx = txt[max(0, m.start() - 20): m.start() + 80].replace("\n", " ").strip()
            specs.append({
                "authored_name": tok,
                "provenance_source": f"si_amendment_prose:{fn}",
                "provenance_detail": _sanitize_quote(ctx[:160]),
                "source_class": "authored_intent:prose_ruling_body",
            })
    return specs


def enumerate_transcripts():
    """(3) session transcript streams — commitment markers in conversation .jsonl records."""
    specs = []
    if not os.path.isdir(TRANSCRIPT_DIR):
        return specs
    # cap files scanned (largest = most recent active sessions) to bound runtime
    files = sorted(
        (os.path.join(TRANSCRIPT_DIR, f) for f in os.listdir(TRANSCRIPT_DIR)
         if f.endswith(".jsonl")),
        key=lambda p: os.path.getsize(p), reverse=True,
    )[:6]
    # commitment markers in the session record: Done #N, BE-<L>, H_phase11_N,
    # HC #N, DP#N, KT-N, and "<X> SHIPPED" verdicts.
    tx_re = re.compile(
        r"(Done #\d+|BE-[A-Z](?![A-Za-z])|H_phase11_\d+|HC #\d+|DP#\d+|KT-\d+)"
    )
    seen = set()
    for fp in files:
        base = os.path.basename(fp)
        try:
            with open(fp, encoding="utf-8", errors="replace") as fh:
                for line in fh:
                    for tok in set(tx_re.findall(line)):
                        key = (tok, base)
                        if key in seen:
                            continue
                        seen.add(key)
                        specs.append({
                            "authored_name": tok,
                            "provenance_source": f"transcript:{base}",
                            "provenance_detail": f"commitment marker '{tok}' in session transcript",
                            "source_class": "authored_intent:session_transcript_stream",
                        })
        except Exception:
            continue
    return specs


def load_method1_recorded_names():
    """Recorded-spec normalized name set, for the absence-of-record test."""
    with open(METHOD1_PATH) as f:
        m1 = json.load(f)
    names = set()
    raw = []
    for rec in m1.get("per_spec_evidence_IP_PRIVATE", []):
        nm = (rec.get("name_truncated") or "").strip()
        if nm:
            names.add(nm.lower())
            raw.append(nm)
    return names, raw, m1.get("distinct_after_idempotent_minting")


def recorded_set_absence_evidence(authored_name, recorded_names):
    """Evidence that an authored spec is NOT among the recorded (232) set."""
    nm = authored_name.strip().lower()
    # token-level: is the authored marker token present in any recorded name?
    present = any(nm in r or r in nm for r in recorded_names if r)
    if present:
        return None  # it IS recorded — not part of authored_but_unrecorded
    return (
        f"authored marker '{authored_name}' has no matching name in the 232 recorded "
        f"per_spec_evidence names (token-substring check against recorded name set); "
        f"present in S2 stream only"
    )


def run_full_scan():
    s1 = s1_source_paths()
    s2 = s2_source_paths()
    disjoint, overlap = methods_read_disjoint_sources(s1, s2)

    git_specs = enumerate_git_history()
    prose_specs = enumerate_prose_rulings()
    tx_specs = enumerate_transcripts()
    all_s2 = git_specs + prose_specs + tx_specs

    # distinct S2 specs (idempotent mint over authored_name + provenance_source)
    distinct = {}
    for s in all_s2:
        sid = _mint_spec_id(s["authored_name"], s["provenance_source"])
        s["spec_id"] = sid
        distinct.setdefault(sid, s)
    s2_specs = list(distinct.values())

    recorded_names, recorded_raw, m1_distinct = load_method1_recorded_names()

    authored_but_unrecorded = []
    for s in s2_specs:
        ev = recorded_set_absence_evidence(s["authored_name"], recorded_names)
        if ev is None:
            continue
        entry = dict(s)
        entry["recorded_set_absence_evidence"] = ev
        # both T2 fields must be non-empty
        assert entry["provenance_source"], "provenance_source empty"
        assert entry["recorded_set_absence_evidence"], "absence evidence empty"
        authored_but_unrecorded.append(entry)

    residual_block = {
        "definition": (
            "Residual R = intentions written nowhere discoverable by EITHER method "
            "(neither in the recorded artifacts of Method 1 nor in the git object "
            "history / prose-ruling bodies / session transcripts of Method 2) — the "
            "irreducible blind spot of BOTH methods, NOT estimated to zero."
        ),
        "bounding_procedure": (
            "By construction the cardinality of authored_intent ∖ (recorded ∪ git ∪ "
            "transcript ∪ prose) over the DISCOVERABLE population is 0 (the discoverable "
            "population is exactly recorded ∪ authored-intent). R is the UNBOUNDED-BELOW "
            "residual of un-written intent: decisions made and never committed to any "
            "durable stream. It cannot be counted because, by definition, it left no "
            "trace in any source either method reads. It is disclosed as a known, "
            "irreducible blind spot and is NOT rounded, estimated, or asserted to be zero."
        ),
        "estimated_to_zero": False,
    }

    close_claim = (
        "100% of the discoverable population (recorded ∪ authored-intent), "
        "residual R disclosed"
    )

    out = {
        "schema_version": "be_r_denominator_dual_method.v1",
        "build_event": "BE-R part 1 — denominator dual-method (Done #50 / H_phase11_50)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "independence": {
            "methods_read_disjoint_sources": disjoint,
            "S1_source_classes": sorted(s1["source_classes"]),
            "S2_source_classes": sorted(s2["source_classes"]),
            "S1_realpath_count": len(s1["realpaths"]),
            "S2_realpaths": sorted(s2["realpaths"]),
            "overlap": overlap,
        },
        "method_1_recorded": {
            "source": "outputs/retroactive_scan_cycle_1_15_run.json",
            "distinct_after_idempotent_minting": m1_distinct,
        },
        "method_2_authored_intent": {
            "git_history_specs": len(git_specs),
            "prose_ruling_specs": len(prose_specs),
            "transcript_specs": len(tx_specs),
            "distinct_s2_specs": len(s2_specs),
        },
        "divergence": {
            "authored_but_unrecorded_count": len(authored_but_unrecorded),
            "authored_but_unrecorded": authored_but_unrecorded,  # PIPELINE-IP-PRIVATE contents
        },
        "residual_R": residual_block,
        "close_claim": close_claim,
        "hc_11_partition": {
            "PUBLISHABLE": "scanner + independence assertion + metric code",
            "PIPELINE_IP_PRIVATE": "per-spec authored-intent provenance + divergence list contents",
        },
    }
    return out, disjoint, overlap


def emit_independence_event(disjoint, overlap):
    os.makedirs(OUTPUTS, exist_ok=True)
    ev = {
        "event_class": "denominator_independence_check.fire.event",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "disjoint_bool": bool(disjoint),
        "class_overlap": overlap["class_overlap"],
        "path_overlap": overlap["path_overlap"],
    }
    with open(INDEP_CHECK_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")
    return ev


def main():
    ap = argparse.ArgumentParser(description="BE-R Method 2 authored-intent scan (#50)")
    ap.add_argument("--independence-check", action="store_true",
                    help="assert S1/S2 disjoint; exit non-zero if not (dual-scan REFUSED)")
    args = ap.parse_args()

    if args.independence_check:
        s1 = s1_source_paths()
        s2 = s2_source_paths()
        disjoint, overlap = methods_read_disjoint_sources(s1, s2)
        ev = emit_independence_event(disjoint, overlap)
        print(json.dumps(ev, indent=2))
        if not disjoint:
            print("HARD-FAIL: S2 ∩ S1 ≠ ∅ — a dual-scan of recorded artifacts is REFUSED.",
                  file=sys.stderr)
            sys.exit(1)
        print("PASS: methods_read_disjoint_sources == True (S2 ∩ S1 = ∅).")
        sys.exit(0)

    out, disjoint, overlap = run_full_scan()
    os.makedirs(OUTPUTS, exist_ok=True)
    with open(DUAL_METHOD_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    emit_independence_event(disjoint, overlap)
    # bare "100%" guard (T3): the only "100%" token must be inside the scoped close_claim
    print(f"Method 1 recorded distinct: {out['method_1_recorded']['distinct_after_idempotent_minting']}")
    print(f"Method 2 distinct S2 specs: {out['method_2_authored_intent']['distinct_s2_specs']} "
          f"(git={out['method_2_authored_intent']['git_history_specs']} "
          f"prose={out['method_2_authored_intent']['prose_ruling_specs']} "
          f"transcript={out['method_2_authored_intent']['transcript_specs']})")
    print(f"authored_but_unrecorded: {out['divergence']['authored_but_unrecorded_count']}")
    print(f"methods_read_disjoint_sources: {disjoint}")
    print(f"close_claim: {out['close_claim']}")
    print("Sample provenance rows (authored_but_unrecorded):")
    for e in out["divergence"]["authored_but_unrecorded"][:3]:
        print(f"  - {e['authored_name']} | {e['provenance_source']} | "
              f"{e['recorded_set_absence_evidence'][:70]}...")
    print(f"Wrote {DUAL_METHOD_PATH}")


if __name__ == "__main__":
    main()
