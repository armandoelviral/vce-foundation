# Commerce Ontology Relationship Assertion Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative model for explicit
semantic relationships between registered
Ontology Nodes.

A Relationship Assertion records one
canonical, directed, traceable, and auditable
semantic statement.

---

## Relationship Assertion

A Relationship Assertion connects one Source
Node to one Target Node through one canonical
Relationship Type.

Every Relationship Assertion shall declare:

Canonical Identifier.

Source Node.

Canonical Relationship Type.

Target Node.

Directionality.

Inverse Relationship Reference.

Lifecycle Status.

Evidence Reference.

---

## Source Node

The Source Node is the registered Ontology
Node from which the Relationship Assertion
originates.

The Source Node shall preserve its Canonical
Identifier.

---

## Target Node

The Target Node is the registered Ontology
Node to which the Relationship Assertion is
directed.

The Target Node shall preserve its Canonical
Identifier.

---

## Canonical Relationship Type

Every Relationship Assertion shall use one
relationship type defined by the frozen
Semantic Relationship Model.

Initial canonical relationship types include:

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

Every Relationship Assertion shall declare
explicit directionality.

A Relationship Assertion may be:

Unidirectional.

Bidirectional.

Inverse-Paired.

Directionality shall not be inferred from
presentation order.

---

## Inverse Relationship

Inverse-paired relationships shall declare an
explicit inverse Relationship Assertion.

Canonical inverse pairs include:

Part Of

is inverse to

Contains.

Uses

is inverse to

Used By.

An inverse relationship shall preserve the
same participating Ontology Nodes in reversed
semantic direction.

---

## Relationship Identity

Every Relationship Assertion shall possess
one immutable Canonical Identifier.

Example

CKP-REL-000001

Relationship identifiers shall never be
reused.

---

## Initial Relationship Assertions

Retail

Is A

Commerce.

Wholesale

Is A

Commerce.

Ecommerce

Is A

Commerce.

Informal Commerce

Is A

Commerce.

SKU

Part Of

Product.

Product

Contains

SKU.

Product

Tracked As

SKU.

Retail

Uses

Channel.

Channel

Used By

Retail.

Product

Sold Through

Channel.

Inventory

Applies To

SKU.

Customer

Uses

Channel.

---

## Relationship Constraints

Every Source Node shall be registered.

Every Target Node shall be registered.

Every Relationship Type shall be canonical.

Every Relationship Assertion shall declare
directionality.

Every inverse-paired assertion shall reference
its inverse assertion.

Relationship identifiers shall be unique.

Duplicate semantic assertions shall be
prohibited.

A Relationship Assertion shall not connect an
Ontology Node to itself unless the canonical
relationship explicitly permits reflexivity.

Related To shall be used only when no more
specific canonical Relationship Type applies.

No domain-specific assertion may redefine
frozen canonical Commerce semantics.

---

## Relationship Invariants

Canonical Identity Preservation.

Source Identity Preservation.

Target Identity Preservation.

Direction Preservation.

Inverse Consistency.

Relationship Type Canonicality.

No Duplicate Assertions.

Registered Node Closure.

Semantic Closure.

Traceability Closure.

---

## Audit Evidence

Every Relationship Assertion shall produce
deterministic audit evidence.

Audit Evidence shall declare:

Relationship Assertion Identifier.

Source Node Identifier.

Relationship Type.

Target Node Identifier.

Directionality.

Inverse Relationship Identifier.

Validation Result.

Failure Reason.

---

## Release Criteria

Relationship Assertion is explicitly defined.

Source and Target Nodes are explicitly
defined.

Canonical Relationship Types are declared.

Directionality is declared.

Inverse relationships are constrained.

Relationship identity is defined.

Initial Relationship Assertions are declared.

Relationship constraints are declared.

Relationship invariants are declared.

Audit Evidence is defined.
