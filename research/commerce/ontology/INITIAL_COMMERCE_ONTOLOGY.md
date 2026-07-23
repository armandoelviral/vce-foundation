# Initial Commerce Ontology

Version

1.0

Status

Draft

---

## Purpose

Define the first concrete and auditable
Commerce Ontology using exclusively the first
ten registered Canonical Commerce Terms.

No unregistered Knowledge Object participates
in this ontology.

---

## Ontology Boundary

The Initial Commerce Ontology contains exactly
ten Ontology Nodes.

Every Ontology Node references one registered
Canonical Commerce Term.

No additional node may enter this ontology
without prior registration in the Knowledge
Registry.

---

## Ontology Nodes

### CKP-TERM-000001

Preferred Name

Commerce

Ontology Class

Commerce Domain

Lifecycle Status

Draft

---

### CKP-TERM-000002

Preferred Name

Retail

Ontology Class

Commerce Model

Lifecycle Status

Draft

---

### CKP-TERM-000003

Preferred Name

Wholesale

Ontology Class

Commerce Model

Lifecycle Status

Draft

---

### CKP-TERM-000004

Preferred Name

Ecommerce

Ontology Class

Commerce Channel Model

Lifecycle Status

Draft

---

### CKP-TERM-000005

Preferred Name

Informal Commerce

Ontology Class

Commerce Model

Lifecycle Status

Draft

---

### CKP-TERM-000006

Preferred Name

Product

Ontology Class

Commerce Object

Lifecycle Status

Draft

---

### CKP-TERM-000007

Preferred Name

SKU

Ontology Class

Commerce Object

Lifecycle Status

Draft

---

### CKP-TERM-000008

Preferred Name

Inventory

Ontology Class

Commerce State

Lifecycle Status

Draft

---

### CKP-TERM-000009

Preferred Name

Customer

Ontology Class

Commerce Participant

Lifecycle Status

Draft

---

### CKP-TERM-000010

Preferred Name

Channel

Ontology Class

Commerce Path

Lifecycle Status

Draft

---

## Root Node

CKP-TERM-000001

Commerce

Commerce is the root Ontology Node.

Commerce shall not declare a parent inside
the Initial Commerce Ontology.

---

## Hierarchy Assertions

### CKP-REL-000001

Parent Node

CKP-TERM-000001

Relationship Type

Is A

Child Node

CKP-TERM-000002

Directionality

Unidirectional

Assertion

Retail Is A Commerce.

Status

Draft

---

### CKP-REL-000002

Parent Node

CKP-TERM-000001

Relationship Type

Is A

Child Node

CKP-TERM-000003

Directionality

Unidirectional

Assertion

Wholesale Is A Commerce.

Status

Draft

---

### CKP-REL-000003

Parent Node

CKP-TERM-000001

Relationship Type

Is A

Child Node

CKP-TERM-000004

Directionality

Unidirectional

Assertion

Ecommerce Is A Commerce.

Status

Draft

---

### CKP-REL-000004

Parent Node

CKP-TERM-000001

Relationship Type

Is A

Child Node

CKP-TERM-000005

Directionality

Unidirectional

Assertion

Informal Commerce Is A Commerce.

Status

Draft

---

## Semantic Relationship Assertions

### CKP-REL-000005

Source Node

CKP-TERM-000007

Relationship Type

Part Of

Target Node

CKP-TERM-000006

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000006

Assertion

SKU Part Of Product.

Status

Draft

---

### CKP-REL-000006

Source Node

CKP-TERM-000006

Relationship Type

Contains

Target Node

CKP-TERM-000007

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000005

Assertion

Product Contains SKU.

Status

Draft

---

### CKP-REL-000007

Source Node

CKP-TERM-000006

Relationship Type

Tracked As

Target Node

CKP-TERM-000007

Directionality

Unidirectional

Inverse Relationship Reference

None

Assertion

Product Tracked As SKU.

Status

Draft

---

### CKP-REL-000008

Source Node

CKP-TERM-000002

Relationship Type

Uses

Target Node

CKP-TERM-000010

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000009

Assertion

Retail Uses Channel.

Status

Draft

---

### CKP-REL-000009

Source Node

CKP-TERM-000010

Relationship Type

Used By

Target Node

CKP-TERM-000002

Directionality

Inverse-Paired

Inverse Relationship Reference

CKP-REL-000008

Assertion

Channel Used By Retail.

Status

Draft

---

### CKP-REL-000010

Source Node

CKP-TERM-000006

Relationship Type

Sold Through

Target Node

CKP-TERM-000010

Directionality

Unidirectional

Inverse Relationship Reference

None

Assertion

Product Sold Through Channel.

Status

Draft

---

### CKP-REL-000011

Source Node

CKP-TERM-000008

Relationship Type

Applies To

Target Node

CKP-TERM-000007

Directionality

Unidirectional

Inverse Relationship Reference

None

Assertion

Inventory Applies To SKU.

Status

Draft

---

### CKP-REL-000012

Source Node

CKP-TERM-000009

Relationship Type

Uses

Target Node

CKP-TERM-000010

Directionality

Unidirectional

Inverse Relationship Reference

None

Assertion

Customer Uses Channel.

Status

Draft

---

## Domain Membership Assertions

CKP-TERM-000001 applies to Commerce.

CKP-TERM-000002 applies to Retail.

CKP-TERM-000003 applies to Wholesale.

CKP-TERM-000004 applies to Ecommerce.

CKP-TERM-000005 applies to Informal Commerce.

CKP-TERM-000006 applies to Commerce.

CKP-TERM-000007 applies to Commerce.

CKP-TERM-000008 applies to Commerce.

CKP-TERM-000009 applies to Commerce.

CKP-TERM-000010 applies to Commerce.

---

## Ontology Constraints

Every Ontology Node shall reference one of the
first ten registered Canonical Terms.

Every Relationship Assertion shall reference
registered Ontology Nodes.

Every Relationship Assertion shall use a
canonical Relationship Type.

Every assertion shall declare directionality.

Inverse-paired assertions shall reference one
another consistently.

Commerce shall remain the only root node.

No Ontology Node shall be its own ancestor.

No duplicate semantic assertion shall exist.

No frozen canonical definition shall be
privately redefined.

---

## Ontology Invariants

Canonical Identity Preservation.

Vocabulary Compatibility.

Registered Object Closure.

Single Root Preservation.

Hierarchy Acyclicity.

Relationship Direction Preservation.

Inverse Relationship Consistency.

No Duplicate Assertions.

Domain Separation.

Semantic Closure.

Traceability Closure.

---

## Audit Evidence

The Initial Commerce Ontology shall produce
deterministic audit evidence for:

Node Registration.

Canonical Identity.

Root Validation.

Hierarchy Validation.

Relationship Type Validation.

Directionality Validation.

Inverse Consistency.

Duplicate Detection.

Registry Closure.

Semantic Closure.

---

## Release Criteria

Exactly ten Ontology Nodes are declared.

Commerce is the only root Ontology Node.

Four hierarchy assertions are declared.

Twelve canonical Relationship Assertions are
declared.

All assertions reference registered Ontology
Nodes.

All relationship types are canonical.

Inverse-paired assertions are consistent.

No duplicate assertion exists.

Ontology invariants are declared.

Audit Evidence requirements are declared.
