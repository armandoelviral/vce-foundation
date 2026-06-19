class PolicyVersionReport:

    def __init__(
        self,
        versions,
    ):

        self.versions = versions

    def version_count(
        self,
    ) -> int:

        return len(
            self.versions
        )

    def version_ids(
        self,
    ):

        return list(
            self.versions.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "version_count":
                self.version_count(),

            "version_ids":
                self.version_ids(),
        }
