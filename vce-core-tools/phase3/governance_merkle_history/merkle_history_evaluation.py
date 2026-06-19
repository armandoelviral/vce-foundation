from phase3.governance_merkle_history.governance_merkle_leaf import (
    GovernanceMerkleLeaf,
)


class MerkleHistoryEvaluation:

    @staticmethod
    def evaluate(
        leaf: GovernanceMerkleLeaf,
    ) -> bool:

        if not leaf.leaf_id:
            return False

        if not leaf.snapshot_id:
            return False

        if not leaf.hash_value:
            return False

        return True
