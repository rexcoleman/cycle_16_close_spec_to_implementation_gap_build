#!/usr/bin/env bash
# probe_coverage_check.sh — Cycle 16 BE-H / Done #15d.
#
# At FINDINGS close: for every class the cycle governs (A/B/C/D), require >=1
# PRODUCTION probe fire with a non-zero implemented count. Smoke / self-test
# fires are EXCLUDED via the run_id-prefix discriminator (*_smoke_* and
# *_self_test_* run_ids are NOT counted). A class with 0 production fires ->
# refuse (exit non-zero) — this is the recursive-meta-failure guard (KT-10).
#
# KT-8: this gate IMPORTS + subprocess-EXECUTES each named BE-F probe with
# --aggregate-cycle N to PRODUCE the fires it then counts; it never reads a
# pre-existing status enum or string-matches a probe ID.
#
# DP#44 refuse-on-missing-precondition: probes dir absent -> refuse.
#
# Sink: outputs/structural_prevention_probe_coverage_events.jsonl
#
# Usage:
#   probe_coverage_check.sh <project_dir> [--cycle N] [--probes-dir DIR]
#   probe_coverage_check.sh --help

set -euo pipefail

DIR="."
CYCLE_N=""
PROBES_DIR=""
RUN_ID_PREFIX="s13_be_h_production_probe_coverage"
while [ $# -gt 0 ]; do
    case "$1" in
        --cycle) CYCLE_N="$2"; shift 2 ;;
        --probes-dir) PROBES_DIR="$2"; shift 2 ;;
        --run-id-prefix) RUN_ID_PREFIX="$2"; shift 2 ;;
        --help|-h)
            echo "probe_coverage_check.sh <project_dir> [--cycle N] [--probes-dir DIR]"
            echo "  Refuses if any governed class has 0 PRODUCTION probe fires (smoke excluded)."
            exit 0 ;;
        *) DIR="$1"; shift ;;
    esac
done
[ -d "$DIR" ] || { echo "FAIL: project_dir '$DIR' missing" >&2; exit 1; }
DIR=$(cd "$DIR" && pwd)
PROBES_DIR="${PROBES_DIR:-$DIR/scripts/probes}"
SINK="$DIR/outputs/structural_prevention_probe_coverage_events.jsonl"
FIRE_SINK="$DIR/outputs/structural_prevention_probe_coverage_fires.jsonl"
SCAN_JSON="$DIR/outputs/retroactive_scan_cycle_1_15_run.json"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
mkdir -p "$DIR/outputs"
: > "$FIRE_SINK"
[ -z "$CYCLE_N" ] && CYCLE_N=$(python3 -c "import json;print(json.load(open('$DIR/state.json')).get('cycle_id',16))" 2>/dev/null || echo 16)

emit() {  # event_class refuse_bool detail_json
    python3 - "$SINK" "$1" "$RUN_ID_PREFIX" "$2" "$3" "$TS" <<'PY'
import json, sys, uuid
sink, ec, pfx, refuse, detail, ts = sys.argv[1:7]
ev = {"schema_version":"0.1","namespace":"cycle_16.be_h.probe_coverage_check",
      "event_class": ec, "predicateType":"cycle16:probe_coverage_v1",
      "timestamp": ts, "run_id": f"{pfx}_{uuid.uuid4().hex[:8]}",
      "payload": {**json.loads(detail), "refuse": refuse=="true"}}
with open(sink,"a") as f: f.write(json.dumps(ev)+"\n")
PY
}

if [ ! -d "$PROBES_DIR" ]; then
    echo "REFUSE: probes dir absent ($PROBES_DIR)" >&2
    emit "probe_coverage_check.refuse.event" true "{\"reason\":\"probes_dir_absent\"}"
    exit 3
fi

declare -A CLASS_MOD=( [a]=probe_agent_contract [b]=probe_schema \
                       [c]=probe_design_decision [d]=probe_methodology_commitment )

# KT-8: subprocess-execute each probe to PRODUCE production fires.
for cls in a b c d; do
    mod="${CLASS_MOD[$cls]}"
    p="$PROBES_DIR/$cls/$mod.py"
    [ -f "$p" ] || continue
    python3 "$p" --aggregate-cycle "$CYCLE_N" --scan-json "$SCAN_JSON" \
        --sink "$FIRE_SINK" --run-id-prefix "${RUN_ID_PREFIX}_${cls}" \
        >/dev/null 2>&1 || true
done

# Count PRODUCTION fires per class, EXCLUDING smoke/self-test run_ids.
COVERAGE=$(python3 - "$FIRE_SINK" <<'PY'
import json, sys, collections
sink = sys.argv[1]
prod = collections.Counter()
prod_impl = collections.Counter()
try:
    for line in open(sink):
        line=line.strip()
        if not line: continue
        try: row=json.loads(line)
        except json.JSONDecodeError: continue
        if row.get("event_class")!="probe_library.fire.event": continue
        rid=(row.get("run_id") or "")
        if "_smoke_" in rid or "_self_test_" in rid: continue  # exclude smoke
        pay=row.get("payload") or {}
        cls=(pay.get("primitive_class") or pay.get("probe_class") or "").lower()
        if cls not in ("a","b","c","d"):
            # derive class from run_id suffix _a/_b/_c/_d
            for c in ("a","b","c","d"):
                if rid.endswith(f"_{c}") or f"_{c}_" in rid: cls=c; break
        prod[cls]+=1
        if pay.get("implemented") is True: prod_impl[cls]+=1
except FileNotFoundError:
    pass
print(json.dumps({c:{"prod":prod.get(c,0),"impl":prod_impl.get(c,0)} for c in "abcd"}))
PY
)

MISSING=0
for cls in a b c d; do
    impl=$(echo "$COVERAGE" | python3 -c "import sys,json;print(json.load(sys.stdin)['$cls']['impl'])")
    if [ "${impl:-0}" -lt 1 ]; then
        echo "  CLASS $cls: 0 production implemented fires" >&2
        emit "probe_coverage_check.refuse.event" true \
            "{\"reason\":\"zero_production_fires\",\"class\":\"$cls\",\"coverage\":$COVERAGE}"
        MISSING=$((MISSING+1))
    fi
done

if [ "$MISSING" -gt 0 ]; then
    echo "BLOCKED: $MISSING class(es) with 0 production fires (KT-10 surface)." >&2
    exit 1
fi
echo "CLEAR: all 4 classes have >=1 production implemented fire. coverage=$COVERAGE"
emit "probe_coverage_check.pass.event" false \
    "{\"reason\":\"all_classes_production_fire_present\",\"coverage\":$COVERAGE,\"cycle\":$CYCLE_N}"
exit 0
