#!/usr/bin/env python3
"""Embodiment pair 12 — name matches but behavior is WRONG."""


def enforce_obligation_12(record):
    # Misnamed: DELETES the field instead of enforce-ing per the contract.
    record.pop("enforced", None)
    return record


def run(records):
    return [enforce_obligation_12(r) for r in records]


def main():
    print(run([{"id": i, "enforced": True} for i in range(3)]))


if __name__ == "__main__":
    main()
