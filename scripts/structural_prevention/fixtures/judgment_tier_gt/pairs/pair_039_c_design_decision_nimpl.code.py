#!/usr/bin/env python3
"""Embodiment pair 39 — claims to gate but does NOT.

TODO: we intend to gate the records. The contract requires us to gate each one. For now this
only loads and prints them; the gate step is not built.
"""


def load(records):
    # NOTE: a real implementation would gate() each record. It does not yet.
    return list(records)


def main():
    print(load([{"id": i} for i in range(3)]))   # only loads; never gates


if __name__ == "__main__":
    main()
