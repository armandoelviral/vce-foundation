# ALM-001 Refutation Cycle 2

Target

ALM-001 Version 0.2 Draft

Title

Architecture Responsibility
Candidate Model

Refutation Type

Targeted Candidate
Responsibility Refutation

Status

Research

---

## Purpose

Determine whether
the four candidate
responsibility dimensions

identified during
Refutation Cycle 1

possess independently
necessary
architectural semantics.

Candidates:

DATA_ARCHITECTURE.

INTEGRATION_ARCHITECTURE.

DEPLOYMENT_ARCHITECTURE.

OBSERVABILITY_ARCHITECTURE.

A candidate
shall survive
only if
its responsibilities

cannot be represented
adequately

through the retained
responsibility dimensions

without semantic loss
or harmful conflation.

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

# TR-001 — Data Ownership

## Scenario

A system
defines explicit
ownership boundaries

for persistent data.

## Attack

Can this be represented
entirely as
Domain Architecture?

## Analysis

Not always.

Domain ownership
may define
business meaning,

while data ownership
may define
architectural responsibility
for storage,
mutation,
and custody.

## Result

DATA CANDIDATE
SURVIVES.

---

# TR-002 — Data Consistency

## Scenario

A distributed system
requires explicit
consistency semantics.

## Attack

Is this only
Runtime Architecture?

## Analysis

No.

Runtime mechanisms
may implement
consistency,

but architectural
consistency responsibility
may exist independently
of one runtime.

## Result

DATA CANDIDATE
SURVIVES.

---

# TR-003 — Data Locality

## Scenario

Architectural correctness
depends upon
where data
may physically
or jurisdictionally reside.

## Attack

Is this only
Deployment Architecture?

## Analysis

Not necessarily.

Deployment may realize
locality,

but data locality
may remain
an independent
data responsibility.

## Result

DATA CANDIDATE
SURVIVES.

---

# TR-004 — Artifact Data

## Scenario

Data is stored
inside
versioned artifacts.

## Attack

Does Artifact Architecture
fully subsume
Data Architecture?

## Analysis

No.

Artifact identity
and data semantics
remain distinguishable.

## Result

DATA
NOT SUBSUMED.

---

# TR-005 — Domain Data

## Scenario

Data represents
domain entities.

## Attack

Does Domain Architecture
fully subsume
Data Architecture?

## Analysis

No.

Domain meaning
and data
structural responsibility

may intersect
without equivalence.

## Result

DATA
NOT SUBSUMED.

---

# TR-006 — Runtime Data

## Scenario

Data exists only
during execution.

## Attack

Does Runtime Architecture
fully subsume
Data Architecture?

## Analysis

Not necessarily.

Ephemeral data
may still have
architectural responsibilities
around:

Ownership.

Consistency.

Isolation.

Transformation.

## Result

DATA
SURVIVES.

---

# TR-007 — Security Data

## Scenario

Sensitive data
requires
confidentiality constraints.

## Attack

Does Security Architecture
fully subsume
Data Architecture?

## Analysis

No.

Security responsibility
and data responsibility
remain distinct.

## Result

DATA
SURVIVES.

---

# TR-008 — Data Without Persistence

## Scenario

A streaming system
contains no durable
data store.

## Attack

Does Data Architecture
still exist?

## Analysis

Potentially yes.

Data movement,
ownership,
transformation,
and consistency

may remain architectural
responsibilities.

## Result

PERSISTENCE
NOT REQUIRED.

---

# TR-009 — Data as Cross-Cutting Concern

## Attack

Could Data Architecture
be treated merely
as intersections
between Domain,
Runtime,
Artifact,
and Security?

## Analysis

Possibly,

but doing so
would distribute
data ownership,
movement,
consistency,
and locality

across unrelated
responsibility dimensions.

This risks
semantic fragmentation.

## Result

INDEPENDENT VALUE
DEMONSTRATED.

---

# TR-010 — Data Candidate Outcome

## Finding

DATA_ARCHITECTURE
demonstrates
independent responsibility

not adequately reducible
to the retained
five dimensions.

## Result

PROMOTE INTO
RETAINED TAXONOMY
FOR NEXT REVISION.

---

# TR-011 — External Protocol Boundary

## Scenario

A system
integrates with
an external system

through a stable
protocol boundary.

## Attack

Can this be represented
as Shared Architecture?

## Analysis

Not necessarily.

