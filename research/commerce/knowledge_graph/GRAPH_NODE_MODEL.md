# Commerce Knowledge Graph Node Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative Graph Node model of the
Commerce Knowledge Graph.

A Graph Node represents one registered
Knowledge Object without redefining its
canonical identity or semantics.

---

## Graph Node

Every Graph Node shall represent exactly one
registered Knowledge Object.

A Graph Node is a graph representation of
source knowledge.

A Graph Node shall not become an independent
source of canonical meaning.

---

## Graph Node Properties

Every Graph Node shall declare:

Canonical Identifier.

Knowledge Object Type.

Preferred Name.

Canonical Definition Reference.

Lifecycle Status.

Ontology Membership.

Domain Membership.

Registry Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Source Evidence Reference.

Node Integrity Reference.

---

## Canonical Identity

A Graph Node shall inherit the Canonical
Identifier of its registered Knowledge
Object.

Graph representation shall not allocate a
second semantic identifier for the same
Knowledge Object.

The Canonical Identifier shall remain
immutable.

The Canonical Identifier shall remain the
primary identity of the Graph Node.

---

## Knowledge Object Reference

Every Graph Node shall reference one object
registered in the Knowledge Registry.

The Registry Reference shall resolve to the
same Canonical Identifier declared by the
Graph Node.

No unregistered object may be represented as
a Graph Node.

---

## Preferred Name

Every Graph Node shall preserve the Preferred
Name of its registered Knowledge Object.

A display label may differ only as a
non-normative presentation property.

A display label shall not replace the
Preferred Name.

---

## Canonical Definition

A Graph Node shall not copy, rewrite, shorten,
extend, or privately redefine a frozen
Canonical Definition.

The Canonical Definition Reference shall
resolve to the definition maintained by the
Knowledge Registry.

---

## Knowledge Object Type

Every Graph Node shall preserve the canonical
Knowledge Object Type of its registered
source object.

Initial Graph Nodes use the TERM Knowledge
Object Type.

Future Graph Nodes may use other object types
only after those objects are registered.

---

## Lifecycle Status

Every Graph Node shall declare one Lifecycle
Status.

Permitted initial values are:

Draft.

Approved.

Deprecated.

Retired.

Graph Node lifecycle shall remain compatible
with the lifecycle of its source Knowledge
Object.

A Graph Node shall not remain active after
its source Knowledge Object is Retired.

---

## Ontology Membership

Every Graph Node shall reference its frozen
CKP-002 Ontology membership.

Ontology membership shall not be inferred by
the Graph.

The Graph shall preserve the Ontology Class
and assertions already established by
CKP-002.

---

## Domain Membership

Every Graph Node shall preserve one or more
canonical Domain Membership assertions.

Domain Membership shall derive from the
frozen Commerce Ontology.

Domain-specific presentation shall not
redefine canonical domain membership.

---

## Registry Reference

Every Graph Node shall maintain a resolvable
reference to its source Knowledge Registry
record.

Registry resolution shall verify:

Canonical Identifier.

Preferred Name.

Knowledge Object Type.

Lifecycle Status.

---

## Baseline References

Every Graph Node shall reference:

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

Baseline references shall remain explicit and
auditable.

---

## Node Integrity

Every Graph Node shall possess one
deterministic Node Integrity Reference.

Node Integrity shall bind:

Canonical Identifier.

Knowledge Object Type.

Preferred Name.

Lifecycle Status.

Ontology Membership.

Domain Membership.

Registry Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

---

## Root Graph Node

CKP-TERM-000001 is the root Graph Node of the
initial Commerce Knowledge Graph.

Its Preferred Name is Commerce.

The root Graph Node shall not declare an
incoming canonical Is A edge inside the
initial graph.

Exactly one root Graph Node shall exist.

---

## Initial Graph Nodes

The initial Commerce Knowledge Graph shall
contain exactly these Graph Nodes:

CKP-TERM-000001 Commerce.

CKP-TERM-000002 Retail.

CKP-TERM-000003 Wholesale.

CKP-TERM-000004 Ecommerce.

CKP-TERM-000005 Informal Commerce.

CKP-TERM-000006 Product.

CKP-TERM-000007 SKU.

CKP-TERM-000008 Inventory.

CKP-TERM-000009 Customer.

CKP-TERM-000010 Channel.

No additional Graph Node may enter the
initial graph.

---

## Deterministic Ordering

Graph Nodes shall be ordered by Canonical
Identifier when no explicit semantic order is
defined.

Identical Graph Node sets shall produce the
same deterministic ordering.

Presentation order shall not alter semantic
identity.

---

## Node Equality

Two Graph Node representations are equal
when all normative Graph Node Properties are
equal.

Display-only presentation properties shall
not affect normative Graph Node equality.

Two different Canonical Identifiers shall
never represent the same Graph Node.

---

## Node Constraints

Every Graph Node shall reference one
registered Knowledge Object.

Every Graph Node shall preserve one immutable
Canonical Identifier.

Every Graph Node shall preserve its Preferred
Name.

Every Graph Node shall preserve its Knowledge
Object Type.

Every Graph Node shall reference the frozen
Vocabulary and Ontology baselines.

No Graph Node shall privately redefine
canonical Commerce semantics.

No duplicate Canonical Identifier shall exist
inside one Commerce Knowledge Graph.

No orphan Graph Node shall exist.

No Graph Node shall represent more than one
Knowledge Object.

---

## Node Invariants

Canonical Identity Preservation.

Registered Object Closure.

Preferred Name Preservation.

Knowledge Object Type Preservation.

Lifecycle Compatibility.

Ontology Membership Preservation.

Domain Membership Preservation.

Vocabulary Compatibility.

Ontology Compatibility.

No Duplicate Nodes.

No Orphan Nodes.

Deterministic Ordering.

Normative Equality.

Semantic Closure.

Traceability Closure.

Node Evidence Completeness.

---

## Node Validation Evidence

Every Graph Node validation shall produce
deterministic Node Validation Evidence.

Node Validation Evidence shall declare:

Evidence Identifier.

Canonical Identifier.

Registry Resolution Result.

Preferred Name Validation.

Knowledge Object Type Validation.

Lifecycle Validation.

Ontology Membership Validation.

Domain Membership Validation.

Vocabulary Baseline Validation.

Ontology Baseline Validation.

Node Integrity Result.

Validation Result.

Failure Reason.

---

## Release Criteria

Graph Node is explicitly defined.

Graph Node Properties are explicitly defined.

Canonical Identity behavior is defined.

Knowledge Registry resolution is defined.

Preferred Name preservation is defined.

Canonical Definition behavior is defined.

Knowledge Object Type preservation is
defined.

Lifecycle behavior is defined.

Ontology and Domain Membership are defined.

Baseline References are defined.

Node Integrity is defined.

Root Graph Node is declared.

Initial Graph Nodes are declared.

Deterministic Ordering is defined.

Node Equality is defined.

Node Constraints are declared.

Node Invariants are declared.

Node Validation Evidence is defined.
