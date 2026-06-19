from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)


class GovernanceMerkleRegistry:

    def __init__(self):

        self._leaves = {}

    def add(
        self,
        leaf: GovernanceMerkleLeaf,
    ) -> None:

        self._leaves[
            leaf.leaf_id
        ] = leaf

    def get(
        self,
        leaf_id: str,
    ):

        return self._leaves.get(
            leaf_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._leaves
        )

    def leaf_ids(
        self,
    ):

        return list(
            self._leaves.keys()
        )
