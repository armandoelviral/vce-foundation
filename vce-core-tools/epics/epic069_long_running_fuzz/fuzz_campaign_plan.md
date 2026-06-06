# EPIC069 — Fuzz Campaign Plan

## Campaign 1 — Replay

Target:

- fuzz_target_1

Initial Runs:

- 100000

Command:

cargo fuzz run fuzz_target_1 -- -runs=100000

Expected Result:

- no crash
- no panic
- no abort
- no out-of-memory failure

Corpus:

- fuzz-runtime/fuzz/corpus/fuzz_target_1

Artifacts:

- fuzz-runtime/fuzz/artifacts/fuzz_target_1

---

## Campaign 2 — Hash Chain

Target:

- hash_chain_fuzz_target

Initial Runs:

- 100000

Expected Result:

- no crash
- no panic
- no abort
- no out-of-memory failure

Corpus:

- fuzz-runtime/fuzz/corpus/hash_chain_fuzz_target

Artifacts:

- fuzz-runtime/fuzz/artifacts/hash_chain_fuzz_target

---

## Campaign 3 — WAL Recovery

Target:

- wal_recovery_fuzz_target

Initial Runs:

- 100000

Expected Result:

- no crash
- no panic
- no abort
- no out-of-memory failure

Corpus:

- fuzz-runtime/fuzz/corpus/wal_recovery_fuzz_target

Artifacts:

- fuzz-runtime/fuzz/artifacts/wal_recovery_fuzz_target
