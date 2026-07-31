# CKP-005

Title

Commerce Reasoning Request Model

Abbreviation

CRRM

Version

1.0

Status

Draft

---

## Purpose

Define the canonical, deterministic,
immutable, traceable, evidence-producing, and
auditable Reasoning Request model for the
Commerce Knowledge Platform.

The Reasoning Request Model specializes the
Reasoning Request Node defined by the Commerce
Reasoning Structure Model.

A Reasoning Request shall declare every
normative input required to evaluate one
explicit reasoning goal over immutable
Commerce Knowledge Platform baselines.

The Reasoning Request Model defines request
structure and validation only.

It does not implement a reasoning engine.

It does not implement rule execution.

It does not implement graph mutation.

It does not implement baseline admission.

---

## Normative Dependencies

The Commerce Reasoning Request Model consumes:

HAS Foundation 1.0 LTS.

Specification Runtime 1.0.

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

CKP-003 Commerce Knowledge Graph 1.0.

CKP-004 Commerce Query Language 1.0.

CKP-005.1 Commerce Reasoning Charter.

CKP-005.2 Commerce Reasoning Structure Model.

Every dependency shall remain immutable.

A Reasoning Request shall not redefine any
frozen baseline.

---

## Request Identity

Every Reasoning Request shall possess one
immutable Reasoning Request Identifier.

Example

CKP-REASONING-REQUEST-000001

Every Reasoning Request Identifier shall be
unique within one Reasoning Execution
Context.

Request identity shall remain distinct from
Request Version.

A Reasoning Request Identifier shall never be
reused for a different normative Reasoning
Request.

A Reasoning Request Identifier shall not
create canonical Commerce meaning.

A missing, duplicated, malformed, or reused
Reasoning Request Identifier shall cause
validation failure.

---

## Request Version

Every Reasoning Request shall declare one
Reasoning Request Version.

The initial supported Reasoning Request
Version is:

1.0.

Request Version shall identify the normative
request schema used for validation.

Request Version shall not replace Request
Identity.

An unsupported Request Version shall cause
validation failure.

Version compatibility shall be explicitly
verified before reasoning begins.

---

## Request Lifecycle

Every Reasoning Request shall declare one
Lifecycle Status.

Permitted initial Lifecycle Status values
are:

Draft.

Approved.

Deprecated.

Retired.

Only an Approved Reasoning Request may enter
reasoning evaluation.

A Deprecated Reasoning Request shall not
execute unless explicitly permitted by the
Reasoning Execution Context.

A Retired Reasoning Request shall not execute.

Lifecycle Status shall remain immutable after
reasoning evaluation begins.

---

## Reasoning Form

Every Reasoning Request shall declare exactly
one canonical Reasoning Form.

Permitted initial Reasoning Forms are:

DERIVE ASSERTION.

VALIDATE ASSERTION.

EXPLAIN ASSERTION.

PROVE ASSERTION.

DETECT CONTRADICTION.

Unknown or private Reasoning Forms shall be
invalid.

Reasoning Form shall remain compatible with
the Goal Assertion, expected outcome,
registered Rule Set, and Execution Context.

A Reasoning Form shall not be inferred from
presentation text.

---

## Request Properties

Every Reasoning Request shall declare:

Reasoning Request Identifier.

Reasoning Request Version.

Lifecycle Status.

Reasoning Form.

Goal Assertion Reference.

Graph Identifier.

Graph Version.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Query Language Baseline Reference.

Fact Source References.

Premise References.

Inference Rule References.

Constraint References.

Reasoning Execution Context Reference.

Maximum Reasoning Depth.

Maximum Rule Applications.

Maximum Derived Assertions.

Closed-World Policy.

Contradiction Policy.

Expected Reasoning Outcome.

Request Evidence Reference.

Request Integrity Reference.

Source Evidence Reference.

Every mandatory property shall be explicit.

No mandatory property shall be inferred from
runtime defaults.

---

## Goal Assertion Reference

Every Reasoning Request shall reference
exactly one Goal Assertion.

The Goal Assertion Reference shall resolve to
one valid Goal Assertion within the same
Reasoning Request scope.

The referenced Goal Assertion shall declare:

Goal Assertion Identifier.

Subject Identifier.

Predicate Identifier.

Object Identifier or Literal Value.

Assertion Polarity.

