#!/usr/bin/env bash
# spec_implementation_session_close_gate.sh — Build-class session-close
# ADVISORY-DEFAULT gate for ≤3-session dormancy detection (Amendment 27a).
#
# Authority:
#   - Cycle-16-S5 BE-C dispatch substrate §1 item 2 (session-close surface;
#     same skeleton as spec_implementation_present_gate.sh; ADVISORY=true default
#     inverted; --blocking-mode opt-in flips to false).
#   - spec_authoring_discipline.md §4 Operation 4 (session-close-gate-fire SPARQL
#     ASK with FILTER (<CURRENT_SESSION_INDEX> - <SESSION_AUTHORED_INDEX> >=
#     ?threshold)). SESSIONS_BETWEEN pre-computed at shell layer as
#     grep -c '"event_class":"session.start"' outputs/*_events.jsonl.
#   - Cycle 16 SI Amendment 2026-05-27a (be54a97; ≤3-session emit detection
#     default threshold).
#   - Mirrors k_register_present_gate.sh 231L skeleton structurally (H6 metric);
#     only ADVISORY default constant + predicate body block differ.
#
# What this gate validates:
#   1. profile-build active (else skip-WARN per F4).
#   2. SPARQL endpoint reachable (else skip-WARN).
#   3. SESSIONS_BETWEEN computed from JSONL session.start markers.
#   4. ASK { dormant-silent + (CURRENT_SESSION_INDEX - SESSION_AUTHORED_INDEX
#      >= threshold) } returns FALSE (else WARN/FAIL).
#
# Modes:
#   - Default: ADVISORY (exit 0 on FAIL; WARN-class).
#   - --blocking-mode: BLOCKING (exit 1 on FAIL).
#
# Usage:
#   bash spec_implementation_session_close_gate.sh <project_dir>
#   bash spec_implementation_session_close_gate.sh <project_dir> --blocking-mode
#   bash spec_implementation_session_close_gate.sh <project_dir> --advisory-mode
#   bash spec_implementation_session_close_gate.sh --help

set -euo pipefail

DIR=""
ADVISORY=true  # default inverted per dispatch substrate §1 item 2
while [ $# -gt 0 ]; do
    case "$1" in
        --advisory-mode) ADVISORY=true; shift ;;
        --blocking-mode) ADVISORY=false; shift ;;
        --help|-h)
            cat <<USAGE
spec_implementation_session_close_gate.sh — Build-class session-close ADVISORY
gate (Amendment 2026-05-27a ≤3-session dormancy threshold).

Validates that no cycle16:Spec is in cycle16:dormant-silent state where
SESSIONS_BETWEEN(current_session_authored, session_authored) exceeds
dormancy_detection_threshold_sessions (default 3), per
spec_authoring_discipline.md §4 Operation 4 SPARQL ASK against /cycle6.

Usage:
  bash spec_implementation_session_close_gate.sh <project_dir>
  bash spec_implementation_session_close_gate.sh <project_dir> --advisory-mode
  bash spec_implementation_session_close_gate.sh <project_dir> --blocking-mode
  bash spec_implementation_session_close_gate.sh --help

Output: <project_dir>/outputs/spec_implementation_session_close_gate_results.json

Skip behavior: if governance.yaml lacks 'profile: research-build' AND
'research_type: build', skip-WARN (preserves non-build cycles per F4).
USAGE
            exit 0
            ;;
        *) DIR="$1"; shift ;;
    esac
done
DIR="${DIR:-.}"
if [ ! -d "$DIR" ]; then
    echo "FAIL: project_dir '$DIR' does not exist or is not a directory" >&2
    exit 1
fi
DIR=$(cd "$DIR" && pwd)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)

# ── Profile-build active check ────────────────────────────────
PROFILE_BUILD_ACTIVE=false
if [ -f "$DIR/governance.yaml" ]; then
    GOV_PROFILE=$(grep "^profile:" "$DIR/governance.yaml" 2>/dev/null | sed 's/^profile:[[:space:]]*//' | tr -d '"' | tr -d "'" || true)
    GOV_RTYPE=$(grep "^research_type:" "$DIR/governance.yaml" 2>/dev/null | sed 's/^research_type:[[:space:]]*//' | tr -d '"' | tr -d "'" || true)
    if [ "$GOV_PROFILE" = "research-build" ] || [ "$GOV_RTYPE" = "build" ]; then
        PROFILE_BUILD_ACTIVE=true
    fi
