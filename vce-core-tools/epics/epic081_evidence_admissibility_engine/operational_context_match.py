class OperationalContextMatch:

    def matches(
        self,
        expected_context,
        runtime_context,
    ):

        return expected_context == runtime_context
