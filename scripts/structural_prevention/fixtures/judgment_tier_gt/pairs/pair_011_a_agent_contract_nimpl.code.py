#!/usr/bin/env python3
"""Embodiment pair 11 — enforce is a STUB that does nothing."""


def enforce_obligation_11(record):
    # STUB: contract says enforce, but this is not implemented.
    pass


def run(records):
    for r in records:
        enforce_obligation_11(r)          # called, but does nothing
    return records


def main():
    print(run([{"id": i} for i in range(3)]))


if __name__ == "__main__":
    main()
