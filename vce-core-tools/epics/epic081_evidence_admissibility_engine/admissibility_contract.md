# EPIC081 — Evidence Admissibility Engine

## Goal

Determine whether a cryptographically valid Veracity artifact is admissible before it can be written to the global evidence ledger.

## Core Principle

Cryptographic validity is necessary but not sufficient for evidence admission.

## Admission Rules

The engine must evaluate:

- process is cataloged
- CPS threshold is satisfied
- operational context matches
- governance approval is active

## Required Inputs

- signed_veracity_proof
- process_id
- cps_level
- required_cps_level
- operational_context
- expected_context
- governance_status

## Admission Decisions

The engine must emit:

- ADMIT
- REJECT

## Rejection Reasons

The engine must support:

- PROCESS_NOT_CATALOGED
- CPS_THRESHOLD_NOT_MET
- CONTEXT_MISMATCH
- GOVERNANCE_NOT_ACTIVE

## Required Property

Only admitted evidence may be written to the global evidence ledger.
