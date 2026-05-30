#!/usr/bin/env python3
"""Embodiment pair 28 — has a validate function that is never reached."""


def validate_obligation_28(record):
    record["validated"] = True
    return record


def main():
    # validate_obligation_28 is defined but main NEVER calls it (dead code).
    print([{"id": i} for i in range(3)])


if __name__ == "__main__":
    main()