Assertion Type.

Graph Scope.

Expected Truth Value.

Goal Integrity Reference.

A Goal Assertion Reference shall not resolve
to multiple assertions.

The Goal Assertion shall remain immutable
throughout evaluation.

Goal substitution is prohibited.

Goal mutation is prohibited.

---

## Graph Target

Every Reasoning Request shall declare one
Graph Identifier and one Graph Version.

The Graph Identifier shall resolve to one
registered immutable Commerce Knowledge
Graph.

The Graph Version shall resolve to one
supported immutable Graph Version.

Every Fact, Premise, Rule, Constraint,
Conclusion, Proof, and Evidence artifact shall
remain compatible with the declared Graph
target.

A Reasoning Request shall not span multiple
Graph Versions unless a future normative
version explicitly defines cross-version
reasoning.

Graph substitution during evaluation is
prohibited.

---

## Baseline References

Every Reasoning Request shall declare:

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Query Language Baseline Reference.

Every baseline reference shall resolve to one
immutable supported baseline.

Baseline references shall be mutually
compatible.

A Reasoning Request shall fail when any
baseline reference is missing, unknown,
incompatible, mutable, or unverifiable.

Reasoning shall not continue after baseline
validation failure.

---

## Fact Source References

A Reasoning Request may declare zero or more
Fact Source References.

Permitted initial Fact Sources are:

Canonical Vocabulary.

Commerce Ontology.

Commerce Knowledge Graph.

Validated Commerce Query Result.

Registered Reasoning Evidence.

Every Fact Source Reference shall declare:

Fact Source Identifier.

Fact Source Type.

Source Baseline Reference.

Source Version.

Source Integrity Reference.

Source Validation Evidence Reference.

Every Fact Source shall be resolvable,
compatible, immutable, and integrity-valid.

A Fact Source Reference shall not create a
Fact.

A Fact Source Reference shall identify where
Facts may be resolved.

Undocumented Fact Sources shall be invalid.

---

## Premise References

A Reasoning Request may declare zero or more
Premise References.

Every Premise Reference shall identify one
Premise declared within the Request scope or
one registered Premise Set compatible with the
Request.

Every Premise Reference shall declare:

Premise Identifier.

Required Polarity.

Required Source Type.

Assertion Pattern Reference.

Variable Reference Set.

Premise Priority.

Premise Validation Reference.

Premise Integrity Reference.

Duplicate Premise References shall be
invalid.

An unresolved mandatory Premise shall cause
reasoning failure.

Premise ordering shall remain deterministic.

---

## Inference Rule References

A Reasoning Request may declare zero or more
Inference Rule References.

Every Inference Rule Reference shall identify
one registered Rule.

Every Rule Reference shall declare:

Rule Identifier.

Rule Version.

Rule Type.

Rule Registry Reference.

Rule Priority.

Rule Integrity Reference.

Rule Validation Evidence Reference.

Unknown, private, unregistered, incompatible,
or integrity-invalid Rules shall not
participate in reasoning.

Duplicate Rule References shall be invalid
within one Request scope.

Runtime-discovered private Rules shall not
enter the normative Rule Set.

---

## Constraint References

A Reasoning Request may declare zero or more
Constraint References.

Every Constraint Reference shall identify one
registered Reasoning Constraint.

Every Constraint Reference shall declare:

Constraint Identifier.

Constraint Version.

Constraint Type.

Constraint Registry Reference.

Constraint Priority.

Constraint Integrity Reference.

Constraint Validation Evidence Reference.

Every mandatory Constraint shall be evaluated.

A violated Constraint shall produce explicit
failure evidence.

Constraint evaluation shall not repair the
Request or its source knowledge.

---

## Reasoning Execution Context Reference

Every Reasoning Request shall reference
exactly one immutable Reasoning Execution
Context.

The Reasoning Execution Context shall declare:

Execution Identifier.

Graph Identifier.

Graph Version.

Vocabulary Baseline.

Ontology Baseline.

Graph Baseline.

Query Language Baseline.

Fact Registry Reference.

Rule Registry Reference.

Constraint Registry Reference.

Maximum Reasoning Depth.

Maximum Rule Applications.

Maximum Derived Assertions.

Closed-World Policy.

Contradiction Policy.

Execution Timestamp.

The Request and Execution Context shall be
mutually compatible.

