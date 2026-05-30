# Spec (AgentContract) — construct pair a_agent_contract#3

COMMITMENT: every record MUST be enforced before it is accepted. The system shall enforce each record and mark it as enforced. A record that is not enforced is invalid. The embodiment must actually enforce the records (not merely mention enforce-ing them).

ACCEPTANCE: the code defines a enforce operation reachable from a runnable entrypoint that, when run, marks records as enforced.
