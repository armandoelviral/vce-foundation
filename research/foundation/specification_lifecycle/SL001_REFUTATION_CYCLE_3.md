# SL-001 Refutation Cycle 3

Title

Repository Specification Lifecycle
Third Refutation Cycle

Target

SL-001 Version 0.3 Draft

Version

0.1

Status

Research

---

## Purpose

Determine whether
the concepts

CANDIDATE_FOR_BASELINE,

Promotion Gate,

and

Version Authority

represent

three distinct
architectural concerns

or unnecessary
semantic duplication.

The objective
is reduction.

Concepts shall survive
only when removing them
would reduce

normative clarity,

authority traceability,

version integrity,

or promotion safety.

---

## Refutation Questions

This cycle asks:

Is CANDIDATE_FOR_BASELINE
a lifecycle state
or merely eligibility metadata?

Is Promotion Gate
a distinct architectural mechanism
or simply the transition
that grants authority?

Is Version Authority
a separate concern
or merely the result
of promotion?

Can these concepts
be reduced
without losing semantics?

---

# R3-SL001-001

## Target

CANDIDATE_FOR_BASELINE

---

## Hypothesis

CANDIDATE_FOR_BASELINE
is a necessary
Specification Lifecycle state.

---

## Challenge

The state appears
to express only:

all required
maturation work
has completed.

That may be
an eligibility condition,

not a meaningful
behavioral state.

A specification
under refutation
can become
eligible for promotion
the instant
its final blocking issue
is resolved.

No new activity
necessarily begins.

---

## Reduction Test

Replace:

UNDER_REFUTATION

↓

CANDIDATE_FOR_BASELINE

↓

Promotion Gate

with:

UNDER_REFUTATION

↓

Promotion Eligibility Satisfied

↓

Promotion Gate

The resulting model
preserves all
promotion semantics.

---

## Result

REFUTED
as a mandatory
lifecycle state.

---

## Finding

Candidate status
is better modeled
as a promotion
eligibility condition.

It describes
whether required
maturation criteria
have been satisfied.

It does not necessarily
describe a distinct
lifecycle activity.

---

## Required Correction

Remove

CANDIDATE_FOR_BASELINE

from the minimal
Specification Lifecycle.

Replace it with:

Promotion Eligibility.

---

# R3-SL001-002

## Target

Promotion Eligibility

---

## Hypothesis

Promotion Eligibility
must remain
explicit.

---

## Challenge

Could Promotion Gate
itself determine eligibility
without a separate concept?

Yes.

But combining
eligibility assessment
with authority assignment
would merge two
different questions:

Has the candidate
satisfied prerequisite criteria?

and

Shall normative authority
be granted?

---

## Counterexample

A candidate may satisfy
all technical
promotion criteria

but remain
unpromoted because:

Required approval
is missing.

Release window
is closed.

Regulatory review
is pending.

Conflicting version
authority exists.

Repository governance
blocks publication.

Thus:

Eligible

does not imply

Promoted.

---

## Result

SURVIVES
as a distinct
promotion concept.

---

## Finding

Promotion Eligibility
and Promotion Decision
shall remain separate.

---

# R3-SL001-003

## Target

Promotion Gate

---

## Hypothesis

Promotion Gate
is a distinct
architectural mechanism.

---

## Challenge

Could promotion
simply be modeled
as a state transition?

For example:

Draft

↓

Baseline

without a named
Promotion Gate.

---

## Counterexample

Normative authority
must not emerge
implicitly.

A transition
from candidate
to baseline
requires an explicit
decision point
that evaluates:

Eligibility.

Required approvals.

Compatibility impact.

Conflicting authority.

Governance constraints.

Release policy.

Without an explicit
promotion mechanism,

authority may appear
as an accidental
metadata change.

---

## Result

SURVIVES.

---

## Finding

Promotion Gate
is not a lifecycle state.

It is an explicit
authority-granting
decision mechanism.

Its purpose is to answer:

May this identified
specification version
receive normative authority?

---

# R3-SL001-004

## Target

Version Authority

---

## Hypothesis

Version Authority
is a distinct
architectural concern.

---

## Challenge

Could Version Authority
be represented
only by:

version number
+
Promotion result?

Potentially.

If Promotion Gate
produces PROMOTED,

why also require
Version Authority?

---

## Counterexample

Authority continues
after promotion.

A version may later become:

Superseded.

Withdrawn.

Invalidated.

Deprecated.

Authority state
therefore persists
and evolves
independently
of the promotion event.

Promotion is an event.

Authority is a
continuing state
of an identified version.

---

## Result

SURVIVES.

---

## Finding

Promotion Gate

and

Version Authority

represent different
temporal concepts.

Promotion Gate
is an authority
transition event.

Version Authority
is persistent
normative status.

---

# R3-SL001-005

## Target

Baseline

---

## Hypothesis

Baseline is
the only useful
authoritative
version status.

---

## Challenge

Authority
is not binary.

Repository history
requires distinctions
between:

Current authority.

Historical authority.

Superseded authority.

Withdrawn authority.

Invalid authority.

---

## Counterexample

Version 1.0
may remain
historically authoritative

while Version 1.1
is current.

A compromised
Version 1.2
may need
explicit invalidation.

A draft
may be published
for review
without authority.

---

## Result

REFUTED.

---

## Finding

Version Authority
requires
a richer status model
than Baseline alone.

---

# R3-SL001-006

## Target

Candidate Version Status

---

## Hypothesis

Candidate
should exist
as a Version Authority status.

---

## Challenge

If candidacy
means only
promotion eligibility,

adding Candidate
to Version Authority
duplicates
Promotion Eligibility.

---

## Reduction Test

Authority statuses:

Draft.

Baseline.

Superseded.

Withdrawn.

Invalidated.

Promotion Eligibility
exists separately.

No semantic loss
is observed.

---

## Result

REFUTED
as necessary
Version Authority status.

---

## Finding

Candidate
belongs more naturally
to promotion semantics
than authority semantics.

---

# R3-SL001-007

## Target

Draft Version Authority

---

## Hypothesis

Draft
belongs to
Version Authority.

---

## Challenge

Draft describes
maturity,
not authority.

A Draft specification
has no normative authority.

Therefore
calling Draft
an authority state
may confuse
maturity
with authority.

---

## Result

REFUTED
as authority state.

---

## Finding

Version metadata
and Version Authority
shall remain distinct.

A version may have:

Maturity Status.

Authority Status.

These shall not
be conflated.

---

# R3-SL001-008

## Target

Version Authority Model

---

## Hypothesis

Version Authority
can be represented
with a minimal
authority state set.

---

## Reduction Test

Candidate authority statuses:

NONE.

AUTHORITATIVE.

SUPERSEDED.

WITHDRAWN.

INVALIDATED.

---

## Analysis

NONE

means
the version exists
but possesses
no normative authority.

AUTHORITATIVE

means
the version currently
possesses normative authority.

SUPERSEDED

means
authority has been replaced
by a later version
but historical traceability
remains.

WITHDRAWN

means
authority was intentionally
removed.

INVALIDATED

means
the version
must not be relied upon
because its normative validity
has been explicitly rejected.

---

## Result

SURVIVES
as a candidate
minimal authority model.

---

# R3-SL001-009

## Target

Promotion Gate Outcome

---

## Hypothesis

Promotion Gate
requires multiple outcomes.

---

## Reduction Test

Could promotion simply
produce:

PROMOTED

or

NOT_PROMOTED?

---

## Counterexample

Operationally distinct
non-promotion outcomes
matter.

For example:

REJECTED

means
the candidate failed
promotion.

DEFERRED

means
promotion remains possible
but intentionally postponed.

RETURN_TO_LIFECYCLE

means
additional maturation
is required.

These outcomes
have different
traceability semantics.

---

## Result

SURVIVES.

---

## Candidate Outcomes

PROMOTED.

REJECTED.

DEFERRED.

RETURN_TO_LIFECYCLE.

---

# R3-SL001-010

## Target

Promotion Gate and
Version Authority Coupling

---

## Hypothesis

A successful
Promotion Gate
must directly
assign Version Authority.

---

## Challenge

Could Promotion Gate
produce only
an approval record,

with a separate
authority system
activating the version?

