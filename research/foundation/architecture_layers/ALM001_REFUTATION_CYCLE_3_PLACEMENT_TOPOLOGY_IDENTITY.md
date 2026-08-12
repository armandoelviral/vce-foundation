# ALM-001 Refutation Cycle 3

Target

ALM-001 Version 0.3 Draft

Title

Expanded Architecture
Responsibility Model

Refutation Type

Placement /
Topology
Identity Refutation

Status

Research

---

## Purpose

Determine whether
the surviving
placement-related
architectural responsibility

constitutes
an independent
architecture dimension

and determine
its minimum
correct identity.

Candidate names:

DEPLOYMENT_ARCHITECTURE.

INFRASTRUCTURE_ARCHITECTURE.

TOPOLOGY_ARCHITECTURE.

PLACEMENT_ARCHITECTURE.

The investigation
shall distinguish:

Architectural placement.

Operational deployment.

Infrastructure technology.

Runtime structure.

Network topology.

Failure-domain structure.

Data locality.

Security separation.

The candidate
shall survive
only if
its architectural
responsibility
cannot be represented
adequately
through existing
retained dimensions.

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

NAM-001
Normative Authority Model
Baseline 1.0.

ALM-001 remains
non-authoritative.

---

# PT-001 — VM Relocation

## Scenario

A service
moves from
VM A
to VM B

with no change
to architectural
correctness.

## Attack

Does this create
architectural
placement semantics?

## Analysis

No.

Operational relocation
without architectural impact

is deployment
or implementation detail.

## Result

DEPLOYMENT MECHANICS
INSUFFICIENT.

---

# PT-002 — Availability Zone Separation

## Scenario

Two replicas
must reside
in independent
availability zones.

## Attack

Can this be reduced
to Runtime Architecture?

## Analysis

No.

Runtime Architecture
may define
replication behavior,

but failure-domain
placement
is an independently
meaningful responsibility.

## Result

PLACEMENT RESPONSIBILITY
SURVIVES.

---

# PT-003 — Jurisdictional Placement

## Scenario

Data-processing components
must execute
within a defined
jurisdiction.

## Attack

Is this only
Data Architecture?

## Analysis

No.

Data Architecture
may define
locality requirements.

Architectural placement
determines
where realization
may occur.

## Result

DISTINCT
BUT INTERSECTING.

---

# PT-004 — Security Zone Placement

## Scenario

A sensitive component
must execute
inside a protected
network zone.

## Attack

Is this only
Security Architecture?

## Analysis

No.

Security Architecture
defines the
security boundary.

Placement responsibility
defines
where architectural
realization must occur.

## Result

DISTINCT
BUT INTERSECTING.

---

# PT-005 — Runtime Worker Placement

## Scenario

Runtime workers
must be distributed
across independent
failure domains.

## Attack

Does Runtime Architecture
fully subsume
the responsibility?

## Analysis

No.

Execution structure
and placement topology
remain distinguishable.

## Result

INDEPENDENT VALUE
SURVIVES.

---

# PT-006 — Network Topology

## Scenario

Architectural correctness
depends upon
network segmentation
and connectivity topology.

## Attack

Is this
TOPOLOGY_ARCHITECTURE?

## Analysis

Topology
describes one important
part of the responsibility,

but not all
placement semantics.

## Result

TOPOLOGY
TOO NARROW.

---

# PT-007 — Non-Network Placement

## Scenario

Architectural correctness
depends upon:

Physical region.

Hardware trust boundary.

Jurisdiction.

Failure domain.

None is primarily
a network topology concern.

## Attack

Can
TOPOLOGY_ARCHITECTURE
represent these
without semantic strain?

## Analysis

Not reliably.

## Result

TOPOLOGY
NOT SUFFICIENT
AS PRIMARY IDENTITY.

---

# PT-008 — Infrastructure Provider

## Scenario

A workload
moves from
Cloud Provider A
to Cloud Provider B

while preserving
all required
architectural constraints.

## Attack

Does infrastructure
provider identity
define this architecture?

## Analysis

No.

Provider
is implementation
or realization detail

unless architecture
depends materially
upon provider-specific
properties.

## Result

INFRASTRUCTURE
NAME OVER-BROAD.

---

# PT-009 — Infrastructure Technology

## Scenario

Kubernetes
is replaced
by another
orchestrator.

Architectural placement
semantics remain unchanged.

## Attack

Does Infrastructure
Architecture identity
remain useful?

## Analysis

The responsibility
survives implementation
replacement.

Infrastructure technology
is therefore
not its core identity.

