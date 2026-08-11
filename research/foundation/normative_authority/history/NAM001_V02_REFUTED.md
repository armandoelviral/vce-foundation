# Normative Authority Model

Identifier

NAM-001

Version

0.2

Status

Draft

Model

Typed Authority
Relationship Model

Authority

NONE.

---

## Purpose

Define a candidate
repository model

for representing
normative authority
through:

Explicit authority states.

Typed authority
relationships.

Scoped authority.

Conditional authority.

Temporal authority.

Traceable
authority sources.

Authority transitions.

Conflict relationships.

Joint authority.

Quorum authority.

The model shall not
represent every
repository relationship.

It shall represent
normative authority only.

---

## Governing Context

NAM-001
is subordinate to
the currently authoritative
Repository Constitution.

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

---

## Core Proposition

Repository normative authority
shall be represented

as explicit,
typed,
scoped,
traceable,
and condition-aware
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

Graph edges
shall represent
typed authority
relationships.

Generic unlabeled
authority edges
shall not be used.

---

## Authority Relationship Record

Every authority
relationship
shall identify,
where applicable:

Relationship Type.

Authority Source.

Authority Target.

Repository Authority Context.

Authority Scope.

Effective Start.

Effective End.

Applicability Conditions.

Authority State.

Delegation Bounds.

Revocation State.

Precedence Rule.

Joint Decision Rule.

Quorum Rule.

Historical Predecessor.

Promotion Evidence.

Transition Evidence.

Not every field
shall apply
to every
relationship.

Required fields
shall depend upon
relationship type.

---

## Authority Relationship Types

The model recognizes
the following
candidate relation types:

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

Additional relation types
shall require
independent justification.

---

## Authority States

A normative artifact
or authority relationship
may possess
an explicit
authority state.

Candidate states:

NONE.

CANDIDATE.

ACTIVE.

SUSPENDED.

SUPERSEDED.

WITHDRAWN.

INVALIDATED.

EXPIRED.

HISTORICAL.

These states
shall not be treated
as interchangeable.

---

## No Authority

Authority

NONE

shall mean
no current
normative authority
exists.

Authority NONE
shall remain distinct
from:

SUSPENDED.

WITHDRAWN.

SUPERSEDED.

INVALIDATED.

EXPIRED.

HISTORICAL.

Never-authoritative artifacts
shall remain distinguishable
from formerly-authoritative
artifacts.

---

## Candidate Authority State

CANDIDATE

shall mean
the artifact
may contain
normative propositions

but has not yet
received current
normative authority.

Candidate existence
shall not imply
promotion.

---

## Active Authority

ACTIVE

shall mean
the authority relationship
is currently effective

within its declared:

Repository Authority Context.

Scope.

Temporal interval.

Applicability conditions.

ACTIVE
shall not imply
repository-wide authority.

---

## Suspended Authority

SUSPENDED

shall mean
authority is temporarily
non-effective

pending an explicit
resolution condition
or authority transition.

Suspension
shall not erase
historical authority.

Suspension
shall not automatically
invalidate
the artifact.

---

## Superseded Authority

SUPERSEDED

shall mean
an authority relationship
has been replaced
within an explicitly
defined scope

by a successor
authority relationship.

Supersession
shall remain traceable.

A newer version
shall not automatically
create supersession.

---

## Withdrawn Authority

WITHDRAWN

shall mean
current authority
has been explicitly
terminated

without requiring
a replacement.

Withdrawal
shall remain
historically traceable.

---

## Invalidated Authority

INVALIDATED

shall mean
the authority relationship
is explicitly rejected

because the underlying
normative basis
has been determined
invalid
under the applicable
authority process.

Invalidation
shall not erase
historical identity.

---

## Expired Authority

EXPIRED

shall mean
authority ended
because an explicit
temporal boundary
was reached.

Expiration
shall not be inferred
from age.

---

## Historical Authority

HISTORICAL

shall represent
authority that was
valid in a prior
effective interval

but is not
currently active.

Historical authority
shall remain
traceable.

---

## Repository Authority Context

Every authority claim
shall exist
within an identified
Repository Authority Context.

Authority
shall not silently
transfer
between contexts.

Repository forks
shall not automatically
inherit
current authority.

Context transitions
shall remain explicit.

---

## Authority Scope

Authority
shall be scoped.

A relationship
may apply to:

Repository constitutional
semantics.

Lifecycle semantics.

Classification semantics.

Architecture Principle
semantics.

Specification semantics.

Domain semantics.

Runtime semantics.

Artifact semantics.

Security semantics.

Other explicitly
declared normative scope.

Authority
outside declared scope
shall not be inferred.

---

## Conditional Authority

