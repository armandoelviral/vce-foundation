class GovernanceChainVerifier:

    def verify(
        self,
        records,
    ) -> bool:

        if not records:
            return True

        for index in range(
            1,
            len(records),
        ):

            previous = records[
                index - 1
            ]

            current = records[
                index
            ]

            if (
                current["previous_hash"]
                != previous["current_hash"]
            ):
                return False

        return True
