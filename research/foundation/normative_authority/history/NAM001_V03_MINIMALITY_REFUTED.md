# Normative Authority Model

Identifier

NAM-001

Version

0.3

Status

Draft

Model

Typed Authority
Relationship and
Transition Model

Authority

NONE.

---

## Purpose

Define a candidate
repository model

for representing
normative authority
through:

Stable authority
relationship identity.

Typed authority
relationships.

Explicit authority
disposition.

Explicit effectivity.

Explicit applicability.

Temporal evaluation.

Traceable
authority transitions.

Authority dependencies.

Joint and quorum
configuration pinning.

Historical authority replay.

Authority-root
failure semantics.

The model
shall represent
normative authority only.

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
and transition-aware
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

Generic unlabeled
authority edges
shall not be used.

---

## Authority Relationship Identity

Every authority
relationship
shall possess
stable identity.

Relationship identity
shall remain stable
across:

State transitions.

Suspension.

Reactivation.

Supersession.

Withdrawal.

Invalidation.

Historical replay.

A new authority
relationship
shall receive
new identity

when its normative
identity changes
materially.

Relationship identity
shall permit
distinguishing:

Revision.

Transition.

Duplicate claim.

Replacement.

Successor.

Historical predecessor.

Reactivation.

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

Effectivity.

Effective Start.

Effective End.

Applicability Conditions.

Dependency Relationships.

Delegation Bounds.

Revocation Mechanism.

Joint Decision Rule.

Quorum Rule.

Historical Predecessor.

Promotion Evidence.

Transition Evidence.

Not every field
shall apply
to every
relationship type.

Required fields
shall remain
type-dependent.

---

## Authority Relationship Types

The candidate
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

QUORUM_AUTHORITY.

SUBORDINATION.

SUPERSESSION.

REVOCATION.

WITHDRAWAL.

SUSPENSION.

INVALIDATION.

HISTORICAL_PREDECESSOR.

Additional
relationship types
shall require
independent justification.

---

## Authority Disposition

Authority Disposition
shall describe
the normative
disposition
of the relationship.

Candidate dispositions:

ESTABLISHED.

SUSPENDED.

SUPERSEDED.

WITHDRAWN.

INVALIDATED.

Disposition
shall not encode:

Current applicability.

Candidate lifecycle state.

Historical perspective.

Temporal effectivity.

These dimensions
shall remain separate.

---

## Established Disposition

ESTABLISHED

shall mean
the authority relationship
has been validly
established

under its
applicable authority source.

ESTABLISHED
shall not imply
that the relationship
is currently applicable.

---

## Suspended Disposition

SUSPENDED

shall mean
authority has been
temporarily disabled

through an explicit
authority transition.

Suspension
shall preserve
relationship identity.

Suspension
shall not erase
historical authority.

---

## Superseded Disposition

SUPERSEDED

shall mean
the relationship
has been explicitly
replaced

within a declared
scope
by a successor
authority relationship.

Supersession
shall preserve
historical lineage.

---

## Withdrawn Disposition

WITHDRAWN

shall mean
authority has been
explicitly terminated

without requiring
a successor.

Withdrawal
shall preserve
historical traceability.

---

## Invalidated Disposition

INVALIDATED

shall mean
the governing
authority mechanism
has explicitly
rejected
the normative basis

of the relationship.

Invalidation
shall not erase
historical identity.

---

## Effectivity

Effectivity
shall answer:

Is the authority
relationship
effective
at the
Evaluation Time?

Candidate effectivity values:

EFFECTIVE.

NOT_YET_EFFECTIVE.

EXPIRED.

TERMINATED.

Effectivity
shall be derived
from:

Effective interval.

Applicable transitions.

Authority disposition.

Pinned authority
configuration.

Effectivity
shall not be inferred
from file timestamps.

---

## Applicability

Applicability
shall answer:

Does the effective
authority relationship
apply to the
evaluated claim
under the
evaluated conditions?

Candidate applicability values:

APPLICABLE.

NOT_APPLICABLE.

