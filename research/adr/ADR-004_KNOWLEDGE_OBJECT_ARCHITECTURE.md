# ADR-004

Title

Knowledge Object Architecture

Status

Accepted

---

## Context

The Commerce Knowledge Platform began with
Canonical Terms as its primary semantic unit.

During CKP-001, the platform introduced:

Canonical Terms.

Semantic Relationships.

Normative Claims.

Business Rules.

Capabilities.

Policies.

Processes.

Events.

Metrics.

Decisions.

These elements require stable identity,
lifecycle, traceability, and semantic
relationships.

Treating only Terms as first-class registered
objects would create incompatible registries
and identifier models as the platform grows.

---

## Decision

The fundamental registered unit of the
Commerce Knowledge Platform shall be the
Knowledge Object.

Every canonical semantic asset shall be
represented as one typed Knowledge Object.

---

## Knowledge Object Types

TERM

RELATIONSHIP

CLAIM

RULE

CAPABILITY

POLICY

ROLE

PROCESS

EVENT

METRIC

DOCUMENT

DECISION

CONSTRAINT

---

## Knowledge Object Properties

Canonical Identifier.

Object Type.

Preferred Name.

Canonical Definition.

Lifecycle Status.

Version.

Relationships.

Traceability References.

---

## Identifier Model

Every Knowledge Object shall possess one
immutable Canonical Identifier.

Identifiers shall use a canonical object-type
prefix.

Examples

CKP-TERM-000001

CKP-REL-000001

CKP-CLAIM-000001

CKP-RULE-000001

CKP-CAP-000001

CKP-POLICY-000001

CKP-ROLE-000001

CKP-PROCESS-000001

CKP-EVENT-000001

CKP-METRIC-000001

CKP-DOC-000001

CKP-DECISION-000001

CKP-CONSTRAINT-000001

Identifiers shall remain permanent even when
names, definitions, versions, or lifecycle
status change.

---

## Registry Architecture

The Knowledge Registry shall manage all
Knowledge Objects.

No canonical Knowledge Object may exist
outside the Registry.

The Registry shall preserve:

Identity.

Type.

Definition.

Lifecycle.

Version.

Relationships.

Traceability.

---

## Relationship Architecture

Semantic Relationships are Knowledge Objects.

Every Relationship shall possess:

Canonical Identifier.

Source Knowledge Object.

Canonical Relationship Type.

Target Knowledge Object.

Directionality.

Inverse Relationship Reference.

Lifecycle Status.

Relationships shall connect registered
Knowledge Objects only.

---

## Knowledge Graph

The Commerce Knowledge Graph consists of:

Knowledge Objects as Nodes.

Semantic Relationships as Edges.

The graph shall remain:

Canonical.

Directed.

Traceable.

Auditable.

Versioned.

Semantically closed.

---

## Traceability

The architecture shall support the chain:

Knowledge Object

↓

Normative Claim

↓

Specification

↓

Implementation

↓

Decision

↓

Evidence

---

## Domain Separation

Commerce shall remain the root business
domain.

Retail, Wholesale, Ecommerce, Marketplace,
Omnichannel, Distribution, Social Commerce,
and Informal Commerce shall specialize or
consume Commerce Knowledge Objects.

Domain-specific knowledge shall not redefine
canonical Commerce semantics.

---

## Consequences

The Registry becomes a registry of typed
Knowledge Objects rather than a registry of
Terms only.

Canonical Terms remain one Knowledge Object
type.

Semantic Relationships receive independent
identity and lifecycle.

Claims, Rules, Capabilities, Policies, Roles,
Processes, Events, Metrics, Documents,
Decisions, and Constraints may be introduced
without redesigning the Registry.

Future ontology and Knowledge Graph work
shall use this architecture.

---

## Constraints

Every canonical semantic asset shall be a
registered Knowledge Object.

Every Knowledge Object shall declare one
canonical type.

Every Knowledge Object shall have one
immutable identifier.

No object-type namespace shall reuse an
identifier.

No domain shall redefine an existing
canonical Knowledge Object privately.

---

## Alternatives Rejected

Term-only Registry.

Rejected because it cannot represent Claims,
Rules, Policies, Events, Metrics, Decisions,
and Relationships without incompatible
special cases.

Document-only Architecture.

Rejected because documents organize
knowledge but are not the fundamental unit of
semantic identity.

Relationship-without-Identity Model.

Rejected because relationships require
lifecycle, traceability, versioning, and
auditability.

---

## Resulting Architecture

Knowledge Objects

↓

Knowledge Registry

↓

Knowledge Graph

↓

Commerce Ontology

↓

Executable Specifications

↓

Specification Runtime

↓

Decision Services

↓

Commerce Applications
