#!/usr/bin/env bash
# library_self_test_gate.sh — Cycle 16 BE-H / Done #15e.
#
# At session close: exercise EVERY probe primitive against its fixtures
# (subprocess --self-test). Emit results to
# outputs/probe_library_self_test_events.jsonl. A primitive that FAILS self-test
# for 2 CONSECUTIVE sessions AUTO-DEPRECATES (emit
# outputs/probe_library_auto_deprecate_events.jsonl) and blocks close until
# repair / paradigm-removal.
#
# HC-BE-G-1 TIE (BINDING): a CRASHING probe (non-zero exit OR exception OR
# timeout) counts as a self-test FAIL — never silently treated as pass. The
# crash verdict is distinct from a clean fail and is recorded as crash=true.
#
# KT-8: presence-on-disk is not acceptance; every probe is IMPORTED +
# subprocess-EXECUTED.
#
# DP#44 refuse-on-missing-precondition: probes dir absent -> refuse.
#
# Sinks:
#   outputs/structural_prevention_library_self_test_events.jsonl  (gate verdict)
#   outputs/probe_library_self_test_events.jsonl                  (per-probe rows)
#   outputs/probe_library_auto_deprecate_events.jsonl             (deprecations)
#
# Usage:
#   library_self_test_gate.sh <project_dir> [--session SID] [--probes-dir DIR]
#   library_self_test_gate.sh --help

set -euo pipefail

DIR="."
SESSION=""
PROBES_DIR=""
RUN_ID_PREFIX="s13_be_h_production_library_self_test"
while [ $# -gt 0 ]; do
    case "$1" in
        --session) SESSION="$2"; shift 2 ;;
        --probes-dir) PROBES_DIR="$2"; shift 2 ;;
        --run-id-prefix) RUN_ID_PREFIX="$2"; shift 2 ;;
        --help|-h)
            echo "library_self_test_gate.sh <project_dir> [--session SID] [--probes-dir DIR]"
            echo "  Crashing probe = self-test FAIL (HC-BE-G-1). 2 consecutive fails -> auto-deprecate."
            exit 0 ;;
        *) DIR="$1"; shift ;;
    esac
done
[ -d "$DIR" ] || { echo "FAIL: project_dir '$DIR' missing" >&2; exit 1; }
DIR=$(cd "$DIR" && pwd)
PROBES_DIR="${PROBES_DIR:-$DIR/scripts/probes}"
SESSION="${SESSION:-$(date -u +%Y%m%dT%H%M%SZ)}"
GATE_SINK="$DIR/outputs/structural_prevention_library_self_test_events.jsonl"
PROBE_SINK="$DIR/outputs/probe_library_self_test_events.jsonl"
DEP_SINK="$DIR/outputs/probe_library_auto_deprecate_events.jsonl"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
mkdir -p "$DIR/outputs"

gate_emit() {  # event_class refuse_bool detail_json
    python3 - "$GATE_SINK" "$1" "$RUN_ID_PREFIX" "$2" "$3" "$TS" <<'PY'
import json, sys, uuid
sink, ec, pfx, refuse, detail, ts = sys.argv[1:7]
ev={"schema_version":"0.1","namespace":"cycle_16.be_h.library_self_test_gate",
    "event_class":ec,"predicateType":"cycle16:library_self_test_v1",
    "timestamp":ts,"run_id":f"{pfx}_{uuid.uuid4().hex[:8]}",
    "payload":{**json.loads(detail),"refuse":refuse=="true"}}
open(sink,"a").write(json.dumps(ev)+"\n")
PY
}

if [ ! -d "$PROBES_DIR" ]; then
    echo "REFUSE: probes dir absent ($PROBES_DIR)" >&2
    gate_emit "library_self_test_gate.refuse.event" true "{\"reason\":\"probes_dir_absent\"}"
    exit 3
fi

