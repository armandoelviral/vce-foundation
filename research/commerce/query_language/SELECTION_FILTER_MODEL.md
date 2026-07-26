# Commerce Query Language Selection and Filter Model

Version

1.0

Status

Draft

---

## Purpose

Define the normative Selection and Filter
model for Commerce Query Language.

The Selection and Filter Model defines how a
Query Request identifies one registered Graph
Component type and restricts eligible Graph
Components through explicit, canonical,
typed, deterministic, and auditable Filter
Expressions.

Selection and filtering shall remain
read-only.

Selection and filtering shall not create,
modify, infer, or redefine canonical Commerce
knowledge.

---

## Selection and Filter Pipeline

The normative Selection and Filter pipeline
is:

Query Form Validation.

Selection Expression Resolution.

Selection Scope Validation.

Candidate Set Resolution.

Filter Reference Resolution.

Filter Validation.

Filter Group Validation.

Deterministic Filter Ordering.

Filter Evaluation.

Eligible Component Set Construction.

Selection Evidence Construction.

Filter Evidence Construction.

Integrity Construction.

A later stage shall not execute before all
mandatory earlier stages have passed.

---

## Selection Expression

A Selection Expression identifies exactly one
registered Graph Component type targeted by a
Query Request.

Every Query Request shall reference exactly
one Selection Expression.

Every Selection Expression shall declare:

Selection Identifier.

Expression Version.

Query Identifier.

Query Form.

Selection Target.

Selection Scope Reference.

Selection Cardinality.

Lifecycle Status.

Selection Integrity Reference.

Selection Validation Evidence Reference.

Source Evidence Reference.

---

## Selection Identity

Every Selection Expression shall possess one
immutable Selection Identifier.

Example

CKP-SELECTION-000001

Selection Identifiers shall be unique within
one Query Request.

Selection identity shall remain distinct from
Expression Version.

A Selection Identifier shall never be reused
for a different normative Selection
Expression.

A Selection Identifier shall not create
canonical Commerce meaning.

---

## Selection Targets

Permitted initial Selection Targets are:

Graph Node.

Graph Edge.

Graph Path.

Unknown or private Selection Targets shall be
invalid.

Selection Target shall remain compatible with
Query Form.

---

## Query Form and Selection Compatibility

SELECT NODE shall select Graph Node.

SELECT EDGE shall select Graph Edge.

SELECT PATH shall select Graph Path.

VALIDATE EXISTS shall select the registered
Graph Component subject to existence
validation.

VALIDATE REACHABLE shall select Graph Nodes
participating in reachability validation.

VALIDATE RELATIONSHIP shall select Graph Nodes
or Graph Edges participating in direct
relationship validation.

VALIDATE PATH shall select one registered
Graph Path or the registered Graph Components
required for explicit path validation.

A Query Form and Selection Target mismatch
shall cause validation failure.

---

## Selection Scope

Selection Scope defines the immutable Graph
boundary from which candidate Graph
Components may be selected.

Every Selection Scope shall declare:

Selection Scope Identifier.

Graph Identifier.

Graph Version.

Selection Target.

Component Registry Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Execution Context Reference.

Selection Scope Integrity Reference.

Selection Scope shall reference one immutable
Graph Version.

Selection Scope shall remain compatible with
the Query Request and Execution Context.

Selection shall not escape its declared
Selection Scope.

---

## Candidate Set

Candidate Set is the deterministic set of all
registered Graph Components compatible with
the Selection Target and Selection Scope
before Filter evaluation.

Every Candidate Set shall declare:

Candidate Set Identifier.

Selection Identifier.

Selection Target.

Graph Identifier.

Graph Version.

Ordered Candidate Identifiers.

Candidate Count.

Candidate Set Integrity Reference.

Every candidate Graph Component shall be
registered in the referenced Graph Manifest.

Candidate Set ordering shall use canonical
default ordering.

Graph Nodes shall be ordered by Canonical
Identifier.

