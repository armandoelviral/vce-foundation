# Platform Services

Version: 1.0

Status: Draft

Classification: Platform Architecture

---

# Purpose

Define the canonical services composing the Institutional Capability Platform.

Each service owns one business capability.

Services collaborate through immutable domain events.

Services never own overlapping responsibilities.

---

# Service 1

## Recommendation Service

Purpose

Produce explainable recommendations.

Responsibilities

- Recommendation generation
- Recommendation scoring
- Confidence estimation
- Recommendation explanation
- Recommendation versioning

Consumes

- ContextUpdated
- EvidenceRecorded
- CapabilityInstitutionalized

Publishes

- RecommendationGenerated
- RecommendationUpdated

API

POST /recommendations

GET /recommendations/{id}

---

# Service 2

## Simulation Service

Purpose

Evaluate hypothetical operational scenarios.

Responsibilities

- What-if analysis
- Forecast simulation
- Policy comparison
- Constraint validation

Consumes

RecommendationGenerated

Publishes

SimulationCompleted

API

POST /simulations

---

# Service 3

## Human Expertise Service

Purpose

Capture expert judgment.

Responsibilities

- Decision recording
- Rationale capture
- Exception management
- Expert attribution

Consumes

RecommendationGenerated

Publishes

ExpertDecisionRecorded

ExpertReasonCaptured

API

POST /expert-decisions

POST /expert-rationale

---

# Service 4

## Operational Evidence Service

Purpose

Capture real operational outcomes.

Responsibilities

- KPI collection
- Execution recording
- Compliance measurement
- Outcome comparison

Consumes

ExecutionCompleted

Publishes

EvidenceRecorded

OutcomeMeasured

ComplianceVerified

API

POST /evidence

POST /kpis

---

# Service 5

## Institutional Memory Service

Purpose

Persist organizational knowledge.

Responsibilities

- Decision history
- Rationale history
- Policy history
- Evidence history
- Longitudinal records

Consumes

EvidenceRecorded

ExpertReasonCaptured

Publishes

KnowledgeStored

KnowledgeLinked

API

GET /knowledge

GET /history

---

# Service 6

## Governance Service

Purpose

Evaluate candidate knowledge.

Responsibilities

- Reviews
- Approvals
- Rejections
- Policy promotion

Consumes

KnowledgeCandidateCreated

CapabilityCandidateCreated

Publishes

PolicyApproved

PolicyRejected

CapabilityInstitutionalized

API

POST /governance/review

POST /governance/approve

---

# Service 7

## Capability Service

Purpose

Manage Institutional Capabilities.

Responsibilities

- Capability lifecycle
- Registry
- Versioning
- Metrics
- Monitoring

Consumes

PolicyApproved

Publishes

CapabilityCreated

CapabilityUpdated

CapabilityDeprecated

API

GET /capabilities

POST /capabilities

---

# Service 8

## Knowledge Graph Service

Purpose

Maintain semantic organizational relationships.

Responsibilities

- Entity management
- Relationship management
- Provenance
- Temporal graph

Consumes

KnowledgeStored

Publishes

KnowledgeLinked

API

GET /graph

POST /graph

---

# Service 9

## Asset Service

Purpose

Manage reusable organizational assets.

Responsibilities

- Asset storage
- Versioning
- Templates
- Integrity
- Metadata

Consumes

AssetCreated

Publishes

AssetVersionReleased

API

POST /assets

GET /assets

---

# Service 10

## Workflow Service

Purpose

Coordinate platform workflows.

Responsibilities

- State transitions
- Event routing
- Process orchestration

Consumes

Platform Events

Publishes

WorkflowStarted

WorkflowCompleted

WorkflowFailed

API

POST /workflows

---

# Service 11

## Context Service

Purpose

Provide contextual intelligence.

Responsibilities

- Context aggregation
- Environmental signals
- Context scoring

Publishes

ContextUpdated

API

GET /context

---

# Service 12

## Identity Service

Purpose

Protect organizational integrity.

Responsibilities

- Authentication
- Authorization
- Audit
- Tenancy

Publishes

IdentityVerified

PermissionGranted

API

POST /login

POST /authorize

---

# Service Principles

Each service owns one business capability.

Services communicate exclusively through events.

Business policies remain outside service implementation.

Services are independently deployable.

Services are independently testable.

Services are independently evolvable.