# Per-probe self-test with crash detection (HC-BE-G-1). Then 2-consecutive-fail
# deprecation logic, reading the persistent PROBE_SINK history.
RESULT=$(python3 - "$PROBES_DIR" "$PROBE_SINK" "$DEP_SINK" "$SESSION" "$TS" <<'PY'
import json, os, subprocess, sys, uuid, datetime
probes_dir, probe_sink, dep_sink, session, ts = sys.argv[1:6]

def discover(d):
    out=[]
    for cls in sorted(os.listdir(d)):
        cd=os.path.join(d,cls)
        if not os.path.isdir(cd) or cls.startswith(("_","__")) or cls in ("tests","__pycache__"):
            continue
        for f in sorted(os.listdir(cd)):
            if f.startswith("probe_") and f.endswith(".py"):
                out.append((cls,os.path.join(cd,f)))
    return out

def run_self_test(path):
    # Returns (verdict, crash_bool, exit_code, evidence)
    try:
        r=subprocess.run([sys.executable,path,"--self-test"],
                         capture_output=True,text=True,timeout=120)
        if r.returncode==0:
            return ("pass",False,0,"self_test_distinguished")
        # non-zero exit: could be a clean "fixtures-not-distinguished" fail OR a crash.
        crash = ("Traceback" in (r.stderr or "")) or r.returncode not in (1,)
        return ("fail",crash,r.returncode,(r.stderr or r.stdout or "")[:200])
    except subprocess.TimeoutExpired:
        return ("fail",True,-1,"self_test_timeout_120s_crash")
    except Exception as e:
        return ("fail",True,-2,f"self_test_exception_crash:{e}")

probes=discover(probes_dir)
# Emit one per-probe row to PROBE_SINK.
rows_this_session=[]
for cls,path in probes:
    verdict,crash,rc,ev=run_self_test(path)
    row={"schema_version":"0.1","namespace":"cycle_16.be_h.probe_library_self_test",
         "event_class":f"probe_library_self_test.{verdict}.event",
         "predicateType":"cycle16:library_self_test_v1","timestamp":ts,
         "run_id":f"{session}_self_test_{cls}_{uuid.uuid4().hex[:8]}",
         "payload":{"probe_path":path,"probe_id":os.path.basename(path)[:-3],
                    "primitive_class":cls.upper(),"verdict":verdict,
                    "crash":crash,"self_test_exit":rc,"session":session,"evidence":ev}}
    open(probe_sink,"a").write(json.dumps(row)+"\n")
    rows_this_session.append(row["payload"])

# Deprecation: a probe failing self-test for 2 CONSECUTIVE DISTINCT sessions.
# Read history, group by probe_id, order sessions, find latest-2-consecutive fails.
hist={}
if os.path.exists(probe_sink):
    for line in open(probe_sink):
        line=line.strip()
        if not line: continue
        try: r=json.loads(line)
        except json.JSONDecodeError: continue
        if r.get("event_class","").startswith("probe_library_self_test"):
            p=r.get("payload") or {}
            pid=p.get("probe_id"); ses=p.get("session")
            if pid and ses:
                hist.setdefault(pid,{}).setdefault(ses,p.get("verdict"))

deprecations=[]
for pid,sess_map in hist.items():
    # order sessions by first-seen timestamp proxy = lexical session string order
    ordered=sorted(sess_map.keys())
    if len(ordered)>=2:
        last2=[sess_map[ordered[-1]],sess_map[ordered[-2]]]
        if last2==["fail","fail"]:
            dep={"schema_version":"0.1","namespace":"cycle_16.be_h.probe_library_auto_deprecate",
                 "event_class":"probe_library_auto_deprecate.deprecate.event",
                 "predicateType":"cycle16:auto_deprecate_v1","timestamp":ts,
                 "run_id":f"{session}_auto_deprecate_{uuid.uuid4().hex[:8]}",
                 "payload":{"probe_id":pid,"reason":"self_test_failed_2_consecutive_sessions",
                            "sessions":[ordered[-2],ordered[-1]],"refuse":True,
                            "action":"block_close_until_repair_or_paradigm_removal"}}
            open(dep_sink,"a").write(json.dumps(dep)+"\n")
            deprecations.append(pid)

fails=[r for r in rows_this_session if r["verdict"]=="fail"]
crashes=[r for r in rows_this_session if r["crash"]]
print(json.dumps({"probes":len(rows_this_session),
                  "fails":len(fails),"crashes":len(crashes),
                  "deprecations":deprecations}))
PY
)

DEPS=$(echo "$RESULT" | python3 -c "import sys,json;print(len(json.load(sys.stdin)['deprecations']))")
FAILS=$(echo "$RESULT" | python3 -c "import sys,json;print(json.load(sys.stdin)['fails'])")
CRASHES=$(echo "$RESULT" | python3 -c "import sys,json;print(json.load(sys.stdin)['crashes'])")

if [ "${DEPS:-0}" -gt 0 ]; then
    echo "BLOCKED: $DEPS probe(s) auto-deprecated (2 consecutive self-test fails). $RESULT" >&2
    gate_emit "library_self_test_gate.refuse.event" true "{\"result\":$RESULT}"
    exit 1
fi
if [ "${FAILS:-0}" -gt 0 ]; then
    echo "WARN: $FAILS probe self-test fail(s) this session ($CRASHES crash). $RESULT" >&2
    gate_emit "library_self_test_gate.refuse.event" true "{\"result\":$RESULT,\"reason\":\"self_test_fail_single_session\"}"
    exit 1
fi
echo "CLEAR: all probes pass self-test. $RESULT"
gate_emit "library_self_test_gate.pass.event" false "{\"result\":$RESULT}"
exit 0
