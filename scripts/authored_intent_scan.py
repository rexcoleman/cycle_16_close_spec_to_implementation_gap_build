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

# S23 (a′) DesignDecision count-grain pin — the NEW freeze, committed FIRST (frozen def §7).
# The grain-pin freeze pins the DesignDecision counting grain to one decision-identity
# (§7.1) and binds the §7.4 per-method (M1/M2/M3) reconciliation. The re-count output cites
# this by path + SHA (threshold 6″-FB); the cited commit is an ancestor of the re-count commit.
GRAIN_PIN_PATH = "docs/spec_class_frozen_definition.md#7"
GRAIN_PIN_COMMIT = "d50b6e9"

DESIGN_DECISION_CLASS = "c_design_decision"

# §7.1 minting/serialization suffix stripping: trailing dates, landed_* markers, and
# _NNNN minting suffixes are serialization artifacts on the decision-name, not part of the
# decision-identity. Stripped BEFORE the identity hash so a decision recorded at site A
# (e.g. `..._landed_2026_05_17`) and mirrored at site B (`...`) resolve to ONE identity.
_DD_SUFFIX_RE = re.compile(
    r"(?:[_\-\s]+(?:landed|land|minted|mint|recorded|closed|close|added)\b[a-z0-9_\-]*"  # landed_* / closed_* markers
    r"|[_\-\s]*\b\d{4}[_\-]\d{1,2}[_\-]\d{1,2}\b"   # trailing ISO-ish date 2026_05_17 / 2026-05-17
    r"|[_\-\s]*\b\d{4}\b"                            # trailing bare year
    r"|[_\-]\d{3,4}$)+\s*$",                         # trailing _NNNN minting suffix
    re.I,
)


