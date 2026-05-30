#!/usr/bin/env python3
"""Embodiment pair 51 — genuinely implements the committed check behavior."""


def check_obligation_51(record):
    if not isinstance(record, dict):
        raise ValueError("check target must be a record")
    record["checkd"] = True
    record["check_status"] = "check_applied_51"
    return record


def run(records):
    out = []
    for r in records:
        out.append(check_obligation_51(r))   # wired into a reachable call path
    return out


def main():
    result = run([{"id": i} for i in range(3)])
    print({"checkd_count": sum(1 for r in result if r.get("checkd"))})


if __name__ == "__main__":
    main()
