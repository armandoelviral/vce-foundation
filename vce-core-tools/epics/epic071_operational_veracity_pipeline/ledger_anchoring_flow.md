# EPIC071-D4 — Ledger Anchoring Flow

## Goal

Define how a validated VeracityArtifact is anchored into the deterministic evidence ledger.

## Anchoring Preconditions

Before anchoring, the artifact must pass:

- schema validation
- required field validation
- content hash validation
- replay metadata validation
- trust metadata validation

## Canonical Serialization

Before commit, the artifact must be serialized using:

- stable key ordering
- deterministic JSON encoding
- UTF-8 encoding
- no nondeterministic host fields
- reproducible byte representation

## Ledger Commit Flow

The anchoring flow consists of:

1. accept validated VeracityArtifact
2. canonicalize artifact payload
3. compute artifact content hash
4. append artifact hash to evidence ledger
5. assign ledger sequence number
6. compute new ledger state hash
7. emit commit receipt

## Commit Receipt

Each successful ledger anchor operation must produce:

- artifact_id
- artifact_hash
- ledger_sequence
- ledger_state_hash
- commit_timestamp
- ledger_backend
- anchoring_status

## Failure Conditions

Anchoring must fail if:

- artifact schema is invalid
- required fields are missing
- content hash mismatch is detected
- replay metadata is invalid
- ledger append fails
- canonical serialization fails

## Required Property

The same artifact payload, serialized under the same canonicalization policy, must produce the same artifact_hash and the same ledger anchoring result.
