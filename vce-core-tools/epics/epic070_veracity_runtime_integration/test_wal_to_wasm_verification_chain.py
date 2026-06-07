from pathlib import Path

import wasmtime

from epics.epic012_replay_runtime.replay_engine import (
    ReplayEngine,
)
from epics.epic063_wal_recovery.wal_recovery import (
    WALRecovery,
)


WASM = Path(
    "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
)


def test_wal_recovery_replay_and_wasm_agreement():

    wal_lines = [
        "1|APPEND_EVIDENCE|APPEND_EVIDENCE",
        "2|REGISTER_ARTIFACT|REGISTER_ARTIFACT",
        "3|SEAL_SNAPSHOT|SEAL_SNAPSHOT",
        "INVALID|APPEND_EVIDENCE|corrupt-tail",
    ]

    recovered = WALRecovery().recover_after_crash(
        wal_lines
    )

    events = [
        line.split("|")[2]
        for line in recovered
    ]

    python_state = ReplayEngine().replay(
        events
    )

    expected_hash_prefix = int(
        python_state.state_hash[:8],
        16,
    )

    engine = wasmtime.Engine()
    store = wasmtime.Store(engine)

    module = wasmtime.Module.from_file(
        engine,
        str(WASM),
    )

    instance = wasmtime.Instance(
        store,
        module,
        [],
    )

    exports = instance.exports(
        store
    )

    wasm_sequence = exports["replay_sequence_number"](
        store
    )

    wasm_hash_prefix = (
        exports["replay_hash_prefix"](
            store
        )
        & 0xFFFFFFFF
    )

    assert recovered == [
        "1|APPEND_EVIDENCE|APPEND_EVIDENCE",
        "2|REGISTER_ARTIFACT|REGISTER_ARTIFACT",
        "3|SEAL_SNAPSHOT|SEAL_SNAPSHOT",
    ]

    assert wasm_sequence == python_state.sequence_number
    assert wasm_hash_prefix == expected_hash_prefix
