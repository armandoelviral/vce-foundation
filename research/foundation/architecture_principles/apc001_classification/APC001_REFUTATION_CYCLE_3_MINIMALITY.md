# APC-001 Refutation Cycle 3

Target

APC-001 Version 0.3 Draft

Title

Architecture Principle Classification Model

Refutation Type

Classifier Minimality Attack

Status

Research

---

## Purpose

Determine whether
the twenty-two
APC-001 criteria

represent
independently necessary
classification dimensions

or whether
the classifier itself
contains:

Duplication.

Subsumption.

Artificial fragmentation.

Overlapping tests.

Unnecessary normative
surface.

The objective
is not to minimize
criterion count
for aesthetic reasons.

The objective
is to determine
whether criteria
can be merged

without reducing
classification power.

---

## Governing Authority

This investigation
is subordinate to

RC-001
Repository Constitution
Baseline 1.0

and governed by

SL-001
Repository Specification Lifecycle
Baseline 1.0.

APC-001 remains
non-authoritative.

---

# MA-001 — Necessity versus Independent Semantics

## Compared Criteria

APC-01
Architectural Necessity.

APC-04
Independent Semantics.

## Attack

If a proposition
has no independent
semantics,

can it possess
independent
architectural necessity?

## Analysis

Ordinarily no.

However,
the tests answer
different questions.

Architectural Necessity asks:

Would architecture
materially weaken
without the proposition?

Independent Semantics asks:

Is the proposition
already fully governed
elsewhere?

A proposition
may be architecturally useful
and necessary in practice

yet normatively redundant.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-002 — Layer Correctness versus Subject / Layer Separation

## Compared Criteria

APC-02
Layer Correctness.

APC-03
Subject / Layer Separation.

## Attack

Does Subject / Layer
Separation provide
an independent test?

## Analysis

Subject / Layer Separation
exists primarily
to prevent
misapplication
of Layer Correctness.

It clarifies
that labels such as:

Runtime.

Security.

Artifact.

Domain.

do not determine
normative layer.

The underlying
classification question
remains
Layer Correctness.

## Result

SEMANTICALLY
SUBSUMED.

MERGE.

---

# MA-003 — Independent Semantics versus Semantic Duplication

## Compared Criteria

APC-04
Independent Semantics.

APC-15
Semantic Duplication.

## Attack

Do both test
the same failure?

## Analysis

They substantially overlap.

Independent Semantics
asks whether
the candidate contributes
new architectural meaning.

Semantic Duplication
tests whether
another proposition
already expresses
that meaning.

Semantic duplication
is therefore
a principal method
for evaluating
independent semantics.

## Result

SUBSTANTIAL OVERLAP.

MERGE.

---

# MA-004 — Independent Semantics versus Subsumption

## Compared Criteria

APC-04
Independent Semantics.

APC-16
Subsumption.

## Attack

Is Subsumption
merely another
duplication test?

## Analysis

Not entirely.

A candidate
may possess
distinct wording
and narrower scope

while its semantics
are fully contained
inside another principle.

Subsumption
tests containment,

not merely equivalence.

## Result

DISTINCT ENOUGH
TO RETAIN
AS ANALYSIS OPERATION.

NOT NECESSARILY
A TOP-LEVEL CRITERION.

---

# MA-005 — Reduction versus Candidate Minimality

## Compared Criteria

APC-05
Reduction.

APC-13
Candidate Minimality.

## Attack

Does Reduction
need independent
criterion status?

## Analysis

Reduction
is primarily
a corrective operation

triggered when
a candidate contains:

Redundancy.

Layer contamination.

Excess semantics.

Candidate Minimality
defines
the required property.

Reduction
is a response
to failure.

## Result

REDUCTION
IS AN OPERATION,

NOT AN INDEPENDENT
CLASSIFICATION DIMENSION.

REMOVE FROM
TOP-LEVEL CRITERIA.

---

# MA-006 — Explicit Scope versus Applicability Boundary

## Compared Criteria

APC-06
Explicit Scope.

APC-07
Applicability Boundary.

## Attack

Can these
be one criterion?

## Analysis

They are closely related
but not identical.

Scope identifies
where authority applies.

Applicability identifies
when the proposition
becomes operative
inside that scope.

Example:

Scope

Runtime Architecture.

Applicability

Only executions
crossing an
external trust boundary.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-007 — Explicit Scope versus Technology-Bounded Scope

## Compared Concepts

APC-06
Explicit Scope.

Technology-Bounded
Architecture Scope.

## Attack

