class GovernanceQuery:

    def __init__(
        self,
        resolutions,
    ):

        self.resolutions = resolutions

    def by_id(
        self,
        resolution_id: str,
    ):

        return self.resolutions.get(
            resolution_id
        )
