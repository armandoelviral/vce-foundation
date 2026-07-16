# HAS Conformance Input Contract

Version

1.0

Status

Draft

---

## Purpose

Define the normative input required by the
Conformance Engine.

The Conformance Engine shall depend only
upon this contract.

---

## Required Inputs

Normative Claim

Capability

Executable Contract

Coverage Status

---

## Validation Rules

Every input shall reference exactly one
Normative Claim.

Every input shall reference exactly one
Capability.

Every input shall reference at least one
Executable Contract.

Coverage Status shall be either:

Covered

or

Not Covered.

---

## Failure Conditions

Missing Claim.

Missing Capability.

Missing Contract.

Undefined Coverage Status.

---

## Output

Conformance Decision.

Failure Reason.

