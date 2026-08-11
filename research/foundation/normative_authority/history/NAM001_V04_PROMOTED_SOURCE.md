# Normative Authority Model

Identifier

NAM-001

Version

0.4

Status

Draft

Model

Reduced Deterministic
Authority Model

Authority

NONE.

---

## Purpose

Define a minimal
candidate model

for deterministic
representation,
evaluation,
transition,
and replay

of repository
normative authority.

The model shall preserve:

Stable relationship identity.

Typed authority relationships.

Authority disposition.

Effectivity.

Applicability.

Evaluation time.

Explicit transitions.

Authority dependencies.

Authority-of-authority.

Conflict semantics.

Historical replay.

Fail-closed evaluation.

The model shall not
represent
non-authority relationships.

---

## Governing Context

NAM-001
shall conform to:

RC-001
Repository Constitution
Baseline 1.0.

SL-001
Repository Specification Lifecycle
Baseline 1.0.

APC-001
Architecture Principle
Classification Baseline 1.0.

NAM-001
does not grant
authority to itself.

NAM-001
does not grant
authority to any
other artifact.

---

## Core Proposition

Repository normative authority
shall be represented

as explicit,
typed,
scoped,
traceable,
temporally evaluable,
transition-aware,
and deterministically
resolvable
authority relationships.

Authority
shall not be inferred
from:

File presence.

Repository path.

Directory depth.

Version recency.

Commit order.

Tag presence.

Implementation behavior.

Test behavior.

Execution order.

Dependency direction.

Reference count.

Historical popularity.

Naming convention.

Architectural importance.

Commercial importance.

---

## Authority Graph

Normative authority
shall be representable
as a graph.

Graph nodes
may represent:

Normative artifacts.

Authority contexts.

Authority-granting
mechanisms.

Authorized actors.

Authority groups.

Authority roots.

Graph edges
shall represent
typed authority
relationships.

Authority graph edges
shall remain minimal.

---

## Relationship Identity

Every authority
relationship
shall possess
stable identity.

Relationship identity
shall permit
distinguishing:

Creation.

Transition.

Amendment.

Reactivation.

Replacement.

Duplicate claim.

Successor relationship.

Historical predecessor.

A material change
to normative identity

shall require
a new
Relationship Identifier.

---

## Identity Materiality

The following
shall ordinarily
require
new relationship identity:

Authority Source change.

Repository Authority Context
change.

Fundamental
Relationship Type change.

Fundamental
Authority Target change.

The following
may preserve identity
through explicit
amendment semantics:

Scope narrowing.

Condition amendment.

Temporal interval amendment.

Other changes
shall require
materiality analysis.

Historical values
shall remain traceable.

---

## Authority Relationship Record

Every authority
relationship
shall identify,
where applicable:

Relationship Identifier.

Relationship Type.

Authority Source.

Authority Target.

Repository Authority Context.

Authority Scope.

Authority Disposition.

Effective Start.

Effective End.

Applicability Conditions.

Authority Dependencies.

Joint Decision Rule.

Quorum Rule.

Transition History.

Promotion Evidence.

Authority Configuration.

Required fields
shall depend
upon relationship type.

---

## Authority Relationship Types

The reduced
relationship types are:

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

These ten
relationship types
shall not be expanded
without independent
justification.

---

## Direct Authority

DIRECT_AUTHORITY

shall represent
authority established
through an explicit
recognized
authority mechanism

without depending
upon delegated
or derived authority
from another
current relationship.

---

## Derived Authority

DERIVED_AUTHORITY

shall represent
bounded authority
explicitly permitted
by another
valid authority relationship.

Derived Authority
shall not exceed:

Source scope.

Source context.

Source conditions.

Source temporal bounds.

---

## Delegated Authority

DELEGATED_AUTHORITY

shall represent
bounded authority
exercised by
another authorized target

without necessarily
terminating
the delegator's
own authority.

Delegation
shall identify:

Delegator.

Delegate.

Scope.

Conditions.

Effective interval.

Revocation mechanism.

---

## Transferred Authority

TRANSFERRED_AUTHORITY

shall represent
authority moved
from one holder
to another

within an explicit
scope.

Transfer
may terminate
the transferor's
authority
within transferred scope.

Transfer
shall remain distinct
from delegation.

---

## Classification Authority

CLASSIFICATION_AUTHORITY

shall permit
an authoritative classifier
to determine
candidate classification

