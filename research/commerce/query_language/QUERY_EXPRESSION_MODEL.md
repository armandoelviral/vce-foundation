# Commerce Query Language Expression Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative expression model for
Commerce Query Language.

The Query Expression Model defines how
Selection, Filter, Projection, Ordering,
Pagination, and Validation Expressions are
identified, composed, validated, ordered, and
evidenced.

Query Expressions shall remain read-only and
shall not create, modify, infer, or redefine
canonical Commerce knowledge.

---

## Query Expression

A Query Expression is one immutable,
typed, and independently validatable
component of a Query Request.

Every Query Expression shall:

Possess one immutable Expression Identifier.

Declare one canonical Expression Type.

Reference one Query Identifier.

Preserve compatibility with one Query Form.

Use registered properties and values.

Produce deterministic validation evidence.

Remain immutable during Query execution.

---

## Expression Types

Permitted initial Expression Types are:

Selection Expression.

Filter Expression.

Projection Expression.

Ordering Expression.

Pagination Expression.

Validation Expression.

Unknown or private Expression Types shall be
invalid.

---

## Expression Properties

Every Query Expression shall declare:

Expression Identifier.

Expression Version.

Expression Type.

Query Identifier.

Query Form Compatibility.

Lifecycle Status.

Expression Priority.

Expression Integrity Reference.

Validation Evidence Reference.

Source Evidence Reference.

Expression-specific properties.

---

## Expression Identity

Every Query Expression shall possess one
immutable Expression Identifier.

Initial identifier forms are:

CKP-SELECTION-000001.

CKP-FILTER-000001.

CKP-PROJECTION-000001.

CKP-ORDERING-000001.

CKP-PAGINATION-000001.

CKP-VALIDATION-000001.

Expression Identifiers shall be unique within
one Query Request.

Expression identity shall remain distinct
from Expression Version.

An Expression Identifier shall not create
canonical Commerce meaning.

An Expression Identifier shall never be
reused for a different normative expression.

---

## Expression Version

Every Query Expression shall declare one
Expression Version.

Initial Expression Version

1.0

Expression Version defines the normative
structure used to interpret the expression.

Expression Version shall remain compatible
with Query Version.

An unsupported Expression Version shall cause
validation failure.

---

## Expression Lifecycle

Every Query Expression shall declare one
Lifecycle Status.

Permitted initial Lifecycle Status values are:

Draft.

Approved.

Deprecated.

Retired.

Only Approved Query Expressions may
participate in normal Query execution.

Draft expressions may be validated but shall
not participate in normal execution.

Deprecated expressions may participate only
when explicitly permitted by Execution
Context.

Retired expressions shall not participate in
Query execution.

---

## Selection Expression

A Selection Expression identifies one
registered Graph Component type targeted by a
Query Request.

Every Selection Expression shall declare:

Selection Identifier.

Selection Target.

Query Form.

Selection Scope.

Selection Validation Reference.

Permitted initial Selection Targets are:

Graph Node.

Graph Edge.

Graph Path.

Every Query Request shall reference exactly
one Selection Expression.

Selection shall not create or infer a Graph
Component.

---

## Selection Scope

Selection Scope defines the immutable Graph
boundary within which selection occurs.

Every Selection Scope shall declare:

Graph Identifier.

Graph Version.

Component Registry Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Selection Scope shall remain compatible with
the Query Request and Execution Context.

Selection shall not escape its declared Graph
Scope.

---

## Selection Compatibility

SELECT NODE shall select Graph Node.

SELECT EDGE shall select Graph Edge.

SELECT PATH shall select Graph Path.

VALIDATE EXISTS shall select the registered
Graph Component subject to existence
validation.

VALIDATE REACHABLE shall select Graph Nodes
participating in reachability validation.

VALIDATE RELATIONSHIP shall select Graph
Edges or Graph Nodes participating in direct
relationship validation.

VALIDATE PATH shall select one registered
Graph Path or the Graph Nodes and Graph Edges
required for path validation.

An incompatible Selection Target and Query
Form shall cause validation failure.

---

## Filter Expression

A Filter Expression restricts Graph
Components eligible for selection.

Every Filter Expression shall declare:

Filter Identifier.

Filter Property.

Filter Operator.

Filter Value.

Filter Value Type.

Filter Conjunction.

Filter Negation.

Filter Priority.

Filter Validation Reference.

A Query Request may reference zero or more
Filter Expressions.

