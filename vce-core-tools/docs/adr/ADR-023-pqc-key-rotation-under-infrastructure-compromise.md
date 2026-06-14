# ADR-023: PQC Key Rotation Under Infrastructure Compromise

## Status

Accepted

## Context

Zero-Trust Compute relies on witness signatures to produce consensus evidence.

A witness key compromise must not allow an attacker to forge evidence, rewrite historical decisions, or silently continue participating in quorum.

The system must support emergency key rotation while preserving historical verification and avoiding downtime when quorum can still be satisfied by independent healthy witnesses.

## Decision

The system will support an emergency key rotation protocol for witness signing keys.

The protocol applies to hybrid signing identities, including:

```text
classical signature layer
post-quantum signature layer

## Incident Triggers

Emergency rotation MAY be triggered by:

```text
repeated mTLS verification failures
persistent witness vote divergence
unauthorized IAM policy modification
unauthorized KMS or HSM access events
cloud-provider security alerts
unexpected witness identity changes

## Rotation Pipeline

The emergency rotation protocol has four phases.

1. Quarantine
2. Key Generation
3. Key Registration
4. Atomic Activation

## Security Requirements

A suspended witness must not contribute to quorum.

A compromised key must not be allowed to produce new valid attestations after suspension.

Historical keys must remain available for verification of old attestations.

Historical keys must not be used for new signing.

Key transitions must be transparency-anchored.

Key transitions must be replay-verifiable.

## Store Now, Forge Later Mitigation

An attacker holding one compromised witness key cannot forge valid consensus evidence unless the attacker controls enough independent witnesses to satisfy quorum.

Historical forgery attempts must fail transparency verification.

## Non-Goals

This ADR does not mandate a specific ML-DSA implementation.

This ADR does not mandate a specific cloud KMS implementation.

This ADR does not define organizational incident response procedures.

## Consequences

This introduces operational crypto-agility.

This introduces:

key slots
key validity windows
emergency quorum mutation
registry updates
transparency-bound activation
Future Work

## Future implementation tracks may introduce:

witness suspension records
key rotation records
key validity windows
emergency quorum policy
rotation attestation
browser key-history verification
PQC signing adapters
KMS-backed signing adapters