within an explicit
classification scope.

Classification Authority
shall not grant
normative authority
to classified candidates.

---

## Lifecycle Authority

LIFECYCLE_AUTHORITY

shall govern
normative maturation
and lifecycle transitions

within its declared scope.

Lifecycle Authority
shall not automatically
create semantic authority
over governed artifacts.

---

## Promotion Authority

PROMOTION_AUTHORITY

shall permit
an explicitly
authorized mechanism

to grant
or transition
normative authority

within its declared scope.

A Promotion Gate
shall not possess
Promotion Authority
merely because
it uses that name.

---

## Conflict Resolution Authority

CONFLICT_RESOLUTION_AUTHORITY

shall permit
an explicitly
authorized mechanism

to resolve
conflicting
authority claims

within its declared
scope
and Repository
Authority Context.

---

## Joint Authority

JOINT_AUTHORITY

shall represent
authority requiring
multiple authorized
participants

under an explicit
joint decision rule.

A quorum
shall be represented
as a Joint Authority
configuration
with a threshold rule.

No independent
QUORUM_AUTHORITY
relationship type
is required.

---

## Subordination

SUBORDINATION

shall represent
a normative relationship

where one artifact
must remain
conformant to
another applicable
authority

within overlapping
scope.

Subordination
shall not imply
universal superiority
outside that scope.

---

## Authority Disposition

Authority Disposition
shall describe
the normative
status
of an established
relationship.

Exactly five
candidate dispositions
are recognized:

ESTABLISHED.

SUSPENDED.

SUPERSEDED.

WITHDRAWN.

INVALIDATED.

Disposition
shall not encode:

Candidate lifecycle state.

Effectivity.

Applicability.

Historical perspective.

---

## Effectivity

Effectivity
shall be derived
for a specified
Evaluation Time.

Candidate effectivity
values:

EFFECTIVE.

NOT_YET_EFFECTIVE.

EXPIRED.

TERMINATED.

Effectivity
shall be computed
from:

Effective interval.

Disposition.

Applicable transitions.

Pinned authority
configuration.

---

## Applicability

Applicability
shall answer
whether an
EFFECTIVE relationship

governs the
evaluated claim
under evaluated
conditions.

Candidate applicability
values:

APPLICABLE.

NOT_APPLICABLE.

UNRESOLVED_APPLICABILITY.

Applicability
shall remain distinct
from Effectivity.

---

## Candidate Status

Candidate status
shall remain
outside normative
authority disposition.

A candidate
may contain
normative propositions

without possessing
current normative authority.

---

## Historical Perspective

Historical perspective
shall be derived
from:

Evaluation Time.

Transition History.

Authority Configuration.

Historical Evidence.

HISTORICAL
shall not be modeled
as a disposition.

---

## Evaluation Time

Every authority
evaluation
shall pin
an Evaluation Time.

Evaluation Time
shall not change
during one
authority projection
or replay operation.

Current authority
shall be treated
as temporal evaluation
at a pinned
current time.

---

## Temporal Interval

Effective Start
shall be inclusive.

Effective End
shall be exclusive.

An absent
Effective End
shall represent
an open interval.

Where:

Effective Start
equals
Effective End,

the relationship
shall possess
no effective interval

unless explicit
point-in-time authority
is defined elsewhere.

---

## Applicability Conditions

Authority conditions
shall be:

Explicit.

Normatively governed.

Determinable.

Replayable
where historical
evaluation is required.

Missing or ambiguous
required condition evidence

shall produce:

UNRESOLVED_APPLICABILITY.

---

## Authority Transition

Authority changes
shall be represented
through explicit
transition records.

Direct destructive
mutation
shall not replace
historical transition
evidence.

Every transition
shall identify,
where applicable:

Transition Identifier.

Prior Relationship.

Transition Type.

Authority Source.

Repository Authority Context.

Affected Scope.

Effective Time.

Successor Relationship.

Dependency Effects.

Transition Evidence.

---

## Transition Types

The reduced
transition types are:

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

Exactly twelve
top-level transition types
are recognized.

---

## Derived Expiration

Expiration
shall be derived
from:

Effective End.

Evaluation Time.

An independent
EXPIRE transition
shall not be required
for natural interval
completion.

Explicit early
termination
shall use
the applicable
normative transition.

---

## Root-Specific Transitions

Authority Root
suspension,
invalidation,
or replacement

shall use
the general:

SUSPEND.

