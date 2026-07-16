# HAS Release Gates

Version

1.0

Status

Draft

---

## Runtime Invariant Gate

Command

python -m pytest tests/runtime/invariants -q

Purpose

Validate every executable invariant protecting
the HAS Runtime Kernel.

---

## Runtime Gate

Command

python -m pytest tests/runtime -q

Purpose

Validate the complete Runtime implementation.

