# Commerce Query Language Initial Executable Queries

Version

1.0

Status

Draft

Graph Identifier

CKP-GRAPH-000001

Graph Version

1.0

---

## Purpose

Define the first canonical executable
specification queries for Commerce Query
Language.

The Initial Executable Queries demonstrate
that the frozen Commerce Knowledge Graph can
be queried and validated through explicit,
deterministic, read-only, traceable, and
auditable Query Requests.

Executable Query specifications shall not
require a parser, interpreter, database,
storage adapter, network transport, or query
runtime.

---

## Execution Boundary

The Initial Executable Queries target:

CKP-GRAPH-000001.

Graph Version 1.0.

The Graph contains:

10 registered Graph Nodes.

12 registered Graph Edges.

4 registered Graph Paths.

The queries consume:

CKP-001 Canonical Commerce Vocabulary 1.0.

CKP-002 Commerce Ontology 1.0.

CKP-003 Commerce Knowledge Graph 1.0.

No query may modify these immutable
baselines.

---

## Executable Query Contract

Every Initial Executable Query shall declare:

Query Identifier.

Query Version.

Lifecycle Status.

Graph Identifier.

Graph Version.

Query Form.

Selection Target.

Selection Cardinality.

Filter Expressions.

Projection Properties.

Ordering Rules.

Pagination Rules.

Validation Type.

Expected Result.

Expected Matched Identifiers.

Expected Matched Record Count.

Expected Returned Record Count.

Expected Validation Outcome.

Expected Expectation Match Result.

Execution Context Reference.

Vocabulary Baseline Reference.

Ontology Baseline Reference.

Graph Baseline Reference.

Expected Evidence Reference.

Expected Result Integrity Reference.

---

## Execution Context

Initial Execution Context Identifier

CKP-QUERY-CONTEXT-000001

Graph Identifier

CKP-GRAPH-000001

Graph Version

1.0

Vocabulary Baseline

CKP-001 Canonical Commerce Vocabulary 1.0

Ontology Baseline

CKP-002 Commerce Ontology 1.0

Graph Baseline

CKP-003 Commerce Knowledge Graph 1.0

Maximum Result Limit

100

Maximum Validation Depth

10

Node Registry Reference

research/commerce/registry/TERM_REGISTRY.md

Edge Registry Reference

research/commerce/ontology/INITIAL_COMMERCE_ONTOLOGY.md

Path Registry Reference

research/commerce/knowledge_graph/initial/INITIAL_COMMERCE_KNOWLEDGE_GRAPH.md

The Initial Execution Context is immutable.

---

## Canonical Result Ordering

Unless an executable query declares explicit
ordering:

Graph Nodes shall be ordered by Canonical
Identifier.

Graph Edges shall be ordered by Relationship
Identifier.

Graph Paths shall be ordered by Path
Identifier.

All identifier ordering shall be ascending.

Pagination shall occur after deterministic
ordering.

---

## IEQ-001 — Select All Graph Nodes

Query Identifier

CKP-QUERY-000001

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT NODE

Selection Target

Graph Node

Selection Cardinality

ZERO OR MORE

Filter Expressions

None

Projection Properties

Canonical Identifier.

Preferred Name.

Knowledge Object Type.

Lifecycle Status.

Ontology Membership.

Domain Membership.

Ordering Rules

Canonical Identifier ASCENDING.

Pagination Rules

Limit 100.

Offset 0.

Expected Matched Identifiers

CKP-TERM-000001.

CKP-TERM-000002.

CKP-TERM-000003.

CKP-TERM-000004.

CKP-TERM-000005.

CKP-TERM-000006.

CKP-TERM-000007.

CKP-TERM-000008.

CKP-TERM-000009.

CKP-TERM-000010.

Expected Matched Record Count

10

Expected Returned Record Count

10

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000001

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000001

---

## IEQ-002 — Select Retail Graph Node

Query Identifier

CKP-QUERY-000002

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT NODE

Selection Target

Graph Node

Selection Cardinality

