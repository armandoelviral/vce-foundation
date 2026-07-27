# Commerce Query Language Validation Query Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative Validation Query model
for Commerce Query Language.

The Validation Query Model defines how CQL
validates the existence, reachability, direct
relationships, and registered or composed
paths of immutable Commerce Knowledge Graph
components.

Validation Queries shall remain read-only.

Validation Queries shall not create, modify,
infer, repair, or redefine canonical Commerce
knowledge.

---

## Validation Query

A Validation Query is one explicit,
deterministic, read-only request that evaluates
one canonical graph validation proposition.

Every Validation Query shall declare:

Validation Query Identifier.

Query Identifier.

Query Version.

Validation Type.

Selection Expression Reference.

Validation Expression Reference.

Execution Context Reference.

Graph Identifier.

Graph Version.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Expected Result.

Validation Query Integrity Reference.

Validation Query Evidence Reference.

---

## Validation Query Identity

Every Validation Query shall possess one
immutable Validation Query Identifier.

Example

CKP-VALIDATION-QUERY-000001

Validation Query Identifiers shall be unique
within one Execution Context.

Validation Query identity shall remain
distinct from Query Identifier and Validation
Expression Identifier.

A Validation Query Identifier shall never be
reused for a different normative Validation
Query.

A Validation Query Identifier shall not create
canonical Commerce meaning.

---

## Validation Types

Permitted initial Validation Types are:

EXISTS.

REACHABLE.

RELATIONSHIP.

PATH.

Every Validation Query shall declare exactly
one Validation Type.

Unknown or private Validation Types shall be
invalid.

Validation Type shall remain compatible with
the Query Form and Validation Expression.

---

## Query Form Compatibility

VALIDATE EXISTS shall use Validation Type
EXISTS.

VALIDATE REACHABLE shall use Validation Type
REACHABLE.

VALIDATE RELATIONSHIP shall use Validation
Type RELATIONSHIP.

VALIDATE PATH shall use Validation Type PATH.

A Validation Query whose Query Form and
Validation Type are incompatible shall fail
validation.

SELECT Query Forms shall not be interpreted
as Validation Query Forms.

---

## Validation Subject

Every Validation Query shall declare one
Validation Subject.

A Validation Subject shall declare:

Subject Identifier.

Subject Component Type.

Subject Registry Reference.

Subject Baseline Reference.

Subject Resolution Result.

Permitted Subject Component Types are:

Graph Node.

Graph Edge.

Graph Path.

The Validation Subject shall resolve to a
registered Graph Component when the
Validation Type requires registration.

An unknown or private Subject Component Type
shall be invalid.

---

## Validation Object

A Validation Query may declare one Validation
Object when required by its Validation Type.

A Validation Object shall declare:

Object Identifier.

Object Component Type.

Object Registry Reference.

Object Baseline Reference.

Object Resolution Result.

REACHABLE requires one Object Graph Node.

RELATIONSHIP requires one Object Graph Node.

PATH validation using Start and End Graph
Nodes requires one Object Graph Node.

EXISTS may omit Validation Object.

A missing required Validation Object shall
cause validation failure.

---

## Expected Result

Every Validation Query shall declare one
Expected Result.

Permitted Expected Result values are:

TRUE.

FALSE.

Expected Result represents the proposition
the caller expects the Graph to satisfy.

Expected Result shall not influence graph
evaluation.

The actual Validation Outcome shall be
calculated independently.

A mismatch between Expected Result and actual
Validation Outcome shall produce a failed
expectation result without mutating graph
semantics.

---

## Validation Outcome

Every completed Validation Query shall produce
one Validation Outcome.

Permitted Validation Outcome values are:

TRUE.

FALSE.

ERROR.

TRUE means the requested graph proposition is
satisfied.

FALSE means the requested graph proposition
is not satisfied.

ERROR means the proposition could not be
validly evaluated.

ERROR shall cause fail-closed evaluation.

Validation Outcome shall remain distinct from
Validation Status and Expected Result.

---

## Validation Status

Every Validation Query Result shall declare
one Validation Status.

Permitted Validation Status values are:

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

A terminal Validation Query Result shall not
return to Running.

