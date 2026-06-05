class MajorityAcknowledgement:

    def evaluate(
        self,
        acknowledgements,
        total_nodes
    ):

        required = (
            total_nodes // 2
        ) + 1

        received = len(
            acknowledgements
        )

        return {
            "required": required,
            "received": received,
            "commit": received >= required
        }
