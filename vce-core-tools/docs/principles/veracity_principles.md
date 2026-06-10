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

---

## VERACITY PRINCIPLE #3

### Execution Integrity Is Not Decision Validity

A verifiable execution does not imply a correct decision.

Veracity proves execution integrity.

Veracity does not certify decision correctness.

A Signed Veracity Proof demonstrates that a specific input footprint passed through a specific runtime, model, container, and execution path to produce a specific output footprint at a specific time.

It does not prove that the input was true, complete, lawful, unbiased, clinically valid, financially justified, or ethically correct.

Veracity may prove that a decision was executed exactly as specified.

Veracity does not prove that the decision should have been made.

Application data quality, model training quality, policy compliance, medical correctness, financial fairness, and business-rule validity remain responsibilities of the application governance layer.

A perfectly verified execution can still produce a wrong, harmful, illegal, or biased result if the input data, model, or business policy is defective.
