#!/usr/bin/env bash
# three_registry_reconciliation_gate.sh — Cycle 16 BE-G Done #12 reconciliation gate.
#
# Reads three registries at session close and detects drift:
#   (a) filesystem spec-class file inventory (agent_spec .md + schema TTL + ADR count)
#   (b) Fuseki /cycle6 cycle16:Spec count via SPARQL SELECT
#   (c) prompt_inventory SQLite table (singularity.db; agent_spec rows)
#
# Three-way drift = forbidden state blocking close. Emits
#   three_registry_reconciliation.fire.event with drift_detected_bool to
#   outputs/three_registry_reconciliation_events.jsonl on every fire.
#
# Authority: BE-G dispatch substrate §2 item 4 + ED §5.8 threshold 3.
#
# Modes:
#   bash three_registry_reconciliation_gate.sh <repo_dir>            # blocking
#   bash three_registry_reconciliation_gate.sh <repo_dir> --advisory # exit 0 on drift
#
# Drift definition (reconciliation, NOT exact-equality — the three registries count
# different universes): drift_detected_bool=true iff the KG count is ZERO while the
# filesystem has spec-class files (KG lost the inventory) OR the prompt_inventory
# agent_spec count is ZERO while the filesystem has agent specs (guard-the-guards
# gap per Done #30). Reconciliation tolerates known scope differences (FS counts
# THIS repo; KG counts all retroactively-scanned specs across cycles); the gate
# fires drift only on a registry going DARK relative to a populated peer.
#
# KT-8 note: predicate reads live registry COUNTS (real SPARQL SELECT + real sqlite3
# query + real filesystem scan), not a status enum.

set -uo pipefail

REPO_DIR=""
ADVISORY=false
RUN_ID_PREFIX="${RECONCILE_RUN_ID_PREFIX:-s12_be_g_production_reconcile}"
SESSION_LABEL="${RECONCILE_SESSION_LABEL:-S12}"
while [ $# -gt 0 ]; do
    case "$1" in
        --advisory) ADVISORY=true; shift ;;
        --run-id-prefix) RUN_ID_PREFIX="$2"; shift 2 ;;
        --session-label) SESSION_LABEL="$2"; shift 2 ;;
        --help|-h) sed -n '2,30p' "$0"; exit 0 ;;
        *) REPO_DIR="$1"; shift ;;
    esac
done
REPO_DIR="${REPO_DIR:-.}"
REPO_DIR="$(cd "$REPO_DIR" && pwd)"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"
SINK="$REPO_DIR/outputs/three_registry_reconciliation_events.jsonl"
SPARQL_ENDPOINT="${CYCLE6_QUERY_ENDPOINT:-http://localhost:3030/cycle6/query}"
DB="${SINGULARITY_DB:-$HOME/singularity.db}"

# --- (a) filesystem spec-class inventory ---
FS_AGENTS=$(find "$REPO_DIR" -path '*/.claude/agents/*.md' 2>/dev/null | wc -l | tr -d ' ')
FS_SCHEMAS=$(find "$REPO_DIR" \( -name '*.shacl.ttl' -o -name '*_schema.ttl' -o -name '*_shapes.ttl' \) 2>/dev/null | wc -l | tr -d ' ')
FS_COUNT=$((FS_AGENTS + FS_SCHEMAS))

# --- (b) Fuseki /cycle6 cycle16:Spec count ---
KG_COUNT=$(python3 - "$SPARQL_ENDPOINT" <<'PY'
import sys, urllib.request, urllib.parse, json
ep = sys.argv[1]
q = """PREFIX cycle16: <http://cycle16.local/ontology#>
SELECT (COUNT(?s) AS ?n) WHERE { GRAPH <http://cycle16.local/registry/assertion> { ?s a cycle16:Spec } }"""
try:
    body = urllib.parse.urlencode({"query": q}).encode()
    req = urllib.request.Request(ep, data=body, headers={"Accept": "application/sparql-results+json"})
    r = urllib.request.urlopen(req, timeout=10)
    d = json.loads(r.read())
    b = d.get("results", {}).get("bindings", [])
    print(int(b[0]["n"]["value"]) if b else 0)
except Exception:
    print(-1)
PY
)