## Result

INFRASTRUCTURE
NOT PRIMARY SEMANTIC
IDENTITY.

---

# PT-010 — Infrastructure-Specific Constraint

## Scenario

A hardware enclave
is required
for architectural correctness.

## Attack

Does this justify
INFRASTRUCTURE_ARCHITECTURE?

## Analysis

Not necessarily.

The architectural concern
is placement
into a qualifying
execution environment.

Infrastructure
realizes the requirement.

## Result

PLACEMENT
MORE PRECISE.

---

# PT-011 — Deployment Pipeline

## Scenario

CI/CD deploys
a component
to production.

## Attack

Does the deployment process
belong to
the candidate dimension?

## Analysis

No.

Deployment process
is lifecycle,
release,
or operational
concern.

## Result

DEPLOYMENT TERM
RISKS CONFLATION.

---

# PT-012 — Deployment State

## Scenario

A component
is:

Staged.

Canary.

Production.

## Attack

Are these
architectural
placement dimensions?

## Analysis

Not necessarily.

These may represent
release or lifecycle state.

## Result

DEPLOYMENT
NAME CONFLATES
LIFECYCLE.

---

# PT-013 — Placement Constraint

## Scenario

A component
must execute
within 5 milliseconds
of a data source.

## Attack

Is the core responsibility
deployment

or placement?

## Analysis

Placement.

The architectural meaning
concerns allowable
location relationships,

not the act
of deploying.

## Result

PLACEMENT
SUPPORTED.

---

# PT-014 — Co-Location

## Scenario

Components A and B
must be co-located.

## Attack

Can existing
responsibility dimensions
represent this
without a placement concept?

## Analysis

Not cleanly.

Runtime,
Data,
or Integration Architecture

may explain
why co-location matters,

but placement
captures
the structural location
constraint itself.

## Result

PLACEMENT
INDEPENDENT VALUE.

---

# PT-015 — Anti-Affinity

## Scenario

Components A and B
must never share
one failure domain.

## Attack

Is anti-affinity
only Runtime Architecture?

## Analysis

No.

Runtime may realize it,

but the architectural
placement relation
is independently meaningful.

## Result

PLACEMENT
SURVIVES.

---

# PT-016 — Region Constraint

## Scenario

An authority-sensitive
component
must run
inside one region.

## Attack

Does Security Architecture
or Data Architecture
fully express this?

## Analysis

They may define
the reason.

Placement Architecture
defines the
location constraint.

## Result

PLACEMENT
SURVIVES.

---

# PT-017 — Hardware Class Constraint

## Scenario

A workload
must run
on confidential-compute
hardware.

## Attack

Is this
Security Architecture?

## Analysis

Security Architecture
defines the required
security property.

Placement Architecture
defines
the admissible
execution placement.

## Result

INTERSECTION,
NOT SUBSUMPTION.

---

# PT-018 — Failure-Domain Geometry

## Scenario

A service
requires
3 replicas

across at least
2 independent
failure domains.

## Attack

Is this merely
a deployment count?

## Analysis

No.

The architecture
contains a placement
and resilience
constraint.

## Result

PLACEMENT
SURVIVES.

---

# PT-019 — Data Locality

## Scenario

Compute must remain
near data.

## Attack

Does Data Architecture
subsume the placement
responsibility?

## Analysis

No.

Data Architecture
defines data-side
locality semantics.

Placement Architecture
defines
compute-location
constraints.

## Result

DISTINCT.

---

# PT-020 — Integration Locality

## Scenario

Two systems
must communicate
through a specific
network boundary.

## Attack

Does Integration Architecture
subsume placement?

## Analysis

No.

Integration defines
interaction responsibility.

Placement defines
where endpoints
may exist.

## Result

DISTINCT.

---

# PT-021 — Placement Without Deployment

## Scenario

An architecture model
declares
location constraints

before any
deployment mechanism
exists.

## Attack

Can placement
be architectural
without deployment?

## Analysis

Yes.

## Result

DEPLOYMENT
NOT FUNDAMENTAL.

---

# PT-022 — Deployment Without Placement Semantics

## Scenario

An application
is deployed repeatedly

without any material
location constraints.

## Attack

Does deployment alone
create Placement Architecture?

## Analysis

No.

## Result

PLACEMENT
REQUIRES ARCHITECTURAL
MATERIALITY.

---

# PT-023 — Topology Without Placement

## Scenario

A logical graph
defines communication
relationships

without physical,
regional,
failure-domain,
or locality constraints.

## Attack

Is every topology
Placement Architecture?

