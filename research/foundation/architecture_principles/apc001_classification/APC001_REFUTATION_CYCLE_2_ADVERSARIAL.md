# APC-001 Refutation Cycle 2

Target

APC-001 Version 0.2 Draft

Title

Architecture Principle Classification Model

Refutation Type

Adversarial Classification Cases

Status

Research

---

## Purpose

Attempt to defeat
APC-001 Version 0.2

using candidate propositions
designed to appear
architecturally legitimate

while containing:

Layer confusion.

Hidden redundancy.

Scope inflation.

Semantic duplication.

Conditional applicability.

Technology capture.

Authority inflation.

Composition failure.

Subsumption.

Implementation leakage.

The objective
is to determine whether
APC-001 can reject,
reduce,
relocate,
or preserve

difficult candidates
without relying upon
naming
or architectural intuition.

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

# AC-001 — Security-Sounding Architecture Principle

## Candidate

All sensitive services
shall use
mutual TLS.

## Attack

The proposition
is security-critical
and affects
many systems.

Should it become
an Architecture Principle?

## Analysis

No.

The candidate specifies
a concrete mechanism.

Its architectural
purpose may be valid,

but mTLS itself
belongs to:

Security specification.

Protocol profile.

Deployment requirements.

A more abstract
architectural proposition
may exist,

such as authenticated
peer communication,

but must be
independently justified.

## Expected Classification

RELOCATE_TO_SECURITY.

## Result

PASS.

---

# AC-002 — Runtime Architecture Candidate

## Candidate

Runtime execution
shall occur
inside a declared
execution boundary.

## Attack

Is this Runtime behavior
or Runtime Architecture?

## Analysis

The proposition
constrains structural
relationship between
Runtime execution
and host environment.

It does not prescribe
a specific mechanism.

It may therefore qualify
as a bounded
Runtime Architecture
candidate.

Further necessity
and evidence analysis
remain required.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE.

Scope

Runtime Architecture.

## Result

PASS.

---

# AC-003 — Runtime Specification Candidate

## Candidate

Runtime memory
shall never exceed
512 MiB.

## Attack

It constrains every
Runtime implementation.

Is it architectural?

## Analysis

No.

The proposition
defines
a concrete
behavioral/resource limit.

It belongs to
Runtime Specification
or Execution Profile.

## Expected Classification

RELOCATE_TO_RUNTIME.

## Result

PASS.

---

# AC-004 — Artifact Architecture Candidate

## Candidate

Artifact admission
shall require
independent identity
and integrity evidence.

## Attack

Does Artifact subject matter
force relocation
to Artifact Specification?

## Analysis

Not necessarily.

If the proposition
constrains relationships
across artifact admission
mechanisms

without prescribing
a schema
or algorithm,

it may represent
Artifact Architecture.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE.

Scope

Artifact Architecture.

## Result

PASS.

---

# AC-005 — Artifact Format Candidate

## Candidate

Artifact identity
shall be encoded
as SHA-256
in field
artifact_hash.

## Attack

Is this
Artifact Architecture?

## Analysis

No.

It defines:

Algorithm.

Field name.

Representation.

This belongs
to specification
or schema.

## Expected Classification

RELOCATE_TO_ARTIFACT.

## Result

PASS.

---

# AC-006 — Constitutional Restatement

## Candidate

Implementation
shall not create
normative authority.

## Attack

This is clearly
architecturally useful.

Should it become
an AP?

## Analysis

No.

Its full normative
meaning
already exists
in RC-001.

An AP
would duplicate
constitutional authority.

## Expected Classification

REDUNDANT_WITH_CONSTITUTION.

## Result

PASS.

---

# AC-007 — Partial Constitutional Overlap

## Candidate

Reference implementations
shall not create
normative authority

and shall remain
replaceable
without changing
normative contracts.

## Attack

The first half
duplicates RC-001.

The second half
may be architectural.

Should the entire
candidate be rejected?

## Analysis

No.

APC-001 Reduction
requires separating
the redundant
constitutional clause

from the potentially
independent
architectural constraint.

## Expected Classification

REDUCE.

## Result

PASS.

---

# AC-008 — Scope Inflation

