# CKP-005

Title

Commerce Inference Rule Model

Abbreviation

CIRM

Version

1.0

Status

Draft

---

## Purpose

Define the canonical, deterministic,
registered, immutable, traceable,
evidence-producing, and auditable Inference
Rule model for the Commerce Knowledge
Platform.

The Inference Rule Model specializes the
Inference Rule structural component defined by
the Commerce Reasoning Structure Model.

An Inference Rule shall define one explicit
permitted derivation from validated Premises
to one deterministic Conclusion template.

The Inference Rule Model defines rule
structure, registration, applicability,
validation, evidence, and integrity.

It does not implement a reasoning engine.

It does not implement rule execution runtime.

It does not implement a parser or compiler.

It does not implement graph mutation.

---

## Normative Dependencies

The Commerce Inference Rule Model consumes:

HAS Foundation 1.0 LTS.

Specification Runtime 1.0.

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

CKP-003 Commerce Knowledge Graph 1.0.

CKP-004 Commerce Query Language 1.0.

CKP-005.1 Commerce Reasoning Charter.

CKP-005.2 Commerce Reasoning Structure Model.

CKP-005.3 Commerce Reasoning Request Model.

Every dependency shall remain immutable.

An Inference Rule shall not redefine any
frozen baseline.

---

## Rule Identity

Every Inference Rule shall possess one
immutable Rule Identifier.

Example

CKP-RULE-000001

Every Rule Identifier shall be globally unique
within one Rule Registry Version.

Rule identity shall remain distinct from Rule
Version.

A Rule Identifier shall never be reused for a
different normative Rule.

A Rule Identifier shall not create canonical
Commerce meaning.

A missing, malformed, duplicated, or reused
Rule Identifier shall cause validation
failure.

---

## Rule Version

Every Inference Rule shall declare one Rule
Version.

The initial supported Rule Version is:

1.0.

Rule Version shall identify the normative Rule
schema and semantic version.

Rule Version shall not replace Rule Identity.

An unsupported Rule Version shall cause
validation failure.

Rule version compatibility shall be verified
before applicability evaluation.

---

## Rule Lifecycle

Every Inference Rule shall declare one
Lifecycle Status.

Permitted initial Lifecycle Status values are:

Draft.

Approved.

Deprecated.

Retired.

Only an Approved Rule may participate in
reasoning.

A Deprecated Rule shall not participate unless
explicitly permitted by the Reasoning
Execution Context.

A Retired Rule shall not participate.

Lifecycle Status shall remain immutable during
one Reasoning Execution.

---

## Rule Type

Every Inference Rule shall declare exactly one
canonical Rule Type.

Permitted initial Rule Types are:

DIRECT.

HIERARCHICAL.

INVERSE.

TRANSITIVE.

COMPOSITIONAL.

CONSTRAINT.

CONTRADICTION.

DIRECT derives one Conclusion from explicit
validated Premises.

HIERARCHICAL derives only through registered
hierarchy semantics.

INVERSE derives only through a registered
canonical inverse relationship.

TRANSITIVE derives only through a Relationship
Type explicitly declared transitive.

COMPOSITIONAL derives only through one
registered Relationship Composition Rule.

CONSTRAINT evaluates compliance with one
registered constraint.

CONTRADICTION identifies incompatible explicit
assertions without repairing them.

Unknown or private Rule Types shall be invalid.

---

## Rule Properties

Every Inference Rule shall declare:

Rule Identifier.

Rule Version.

Preferred Rule Name.

Rule Type.

Lifecycle Status.

Rule Registry Reference.

Premise Definitions.

Premise Conjunction.

Variable Definitions.

Variable Binding Rules.

Applicability Constraints.

Conclusion Template.

Rule Priority.

Maximum Application Count.

Rule Evidence Reference.

Rule Integrity Reference.

Source Evidence Reference.

Every mandatory Rule property shall be
explicit.

No mandatory Rule property shall be inferred
from runtime defaults.

---

## Preferred Rule Name

