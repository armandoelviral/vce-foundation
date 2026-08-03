# CKP-005

Title

Commerce Explanation Model

Abbreviation

CEM

Version

1.0

Status

Draft

---

## Purpose

Define the canonical, deterministic,
immutable, traceable, auditable,
human-consumable, machine-readable, and
normatively verifiable Explanation Model for
the Commerce Knowledge Platform.

The Explanation Model specializes the
Explanation Structure defined by the Commerce
Reasoning Structure Model.

An Explanation shall communicate how a
Reasoning Request produced one terminal
Reasoning Outcome without altering the
underlying reasoning process.

An Explanation shall derive exclusively from
validated normative artifacts.

An Explanation shall preserve semantic
equivalence with the underlying Reasoning
Evidence.

The Explanation Model defines explanation
identity, structure, traceability,
construction, validation, ordering,
determinism, integrity, and read-only
boundaries.

The Explanation Model does not execute
reasoning.

It does not infer additional conclusions.

It does not repair inconsistent evidence.

It does not modify ontology, graph, or proof
artifacts.

---

## Normative Dependencies

The Commerce Explanation Model consumes:

HAS Foundation 1.0 LTS.

Specification Runtime 1.0.

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

CKP-003 Commerce Knowledge Graph 1.0.

CKP-004 Commerce Query Language 1.0.

CKP-005.1 Commerce Reasoning Charter.

CKP-005.2 Commerce Reasoning Structure Model.

CKP-005.3 Commerce Reasoning Request Model.

CKP-005.4 Inference Rule Model.

CKP-005.5 Fact and Premise Model.

CKP-005.6 Proof Model.

CKP-005.7 Reasoning Evidence Model.

Every dependency shall remain immutable.

An Explanation shall never redefine or modify
any dependency.

---

## Explanation Identity

Every Explanation shall possess exactly one
immutable Explanation Identifier.

Example

CKP-EXPLANATION-000001

Every Explanation Identifier shall be unique
within one Reasoning Execution.

Explanation Identity shall remain distinct
from Explanation Version.

An Explanation Identifier shall never be
reused.

A missing, malformed, duplicated, or reused
Explanation Identifier shall cause validation
failure.

---

## Explanation Version

Every Explanation shall declare one
Explanation Version.

The initial supported Explanation Version is:

1.0.

Explanation Version identifies the normative
Explanation schema.

Explanation Version shall not replace
Explanation Identity.

Unsupported Explanation Versions shall cause
validation failure.

---

## Explanation Lifecycle

Every Explanation shall declare one Lifecycle
Status.

Permitted values are:

Draft.

Constructed.

Validated.

Invalid.

Superseded.

Archived.

Only a Validated Explanation may accompany a
terminal Reasoning Result.

Lifecycle Status shall not regress.

---

## Explanation Type

Every Explanation shall declare exactly one
canonical Explanation Type.

Initial supported types are:

SUMMARY.

DETAILED.

TRACE.

CONTRADICTION.

FAILURE.

TERMINAL.

Unknown Explanation Types shall be invalid.

---

## Explanation Properties

Every Explanation shall declare:

Explanation Identifier.

Explanation Version.

Explanation Type.

Lifecycle Status.

Reasoning Request Identifier.

Reasoning Outcome.

Reasoning Status.

Graph Identifier.

Graph Version.

Execution Context Reference.

Evidence References.

Proof References.

Explanation Integrity Reference.

---

## Explanation Scope

Every Explanation shall belong to exactly one
Reasoning Request.

An Explanation shall explain exactly one
terminal Reasoning Outcome.

An Explanation shall not merge independent
Reasoning Requests.

Scope shall remain immutable.

---

## Explanation Audience

The intended audience shall be explicit.

Supported audiences are:

Human.

Machine.

Hybrid.

Audience selection shall not modify semantic
meaning.

---

## Explanation Granularity

Explanation Granularity shall be explicit.

Supported levels are:

Summary.

Standard.

Detailed.

Trace.

Granularity shall affect presentation only.

Granularity shall not alter semantic content.

---

## Explanation Source References

Every Explanation shall reference only
validated normative artifacts.

Referenced artifacts may include:

Facts.

Premises.

Rules.

Rule Applications.

Proofs.

Proof Steps.

Reasoning Evidence.

Contradiction Evidence.

Failure Evidence.

Terminal Evidence.

No undocumented source shall be introduced.

---

## Explanation Narrative

Every Explanation shall provide one coherent
narrative.

The narrative shall preserve semantic
equivalence with the underlying reasoning.

The narrative shall not introduce new facts,
premises, rules, or conclusions.

---

