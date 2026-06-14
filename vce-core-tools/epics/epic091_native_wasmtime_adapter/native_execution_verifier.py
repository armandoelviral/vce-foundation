from epics.epic091_native_wasmtime_adapter.native_execution_result import (
    NativeExecutionResult,
)


class NativeExecutionVerifier:

    @staticmethod
    def verify(
        first: NativeExecutionResult,
        second: NativeExecutionResult,
    ) -> bool:

        return (
            first.module_hash == second.module_hash
            and first.function_name == second.function_name
            and first.output_payload == second.output_payload
            and first.success == second.success
            and first.trap == second.trap
        )
