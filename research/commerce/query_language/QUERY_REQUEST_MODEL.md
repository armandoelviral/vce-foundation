# Commerce Query Language Request Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative Query Request model for
Commerce Query Language.

A Query Request represents one explicit,
immutable, read-only instruction against one
frozen Commerce Knowledge Graph version.

The Query Request Model defines request
identity, composition, validation,
compatibility, lifecycle, integrity, and
evidence requirements.

---

## Query Request

Every Query Request shall represent exactly
one canonical CQL operation.

Every Query Request shall reference exactly
one immutable Commerce Knowledge Graph
version.

Every Query Request shall be read-only.

Every Query Request shall be complete before
execution begins.

A Query Request shall not become a source of
canonical Commerce meaning.

---

## Query Request Properties

Every Query Request shall declare:

Query Identifier.

Query Version.

Lifecycle Status.

Graph Identifier.

Graph Version.

Query Form.

Selection Expression Reference.

Filter Expression References.

Projection Expression Reference.

Ordering Expression References.

Pagination Expression Reference.

Validation Expression Reference.

Execution Context Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Query Integrity Reference.

Source Evidence Reference.

---

## Query Identity

Every Query Request shall possess one
immutable Query Identifier.

Example

CKP-QUERY-000001

The Query Identifier shall uniquely identify
one normative Query Request within one
Execution Context.

Query identity shall remain distinct from
Query Version.

A Query Identifier shall not encode canonical
Commerce semantics.

A Query Identifier shall never be reused for
a different normative Query Request.

---

## Query Version

Every Query Request shall declare one Query
Version.

Initial Query Version

1.0

Query Version identifies the normative
request structure used to interpret the
Query Request.

Query Version shall not replace Graph Version.

Query Version shall not modify the meaning of
a frozen Graph Component.

An unsupported Query Version shall cause
validation failure.

---

## Lifecycle Status

Every Query Request shall declare one
Lifecycle Status.

Permitted initial Lifecycle Status values are:

Draft.

Approved.

Deprecated.

Retired.

Only Approved Query Requests may enter normal
execution.

Draft Query Requests may be validated but
shall not enter normal execution.

Deprecated Query Requests may execute only
when explicitly permitted by Execution
Context.

Retired Query Requests shall not execute.

---

## Graph Target

Every Query Request shall reference one
Graph Identifier and one Graph Version.

Initial Graph Identifier

CKP-GRAPH-000001

Initial Graph Version

1.0

The referenced Graph Manifest shall be
resolvable.

The Graph Version shall remain immutable
during execution.

A Query Request shall not switch Graph
Identifier or Graph Version after execution
begins.

---

## Query Form

Every Query Request shall declare exactly one
canonical Query Form.

Permitted initial Query Forms are:

SELECT NODE.

SELECT EDGE.

SELECT PATH.

VALIDATE EXISTS.

VALIDATE REACHABLE.

VALIDATE RELATIONSHIP.

VALIDATE PATH.

Query Form shall determine the mandatory
request components.

Unknown or private Query Forms shall be
invalid.

---

## Query Form Compatibility

SELECT NODE shall reference a Graph Node
Selection Expression.

SELECT EDGE shall reference a Graph Edge
Selection Expression.

SELECT PATH shall reference a Graph Path
Selection Expression.

VALIDATE EXISTS shall reference one
Validation Expression of type EXISTS.

VALIDATE REACHABLE shall reference one
Validation Expression of type REACHABLE.

VALIDATE RELATIONSHIP shall reference one
Validation Expression of type RELATIONSHIP.

VALIDATE PATH shall reference one Validation
Expression of type PATH.

A Query Request with an incompatible Query
Form and expression combination shall be
invalid.

---

## Selection Expression Reference

Every Query Request shall reference exactly
one Selection Expression.

The Selection Expression shall resolve to one
registered Selection Target.

Permitted Selection Targets are:

Graph Node.

Graph Edge.

Graph Path.

The Selection Target shall remain compatible
with the declared Query Form.

A missing or unresolved Selection Expression
shall cause validation failure.

---

## Filter Expression References

A Query Request may reference zero or more
Filter Expressions.

Every referenced Filter Expression shall
possess one unique Filter Identifier.

Every Filter Expression shall use:

One canonical Filter Property.

One permitted Filter Operator.

One compatible Filter Value.

One explicit Filter Conjunction when
required.

One explicit Filter Negation state.

Duplicate Filter Identifiers shall be
prohibited.

Presentation order shall not replace explicit
Filter Conjunction.

---

## Filter Evaluation Order

Filter Expressions shall be evaluated in
deterministic Filter Identifier order unless
an explicit canonical Filter Priority is
declared.

Equivalent Filter Expression sets shall
produce equivalent selection semantics.

Evaluation order shall not change the
normative meaning of explicit AND and OR
conjunctions.

---

## Projection Expression Reference

A Query Request may reference one Projection
Expression.

When Projection Expression is omitted, the
canonical default projection for the selected
Graph Component shall apply.

The Projection Expression shall reference
registered properties only.

Projection shall not create or rename
canonical properties.

Projection shall not alter source Graph
Components.