Does technology-bounded
scope require
an additional criterion?

## Analysis

No.

Technology-bounded scope
is a valid
scope form.

It is already
governed by
Explicit Scope

plus

Technology Independence.

## Result

CLARIFICATION ONLY.

NO NEW CRITERION.

---

# MA-008 — Cross-Decision Value versus Architectural Necessity

## Compared Criteria

APC-08
Cross-Decision Value.

APC-01
Architectural Necessity.

## Attack

If a proposition
is architecturally necessary,

must it automatically
constrain
multiple decisions?

## Analysis

No.

A proposition
could be necessary
for one architectural
boundary

yet too narrow
to deserve
principle status.

Cross-decision value
tests whether
principle abstraction
is justified.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-009 — Technology Independence versus Replaceability of Form

## Compared Criteria

APC-09
Technology Independence.

APC-20
Replaceability of Form.

## Attack

Are these
the same principle
expressed differently?

## Analysis

They overlap
but protect
different failure modes.

Technology Independence
prevents dependence
upon implementation
technology.

Replaceability of Form
prevents dependence
upon architectural
representation.

A technology-neutral
principle
could still depend
upon one particular
diagram,
component taxonomy,
or topology.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-010 — Falsifiability versus Evidence Basis

## Compared Criteria

APC-10
Falsifiability.

APC-11
Evidence Basis.

## Attack

Does evidence
automatically imply
falsifiability?

## Analysis

No.

A candidate
may possess
supporting evidence

while being framed
so broadly
that no evidence
could count against it.

Likewise,

a falsifiable proposition
may currently possess
insufficient evidence.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-011 — Authority Non-Expansion versus Explicit Scope

## Compared Criteria

APC-12
Authority Non-Expansion.

APC-06
Explicit Scope.

## Attack

If scope
is explicit,

is authority
non-expansion automatic?

## Analysis

No.

A candidate
may declare
a narrow scope

yet still claim
authority
over a higher
normative layer.

Scope
and authority level
are separate dimensions.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-012 — Candidate Minimality versus Semantic Cohesion

## Compared Criteria

APC-13
Candidate Minimality.

APC-14
Semantic Cohesion.

## Attack

Does minimality
already require
cohesion?

## Analysis

Partially.

A candidate
may contain
only necessary statements

yet those statements
may represent
two independent
architectural propositions.

Semantic Cohesion
tests conceptual unity.

Candidate Minimality
tests excess semantics.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-013 — Candidate Minimality versus Semantic Duplication

## Compared Criteria

APC-13
Candidate Minimality.

APC-15
Semantic Duplication.

## Attack

Can duplication
be handled entirely
by Candidate Minimality?

## Analysis

At candidate level,
duplicated external semantics
make independent
candidate existence
unnecessary.

However,
this is more directly
captured by
Independent Semantics.

## Result

SEMANTIC DUPLICATION
SHALL MERGE INTO
INDEPENDENT SEMANTICS.

---

# MA-014 — Semantic Duplication versus Subsumption

## Compared Criteria

APC-15
Semantic Duplication.

APC-16
Subsumption.

## Attack

Can one operation
cover both?

## Analysis

They represent
two relationships:

Equivalence.

Containment.

Both belong
to semantic
relationship analysis.

They need not remain
separate
top-level criteria.

## Result

MERGE INTO
SEMANTIC INDEPENDENCE
ANALYSIS.

---

# MA-015 — Compatibility versus Composition

## Compared Criteria

APC-17
Compatibility.

APC-18
Composition.

## Attack

Is Composition
simply one
compatibility test?

## Analysis

Composition examines
whether individually
acceptable principles

produce invalid behavior
when combined.

This is a form
of compatibility analysis.

No independent
top-level criterion
is required

if compatibility
explicitly includes
composition.

## Result

MERGE.

---

# MA-016 — Compatibility versus Set-Level Minimality

## Compared Criteria

APC-17
Compatibility.

APC-19
Set-Level Minimality.

## Attack

Can set-level minimality
be absorbed
into compatibility?

## Analysis

No.

A set
may be fully compatible

yet contain:

Redundancy.

Fragmentation.

Subsumption.

Unnecessary principles.

Compatibility
does not establish
minimality.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-017 — Candidate Minimality versus Set-Level Minimality

## Compared Criteria

APC-13
Candidate Minimality.

APC-19
Set-Level Minimality.

## Attack

Does candidate minimality
scale automatically
to the AP set?

## Analysis

No.

Every candidate
may be individually minimal

