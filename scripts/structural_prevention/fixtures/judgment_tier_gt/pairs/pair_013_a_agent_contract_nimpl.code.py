#!/usr/bin/env python3
"""Embodiment pair 13 — claims to enforce but does NOT.

TODO: we intend to enforce the records. The contract requires us to enforce each one. For now this
only loads and prints them; the enforce step is not built.
"""


def load(records):
    # NOTE: a real implementation would enforce() each record. It does not yet.
    return list(records)


def main():
    print(load([{"id": i} for i in range(3)]))   # only loads; never enforces


if __name__ == "__main__":
    main()
