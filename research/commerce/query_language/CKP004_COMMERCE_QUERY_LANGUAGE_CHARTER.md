# CKP-004

Title

Commerce Query Language

Abbreviation

CQL

Version

1.0

Status

Draft

---

## Vision

Establish a canonical, declarative,
deterministic, traceable, and auditable
language for querying immutable Commerce
Knowledge Graphs.

Commerce Query Language shall allow consumers
to request registered Commerce knowledge
without modifying, extending, or redefining
the queried Graph.

---

## Mission

Define a technology-independent query
language over the frozen Commerce Knowledge
Graph.

CQL shall transform explicit Query Requests
into deterministic Query Results and Query
Evidence.

CQL shall preserve canonical identity,
relationship direction, graph boundaries,
baseline compatibility, and semantic closure.

---

## Inputs

HAS Foundation 1.0 LTS.

Specification Runtime 1.0.

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

CKP-003 Commerce Knowledge Graph 1.0.

Graph Manifest.

Graph Nodes.

Graph Edges.

Registered Graph Paths.

Traversal Model.

Graph Consistency Evidence.

---

## Outputs

Commerce Query Language Charter.

Query Structure Model.

Query Request Model.

Query Expression Model.

Selection Model.

Filter Model.

Projection Model.

Ordering Model.

Pagination Model.

Query Result Model.

Query Evidence Model.

Initial Executable Queries.

Query Consistency Audit.

Commerce Query Language Freeze.

---

## Language Boundary

CQL is a read-only declarative query
language.

CQL shall describe what registered Commerce
knowledge is requested.

CQL shall not prescribe storage technology,
graph database vendor, traversal algorithm,
or physical execution strategy.

CQL shall not mutate the queried Graph.

---

## Initial Query Capabilities

The initial Commerce Query Language shall
support:

Node Selection.

Edge Selection.

Path Selection.

Relationship-Type Filtering.

Node-Type Filtering.

Canonical Identifier Filtering.

Preferred Name Filtering.

Domain Membership Filtering.

Lifecycle Status Filtering.

Source Node Filtering.

Target Node Filtering.

Direction Filtering.

Exact Match Filtering.

Deterministic Ordering.

Result Limiting.

Result Offset.

Projection.

Existence Validation.

Reachability Validation.

Direct Relationship Validation.

Registered Path Validation.

---

## Initial Query Forms

The initial canonical query forms are:

SELECT NODE.

SELECT EDGE.

SELECT PATH.

VALIDATE EXISTS.

VALIDATE REACHABLE.

VALIDATE RELATIONSHIP.

VALIDATE PATH.

Every Query Request shall select exactly one
canonical Query Form.

---

## Query Request Responsibilities

Every Query Request shall declare:

Query Identifier.

Query Version.

Graph Identifier.

Graph Version.

Query Form.

Selection Target.

Filter Expression.

Projection Expression.

Ordering Expression.

Limit.

Offset.

Execution Context.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

---

## Query Identity

Every Query Request shall possess one
immutable Query Identifier.

Example

CKP-QUERY-000001

Query Identifiers shall be unique within one
execution context.

Query identity shall remain distinct from
Query Version.

Query Identifiers shall not create canonical
Commerce meaning.

---

## Selection Responsibilities

Selection shall operate only over registered
Graph Components.

A Selection Target may be:

Graph Node.

Graph Edge.

Graph Path.

Selection shall not create a Graph Component.

Selection shall not infer an undocumented
Graph Component.

---

## Filter Responsibilities

Every Filter Expression shall use explicit
canonical properties.

Initial filterable properties include:

Canonical Identifier.

Relationship Identifier.

Preferred Name.

Knowledge Object Type.

Canonical Relationship Type.

Source Node Identifier.

Target Node Identifier.

Directionality.

Lifecycle Status.

Ontology Membership.

Domain Membership.

Path Identifier.

Path Length.

Every filter value shall be validated against
the frozen baselines when applicable.

---

## Projection Responsibilities

Projection defines which registered
properties appear in a Query Result.

Projection shall not create canonical
properties.

Projection shall not rename a canonical
property into a different normative meaning.

Omitted properties shall remain available in
Query Evidence when required for
traceability.

---

## Ordering Responsibilities

Query Results shall use deterministic
ordering.

When no explicit ordering is declared:

Graph Nodes shall be ordered by Canonical
Identifier.

Graph Edges shall be ordered by Relationship
Identifier.

Graph Paths shall be ordered by Path
Identifier.

Explicit ordering shall use registered and
comparable properties only.

Presentation order shall not redefine
canonical identity or semantic direction.

---

## Pagination Responsibilities

CQL shall support deterministic Limit and
Offset behavior.

Limit shall declare the maximum number of
returned records.

Offset shall declare the number of ordered
records skipped before result collection.

Pagination shall occur after filtering and
deterministic ordering.

Negative Limit or Offset values shall be
invalid.

Identical paginated queries against the same
immutable Graph Version shall produce
identical page boundaries.

---

## Query Result Responsibilities

Every Query Result shall declare:

Query Identifier.

Graph Identifier.

Graph Version.

Query Status.

Selected Component Type.

Matched Record Count.

Returned Record Count.

Ordered Results.

Limit.

Offset.

Failure Reason.

Query Evidence Reference.

Result Integrity Reference.

---

## Query Status

Permitted initial Query Status values are:

Not Executed.

Running.

Completed.

Failed.

Cancelled.

Completed, Failed, and Cancelled are terminal
statuses.

A terminal Query Result shall not return to
Running.

---

## Query Evidence Responsibilities

Every Query execution shall produce
deterministic Query Evidence.

Query Evidence shall identify:

Evidence Identifier.

Query Identifier.

Graph Identifier.

Graph Version.

Query Form.

Selection Target.

Applied Filters.

Applied Projection.

Applied Ordering.

Applied Limit.

Applied Offset.

Matched Component Identifiers.

Returned Component Identifiers.

Baseline Validation Result.

Graph Closure Result.

Direction Validation Result.

Determinism Result.

Result Hash.

Validation Result.

Failure Reason.

---

## Failed Query Evidence

A failed Query shall still produce Query
Evidence.

Failure evidence shall identify:

The failed validation rule.

The invalid query component.

The execution stage.

The deterministic Failure Reason.

No failed Query shall omit evidence.

---

## Query Determinism

Identical valid Query Requests executed
against the same immutable Graph Version and
Execution Context shall produce identical
terminal Query Results.

Determinism includes:

Query Status.

Matched Record Count.

Returned Record Count.

Ordered Results.

Failure Reason.

Result Integrity Reference.

Execution Timestamp shall not alter normative
Query Result equality.

---

## Query Validation

Query validation shall occur before, during,
and after execution.

Pre-Query Validation shall verify:

Query completeness.

Query Identifier validity.

Graph Manifest resolution.

Graph Version compatibility.

Query Form validity.

Selection Target validity.

Filter validity.

Projection validity.

Ordering validity.

Limit validity.

Offset validity.

Baseline compatibility.

During-Query Validation shall verify:

Registered Node Closure.

Registered Edge Closure.

Registered Path Closure.

Direction Preservation.

Filter enforcement.

Projection enforcement.

Deterministic ordering.

Pagination enforcement.

Post-Query Validation shall verify:

Result count consistency.

Returned component registration.

Ordering consistency.

Evidence completeness.

Result Integrity.

Terminal status consistency.

---

## Read-Only Semantics

CQL shall be read-only.

A Query shall not:

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

Modify a frozen baseline.

Create undocumented semantic meaning.

---

## Non-Goals

CKP-004 shall not:

- modify HAS Foundation 1.0 LTS;

- modify Specification Runtime 1.0;

- modify CKP-001 Vocabulary 1.0;

- modify CKP-002 Ontology 1.0;

- modify CKP-003 Knowledge Graph 1.0;

- implement a graph database;

- select a graph database vendor;

- require SQL;

- require SPARQL;

- require Cypher;

- require GraphQL;

- define a network transport;

- define an HTTP API;

- define a user interface;

- implement authorization;

- implement commercial decision logic;

- infer undocumented Commerce semantics;

- create machine-learning behavior.

---

## Language Principles

Read-only before extensible.

Canonical identity before aliases.

Explicit selection before inference.

Explicit filters before implicit assumptions.

Deterministic ordering before pagination.

Validation before execution.

Evidence for success and failure.

Query semantics shall remain independent of
storage technology.

---

## Language Invariants

Read-Only Preservation.

Canonical Identity Preservation.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Registered Node Closure.

Registered Edge Closure.

Registered Path Closure.

Direction Preservation.

Inverse Relationship Consistency.

Selection Target Validity.

Filter Canonicality.

Projection Canonicality.

Deterministic Ordering.

Deterministic Pagination.

Deterministic Query Result.

Query Evidence Completeness.

Result Integrity.

Semantic Closure.

Traceability Closure.

Fail-Closed Evaluation.

---

## Failure Conditions

A Query shall fail when:

The Query Request is incomplete.

The Query Identifier is invalid.

The Graph Manifest cannot be resolved.

The Graph Version is incompatible.

The Query Form is unknown.

The Selection Target is unknown.

A filter property is unknown.

A filter value violates a frozen baseline.

A projection property is unknown.

An ordering property is unknown.

Limit is negative.

Offset is negative.

A selected Graph Node is unregistered.

A selected Graph Edge is unregistered.

A selected Graph Path is unregistered.

Canonical direction is violated.

Deterministic ordering cannot be established.

Query Evidence cannot be produced.

Result Integrity cannot be established.

A Query attempts to mutate the Graph.

A Query attempts to redefine frozen Commerce
semantics.

---

## Frozen Baseline Boundary

HAS Foundation 1.0 LTS remains frozen.

Specification Runtime 1.0 remains frozen.

CKP-001 Canonical Commerce Vocabulary 1.0
remains frozen.

CKP-002 Commerce Ontology 1.0 remains frozen.

CKP-003 Commerce Knowledge Graph 1.0 remains
frozen.

CQL shall consume these immutable baselines
without modifying their normative behavior,
canonical identity, assertions, graph
structure, or semantics.

---

## Success Criteria

Every Query Request references one immutable
Graph Version.

Every Query Form is canonical.

Every Selection Target is registered.

Every filter uses a registered property.

Every projection uses a registered property.

Every ordering operation is deterministic.

Every pagination boundary is deterministic.

Every returned Graph Component is registered.

Every successful or failed Query produces
Query Evidence.

No Query mutates the Graph.

No Query privately redefines frozen Commerce
semantics.

Query consistency is executable and
auditable.

---

## Deliverables

Commerce Query Language Charter.

Query Structure Model.

Query Request Model.

Query Expression Model.

Selection Model.

Filter Model.

Projection Model.

Ordering and Pagination Model.

Query Result Model.

Query Evidence Model.

Initial Executable Queries.

Query Consistency Audit.

Commerce Query Language Freeze.

---

## Release Boundary

CKP-004 shall remain specification-first.

No parser, interpreter, compiler, storage
adapter, network interface, or query runtime
shall be implemented before the normative
query models and executable specification
contracts are complete.

---

## Next Deliverable

CKP-004.2

Query Structure Model.
