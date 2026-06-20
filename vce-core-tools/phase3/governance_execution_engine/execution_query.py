from phase3.governance_execution_engine.execution_request_registry import (
    ExecutionRequestRegistry,
)


class ExecutionQuery:

    def __init__(
        self,
        registry: ExecutionRequestRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        request_id: str,
    ):

        return self.registry.get(
            request_id
        )