---

## Ordering Expression References

A Query Request may reference zero or more
Ordering Expressions.

Every Ordering Expression shall possess one
unique Ordering Identifier.

Every Ordering Expression shall reference one
registered and comparable property.

Multiple Ordering Expressions shall declare
unique Ordering Priority values.

Duplicate Ordering Priority values shall be
invalid.

When no Ordering Expression is referenced,
canonical default ordering shall apply.

---

## Pagination Expression Reference

A Query Request may reference one Pagination
Expression.

Pagination Expression shall declare:

Limit.

Offset.

Limit and Offset shall be non-negative
integers.

Limit shall not exceed the Maximum Result
Limit declared by Execution Context.

Pagination shall apply after filtering and
deterministic ordering.

A Query Request shall not reference more than
one Pagination Expression.

---

## Validation Expression Reference

A VALIDATE Query Form shall reference exactly
one Validation Expression.

A SELECT Query Form may omit Validation
Expression.

A Validation Expression shall reference
registered Graph Components.

Validation Type shall remain compatible with
Query Form.

Maximum Depth shall not exceed the Maximum
Validation Depth declared by Execution
Context.

Validation Expression shall not create
semantic inference.

---

## Execution Context Reference

Every Query Request shall reference exactly
one immutable Execution Context.

Execution Context shall resolve:

Execution Identifier.

Graph Identifier.

Graph Version.

Vocabulary Baseline.

Ontology Baseline.

Graph Baseline.

Node Registry Reference.

Edge Registry Reference.

Path Registry Reference.

Maximum Result Limit.

Maximum Validation Depth.

The Query Request and Execution Context shall
reference the same Graph Identifier and Graph
Version.

---

## Baseline References

Every Query Request shall reference:

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

CKP-003 Commerce Knowledge Graph 1.0.

Every baseline reference shall be explicit,
resolvable, immutable, and auditable.

The Query Request and Execution Context shall
reference compatible baselines.

An unknown or incompatible baseline shall
cause validation failure.

---

## Request Completeness

A Query Request is complete when all
mandatory properties for its Query Form are
present and resolvable.

Mandatory properties for every Query Request
are:

Query Identifier.

Query Version.

Lifecycle Status.

Graph Identifier.

Graph Version.

Query Form.

Selection Expression Reference.

Execution Context Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Query Integrity Reference.

Additional mandatory components shall be
determined by Query Form.

An incomplete Query Request shall not enter
execution.

---

## Request Immutability

A Query Request shall become immutable before
execution begins.

The following properties shall not change
during execution:

Query Identifier.

Query Version.

Graph Identifier.

Graph Version.

Query Form.

Selection Expression Reference.

Filter Expression References.

Projection Expression Reference.

Ordering Expression References.

Pagination Expression Reference.

Validation Expression Reference.

Execution Context Reference.

Baseline References.

Query Integrity Reference.

Any mutation after execution begins shall
invalidate the Query Request.

---

## Query Integrity

Every Query Request shall declare one
deterministic Query Integrity Reference.

Query Integrity shall bind:

Query Identifier.

Query Version.

Lifecycle Status.

Graph Identifier.

Graph Version.

Query Form.

Selection Expression Reference.

Filter Expression References.

Projection Expression Reference.

Ordering Expression References.

Pagination Expression Reference.

Validation Expression Reference.

Execution Context Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

---

## Canonical Serialization

A Query Request shall possess one
deterministic canonical serialization.

Canonical serialization shall:

Preserve every normative Query Request
property.

Use deterministic property ordering.

Use deterministic expression reference
ordering.

Exclude non-normative presentation metadata.

Produce identical output for normatively
equal Query Requests.

Canonical serialization shall be suitable for
Query Integrity calculation.

---

## Request Equality

Two Query Requests are normatively equal when
all normative Query Request Properties are
equal.

Non-normative presentation metadata shall not
affect Query Request equality.

Different Query Identifiers shall represent
different Query Requests.

Two Query Requests with the same Query
Identifier but different normative properties
shall be invalid.

---

## Request Validation

Query Request validation shall occur before
execution.

Request Validation shall verify:

Query Identifier validity.

Query Version support.

Lifecycle Status compatibility.

Graph Manifest resolution.

Graph Version compatibility.

Query Form validity.

Query Form compatibility.

Selection Expression resolution.

Filter Expression resolution.

Projection Expression resolution.

Ordering Expression resolution.

Pagination Expression resolution.

Validation Expression resolution.

Execution Context resolution.

Baseline compatibility.

Request completeness.

Request immutability.

Canonical serialization.

Query Integrity.

---

## Validation Result

Every Query Request validation shall produce
one deterministic Validation Result.

Permitted Validation Result values are:

PASS.

FAIL.

PASS means every mandatory Query Request rule
is satisfied.

FAIL means one or more mandatory Query Request
rules are violated.

Validation shall fail closed.

A Query Request with Validation Result FAIL
shall not enter execution.

---

## Request Validation Evidence

Every Query Request validation shall produce
deterministic Request Validation Evidence.

Request Validation Evidence shall declare:

Evidence Identifier.

Query Identifier.

Query Version.

