from pathlib import Path


WASM_PATH = Path(
    "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
)


def test_wasm_build_artifact_exists():

    assert WASM_PATH.exists()


def test_wasm_build_artifact_is_not_empty():

    assert WASM_PATH.stat().st_size > 0