INVALIDATE.

SUPERSEDE.

transition types

with an
Authority Root
as the target.

Separate
ROOT_SUSPEND,
ROOT_INVALIDATE,
and ROOT_REPLACE
types
shall not be required.

---

## Reactivation

A suspended
relationship
shall return
to ESTABLISHED

only through
an authorized
REACTIVATE transition

unless the governing
authority mechanism
explicitly defines
automatic reactivation.

---

## Terminal Dispositions

The following
dispositions
shall be terminal
for the same
Relationship Identifier:

SUPERSEDED.

WITHDRAWN.

INVALIDATED.

A terminal relationship
shall not silently
return to ESTABLISHED.

Subsequent authority
shall require
a new relationship
or explicit
successor semantics.

---

## Retroactivity

Authority transitions
shall be prospective
by default.

Retroactive effect
shall require
explicit authorization.

A retroactive transition
shall preserve:

Decision Time.

Effective Time.

Authority Source.

Affected Historical Interval.

Historical Validity Impact.

---

## Authority Dependency

Authority dependency
shall be explicit.

Graph reachability
alone
shall not establish
dependency.

A dependency
shall identify:

Dependency Source.

Dependency Target.

Scope.

Failure Behavior.

Authority dependency
shall represent only
relationships that affect
normative authority.

---

## Dependency Propagation

Loss or change
of source authority

shall trigger
dependency evaluation.

Propagation
shall remain:

Scope-aware.

Type-aware.

Transition-aware.

Dependency loss
shall not automatically
erase historical authority.

---

## Transitive Revocation

Where authority C
depends exclusively
upon B,

and B depends
exclusively upon A,

revocation of B
shall propagate
to C

unless an independent
authority source
preserves C.

---

## Transfer Scope

Transfer
shall operate
on explicit scope.

Transferred scope
shall be removed
from the transferor

unless explicitly
retained.

Untransferred scope
shall remain unaffected.

---

## Authority Root

Every current
authority chain
shall remain
traceable
to at least one
valid Authority Root

within its
Repository Authority Context.

Multiple roots
may exist.

No universal
repository-independent
root
shall be assumed.

---

## Authority-of-Authority

Every mechanism
that:

Establishes.

Promotes.

Delegates.

Transfers.

Revokes.

Suspends.

Reactivates.

Supersedes.

Withdraws.

Invalidates.

Resolves conflicts.

or amends
normative authority

shall itself
possess traceable
authority
for that action.

Authority-granting
mechanisms
shall not self-authorize.

---

## Circular Authority

Graph cycles
shall not automatically
be invalid.

A cycle
shall be invalid
when:

Authority is created
solely through
circular support.

No independently
valid authority root
can be reached.

Scope expands
through the cycle
without authority.

Evaluation cannot
terminate deterministically.

---

## Root Failure

Authority Root:

Suspension.

Invalidation.

Compromise.

Supersession.

Conflict.

shall trigger
explicit
dependency evaluation.

Current validity.

Historical validity.

Retroactive validity.

shall remain
distinct questions.

---

## Root Compromise

Root compromise
shall identify,
where evidence permits:

Discovery Time.

Estimated Compromise Start.

Confidence Interval.

Affected Scope.

Affected Relationships.

Uncertain compromise time
shall remain uncertain.

It shall not be
silently converted
to a precise
historical boundary.

---

## Joint Authority Configuration

Joint Authority
shall use
a pinned
Authority Configuration.

Configuration shall identify:

Configuration Identifier.

Authorized Participants.

Membership Set.

Required Participation
or Threshold.

Decision Rule.

Scope.

Repository Authority Context.

Evaluation Time.

Applicable Conditions.

Authority Source.

A quorum
is represented
through
Required Threshold.

---

## Configuration Pinning

Authority configuration
shall be pinned
for one
authority decision.

Membership,
threshold,
or decision-rule changes

during evaluation
shall not alter
the pinned decision.

---

## Authority Conflict

Authority conflict
exists when
two simultaneously:

EFFECTIVE.

APPLICABLE.

authority relationships

within overlapping
scope
cannot both
be satisfied.

Conflict evaluation
shall consider:

Repository Authority Context.

Scope.

Relationship Type.

Authority Source.

Disposition.

Effectivity.

Applicability.

Explicit Precedence.

Conflict Resolution Authority.

Joint Decision Rule.

---

## Authority Compatibility

