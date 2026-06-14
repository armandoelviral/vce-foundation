class DeterministicExecutionPolicy:

    def allow(
        self,
        uses_system_time: bool,
        uses_randomness: bool,
    ) -> bool:

        if uses_system_time:
            return False

        if uses_randomness:
            return False

        return True