## Analysis

No.

Topology alone
may belong
to Integration,
Runtime,
or another
responsibility.

## Result

TOPOLOGY
OVERGENERALIZES.

---

# PT-024 — Placement Without Topology

## Scenario

A component
must run
inside jurisdiction X

but no
inter-component topology
is specified.

## Attack

Can topology
fully represent
the responsibility?

## Analysis

No.

## Result

PLACEMENT
BROADER
THAN TOPOLOGY.

---

# PT-025 — Infrastructure Without Placement Semantics

## Scenario

A system
uses complex
infrastructure

but architecture
does not constrain
where components
must reside.

## Attack

Does complexity
justify an
Infrastructure Architecture
dimension?

## Analysis

No.

Implementation complexity
is insufficient.

## Result

INFRASTRUCTURE
OVERGENERALIZES.

---

# PT-026 — Placement and Scaling

## Scenario

Replica count
changes dynamically

while placement
constraints remain
stable.

## Attack

Is scaling
part of
Placement Architecture?

## Analysis

Only where scaling
interacts materially
with placement rules.

Replica count alone
is not enough.

## Result

BOUNDARY
SURVIVES.

---

# PT-027 — Placement and Capacity

## Scenario

A workload
requires a minimum
hardware capacity.

## Attack

Is capacity
a placement responsibility?

## Analysis

Possibly,

when it defines
admissible execution
locations.

But raw resource sizing
may remain
implementation detail.

## Result

MATERIALITY
REQUIRED.

---

# PT-028 — Placement and Resilience

## Scenario

Resilience
depends upon
geographic distribution.

## Attack

Can Runtime Architecture
express resilience alone?

## Analysis

It may define
behavior,

but geographic
placement constraint
remains independent.

## Result

PLACEMENT
SURVIVES.

---

# PT-029 — Placement and Compliance

## Scenario

Compliance requires
processing within
specific boundaries.

## Attack

Is this
Domain Architecture?

## Analysis

Domain or regulatory
semantics may define
the requirement.

Placement captures
architectural realization
of location constraints.

## Result

DISTINCT.

---

# PT-030 — Placement and Artifact Architecture

## Scenario

A specific artifact
may execute only
in approved
environments.

## Attack

Does Artifact Architecture
subsume placement?

## Analysis

No.

Artifact Architecture
identifies
artifact admission
or compatibility.

Placement defines
the admissible
execution location.

## Result

DISTINCT.

---

# PT-031 — Placement as Relationship Only

## Attack

Could placement
be represented solely
through relationships
between existing
responsibility dimensions?

## Analysis

Not adequately.

Relationships can express:

USES.

CONSTRAINS.

INTERSECTS.

But they do not
provide a responsibility
dimension
for location,
affinity,
failure-domain,
and admissible-environment
semantics.

## Result

INDEPENDENT DIMENSION
JUSTIFIED.

---

# PT-032 — Placement as Context Only

## Attack

Could Architecture Context
fully replace
Placement Architecture?

## Analysis

No.

Architecture Context
defines
where classification
is evaluated.

Placement Architecture
defines
architectural constraints
about where realization
may occur.

## Result

NOT REDUCIBLE
TO CONTEXT.

---

# PT-033 — Placement as Runtime Property

## Attack

Could every
placement responsibility
be represented
inside
Runtime Architecture?

## Analysis

No.

Placement semantics
may apply to:

Data processing.

Artifacts.

Security boundaries.

Integration endpoints.

Non-runtime resources.

## Result

NOT SUBSUMED.

---

# PT-034 — Placement as Security Property

## Attack

Could every
placement rule
be modeled
as Security Architecture?

## Analysis

No.

Failure-domain,
latency,
resilience,
and locality

may be architectural
without primary
security purpose.

## Result

NOT SUBSUMED.

---

# PT-035 — Placement as Data Property

## Attack

Could every
placement rule
be modeled
as Data Architecture?

## Analysis

No.

Many placement
constraints
do not involve data.

## Result

NOT SUBSUMED.

---

# PT-036 — Placement as Integration Property

## Attack

Could every
placement rule
be modeled
as Integration Architecture?

## Analysis

No.

Placement can exist
without an integration
boundary.

## Result

NOT SUBSUMED.

---

# PT-037 — Naming: Deployment Architecture

## Evaluation

DEPLOYMENT_ARCHITECTURE
suggests:

Deployment process.

Release activity.

Operational rollout.

These are broader
or different
from the demonstrated
architectural responsibility.

## Result

REJECT NAME.

---

