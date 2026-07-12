# Architecture Review Checkpoint 0.1

Artifact ID: SP001-AR-0.1

Version: 0.1

Status: Completed

Classification: Architecture Review

Owner: SP001 Retail Reference Implementation

---

# Purpose

Evaluate the internal consistency of the Scientific Product reference architecture before implementation begins.

This review determines whether the current architecture is sufficiently coherent to support an executable SP001 skeleton.

---

# Review Question 001

## Does responsibility duplication exist between layers or services?

### Finding

Partial duplication exists between:

- Institutional Memory Service
- Knowledge Graph Service

Institutional Memory currently preserves:

- decisions;
- rationale;
- evidence;
- policies;
- longitudinal history.

Knowledge Graph currently maintains:

- entities;
- relationships;
- provenance;
- temporal links;
- evidence links.

### Decision

The responsibilities shall be separated as follows.

Institutional Memory owns durable records and historical truth.

Knowledge Graph owns semantic projection and relationship traversal.

The Knowledge Graph shall reference Institutional Memory records.

It shall not become the authoritative source of historical evidence.

### Status

Resolved by boundary clarification.

---

# Review Question 002

## Can any service be eliminated because another service already covers its responsibility?

### Finding A

The candidate Capability Operating System overlaps with:

- Workflow Service;
- Governance Service;
- Capability Service;
- monitoring responsibilities.

### Decision

Capability Operating System shall not be introduced in SP001-0.1.

Its proposed behavior shall first be implemented through coordinated responsibilities of:

- Workflow Service;
- Governance Service;
- Capability Service.

A separate Capability Operating System may be reconsidered only if implementation evidence demonstrates irreducible orchestration behavior.

### Status

Candidate deferred.

---

### Finding B

Context Service and Recommendation Service are distinct.

Context Service produces governed contextual information.

Recommendation Service consumes context and generates recommendations.

### Decision

Preserve both services.

### Status

No reduction required.

---

### Finding C

Simulation Service is separable from Recommendation Service because simulation evaluates counterfactual scenarios rather than producing the primary recommendation.

### Decision

Preserve Simulation Service, but do not include it in the first executable workflow.

### Status

Deferred from Minimum Executable Slice.

---

# Review Question 003

## Does every aggregate possess a clear lifecycle?

### Finding

The following aggregates currently possess sufficient candidate lifecycles:

- Objective
- Case
- Recommendation
- Expert Decision
- Evidence
- Capability
- Policy
- Workflow
- Asset

The following remain insufficiently defined:

- Context
- Knowledge
- Project

### Decision

Context shall be treated initially as a versioned immutable snapshot rather than a long-lived aggregate.

Knowledge shall not be implemented as one universal aggregate.

Knowledge records shall be represented by typed records within Institutional Memory.

Project shall not be introduced until evidence demonstrates behavior not already represented by Objective and Case.

### Status

Conditional approval.

---

# Review Question 004

## Does any Core contract depend accidentally upon Retail?

### Finding

The canonical Scientific Product Domain Model remains independent from Retail.

However, implementation risk exists in:

- metric names;
- asset metadata;
- recommendation payloads;
- context schemas;
- compliance evidence.

### Decision

Core contracts shall use generic structures.

Examples:

- Metric rather than GMROI
- Domain Asset rather than Garment Asset
- Recommendation Action rather than Planogram Action
- Evidence Observation rather than Store Compliance
- Context Signal rather than Retail Climate Context

Retail-specific fields shall remain inside the Retail Vertical Pack.

### Status

Boundary preserved with implementation constraint.

---

# Review Question 005

## Can a second vertical be implemented without modifying the Core?

### Evaluation Domain

Healthcare was used as an adversarial mapping test.

### Mapping

Objective

Retail:
Increase sell-through.

Healthcare:
Reduce patient appointment no-shows.

---

Case

Retail:
Back-to-School campaign in Store A.

Healthcare:
Appointment adherence intervention in Clinic B.

---

Recommendation

Retail:
Increase product facing.

Healthcare:
Send targeted reminder and schedule intervention.

---

Expert Decision

Retail:
VM Senior modifies recommendation.

Healthcare:
Clinical operations specialist modifies recommendation.

---

Operational Evidence

Retail:
Sales, compliance and inventory movement.

Healthcare:
Attendance, intervention response and operational impact.

---

Candidate Capability

Retail:
Seasonal transition capability.

Healthcare:
Appointment adherence capability.

### Finding

The domain model supports both mappings without changing:

- Objective;
- Case;
- Recommendation;
- Expert Decision;
- Evidence;
- Governance;
- Capability.

### Decision

The three-layer separation remains viable:

1. Scientific Product Domain
2. Institutional Capability Platform
3. Vertical Pack

### Status

Provisionally validated conceptually.

Operational validation remains pending.

---

# Service Boundary Decisions

## Institutional Memory Service

Owns:

- immutable knowledge records;
- decision history;
- rationale history;
- evidence references;
- policy history;
- version history;
- longitudinal records.

Does not own:

- semantic traversal;
- graph-specific query optimization;
- capability lifecycle decisions.

---

## Knowledge Graph Service

Owns:

- semantic relationships;
- ontology projection;
- provenance links;
- temporal relationships;
- graph queries.

Does not own:

- authoritative evidence records;
- policy approval;
- capability lifecycle.

---

## Governance Service

Owns:

- review processes;
- admission decisions;
- approval;
- rejection;
- deferral;
- scope restriction;
- promotion authorization.

Does not own:

- capability state persistence;
- capability metrics;
- capability monitoring.

---

## Capability Service

Owns:

- capability identity;
- lifecycle state;
- versioning;
- dependencies;
- adoption state;
- monitoring;
- deprecation;
- retirement.

Does not approve its own promotion.

Promotion authority belongs to Governance.

---

## Workflow Service

Owns:

- process coordination;
- workflow state;
- retries;
- timeouts;
- event-driven progression.

Does not own domain decisions.

---

# Minimum Executable Slice

The first executable slice shall contain only:

- Recommendation Service;
- Human Expertise Service;
- Operational Evidence Service;
- Governance Service;
- Capability Service;
- Workflow Service;
- canonical event contracts;
- in-memory persistence.

The following remain outside the first slice:

- Simulation Service;
- Knowledge Graph Service;
- Asset Service;
- Context aggregation;
- rendering;
- distributed event infrastructure;
- dedicated Capability Registry;
- Capability Operating System.

---

# Review Decision

Architecture 0.1 is approved for Minimum Executable Slice implementation with the boundary corrections documented above.

The architecture is not approved for distributed deployment.

The first implementation shall remain a modular monolith.

---

# Rationale

Current evidence supports logical service separation.

It does not yet justify physical microservice separation.

A modular monolith minimizes operational complexity while preserving bounded contexts and contracts.

---

# Next Action

Produce the Minimum Executable Slice specification and repository skeleton.
