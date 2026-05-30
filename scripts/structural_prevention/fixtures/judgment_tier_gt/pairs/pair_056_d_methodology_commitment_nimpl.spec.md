# Spec (MethodologyCommitment) — construct pair d_methodology_commitment#56

COMMITMENT: every record MUST be checkd before it is accepted. The system shall check each record and mark it as checkd. A record that is not checkd is invalid. The embodiment must actually check the records (not merely mention check-ing them).

ACCEPTANCE: the code defines a check operation reachable from a runnable entrypoint that, when run, marks records as checkd.
