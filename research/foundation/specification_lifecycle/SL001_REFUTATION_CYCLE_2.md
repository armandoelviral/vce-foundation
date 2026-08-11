# SL-001 Refutation Cycle 2

Title

Repository Specification Lifecycle
Second Refutation Cycle

Target

SL-001 Version 0.2 Draft

Version

0.1

Status

Research

---

## Purpose

Perform a second
systematic refutation
of the Repository
Specification Lifecycle.

This cycle challenges
the remaining structural
assumptions introduced
by SL-001 Version 0.2.

The objective
is reduction.

No lifecycle concept
shall survive
merely because
it provides
organizational convenience.

A concept shall remain
in the canonical lifecycle
only when removing it
would damage
normative integrity,
traceability,
or evolution.

---

## Refutation Questions

This cycle evaluates
four primary questions:

Is BASELINED
a lifecycle state?

Do VERIFYING
and IMPLEMENTING
belong to
the normative lifecycle?

Is RETIRED
a universal lifecycle state?

Are Lifecycle Profiles
necessary architecture
or premature complexity?

---

# R2-SL001-001

## Target

BASELINED

---

## Hypothesis

BASELINED
is a canonical
lifecycle state.

---

## Challenge

A baseline
does not necessarily
describe what
a specification
is doing.

It describes
the authority
and stability
of a particular
specification version.

A specification
may simultaneously be:

Published as
Baseline 1.0

while

Version 1.1
is under investigation.

Therefore
baseline status
belongs naturally
to a version,

not necessarily
to the lifecycle
of the specification
as a conceptual artifact.

---

## Counterexample

Specification A

Version 1.0

Baseline

while simultaneously:

Specification A

Version 2.0

Under Refutation.

If BASELINED
is modeled as
the state
of Specification A,

the model cannot
represent both conditions
without ambiguity.

---

## Result

REFUTED
as a universal
artifact lifecycle state.

---

## Finding

Baseline
is better modeled
as a normative
version status.

Candidate statuses
may include:

Draft.

Candidate.

Baseline.

Superseded.

Withdrawn.

The exact status model
requires independent
specification.

---

## Required Correction

Remove BASELINED
from the canonical
artifact lifecycle.

Preserve
Baseline Semantics
as a separate
version-governance concept.

---

# R2-SL001-002

## Target

VERIFYING

---

## Hypothesis

VERIFYING
is a canonical state
of the normative
specification lifecycle.

---

## Challenge

Verification
operates upon
normative claims.

It does not necessarily
change the lifecycle state
of the specification itself.

Multiple verification
activities may occur
against the same
normative version:

Structural Verification.

Behavioral Verification.

Semantic Verification.

Formal Verification.

Compatibility Verification.

Reproducibility Verification.

These may execute
repeatedly
and independently.

---

## Counterexample

A Baseline Specification
may remain unchanged

while its executable
contract runs
thousands of times.

The specification
does not repeatedly
transition into
and out of
VERIFYING.

The verification artifact
has its own lifecycle
and execution history.

---

## Result

REFUTED
as a canonical
specification lifecycle state.

---

## Finding

Verification
is a relation
between:

Normative Requirement.

Verification Mechanism.

Verification Evidence.

Verification Result.

It is not necessarily
a state
of the specification.

---

## Required Correction

Remove VERIFYING
from the canonical
specification lifecycle.

Retain
Verification Semantics
as an associated
normative mechanism.

---

# R2-SL001-003

## Target

IMPLEMENTING

---

## Hypothesis

IMPLEMENTING
belongs to
the canonical
specification lifecycle.

---

## Challenge

Implementation
is downstream
from specification.

Multiple implementations
may conform
to the same specification.

For example:

Python Reference Runtime.

Rust Reference Runtime.

WASM Runtime.

Commercial Runtime.

Experimental Runtime.

Each implementation
possesses
its own identity,
version,
artifact lifecycle,
verification evidence,
and deployment lifecycle.

The normative specification
does not become
IMPLEMENTING
because an implementation
is being created.

---

## Counterexample

Specification S
remains Baseline 1.0.

Implementation A
is production-ready.

Implementation B
is experimental.

Implementation C
has been retired.

One specification
therefore relates
simultaneously
to multiple
implementation states.

Representing IMPLEMENTING
as the state
of S
collapses independent
lifecycles.

---

## Result

REFUTED.

---

## Finding

Specification Lifecycle

and

Implementation Lifecycle

are distinct.

They may interact.

They shall not
be conflated.

---

## Required Correction

Remove IMPLEMENTING
from the canonical
Specification Lifecycle.

Define
implementation relationships
outside SL-001
or through
a future independent
artifact lifecycle.