## Candidate

All repository abstractions
shall remain
domain-independent.

## Attack

Could this
be a strong
architecture principle?

## Analysis

No.

Domain-local abstractions
may legitimately exist.

The candidate
claims broader scope
than justified.

## Expected Classification

REDUCE
or
REFUTED.

## Result

PASS.

---

# AC-009 — Bounded Scope

## Candidate

Shared architectural
semantics
shall not silently acquire
domain-specific meaning.

## Attack

The candidate
does not apply
to domain-local
architecture.

Does bounded applicability
disqualify it?

## Analysis

No.

The scope
can be explicitly limited
to shared architecture.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE.

Scope

Shared Architecture.

## Result

PASS.

---

# AC-010 — Conditional Applicability

## Candidate

Architectural claims
that materially depend
upon external trust
shall identify
those trust assumptions.

## Attack

The candidate
is conditional.

Can an AP
be conditional?

## Analysis

Yes.

Applicability
is explicit
and architecturally meaningful.

Constitutional necessity
is not implied.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE.

## Result

PASS.

---

# AC-011 — Hidden Implementation Detail

## Candidate

Shared services
shall use
dependency injection

to remain
implementation-independent.

## Attack

The rationale
sounds architectural.

Does the implementation
pattern make it an AP?

## Analysis

No.

Dependency injection
is one implementation
or design mechanism.

The candidate confuses
goal
with technique.

## Expected Classification

RELOCATE_TO_IMPLEMENTATION
or
REFUTED.

## Result

CLASSIFICATION OUTCOME GAP.

---

# AC-012 — Missing Outcome

## Finding

APC-001 currently
does not define:

RELOCATE_TO_IMPLEMENTATION.

## Analysis

Some propositions
are neither:

Specification.

Runtime.

Artifact.

Security.

Domain.

Research.

Commercial.

They are simply
implementation
or engineering mechanics.

## Result

GAP IDENTIFIED.

---

# AC-013 — Technology-Specific Architecture Family

## Candidate

WASM runtimes
shall expose
explicit capability boundaries.

## Attack

Is Technology Independence
violated?

## Analysis

The candidate
may legitimately
belong to
a bounded
WASM architecture

but it cannot
claim general
repository architecture
authority.

The normative meaning
must remain scoped
to that technology family.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE
WITH TECHNOLOGY-BOUNDED SCOPE

or

RELOCATE_TO_RUNTIME.

## Result

AMBIGUITY REMAINS.

---

# AC-014 — Semantic Alias

## Candidate A

Shared assessment
shall not create
domain decision authority.

## Candidate B

Reusable evidence outputs
shall remain advisory
until interpreted
by domain authority.

## Attack

Can both become APs?

## Analysis

Potentially not.

They may express
the same
architectural constraint
using different vocabulary.

Semantic equivalence
must be tested.

## Expected Classification

REDUNDANT_WITH_EXISTING_AP
for one candidate.

## Result

PASS.

---

# AC-015 — Subsumed Candidate

## Candidate A

Implementation behavior
shall not silently
redefine
normative semantics.

## Candidate B

Reference Runtime behavior
shall not silently
redefine
normative semantics.

## Attack

Should both exist?

## Analysis

Candidate B
is likely a subset
of Candidate A.

Without independent
architectural necessity,

B should not receive
separate authority.

## Expected Classification

SUBSUMED.

## Result

PASS.

---

# AC-016 — Two Valid but Conflicting Principles

## AP Candidate A

All critical execution
shall maximize
deterministic isolation.

## AP Candidate B

All critical execution
shall maximize
environmental adaptability.

## Attack

Each could possess
reasonable
architectural evidence.

Can APC-001
promote both?

## Analysis

Not without
compatibility
and composition analysis.

Independent validity
does not establish
combined validity.

## Expected Classification

UNRESOLVED
or
CONFLICTING.

## Result

PASS.

---

# AC-017 — Conflict by Specificity

## Broad Candidate

Shared services
shall remain
stateless.

## Narrow Candidate

Audit services
shall preserve
durable state.

## Attack

Does narrower scope
automatically override
the broader principle?

## Analysis

No.

