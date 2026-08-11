# NAM-001 Refutation Cycle 3

Target

NAM-001 Version 0.3 Draft

Title

Typed Authority
Relationship and
Transition Model

Refutation Type

Minimality,
Determinism,
and Replay Testing

Status

Research

---

## Purpose

Determine whether
NAM-001 Version 0.3

contains redundant
semantic dimensions,

ambiguous transition semantics,

or insufficient
historical reconstruction rules.

The objective
is to test whether
current and historical
authority can be
reconstructed deterministically

without unnecessary
model complexity.

---

## Governing Authority

This investigation
is subordinate to:

RC-001
Repository Constitution
Baseline 1.0.

SL-001
Repository Specification Lifecycle
Baseline 1.0.

APC-001
Architecture Principle
Classification Baseline 1.0.

NAM-001 remains
non-authoritative.

---

# MD-001 — Disposition versus Effectivity

## Attack

Could Authority Disposition
and Effectivity
be collapsed
into one field?

## Analysis

No.

A relationship
may be:

ESTABLISHED

but

NOT_YET_EFFECTIVE.

Likewise,

a relationship
may remain
ESTABLISHED

while being
NOT_APPLICABLE
under current conditions.

## Result

DISTINCT.

---

# MD-002 — Effectivity versus Applicability

## Attack

Could Effectivity
and Applicability
be merged?

## Analysis

No.

Effectivity answers:

Is the relationship
currently effective
at Evaluation Time?

Applicability answers:

Does the relationship
govern
the evaluated claim
under current conditions?

An EFFECTIVE
relationship
may be
NOT_APPLICABLE.

## Result

DISTINCT.

---

# MD-003 — Candidate Status versus Disposition

## Attack

Should CANDIDATE
be reintroduced
as an Authority Disposition?

## Analysis

No.

Candidate status
does not establish
normative authority.

It describes
maturation state
or eligibility.

## Result

KEEP EXTERNAL.

---

# MD-004 — Historical Perspective versus Disposition

## Attack

Should HISTORICAL
be an Authority Disposition?

## Analysis

No.

Historical perspective
depends upon
Evaluation Time.

A currently
SUPERSEDED relationship
may have been
ESTABLISHED
and effective
historically.

## Result

KEEP DERIVED.

---

# MD-005 — SUSPENDED as Disposition

## Attack

Is SUSPENDED
truly a disposition

or merely
effectivity state?

## Analysis

Suspension
is an explicit
authority transition

that changes
the normative availability
of the relationship.

It must remain
historically traceable.

Pure effectivity
cannot preserve
the suspension cause.

## Result

RETAIN AS DISPOSITION.

---

# MD-006 — EXPIRED as Effectivity

## Attack

Should EXPIRED
be a disposition?

## Analysis

No.

Expiration
results from
temporal evaluation
against an
effective interval.

No independent
normative disposition
is required.

## Result

RETAIN AS EFFECTIVITY.

---

# MD-007 — TERMINATED Effectivity

## Attack

Is TERMINATED
independently necessary

when disposition
may already be:

WITHDRAWN.

INVALIDATED.

SUPERSEDED.

## Analysis

Potentially yes.

TERMINATED
provides a normalized
effectivity result

derived from
different terminal
dispositions.

It avoids forcing
consumers
to interpret
each disposition
when asking only
whether authority
is currently effective.

## Result

RETAIN.

---

# MD-008 — ESTABLISH Transition

## Attack

Is ESTABLISH
redundant
with creation
of the relationship record?

## Analysis

No.

Record creation
and normative
authority establishment
must remain distinct.

An artifact record
may exist
before authority
is established.

## Result

RETAIN.

---

# MD-009 — EXPIRE Transition

## Attack

Does EXPIRE
need to exist
as a transition

if expiration
is derived automatically
from Effective End?

## Analysis

Not necessarily.

Temporal expiration
can be derived
from interval semantics.

An explicit EXPIRE
transition would be required
only when
a governing mechanism
terminates authority

through a normative event
rather than
natural interval completion.

## Result

POTENTIAL REDUNDANCY.

---

# MD-010 — REPLACE versus SUPERSEDE

## Attack

Are REPLACE
and SUPERSEDE
semantically distinct
transition types?

## Analysis

Insufficiently.

SUPERSEDE already
represents explicit
replacement
of one authority relationship
by a successor.

REPLACE
does not currently
define an independent
transition meaning.

## Result

REDUNDANT
UNLESS FURTHER JUSTIFIED.

---

