# Gate: spec-implementation present gate

The spec_implementation_present_gate MUST fire at session close and MUST hard-fail with a
nonzero exit code when a spec marked implemented has no corresponding probe fire in the
events jsonl. The gate emits `spec_implementation.gate.fire` with a verdict payload. This
is a checkable runtime obligation requiring code.