---

## EXISTS Validation

EXISTS validates whether one declared Graph
Component is registered in the immutable
Graph boundary.

EXISTS shall require:

One Validation Subject.

One Subject Component Type.

One immutable Graph Identifier and Graph
Version.

One applicable Component Registry Reference.

EXISTS may validate:

Graph Node registration.

Graph Edge registration.

Graph Path registration.

EXISTS shall not require Validation Object.

EXISTS shall not perform semantic inference.

---

## EXISTS Evaluation

EXISTS shall return TRUE when:

The Subject Identifier is valid.

The Subject Registry Reference resolves.

The Subject Identifier exists in the
applicable registry.

The registered Subject belongs to the
referenced Graph Version.

EXISTS shall return FALSE when:

The Subject Identifier is structurally valid
but is not registered in the referenced Graph
Version.

EXISTS shall return ERROR when:

The Graph Manifest cannot be resolved.

The applicable registry cannot be resolved.

The Subject Component Type is unknown.

The Subject Identifier is malformed.

Baseline compatibility cannot be established.

---

## EXISTS Evidence

EXISTS validation evidence shall declare:

Subject Identifier.

Subject Component Type.

Graph Identifier.

Graph Version.

Registry Resolution Result.

Registration Lookup Result.

Graph Membership Result.

Baseline Validation Result.

Validation Outcome.

Expected Result.

Expectation Match Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## REACHABLE Validation

REACHABLE validates whether one registered
Subject Graph Node can reach one registered
Object Graph Node under explicit traversal
constraints.

REACHABLE shall require:

One Subject Graph Node.

One Object Graph Node.

One Validation Direction.

One Maximum Depth.

One Traversal Strategy.

Zero or more Relationship Type Constraints.

Zero or more Node Type Constraints.

One immutable Graph Version.

REACHABLE shall not infer undocumented Graph
Edges.

---

## Reachability Direction

Permitted Reachability Direction values are:

FORWARD.

REVERSE.

BIDIRECTIONAL.

FORWARD shall preserve stored Source-to-Target
Graph Edge direction.

REVERSE shall require canonical reverse
navigation or an applicable canonical inverse
relationship.

BIDIRECTIONAL shall inspect supported
canonical directions.

BIDIRECTIONAL shall not reinterpret a
Unidirectional Graph Edge as bidirectional.

---

## Reachability Strategy

Permitted initial Reachability Strategies are:

HIERARCHY.

SEMANTIC.

MIXED.

HIERARCHY shall use canonical hierarchy Graph
Edges only.

SEMANTIC shall use canonical non-hierarchy
Graph Edges only.

MIXED may use hierarchy and semantic Graph
Edges while preserving every canonical
Relationship Type.

Unknown or private Reachability Strategies
shall be invalid.

---

## Reachability Maximum Depth

Maximum Depth shall be a non-negative integer.

Maximum Depth shall not exceed the Maximum
Validation Depth declared by Execution
Context.

Maximum Depth zero shall validate only
whether Subject and Object identify the same
registered Graph Node.

Maximum Depth shall count traversed Graph
Edges.

Traversal shall not continue beyond Maximum
Depth.

---

## REACHABLE Evaluation

REACHABLE shall return TRUE when at least one
continuous permitted path exists from Subject
to Object within Maximum Depth.

REACHABLE shall return FALSE when Subject and
Object are registered but no permitted path
exists within Maximum Depth.

REACHABLE shall return ERROR when:

Subject or Object cannot be resolved.

Traversal constraints are invalid.

Direction cannot be preserved.

A required inverse relationship is missing.

A traversed component is unregistered.

A hierarchy cycle invalidates hierarchy
traversal.

Maximum Depth is invalid.

Deterministic traversal cannot be
established.

---

## Reachability Path Evidence

Every successful REACHABLE outcome shall
identify at least one deterministic witness
path.

A Reachability Witness Path shall declare:

Witness Path Identifier.

Subject Node Identifier.

Object Node Identifier.

Ordered Node Sequence.

Ordered Edge Sequence.

Traversal Direction.

Traversal Strategy.

Path Length.

Maximum Depth.