A protocol
may not be reusable
across multiple contexts.

Integration responsibility
may still exist.

## Result

INTEGRATION CANDIDATE
SURVIVES.

---

# TR-012 — Messaging Topology

## Scenario

Architectural correctness
depends upon
message routing,
delivery,
and boundary semantics.

## Attack

Is this only
Runtime Architecture?

## Analysis

Runtime realizes
the messaging behavior,

but integration
responsibility
may remain distinct.

## Result

INTEGRATION
SURVIVES.

---

# TR-013 — Domain Contract

## Scenario

Two domains communicate
through an explicit
contract.

## Attack

Is this only
Domain Architecture?

## Analysis

No.

Domain meaning
and inter-domain
integration responsibility

are distinguishable.

## Result

INTEGRATION
SURVIVES.

---

# TR-014 — Shared Interface

## Scenario

One interface
is reused
across many systems.

## Attack

Does Shared Architecture
subsume Integration Architecture?

## Analysis

No.

Shared
describes reuse context.

Integration
describes boundary
and interaction responsibility.

## Result

DISTINCT DIMENSIONS.

---

# TR-015 — Runtime Invocation

## Scenario

Service A
calls Service B.

## Attack

Does every invocation
create
Integration Architecture?

## Analysis

No.

Execution interaction
alone
is insufficient.

Integration Architecture
requires
architecturally meaningful
system-boundary responsibility.

## Result

BOUNDARY REQUIRED.

---

# TR-016 — Internal Module Call

## Scenario

Two modules
inside one component
call each other.

## Attack

Is this integration?

## Analysis

Not necessarily.

No independently
meaningful integration
boundary
may exist.

## Result

OVERGENERALIZATION
REFUTED.

---

# TR-017 — Integration Without External System

## Scenario

Two independently
evolving subsystems
within one system

communicate through
a durable contract.

## Attack

Must integration
cross organizational
or repository boundaries?

## Analysis

No.

Independent evolution
and architectural boundary
may be sufficient.

## Result

EXTERNALITY
NOT REQUIRED.

---

# TR-018 — Integration as Relationship Only

## Attack

Could Integration Architecture
be replaced
by relationship types
such as:

USES.

EXPOSES.

COMPOSES_WITH.

## Analysis

Not fully.

Those relationships
describe structural edges.

They do not capture
the architectural responsibility
for maintaining
interaction boundaries,
protocol compatibility,
and mediation.

## Result

INDEPENDENT VALUE
DEMONSTRATED.

---

# TR-019 — Integration and Security

## Scenario

An API boundary
contains authentication
and authorization.

## Attack

Does Security Architecture
subsume Integration Architecture?

## Analysis

No.

Security and integration
responsibilities intersect.

## Result

INTEGRATION
SURVIVES.

---

# TR-020 — Integration Candidate Outcome

## Finding

INTEGRATION_ARCHITECTURE
demonstrates
independent responsibility

not adequately reducible
to the retained taxonomy.

## Result

PROMOTE INTO
RETAINED TAXONOMY
FOR NEXT REVISION.

---

# TR-021 — Availability Zones

## Scenario

A system
requires replicas
across independent
failure zones.

## Attack

Is this merely
implementation deployment?

## Analysis

Not when
architectural correctness
depends upon
failure-domain separation.

## Result

DEPLOYMENT CANDIDATE
SURVIVES.

---

# TR-022 — Placement Constraint

## Scenario

A component
must execute
near a data source.

## Attack

Is locality
only implementation detail?

## Analysis

Not when
latency,
jurisdiction,
or failure behavior

is an architectural
constraint.

## Result

DEPLOYMENT
SURVIVES.

---

# TR-023 — Runtime Topology

## Scenario

Runtime architecture
defines distributed workers.

## Attack

Does Runtime Architecture
fully subsume
Deployment Architecture?

## Analysis

No.

Runtime responsibility
defines execution structure.

Deployment responsibility
defines placement
of that structure
into operational topology.

## Result

DISTINCT
PROVISIONALLY.

---

# TR-024 — Security Placement

## Scenario

A security boundary
requires
physical or network
separation.

## Attack

Does Security Architecture
subsume Deployment Architecture?

## Analysis

No.

Security defines
why separation
is required.

Deployment defines
how architectural
placement boundaries
must exist.

## Result

DISTINCT.

---

# TR-025 — Deployment Without Architectural Constraint

## Scenario

