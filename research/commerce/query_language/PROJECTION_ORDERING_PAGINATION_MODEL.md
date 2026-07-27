# Commerce Query Language Projection, Ordering, and Pagination Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative Projection, Ordering,
and Pagination model for Commerce Query
Language.

The model defines how eligible registered
Graph Components are projected into
read-only result records, deterministically
ordered, and divided into stable result
windows.

Projection, Ordering, and Pagination shall
not create, modify, infer, or redefine
canonical Commerce knowledge.

---

## Processing Pipeline

The normative processing pipeline is:

Eligible Component Set Resolution.

Projection Expression Resolution.

Projection Validation.

Projection Application.

Projected Record Set Construction.

Ordering Expression Resolution.

Ordering Validation.

Deterministic Ordering Application.

Ordered Record Set Construction.

Pagination Expression Resolution.

Pagination Validation.

Pagination Application.

Returned Result Window Construction.

Evidence Construction.

Integrity Construction.

A later stage shall not execute before all
mandatory earlier stages have passed.

---

## Projection Expression

A Projection Expression defines the
registered properties returned for each
eligible Graph Component.

Every Projection Expression shall declare:

Projection Identifier.

Expression Version.

Query Identifier.

Selection Identifier.

Selected Component Type.

Projected Property References.

Projection Alias References.

Projection Position References.

Lifecycle Status.

Projection Integrity Reference.

Projection Validation Evidence Reference.

Source Evidence Reference.

A Query Request may reference zero or one
Projection Expression.

When no Projection Expression is referenced,
the canonical default projection shall apply.

---

## Projection Identity

Every Projection Expression shall possess one
immutable Projection Identifier.

Example

CKP-PROJECTION-000001

Projection Identifiers shall be unique within
one Query Request.

Projection identity shall remain distinct from
Expression Version.

A Projection Identifier shall not create
canonical Commerce meaning.

A Projection Identifier shall never be reused
for a different normative Projection
Expression.

---

## Projected Property

Every Projected Property shall declare:

Projected Property Identifier.

Canonical Property Name.

Selected Component Type.

Projection Position.

Projection Alias Reference.

Property Validation Reference.

Projected Property Integrity Reference.

Every Projected Property shall be registered.

Every Projected Property shall be applicable
to the selected Graph Component type.

Every Projected Property shall preserve its
canonical normative meaning.

Every Projected Property shall remain
traceable to its source Graph Component.

Projection shall not create a canonical
property.

Projection shall not modify source Graph
Components.

---

## Graph Node Projection Properties

Permitted initial Graph Node Projection
Properties are:

Canonical Identifier.

Preferred Name.

Knowledge Object Type.

Lifecycle Status.

Ontology Membership.

Domain Membership.

Registry Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Node Integrity Reference.

Unknown or private Graph Node Projection
Properties shall be invalid.

---

## Graph Edge Projection Properties

Permitted initial Graph Edge Projection
Properties are:

Relationship Identifier.

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

Directionality.

Inverse Relationship Reference.

Lifecycle Status.

Ontology Assertion Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Edge Integrity Reference.

Unknown or private Graph Edge Projection
Properties shall be invalid.

---

## Graph Path Projection Properties

Permitted initial Graph Path Projection
Properties are:

Path Identifier.

Start Node Identifier.

End Node Identifier.

Ordered Node Sequence.

Ordered Edge Sequence.

Traversal Direction.

Path Length.

Validation Result.

Evidence Reference.

Unknown or private Graph Path Projection
Properties shall be invalid.

---

## Projection Applicability

A Graph Node Projection Expression shall use
only Graph Node Projection Properties.

A Graph Edge Projection Expression shall use
only Graph Edge Projection Properties.

A Graph Path Projection Expression shall use
only Graph Path Projection Properties.

A registered property that is inapplicable to
the selected Graph Component type shall be
invalid.

Projection applicability shall be validated
before Projection Application.

---

## Projection Alias

A Projection Alias is one non-normative
presentation label.

Every Projection Alias shall declare:

Projection Alias Identifier.

Projected Property Identifier.

Alias Value.

Alias Validation Reference.

Projection Alias Integrity Reference.

Projection Aliases shall not replace
canonical property names.

Projection Aliases shall not change normative
property meaning.

Projection Aliases shall not become canonical
identifiers.

