from epics.epic091_native_wasmtime_adapter.wasmtime_engine_wrapper import (
    WasmtimeEngineWrapper,
)


def test_engine_wrapper_builds_engine():

    wrapper = WasmtimeEngineWrapper()

    engine = wrapper.create_engine()

    assert engine is not None


def test_engine_wrapper_returns_same_type():

    wrapper = WasmtimeEngineWrapper()

    engine_a = wrapper.create_engine()
    engine_b = wrapper.create_engine()

    assert type(engine_a) is type(engine_b)