An operator
moves a service
from one VM
to another

without semantic
architectural impact.

## Attack

Is this
Deployment Architecture?

## Analysis

No.

Operational placement
alone
is implementation
or operations detail.

## Result

ARCHITECTURAL
MATERIALITY REQUIRED.

---

# TR-026 — Container Count

## Scenario

Deployment changes
from three containers
to five.

## Attack

Does the Architecture
Responsibility Model change?

## Analysis

Not necessarily.

Scale mechanics
alone
do not imply
architectural responsibility.

## Result

IMPLEMENTATION
BOUNDARY SURVIVES.

---

# TR-027 — Failure Domain

## Scenario

The architecture
requires
independent failure domains.

## Attack

Can this be represented
solely through
Security or Runtime?

## Analysis

Not adequately
in every case.

Availability structure
may have
independent architectural
meaning.

## Result

DEPLOYMENT
INDEPENDENT VALUE
DEMONSTRATED.

---

# TR-028 — Deployment Topology as Context

## Attack

Could Deployment Architecture
be represented only
as Architecture Context?

## Analysis

Not fully.

Context identifies
where classification
is evaluated.

Deployment responsibility
may itself
contain architecture
constraints.

## Result

NOT REDUCIBLE
TO CONTEXT.

---

# TR-029 — Deployment versus Infrastructure Architecture

## Question

Is
DEPLOYMENT_ARCHITECTURE

the correct
name and scope?

## Analysis

Possibly not.

Some demonstrated
responsibilities
may be broader:

Placement.

Topology.

Failure domains.

Network boundaries.

Infrastructure realization.

The candidate
survives semantically,

but terminology
may be too narrow.

## Result

SEMANTICS SURVIVE,
NAME UNDER REVIEW.

---

# TR-030 — Deployment Candidate Outcome

## Finding

A placement/topology
architectural responsibility
has independent value.

## Result

CANDIDATE SURVIVES

but requires
scope and naming
refinement
before inclusion.

---

# TR-031 — Telemetry

## Scenario

A system
produces metrics
and logs.

## Attack

Does telemetry existence
create
Observability Architecture?

## Analysis

No.

Instrumentation alone
is insufficient.

## Result

OVERGENERALIZATION
REFUTED.

---

# TR-032 — Trace Correlation

## Scenario

Distributed trace
correlation
is necessary
to understand
cross-service execution.

## Attack

Is this
Runtime Architecture?

## Analysis

Potentially.

It may be
a runtime-supporting
responsibility

rather than
independent architecture.

## Result

OBSERVABILITY
UNDER PRESSURE.

---

# TR-033 — Auditability

## Scenario

A system
must preserve
audit evidence
across security
boundaries.

## Attack

Is this
Observability Architecture?

## Analysis

Possibly,

but the responsibility
may belong
to:

Security Architecture.

Evidence Processing.

Artifact Architecture.

## Result

INDEPENDENCE
NOT DEMONSTRATED.

---

# TR-034 — Operational Evidence

## Scenario

Operational evidence
is consumed
for later verification.

## Attack

Does this create
Observability Architecture?

## Analysis

Not necessarily.

Evidence generation
and evidence processing
may be modeled
outside ALM-001.

## Result

BOUNDARY
UNCLEAR.

---

# TR-035 — Diagnostic Boundary

## Scenario

A subsystem
must expose
diagnostic state.

## Attack

Can EXPOSES
plus Runtime Architecture
represent the responsibility?

## Analysis

Often yes.

## Result

POSSIBLE REDUCTION.

---

# TR-036 — Observability Without Runtime

## Scenario

A static artifact
contains
provenance metadata.

## Attack

Is this Observability?

## Analysis

No.

Artifact provenance
is better represented
through Artifact Architecture
or evidence models.

## Result

OBSERVABILITY
NOT GENERAL.

---

# TR-037 — Security Monitoring

## Scenario

A security system
monitors
authentication failures.

## Attack

Is this independent
Observability Architecture?

## Analysis

Not necessarily.

The primary
architectural responsibility
may be Security.

## Result

SUBSUMPTION POSSIBLE.

---

# TR-038 — Domain Monitoring

## Scenario

A commercial domain
monitors
domain-specific events.

## Attack

Does monitoring
create independent
architecture?

## Analysis

No.

Monitoring alone
does not establish
independent responsibility.

## Result

OBSERVABILITY
WEAKENED.

---

