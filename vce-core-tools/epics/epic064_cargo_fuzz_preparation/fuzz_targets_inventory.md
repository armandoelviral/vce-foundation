# EPIC064 — cargo-fuzz Preparation

## Fuzz Target Inventory

### 1. Replay Engine

Input:

- Arbitrary event streams
- Empty events
- Long events
- Unicode payloads
- Repeated events

Invariant:

- Replay must not crash
- Same input must produce same state hash
- Sequence number must equal event count

---

### 2. LSN Validator

Input:

- Arbitrary LSN sequences
- Gaps
- Duplicates
- Negative numbers
- Non-integer values

Invariant:

- Contiguous positive sequence is valid
- Gaps are invalid
- Duplicates are invalid
- Non-integer LSN values are invalid

---

### 3. WAL Recovery

Input:

- Truncated records
- Corrupted records
- Empty records
- Partial WAL tails
- Mixed valid and invalid records

Invariant:

- Recovery must stop at first corrupt record
- Recovered prefix must contain only valid records
- Recovery must never include corrupt tail

---

### 4. Hash Chain

Input:

- Arbitrary strings
- Empty strings
- Repeated records
- Large records
- Unicode records

Invariant:

- Every append must produce a hash
- Hash length must remain stable
- Chain verification must reject tampering

---

### 5. Opcode Dispatch

Input:

- Unknown opcodes
- Empty opcode names
- Invalid payloads
- Valid opcode sequences
- Reordered opcode sequences

Invariant:

- Unknown opcodes must be rejected
- Valid opcodes must update state deterministically
- Invalid transition must fail safely