UNRESOLVED_APPLICABILITY.

Applicability
shall remain distinct
from effectivity.

A relationship
may be EFFECTIVE
but NOT_APPLICABLE.

---

## Candidate Status

Candidate status
shall remain external
to current normative
authority disposition.

An artifact
may be:

Research Candidate.

Specification Candidate.

Architecture Principle
Candidate.

Freeze Candidate.

without possessing
current normative authority.

Candidate status
shall not be encoded
as an Authority
Disposition.

---

## Historical Perspective

Historical status
shall be derived
from evaluation context.

A relationship
may be:

currently superseded,

while having been
effective and applicable
at an earlier time.

HISTORICAL
shall therefore
not be modeled
as a mutually exclusive
Authority Disposition.

---

## Evaluation Time

Every authority
evaluation
shall identify
an Evaluation Time.

Evaluation Time
may represent:

Current evaluation.

Historical replay.

Future scheduled
authority evaluation.

The applicable
authority set
shall be computed
relative to
Evaluation Time.

---

## Temporal Interval

An authority
relationship
may define:

Effective Start.

Effective End.

Effective Start
shall be inclusive
unless another
normative rule
explicitly defines
otherwise.

Effective End
shall be exclusive
unless another
normative rule
explicitly defines
otherwise.

An absent
Effective End
shall represent
an open-ended interval

subject to
later authority
transitions.

---

## Zero-Length Interval

Where
Effective Start
equals
Effective End,

the authority
relationship
shall possess
no effective interval

unless another
normative rule
explicitly establishes
point-in-time authority.

---

## Future Effectivity

An authority
relationship
may be validly
approved

before becoming
effective.

Approval
and effectivity
shall remain distinct.

A future
Effective Start
shall produce:

NOT_YET_EFFECTIVE

before that time.

---

## Applicability Conditions

Authority
may be conditional.

Applicability conditions
shall be:

Explicit.

Normatively governed.

Determinable
at evaluation time.

Stable enough
for reproducible
authority evaluation.

Ambiguous conditions
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
of historical
authority state
shall not replace
transition evidence.

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

Resulting Disposition.

Successor Relationship.

Dependency Effects.

Transition Evidence.

---

## Transition Types

Candidate transition types:

ESTABLISH.

SUSPEND.

REACTIVATE.

SUPERSEDE.

WITHDRAW.

INVALIDATE.

EXPIRE.

DELEGATE.

TRANSFER.

REVOKE.

REPLACE.

AMEND_SCOPE.

AMEND_CONDITION.

AMEND_INTERVAL.

ROOT_SUSPEND.

ROOT_INVALIDATE.

ROOT_REPLACE.

Transition types
shall remain
explicit.

---

## Reactivation

REACTIVATE

shall restore
a suspended
relationship
to ESTABLISHED
disposition

only through
an explicitly
authorized transition.

Satisfaction
of a suspension
resolution condition
shall not automatically
reactivate authority

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
relationship identity:

WITHDRAWN.

INVALIDATED.

SUPERSEDED.

A terminal
relationship
shall not silently
return to ESTABLISHED.

Restoration
after a terminal
disposition

shall require
a new authority
relationship
or explicit
replacement semantics.

---

## Suspension Non-Terminality

SUSPENDED
shall not be terminal.

A suspended
relationship
may become
ESTABLISHED again

through
an authorized
REACTIVATE transition.

---

## Temporal Mutation

Changes to:

Effective Start.

Effective End.

shall require
explicit
AMEND_INTERVAL
transition semantics.

A temporal amendment
shall not silently
rewrite
historical authority.

Retroactive amendments
shall require
explicit authorization.

---

## Retroactivity

Authority transitions
shall be prospective
by default.

Retroactive effect
shall require
explicit
authority semantics.

A retroactive transition
shall identify:

Decision Time.

Effective Time.

Retroactive authority source.

Affected historical interval.

Historical validity impact.

Retroactivity
shall not be inferred.

---

## Historical Validity

Historical evaluation
shall distinguish:

