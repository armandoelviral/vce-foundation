# EPIC074 — Veracity CLI

## Goal

Expose the Veracity SDK through a minimal command-line interface.

## Commands

The CLI must support:

- veracity prove
- veracity verify
- veracity audit

## prove

Purpose:

Create a Veracity proof from an artifact payload.

Expected output:

- artifact_hash
- ledger_sequence
- verified

## verify

Purpose:

Verify a proof against its anchored receipt.

Expected output:

- verified
- artifact_hash
- ledger_sequence

## audit

Purpose:

Replay-audit an existing proof.

Expected output:

- audit_status
- verified
- artifact_hash
- ledger_sequence

## Required Properties

CLI output must be:

- valid JSON
- deterministic
- machine-readable
- CI/CD friendly
