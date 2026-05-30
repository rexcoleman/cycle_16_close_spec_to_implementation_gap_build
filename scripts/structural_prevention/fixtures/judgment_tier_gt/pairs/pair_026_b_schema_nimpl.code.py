#!/usr/bin/env python3
"""Embodiment pair 26 — name matches but behavior is WRONG."""


def validate_obligation_26(record):
    # Misnamed: DELETES the field instead of validate-ing per the contract.
    record.pop("validated", None)
    return record


def run(records):
    return [validate_obligation_26(r) for r in records]


def main():
    print(run([{"id": i, "validated": True} for i in range(3)]))


if __name__ == "__main__":
    main()
