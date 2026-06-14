from epics.epic090_wasmtime_runtime_integration.wasmtime_module_reference import (
    WasmtimeModuleReference,
)


def test_module_reference_contains_identity():
    module = WasmtimeModuleReference(
        module_hash="wasm-123",
        module_name="calculator.wasm",
    )

    assert module.module_hash == "wasm-123"
    assert module.module_name == "calculator.wasm"


def test_module_reference_serializes():
    module = WasmtimeModuleReference(
        module_hash="wasm-123",
        module_name="calculator.wasm",
    )

    assert module.to_dict() == {
        "module_hash": "wasm-123",
        "module_name": "calculator.wasm",
    }
