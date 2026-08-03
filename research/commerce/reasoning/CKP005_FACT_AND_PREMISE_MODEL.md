# CKP-005

Title

Commerce Fact and Premise Model

Abbreviation

CFPM

Version

1.0

Status

Draft

---

## Purpose

Define the canonical, deterministic,
immutable, evidence-producing, integrity-
preserving, and auditable Fact and Premise
Model for the Commerce Knowledge Platform.

The Fact and Premise Model defines the
normative representation of observable Facts
and Reasoning Premises consumed during
Reasoning evaluation.

The model establishes deterministic identity,
validation, provenance, integrity, evidence,
and traceability.

This specification defines structure only.

It does not implement storage.

It does not implement inference.

It does not implement graph mutation.

It does not implement reasoning execution.

---

## Normative Dependencies

The Commerce Fact and Premise Model consumes:

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

Every dependency shall remain immutable.

No dependency shall be modified by this
specification.

---

## Fact Identity

Every Fact shall possess exactly one immutable
Fact Identifier.

Example

CKP-FACT-000001

Fact Identifiers shall be globally unique.

Fact Identity shall remain stable throughout
its lifecycle.

Fact Identity shall never be reused.

Missing, duplicated, malformed, or reused
Fact Identifiers shall invalidate the Fact.

---

## Fact Version

Every Fact shall declare one Fact Version.

The initial supported version is:

1.0.

Fact Version identifies the normative Fact
schema.

Unsupported versions shall fail validation.

---

## Fact Lifecycle

Every Fact shall declare one Lifecycle Status.

Permitted values are:

Draft.

Approved.

Deprecated.

Retired.

Only Approved Facts may participate in
Reasoning.

Lifecycle Status shall remain immutable during
Reasoning execution.

---

## Fact Type

Every Fact shall declare exactly one Fact
Type.

Permitted initial Fact Types are:

OBSERVED.

DERIVED.

ASSERTED.

IMPORTED.

Unknown Fact Types shall be invalid.

---

## Fact Properties

Every Fact shall declare:

Fact Identifier.

Fact Version.

Fact Type.

Lifecycle Status.

Subject.

Predicate.

Object or Literal Value.

Assertion Type.

Assertion Polarity.

Graph Scope.

Evidence Reference.

Integrity Reference.

Source Reference.

Timestamp.

Every mandatory property shall be explicit.

No mandatory property shall be inferred.

---

## Fact Source

Every Fact shall reference exactly one Fact
Source.

A Fact Source shall declare:

Source Identifier.

Source Type.

Source Version.

Source Integrity Reference.

Unknown Fact Sources shall invalidate the
Fact.

---

## Fact Provenance

Every Fact shall preserve complete
provenance.

Fact Provenance shall include:

Origin.

Collection Method.

Observation Timestamp.

Responsible System.

Evidence Chain.

Fact Provenance shall remain immutable.

---

## Fact Confidence

Every Fact shall declare one Confidence
Level.

Confidence shall be explicitly declared.

Confidence shall not modify Fact semantics.

Confidence shall not influence deterministic
Reasoning.

---

## Fact Integrity

Every Fact shall possess one deterministic
Integrity Reference.

Integrity shall bind every normative Fact
property.

Any normative mutation shall invalidate Fact
Integrity.

---

## Fact Evidence

Every Fact shall possess one Evidence
Reference.

Evidence shall be deterministic.

Evidence shall be complete.

Evidence shall remain immutable.

---

## Premise Identity

Every Premise shall possess exactly one
immutable Premise Identifier.

Example

CKP-PREMISE-000001

Premise Identifiers shall be globally unique.

Premise Identity shall never be reused.

---

## Premise Version

Every Premise shall declare one Premise
Version.

The initial supported version is:

1.0.

Unsupported versions shall invalidate the
Premise.

---

## Premise Type

Every Premise shall declare exactly one
Premise Type.

Permitted initial Premise Types are:

MANDATORY.

OPTIONAL.

NEGATIVE.

DERIVED.

Unknown Premise Types shall be invalid.

---

## Premise Properties

Every Premise shall declare:

Premise Identifier.

Premise Version.

Premise Type.

Lifecycle Status.

Referenced Fact.

Validation Reference.

Evidence Reference.

Integrity Reference.

Priority.

Optionality.

Every mandatory property shall be explicit.

---

## Premise Source Reference

Every Premise shall reference exactly one
Fact Source.

Premises shall not invent Facts.

Premises shall reference only validated
Facts.

---

## Premise Validation

Premise Validation shall verify:

Premise Identity.

Referenced Fact.

Fact Integrity.