Graph Edges shall be ordered by Relationship
Identifier.

Graph Paths shall be ordered by Path
Identifier.

No unregistered or implicit Graph Component
may enter the Candidate Set.

---

## Selection Cardinality

Selection Cardinality defines the permitted
number of eligible Graph Components.

Permitted initial Selection Cardinality values
are:

ZERO OR MORE.

ONE OR MORE.

EXACTLY ONE.

ZERO OR ONE.

Selection Cardinality shall be explicit.

Selection Cardinality shall be evaluated
after all Filter Expressions have been
applied.

A Selection Result that violates declared
Selection Cardinality shall fail validation.

---

## Selection Result

Selection Result represents the deterministic
outcome of Selection Scope resolution and
Filter evaluation.

Every Selection Result shall declare:

Selection Identifier.

Query Identifier.

Selection Target.

Candidate Count.

Eligible Component Count.

Ordered Eligible Component Identifiers.

Selection Cardinality.

Cardinality Validation Result.

Filter Set Reference.

Selection Status.

Failure Classification.

Failure Reason.

Selection Evidence Reference.

Selection Result Integrity Reference.

---

## Selection Status

Permitted initial Selection Status values are:

Not Evaluated.

Evaluated.

Failed.

Cancelled.

Evaluated, Failed, and Cancelled are terminal
Selection Status values.

A terminal Selection Result shall not return
to Not Evaluated.

---

## Filter Expression

A Filter Expression defines one explicit
predicate applied to Graph Components in the
Candidate Set.

Every Filter Expression shall declare:

Filter Identifier.

Expression Version.

Query Identifier.

Selection Identifier.

Filter Property.

Filter Operator.

Filter Value.

Filter Value Type.

Filter Conjunction.

Filter Negation.

Filter Priority.

Filter Group Reference.

Lifecycle Status.

Filter Integrity Reference.

Filter Validation Evidence Reference.

Source Evidence Reference.

---

## Filter Identity

Every Filter Expression shall possess one
immutable Filter Identifier.

Example

CKP-FILTER-000001

Filter Identifiers shall be unique within one
Query Request.

Filter identity shall remain distinct from
Expression Version.

A Filter Identifier shall never be reused for
a different normative Filter Expression.

Duplicate Filter Identifiers shall be
invalid.

---

## Filter Property Registry

Every Filter Property shall be registered,
canonical, and applicable to the selected
Graph Component type.

Permitted initial Graph Node Filter Properties
are:

Canonical Identifier.

Preferred Name.

Knowledge Object Type.

Lifecycle Status.

Ontology Membership.

Domain Membership.

Registry Reference.

Permitted initial Graph Edge Filter Properties
are:

Relationship Identifier.

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

Directionality.

Inverse Relationship Reference.

Lifecycle Status.

Ontology Assertion Reference.

Permitted initial Graph Path Filter Properties
are:

Path Identifier.

Start Node Identifier.

End Node Identifier.

Ordered Node Sequence.

Ordered Edge Sequence.

Traversal Direction.

Path Length.

Validation Result.

Unknown or private Filter Properties shall be
invalid.

A registered property that is inapplicable to
the Selection Target shall be invalid.

---

## Canonical Identifier Filtering

Canonical Identifier filtering applies only
to Graph Nodes.

Canonical Identifier shall use the IDENTIFIER
Filter Value Type.

Canonical Identifier shall support:

EQUALS.

NOT EQUALS.

IN.

NOT IN.

EXISTS.

NOT EXISTS.

A Canonical Identifier Filter Value shall
resolve to a registered Canonical Commerce
Term when the operator requires a concrete
identifier.

---

## Relationship Identifier Filtering

Relationship Identifier filtering applies
only to Graph Edges.

Relationship Identifier shall use the
IDENTIFIER Filter Value Type.

Relationship Identifier shall support:

EQUALS.

NOT EQUALS.

IN.

NOT IN.