---

## Filter Properties

Permitted initial Filter Properties include:

Canonical Identifier.

Relationship Identifier.

Path Identifier.

Preferred Name.

Knowledge Object Type.

Canonical Relationship Type.

Source Node Identifier.

Target Node Identifier.

Start Node Identifier.

End Node Identifier.

Directionality.

Lifecycle Status.

Ontology Membership.

Domain Membership.

Path Length.

Every Filter Property shall be registered,
canonical, and applicable to the selected
Graph Component type.

Unknown or private Filter Properties shall be
invalid.

---

## Filter Operators

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

Every Filter Operator shall be compatible
with the Filter Property and Filter Value
Type.

Unknown or private Filter Operators shall be
invalid.

---

## Filter Value

Every Filter Value shall declare one explicit
Filter Value Type.

Permitted initial Filter Value Types are:

IDENTIFIER.

TEXT.

INTEGER.

BOOLEAN.

ENUMERATION.

IDENTIFIER LIST.

TEXT LIST.

INTEGER LIST.

A Filter Value shall be compatible with its
Filter Property and Filter Operator.

A Filter Value that references canonical
knowledge shall resolve against the frozen
baselines.

Implicit type conversion shall be invalid.

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

Filter grouping shall be explicit when AND
and OR occur in the same Query Request.

Ambiguous Filter grouping shall cause
validation failure.

---

## Filter Negation

Permitted initial Filter Negation values are:

NEGATED.

NOT NEGATED.

Negation shall apply only to the Filter
Expression or explicit Filter Group in which
it is declared.

Implicit negation shall be invalid.

Double negation shall be represented
explicitly and normalized deterministically.

---

## Filter Group

A Filter Group represents one explicitly
grouped set of Filter Expressions.

Every Filter Group shall declare:

Filter Group Identifier.

Ordered Filter References.

Group Conjunction.

Group Negation.

Group Priority.

Group Validation Reference.

Filter Groups shall not contain cyclic
references.

Every referenced Filter Expression or nested
Filter Group shall exist within the same
Query Request.

---

## Filter Evaluation Order

Filter Expressions and Filter Groups shall be
evaluated in deterministic priority order.

Lower numeric priority shall be evaluated
before higher numeric priority.

Equal priority values within the same
evaluation scope shall be invalid.

Evaluation order shall preserve explicit
grouping, conjunction, and negation.

Execution strategy shall not alter normative
filter semantics.

---

## Projection Expression

A Projection Expression declares the
registered properties returned for each
selected Graph Component.

Every Projection Expression shall declare:

Projection Identifier.

Selected Component Type.

Projected Properties.

Projection Aliases.

Projection Order.

Projection Validation Reference.

A Query Request may reference zero or one
Projection Expression.

When omitted, the canonical default projection
shall apply.

---

## Projected Properties

Every Projected Property shall:

Be registered.

Be applicable to the selected Graph Component.

Preserve its canonical normative meaning.

Remain traceable to its source Graph
Component.

Projection shall not create a canonical
property.

Projection shall not change source Graph
Components.

Unknown Projected Properties shall cause
validation failure.

---

## Projection Aliases

Projection Aliases are non-normative
presentation labels.

A Projection Alias shall not:

Replace the canonical property name.

Change the normative meaning of a property.

Become a canonical identifier.

Become a canonical definition.

A Query Result and Query Evidence shall retain
the canonical property reference even when an
alias is displayed.

---

## Projection Order

Projection Order shall be explicit and
deterministic.

Every Projected Property shall possess one
unique Projection Position.

Duplicate Projection Positions shall be
invalid.

When no explicit Projection Order is declared,
canonical default property order shall apply.

Presentation layout shall not redefine
Projection Order.

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

An Ordering Expression defines one
deterministic ordering rule for Query Results.

Every Ordering Expression shall declare:

Ordering Identifier.

Ordering Property.

Ordering Direction.

Null Ordering.

Ordering Priority.

Ordering Validation Reference.

A Query Request may reference zero or more
Ordering Expressions.

---

## Ordering Property

Every Ordering Property shall:

Be registered.

Be applicable to the selected Graph
Component.

Be deterministically comparable.

Preserve canonical property meaning.

Unknown or non-comparable Ordering Properties
shall be invalid.

---

## Ordering Direction

Permitted initial Ordering Direction values
are:

ASCENDING.

DESCENDING.

Unknown Ordering Direction values shall be
invalid.

