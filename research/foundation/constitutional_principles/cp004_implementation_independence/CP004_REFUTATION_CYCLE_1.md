# CP-004 Refutation Cycle 1

Target

CP-004 Version 0.1 Draft

Title

Implementation Independence

Refutation Type

Constitutional Redundancy
and Layer Contamination

Status

Research

---

## Purpose

Determine whether
CP-004 contains
an irreducible
Constitutional Principle

or whether
its propositions are:

Already governed
by RC-001.

Architectural constraints.

Runtime requirements.

Artifact requirements.

Supply-chain requirements.

Implementation choices.

Operational hardening.

Commercial strategy.

The objective
is not to preserve
CP-004 as written.

The objective
is to identify
which properties survive
and the authority layer
to which they belong.

---

## Governing Authority

This refutation
is subordinate to

RC-001
Repository Constitution
Baseline 1.0

and governed by

SL-001
Repository Specification Lifecycle
Baseline 1.0.

CP-004 remains
non-authoritative.

---

# II-001 — Constitutional Implementation Independence

## Claim

Repository normative
authority shall remain
independent
from implementation.

## Attack

Does CP-004 need
to establish
this independently?

## Analysis

No.

RC-001 already
establishes
Implementation Independence.

CP-004 cannot obtain
independent constitutional
necessity merely
by restating
an existing
constitutional invariant.

## Result

SURVIVES
BUT REDUNDANT
AT CONSTITUTIONAL LEVEL.

---

# II-002 — Technology Independence

## Claim

Normative semantics
shall not depend upon
a particular
technology.

## Attack

Does CP-004 provide
independent
constitutional protection?

## Analysis

No.

RC-001 already
establishes
Technology Independence.

## Result

CONSTITUTIONALLY
REDUNDANT.

---

# II-003 — Existing Code as Authority

## Scenario

A production implementation
already behaves
in a particular way.

The implementation
has existed
for years.

## Attack

Does historical
implementation behavior
create normative truth?

## Analysis

No.

Implementation existence,
age,
deployment,
or popularity
does not create
normative authority.

This follows
from RC-001
Implementation Independence.

## Result

SURVIVES
BUT ALREADY
CONSTITUTIONALLY COVERED.

---

# II-004 — Reference Implementation

## Claim

A Reference Implementation
shall remain
replaceable.

## Attack

Is replaceability
itself
a constitutional property?

## Analysis

Not necessarily.

The Constitution
requires normative authority
to remain independent
from implementation.

Whether a particular
Reference Implementation
must satisfy
specific replacement
properties

is an architectural
or specification-level
question.

## Result

ARCHITECTURAL PROPERTY
IDENTIFIED.

---

# II-005 — Runtime Replacement

## Scenario

Runtime A
is replaced
by Runtime B.

Both conform
to the same
normative specification
and executable contracts.

## Attack

Does implementation
replacement alter
normative meaning?

## Analysis

It should not.

But the mechanisms
required to prove
equivalence or conformance

belong below
constitutional authority.

## Result

SURVIVES
AS ARCHITECTURAL
AND VERIFICATION
CONCERN.

---

# II-006 — Programming Language

## Scenario

A Runtime
is implemented
in Python

and later
rewritten
in Rust.

## Attack

Does the programming
language define
normative semantics?

## Analysis

No.

Language choice
is an implementation
decision

unless a higher
normative artifact
explicitly constrains it
for a justified reason.

## Result

CONSTITUTIONAL CORE
ALREADY COVERED.

---

# II-007 — Library Dependency

## Scenario

An implementation
depends upon:

OpenCV.

ONNX.

CUDA.

or another library.

## Attack

Does dependency
selection belong
to constitutional authority?

## Analysis

No.

Library selection
is ordinarily
an implementation
or runtime concern.

A specification
may constrain
observable behavior

without constitutionalizing
the dependency.

## Result

RELOCATE.

---

# II-008 — Execution Environment

## Scenario

Correct execution
depends upon:

WASM.

WASI.

Containers.

Operating system
capabilities.

Hardware acceleration.

## Attack