Projection Aliases shall not become canonical
definitions.

Query Evidence shall retain the canonical
property name when an alias is presented.

Duplicate Projection Alias Identifiers shall
be invalid.

---

## Projection Position

Every Projected Property shall possess one
explicit Projection Position.

Projection Position shall be a non-negative
integer.

Projection Position values shall be unique
within one Projection Expression.

Lower Projection Position values shall appear
before higher Projection Position values.

Duplicate Projection Position values shall be
invalid.

Projection Position shall not alter canonical
property meaning.

---

## Default Graph Node Projection

The canonical default Graph Node projection
is:

Position 0

Canonical Identifier.

Position 1

Preferred Name.

Position 2

Knowledge Object Type.

Position 3

Lifecycle Status.

Position 4

Ontology Membership.

Position 5

Domain Membership.

---

## Default Graph Edge Projection

The canonical default Graph Edge projection
is:

Position 0

Relationship Identifier.

Position 1

Source Node Identifier.

Position 2

Canonical Relationship Type.

Position 3

Target Node Identifier.

Position 4

Directionality.

Position 5

Lifecycle Status.

---

## Default Graph Path Projection

The canonical default Graph Path projection
is:

Position 0

Path Identifier.

Position 1

Start Node Identifier.

Position 2

End Node Identifier.

Position 3

Ordered Node Sequence.

Position 4

Ordered Edge Sequence.

Position 5

Path Length.

---

## Projected Record

A Projected Record is one read-only
representation of one eligible Graph
Component.

Every Projected Record shall declare:

Projected Record Identifier.

Source Component Identifier.

Selected Component Type.

Ordered Projected Properties.

Canonical Property References.

Projection Alias References.

Projection Identifier.

Projected Record Integrity Reference.

Every Projected Record shall reference exactly
one source Graph Component.

A Projected Record shall not become an
independent Graph Component.

A Projected Record shall not replace its
source Graph Component.

---

## Projected Record Set

Projected Record Set is the deterministic
ordered collection of Projected Records
created from the Eligible Component Set.

Every Projected Record Set shall declare:

Projected Record Set Identifier.

Eligible Set Identifier.

Projection Identifier.

Ordered Projected Record Identifiers.

Projected Record Count.

Projected Record Set Integrity Reference.

Projected Record Count shall equal Eligible
Component Count before Pagination is applied.

Every Projected Record shall correspond to
exactly one eligible Graph Component.

Projection shall preserve Eligible Component
Set ordering until Ordering Expressions are
applied.

---

## Projection Result

Projection Result represents the deterministic
outcome of Projection Application.

Every Projection Result shall declare:

Projection Identifier.

Query Identifier.

Eligible Set Identifier.

Projected Record Set Identifier.

Input Component Count.

Projected Record Count.

Projection Status.

Failure Classification.

Failure Reason.

Projection Evidence Reference.

Projection Result Integrity Reference.

Permitted Projection Status values are:

Not Evaluated.

Evaluated.

Failed.

Cancelled.

Evaluated, Failed, and Cancelled are terminal
Projection Status values.

---

## Projection Evidence

Every Projection operation shall produce
deterministic Projection Evidence.

Projection Evidence shall declare:

Evidence Identifier.

Projection Identifier.

Query Identifier.

Selected Component Type.

Eligible Set Identifier.

Applied Property References.

Applied Projection Positions.

Applied Alias References.

Projected Record Set Identifier.

Input Component Count.

Projected Record Count.

Property Applicability Result.

Projection Position Validation Result.

Alias Validation Result.

Projection Integrity Result.

Projection Result Integrity Result.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Ordering Expression

An Ordering Expression defines one
deterministic ordering rule for Projected
Records.

Every Ordering Expression shall declare:

Ordering Identifier.

Expression Version.

Query Identifier.

Projection Identifier.

Ordering Property.

Ordering Direction.

Null Ordering.

Ordering Priority.

Lifecycle Status.

Ordering Integrity Reference.

Ordering Validation Evidence Reference.

Source Evidence Reference.

A Query Request may reference zero or more
Ordering Expressions.

---

## Ordering Identity

Every Ordering Expression shall possess one
immutable Ordering Identifier.

Example

CKP-ORDERING-000001

Ordering Identifiers shall be unique within
one Query Request.