# MD-011 — AMEND_SCOPE

## Attack

Can scope amendment
occur on the same
relationship identity?

## Analysis

Potentially,

but material scope change
may alter
the normative identity
of the relationship.

The model currently
does not define
the boundary.

## Result

IDENTITY RULE
REQUIRES CLARIFICATION.

---

# MD-012 — AMEND_CONDITION

## Attack

Can applicability conditions
change
without creating
a new relationship?

## Analysis

Only when
the amendment
does not materially
change normative identity.

The boundary
must remain explicit.

## Result

IDENTITY RULE
REQUIRES CLARIFICATION.

---

# MD-013 — AMEND_INTERVAL

## Attack

Can temporal boundaries
change
on the same relationship?

## Analysis

Yes,
through explicit
transition evidence,

provided historical
authority is not
silently rewritten.

Retroactive amendment
requires separate
authorization.

## Result

RETAIN.

---

# MD-014 — ROOT_SUSPEND Transition

## Attack

Is ROOT_SUSPEND
a special transition

or simply
SUSPEND
applied to
an Authority Root?

## Analysis

Semantically
it is a specialization
of SUSPEND.

The special type
may be unnecessary
if target type
is explicit.

## Result

POTENTIAL REDUNDANCY.

---

# MD-015 — ROOT_INVALIDATE Transition

## Attack

Is ROOT_INVALIDATE
different from INVALIDATE?

## Analysis

The same
invalidation semantics
may apply

with root-specific
dependency consequences.

The root identity
can be represented
by the transition target.

## Result

POTENTIAL REDUNDANCY.

---

# MD-016 — ROOT_REPLACE Transition

## Attack

Is ROOT_REPLACE
independent
from SUPERSEDE?

## Analysis

Potentially not.

Replacing an Authority Root
may be modeled
as supersession

plus root-specific
dependency evaluation.

## Result

POTENTIAL REDUNDANCY.

---

# MD-017 — Relationship Type SUSPENSION

## Attack

Should SUSPENSION
exist as both:

Relationship Type.

and

Authority Disposition /
Transition?

## Analysis

No clear
independent relationship
semantics
have been demonstrated.

Suspension primarily
describes transition
and resulting disposition.

## Result

RELATIONSHIP TYPE
LIKELY REDUNDANT.

---

# MD-018 — Relationship Type INVALIDATION

## Attack

Should INVALIDATION
remain
a relationship type?

## Analysis

Invalidation
primarily represents
a transition
and resulting disposition.

It does not necessarily
define a durable
authority relationship.

## Result

RELATIONSHIP TYPE
LIKELY REDUNDANT.

---

# MD-019 — Relationship Type WITHDRAWAL

## Attack

Should WITHDRAWAL
remain
a relationship type?

## Analysis

Withdrawal
primarily represents
termination transition
and disposition.

## Result

RELATIONSHIP TYPE
LIKELY REDUNDANT.

---

# MD-020 — Relationship Type REVOCATION

## Attack

Should REVOCATION
remain
a relationship type?

## Analysis

Revocation
primarily represents
a transition
against another
authority relationship.

It may not deserve
relationship-type status.

## Result

LIKELY TRANSITION ONLY.

---

# MD-021 — Historical Predecessor as Authority Relationship

## Attack

Does
HISTORICAL_PREDECESSOR
represent authority

or merely lineage?

## Analysis

Lineage
does not itself
grant normative authority.

Historical predecessor
belongs more naturally
to transition/history metadata.

## Result

REMOVE FROM
AUTHORITY RELATIONSHIP TYPES.

---

# MD-022 — Subordination as Authority Relationship

## Attack

Does SUBORDINATION
belong in
the authority graph?

## Analysis

Yes.

It represents
an explicit
normative relationship

where one artifact
must conform
to another
within overlapping scope.

## Result

RETAIN.

---

# MD-023 — Supersession as Relationship Type

## Attack

Should SUPERSESSION
remain both
relationship type
and transition?

## Analysis

Supersession
is principally
an authority transition
and lineage relationship.

Its durable semantics
may be captured
through transition history
and successor linkage.

## Result

POTENTIAL DUPLICATION.

---

# MD-024 — Direct versus Derived Authority

## Attack

Can DIRECT_AUTHORITY
and DERIVED_AUTHORITY
be merged?

## Analysis

No.

The distinction
is necessary
for authority-source
analysis
and failure propagation.

## Result

RETAIN BOTH.

---

# MD-025 — Delegated versus Derived Authority

## Attack