# --- (c) prompt_inventory agent_spec count ---
if [ -f "$DB" ]; then
    PI_COUNT=$(sqlite3 "$DB" "SELECT COUNT(*) FROM prompt_inventory WHERE type='agent_spec';" 2>/dev/null || echo -1)
else
    PI_COUNT=-1
fi

# --- drift detection ---
DRIFT=false
DRIFT_REASON="none"
if [ "$KG_COUNT" -eq 0 ] && [ "$FS_COUNT" -gt 0 ]; then
    DRIFT=true; DRIFT_REASON="kg_dark_vs_populated_fs (KG cycle16:Spec=0 while FS spec-class=$FS_COUNT)"
elif [ "$KG_COUNT" -lt 0 ]; then
    DRIFT=true; DRIFT_REASON="kg_unreachable (SPARQL endpoint $SPARQL_ENDPOINT returned error)"
elif [ "$PI_COUNT" -eq 0 ] && [ "$FS_AGENTS" -gt 0 ]; then
    DRIFT=true; DRIFT_REASON="prompt_inventory_dark_vs_fs_agents (PI agent_spec=0 while FS agents=$FS_AGENTS; guard-the-guards gap)"
elif [ "$PI_COUNT" -lt 0 ]; then
    DRIFT=true; DRIFT_REASON="prompt_inventory_unreachable (singularity.db missing at $DB)"
fi

echo "================================================================"
echo "  3-Registry Reconciliation Gate ($SESSION_LABEL)"
echo "  (a) filesystem spec-class : $FS_COUNT (agents=$FS_AGENTS schemas=$FS_SCHEMAS)"
echo "  (b) Fuseki /cycle6 Spec   : $KG_COUNT"
echo "  (c) prompt_inventory      : $PI_COUNT (agent_spec rows)"
echo "  drift_detected            : $DRIFT ($DRIFT_REASON)"
echo "================================================================"

mkdir -p "$REPO_DIR/outputs"; [ -f "$SINK" ] || touch "$SINK"
DRIFT_PY=$([ "$DRIFT" = true ] && echo true || echo false)
python3 - "$SINK" "$TS" "$RUN_ID_PREFIX" "$SESSION_LABEL" "$FS_COUNT" "$FS_AGENTS" "$FS_SCHEMAS" "$KG_COUNT" "$PI_COUNT" "$DRIFT_PY" "$DRIFT_REASON" <<'PY'
import json, sys, uuid
(sink, ts, prefix, sess, fs, fsa, fss, kg, pi, drift, reason) = sys.argv[1:12]
ev = {
  "schema_version": "0.1",
  "namespace": "cycle_16.be_g.three_registry_reconciliation",
  "event_class": "three_registry_reconciliation.fire.event",
  "timestamp": ts,
  "run_id": f"{prefix}_{sess}_{uuid.uuid4().hex[:8]}",
  "payload": {
    "session_label": sess,
    "filesystem_spec_class_count": int(fs),
    "filesystem_agent_spec_count": int(fsa),
    "filesystem_schema_count": int(fss),
    "kg_cycle16_spec_count": int(kg),
    "prompt_inventory_agent_spec_count": int(pi),
    "drift_detected_bool": (drift == "true"),
    "drift_reason": reason,
    "evidence_type": "three_registry_count_reconciliation",
  },
}
with open(sink, "a") as f:
    f.write(json.dumps(ev) + "\n")
PY

if [ "$DRIFT" = true ]; then
    if [ "$ADVISORY" = true ]; then
        echo "  ADVISORY: drift detected — exit 0 per --advisory"; exit 0
    fi
    echo "  BLOCKED: 3-registry drift blocks close" >&2; exit 1
fi
echo "  CLEAR: no drift"; exit 0