---

## Null Ordering

Permitted initial Null Ordering values are:

NULLS FIRST.

NULLS LAST.

Null Ordering shall be explicit when the
Ordering Property permits absent values.

Implicit platform-specific null ordering
shall be prohibited.

---

## Ordering Priority

Every Ordering Expression shall declare one
unique Ordering Priority within the Query
Request.

Lower numeric priority shall be applied
before higher numeric priority.

Duplicate Ordering Priority values shall be
invalid.

Ordering expressions shall be evaluated in
deterministic priority order.

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

Default ordering shall occur before
pagination.

---

## Pagination Expression

A Pagination Expression defines one
deterministic result window.

Every Pagination Expression shall declare:

Pagination Identifier.

Limit.

Offset.

Pagination Validation Reference.

A Query Request may reference zero or one
Pagination Expression.

Limit and Offset shall be non-negative
integers.

Limit shall not exceed the Maximum Result
Limit declared by Execution Context.

Pagination shall occur after filtering,
projection validation, and deterministic
ordering.

---

## Pagination Determinism

Identical Query Requests against the same
immutable Graph Version shall produce
identical page boundaries.

Offset shall identify the number of
deterministically ordered matching records
skipped.

Limit shall identify the maximum number of
records returned after Offset is applied.

Pagination shall not alter Matched Record
Count.

Pagination shall determine Returned Record
Count.

---

## Validation Expression

A Validation Expression defines one explicit
read-only graph validation operation.

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

A VALIDATE Query Form shall reference exactly
one Validation Expression.

---

## Validation Types

Permitted initial Validation Types are:

EXISTS.

REACHABLE.

RELATIONSHIP.

PATH.

EXISTS validates registration of one Graph
Component.

REACHABLE validates reachability between
registered Graph Nodes under explicit
constraints.

RELATIONSHIP validates one canonical direct
relationship.

PATH validates one registered Graph Path or
one explicitly composed continuous path.

Unknown or private Validation Types shall be
invalid.

---

## Validation Subject and Object

Every declared Subject Identifier shall
resolve to a registered Graph Component.

Every required Object Identifier shall
resolve to a registered Graph Component.

EXISTS requires one Subject Identifier and
may omit Object Identifier.

REACHABLE requires one Subject Graph Node and
one Object Graph Node.

RELATIONSHIP requires compatible Subject and
Object Graph Nodes and one canonical
Relationship Type.

PATH requires one registered Path Identifier
or compatible Start and End Graph Nodes.

---

## Validation Direction

Permitted initial Validation Direction values
are:

FORWARD.

REVERSE.

BIDIRECTIONAL.

Validation Direction shall preserve canonical
Graph Edge direction.

REVERSE validation shall require a canonical
inverse relationship where applicable.

BIDIRECTIONAL validation shall not reinterpret
a Unidirectional Graph Edge as bidirectional.

---

## Maximum Depth

Maximum Depth applies to REACHABLE and
composed PATH validation.

Maximum Depth shall be a non-negative integer.

Maximum Depth shall not exceed the Maximum
Validation Depth declared by Execution
Context.

Maximum Depth zero shall validate only the
Subject Graph Node without traversing an
edge.

EXISTS and direct RELATIONSHIP validation
shall not require traversal beyond their
canonical operation.

---

## Expression Composition

One Query Request may compose:

Exactly one Selection Expression.

Zero or more Filter Expressions.

Zero or more Filter Groups.

Zero or one Projection Expression.

Zero or more Ordering Expressions.

Zero or one Pagination Expression.

Zero or one Validation Expression, except
that VALIDATE Query Forms require exactly
one.

Every composed expression shall reference the
same Query Identifier.

Every composed expression shall remain
compatible with the same Query Form, Graph
target, baselines, and Execution Context.

---

## Expression Dependency Order

The normative expression dependency order is:

Selection Expression.

Filter Expressions and Filter Groups.

Projection Expression.

Ordering Expressions.

Pagination Expression.

Validation Expression.

Expression validation shall respect this
dependency order.

An expression shall not depend on the result
of a later dependency stage.

Circular expression dependencies shall be
invalid.

---

## Expression Immutability

Every Query Expression shall become immutable
before Query execution begins.

Expression Identifier, Version, Type,
properties, references, priorities, grouping,
and integrity references shall not change
during execution.

Any expression mutation after execution begins
shall invalidate the Query Request.

---

