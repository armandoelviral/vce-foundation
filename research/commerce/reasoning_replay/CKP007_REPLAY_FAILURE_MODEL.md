# CKP-007

Title

Commerce Replay Failure Model

Abbreviation

CRFM

Version

1.0

Status

Draft

---

## Purpose

Define the canonical,
deterministic,
immutable,
fail-closed,
traceable,
and integrity-preserving
representation of exactly one
Replay Failure associated
with exactly one Replay.

Replay Failure constitutes
the normative record of one
Replay failure.

Replay Failure shall preserve
exactly one Replay.

Replay Failure shall require
exactly one Replay
Attestation.

Replay Failure shall preserve
Replay Validation.

Replay Failure shall preserve
Replay Integrity.

Replay Failure shall preserve
Replay Traceability.

Replay Failure shall preserve
Failure Evidence.

Replay Failure shall preserve
Failure Causality.

Replay Failure shall be
deterministic.

Replay Failure shall remain
immutable.

Replay Failure shall fail
closed.

Replay Failure shall never
modify,
reinterpret,
normalize,
repair,
replace,
merge,
or regenerate
Replay artifacts.

Replay Failure does not define:

Replay reconstruction.

Replay comparison.

Replay divergence.

Replay validation.

Replay certification.

Replay evidence collection.

Replay attestation.

Failure remediation.

Retry behavior.

Operational behavior.

Implementation behavior.

This specification defines
only the normative
representation of Replay
Failure.

---

## Normative Dependencies

This specification depends upon:

HAS Foundation 1.0 LTS.

Specification Runtime 1.0.

CKP-005 Baseline 1.0.

CKP-005 Specification Freeze.

CKP-006 Baseline 1.0.

CKP-006 Specification Freeze.

CKP-007.1 Commerce Reasoning Replay Charter.

CKP-007.2 Replay Structure Model.

CKP-007.3 Replay Request Model.

CKP-007.4 Replay Environment Model.

CKP-007.5 Replay Artifact Resolution Model.

CKP-007.6 Replay Reconstruction Model.

CKP-007.7 Replay State Reconstruction Model.

CKP-007.8 Replay Stage Reconstruction Model.

CKP-007.9 Replay Transition Reconstruction Model.

CKP-007.10 Replay Artifact Registry Reconstruction Model.

CKP-007.11 Replay Runtime Result Reconstruction Model.

CKP-007.12 Replay Comparison Model.

CKP-007.13 Replay Divergence Model.

CKP-007.14 Replay Validation Model.

CKP-007.15 Replay Certification Model.

CKP-007.16 Replay Evidence Model.

CKP-007.17 Replay Attestation Model.

Dependencies shall remain
immutable.

Dependencies shall remain
normative.

Dependencies shall not be
reinterpreted.

Dependencies shall not be
superseded by implementation.

---

## Replay Failure Identity

Every Replay Failure shall
possess exactly one immutable
Replay Failure Identifier.

Replay Failure Identity shall
be globally unique.

Replay Failure Identity shall
never be reused.

Replay Failure Identity shall
remain immutable throughout
its entire lifecycle.

Missing Replay Failure
Identity shall fail
validation.

Malformed Replay Failure
Identity shall fail
validation.

Duplicated Replay Failure
Identity shall fail
validation.

Replay Failure Identity shall
remain fully traceable.

---

## Replay Failure Version

Every Replay Failure shall
declare exactly one Version.

Replay Failure Version
identifies the applicable
Replay Failure schema.

Replay Failure Version shall
remain immutable.

Unsupported Replay Failure
Version shall fail
validation.

---

## Replay Failure Lifecycle

The canonical Replay Failure
Lifecycle is:

Created.

Initialized.

Detected.

Recorded.

Archived.

Lifecycle regression is
prohibited.

Lifecycle transitions shall
remain deterministic.

Terminal lifecycle states
shall remain immutable.

No additional lifecycle
states shall be defined by
this specification.

---

## Replay Failure Scope

One Replay Failure shall
represent exactly one Replay.

One Replay Failure shall
belong to exactly one Replay
Attestation.

Replay Failure Scope shall
remain immutable.

Replay Failure Scope shall
never expand beyond one
Replay.

Replay Failure Scope shall
never merge multiple Replay
instances.

---

## Replay Failure Inputs

Replay Failure shall
consume:

Replay Failure
Identifier.

Replay Failure Version.

Replay Attestation
Reference.

Replay Certification
Reference.

Replay Validation
Reference.

Replay Result
Reference.

Failure Identifier.

Failure Classification.

Failure Status.

Failure Condition.

Failure Source.

Failure Stage.

Failure Causality.

Failure Evidence
Reference.

Failure Integrity
Reference.

Failure Traceability
Reference.

Replay Failure
Integrity Reference.

Every mandatory input shall
be present.

Missing mandatory inputs
shall fail validation.

Unexpected inputs shall not
alter Replay Failure
semantics.

---

## Replay Failure Preconditions

Replay Failure requires:

Validated Replay
Attestation.

Validated Replay
Validation.

Resolved Replay
Result.

Verified Replay
Integrity.

Verified Replay
Traceability.

Every precondition shall
succeed.

Unsatisfied preconditions
shall fail validation.

Replay Failure shall not
exist prior to successful
Replay Attestation.

---

## Replay Attestation Reference

Replay Failure shall
reference exactly one
immutable Replay
Attestation.

Replay Attestation
Reference shall remain
resolvable.

Replay Attestation
Reference shall remain
immutable.

Replay Attestation
Reference shall preserve
attestation traceability.

Missing Replay
Attestation Reference
shall fail validation.

Unresolved Replay
Attestation Reference
shall fail validation.

---

## Failure Identity

Every Failure shall possess
exactly one immutable
Failure Identifier.

Failure Identity shall be
globally unique.

Failure Identity shall
never be reused.

Failure Identity shall
remain immutable throughout
the entire Replay Failure
Lifecycle.

Missing Failure Identifier
shall fail validation.

Malformed Failure
Identifier shall fail
validation.

Duplicated Failure
Identifier shall fail
validation.

Failure Identity shall
remain fully traceable.

---

## Failure Classification

Every Replay Failure shall
declare exactly one
Failure Classification.

Failure Classification
identifies the normative
category of the Replay
Failure.

Failure Classification
shall remain immutable.

Failure Classification
shall remain fully
traceable.

Missing Failure
Classification shall fail
validation.

Unsupported Failure
Classification shall fail
validation.

---

## Failure Status

Every Replay Failure shall
declare exactly one
Failure Status.

The canonical Failure
Status values are:

Open.

Confirmed.

Terminal.

Failure Status shall
remain immutable after
terminal completion.

Unsupported Failure
Status shall fail
validation.

Lifecycle and Failure
Status shall remain
independent normative
concepts.

---

## Failure Condition

Every Replay Failure shall
declare exactly one
Failure Condition.

Failure Condition shall
describe the normative
condition responsible for
the Replay Failure.

Failure Condition shall
remain immutable.

Failure Condition shall
remain completely
traceable.

Missing Failure
Condition shall fail
validation.

---

## Failure Source

Every Replay Failure shall
declare exactly one
Failure Source.

Failure Source identifies
the origin responsible for
the detected Replay
Failure.

Failure Source shall
remain immutable.

Failure Source shall
remain fully traceable.

Missing Failure Source
shall fail validation.

---

## Failure Stage

Every Replay Failure shall
declare exactly one
Failure Stage.

Failure Stage identifies
the Replay Stage where the
Failure occurred.

Failure Stage shall remain
immutable.

Failure Stage shall
preserve historical
ordering.

Missing Failure Stage
shall fail validation.

---

## Failure Causality

Replay Failure shall
declare exactly one
Failure Causality.

Failure Causality shall
identify the causal
relationship explaining
the Replay Failure.

Failure Causality shall
remain immutable.

Failure Causality shall
remain completely
traceable.

Missing Failure
Causality shall fail
validation.

---

## Failure Evidence

Replay Failure shall
reference exactly one
Failure Evidence.

Failure Evidence shall
preserve the historical
evidence supporting the
Replay Failure.

Failure Evidence shall
remain immutable.

Failure Evidence shall
remain completely
traceable.

Missing Failure Evidence
shall fail validation.

Unresolved Failure
Evidence shall fail
validation.

---

## Failure Integrity

Replay Failure shall
possess exactly one
deterministic Failure
Integrity Reference.

Failure Integrity shall
bind:

Failure Identity.

Replay Failure Identity.

Failure Classification.

Failure Status.

Failure Condition.

Failure Source.