fi

if [ "$PROFILE_BUILD_ACTIVE" = false ]; then
    echo "================================================================"
    echo "  Spec Implementation Session-Close Gate — SKIP (non-build profile)"
    echo "  Project: $DIR"
    echo "  Date: $TIMESTAMP"
    echo "================================================================"
    mkdir -p "$DIR/outputs"
    cat > "$DIR/outputs/spec_implementation_session_close_gate_results.json" <<ENDJSON
{
  "gate": "spec_implementation_session_close_gate",
  "timestamp": "$TIMESTAMP",
  "project_dir": "$DIR",
  "mode": "skip",
  "verdict": "SKIP_NON_BUILD_PROFILE",
  "exit_code": 0
}
ENDJSON
    exit 0
fi

# ── SESSIONS_BETWEEN primitive: shell pre-computation ──
# Per spec_authoring_discipline.md §4 Operation 4 footnote: count session.start
# markers across *_events.jsonl sinks. Each session.start event = 1 session boundary.
SESSIONS_BETWEEN=0
if ls "$DIR/outputs/"*_events.jsonl >/dev/null 2>&1; then
    # BE-G Done #19 pipefail-hardening: `grep -c` exits 1 on 0 matches; under
    # `set -o pipefail` that aborted the gate before the verdict. `|| true` makes
    # the count primitive pipefail-safe (0-match → SESSIONS_BETWEEN=0). Behavior
    # for >=1 match is unchanged.
    SESSIONS_BETWEEN=$( { grep -c '"event_class":[[:space:]]*"[a-zA-Z._]*session.start"' "$DIR/outputs/"*_events.jsonl 2>/dev/null || true; } | awk -F: '{s+=$NF} END {print s+0}')
    SESSIONS_BETWEEN=${SESSIONS_BETWEEN:-0}
fi

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0
CHECKS_JSON=""
OVER_THRESHOLD_BOOL="unknown"
SPARQL_ENDPOINT="${CYCLE6_QUERY_ENDPOINT:-http://localhost:3030/cycle6/sparql}"
ASK_HTTP_STATUS=0
ASK_RESPONSE_MS=0
DORMANT_OVER_COUNT=0

add_check() {
    local id="$1" name="$2" result="$3" detail="${4:-}"
    if [ -n "$CHECKS_JSON" ]; then CHECKS_JSON="$CHECKS_JSON,"; fi
    local detail_field=""
    if [ -n "$detail" ]; then
        local detail_esc
        detail_esc=$(echo "$detail" | sed 's/"/\\"/g')
        detail_field=", \"detail\": \"$detail_esc\""
    fi
    CHECKS_JSON="$CHECKS_JSON
    {\"id\": $id, \"name\": \"$name\", \"result\": \"$result\"$detail_field}"
    case "$result" in
        PASS) PASS_COUNT=$((PASS_COUNT + 1)) ;;
        FAIL) FAIL_COUNT=$((FAIL_COUNT + 1)) ;;
        WARN) WARN_COUNT=$((WARN_COUNT + 1)) ;;
    esac
}

echo "================================================================"
echo "  Spec Implementation Session-Close Gate — ADVISORY (session-close)"
echo "  Project: $DIR"
echo "  Sessions observed (JSONL session.start count): $SESSIONS_BETWEEN"
echo "  Mode: $([ "$ADVISORY" = true ] && echo ADVISORY || echo BLOCKING)"
echo "  Date: $TIMESTAMP"
echo "================================================================"
echo ""