while the complete set
remains redundant
or fragmented.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-018 — Semantic Cohesion versus Set-Level Minimality

## Compared Criteria

APC-14
Semantic Cohesion.

APC-19
Set-Level Minimality.

## Attack

Could set-level minimality
replace cohesion?

## Analysis

No.

Set-level minimality
operates across principles.

Semantic Cohesion
operates inside
one principle.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-019 — Replaceability of Form versus Technology Independence

## Scenario

A principle
mentions no
specific technology

but assumes
a fixed
three-tier topology.

## Attack

Would Technology Independence
detect the defect?

## Analysis

No.

The candidate
is technology-independent

but representation
or topology dependent.

## Result

REPLACEABILITY OF FORM
RETAINS
INDEPENDENT VALUE.

---

# MA-020 — Non-Circular Justification versus Evidence Basis

## Compared Criteria

APC-21
Non-Circular Justification.

APC-11
Evidence Basis.

## Attack

Could Evidence Basis
reject circular evidence
without another criterion?

## Analysis

Potentially,

but Non-Circular
Justification identifies
a specific
authority failure:

The architecture
cannot prove
its own authority
merely through existence.

This is important enough
to preserve explicitly

but may become
a constraint
inside Evidence Basis.

## Result

MERGE CANDIDATE.

---

# MA-021 — Evolution Readiness versus Authority Non-Expansion

## Compared Criteria

APC-22
Evolution Readiness.

APC-12
Authority Non-Expansion.

## Attack

Are both
authority semantics?

## Analysis

They concern
different dimensions.

Authority Non-Expansion
limits present authority.

Evolution Readiness
governs future
normative change.

## Result

DISTINCT.

RETAIN BOTH.

---

# MA-022 — Evolution Readiness versus SL-001

## Attack

If SL-001 already
governs normative
lifecycle,

does APC-001 need
Evolution Readiness
as a classification criterion?

## Analysis

Potentially not.

If every AP
is already governed
by SL-001,

versioned evolution
may be inherited
from higher normative
lifecycle semantics.

APC-001 need only
require conformance
to that lifecycle.

## Result

POTENTIAL
REDUNDANCY IDENTIFIED.

REQUIRES DIRECT
SL-001 COVERAGE TEST.

---

# MA-023 — Authority Non-Expansion versus RC-001

## Attack

RC-001 already
governs
authority hierarchy.

Does APC-001 need
an independent
Authority Non-Expansion
criterion?

## Analysis

The rule itself
is inherited
from RC-001.

However,
classification must test
whether a candidate
violates it.

The classifier
need not create
new authority semantics,

but must preserve
the conformance test.

## Result

RETAIN
AS CONFORMANCE TEST,

NOT INDEPENDENT
AUTHORITY SOURCE.

---

# MA-024 — Technology Independence versus RC-001

## Attack

RC-001 already
contains
Technology Independence.

Is APC-09 redundant?

## Analysis

Its authority
is inherited.

Its classification
function remains necessary:

APC-001 must detect
candidate violations
of RC-001.

## Result

RETAIN
AS CONFORMANCE TEST.

---

# MA-025 — Criterion versus Operation

## Finding

APC-001 v0.3
mixes:

Classification dimensions.

Conformance tests.

Analysis operations.

Corrective actions.

## Examples

Classification dimensions:

Architectural Necessity.

Layer Correctness.

Scope.

Cross-Decision Value.

Falsifiability.

---

Conformance tests:

Technology Independence.

Authority Non-Expansion.

---

Analysis operations:

Reduction.

Subsumption.

Composition.

Semantic duplication.

---

Corrective actions:

Relocation.

Reduction.

Rejection.

## Result

MODEL TAXONOMY
REQUIRES REFINEMENT.

---

# MA-026 — Reduction as Outcome and Criterion

## Attack

APC-001 contains
Reduction

both as
Criterion 5

and as
classification outcome:

REDUCE.

## Analysis

This creates
unnecessary
conceptual duplication.

Reduction
should be
an operation
or outcome,

not both
a required property
and response.

## Result

CRITERION 5
SHOULD BE REMOVED.

---

# MA-027 — Composition as Criterion and Analysis

## Attack

Composition
is currently
a top-level criterion

while compatibility
already requires
composition analysis.

## Analysis

This duplicates
the evaluation path.

## Result

CRITERION 18
SHOULD MERGE
INTO COMPATIBILITY.

---

# MA-028 — Semantic Relations

## Finding

Independent Semantics.

Semantic Duplication.

Subsumption.