Fact Evidence.

Fact Lifecycle.

Fact Version.

Premise Version.

Premise Type.

Validation shall fail closed.

---

## Premise Satisfaction

A Premise is satisfied only when:

Referenced Fact exists.

Referenced Fact is Approved.

Referenced Fact Integrity is valid.

Referenced Fact Evidence is complete.

Referenced Fact satisfies every Rule
requirement.

Otherwise the Premise shall be considered
unsatisfied.

---

## Premise Evidence

Every Premise shall preserve deterministic
Evidence.

Premise Evidence shall reference the
underlying Fact Evidence.

Premise Evidence shall remain immutable.

---

## Premise Integrity

Every Premise shall possess one deterministic
Integrity Reference.

Integrity shall bind every normative Premise
property.

Any mutation shall invalidate Premise
Integrity.

---

## Fact–Premise Relationships

Every Premise shall reference one or more
Facts.

Every Fact may participate in zero or more
Premises.

A Premise shall never create a Fact.

A Fact shall never be rewritten by a
Premise.

Relationships shall be deterministic.

Relationships shall be traceable.

---

## Canonical Serialization

Facts and Premises shall possess canonical
serialization.

Serialization shall:

Preserve every normative property.

Use deterministic ordering.

Exclude presentation metadata.

Produce identical output for equivalent
structures.

Canonical serialization shall support
integrity calculation.

---

## Deterministic Ordering

Facts shall be ordered by:

Fact Identifier.

Premises shall be ordered by:

Priority.

Then Premise Identifier.

Runtime ordering shall not affect normative
ordering.

Implementation-defined ordering is prohibited.

---

## Validation Result

Every validation shall produce exactly one
Validation Result.

Permitted values are:

PASS.

FAIL.

Validation Results shall remain immutable.

---

## Failure Classifications

Initial classifications are:

FACT_IDENTITY_VIOLATION.

FACT_VERSION_VIOLATION.

FACT_TYPE_VIOLATION.

FACT_SOURCE_VIOLATION.

FACT_PROVENANCE_VIOLATION.

FACT_CONFIDENCE_VIOLATION.

FACT_INTEGRITY_VIOLATION.

FACT_EVIDENCE_VIOLATION.

PREMISE_IDENTITY_VIOLATION.

PREMISE_VERSION_VIOLATION.

PREMISE_TYPE_VIOLATION.

PREMISE_REFERENCE_VIOLATION.

PREMISE_VALIDATION_VIOLATION.

PREMISE_SATISFACTION_VIOLATION.

SERIALIZATION_VIOLATION.

READ_ONLY_VIOLATION.

---

## Failure Conditions

Validation shall fail when:

Fact Identity is invalid.

Fact Version is unsupported.

Fact Source cannot be resolved.

Fact Integrity is invalid.

Fact Evidence is incomplete.

Premise Identity is invalid.

Referenced Fact cannot be resolved.

Premise Validation fails.

Premise Satisfaction fails.

Canonical Serialization cannot be produced.

A frozen baseline is modified.

---

## Read-Only Boundary

This specification shall not:

Create a Canonical Commerce Term.

Modify CKP-001.

Modify CKP-002.

Modify CKP-003.

Modify CKP-004.

Modify CKP-005.1.

Modify CKP-005.2.

Modify CKP-005.3.

Modify CKP-005.4.

Modify a registered Fact.

Modify a registered Premise.

Modify a registered Rule.

Modify a registered Constraint.

Modify an Execution Context.

Rewrite Graph Knowledge.

Repair missing Facts.

Repair Premises.

Create undocumented semantic meaning.

---

## Fact and Premise Invariants

Read-Only Preservation.

Canonical Fact Identity.

Canonical Premise Identity.

Fact Integrity.

Premise Integrity.

Evidence Completeness.

Source Traceability.

Deterministic Ordering.

Canonical Serialization.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Success Criteria

The Fact and Premise Model is valid only when:

Every Fact possesses unique identity.

Every Premise possesses unique identity.

Every referenced Fact is valid.

Evidence is complete.

Integrity is valid.

Canonical Serialization succeeds.

Deterministic Ordering succeeds.

No Failure Condition remains open.

No frozen baseline is modified.

---

## Release Boundary

Version 1.0 defines the canonical Commerce
Fact and Premise Model.

Future implementations shall preserve this
normative contract.

Version 1.0 does not define:

Reasoning Engine.

Inference Execution.

Rule Scheduling.

Persistence.

Distributed Execution.

Machine Learning.

Probabilistic Reasoning.

---

## Next Deliverable

CKP-005.6

Proof Model.

---

# End of Specification