Authority that
was valid
at the time.

Authority later
declared invalid
with prospective effect.

Authority later
declared invalid
with retroactive effect.

Authority that
never possessed
valid authority.

These cases
shall remain distinct.

---

## Authority Dependency

Authority relationships
may depend upon
other authority
relationships.

Dependency
shall be explicit.

Graph reachability
alone
shall not create
authority dependency.

A dependency
shall identify:

Dependency source.

Dependency target.

Dependency type.

Scope.

Failure behavior.

---

## Derived Authority Dependency

DERIVED_AUTHORITY
shall depend
upon its
authority source

unless another
authority mechanism
explicitly stabilizes
the derived authority.

Loss of source
authority
shall trigger
dependency evaluation.

---

## Delegated Authority Dependency

DELEGATED_AUTHORITY
shall ordinarily depend
upon continued validity
of the delegator's
authority.

Revocation,
withdrawal,
or invalidation
of the delegator

shall trigger
evaluation
of dependent
delegations.

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

Propagation
shall remain
scope-aware.

---

## Transfer Scope

TRANSFERRED_AUTHORITY
shall operate
on explicit scope.

Transferred scope
shall be removed
from the transferor's
current authority

unless explicitly
retained.

Partial transfer
shall not affect
untransferred scope.

---

## Authority Conflict

Authority conflict
exists when
two simultaneously:

Effective.

Applicable.

authority relationships

within overlapping
scope
cannot both
be satisfied.

Conflict evaluation
shall consider:

Repository Authority Context.

Scope.

Relationship type.

Authority source.

Disposition.

Effectivity.

Applicability.

Explicit precedence.

Conflict Resolution Authority.

Joint or quorum rules.

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
at a defined
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

## Authority-of-Authority

Every mechanism
that changes
normative authority

shall itself
possess traceable
authority
for the action.

This applies to:

Promotion.

Delegation.

Transfer.

Revocation.

Suspension.

Reactivation.

Supersession.

Withdrawal.

Invalidation.

Conflict resolution.

Root replacement.

Authority-granting mechanisms
shall not self-authorize.

---

## Authority Root

Every current
authority chain
shall remain
traceable
to at least one
valid authority root

within its Repository
Authority Context.

Multiple authority roots
may exist.

A universal
repository-independent
authority root
shall not be assumed.

---

## Root Dependency

Authority relationships
may depend
upon an
Authority Root.

Root dependency
shall be explicit.

Root:

Suspension.

Invalidation.

Compromise.

Replacement.

shall trigger
authority dependency
evaluation.

No universal
failure propagation
shall be assumed.

---

## Root Suspension

ROOT_SUSPEND

shall temporarily
affect authority
dependent upon
the suspended root

according to
explicit dependency
semantics.

Historical authority
shall not automatically
be erased.

---

## Root Invalidation

ROOT_INVALIDATE

shall terminate
current root authority

according to
the applicable
authority process.

Derived authority
shall be reevaluated.

Retroactive invalidation
shall require
explicit semantics.

---

## Root Compromise

A compromised
authority root
shall identify,
where possible:

Compromise discovery time.

Estimated compromise start.

Confidence interval.

Affected scope.

Affected authority
relationships.

The model
shall not assume
that compromise discovery
establishes
the exact compromise time.

---

## Root Conflict

Multiple roots
within the same
Repository Authority Context

may conflict.

Root identity
alone
shall not establish
precedence.

Conflict resolution
shall require
applicable governing
authority semantics.

---

## Joint Authority

JOINT_AUTHORITY
shall require
an explicit
joint decision rule.

Joint configuration
shall identify:

Participants.

Required participation.

Failure behavior.

Scope.

Repository Authority Context.

Evaluation Time.

Applicable conditions.

---

## Quorum Authority

QUORUM_AUTHORITY
shall require
an explicit
quorum configuration.

Quorum configuration
shall identify:

Authorized participants.

Membership set.

Required threshold.

Decision rule.

Scope.

Repository Authority Context.

Evaluation Time.

Applicable conditions.

