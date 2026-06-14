from epics.epic091_native_wasmtime_adapter.export_function_resolver import (
    ExportFunctionResolver,
)


def test_resolver_returns_function_name():

    resolver = ExportFunctionResolver()

    function_name = resolver.resolve(
        "run"
    )

    assert function_name == "run"


def test_resolver_returns_requested_export():

    resolver = ExportFunctionResolver()

    function_name = resolver.resolve(
        "calculate"
    )

    assert function_name == "calculate"