EXISTS.

NOT EXISTS.

A Relationship Identifier Filter Value shall
resolve to one registered Graph Edge when the
operator requires a concrete identifier.

---

## Path Identifier Filtering

Path Identifier filtering applies only to
Graph Paths.

Path Identifier shall use the IDENTIFIER
Filter Value Type.

Path Identifier shall support:

EQUALS.

NOT EQUALS.

IN.

NOT IN.

EXISTS.

NOT EXISTS.

A Path Identifier Filter Value shall resolve
to one registered Graph Path when the
operator requires a concrete identifier.

---

## Preferred Name Filtering

Preferred Name filtering applies only to
Graph Nodes.

Preferred Name shall use the TEXT Filter Value
Type.

Preferred Name filtering shall compare the
canonical Preferred Name.

A display label or Projection Alias shall not
replace the canonical Preferred Name during
Filter evaluation.

Initial Preferred Name comparison shall be
exact and case-sensitive.

Normalization rules shall not be inferred.

---

## Knowledge Object Type Filtering

Knowledge Object Type filtering applies only
to Graph Nodes.

Knowledge Object Type shall use the
ENUMERATION Filter Value Type.

Initial Graph Nodes use:

TERM.

Unknown or private Knowledge Object Types
shall be invalid.

---

## Relationship Type Filtering

Canonical Relationship Type filtering applies
only to Graph Edges.

Canonical Relationship Type shall use the
ENUMERATION Filter Value Type.

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

Related To shall not replace a more specific
canonical Relationship Type.

Unknown or private Relationship Types shall
be invalid.

---

## Source and Target Filtering

Source Node Identifier and Target Node
Identifier filtering apply only to Graph
Edges.

Both properties shall use the IDENTIFIER
Filter Value Type.

Every concrete Source or Target Node Filter
Value shall resolve to a registered Graph
Node.

Source and Target filtering shall preserve
canonical Graph Edge direction.

A Source filter shall not be interpreted as a
Target filter.

A Target filter shall not be interpreted as a
Source filter.

---

## Start and End Filtering

Start Node Identifier and End Node Identifier
filtering apply only to Graph Paths.

Both properties shall use the IDENTIFIER
Filter Value Type.

Every concrete Start or End Node Filter Value
shall resolve to a registered Graph Node.

Start and End filtering shall preserve the
registered direction of the Graph Path.

---

## Directionality Filtering

Directionality filtering applies to Graph
Edges.

Directionality shall use the ENUMERATION
Filter Value Type.

Permitted initial Directionality values are:

Unidirectional.

Inverse-Paired.

Unknown or private Directionality values shall
be invalid.

Directionality filtering shall not mutate or
reinterpret the stored Graph Edge.

---

## Traversal Direction Filtering

Traversal Direction filtering applies to
Graph Paths.

Traversal Direction shall use the ENUMERATION
Filter Value Type.

Permitted initial Traversal Direction values
are:

Forward.

Reverse.

Bidirectional.

Traversal Direction filtering shall preserve
the registered Graph Path semantics.

---

## Lifecycle Status Filtering

Lifecycle Status filtering applies to Graph
Nodes and Graph Edges.

Lifecycle Status shall use the ENUMERATION
Filter Value Type.

Permitted initial Lifecycle Status values are:

Draft.

Approved.

Deprecated.

Retired.

A Retired Graph Component shall not be
selected unless explicitly permitted by
Execution Context and Filter Expression.

---

## Ontology Membership Filtering

Ontology Membership filtering applies to
Graph Nodes.

Ontology Membership shall use the ENUMERATION
or TEXT Filter Value Type according to the
registered ontology membership representation.

Every concrete Ontology Membership Filter
Value shall resolve against CKP-002 Commerce
Ontology 1.0.

Filtering shall not infer new Ontology
Membership.

---

## Domain Membership Filtering

Domain Membership filtering applies to Graph
Nodes.