EXACTLY ONE

Filter Expression

Filter Identifier

CKP-FILTER-000002

Filter Property

Canonical Identifier

Filter Operator

EQUALS

Filter Value Type

IDENTIFIER

Filter Value

CKP-TERM-000002

Filter Negation

NOT NEGATED

Filter Priority

0

Projection Properties

Canonical Identifier.

Preferred Name.

Knowledge Object Type.

Ontology Membership.

Domain Membership.

Expected Matched Identifiers

CKP-TERM-000002.

Expected Preferred Name

Retail

Expected Matched Record Count

1

Expected Returned Record Count

1

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000002

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000002

---

## IEQ-003 — Select Commerce Model Nodes

Query Identifier

CKP-QUERY-000003

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT NODE

Selection Target

Graph Node

Selection Cardinality

ZERO OR MORE

Filter Expression

Filter Identifier

CKP-FILTER-000003

Filter Property

Ontology Membership

Filter Operator

EQUALS

Filter Value Type

TEXT

Filter Value

Commerce Model

Filter Negation

NOT NEGATED

Filter Priority

0

Ordering Rules

Canonical Identifier ASCENDING.

Expected Matched Identifiers

CKP-TERM-000002.

CKP-TERM-000003.

CKP-TERM-000005.

Expected Matched Record Count

3

Expected Returned Record Count

3

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000003

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000003

---

## IEQ-004 — Select Is A Graph Edges

Query Identifier

CKP-QUERY-000004

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT EDGE

Selection Target

Graph Edge

Selection Cardinality

ZERO OR MORE

Filter Expression

Filter Identifier

CKP-FILTER-000004

Filter Property

Canonical Relationship Type

Filter Operator

EQUALS

Filter Value Type

ENUMERATION

Filter Value

Is A

Filter Negation

NOT NEGATED

Filter Priority

0

Projection Properties

Relationship Identifier.

Source Node Identifier.

Canonical Relationship Type.

Target Node Identifier.

Directionality.

Ordering Rules

Relationship Identifier ASCENDING.

Expected Matched Identifiers

CKP-REL-000001.

CKP-REL-000002.

CKP-REL-000003.

CKP-REL-000004.

Expected Matched Record Count

4

Expected Returned Record Count

4

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000004

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000004

---

## IEQ-005 — Select Edges Targeting Commerce

Query Identifier

CKP-QUERY-000005

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT EDGE

Selection Target

Graph Edge

Selection Cardinality

ZERO OR MORE

Filter Expression

Filter Identifier

CKP-FILTER-000005

Filter Property

Target Node Identifier

Filter Operator

EQUALS

Filter Value Type

IDENTIFIER

Filter Value

CKP-TERM-000001

Filter Negation

NOT NEGATED

Filter Priority

0

Ordering Rules

Relationship Identifier ASCENDING.

Expected Matched Identifiers

CKP-REL-000001.

CKP-REL-000002.

CKP-REL-000003.

CKP-REL-000004.

Expected Matched Record Count

4

Expected Returned Record Count

4

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000005

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000005

---

## IEQ-006 — Select Product Semantic Edges

Query Identifier

CKP-QUERY-000006

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT EDGE

Selection Target

Graph Edge

Selection Cardinality

ZERO OR MORE

Filter Group Identifier

CKP-FILTER-GROUP-000006

Group Conjunction

OR

Group Negation

NOT NEGATED

Group Priority

0

Filter Expression A

Filter Identifier

CKP-FILTER-000006-A

Filter Property

Source Node Identifier

Filter Operator

EQUALS

Filter Value Type

IDENTIFIER

Filter Value

CKP-TERM-000006

Filter Negation

NOT NEGATED

Filter Priority

0

Filter Expression B

Filter Identifier

CKP-FILTER-000006-B

Filter Property

Target Node Identifier

Filter Operator

EQUALS

Filter Value Type

IDENTIFIER

Filter Value

CKP-TERM-000006

Filter Negation

NOT NEGATED

Filter Priority

