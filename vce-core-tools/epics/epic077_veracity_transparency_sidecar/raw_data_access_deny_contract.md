# EPIC077-D12 — Raw Data Access Deny Contract

## Goal

Ensure the Veracity Transparency Sidecar can generate, anchor, and audit proofs without access to raw sensitive data.

## Core Security Property

The sidecar must prove execution without reading raw sensitive payloads.

## Denied Data Classes

The sidecar must not access:

- raw PHI
- raw PII
- raw biometrics
- raw financial transactions
- raw medical records
- raw inference inputs
- raw customer payloads

## Allowed Data Classes

The sidecar may access only:

- salted HMAC-SHA256 footprints
- artifact hashes
- execution identifiers
- logical metadata
- anchor jobs
- signed proofs
- transparency receipts
- status updates

## Kubernetes Boundary Requirements

The sidecar must not mount:

- application data volumes
- raw payload volumes
- secrets containing customer data
- PHI/PII storage paths

The sidecar may mount:

- veracity pipe volume
- proof queue volume
- receipt output volume

## IAM Boundary Requirements

The sidecar IAM role must not allow:

- reading raw data buckets
- reading customer data secrets
- deleting evidence ledger objects
- bypassing WORM retention
- managing KMS keys

The sidecar IAM role may allow:

- kms:Sign
- kms:Verify
- kms:GetPublicKey
- kms:DescribeKey
- s3:PutObject to evidence ledger
- s3:GetObject from evidence ledger
- s3:ListBucket on evidence ledger

## Required Property

A compromised sidecar must not expose raw PHI, PII, biometrics, medical records, financial payloads, or raw inference inputs.