Path Continuity Result.

Path Integrity Reference.

When multiple witness paths satisfy the same
request, deterministic path ordering shall
select the canonical first witness unless the
Query explicitly requests all witnesses.

---

## REACHABLE Evidence

REACHABLE validation evidence shall declare:

Subject Node Identifier.

Object Node Identifier.

Traversal Direction.

Traversal Strategy.

Maximum Depth.

Applied Relationship Constraints.

Applied Node Constraints.

Visited Node Identifiers.

Traversed Edge Identifiers.

Witness Path Identifiers.

Path Continuity Result.

Direction Preservation Result.

Maximum Depth Validation Result.

Determinism Result.

Validation Outcome.

Expected Result.

Expectation Match Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## RELATIONSHIP Validation

RELATIONSHIP validates whether one explicit
canonical direct relationship exists between
one Subject Graph Node and one Object Graph
Node.

RELATIONSHIP shall require:

One Subject Graph Node.

One Object Graph Node.

One canonical Relationship Type.

One Validation Direction.

One immutable Graph Version.

RELATIONSHIP validates a direct Graph Edge.

RELATIONSHIP shall not validate transitive
reachability.

RELATIONSHIP shall not infer undocumented
relationships.

---

## Canonical Relationship Types

Permitted initial canonical Relationship
Types are:

Is A.

Part Of.

Contains.

Tracked As.

Uses.

Used By.

Sold Through.

Applies To.

An unknown or private Relationship Type shall
be invalid.

Related To shall not replace a more specific
canonical Relationship Type.

---

## RELATIONSHIP Direction

FORWARD validates an edge from Subject to
Object.

REVERSE validates a canonical reverse edge or
applicable inverse edge from Object to
Subject.

BIDIRECTIONAL validates supported canonical
directions without mutating edge semantics.

Source and Target roles shall remain explicit.

A Subject Node shall not be silently treated
as an Object Node.

An Object Node shall not be silently treated
as a Subject Node.

---

## RELATIONSHIP Evaluation

RELATIONSHIP shall return TRUE when one
registered Graph Edge matches:

Subject Node Identifier.

Object Node Identifier.

Canonical Relationship Type.

Validation Direction.

Referenced Graph Version.

RELATIONSHIP shall return FALSE when Subject
and Object are registered but no matching
direct canonical Graph Edge exists.

RELATIONSHIP shall return ERROR when:

Subject or Object is unregistered.

Relationship Type is unknown.

Validation Direction is invalid.

A required inverse relationship is
inconsistent.

The Graph Edge Registry cannot be resolved.

Baseline compatibility cannot be established.

---

## RELATIONSHIP Evidence

RELATIONSHIP validation evidence shall
declare:

Subject Node Identifier.

Object Node Identifier.

Canonical Relationship Type.

Validation Direction.

Matched Relationship Identifier.

Source Node Validation Result.

Target Node Validation Result.

Relationship Type Validation Result.

Direction Validation Result.

Inverse Relationship Validation Result.

Graph Edge Registration Result.

Validation Outcome.

Expected Result.

Expectation Match Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## PATH Validation

PATH validates one registered Graph Path or
one explicitly composed continuous path.

PATH may operate in:

REGISTERED PATH mode.

COMPOSED PATH mode.

Every PATH Validation Query shall declare
exactly one Path Validation Mode.

Unknown or private Path Validation Modes shall
be invalid.

---

## Registered Path Mode

REGISTERED PATH mode shall require:

One registered Path Identifier.

One immutable Graph Version.

One Path Registry Reference.

The registered path shall preserve:

Start Node Identifier.

End Node Identifier.

Ordered Node Sequence.

Ordered Edge Sequence.

Traversal Direction.

Path Length.

Path Continuity.

A missing or unresolved Path Identifier shall
cause validation failure.

---

## Composed Path Mode

COMPOSED PATH mode shall require:

One Start Node Identifier.

One End Node Identifier.

One Ordered Node Sequence.

One Ordered Edge Sequence.

One Validation Direction.

One declared Path Length.

Every Graph Node shall be registered.

Every Graph Edge shall be registered.