Authority relationships
may evaluate as:

COMPATIBLE.

COMPATIBLE_WITH_SCOPE.

CONDITIONALLY_COMPATIBLE.

CONFLICTING.

UNRESOLVED.

JOINTLY_GOVERNED.

Compatibility
shall be evaluated
at a pinned
Evaluation Time.

---

## Authority Precedence

Authority precedence
shall be explicit.

The following
shall not automatically
create precedence:

Identifier.

File location.

Repository path.

Version number.

Recency.

Specificity.

Implementation adoption.

Test coverage.

Reference count.

Commercial importance.

---

## Transition Conflict

Two transitions
with the same
effective time

and overlapping
relationship scope

shall require
deterministic
resolution.

File order
shall not
resolve the conflict.

If no applicable
resolution exists,

authority evaluation
shall become:

UNRESOLVED.

---

## Deterministic Evaluation

Given identical:

Repository Authority Context.

Scope.

Evaluation Time.

Conditions.

Authority Relationships.

Transition History.

Dependency Evidence.

Authority Root Evidence.

Pinned Configuration.

an evaluator
shall produce
the same:

Effective Authority Projection.

or

explicit unresolved result.

Results
shall not depend upon:

File order.

Iteration order.

Wall-clock drift.

Current configuration
during replay.

Implementation-specific
collection ordering.

---

## Evaluation Termination

Authority evaluation
shall terminate.

Cycles
shall not produce
unbounded recursion.

Evaluation
shall detect
dependency cycles

and determine whether
they are:

Valid and rooted.

Invalid self-support.

Unresolved.

No authority
shall be created
solely because
evaluation encountered
a cycle.

---

## Fail-Closed Evaluation

Authority evaluation
shall not invent
missing authority evidence.

Missing required:

Authority Source.

Transition History.

Historical Conditions.

Configuration Snapshot.

Dependency Evidence.

Conflict Rule.

Root Evidence.

shall produce
an explicit:

UNRESOLVED.

or

non-authoritative result

as defined by
the consuming
normative specification.

Authority
shall not be assumed.

---

## Effective Authority Projection

An Effective
Authority Projection

shall evaluate
relationships
for a specified:

Repository Authority Context.

Scope.

Evaluation Time.

Conditions.

Pinned Configuration,
where required.

A relationship
shall contribute
current authority
only when:

Disposition permits authority.

Effectivity is EFFECTIVE.

Applicability is APPLICABLE.

Dependencies are satisfied.

Required root authority
is valid.

No unresolved
blocking conflict exists.

---

## Authority Replay

Historical authority
shall be replayable.

Replay shall pin:

Repository Authority Context.

Scope.

Evaluation Time.

Replay Mode.

Historical Conditions.

Authority Configuration.

Authority Evidence Set.

Transition Evidence Set.

Root Evidence Set.

---

## Replay Modes

Exactly two
candidate replay modes
are defined.

KNOWLEDGE_AT_TIME.

RETROSPECTIVE_AUTHORITY.

---

## Knowledge-at-Time Replay

KNOWLEDGE_AT_TIME

shall reconstruct
the authority result
that could have been
determined

using authority evidence
available
at the historical
Evaluation Time.

Later evidence
shall not be
silently injected.

---

## Retrospective Authority Replay

RETROSPECTIVE_AUTHORITY

shall reconstruct
what authority
is currently considered
to have governed

the historical
Evaluation Time

after applying
authorized
retroactive authority
transitions.

---

## Replay Determinism

Given identical
replay inputs,

authority replay
shall produce
the same
authority result

or the same
explicit unresolved
result.

Historical gaps
shall not be
filled using
current configuration
or assumption.

---

## Relationship Duplication

Two records
with the same
Relationship Identifier

and conflicting
normative fields

shall constitute:

Authority ambiguity.

Integrity failure.

or both,

according to
the applicable
normative specification.

Duplicate identity
shall not silently
create parallel authority.

---

## Authority Ambiguity

Authority ambiguity
shall exist when
required evidence
cannot deterministically
resolve:

Relationship identity.

Authority source.

Scope.

Disposition.

Effectivity.

Applicability.

Transition history.

Dependency.

Configuration.

Conflict.

Root validity.

Authority ambiguity
shall not be
resolved through
assumption.

---

## Edge Minimality

The authority graph
shall contain
authority-relevant
relationships only.

The following
shall not automatically
create authority edges:

Import.

Execution order.

