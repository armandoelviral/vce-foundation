import wasmtime


def test_engine_supports_fuel_configuration():

    config = wasmtime.Config()

    config.consume_fuel = True

    engine = wasmtime.Engine(config)

    assert engine is not None
