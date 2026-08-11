# NAM-001 Refutation Cycle 2

Target

NAM-001 Version 0.2 Draft

Title

Typed Authority
Relationship Model

Refutation Type

State,
Transition,
and Relationship
Adversarial Testing

Status

Research

---

## Purpose

Attempt to refute
NAM-001 Version 0.2

by attacking
the internal semantics
of:

Authority states.

Authority transitions.

Temporal applicability.

Conditional applicability.

Delegation.

Transfer.

Revocation.

Supersession.

Suspension.

Withdrawal.

Invalidation.

Joint authority.

Quorum authority.

Authority roots.

The objective
is to determine
whether the typed
authority relationship model

can produce
an unambiguous
current authority state

under adversarial
conditions.

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

# ST-001 — ACTIVE and SUSPENDED

## Scenario

The same
authority relationship

is recorded as:

ACTIVE.

and

SUSPENDED.

for the same:

Context.

Scope.

Effective interval.

## Attack

Can both states
simultaneously govern
the same authority instance?

## Analysis

No.

The model currently
enumerates states

but does not
explicitly define
state exclusivity.

## Result

STATE EXCLUSIVITY
REQUIRED.

---

# ST-002 — ACTIVE and INVALIDATED

## Scenario

An authority relationship
is ACTIVE

while an applicable
INVALIDATION
has already become
effective.

## Attack

Which state governs?

## Analysis

The effective
invalidation transition
must terminate
the prior active state.

## Result

TRANSITION PRECEDENCE
REQUIRED.

---

# ST-003 — SUSPENDED then ACTIVE

## Scenario

Authority is suspended.

The resolution condition
is later satisfied.

## Attack

Does authority
automatically return
to ACTIVE?

## Analysis

Not necessarily.

The model does not define
whether resolution
of a suspension condition

is sufficient
for reactivation

or whether
an explicit
reactivation transition
is required.

## Result

REACTIVATION
UNSPECIFIED.

---

# ST-004 — WITHDRAWN then ACTIVE

## Scenario

Authority is
explicitly withdrawn.

A later artifact
marks the same
authority relationship
ACTIVE.

## Attack

Can withdrawn authority
be reactivated?

## Analysis

The model
does not define
whether withdrawal
is terminal

or whether
a new authority
relationship
must be created.

## Result

TERMINALITY
UNSPECIFIED.

---

# ST-005 — INVALIDATED then ACTIVE

## Scenario

Authority is invalidated.

The same authority
relationship
later becomes ACTIVE.

## Attack

Can invalidated authority
be revived?

## Analysis

The model
does not explicitly
forbid revival.

Invalidation
should not silently
permit reactivation
of the same
authority instance.

## Result

INVALIDATION
TERMINALITY REQUIRED.

---

# ST-006 — EXPIRED then ACTIVE

## Scenario

A temporal authority
expires.

The effective end
is later changed.

## Attack

Does the original
authority become
ACTIVE retroactively?

## Analysis

Changing historical
temporal boundaries
would alter
past authority state.

Such mutation
requires explicit
authority and
historical treatment.

## Result

TEMPORAL MUTATION
REQUIRES CONTROL.

---

# ST-007 — SUPERSEDED then ACTIVE

## Scenario

Authority A
is superseded
by Authority B.

A later becomes
ACTIVE again.

## Attack

Is this restoration
or a new authority
relationship?

## Analysis

The distinction
is not defined.

Historical identity
requires that
reactivation
not silently erase
the supersession event.

## Result

RESTORATION SEMANTICS
REQUIRED.

---

# ST-008 — NONE versus CANDIDATE

## Scenario

An artifact
has:

Authority NONE.

and

State CANDIDATE.

## Attack

Is this contradictory?

## Analysis

Potentially no.

NONE describes
absence of
current normative authority.

CANDIDATE describes
candidate lifecycle
or authority eligibility.

The current model
treats both
as authority states,

creating semantic overlap.

## Result