def normalize_decision_identity(name):
    """Frozen def §7.1: map a DesignDecision candidate to its normalized DECISION-IDENTITY.

    The decision-identity is the thing an ADR/disposition *decides*: the DECISION_LOG ADR-ID
    (`ADR-S22-1`), or the state.json disposition decision-name (the `paradigm_dispositions:<key>`
    key, or a `decisions_log` entry's own decision-id/topic). Normalization (§7.1): drop the
    `paradigm_dispositions:`/`decisions_log:` container prefix (the grain is the DECISION, not
    the container), lowercase, strip trailing date / `landed_*` / `_NNNN` minting suffix,
    collapse whitespace/punctuation. This is the §7.2 anchor: mirror/citation sites of the
    SAME decision normalize to the SAME identity and collapse to one hash."""
    s = (name or "").strip()
    # drop the container prefix so paradigm_dispositions:<k> and decisions_log:<k> for the
    # SAME decision-name resolve to the same identity (the grain is the decision, not the file key).
    for prefix in ("paradigm_dispositions:", "decisions_log:", "honest_carries:"):
        if s.lower().startswith(prefix):
            s = s[len(prefix):]
            break
    s = s.lower().strip()
    # strip trailing minting/serialization suffixes (date / landed_* / _NNNN), repeatedly
    prev = None
    while prev != s:
        prev = s
        s = _DD_SUFFIX_RE.sub("", s).strip()
    # collapse internal whitespace/punctuation runs to a single underscore
    s = re.sub(r"[\s\-\.:/#]+", "_", s).strip("_")
    return s or (name or "").strip().lower()

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
    site WITHOUT collapsing distinct decisions/commitments that merely share a file.

    S23 (a′) grain-pin (frozen def §7.2): for class DesignDecision the anchor is pinned to
    the normalized DECISION-IDENTITY (not the bare realpath#name_truncated), and the repo/site
    are DROPPED from the hash, so the SAME decision recorded at site A (a DECISION_LOG ADR row)
    and mirrored at site B (a state.json paradigm_dispositions block) and cited in a handoff
    collapse to ONE hash:  sha256(repo | <normalized-decision-identity> | "c_design_decision").
    The §7.2 canonical-identity hash for DesignDecision keys ONLY on (repo, decision-identity,
    class) — recording-site agnostic. All other classes keep the per-definition-site grain."""
    if spec_class == DESIGN_DECISION_CLASS:
        ident = normalize_decision_identity(anchor)
        return hashlib.sha256(
            f"{repo}|{ident}|{spec_class}".encode("utf-8")
        ).hexdigest()[:16]
    rp = os.path.realpath(canonical_path.replace("~", HOME)) if canonical_path else ""
    site = f"{rp}#{anchor}" if anchor else rp
    return hashlib.sha256(
        f"{repo}|{site}|{spec_class}".encode("utf-8")
    ).hexdigest()[:16]


def compute_m1_prime():
    """Re-count M1 under the FROZEN scope (frozen def §4) + the S23 (a′) grain-pin (§7.4 M1).
    The cycles-1-15 denominator excludes Cycle-16-authored records (cycle_authored == 16).
    Returns (m1_raw_distinct, m1_prime_cycles_1_15, cycle16_excluded, m1_cyc_1_15,
    m1_prime_pre_grain_pin, dd_pre, dd_post) all [measured].

    Two M1′ numbers are reported (§7.5 / threshold 6″-EM transparency): `m1_prime_pre_grain_pin`
    uses the S22 per-definition-site anchor for DesignDecision; `m1_prime` (the post-pin value)
    uses the §7.2 decision-identity anchor — so the collapse from mirror/citation sites is
    MEASURED, not asserted. Per §7.4 M1 was already at the decision grain, so the change is
    only same-decision mirrors that previously survived on differing realpaths."""
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

    def _canon_with_anchor_mode(grain_pinned):
        """Re-dedup the cycles-1-15 records by canonical-identity. When grain_pinned is
        False, DesignDecision uses the S22 per-definition-site anchor (realpath#name); when
        True, it uses the §7.2 decision-identity anchor (via _canonical_identity)."""
        canon = set()
        for r in cyc_1_15:
            at = r.get("audit_tuple", [])
            repo = at[0] if len(at) > 0 else ""
            path = at[1] if len(at) > 1 else ""
            anchor = (r.get("name_truncated") or "").strip()
            cls = r.get("spec_class", "")
            if cls == DESIGN_DECISION_CLASS and not grain_pinned:
                # S22 behaviour: per-definition-site (realpath#name_truncated) hash
                rp = os.path.realpath(path.replace("~", HOME)) if path else ""
                site = f"{rp}#{anchor}" if anchor else rp
                canon.add(hashlib.sha256(
                    f"{repo}|{site}|{cls}".encode("utf-8")).hexdigest()[:16])
            else:
                canon.add(_canonical_identity(repo, path, cls, anchor))
        return canon

    canon_pre = _canon_with_anchor_mode(grain_pinned=False)
    canon_post = _canon_with_anchor_mode(grain_pinned=True)
    # DesignDecision-only before/after, to show the pin's effect inside the class
    dd_recs = [r for r in cyc_1_15 if r.get("spec_class") == DESIGN_DECISION_CLASS]
    dd_pre, dd_post = set(), set()
    for r in dd_recs:
        at = r.get("audit_tuple", [])
        repo = at[0] if len(at) > 0 else ""
        path = at[1] if len(at) > 1 else ""
        anchor = (r.get("name_truncated") or "").strip()
        rp = os.path.realpath(path.replace("~", HOME)) if path else ""
        site = f"{rp}#{anchor}" if anchor else rp
        dd_pre.add(hashlib.sha256(
            f"{repo}|{site}|{DESIGN_DECISION_CLASS}".encode("utf-8")).hexdigest()[:16])
        dd_post.add(_canonical_identity(repo, path, DESIGN_DECISION_CLASS, anchor))
    return (raw_distinct, len(canon_post), len(cycle16), len(cyc_1_15),
            len(canon_pre), len(dd_pre), len(dd_post))


def compute_m3_census():
    """M3 (§7.4 identifier census) under the pinned grain — the re-measurement that produced
    63 → 424 at S22. M3 reads the RAW state.json / DECISION_LOG.md DesignDecision source files
    (the cycles-1-15 sources M1 recorded) and censuses identifier OCCURRENCES at three grains,
    then maps each occurrence to the decision-identity it RECORDS (§7.4 M3) and dedups by the
    §7.2 hash. Reports all three raw grains [measured] + the post-pin decision-identity count.

      - whole-block grain  (the 63-style under-count): one paradigm_dispositions block + one
        decisions_log block per file = 1 each.
      - sub-field grain    (the 424-style over-count): each leaf sub-field of every disposition
        value object + each decisions_log entry counts as one occurrence.
      - decision-identity  (the PINNED grain, §7.1): each paradigm_dispositions:<key> → its
        disposition decision-identity (sub-case ii: ALL its sub-fields collapse to that ONE
        identity → defeats 424); each decisions_log entry → its OWN decision-identity
        (sub-case iii: N distinct entries = N identities → defeats 63); mirror/citation of an
        already-seen identity collapses (sub-case i). Dedup by the §7.2 hash; count DISTINCT
        decision-identities, NOT occurrences.

    All three numbers are MEASURED off the same raw files; the pinned-grain number is the M3
    figure reconciled to the §7.4 mapping. Never tuned (§7.5)."""
    # the cycles-1-15 DesignDecision source files M1 recorded (from audit_tuple[1])
    with open(METHOD1_PATH) as f:
        m1 = json.load(f)
    src_files = {}  # realpath -> repo
    for r in m1.get("per_spec_evidence_IP_PRIVATE", []):
        if r.get("spec_class") != DESIGN_DECISION_CLASS:
            continue
        if r.get("cycle_authored") not in range(1, 16):
            continue
        at = r.get("audit_tuple", [])
        if len(at) < 2 or not at[1]:
            continue
        rp = os.path.realpath(at[1].replace("~", HOME))
        src_files.setdefault(rp, at[0] if at[0] else "")

    whole_block = 0
    sub_field = 0
    identity_hashes = set()
    decisions_log_entries = 0
    paradigm_keys = 0

    for rp, repo in sorted(src_files.items()):
        if not os.path.isfile(rp):
            continue
        base = os.path.basename(rp).lower()
        if base == "state.json":
            try:
                d = json.load(open(rp, encoding="utf-8", errors="replace"))
            except Exception:
                continue
            pd = d.get("paradigm_dispositions")
            dl = d.get("decisions_log")
            if isinstance(pd, dict) and pd:
                whole_block += 1  # the whole paradigm_dispositions block = 1 (63-style)
                for key, val in pd.items():
                    paradigm_keys += 1
                    # sub-field grain: each leaf sub-field of the value object (424-style)
                    if isinstance(val, dict) and val:
                        sub_field += len(val)
                    else:
                        sub_field += 1
                    # §7.4 M3 / sub-case (ii): the WHOLE block's sub-fields map to ONE
                    # disposition decision-identity → dedup by §7.2 hash.
                    ident = _canonical_identity(repo, rp, DESIGN_DECISION_CLASS, key)
                    identity_hashes.add(ident)
            if isinstance(dl, list) and dl:
                whole_block += 1  # the whole decisions_log block = 1 (63-style)
                for i, entry in enumerate(dl):
                    sub_field += 1  # each entry counts at sub-field grain too
                    decisions_log_entries += 1
                    # §7.4 M3 / sub-case (iii): each distinct decisions_log entry → its OWN
                    # decision-identity (defeats the 63 under-count). Anchor on the entry's
                    # own decision-name/topic (decision/topic/id field) else a stable per-entry id.
                    if isinstance(entry, dict):
                        topic = (entry.get("decision") or entry.get("topic")
                                 or entry.get("id") or entry.get("ruling")
                                 or entry.get("session") or "")
                    else:
                        topic = str(entry)
                    if not topic:
                        topic = f"decisions_log_entry_{i}"
                    ident = _canonical_identity(
                        repo, rp, DESIGN_DECISION_CLASS, f"decisions_log:{topic}")
                    identity_hashes.add(ident)
        elif base.endswith(".md"):
            # DECISION_LOG.md ADR rows — each ADR-ID is one decision-identity (sub-case iii);
            # mere mentions/citations of an already-seen ADR-ID collapse (sub-case i).
            try:
                txt = open(rp, encoding="utf-8", errors="replace").read()
            except Exception:
                continue
            adr_ids = set(re.findall(r"\bADR-[A-Za-z0-9\-]+\b", txt))
            if adr_ids:
                whole_block += 1
            for adr in adr_ids:
                sub_field += 1
                ident = _canonical_identity(repo, rp, DESIGN_DECISION_CLASS, adr)
                identity_hashes.add(ident)

    return {
        "whole_block_grain": whole_block,          # the 63-style under-count
        "sub_field_grain": sub_field,              # the 424-style over-count
        "paradigm_disposition_keys": paradigm_keys,
        "decisions_log_entries": decisions_log_entries,
        "decision_identity_grain": len(identity_hashes),  # the PINNED grain (§7.1)
        "source_files_censused": len(src_files),
    }


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
    # M1' under the frozen scope (cycles-1-15 only) + the S23 (a′) grain-pin (§7.4 M1)
    (m1_raw, m1_prime, m1_cycle16_excluded, m1_cyc_1_15,
     m1_prime_pre_pin, dd_pre, dd_post) = compute_m1_prime()

    # ----- S23 (a′) M3 identifier census under the pinned grain (§7.4 M3) -----
    m3 = compute_m3_census()

    # ----- S23 (a′) M2 DesignDecision reconciliation to decision-identities (§7.4 M2) -----
    # Build the set of M1-recorded DesignDecision decision-identities so an M2 authored-intent
    # candidate that resolves to an already-recorded decision-identity collapses (citation /
    # recording-site, §7.2 — NOT a new spec). M2 DesignDecision candidates that resolve to a
    # NEW decision-identity are genuine authored_but_unrecorded decisions.
    with open(METHOD1_PATH) as f:
        _m1full = json.load(f)
    m1_dd_identities = set()
    for r in _m1full.get("per_spec_evidence_IP_PRIVATE", []):
        if r.get("spec_class") == DESIGN_DECISION_CLASS and r.get("cycle_authored") in range(1, 16):
            m1_dd_identities.add(normalize_decision_identity(r.get("name_truncated") or ""))
    # M2 decision-identities: authored-intent DesignDecision-shaped candidates (those whose
    # authored_name looks like an ADR-ID or a disposition decision-name), mapped to identity
    # and deduped; citations of an M1 identity collapse into it (not counted as new).
    _ADR_LIKE = re.compile(r"^(ADR-|paradigm_dispositions:|decisions_log:)", re.I)
    m2_dd_new_identities = set()
    m2_dd_collapsed_into_m1 = set()
    for s in s2_specs:
        nm = (s.get("authored_name") or "").strip()
        if not _ADR_LIKE.match(nm):
            continue
        ident = normalize_decision_identity(nm)
        if not ident:
            continue
        if ident in m1_dd_identities:
            m2_dd_collapsed_into_m1.add(ident)  # citation of a recorded decision → collapse
        else:
            m2_dd_new_identities.add(ident)
    # M2 DesignDecision count = M1 identities it re-states (collapsed) ∪ new identities it states
    m2_dd_identity_count = len(m1_dd_identities | m2_dd_new_identities)

    # ----- the cross-method DesignDecision decision-identity spread (§7.5 / 6″-EM) -----
    # All three methods now express DesignDecision as DISTINCT decision-identities over the
    # cycles-1-15 population. The spread is MEASURED, never tuned.
    m1_dd_count = dd_post
    m3_dd_count = m3["decision_identity_grain"]
    method_dd_counts = {"M1": m1_dd_count, "M2": m2_dd_identity_count, "M3": m3_dd_count}
    dd_vals = [m1_dd_count, m2_dd_identity_count, m3_dd_count]
    dd_max, dd_min = max(dd_vals), min(dd_vals)
    dd_mean = sum(dd_vals) / len(dd_vals)
    # spread expressed as max deviation from the mean, as a fraction (±X%)
    dd_spread_frac = ((dd_max - dd_min) / dd_mean) if dd_mean else 0.0
    pm5_emerged = dd_spread_frac <= 0.05

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
        # S23 (a′) grain-pin freeze-before-count binding (threshold 6″-FB): cite the
        # grain-pin freeze (frozen def §7) by path + SHA; the cited commit is an ancestor
        # of the re-count commit (Coach verifies `git merge-base --is-ancestor`).
        "grain_pin_path": GRAIN_PIN_PATH,
        "grain_pin_commit": GRAIN_PIN_COMMIT,
        # the three per-method DesignDecision decision-identity counts + measured spread (§7.4/§7.5)
        "design_decision_grain_pin": {
            "pinned_grain": "one_decision_identity = one DesignDecision spec (frozen def §7.1)",
            "per_method_decision_identity_counts": method_dd_counts,
            "cross_method_spread_fraction": round(dd_spread_frac, 4),
            "cross_method_spread_pct": round(dd_spread_frac * 100, 2),
            "pm5_emerged": pm5_emerged,
            "m3_raw_grains_before_pin": {
                "whole_block_grain_63_style": m3["whole_block_grain"],
                "sub_field_grain_424_style": m3["sub_field_grain"],
                "paradigm_disposition_keys": m3["paradigm_disposition_keys"],
                "decisions_log_entries": m3["decisions_log_entries"],
                "decision_identity_grain_pinned": m3["decision_identity_grain"],
                "source_files_censused": m3["source_files_censused"],
            },
            "m3_collapse_note": (
                "M3 sub-field grain (424-style over-count) collapses to the decision-identity "
                "grain via sub-case (ii): all sub-fields of one paradigm_dispositions:<key> map "
                "to that key's ONE decision-identity. M3 whole-block grain (63-style under-count) "
                "lifts to the decision-identity grain via sub-case (iii): each distinct "
                "decisions_log entry maps to its OWN decision-identity. MEASURED, never tuned (§7.5)."
            ),
            "m2_reconciliation": {
                "m1_recorded_dd_identities": len(m1_dd_identities),
                "m2_new_dd_identities_authored_but_unrecorded": len(m2_dd_new_identities),
                "m2_citations_collapsed_into_m1": len(m2_dd_collapsed_into_m1),
                "m2_dd_identity_count": m2_dd_identity_count,
            },
        },
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
            # S23 (a′) grain-pin before/after (§7.5 transparency): pre-pin uses the S22
            # per-definition-site DesignDecision anchor; post-pin (= m1_prime) uses the
            # §7.2 decision-identity anchor. The delta is same-decision mirror collapse.
            "m1_prime_pre_grain_pin": m1_prime_pre_pin,
            "m1_prime_post_grain_pin": m1_prime,
            "design_decision_pre_grain_pin": dd_pre,
            "design_decision_post_grain_pin": dd_post,
            "m1_prime_note": ("M1' = cycles-1-15 records (cycle_authored ∈ 1..15) after "
                              "the §1 canonical-identity unit + the §7 decision-identity "
                              "grain-pin; Cycle-16-authored records filtered out per §4. "
                              "Per §7.4 M1 was already at the decision grain — the pin only "
                              "collapses same-decision mirrors that survived on differing realpaths."),
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
    print(f"M1' (cycles-1-15, frozen unit + grain-pin): {m1r['m1_prime_cycles_1_15_frozen_unit']} "
          f"(pre-pin {m1r['m1_prime_pre_grain_pin']} -> post-pin {m1r['m1_prime_post_grain_pin']}; "
          f"DesignDecision {m1r['design_decision_pre_grain_pin']} -> {m1r['design_decision_post_grain_pin']})")
    gp = out["design_decision_grain_pin"]
    g3 = gp["m3_raw_grains_before_pin"]
    print(f"grain-pin: {out['grain_pin_path']} @ {out['grain_pin_commit']}")
    print(f"M3 raw grains: whole-block(63-style)={g3['whole_block_grain_63_style']} "
          f"sub-field(424-style)={g3['sub_field_grain_424_style']} "
          f"-> decision-identity(pinned)={g3['decision_identity_grain_pinned']} "
          f"(pd-keys={g3['paradigm_disposition_keys']} dl-entries={g3['decisions_log_entries']})")
    print(f"per-method DesignDecision decision-identity counts: {gp['per_method_decision_identity_counts']}")
    print(f"cross-method spread: {gp['cross_method_spread_pct']}%  ±5% emerged: {gp['pm5_emerged']}")
    print(f"M2 reconciliation: {gp['m2_reconciliation']}")
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