1

Ordering Rules

Relationship Identifier ASCENDING.

Expected Matched Identifiers

CKP-REL-000005.

CKP-REL-000006.

CKP-REL-000007.

CKP-REL-000010.

Expected Matched Record Count

4

Expected Returned Record Count

4

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000006

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000006

---

## IEQ-007 — Select Registered Graph Paths

Query Identifier

CKP-QUERY-000007

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT PATH

Selection Target

Graph Path

Selection Cardinality

ZERO OR MORE

Filter Expressions

None

Projection Properties

Path Identifier.

Start Node Identifier.

End Node Identifier.

Ordered Node Sequence.

Ordered Edge Sequence.

Path Length.

Ordering Rules

Path Identifier ASCENDING.

Expected Matched Identifiers

CKP-PATH-000001.

CKP-PATH-000002.

CKP-PATH-000003.

CKP-PATH-000004.

Expected Matched Record Count

4

Expected Returned Record Count

4

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000007

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000007

---

## IEQ-008 — Select Composite Paths

Query Identifier

CKP-QUERY-000008

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT PATH

Selection Target

Graph Path

Selection Cardinality

ZERO OR MORE

Filter Expression

Filter Identifier

CKP-FILTER-000008

Filter Property

Path Length

Filter Operator

GREATER THAN

Filter Value Type

INTEGER

Filter Value

1

Filter Negation

NOT NEGATED

Filter Priority

0

Expected Matched Identifiers

CKP-PATH-000004.

Expected Matched Record Count

1

Expected Returned Record Count

1

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000008

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000008

---

## IEQ-009 — Paginate Graph Nodes

Query Identifier

CKP-QUERY-000009

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT NODE

Selection Target

Graph Node

Selection Cardinality

ZERO OR MORE

Filter Expressions

None

Projection Properties

Canonical Identifier.

Preferred Name.

Ordering Rules

Canonical Identifier ASCENDING.

Pagination Rules

Limit 3.

Offset 2.

Expected Matched Identifiers

CKP-TERM-000001.

CKP-TERM-000002.

CKP-TERM-000003.

CKP-TERM-000004.

CKP-TERM-000005.

CKP-TERM-000006.

CKP-TERM-000007.

CKP-TERM-000008.

CKP-TERM-000009.

CKP-TERM-000010.

Expected Returned Identifiers

CKP-TERM-000003.

CKP-TERM-000004.

CKP-TERM-000005.

Expected Matched Record Count

10

Expected Returned Record Count

3

Expected Offset

2

Expected Limit

3

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000009

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000009

---

## IEQ-010 — Validate Retail Exists

Validation Query Identifier

CKP-VALIDATION-QUERY-000010

Query Identifier

CKP-QUERY-000010

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE EXISTS

Validation Type

EXISTS

Selection Target

Graph Node

Subject Identifier

CKP-TERM-000002

Subject Component Type

Graph Node

Validation Object

None

Expected Result

TRUE

Expected Validation Outcome

TRUE

Expected Expectation Match Result

MATCH

Expected Matched Identifiers

CKP-TERM-000002.

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000010

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000010

---

## IEQ-011 — Validate Unknown Node Does Not Exist

Validation Query Identifier

CKP-VALIDATION-QUERY-000011

Query Identifier

CKP-QUERY-000011

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE EXISTS

Validation Type

EXISTS

Selection Target

Graph Node

Subject Identifier

CKP-TERM-999999

Subject Component Type

Graph Node

Validation Object

None

Expected Result

FALSE

Expected Validation Outcome

FALSE

Expected Expectation Match Result

MATCH

Expected Matched Identifiers

None

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000011

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000011

---

## IEQ-012 — Validate Retail Is A Commerce

Validation Query Identifier

CKP-VALIDATION-QUERY-000012

Query Identifier

CKP-QUERY-000012

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE RELATIONSHIP

Validation Type

RELATIONSHIP

Subject Identifier

CKP-TERM-000002

Object Identifier

CKP-TERM-000001