That would introduce
additional indirection.

---

## Reduction Test

Promotion Gate

↓

PROMOTED

↓

Version Authority
becomes AUTHORITATIVE

This preserves:

Explicit decision.

Traceable authority change.

Minimal architecture.

---

## Result

SURVIVES.

---

## Finding

Successful Promotion
shall produce
an explicit
Version Authority transition.

Promotion
and authority
remain separate concepts,

but they are
normatively linked.

---

# R3-SL001-011

## Target

Single Authoritative Version

---

## Hypothesis

A specification family
may have exactly
one authoritative version
at a time.

---

## Challenge

Some migration models
may temporarily require
multiple supported
or authoritative versions.

Different consumers
may conform
to different
major versions.

---

## Result

NOT UNIVERSALLY VALID.

---

## Finding

SL-001
shall not define
single-version authority.

Cardinality
of authoritative versions
belongs to
Version Authority policy.

---

# R3-SL001-012

## Target

Authority as Lifecycle

---

## Hypothesis

Version Authority
could still be modeled
inside SL-001
for convenience.

---

## Counterexample

Authority can change
without restarting
the specification
maturation lifecycle.

For example:

AUTHORITATIVE

↓

SUPERSEDED

may occur
because another version
is promoted.

The superseded version
does not re-enter
investigation,
specification,
review,
or refutation.

---

## Result

REFUTED.

---

## Finding

Version Authority
must remain
outside
the minimal
Specification Lifecycle.

---

# Consolidated Reduction

SL-001 Version 0.3
currently contains:

TRIGGERED.

INVESTIGATING.

SPECIFYING.

UNDER_REVIEW.

UNDER_REFUTATION.

CANDIDATE_FOR_BASELINE.

The third
refutation cycle
removes:

CANDIDATE_FOR_BASELINE.

The minimal lifecycle
therefore becomes:

TRIGGERED.

INVESTIGATING.

SPECIFYING.

UNDER_REVIEW.

UNDER_REFUTATION.

After successful
maturation,

the lifecycle exposes:

Promotion Eligibility.

Promotion Eligibility
is not
a lifecycle state.

---

# Promotion Architecture Candidate

The candidate
promotion architecture is:

Specification Lifecycle

↓

Promotion Eligibility

↓

Promotion Gate

↓

Promotion Outcome

↓

Version Authority Transition

---

# Version Authority Candidate

Version Authority
is separate
from specification
maturation.

Candidate minimal
authority statuses:

NONE.

AUTHORITATIVE.

SUPERSEDED.

WITHDRAWN.

INVALIDATED.

Maturity metadata
such as:

Draft.

Under Review.

Under Refutation.

shall not be
represented as
Version Authority.

---

# Semantic Separation

Specification Lifecycle

answers:

How has this
normative proposition
matured?

Promotion Eligibility

answers:

Has it satisfied
the prerequisites
for authority consideration?

Promotion Gate

answers:

May authority
be granted?

Version Authority

answers:

What normative authority
does this identified
version currently possess?

These four questions
shall not be conflated.

---

# Critical Finding

The architecture
previously confused

maturity,

eligibility,

promotion,

and authority.

These are distinct
concerns.

The reduced model
preserves each
without requiring
additional lifecycle states.

---

# Third Refutation Outcome

Target

SL-001 Version 0.3 Draft.

Outcome

REFUTED IN PART.

Minimal Lifecycle

REDUCED.

Promotion Gate

SURVIVES.

Version Authority

SURVIVES.

Candidate for Baseline
Lifecycle State

REFUTED.

Promotion Eligibility

SURVIVES
as non-state semantics.

Freeze

STILL PROHIBITED.

---

# Surviving Minimal Lifecycle

TRIGGERED

↓

INVESTIGATING

↓

SPECIFYING

↓

UNDER_REVIEW

↓

UNDER_REFUTATION

---

# Post-Lifecycle Promotion

Promotion Eligibility

↓

Promotion Gate

↓

Version Authority

---

# Research Principle Reinforced

Minimal architecture
shall separate

process,

eligibility,

decision,

and authority.

Convenient terminology
shall not justify
semantic duplication.

---

# End of Refutation Cycle 3