Specificity
shall not create
automatic authority precedence.

The relationship
must be explicit.

## Expected Classification

CONFLICTING
or
COMPATIBLE_WITH_SCOPE

depending upon
declared semantics.

## Result

PASS.

---

# AC-018 — Conflict by Recency

## Scenario

AP-001 Version 1.0
and AP-002 Version 2.0
conflict.

AP-002 is newer.

## Attack

Does recency
resolve the conflict?

## Analysis

No.

Version recency
does not create
cross-principle precedence.

## Expected Classification

CONFLICTING.

## Result

PASS.

---

# AC-019 — Composition Failure

## Candidate A

Every component
shall minimize
external dependencies.

## Candidate B

Every capability
shall be delegated
to specialized
external services.

## Attack

Each may be
internally coherent.

Can both coexist?

## Analysis

Potentially not.

Composition analysis
is required.

## Expected Classification

INCOMPATIBLE
or
UNRESOLVED.

## Result

PASS.

---

# AC-020 — Principle Fragmentation

## Scenario

One proposition:

Architectural assumptions
shall be explicit
and refutable.

is split into:

AP-X
Explicit assumptions.

AP-Y
Traceable assumptions.

AP-Z
Refutable assumptions.

## Attack

Can all three pass
candidate-level criteria?

## Analysis

Possibly.

Set-level minimality
and semantic cohesion
must prevent
artificial fragmentation.

## Expected Classification

REDUCE
or
SUBSUMED.

## Result

PASS.

---

# AC-021 — Principle Over-Aggregation

## Candidate

Architecture shall:

Expose assumptions.

Preserve provenance.

Separate domains.

Support replay.

Protect IP.

Limit memory.

Use evidence-driven
promotion.

## Attack

The candidate
contains many valuable rules.

Can it qualify
as one AP?

## Analysis

No.

Semantic cohesion fails.

Multiple concerns
belong to
different layers.

## Expected Classification

REDUCE.

## Result

PASS.

---

# AC-022 — Current Architecture Consensus

## Scenario

Every current subsystem
follows a candidate rule.

## Attack

Is repository-wide adoption
sufficient evidence
for promotion?

## Analysis

No.

Shared implementation history
may reflect
shared architectural bias.

## Expected Classification

INSUFFICIENT_EVIDENCE
unless independent
necessity is shown.

## Result

PASS.

---

# AC-023 — Formal Necessity

## Candidate

A formal proof
shows that
without constraint X,

two required
architectural invariants
cannot both hold.

No production evidence
exists yet.

## Attack

Is empirical evidence
required?

## Analysis

No.

Formal evidence
may establish
architectural necessity.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE.

## Result

PASS.

---

# AC-024 — Strong Empirical Evidence

## Candidate

Across many systems,
architecture lacking
constraint X
repeatedly fails.

No formal proof
exists.

## Attack

Can empirical evidence
support AP classification?

## Analysis

Yes,
if scope
and causal interpretation
are sufficiently justified.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE
or
INSUFFICIENT_EVIDENCE.

## Result

PASS.

---

# AC-025 — Domain-Family Principle

## Candidate

Within regulated
financial architecture,

decision evidence
and authorization
shall remain distinct.

## Attack

Does domain specificity
prevent AP classification?

## Analysis

No.

A Domain-family
Architecture Principle
may exist.

Its scope
must remain explicit.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE.

Scope

Domain-family Architecture.

## Result

PASS.

---

# AC-026 — Commercial Architecture Claim

## Candidate

Architecture shall
maximize proprietary
calibration secrecy.

## Attack

It influences
architectural design.

Does that make it
an AP?

## Analysis

Not necessarily.

The primary purpose
is commercial
asset protection.

Unless an independent
architectural invariant
exists,

the candidate belongs
to commercial
or security strategy.

## Expected Classification

RELOCATE_TO_COMMERCIAL
or
RELOCATE_TO_SECURITY.

## Result

PASS.

---

# AC-027 — Research Methodology Claim

## Candidate

Every architecture
shall be tested
against three
independent domains
before promotion.

## Attack

Does architectural
relevance make it
an AP?

## Analysis

No.

