#!/usr/bin/env python3
"""Embodiment pair 53 — claims to check but does NOT.

TODO: we intend to check the records. The contract requires us to check each one. For now this
only loads and prints them; the check step is not built.
"""


def load(records):
    # NOTE: a real implementation would check() each record. It does not yet.
    return list(records)


def main():
    print(load([{"id": i} for i in range(3)]))   # only loads; never checks


if __name__ == "__main__":
    main()
