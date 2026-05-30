#!/usr/bin/env python3
"""Embodiment pair 10 — has a enforce function that is never reached."""


def enforce_obligation_10(record):
    record["enforced"] = True
    return record


def main():
    # enforce_obligation_10 is defined but main NEVER calls it (dead code).
    print([{"id": i} for i in range(3)])


if __name__ == "__main__":
    main()
