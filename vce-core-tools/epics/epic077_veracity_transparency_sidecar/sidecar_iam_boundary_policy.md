# EPIC077-D13 — Sidecar IAM Boundary Policy

## Goal

Enforce least-privilege access boundaries for the Veracity Transparency Sidecar.

## Core Principle

The sidecar must possess only the permissions required to:

- sign proofs
- verify proofs
- write evidence
- read evidence
- perform transparency operations

The sidecar must not possess permissions required to:

- access raw customer data
- access PHI
- access PII
- access biometrics
- access medical records
- access application databases
- access application secrets

## Allowed AWS KMS Actions

- kms:Sign
- kms:Verify
- kms:GetPublicKey
- kms:DescribeKey

## Denied AWS KMS Actions

- kms:CreateKey
- kms:ScheduleKeyDeletion
- kms:PutKeyPolicy
- kms:DisableKey
- kms:RotateKeyOnDemand

## Allowed S3 Actions

- s3:PutObject
- s3:GetObject
- s3:ListBucket

## Denied S3 Actions

- s3:DeleteObject
- s3:DeleteObjectVersion
- s3:BypassGovernanceRetention

## Kubernetes Requirements

The sidecar must run under a dedicated ServiceAccount.

The sidecar ServiceAccount must not be shared with:

- application containers
- database workloads
- customer-facing services

## Pod Identity Requirements

The sidecar IAM role must be assumable only by:

- pods.eks.amazonaws.com
- approved namespace
- approved service account

## Required Security Property

Compromise of the sidecar must not grant access to raw customer data.
