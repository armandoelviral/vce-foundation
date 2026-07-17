# HAS Conformance Evaluator Contract

Version

1.0

Status

Draft

---

## Purpose

Define the normative behavior of the
Conformance Evaluator.

The Evaluator applies the Decision Model
to validated Conformance Inputs.

It does not define decisions.

It does not execute runtime tests.

---

## Inputs

Validated Conformance Input.

Decision Model.

Evidence Model.

---

## Responsibilities

Validate Inputs.

Evaluate Evidence.

Apply Decision Rules.

Produce Conformance Decision.

---

## Outputs

Conformance Decision.

Failure Reason.

Evidence Summary.

---

## Constraints

The Evaluator shall be deterministic.

The Evaluator shall not modify
its inputs.

The Evaluator shall produce the same
decision for identical inputs.

