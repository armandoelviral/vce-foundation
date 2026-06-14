def test_wasmtime_dependency_available():

    import wasmtime

    assert wasmtime is not None