Every Inference Rule shall declare one
Preferred Rule Name.

The Preferred Rule Name shall be:

Human-readable.

Stable within one Rule Version.

Non-normative for Rule identity.

Traceable to the Rule Identifier.

A Preferred Rule Name shall not replace the
Rule Identifier.

Duplicate Preferred Rule Names may exist only
when Rule Identifiers and Rule Versions remain
distinct and unambiguous.

---

## Rule Registry Reference

Every Inference Rule shall reference exactly
one Rule Registry.

The Rule Registry Reference shall declare:

Registry Identifier.

Registry Version.

Registry Status.

Registry Integrity Reference.

Registry Validation Evidence Reference.

The Rule Registry shall be immutable during
reasoning.

An unregistered Rule shall not participate in
reasoning.

Rule Registry substitution during evaluation
is prohibited.

---

## Premise Definition

Every Inference Rule shall declare one or more
Premise Definitions.

Every Premise Definition shall declare:

Premise Identifier.

Assertion Pattern.

Required Assertion Type.

Required Polarity.

Required Source Type.

Variable References.

Premise Priority.

Premise Optionality.

Premise Validation Reference.

Premise Integrity Reference.

Every mandatory Premise shall resolve before
Rule Application.

A Premise Definition shall not invent a Fact.

A Premise Definition shall not repair an
unresolved Fact or Assertion.

Duplicate Premise Identifiers shall be
invalid.

---

## Premise Conjunction

Every Inference Rule shall declare one
Premise Conjunction.

Permitted initial Premise Conjunction values
are:

ALL.

ANY.

ALL requires every mandatory Premise to
resolve successfully.

ANY requires at least one permitted Premise
branch to resolve successfully.

Premise Conjunction shall be explicit.

Conjunction shall not be inferred from
presentation order.

Ambiguous Premise grouping shall be invalid.

---

## Premise Priority

Every Premise Definition shall declare one
Premise Priority.

Premise Priority shall be a non-negative
integer.

Lower Premise Priority values shall be
evaluated before higher values.

Duplicate Premise Priority values within one
exclusive Premise scope shall be invalid.

Premise Priority shall not change Premise
semantics.

---

## Variable Definition

An Inference Rule may declare zero or more
Variable Definitions.

Every Variable Definition shall declare:

Variable Identifier.

Variable Type.

Binding Source.

Binding Scope.

Cardinality.

Required Binding.

Variable Validation Reference.

Variable Integrity Reference.

Permitted initial Variable Types are:

GRAPH NODE IDENTIFIER.

GRAPH EDGE IDENTIFIER.

GRAPH PATH IDENTIFIER.

CANONICAL TERM IDENTIFIER.

RELATIONSHIP TYPE.

TEXT.

INTEGER.

BOOLEAN.

ENUMERATION.

Unknown or private Variable Types shall be
invalid.

---

## Variable Binding Rules

Every referenced Variable shall possess one
explicit Binding Rule.

A Variable Binding Rule shall declare:

Variable Identifier.

Source Premise Reference.

Source Property.

Expected Variable Type.

Binding Cardinality.

Binding Compatibility Rule.

Binding Validation Reference.

Every required Variable shall be bound before
Conclusion construction.

Implicit type conversion shall be invalid.

Conflicting Variable Bindings shall invalidate
Rule Applicability.

Variable rebinding within one Rule Application
shall be prohibited.

---

## Applicability Constraints

An Inference Rule may declare zero or more
Applicability Constraints.

Every Applicability Constraint shall declare:

Constraint Identifier.

Constraint Type.

Constraint Scope.

Required Condition.

Forbidden Condition.

Cardinality Condition.

Value Condition.

Graph Scope.

Constraint Priority.

Constraint Integrity Reference.

Constraint Validation Evidence Reference.

Every mandatory Applicability Constraint shall
be satisfied before Rule Application.

Constraint evaluation shall not repair source
knowledge.

---

## Conclusion Template

Every Inference Rule shall declare exactly one
Conclusion Template.