STATE DIMENSIONS
CONFLATED.

---

# ST-009 — HISTORICAL versus SUPERSEDED

## Scenario

An authority
is SUPERSEDED

and therefore
also historical.

## Attack

Are these
mutually exclusive states?

## Analysis

No.

SUPERSEDED describes
why current authority ended.

HISTORICAL describes
temporal relationship
to current authority.

They are
different dimensions.

## Result

STATE TAXONOMY
CONFLATED.

---

# ST-010 — HISTORICAL versus INVALIDATED

## Scenario

An invalidated
authority
remains historically
important.

## Attack

Should it be
INVALIDATED
or HISTORICAL?

## Analysis

Both propositions
may be true.

The single-state
enumeration
cannot represent
both without loss.

## Result

SINGLE STATE MODEL
REFUTED.

---

# ST-011 — Historical Authority Instance

## Scenario

Authority was ACTIVE
from T1 to T2.

It was superseded
at T2.

## Attack

What is its
historical state
for a replay
at T1.5?

## Analysis

For historical evaluation
at T1.5

the authority
was ACTIVE.

For present evaluation
it is SUPERSEDED.

Authority evaluation
therefore requires
an evaluation time.

## Result

EVALUATION TIME
REQUIRED.

---

# ST-012 — Retroactive Revocation

## Scenario

A delegation
was valid
from T1.

At T3
a revocation claims
effect from T2.

## Attack

Can revocation
retroactively alter
authority?

## Analysis

Potentially,
but only under
explicitly authorized
retroactivity semantics.

The current model
does not define this.

## Result

RETROACTIVITY
UNSPECIFIED.

---

# ST-013 — Retroactive Invalidation

## Scenario

At T3
an authority is
declared invalid
since T1.

## Attack

Does this mean
the authority
never existed,

or that it existed
but is now
retroactively invalidated?

## Analysis

These are
different historical claims.

The model
does not distinguish them.

## Result

HISTORICAL VALIDITY
SEMANTICS REQUIRED.

---

# ST-014 — Temporal Overlap

## Scenario

Authority A
is active
from T1 to T5.

Authority B
claims the same
scope
from T4 to T8.

## Attack

What governs
between T4 and T5?

## Analysis

Temporal overlap
creates simultaneous
applicability.

Conflict or compatibility
must be evaluated
within the overlap.

## Result

INTERVAL OVERLAP
SEMANTICS REQUIRED.

---

# ST-015 — Zero-Length Authority

## Scenario

Effective Start
equals
Effective End.

## Attack

Does authority
exist?

## Analysis

The model
does not define
interval boundary
semantics.

## Result

TEMPORAL BOUNDARY
SEMANTICS REQUIRED.

---

# ST-016 — Open-Ended Authority

## Scenario

Authority possesses
Effective Start

but no
Effective End.

## Attack

Is authority
indefinite?

## Analysis

Potentially yes,

subject to later
authority transitions.

Open intervals
must be explicit.

## Result

MODEL SURVIVES
WITH CLARIFICATION.

---

# ST-017 — Future Authority

## Scenario

A promotion
is approved today

with an effective
start tomorrow.

## Attack

Is the artifact
currently ACTIVE?

## Analysis

No.

Approved authority
and currently effective
authority
are distinct.

## Result

APPROVAL AND EFFECTIVITY
MUST REMAIN DISTINCT.

---

# ST-018 — Condition Becomes False

## Scenario

Conditional authority
is ACTIVE
while condition X
is true.

X becomes false.

## Attack

Does authority
automatically cease
to apply?

## Analysis

If condition X
is part of
applicability semantics,
yes.

But this is
non-applicability,

not necessarily
withdrawal,
suspension,
or invalidation.

## Result

APPLICABILITY
DISTINCT FROM STATE.

---

# ST-019 — Condition Becomes True Again

## Scenario

Condition X
becomes false
and later true.

## Attack

Does authority
require reactivation?

## Analysis

Not if
the authority relationship
remained valid
and only applicability
changed.