Does RC-001 need
to prescribe
these mechanisms?

## Analysis

No.

Execution environment
constraints
belong to
runtime specifications,
execution profiles,
or deployment architecture.

## Result

RELOCATE.

---

# II-009 — Capability Isolation

## Claim

Runtime execution
shall possess
defined
capability boundaries.

## Attack

Is capability isolation
part of
Implementation Independence?

## Analysis

Not inherently.

Capability isolation
may be essential
for security

but represents
a Runtime
or security architecture
property.

## Result

SEPARATE CONCERN.

---

# II-010 — Artifact Identity

## Claim

Runtime artifacts
shall possess
stable identity.

## Attack

Is artifact identity
an Implementation
Independence principle?

## Analysis

Not necessarily.

Artifact identity
supports:

Verification.

Provenance.

Replay.

Attestation.

Supply-chain security.

It requires
its own
normative semantics.

## Result

RELOCATE
TO ARTIFACT
SEMANTICS.

---

# II-011 — Provenance

## Claim

Implementation artifacts
shall preserve
provenance.

## Attack

Does provenance
require
constitutional
Implementation Independence?

## Analysis

No.

Provenance
is independently useful

but belongs
to artifact,
evidence,
or supply-chain
semantics.

## Result

RELOCATE.

---

# II-012 — Reproducibility

## Claim

Implementations
shall be reproducible.

## Attack

Is universal
reproducibility
required
for implementation
independence?

## Analysis

No.

Normative semantics
may remain independent
from implementation

even when
a particular implementation
cannot be reproduced
bit-for-bit.

Reproducibility
may still be required
by a narrower
specification.

## Result

UNIVERSAL CLAIM
REFUTED.

---

# II-013 — Source Protection

## Scenario

Production packaging
attempts to hide
or exclude
source code.

## Attack

Does source exclusion
belong to
constitutional
Implementation Independence?

## Analysis

No.

Source protection
is an implementation,
deployment,
intellectual-property,
or commercial concern.

## Result

REMOVE
FROM CONSTITUTIONAL
CANDIDATE.

---

# II-014 — Compilation Strategy

## Scenario

An implementation
uses:

Cython.

Native compilation.

Multi-stage builds.

Binary packaging.

## Attack

Do these choices
establish
implementation independence?

## Analysis

No.

They are concrete
implementation
or deployment mechanisms.

Constitutionalizing them
would contradict
Technology Independence.

## Result

REMOVE
FROM CONSTITUTIONAL
CANDIDATE.

---

# II-015 — Calibration Assets

## Scenario

Commercial value
depends upon
proprietary:

Calibration.

Models.

Thresholds.

Reference data.

## Attack

Does protecting
those assets
constitute
Implementation Independence?

## Analysis

No.

They may represent
valuable implementation
or commercial assets.

Their protection
requires
separate architecture,
security,
or commercial policy.

## Result

SEPARATE CONCERN.

---

# II-016 — Implementation Optimization

## Scenario

One implementation
uses hardware acceleration.

Another uses
portable software execution.

Both satisfy
the same
normative contract.

## Attack

Does optimization
change normative authority?

## Analysis

No.

Performance strategy
shall not silently
redefine
normative semantics.

## Result

SURVIVES
AS CONSEQUENCE
OF RC-001.

---

# II-017 — Implementation-Specific Evidence

## Scenario

A particular implementation
produces strong
experimental evidence.

## Attack

Can successful
implementation evidence
promote its behavior
into normative truth?

## Analysis

No.

Evidence may challenge
or support
a normative proposition.

It does not
automatically acquire
normative authority.

## Result

SURVIVES.

---

# II-018 — Conformance Without Identity

## Scenario

Two implementations
are internally different

but satisfy
the same
observable
normative requirements.

## Attack

Must they be
structurally identical?

## Analysis

No.

Implementation Independence
requires
semantic conformance,

not internal
implementation identity.

## Result

SURVIVES
AS LOWER-LAYER
CONFORMANCE PROPERTY.

---

# II-019 — Normative Leakage from Implementation

## Scenario

A specification
is ambiguous.

