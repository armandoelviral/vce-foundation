# EPIC077 — Veracity Transparency Sidecar

## Goal

Provide an asynchronous transparency anchoring sidecar that keeps external trust infrastructure outside the critical runtime hot path.

## Architecture

App Container
  -> Veracity SDK
  -> Local Signed Proof
  -> Local Evidence Ledger
  -> Fast Response

Veracity Transparency Sidecar
  -> Reads pending proofs
  -> Creates anchor jobs
  -> Submits to transparency backend
  -> Stores transparency receipt
  -> Updates anchor status

## Responsibilities

The sidecar is responsible for:

- asynchronous transparency anchoring
- retry handling
- backoff handling
- external transparency submission
- Rekor-compatible anchoring
- private transparency log anchoring
- SET receipt handling
- anchor status updates
- Prometheus metrics emission

## Non-Responsibilities

The sidecar must not:

- execute business logic
- block application responses
- mutate original VeracityArtifact payloads
- become required for local proof creation
- become required for local verification

## Required Status Model

The sidecar must support:

- LOCAL_COMMITTED
- PENDING_TRANSPARENCY
- ANCHORING
- TRANSPARENCY_ANCHORED
- RETRYING
- FAILED

## Required Runtime Property

External transparency anchoring must be asynchronous, retryable, idempotent, and outside the critical execution path.