all evaluate
relationships
between candidate semantics
and existing authority.

## Analysis

They can be represented
through one stronger
classification dimension:

Semantic Independence.

Its analysis
shall test:

Equivalence.

Overlap.

Containment.

Partial derivation.

Existing authority.

## Result

THREE CRITERIA
CAN REDUCE
TO ONE.

---

# MA-029 — Evidence Integrity

## Finding

Evidence Basis
and Non-Circular
Justification
are closely coupled.

## Analysis

A stronger
Evidence Basis criterion
can require evidence
to be:

Relevant.

Scope-matched.

Non-circular.

Independent
where required.

Refutable.

However,
Falsifiability
remains distinct

because it concerns
the proposition,

not merely
supporting evidence.

## Result

NON-CIRCULAR
JUSTIFICATION
CAN MERGE
INTO EVIDENCE BASIS.

---

# MA-030 — Minimal Classifier

## Question

Can APC-001
reduce its
twenty-two criteria

without losing
the adversarial
classification capability
demonstrated
in Cycle 2?

## Analysis

Yes.

At minimum,
the following reductions
are supported:

Layer Correctness
absorbs
Subject / Layer Separation.

Semantic Independence
absorbs:

Independent Semantics.

Semantic Duplication.

Subsumption analysis.

Reduction becomes
an operation,
not a criterion.

Compatibility
absorbs
Composition.

Evidence Basis
absorbs
Non-Circular Justification.

Evolution Readiness
requires direct comparison
against SL-001
before retention.

The remaining criteria
continue to represent
distinct classification
or conformance dimensions.

## Result

APC-001 v0.3
IS NOT MINIMAL.

REDUCTION REQUIRED.

---

# Minimality Findings

Original APC-001 v0.1
Criteria

12.

APC-001 v0.2
and v0.3 Criteria

22.

The expansion
corrected genuine
classification gaps

but promoted
several analysis operations
and clarifications
into independent criteria.

The classifier
therefore became
more robust

but less minimal.

---

# Supported Merges

Merge 1

Layer Correctness

absorbs

Subject / Layer Separation.

---

Merge 2

Semantic Independence

absorbs

Independent Semantics.

Semantic Duplication.

Subsumption.

Partial overlap analysis.

---

Merge 3

Compatibility

absorbs

Composition.

---

Merge 4

Evidence Basis

absorbs

Non-Circular Justification.

---

# Supported Removal

Reduction

shall cease
to be
a top-level criterion.

Reduction remains:

An analysis operation.

A classification outcome.

A corrective action.

---

# Unresolved Criterion

Evolution Readiness

may duplicate
SL-001 lifecycle
authority.

Its retention
requires direct
coverage analysis
against SL-001.

---

# Required Model Separation

Future APC-001
shall distinguish:

Classification Criteria.

Constitutional
Conformance Tests.

Semantic
Analysis Operations.

Classification Outcomes.

Corrective Actions.

These categories
shall not be
silently conflated.

---

# Candidate Reduced Structure

Classification Criteria
may reduce toward:

Architectural Necessity.

Layer Correctness.

Semantic Independence.

Explicit Scope.

Applicability Boundary.

Cross-Decision Value.

Candidate Minimality.

Semantic Cohesion.

Falsifiability.

Evidence Basis.

Compatibility.

Set-Level Minimality.

Replaceability of Form.

Evolution Conformance,
if not fully inherited.

---

Constitutional
Conformance Tests:

Technology Independence.

Authority Non-Expansion.

---

Analysis Operations:

Reduction.

Equivalence analysis.

Overlap analysis.

Subsumption analysis.

Composition analysis.

Relocation analysis.

---

Classification Outcomes
remain distinct
from criteria.

---

# Refutation Outcome

Target

APC-001 Version 0.3 Draft.

Outcome

REFUTED
ON MINIMALITY.

Classification Power

SURVIVES.

Adversarial Robustness

SURVIVES.

Twenty-Two Criterion Model

REFUTED.

Layer Correctness /
Subject Separation

MERGE.

Independent Semantics /
Duplication /
Subsumption

MERGE.

Reduction Criterion

REMOVE.

Compatibility /
Composition

MERGE.

Evidence Basis /
Non-Circular Justification

MERGE.

Evolution Readiness

UNRESOLVED
PENDING SL-001
COVERAGE TEST.

Authority

NONE.

Freeze

PROHIBITED.

Promotion

PROHIBITED.

Next Required Activity

SL-001 Coverage Test
for AP Evolution.

---

# End of APC-001 Refutation Cycle 3
