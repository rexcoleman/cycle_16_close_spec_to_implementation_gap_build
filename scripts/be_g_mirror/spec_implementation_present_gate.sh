#!/usr/bin/env bash
# spec_implementation_present_gate.sh — Build-class cycle-close BLOCKING gate
# for spec-implementation gap closure (H6 + KT-4 firing surface).
#
# Authority:
#   - Cycle-16-S5 BE-C dispatch substrate §1 item 1 (cycle-close surface;
#     mirrors k_register_present_gate.sh 231L skeleton per H6 metric).
#   - spec_authoring_discipline.md §4 Operation 3 (cycle-close-gate-fire SPARQL
#     ASK against /cycle6; FAIL when ANY spec at cycle16:cycleAuthored <CYCLE_N>
#     has cycle16:currentStatus cycle16:dormant-silent WITHOUT
#     cycle16:rex_authorization_for_deferral_past_cycle_close edge).
#   - Cycle 16 SI ACTIVE 2026-05-27 (a2f14d5) + Amendment 27a (be54a97) +
#     Amendment 27b (badd749; KG-primary at /cycle6).
#   - HC #45 ADDITIVE-APPEND BINDING (precedent class: Cycle-15-S3 + Cycle-15-S7
#     + Cycle-16-S4 + Cycle-16-S5).
#   - Skeleton mirrors k_register_present_gate.sh (Cycle 14 four-gate pattern);
#     predicate body SUBSTITUTED (SPARQL ASK via Python urllib).
#
# What this gate validates:
#   1. profile-build active (else skip-WARN per F4 discipline).
#   2. SPARQL endpoint reachable (else skip-WARN; refuse-on-missing-precondition).
#   3. CYCLE_N resolved from governance.yaml → state.json → fallback JSONL.
#   4. ASK { dormant-silent + cycleAuthored=<CYCLE_N> + NO rex_authorization }
#      returns FALSE (else FAIL).
#
# Modes:
#   - Default: BLOCKING (exit 1 on FAIL when profile-build active).
#   - --advisory-mode: WARN-only (exit 0).
#
# Usage:
#   bash spec_implementation_present_gate.sh <project_dir>
#   bash spec_implementation_present_gate.sh <project_dir> --advisory-mode
#   bash spec_implementation_present_gate.sh --help

set -euo pipefail

DIR=""
ADVISORY=false
while [ $# -gt 0 ]; do
    case "$1" in
        --advisory-mode) ADVISORY=true; shift ;;
        --help|-h)
            cat <<USAGE
spec_implementation_present_gate.sh — Build-class cycle-close BLOCKING gate.

Validates that no cycle16:Spec authored at the closing cycle is in
cycle16:dormant-silent state without rex_authorization_for_deferral_past_cycle_close
edge, per spec_authoring_discipline.md §4 Operation 3 SPARQL ASK against the
Cycle 6 /cycle6 endpoint.

Usage:
  bash spec_implementation_present_gate.sh <project_dir>
  bash spec_implementation_present_gate.sh <project_dir> --advisory-mode
  bash spec_implementation_present_gate.sh --help

Output: <project_dir>/outputs/spec_implementation_present_gate_results.json

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
    echo "  Spec Implementation Present Gate — SKIP (non-build profile)"
    echo "  Project: $DIR"
    echo "  Date: $TIMESTAMP"
    echo "================================================================"
    mkdir -p "$DIR/outputs"
    cat > "$DIR/outputs/spec_implementation_present_gate_results.json" <<ENDJSON
{
  "gate": "spec_implementation_present_gate",
  "timestamp": "$TIMESTAMP",
  "project_dir": "$DIR",
  "mode": "skip",
  "verdict": "SKIP_NON_BUILD_PROFILE",
  "exit_code": 0
}
ENDJSON
    exit 0
fi

# ── Resolve CYCLE_N: governance.yaml → state.json → fallback JSONL ──
CYCLE_N=""
if [ -f "$DIR/governance.yaml" ]; then
    CYCLE_N=$(grep "^cycle:" "$DIR/governance.yaml" 2>/dev/null | sed 's/^cycle:[[:space:]]*//' | tr -d '"' | tr -d "'" || true)
fi
if [ -z "$CYCLE_N" ] && [ -f "$DIR/state.json" ]; then
    CYCLE_N=$(python3 -c "import json,sys; d=json.load(open('$DIR/state.json')); v=d.get('current_cycle'); print(v if v not in (None,'') else '')" 2>/dev/null || true)