Execution Context substitution during
evaluation is prohibited.

---

## Reasoning Limits

Every Reasoning Request shall declare:

Maximum Reasoning Depth.

Maximum Rule Applications.

Maximum Derived Assertions.

Every limit shall be a non-negative integer.

Request limits shall not exceed the
corresponding Execution Context limits.

Maximum Reasoning Depth limits normative Rule
Application depth.

Maximum Rule Applications limits the total
number of Rule Applications.

Maximum Derived Assertions limits the total
number of derived Assertions.

A zero limit shall prohibit the corresponding
operation.

A limit violation shall cause fail-closed
evaluation.

---

## Closed-World Policy

Every Reasoning Request shall declare one
Closed-World Policy.

Permitted initial Closed-World Policy values
are:

OPEN WORLD.

EXPLICIT CLOSED WORLD.

OPEN WORLD shall treat absence of evidence as
insufficient to establish negation.

EXPLICIT CLOSED WORLD may establish negative
conclusions only within an explicitly declared
closed domain and registered Rule boundary.

Closed-world behavior shall not be inferred
implicitly.

A Request Closed-World Policy shall not exceed
the permissions of its Execution Context.

---

## Contradiction Policy

Every Reasoning Request shall declare one
Contradiction Policy.

Permitted initial Contradiction Policy values
are:

REPORT.

FAIL.

REPORT shall preserve both incompatible
proofs and produce CONTRADICTED.

FAIL shall construct contradiction evidence
and produce ERROR.

Contradiction Policy shall not delete,
rewrite, suppress, or repair conflicting
assertions.

The Request Contradiction Policy shall remain
compatible with the Execution Context.

---

## Expected Reasoning Outcome

Every Reasoning Request shall declare one
Expected Reasoning Outcome.

Permitted initial Expected Reasoning Outcome
values are:

PROVEN.

DISPROVEN.

UNDETERMINED.

CONTRADICTED.

ERROR.

Expected Reasoning Outcome shall not influence
reasoning evaluation.

Actual Reasoning Outcome shall be calculated
independently.

A mismatch between expected and actual outcome
shall be reported without modifying the actual
outcome.

UNDETERMINED shall remain distinct from
DISPROVEN.

ERROR shall remain distinct from
UNDETERMINED.

---

## Request Evidence

Every Reasoning Request shall declare one
Request Evidence Reference.

Request Evidence shall preserve:

Reasoning Request Identifier.

Reasoning Request Version.

Lifecycle Status.

Reasoning Form.

Goal Assertion Reference.

Graph Identifier.

Graph Version.

Baseline References.

Fact Source References.

Premise References.

Inference Rule References.

Constraint References.

Execution Context Reference.

Reasoning Limits.

Closed-World Policy.

Contradiction Policy.

Expected Reasoning Outcome.

Request Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

No valid or invalid Reasoning Request shall
omit deterministic validation evidence.

---

## Request Integrity

Every Reasoning Request shall possess one
deterministic Request Integrity Reference.

Request Integrity shall bind:

Reasoning Request Identifier.

Reasoning Request Version.

Lifecycle Status.

Reasoning Form.

Goal Assertion Reference.

Graph Identifier.

Graph Version.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Query Language Baseline Reference.

Fact Source References.

Premise References.

Inference Rule References.

Constraint References.

Execution Context Reference.

Maximum Reasoning Depth.

Maximum Rule Applications.

Maximum Derived Assertions.

Closed-World Policy.

Contradiction Policy.

Expected Reasoning Outcome.

Request Evidence Reference.

Source Evidence Reference.

Any normative Request mutation shall invalidate
the Request Integrity Reference.

---

## Canonical Serialization

Every Reasoning Request shall possess one
deterministic canonical serialization.

Canonical serialization shall:

Preserve every normative Request property.

Use deterministic property ordering.

Use deterministic reference ordering.

Preserve Goal Assertion identity.

Preserve Fact Source ordering.

Preserve Premise ordering.

Preserve Rule ordering.

Preserve Constraint ordering.

Preserve Reasoning Limits.

Preserve Closed-World Policy.

Preserve Contradiction Policy.

Preserve Expected Reasoning Outcome.

Preserve canonical identifiers.

Exclude non-normative presentation metadata.

Produce identical output for normatively
equal Requests.