Ordering identity shall remain distinct from
Expression Version.

An Ordering Identifier shall not create
canonical Commerce meaning.

An Ordering Identifier shall never be reused
for a different normative Ordering
Expression.

---

## Ordering Property

Every Ordering Property shall be:

Registered.

Applicable to the selected Graph Component
type.

Present in the canonical source Graph
Component.

Deterministically comparable.

Normatively stable.

An Ordering Property does not need to be
included in the visible Projection Result,
but it shall remain available through Query
Evidence.

Unknown, private, inapplicable, or
non-comparable Ordering Properties shall be
invalid.

Projection Aliases shall not be used as
normative Ordering Properties.

---

## Comparable Property Types

Permitted initial comparable property types
are:

IDENTIFIER.

TEXT.

INTEGER.

ENUMERATION.

BOOLEAN.

Composite lists and nested structures shall
not be ordering properties in Version 1.0.

Ordering comparison shall not depend on
storage technology.

Implicit property type conversion shall be
invalid.

---

## Ordering Direction

Permitted initial Ordering Direction values
are:

ASCENDING.

DESCENDING.

ASCENDING shall place lower canonical values
before higher canonical values.

DESCENDING shall place higher canonical
values before lower canonical values.

Unknown or private Ordering Direction values
shall be invalid.

---

## Null Ordering

Permitted initial Null Ordering values are:

NULLS FIRST.

NULLS LAST.

Null Ordering shall be explicit when an
Ordering Property permits absent values.

NULLS FIRST shall place absent values before
present values.

NULLS LAST shall place absent values after
present values.

Implicit platform-specific null ordering
shall be prohibited.

---

## Ordering Priority

Every Ordering Expression shall declare one
Ordering Priority.

Ordering Priority shall be a non-negative
integer.

Ordering Priority values shall be unique
within one Query Request.

Lower Ordering Priority values shall be
applied before higher Ordering Priority
values.

Duplicate Ordering Priority values shall be
invalid.

Ordering Priority shall not alter canonical
property meaning.

---

## Deterministic Ordering

Ordering Expressions shall be applied in this
order:

Ordering Priority.

Then Ordering Identifier as a deterministic
tie-breaker only where equal priority is
permitted by a future version.

Version 1.0 prohibits equal Ordering Priority
values.

When all explicit Ordering Properties compare
equal, canonical default identifier ordering
shall act as the final deterministic
tie-breaker.

Graph Node records shall use Canonical
Identifier.

Graph Edge records shall use Relationship
Identifier.

Graph Path records shall use Path Identifier.

Identical Projected Record Sets and Ordering
Expressions shall produce identical Ordered
Record Sets.

---

## Default Ordering

When no Ordering Expression is declared:

Graph Node records shall be ordered by
Canonical Identifier in ASCENDING order.

Graph Edge records shall be ordered by
Relationship Identifier in ASCENDING order.

Graph Path records shall be ordered by Path
Identifier in ASCENDING order.

Default ordering shall be deterministic.

Default ordering shall occur before
Pagination Application.

Presentation order shall not replace
normative ordering.

---

## Ordered Record Set

Ordered Record Set is the deterministic
ordering of one Projected Record Set.

Every Ordered Record Set shall declare:

Ordered Record Set Identifier.

Projected Record Set Identifier.

Ordered Record Identifiers.

Applied Ordering References.

Default Ordering Applied.

Ordering Tie-Breaker.

Ordered Record Count.

Ordered Record Set Integrity Reference.

Ordered Record Count shall equal Projected
Record Count.

Ordering shall not create or remove Projected
Records.

Ordering shall only change record position.

---

## Ordering Result

Ordering Result represents the deterministic
outcome of Ordering Application.

Every Ordering Result shall declare:

Query Identifier.

Projected Record Set Identifier.

Ordered Record Set Identifier.

Applied Ordering Expression Count.

Default Ordering Applied.

Ordered Record Count.

Ordering Status.

Failure Classification.

Failure Reason.

Ordering Evidence Reference.

Ordering Result Integrity Reference.

Permitted Ordering Status values are:

Not Evaluated.

Evaluated.

Failed.

Cancelled.

Evaluated, Failed, and Cancelled are terminal
Ordering Status values.

---

## Ordering Evidence