Domain Membership shall use the ENUMERATION
or TEXT Filter Value Type according to the
registered domain representation.

Every concrete Domain Membership Filter Value
shall resolve against the frozen Commerce
Ontology.

Filtering shall not redefine or infer Domain
Membership.

---

## Path Length Filtering

Path Length filtering applies only to Graph
Paths.

Path Length shall use the INTEGER Filter Value
Type.

Path Length shall support:

EQUALS.

NOT EQUALS.

IN.

NOT IN.

GREATER THAN.

GREATER THAN OR EQUAL.

LESS THAN.

LESS THAN OR EQUAL.

Path Length values shall be non-negative
integers.

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

## Operator Semantics

EQUALS returns true when the registered
property value is normatively equal to the
Filter Value.

NOT EQUALS returns true when the registered
property value is not normatively equal to
the Filter Value.

IN returns true when the registered property
value belongs to the explicit Filter Value
collection.

NOT IN returns true when the registered
property value does not belong to the
explicit Filter Value collection.

EXISTS returns true when the registered
property is present.

NOT EXISTS returns true when the registered
property is absent.

GREATER THAN, GREATER THAN OR EQUAL, LESS
THAN, and LESS THAN OR EQUAL require a
deterministically comparable property and
value.

Operator semantics shall not depend on
storage technology.

---

## Filter Value Types

Permitted initial Filter Value Types are:

IDENTIFIER.

TEXT.

INTEGER.

BOOLEAN.

ENUMERATION.

IDENTIFIER LIST.

TEXT LIST.

INTEGER LIST.

Every Filter Value shall declare exactly one
Filter Value Type.

A scalar operator shall not consume a list
value unless its normative operator permits a
list.

IN and NOT IN shall consume an applicable
list value.

Implicit type conversion shall be invalid.

---

## Filter Value Validation

Filter Value validation shall verify:

Value presence when required.

Value absence for EXISTS and NOT EXISTS.

Value Type validity.

Property and Value Type compatibility.

Operator and Value Type compatibility.

Canonical identifier resolution.

Enumeration membership.

Integer boundary validity.

List member type consistency.

List determinism.

Baseline compatibility.

A Filter Value that references canonical
knowledge shall resolve against the frozen
baselines.

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

AND requires every participating predicate to
evaluate true.

OR requires at least one participating
predicate to evaluate true.

---

## Filter Negation

Permitted initial Filter Negation values are:

NEGATED.

NOT NEGATED.

Negation shall apply only to the Filter
Expression or Filter Group in which it is
declared.

Implicit negation shall be invalid.

Double negation shall be represented
explicitly.

Double negation shall normalize
deterministically without changing canonical
Filter meaning.

---

## Filter Group

A Filter Group represents one explicit,
ordered, and independently validatable
composition of Filter Expressions or nested
Filter Groups.

Every Filter Group shall declare:

Filter Group Identifier.

Query Identifier.

Selection Identifier.

Ordered Filter References.

Ordered Nested Group References.

Group Conjunction.

Group Negation.

Group Priority.

Lifecycle Status.

Group Integrity Reference.

Group Validation Evidence Reference.

---

## Filter Group Identity

Every Filter Group shall possess one immutable
Filter Group Identifier.

Example

CKP-FILTER-GROUP-000001

Filter Group Identifiers shall be unique
within one Query Request.

A Filter Group Identifier shall never be
reused for a different normative Filter
Group.

---

## Filter Group Closure

Every Filter Expression and nested Filter
Group referenced by a Filter Group shall
exist within the same Query Request.

Every referenced Filter Expression shall
reference the same Selection Identifier.

Every nested Filter Group shall reference the
same Selection Identifier.

A Filter Group shall not reference itself.

Filter Groups shall not contain direct or
indirect cyclic references.

An orphan Filter Expression or Filter Group
shall not participate in Filter evaluation.

---

## Filter Priority

Every Filter Expression and Filter Group
shall declare one Filter Priority within its
evaluation scope.

