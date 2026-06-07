# EPIC071-D5 — Drift Auditing Flow

## Goal

Define how historical VeracityArtifact records are re-executed and compared against their original evidence to detect drift, tampering, or runtime divergence.

## Audit Inputs

A drift audit requires:

- ledger_sequence
- artifact_id
- original_artifact_hash
- original_state_hash
- original_replay_uri
- original_deterministic_checksum
- original_runtime_version
- original_input_hash
- original_code_hash

## Audit Flow

The drift auditing process consists of:

1. read historical ledger entry
2. recover original VeracityArtifact
3. resolve replay artifact through immutable replay_uri
4. verify replay artifact checksum
5. restore hermetic execution boundary
6. re-run replay execution
7. recompute state hash
8. compare recomputed state hash against original_state_hash
9. emit audit result

## Audit Result

Each drift audit must emit:

- audit_id
- artifact_id
- ledger_sequence
- original_state_hash
- recomputed_state_hash
- drift_detected
- audit_timestamp
- audit_status

## Drift Conditions

Drift must be reported when:

- recomputed_state_hash differs from original_state_hash
- replay artifact checksum does not match original_deterministic_checksum
- replay artifact cannot be resolved
- hermetic execution boundary cannot be restored
- required historical evidence is missing
- runtime version mismatch is not explicitly allowed

## Required Property

If the original artifact, replay artifact, runtime version, and hermetic execution boundary are unchanged, the recomputed state hash must exactly match the original state hash.