The Conclusion Template shall declare:

Conclusion Template Identifier.

Subject Expression.

Predicate Expression.

Object Expression or Literal Expression.

Assertion Type.

Assertion Polarity.

Conclusion Type.

Graph Scope.

Lifecycle Status.

Conclusion Validation Reference.

Conclusion Integrity Template Reference.

Every required Variable referenced by the
Conclusion Template shall be bound.

A Conclusion Template shall not create
undocumented semantic meaning.

A Conclusion Template shall not automatically
register a Derived Assertion as a Graph Fact.

---

## Rule Priority

Every Inference Rule shall declare one Rule
Priority.

Rule Priority shall be a non-negative integer.

Lower Rule Priority values shall be evaluated
before higher values.

Duplicate Rule Priority values within one
exclusive Rule evaluation scope shall be
invalid.

Rule Priority shall not change Rule semantics.

Runtime discovery order shall not replace
normative Rule ordering.

---

## Maximum Application Count

Every Inference Rule shall declare one Maximum
Application Count.

Maximum Application Count shall be a
non-negative integer.

Maximum Application Count limits the number of
times the same Rule may be applied within one
Reasoning Request.

A value of zero shall prohibit Rule
Application.

A Rule shall not execute after its Maximum
Application Count is reached.

Exceeding Maximum Application Count shall
cause fail-closed evaluation.

---

## Rule Registration

Every Inference Rule shall be registered
before use.

Rule Registration shall verify:

Rule Identifier uniqueness.

Rule Version support.

Lifecycle validity.

Rule Type validity.

Rule Registry compatibility.

Premise Definition validity.

Premise Conjunction validity.

Variable Definition validity.

Variable Binding Rule validity.

Applicability Constraint validity.

Conclusion Template validity.

Rule Priority validity.

Maximum Application Count validity.

Canonical serialization.

Rule Evidence completeness.

Rule Integrity.

A Rule Registration Result shall be:

PASS.

FAIL.

A Rule with Registration Result FAIL shall not
participate in reasoning.

---

## Rule Applicability

An Inference Rule is applicable only when:

The Rule is registered.

The Rule Version is supported.

The Rule Lifecycle Status permits execution.

The Rule Type is permitted.

The Rule Registry is compatible.

Every mandatory Premise resolves.

Premise polarity is compatible.

Premise source type is compatible.

Premise conjunction is satisfied.

Every required Variable is bound.

Variable bindings are type-compatible.

Applicability Constraints are satisfied.

The Graph target is compatible.

Frozen baselines are compatible.

Maximum Reasoning Depth is not exceeded.

Maximum Application Count is not exceeded.

Rule Integrity is valid.

A Rule shall fail closed when applicability
cannot be established.

---

## Rule Application Input

Every Rule Application shall declare:

Rule Application Identifier.

Reasoning Request Identifier.

Rule Identifier.

Rule Version.

Resolved Premise References.

Resolved Fact References.

Resolved Derived Assertion References.

Variable Binding Set Reference.

Applicability Constraint Results.

Current Reasoning Depth.

Current Rule Application Count.

Execution Context Reference.

Rule Application Evidence Reference.

Rule Application Integrity Reference.

Every Rule Application Input shall remain
immutable during evaluation.

---

## Rule Application Result

Every attempted Rule Application shall produce
one Rule Application Result.

Permitted Rule Application Result values are:

APPLIED.

NOT APPLICABLE.

FAILED.

CANCELLED.

APPLIED means the Rule produced one valid
Conclusion.

NOT APPLICABLE means the Rule was valid but
its applicability conditions were not
satisfied.

FAILED means valid evaluation could not be
completed.

CANCELLED means evaluation was explicitly
terminated before completion.

A Rule Application Result shall declare:

Rule Application Identifier.

Rule Identifier.

Rule Version.

Application Status.

Applicability Result.

Resolved Premise References.

Variable Bindings.

Conclusion Reference.

Reasoning Depth.

Failure Classification.

Failure Reason.