## Explanation Structure

Every Explanation shall contain:

Introduction.

Reasoning Context.

Evidence Summary.

Inference Summary.

Proof Summary.

Outcome Summary.

References.

---

## Explanation Sections

Each structural section shall appear exactly
once.

Sections shall not overlap semantically.

Sections shall preserve deterministic order.

---

## Explanation Ordering

Explanation Sections shall appear in this
order:

Introduction.

Reasoning Context.

Evidence Summary.

Inference Summary.

Proof Summary.

Outcome Summary.

References.

Implementation-defined ordering is
prohibited.

---

## Explanation Traceability

Every statement contained within an
Explanation shall be traceable to one or more
validated normative artifacts.

No orphan explanation statement shall exist.

Every referenced artifact shall resolve.

---

## Explanation Completeness

An Explanation is complete only when:

Every referenced artifact resolves.

Every normative statement is traceable.

Reasoning Outcome is represented.

Supporting Proof is represented when
applicable.

Supporting Evidence is represented.

Failure Evidence is represented when
applicable.

Terminal Evidence is represented.

---

## Explanation Validation

Explanation Validation shall verify:

Identity.

Version.

Lifecycle.

Type.

Scope.

Audience.

Granularity.

Traceability.

Completeness.

Ordering.

Integrity.

Validation shall fail closed.

---

## Explanation Validation Result

Every Explanation Validation shall produce
exactly one deterministic Validation Result.

Permitted values are:

PASS.

FAIL.

Validation Results shall remain immutable.

---

## Explanation Integrity

Every Explanation shall possess exactly one
Explanation Integrity Reference.

Integrity shall bind:

Identity.

Version.

Type.

Lifecycle.

Reasoning Request.

Reasoning Outcome.

Evidence References.

Proof References.

Narrative Structure.

Any normative mutation shall invalidate
Explanation Integrity.

---

## Canonical Serialization

Every Explanation shall possess one
deterministic canonical serialization.

Canonical serialization shall preserve:

Identity.

Version.

Type.

Ordering.

Narrative Structure.

References.

Integrity.

Presentation metadata shall be excluded.

Canonical serialization shall be suitable for
integrity calculation.

---

## Determinism

Identical Reasoning Executions shall produce
normatively identical Explanations.

Presentation formatting shall not affect
Explanation equality.

---

## Failure Classifications

Initial Failure Classifications are:

EXPLANATION_IDENTITY_VIOLATION.

EXPLANATION_VERSION_VIOLATION.

EXPLANATION_LIFECYCLE_VIOLATION.

EXPLANATION_TYPE_VIOLATION.

TRACEABILITY_VIOLATION.

COMPLETENESS_VIOLATION.

ORDERING_VIOLATION.

SERIALIZATION_VIOLATION.

INTEGRITY_VIOLATION.

READ_ONLY_VIOLATION.

---

## Failure Conditions

Validation shall fail when:

Identity is invalid.

Version is unsupported.

Lifecycle is incompatible.

Type is invalid.

Traceability cannot be established.

Completeness cannot be established.

Ordering is non-deterministic.

Canonical serialization cannot be produced.

Integrity cannot be established.

The Explanation attempts to modify source
knowledge.

---

## Read-Only Boundary

An Explanation shall not:

Create ontology artifacts.

Create graph artifacts.

Create reasoning artifacts.

Create proofs.

Modify evidence.

Modify reasoning outcomes.

Modify ontology.

Modify graph.

Modify proof.

Modify reasoning evidence.

Modify immutable baselines.

Create undocumented semantic meaning.

---

## Explanation Invariants

Read-Only Preservation.

Canonical Explanation Identity.

Version Preservation.

Lifecycle Validity.

Canonical Explanation Type.

Exactly One Reasoning Scope.

Semantic Equivalence.

Complete Traceability.

Deterministic Ordering.

Canonical Serialization.

Integrity Preservation.

Fail-Closed Validation.

---

## Success Criteria

An Explanation is valid only when:

Identity is valid.

Version is supported.

Lifecycle permits validation.

Type is valid.

Traceability is complete.

Completeness is established.

Ordering is deterministic.

Canonical serialization succeeds.

Integrity is valid.

No Failure Condition remains open.

---

## Release Boundary

Version 1.0 defines the canonical Commerce
Explanation Model.

Version 1.0 excludes:

Natural language optimization.

Localization.

Summarization algorithms.

LLM integration.

Interactive explanations.

Visualization.

Machine learning.

Probabilistic explanations.

Future implementations shall preserve this
normative contract.

---

## Next Deliverable

CKP-005.9

Reasoning Validation Model.

---

# End of Specification
