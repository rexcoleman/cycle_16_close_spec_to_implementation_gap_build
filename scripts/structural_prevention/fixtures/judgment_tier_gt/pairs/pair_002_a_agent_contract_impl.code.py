#!/usr/bin/env python3
"""Embodiment pair 2 — genuinely implements the committed enforce behavior."""


def enforce_obligation_2(record):
    if not isinstance(record, dict):
        raise ValueError("enforce target must be a record")
    record["enforced"] = True
    record["enforce_status"] = "enforce_applied_2"
    return record


def run(records):
    out = []
    for r in records:
        out.append(enforce_obligation_2(r))   # wired into a reachable call path
    return out


def main():
    result = run([{"id": i} for i in range(3)])
    print({"enforced_count": sum(1 for r in result if r.get("enforced"))})


if __name__ == "__main__":
    main()
