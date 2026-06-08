# EPIC075 — Signed Veracity Proofs

## Goal

Transform a Veracity proof into a signed, portable, independently verifiable evidence envelope.

## Architecture

ENGINE RUNTIME
  -> EPIC075 ORCHESTRATION
  -> SIGNED VERACITY PROOF

## Engine Runtime Responsibilities

- create VeracityArtifact
- compute artifact hash
- anchor artifact
- emit receipt
- verify proof

## Orchestration Responsibilities

- isolate signed envelope from runtime internals
- canonicalize proof payload
- sign canonical payload
- attach signing metadata
- prepare Sigstore integration
- prepare Rekor SET inclusion

## Signed Veracity Proof Requirements

A signed proof must contain:

- open_vce_payload
- artifact_hash
- ledger_sequence
- verified
- signature
- signing_key_id
- signature_algorithm
- signing_timestamp
- rekor_set

## Envelope Isolation

The signed envelope must not mutate the original VeracityArtifact.

The signed envelope must be independently serializable.

The signed envelope must be independently verifiable.

## Sigstore Integration

Future Sigstore integration must support:

- Fulcio identity certificate
- Rekor transparency log entry
- Signed Entry Timestamp
- certificate identity binding

## Non-goals

- production key custody
- cloud KMS integration
- legal certification
- live Rekor network dependency