# TR-039 — Cross-Cutting Observability

## Attack

Could observability
be represented
as:

Runtime responsibility.

Security responsibility.

Domain responsibility.

Evidence-processing concern.

EXPOSES relationships.

## Analysis

For the evaluated cases,
yes.

No unique
architectural responsibility

has yet been shown
that requires
an independent
Observability dimension.

## Result

REDUCIBLE.

---

# TR-040 — Observability Candidate Outcome

## Finding

OBSERVABILITY_ARCHITECTURE

has not demonstrated
independent necessity.

## Result

REFUTED
AS INDEPENDENT
RESPONSIBILITY DIMENSION.

---

# Targeted Refutation Findings

Candidates Evaluated

4.

DATA_ARCHITECTURE

Independent Value

DEMONSTRATED.

---

INTEGRATION_ARCHITECTURE

Independent Value

DEMONSTRATED.

---

DEPLOYMENT_ARCHITECTURE

Independent Value

PARTIALLY DEMONSTRATED.

Naming and scope

REQUIRE REFINEMENT.

---

OBSERVABILITY_ARCHITECTURE

Independent Value

NOT DEMONSTRATED.

---

# Data Architecture Finding

Data responsibilities
cannot be represented
adequately
through only:

Domain.

Runtime.

Artifact.

Security.

Shared.

Data ownership,
consistency,
movement,
locality,
and transformation

demonstrate
an independent
responsibility dimension.

DATA_ARCHITECTURE
shall enter
the retained
candidate taxonomy
in the next revision.

---

# Integration Architecture Finding

Integration responsibilities
cannot be reduced
to:

Shared Architecture.

Domain Architecture.

Runtime Architecture.

or architectural
relationship edges alone.

Protocol boundaries,
inter-system contracts,
messaging,
and compatibility

demonstrate
independent
architectural responsibility.

INTEGRATION_ARCHITECTURE
shall enter
the retained
candidate taxonomy
in the next revision.

---

# Deployment Architecture Finding

Placement,
topology,
and failure-domain
responsibilities

demonstrate
independent
architectural value.

However,
DEPLOYMENT_ARCHITECTURE
may be too narrow
or implementation-associated
as terminology.

The responsibility
shall survive,

but the next revision
shall evaluate
whether its proper identity is:

DEPLOYMENT_ARCHITECTURE.

INFRASTRUCTURE_ARCHITECTURE.

TOPOLOGY_ARCHITECTURE.

or another
more precise term.

---

# Observability Architecture Finding

The evaluated
Observability responsibilities

can presently
be represented through
existing responsibility
dimensions
and external
processing models.

No independently
necessary
architectural responsibility
was demonstrated.

OBSERVABILITY_ARCHITECTURE

shall not enter
the retained taxonomy
without new evidence.

---

# Taxonomy Result

Version 0.2
retained:

5 dimensions.

Targeted refutation
demonstrates:

2 additions
with strong support.

1 addition
with semantic support
but unresolved naming.

1 candidate
refuted
as independent.

The next revision
shall therefore
contain:

7 stable
responsibility dimensions.

1 unresolved
placement/topology
candidate.

0 independent
Observability dimension.

---

# Relationship Impact

No new
architectural relationship
type
was required
by the targeted
candidate tests.

The existing
seven relationship types
were sufficient
for structural
relationships encountered.

Relationship taxonomy
therefore remains:

7 provisional types.

---

# Minimality Finding

Adding Data
and Integration

reduces harmful
semantic conflation.

Adding Observability
would currently
increase taxonomy
without demonstrated
independent value.

Placement/topology
responsibility
requires one more
focused naming
and boundary test

before admission.

---

# Refutation Outcome

Target

ALM-001 Version 0.2 Draft.

Outcome

REFUTED
ON TAXONOMY
COMPLETENESS.

Responsibility Model

SURVIVES.

Five Retained Dimensions

SURVIVE.

DATA_ARCHITECTURE

ADD.

INTEGRATION_ARCHITECTURE

ADD.

DEPLOYMENT_ARCHITECTURE

SURVIVES
SEMANTICALLY,
IDENTITY UNRESOLVED.

OBSERVABILITY_ARCHITECTURE

REFUTED
AS INDEPENDENT.

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

ALM-001 Version 0.3

Expanded Architecture
Responsibility Model

with targeted
Placement / Topology
Identity Refutation.

---

# End of ALM-001 Refutation Cycle 2
