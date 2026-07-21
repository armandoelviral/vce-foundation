# Semantic Relationship Model

Version

1.0

Status

Draft

---

## Purpose

Define the canonical relationship types used
by the Commerce Knowledge Platform.

Semantic relationships shall express explicit
meaning between registered knowledge objects.

---

## Relationship Types

Is A.

Part Of.

Contains.

Uses.

Used By.

Sold Through.

Supports.

Tracked As.

Applies To.

Related To.

---

## Directionality

Every relationship shall declare direction.

A relationship may be:

Unidirectional.

Bidirectional.

Inverse-Paired.

---

## Inverse Relationships

Part Of

is inverse to

Contains.

Uses

is inverse to

Used By.

---

## Relationship Properties

Canonical Identifier.

Source Object.

Relationship Type.

Target Object.

Directionality.

Inverse Relationship.

Status.

---

## Constraints

Every relationship shall reference registered
knowledge objects.

Every relationship type shall be canonical.

Ambiguous relationships shall not be used.

Related To shall be used only when no more
specific canonical relationship applies.

Inverse relationships shall remain
semantically consistent.

---

## Runtime Invariants

Relationship Identity Preservation.

Relationship Direction Preservation.

Inverse Consistency.

Semantic Closure.

---

## Release Criteria

Canonical relationship types are defined.

Directionality is defined.

Inverse relationships are defined.

Constraints are declared.

Runtime invariants are declared.
