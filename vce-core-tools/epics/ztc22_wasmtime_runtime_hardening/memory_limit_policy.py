class MemoryLimitPolicy:

    def __init__(
        self,
        max_memory_bytes: int,
    ):

        self.max_memory_bytes = max_memory_bytes

    def allow(
        self,
        requested_memory_bytes: int,
    ) -> bool:

        return (
            requested_memory_bytes
            <= self.max_memory_bytes
        )
