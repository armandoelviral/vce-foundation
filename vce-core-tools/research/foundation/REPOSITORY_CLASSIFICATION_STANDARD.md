# Repository Classification Standard

# Repository Classification Standard

Version: 1.0

Status: Active

Classification: Foundation Standard

---

# Purpose

Establish a unified classification model for every permanent artifact within the VCE Research Program.

Every repository artifact shall expose sufficient metadata to support:

- governance;
- traceability;
- reproducibility;
- dependency analysis;
- historical reconstruction;
- lifecycle management.

Artifacts are considered first-class governed entities.

---

# Mandatory Metadata

Every permanent artifact shall declare the following fields.

---

## Artifact ID

Globally unique identifier.

Example

SPF-0003

RC2-061

PM-0001

ADR-022

P-001

H-003

---

## Title

Human-readable artifact title.

---

## Version

Current artifact version.

Example

1.0

1.1

2.0

---

## Status

Current lifecycle status.

Allowed values:

Draft

Candidate

Active

Deprecated

Archived

Superseded

Retired

---

## Classification

Primary repository classification.

Examples

Research Cycle

Scientific Object

Scientific Product

Program Milestone

Architecture Decision Record

Principle

Hypothesis

Capability

Governance

Foundation

Release

Standard

Policy

Manifesto

Specification

---

## Owner

Responsible entity.

Examples

Research Program

Scientific Product Factory

Architecture Board

Governance Board

---

## Purpose

Why the artifact exists.

---

## Scope

Which parts of the program are governed by this artifact.

---

## Dependencies

Explicit list of required artifacts.

Dependencies shall reference Artifact IDs.

---

## Related Artifacts

Optional relationships.

Examples

implements

extends

supersedes

references

validates

produces

consumes

---

## Promotion Status

Current maturity.

Possible values

Candidate

Validated

Permanent

Experimental

---

## Evidence Status

Current validation state.

Possible values

Conceptual

Experimental

Operational

Longitudinal

Externally Validated

---

## Applicable Principles

List of governing principles.

Example

P-001

P-004

---

## Applicable Hypotheses

List of related hypotheses.

Example

H-002

H-006

---

## Applicable Program Milestones

Program Milestones related to this artifact.

Example

PM-0001

---

## Review Frequency

Recommended review interval.

Examples

Quarterly

Every Research Cycle

Annual

On Evidence Change

---

## Review Authority

Entity authorized to approve modifications.

Examples

Research Governance Board

Architecture Review Board

Scientific Product Board

---

# Artifact Lifecycle

Draft

↓

Candidate

↓

Validation

↓

Governance Review

↓

Active

↓

Revision

↓

Superseded

↓

Archived

Retired

---

# Classification Rules

Every artifact shall have exactly one primary classification.

Secondary relationships shall be expressed through explicit references rather than multiple classifications.

Classification determines governance.

Relationships determine architecture.

---

# Repository Consistency Rules

Artifacts shall never exist without metadata.

Dependencies shall always be explicit.

Promotion Status shall reflect available evidence.

Every permanent artifact shall be reconstructible.

Every revision shall preserve historical traceability.

---

# Governance Rule

Repository structure shall evolve through governed architectural decisions.

Folder organization shall never replace formal classification.

The repository is organized by governance first, storage second.

---

# Closing Statement

The repository is not a document archive.

It is the governed institutional memory of the VCE Research Program.

Classification exists to preserve identity, traceability, governance and long-term reconstructibility of every permanent artifact.
