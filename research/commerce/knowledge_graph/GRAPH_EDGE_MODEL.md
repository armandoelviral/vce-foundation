# Commerce Knowledge Graph Edge Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative Graph Edge model of the
Commerce Knowledge Graph.

A Graph Edge represents one frozen Ontology
Assertion without creating, extending, or
redefining canonical Commerce semantics.

---

## Graph Edge

Every Graph Edge shall represent exactly one
frozen CKP-002 Ontology Assertion.

A Graph Edge is a directed graph
representation of an existing semantic
assertion.

A Graph Edge shall not become an independent
source of canonical meaning.

---

## Graph Edge Properties

Every Graph Edge shall declare:

Relationship Identifier.

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

Directionality.

Inverse Relationship Reference.

Lifecycle Status.

Ontology Assertion Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Source Evidence Reference.

Edge Integrity Reference.

---

## Relationship Identity

A Graph Edge shall inherit the Relationship
Identifier of its frozen Ontology Assertion.

Graph representation shall not allocate a
second semantic identifier for the same
Ontology Assertion.

The Relationship Identifier shall remain
immutable.

Relationship Identifiers shall never be
reused.

---

## Ontology Assertion Reference

Every Graph Edge shall reference exactly one
frozen CKP-002 Ontology Assertion.

The Ontology Assertion Reference shall
resolve to the same:

Relationship Identifier.

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

Directionality.

Inverse Relationship Reference.

No Graph Edge may exist without a resolvable
Ontology Assertion Reference.

---

## Source Graph Node

Every Graph Edge shall reference one
registered Source Graph Node.

The Source Node Identifier shall resolve to
one Graph Node in the same Graph Manifest.

The Source Graph Node shall preserve its
Canonical Identifier.

No private Source Node Identifier may be
introduced.

---

## Target Graph Node

Every Graph Edge shall reference one
registered Target Graph Node.

The Target Node Identifier shall resolve to
one Graph Node in the same Graph Manifest.

The Target Graph Node shall preserve its
Canonical Identifier.

No private Target Node Identifier may be
introduced.

---

## Canonical Relationship Type

Every Graph Edge shall preserve the canonical
Relationship Type declared by its frozen
Ontology Assertion.

Initial canonical Relationship Types are:

Is A.

Part Of.

Contains.

Tracked As.

Uses.

Used By.

Sold Through.

Applies To.

A Graph Edge shall not replace a specific
canonical Relationship Type with Related To.

A Graph Edge shall not introduce a private
Relationship Type.

---

## Directionality

Every Graph Edge shall preserve the explicit
directionality of its frozen Ontology
Assertion.

Permitted directionality values are:

Unidirectional.

Bidirectional.

Inverse-Paired.

Source and Target presentation order shall
not redefine edge direction.

A reverse traversal shall not mutate the
original Graph Edge.

---

## Inverse Relationship Reference

Every Inverse-Paired Graph Edge shall
reference its canonical inverse Graph Edge.

The inverse Graph Edge shall:

Reference the same participating Graph Nodes.

Reverse Source and Target Node identifiers.

Use the canonical inverse Relationship Type.

Reference the original Graph Edge as its
inverse.

Preserve compatible Lifecycle Status.

A Unidirectional Graph Edge shall declare:

None

as its Inverse Relationship Reference.

---

## Canonical Inverse Pairs

Part Of

is inverse to

Contains.

Uses

is inverse to

Used By.

The initial graph shall preserve:

CKP-REL-000005

as inverse-paired with

CKP-REL-000006.

CKP-REL-000008

as inverse-paired with

CKP-REL-000009.

---

## Lifecycle Status

Every Graph Edge shall declare one Lifecycle
Status.

Permitted initial values are:

Draft.

Approved.

Deprecated.

Retired.

Graph Edge lifecycle shall remain compatible
with the lifecycle of its source Ontology
Assertion.

A Graph Edge shall not remain active after
its source Ontology Assertion is Retired.

Inverse-paired Graph Edges shall preserve
compatible lifecycle states.

---

## Baseline References

Every Graph Edge shall reference:

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

Baseline references shall remain explicit,
resolvable, and auditable.

---

## Edge Integrity

Every Graph Edge shall possess one
deterministic Edge Integrity Reference.

Edge Integrity shall bind:

Relationship Identifier.

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

Directionality.

Inverse Relationship Reference.

Lifecycle Status.

Ontology Assertion Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

---

## Initial Graph Edges

The initial Commerce Knowledge Graph shall
contain exactly these twelve Graph Edges:

CKP-REL-000001

Retail Is A Commerce.

CKP-REL-000002

Wholesale Is A Commerce.

CKP-REL-000003

Ecommerce Is A Commerce.

CKP-REL-000004

Informal Commerce Is A Commerce.

CKP-REL-000005

SKU Part Of Product.

CKP-REL-000006

Product Contains SKU.