File reference.

Test coverage.

Artifact derivation.

Data flow.

Deployment relationship.

Historical association.

Shared implementation.

Documentation reference.

Ordinary software
dependency.

---

## Executable Contracts

Executable Contracts
may:

Test conformance.

Provide evidence.

Detect violations.

Enforce applicable
requirements.

They shall not
create authority
merely through
execution
or successful tests.

---

## Implementation Relationship

Implementation
may realize
normative semantics.

Implementation
shall not create
authority through:

Existence.

Deployment.

Correctness.

Performance.

Popularity.

Commercial success.

Historical use.

Implementation consensus
shall not silently
resolve
normative ambiguity.

---

## Evidence Relationship

Evidence
may:

Support.

Challenge.

Refute.

Narrow.

Trigger revision.

Evidence
shall not automatically
create
or terminate
normative authority.

Authority transitions
shall remain explicit.

---

## Freeze Relationship

Freeze
shall remain
a lifecycle,
baseline,
or release-control
relationship.

Freeze
shall not automatically
create authority.

Freeze
shall not automatically
mean immutability.

Freeze
shall not become
an authority layer.

---

## Orthogonal Models

NAM-001
shall remain distinct
from:

Architecture Layer Model.

Runtime Processing Model.

Evidence Processing Model.

Artifact Lifecycle Model.

Deployment Topology.

Repository Directory Model.

Specification Lifecycle.

These models
may reference
authority relationships.

They shall not
silently redefine
authority.

---

## Current Foundation Example

Current foundation
contains multiple
authority scopes.

RC-001

Repository Constitution
Baseline 1.0.

Authority Scope

Constitutional
repository authority.

---

SL-001

Repository Specification
Lifecycle
Baseline 1.0.

Authority Scope

Normative lifecycle
semantics.

---

APC-001

Architecture Principle
Classification
Baseline 1.0.

Authority Scope

Architecture Principle
classification only.

---

These scopes
shall not be
collapsed
into one universal
linear hierarchy.

---

## Current CTA State

Common Trust Architecture
remains
non-authoritative.

Historical use
within CP-001

shall not establish
CTA authority.

Any future
CTA authority

shall require
its own
explicit authority
transition.

---

## Candidate Invariants

Relationship identity
shall be stable.

Relationship types
shall remain minimal.

Authority disposition
shall remain distinct
from effectivity.

Effectivity
shall remain distinct
from applicability.

Candidate status
shall remain distinct
from normative authority.

Historical perspective
shall remain
evaluation-relative.

Evaluation Time
shall be pinned.

Authority transitions
shall be explicit.

Authority history
shall not be
destructively rewritten.

Terminal dispositions
shall remain terminal
for one relationship identity.

Suspension
shall remain
reactivatable.

Retroactivity
shall require
explicit authority.

Dependencies
shall be explicit.

Circular support
shall not create authority.

Authority roots
shall remain traceable.

Joint configuration
shall be pinned.

Quorum
shall remain
a joint decision rule,
not an independent
authority relationship type.

Authority conflict
shall not be
resolved through
implicit precedence.

Evaluation
shall be deterministic.

Evaluation
shall terminate.

Missing authority evidence
shall fail closed.

Historical authority
shall be replayable.

Replay mode
shall be explicit.

Authority ambiguity
shall remain explicit.

Authority graph edges
shall remain minimal.

---

## Falsifiability

NAM-001
shall be refuted
or revised
if evidence demonstrates

that the reduced
deterministic model
cannot represent:

Current authority.

Historical authority.

Delegation.

Transfer.

Promotion.

Lifecycle authority.

Classification authority.

Conflict resolution.

Joint or quorum authority.

Authority roots.

Root failure.

Conditional authority.

Temporal authority.

Retroactive authority.

without:

Contradiction.

Silent authority expansion.

Non-determinism.

Non-termination.

Historical loss.

Self-authorization.

Unbounded graph growth.

---

## Current Status

Identifier

NAM-001

Version

0.4

Status

Draft

Model

Reduced Deterministic
Authority Model

Refutation Cycles Completed

3

Authority Relationship Types

10

Authority Dispositions

5

Effectivity Values

4

Applicability Values

3

Transition Types

12

Replay Modes

2

Authority

NONE.

Promotion

PROHIBITED.

Next Required Activity

Final Adversarial
Determinism and
Authority Replay
Refutation.

---

# End of Normative Authority Model