---

## Authority Configuration Snapshot

Joint and quorum
authority decisions
shall use
a pinned
Authority Configuration Snapshot.

The snapshot
shall identify:

Configuration Identifier.

Membership set.

Threshold,
where applicable.

Decision rule.

Scope.

Repository Authority Context.

Evaluation Time.

Applicable conditions.

Authority source.

A decision
shall not silently
change semantics
because configuration
changes during evaluation.

---

## Authority Replay

Historical authority
shall be replayable.

Authority Replay
shall reconstruct
the effective
authority set

for a specified:

Repository Authority Context.

Scope.

Evaluation Time.

Conditions.

Authority Configuration.

Replay shall consider:

Historical relationships.

Transitions.

Dispositions.

Temporal intervals.

Dependencies.

Authority roots.

Joint configuration.

Quorum configuration.

---

## Effective Authority Projection

Current authority
shall be representable
as an
Effective Authority Projection.

The projection
shall evaluate
authority relationships
for a specified:

Repository Authority Context.

Scope.

Evaluation Time.

Conditions.

The projection
shall include only
relationships that are:

ESTABLISHED.

EFFECTIVE.

APPLICABLE.

and not terminated
by an applicable
authority transition.

---

## Relationship Duplication

Two records
claiming the same
relationship identity

with conflicting
normative fields

shall represent
an authority ambiguity
or integrity failure.

Duplicate identity
shall not silently
create parallel authority.

---

## Authority Ambiguity

Authority ambiguity
shall exist when
the repository
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

Applicable configuration.

Conflict rule.

Authority ambiguity
shall not be resolved
through assumption.

---

## Edge Minimality

Authority graph edges
shall represent
normative authority
relationships only.

The following
shall not automatically
create authority edges:

Dependency
unless explicitly
normative.

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
create
normative authority
merely through
execution or success.

---

## Implementation Relationship

Implementation
may realize
normative semantics.

Implementation
shall not establish
normative authority
through:

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
distinct
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
collapsed into
one universal
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

CTA authority,
if later established,

shall require
explicit
authority transition.

---

## Candidate Invariants

Authority relationships
shall possess
stable identity.

Authority relationships
shall be typed.

Authority disposition
shall be explicit.

Effectivity
shall remain distinct
from disposition.

Applicability
shall remain distinct
from effectivity.

Candidate status
shall remain distinct
from normative authority.

Historical perspective
shall remain
evaluation-relative.

Evaluation Time
shall be explicit.

Transitions
shall be evidenced.

Terminal dispositions
shall not silently
reactivate.

Suspension
shall remain
non-terminal.

Retroactivity
shall require
explicit authority.

Dependencies
shall be explicit.

Transfer
shall remain distinct
from delegation.

Joint and quorum
configuration
shall be pinned.

Authority roots
shall remain
traceable.

Root failure
shall trigger
dependency evaluation.

Historical authority
shall be replayable.

Authority ambiguity
shall not be
resolved by assumption.

Authority graph edges
shall remain minimal.

---

## Falsifiability

NAM-001
shall be refuted
or revised
if evidence demonstrates
that the relationship
and transition model

cannot deterministically
represent:

Current authority.

Historical authority.

Authority transitions.

Conditional applicability.

Temporal applicability.

Delegation dependencies.

Transfer semantics.

Joint authority.

Quorum authority.

Root failure.

Authority conflict.

Authority ambiguity.

without:

Contradiction.

Silent scope expansion.

Historical loss.

Self-authorization.

Unbounded graph growth.

---

## Current Status

Identifier

NAM-001

Version

0.3

Status

Draft

Model

Typed Authority
Relationship and
Transition Model

Refutation Cycles Completed

2

Authority Relationship Types

17

Authority Dispositions

5

Effectivity Values

4

Applicability Values

3

Transition Types

17

Authority

NONE.

Promotion

PROHIBITED.

Next Required Activity

Refutation Cycle 3

Minimality,
Determinism,
and Replay Testing.

---

# End of Normative Authority Model
