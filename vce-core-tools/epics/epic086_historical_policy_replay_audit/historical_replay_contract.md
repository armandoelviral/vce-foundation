# EPIC086-D1 Historical Replay Contract

## Goal

Reconstruct historical evidence decisions using the exact policy version that governed the original execution.

## Core Principle

History must be replayed using the policy that governed history.

## Required Inputs

- evidence_hash
- policy_id
- policy_version
- execution_attributes
- original_decision

## Required Outputs

- REPLAY_MATCH
- REPLAY_MISMATCH

## Required Properties

Replay must be:

- deterministic
- version-pinned
- independently verifiable
- auditable

## Replay Rule

The replay engine must resolve the original policy version before replay begins.

## Non Goals

Replay does not reinterpret history.

Replay reconstructs history.