Lower numeric priority shall be evaluated
before higher numeric priority.

Equal priority values within the same
evaluation scope shall be invalid.

Filter Priority shall not replace explicit
Filter Conjunction or grouping.

---

## Deterministic Filter Ordering

Filter Expressions shall be ordered by:

Filter Priority.

Then Filter Identifier.

Filter Groups shall be ordered by:

Group Priority.

Then Filter Group Identifier.

Canonical identifier ordering shall act only
as a deterministic tie-breaker where equal
priority is explicitly permitted by a future
version.

The initial model prohibits equal priority
within one evaluation scope.

Identical Filter Sets shall produce identical
evaluation order.

---

## Filter Set

A Filter Set is the complete, closed, and
ordered collection of Filter Expressions and
Filter Groups referenced by one Query
Request.

Every Filter Set shall declare:

Filter Set Identifier.

Query Identifier.

Selection Identifier.

Ordered Root Filter References.

Ordered Root Group References.

Filter Count.

Filter Group Count.

Filter Set Integrity Reference.

Filter Set Validation Evidence Reference.

A Query Request with no filters shall declare
an empty Filter Set or an explicit absence of
Filter Set according to Query Request
serialization rules.

An empty Filter Set shall preserve the entire
Candidate Set as eligible.

---

## Filter Evaluation

Every candidate Graph Component shall be
evaluated against the complete valid Filter
Set.

Filter evaluation shall:

Preserve Candidate Set ordering.

Apply explicit grouping.

Apply explicit conjunction.

Apply explicit negation.

Respect deterministic priority.

Use canonical registered property values.

Reject invalid properties, operators, values,
groups, or references.

Produce one deterministic predicate result
for every evaluated Filter Expression.

Filter evaluation shall not modify Candidate
Set components.

---

## Filter Evaluation Result

Every Filter Expression evaluation shall
produce one Filter Evaluation Result.

Every Filter Evaluation Result shall declare:

Filter Identifier.

Candidate Component Identifier.

Property Resolution Result.

Operator Evaluation Result.

Negation Application Result.

Predicate Result.

Failure Classification.

Failure Reason.

Filter Evaluation Evidence Reference.

Filter Evaluation Integrity Reference.

Predicate Result values are:

TRUE.

FALSE.

ERROR.

ERROR shall cause fail-closed Filter Set
evaluation.

---

## Filter Group Evaluation Result

Every Filter Group evaluation shall produce
one Filter Group Evaluation Result.

Every Filter Group Evaluation Result shall
declare:

Filter Group Identifier.

Candidate Component Identifier.

Ordered Child Results.

Conjunction Result.

Negation Application Result.

Group Predicate Result.

Failure Classification.

Failure Reason.

Group Evaluation Evidence Reference.

Group Evaluation Integrity Reference.

---

## Eligible Component Set

Eligible Component Set is the deterministic
ordered subset of Candidate Set components
that satisfy the complete Filter Set.

Every Eligible Component Set shall declare:

Eligible Set Identifier.

Candidate Set Identifier.

Filter Set Identifier.

Selection Identifier.

Ordered Eligible Component Identifiers.

Eligible Component Count.

Eligible Set Integrity Reference.

Every eligible component shall originate from
the Candidate Set.

No Filter evaluation shall create an eligible
component not present in the Candidate Set.

Eligible Component Set ordering shall preserve
Candidate Set canonical order unless a later
Ordering Expression explicitly defines result
ordering.

---

## Selection Evidence

Every Selection evaluation shall produce
deterministic Selection Evidence.

Selection Evidence shall declare:

Evidence Identifier.

Selection Identifier.

Query Identifier.

Query Form.

Selection Target.

Selection Scope Identifier.

Graph Identifier.

Graph Version.

Candidate Set Identifier.

Candidate Count.

Eligible Set Identifier.

Eligible Component Count.

Cardinality Validation Result.