Every Ordering operation shall produce
deterministic Ordering Evidence.

Ordering Evidence shall declare:

Evidence Identifier.

Query Identifier.

Projected Record Set Identifier.

Applied Ordering Identifiers.

Applied Ordering Properties.

Applied Ordering Directions.

Applied Null Ordering Rules.

Applied Ordering Priorities.

Applied Tie-Breaker.

Ordered Record Set Identifier.

Input Record Count.

Ordered Record Count.

Property Comparability Result.

Priority Validation Result.

Determinism Result.

Ordering Integrity Result.

Ordering Result Integrity Result.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Pagination Expression

A Pagination Expression defines one
deterministic window over an Ordered Record
Set.

Every Pagination Expression shall declare:

Pagination Identifier.

Expression Version.

Query Identifier.

Ordered Record Set Reference.

Limit.

Offset.

Lifecycle Status.

Pagination Integrity Reference.

Pagination Validation Evidence Reference.

Source Evidence Reference.

A Query Request may reference zero or one
Pagination Expression.

---

## Pagination Identity

Every Pagination Expression shall possess one
immutable Pagination Identifier.

Example

CKP-PAGINATION-000001

Pagination Identifiers shall be unique within
one Query Request.

Pagination identity shall remain distinct from
Expression Version.

A Pagination Identifier shall not create
canonical Commerce meaning.

A Pagination Identifier shall never be reused
for a different normative Pagination
Expression.

---

## Limit

Limit defines the maximum number of Ordered
Records returned.

Limit shall be a non-negative integer.

Limit shall not exceed the Maximum Result
Limit declared by Execution Context.

Limit zero shall return an empty Returned
Result Window.

Limit zero shall not change Matched Record
Count.

An omitted Pagination Expression shall use
the Execution Context default result boundary
when one is declared.

---

## Offset

Offset defines the number of Ordered Records
skipped before result collection begins.

Offset shall be a non-negative integer.

Offset zero shall begin at the first Ordered
Record.

Offset equal to Ordered Record Count shall
return an empty Returned Result Window.

Offset greater than Ordered Record Count shall
return an empty Returned Result Window.

Offset shall not change Matched Record Count.

---

## Pagination Application

Pagination shall occur only after:

Selection.

Filtering.

Projection.

Deterministic Ordering.

Pagination shall apply Offset first.

Pagination shall apply Limit after Offset.

Pagination shall not reorder records.

Pagination shall not create records.

Pagination shall not remove records from the
underlying Ordered Record Set.

Pagination affects only the Returned Result
Window.

---

## Page Boundary

Page Boundary defines the deterministic start
and end positions of one Returned Result
Window.

Every Page Boundary shall declare:

Boundary Identifier.

Ordered Record Count.

Offset.

Limit.

Start Position.

End Position Exclusive.

Returned Record Count.

Has Previous Records.

Has Following Records.

Boundary Integrity Reference.

Start Position shall equal the lesser of
Offset and Ordered Record Count.

End Position Exclusive shall equal the lesser
of:

Start Position plus Limit.

Ordered Record Count.

Returned Record Count shall equal:

End Position Exclusive minus Start Position.

---

## Returned Result Window

Returned Result Window is the deterministic
ordered subset of an Ordered Record Set
selected by Pagination.

Every Returned Result Window shall declare:

Returned Window Identifier.

Ordered Record Set Identifier.

Pagination Identifier.

Page Boundary Identifier.

Ordered Returned Record Identifiers.

Matched Record Count.

Returned Record Count.

Offset.

Limit.

Returned Window Integrity Reference.

Matched Record Count shall equal Ordered
Record Count.

Returned Record Count shall equal the number
of Ordered Returned Record Identifiers.

Every returned record shall originate from
the referenced Ordered Record Set.

Returned ordering shall preserve Ordered
Record Set ordering.

---

## Pagination Result

Pagination Result represents the
deterministic outcome of Pagination
Application.

Every Pagination Result shall declare:

Pagination Identifier.

Query Identifier.

Ordered Record Set Identifier.

Returned Window Identifier.

Matched Record Count.

Returned Record Count.

Offset.

Limit.

Pagination Status.

Failure Classification.

Failure Reason.

Pagination Evidence Reference.

Pagination Result Integrity Reference.

Permitted Pagination Status values are:

