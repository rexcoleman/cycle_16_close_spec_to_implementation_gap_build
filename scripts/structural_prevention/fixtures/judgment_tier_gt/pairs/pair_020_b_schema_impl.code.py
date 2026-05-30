#!/usr/bin/env python3
"""Embodiment pair 20 — genuinely implements the committed validate behavior."""


def validate_obligation_20(record):
    if not isinstance(record, dict):
        raise ValueError("validate target must be a record")
    record["validated"] = True
    record["validate_status"] = "validate_applied_20"
    return record


def run(records):
    out = []
    for r in records:
        out.append(validate_obligation_20(r))   # wired into a reachable call path
    return out


def main():
    result = run([{"id": i} for i in range(3)])
    print({"validated_count": sum(1 for r in result if r.get("validated"))})


if __name__ == "__main__":
    main()