Failure Stage.

Failure Causality.

Mutation shall invalidate
Failure Integrity.

Failure Integrity shall
remain immutable.

---

## Failure Traceability

Replay Failure shall
preserve complete
traceability to:

Replay Attestation.

Replay Validation.

Replay Result.

Replay Integrity.

Replay Traceability.

Failure Evidence.

Failure Causality.

Traceability shall remain
complete.

Broken traceability shall
fail validation.

---

## Failure Relationships

Replay Failure belongs to
exactly one Replay.

Replay Failure references
exactly one Replay
Attestation.

Replay Failure references
exactly one Replay
Validation.

Replay Failure references
exactly one Replay
Result.

Replay Failure references
exactly one Failure
Evidence.

Relationships shall
remain explicit.

Relationships shall
remain immutable.

Relationships shall
preserve complete
traceability.

---

## Failure Ordering

Failure Ordering shall be
deterministic.

Equivalent Replay inputs
shall produce equivalent
Failure Ordering.

Implementation-defined
ordering is prohibited.

Failure Ordering shall
remain immutable.

Ordering violations shall
fail validation.

---

## Failure Completeness

Replay Failure shall
preserve all mandatory
Failure information.

Replay Failure shall
preserve all mandatory
references.

Replay Failure shall
preserve all mandatory
traceability.

Partial Replay Failure
shall fail validation.

Missing mandatory
Failure information shall
fail validation.

---

## Failure Consistency

Replay Failure shall
remain consistent with:

Replay Attestation.

Replay Validation.

Replay Result.

Replay Integrity.

Replay Traceability.

Failure Evidence.

Failure Causality.

Failure Classification.

Failure Status.

Consistency violations
shall fail validation.

Replay Failure shall
never reinterpret
preserved Replay
artifacts.

Replay Failure shall
never normalize
preserved information.

Replay Failure shall
never repair preserved
information.

Replay Failure shall
remain deterministic
throughout its entire
lifecycle.

---

## Canonical Serialization

Replay Failure shall
possess exactly one
canonical serialization.

Canonical serialization
shall preserve:

Replay Failure Identity.

Replay Failure Version.

Failure Identity.

Failure Classification.

Failure Status.

Failure Condition.

Failure Source.

Failure Stage.

Failure Causality.

Failure Evidence.

Failure Integrity.

Failure Traceability.

Replay Attestation
Reference.

Replay Validation
Reference.

Replay Result
Reference.

Canonical serialization
shall remain
deterministic.

Canonical serialization
shall remain immutable.

Canonical serialization
shall not suppress
mandatory Failure
information.

Canonical serialization
shall not reorder
normative relationships.

Serialization failures
shall fail validation.

---

## Deterministic Ordering

Replay Failure Ordering
shall be deterministic.

Equivalent Replay inputs
shall produce equivalent
Replay Failure Ordering.

Equivalent Replay
Failures shall produce
identical ordering.

Implementation-defined
ordering is prohibited.

Ordering shall remain
immutable.

Ordering violations
shall fail validation.

---

## Failure Classifications

REPLAY_FAILURE_IDENTITY_VIOLATION.

REPLAY_FAILURE_VERSION_VIOLATION.

REPLAY_FAILURE_LIFECYCLE_VIOLATION.

REPLAY_FAILURE_SCOPE_VIOLATION.

REPLAY_FAILURE_INPUT_VIOLATION.

REPLAY_FAILURE_PRECONDITION_VIOLATION.

REPLAY_FAILURE_REFERENCE_VIOLATION.

FAILURE_IDENTITY_VIOLATION.

FAILURE_CLASSIFICATION_VIOLATION.

FAILURE_STATUS_VIOLATION.

FAILURE_CONDITION_VIOLATION.

FAILURE_SOURCE_VIOLATION.

FAILURE_STAGE_VIOLATION.

FAILURE_CAUSALITY_VIOLATION.

FAILURE_EVIDENCE_VIOLATION.

FAILURE_INTEGRITY_VIOLATION.

FAILURE_TRACEABILITY_VIOLATION.

FAILURE_RELATIONSHIP_VIOLATION.

FAILURE_ORDERING_VIOLATION.

FAILURE_COMPLETENESS_VIOLATION.

FAILURE_CONSISTENCY_VIOLATION.

REPLAY_FAILURE_SERIALIZATION_VIOLATION.