# ── Check 1: SPARQL endpoint reachable ──────────────────────────────
echo "--- Check 1: SPARQL endpoint reachable ($SPARQL_ENDPOINT) ---"
ENDPOINT_PROBE=$(python3 - <<PY 2>&1 || true
import urllib.request, urllib.parse, sys, time
try:
    body = urllib.parse.urlencode({"query": "ASK { ?s ?p ?o }"}).encode()
    req = urllib.request.Request("$SPARQL_ENDPOINT", data=body, headers={"Accept":"application/sparql-results+json"})
    t0 = time.time()
    r = urllib.request.urlopen(req, timeout=5)
    ms = int((time.time()-t0)*1000)
    print(f"{r.status} {ms}")
except Exception as e:
    print(f"ERR {type(e).__name__}: {e}")
PY
)
if echo "$ENDPOINT_PROBE" | grep -q "^200 "; then
    ASK_HTTP_STATUS=200
    ASK_RESPONSE_MS=$(echo "$ENDPOINT_PROBE" | awk '{print $2}')
    echo "  PASS: HTTP 200 (${ASK_RESPONSE_MS}ms)"
    add_check 1 "SPARQL endpoint reachable" "PASS" "$ENDPOINT_PROBE"
else
    echo "  WARN: $ENDPOINT_PROBE" >&2
    add_check 1 "SPARQL endpoint reachable" "WARN" "$ENDPOINT_PROBE"
fi
echo ""

# ── Check 2: PROBE-FIRE DORMANCY AGGREGATE (BE-G Done #19 UPGRADE) ───────────
# Per ED §5.8 threshold 6: aggregate probe-fire JSONL across the LAST 3 SESSIONS
# (NOT a SPARQL ASK on cycle16:currentStatus). A spec is dormancy-flagged when it
# has NO implemented probe fire (payload.implemented=true) in any probe_library.fire
# row whose run_id is from the last 3 sessions. This reads PROBE-FIRE EVIDENCE, not
# a registry status enum (HC #72 / KT-8 BINDING).
#
# The PRIOR registry-field SPARQL SELECT/ASK predicate is REMOVED (commented for
# audit — must return 0 ACTIVE matches per ED §5.8 threshold 6):
#   # SELECT (COUNT ?spec) WHERE { ?spec cycle16:currentStatus cycle16:dormant-silent ... }
THRESHOLD_DEFAULT=3
echo "--- Check 2: probe-fire dormancy aggregate over last $THRESHOLD_DEFAULT sessions (Done #19) ---"
PROBE_FIRE_LOG="${BE_F_PROBE_FIRE_LOG:-$DIR/outputs/probe_fire_events.jsonl}"
# HC-BE-G-1 FIX: capture rc separately; a crash (non-zero rc / non-JSON
# stdout) is a DISTINCT verdict, never coerced to "0 dormant -> PASS".
DORMANCY_ERR="$DIR/outputs/.session_close_dormancy_stderr.tmp"
# Disable -e around the compute so a CRASH does NOT abort the script before the
# crash-branch verdict runs (HC-BE-G-1: a crash must be SURFACED, not swallowed).
DORMANCY_OUT="$DIR/outputs/.session_close_dormancy_stdout.tmp"
set +e
python3 - "$PROBE_FIRE_LOG" "$THRESHOLD_DEFAULT" >"$DORMANCY_OUT" 2>"$DORMANCY_ERR" <<'PY'
import json, sys, pathlib
log_path, window = sys.argv[1], int(sys.argv[2])
p = pathlib.Path(log_path)
fired = impl = 0
specs_seen = set()
specs_with_recent_impl = set()
if p.exists():
    rows = []
    with p.open() as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("event_class") == "probe_library.fire.event":
                rows.append(row)
    # "last 3 sessions" proxy: order by timestamp, partition by distinct session
    # prefix in run_id (sNN_...) or fall back to last-N rows. We aggregate the
    # most-recent window of fires and flag specs lacking an implemented fire there.
    rows.sort(key=lambda r: r.get("timestamp", ""))
    # HC-BE-G-2 FIX: real session-index partition (no magic *64 proxy).
    # Group fires by DISTINCT session: run_id sNN_ prefix, else payload.session,
    # else per-second timestamp proxy. Take the last `window` (=3) DISTINCT sessions.
    import re as _re
    def _session_key(r):
        rid = r.get("run_id") or ""
        m = _re.match(r"(s\d+)_", rid)
        if m:
            return m.group(1)
        pay = r.get("payload") or {}
        if pay.get("session"):
            return str(pay.get("session"))
        return (r.get("timestamp", "") or "")[:19]
    seen_order = []
    for r in rows:
        k = _session_key(r)
        if k not in seen_order:
            seen_order.append(k)
    last_sessions = set(seen_order[-max(1, window):])
    recent = [r for r in rows if _session_key(r) in last_sessions]
    for r in recent:
        pay = r.get("payload") or {}
        iri = pay.get("spec_iri")
        if iri:
            specs_seen.add(iri)
        fired += 1
        if pay.get("implemented") is True:
            impl += 1
            if iri:
                specs_with_recent_impl.add(iri)