Registry Closure Result.

Baseline Validation Result.

Selection Integrity Result.

Selection Result Integrity.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Filter Validation Evidence

Every Filter Expression validation shall
produce deterministic Filter Validation
Evidence.

Filter Validation Evidence shall declare:

Evidence Identifier.

Filter Identifier.

Query Identifier.

Selection Identifier.

Filter Property.

Filter Operator.

Filter Value Type.

Property Applicability Result.

Operator Compatibility Result.

Value Compatibility Result.

Conjunction Validation Result.

Negation Validation Result.

Priority Validation Result.

Group Closure Result.

Baseline Validation Result.

Filter Integrity Result.

Validation Result.

Failure Classification.

Failure Reason.

Evidence Integrity Reference.

---

## Filter Evaluation Evidence

Every Filter Expression evaluation shall
produce deterministic Filter Evaluation
Evidence.

Filter Evaluation Evidence shall declare:

Evidence Identifier.

Filter Identifier.

Candidate Component Identifier.

Resolved Property Value.

Filter Operator.

Filter Value.

Filter Value Type.

Raw Predicate Result.

Negation Application Result.

Final Predicate Result.

Evaluation Order.

Evaluation Integrity Reference.

Failure Classification.

Failure Reason.

---

## Selection Integrity

Every Selection Expression shall possess one
deterministic Selection Integrity Reference.

Selection Integrity shall bind:

Selection Identifier.

Expression Version.

Query Identifier.

Query Form.

Selection Target.

Selection Scope Reference.

Selection Cardinality.

Lifecycle Status.

---

## Filter Integrity

Every Filter Expression shall possess one
deterministic Filter Integrity Reference.

Filter Integrity shall bind:

Filter Identifier.

Expression Version.

Query Identifier.

Selection Identifier.

Filter Property.

Filter Operator.

Filter Value.

Filter Value Type.

Filter Conjunction.

Filter Negation.

Filter Priority.

Filter Group Reference.

Lifecycle Status.

---

## Filter Group Integrity

Every Filter Group shall possess one
deterministic Group Integrity Reference.

Group Integrity shall bind:

Filter Group Identifier.

Query Identifier.

Selection Identifier.

Ordered Filter References.

Ordered Nested Group References.

Group Conjunction.

Group Negation.

Group Priority.

Lifecycle Status.

---

## Canonical Serialization

Selection Expressions, Filter Expressions,
Filter Groups, Candidate Sets, Filter Sets,
and Eligible Component Sets shall each possess
one deterministic canonical serialization.

Canonical serialization shall:

Preserve every normative property.

Use deterministic property ordering.

Use deterministic reference ordering.

Preserve grouping, conjunction, negation, and
priority.

Preserve canonical identifiers.

Exclude non-normative presentation metadata.

Produce identical output for normatively
equal structures.

Canonical serialization shall be suitable for
integrity calculation.

---

## Selection Validation

Selection Validation shall verify:

Selection Identifier validity.

Expression Version support.

Query Identifier resolution.

Query Form validity.

Query Form and Selection Target compatibility.

Selection Target validity.

Selection Scope resolution.

Graph Manifest resolution.

Component Registry resolution.

Baseline compatibility.

Selection Cardinality validity.

Lifecycle compatibility.

Selection immutability.

Canonical serialization.

Selection Integrity.

---

## Filter Validation

Filter Validation shall verify:

Filter Identifier validity.

Expression Version support.

Query Identifier resolution.

Selection Identifier resolution.

Filter Property registration.

Filter Property applicability.

Filter Operator validity.

Operator and Property compatibility.

Filter Value Type validity.

Filter Value compatibility.

Canonical identifier resolution.

Enumeration membership.

Explicit conjunction.

Explicit negation.

Filter Priority uniqueness.

Filter Group resolution.

Filter Group closure.

Baseline compatibility.

Filter immutability.

Canonical serialization.

Filter Integrity.

---

