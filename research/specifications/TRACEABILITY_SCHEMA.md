# HAS Specification Traceability Schema

Version

1.0

Status

Draft

---

## Purpose

Define the normative structure of the
Specification Traceability Registry.

The schema defines relationships.

It does not contain traceability data.

---

## Traceability Unit

The primary traceability unit is the
Normative Claim.

Every Claim shall possess a stable identifier.

---

## Required Fields

Claim ID

Unique identifier.

Specification Asset

Normative document containing the Claim.

Capability

Runtime capability satisfying the Claim.

Executable Contracts

One or more executable contracts providing
objective evidence.

Runtime Components

One or more runtime components implementing
the Capability.

---

## Relationship

Normative Claim

↓

Specification Asset

↓

Capability

↓

Executable Contract(s)

↓

Runtime Component(s)

---

## Constraints

Every Claim shall reference exactly one
Specification Asset.

Every Claim shall reference at least one
Capability.

Every Capability shall reference at least one
Executable Contract.

Every Capability shall reference at least one
Runtime Component.

---

## Future Extensions

Bidirectional traceability.

Coverage analysis.

Impact analysis.

Dependency graph.

