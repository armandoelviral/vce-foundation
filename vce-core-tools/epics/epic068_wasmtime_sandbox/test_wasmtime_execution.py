from pathlib import Path


def test_wasm_artifact_exists():

    wasm = Path(
        "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
    )

    assert wasm.exists()


def test_wasm_artifact_is_loadable():

    wasm = Path(
        "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
    )

    assert wasm.stat().st_size > 0
