from phase3.governance_execution_engine.execution_request_record import (
    ExecutionRequestRecord,
)


class ExecutionRequestRegistry:

    def __init__(self):

        self._requests = {}

    def add(
        self,
        request: ExecutionRequestRecord,
    ) -> None:

        self._requests[
            request.request_id
        ] = request

    def get(
        self,
        request_id: str,
    ):

        return self._requests.get(
            request_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._requests
        )

    def request_ids(
        self,
    ):

        return list(
            self._requests.keys()
        )