CKP-REL-000007

Product Tracked As SKU.

CKP-REL-000008

Retail Uses Channel.

CKP-REL-000009

Channel Used By Retail.

CKP-REL-000010

Product Sold Through Channel.

CKP-REL-000011

Inventory Applies To SKU.

CKP-REL-000012

Customer Uses Channel.

No additional Graph Edge may enter the
initial graph.

---

## Hierarchy Edges

CKP-REL-000001 through CKP-REL-000004 are
canonical hierarchy Graph Edges.

Every hierarchy Graph Edge shall use the
canonical Is A Relationship Type.

Hierarchy Graph Edges shall be directed from
the specialized Source Graph Node to the
broader Target Graph Node.

Hierarchy Graph Edges shall preserve
acyclicity.

No Graph Node may become its own ancestor.

---

## Semantic Edges

CKP-REL-000005 through CKP-REL-000012 are
canonical semantic Graph Edges.

Semantic Graph Edges shall preserve the
Relationship Type, directionality, and
inverse references declared by CKP-002.

Semantic Graph Edges shall not create
undocumented meaning.

---

## Edge Uniqueness

A Graph Edge is uniquely identified by its
Relationship Identifier.

No duplicate Relationship Identifier shall
exist inside one Commerce Knowledge Graph.

Two Graph Edges shall not represent the same
normative assertion under different
Relationship Identifiers.

The tuple:

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

shall not be duplicated unless the ontology
explicitly distinguishes the assertions.

---

## Edge Equality

Two Graph Edge representations are equal
when all normative Graph Edge Properties are
equal.

Display-only presentation properties shall
not affect normative Graph Edge equality.

Different Relationship Identifiers shall not
be treated as the same Graph Edge.

---

## Deterministic Ordering

Graph Edges shall be ordered by Relationship
Identifier when no explicit semantic order is
defined.

Identical Graph Edge sets shall produce the
same deterministic ordering.

Presentation order shall not alter semantic
identity or directionality.

---

## Self-Reference

A Graph Edge shall not connect a Graph Node
to itself unless its canonical Relationship
Type explicitly permits reflexivity.

No initial Graph Edge permits reflexivity.

---

## Edge Constraints

Every Graph Edge shall reference one frozen
Ontology Assertion.

Every Graph Edge shall reference registered
Source and Target Graph Nodes.

Every Graph Edge shall preserve one immutable
Relationship Identifier.

Every Graph Edge shall use one canonical
Relationship Type.

Every Graph Edge shall preserve explicit
directionality.

Every Inverse-Paired Graph Edge shall
reference a consistent inverse Graph Edge.

Every Graph Edge shall reference the frozen
Vocabulary and Ontology baselines.

No Graph Edge shall privately redefine
canonical Commerce semantics.

No duplicate Graph Edge shall exist.

No orphan Graph Edge shall exist.

No implicit Graph Edge shall exist.

No initial Graph Edge shall be reflexive.

---

## Edge Invariants

Relationship Identity Preservation.

Ontology Assertion Closure.

Registered Source Node Closure.

Registered Target Node Closure.

Canonical Relationship Type Preservation.

Direction Preservation.

Inverse Relationship Consistency.

Lifecycle Compatibility.

Vocabulary Compatibility.

Ontology Compatibility.

No Duplicate Edges.

No Orphan Edges.

No Implicit Edges.

No Initial Reflexivity.

Deterministic Ordering.

Normative Equality.

Semantic Closure.

Traceability Closure.

Edge Evidence Completeness.

---

## Edge Validation Evidence

Every Graph Edge validation shall produce
deterministic Edge Validation Evidence.

Edge Validation Evidence shall declare:

Evidence Identifier.

Relationship Identifier.

Ontology Assertion Resolution Result.

Source Node Resolution Result.

Target Node Resolution Result.

Relationship Type Validation.

Directionality Validation.

Inverse Relationship Validation.

Lifecycle Validation.

Vocabulary Baseline Validation.

Ontology Baseline Validation.

Edge Integrity Result.

Duplicate Detection Result.

Reflexivity Validation.

Validation Result.

Failure Reason.

---

## Release Criteria

Graph Edge is explicitly defined.

Graph Edge Properties are explicitly defined.

Relationship Identity behavior is defined.

Ontology Assertion resolution is defined.

Source and Target Graph Node resolution is
defined.

Canonical Relationship Type preservation is
defined.

Directionality behavior is defined.

Inverse Relationship behavior is defined.

Lifecycle behavior is defined.

Baseline References are defined.

Edge Integrity is defined.

Initial Graph Edges are declared.

Hierarchy and Semantic Edges are
distinguished.

Edge Uniqueness is defined.

Edge Equality is defined.

Deterministic Ordering is defined.

Self-Reference behavior is defined.

Edge Constraints are declared.

Edge Invariants are declared.

Edge Validation Evidence is defined.