## Result

STATE AND APPLICABILITY
MUST BE SEPARATED.

---

# ST-020 — Ambiguous Condition

## Scenario

Authority applies
when:

"security conditions
are acceptable."

## Attack

Can applicability
be deterministically
evaluated?

## Analysis

No.

Authority conditions
must possess
determinable semantics.

## Result

CONDITION
DETERMINABILITY REQUIRED.

---

# ST-021 — Delegation After Source Suspension

## Scenario

A delegates
authority to B.

A is later
SUSPENDED.

## Attack

Does B's
delegated authority
remain active?

## Analysis

The model
does not specify
whether delegation
depends continuously
upon source authority.

## Result

DERIVATION DEPENDENCY
REQUIRED.

---

# ST-022 — Delegation After Source Invalidation

## Scenario

A delegates
authority to B.

A's authority
is later
INVALIDATED.

## Attack

Does B retain
delegated authority?

## Analysis

Not automatically.

The answer depends
upon whether
the delegation
was independently
stabilized
by another
authority mechanism.

## Result

DEPENDENCY SEMANTICS
REQUIRED.

---

# ST-023 — Delegation Chain

## Scenario

A delegates to B.

B delegates
a subset to C.

A revokes B.

## Attack

What happens
to C?

## Analysis

If C depends
solely upon B's
delegated authority,

C's authority
must cease
or become inapplicable.

## Result

TRANSITIVE REVOCATION
SEMANTICS REQUIRED.

---

# ST-024 — Transfer and Residual Authority

## Scenario

A transfers
scope S
to B.

A continues
claiming authority
over subset S1
inside S.

## Attack

Is residual authority
valid?

## Analysis

Only if
the transfer
explicitly retained
that subset.

## Result

TRANSFER SCOPE
SUBTRACTION REQUIRED.

---

# ST-025 — Partial Transfer

## Scenario

A possesses
authority over:

S1.

S2.

S3.

A transfers
only S2
to B.

## Attack

Does A lose
S1 and S3?

## Analysis

No.

Transfer must operate
on explicit scope.

## Result

MODEL SURVIVES.

---

# ST-026 — Conflicting Transfers

## Scenario

A transfers
the same scope
to B

and independently
to C.

## Attack

Can both
be valid?

## Analysis

Not unless
joint authority
was explicitly intended.

Otherwise
a conflict exists.

## Result

TRANSFER CONFLICT
SEMANTICS REQUIRED.

---

# ST-027 — Joint Authority Missing Member

## Scenario

A,
B,
and C

jointly possess
authority.

C is suspended.

## Attack

Can A and B
still act?

## Analysis

Only if
the joint decision rule
defines behavior
for unavailable members.

## Result

JOINT AVAILABILITY
SEMANTICS REQUIRED.

---

# ST-028 — Joint Authority Member Withdraws

## Scenario

One participant
withdraws
from a joint
authority relationship.

## Attack

Does the joint authority
continue?

## Analysis

The relationship
may become unsatisfied
or require
explicit reconstitution.

## Result

JOINT MEMBERSHIP
TRANSITION REQUIRED.

---

# ST-029 — Quorum Membership Change

## Scenario

A quorum
requires
3 of 5 participants.

During evaluation,
membership changes
to 4 participants.

## Attack

Which membership set
governs the decision?

## Analysis

The authority decision
requires a stable
evaluation snapshot.

## Result

AUTHORITY SNAPSHOT
REQUIRED.

---

# ST-030 — Quorum Threshold Change

## Scenario

Threshold changes
from 3 of 5
to 4 of 5

while a promotion
decision
is in progress.

## Attack

Which threshold applies?

## Analysis

The applicable
authority configuration
must be pinned
to the decision context.

## Result

CONFIGURATION PINNING
REQUIRED.

---

# ST-031 — Quorum Self-Modification

## Scenario

A quorum
uses its own authority

to reduce
the threshold
required
to exercise
that authority.

## Attack