# PT-038 — Naming: Infrastructure Architecture

## Evaluation

INFRASTRUCTURE_ARCHITECTURE
suggests:

Infrastructure technology.

Platform components.

Operational substrate.

The demonstrated
responsibility
can survive
infrastructure replacement.

## Result

REJECT NAME.

---

# PT-039 — Naming: Topology Architecture

## Evaluation

TOPOLOGY_ARCHITECTURE
captures structural
arrangement

but does not
adequately cover:

Jurisdiction.

Admissible environment.

Affinity.

Anti-affinity.

Physical or logical
placement constraints.

## Result

REJECT NAME
AS TOO NARROW.

---

# PT-040 — Naming: Placement Architecture

## Evaluation

PLACEMENT_ARCHITECTURE

directly captures
the demonstrated
independent responsibility:

Where architectural
realization
may or must occur,

including:

Location.

Affinity.

Anti-affinity.

Failure domains.

Admissible environments.

Locality.

Jurisdiction.

Resilience placement.

## Result

BEST CURRENT
IDENTITY.

---

# Placement Responsibility Finding

The adversarial set
demonstrates
an independent
architectural
responsibility

for constraining
where architectural
realization
may or must occur.

This responsibility
is not adequately
subsumed by:

Runtime Architecture.

Artifact Architecture.

Security Architecture.

Data Architecture.

Integration Architecture.

Architecture Context.

---

# Naming Finding

The candidate names
were evaluated.

DEPLOYMENT_ARCHITECTURE

was rejected
because it conflates
architectural placement
with deployment process
and lifecycle activity.

INFRASTRUCTURE_ARCHITECTURE

was rejected
because it over-associates
the responsibility
with implementation
substrate.

TOPOLOGY_ARCHITECTURE

was rejected
because topology
is narrower
than the demonstrated
responsibility.

PLACEMENT_ARCHITECTURE

best matches
the surviving semantics.

---

# Placement Boundary

PLACEMENT_ARCHITECTURE

shall represent
architectural responsibility
for constraints
on where realization
may or must occur.

It may include:

Location constraints.

Affinity.

Anti-affinity.

Failure-domain
distribution.

Admissible environments.

Jurisdiction.

Locality.

Resilience placement.

Placement Architecture
shall not include
ordinary deployment
or operations mechanics

unless they
materially affect
architectural correctness.

---

# Implementation Boundary Finding

The same
Placement Architecture
may be realized by
different:

Cloud providers.

Orchestrators.

Schedulers.

Operating systems.

Infrastructure platforms.

Therefore
implementation substrate
shall not define
Placement Architecture
identity.

---

# Intersection Finding

Placement Architecture
may intersect:

Runtime Architecture.

Artifact Architecture.

Security Architecture.

Data Architecture.

Integration Architecture.

Domain Architecture.

Intersection
shall not imply
subsumption.

---

# Taxonomy Finding

The retained taxonomy
may now expand
from seven
to eight
responsibility dimensions.

The eighth
candidate is:

PLACEMENT_ARCHITECTURE.

No evidence
from this cycle
requires
reintroducing:

DEPLOYMENT_ARCHITECTURE.

INFRASTRUCTURE_ARCHITECTURE.

TOPOLOGY_ARCHITECTURE.

as independent
peer dimensions.

---

# Relationship Finding

No new
relationship type
was required.

The existing
seven
architectural relationship
types
remain sufficient
for the evaluated
placement cases.

---

# Refutation Outcome

Target

ALM-001 Version 0.3 Draft.

Outcome

SURVIVES
TARGETED
PLACEMENT REFUTATION

WITH TAXONOMY
EXPANSION.

Placement Responsibility

INDEPENDENT VALUE
DEMONSTRATED.

Selected Identity

PLACEMENT_ARCHITECTURE.

DEPLOYMENT_ARCHITECTURE

REJECTED
AS PRIMARY IDENTITY.

INFRASTRUCTURE_ARCHITECTURE

REJECTED
AS PRIMARY IDENTITY.

TOPOLOGY_ARCHITECTURE

REJECTED
AS PRIMARY IDENTITY.

Retained Dimensions
for Next Revision

8.

Relationship Types

7
UNCHANGED.

Architecture Context

SURVIVES.

Multi-Dimensional
Participation

SURVIVES.

Graph Minimality

SURVIVES.

Authority

NONE.

Promotion

PROHIBITED.

Next Required Activity

ALM-001 Version 0.4

Reduced Architecture
Responsibility Model

with eight
retained dimensions.

---

# End of ALM-001 Refutation Cycle 3
