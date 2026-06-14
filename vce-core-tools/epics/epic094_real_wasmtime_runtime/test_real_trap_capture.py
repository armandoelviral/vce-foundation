import wasmtime


def test_captures_wasmtime_trap():

    engine = wasmtime.Engine()

    wat = """
    (module
      (func (export "run")
        unreachable)
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

    trap = None

    try:
        run(store)
    except wasmtime.Trap as error:
        trap = str(error)

    assert trap is not None
    assert "unreachable" in trap.lower()
