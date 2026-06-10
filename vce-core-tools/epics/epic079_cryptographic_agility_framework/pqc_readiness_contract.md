# EPIC079-D5 — PQC Readiness Contract

## Goal

Ensure Veracity proofs can migrate toward post-quantum cryptographic primitives without invalidating historical evidence.

## Core Requirement

Veracity must not hardcode trust into:

- a single signature algorithm
- a single hash algorithm
- a single certificate authority
- a single transparency ledger

## Required Design Properties

The cryptographic agility layer must support:

- explicit signature_algorithm identifiers
- explicit hash_algorithm identifiers
- explicit cryptographic_epoch identifiers
- registry-based verification dispatch
- multi-signature transition proofs
- legacy proof preservation
- future PQC algorithm registration

## PQC Candidate Families

The system must be able to model future post-quantum signature families such as:

- ML-DSA
- SLH-DSA
- future NIST-approved algorithms

## Migration Requirements

During migration windows, Veracity must support:

- legacy signatures
- post-quantum signatures
- dual-signed proofs
- epoch-aware verification
- algorithm deprecation metadata
- migration audit reporting

## Non-goals

- production PQC implementation
- live PQC certificate issuance
- replacing existing trust infrastructure immediately
- claiming quantum resistance before approved integration