Is delegation
just one form
of derived authority?

## Analysis

Delegated authority
is derived
in a broad sense,

but it includes
specific semantics:

Delegator.

Delegate.

Revocation.

Continued delegator authority.

These justify
independent typing.

## Result

RETAIN BOTH.

---

# MD-026 — Transferred versus Delegated Authority

## Attack

Can transfer
be modeled
as delegation
plus revocation?

## Analysis

Potentially,
but transfer
has distinct semantics:

Authority moves
to another holder.

Transferor authority
may terminate
within transferred scope.

The distinction
is operationally
and historically meaningful.

## Result

RETAIN BOTH.

---

# MD-027 — Classification Authority

## Attack

Could classification authority
be represented
as generic
derived authority?

## Analysis

It could,
but the semantic boundary
between:

Classification.

Promotion.

Candidate authority.

has already proven
architecturally important.

## Result

RETAIN.

---

# MD-028 — Lifecycle Authority

## Attack

Could lifecycle authority
be generic
derived authority?

## Analysis

Potentially,

but preserving
the distinction
prevents process authority
from silently becoming
semantic authority.

## Result

RETAIN.

---

# MD-029 — Promotion Authority

## Attack

Could promotion authority
be generic direct
or derived authority?

## Analysis

Technically yes,

but promotion
changes normative
authority itself.

Explicit typing
supports
authority-of-authority
validation.

## Result

RETAIN.

---

# MD-030 — Conflict Resolution Authority

## Attack

Could conflict-resolution
authority
be represented
as generic authority?

## Analysis

Potentially,

but explicit typing
prevents
ordinary authority
from silently acquiring
precedence power.

## Result

RETAIN.

---

# MD-031 — Joint Authority

## Attack

Can joint authority
be represented
as multiple
ordinary authority edges?

## Analysis

No.

Doing so
would incorrectly imply
individual possession
of authority.

## Result

RETAIN.

---

# MD-032 — Quorum Authority

## Attack

Can quorum authority
be represented
as joint authority
with a threshold?

## Analysis

Possibly.

Quorum Authority
may be a specialization
of Joint Authority

with an explicit
threshold rule.

The independent
top-level relationship type
may not be necessary.

## Result

REDUCTION CANDIDATE.

---

# MD-033 — Replay Determinism

## Scenario

Given identical:

Repository Authority Context.

Scope.

Evaluation Time.

Conditions.

Authority graph.

Transition history.

Configuration snapshot.

## Attack

Can two valid evaluators
produce different
effective authority sets?

## Analysis

They should not.

NAM-001 requires
deterministic evaluation,

but no explicit
determinism invariant
currently states this.

## Result

DETERMINISM
MUST BE EXPLICIT.

---

# MD-034 — Missing Configuration Snapshot

## Scenario

Historical replay
requires quorum authority,

but no pinned
Authority Configuration Snapshot
exists.

## Attack

Can replay
infer configuration
from current membership?

## Analysis

No.

Historical authority
is unresolved.

## Result

FAIL CLOSED
REQUIRED.

---

# MD-035 — Missing Historical Condition

## Scenario

Authority depends
on condition X.

Historical value
of X
cannot be reconstructed.

## Attack

Can replay assume
the condition
was satisfied?

## Analysis

No.

Historical applicability
must become unresolved.

## Result

FAIL CLOSED
REQUIRED.

---

# MD-036 — Missing Transition

## Scenario

Current metadata
says SUPERSEDED,

but the supersession
transition evidence
is absent.

## Attack

Can replay trust
the current disposition?

## Analysis

Not safely.

The authority history
is incomplete.

## Result

AUTHORITY AMBIGUITY.

---

# MD-037 — Conflicting Transition Order

## Scenario

Two transitions
have identical
effective time

and produce
different outcomes.

## Attack

Can file order
resolve them?

## Analysis

No.

Transition ordering
requires explicit
deterministic semantics.

## Result

TIE-BREAK RULE
OR CONFLICT REQUIRED.

---

# MD-038 — Same-Time Suspend and Invalidate

## Scenario

SUSPEND
and INVALIDATE

become effective
at the same instant.

## Attack

Which resulting
disposition wins?

## Analysis

The model
currently lacks
transition conflict
semantics.

Invalidation may
logically dominate
suspension,

but this shall not
be assumed.

## Result

TRANSITION CONFLICT
MODEL REQUIRED.

---

# MD-039 — Replay of Retroactive Change

## Scenario

At T3
a transition
retroactively changes
authority effective
from T1.