REPLAY_FAILURE_FAILURE.

READ_ONLY_VIOLATION.

---

## Failure Conditions

Validation shall fail
when:

Replay Failure Identity
is invalid.

Replay Failure Version
is unsupported.

Mandatory inputs are
missing.

Mandatory references
cannot be resolved.

Replay Attestation
cannot be resolved.

Replay Validation
cannot be resolved.

Replay Result cannot
be resolved.

Failure Evidence
cannot be resolved.

Failure Integrity
verification fails.

Failure Traceability
verification fails.

Failure Classification
is invalid.

Failure Status is
invalid.

Failure Condition is
missing.

Failure Source is
missing.

Failure Stage is
missing.

Failure Causality is
missing.

Canonical serialization
fails.

Deterministic ordering
fails.

Any mandatory invariant
is violated.

---

## Read-Only Historical Boundary

Replay Failure shall
never modify:

Historical Runtime
Execution.

Historical Runtime
Environment.

Historical Runtime
State.

Historical Runtime
Stage Set.

Historical Runtime
Transition Set.

Historical Artifact
Registry.

Historical Runtime
Result.

Historical Replay
Attestation.

Historical References.

Frozen Baselines.

Replay Failure shall
never modify,
reinterpret,
normalize,
repair,
replace,
merge,
or suppress
historical artifacts.

Replay Failure shall
preserve the original
historical information
exactly as recorded.

---

## Replay Failure Invariants

Exactly one Replay
Failure Identity.

Exactly one Replay.

Exactly one Replay
Attestation.

Exactly one Failure
Classification.

Exactly one Failure
Status.

Exactly one Replay
Failure Integrity
Reference.

Identity Preservation.

Attestation
Preservation.

Failure
Preservation.

Integrity
Preservation.

Traceability
Preservation.

Read-Only
Preservation.

Fail-Closed Failure.

Replay Failure shall
remain immutable
throughout its entire
lifecycle.

---

## Success Criteria

Replay Failure is
successful only when:

Identity is valid.

Version is supported.

Lifecycle is valid.

Scope is valid.

Inputs are complete.

Preconditions are
satisfied.

Replay Attestation
resolves successfully.

Replay Validation
resolves successfully.

Replay Result resolves
successfully.

Failure
Classification is
valid.

Failure Status is
valid.

Failure Condition is
complete.

Failure Source is
consistent.

Failure Stage is
consistent.

Failure Causality is
preserved.

Failure Evidence is
resolved.

Failure Integrity is
verified.

Failure Traceability
is complete.

Canonical
serialization
succeeds.

Deterministic
ordering succeeds.

All invariants are
preserved.

---

## Release Boundary

Version 1.0 defines:

Replay Failure
Identity.

Replay Failure
Version.

Replay Failure
Lifecycle.

Replay Failure
Scope.

Replay Failure
Inputs.

Replay Failure
Preconditions.

Replay Attestation
Reference.

Failure Identity.

Failure
Classification.

Failure Status.

Failure Condition.

Failure Source.

Failure Stage.

Failure Causality.

Failure Evidence.

Failure Integrity.

Failure Traceability.

Failure
Relationships.

Failure Ordering.

Failure
Completeness.

Failure
Consistency.

Canonical
Serialization.

Deterministic
Ordering.

Failure Behavior.

Read-Only Historical
Boundary.

Replay Failure
Invariants.

This specification
does not define:

Replay engine.

Recovery engine.

Retry engine.

Remediation engine.

Persistence.

WAL.

Event sourcing.

Scheduler.

Concurrency.

Distributed
infrastructure.

Cryptographic
algorithms.

PKI.

HSM.

Storage.

Implementation
classes.

Future CKP-007
specifications shall
preserve this Replay
Failure Model.

---

## Next Deliverable

CKP-007.19

Replay Result Model.

Replay Result Model shall
define the canonical,
deterministic,
immutable,
fail-closed,
traceable,
and integrity-preserving
representation of exactly one
Replay Result produced for
exactly one Replay.

Replay Result shall preserve
Replay Failure.

Replay Result shall preserve
Replay Attestation.

Replay Result shall preserve
Replay Evidence.

Replay Result shall preserve
Replay Certification.

Future CKP-007 specifications
shall preserve the normative
semantics established by this
Replay Failure Model.

---

# End of Specification
