# Minimum Executable Slice

Artifact ID: SP001-MES-001

Version: 0.1

Status: Active

Classification: Implementation Specification

---

# Purpose

Define the smallest executable implementation capable of exercising the central Scientific Product lifecycle.

The objective is architectural validation, not commercial completeness.

---

# Workflow

RecommendationGenerated

↓

ExpertDecisionRecorded

↓

ExpertReasonCaptured

↓

EvidenceRecorded

↓

CapabilityCandidateCreated

↓

GovernanceReviewRequested

↓

CapabilityApproved or CapabilityRejected

↓

CapabilityInstitutionalized when approved

---

# Included Modules

## Recommendation

Creates an immutable, explainable recommendation.

---

## Expertise

Records expert action and rationale.

---

## Evidence

Records observed operational outcomes.

---

## Capability

Creates and manages Candidate Capabilities.

---

## Governance

Approves, rejects or defers capability promotion.

---

## Workflow

Coordinates the end-to-end state transition.

---

## Contracts

Defines commands, events and identifiers shared across modules.

---

# Excluded Capabilities

- AI model integration
- Retail rendering
- simulation
- external event broker
- graph database
- object storage
- authentication provider
- distributed deployment
- marketplace
- billing
- cloud orchestration

---

# Persistence

Initial persistence shall be in-memory.

Persistence interfaces shall remain explicit.

---

# Deployment

Initial deployment shall be one Python process.

Logical boundaries shall be preserved as modules.

---

# Acceptance Scenario

Given an organizational objective and case,

when a recommendation is created,

and an expert modifies the recommendation with a rationale,

and operational evidence supports the modified decision,

and a capability candidate is created,

and governance approves the candidate,

then an Institutional Capability shall be created with:

- identity;
- version;
- provenance;
- evidence references;
- expert rationale reference;
- governance decision;
- active status.

---

# Architectural Evidence Produced

The slice shall reveal:

- whether service boundaries are coherent;
- whether canonical event contracts are sufficient;
- whether Objective and Case are necessary;
- whether Capability requires a dedicated registry;
- whether workflow coordination becomes overly complex;
- whether Governance and Capability remain properly separated.

---

# Exit Criteria

The slice is complete when:

- the complete workflow executes in memory;
- all domain events are recorded;
- the workflow is replayable;
- tests verify every transition;
- no Retail-specific field exists in Core modules;
- at least one Retail mapping exercises the workflow;
- architecture findings are recorded.
