import wasmtime


class WasmtimeEngineWrapper:

    def create_engine(self):

        return wasmtime.Engine()
