#!/usr/bin/env bash
# stage_0_probe_presence_check.sh — Cycle 16 BE-H / Done #15a.
#
# Inventory the required BE-F probe primitives BEFORE Stage 1 entry. Exit
# non-zero (halt-and-surface for Builder-ARCH dispatch) if ANY required
# primitive is absent OR fails its --self-test. There is NO "proceed with
# temporary citation density" escape hatch — that is the substitution this
# layer prevents.
#
# DP#44 refuse-on-missing-precondition: a missing/failing probe HALTS Stage 0.
#
# KT-8: each present probe is IMPORTED + subprocess-EXECUTED with --self-test;
# presence-on-disk alone is NOT acceptance (a probe that exists but cannot
# distinguish known-good/known-bad is treated as ABSENT).
#
# Sink: outputs/structural_prevention_stage_0_probe_presence_events.jsonl
#       (>=1 refuse.event on any gap; >=1 pass.event when all present).
#
# Usage:
#   stage_0_probe_presence_check.sh <project_dir> [--probes-dir DIR]
#   stage_0_probe_presence_check.sh --help

set -euo pipefail

DIR="."
PROBES_DIR=""
RUN_ID_PREFIX="s13_be_h_production_stage_0_probe_presence"
while [ $# -gt 0 ]; do
    case "$1" in
        --probes-dir) PROBES_DIR="$2"; shift 2 ;;
        --run-id-prefix) RUN_ID_PREFIX="$2"; shift 2 ;;
        --help|-h)
            echo "stage_0_probe_presence_check.sh <project_dir> [--probes-dir DIR]"
            echo "  Refuses (exit non-zero) if any required probe is absent or fails self-test."
            exit 0 ;;
        *) DIR="$1"; shift ;;
    esac
done
[ -d "$DIR" ] || { echo "FAIL: project_dir '$DIR' missing" >&2; exit 1; }
DIR=$(cd "$DIR" && pwd)
PROBES_DIR="${PROBES_DIR:-$DIR/scripts/probes}"
SINK="$DIR/outputs/structural_prevention_stage_0_probe_presence_events.jsonl"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
mkdir -p "$DIR/outputs"

# Required primitives (class -> module). These are the BE-F canonical vocabulary.
REQUIRED=( "a:probe_agent_contract" "b:probe_schema" \
           "c:probe_design_decision" "d:probe_methodology_commitment" )

emit() {  # event_class refuse_bool detail_json
    python3 - "$SINK" "$1" "$RUN_ID_PREFIX" "$2" "$3" "$TS" <<'PY'
import json, sys, uuid
sink, ec, pfx, refuse, detail, ts = sys.argv[1:7]
ev = {"schema_version":"0.1",
      "namespace":"cycle_16.be_h.stage_0_probe_presence_check",
      "event_class": ec, "predicateType":"cycle16:probe_presence_v1",
      "timestamp": ts, "run_id": f"{pfx}_{uuid.uuid4().hex[:8]}",
      "payload": {**json.loads(detail), "refuse": refuse=="true"}}
with open(sink,"a") as f: f.write(json.dumps(ev)+"\n")
PY
}

# DP#44: probes dir must exist.
if [ ! -d "$PROBES_DIR" ]; then
    echo "REFUSE: probes dir absent ($PROBES_DIR) — Builder-ARCH dispatch required" >&2
    emit "stage_0_probe_presence_check.refuse.event" true \
        "{\"reason\":\"probes_dir_absent\",\"probes_dir\":\"$PROBES_DIR\"}"
    exit 3
fi

MISSING=0
PRESENT=0
for entry in "${REQUIRED[@]}"; do
    cls="${entry%%:*}"; mod="${entry##*:}"
    p="$PROBES_DIR/$cls/$mod.py"
    if [ ! -f "$p" ]; then
        echo "  ABSENT: $cls/$mod.py" >&2
        emit "stage_0_probe_presence_check.refuse.event" true \
            "{\"reason\":\"probe_absent\",\"class\":\"$cls\",\"module\":\"$mod\",\"path\":\"$p\"}"
        MISSING=$((MISSING+1)); continue
    fi
    # KT-8: physically execute --self-test; presence alone is not acceptance.
    if python3 "$p" --self-test >/dev/null 2>&1; then
        PRESENT=$((PRESENT+1))
    else
        rc=$?
        echo "  PRESENT-BUT-FAILS-SELF-TEST: $cls/$mod.py (exit $rc) -> treated as absent" >&2
        emit "stage_0_probe_presence_check.refuse.event" true \
            "{\"reason\":\"probe_self_test_failed\",\"class\":\"$cls\",\"module\":\"$mod\",\"self_test_exit\":$rc}"
        MISSING=$((MISSING+1))
    fi
done

if [ "$MISSING" -gt 0 ]; then
    echo "BLOCKED: $MISSING required probe(s) missing/failing — NO citation-density escape hatch." >&2
    exit 1
fi
echo "CLEAR: all ${#REQUIRED[@]} required probes present + pass self-test."
emit "stage_0_probe_presence_check.pass.event" false \
    "{\"reason\":\"all_required_probes_present_and_self_test_pass\",\"present\":$PRESENT,\"required\":${#REQUIRED[@]}}"
exit 0