Replay is requested
for T2.

## Attack

Should replay use
knowledge available
at T2

or the authority model
as retrospectively corrected
at T3?

## Analysis

These are
different replay questions.

## Result

REPLAY MODE
DISTINCTION REQUIRED.

---

# MD-040 — Historical Knowledge Replay

## Required Distinction

Replay may ask:

What authority
was believed current
at T2?

or

What authority
is now considered
to have governed
at T2?

These are not
necessarily identical
under retroactive change.

## Result

TWO REPLAY MODES
REQUIRED.

---

# MD-041 — Current Projection Determinism

## Scenario

Current evaluation
uses the same
authority evidence twice.

## Attack

May results differ
because wall-clock time
advances
during evaluation?

## Analysis

No.

Evaluation Time
must be pinned
before projection.

## Result

TIME PINNING
REQUIRED.

---

# MD-042 — Quorum Determinism

## Scenario

The same quorum
evidence
is evaluated twice.

## Attack

Can dynamic membership
change the result?

## Analysis

No.

Pinned configuration
must control
the decision.

## Result

MODEL SURVIVES.

---

# MD-043 — Dependency Cycle

## Scenario

A depends upon B.

B depends upon A.

Both possess
valid authority roots.

## Attack

Can dependency evaluation
loop forever?

## Analysis

Yes,
without explicit
cycle handling.

## Result

EVALUATION
TERMINATION REQUIRED.

---

# MD-044 — Dependency Cycle Without Independent Root

## Scenario

A depends upon B.

B depends upon A.

Neither has
independent authority source.

## Result

INVALID
SELF-SUPPORTING
AUTHORITY CYCLE.

---

# MD-045 — Dependency Cycle With Independent Roots

## Scenario

A and B
each possess
independent valid roots

but also depend
upon one another
for bounded conditions.

## Analysis

The cycle
may be valid,

provided evaluation
terminates
and no authority
is created
through the cycle.

## Result

GRAPH CYCLE
NOT AUTOMATICALLY
INVALID.

---

# MD-046 — Edge Minimality

## Attack

Does explicit
Dependency Relationship
risk reintroducing
all repository dependencies
into the authority graph?

## Analysis

Yes.

Only dependencies
that affect
normative authority
shall qualify.

## Result

RETAIN MINIMALITY RULE.

---

# MD-047 — Stable Identity Over Scope Amendment

## Scenario

Authority scope
changes from S1
to S1 + S2.

## Attack

Is this
the same relationship?

## Analysis

Not always.

A material expansion
may constitute
new normative identity.

## Result

MATERIALITY TEST
REQUIRED.

---

# MD-048 — Stable Identity Over Narrowing

## Scenario

Scope changes
from S1 + S2
to S1.

## Attack

Can identity remain
the same?

## Analysis

Possibly,

if the governing
authority model
treats narrowing
as amendment

and preserves
historical scope.

## Result

IDENTITY MAY SURVIVE
WITH TRACEABLE AMENDMENT.

---

# MD-049 — Stable Identity Over Authority Source Change

## Scenario

The same target
and scope
receive authority
from a new
authority source.

## Attack

Is relationship identity
unchanged?

## Analysis

Likely not.

Authority source
is fundamental
to normative identity.

## Result

NEW RELATIONSHIP
LIKELY REQUIRED.

---

# MD-050 — Minimal Model Question

## Question

Can NAM-001 v0.3
be reduced

without losing
deterministic
authority evaluation?

## Analysis

Yes.

Several current
relationship types
are better represented
as transitions
or history metadata.

Several transition types
are specializations
of more general
transition semantics.

The dimensional separation
introduced in v0.3
is necessary,

but the taxonomy
remains inflated.

## Result

REDUCTION REQUIRED.

---

# Refutation Findings

NAM-001 Version 0.3
survives
the separation of:

Disposition.

Effectivity.

Applicability.

Candidate status.

Historical perspective.

Evaluation time.

That decomposition
is necessary
for deterministic
authority evaluation.

However,
the current relationship
and transition taxonomies
contain redundancy.

---

# Relationship Type Reduction

The following
relationship types
remain strongly justified:

DIRECT_AUTHORITY.

DERIVED_AUTHORITY.

DELEGATED_AUTHORITY.

TRANSFERRED_AUTHORITY.

CLASSIFICATION_AUTHORITY.

LIFECYCLE_AUTHORITY.

PROMOTION_AUTHORITY.

CONFLICT_RESOLUTION_AUTHORITY.

