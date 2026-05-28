#!/usr/bin/env bash
# spec_authoring_pre_commit_hook.sh — Cycle 16 BE-G Done #12 write-boundary closure.
#
# Blocks a commit that STAGES a spec-class artifact (agent_spec .md under .claude/agents/,
# a SHACL/TTL schema, or a DECISION_LOG ADR entry) UNLESS a matching `register_spec()`
# call lands in the SAME commit (staged diff contains a register_spec invocation OR a
# spec_registry.write.event JSONL row referencing the artifact).
#
# Authority: BE-G dispatch substrate §2 item 1 + ED §5.8 threshold 1 + HC-BE-D-1 closure.
#
# Install: symlink as <repo>/.git/hooks/pre-commit OR invoke from a pre-commit framework.
# Test-harness mode: --check-staged <repo_dir> runs the same predicate against the
#   currently-staged index (used by the BE-G acceptance fixtures).
#
# Emits: pre_commit_hook_block.fire.event → <repo>/outputs/spec_authoring_events.jsonl
#   on every HARD-BLOCK (non-zero exit).
#
# KT-8 note: this hook's acceptance predicate is "a register_spec() authoring call is
#   present in the same commit", NOT "a status string equals X". It inspects the staged
#   DIFF for an authoring CALL — a behavioral/write-path predicate, not a registry enum.

set -uo pipefail

REPO_DIR=""
MODE="hook"
RUN_ID_PREFIX="${SPEC_AUTHORING_RUN_ID_PREFIX:-s12_be_g_production_hook}"
while [ $# -gt 0 ]; do
    case "$1" in
        --check-staged) MODE="check-staged"; REPO_DIR="${2:-}"; shift 2 ;;
        --run-id-prefix) RUN_ID_PREFIX="${2:-}"; shift 2 ;;
        --help|-h)
            sed -n '2,30p' "$0"; exit 0 ;;
        *) REPO_DIR="$1"; shift ;;
    esac
done
REPO_DIR="${REPO_DIR:-$(git rev-parse --show-toplevel 2>/dev/null || pwd)}"
REPO_DIR="$(cd "$REPO_DIR" && pwd)"
SINK="$REPO_DIR/outputs/spec_authoring_events.jsonl"
TS="$(date -u +%Y-%m-%dT%H:%M:%SZ)"

# --- Staged file list (added/copied/modified) ---
STAGED="$(git -C "$REPO_DIR" diff --cached --name-only --diff-filter=ACM 2>/dev/null || true)"

# --- Spec-class discriminator ---
is_spec_class() {
    local f="$1"
    case "$f" in
        *.claude/agents/*.md) return 0 ;;        # agent_spec
        *.shacl.ttl|*_schema.ttl|*_shapes.ttl) return 0 ;;  # schema
        *) ;;
    esac
    # DECISION_LOG ADR entry: staged DECISION_LOG with a NEW '## ADR-' line
    case "$f" in
        *DECISION_LOG.md)
            if git -C "$REPO_DIR" diff --cached -- "$f" | grep -qE '^\+## ADR-'; then
                return 0
            fi
            ;;
    esac
    return 1
}

# --- register_spec() presence in the SAME staged commit ---
# A matching authoring call = staged diff adds a `register_spec(` invocation OR a
# spec_registry.write.event JSONL row (the write-path artifact a real register_spec emits).
register_spec_in_commit() {
    local staged_diff
    staged_diff="$(git -C "$REPO_DIR" diff --cached 2>/dev/null || true)"
    if echo "$staged_diff" | grep -qE '^\+.*register_spec\s*\('; then return 0; fi
    if echo "$staged_diff" | grep -qE '^\+.*spec_registry\.write\.event'; then return 0; fi
    return 1
}

emit_block() {
    local violating_files="$1"
    mkdir -p "$REPO_DIR/outputs"
    [ -f "$SINK" ] || touch "$SINK"
    python3 - "$SINK" "$TS" "$RUN_ID_PREFIX" "$violating_files" <<'PY'
import json, sys, uuid
sink, ts, prefix, files = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]
ev = {
  "schema_version": "0.1",
  "namespace": "cycle_16.be_g.spec_authoring",
  "event_class": "pre_commit_hook_block.fire.event",
  "timestamp": ts,
  "run_id": f"{prefix}_{uuid.uuid4().hex[:8]}",
  "payload": {
    "verdict": "HARD_BLOCK",
    "reason": "spec-class artifact staged without matching register_spec() in same commit",
    "violating_files": [f for f in files.split("\n") if f],
    "evidence_type": "write_boundary_violation",
  },
}
with open(sink, "a") as f:
    f.write(json.dumps(ev) + "\n")
PY
}

VIOLATIONS=""
while IFS= read -r f; do
    [ -z "$f" ] && continue
    if is_spec_class "$f"; then
        VIOLATIONS="$VIOLATIONS$f"$'\n'
    fi
done <<< "$STAGED"

if [ -n "$VIOLATIONS" ]; then
    if register_spec_in_commit; then
        echo "spec_authoring_pre_commit_hook: spec-class artifact staged AND register_spec() present — ALLOW"
        exit 0
    fi
    echo "================================================================" >&2
    echo "  BLOCKED: spec-class artifact staged WITHOUT register_spec()" >&2
    echo "  Files:" >&2
    echo "$VIOLATIONS" | sed 's/^/    - /' >&2
    echo "  ACTION: add a register_spec() authoring call (or its" >&2
    echo "          spec_registry.write.event) to THIS commit, or unstage." >&2
    echo "  (BE-G Done #12 write-boundary closure; HC-BE-D-1)" >&2
    echo "================================================================" >&2
    emit_block "$VIOLATIONS"
    exit 1
fi

echo "spec_authoring_pre_commit_hook: no spec-class artifact staged — ALLOW"
exit 0
