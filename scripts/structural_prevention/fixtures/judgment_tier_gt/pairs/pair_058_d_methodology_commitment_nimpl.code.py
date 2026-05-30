#!/usr/bin/env python3
"""Embodiment pair 58 — has a check function that is never reached."""


def check_obligation_58(record):
    record["checkd"] = True
    return record


def main():
    # check_obligation_58 is defined but main NEVER calls it (dead code).
    print([{"id": i} for i in range(3)])


if __name__ == "__main__":
    main()
