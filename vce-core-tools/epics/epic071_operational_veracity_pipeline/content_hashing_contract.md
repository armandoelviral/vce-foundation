# EPIC071-D2 — Content Hashing Contract

## Goal

Define how every execution-relevant component is converted into immutable, content-addressed evidence.

## Hashing Requirements

Every artifact entering the Veracity Runtime pipeline must have:

- canonical byte representation
- cryptographic hash
- declared hash algorithm
- declared artifact type
- declared artifact source
- declared capture timestamp

## Required Hash Algorithm

The default hash algorithm is:

- SHA-256

Alternative algorithms must be explicitly declared.

## Required Artifact Classes

The pipeline must support hashing for:

- execution input
- compiled code binary
- WASM module
- container image digest
- dependency lockfile
- model weights
- runtime configuration
- output payload

## Canonicalization Requirements

Before hashing, structured data must be canonicalized using:

- stable key ordering
- deterministic serialization
- no host-specific formatting
- no nondeterministic timestamps inside the hashed payload
- explicit encoding policy

## Required Output

Each content hash operation must produce:

- artifact_id
- artifact_type
- hash_algorithm
- content_hash
- canonicalization_policy
- source_uri
- captured_at

## Non-goals

- storing large binary payloads directly in the ledger
- replacing artifact storage systems
- remote attestation
- production key management