Can authority rules
modify themselves?

## Analysis

Only if
the governing
authority source
explicitly permits
self-amendment

under defined
constraints.

## Result

SELF-AMENDMENT
REQUIRES GOVERNANCE.

---

# ST-032 — Authority Root Suspension

## Scenario

An authority root
is suspended.

## Attack

Do all
derived authority
relationships
immediately cease?

## Analysis

The current model
does not define
root-compromise
or root-suspension
propagation.

## Result

ROOT DEPENDENCY
SEMANTICS REQUIRED.

---

# ST-033 — Authority Root Invalidation

## Scenario

A root
is invalidated.

Thousands of
authority relationships
derive from it.

## Attack

Are all descendants
retroactively invalid?

## Analysis

Not necessarily.

Current validity,
historical validity,
and retroactive validity

must remain
separate questions.

## Result

ROOT FAILURE
MODEL REQUIRED.

---

# ST-034 — Compromised Authority Root

## Scenario

A cryptographic
or institutional
authority root

is discovered
to have been compromised
at unknown time.

## Attack

Which derived
authority decisions
remain valid?

## Analysis

NAM-001
cannot determine this
from relationship type
alone.

The model requires
evidence-bounded
compromise semantics.

## Result

COMPROMISE WINDOW
REQUIRED.

---

# ST-035 — Conflicting Authority Roots

## Scenario

Two valid roots
within the same
Repository Authority Context

claim incompatible
authority
over the same scope.

## Attack

Does root status
resolve the conflict?

## Analysis

No.

Root status alone
does not establish
precedence
between roots.

## Result

ROOT CONFLICT
REQUIRES GOVERNANCE.

---

# ST-036 — Historical Replay

## Scenario

A replay asks:

What authority
governed
at T1?

Current authority
is different.

## Attack

Can current-state
evaluation answer
the replay?

## Analysis

No.

Historical authority
must be evaluated
against:

Historical relationships.

Historical states.

Historical conditions.

Historical authority
configuration.

Evaluation time.

## Result

HISTORICAL AUTHORITY
REPLAY REQUIRED.

---

# ST-037 — Current Evaluation

## Scenario

A consumer asks:

What authority
governs now?

## Attack

Must it inspect
every historical state?

## Analysis

No.

Current evaluation
should derive
the effective
authority set

for a specified:

Context.

Scope.

Evaluation time.

Conditions.

## Result

EFFECTIVE AUTHORITY
PROJECTION REQUIRED.

---

# ST-038 — State Mutation

## Scenario

An authority record
changes directly from:

ACTIVE

to

INVALIDATED

by editing
the existing record.

## Attack

Is mutation sufficient?

## Analysis

No.

Direct mutation
destroys
transition evidence
and historical state.

## Result

STATE TRANSITIONS
MUST BE EVIDENCED.

---

# ST-039 — Deleted Authority Record

## Scenario

A superseded
authority record
is deleted
because it is
no longer current.

## Attack

Can historical authority
still be reconstructed?

## Analysis

No.

Historical traceability
is destroyed.

## Result

AUTHORITY HISTORY
MUST BE PRESERVED.

---

# ST-040 — Duplicate Relationship Identity

## Scenario

Two authority records
contain identical:

Source.

Target.

Scope.

Context.

Time.

but different states.

## Attack

Are they
the same relationship?

## Analysis

NAM-001
does not define
authority relationship
identity.

## Result

RELATIONSHIP IDENTITY
REQUIRED.

---

# Refutation Findings

NAM-001 Version 0.2
successfully distinguishes
typed authority
relationships

but its
single authority-state model
does not survive
adversarial testing.

Several declared states
represent different
semantic dimensions.

In particular:

CANDIDATE
describes eligibility
or lifecycle position.

ACTIVE
describes current
effectivity.

SUSPENDED
describes authority
availability.

SUPERSEDED
describes termination
cause and lineage.

INVALIDATED
describes normative
disposition.

HISTORICAL
describes evaluation
relative to time.

