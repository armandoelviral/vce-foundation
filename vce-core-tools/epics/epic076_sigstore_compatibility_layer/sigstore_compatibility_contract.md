# EPIC076 — Sigstore Compatibility Layer

## Goal

Define how Signed Veracity Proofs become compatible with Sigstore-style identity, signing, and transparency workflows.

## Inputs

The compatibility layer accepts:

- Signed Veracity Proof
- canonical signing payload
- artifact_hash
- signing_key_id
- signature
- signature_algorithm

## OIDC Identity Requirements

Future integration must support:

- oidc_issuer
- oidc_subject
- workflow_identity
- runner_identity
- repository_identity

## Fulcio Compatibility Requirements

Future Fulcio compatibility must support:

- ephemeral certificate
- certificate_subject
- certificate_issuer
- certificate_not_before
- certificate_not_after
- public_key_binding

## Rekor Compatibility Requirements

Future Rekor compatibility must support:

- transparency_log_entry
- log_index
- integrated_time
- signed_entry_timestamp
- inclusion_proof

## Sigstore Bundle Fields

A Sigstore-compatible Veracity proof envelope must be able to carry:

- open_vce_payload
- artifact_hash
- signature
- signing_key_id
- signature_algorithm
- oidc_identity
- fulcio_certificate
- rekor_set
- transparency_log_entry

## Non-goals

- live Sigstore network integration
- production certificate issuance
- production key custody
- external Rekor submission

## Transparency Log Requirements

The compatibility layer must support future
Transparency Log integrations.

Required fields:

- transparency_log_entry
- log_index
- integrated_time
- signed_entry_timestamp
- inclusion_proof
