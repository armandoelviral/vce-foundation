from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)


class RootEvaluation:

    @staticmethod
    def evaluate(
        root: GovernanceMerkleRootRecord,
    ) -> bool:

        if not root.root_id:
            return False

        if not root.root_hash:
            return False

        if root.leaf_count <= 0:
            return False

        return True
