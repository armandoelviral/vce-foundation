import hashlib

from epics.epic090_wasmtime_runtime_integration.wasmtime_module_reference import (
    WasmtimeModuleReference,
)


class WasmModuleLoader:

    def load(
        self,
        module_path: str,
    ) -> WasmtimeModuleReference:

        module_hash = hashlib.sha256(
            module_path.encode()
        ).hexdigest()

        return WasmtimeModuleReference(
            module_hash=module_hash,
            module_name=module_path,
        )
