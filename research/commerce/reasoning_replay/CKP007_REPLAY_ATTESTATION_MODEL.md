# CKP-007

Title

Commerce Replay Attestation Model

Abbreviation

CRAM

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
Replay Attestation produced
by exactly one Replay
Certification using exactly
one Replay Evidence.

Replay Attestation constitutes
the normative declaration
resulting from one completed
Replay Certification.

Replay Attestation shall preserve
exactly one Replay.

Replay Attestation shall require
exactly one Replay
Certification.

Replay Attestation shall require
exactly one Replay
Evidence.

Replay Attestation shall preserve
Replay Validation.

Replay Attestation shall preserve
Replay Integrity.

Replay Attestation shall preserve
Replay Traceability.

Replay Attestation shall preserve
Attestation Claims.

Replay Attestation shall be
deterministic.

Replay Attestation shall remain
immutable.

Replay Attestation shall fail
closed.

Replay Attestation shall never
modify,
reinterpret,
normalize,
repair,
replace,
merge,
or regenerate
any Replay artifact.

Replay Attestation does not define:

Replay reconstruction.

Replay comparison.

Replay divergence.

Replay validation.

Replay certification.

Evidence collection.

Attestation issuance
mechanisms.

Cryptographic protocols.

Operational behavior.

Implementation behavior.

This specification defines only
the normative representation of
Replay Attestation.

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

Dependencies shall remain
immutable.

Dependencies shall remain
normative.

Dependencies shall not be
reinterpreted.

Dependencies shall not be
superseded by implementation.

---

## Replay Attestation Identity

Every Replay Attestation shall
possess exactly one immutable
Replay Attestation Identifier.

Replay Attestation Identity
shall be globally unique.

Replay Attestation Identity
shall never be reused.

Replay Attestation Identity
shall remain immutable
throughout its entire
lifecycle.

Missing Replay Attestation
Identity shall fail
validation.

Malformed Replay Attestation
Identity shall fail
validation.

Duplicated Replay Attestation
Identity shall fail
validation.

---

## Replay Attestation Version

Every Replay Attestation shall
declare exactly one Version.

Replay Attestation Version
identifies the applicable
Replay Attestation schema.

Replay Attestation Version
shall remain immutable.

Unsupported Replay
Attestation Version shall
fail validation.

---

## Replay Attestation Lifecycle

The canonical Replay
Attestation Lifecycle is:

Created.

Initialized.

Attesting.

Completed.

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

## Replay Attestation Scope

One Replay Attestation shall
represent exactly one Replay.

One Replay Attestation shall
belong to exactly one Replay
Certification.

One Replay Attestation shall
reference exactly one Replay
Evidence.

Replay Attestation Scope
shall remain immutable.

Replay Attestation Scope
shall never expand beyond
one Replay.

Replay Attestation Scope
shall never merge multiple
Replay instances.

---

## Replay Attestation Inputs

Replay Attestation shall
consume:

Replay Attestation
Identifier.

Replay Attestation Version.

Replay Certification
Reference.

Replay Evidence
Reference.

Replay Validation
Reference.

Replay Result
Reference.

Attestation Identifier.

Attestation Subject.

Attestation Claims.

Attestation Basis.

Attestation Authority.

Attestation Validity.

Attestation Integrity
Reference.

Attestation Traceability
Reference.

Replay Attestation
Integrity Reference.

Every mandatory input shall
be present.

Missing mandatory inputs
shall fail validation.

Unexpected inputs shall not
alter Replay Attestation
semantics.

---

## Replay Attestation Preconditions

Replay Attestation requires:

Validated Replay
Certification.

Validated Replay
Evidence.

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

Replay Attestation shall
not exist prior to
successful Replay
Certification.

---

## Replay Certification Reference

Replay Attestation shall
reference exactly one
immutable Replay
Certification.

Replay Certification
Reference shall remain
resolvable.

