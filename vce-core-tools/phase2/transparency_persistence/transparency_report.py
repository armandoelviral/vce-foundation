class TransparencyReport:

    def __init__(
        self,
        roots,
    ):

        self.roots = roots

    def total_roots(
        self,
    ) -> int:

        return len(
            self.roots
        )

    def root_hashes(
        self,
    ):

        return [
            root.root_hash
            for root in self.roots
        ]

    def to_dict(
        self,
    ):

        return {
            "total_roots":
                self.total_roots(),
            "root_hashes":
                self.root_hashes(),
        }
