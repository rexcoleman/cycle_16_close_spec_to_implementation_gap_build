# Spec (Schema) — construct pair b_schema#30

COMMITMENT: every record MUST be validated before it is accepted. The system shall validate each record and mark it as validated. A record that is not validated is invalid. The embodiment must actually validate the records (not merely mention validate-ing them).

ACCEPTANCE: the code defines a validate operation reachable from a runnable entrypoint that, when run, marks records as validated.