This is primarily
research
or promotion methodology.

The fixed count
also lacks
independent justification.

## Expected Classification

RELOCATE_TO_RESEARCH
or
REFUTED.

## Result

PASS.

---

# AC-028 — Specification Boundary

## Candidate

Every API response
shall contain
a provenance field.

## Attack

Could this be
an Architecture Principle
because it promotes
traceability?

## Analysis

No.

It prescribes
interface structure.

## Expected Classification

RELOCATE_TO_SPECIFICATION.

## Result

PASS.

---

# AC-029 — Principle Evolution

## Scenario

An authoritative AP
is later shown
to be too broad.

## Attack

Can APC-001
permit silent editing
because architecture
is below Constitution?

## Analysis

No.

Lower authority
does not eliminate
normative history.

Versioned evolution
remains required.

## Expected Classification

CURRENT AP
REQUIRES
EXPLICIT EVOLUTION.

## Result

PASS.

---

# AC-030 — Candidate Passes Every Criterion

## Scenario

A candidate
passes all
twenty-two criteria.

## Attack

Does APC-001
therefore grant
Architecture Principle
authority?

## Analysis

No.

Classification
remains separate
from:

Promotion Eligibility.

Promotion Gate.

Authority transition.

## Expected Classification

ARCHITECTURE_PRINCIPLE_CANDIDATE.

Authority

NONE.

## Result

PASS.

---

# Adversarial Findings

Cases Evaluated

30.

Primary Misclassification
Failures

0.

Classifier Gaps

2.

Gap 1

No explicit
RELOCATE_TO_IMPLEMENTATION
outcome.

Gap 2

Technology-bounded
Architecture Principle
classification
requires clearer semantics.

---

# Required Clarifications

APC-001
shall clarify
that:

Implementation mechanics
may require
direct relocation
to Implementation.

Technology-bounded
architectural scope
may exist

without allowing
technology-specific
semantics
to redefine
higher authority.

A bounded
technology architecture
shall declare
its authority scope
explicitly.

---

# Classification Outcome Addition

The following
classification outcome
shall be added:

RELOCATE_TO_IMPLEMENTATION.

This outcome
shall apply
when the proposition
primarily defines:

Coding pattern.

Implementation technique.

Internal software structure.

Optimization mechanism.

Concrete engineering practice.

without independent
architecture-level semantics.

---

# Technology-Bounded Architecture Finding

A proposition
may be architectural
within
a technology-bounded
scope.

For example:

WASM Runtime Architecture.

OCI Artifact Architecture.

GPU Execution Architecture.

Such classification
does not grant
the technology
constitutional
or repository-wide
authority.

Technology-specific
architectural authority
shall remain subordinate
to broader
technology-independent
normative authority.

---

# Robustness Finding

APC-001 Version 0.2
successfully distinguished
in the adversarial set:

Architecture
from Specification.

Architecture
from Runtime behavior.

Architecture
from implementation mechanics.

Architecture
from constitutional duplication.

Architecture
from commercial concerns.

Bounded scope
from universal scope.

Candidate validity
from authority.

Individual validity
from compatibility.

Individual minimality
from set-level minimality.

The surviving gaps
require clarification

but do not refute
the core
classification model.

---

# Refutation Outcome

Target

APC-001 Version 0.2 Draft.

Outcome

SURVIVES
ADVERSARIAL
CLASSIFICATION REFUTATION

WITH REQUIRED
CLARIFICATIONS.

Cases Evaluated

30.

Primary
Misclassification Failures

0.

Classifier Gaps

2.

Core Classification Model

SURVIVES.

Conflict Boundary

SURVIVES.

Compatibility Model

SURVIVES.

Composition Model

SURVIVES.

Set-Level Minimality

SURVIVES.

Required New Outcome

RELOCATE_TO_IMPLEMENTATION.

Technology-Bounded Scope

REQUIRES
EXPLICIT CLARIFICATION.

Authority

NONE.

Freeze

PROHIBITED.

Promotion

PROHIBITED.

Next Required Activity

APC-001 Version 0.3

Adversarially Refined
Classification Model.

---

# End of APC-001 Refutation Cycle 2