Every adjacent node pair shall be connected
by its corresponding Graph Edge.

A composed path shall not become a registered
canonical Graph Path merely by being
validated.

---

## Path Continuity

Path Continuity requires that:

Ordered Node Sequence contains exactly one
more element than Ordered Edge Sequence.

Every edge connects the corresponding adjacent
node pair.

The first node equals Start Node Identifier.

The final node equals End Node Identifier.

Declared Path Length equals the number of
ordered edges.

Edge direction remains compatible with
Validation Direction.

No implicit Graph Edge participates in the
path.

A disconnected path shall be invalid.

---

## PATH Evaluation

PATH shall return TRUE when the registered or
composed path satisfies every mandatory path
rule.

PATH shall return FALSE when all referenced
components are valid but the declared path
proposition is not satisfied.

PATH shall return ERROR when:

A required node is unregistered.

A required edge is unregistered.

The Path Identifier cannot be resolved.

Node and edge sequence lengths are
incompatible.

An adjacent node pair is disconnected.

Declared Path Length is incorrect.

Validation Direction is violated.

An implicit edge is required.

Path Integrity cannot be established.

---

## PATH Evidence

PATH validation evidence shall declare:

Path Validation Mode.

Path Identifier.

Start Node Identifier.

End Node Identifier.

Ordered Node Sequence.

Ordered Edge Sequence.

Validation Direction.

Declared Path Length.

Calculated Path Length.

Node Registration Result.

Edge Registration Result.

Sequence Cardinality Result.

Path Continuity Result.

Direction Preservation Result.

Implicit Edge Detection Result.

Path Integrity Result.

Validation Outcome.

Expected Result.

Expectation Match Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Expectation Match

Every Validation Query Result shall declare
one Expectation Match Result.

Permitted Expectation Match Result values are:

MATCH.

MISMATCH.

NOT EVALUATED.

MATCH means Expected Result equals the actual
TRUE or FALSE Validation Outcome.

MISMATCH means Expected Result differs from
the actual TRUE or FALSE Validation Outcome.

NOT EVALUATED applies when Validation Outcome
is ERROR or execution does not reach terminal
evaluation.

Expectation mismatch shall not change the
actual Validation Outcome.

---

## Validation Query Result

Every Validation Query shall produce one
Validation Query Result.

Every Validation Query Result shall declare:

Validation Query Identifier.

Query Identifier.

Graph Identifier.

Graph Version.

Validation Type.

Validation Status.

Validation Outcome.

Expected Result.

Expectation Match Result.

Subject Identifier.

Object Identifier.

Matched Component Identifiers.

Witness Path Identifiers.

Failure Classification.

Failure Reason.

Validation Query Evidence Reference.

Validation Result Integrity Reference.

---

## Validation Query Evidence

Every successful, false, failed, or cancelled
Validation Query shall produce deterministic
Validation Query Evidence.

Validation Query Evidence shall declare:

Evidence Identifier.

Validation Query Identifier.

Query Identifier.

Graph Identifier.

Graph Version.

Validation Type.

Subject Identifier.

Object Identifier.

Applied Direction.

Applied Maximum Depth.

Applied Relationship Type.

Applied Path Mode.

Registry Closure Result.

Graph Closure Result.

Baseline Validation Result.

Validation Outcome.

Expected Result.

Expectation Match Result.

Determinism Result.

Result Hash.

Validation Status.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Validation Query Integrity

Every Validation Query shall possess one
deterministic Validation Query Integrity
Reference.

Validation Query Integrity shall bind:

Validation Query Identifier.

Query Identifier.

Query Version.

Validation Type.

Subject Identifier.

Object Identifier.

Relationship Type.

Validation Direction.

Maximum Depth.

Expected Result.

Graph Identifier.

Graph Version.

Execution Context Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

---

## Validation Result Integrity

Every terminal Validation Query Result shall
possess one deterministic Validation Result
Integrity Reference.

Validation Result Integrity shall bind:

Validation Query Identifier.

Query Identifier.

Graph Identifier.

Graph Version.

Validation Type.

Validation Status.

Validation Outcome.

Expected Result.

Expectation Match Result.

Matched Component Identifiers.

