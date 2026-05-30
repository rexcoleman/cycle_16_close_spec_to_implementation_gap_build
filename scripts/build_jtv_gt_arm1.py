#!/usr/bin/env python3
"""Cycle-16-S28 BE-JTV — author Arm-1 construct-by-design GT pairs (labels true by construction).

Emits N spec<->embodiment pairs into
scripts/structural_prevention/fixtures/judgment_tier_gt/pairs/ + labels.json.
The label is TRUE BY CONSTRUCTION:
  - IMPLEMENTED: the embodiment genuinely does what the prose commits, wired into a reachable
    call path (def + call, OR CLI entrypoint that invokes it).
  - NOT-IMPLEMENTED: adversarial near-misses — same vocabulary (so token-matching is fooled) but
    the obligation is only in a comment/docstring/string, OR an unreferenced/never-called def, OR
    a pass/return-None stub, OR it does a DIFFERENT (wrong) thing.

Authored INDEPENDENTLY of the verifier judge code (imports NONE of judgment_tier_verifier's
judges). The verifier sees ONLY the (prose, code) pair; never labels.json. Reusable authored
test data (like fixtures/**), NOT a human decision in the live close path.

Stratified across the 4 judgment-tier strata (named to MATCH the real spec_class values so the
harness routes them per stratum): a_agent_contract, b_schema, c_design_decision,
d_methodology_commitment. Embodiments are .py so all three judges (incl. J3's AST) can engage —
construct GT deliberately gives J3 a fair test (real c/d specs lack code, the §B.4 residual).
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
GT_DIR = os.path.join(HERE, "structural_prevention", "fixtures", "judgment_tier_gt")
PAIRS = os.path.join(GT_DIR, "pairs")
os.makedirs(PAIRS, exist_ok=True)

STRATA = ["a_agent_contract", "b_schema", "c_design_decision", "d_methodology_commitment"]
VERBS = {"a_agent_contract": "enforce", "b_schema": "validate",
         "c_design_decision": "gate", "d_methodology_commitment": "check"}


def impl_code(idx, verb):
    fn = f"{verb}_obligation_{idx}"
    return f'''#!/usr/bin/env python3
"""Embodiment pair {idx} — genuinely implements the committed {verb} behavior."""


def {fn}(record):
    if not isinstance(record, dict):
        raise ValueError("{verb} target must be a record")
    record["{verb}d"] = True
    record["{verb}_status"] = "{verb}_applied_{idx}"
    return record


def run(records):
    out = []
    for r in records:
        out.append({fn}(r))   # wired into a reachable call path
    return out


def main():
    result = run([{{"id": i}} for i in range(3)])
    print({{"{verb}d_count": sum(1 for r in result if r.get("{verb}d"))}})


if __name__ == "__main__":
    main()
'''


def nimpl_code(idx, verb, shape):
    fn = f"{verb}_obligation_{idx}"
    if shape == 0:  # verb only in comment/docstring
        return f'''#!/usr/bin/env python3
"""Embodiment pair {idx} — claims to {verb} but does NOT.

