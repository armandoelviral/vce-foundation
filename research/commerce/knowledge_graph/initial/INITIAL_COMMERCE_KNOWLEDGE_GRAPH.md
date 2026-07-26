# Initial Commerce Knowledge Graph

Version

1.0

Status

Draft

---

## Purpose

Materialize the frozen CKP-002 Commerce
Ontology as the first canonical, directed,
traceable, and auditable Commerce Knowledge
Graph.

The Initial Commerce Knowledge Graph shall
not create, infer, extend, or redefine
canonical Commerce semantics.

---

## Graph Manifest

Graph Identifier

CKP-GRAPH-000001

Graph Version

1.0

Lifecycle Status

Draft

Root Node Identifier

CKP-TERM-000001

Node Count

10

Edge Count

12

Vocabulary Baseline

CKP-001 Canonical Commerce Vocabulary 1.0

Ontology Baseline

CKP-002 Commerce Ontology 1.0

Node Registry Reference

research/commerce/registry/TERM_REGISTRY.md

Edge Registry Reference

research/commerce/ontology/INITIAL_COMMERCE_ONTOLOGY.md

Graph Integrity Reference

CKP-GRAPH-INTEGRITY-000001

---

## Graph Boundary

The Initial Commerce Knowledge Graph contains
exactly ten Graph Nodes.

The Initial Commerce Knowledge Graph contains
exactly twelve Graph Edges.

Every Graph Node derives from one registered
Canonical Commerce Term.

Every Graph Edge derives from one frozen
CKP-002 Ontology Assertion.

No unregistered Knowledge Object participates
in the Graph.

No implicit Graph Edge participates in the
Graph.

---

## Root Graph Node

Canonical Identifier

CKP-TERM-000001

Preferred Name

Commerce

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Domain

Domain Membership

Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000001_COMMERCE.md

Vocabulary Baseline Reference

CKP-001 Canonical Commerce Vocabulary 1.0

Ontology Baseline Reference

CKP-002 Commerce Ontology 1.0

Node Integrity Reference

CKP-NODE-INTEGRITY-000001

Root Status

Root

Commerce is the only root Graph Node.

Commerce has no outgoing canonical Is A edge
inside the Initial Commerce Knowledge Graph.

---

## Graph Nodes

### CKP-TERM-000001

Preferred Name

Commerce

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Domain

Domain Membership

Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000001_COMMERCE.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000001

---

### CKP-TERM-000002

Preferred Name

Retail

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Model

Domain Membership

Retail

Registry Reference

research/commerce/registry/terms/CKP-TERM-000002_RETAIL.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000002

---

### CKP-TERM-000003

Preferred Name

Wholesale

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Model

Domain Membership

Wholesale

Registry Reference

research/commerce/registry/terms/CKP-TERM-000003_WHOLESALE.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000003

---

### CKP-TERM-000004

Preferred Name

Ecommerce

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Channel Model

Domain Membership

Ecommerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000004_ECOMMERCE.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000004

---

### CKP-TERM-000005

Preferred Name

Informal Commerce

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Model

Domain Membership

Informal Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000005_INFORMAL_COMMERCE.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000005

---

### CKP-TERM-000006

Preferred Name

Product

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Object

Domain Membership

Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000006_PRODUCT.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000006

---

### CKP-TERM-000007

Preferred Name

SKU

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Object

Domain Membership

Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000007_SKU.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000007

---

### CKP-TERM-000008

Preferred Name

Inventory

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce State

Domain Membership

Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000008_INVENTORY.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000008

---

### CKP-TERM-000009

Preferred Name

Customer

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Participant

Domain Membership

Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000009_CUSTOMER.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000009

---

### CKP-TERM-000010

Preferred Name

Channel

Knowledge Object Type

TERM

Lifecycle Status

Draft

Ontology Membership

Commerce Path

Domain Membership

Commerce

Registry Reference

research/commerce/registry/terms/CKP-TERM-000010_CHANNEL.md

Node Integrity Reference

CKP-NODE-INTEGRITY-000010

---

## Hierarchy Graph Edges

### CKP-REL-000001

Source Node Identifier

CKP-TERM-000002

Canonical Relationship Type

Is A

Target Node Identifier

CKP-TERM-000001

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000001

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000001

Assertion

Retail Is A Commerce.

---