## Filter Set Validation

Filter Set Validation shall verify:

Filter Set Identifier validity.

Query Identifier resolution.

Selection Identifier resolution.

Filter reference closure.

Filter Group reference closure.

No orphan Filter Expression exists.

No orphan Filter Group exists.

No cyclic Filter Group reference exists.

Priority uniqueness.

Deterministic ordering.

Canonical serialization.

Filter Set Integrity.

---

## Validation Result

Selection, Filter, and Filter Set validation
shall each produce one deterministic
Validation Result.

Permitted Validation Result values are:

PASS.

FAIL.

PASS means every mandatory validation rule is
satisfied.

FAIL means one or more mandatory validation
rules are violated.

Validation shall fail closed.

A Selection Expression, Filter Expression, or
Filter Set with Validation Result FAIL shall
not participate in Query execution.

---

## Failure Classifications

Initial Selection and Filter Failure
Classifications are:

SELECTION_IDENTITY_VIOLATION.

SELECTION_TARGET_VIOLATION.

SELECTION_SCOPE_VIOLATION.

SELECTION_CARDINALITY_VIOLATION.

CANDIDATE_SET_VIOLATION.

FILTER_IDENTITY_VIOLATION.

FILTER_PROPERTY_VIOLATION.

FILTER_PROPERTY_APPLICABILITY_VIOLATION.

FILTER_OPERATOR_VIOLATION.

FILTER_OPERATOR_COMPATIBILITY_VIOLATION.

FILTER_VALUE_TYPE_VIOLATION.

FILTER_VALUE_COMPATIBILITY_VIOLATION.

FILTER_CONJUNCTION_VIOLATION.

FILTER_NEGATION_VIOLATION.

FILTER_PRIORITY_VIOLATION.

FILTER_GROUP_IDENTITY_VIOLATION.

FILTER_GROUP_CLOSURE_VIOLATION.

FILTER_GROUP_CYCLE_VIOLATION.

FILTER_SET_VIOLATION.

REGISTRY_CLOSURE_VIOLATION.

BASELINE_VIOLATION.

CARDINALITY_VIOLATION.

IMMUTABILITY_VIOLATION.

SERIALIZATION_VIOLATION.

INTEGRITY_VIOLATION.

EVIDENCE_VIOLATION.

---

## Failure Conditions

Selection or Filter validation shall fail
when:

The Selection Identifier is missing, invalid,
duplicated, or improperly reused.

The Selection Target is unknown or private.

The Selection Target is incompatible with
Query Form.

The Selection Scope cannot be resolved.

The Selection Scope references an incompatible
Graph Version.

The Component Registry cannot be resolved.

The Candidate Set contains an unregistered or
implicit Graph Component.

Selection Cardinality is missing or invalid.

The Selection Result violates declared
Selection Cardinality.

The Filter Identifier is missing, invalid,
duplicated, or improperly reused.

The Filter Property is unknown or private.

The Filter Property is inapplicable to the
Selection Target.

The Filter Operator is unknown or private.

The Filter Operator is incompatible with the
Filter Property.

The Filter Value Type is unknown.

The Filter Value is incompatible with its
property or operator.

A canonical Filter Value cannot be resolved.

Filter Conjunction is missing when required.

Filter Negation is missing or ambiguous.

Filter Priority is duplicated.

A Filter Group reference cannot be resolved.

A Filter Group references itself.

A direct or indirect Filter Group cycle
exists.

An orphan Filter Expression exists.

An orphan Filter Group exists.

The Filter Set is not closed.

Deterministic Filter ordering cannot be
established.

A baseline reference is missing, unknown, or
incompatible.

Selection or Filter canonical serialization
cannot be produced.

Selection, Filter, Group, Set, or Result
integrity cannot be established.

Required evidence cannot be produced.

---

## Read-Only Boundary

Selection and filtering shall not:

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Component.

Modify a Candidate Set component.

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

## Selection and Filter Constraints

