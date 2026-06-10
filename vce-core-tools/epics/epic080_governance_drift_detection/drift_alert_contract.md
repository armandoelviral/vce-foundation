# EPIC080-D5 — Drift Alert Contract

## Goal

Define the alert emitted when governance drift is detected between an approved model manifest and a runtime model fingerprint.

## Drift Alert Purpose

A drift alert records that the runtime execution artifact no longer matches an approved governance baseline.

## Required Alert Fields

A drift alert must contain:

- alert_id
- model_id
- model_version
- drift_type
- expected_hash
- observed_hash
- detected_at
- severity
- blocking_required

## Drift Types

The system must support:

- MODEL_HASH_MISMATCH
- WEIGHTS_HASH_MISMATCH
- RUNTIME_IMAGE_HASH_MISMATCH
- UNAPPROVED_MODEL_VERSION
- MISSING_GOVERNANCE_MANIFEST

## Severity Levels

The system must support:

- LOW
- MEDIUM
- HIGH
- CRITICAL

## Required Response

For critical governance drift, the system must:

- emit a drift alert
- block transaction execution
- preserve evidence of the rejected attempt
- avoid anchoring the execution as valid

## Scope Boundary

A drift alert proves governance baseline mismatch.

A drift alert does not prove business, medical, financial, or ethical decision correctness.
