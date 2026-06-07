# EPIC071-D6 — CLI Proof Simulation

## Goal

Define the expected command-line proof output for an operational Veracity Runtime audit.

## CLI Command

Example:

veracity-assess /etc/veracity/fintech_baseline.json

## Expected Output

The CLI must emit a deterministic JSON document containing:

- assessment
- organization
- certification_status
- metrics
- evidence_coverage_ratio_pct
- evidence_debt_index_adimensional
- estimated_evidence_exposure_usd
- drift_detected
- audit_status

## Required Properties

The CLI output must be:

- valid JSON
- deterministic
- machine-readable
- suitable for CI/CD pipelines
- suitable for compliance evidence export

## Non-goals

- production certification issuance
- legal certification
- regulator approval
- cloud-specific integration
