import hashlib
from pathlib import Path

import wasmtime

from epics.epic012_replay_runtime.replay_engine import (
    ReplayEngine,
)


CORPUS = Path(
    "epics/epic067_differential_verification/corpus/replay_events.txt"
)

WASM = Path(
    "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
)


def test_end_to_end_runtime_sequence_and_hash_agreement():

    events = CORPUS.read_text().splitlines()

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

    assert wasm_sequence == python_state.sequence_number
    assert wasm_hash_prefix == expected_hash_prefix
