# Commerce Ontology Hierarchy Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative hierarchy model of the
Commerce Ontology.

The Hierarchy Model establishes explicit,
directed, and auditable parent-child
relationships between registered Ontology
Nodes.

---

## Hierarchy Assertion

A Hierarchy Assertion declares one explicit
semantic relationship between one Parent Node
and one Child Node.

Every Hierarchy Assertion shall reference:

Canonical Identifier.

Parent Node.

Child Node.

Canonical Relationship Type.

Directionality.

Lifecycle Status.

Evidence Reference.

---

## Canonical Hierarchy Relationship

The canonical hierarchy relationship type is:

Is A.

An Is A assertion means that the Child Node
is a semantic specialization of the Parent
Node.

---

## Parent Node

A Parent Node represents the broader
canonical semantic category.

A Parent Node may contain one or more direct
Child Nodes.

---

## Child Node

A Child Node represents a narrower canonical
semantic specialization.

Every Child Node shall reference at least one
explicit Parent Node.

---

## Root Node

Commerce is the root Ontology Node of the
Commerce Ontology.

The Commerce root node shall not declare a
parent within the Commerce Ontology.

---

## Initial Hierarchy

Commerce

↓

Retail

Commerce

↓

Wholesale

Commerce

↓

Ecommerce

Commerce

↓

Informal Commerce

Product

↓

SKU

Inventory

↓

SKU Inventory

Channel

↓

Retail Channel

Channel

↓

Wholesale Channel

Channel

↓

Ecommerce Channel

Channel

↓

Informal Commerce Channel

---

## Directionality

Hierarchy Assertions are directed from the
broader Parent Node to the narrower Child
Node.

Parent Node

↓

Child Node

Directionality shall be explicit.

---

## Transitivity

Hierarchy transitivity may be derived only
from explicit valid hierarchy assertions.

Derived transitivity shall not replace
explicit direct parent-child assertions.

---

## Multiple Inheritance

A Child Node may declare more than one Parent
Node only when each parent relationship is
semantically valid and explicitly audited.

Multiple inheritance shall not create
contradictory canonical meaning.

---

## Hierarchy Constraints

Every Parent Node shall be a registered
Ontology Node.

Every Child Node shall be a registered
Ontology Node.

Every Hierarchy Assertion shall use the
canonical Is A relationship type.

A Node shall not be its own ancestor.

Circular hierarchy paths shall be prohibited.

Duplicate parent-child assertions shall be
prohibited.

Implicit hierarchy shall not be treated as
normative.

Domain-specific hierarchy shall not redefine
canonical Commerce semantics.

---

## Hierarchy Invariants

Canonical Identity Preservation.

Explicit Parentage.

Direction Preservation.

Acyclicity.

No Self-Ancestry.

No Duplicate Assertions.

Hierarchy Consistency.

Vocabulary Compatibility.

Traceability Closure.

---

## Audit Evidence

Every Hierarchy Assertion shall produce
deterministic audit evidence.

Audit Evidence shall identify:

Hierarchy Assertion Identifier.

Parent Node Identifier.

Child Node Identifier.

Relationship Type.

Validation Result.

Failure Reason.

---

## Release Criteria

Hierarchy Assertion is explicitly defined.

Canonical hierarchy relationship is defined.

Root Node is declared.

Initial hierarchy is declared.

Directionality is declared.

Transitivity is constrained.

Multiple inheritance is constrained.

Circularity is prohibited.

Hierarchy invariants are declared.

Audit Evidence is defined.