## Expression Integrity

Every Query Expression shall possess one
deterministic Expression Integrity Reference.

Expression Integrity shall bind:

Expression Identifier.

Expression Version.

Expression Type.

Query Identifier.

Query Form Compatibility.

Lifecycle Status.

Expression Priority.

All expression-specific normative properties.

All expression-specific references.

---

## Canonical Serialization

Every Query Expression shall possess one
deterministic canonical serialization.

Canonical serialization shall:

Preserve every normative expression property.

Use deterministic property ordering.

Use deterministic reference ordering.

Preserve explicit grouping and priority.

Exclude non-normative presentation metadata.

Produce identical output for normatively
equal Query Expressions.

Canonical serialization shall be suitable for
Expression Integrity calculation.

---

## Expression Equality

Two Query Expressions are normatively equal
when all normative Expression Properties and
expression-specific properties are equal.

Non-normative presentation metadata and
Projection Aliases shall not alter normative
expression equality.

Different Expression Identifiers shall
represent different Query Expressions.

The same Expression Identifier with different
normative properties shall be invalid.

---

## Expression Validation

Expression Validation shall verify:

Expression Identifier validity.

Expression Version support.

Expression Type validity.

Query Identifier compatibility.

Query Form compatibility.

Lifecycle compatibility.

Property registration.

Property applicability.

Operator validity.

Value type compatibility.

Explicit conjunction.

Explicit negation.

Group closure.

Priority uniqueness.

Projection validity.

Ordering comparability.

Pagination boundaries.

Validation Type compatibility.

Graph Component registration.

Maximum Depth boundary.

Baseline compatibility.

Expression immutability.

Canonical serialization.

Expression Integrity.

---

## Expression Validation Result

Every Query Expression validation shall
produce one deterministic Validation Result.

Permitted Validation Result values are:

PASS.

FAIL.

PASS means every mandatory expression rule is
satisfied.

FAIL means one or more mandatory expression
rules are violated.

Expression validation shall fail closed.

An expression with Validation Result FAIL
shall not participate in Query execution.

---

## Expression Validation Evidence

Every Query Expression validation shall
produce deterministic Expression Validation
Evidence.

Expression Validation Evidence shall declare:

Evidence Identifier.

Expression Identifier.

Expression Version.

Expression Type.

Query Identifier.

Query Form Compatibility Result.

Lifecycle Validation Result.

Property Validation Result.

Operator Validation Result.

Value Validation Result.

Grouping Validation Result.

Priority Validation Result.

Projection Validation Result.

Ordering Validation Result.

Pagination Validation Result.

Validation Expression Result.

Graph Closure Result.

Baseline Validation Result.

Immutability Validation Result.

Canonical Serialization Result.

Expression Integrity Result.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Failure Classifications

Initial Query Expression Failure
Classifications are:

EXPRESSION_IDENTITY_VIOLATION.

EXPRESSION_VERSION_VIOLATION.

EXPRESSION_TYPE_VIOLATION.

EXPRESSION_LIFECYCLE_VIOLATION.

QUERY_COMPATIBILITY_VIOLATION.

SELECTION_EXPRESSION_VIOLATION.

FILTER_PROPERTY_VIOLATION.

FILTER_OPERATOR_VIOLATION.

FILTER_VALUE_VIOLATION.

FILTER_GROUP_VIOLATION.

FILTER_PRIORITY_VIOLATION.

PROJECTION_PROPERTY_VIOLATION.

PROJECTION_ORDER_VIOLATION.

ORDERING_PROPERTY_VIOLATION.

ORDERING_PRIORITY_VIOLATION.

PAGINATION_VIOLATION.

VALIDATION_TYPE_VIOLATION.

VALIDATION_SUBJECT_VIOLATION.

VALIDATION_OBJECT_VIOLATION.

VALIDATION_DIRECTION_VIOLATION.

MAXIMUM_DEPTH_VIOLATION.

GRAPH_CLOSURE_VIOLATION.

BASELINE_VIOLATION.

IMMUTABILITY_VIOLATION.

SERIALIZATION_VIOLATION.

EXPRESSION_INTEGRITY_VIOLATION.

EVIDENCE_VIOLATION.

---

## Failure Conditions

A Query Expression shall fail validation when:

The Expression Identifier is missing,
invalid, duplicated, or improperly reused.

The Expression Version is unsupported.

The Expression Type is unknown or private.

Lifecycle Status is incompatible with
execution.

