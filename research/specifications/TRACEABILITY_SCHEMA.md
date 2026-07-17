# HAS Specification Traceability Schema

Version

1.1

Status

Draft

---

## Purpose

Define the normative structure of the
Specification Traceability Registry.

The schema defines relationships.

It does not contain implementation evidence.

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

Normative capability required by the Claim.

Executable Contracts

One or more executable contracts providing
objective evidence.

---

## Relationship

Normative Claim

↓

Specification Asset

↓

Capability

↓

Executable Contract(s)

---

## Runtime Mapping

Runtime components are intentionally outside
the scope of the Specification Platform.

They shall be introduced by the
Conformance milestone.

---

## Constraints

Every Claim shall reference exactly one
Specification Asset.

Every Claim shall reference at least one
Capability.

Every Capability shall reference at least one
Executable Contract.
