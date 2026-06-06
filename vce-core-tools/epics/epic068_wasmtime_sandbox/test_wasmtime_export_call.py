from pathlib import Path

import wasmtime


def test_wasmtime_calls_replay_sequence_number_export():

    wasm_path = Path(
        "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
    )

    engine = wasmtime.Engine()
    store = wasmtime.Store(engine)

    module = wasmtime.Module.from_file(
        engine,
        str(wasm_path),
    )

    instance = wasmtime.Instance(
        store,
        module,
        [],
    )

    replay_sequence_number = instance.exports(
        store
    )["replay_sequence_number"]

    result = replay_sequence_number(
        store
    )

    assert result == 3