Canonical Relationship Type

Is A

Validation Direction

FORWARD

Expected Result

TRUE

Expected Validation Outcome

TRUE

Expected Expectation Match Result

MATCH

Expected Matched Identifiers

CKP-REL-000001.

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000012

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000012

---

## IEQ-013 — Validate Commerce Is Not A Retail

Validation Query Identifier

CKP-VALIDATION-QUERY-000013

Query Identifier

CKP-QUERY-000013

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE RELATIONSHIP

Validation Type

RELATIONSHIP

Subject Identifier

CKP-TERM-000001

Object Identifier

CKP-TERM-000002

Canonical Relationship Type

Is A

Validation Direction

FORWARD

Expected Result

FALSE

Expected Validation Outcome

FALSE

Expected Expectation Match Result

MATCH

Expected Matched Identifiers

None

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000013

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000013

---

## IEQ-014 — Validate Product Contains SKU

Validation Query Identifier

CKP-VALIDATION-QUERY-000014

Query Identifier

CKP-QUERY-000014

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE RELATIONSHIP

Validation Type

RELATIONSHIP

Subject Identifier

CKP-TERM-000006

Object Identifier

CKP-TERM-000007

Canonical Relationship Type

Contains

Validation Direction

FORWARD

Expected Result

TRUE

Expected Validation Outcome

TRUE

Expected Expectation Match Result

MATCH

Expected Matched Identifiers

CKP-REL-000006.

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000014

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000014

---

## IEQ-015 — Validate Inventory Reaches Product

Validation Query Identifier

CKP-VALIDATION-QUERY-000015

Query Identifier

CKP-QUERY-000015

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE REACHABLE

Validation Type

REACHABLE

Subject Identifier

CKP-TERM-000008

Object Identifier

CKP-TERM-000006

Validation Direction

FORWARD

Traversal Strategy

SEMANTIC

Maximum Depth

2

Relationship Type Constraints

Applies To.

Part Of.

Expected Result

TRUE

Expected Validation Outcome

TRUE

Expected Expectation Match Result

MATCH

Expected Witness Path Identifier

CKP-PATH-000004

Expected Ordered Node Sequence

CKP-TERM-000008.

CKP-TERM-000007.

CKP-TERM-000006.

Expected Ordered Edge Sequence

CKP-REL-000011.

CKP-REL-000005.

Expected Path Length

2

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000015

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000015

---

## IEQ-016 — Validate Inventory Cannot Reach Product at Depth One

Validation Query Identifier

CKP-VALIDATION-QUERY-000016

Query Identifier

CKP-QUERY-000016

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE REACHABLE

Validation Type

REACHABLE

Subject Identifier

CKP-TERM-000008

Object Identifier

CKP-TERM-000006

Validation Direction

FORWARD

Traversal Strategy

SEMANTIC

Maximum Depth

1

Relationship Type Constraints

Applies To.

Part Of.

Expected Result

FALSE

Expected Validation Outcome

FALSE

Expected Expectation Match Result

MATCH

Expected Witness Path Identifier

None

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000016

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000016

---

## IEQ-017 — Validate Registered Composite Path

Validation Query Identifier

CKP-VALIDATION-QUERY-000017

Query Identifier

CKP-QUERY-000017

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE PATH

Validation Type

PATH

Path Validation Mode

REGISTERED PATH

Path Identifier

CKP-PATH-000004

Start Node Identifier

CKP-TERM-000008

End Node Identifier

CKP-TERM-000006

Validation Direction

FORWARD

Expected Result

TRUE

Expected Validation Outcome

TRUE

Expected Expectation Match Result

MATCH

Expected Path Length

2

Expected Path Continuity Result

Valid

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000017

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000017

---

## IEQ-018 — Validate Composed Continuous Path

Validation Query Identifier

CKP-VALIDATION-QUERY-000018

Query Identifier

CKP-QUERY-000018

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE PATH

Validation Type

PATH

Path Validation Mode

COMPOSED PATH

Start Node Identifier

