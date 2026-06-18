from phase2.transparency_persistence.merkle_root_record import (
    MerkleRootRecord,
)

from phase2.transparency_persistence.transparency_verifier import (
    TransparencyVerifier,
)


def test_verifier_accepts_matching_root():

    root = MerkleRootRecord(
        root_hash="root-001",
        entry_count=5,
    )

    assert (
        TransparencyVerifier.verify(
            root,
            expected_root="root-001",
        )
        is True
    )


def test_verifier_rejects_mismatch():

    root = MerkleRootRecord(
        root_hash="root-001",
        entry_count=5,
    )

    assert (
        TransparencyVerifier.verify(
            root,
            expected_root="root-999",
        )
        is False
    )


def test_verifier_rejects_empty_root():

    root = MerkleRootRecord(
        root_hash="",
        entry_count=5,
    )

    assert (
        TransparencyVerifier.verify(
            root,
            expected_root="",
        )
        is False
    )
