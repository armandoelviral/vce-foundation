# EPIC082-D1 Ledger Root Contract

## Goal

Define the cryptographic root exported from the evidence ledger for external anchoring.

## Root Fields

A ledger root must contain:

- root_hash
- sequence_start
- sequence_end
- evidence_count
- region
- generated_at

## Properties

The root must:

- be deterministic
- represent admitted evidence only
- be reproducible
- be independently verifiable

## Non Goals

The root must not contain:

- raw evidence
- PII
- PHI
- business payloads
