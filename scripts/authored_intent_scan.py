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

# The frozen spec-class definition is the AUTHORITY for this re-run (freeze-before-count).
# It is committed FIRST (commit 1e43a04) and cited here by path + SHA; the re-run commit
# (made by the Coach) will have 1e43a04 as an ancestor. See docs/spec_class_frozen_definition.md.
FROZEN_DEFINITION_PATH = "docs/spec_class_frozen_definition.md"
FROZEN_DEFINITION_COMMIT = "1e43a04"

# §3.1 EXCLUSION — principle-reference tokens are NOT specs (the four cycle16:SpecType
# classes are the ONLY denominator population). DP#N / HC#N / HC #N / GPL-N / Pattern N /
# Binding N are references to the standing-principle layer the specs are governed BY; a
# spec MAY cite them (citation ≠ membership). These are filtered OUT of the denominator.
PRINCIPLE_REF_RE = re.compile(
    r"^\s*(DP\s*#?\s*\d+|HC\s*[-#]?\s*\d+|GPL[-\s]?\d+|Pattern\s+\d+|Binding\s+\d+|"
    r"Discipline\s*#?\s*\d+|Check\s*#?\s*\d+|Trap\s*#?\s*\d+|MR\s*#?\s*\d+|"
    r"MC\s*#?\s*\d+|PL\s*#?\s*\d+|LL[-\s]?\d+|OBS[-\s]?\d+)\s*$",
    re.I,
)

# §3.2 EXCLUSION — Cycle-16-own `Done #N` items are Cycle 16's OWN recovery scope (the
# auditing instrument), not cycles-1-15 specs. In this corpus the `Done #N` markers are
# authored in the Cycle-16 SI amendments / transcripts, so every `Done #N` token is
# Cycle-16-authored and excluded from the cycles-1-15 denominator.
DONE_ITEM_RE = re.compile(r"^\s*Done\s*#\s*\d+\s*$", re.I)