Rule Application Evidence Reference.

Rule Application Result Integrity Reference.

---

## Derived Conclusion

An APPLIED Rule Application shall produce
exactly one Derived Conclusion.

Every Derived Conclusion shall declare:

Conclusion Identifier.

Rule Application Identifier.

Rule Identifier.

Rule Version.

Bound Premise References.

Resolved Fact References.

Variable Bindings.

Subject.

Predicate.

Object or Value.

Assertion Polarity.

Assertion Type.

Conclusion Type.

Graph Scope.

Reasoning Depth.

Proof Reference.

Evidence Reference.

Conclusion Integrity Reference.

A Derived Conclusion shall remain distinct from
a registered Fact.

A Derived Conclusion shall not automatically
enter a frozen baseline.

---

## Rule Evidence

Every registered Rule and every attempted Rule
Application shall produce deterministic
evidence.

Rule Evidence shall preserve:

Rule Identifier.

Rule Version.

Preferred Rule Name.

Rule Type.

Lifecycle Status.

Rule Registry Reference.

Premise Definitions.

Premise Conjunction.

Variable Definitions.

Variable Binding Rules.

Applicability Constraints.

Conclusion Template.

Rule Priority.

Maximum Application Count.

Registration Result.

Applicability Result.

Rule Application Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

No valid, invalid, applicable, non-applicable,
failed, or cancelled Rule evaluation shall
omit evidence.

---

## Rule Integrity

Every Inference Rule shall possess one
deterministic Rule Integrity Reference.

Rule Integrity shall bind:

Rule Identifier.

Rule Version.

Preferred Rule Name.

Rule Type.

Lifecycle Status.

Rule Registry Reference.

Premise Definitions.

Premise Conjunction.

Variable Definitions.

Variable Binding Rules.

Applicability Constraints.

Conclusion Template.

Rule Priority.

Maximum Application Count.

Rule Evidence Reference.

Source Evidence Reference.

Any normative Rule mutation shall invalidate
the Rule Integrity Reference.

---

## Rule Application Integrity

Every Rule Application shall possess one
deterministic Rule Application Integrity
Reference.

Rule Application Integrity shall bind:

Rule Application Identifier.

Reasoning Request Identifier.

Rule Identifier.

Rule Version.

Resolved Premise References.

Resolved Fact References.

Resolved Derived Assertion References.

Variable Bindings.

Applicability Constraint Results.

Reasoning Depth.

Rule Application Count.

Execution Context Reference.

Rule Application Evidence Reference.

---

## Canonical Serialization

Every Inference Rule and Rule Application
shall possess one deterministic canonical
serialization.

Canonical serialization shall:

Preserve every normative Rule property.

Preserve every normative Rule Application
property.

Use deterministic property ordering.

Use deterministic reference ordering.

Preserve Premise ordering.

Preserve Premise Conjunction.

Preserve Variable Definitions.

Preserve Variable Binding Rules.

Preserve Applicability Constraint ordering.

Preserve Conclusion Template structure.

Preserve Rule Priority.

Preserve Maximum Application Count.

Preserve Assertion Polarity.

Exclude non-normative presentation metadata.

Produce identical output for normatively equal
Rules and Rule Applications.

Canonical serialization shall be suitable for
integrity calculation.

---

## Deterministic Ordering

Every Rule collection shall possess one
deterministic ordering.

Premise Definitions shall be ordered by:

Premise Priority.

Then Premise Identifier.

Variable Definitions shall be ordered by:

Variable Identifier.

Applicability Constraints shall be ordered by:

Constraint Priority.

Then Constraint Identifier.

Applicable Rules shall be ordered by:

Rule Priority.

Then Rule Identifier.

Rule Applications shall be ordered by:

Reasoning Depth.

Then Rule Priority.

Then Rule Identifier.

Then Rule Application Identifier.

Runtime discovery order shall not affect
normative ordering.

Implementation-defined ordering is prohibited.

---

## Rule Validation

Rule Validation shall verify:

Rule Identifier validity.

