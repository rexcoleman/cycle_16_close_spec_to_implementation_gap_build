#!/usr/bin/env python3
"""Embodiment pair 23 — claims to validate but does NOT.

TODO: we intend to validate the records. The contract requires us to validate each one. For now this
only loads and prints them; the validate step is not built.
"""


def load(records):
    # NOTE: a real implementation would validate() each record. It does not yet.
    return list(records)


def main():
    print(load([{"id": i} for i in range(3)]))   # only loads; never validates


if __name__ == "__main__":
    main()
