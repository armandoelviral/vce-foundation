from phase3.governance_merkle_root.governance_merkle_root_record import (
    GovernanceMerkleRootRecord,
)


class GovernanceRootRegistry:

    def __init__(self):

        self._roots = {}

    def add(
        self,
        root: GovernanceMerkleRootRecord,
    ) -> None:

        self._roots[
            root.root_id
        ] = root

    def get(
        self,
        root_id: str,
    ):

        return self._roots.get(
            root_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._roots
        )

    def root_ids(
        self,
    ):

        return list(
            self._roots.keys()
        )