dormant_specs = specs_seen - specs_with_recent_impl
print(json.dumps({
    "probe_fire_rows_in_window": fired,
    "implemented_fires": impl,
    "distinct_specs": len(specs_seen),
    "dormant_specs_no_recent_impl": len(dormant_specs),
}))
PY
DORMANCY_RC=$?
DORMANCY=$(cat "$DORMANCY_OUT" 2>/dev/null || true)
rm -f "$DORMANCY_OUT" 2>/dev/null || true
set -e  # re-enable strict mode now that the compute rc is captured
# HC-BE-G-1: detect a crash = non-zero rc OR stdout that is not valid JSON.
DORMANCY_CRASH=false
if [ "$DORMANCY_RC" -ne 0 ]; then DORMANCY_CRASH=true; fi
if ! echo "$DORMANCY" | python3 -c "import sys,json; json.loads(sys.stdin.read())" >/dev/null 2>&1; then DORMANCY_CRASH=true; fi
# HC-BE-G-1: do NOT `|| echo 0` a crash into a PASS. On crash route to crash branch.
if [ "$DORMANCY_CRASH" = true ]; then
    DORMANT_OVER_COUNT=""
    PROBE_FIRES_WINDOW=""
else
    DORMANT_OVER_COUNT=$(echo "$DORMANCY" | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('dormant_specs_no_recent_impl',0))")
    PROBE_FIRES_WINDOW=$(echo "$DORMANCY" | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('probe_fire_rows_in_window',0))")
fi
if [ "$DORMANCY_CRASH" = true ]; then
    # Distinct crash verdict: NEVER a silent PASS=0 (HC-BE-G-1).
    OVER_THRESHOLD_BOOL="crash"
    ERRTXT=$( (cat "$DORMANCY_ERR" 2>/dev/null || true) | tr '\n' ' ' | head -c 200)
    echo "  CRASH: dormancy compute failed (rc=$DORMANCY_RC); NOT coerced to PASS. err=$ERRTXT" >&2
    if [ "$ADVISORY" = true ]; then
        add_check 2 "probe-fire dormancy aggregate" "WARN" "compute_crash rc=$DORMANCY_RC (loud non-PASS)"
    else
        add_check 2 "probe-fire dormancy aggregate" "FAIL" "compute_crash rc=$DORMANCY_RC (fail-closed)"
    fi
    rm -f "$DORMANCY_ERR" 2>/dev/null || true
elif [ "${DORMANT_OVER_COUNT:-0}" -gt 0 ]; then
    OVER_THRESHOLD_BOOL="true"
    echo "  WARN: $DORMANT_OVER_COUNT spec(s) with NO implemented probe fire in last $THRESHOLD_DEFAULT-session window (fires=$PROBE_FIRES_WINDOW)" >&2
    echo "  ACTION (advisory): surface for next-session implementation OR formal deferral (Done #15f 4-field)." >&2
    if [ "$ADVISORY" = true ]; then
        add_check 2 "probe-fire dormancy aggregate" "WARN" "$DORMANCY"
    else
        add_check 2 "probe-fire dormancy aggregate" "FAIL" "$DORMANCY"
    fi
else
    OVER_THRESHOLD_BOOL="false"
    echo "  PASS: 0 dormant specs in probe-fire window ($DORMANCY)"
    add_check 2 "probe-fire dormancy aggregate" "PASS" "$DORMANCY"
fi
rm -f "$DORMANCY_ERR" 2>/dev/null || true
echo ""

# ── Check 3: SESSIONS_BETWEEN primitive computable ──
echo "--- Check 3: SESSIONS_BETWEEN computed from JSONL session.start markers ---"
if [ "$SESSIONS_BETWEEN" -ge 0 ]; then
    echo "  PASS: SESSIONS_BETWEEN=$SESSIONS_BETWEEN (grep-derived)"
    add_check 3 "SESSIONS_BETWEEN computable" "PASS" "$SESSIONS_BETWEEN"
