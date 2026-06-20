class ExecutionReport:

    def __init__(
        self,
        requests,
    ):

        self.requests = requests

    def request_count(
        self,
    ) -> int:

        return len(
            self.requests
        )

    def request_ids(
        self,
    ):

        return list(
            self.requests.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "request_count":
                self.request_count(),

            "request_ids":
                self.request_ids(),
        }