CKP-TERM-000006

End Node Identifier

CKP-TERM-000010

Ordered Node Sequence

CKP-TERM-000006.

CKP-TERM-000010.

Ordered Edge Sequence

CKP-REL-000010.

Validation Direction

FORWARD

Declared Path Length

1

Expected Result

TRUE

Expected Validation Outcome

TRUE

Expected Expectation Match Result

MATCH

Expected Path Continuity Result

Valid

Expected Registration Effect

None

Expected Validation Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000018

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000018

---

## IEQ-019 — Validate Disconnected Composed Path

Validation Query Identifier

CKP-VALIDATION-QUERY-000019

Query Identifier

CKP-QUERY-000019

Query Version

1.0

Lifecycle Status

Approved

Query Form

VALIDATE PATH

Validation Type

PATH

Path Validation Mode

COMPOSED PATH

Start Node Identifier

CKP-TERM-000008

End Node Identifier

CKP-TERM-000010

Ordered Node Sequence

CKP-TERM-000008.

CKP-TERM-000010.

Ordered Edge Sequence

CKP-REL-000011.

Validation Direction

FORWARD

Declared Path Length

1

Expected Result

FALSE

Expected Validation Outcome

ERROR

Expected Expectation Match Result

NOT EVALUATED

Expected Path Continuity Result

Invalid

Expected Failure Classification

PATH_CONTINUITY_VIOLATION

Expected Validation Status

Failed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000019

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000019

---

## IEQ-020 — Select First Two Graph Edges

Query Identifier

CKP-QUERY-000020

Query Version

1.0

Lifecycle Status

Approved

Query Form

SELECT EDGE

Selection Target

Graph Edge

Selection Cardinality

ZERO OR MORE

Filter Expressions

None

Projection Properties

Relationship Identifier.

Canonical Relationship Type.

Ordering Rules

Relationship Identifier ASCENDING.

Pagination Rules

Limit 2.

Offset 0.

Expected Matched Record Count

12

Expected Returned Identifiers

CKP-REL-000001.

CKP-REL-000002.

Expected Returned Record Count

2

Expected Query Status

Completed

Expected Evidence Reference

CKP-QUERY-EVIDENCE-000020

Expected Result Integrity Reference

CKP-QUERY-RESULT-INTEGRITY-000020

---

## Deterministic Query Order

CKP-QUERY-000001.

CKP-QUERY-000002.

CKP-QUERY-000003.

CKP-QUERY-000004.

CKP-QUERY-000005.

CKP-QUERY-000006.

CKP-QUERY-000007.

CKP-QUERY-000008.

CKP-QUERY-000009.

CKP-QUERY-000010.

CKP-QUERY-000011.

CKP-QUERY-000012.

CKP-QUERY-000013.

CKP-QUERY-000014.

CKP-QUERY-000015.

CKP-QUERY-000016.

CKP-QUERY-000017.

CKP-QUERY-000018.

CKP-QUERY-000019.

CKP-QUERY-000020.

---

## Query Count

Initial Executable Query Count

20

SELECT NODE Query Count

4

SELECT EDGE Query Count

4

SELECT PATH Query Count

2

VALIDATE EXISTS Query Count

2

VALIDATE RELATIONSHIP Query Count

3

VALIDATE REACHABLE Query Count

2

VALIDATE PATH Query Count

3

---

## Query Evidence Requirements

Every Initial Executable Query shall produce
deterministic Query Evidence.

Evidence shall preserve:

Query Identifier.

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

Validation Outcome.

Expected Result.

Expectation Match Result.

Failure Classification.

Failure Reason.

Result Hash.

Evidence Integrity Reference.

No successful, false, failed, or cancelled
query shall omit evidence.

---

## Query Integrity Requirements

Every Initial Executable Query shall possess
one deterministic Query Integrity Reference.

Every terminal Query Result shall possess one
deterministic Result Integrity Reference.

Integrity shall bind every normative request,
expression, result, evidence, ordering,
pagination, and validation property.

