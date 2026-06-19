class RootReport:

    def __init__(
        self,
        roots,
    ):

        self.roots = roots

    def root_count(
        self,
    ) -> int:

        return len(
            self.roots
        )

    def root_ids(
        self,
    ):

        return list(
            self.roots.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "root_count":
                self.root_count(),

            "root_ids":
                self.root_ids(),
        }
