# Commerce Query Language Structure Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative structure of a Commerce
Query Language Query.

The Query Structure Model defines how
read-only Query Requests are identified,
composed, validated, executed, represented,
and evidenced without modifying the frozen
Commerce Knowledge Graph.

---

## Query Components

Query Manifest.

Query Request.

Query Form.

Selection Expression.

Filter Expression.

Projection Expression.

Ordering Expression.

Pagination Expression.

Validation Expression.

Execution Context.

Query Result.

Query Evidence.

Query Constraint.

Query Integrity Reference.

---

## Query Manifest

A Query Manifest identifies one complete CQL
Query Request.

Every Query Manifest shall declare:

Query Identifier.

Query Version.

Lifecycle Status.

Graph Identifier.

Graph Version.

Query Form.

Selection Expression Reference.

Filter Expression Reference.

Projection Expression Reference.

Ordering Expression Reference.

Pagination Expression Reference.

Validation Expression Reference.

Execution Context Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Query Integrity Reference.

---

## Query Request

A Query Request represents one explicit,
read-only request against one immutable
Commerce Knowledge Graph version.

Every Query Request shall contain exactly one
Query Manifest.

Every Query Request shall select exactly one
canonical Query Form.

Every Query Request shall reference one
immutable Graph Identifier and Graph Version.

A Query Request shall not modify its Graph
target.

---

## Query Identity

Every Query Request shall possess one
immutable Query Identifier.

Example

CKP-QUERY-000001

Query identity shall remain distinct from
Query Version.

Query Identifiers shall be unique within one
Execution Context.

A Query Identifier shall not create canonical
Commerce meaning.

Query Identifiers shall never be reused for a
different normative Query Request.

---

## Query Form

Query Form declares the canonical operation
requested by CQL.

Permitted initial Query Forms are:

SELECT NODE.

SELECT EDGE.

SELECT PATH.

VALIDATE EXISTS.

VALIDATE REACHABLE.

VALIDATE RELATIONSHIP.

VALIDATE PATH.

Every Query Request shall declare exactly one
Query Form.

Unknown or private Query Forms shall be
invalid.

---

## Selection Expression

Selection Expression identifies the
registered Graph Component type targeted by
the Query.

Permitted initial Selection Targets are:

Graph Node.

Graph Edge.

Graph Path.

Selection Expression shall remain compatible
with the declared Query Form.

SELECT NODE shall target Graph Node.

SELECT EDGE shall target Graph Edge.

SELECT PATH shall target Graph Path.

Validation Query Forms shall target the Graph
Component required by their validation
operation.

Selection shall not create or infer a Graph
Component.

---

## Filter Expression

Filter Expression restricts the Graph
Components eligible for selection.

Every Filter Expression shall declare:

Filter Identifier.

Filter Property.

Filter Operator.

Filter Value.

Filter Value Type.

Filter Conjunction.

Filter Negation.

Filter Validation Reference.

A Query Request may contain zero or more
Filter Expressions.

Every Filter Property shall be registered and
canonical.

Every Filter Value shall be compatible with
its Filter Property.

---

## Initial Filter Operators

Permitted initial Filter Operators are:

EQUALS.

NOT EQUALS.

IN.

NOT IN.

EXISTS.

NOT EXISTS.

GREATER THAN.

GREATER THAN OR EQUAL.

LESS THAN.

LESS THAN OR EQUAL.

Unknown or private Filter Operators shall be
invalid.

---

## Filter Conjunction

Permitted initial Filter Conjunction values
are:

AND.

OR.

A Query containing multiple Filter
Expressions shall declare explicit
conjunction.

Conjunction shall not be inferred from
presentation order.

---

## Filter Negation

Filter Negation shall be explicit.

Permitted initial values are:

NEGATED.

NOT NEGATED.

Negation shall apply only to the Filter
Expression in which it is declared.

Implicit negation shall be invalid.

---

## Projection Expression

Projection Expression declares the
registered properties returned for each
selected Graph Component.

Every Projection Expression shall declare:

Projection Identifier.

Projected Properties.

Projection Order.

Projection Validation Reference.

A Query Request may omit Projection
Expression only when the canonical default
projection is used.

Projection shall not create a canonical
property.

Projection shall not rename a property into a
different normative meaning.

Projection shall preserve traceability to the
source Graph Component.

---

## Default Projection

The default Graph Node projection includes:

Canonical Identifier.

Preferred Name.

Knowledge Object Type.

Lifecycle Status.

Ontology Membership.

Domain Membership.

The default Graph Edge projection includes:

Relationship Identifier.

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

Directionality.

Lifecycle Status.

The default Graph Path projection includes:

Path Identifier.

Start Node Identifier.

End Node Identifier.