Witness Path Identifiers.

Failure Classification.

Failure Reason.

Validation Query Evidence Reference.

---

## Deterministic Validation

Identical valid Validation Queries executed
against the same immutable Graph Version and
Execution Context shall produce identical
terminal normative results.

Determinism includes:

Validation Status.

Validation Outcome.

Expectation Match Result.

Matched Component Identifiers.

Witness Path selection.

Failure Classification.

Failure Reason.

Validation Result Integrity Reference.

Execution Timestamp shall not alter normative
Validation Query equality.

---

## Canonical Serialization

Validation Queries, Validation Subjects,
Validation Objects, Witness Paths, Validation
Results, and Validation Evidence shall each
possess one deterministic canonical
serialization.

Canonical serialization shall:

Preserve every normative property.

Use deterministic property ordering.

Use deterministic identifier ordering.

Preserve path ordering.

Preserve direction and Maximum Depth.

Preserve Expected Result.

Exclude non-normative presentation metadata.

Produce identical output for normatively
equal structures.

Canonical serialization shall be suitable for
integrity calculation.

---

## Validation Query Validation

Validation Query validation shall verify:

Validation Query Identifier validity.

Query Identifier resolution.

Query Version support.

Validation Type validity.

Query Form compatibility.

Subject presence and registration.

Object presence and registration when
required.

Expected Result validity.

Graph Manifest resolution.

Graph Version compatibility.

Execution Context compatibility.

Direction validity.

Relationship Type validity.

Maximum Depth validity.

Path Validation Mode validity.

Path sequence validity.

Registry closure.

Graph closure.

Baseline compatibility.

Canonical serialization.

Validation Query Integrity.

---

## Validation Execution Order

The normative Validation Query execution
order is:

Validation Query Manifest Validation.

Baseline Validation.

Graph Manifest Resolution.

Query Form Validation.

Validation Type Validation.

Subject Resolution.

Object Resolution when required.

Direction Validation.

Relationship Type Validation when required.

Maximum Depth Validation when required.

Path Structure Validation when required.

Validation Evaluation.

Expected Result Comparison.

Validation Result Construction.

Evidence Construction.

Integrity Construction.

Terminal Status Validation.

Execution strategy shall not alter this
normative order.

---

## Failure Classifications

Initial Validation Query Failure
Classifications are:

VALIDATION_QUERY_IDENTITY_VIOLATION.

VALIDATION_TYPE_VIOLATION.

QUERY_FORM_COMPATIBILITY_VIOLATION.

SUBJECT_VIOLATION.

OBJECT_VIOLATION.

EXPECTED_RESULT_VIOLATION.

GRAPH_TARGET_VIOLATION.

REGISTRY_CLOSURE_VIOLATION.

GRAPH_CLOSURE_VIOLATION.

DIRECTION_VIOLATION.

RELATIONSHIP_TYPE_VIOLATION.

INVERSE_RELATIONSHIP_VIOLATION.

MAXIMUM_DEPTH_VIOLATION.

TRAVERSAL_STRATEGY_VIOLATION.

REACHABILITY_VIOLATION.

PATH_MODE_VIOLATION.

PATH_REGISTRATION_VIOLATION.

PATH_SEQUENCE_VIOLATION.

PATH_CONTINUITY_VIOLATION.

PATH_LENGTH_VIOLATION.

IMPLICIT_EDGE_VIOLATION.

BASELINE_VIOLATION.

DETERMINISM_VIOLATION.

SERIALIZATION_VIOLATION.

VALIDATION_INTEGRITY_VIOLATION.

RESULT_INTEGRITY_VIOLATION.

EVIDENCE_VIOLATION.

---

## Failure Conditions

A Validation Query shall fail when:

The Validation Query Identifier is missing,
invalid, duplicated, or improperly reused.

The Query Identifier cannot be resolved.

The Query Form and Validation Type are
incompatible.

The Validation Type is unknown or private.

Expected Result is missing or invalid.

The Validation Subject is missing, malformed,
or unresolved.

A required Validation Object is missing,
malformed, or unresolved.

The Graph Manifest cannot be resolved.