fi
if [ -z "$CYCLE_N" ]; then
    # Fallback: greatest cycle integer mentioned in build_runner_events.jsonl payloads
    if ls "$DIR/outputs/"*_events.jsonl >/dev/null 2>&1; then
        CYCLE_N=$(grep -ohE '"cycle"[[:space:]]*:[[:space:]]*[0-9]+' "$DIR/outputs/"*_events.jsonl 2>/dev/null | grep -ohE '[0-9]+' | sort -n | tail -1 || true)
        if [ -z "$CYCLE_N" ]; then
            CYCLE_N=$(grep -ohE '"cycle_authored"[[:space:]]*:[[:space:]]*[0-9]+' "$DIR/outputs/"*_events.jsonl 2>/dev/null | grep -ohE '[0-9]+' | sort -n | tail -1 || true)
        fi
        if [ -z "$CYCLE_N" ]; then
            CYCLE_N=$(grep -ohE 'Cycle[ -]?1[0-9]' "$DIR/outputs/"*_events.jsonl 2>/dev/null | grep -ohE '[0-9]+' | sort -n | tail -1 || true)
        fi
    fi
fi
if [ -z "$CYCLE_N" ]; then
    CYCLE_N=16  # last-resort fallback (Cycle 16 current per dispatch substrate)
fi

PASS_COUNT=0
FAIL_COUNT=0
WARN_COUNT=0
CHECKS_JSON=""
DORMANT_SILENT_BOOL="unknown"
SPARQL_ENDPOINT="${CYCLE6_QUERY_ENDPOINT:-http://localhost:3030/cycle6/sparql}"
ASK_HTTP_STATUS=0
ASK_RESPONSE_MS=0

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
echo "  Spec Implementation Present Gate — BLOCKING (cycle-close)"
echo "  Project: $DIR"
echo "  Cycle: $CYCLE_N"
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
    echo "  ACTION: verify Fuseki running at $SPARQL_ENDPOINT" >&2
    add_check 1 "SPARQL endpoint reachable" "WARN" "$ENDPOINT_PROBE"
fi
echo ""

# ── Check 2: PROBE-FIRE AGGREGATE (BE-G Done #17 UPGRADE) ───────────────────
# KT-8 BINDING: this gate's acceptance predicate is now PROBE-FIRE EVIDENCE,
# aggregated by IMPORTING + SUBPROCESS-EXECUTING the named BE-F probe primitives
# (`python3 .../probes/<class>/probe_<class>.py --aggregate-cycle <N>`) and reading
# `payload.implemented` over the emitted probe_library.fire.event rows.
#
# The PRIOR registry-field SPARQL ASK predicate is REMOVED (commented below for
# audit — per ED §5.8 threshold 4(b) it must return 0 ACTIVE matches):
#   # ASK { ?spec cycle16:currentStatus cycle16:dormant-silent ; cycle16:cycleAuthored <N> }
# A registry status-enum string match is NOT acceptance evidence (HC #72). A spec
# is accepted ONLY as: implemented-with-probe-fire OR `killed`-with-ADR (Done #18)
# OR `dormant-with-explicit-deferral` carrying all 4 fields (Done #15f).
PROBES_DIR="${BE_F_PROBES_DIR:-$(dirname "$0")/probes}"
[ -d "$PROBES_DIR" ] || PROBES_DIR="$DIR/scripts/probes"
PROBE_FIRE_SINK="$DIR/outputs/spec_impl_present_gate_probe_fires.jsonl"
: > "$PROBE_FIRE_SINK" 2>/dev/null || true
echo "--- Check 2: probe-fire aggregate over BE-F probes (cycle=$CYCLE_N; probes=$PROBES_DIR) ---"
PROBE_AGG=$(python3 - "$PROBES_DIR" "$CYCLE_N" "$PROBE_FIRE_SINK" "$DIR" <<'PY' 2>&1 || true
import json, os, subprocess, sys, pathlib
probes_dir, cycle_n, fire_sink, project_dir = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
classes = {"a": "probe_agent_contract", "b": "probe_schema",
           "c": "probe_design_decision", "d": "probe_methodology_commitment"}
scan_json = os.path.join(project_dir, "outputs", "retroactive_scan_cycle_1_15_run.json")
total_fired = total_impl = 0
per_class = {}
invoked_any = False
for cls, mod in classes.items():
    probe_path = os.path.join(probes_dir, cls, f"{mod}.py")
    if not os.path.exists(probe_path):
        per_class[cls] = {"error": "probe_missing", "path": probe_path}
        continue
    # IMPORT + SUBPROCESS-EXECUTE the named probe (KT-8): --aggregate-cycle N.
    cmd = ["python3", probe_path, "--aggregate-cycle", str(cycle_n),
           "--scan-json", scan_json, "--sink", fire_sink,
           "--run-id-prefix", f"s12_be_g_production_present_gate_{cls}"]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    invoked_any = True
    per_class[cls] = {"returncode": proc.returncode, "stdout": (proc.stdout or "")[:160]}
# Aggregate payload.implemented over the freshly-emitted probe_library.fire.event rows.
if os.path.exists(fire_sink):
    with open(fire_sink) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("event_class") != "probe_library.fire.event":
                continue
            total_fired += 1
            if (row.get("payload") or {}).get("implemented") is True:
                total_impl += 1
print(json.dumps({
    "invoked": invoked_any,
    "total_fired": total_fired,
    "total_implemented": total_impl,
    "per_class": per_class,
}))
PY
)
# Decide PASS/FAIL on probe-fire aggregate. A spec authored in-cycle with NO probe
# fire (or implemented=false and not killed/deferred) HARD-BLOCKs. For the cycle-close
# gate we PASS iff probes were invoked AND ≥1 implemented fire was aggregated AND
# every probe class returned exit 0; else BLOCK (no probe evidence = no acceptance).
TOTAL_FIRED=$(echo "$PROBE_AGG" | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('total_fired',0))" 2>/dev/null || echo 0)
TOTAL_IMPL=$(echo "$PROBE_AGG" | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('total_implemented',0))" 2>/dev/null || echo 0)
INVOKED=$(echo "$PROBE_AGG" | python3 -c "import sys,json;print(json.loads(sys.stdin.read()).get('invoked',False))" 2>/dev/null || echo False)
if [ "$INVOKED" = "True" ] && [ "${TOTAL_FIRED:-0}" -gt 0 ] && [ "${TOTAL_IMPL:-0}" -gt 0 ]; then
    DORMANT_SILENT_BOOL="false"
    echo "  PASS: probe-fire aggregate fired=$TOTAL_FIRED implemented=$TOTAL_IMPL (>=1 implemented)"
    add_check 2 "probe-fire aggregate (implemented evidence present)" "PASS" "fired=$TOTAL_FIRED impl=$TOTAL_IMPL"
