# EPIC067 — Differential Verification Contract

## Goal

Validate that the Python replay runtime and the Rust replay core produce equivalent state for the same event stream.

## Implementations

### Python ReplayEngine

Input:

- list[str]

Output:

- sequence_number
- state_hash

### Rust replay_events

Input:

- &[&str]

Output:

- sequence_number
- state_hash

## Required Invariants

For the same event stream:

- Python sequence_number == Rust sequence_number
- Python state_hash == Rust state_hash
- Same input always produces same output
- Different ordered input should produce different state_hash when order changes

## Non-goals

- No FFI bridge yet
- No Wasmtime yet
- No production runtime integration yet