The Graph Version is incompatible.

Execution Context targets a different Graph.

Validation Direction is unknown or invalid.

A required Relationship Type is missing,
unknown, or private.

A required inverse relationship is missing or
inconsistent.

Maximum Depth is negative.

Maximum Depth exceeds the Execution Context
boundary.

Traversal Strategy is unknown or
incompatible.

A required registry cannot be resolved.

A referenced Graph Component is unregistered.

A registered Path Identifier cannot be
resolved.

Path Validation Mode is unknown.

Node and edge sequence cardinalities are
incompatible.

A path contains a disconnected node pair.

Declared Path Length is incorrect.

An implicit Graph Edge is required.

Deterministic evaluation cannot be
established.

Canonical serialization cannot be produced.

Validation Query Integrity cannot be
established.

Validation Result Integrity cannot be
established.

Validation Query Evidence cannot be produced.

---

## Read-Only Boundary

Validation Queries shall not:

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Register a composed Graph Path.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Component.

Repair a missing Graph Component.

Repair a broken inverse relationship.

Repair a disconnected path.

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

## Validation Query Constraints

Every Validation Query shall be read-only.

Every Validation Query shall declare exactly
one canonical Validation Type.

Every Validation Query shall reference one
immutable Graph Version.

Every Validation Query shall declare one
Validation Subject.

Every required Validation Object shall be
explicit.

Every Expected Result shall be explicit.

Every registered Graph Component reference
shall be resolvable.

Every direction shall preserve canonical
Graph semantics.

Every Maximum Depth shall remain within
Execution Context boundaries.

Every witness path shall be continuous.

Every Validation Outcome shall be calculated
independently from Expected Result.

Every successful, false, failed, or cancelled
Validation Query shall produce deterministic
evidence.

No Validation Query shall infer an
undocumented Graph Component or relationship.

No invalid Validation Query shall execute.

No Validation Query shall redefine frozen
Commerce semantics.

---

## Validation Query Invariants

Read-Only Preservation.

Canonical Validation Query Identity.

Canonical Validation Type.

Query Form Compatibility.

Immutable Graph Target.

Subject Registration Closure.

Object Registration Closure.

Expected Result Independence.

Validation Outcome Integrity.

Expectation Match Integrity.

EXISTS Registry Closure.

Reachability Direction Preservation.

Reachability Maximum Depth Enforcement.

Reachability Witness Continuity.

Canonical Relationship Type Preservation.

Direct Relationship Semantics.

Inverse Relationship Consistency.

Path Mode Validity.

Registered Path Closure.

Composed Path Non-Registration.

Path Sequence Cardinality.

Path Continuity.

Path Length Integrity.

No Implicit Edges.

Deterministic Witness Selection.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Validation Query Integrity.

Validation Result Integrity.

Canonical Serialization.

Validation Evidence Completeness.

Deterministic Validation.

Fail-Closed Evaluation.

Semantic Closure.

Traceability Closure.

---

## Release Criteria

Validation Query is explicitly defined.

Validation Query Identity is explicitly
defined.

Validation Types and Query Form compatibility
are explicitly defined.

Validation Subject and Object are explicitly
defined.

Expected Result, Validation Outcome, and
Validation Status are explicitly defined.

EXISTS validation, evaluation, and evidence
are explicitly defined.

REACHABLE validation, direction, strategy,
depth, evaluation, witness paths, and evidence
are explicitly defined.

RELATIONSHIP validation, canonical types,
direction, evaluation, and evidence are
explicitly defined.

PATH validation, registered and composed
modes, continuity, evaluation, and evidence
are explicitly defined.

Expectation Match is explicitly defined.

Validation Query Result and Evidence are
explicitly defined.

Validation Query and Result Integrity are
explicitly defined.

Deterministic Validation is explicitly
defined.

Canonical Serialization is explicitly
defined.

Validation Query Validation and Execution
Order are explicitly defined.

Failure Classifications and Failure Conditions
are explicitly defined.

Read-Only Boundary is declared.

Validation Query Constraints are declared.

Validation Query Invariants are declared.

---

## Next Deliverable

CKP-004.8

Initial Executable Queries.