### CKP-REL-000002

Source Node Identifier

CKP-TERM-000003

Canonical Relationship Type

Is A

Target Node Identifier

CKP-TERM-000001

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000002

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000002

Assertion

Wholesale Is A Commerce.

---

### CKP-REL-000003

Source Node Identifier

CKP-TERM-000004

Canonical Relationship Type

Is A

Target Node Identifier

CKP-TERM-000001

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000003

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000003

Assertion

Ecommerce Is A Commerce.

---

### CKP-REL-000004

Source Node Identifier

CKP-TERM-000005

Canonical Relationship Type

Is A

Target Node Identifier

CKP-TERM-000001

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000004

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000004

Assertion

Informal Commerce Is A Commerce.

---

## Semantic Graph Edges

### CKP-REL-000005

Source Node Identifier

CKP-TERM-000007

Canonical Relationship Type

Part Of

Target Node Identifier

CKP-TERM-000006

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000006

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000005

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000005

Assertion

SKU Part Of Product.

---

### CKP-REL-000006

Source Node Identifier

CKP-TERM-000006

Canonical Relationship Type

Contains

Target Node Identifier

CKP-TERM-000007

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000005

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000006

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000006

Assertion

Product Contains SKU.

---

### CKP-REL-000007

Source Node Identifier

CKP-TERM-000006

Canonical Relationship Type

Tracked As

Target Node Identifier

CKP-TERM-000007

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000007

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000007

Assertion

Product Tracked As SKU.

---

### CKP-REL-000008

Source Node Identifier

CKP-TERM-000002

Canonical Relationship Type

Uses

Target Node Identifier

CKP-TERM-000010

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000009

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000008

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000008

Assertion

Retail Uses Channel.

---

### CKP-REL-000009

Source Node Identifier

CKP-TERM-000010

Canonical Relationship Type

Used By

Target Node Identifier

CKP-TERM-000002

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000008

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000009

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000009

Assertion

Channel Used By Retail.

---

### CKP-REL-000010

Source Node Identifier

CKP-TERM-000006

Canonical Relationship Type

Sold Through

Target Node Identifier

CKP-TERM-000010

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000010

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000010

Assertion

Product Sold Through Channel.

---

### CKP-REL-000011

Source Node Identifier

CKP-TERM-000008

Canonical Relationship Type

Applies To

Target Node Identifier

CKP-TERM-000007

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000011

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000011

Assertion

Inventory Applies To SKU.

---

### CKP-REL-000012

Source Node Identifier

CKP-TERM-000009

Canonical Relationship Type

Uses

Target Node Identifier

CKP-TERM-000010

Directionality

Unidirectional

Inverse Relationship Reference

None

Lifecycle Status

Draft

Ontology Assertion Reference

CKP-REL-000012

Edge Integrity Reference

CKP-EDGE-INTEGRITY-000012

Assertion

Customer Uses Channel.

---

## Deterministic Node Order

CKP-TERM-000001

CKP-TERM-000002

CKP-TERM-000003

CKP-TERM-000004

CKP-TERM-000005

CKP-TERM-000006

CKP-TERM-000007

CKP-TERM-000008

CKP-TERM-000009

CKP-TERM-000010

---

## Deterministic Edge Order

CKP-REL-000001

CKP-REL-000002

CKP-REL-000003

CKP-REL-000004

CKP-REL-000005

CKP-REL-000006

CKP-REL-000007

CKP-REL-000008

CKP-REL-000009

CKP-REL-000010

CKP-REL-000011

CKP-REL-000012

---

## Registered Direct Paths

### CKP-PATH-000001

Start Node Identifier

CKP-TERM-000002

End Node Identifier

CKP-TERM-000001

Ordered Node Sequence

CKP-TERM-000002

CKP-TERM-000001

Ordered Edge Sequence

CKP-REL-000001

Traversal Direction

Forward

Path Length

1

Assertion

Retail Is A Commerce.

---

### CKP-PATH-000002

Start Node Identifier

CKP-TERM-000007

End Node Identifier

CKP-TERM-000006

Ordered Node Sequence

CKP-TERM-000007

CKP-TERM-000006

Ordered Edge Sequence

CKP-REL-000005

Traversal Direction

Forward

Path Length

1

Assertion

SKU Part Of Product.

---

