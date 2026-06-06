from pathlib import Path


def test_wasm_runtime_contract_exists():

    assert Path(
        "epics/epic068_wasmtime_sandbox/wasmtime_contract.md"
    ).exists()


def test_contract_mentions_wasmtime():

    content = Path(
        "epics/epic068_wasmtime_sandbox/wasmtime_contract.md"
    ).read_text()

    assert "Wasmtime" in content
    assert "WebAssembly" in content
    assert "deterministic execution" in content
