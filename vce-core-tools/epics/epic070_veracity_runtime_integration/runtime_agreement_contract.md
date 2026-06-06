# EPIC070 — Veracity Runtime Integration

## Goal

Integrate the Python replay runtime, Rust replay core, WASM artifact, and Wasmtime execution path into a single verifiable runtime surface.

## Runtime Agreement

For the same event stream:

- Python ReplayEngine must produce a sequence_number.
- Python ReplayEngine must produce a state_hash.
- Rust replay_events must produce an equivalent sequence_number.
- Rust replay_events must produce an equivalent state_hash.
- WASM export execution through Wasmtime must produce deterministic replay evidence.

## Required Agreement Properties

- same input -> same sequence_number
- same input -> same state_hash
- same input -> deterministic output
- invalid WAL input -> safe recovery path
- sandbox execution -> no host-side uncontrolled mutation

## Components

- Python ReplayEngine
- Rust replay_events
- WASM build artifact
- Wasmtime execution
- WALRecovery
- cargo-fuzz campaign evidence

## Non-goals

- distributed consensus
- networking
- production signing keys
- remote attestation