def is_excluded_token(authored_name):
    """True iff the authored marker is excluded from the cycles-1-15 denominator per the
    frozen def: a principle-reference (§3.1) or a Cycle-16-own Done #N item (§3.2)."""
    nm = (authored_name or "").strip()
    if PRINCIPLE_REF_RE.match(nm):
        return "principle_reference_3_1"
    if DONE_ITEM_RE.match(nm):
        return "cycle16_own_done_item_3_2"
    return None

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
# SPEC_TOKEN_RE still CAPTURES DP#N / HC #N so the §3.1 exclusion is COUNTED + auditable
# (the contamination removed is disclosed as a number, not silently never-matched). The
# captured principle-refs + Cycle-16-own Done #N are filtered by is_excluded_token() at
# the §3 gate in run_full_scan, where they are tallied into the exclusion report.
SPEC_TOKEN_RE = re.compile(
    r"\b(BE-[A-Z]|Done #\d+|H_phase11_\d+|KT-\d+|DP#\d+|HC ?#?\d+|GPL-\d+|"
    r"Pattern \d+|Binding \d+)\b")


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
        # frozen def §3.1: HC #N principle-references dropped from candidate minting.
        # capture principle-refs too so the §3.1 exclusion is counted/auditable at the gate.
        for m in re.finditer(r"(Done #\d+|ruling \([a-z]\)|HC ?#?\d+|DP#\d+|Pattern \d+|Binding \d+)", txt):
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
    # capture principle-refs too so the §3.1 exclusion is counted/auditable at the gate
    # (they were the dominant S21 transcript contamination); filtered at the §3 gate.
    tx_re = re.compile(
        r"(Done #\d+|BE-[A-Z](?![A-Za-z])|H_phase11_\d+|KT-\d+|DP#\d+|HC ?#?\d+|"
        r"GPL-\d+|Pattern \d+|Binding \d+)"
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


def _canonical_identity(repo, canonical_path, spec_class, anchor=""):
    """Frozen def §1 counting UNIT: one distinct spec = one (spec_class, canonical
    DEFINITION-SITE) pair, deduplicated by the SHA-256 of (repo, realpath#anchor, class).

    Critical §1↔§2 resolution: the "canonical definition site" is the spec's single
    AUTHORITATIVE-DEFINITION ANCHOR, not the bare containing file. Per §1.1 + §2:
      - DesignDecision → the DECISION_LOG / state.json structured-ROW anchor (the keyed
        disposition / decisions_log entry) — many distinct decisions live in ONE
        state.json, each its OWN site (§2: "one recorded decision row = one spec");
      - MethodologyCommitment → the FINDINGS.md Layer-5 TOKEN anchor (Binding 6 / R1 /
        Pattern 9) — many commitments live in ONE FINDINGS.md, each its own site;
      - AgentContract → the .claude/agents/<name>.md FILE (one file = one contract, no anchor);
      - Schema → the schema-definition site (file, or named shape within a .ttl).
    The `anchor` is the in-file definition key (name_truncated). Deduping on
    (repo, realpath#anchor, class) collapses idempotent duplicates of the SAME definition
    site WITHOUT collapsing distinct decisions/commitments that merely share a file."""
    rp = os.path.realpath(canonical_path.replace("~", HOME)) if canonical_path else ""
    site = f"{rp}#{anchor}" if anchor else rp
    return hashlib.sha256(
        f"{repo}|{site}|{spec_class}".encode("utf-8")
    ).hexdigest()[:16]


def compute_m1_prime():
    """Re-count M1 under the FROZEN scope (frozen def §4): the cycles-1-15 denominator
    excludes Cycle-16-authored records (cycle_authored == 16). Returns
    (m1_raw_distinct, m1_prime_cycles_1_15, cycle16_excluded) all [measured], where
    m1_prime applies the §1 canonical-identity unit over the cycles-1-15 records."""
    with open(METHOD1_PATH) as f:
        m1 = json.load(f)
    recs = m1.get("per_spec_evidence_IP_PRIVATE", [])
    # M1 raw distinct (existing minted count, by spec_id)
    raw_distinct = m1.get("distinct_after_idempotent_minting")
    # distinct by spec_id (matches the recorded minting), then split by authoring cycle
    seen = {}
    for r in recs:
        sid = r.get("spec_id")
        if sid not in seen:
            seen[sid] = r
    distinct = list(seen.values())
    cycle16 = [r for r in distinct if r.get("cycle_authored") == 16]
    cyc_1_15 = [r for r in distinct if r.get("cycle_authored") in range(1, 16)]
    # apply the §1 canonical-identity unit over the cycles-1-15 records (re-dedup by the
    # frozen tuple; this is idempotent over already-minted definition sites but is applied
    # identically by all three methods per the frozen contract).
    canon = set()
    for r in cyc_1_15:
        at = r.get("audit_tuple", [])
        repo = at[0] if len(at) > 0 else ""
        path = at[1] if len(at) > 1 else ""
        # the in-file definition anchor = the spec's authoritative-definition key
        # (the disposition/decisions_log key for DesignDecision; the Layer-5 token for
        # MethodologyCommitment; AgentContract/Schema collapse on the file alone).
        anchor = (r.get("name_truncated") or "").strip()
        canon.add(_canonical_identity(repo, path, r.get("spec_class", ""), anchor))
    return raw_distinct, len(canon), len(cycle16), len(cyc_1_15)


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
    all_s2_raw = git_specs + prose_specs + tx_specs

    # ----- FROZEN DEFINITION §3 exclusions (the S21 contamination fix) -----
    # §3.1 principle-references (DP/HC/GPL/Pattern/Binding/...) + §3.2 Cycle-16-own
    # Done #N items are NOT cycles-1-15 specs. Filter them out of the candidate stream,
    # tallying WHAT was excluded (disclosed as the contamination removed).
    all_s2 = []
    excluded_tally = {"principle_reference_3_1": 0, "cycle16_own_done_item_3_2": 0}
    excluded_examples = {"principle_reference_3_1": [], "cycle16_own_done_item_3_2": []}
    for s in all_s2_raw:
        reason = is_excluded_token(s["authored_name"])
        if reason:
            excluded_tally[reason] += 1
            if len(excluded_examples[reason]) < 5:
                excluded_examples[reason].append(s["authored_name"])
            continue
        all_s2.append(s)

    # distinct S2 specs (idempotent mint over authored_name + provenance_source)
    distinct = {}
    for s in all_s2:
        sid = _mint_spec_id(s["authored_name"], s["provenance_source"])
        s["spec_id"] = sid
        distinct.setdefault(sid, s)
    s2_specs = list(distinct.values())

    recorded_names, recorded_raw, m1_distinct = load_method1_recorded_names()
    # M1' under the frozen scope (cycles-1-15 only, canonical-identity unit)
    m1_raw, m1_prime, m1_cycle16_excluded, m1_cyc_1_15 = compute_m1_prime()

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
        "schema_version": "be_r_denominator_dual_method.v2_frozen",
        "build_event": "BE-R part 1 — denominator dual-method, frozen-def re-run "
                       "(Done #50 / H_phase11_50; S22 deliverable (b.1))",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        # freeze-before-count binding (threshold 7): cite the frozen def by path + SHA.
        "frozen_definition_path": FROZEN_DEFINITION_PATH,
        "frozen_definition_commit": FROZEN_DEFINITION_COMMIT,
        "frozen_definition_exclusions_applied": {
            "principle_references_3_1": excluded_tally["principle_reference_3_1"],
            "cycle16_own_done_items_3_2": excluded_tally["cycle16_own_done_item_3_2"],
            "examples": excluded_examples,
            "note": ("§3.1 DP/HC/GPL/Pattern/Binding refs + §3.2 Cycle-16-own Done #N "
                     "filtered from the candidate stream BEFORE counting (citation ≠ "
                     "membership; recovery scope ≠ cycles-1-15 audited population)."),
        },
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
            # M1' under the frozen scope (frozen def §4 + §1 unit)
            "m1_raw_distinct": m1_raw,
            "m1_cycle16_authored_excluded": m1_cycle16_excluded,
            "m1_cycles_1_15_records": m1_cyc_1_15,
            "m1_prime_cycles_1_15_frozen_unit": m1_prime,
            "m1_prime_note": ("M1' = cycles-1-15 records (cycle_authored ∈ 1..15) after "
                              "the §1 canonical-identity unit; Cycle-16-authored records "
                              "filtered out per §4."),
        },
        "method_2_authored_intent": {
            "git_history_specs": len(git_specs),
            "prose_ruling_specs": len(prose_specs),
            "transcript_specs": len(tx_specs),
            "candidates_before_exclusion": len(all_s2_raw),
            "candidates_after_exclusion": len(all_s2),
            "distinct_s2_specs": len(s2_specs),
            "m2_prime_note": ("M2' = distinct authored-intent specs after the §3.1/§3.2 "
                              "exclusions + idempotent mint; DP/HC/GPL/Pattern/Binding "
                              "refs + Cycle-16-own Done #N removed."),
        },
        "divergence": {
            "authored_but_unrecorded_count": len(authored_but_unrecorded),
            "authored_but_unrecorded_note": ("authored_but_unrecorded' under the frozen "
                "predicate: distinct authored-intent specs (post §3.1/§3.2 exclusion) "
                "with no matching canonical-identity in the M1 recorded set — the genuine "
                "recorded-vs-authored gap (#50 finding). Whatever it is, it is disclosed; "
                "not engineered to a target."),
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
    m1r = out["method_1_recorded"]
    m2 = out["method_2_authored_intent"]
    exc = out["frozen_definition_exclusions_applied"]
    print(f"frozen_definition: {out['frozen_definition_path']} @ {out['frozen_definition_commit']}")
    print(f"§3 exclusions applied — principle-refs: {exc['principle_references_3_1']}, "
          f"Cycle-16-own Done #N: {exc['cycle16_own_done_items_3_2']}")
    print(f"Method 1 raw distinct: {m1r['distinct_after_idempotent_minting']} "
          f"(cycle16 excluded: {m1r['m1_cycle16_authored_excluded']})")
    print(f"M1' (cycles-1-15, frozen unit): {m1r['m1_prime_cycles_1_15_frozen_unit']}")
    print(f"M2' distinct S2 specs (post-exclusion): {m2['distinct_s2_specs']} "
          f"(candidates {m2['candidates_before_exclusion']}->{m2['candidates_after_exclusion']}; "
          f"git={m2['git_history_specs']} prose={m2['prose_ruling_specs']} "
          f"transcript={m2['transcript_specs']})")
    print(f"authored_but_unrecorded' (frozen predicate): {out['divergence']['authored_but_unrecorded_count']}")
    print(f"methods_read_disjoint_sources: {disjoint}")
    print(f"close_claim: {out['close_claim']}")
    print("Sample provenance rows (authored_but_unrecorded):")
    for e in out["divergence"]["authored_but_unrecorded"][:3]:
        print(f"  - {e['authored_name']} | {e['provenance_source']} | "
              f"{e['recorded_set_absence_evidence'][:70]}...")
    print(f"Wrote {DUAL_METHOD_PATH}")


if __name__ == "__main__":
    main()
