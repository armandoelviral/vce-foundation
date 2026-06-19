class MerkleHistoryReport:

    def __init__(
        self,
        leaves,
    ):

        self.leaves = leaves

    def leaf_count(
        self,
    ) -> int:

        return len(
            self.leaves
        )

    def leaf_ids(
        self,
    ):

        return list(
            self.leaves.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "leaf_count":
                self.leaf_count(),

            "leaf_ids":
                self.leaf_ids(),
        }
