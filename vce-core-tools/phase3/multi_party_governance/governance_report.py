class GovernanceReport:

    def __init__(
        self,
        resolutions,
    ):

        self.resolutions = resolutions

    def resolution_count(
        self,
    ) -> int:

        return len(
            self.resolutions
        )

    def resolution_ids(
        self,
    ):

        return list(
            self.resolutions.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "resolution_count":
                self.resolution_count(),
            "resolution_ids":
                self.resolution_ids(),
        }
