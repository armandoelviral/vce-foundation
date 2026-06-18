from phase2.transparency_persistence.merkle_root_record import (
    MerkleRootRecord,
)


class TransparencyVerifier:

    @staticmethod
    def verify(
        root: MerkleRootRecord,
        expected_root: str,
    ) -> bool:

        if not root.root_hash:
            return False

        return (
            root.root_hash
            == expected_root
        )
