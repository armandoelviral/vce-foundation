class VersionChangeEvaluation:

    @staticmethod
    def evaluate(
        current_version: str,
        proposed_version: str,
    ) -> bool:

        current = int(
            current_version.replace(
                "v",
                "",
            )
        )

        proposed = int(
            proposed_version.replace(
                "v",
                "",
            )
        )

        return proposed > current