Canonical serialization shall be suitable for
integrity calculation.

---

## Deterministic Ordering

Every Request collection shall possess one
deterministic ordering.

Fact Source References shall be ordered by:

Fact Source Type.

Then Fact Source Identifier.

Premise References shall be ordered by:

Premise Priority.

Then Premise Identifier.

Inference Rule References shall be ordered by:

Rule Priority.

Then Rule Identifier.

Constraint References shall be ordered by:

Constraint Priority.

Then Constraint Identifier.

Identical Requests shall produce identical
reference ordering.

Runtime discovery order shall not affect
normative Request ordering.

Implementation-defined ordering is
prohibited.

---

## Request Validation

Request Validation shall verify:

Reasoning Request Identifier validity.

Reasoning Request Version support.

Lifecycle Status validity.

Reasoning Form validity.

Goal Assertion resolution.

Goal Assertion integrity.

Graph Identifier resolution.

Graph Version compatibility.

Vocabulary Baseline compatibility.

Ontology Baseline compatibility.

Graph Baseline compatibility.

Query Language Baseline compatibility.

Fact Source resolution.

Premise Reference closure.

Inference Rule registration.

Constraint registration.

Execution Context resolution.

Execution Context compatibility.

Maximum Reasoning Depth validity.

Maximum Rule Applications validity.

Maximum Derived Assertions validity.

Closed-World Policy validity.

Contradiction Policy validity.

Expected Reasoning Outcome validity.

Canonical serialization.

Request Evidence completeness.

Request Integrity.

Validation shall fail closed.

An invalid Reasoning Request shall not enter
reasoning evaluation.

---

## Validation Result

Every Request Validation shall produce one
deterministic Validation Result.

Permitted Validation Result values are:

PASS.

FAIL.

PASS means every mandatory Request rule is
satisfied.

FAIL means one or more mandatory Request rules
are violated.

The Validation Result shall declare:

Validation Identifier.

Reasoning Request Identifier.

Validated Request Version.

Validation Outcome.

Detected Violations.

Failure Classifications.

Failure Reasons.

Validation Evidence Reference.

Validation Integrity Reference.

Validation results shall remain immutable and
auditable.

---

## Failure Classifications

Initial Reasoning Request Failure
Classifications are:

REQUEST_IDENTITY_VIOLATION.

REQUEST_VERSION_VIOLATION.

REQUEST_LIFECYCLE_VIOLATION.

REASONING_FORM_VIOLATION.

GOAL_REFERENCE_VIOLATION.

GOAL_INTEGRITY_VIOLATION.

GRAPH_TARGET_VIOLATION.

VOCABULARY_BASELINE_VIOLATION.

ONTOLOGY_BASELINE_VIOLATION.

GRAPH_BASELINE_VIOLATION.

QUERY_LANGUAGE_BASELINE_VIOLATION.

FACT_SOURCE_VIOLATION.

PREMISE_REFERENCE_VIOLATION.

RULE_REFERENCE_VIOLATION.

CONSTRAINT_REFERENCE_VIOLATION.

EXECUTION_CONTEXT_VIOLATION.

REASONING_DEPTH_LIMIT_VIOLATION.

RULE_APPLICATION_LIMIT_VIOLATION.

DERIVED_ASSERTION_LIMIT_VIOLATION.

CLOSED_WORLD_POLICY_VIOLATION.

CONTRADICTION_POLICY_VIOLATION.

EXPECTED_OUTCOME_VIOLATION.

SERIALIZATION_VIOLATION.

EVIDENCE_VIOLATION.

INTEGRITY_VIOLATION.

READ_ONLY_VIOLATION.

---

## Failure Conditions

A Reasoning Request shall fail validation
when:

The Reasoning Request Identifier is missing,
invalid, duplicated, or improperly reused.

The Reasoning Request Version is missing or
unsupported.

Lifecycle Status is missing, unknown, or
incompatible with execution.

Reasoning Form is missing, unknown, private,
or incompatible.

The Goal Assertion Reference is missing,
duplicated, unresolved, or integrity-invalid.

The Graph Identifier cannot be resolved.

The Graph Version is incompatible.

A baseline reference is missing, unknown,
mutable, incompatible, or unverifiable.

A Fact Source is undocumented, unresolved, or
integrity-invalid.

A mandatory Premise Reference cannot be
resolved.