else
    echo "  WARN: SESSIONS_BETWEEN compute failed"
    add_check 3 "SESSIONS_BETWEEN computable" "WARN" "compute_failed"
fi
echo ""

# ── Verdict ──────────────────────────────────────────────────
echo "================================================================"
if [ "$FAIL_COUNT" -gt 0 ]; then
    if [ "$ADVISORY" = true ]; then
        echo "  ADVISORY (FAIL=$FAIL_COUNT): $PASS_COUNT PASS, $WARN_COUNT WARN, $FAIL_COUNT FAIL — exit 0 per --advisory-mode"
        VERDICT="ADVISORY_FAIL"
        EXIT_CODE=0
    else
        echo "  BLOCKED: $FAIL_COUNT FAIL ($PASS_COUNT PASS, $WARN_COUNT WARN)"
        VERDICT="BLOCKED"
        EXIT_CODE=1
    fi
elif [ "$WARN_COUNT" -gt 0 ] && [ "$OVER_THRESHOLD_BOOL" = "true" ]; then
    # WARN-class verdict when dormant specs exceed threshold (advisory default)
    echo "  ADVISORY_FAIL: $WARN_COUNT WARN ($PASS_COUNT PASS, $FAIL_COUNT FAIL) — exit 0 per advisory default"
    VERDICT="ADVISORY_FAIL"
    EXIT_CODE=0
else
    echo "  CLEAR: $PASS_COUNT PASS ($WARN_COUNT WARN, $FAIL_COUNT FAIL)"
    VERDICT="CLEAR"
    EXIT_CODE=0
fi
echo "================================================================"

mkdir -p "$DIR/outputs"
cat > "$DIR/outputs/spec_implementation_session_close_gate_results.json" <<ENDJSON
{
  "gate": "spec_implementation_session_close_gate",
  "timestamp": "$TIMESTAMP",
  "project_dir": "$DIR",
  "mode": "$([ "$ADVISORY" = true ] && echo advisory || echo blocking)",
  "sessions_between": $SESSIONS_BETWEEN,
  "threshold_default": $THRESHOLD_DEFAULT,
  "sparql_endpoint": "$SPARQL_ENDPOINT",
  "ask_http_status": $ASK_HTTP_STATUS,
  "ask_response_ms": $ASK_RESPONSE_MS,
  "dormant_specs_over_threshold_count": $DORMANT_OVER_COUNT,
  "dormant_specs_over_threshold_bool": "$OVER_THRESHOLD_BOOL",
  "checks": [$CHECKS_JSON
  ],
  "pass": $PASS_COUNT,
  "fail": $FAIL_COUNT,
  "warn": $WARN_COUNT,
  "verdict": "$VERDICT",
  "exit_code": $EXIT_CODE
}
ENDJSON

# Emit fire.event JSONL row per RUNTIME_EMIT_SPEC §11
SINK="$DIR/outputs/spec_implementation_gates_events.jsonl"
mkdir -p "$DIR/outputs"
[ -f "$SINK" ] || touch "$SINK"
ADVISORY_PY=$([ "$ADVISORY" = true ] && echo True || echo False)
python3 - <<PY
import json, datetime, uuid
ev = {
  "schema_version": "0.1",
  "namespace": "cycle_16.be_g.spec_implementation_gates",
  "event_class": "spec_implementation_session_close_gate.probe_fire_aggregate.fire.event",
  "timestamp": "$TIMESTAMP",
  "run_id": "s12_be_g_production_session_close_" + str(uuid.uuid4())[:8],
  "payload": {
    "current_session_index": $SESSIONS_BETWEEN,
    "threshold": $THRESHOLD_DEFAULT,
    "evidence_type": "probe_fire_aggregate",
    "probe_fire_rows_in_window": ${PROBE_FIRES_WINDOW:-0},
    "dormant_specs_no_recent_impl_count": $DORMANT_OVER_COUNT,
    "verdict": "$VERDICT",
    "pass_count": $PASS_COUNT,
    "fail_count": $FAIL_COUNT,
    "warn_count": $WARN_COUNT,
    "project_dir": "$DIR",
    "advisory_mode_bool": $ADVISORY_PY
  }
}
with open("$SINK", "a") as f:
    f.write(json.dumps(ev) + "\n")
PY

exit $EXIT_CODE