Replay Certification
Reference shall remain
immutable.

Replay Certification
Reference shall preserve
certification traceability.

Missing Replay
Certification Reference
shall fail validation.

Unresolved Replay
Certification Reference
shall fail validation.

---

## Replay Evidence Reference

Replay Attestation shall
reference exactly one
immutable Replay
Evidence.

Replay Evidence
Reference shall remain
resolvable.

Replay Evidence
Reference shall remain
immutable.

Replay Evidence
Reference shall preserve
evidence traceability.

Missing Replay
Evidence Reference
shall fail validation.

Unresolved Replay
Evidence Reference
shall fail validation.

---

## Attestation Identity

Every Attestation shall possess
exactly one immutable
Attestation Identifier.

Attestation Identity shall be
globally unique.

Attestation Identity shall
never be reused.

Attestation Identity shall
remain immutable throughout
the entire Replay Attestation
Lifecycle.

Missing Attestation Identifier
shall fail validation.

Malformed Attestation
Identifier shall fail
validation.

Duplicated Attestation
Identifier shall fail
validation.

Attestation Identity shall
remain fully traceable.

---

## Attestation Subject

Every Replay Attestation shall
declare exactly one
Attestation Subject.

Attestation Subject identifies
the Replay that is the subject
of the Attestation.

Attestation Subject shall
remain immutable.

Attestation Subject shall
remain fully traceable.

Missing Attestation Subject
shall fail validation.

---

## Attestation Claims

Every Replay Attestation shall
declare exactly one complete
Attestation Claims set.

Attestation Claims shall
represent the normative
statements supported by the
Replay Certification and
Replay Evidence.

Attestation Claims shall
remain immutable.

Incomplete Attestation Claims
shall fail validation.

Unsupported Attestation
Claims shall fail validation.

---

## Attestation Basis

Replay Attestation shall
declare exactly one
Attestation Basis.

Attestation Basis shall
identify the normative basis
supporting the Attestation.

Attestation Basis shall
reference:

Replay Certification.

Replay Evidence.

Replay Validation.

Replay Result.

Attestation Basis shall
remain immutable.

Missing Attestation Basis
shall fail validation.

---

## Attestation Authority

Every Replay Attestation shall
declare exactly one
Attestation Authority.

Attestation Authority
identifies the normative
authority responsible for the
Attestation.

Attestation Authority shall
remain immutable.

Unknown Attestation Authority
shall fail validation.

This specification defines no
cryptographic authority model.

---

## Attestation Validity

Every Replay Attestation shall
declare exactly one
Attestation Validity.

The canonical validity states
are:

Pending.

Valid.

Invalid.

Attestation Validity shall
remain immutable after
completion.

Unsupported validity states
shall fail validation.

Lifecycle and Validity shall
remain independent normative
concepts.

---

## Attestation Integrity

Replay Attestation shall
possess exactly one
deterministic Attestation
Integrity Reference.

Attestation Integrity shall
bind:

Attestation Identity.

Replay Attestation Identity.

Replay Certification
Reference.

Replay Evidence Reference.

Attestation Subject.

Attestation Claims.

Attestation Basis.

Attestation Validity.

Mutation shall invalidate
Attestation Integrity.

Attestation Integrity shall
remain immutable.

---

## Attestation Traceability

Replay Attestation shall
preserve complete
traceability to:

Replay Certification.

Replay Evidence.

Replay Validation.

Replay Result.

Replay Integrity.

Replay Traceability.

Attestation Basis.

Traceability shall remain
complete.

Broken traceability shall
fail validation.

---

## Attestation Relationships

Replay Attestation belongs to
exactly one Replay.

Replay Attestation references
exactly one Replay
Certification.

Replay Attestation references
exactly one Replay Evidence.

Replay Attestation references
exactly one Replay
Validation.

Replay Attestation references
exactly one Replay Result.

Relationships shall remain
explicit.

Relationships shall remain
immutable.

