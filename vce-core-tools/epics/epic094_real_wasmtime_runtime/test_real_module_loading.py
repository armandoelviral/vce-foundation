import wasmtime


def test_can_create_module_from_wat():

    engine = wasmtime.Engine()

    wat = """
    (module
      (func (export "run") (result i32)
        i32.const 42)
    )
    """

    module = wasmtime.Module(engine, wat)

    assert module is not None
