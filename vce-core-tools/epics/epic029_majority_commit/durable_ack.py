class DurableAcknowledgement:

    def filter(
        self,
        results
    ):

        acknowledgements = []

        for result in results:

            if (
                "status" in result
                and
                result["status"].get(
                    "durable"
                ) is True
            ):

                acknowledgements.append(
                    result["peer"]
                )

        return acknowledgements