A Rule Reference is private, unregistered,
unsupported, or integrity-invalid.

A Constraint Reference is unregistered or
integrity-invalid.

The Execution Context cannot be resolved.

The Execution Context is incompatible with
the Request.

A Request limit is negative.

A Request limit exceeds its Execution Context
boundary.

Closed-World Policy is missing, unknown, or
incompatible.

Contradiction Policy is missing, unknown, or
incompatible.

Expected Reasoning Outcome is missing or
unknown.

Deterministic reference ordering cannot be
established.

Canonical serialization cannot be produced.

Request Evidence cannot be produced.

Request Integrity cannot be established.

The Request attempts to mutate a frozen
baseline.

---

## Read-Only Boundary

A Reasoning Request shall not:

Create a Canonical Commerce Term.

Create an Ontology Assertion.

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Create a registered Graph Fact.

Delete a Canonical Commerce Term.

Delete an Ontology Assertion.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Component.

Modify a Query Result.

Modify a registered Fact.

Modify a registered Inference Rule.

Modify a registered Constraint.

Modify an Execution Context.

Repair an unresolved Premise.

Repair an invalid Rule Reference.

Repair a violated Constraint.

Modify HAS Foundation 1.0 LTS.

Modify Specification Runtime 1.0.

Modify CKP-001.

Modify CKP-002.

Modify CKP-003.

Modify CKP-004.

Create undocumented semantic meaning.

---

## Request Invariants

Read-Only Preservation.

Canonical Request Identity.

Request Version Preservation.

Lifecycle Validity.

Canonical Reasoning Form.

Exactly One Goal Assertion.

Immutable Goal Assertion.

Immutable Graph Target.

Vocabulary Baseline Compatibility.

Ontology Baseline Compatibility.

Graph Baseline Compatibility.

Query Language Baseline Compatibility.

Fact Source Closure.

Premise Reference Closure.

Rule Registration Closure.

Constraint Registration Closure.

Execution Context Closure.

Reasoning Depth Boundary.

Rule Application Boundary.

Derived Assertion Boundary.

Explicit Closed-World Policy.

Explicit Contradiction Policy.

Expected Outcome Independence.

Deterministic Fact Source Ordering.

Deterministic Premise Ordering.

Deterministic Rule Ordering.

Deterministic Constraint Ordering.

Canonical Serialization.

Request Evidence Completeness.

Request Integrity.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Success Criteria

A Reasoning Request is valid only when:

Request Identity is valid and unique.

Request Version is supported.

Lifecycle Status permits evaluation.

Exactly one canonical Reasoning Form is
declared.

Exactly one valid Goal Assertion is
referenced.

Graph target is immutable and resolvable.

All baseline references are compatible.

All Fact Source References are resolvable.

All mandatory Premise References are closed.

All referenced Rules are registered.

All referenced Constraints are registered.

Exactly one compatible Execution Context is
referenced.

Every Reasoning Limit is valid.

Closed-World Policy is explicit and
compatible.

Contradiction Policy is explicit and
compatible.

Expected Reasoning Outcome is explicit and
independent.

Canonical serialization succeeds.

Request Evidence is complete.

Request Integrity is valid.

No Failure Condition remains open.

The Request does not mutate a frozen
baseline.

---

## Release Boundary

Version 1.0 defines the canonical Reasoning
Request contract.

Version 1.0 includes:

Request identity.

Request version.

Request lifecycle.

Reasoning Form.

Goal Assertion Reference.

Graph target.

Baseline references.

Fact Source References.

Premise References.

Inference Rule References.

Constraint References.

Execution Context Reference.

Reasoning limits.

Closed-World Policy.

Contradiction Policy.

Expected Reasoning Outcome.

Request Evidence.

Request Integrity.

Canonical serialization.

Deterministic ordering.

Request Validation.

Failure behavior.

Read-only boundary.

Request invariants.

The following remain outside Version 1.0:

Production reasoning engine.

Rule execution implementation.

Parser implementation.

Compiler implementation.

Persistence implementation.

Transport implementation.

Graph mutation.

Ontology mutation.

Autonomous baseline admission.

Machine learning.

Probabilistic reasoning.

Future implementations shall preserve this
normative Request contract.

---

## Next Deliverable

CKP-005.4

Inference Rule Model.

---

# End of Specification