Rule Version support.

Lifecycle Status validity.

Rule Type validity.

Rule Registry resolution.

Rule Registry compatibility.

Preferred Rule Name presence.

Premise Definition completeness.

Premise Identifier uniqueness.

Premise Priority validity.

Premise Conjunction validity.

Variable Definition completeness.

Variable Type validity.

Variable Binding Rule completeness.

Variable Binding compatibility.

Applicability Constraint completeness.

Applicability Constraint consistency.

Conclusion Template completeness.

Conclusion Variable closure.

Rule Priority validity.

Maximum Application Count validity.

Canonical serialization.

Rule Evidence completeness.

Rule Integrity.

Validation shall fail closed.

An invalid Rule shall not be registered or
applied.

---

## Validation Result

Every Rule Validation shall produce one
deterministic Validation Result.

Permitted Validation Result values are:

PASS.

FAIL.

PASS means every mandatory Rule validation
requirement is satisfied.

FAIL means one or more mandatory Rule
requirements are violated.

The Validation Result shall declare:

Validation Identifier.

Rule Identifier.

Rule Version.

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

Initial Inference Rule Failure
Classifications are:

RULE_IDENTITY_VIOLATION.

RULE_VERSION_VIOLATION.

RULE_LIFECYCLE_VIOLATION.

RULE_TYPE_VIOLATION.

RULE_REGISTRY_VIOLATION.

PREFERRED_NAME_VIOLATION.

PREMISE_DEFINITION_VIOLATION.

PREMISE_IDENTITY_VIOLATION.

PREMISE_PRIORITY_VIOLATION.

PREMISE_CONJUNCTION_VIOLATION.

VARIABLE_DEFINITION_VIOLATION.

VARIABLE_TYPE_VIOLATION.

VARIABLE_BINDING_VIOLATION.

APPLICABILITY_CONSTRAINT_VIOLATION.

CONCLUSION_TEMPLATE_VIOLATION.

CONCLUSION_VARIABLE_CLOSURE_VIOLATION.

RULE_PRIORITY_VIOLATION.

MAXIMUM_APPLICATION_COUNT_VIOLATION.

RULE_REGISTRATION_VIOLATION.

RULE_APPLICABILITY_VIOLATION.

RULE_APPLICATION_VIOLATION.

CONCLUSION_VIOLATION.

BASELINE_VIOLATION.

SERIALIZATION_VIOLATION.

EVIDENCE_VIOLATION.

INTEGRITY_VIOLATION.

READ_ONLY_VIOLATION.

---

## Failure Conditions

An Inference Rule shall fail validation or
application when:

The Rule Identifier is missing, malformed,
duplicated, or improperly reused.

The Rule Version is missing or unsupported.

Lifecycle Status is missing, unknown, or
incompatible.

Rule Type is missing, unknown, private, or
incompatible.

The Rule Registry cannot be resolved.

The Rule Registry is incompatible.

Preferred Rule Name is missing.

A mandatory Premise Definition is incomplete.

A Premise Identifier is missing or duplicated.

Premise Priority is negative or duplicated.

Premise Conjunction is missing, unknown, or
ambiguous.

A Variable Definition is incomplete.

A Variable Type is unknown or private.

A required Variable cannot be bound.

A Variable Binding is type-incompatible.

Conflicting Variable Bindings exist.

An Applicability Constraint is unresolved or
violated.

The Conclusion Template is incomplete.

A Conclusion Template references an unbound
Variable.

Rule Priority is negative or duplicated.

Maximum Application Count is negative.

Maximum Application Count is exceeded.

The Rule is unregistered.

Rule Applicability cannot be established.

A Derived Conclusion violates the Conclusion
Template.

A frozen baseline reference is incompatible.

Deterministic ordering cannot be established.

Canonical serialization cannot be produced.

Rule Evidence cannot be produced.

Rule Integrity cannot be established.

Rule Application Integrity cannot be
established.

The Rule attempts to mutate source knowledge
or a frozen baseline.

---

