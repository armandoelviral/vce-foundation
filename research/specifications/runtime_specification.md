# HAS Runtime Specification

Version

0.1

Status

Draft

---

## Purpose

Describe the executable semantics of the
Knowledge Runtime independently from the
implementation.

The specification is normative.

The implementation must conform to it.

---

# Knowledge States

The Runtime recognizes exactly four
knowledge states.

1. Observation

2. Hypothesis

3. Candidate Principle

4. Principle

No additional states are currently part of
the executable specification.

---

# Allowed Transitions

The Runtime permits only the following
state transitions.

Observation

↓

Hypothesis

Hypothesis

↓

Candidate Principle

Candidate Principle

↓

Principle

Every other transition shall be rejected.

---

# Guaranteed Properties

The Runtime guarantees the following
properties.

- Replay Determinism

- History Integrity

- Verification Closure

- Pipeline Closure

- State Monotonicity

No additional guarantees are currently
defined by this specification.
