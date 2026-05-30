#!/usr/bin/env bash
# kernel_coach_emit_present_gate.sh — Cycle-16-S25 vertical slice T3 (#31).
#
# Enforcement-blocks-absence gate. Runs the INDEPENDENT verifier (T2; NOT the
# F-probe). PRESENT -> exit 0 (PASS). ABSENT (sink/transition.fire removed) ->
# exit 1 (BLOCKED, catches the gap). This proves the FORWARD guarantee on this
# one spec: if the kernel-coach's committed emit ever stops firing, the gate
# fails closed.
#
# It NEVER touches the F-probe, the probe-accuracy harness, the calibration
# floors (0.20/0.80/0.20), or any fixture. ADDITIVE only.
#
# Usage:
#   kernel_coach_emit_present_gate.sh            # gate the default sink
#   kernel_coach_emit_present_gate.sh <sink>     # gate a specific sink path
#
# Authority: Cycle-16-S25 dispatch substrate T3 (#31 enforcement-blocks-absence).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
VERIFIER="${PROJECT_ROOT}/scripts/independent_emit_contract_verifier.py"
SINK="${1:-${PROJECT_ROOT}/outputs/kernel_coach_events.jsonl}"

echo "[kernel_coach_emit_present_gate] verifier=${VERIFIER}"
echo "[kernel_coach_emit_present_gate] sink=${SINK}"

if python3 "${VERIFIER}" --sink "${SINK}" --quiet; then
  echo "[kernel_coach_emit_present_gate] VERDICT=PASS (kernel-coach emit contract present + conformant)"
  exit 0
else
  echo "[kernel_coach_emit_present_gate] VERDICT=BLOCKED (kernel-coach emit absent/non-conformant — gap caught)"
  exit 1
fi