Identical queries against the same immutable
Graph Version shall produce identical
normative results and integrity references.

---

## Query Validation

Every Initial Executable Query shall validate:

Query identity.

Query Version.

Lifecycle Status.

Graph target.

Query Form.

Selection target.

Selection cardinality.

Filter properties.

Filter operators.

Filter value types.

Filter grouping.

Projection properties.

Ordering rules.

Pagination boundaries.

Validation Type.

Validation Subject.

Validation Object when required.

Direction.

Maximum Depth.

Path structure.

Expected Result.

Baseline compatibility.

Canonical serialization.

Query Integrity.

Evidence completeness.

---

## Failure Behavior

Invalid Query Requests shall fail closed.

Invalid Filter Expressions shall fail closed.

Invalid Pagination boundaries shall fail
closed.

Invalid Validation Queries shall fail closed.

A structurally valid negative proposition
shall return FALSE rather than ERROR.

An unevaluable proposition shall return ERROR.

FALSE shall remain a valid Validation Outcome.

ERROR shall not be converted into FALSE.

No failure shall mutate or repair the Graph.

---

## Read-Only Boundary

Initial Executable Queries shall not:

Create a Graph Node.

Create a Graph Edge.

Create a Graph Path.

Register a composed Graph Path.

Delete a Graph Node.

Delete a Graph Edge.

Delete a Graph Path.

Modify a Graph Component.

Modify a Candidate Set.

Modify an Eligible Component Set.

Modify a Projected Record source.

Modify canonical ordering.

Repair an invalid Graph Component.

Repair a broken relationship.

Repair a disconnected path.

Modify CKP-001.

Modify CKP-002.

Modify CKP-003.

Create undocumented semantic meaning.

---

## Executable Query Invariants

Read-Only Preservation.

Canonical Query Identity.

Immutable Graph Target.

Query Form Canonicality.

Selection Target Compatibility.

Selection Cardinality Integrity.

Filter Property Canonicality.

Filter Operator Validity.

Filter Value Compatibility.

Filter Group Closure.

Deterministic Filter Ordering.

Projection Property Canonicality.

Deterministic Projection Position.

Deterministic Result Ordering.

Pagination Boundary Integrity.

Matched Record Count Preservation.

Returned Record Count Integrity.

Canonical Validation Type.

Expected Result Independence.

Validation Outcome Integrity.

Expectation Match Integrity.

Direct Relationship Semantics.

Reachability Maximum Depth Enforcement.

Witness Path Continuity.

Registered Path Closure.

Composed Path Non-Registration.

No Implicit Edges.

Vocabulary Compatibility.

Ontology Compatibility.

Graph Compatibility.

Query Evidence Completeness.

Query Integrity.

Result Integrity.

Canonical Serialization.

Deterministic Execution Specification.

Fail-Closed Validation.

Semantic Closure.

Traceability Closure.

---

## Release Criteria

Execution Boundary is explicitly defined.

Executable Query Contract is explicitly
defined.

Execution Context is explicitly defined.

Canonical Result Ordering is explicitly
defined.

SELECT NODE queries are declared.

SELECT EDGE queries are declared.

SELECT PATH queries are declared.

VALIDATE EXISTS queries are declared.

VALIDATE RELATIONSHIP queries are declared.

VALIDATE REACHABLE queries are declared.

VALIDATE PATH queries are declared.

Positive validation outcomes are declared.

Negative validation outcomes are declared.

Error validation outcomes are declared.

Deterministic pagination is demonstrated.

Deterministic witness path selection is
demonstrated.

Expected Result independence is demonstrated.

Composed Path non-registration is
demonstrated.

Deterministic Query Order is declared.

Exactly twenty Initial Executable Queries are
declared.

Query Evidence Requirements are declared.

Query Integrity Requirements are declared.

Query Validation is declared.

Failure Behavior is declared.

Read-Only Boundary is declared.

Executable Query Invariants are declared.

---

## Next Deliverable

CKP-004.9

Query Consistency Audit.
