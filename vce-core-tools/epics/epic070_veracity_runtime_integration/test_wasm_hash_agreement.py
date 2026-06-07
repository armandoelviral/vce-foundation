import hashlib
from pathlib import Path

import wasmtime


CORPUS = Path(
    "epics/epic067_differential_verification/corpus/replay_events.txt"
)

WASM = Path(
    "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
)


def test_wasm_hash_prefix_matches_python_hash_prefix():

    events = CORPUS.read_text().splitlines()

    payload = "|".join(events)

    python_hash = hashlib.sha256(
        payload.encode()
    ).hexdigest()

    expected_prefix = int(
        python_hash[:8],
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

    replay_hash_prefix = instance.exports(
        store
    )["replay_hash_prefix"]

    wasm_prefix = replay_hash_prefix(
        store
    ) & 0xFFFFFFFF

    assert wasm_prefix == expected_prefix
