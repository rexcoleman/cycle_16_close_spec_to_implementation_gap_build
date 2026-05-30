# Runtime emit: kernel-coach transition

The kernel-coach AgentContract commits to emitting `kernel_coach.transition.fire` end to
end, recorded to outputs/kernel_coach_events.jsonl with a shared run_id. Enforcement MUST
block when the emission is absent. The KG node MUST equal the fire. Code must execute this.
