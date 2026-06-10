# Veracity Principles

## VERACITY PRINCIPLE #1

### Proof Without Disclosure

The system may prove execution without possessing or disclosing the data that produced the execution.

Raw sensitive data remains inside the trust boundary.

Only deterministic cryptographic evidence leaves the trust boundary.

The sidecar can prove execution, but cannot read the data that produced the execution.

---

## VERACITY PRINCIPLE #2

### Evidence Must Outlive Cryptography

Evidence must outlive the cryptography used to create it.

Cryptographic algorithms evolve.

Hash functions evolve.

Certificate authorities evolve.

Transparency infrastructures evolve.

Trust systems evolve.

Evidence must remain verifiable across those changes.

Veracity therefore treats cryptographic algorithms as replaceable implementation details rather than permanent trust anchors.

Historical evidence must remain replayable, auditable, and verifiable after migration to future cryptographic primitives.

The lifetime of evidence must exceed the lifetime of any specific:

* signature algorithm
* hash function
* certificate authority
* transparency ledger
* trust infrastructure

Veracity preserves cryptographic context through explicit epoch metadata, algorithm metadata, and verification metadata.

A proof signed in one cryptographic era must remain independently verifiable in future eras.

The objective is not to preserve a particular algorithm.

The objective is to preserve trust in the evidence.

