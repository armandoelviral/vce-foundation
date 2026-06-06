import subprocess
from pathlib import Path


def test_wasm_executes_with_wasmtime_cli():

    wasm = Path(
        "fuzz-runtime/target/wasm32-unknown-unknown/debug/vce_fuzz_runtime.wasm"
    )

    result = subprocess.run(
        [
            "wasmtime",
            str(wasm),
        ],
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0