Developers resolve
the ambiguity
by observing
the current implementation.

The observed behavior
then becomes
de facto normative.

## Attack

Is this acceptable?

## Analysis

No.

Implementation behavior
may expose
a specification defect.

The defect
must be resolved
through the appropriate
normative process.

The implementation
shall not silently
resolve
normative ambiguity.

## Result

SURVIVES STRONGLY.

---

# II-020 — Minimal Surviving Proposition

## Question

What remains
after removing:

RC-001 duplication.

Technology-specific choices.

Runtime isolation.

Artifact provenance.

Supply-chain semantics.

Deployment hardening.

Commercial protection.

Implementation mechanics.

## Analysis

A narrower proposition
survives:

Normative semantics
shall remain
independent
from any particular
implementation.

Multiple implementations
may realize
the same
normative contract.

Implementation behavior
shall not silently
create,
resolve,
or redefine
normative meaning.

## Attack

Is this proposition
independent
from RC-001?

## Analysis

Its constitutional core
is already governed
by RC-001.

Its operational consequences
belong to:

Architecture.

Specifications.

Executable Contracts.

Conformance.

Verification.

## Result

NO NEW
CONSTITUTIONAL CORE
IDENTIFIED.

---

# Refutation Findings

CP-004 Version 0.1
contains multiple
valuable concerns

but places them
under a single
constitutional label.

The candidate conflates:

Constitutional
Implementation Independence.

Technology Independence.

Reference implementation
replaceability.

Runtime isolation.

Execution environment.

Artifact identity.

Provenance.

Reproducibility.

Deployment hardening.

Source protection.

Commercial
intellectual property.

Conformance.

The constitutional core
is already governed
by RC-001.

---

# Surviving Distinctions

The following
shall remain distinct:

Normative semantics.

Implementation behavior.

Reference implementation.

Runtime environment.

Artifact identity.

Artifact provenance.

Conformance.

Reproducibility.

Deployment hardening.

Commercial
asset protection.

Evidence
from implementation

and

authority
of specification.

---

# Layer Classification

Constitutional:

Implementation Independence.

Technology Independence.

Already governed
by RC-001.

---

Architectural:

Reference implementation
replaceability.

Implementation substitution.

Normative-to-implementation
boundary.

---

Specification
and Contract:

Observable conformance.

Behavioral requirements.

Implementation-independent
contract semantics.

---

Runtime
and Security:

Execution isolation.

Capabilities.

Resource boundaries.

Execution environment.

---

Artifact
and Supply Chain:

Artifact identity.

Provenance.

Build evidence.

Artifact verification.

---

Implementation
and Deployment:

Programming language.

Libraries.

Compilation.

Containers.

Optimization.

Packaging.

---

Commercial:

Source protection.

Proprietary calibration.

Intellectual-property
strategy.

Commercial moat.

---

# Candidate Reduction

No independent
constitutional reduction
has yet been identified.

The strongest
surviving CP-004
properties
appear to be
consequences
of RC-001

plus lower-layer
architectural
and conformance rules.

A future reduced
candidate
shall not duplicate
RC-001.

If no independent
property survives,

CP-004 should proceed
directly toward
constitutional
necessity refutation

rather than creating
a synthetic
Version 0.2.

---

# Refutation Outcome

Target

CP-004 Version 0.1 Draft.

Outcome

REFUTED
IN CURRENT FORM.

Constitutional
Implementation Independence

ALREADY GOVERNED
BY RC-001.

Technology Independence

ALREADY GOVERNED
BY RC-001.

Architectural Properties

RETAINED
FOR CLASSIFICATION.

Runtime Properties

RELOCATE.

Artifact Properties

RELOCATE.

Implementation Mechanics

REMOVE
FROM CONSTITUTIONAL
CANDIDATE.

Commercial Properties

REMOVE
FROM CONSTITUTIONAL
CANDIDATE.

Independent
Constitutional Property

NOT IDENTIFIED.

Freeze

PROHIBITED.

Promotion

PROHIBITED.

Next Required Activity

Constitutional
Necessity Test.

---

# End of CP-004 Refutation Cycle 1
