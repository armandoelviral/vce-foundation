# EPIC069 — Long Running Fuzz Campaign

## Goal

Run sustained fuzzing campaigns against runtime-critical components.

## Required Targets

### Replay Target

Purpose:

- Exercise replay input handling.
- Validate no panic, abort, or uncontrolled crash occurs.

### Hash Chain Target

Purpose:

- Exercise arbitrary record hashing.
- Validate stable hash generation under adversarial input.

### WAL Recovery Target

Purpose:

- Exercise corrupted, truncated, and arbitrary WAL records.
- Validate recovery stops safely at the first invalid record.

## Campaign Requirements

Each campaign must define:

- target name
- run count
- expected result
- corpus location
- crash artifact location

## Success Criteria

A campaign is considered successful when:

- cargo-fuzz completes the configured run count
- no crash artifact is produced
- no panic occurs
- no out-of-memory failure occurs
- corpus remains usable for future runs