### CKP-PATH-000003

Start Node Identifier

CKP-TERM-000006

End Node Identifier

CKP-TERM-000010

Ordered Node Sequence

CKP-TERM-000006

CKP-TERM-000010

Ordered Edge Sequence

CKP-REL-000010

Traversal Direction

Forward

Path Length

1

Assertion

Product Sold Through Channel.

---

## Registered Composite Path

### CKP-PATH-000004

Start Node Identifier

CKP-TERM-000008

End Node Identifier

CKP-TERM-000006

Ordered Node Sequence

CKP-TERM-000008

CKP-TERM-000007

CKP-TERM-000006

Ordered Edge Sequence

CKP-REL-000011

CKP-REL-000005

Traversal Direction

Forward

Path Length

2

Assertions

Inventory Applies To SKU.

SKU Part Of Product.

Path Continuity

Valid

---

## Graph Constraints

Every Graph Node shall reference one
registered Canonical Commerce Term.

Every Graph Edge shall reference registered
Source and Target Graph Nodes.

Every Graph Edge shall derive from one frozen
CKP-002 Ontology Assertion.

Every Graph Edge shall use one canonical
Relationship Type.

Every Graph Edge shall preserve its frozen
directionality.

Every inverse-paired Graph Edge shall
reference its canonical inverse.

Commerce shall remain the only root Graph
Node.

Hierarchy Graph Edges shall remain acyclic.

No duplicate Graph Node shall exist.

No duplicate Graph Edge shall exist.

No orphan Graph Node shall exist.

No orphan Graph Edge shall exist.

No implicit Graph Edge shall exist.

No initial Graph Edge shall be reflexive.

No Graph Component shall privately redefine
canonical Commerce semantics.

---

## Graph Invariants

Canonical Identity Preservation.

Registered Node Closure.

Canonical Edge Closure.

Single Root Preservation.

Direction Preservation.

Inverse Relationship Consistency.

Hierarchy Acyclicity.

No Duplicate Nodes.

No Duplicate Edges.

No Orphan Nodes.

No Orphan Edges.

No Implicit Edges.

No Initial Reflexivity.

Path Continuity.

Deterministic Node Ordering.

Deterministic Edge Ordering.

Vocabulary Compatibility.

Ontology Compatibility.

Semantic Closure.

Traceability Closure.

Graph Evidence Completeness.

---

## Graph Validation Evidence

The Initial Commerce Knowledge Graph shall
produce deterministic validation evidence
for:

Graph Manifest Validation.

Node Count Validation.

Edge Count Validation.

Root Node Validation.

Node Registry Closure.

Edge Ontology Closure.

Relationship Type Validation.

Directionality Validation.

Inverse Relationship Validation.

Hierarchy Acyclicity Validation.

Duplicate Node Detection.

Duplicate Edge Detection.

Orphan Node Detection.

Orphan Edge Detection.

Reflexivity Validation.

Path Continuity Validation.

Deterministic Ordering Validation.

Vocabulary Baseline Validation.

Ontology Baseline Validation.

Graph Integrity Validation.

---

## Graph Integrity

Graph Integrity Reference

CKP-GRAPH-INTEGRITY-000001

Graph Integrity shall bind:

Graph Identifier.

Graph Version.

Root Node Identifier.

Deterministic Node Order.

Deterministic Edge Order.

Vocabulary Baseline.

Ontology Baseline.

Node Count.

Edge Count.

---

## Release Criteria

One Graph Manifest is declared.

Graph Identifier CKP-GRAPH-000001 is
declared.

Exactly ten Graph Nodes are declared.

Exactly twelve Graph Edges are declared.

Exactly one root Graph Node is declared.

CKP-TERM-000001 is the root Graph Node.

Every Graph Node references a registered
Canonical Commerce Term.

Every Graph Edge derives from a frozen CKP-002
Ontology Assertion.

Four hierarchy Graph Edges are declared.

Eight semantic Graph Edges are declared.

Canonical directionality is preserved.

Inverse-paired Graph Edges are consistent.

Deterministic Node Order is declared.

Deterministic Edge Order is declared.

Registered Graph Paths are declared.

Path Continuity is demonstrated.

Graph Constraints are declared.

Graph Invariants are declared.

Graph Validation Evidence is declared.

Graph Integrity is declared.