Graph Identifier.

Graph Version.

Query Form.

Lifecycle Validation Result.

Graph Resolution Result.

Query Form Validation Result.

Selection Validation Result.

Filter Validation Result.

Projection Validation Result.

Ordering Validation Result.

Pagination Validation Result.

Validation Expression Result.

Execution Context Validation Result.

Baseline Validation Result.

Completeness Validation Result.

Immutability Validation Result.

Canonical Serialization Result.

Query Integrity Result.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Failure Classifications

Initial Query Request Failure
Classifications are:

QUERY_IDENTITY_VIOLATION.

QUERY_VERSION_VIOLATION.

LIFECYCLE_VIOLATION.

GRAPH_TARGET_VIOLATION.

QUERY_FORM_VIOLATION.

SELECTION_VIOLATION.

FILTER_VIOLATION.

PROJECTION_VIOLATION.

ORDERING_VIOLATION.

PAGINATION_VIOLATION.

VALIDATION_EXPRESSION_VIOLATION.

EXECUTION_CONTEXT_VIOLATION.

BASELINE_VIOLATION.

COMPLETENESS_VIOLATION.

IMMUTABILITY_VIOLATION.

SERIALIZATION_VIOLATION.

QUERY_INTEGRITY_VIOLATION.

EVIDENCE_VIOLATION.

---

## Failure Conditions

A Query Request shall fail validation when:

The Query Identifier is missing or invalid.

The Query Identifier is reused improperly.

The Query Version is missing or unsupported.

Lifecycle Status is missing or incompatible
with execution.

The Graph Identifier is missing or invalid.

The Graph Version is missing or incompatible.

The Graph Manifest cannot be resolved.

The Query Form is missing, unknown, or
private.

The Query Form is incompatible with its
expressions.

The Selection Expression is missing or
unresolved.

A Filter Expression is invalid.

A duplicate Filter Identifier exists.

A Projection Expression is invalid.

An Ordering Expression is invalid.

A duplicate Ordering Identifier exists.

A duplicate Ordering Priority exists.

A Pagination Expression is invalid.

More than one Pagination Expression is
referenced.

A required Validation Expression is missing.

Validation Type is incompatible with Query
Form.

Maximum Validation Depth is exceeded.

Execution Context cannot be resolved.

Execution Context targets a different Graph.

A baseline reference is missing, unknown, or
incompatible.

The Query Request is incomplete.

The Query Request is mutated after execution
begins.

Canonical serialization cannot be produced.

Query Integrity cannot be established.

Request Validation Evidence cannot be
produced.

---

## Read-Only Boundary

A Query Request shall not:

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Component.

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

## Query Request Constraints

Every Query Request shall be read-only.

Every Query Request shall reference exactly
one immutable Graph Version.

Every Query Request shall declare exactly one
canonical Query Form.

Every Query Request shall reference exactly
one Selection Expression.

Every Query Request shall reference exactly
one Execution Context.

Every Query Request shall preserve compatible
frozen baselines.

Every Query Request shall become immutable
before execution.

Every Query Request shall possess
deterministic canonical serialization.

Every Query Request shall possess one Query
Integrity Reference.

Every successful or failed validation shall
produce Request Validation Evidence.

No incomplete Query Request shall execute.

No invalid Query Request shall execute.

No Query Request shall redefine frozen
Commerce semantics.

---

## Query Request Invariants

Read-Only Preservation.

Canonical Query Identity.

Query Version Preservation.

Lifecycle Compatibility.

Immutable Graph Target.

Canonical Query Form.

Query Form Compatibility.

Selection Reference Closure.

Filter Reference Closure.

Projection Reference Closure.

Ordering Reference Closure.

Pagination Reference Closure.

Validation Reference Closure.

Execution Context Closure.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Request Completeness.

Request Immutability.

Canonical Serialization.

Deterministic Query Integrity.

Request Validation Evidence Completeness.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Release Criteria

Query Request is explicitly defined.

Query Request Properties are explicitly
defined.

Query Identity is explicitly defined.

Query Version is explicitly defined.

Lifecycle Status behavior is explicitly
defined.

Graph Target is explicitly defined.

Query Forms and compatibility are explicitly
defined.

Selection Expression Reference is explicitly
defined.

Filter Expression References and evaluation
order are explicitly defined.

Projection Expression Reference is explicitly
defined.

Ordering Expression References are
explicitly defined.

Pagination Expression Reference is explicitly
defined.

Validation Expression Reference is explicitly
defined.

Execution Context Reference is explicitly
defined.

Baseline References are explicitly defined.

Request Completeness is explicitly defined.

Request Immutability is explicitly defined.

Query Integrity is explicitly defined.

Canonical Serialization is explicitly
defined.

Request Equality is explicitly defined.

Request Validation is explicitly defined.

Validation Result is explicitly defined.

Request Validation Evidence is explicitly
defined.

Failure Classifications are explicitly
defined.

Failure Conditions are explicitly defined.

Read-Only Boundary is declared.

Query Request Constraints are declared.

Query Request Invariants are declared.

---

## Next Deliverable

CKP-004.4

Query Expression Model.