The Query Identifier cannot be resolved.

The Expression is incompatible with Query
Form.

A Selection Target is unknown or
incompatible.

A Filter Property is unknown or inapplicable.

A Filter Operator is unknown or incompatible.

A Filter Value Type is incompatible.

Filter Conjunction is missing when required.

Filter grouping is ambiguous or cyclic.

Filter Priority is duplicated.

A Projected Property is unknown or
inapplicable.

Projection Position is duplicated.

An Ordering Property is unknown,
inapplicable, or non-comparable.

Ordering Priority is duplicated.

Limit or Offset is negative.

Limit exceeds the Execution Context boundary.

A Validation Type is unknown or incompatible.

A Validation Subject is unregistered.

A required Validation Object is unregistered.

Validation Direction violates canonical edge
direction.

Maximum Depth is negative.

Maximum Depth exceeds the Execution Context
boundary.

A Graph Component reference cannot be
resolved.

A baseline reference is incompatible.

The expression is mutated after execution
begins.

Canonical serialization cannot be produced.

Expression Integrity cannot be established.

Expression Validation Evidence cannot be
produced.

---

## Read-Only Boundary

A Query Expression shall not:

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

## Query Expression Constraints

Every Query Expression shall be read-only.

Every Query Expression shall possess one
immutable Expression Identifier.

Every Query Expression shall declare one
canonical Expression Type.

Every Query Expression shall reference one
Query Identifier.

Every expression property shall be registered
and applicable.

Every expression operator shall be permitted
and compatible.

Every expression value shall possess an
explicit compatible type.

Every expression grouping and priority shall
be explicit and deterministic.

Every Query Expression shall become immutable
before execution.

Every Query Expression shall possess
deterministic canonical serialization.

Every Query Expression shall possess one
Expression Integrity Reference.

Every successful or failed validation shall
produce Expression Validation Evidence.

No invalid Query Expression shall participate
in execution.

No Query Expression shall redefine frozen
Commerce semantics.

---

## Query Expression Invariants

Read-Only Preservation.

Canonical Expression Identity.

Expression Version Preservation.

Canonical Expression Type.

Query Reference Closure.

Query Form Compatibility.

Lifecycle Compatibility.

Selection Target Validity.

Filter Property Canonicality.

Filter Operator Validity.

Filter Value Compatibility.

Explicit Filter Conjunction.

Explicit Filter Negation.

Filter Group Closure.

Deterministic Filter Priority.

Projection Property Canonicality.

Projection Order Integrity.

Ordering Property Canonicality.

Deterministic Ordering Priority.

Deterministic Default Ordering.

Pagination Boundary Integrity.

Deterministic Pagination.

Validation Type Validity.

Validation Subject Closure.

Validation Object Closure.

Direction Preservation.

Maximum Depth Enforcement.

Expression Dependency Acyclicity.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Expression Immutability.

Canonical Serialization.

Deterministic Expression Integrity.

Expression Validation Evidence Completeness.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Release Criteria

Query Expression is explicitly defined.

Expression Types are explicitly defined.

Expression Properties are explicitly defined.

Expression Identity is explicitly defined.

Expression Version is explicitly defined.

Expression Lifecycle is explicitly defined.

Selection Expression and Scope are explicitly
defined.

Selection Compatibility is explicitly
defined.

Filter Expression, Properties, Operators, and
Values are explicitly defined.

Filter Conjunction, Negation, Groups, and
Evaluation Order are explicitly defined.

Projection Expression, Aliases, Order, and
Default Projection are explicitly defined.

Ordering Expression, Property, Direction,
Null Ordering, Priority, and Default Ordering
are explicitly defined.

Pagination Expression and Determinism are
explicitly defined.

Validation Expression, Types, Subject,
Object, Direction, and Maximum Depth are
explicitly defined.

Expression Composition and Dependency Order
are explicitly defined.

Expression Immutability is explicitly
defined.

Expression Integrity is explicitly defined.

Canonical Serialization is explicitly
defined.

Expression Equality is explicitly defined.

Expression Validation and Validation Result
are explicitly defined.

Expression Validation Evidence is explicitly
defined.

Failure Classifications are explicitly
defined.

Failure Conditions are explicitly defined.

Read-Only Boundary is declared.

Query Expression Constraints are declared.

Query Expression Invariants are declared.

---

## Next Deliverable

CKP-004.5

Selection and Filter Model.
