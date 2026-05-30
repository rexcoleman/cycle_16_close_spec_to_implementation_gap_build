#!/usr/bin/env python3
"""
spec_extraction_pipeline.py — BE-R part 2 (Spec-extraction completeness, Done #49 / H_phase11_49).

For each cycles-1–16 spec, extract its checkable commitments by TWO independent mechanisms,
then reconcile into a VALIDATED commitment set V that becomes the detector input.

  E1 = rule-based parser  — must-clause / SHALL / MUST / MUST-NOT / SHOULD patterns over the
       spec's prose neighborhood (deterministic, no model). mechanism id = "rule_based_clause_parser".
  E2 = LLM-judge extraction at a DIFFERENT reader — claude-haiku-4-5 reads the same prose and
       returns the checkable commitments. mechanism id = "llm_extraction:claude-haiku-4-5".

INDEPENDENCE bars:
  T4 extraction_methods_distinct(E1, E2) — mechanism ids MUST differ (single reader twice REFUSED).
  T6 detector input MUST be the reconciled validated set V (= E1∩E2 + adjudicated E1△E2);
     a single-reader extraction (E1-alone / E2-alone) as detector input HARD-FAILS.

Completeness (T5): per-spec + aggregate jaccard = |E1∩E2|/|E1∪E2|; every member of E1△E2 is
written to a symmetric_difference_ledger (which reader missed it + why) — never dropped.
Ledger length == |E1△E2| (mechanical equality).

Outputs:
  outputs/extraction_completeness.json          (T5 per-spec + aggregate Jaccard + ledger)
  outputs/validated_commitment_set.json         (T6 reconciled V; detector_input flag)
  outputs/extraction_methods_distinct_check.jsonl (T4 fire event)

Scope honesty: E2 (LLM) is itself judgment-tier. We measure E1/E2 AGREEMENT (completeness
proxy), NOT ground-truth completeness. High disagreement is a disclosed measured finding,
NOT a failure to hide. DP#44: refuse on missing key, never fabricate E2.

HC-11 partition: parser + LLM-extraction harness + metric code + assertions = PUBLISHABLE;
per-spec commitment-set contents = PIPELINE-IP-PRIVATE.
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import datetime, timezone

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUTS = os.path.join(PROJECT_ROOT, "outputs")
METHOD1_PATH = os.path.join(OUTPUTS, "retroactive_scan_cycle_1_15_run.json")
COMPLETENESS_PATH = os.path.join(OUTPUTS, "extraction_completeness.json")
VALIDATED_SET_PATH = os.path.join(OUTPUTS, "validated_commitment_set.json")
DISTINCT_CHECK_JSONL = os.path.join(OUTPUTS, "extraction_methods_distinct_check.jsonl")
HOME = os.path.expanduser("~")

E1_MECHANISM = "rule_based_clause_parser"
E2_MECHANISM = "llm_extraction:claude-haiku-4-5"
E2_MODEL = "claude-haiku-4-5"
ENV_BACKUP = os.path.join(HOME, "Moonshots_Career_Thesis_v2", ".env.backup")


# ---------------------------------------------------------------------------
# Independence assertion (T4)
# ---------------------------------------------------------------------------
def extraction_methods_distinct(method_e1, method_e2):
    """True iff the two extraction mechanism identifiers differ. A single reader twice
    (identical mechanism) is REFUSED."""
    return method_e1 != method_e2


# ---------------------------------------------------------------------------
# Prose loading
# ---------------------------------------------------------------------------
def load_population(limit=None):
    """The cycles-1–16 spec population = Method 1's DISTINCT specs (232 after idempotent
    minting; the 268 raw rows include idempotent duplicates). Dedup by spec_id so the
    extraction population equals the canonical denominator."""
    with open(METHOD1_PATH) as f:
        m1 = json.load(f)
    raw = m1.get("per_spec_evidence_IP_PRIVATE", [])
    seen = {}
    for r in raw:
        sid = r.get("spec_id")
        if sid not in seen:
            seen[sid] = r
    recs = list(seen.values())
    if limit:
        recs = recs[:limit]
    return recs


def _json_prose_for_key(path, name, n):
    """state.json dispositions/decisions specs name an interior key
    ('paradigm_dispositions:<k>' / 'decisions_log:<k>'). The DEFINITION-SITE prose
    is that key's value object (scope / authority / rationale text), NOT the file
    header. Resolve the block by locating the key inside its container and
    serializing its value; if the value is a string, return it directly. Returns
    None when the key cannot be resolved (caller falls back to text search)."""
    try:
        d = json.load(open(path, encoding="utf-8", errors="replace"))
    except Exception:
        return None
    container, _, key = name.partition(":")
    block = d.get(container)
    val = None
    if isinstance(block, dict):
        if key and key in block:
            val = block[key]
        else:
            # key may be a truncated/normalized form — match by prefix
            for k, v in block.items():
                if key and (k.startswith(key) or key.startswith(k)):
                    val = v
                    break
    elif isinstance(block, list):
        for item in block:
            if isinstance(item, dict) and key and key in json.dumps(item):
                val = item
                break
    if val is None:
        return None
    if isinstance(val, str):
        return val[:n]
    # dict/list → join the human-readable text fields (scope/decision/rationale/...)
    parts = []

    def _walk(o):
        if isinstance(o, str):
            parts.append(o)
        elif isinstance(o, dict):
            for vv in o.values():
                _walk(vv)
        elif isinstance(o, list):
            for vv in o:
                _walk(vv)

    _walk(val)
    return (". ".join(parts))[:n] if parts else None


def _findings_block(txt, name, n):
    """FINDINGS.md methodology-commitment specs name a Layer-5 token
    ('Binding 6', 'DP#44', 'Pattern 9', 'R1', 'HC-11', 'Discipline #13', ...). The
    DEFINITION-SITE prose is the block where that token is AUTHORED (the row/line
    that introduces it), not the first occurrence in a downstream citation. Prefer a
    line that introduces the token (start-of-line, optionally bolded / in a table
    cell); fall back to first occurrence. Take a window FORWARD from there so the
    obligation clauses that follow the token are inside the window."""
    esc = re.escape(name.strip())
    # introduction patterns: '**Binding 6**', '| Binding 6 |', '- Binding 6:', '### DP#44'
    intro = re.search(r"(?m)^[ \t|#>*\-]{0,8}\**\s*" + esc + r"\b", txt)
    m = intro or re.search(esc, txt)
    if not m:
        return None
    start = max(0, m.start() - 30)
    return txt[start:start + n]


def spec_prose_window(rec, n=900):
    """Resolve the spec's ACTUAL definition-site prose, class-aware (frozen def §6).

    The S21 bug: a bare `name` find + 700-char window degraded to the FILE HEADER
    (YAML frontmatter / .ttl prefixes / state.json top) for 152/232 specs whose name
    is not a literal substring of the file, leaving E1 to read no obligation prose.
    The competent reader resolves the definition SITE per class:
      - state.json dispositions/decisions (c_design_decision) → the keyed value block;
      - FINDINGS.md tokens (d_methodology_commitment) → the authoring Layer-5 block;
      - agent .md / schema .ttl/.json/.py → the body/definition block (skip frontmatter).
    Only degrades to the bare name when the file is genuinely unreadable."""
    at = rec.get("audit_tuple", [])
    path = at[1].replace("~", HOME) if len(at) > 1 else None
    name = rec.get("name_truncated", "")
    if not path or not os.path.isfile(path):
        return name  # degrade to the name itself
    try:
        txt = open(path, encoding="utf-8", errors="replace").read()
    except Exception:
        return name
    base = os.path.basename(path).lower()

    # (1) state.json keyed dispositions/decisions — resolve the keyed value block.
    if base == "state.json" and ":" in name:
        blk = _json_prose_for_key(path, name, n)
        if blk:
            return blk

    # (2) FINDINGS.md (+ DECISION_LOG.md) token specs — resolve the authoring block.
    if base.endswith(".md") and (
        rec.get("spec_class") in ("d_methodology_commitment", "c_design_decision")
    ):
        blk = _findings_block(txt, name, n)
        if blk:
            return blk

    # (3) agent .md / schema files — locate the name, else the body after the header.
    i = txt.find(name)
    if i < 0 and ":" in name:
        i = txt.find(name.split(":")[-1])
    if i >= 0:
        return txt[max(0, i - 60): i + n]
    # name not present: for markdown skip YAML frontmatter; for schema take the
    # definition region. Avoid degrading to the bare top-of-file header alone.
    body = txt
    if txt.startswith("---"):
        end = txt.find("\n---", 3)
        if end > 0:
            body = txt[end + 4:]
    return (name + "\n" + body[:n]).strip()


# ---------------------------------------------------------------------------
# Commitment normalization (so E1 and E2 are comparable)
# ---------------------------------------------------------------------------
_STOP = set("the a an of to and or for in on at by with is are be must shall should not "
            "this that it its as per via into".split())


def _content_tokens(text):
    toks = re.findall(r"[a-z0-9]+", text.lower())
    # crude stem: drop a trailing 's' to align enforce/enforces, entry/entries-ish forms
    out = set()
    for t in toks:
        if t in _STOP or len(t) <= 2:
            continue
        out.add(t[:-1] if (len(t) > 4 and t.endswith("s")) else t)
    return out


def normalize_commitment(text):
    """Comparable signature: sorted content-token stem set, truncated. Used as the dict key
    so identical obligations collapse; cross-reader matching uses token-overlap (see
    _commitments_match) because two readers paraphrase the same obligation differently."""
    toks = sorted(_content_tokens(text))
    sig = "_".join(toks[:6])
    return sig or text.lower().strip()[:24]


def _commitments_match(text_a, text_b, min_overlap=2):
    """Two extracted commitments refer to the SAME obligation iff their content-token stem
    sets share >= min_overlap tokens AND Jaccard of those token sets >= 0.34. This is the
    cross-reader matcher (E1 clause vs E2 paraphrase); exact-signature equality is too brittle
    across two different readers and would manufacture a near-zero (artifactual) Jaccard."""
    a, b = _content_tokens(text_a), _content_tokens(text_b)
    if not a or not b:
        return False
    inter = a & b
    if len(inter) < min_overlap:
        return False
    return (len(inter) / len(a | b)) >= 0.34


# ---------------------------------------------------------------------------
# E1 — rule-based clause parser
# ---------------------------------------------------------------------------
# Modal/obligation anchors that START a checkable commitment. E1 splits the prose at each
# anchor and takes the clause that FOLLOWS it (one obligation per anchor), so E1 produces
# atomic commitments comparable to E2 instead of one run-on clause.
# E1's obligation anchors are the modal/imperative markers that, IN THIS CORPUS'S
# DEFINITION-SITE PROSE, begin a checkable commitment. These are real obligation
# vocabulary surveyed from the spec prose itself (agent .md / FINDINGS Layer-5 /
# state.json dispositions / schema comments) — NOT tuned to mimic E2's output. E1
# stays a deterministic clause-splitter: it finds an anchor and takes the predicate
# clause that follows. Any anchor here denotes "a thing that MUST/MUST-NOT happen,
# is REQUIRED/BINDING, is asserted/enforced/verified, HALTs/FAILs/BLOCKs, or is
# REFUSED/LOCKED" — the principled definition of a checkable commitment.
E1_ANCHOR = re.compile(
    r"\b(MUST NOT|MUST|SHALL NOT|SHALL|SHOULD NOT|SHOULD|REQUIRED|BINDING|BLOCKING|"
    r"enforces?|asserts?|requires?|ensures?|HARD-?FAILs?|REFUSED?|REFUSE|"
    r"verif(?:y|ies|ied)|exits? non-zero|returns? True|HALTs?|BLOCKs?|"
    r"FAILs?|PASS(?:es)?|LOCKED|UNCHANGED|forbidden|prohibited|"
    r"NOT (?:appear|route|edit|commit|drop|exceed)|may not|cannot)\b",
    re.I,
)


def extract_e1(prose):
    """Rule-based: each modal/obligation anchor begins one checkable commitment; the clause
    is the anchor PLUS the substantive predicate up to the next anchor / clause boundary.

    Quality rule (deterministic, NOT E2-mimicking): a checkable commitment is an obligation
    anchor FOLLOWED BY a predicate naming what is obligated. A lone anchor keyword with no
    following predicate ('BINDING' on its own line; a bare 'PASS' table cell) is NOT a
    checkable commitment — it is dropped. The predicate must carry >=2 content tokens
    (after stop-word removal) so 'MUST' / 'BINDING' alone do not mint a junk commitment."""
    commitments = {}
    anchors = list(E1_ANCHOR.finditer(prose))
    for idx, m in enumerate(anchors):
        start = m.start()
        # predicate ends at next anchor OR a sentence/clause boundary, whichever is first
        nxt = anchors[idx + 1].start() if idx + 1 < len(anchors) else len(prose)
        bound = re.search(r"[.;\n|]", prose[start:nxt])
        end = start + bound.start() if bound else nxt
        clause = prose[start:end].strip()
        if len(clause) < 10:
            continue
        # the clause must carry a predicate beyond the anchor keyword itself: >=2 content
        # tokens that are not themselves the anchor modal (drops lone 'BINDING'/'MUST').
        anchor_tok = m.group(0).lower().replace("-", "").replace(" ", "")
        pred_tokens = {t for t in _content_tokens(clause)
                       if t.replace("-", "") != anchor_tok and t not in
                       ("must", "shall", "should", "required", "binding", "blocking",
                        "refused", "refuse", "locked", "pass", "fail", "hardfail",
                        "halt", "block", "unchanged", "forbidden", "prohibited")}
        if len(pred_tokens) < 2:
            continue
        sig = normalize_commitment(clause)
        commitments.setdefault(sig, clause[:120])
    return commitments  # {sig: clause_text}


# ---------------------------------------------------------------------------
# E2 — LLM extraction (claude-haiku-4-5), a DIFFERENT reader
# ---------------------------------------------------------------------------
_E2_CLIENT = None


def _load_key():
    if not os.path.isfile(ENV_BACKUP):
        return None
    txt = open(ENV_BACKUP).read()
    m = re.search(r"^ANTHROPIC_API_KEY=(\S+)", txt, re.M)
    if not m:
        return None
    return m.group(1).strip().strip('"').strip("'")


def _e2_client():
    global _E2_CLIENT
    if _E2_CLIENT is not None:
        return _E2_CLIENT
    key = _load_key()
    if not key:
        # DP#44: refuse on missing key — never fabricate E2
        raise RuntimeError("DP#44 REFUSE: ANTHROPIC_API_KEY not found in .env.backup; "
                           "E2 cannot be fabricated.")
    import anthropic
    _E2_CLIENT = anthropic.Anthropic(api_key=key)
    return _E2_CLIENT


E2_PROMPT = (
    "You are extracting the CHECKABLE COMMITMENTS (testable obligations: what MUST/SHALL "
    "happen, what is REQUIRED, what is asserted/enforced/refused) from a software/spec "
    "prose fragment. Return ONLY a JSON array of short commitment strings (each a single "
    "obligation), no prose. If none, return []. Fragment:\n\n"
)


def extract_e2(prose, max_retries=4):
    client = _e2_client()
    last_err = None
    for attempt in range(max_retries):
        try:
            r = client.messages.create(
                model=E2_MODEL,
                max_tokens=400,
                messages=[{"role": "user", "content": E2_PROMPT + prose[:1500]}],
            )
            raw = r.content[0].text.strip()
            mm = re.search(r"\[.*\]", raw, re.S)
            arr = json.loads(mm.group(0)) if mm else []
            commitments = {}
            for c in arr:
                if not isinstance(c, str) or len(c.strip()) < 4:
                    continue
                sig = normalize_commitment(c)
                commitments.setdefault(sig, c.strip()[:120])
            return commitments
        except Exception as e:
            last_err = e
            msg = str(e)
            if "529" in msg or "overload" in msg.lower() or "rate" in msg.lower():
                time.sleep(2 ** attempt)
                continue
            # transient JSON / network — one short retry then give up for this spec
            time.sleep(1)
    raise RuntimeError(f"E2 failed after {max_retries} retries: {last_err}")


# ---------------------------------------------------------------------------
# Reconcile per spec
# ---------------------------------------------------------------------------
def reconcile_spec(spec_id, e1, e2):
    """Match E1 and E2 commitments by token-overlap (greedy bipartite), then:
      intersection = matched obligation pairs (both readers found it);
      E1-only / E2-only = unmatched (the symmetric difference, surfaced to the ledger);
      jaccard = |matched| / (|matched| + |E1-only| + |E2-only|);
      V = matched (canonical text) + adjudicated unmatched members (admit-on-either-reader)."""
    e1_items = list(e1.items())   # (sig, text)
    e2_items = list(e2.items())
    e2_used = set()
    matched = []   # (e1_sig, e1_text, e2_sig, e2_text)
    for s1sig, s1txt in e1_items:
        best = None
        for j, (s2sig, s2txt) in enumerate(e2_items):
            if j in e2_used:
                continue
            if _commitments_match(s1txt, s2txt):
                best = j
                break
        if best is not None:
            e2_used.add(best)
            matched.append((s1sig, s1txt, e2_items[best][0], e2_items[best][1]))

    e1_only = [(s, t) for (s, t) in e1_items
               if s not in {m[0] for m in matched}]
    e2_only = [(s, t) for j, (s, t) in enumerate(e2_items) if j not in e2_used]

    inter_n = len(matched)
    union_n = inter_n + len(e1_only) + len(e2_only)
    sym_n = len(e1_only) + len(e2_only)
    jaccard = (inter_n / union_n) if union_n else 1.0

    ledger = []
    for sig, txt in e1_only:
        ledger.append({
            "spec_id": spec_id, "commitment_sig": sig, "commitment_text": txt,
            "found_by": "E1_rule", "missed_by": "E2_llm",
            "why": "rule-parser surfaced this obligation; LLM extraction did not",
        })
    for sig, txt in e2_only:
        ledger.append({
            "spec_id": spec_id, "commitment_sig": sig, "commitment_text": txt,
            "found_by": "E2_llm", "missed_by": "E1_rule",
            "why": "LLM extraction surfaced this obligation; rule-parser did not",
        })

    # V = matched (E1∩E2, canonical E1 text) + adjudicated unmatched (admit-on-either-reader)
    v_members = []
    for s1sig, s1txt, s2sig, s2txt in matched:
        v_members.append({"commitment_sig": s1sig, "commitment_text": s1txt,
                          "source": "E1∩E2"})
    for sig, txt in e1_only:
        v_members.append({"commitment_sig": sig, "commitment_text": txt,
                          "source": "adjudicated:E1_only"})
    for sig, txt in e2_only:
        v_members.append({"commitment_sig": sig, "commitment_text": txt,
                          "source": "adjudicated:E2_only"})

    return {
        "spec_id": spec_id,
        "e1_count": len(e1_items),
        "e2_count": len(e2_items),
        "intersection": inter_n,
        "union": union_n,
        "symmetric_difference": sym_n,
        "jaccard": round(jaccard, 4),
        "ledger": ledger,
        "v_members": v_members,
    }


# ---------------------------------------------------------------------------
# Detector-input guard (T6)
# ---------------------------------------------------------------------------
# Threshold 6′ composition floors — FROZEN by EXPERIMENTAL_DESIGN.md §5.phase11.1-R
# (derived: 0.20 = 1/(2 readers + 3), the lenient principled per-reader floor; 0.80 =
# 1 − 0.20, the symmetric solo-dominance ceiling; Jaccard ≥ 0.20 = material agreement).
# These are NOT set to whatever the current run scores — DO NOT change them to pass.
T6P_CONTRIB_FLOOR = 0.20
T6P_SOLO_CEILING = 0.80
T6P_JACCARD_FLOOR = 0.20


def v_composition(members, aggregate_jaccard):
    """Compute V's two-reader composition shares from the member `source` tags
    ('E1∩E2' / 'adjudicated:E1_only' / 'adjudicated:E2_only') for the 6′ check."""
    n = len(members)
    inter = sum(1 for m in members if m.get("source") == "E1∩E2")
    e1_only = sum(1 for m in members if m.get("source") == "adjudicated:E1_only")
    e2_only = sum(1 for m in members if m.get("source") == "adjudicated:E2_only")
    e1_share = (inter + e1_only) / n if n else 0.0
    e2_share = (inter + e2_only) / n if n else 0.0
    e1_solo_share = e1_only / n if n else 0.0
    e2_solo_share = e2_only / n if n else 0.0
    return {
        "v_size": n,
        "intersection": inter,
        "e1_only": e1_only,
        "e2_only": e2_only,
        "e1_share": round(e1_share, 4),
        "e2_share": round(e2_share, 4),
        "e1_solo_share": round(e1_solo_share, 4),
        "e2_solo_share": round(e2_solo_share, 4),
        "aggregate_jaccard": round(aggregate_jaccard, 4),
    }


def assert_detector_input(manifest):
    """HARD-FAIL if detector input is NOT a genuine reconciled TWO-READER validated set.

    Threshold 6′ (ED §5.phase11.1-R) strengthens the original label/path check with a
    COMPOSITION check over V (the S21 V passed the label check while 97.6% one reader):
      - each reader's contribution share (intersection + its solo) >= 0.20;
      - neither reader's SOLO share > 0.80 (no single-reader-dominated V under a garnish);
      - aggregate Jaccard >= 0.20 (the two readers materially agree on shared prose).
    Composition is read from the manifest's `composition` block (or computed from
    `members` + `aggregate_jaccard`). The original single-reader-path/label checks are
    retained (a single-reader extraction wired as input still HARD-FAILS on label too)."""
    path = manifest.get("detector_input_path", "")
    is_v = manifest.get("detector_input_is_reconciled_validated_set", False)
    base = os.path.basename(path)
    # --- original label/path check (retained) ---
    single_reader = base in ("e1_extraction.json", "e2_extraction.json") or \
        manifest.get("source_kind") in ("E1_alone", "E2_alone", "single_reader")
    if single_reader or not is_v or base != "validated_commitment_set.json":
        return False, (f"detector input '{base}' is a single-reader / un-reconciled "
                       f"extraction (is_V={is_v}) — REFUSED [label check]")
    # --- threshold 6′ composition check ---
    comp = manifest.get("composition")
    if comp is None:
        members = manifest.get("members")
        if members is None:
            return False, ("threshold 6′: no composition/members available to verify "
                           "V is a genuine two-reader set — REFUSED")
        comp = v_composition(members, manifest.get("aggregate_jaccard", 0.0))
    e1s, e2s = comp.get("e1_share", 0.0), comp.get("e2_share", 0.0)
    e1solo, e2solo = comp.get("e1_solo_share", 0.0), comp.get("e2_solo_share", 0.0)
    jac = comp.get("aggregate_jaccard", 0.0)
    fails = []
    if e1s < T6P_CONTRIB_FLOOR:
        fails.append(f"e1_share {e1s:.4f} < {T6P_CONTRIB_FLOOR} floor")
    if e2s < T6P_CONTRIB_FLOOR:
        fails.append(f"e2_share {e2s:.4f} < {T6P_CONTRIB_FLOOR} floor")
    if e1solo > T6P_SOLO_CEILING:
        fails.append(f"e1_solo_share {e1solo:.4f} > {T6P_SOLO_CEILING} ceiling")
    if e2solo > T6P_SOLO_CEILING:
        fails.append(f"e2_solo_share {e2solo:.4f} > {T6P_SOLO_CEILING} ceiling")
    if jac < T6P_JACCARD_FLOOR:
        fails.append(f"aggregate_jaccard {jac:.4f} < {T6P_JACCARD_FLOOR} floor")
    if fails:
        return False, ("threshold 6′ FAIL — V is single-reader-dominated / low-agreement: "
                       + "; ".join(fails) + " — REFUSED")
    return True, (f"detector input == genuine two-reader V "
                  f"(e1_share={e1s:.4f} e2_share={e2s:.4f} jaccard={jac:.4f}; "
                  f"6′ floors {T6P_CONTRIB_FLOOR}/{T6P_SOLO_CEILING}/{T6P_JACCARD_FLOOR})")


def _members_from_counts(inter, e1_only, e2_only):
    """Build a V `members` list with the given composition (for fixtures)."""
    mem = []
    for i in range(inter):
        mem.append({"commitment_sig": f"i{i}", "source": "E1∩E2"})
    for i in range(e1_only):
        mem.append({"commitment_sig": f"e1_{i}", "source": "adjudicated:E1_only"})
    for i in range(e2_only):
        mem.append({"commitment_sig": f"e2_{i}", "source": "adjudicated:E2_only"})
    return mem


def build_positive_fixture_v():
    """POSITIVE fixture: a GENUINE two-reader V that 6′ must ACCEPT. Composition:
    intersection 40 / E1_only 30 / E2_only 30 over |V|=100 ⇒ e1_share=e2_share=0.70,
    each solo 0.30 (< 0.80 ceiling), Jaccard |∩|/|∪| = 40/100 = 0.40 (>= 0.20).
    Hand-authored composition (NOT the live run) so the accept-path is exercised."""
    inter, e1o, e2o = 40, 30, 30
    members = _members_from_counts(inter, e1o, e2o)
    union = inter + e1o + e2o
    jac = inter / union
    return {
        "detector_input_path": "validated_commitment_set.json",
        "detector_input_is_reconciled_validated_set": True,
        "source_kind": "reconciled_V",
        "members": members,
        "aggregate_jaccard": jac,
        "composition": v_composition(members, jac),
        "_fixture": "positive_genuine_two_reader_V",
    }


def build_negative_fixture_v():
    """NEGATIVE fixture: the S21 single-reader-dominated V that 6′ must REFUSE.
    Composition (S21 [measured]): intersection 21 / E1_only 18 / E2_only 1598 over
    |V|=1637 ⇒ e1_share=0.0238 (< 0.20 floor), e2_solo_share=0.9762 (> 0.80 ceiling),
    Jaccard ∩22/∪1638 = 0.0134 (< 0.20). Multiple 6′ failures — REFUSED."""
    inter, e1o, e2o = 21, 18, 1598
    members = _members_from_counts(inter, e1o, e2o)
    # S21 aggregate Jaccard was 0.0134 (∩22/∪1638) — use the reported value.
    jac = 0.0134
    return {
        "detector_input_path": "validated_commitment_set.json",
        "detector_input_is_reconciled_validated_set": True,
        "source_kind": "reconciled_V",
        "members": members,
        "aggregate_jaccard": jac,
        "composition": v_composition(members, jac),
        "_fixture": "negative_single_reader_dominated_V_S21",
    }


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------
def emit_distinct_event():
    os.makedirs(OUTPUTS, exist_ok=True)
    distinct = extraction_methods_distinct(E1_MECHANISM, E2_MECHANISM)
    ev = {
        "event_class": "extraction_methods_distinct_check.fire.event",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "method_E1": E1_MECHANISM,
        "method_E2": E2_MECHANISM,
        "distinct_bool": bool(distinct),
    }
    with open(DISTINCT_CHECK_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(ev) + "\n")
    return distinct, ev


def run_full(limit=None):
    distinct, ev = emit_distinct_event()
    if not distinct:
        print("HARD-FAIL: E1 and E2 share a mechanism (single reader twice REFUSED).",
              file=sys.stderr)
        sys.exit(1)

    recs = load_population(limit=limit)
    per_spec = []
    full_ledger = []
    v_all = {}
    n_inter = n_union = 0
    e2_errors = 0
    for rec in recs:
        spec_id = rec.get("spec_id")
        prose = spec_prose_window(rec)
        e1 = extract_e1(prose)
        try:
            e2 = extract_e2(prose)
        except RuntimeError as e:
            # DP#44 missing-key is fatal; per-spec E2 failure after retries is disclosed
            if "DP#44" in str(e):
                raise
            e2_errors += 1
            e2 = {}
        res = reconcile_spec(spec_id, e1, e2)
        per_spec.append({k: res[k] for k in
                         ("spec_id", "e1_count", "e2_count", "intersection",
                          "union", "symmetric_difference", "jaccard")})
        full_ledger.extend(res["ledger"])
        n_inter += res["intersection"]
        n_union += res["union"]
        for vm in res["v_members"]:
            key = f"{spec_id}::{vm['commitment_sig']}"
            v_all[key] = {"spec_id": spec_id, **vm}

    agg_jaccard = (n_inter / n_union) if n_union else 1.0
    total_sym = sum(p["symmetric_difference"] for p in per_spec)

    completeness = {
        "schema_version": "be_r_extraction_completeness.v1",
        "build_event": "BE-R part 2 — spec-extraction completeness (Done #49 / H_phase11_49)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "method_E1": E1_MECHANISM,
        "method_E2": E2_MECHANISM,
        "extraction_methods_distinct": distinct,
        "population_count": len(recs),
        "aggregate_jaccard": round(agg_jaccard, 4),
        "aggregate_intersection": n_inter,
        "aggregate_union": n_union,
        "symmetric_difference_total": total_sym,
        "symmetric_difference_ledger_length": len(full_ledger),
        "e2_per_spec_failures_after_retry": e2_errors,
        "scope_honesty": (
            "Measured = E1/E2 AGREEMENT (completeness PROXY), not ground-truth completeness. "
            "E2 is itself judgment-tier (an LLM reader). High E1/E2 disagreement is a DISCLOSED "
            "measured finding, not a failure hidden. Adjudication ADMITS all E1△E2 members to V "
            "(conservative: a commitment seen by either independent reader is a real obligation; "
            "dropping it would re-introduce the silent-false-negative #49 closes)."
        ),
        "per_spec": per_spec,                       # PIPELINE-IP-PRIVATE counts
        "symmetric_difference_ledger": full_ledger,  # PIPELINE-IP-PRIVATE contents
        "hc_11_partition": {
            "PUBLISHABLE": "parser + LLM-extraction harness + metric code + assertions",
            "PIPELINE_IP_PRIVATE": "per-spec commitment-set contents + ledger contents",
        },
    }
    # mechanical equality: ledger length == |E1 △ E2| total (no silent drops)
    completeness["ledger_equals_symmetric_difference"] = (
        len(full_ledger) == total_sym
    )

    members = list(v_all.values())
    composition = v_composition(members, agg_jaccard)
    validated = {
        "schema_version": "be_r_validated_commitment_set.v1",
        "build_event": "BE-R part 2 — reconciled validated set V (detector input)",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "detector_input_is_reconciled_validated_set": True,
        "reconciliation_rule": "V = (E1∩E2) ∪ adjudicated(E1△E2); admit-on-either-reader",
        "v_size": len(v_all),
        # threshold 6′ composition (read by --assert-detector-input); FROZEN floors
        "composition": composition,
        "aggregate_jaccard": round(agg_jaccard, 4),
        "members": members,  # PIPELINE-IP-PRIVATE
    }

    os.makedirs(OUTPUTS, exist_ok=True)
    with open(COMPLETENESS_PATH, "w", encoding="utf-8") as f:
        json.dump(completeness, f, indent=2)
    with open(VALIDATED_SET_PATH, "w", encoding="utf-8") as f:
        json.dump(validated, f, indent=2)

    print(f"population: {len(recs)} specs")
    print(f"method_E1={E1_MECHANISM}  method_E2={E2_MECHANISM}  distinct={distinct}")
    print(f"aggregate Jaccard: {completeness['aggregate_jaccard']} "
          f"(∩={n_inter} ∪={n_union})")
    print(f"|E1 △ E2| total: {total_sym}  ledger length: {len(full_ledger)}  "
          f"equal: {completeness['ledger_equals_symmetric_difference']}")
    print(f"|V|: {len(v_all)}")
    print(f"E2 per-spec failures after retry: {e2_errors}")
    return completeness, validated


def main():
    ap = argparse.ArgumentParser(description="BE-R part 2 spec-extraction pipeline (#49)")
    ap.add_argument("--methods-distinct-check", action="store_true",
                    help="assert E1/E2 mechanisms differ; exit non-zero if same")
    ap.add_argument("--assert-detector-input", action="store_true",
                    help="assert detector input == reconciled V; run negative fixture too")
    ap.add_argument("--limit", type=int, default=None,
                    help="process first N specs (bounded run; default = full population)")
    args = ap.parse_args()

    if args.methods_distinct_check:
        distinct, ev = emit_distinct_event()
        print(json.dumps(ev, indent=2))
        if not distinct:
            print("HARD-FAIL: single reader twice REFUSED.", file=sys.stderr)
            sys.exit(1)
        print("PASS: extraction_methods_distinct == True.")
        sys.exit(0)

    if args.assert_detector_input:
        # ----- POSITIVE fixture: a GENUINE two-reader V (both shares >=0.20,
        # Jaccard >=0.20). Authored here as a frozen fixture so the guard's
        # accept-path is exercised even when the live re-run V fails 6′ (the live
        # V is checked SEPARATELY below as the real run). -----
        pos_fixture = build_positive_fixture_v()
        ok_pos, msg_pos = assert_detector_input(pos_fixture)
        print(f"[positive fixture: genuine two-reader V]  pass={ok_pos}  {msg_pos}")

        # ----- NEGATIVE fixture: the S21 single-reader-dominated V (Jaccard 0.0134,
        # E1 share 2.4%, E2_only 97.6%). MUST be REFUSED by 6′. -----
        neg_fixture = build_negative_fixture_v()
        ok_neg, msg_neg = assert_detector_input(neg_fixture)
        print(f"[negative fixture: single-reader-dominated V (S21 shape)]  "
              f"pass={ok_neg}  {msg_neg}")

        # ----- the LIVE re-run V (real measured state; reported, not gated to pass) -----
        ok_live, msg_live, live_comp = None, "validated_commitment_set.json not found", None
        if os.path.isfile(VALIDATED_SET_PATH):
            v = json.load(open(VALIDATED_SET_PATH))
            live_manifest = {
                "detector_input_path": VALIDATED_SET_PATH,
                "detector_input_is_reconciled_validated_set":
                    v.get("detector_input_is_reconciled_validated_set", False),
                "source_kind": "reconciled_V",
                "composition": v.get("composition"),
                "members": v.get("members"),
                "aggregate_jaccard": v.get("aggregate_jaccard", 0.0),
            }
            ok_live, msg_live = assert_detector_input(live_manifest)
            live_comp = v.get("composition")
        print(f"[LIVE re-run V]  passes_6prime={ok_live}  {msg_live}")
        if live_comp:
            print(f"    composition: {json.dumps(live_comp)}")

        # The GUARD itself is correct iff it ACCEPTS the genuine positive and REFUSES
        # the single-reader negative. Exit 0 attests guard correctness. The live V's
        # 6′ pass/fail is an HONEST MEASURED finding reported above (HC #70) — a live
        # FAIL is disclosed for the Coach's HOLD-vs-record decision, NOT a reason to
        # tune the floors or the fixtures.
        if ok_pos and not ok_neg:
            print("PASS: guard correct (genuine two-reader V accepted, "
                  "single-reader-dominated V REFUSED).")
            if ok_live is False:
                print("DISCLOSE (HC #70): the LIVE re-run V FAILS threshold 6′ — "
                      "honest measured state, surfaced for Coach HOLD-vs-record. "
                      "NOT tuned away.")
            sys.exit(0)
        print("HARD-FAIL: guard did not behave (genuine V must pass, "
              "single-reader-dominated V must be REFUSED).", file=sys.stderr)
        sys.exit(1)

    run_full(limit=args.limit)


if __name__ == "__main__":
    main()
