# EPIC071-D3 — Veracity Ingestion Schema

## Goal

Define the canonical evidence artifact accepted by the Veracity Runtime.

## Artifact Structure

The ingestion payload consists of six layers:

1. Identity Layer
2. Trust Layer
3. Provenance Layer
4. Replay Layer
5. Evidence Layer
6. Governance Layer

## Identity Layer

Required fields:

- identity_id
- execution_id
- runtime_id
- actor_type

## Trust Layer

Required fields:

- certificate_id
- trust_provider
- trust_timestamp

## Provenance Layer

Required fields:

- input_hash
- code_hash
- environment_hash
- dependency_hash

## Replay Layer

Required fields:

- replay_uri
- deterministic_checksum
- runtime_version
- sequence_number

## Evidence Layer

Required fields:

- evidence_hash
- evidence_timestamp
- evidence_type

## Governance Layer

Required fields:

- schema_version
- policy_version
- audit_scope

## Canonicalization Requirements

The artifact must be serialized using:

- stable key ordering
- deterministic JSON encoding
- UTF-8 encoding
- reproducible field ordering

## Validation Requirements

Artifacts must pass:

- schema validation
- hash validation
- required field validation
- replay metadata validation

before ledger anchoring is allowed.
