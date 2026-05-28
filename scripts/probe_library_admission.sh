#!/usr/bin/env bash
# Probe library admission gate — CLI/CI wrapper.
#
# Per Cycle-16-S11 BE-F dispatch substrate §1 item 3 + HR §3.recovery
# H_recovery_3 + DP#44 BINDING refuse-on-missing-precondition.
#
# Invokes scripts/probes/__init__.py admission scan; exits non-zero if ANY
# probe is refused (refused = self-test does not distinguish known_good +
# known_bad fixtures). Emits one PASS/REFUSE event per probe to
# outputs/probe_library_admission_events.jsonl.
#
# Usage:
#   bash scripts/probe_library_admission.sh
#   bash scripts/probe_library_admission.sh --help
#   bash scripts/probe_library_admission.sh --json   # machine-readable summary
#
# Exit codes:
#   0 = all discovered probes admitted (admittable as canonical vocabulary)
#   1 = ≥1 probe refused (refusal logged to admission sink)
#   2 = invocation error (Python missing, probes dir absent, etc.)

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PROBE_PKG="$SCRIPT_DIR/probes"
SINK="$PROJECT_ROOT/outputs/probe_library_admission_events.jsonl"

show_help() {
    cat <<EOF
probe_library_admission.sh — probe library admission gate

Discovers probes at scripts/probes/{a,b,c,d}/probe_*.py, runs --self-test
against each, and refuses any probe whose self-test does not distinguish
known_good + known_bad fixtures.

Usage:
  $0           # run admission scan; exit 0 iff all probes admitted
  $0 --help    # this message
  $0 --json    # emit machine-readable summary to stdout

Outputs admission events to:
  $SINK

Exit codes:
  0 = all probes PASS admission
  1 = ≥1 probe REFUSED (logged to sink)
  2 = invocation error

DP#44 refusal-authority: gate halt on FAIL is the correct outcome; do NOT
route around. Refused probe must be repaired + re-submitted via Builder-ARCH
paradigm dispatch (HC #74 BINDING).
EOF
}

JSON_OUT=0
for arg in "$@"; do
    case "$arg" in
        -h|--help) show_help; exit 0;;
        --json) JSON_OUT=1;;
        *) echo "unknown arg: $arg" >&2; show_help; exit 2;;
    esac
done

if ! command -v python3 >/dev/null 2>&1; then
    echo "FAIL: python3 not on PATH" >&2
    exit 2
fi

if [ ! -d "$PROBE_PKG" ]; then
    echo "FAIL: probe package missing at $PROBE_PKG" >&2
    exit 2
fi

# Run admission via the package __init__; capture verdict via JSON dump.
SUMMARY=$(
    PYTHONDONTWRITEBYTECODE=1 python3 -c "
import json, sys
sys.path.insert(0, '$SCRIPT_DIR')
import probes
admitted, refused = probes.admit_all()
print(json.dumps({
    'admitted_count': len(admitted),
    'refused_count': len(refused),
    'admitted': admitted,
    'refused': refused,
    'sink': '$SINK',
}, indent=2))
"
)

REFUSED_COUNT=$(echo "$SUMMARY" | python3 -c "import json, sys; print(json.load(sys.stdin)['refused_count'])")
ADMITTED_COUNT=$(echo "$SUMMARY" | python3 -c "import json, sys; print(json.load(sys.stdin)['admitted_count'])")

if [ "$JSON_OUT" = "1" ]; then
    echo "$SUMMARY"
else
    echo "Admission summary:"
    echo "  admitted: $ADMITTED_COUNT"
    echo "  refused : $REFUSED_COUNT"
    echo "  sink    : $SINK"
    if [ "$REFUSED_COUNT" -gt 0 ]; then
        echo
        echo "REFUSED probes (DP#44 halt-and-surface; do NOT route around):"
        echo "$SUMMARY" | python3 -c "
import json, sys
d=json.load(sys.stdin)
for r in d['refused']:
    print(f\"  - {r['probe_path']} :: {r['evidence']}\")
"
    fi
fi

if [ "$REFUSED_COUNT" -gt 0 ]; then
    exit 1
fi
exit 0