## Read-Only Boundary

An Inference Rule shall not:

Create a Canonical Commerce Term.

Create an Ontology Assertion.

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Register a Derived Conclusion as a Graph Fact.

Delete a Canonical Commerce Term.

Delete an Ontology Assertion.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Component.

Modify a Query Result.

Modify a registered Fact.

Modify a Premise source.

Modify a registered Rule during execution.

Modify a registered Constraint.

Modify an Execution Context.

Repair an unresolved Premise.

Repair a missing inverse relationship.

Repair a violated Constraint.

Resolve a contradiction by deleting evidence.

Modify HAS Foundation 1.0 LTS.

Modify Specification Runtime 1.0.

Modify CKP-001.

Modify CKP-002.

Modify CKP-003.

Modify CKP-004.

Modify CKP-005.1.

Modify CKP-005.2.

Modify CKP-005.3.

Create undocumented semantic meaning.

---

## Rule Invariants

Read-Only Preservation.

Canonical Rule Identity.

Rule Version Preservation.

Lifecycle Validity.

Canonical Rule Type.

Rule Registration Closure.

Exactly One Rule Registry.

Premise Definition Completeness.

Premise Identity Uniqueness.

Premise Priority Integrity.

Explicit Premise Conjunction.

Variable Definition Completeness.

Variable Type Compatibility.

Variable Binding Completeness.

Variable Binding Consistency.

Applicability Constraint Closure.

Exactly One Conclusion Template.

Conclusion Variable Closure.

Rule Priority Integrity.

Maximum Application Count Enforcement.

Deterministic Premise Ordering.

Deterministic Variable Ordering.

Deterministic Constraint Ordering.

Deterministic Rule Ordering.

Deterministic Rule Application Ordering.

Derived Conclusion Traceability.

Derived Conclusion Non-Registration.

Rule Evidence Completeness.

Rule Integrity.

Rule Application Integrity.

Canonical Serialization.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Success Criteria

An Inference Rule is valid only when:

Rule Identity is valid and unique.

Rule Version is supported.

Lifecycle Status permits registration.

Exactly one canonical Rule Type is declared.

Exactly one compatible Rule Registry is
referenced.

Preferred Rule Name is present.

One or more valid Premise Definitions are
declared.

Premise Conjunction is explicit.

Every Variable Definition is complete.

Every required Variable Binding Rule is
complete.

Every Applicability Constraint is valid.

Exactly one complete Conclusion Template is
declared.

Every Conclusion Variable is closed.

Rule Priority is valid.

Maximum Application Count is valid.

Canonical serialization succeeds.

Rule Evidence is complete.

Rule Integrity is valid.

No Failure Condition remains open.

The Rule does not mutate source knowledge or a
frozen baseline.

---

## Release Boundary

Version 1.0 defines the canonical Commerce
Inference Rule contract.

Version 1.0 includes:

Rule identity.

Rule version.

Rule lifecycle.

Rule type.

Preferred Rule Name.

Rule Registry Reference.

Premise Definitions.

Premise Conjunction.

Premise Priority.

Variable Definitions.

Variable Binding Rules.

Applicability Constraints.

Conclusion Template.

Rule Priority.

Maximum Application Count.

Rule Registration.

Rule Applicability.

Rule Application Input.

Rule Application Result.

Derived Conclusion.

Rule Evidence.

Rule Integrity.

Rule Application Integrity.

Canonical serialization.

Deterministic ordering.

Rule Validation.

Failure behavior.

Read-only boundary.

Rule invariants.

The following remain outside Version 1.0:

Production rule engine.

Rule execution runtime.

Rule parser.

Rule compiler.

Rule optimization.

Distributed rule execution.

Persistence implementation.

Transport implementation.

Graph mutation.

Ontology mutation.

Autonomous Rule admission.

Machine learning.

Probabilistic inference.

Future implementations shall preserve this
normative Inference Rule contract.

---

## Next Deliverable

CKP-005.5

Fact and Premise Model.

---

# End of Specification