Ordered Node Sequence.

Ordered Edge Sequence.

Path Length.

---

## Ordering Expression

Ordering Expression defines deterministic
result order.

Every Ordering Expression shall declare:

Ordering Identifier.

Ordering Property.

Ordering Direction.

Null Ordering.

Ordering Priority.

Ordering Validation Reference.

Permitted initial Ordering Direction values
are:

ASCENDING.

DESCENDING.

Permitted initial Null Ordering values are:

NULLS FIRST.

NULLS LAST.

Every Ordering Property shall be registered
and comparable.

---

## Default Ordering

When no Ordering Expression is declared:

Graph Nodes shall be ordered by Canonical
Identifier in ascending order.

Graph Edges shall be ordered by Relationship
Identifier in ascending order.

Graph Paths shall be ordered by Path
Identifier in ascending order.

Default ordering shall be deterministic.

Presentation order shall not replace
normative result ordering.

---

## Pagination Expression

Pagination Expression defines a deterministic
window over ordered Query Results.

Every Pagination Expression shall declare:

Pagination Identifier.

Limit.

Offset.

Pagination Validation Reference.

Limit shall be a non-negative integer.

Offset shall be a non-negative integer.

Pagination shall occur after filtering,
projection validation, and deterministic
ordering.

Identical Query Requests against the same
immutable Graph Version shall produce
identical page boundaries.

---

## Validation Expression

Validation Expression defines one explicit
graph validation operation.

Every Validation Expression shall declare:

Validation Identifier.

Validation Type.

Subject Identifier.

Object Identifier.

Relationship Type.

Direction.

Maximum Depth.

Expected Result.

Validation Evidence Reference.

Validation Expression is mandatory for
VALIDATE Query Forms.

Validation Expression shall not create
semantic inference.

---

## Initial Validation Types

Permitted initial Validation Types are:

EXISTS.

REACHABLE.

RELATIONSHIP.

PATH.

EXISTS validates registration of one Graph
Component.

REACHABLE validates an explicit registered
or traversable path between Graph Nodes.

RELATIONSHIP validates one canonical direct
relationship.

PATH validates one registered Graph Path.

---

## Execution Context

Execution Context defines the immutable
boundary of one Query execution.

Every Execution Context shall declare:

Execution Identifier.

Graph Identifier.

Graph Version.

Vocabulary Baseline.

Ontology Baseline.

Graph Baseline.

Node Registry Reference.

Edge Registry Reference.

Path Registry Reference.

Execution Timestamp.

Maximum Result Limit.

Maximum Validation Depth.

Execution Context shall remain immutable
during Query execution.

---

## Baseline References

Every Query Request shall reference:

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

CKP-003 Commerce Knowledge Graph 1.0.

Every baseline reference shall be explicit,
resolvable, immutable, and auditable.

A Query Request with an incompatible baseline
shall be invalid.

---

## Query Result

Query Result represents the deterministic
terminal outcome of one Query Request.

Every Query Result shall declare:

Query Identifier.

Query Version.

Graph Identifier.

Graph Version.

Query Status.

Query Form.

Selected Component Type.

Matched Record Count.

Returned Record Count.

Ordered Results.

Limit.

Offset.

Validation Outcome.

Failure Classification.

Failure Reason.

Query Evidence Reference.

Result Integrity Reference.

---

## Query Status

Permitted Query Status values are:

Not Executed.

Running.

Completed.

Failed.

Cancelled.

Permitted status transitions are:

Not Executed to Running.

Running to Completed.

Running to Failed.

Running to Cancelled.

Completed, Failed, and Cancelled are terminal
statuses.

A terminal Query Result shall not return to
Running.

---

## Query Evidence

Query Evidence demonstrates how one Query
Result was produced.

Every Query Evidence record shall declare:

Evidence Identifier.

Query Identifier.

Query Version.

Graph Identifier.

Graph Version.

Query Form.

Selection Target.

Applied Filters.

Applied Projection.

Applied Ordering.

Applied Pagination.

Applied Validation.

Matched Component Identifiers.

Returned Component Identifiers.

Vocabulary Validation Result.

Ontology Validation Result.

Graph Validation Result.

Direction Validation Result.

Ordering Validation Result.

Pagination Validation Result.

Result Count Validation.

Determinism Result.

Result Hash.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Query Integrity

Every Query Request shall possess one
deterministic Query Integrity Reference.

Query Integrity shall bind:

Query Identifier.

Query Version.

Graph Identifier.

Graph Version.

Query Form.

Selection Expression.

Filter Expressions.

Projection Expression.

Ordering Expression.

Pagination Expression.

Validation Expression.

Execution Context.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

---

## Result Integrity

Every terminal Query Result shall possess one
deterministic Result Integrity Reference.

