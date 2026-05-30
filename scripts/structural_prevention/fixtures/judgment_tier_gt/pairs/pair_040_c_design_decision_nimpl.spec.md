# Spec (DesignDecision) — construct pair c_design_decision#40

COMMITMENT: every record MUST be gated before it is accepted. The system shall gate each record and mark it as gated. A record that is not gated is invalid. The embodiment must actually gate the records (not merely mention gate-ing them).

ACCEPTANCE: the code defines a gate operation reachable from a runnable entrypoint that, when run, marks records as gated.