These cannot safely
be represented
as one
mutually exclusive
state enumeration.

---

# State Model Finding

A future revision
shall separate
at minimum:

Authority Disposition.

Authority Effectivity.

Authority Applicability.

Authority History.

Candidate Status.

One field
shall not attempt
to encode
all dimensions.

---

# Transition Finding

Authority changes
shall be represented
through explicit
transition evidence.

Direct destructive
state mutation
shall not replace
historical transition
records.

Transitions
shall identify:

Prior relationship.

Transition type.

Authority source.

Effective time.

Affected scope.

Resulting disposition.

Transition evidence.

---

# Temporal Finding

Authority evaluation
requires an explicit
Evaluation Time.

Current authority
is a special case
of temporal evaluation.

Historical replay
shall evaluate authority
using historically
applicable:

Relationships.

Transitions.

Conditions.

Configuration.

Authority roots.

---

# Applicability Finding

Authority existence
and authority applicability
are distinct.

A valid
authority relationship
may be temporarily
non-applicable

because its
conditions
are unsatisfied

without becoming:

Suspended.

Withdrawn.

Invalidated.

Superseded.

---

# Dependency Finding

Derived,
delegated,
joint,
and quorum authority

may depend
upon other
authority relationships.

Dependency behavior
shall be explicit
under:

Suspension.

Revocation.

Withdrawal.

Invalidation.

Expiration.

Root failure.

Dependency
shall not be inferred
from graph reachability
alone.

---

# Joint and Quorum Finding

Joint and quorum
authority decisions

require a pinned
authority configuration.

Evaluation shall identify:

Membership set.

Threshold.

Decision rule.

Authority context.

Scope.

Evaluation time.

Applicable conditions.

A decision
shall not silently
change semantics
because configuration
changed during evaluation.

---

# Root Failure Finding

Authority roots
require explicit
failure semantics.

Root:

Suspension.

Invalidation.

Compromise.

Replacement.

Conflict.

shall not automatically
produce one universal
effect
over historical
or derived authority.

Current validity,
historical validity,
and retroactive validity

shall remain distinct.

---

# Relationship Identity Finding

Every authority
relationship
requires stable identity.

Identity shall permit
the repository
to distinguish:

Relationship revision.

Relationship transition.

Duplicate claim.

Successor relationship.

Historical predecessor.

Reactivation.

Replacement.

Without stable identity,
authority history
cannot be reconstructed
reliably.

---

# Required Reduction

NAM-001
shall retain:

Typed authority
relationships.

Explicit scope.

Repository Authority Context.

Authority source.

Authority-of-authority.

Edge minimality.

Conflict semantics.

Joint authority.

Quorum authority.

Temporal boundaries.

But the
single Authority States
enumeration
shall be removed
or decomposed.

---

# Candidate Next Model

NAM-001 Version 0.3

should become:

Typed Authority
Relationship and
Transition Model.

It shall model:

Stable relationship identity.

Authority disposition.

Effectivity.

Applicability.

Temporal evaluation.

Explicit transitions.

Dependency behavior.

Pinned joint
and quorum configuration.

Historical replay.

Root failure semantics.

---

# Refutation Outcome

Target

NAM-001 Version 0.2 Draft.

Outcome

REFUTED
IN CURRENT FORM.

Typed Relationship Core

SURVIVES.

Single Authority
State Enumeration

REFUTED.

Authority Relationship
Identity

REQUIRED.

Explicit Transition Model

REQUIRED.

Evaluation Time

REQUIRED.

Applicability Separation

REQUIRED.

Dependency Semantics

REQUIRED.

Configuration Pinning

REQUIRED.

Historical Authority Replay

REQUIRED.

Root Failure Semantics

REQUIRED.

Authority

NONE.

Promotion

PROHIBITED.

Next Required Activity

NAM-001 Version 0.3

Typed Authority
Relationship and
Transition Model.

---

# End of NAM-001 Refutation Cycle 2