Relationships shall preserve
complete traceability.

---

## Attestation Ordering

Attestation Ordering shall be
deterministic.

Equivalent Replay inputs
shall produce equivalent
Attestation Ordering.

Implementation-defined
ordering is prohibited.

Attestation Ordering shall
remain immutable.

Ordering violations shall
fail validation.

---

## Attestation Completeness

Replay Attestation shall
preserve all mandatory
Attestation information.

Replay Attestation shall
preserve all mandatory
references.

Replay Attestation shall
preserve all mandatory
traceability.

Partial Replay Attestation
shall fail validation.

Missing mandatory
Attestation information
shall fail validation.

---

## Attestation Consistency

Replay Attestation shall
remain consistent with:

Replay Certification.

Replay Evidence.

Replay Validation.

Replay Result.

Replay Integrity.

Replay Traceability.

Attestation Basis.

Attestation Claims.

Consistency violations shall
fail validation.

Replay Attestation shall
never reinterpret preserved
Replay artifacts.

Replay Attestation shall
never normalize preserved
information.

Replay Attestation shall
never repair preserved
information.

Replay Attestation shall
remain deterministic
throughout its entire
lifecycle.

---

## Canonical Serialization

Replay Attestation shall
possess exactly one canonical
serialization.

Canonical serialization shall
preserve:

Replay Attestation Identity.

Replay Attestation Version.

Attestation Identity.

Attestation Subject.

Attestation Claims.

Attestation Basis.

Attestation Authority.

Attestation Validity.

Attestation Integrity.

Attestation Traceability.

Replay Certification
Reference.

Replay Evidence
Reference.

Canonical serialization shall
remain deterministic.

Canonical serialization shall
remain immutable.

Canonical serialization shall
not suppress mandatory
Attestation information.

Canonical serialization shall
not reorder normative
relationships.

Serialization failures shall
fail validation.

---

## Deterministic Ordering

Replay Attestation Ordering
shall be deterministic.

Equivalent Replay inputs
shall produce equivalent
Replay Attestation Ordering.

Equivalent Replay
Attestations shall produce
identical ordering.

Implementation-defined
ordering is prohibited.

Ordering shall remain
immutable.

Ordering violations shall
fail validation.

---

## Failure Classifications

REPLAY_ATTESTATION_IDENTITY_VIOLATION.

REPLAY_ATTESTATION_VERSION_VIOLATION.

REPLAY_ATTESTATION_LIFECYCLE_VIOLATION.

REPLAY_ATTESTATION_SCOPE_VIOLATION.

REPLAY_ATTESTATION_INPUT_VIOLATION.

REPLAY_ATTESTATION_PRECONDITION_VIOLATION.

REPLAY_ATTESTATION_REFERENCE_VIOLATION.

ATTESTATION_IDENTITY_VIOLATION.

ATTESTATION_SUBJECT_VIOLATION.

ATTESTATION_CLAIMS_VIOLATION.

ATTESTATION_BASIS_VIOLATION.

ATTESTATION_AUTHORITY_VIOLATION.

ATTESTATION_VALIDITY_VIOLATION.

ATTESTATION_INTEGRITY_VIOLATION.

ATTESTATION_TRACEABILITY_VIOLATION.

ATTESTATION_RELATIONSHIP_VIOLATION.

ATTESTATION_ORDERING_VIOLATION.

ATTESTATION_COMPLETENESS_VIOLATION.

ATTESTATION_CONSISTENCY_VIOLATION.

REPLAY_ATTESTATION_SERIALIZATION_VIOLATION.

REPLAY_ATTESTATION_FAILURE.

READ_ONLY_VIOLATION.

---

## Failure Conditions

Validation shall fail when:

Replay Attestation Identity
is invalid.

Replay Attestation Version
is unsupported.

Mandatory inputs are
missing.

Mandatory references cannot
be resolved.

Replay Certification cannot
be resolved.

