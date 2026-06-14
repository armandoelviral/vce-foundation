from epics.epic091_native_wasmtime_adapter.wasm_module_loader import (
    WasmModuleLoader,
)


def test_loader_creates_module_reference():

    loader = WasmModuleLoader()

    module = loader.load(
        "calculator.wasm"
    )

    assert module.module_name == "calculator.wasm"


def test_loader_generates_module_hash():

    loader = WasmModuleLoader()

    module = loader.load(
        "calculator.wasm"
    )

    assert len(module.module_hash) > 0
