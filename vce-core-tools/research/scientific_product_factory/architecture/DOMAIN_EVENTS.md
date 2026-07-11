# Domain Events

Version: 0.1

Status: Draft

Classification: Architecture

---

# Purpose

Define the canonical business events exchanged between Bounded Contexts.

Events represent facts.

Events are immutable.

Events describe what has happened.

Commands request work.

Policies decide what should happen.

---

# Human Expertise Events

## ExpertDecisionRecorded

A domain expert accepts, rejects or modifies a recommendation.

---

## ExpertReasonCaptured

The expert provides the reasoning behind a decision.

---

## ExpertKnowledgeValidated

Expert reasoning has been reviewed and accepted for institutional evaluation.

---

# Decision Intelligence Events

## RecommendationGenerated

The AI produces a recommendation.

---

## RecommendationSimulated

A simulation has been completed.

---

## RecommendationUpdated

A recommendation changes after new evidence.

---

# Operational Evidence Events

## ExecutionObserved

The recommendation has been implemented.

---

## KPICollected

Operational KPIs have been recorded.

---

## OutcomeMeasured

Business impact has been measured.

---

## ComplianceVerified

Execution has been compared against the intended plan.

---

# Institutional Memory Events

## DecisionArchived

A decision becomes part of institutional memory.

---

## KnowledgeLinked

New relationships are created in the Knowledge Graph.

---

## EvidenceRecorded

Operational evidence is permanently stored.

---

# Governance Events

## KnowledgeCandidateCreated

A candidate institutional rule is proposed.

---

## GovernanceReviewRequested

Candidate knowledge enters governance review.

---

## PolicyApproved

Governance approves institutional promotion.

---

## PolicyRejected

Governance rejects institutional promotion.

---

# Capability Events

## CapabilityCandidateCreated

Potential organizational capability detected.

---

## CapabilityValidated

Evidence supports promotion.

---

## CapabilityInstitutionalized

Capability becomes permanent.

---

## CapabilityDeprecated

Capability is retired.

---

# Platform Events

## WorkflowStarted

---

## WorkflowCompleted

---

## AuditTrailGenerated

---

## VersionReleased

---

# Event Principles

Events are immutable.

Events represent facts.

Events never contain business decisions.

Business policies consume events.

Capabilities emerge from governed event histories.

---

# Closing Statement

Scientific Products evolve through governed events.

Events preserve organizational memory while enabling independent evolution of every bounded context.