Replay Evidence cannot be
resolved.

Replay Validation cannot be
resolved.

Replay Result cannot be
resolved.

Attestation Integrity
verification fails.

Attestation Traceability
verification fails.

Attestation Claims are
incomplete.

Attestation Basis is
incomplete.

Canonical serialization
fails.

Deterministic ordering
fails.

Any mandatory invariant is
violated.

---

## Read-Only Historical Boundary

Replay Attestation shall
never modify:

Historical Runtime
Execution.

Historical Runtime
Environment.

Historical Runtime State.

Historical Runtime Stage
Set.

Historical Runtime
Transition Set.

Historical Artifact
Registry.

Historical Runtime Result.

Historical Replay
Certification.

Historical Replay
Evidence.

Historical References.

Frozen Baselines.

Replay Attestation shall
never modify,
reinterpret,
normalize,
repair,
replace,
merge,
or suppress
historical artifacts.

Replay Attestation shall
preserve the original
historical information
exactly as certified.

---

## Replay Attestation Invariants

Exactly one Replay
Attestation Identity.

Exactly one Replay.

Exactly one Replay
Certification.

Exactly one Replay
Evidence.

Exactly one Attestation
Subject.

Exactly one Replay
Attestation Integrity
Reference.

Identity Preservation.

Certification Preservation.

Evidence Preservation.

Attestation Preservation.

Integrity Preservation.

Traceability Preservation.

Read-Only Preservation.

Fail-Closed Attestation.

Replay Attestation shall
remain immutable throughout
its entire lifecycle.

---

## Success Criteria

Replay Attestation is
successful only when:

Identity is valid.

Version is supported.

Lifecycle is valid.

Scope is valid.

Inputs are complete.

Preconditions are
satisfied.

Replay Certification
resolves successfully.

Replay Evidence resolves
successfully.

Replay Validation resolves
successfully.

Replay Result resolves
successfully.

Attestation Claims are
complete.

Attestation Basis is
complete.

Attestation Validity is
consistent.

Attestation Integrity is
verified.

Attestation Traceability is
complete.

Canonical serialization
succeeds.

Deterministic ordering
succeeds.

All invariants are
preserved.

---

## Release Boundary

Version 1.0 defines:

Replay Attestation
Identity.

Replay Attestation
Version.

Replay Attestation
Lifecycle.

Replay Attestation
Scope.

Replay Attestation
Inputs.

Replay Attestation
Preconditions.

Replay Certification
Reference.

Replay Evidence
Reference.

Attestation Identity.

Attestation Subject.

Attestation Claims.

Attestation Basis.

Attestation Authority.

Attestation Validity.

Attestation Integrity.

Attestation Traceability.

Attestation
Relationships.

Attestation Ordering.

Attestation
Completeness.

Attestation
Consistency.

Canonical
Serialization.

Deterministic
Ordering.

Failure Behavior.

Read-Only Historical
Boundary.

Replay Attestation
Invariants.

This specification does
not define:

Replay engine
implementation.

Attestation engine.

PKI.

Digital signatures.

Cryptographic
algorithms.

Certificates.

TPM.

SGX.

TDX.

SEV.

Persistence.

WAL.

Event sourcing.

Scheduler.

Concurrency.

Distributed
infrastructure.

Storage.

Implementation
classes.

Future CKP-007
specifications shall
preserve this Replay
Attestation Model.

---

## Next Deliverable

CKP-007.18

Replay Failure Model.

Replay Failure Model shall
define the canonical,
deterministic,
immutable,
fail-closed,
traceable,
and integrity-preserving
representation of exactly one
Replay Failure associated
with exactly one Replay.

Replay Failure shall preserve
Replay Attestation.

Replay Failure shall preserve
Replay Evidence.

Replay Failure shall preserve
Replay Certification.

Future CKP-007 specifications
shall preserve the normative
semantics established by this
Replay Attestation Model.

---

# End of Specification