---

# R2-SL001-004

## Target

VALIDATING

---

## Hypothesis

VALIDATING
is a canonical
Specification Lifecycle state.

---

## Challenge

Operational,
commercial,
scientific,
security,
and regulatory validation

may occur
against:

Specifications.

Contracts.

Implementations.

Runtime executions.

Commercial products.

Validation therefore
crosses artifact boundaries.

---

## Counterexample

A normative specification
may remain unchanged

while:

one implementation
passes commercial validation,

another fails
security validation,

and a third
has not yet
been validated.

VALIDATING
cannot accurately describe
the state
of the specification
without collapsing
these relationships.

---

## Result

REFUTED
as a universal
specification state.

---

## Finding

Validation
is evidence
associated with
a target artifact,
claim,
implementation,
or deployment.

It is not necessarily
a state
of the governing
specification.

---

## Required Correction

Remove VALIDATING
from the minimal
Specification Lifecycle.

Preserve validation
as a cross-artifact
evidence relation.

---

# R2-SL001-005

## Target

RETIRED

---

## Hypothesis

RETIRED
is a universal
Specification Lifecycle state.

---

## Challenge

Retirement
may apply differently
to:

A specification family.

A specific version.

A normative requirement.

A Reference Implementation.

A commercial product.

A version
may be superseded
without the specification
family itself
being retired.

---

## Counterexample

SL-001 Version 1.0
may become superseded

while SL-001 Version 2.0
remains authoritative.

The specification
is not retired.

Only a version
lost authority.

---

## Result

PARTIALLY REFUTED.

---

## Finding

Retirement
is meaningful,

but its target
must be explicit.

For specification versions,
the more precise concept
may be:

Superseded.

Withdrawn.

Deprecated.

Invalidated.

Retired
may remain useful
for artifact families
that cease to exist.

---

## Required Correction

Do not treat
RETIRED
as a mandatory
universal state.

Move retirement semantics
into version
and artifact governance.

---

# R2-SL001-006

## Target

EVOLVING

---

## Hypothesis

EVOLVING
is a distinct
Specification Lifecycle state.

---

## Challenge

Evolution
may simply mean
that new evidence
has triggered
a new normative version.

If so,

EVOLVING

duplicates the transition:

Trigger

↓

Investigation

↓

Specification Revision.

---

## Counterexample

Baseline 1.0
remains stable.

New evidence
triggers
Version 1.1.

Version 1.1
enters investigation.

No separate
EVOLVING state
is required.

---

## Result

REFUTED
as an irreducible state.

---

## Finding

Evolution
is a process
that creates
new lifecycle instances
or new specification versions.

It is not necessarily
a state
inside the minimal lifecycle.

---

## Required Correction

Remove EVOLVING
from the minimal
state model.

Preserve
Evolution Rules
as normative policy.

---

# R2-SL001-007

## Target

Lifecycle Profiles

---

## Hypothesis

Different normative
artifact families
require formal
Lifecycle Profiles.

---

## Challenge

Profiles introduce:

Additional artifacts.

Additional terminology.

Additional conformance rules.

Additional maintenance.

Additional possibility
of divergence.

If the common lifecycle
is sufficiently minimal,

different artifact families
may not require
formal profiles.

They may only require
different promotion criteria.

---

## Reduction Test

Candidate minimal lifecycle:

TRIGGERED

↓

INVESTIGATING

↓

SPECIFYING

↓

UNDER_REVIEW

↓

UNDER_REFUTATION

with iterative
backward transitions.

Version authority,
verification,
implementation,
validation,
and retirement

exist outside
the minimal state model.

Under this reduction,

Foundation Specifications,

Constitutional Principles,

Architecture Principles,

and Domain Specifications

can potentially use
the same lifecycle.

---

## Result

NOT PROVEN NECESSARY.

---

## Finding

Lifecycle Profiles
are currently
premature architecture.

No evidence
yet demonstrates
that they are required.

---

## Required Correction

Remove Lifecycle Profiles
from the canonical
minimal model.

Artifact families
may define
their own
promotion criteria

without creating
a formal
Profile abstraction.

Lifecycle Profiles
may return
only if
future evidence
demonstrates necessity.

---

# R2-SL001-008

## Target

UNDER_REFUTATION

---

## Hypothesis

UNDER_REFUTATION
must be
a distinct state
from UNDER_REVIEW.

---

## Challenge

Refutation
may simply be
one specialized
form of review.

If so,
two states
may unnecessarily
increase complexity.

---

## Reduction Test

UNDER_REVIEW

could include:

Consistency Review.

Compatibility Review.

Architectural Review.

Refutation.

