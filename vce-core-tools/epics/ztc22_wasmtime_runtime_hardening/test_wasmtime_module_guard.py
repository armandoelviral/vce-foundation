from epics.ztc22_wasmtime_runtime_hardening.wasmtime_module_guard import (
    WasmtimeModuleGuard,
)


def test_accepts_valid_module_metadata():

    assert WasmtimeModuleGuard.allow(
        module_name="policy.wasm",
        module_hash="hash-001",
    )


def test_rejects_missing_module_name():

    assert not WasmtimeModuleGuard.allow(
        module_name="",
        module_hash="hash-001",
    )


def test_rejects_missing_module_hash():

    assert not WasmtimeModuleGuard.allow(
        module_name="policy.wasm",
        module_hash="",
    )
