import hashlib
import json

from epics.epic090_wasmtime_runtime_integration.wasmtime_runtime_contract import (
    WasmtimeExecutionResult,
)


class ExecutionHash:

    @staticmethod
    def compute(
        result: WasmtimeExecutionResult,
    ) -> str:

        payload = json.dumps(
            {
                "module_hash": result.module_hash,
                "function_name": result.function_name,
                "output_payload": result.output_payload,
                "success": result.success,
            },
            sort_keys=True,
        )

        return hashlib.sha256(
            payload.encode()
        ).hexdigest()
