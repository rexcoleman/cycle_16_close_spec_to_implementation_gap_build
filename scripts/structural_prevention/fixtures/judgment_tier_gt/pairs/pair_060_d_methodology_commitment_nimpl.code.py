#!/usr/bin/env python3
"""Embodiment pair 60 — name matches but behavior is WRONG."""


def check_obligation_60(record):
    # Misnamed: DELETES the field instead of check-ing per the contract.
    record.pop("checkd", None)
    return record


def run(records):
    return [check_obligation_60(r) for r in records]


def main():
    print(run([{"id": i, "checkd": True} for i in range(3)]))


if __name__ == "__main__":
    main()
