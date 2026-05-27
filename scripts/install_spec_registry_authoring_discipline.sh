#!/usr/bin/env bash
# install_spec_registry_authoring_discipline.sh
# Cycle 16 BE-B standalone bootstrap for spec_registry authoring discipline.
#
# Mirrors the structural pattern of govML v2.8.2 install_runtime_emit_substrate()
# (at ~/ml-governance-templates/scripts/init_project.sh L171-L209) so a fresh
# research-build project can be brought up to the authoring-discipline baseline
# without scaffolding-time regeneration. Use this script during Cycle 16 dogfooding
# OR for retroactive installs into pre-v2.8.3 project state.
#
# Authority: Cycle 16 SI ACTIVE 2026-05-27 + Amendments 27a + 27b + Rex back-port
# directive 2026-05-27 (4-repo paired commit including govML v2.8.3).
#
# Usage:
#   bash install_spec_registry_authoring_discipline.sh <project_dir>
#
# Idempotent: safe to re-run; existing files are left in place.

set -euo pipefail

PROJECT_DIR="${1:-.}"
PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)"

if [[ ! -d "$PROJECT_DIR" ]]; then
    echo "Error: project_dir '$PROJECT_DIR' does not exist." >&2
    exit 1
fi

SRC_DIR="${SRC_DIR:-$HOME/ml-governance-templates/templates/build/spec_registry}"

if [[ ! -d "$SRC_DIR" ]]; then
    # Fallback: if govML templates not yet installed, source from cycle_16 docs/
    SRC_DIR="$HOME/cycle_16_close_spec_to_implementation_gap_build"
    SCRIPTS_FALLBACK="$HOME/cycle_16_close_spec_to_implementation_gap_build/scripts"
    DOCS_FALLBACK="$HOME/cycle_16_close_spec_to_implementation_gap_build/docs"
fi

SR_SCRIPTS="${PROJECT_DIR}/scripts/spec_registry"
SR_OUTPUTS="${PROJECT_DIR}/outputs"
SR_DOCS="${PROJECT_DIR}/docs"

echo ""
echo "Installing spec_registry authoring discipline (Cycle 16 BE-B; govML v2.8.3 analog):"

mkdir -p "$SR_SCRIPTS" "$SR_OUTPUTS" "$SR_DOCS"

# Authoring wrapper
if [[ -f "$SRC_DIR/spec_registry_authoring.py" ]]; then
    cp "$SRC_DIR/spec_registry_authoring.py" "$SR_SCRIPTS/spec_registry_authoring.py"
elif [[ -f "${SCRIPTS_FALLBACK:-}/spec_registry_authoring.py" ]]; then
    cp "${SCRIPTS_FALLBACK}/spec_registry_authoring.py" "$SR_SCRIPTS/spec_registry_authoring.py"
else
    echo "  WARNING: spec_registry_authoring.py not found at $SRC_DIR; skipping." >&2
fi
[[ -f "$SR_SCRIPTS/spec_registry_authoring.py" ]] && chmod +x "$SR_SCRIPTS/spec_registry_authoring.py"
echo "  + scripts/spec_registry/spec_registry_authoring.py"

# Schema TTL
if [[ -f "$SRC_DIR/spec_registry_schema.ttl" ]]; then
    cp "$SRC_DIR/spec_registry_schema.ttl" "$SR_DOCS/spec_registry_schema.ttl"
elif [[ -f "${DOCS_FALLBACK:-}/spec_registry_schema.ttl" ]]; then
    cp "${DOCS_FALLBACK}/spec_registry_schema.ttl" "$SR_DOCS/spec_registry_schema.ttl"
fi
echo "  + docs/spec_registry_schema.ttl"

# SHACL shapes
if [[ -f "$SRC_DIR/spec_registry_shapes.shacl.ttl" ]]; then
    cp "$SRC_DIR/spec_registry_shapes.shacl.ttl" "$SR_DOCS/spec_registry_shapes.shacl.ttl"
elif [[ -f "${DOCS_FALLBACK:-}/spec_registry_shapes.shacl.ttl" ]]; then
    cp "${DOCS_FALLBACK}/spec_registry_shapes.shacl.ttl" "$SR_DOCS/spec_registry_shapes.shacl.ttl"
fi
echo "  + docs/spec_registry_shapes.shacl.ttl"

# Authoring discipline doc
if [[ -f "$SRC_DIR/spec_authoring_discipline.md" ]]; then
    cp "$SRC_DIR/spec_authoring_discipline.md" "$SR_DOCS/spec_authoring_discipline.md"
elif [[ -f "${DOCS_FALLBACK:-}/spec_authoring_discipline.md" ]]; then
    cp "${DOCS_FALLBACK}/spec_authoring_discipline.md" "$SR_DOCS/spec_authoring_discipline.md"
fi
echo "  + docs/spec_authoring_discipline.md"

# Obligation doc — written inline if not present (analog to govML RUNTIME_EMIT_OBLIGATION.md)
if [[ -f "$SRC_DIR/SPEC_AUTHORING_DISCIPLINE.md" ]]; then
    cp "$SRC_DIR/SPEC_AUTHORING_DISCIPLINE.md" "$SR_DOCS/SPEC_AUTHORING_DISCIPLINE.md"
fi
echo "  + docs/SPEC_AUTHORING_DISCIPLINE.md"

# __init__.py
if [[ ! -f "$SR_SCRIPTS/__init__.py" ]]; then
    touch "$SR_SCRIPTS/__init__.py"
    echo "  + scripts/spec_registry/__init__.py"
fi

# Empty JSONL sink for spec_registry_events (refuse-on-violation per RUNTIME_EMIT_SPEC §3)
if [[ ! -f "$SR_OUTPUTS/spec_registry_events.jsonl" ]]; then
    touch "$SR_OUTPUTS/spec_registry_events.jsonl"
    echo "  + outputs/spec_registry_events.jsonl (empty sink; sink-exists invariant)"
fi

echo ""
echo "Install complete. Smoke-test:"
echo "  python3 -c 'import sys; sys.path.insert(0, \"$SR_SCRIPTS\"); import spec_registry_authoring; print(spec_registry_authoring.MANDATORY_FIELDS)'"