Counterexample Analysis.

---

## Counterargument

Refutation
has a materially
different epistemic purpose.

Review asks:

Is the specification
well formed?

Refutation asks:

Is the underlying
claim wrong?

A specification
may pass
structural review

and fail
foundational refutation.

---

## Result

SURVIVES.

---

## Finding

UNDER_REFUTATION
shall remain distinct
for foundational
or architecturally significant
normative claims.

Not every minor
normative change
necessarily requires
the same depth
of refutation.

---

# R2-SL001-009

## Target

TRIGGERED

---

## Hypothesis

TRIGGERED
is a meaningful
minimal lifecycle state.

---

## Challenge

A trigger
could be modeled
as metadata
rather than
a lifecycle state.

---

## Reduction Test

Could the lifecycle
start directly at:

INVESTIGATING?

Yes.

But doing so
would lose
the explicit relationship
between normative work
and the evidence
that justified
starting it.

---

## Result

SURVIVES.

---

## Finding

TRIGGERED
preserves
causal traceability.

A normative artifact
should be able
to answer:

Why did this
work begin?

---

# R2-SL001-010

## Target

INVESTIGATING

---

## Hypothesis

INVESTIGATING
is irreducible.

---

## Challenge

Investigation
could potentially
be merged
into SPECIFYING.

---

## Counterexample

A problem
may be investigated

and ultimately produce
no specification.

Research may conclude:

No new architecture
is required.

Existing specification
is sufficient.

The hypothesis
is invalid.

The commercial problem
belongs entirely
to a Domain Runtime.

Therefore
investigation exists
independently
of specification production.

---

## Result

SURVIVES.

---

# R2-SL001-011

## Target

SPECIFYING

---

## Hypothesis

SPECIFYING
is irreducible.

---

## Challenge

Could a specification
move directly
from investigation
to review?

No.

There must exist
a candidate
normative representation
to review.

---

## Result

SURVIVES.

---

# R2-SL001-012

## Target

UNDER_REVIEW

---

## Hypothesis

UNDER_REVIEW
is irreducible.

---

## Challenge

Could refutation
replace review?

No.

Refutation tests
the validity
of claims.

It does not necessarily
detect:

Ambiguous wording.

Broken references.

Missing scope.

Version inconsistencies.

Compatibility errors.

Normative contradictions.

---

## Result

SURVIVES.

---

# Minimal Lifecycle Candidate

After the second
refutation cycle,

the candidate
minimal Specification Lifecycle
is:

TRIGGERED

↓

INVESTIGATING

↓

SPECIFYING

↓

UNDER_REVIEW

↓

UNDER_REFUTATION

↓

CANDIDATE FOR BASELINE

The final step
does not imply
that Baseline
is a lifecycle state.

It means
the specification version
has completed
the lifecycle required
to become eligible
for normative authority.

---

# Separate Concern Model

The following concepts
shall no longer
be assumed
to belong
to the minimal
Specification Lifecycle:

Baseline Status.

Verification.

Executable Contracts.

Implementation.

Validation.

Commercial Validation.

Evolution.

Retirement.

Lifecycle Profiles.

These remain
important concepts.

They require
correct architectural
placement.

---

# Emerging Architecture

The second
refutation cycle
suggests
at least four
separate concerns:

Specification Lifecycle

Version Authority

Verification Model

Implementation Lifecycle

Potentially:

Validation Model

Evidence Lifecycle

These concerns
shall not yet
be promoted
to architecture.

They remain
research findings.

---

# Critical Finding

The previous
SL-001 model
mixed:

Normative knowledge
maturation

with

downstream artifact
lifecycles.

This produced
unnecessary coupling.

The minimal
Specification Lifecycle
should describe only

how a normative proposition
becomes eligible
for authority.

It should not describe

how implementations
are built,

how contracts
are executed,

how products
are validated,

or how runtime artifacts
are deployed.

---

# Second Refutation Outcome

Target

SL-001 Version 0.2 Draft.

Outcome

REFUTED IN PART.

Core lifecycle

SURVIVES.

Extended lifecycle

DOES NOT SURVIVE.

Lifecycle Profiles

NOT JUSTIFIED.

Disposition

REDUCE.

Freeze

PROHIBITED.

---

# Surviving Candidate

TRIGGERED

INVESTIGATING

SPECIFYING

UNDER_REVIEW

UNDER_REFUTATION

CANDIDATE FOR BASELINE

---

# Research Principle Reinforced

Complexity
shall require
evidence.

An abstraction
that can be removed

without reducing

normative integrity,

traceability,

or reproducibility

does not belong

in the minimal
Specification Lifecycle.

---

# End of Refutation Cycle 2
