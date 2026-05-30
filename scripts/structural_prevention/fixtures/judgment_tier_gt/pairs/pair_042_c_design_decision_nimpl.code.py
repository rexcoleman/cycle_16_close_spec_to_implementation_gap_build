#!/usr/bin/env python3
"""Embodiment pair 42 — name matches but behavior is WRONG."""


def gate_obligation_42(record):
    # Misnamed: DELETES the field instead of gate-ing per the contract.
    record.pop("gated", None)
    return record


def run(records):
    return [gate_obligation_42(r) for r in records]


def main():
    print(run([{"id": i, "gated": True} for i in range(3)]))


if __name__ == "__main__":
    main()