JOINT_AUTHORITY.

SUBORDINATION.

---

The following
require reduction
or relocation:

QUORUM_AUTHORITY

may become
Joint Authority
with quorum rule.

SUPERSESSION

is primarily
transition and lineage.

REVOCATION

is primarily
transition.

WITHDRAWAL

is primarily
transition.

SUSPENSION

is primarily
transition
plus disposition.

INVALIDATION

is primarily
transition
plus disposition.

HISTORICAL_PREDECESSOR

is lineage metadata.

---

# Transition Type Reduction

Strongly justified
transition semantics include:

ESTABLISH.

SUSPEND.

REACTIVATE.

SUPERSEDE.

WITHDRAW.

INVALIDATE.

DELEGATE.

TRANSFER.

REVOKE.

AMEND_SCOPE.

AMEND_CONDITION.

AMEND_INTERVAL.

---

Potential reductions:

EXPIRE

may be derived
from interval completion.

REPLACE

may be redundant
with SUPERSEDE.

ROOT_SUSPEND

may specialize
SUSPEND.

ROOT_INVALIDATE

may specialize
INVALIDATE.

ROOT_REPLACE

may specialize
SUPERSEDE.

---

# Determinism Finding

Authority evaluation
shall be deterministic.

Given identical:

Repository Authority Context.

Scope.

Evaluation Time.

Conditions.

Authority evidence.

Transition history.

Dependency evidence.

Authority root evidence.

Pinned configuration.

an evaluator
shall produce
the same
Effective Authority Projection

or the same
explicit unresolved result.

File order.

Wall-clock drift.

Current configuration.

Implementation-specific
iteration order.

shall not alter
the result.

---

# Fail-Closed Finding

Authority evaluation
shall not invent
missing evidence.

Where required
historical or current
authority evidence
is unavailable,

evaluation shall produce
an explicit unresolved
or non-authoritative result

rather than
assuming authority.

This applies to
missing:

Authority source.

Transition history.

Configuration snapshot.

Historical condition.

Dependency evidence.

Conflict rule.

---

# Replay Mode Finding

Historical authority replay
requires at least
two distinct modes.

KNOWLEDGE_AT_TIME.

Reconstruct:

What authority
could have been
determined

from evidence
available
at the historical time?

---

RETROSPECTIVE_AUTHORITY.

Reconstruct:

What authority
is currently considered
to have governed

the historical time

after accounting
for authorized
retroactive transitions?

These modes
shall not be conflated.

---

# Transition Conflict Finding

Transitions sharing
the same
effective time

and overlapping
relationship scope

shall require
deterministic
conflict semantics.

File order
shall not resolve
transition conflict.

If no explicit
resolution exists,

authority evaluation
shall become
UNRESOLVED.

---

# Identity Materiality Finding

Stable relationship identity
requires a materiality rule.

Changes to:

Authority Source.

Repository Authority Context.

Fundamental relationship type.

Fundamental target identity.

shall ordinarily
require
new relationship identity.

Changes to:

Scope.

Conditions.

Temporal interval.

may preserve identity
only when
explicit amendment semantics
permit it

and historical
values remain traceable.

---

# Evaluation Termination Finding

Authority graph evaluation
shall terminate.

Dependency or authority
cycles
shall not cause
unbounded evaluation.

Cycles
shall be evaluated
without allowing
authority creation
through circular support.

---

# Minimality Outcome

NAM-001 v0.3

is not minimal.

Its semantic dimensions
survive.

Its taxonomies
require reduction.

The next revision
should reduce
relationship types

from 17
toward approximately 10

and transition types

from 17
toward approximately 12,

subject to
direct verification.

---

# Refutation Outcome

Target

NAM-001 Version 0.3 Draft.

Outcome

REFUTED
ON TAXONOMY
MINIMALITY.

Disposition /
Effectivity /
Applicability
Separation

SURVIVES.

Evaluation Time

SURVIVES.

Explicit Transition Model

SURVIVES.

Historical Replay

SURVIVES
WITH TWO MODES.

Determinism

REQUIRED
EXPLICITLY.

Fail-Closed Evaluation

REQUIRED.

Relationship Taxonomy

REDUCE.

Transition Taxonomy

REDUCE.

Identity Materiality Rule

REQUIRED.

Evaluation Termination

REQUIRED.

Authority

NONE.

Promotion

PROHIBITED.

Next Required Activity

NAM-001 Version 0.4

Reduced Deterministic
Authority Model.

---

# End of NAM-001 Refutation Cycle 3
