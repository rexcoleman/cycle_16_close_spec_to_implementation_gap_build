#!/usr/bin/env python3
"""Embodiment pair 40 — has a gate function that is never reached."""


def gate_obligation_40(record):
    record["gated"] = True
    return record


def main():
    # gate_obligation_40 is defined but main NEVER calls it (dead code).
    print([{"id": i} for i in range(3)])


if __name__ == "__main__":
    main()
