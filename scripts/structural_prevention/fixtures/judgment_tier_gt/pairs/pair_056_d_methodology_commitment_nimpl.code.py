#!/usr/bin/env python3
"""Embodiment pair 56 — name matches but behavior is WRONG."""


def check_obligation_56(record):
    # Misnamed: DELETES the field instead of check-ing per the contract.
    record.pop("checkd", None)
    return record


def run(records):
    return [check_obligation_56(r) for r in records]


def main():
    print(run([{"id": i, "checkd": True} for i in range(3)]))


if __name__ == "__main__":
    main()
