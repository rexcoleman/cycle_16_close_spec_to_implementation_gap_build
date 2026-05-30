# Agent contract: research-orchestrator emit obligation

The research-orchestrator MUST emit a `research.orchestrator.transition.fire` event at each
stage boundary, with a run_id and schema_version in the payload. The pre_check gate MUST
fire before primary task execution and MUST halt (nonzero exit) on a missing precondition.
This is a runtime obligation: a program must emit the event class and the gate must block.
