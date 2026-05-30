# MADO103-SPEC Core Systems Glossary
**Author:** Armando Miguel Elvira López (2026)
**Classification:** AD-GD Standard Architectural Domain Lexicon

---

## I. Structural Tuple & Equivalence States

### Execution Tuple (E)
The unified mathematical vector expression defining the comprehensive local state space baseline of an isolated ingestion sandbox node:
$$\mathbf{E} = \langle \mathcal{M}, \mathcal{H}, \mathcal{S}, \mathcal{R} \rangle$$

### Local Memory Space (M)
The hard-isolated, host-bounded 256-byte static byte array allocation window reserved exclusively for sandboxed state mutations under WebAssembly guest control.

### Continuous Rolling WAL Hash (H)
An un-resetting, hash-chained rolling cryptographic identifier computed sequentially via bitwise BLAKE3 hashing to prove continuous chronological event lineage across log rotations without temporal gaps:
$$\mathcal{H}_i = \text{BLAKE3}(\mathcal{H}_{i-1} \parallel \text{Opcode}_i \parallel \text{Payload}_i)$$

### System Manifest (S)
The self-authenticating binary metadata tracking container that anchors structural layout configurations, generation indices, and data snapshot hashes on persistent storage media via trailing BLAKE3 signatures.

### Runtime Resource Metadata (R)
The state tracking vector capturing physical system execution attributes, explicitly encapsulating accrued fuel allocations, active capability token bitmaps, and cumulative byte IO accounting counters.

### Local Observational Equivalence
The strict condition under which two independent execution nodes achieve bitwise identity convergence over the output vector tuple $\mathbf{E}$, verified post-traversal without implying global state synchronization.

---

## II. Forensic Recovery & Ingestion Dynamics

### Primitive Monotonic Validation Loop
The minimal constant-space application-tier validation track that asserts state-transition correctness by enforcing a strict sequential linearity check ($\text{LSN}_{i} > \text{LSN}_{i-1}$) over log lines.

### Log Sequence Number (LSN)
The monotonic scalar index number that marks a unique transaction position inside the write-ahead log channel (`governance.wal`).

### Two-Phase Ingestion Framework
The sequential, host-bounded data-ingestion pipeline architecture split into two discrete, non-overlapping execution perimeters:
* **Phase I (Heuristic Static Verification):** A local text scanning layer that leverages regular expression tokenizers to enforce repository-root directory boundaries before data mutations apply.
* **Phase II (Isolated Execution Sandbox):** The host-bounded WebAssembly runtime workspace that runs capability-gated bytecode transactions within strict fuel and memory ceilings.

### Cryptographic Validation Failure
A fatal, terminal system exception raised by the primitive validation loop whenever an incoming transaction frame violates sequence number monotonicity, exposes a broken rolling hash chain, or presents a mismatched manifest signature.

---

## III. Security Hardening & Deployment Boundaries

### Capability Token Bitmask
A rigid, low-level bit flag authority matrix (`CAP_REPLAY_READ`, `CAP_WAL_APPEND`, `CAP_SNAPSHOT_CREATE`) that forces the deployment pipeline and execution threads to operate within a hard, un-escalatable permission perimeter.

### Execution Budget
The rigid configuration parameters that set the absolute physical resource limits for sandboxed guest execution, hard-capping transaction processing at 25,000 fuel units and 512 Kilobytes of static RAM allocation.

### POSIX Sandbox Hardening
The deployment-tier operational configuration enforced by host container orchestrators to restrict process environments via read-only root filesystems (`read-only: true`), memory-allocated volatile spaces (`tmpfs`), and total Linux kernel privilege dropping (`CAP_DROP_ALL`).

### External Execution Oracle
Any host-dependent operational asset operating outside the machine-verifiable bounds of the local specification (including the native Wasmtime VM engine, Cranelift optimization backends, host memory allocators, and hardware disk controllers).