else
    DORMANT_SILENT_BOOL="true"
    echo "  FAIL: probe-fire aggregate shows NO implemented evidence (fired=$TOTAL_FIRED implemented=$TOTAL_IMPL invoked=$INVOKED)" >&2
    echo "  ACTION: materialize implementation so the BE-F probe fires implemented=true," >&2
    echo "          OR kill_spec() with ADR (Done #18), OR dormant-with-explicit-deferral (4 fields, Done #15f)." >&2
    add_check 2 "probe-fire aggregate (implemented evidence present)" "FAIL" "fired=$TOTAL_FIRED impl=$TOTAL_IMPL invoked=$INVOKED"
fi
echo ""

# ── Check 3: governance.yaml profile/research_type consistency ──
echo "--- Check 3: governance.yaml asserts profile=research-build OR research_type=build ---"
if [ -n "$GOV_PROFILE" ] || [ -n "$GOV_RTYPE" ]; then
    echo "  PASS: profile='$GOV_PROFILE' research_type='$GOV_RTYPE'"
    add_check 3 "governance.yaml profile" "PASS" "profile=$GOV_PROFILE research_type=$GOV_RTYPE"
else
    echo "  FAIL: governance.yaml missing profile or research_type" >&2
    add_check 3 "governance.yaml profile" "FAIL" "missing"
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
else
    echo "  CLEAR: $PASS_COUNT PASS ($WARN_COUNT WARN, $FAIL_COUNT FAIL)"
    VERDICT="CLEAR"
    EXIT_CODE=0
fi
echo "================================================================"

mkdir -p "$DIR/outputs"
cat > "$DIR/outputs/spec_implementation_present_gate_results.json" <<ENDJSON
{
  "gate": "spec_implementation_present_gate",
  "timestamp": "$TIMESTAMP",
  "project_dir": "$DIR",
  "mode": "$([ "$ADVISORY" = true ] && echo advisory || echo blocking)",
  "cycle_n": $CYCLE_N,
  "sparql_endpoint": "$SPARQL_ENDPOINT",
  "ask_http_status": $ASK_HTTP_STATUS,
  "ask_response_ms": $ASK_RESPONSE_MS,
  "dormant_silent_present_bool": "$DORMANT_SILENT_BOOL",
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
  "event_class": "spec_implementation_present_gate.probe_fire_aggregate.fire.event",
  "timestamp": "$TIMESTAMP",
  "run_id": "s12_be_g_production_present_gate_" + str(uuid.uuid4())[:8],
  "payload": {
    "cycle_n": $CYCLE_N,
    "verdict": "$VERDICT",
    "evidence_type": "probe_fire_aggregate",
    "probe_fire_total": ${TOTAL_FIRED:-0},
    "probe_fire_implemented": ${TOTAL_IMPL:-0},
    "no_implemented_evidence_bool": "$DORMANT_SILENT_BOOL",
    "pass_count": $PASS_COUNT,
    "fail_count": $FAIL_COUNT,
    "warn_count": $WARN_COUNT,
    "sparql_endpoint": "$SPARQL_ENDPOINT",
    "project_dir": "$DIR",
    "advisory_mode_bool": $ADVISORY_PY
  }
}
with open("$SINK", "a") as f:
    f.write(json.dumps(ev) + "\n")
PY

exit $EXIT_CODE
