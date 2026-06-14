import wasmtime


def test_end_to_end_real_wasm_execution():

    engine = wasmtime.Engine()

    wat = """
    (module
      (func (export "run") (result i32)
        i32.const 42)
    )
    """

    module = wasmtime.Module(
        engine,
        wat,
    )

    store = wasmtime.Store(
        engine
    )

    instance = wasmtime.Instance(
        store,
        module,
        []
    )

    run = instance.exports(
        store
    )["run"]

    result = run(
        store
    )

    assert result == 42