Authority
may be conditional.

Applicability conditions
shall be:

Explicit.

Normatively governed.

Stable enough
for deterministic
authority evaluation.

A condition
shall not silently
change
authority scope.

---

## Temporal Authority

Authority
may possess
an explicit
effective interval.

Temporal authority
shall identify:

Effective Start.

Effective End,
when applicable.

Time-based authority
shall not be inferred
from:

Commit timestamp.

File modification time.

Release date.

Tag date.

---

## Authority Source

Every current
authority relationship
shall possess
a traceable
authority source.

Candidate authority sources
may include:

Bootstrap Authority.

Promotion Authority.

Delegated Authority.

Transferred Authority.

Authoritative predecessor.

Explicit authority transition.

Applicable governing artifact.

Authority source
shall not be circular
without an independently
valid authority root.

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

Direct Authority
shall remain
traceable
to a valid
authority source.

---

## Derived Authority

DERIVED_AUTHORITY

shall represent
bounded authority

explicitly permitted
by another
valid authority relationship.

Derived authority
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

temporarily or
continuously exercised
by another
authorized target

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
from one authority holder
to another

within a defined scope.

Transfer
may terminate
the transferor's
current authority

within the transferred
scope.

Transfer
shall remain distinct
from delegation.

---

## Revocation

REVOCATION

shall terminate
a delegated
or otherwise revocable
authority relationship.

Revocation
shall identify:

Authority relationship
being revoked.

Effective transition.

Revocation source.

Historical state.

Revocation
shall not erase
prior authority.

---

## Classification Authority

CLASSIFICATION_AUTHORITY

shall permit
an authoritative classifier
to determine
candidate classification

within a defined
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
and lifecycle state
transitions

within its declared scope.

Lifecycle Authority
shall not automatically
create semantic authority
over every governed artifact.

---

## Promotion Authority

PROMOTION_AUTHORITY

shall permit
an explicitly
authorized mechanism

to grant
or transition
normative authority

within its declared
scope.

A Promotion Gate
shall not possess
Promotion Authority

merely because
it uses
that name.

Its authority
shall itself
be traceable.

---

## Conflict Resolution Authority

CONFLICT_RESOLUTION_AUTHORITY

shall permit
an explicitly
authorized mechanism

to resolve
conflicting authority claims

within a defined
scope
and Repository
Authority Context.

Specificity
shall not automatically
create this authority.

Recency
shall not automatically
create this authority.

---

## Joint Authority

JOINT_AUTHORITY

shall represent
authority that requires
multiple
identified authority holders

to act jointly.

Joint Authority
shall identify
the applicable
joint decision rule.

No participating holder
shall be assumed
to possess
the full joint authority
individually.

---

## Quorum Authority

QUORUM_AUTHORITY

shall represent
authority dependent
upon satisfaction
of an explicit
quorum rule.

The rule shall identify:

Authorized participants.

Required threshold.

Decision scope.

Applicable conditions.

Failure behavior.

Quorum Authority
shall not be modeled
as simple
binary authority edges.

---

## Subordination

SUBORDINATION

shall represent
a relationship
where one artifact

must remain
conformant to
another applicable
authority

within overlapping
scope.

Subordination
shall not imply
that every semantic
relationship
between the artifacts
is hierarchical.

---

## Supersession

SUPERSESSION

shall explicitly identify:

Predecessor.

Successor.

Affected scope.

Effective transition.

Authority source.

Historical continuity.

Newness alone
shall not establish
supersession.

---

## Withdrawal

WITHDRAWAL

shall explicitly terminate
current authority

without requiring
a successor.

Withdrawal
shall identify:

Affected scope.

Effective transition.

Authority source.

Historical state.

---

## Suspension

SUSPENSION

shall temporarily
disable
current authority.

Suspension
shall identify:

Affected scope.

Effective transition.

Suspension source.

Resolution condition,
where applicable.

---

## Invalidation

INVALIDATION

shall explicitly
terminate current authority

because the governing
authority mechanism
has determined
the normative basis
invalid.

Invalidation
shall preserve
historical traceability.

---

## Historical Predecessor

HISTORICAL_PREDECESSOR

shall record
lineage

without implying
current authority.

Historical lineage
shall remain distinct
from current
authority precedence.

---

## Authority Conflict

Authority conflict
exists when
two simultaneously
applicable
authority relationships

within overlapping
scope
cannot both
be satisfied.

Conflict analysis
shall consider:

Repository Authority Context.

Scope.

Authority source.

Authority state.

Temporal applicability.

Conditions.

Explicit precedence.

Conflict Resolution Authority.

Joint or quorum rules.

---

## Authority Compatibility

Overlapping authority
relationships
may be:

COMPATIBLE.

COMPATIBLE_WITH_SCOPE.

CONDITIONALLY_COMPATIBLE.

CONFLICTING.

UNRESOLVED.

JOINTLY_GOVERNED.

Compatibility
shall not be inferred
from shared terminology.

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

Every artifact
that:

Promotes.

Delegates.

Transfers.

Revokes.

Suspends.

Invalidates.

Resolves conflicts.

or otherwise changes
normative authority

shall itself
possess traceable
authority
for that action.

Authority-granting mechanisms
shall not self-authorize.

Circular
authority-of-authority
chains

without an independently
valid root
shall be invalid.

---

## Authority Root

Every current
authority chain
shall be traceable

to at least one
valid authority root

within its Repository
Authority Context.

Candidate root mechanisms
may include:

Bootstrap Authority.

Constitutionally established
authority.

Other explicitly
recognized
authority-root mechanisms.

The model
shall not assume
that every
Repository Authority Context
shares one universal root.

---

## Circular Authority

Graph cycles
shall not automatically
be invalid.

A cycle
shall be invalid

when authority
within the cycle
cannot be traced
to an independently
valid authority root

or when
the cycle permits
scope expansion
without authority.

---

## Edge Minimality

Authority graph edges
shall represent
normative authority
relationships only.

The following
shall not automatically
create authority edges:

Dependency.

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

Enforce
applicable requirements.

Executable Contracts
shall not create
normative authority

merely through
execution or success.

---

## Implementation Relationship

Implementation
may realize
normative semantics.

Implementation
shall not create
authority
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

Current repository
foundation demonstrates
multiple
distinct authority scopes.

RC-001

Repository Constitution
Baseline 1.0.

Authority scope:

Constitutional
repository authority.

---

SL-001

Repository Specification
Lifecycle
Baseline 1.0.

Authority scope:

Normative lifecycle
semantics.

---

APC-001

Architecture Principle
Classification
Baseline 1.0.

Authority scope:

Architecture Principle
classification only.

---

These authority scopes
shall not be modeled
as interchangeable
levels
of one universal
linear hierarchy.

---

## Current Architecture Principle State

Architecture Principle
classification authority
exists.

No Architecture Principle
candidate
shall be assumed
authoritative

merely because
classification capability
exists.

---

## Current CTA State

Common Trust Architecture
remains
non-authoritative.

Historical use
of the term
within CP-001

shall not establish
CTA authority.

CTA,
if later promoted,

shall require
an explicit
authority transition.

---

## Candidate Invariants

Authority relationships
shall be typed.

Authority shall be explicit.

Authority shall be scoped.

Authority shall be traceable.

Authority shall be
context-bound.

Authority may be
conditional.

Authority may be
temporal.

Authority state
shall be explicit.

Authority source
shall be traceable.

Authority-granting mechanisms
shall themselves
possess authority.

Delegation
shall not exceed
source authority.

Transfer
shall remain distinct
from delegation.

Revocation
shall remain explicit.

Suspension
shall remain distinct
from invalidation.

Withdrawal
shall remain distinct
from supersession.

Historical authority
shall remain distinguishable
from never-authoritative state.

Classification authority
shall remain distinct
from candidate authority.

Lifecycle authority
shall remain distinct
from semantic authority.

Evidence
shall remain distinct
from authority.

Implementation
shall remain distinct
from authority.

Authority conflict
shall not be resolved
through implicit precedence.

Authority graph edges
shall remain minimal.

---

## Falsifiability

NAM-001
shall be refuted
or revised
if evidence demonstrates
that the typed
relationship model

cannot represent
repository authority
without:

Contradiction.

Unbounded authority
edge growth.

Authority ambiguity.

Circular self-authorization.

Silent scope expansion.

Loss of historical
traceability.

Unresolvable conflict.

False authority inheritance.

Candidate refutation
shall test at minimum:

Multiple roots.

Cross-context authority.

Circular authority chains.

Delegation.

Transfer.

Revocation.

Suspension.

Withdrawal.

Supersession.

Invalidation.

Conditional authority.

Temporal authority.

Joint authority.

Quorum authority.

Authority conflict.

Authority-of-authority.

Historical authority.

Never-authoritative candidates.

Executable contracts.

Implementation consensus.

Evidence-driven revision.

---

## Current Status

Identifier

NAM-001

Version

0.2

Status

Draft

Model

Typed Authority
Relationship Model

Refutation Cycles Completed

1

Authority Relationship Types

17

Authority States

9

Authority

NONE.

Promotion

PROHIBITED.

Next Required Activity

Refutation Cycle 2
Adversarial State
and Relationship Testing.

---

# End of Normative Authority Model