Not Evaluated.

Evaluated.

Failed.

Cancelled.

Evaluated, Failed, and Cancelled are terminal
Pagination Status values.

---

## Pagination Determinism

Identical Query Requests executed against the
same immutable Graph Version shall produce
identical:

Ordered Record Sets.

Page Boundaries.

Returned Result Windows.

Matched Record Counts.

Returned Record Counts.

Offset and Limit values.

Pagination Integrity References.

Execution Timestamp shall not alter normative
Pagination equality.

---

## Pagination Evidence

Every Pagination operation shall produce
deterministic Pagination Evidence.

Pagination Evidence shall declare:

Evidence Identifier.

Pagination Identifier.

Query Identifier.

Ordered Record Set Identifier.

Ordered Record Count.

Applied Offset.

Applied Limit.

Execution Context Maximum Result Limit.

Page Boundary Identifier.

Returned Window Identifier.

Matched Record Count.

Returned Record Count.

Boundary Validation Result.

Result Limit Validation Result.

Ordering Preservation Result.

Pagination Integrity Result.

Pagination Result Integrity Result.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Projection Integrity

Every Projection Expression shall possess one
deterministic Projection Integrity Reference.

Projection Integrity shall bind:

Projection Identifier.

Expression Version.

Query Identifier.

Selection Identifier.

Selected Component Type.

Projected Property References.

Projection Alias References.

Projection Position References.

Lifecycle Status.

---

## Projected Record Integrity

Every Projected Record shall possess one
deterministic Projected Record Integrity
Reference.

Projected Record Integrity shall bind:

Projected Record Identifier.

Source Component Identifier.

Selected Component Type.

Ordered Projected Properties.

Canonical Property References.

Projection Alias References.

Projection Identifier.

---

## Ordering Integrity

Every Ordering Expression shall possess one
deterministic Ordering Integrity Reference.

Ordering Integrity shall bind:

Ordering Identifier.

Expression Version.

Query Identifier.

Projection Identifier.

Ordering Property.

Ordering Direction.

Null Ordering.

Ordering Priority.

Lifecycle Status.

---

## Ordered Record Set Integrity

Every Ordered Record Set shall possess one
deterministic Ordered Record Set Integrity
Reference.

Ordered Record Set Integrity shall bind:

Ordered Record Set Identifier.

Projected Record Set Identifier.

Ordered Record Identifiers.

Applied Ordering References.

Default Ordering Applied.

Ordering Tie-Breaker.

Ordered Record Count.

---

## Pagination Integrity

Every Pagination Expression shall possess one
deterministic Pagination Integrity Reference.

Pagination Integrity shall bind:

Pagination Identifier.

Expression Version.

Query Identifier.

Ordered Record Set Reference.

Limit.

Offset.

Lifecycle Status.

---

## Returned Window Integrity

Every Returned Result Window shall possess one
deterministic Returned Window Integrity
Reference.

Returned Window Integrity shall bind:

Returned Window Identifier.

Ordered Record Set Identifier.

Pagination Identifier.

Page Boundary Identifier.

Ordered Returned Record Identifiers.

Matched Record Count.

Returned Record Count.

Offset.

Limit.

---

## Canonical Serialization

Projection Expressions, Projected Records,
Projected Record Sets, Ordering Expressions,
Ordered Record Sets, Pagination Expressions,
Page Boundaries, and Returned Result Windows
shall each possess one deterministic
canonical serialization.

Canonical serialization shall:

Preserve every normative property.

Use deterministic property ordering.

Use deterministic reference ordering.

Preserve Projection Position.

Preserve Ordering Priority.

Preserve Offset and Limit.

Preserve canonical identifiers.

Exclude non-normative presentation metadata.

Produce identical output for normatively
equal structures.

Canonical serialization shall be suitable for
integrity calculation.

---

## Projection Validation

Projection Validation shall verify:

Projection Identifier validity.

Expression Version support.

Query Identifier resolution.

Selection Identifier resolution.

Selected Component Type compatibility.

Projected Property registration.

Projected Property applicability.

Projection Alias validity.

Projection Position validity.

Projection Position uniqueness.

Lifecycle compatibility.

Source component traceability.

Projection immutability.

Canonical serialization.

Projection Integrity.

---

## Ordering Validation

Ordering Validation shall verify:

Ordering Identifier validity.

Expression Version support.

Query Identifier resolution.

Projection Identifier resolution.

Ordering Property registration.

Ordering Property applicability.

Ordering Property comparability.

Ordering Direction validity.

Null Ordering validity.

Ordering Priority validity.

Ordering Priority uniqueness.

Default ordering availability.

Tie-breaker availability.

Lifecycle compatibility.

Ordering immutability.

Canonical serialization.

Ordering Integrity.

---

## Pagination Validation

Pagination Validation shall verify:

Pagination Identifier validity.

Expression Version support.

Query Identifier resolution.

Ordered Record Set resolution.

Limit validity.

Offset validity.

Maximum Result Limit compliance.

Page Boundary correctness.

Returned Record Count correctness.

Matched Record Count preservation.

Ordering preservation.

Lifecycle compatibility.

Pagination immutability.

Canonical serialization.

Pagination Integrity.

---

## Validation Result

Projection, Ordering, and Pagination
validation shall each produce one
deterministic Validation Result.

Permitted Validation Result values are:

PASS.

FAIL.

PASS means every mandatory validation rule is
satisfied.

FAIL means one or more mandatory validation
rules are violated.

Validation shall fail closed.

A Projection Expression, Ordering Expression,
or Pagination Expression with Validation
Result FAIL shall not participate in Query
execution.

---

## Failure Classifications

Initial Projection, Ordering, and Pagination
Failure Classifications are:

PROJECTION_IDENTITY_VIOLATION.

PROJECTION_PROPERTY_VIOLATION.

PROJECTION_APPLICABILITY_VIOLATION.

PROJECTION_ALIAS_VIOLATION.

PROJECTION_POSITION_VIOLATION.

PROJECTED_RECORD_VIOLATION.

PROJECTION_RESULT_VIOLATION.

ORDERING_IDENTITY_VIOLATION.

ORDERING_PROPERTY_VIOLATION.

ORDERING_APPLICABILITY_VIOLATION.

ORDERING_COMPARABILITY_VIOLATION.

ORDERING_DIRECTION_VIOLATION.

NULL_ORDERING_VIOLATION.

ORDERING_PRIORITY_VIOLATION.

DETERMINISTIC_ORDERING_VIOLATION.

ORDERED_RECORD_SET_VIOLATION.

PAGINATION_IDENTITY_VIOLATION.

LIMIT_VIOLATION.

OFFSET_VIOLATION.

PAGE_BOUNDARY_VIOLATION.

RETURNED_WINDOW_VIOLATION.

RESULT_COUNT_VIOLATION.

ORDERING_PRESERVATION_VIOLATION.

LIFECYCLE_VIOLATION.

BASELINE_VIOLATION.

IMMUTABILITY_VIOLATION.

SERIALIZATION_VIOLATION.

INTEGRITY_VIOLATION.

EVIDENCE_VIOLATION.

---

## Failure Conditions

Projection, Ordering, or Pagination
validation shall fail when:

The Projection Identifier is missing,
invalid, duplicated, or improperly reused.

A Projected Property is unknown or private.

A Projected Property is inapplicable to the
selected Graph Component type.

A Projection Alias changes normative property
meaning.

A Projection Position is negative or
duplicated.

A Projected Record cannot be traced to one
eligible Graph Component.

Projected Record Count differs from Eligible
Component Count before Pagination.

The Ordering Identifier is missing, invalid,
duplicated, or improperly reused.

An Ordering Property is unknown, private,
inapplicable, or non-comparable.

Ordering Direction is unknown or private.

Required Null Ordering is missing.

Ordering Priority is negative or duplicated.

Deterministic ordering cannot be established.

No canonical tie-breaker can be resolved.

Ordering creates or removes a Projected
Record.

The Pagination Identifier is missing,
invalid, duplicated, or improperly reused.

Limit is negative.

Limit exceeds the Execution Context Maximum
Result Limit.

Offset is negative.

Pagination is applied before deterministic
ordering.

Page Boundary is inconsistent.

Returned Record Count is inconsistent.

Matched Record Count is changed by
Pagination.

Returned ordering differs from Ordered Record
Set ordering.

A source record or Graph Component reference
cannot be resolved.

A baseline reference is incompatible.

An expression or result structure is mutated
after evaluation begins.

