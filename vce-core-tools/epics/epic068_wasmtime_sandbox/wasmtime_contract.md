# EPIC068 Wasmtime Sandbox

Goal:

Execute Replay Runtime logic inside a deterministic WebAssembly sandbox.

Technology:

- Rust
- WebAssembly
- Wasmtime

Required Properties:

- deterministic execution
- isolated runtime
- replayable execution
- sandboxed memory model

Non-goals:

- distributed execution
- networking
- persistent storage