Every Query Request shall reference exactly
one Selection Expression.

Every Selection Expression shall target one
registered Graph Component type.

Every Selection Scope shall reference one
immutable Graph Version.

Every Candidate Set component shall be
registered.

Every Filter Expression shall reference one
Selection Expression.

Every Filter Property shall be canonical and
applicable.

Every Filter Operator shall be permitted and
compatible.

Every Filter Value shall possess one explicit
compatible type.

Every Filter Conjunction shall be explicit.

Every Filter Negation shall be explicit.

Every Filter Group shall be closed and
acyclic.

Every Filter Priority shall be unique within
its evaluation scope.

Every Filter Set shall be deterministically
ordered.

Every Eligible Component shall originate from
the Candidate Set.

Every successful or failed Selection and
Filter operation shall produce deterministic
evidence.

No invalid Selection Expression shall
participate in execution.

No invalid Filter Expression or Filter Set
shall participate in execution.

No Selection or Filter operation shall
redefine frozen Commerce semantics.

---

## Selection and Filter Invariants

Read-Only Preservation.

Canonical Selection Identity.

Selection Target Validity.

Query Form Compatibility.

Selection Scope Closure.

Immutable Graph Target.

Candidate Registry Closure.

Deterministic Candidate Ordering.

Selection Cardinality Integrity.

Canonical Filter Identity.

Filter Property Canonicality.

Filter Property Applicability.

Filter Operator Validity.

Filter Operator Compatibility.

Filter Value Type Validity.

Filter Value Compatibility.

Explicit Filter Conjunction.

Explicit Filter Negation.

Filter Group Closure.

Filter Group Acyclicity.

Deterministic Filter Priority.

Deterministic Filter Ordering.

Filter Set Closure.

Eligible Set Subset Integrity.

Eligible Set Ordering Preservation.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Selection Integrity.

Filter Integrity.

Filter Group Integrity.

Filter Set Integrity.

Selection Evidence Completeness.

Filter Validation Evidence Completeness.

Filter Evaluation Evidence Completeness.

Canonical Serialization.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Release Criteria

Selection and Filter pipeline is explicitly
defined.

Selection Expression is explicitly defined.

Selection Identity is explicitly defined.

Selection Targets and Query Form compatibility
are explicitly defined.

Selection Scope is explicitly defined.

Candidate Set is explicitly defined.

Selection Cardinality and Selection Result
are explicitly defined.

Filter Expression and Filter Identity are
explicitly defined.

Filter Property Registry is explicitly
defined.

Canonical, Relationship, and Path Identifier
filtering are explicitly defined.

Preferred Name, Knowledge Object Type, and
Relationship Type filtering are explicitly
defined.

Source, Target, Start, and End filtering are
explicitly defined.

Directionality and Traversal Direction
filtering are explicitly defined.

Lifecycle, Ontology, Domain, and Path Length
filtering are explicitly defined.

Filter Operators and Operator Semantics are
explicitly defined.

Filter Value Types and validation are
explicitly defined.

Filter Conjunction and Negation are explicitly
defined.

Filter Groups, closure, identity, and
priority are explicitly defined.

Deterministic Filter Ordering is explicitly
defined.

Filter Set and Filter Evaluation are
explicitly defined.

Filter and Filter Group Evaluation Results
are explicitly defined.

Eligible Component Set is explicitly defined.

Selection, Filter Validation, and Filter
Evaluation Evidence are explicitly defined.

Selection, Filter, and Group Integrity are
explicitly defined.

Canonical Serialization is explicitly
defined.

Selection, Filter, and Filter Set Validation
are explicitly defined.

Validation Result is explicitly defined.

Failure Classifications and Failure Conditions
are explicitly defined.

Read-Only Boundary is declared.

Selection and Filter Constraints are
declared.

Selection and Filter Invariants are declared.

---

## Next Deliverable

CKP-004.6

Projection, Ordering, and Pagination Model.