Canonical serialization cannot be produced.

Required integrity cannot be established.

Required evidence cannot be produced.

---

## Read-Only Boundary

Projection, Ordering, and Pagination shall
not:

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Component.

Modify an Eligible Component Set member.

Modify a Projected Record source.

Modify a Canonical Identifier.

Modify a Preferred Name.

Modify a Canonical Definition.

Modify a Relationship Type.

Modify directionality.

Modify an inverse relationship.

Modify CKP-001.

Modify CKP-002.

Modify CKP-003.

Create undocumented semantic meaning.

---

## Projection Constraints

Every Projected Property shall be registered
and applicable.

Every Projected Property shall preserve
canonical meaning.

Every Projected Record shall reference one
eligible Graph Component.

Every Projection Position shall be unique.

Every Projection Alias shall remain
non-normative.

Projection shall not change Eligible
Component Count.

Projection shall preserve source
traceability.

---

## Ordering Constraints

Every Ordering Property shall be registered,
applicable, and comparable.

Every Ordering Direction shall be explicit.

Every required Null Ordering rule shall be
explicit.

Every Ordering Priority shall be unique.

Every Ordered Record shall originate from the
Projected Record Set.

Ordering shall not create or remove records.

Ordering shall use one deterministic final
tie-breaker.

Ordering shall occur before Pagination.

---

## Pagination Constraints

Limit and Offset shall be non-negative.

Limit shall remain within Execution Context
boundaries.

Pagination shall apply Offset before Limit.

Pagination shall preserve Matched Record
Count.

Every returned record shall originate from
the Ordered Record Set.

Returned ordering shall preserve Ordered
Record Set ordering.

Pagination shall affect only the Returned
Result Window.

---

## Model Invariants

Read-Only Preservation.

Canonical Projection Identity.

Projection Property Canonicality.

Projection Property Applicability.

Projection Alias Non-Normativity.

Projection Position Integrity.

Projected Record Source Closure.

Projected Record Count Integrity.

Canonical Ordering Identity.

Ordering Property Canonicality.

Ordering Property Applicability.

Ordering Property Comparability.

Ordering Direction Validity.

Explicit Null Ordering.

Deterministic Ordering Priority.

Deterministic Default Ordering.

Deterministic Tie-Breaking.

Ordered Record Set Closure.

Ordered Record Count Integrity.

Canonical Pagination Identity.

Limit Boundary Integrity.

Offset Boundary Integrity.

Page Boundary Integrity.

Matched Record Count Preservation.

Returned Record Count Integrity.

Returned Window Subset Integrity.

Returned Ordering Preservation.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Projection Integrity.

Ordering Integrity.

Pagination Integrity.

Canonical Serialization.

Evidence Completeness.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Release Criteria

Processing Pipeline is explicitly defined.

Projection Expression and Identity are
explicitly defined.

Projected Properties and applicability are
explicitly defined.

Graph Node, Graph Edge, and Graph Path
Projection Properties are explicitly defined.

Projection Aliases and Positions are
explicitly defined.

Default Projections are explicitly defined.

Projected Record, Projected Record Set, and
Projection Result are explicitly defined.

Projection Evidence is explicitly defined.

Ordering Expression and Identity are
explicitly defined.

Ordering Property and comparable property
types are explicitly defined.

Ordering Direction, Null Ordering, and
Ordering Priority are explicitly defined.

Deterministic and Default Ordering are
explicitly defined.

Ordered Record Set, Ordering Result, and
Ordering Evidence are explicitly defined.

Pagination Expression and Identity are
explicitly defined.

Limit, Offset, and Pagination Application are
explicitly defined.

Page Boundary is explicitly defined.

Returned Result Window and Pagination Result
are explicitly defined.

Pagination Determinism and Evidence are
explicitly defined.

Projection, Ordering, Pagination, Record Set,
and Returned Window Integrity are explicitly
defined.

Canonical Serialization is explicitly
defined.

Projection, Ordering, and Pagination
Validation are explicitly defined.

Validation Result is explicitly defined.

Failure Classifications and Failure Conditions
are explicitly defined.

Read-Only Boundary is declared.

Projection, Ordering, and Pagination
Constraints are declared.

Model Invariants are declared.

---

## Next Deliverable

CKP-004.7

Validation Query Model.
