#!/usr/bin/env python3
"""Embodiment pair 35 — genuinely implements the committed gate behavior."""


def gate_obligation_35(record):
    if not isinstance(record, dict):
        raise ValueError("gate target must be a record")
    record["gated"] = True
    record["gate_status"] = "gate_applied_35"
    return record


def run(records):
    out = []
    for r in records:
        out.append(gate_obligation_35(r))   # wired into a reachable call path
    return out


def main():
    result = run([{"id": i} for i in range(3)])
    print({"gated_count": sum(1 for r in result if r.get("gated"))})


if __name__ == "__main__":
    main()