TODO: we intend to {verb} the records. The contract requires us to {verb} each one. For now this
only loads and prints them; the {verb} step is not built.
"""


def load(records):
    # NOTE: a real implementation would {verb}() each record. It does not yet.
    return list(records)


def main():
    print(load([{{"id": i}} for i in range(3)]))   # only loads; never {verb}s


if __name__ == "__main__":
    main()
'''
    if shape == 1:  # verb def exists but is never called
        return f'''#!/usr/bin/env python3
"""Embodiment pair {idx} — has a {verb} function that is never reached."""


def {fn}(record):
    record["{verb}d"] = True
    return record


def main():
    # {fn} is defined but main NEVER calls it (dead code).
    print([{{"id": i}} for i in range(3)])


if __name__ == "__main__":
    main()
'''
    if shape == 2:  # stub: called but does nothing
        return f'''#!/usr/bin/env python3
"""Embodiment pair {idx} — {verb} is a STUB that does nothing."""


def {fn}(record):
    # STUB: contract says {verb}, but this is not implemented.
    pass


def run(records):
    for r in records:
        {fn}(r)          # called, but does nothing
    return records


def main():
    print(run([{{"id": i}} for i in range(3)]))


if __name__ == "__main__":
    main()
'''
    return f'''#!/usr/bin/env python3
"""Embodiment pair {idx} — name matches but behavior is WRONG."""


def {fn}(record):
    # Misnamed: DELETES the field instead of {verb}-ing per the contract.
    record.pop("{verb}d", None)
    return record


def run(records):
    return [{fn}(r) for r in records]


def main():
    print(run([{{"id": i, "{verb}d": True}} for i in range(3)]))


if __name__ == "__main__":
    main()
'''


def prose(stratum, idx, verb):
    cls = {"a_agent_contract": "AgentContract", "b_schema": "Schema",
           "c_design_decision": "DesignDecision",
           "d_methodology_commitment": "MethodologyCommitment"}[stratum]
    return (f"# Spec ({cls}) — construct pair {stratum}#{idx}\n\n"
            f"COMMITMENT: every record MUST be {verb}d before it is accepted. The system shall "
            f"{verb} each record and mark it as {verb}d. A record that is not {verb}d is invalid. "
            f"The embodiment must actually {verb} the records (not merely mention {verb}-ing them).\n\n"
            f"ACCEPTANCE: the code defines a {verb} operation reachable from a runnable entrypoint "
            f"that, when run, marks records as {verb}d.\n")


def main():
    labels = {}
    impl_counts = [8, 7, 8, 7]   # 30 implemented
    nimpl_counts = [7, 8, 7, 8]  # 30 not-implemented -> 60 total
    n = 0
    for si, stratum in enumerate(STRATA):
        verb = VERBS[stratum]
        for _ in range(impl_counts[si]):
            n += 1
            base = f"pair_{n:03d}_{stratum}_impl"
            pf, cf = base + ".spec.md", base + ".code.py"
            open(os.path.join(PAIRS, pf), "w").write(prose(stratum, n, verb))
            open(os.path.join(PAIRS, cf), "w").write(impl_code(n, verb))
            labels[base] = {"stratum": stratum, "spec_file": pf, "code_file": cf,
                            "true_label": "implemented",
                            "rationale": f"{verb} def wired into reachable run/main call path"}
        for k in range(nimpl_counts[si]):
            n += 1
            shape = k % 4
            base = f"pair_{n:03d}_{stratum}_nimpl"
            pf, cf = base + ".spec.md", base + ".code.py"
            open(os.path.join(PAIRS, pf), "w").write(prose(stratum, n, verb))
            open(os.path.join(PAIRS, cf), "w").write(nimpl_code(n, verb, shape))
            shapes = {0: "verb only in comment/docstring", 1: "verb def never called",
                      2: "verb is a pass-stub", 3: "verb name does the wrong thing"}
            labels[base] = {"stratum": stratum, "spec_file": pf, "code_file": cf,
                            "true_label": "not_implemented",
                            "rationale": f"adversarial near-miss: {shapes[shape]}"}
    meta = {
        "schema_version": "0.1", "arm": "arm1_construct_by_design",
        "authored": "Cycle-16-S28 BE-JTV; labels true by construction; blind to verifier logic",
        "n_total": len(labels),
        "n_implemented": sum(1 for v in labels.values() if v["true_label"] == "implemented"),
        "n_not_implemented": sum(1 for v in labels.values() if v["true_label"] == "not_implemented"),
        "labels": labels,
    }
    json.dump(meta, open(os.path.join(GT_DIR, "labels.json"), "w"), indent=2)
    print(json.dumps({"n_total": meta["n_total"], "n_implemented": meta["n_implemented"],
                      "n_not_implemented": meta["n_not_implemented"], "pairs_dir": PAIRS}, indent=2))


if __name__ == "__main__":
    main()