Result Integrity shall bind:

Query Identifier.

Query Version.

Graph Identifier.

Graph Version.

Query Status.

Matched Record Count.

Returned Record Count.

Ordered Results.

Limit.

Offset.

Validation Outcome.

Failure Classification.

Failure Reason.

Query Evidence Reference.

---

## Deterministic Evaluation Order

CQL shall evaluate a Query Request in this
normative order:

Query Manifest Validation.

Baseline Validation.

Graph Resolution.

Query Form Validation.

Selection Validation.

Filter Validation.

Filter Evaluation.

Projection Validation.

Ordering Validation.

Deterministic Ordering.

Pagination Validation.

Pagination Application.

Validation Expression Evaluation.

Result Construction.

Evidence Construction.

Integrity Construction.

Terminal Status Validation.

Execution strategy shall not alter this
normative evaluation order.

---

## Query Constraints

Every Query Request shall be read-only.

Every Query Request shall reference one
immutable Graph Version.

Every Query Request shall declare one
canonical Query Form.

Every Selection Target shall be registered.

Every Filter Property shall be canonical.

Every Filter Operator shall be permitted.

Every Projection Property shall be
registered.

Every Ordering Property shall be registered
and comparable.

Every Pagination value shall be
non-negative.

Every Validation Expression shall use
registered Graph Components.

Every successful or failed Query shall
produce Query Evidence.

No Query shall create a Graph Component.

No Query shall modify a Graph Component.

No Query shall create undocumented semantic
meaning.

No Query shall redefine a frozen baseline.

---

## Query Invariants

Read-Only Preservation.

Canonical Query Identity.

Query Version Preservation.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Selection Target Validity.

Filter Property Canonicality.

Filter Operator Validity.

Filter Value Compatibility.

Projection Property Canonicality.

Ordering Property Canonicality.

Deterministic Ordering.

Deterministic Pagination.

Validation Expression Validity.

Registered Node Closure.

Registered Edge Closure.

Registered Path Closure.

Direction Preservation.

Query Evidence Completeness.

Query Integrity.

Result Integrity.

Deterministic Query Result.

Semantic Closure.

Traceability Closure.

Fail-Closed Evaluation.

---

## Failure Conditions

A Query Request shall fail validation when:

The Query Manifest is missing.

The Query Identifier is missing or invalid.

The Query Version is missing or invalid.

The Graph Identifier is missing or invalid.

The Graph Version is missing or incompatible.

The Query Form is unknown or private.

The Selection Target is unknown or
incompatible with the Query Form.

A Filter Property is unknown.

A Filter Operator is unknown.

A Filter Value is incompatible with its
property.

Filter Conjunction is missing when required.

A Projection Property is unknown.

An Ordering Property is unknown or not
comparable.

Limit is negative.

Offset is negative.

Maximum Result Limit is exceeded.

A Validation Type is unknown.

A Validation subject is unregistered.

A Validation object is unregistered.

Maximum Validation Depth is exceeded.

A baseline reference cannot be resolved.

Deterministic ordering cannot be established.

Query Evidence cannot be produced.

Query Integrity cannot be established.

Result Integrity cannot be established.

The Query attempts to mutate the Graph.

The Query attempts to redefine frozen
Commerce semantics.

---

## Read-Only Boundary

Query evaluation shall not:

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Node.

Modify a Graph Edge.

Modify a Graph Path.

Modify a Canonical Identifier.

Modify a Preferred Name.

Modify a Canonical Definition.

Modify a Relationship Type.

Modify directionality.

Modify an inverse relationship.

Modify CKP-001.

Modify CKP-002.

Modify CKP-003.

---

## Release Criteria

Query Components are explicitly defined.

Query Manifest structure is explicitly
defined.

Query Request structure is explicitly
defined.

Query Identity is explicitly defined.

Query Forms are explicitly defined.

Selection Expression is explicitly defined.

Filter Expression is explicitly defined.

Filter Operators are explicitly defined.

Filter Conjunction and Negation are
explicitly defined.

Projection Expression and Default Projection
are explicitly defined.

Ordering Expression and Default Ordering are
explicitly defined.

Pagination Expression is explicitly defined.

Validation Expression and Validation Types
are explicitly defined.

Execution Context is explicitly defined.

Baseline References are explicitly defined.

Query Result is explicitly defined.

Query Status and transitions are explicitly
defined.

Query Evidence is explicitly defined.

Query Integrity is explicitly defined.

Result Integrity is explicitly defined.

Deterministic Evaluation Order is explicitly
defined.

Query Constraints are declared.

Query Invariants are declared.

Failure Conditions are declared.

Read-Only Boundary is declared.

---

## Next Deliverable

CKP-004.3

Query Request Model.
