from phase4.trusted_compute_unit_identity.tcu_identity_block import (
    TcuIdentityBlock,
)


def test_contains_did():

    block = TcuIdentityBlock(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        ed25519_public_key="ed25519-pub-001",
        mldsa65_public_key="mldsa65-pub-001",
    )

    assert block.did.startswith("did:")


def test_contains_ed25519():

    block = TcuIdentityBlock(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        ed25519_public_key="ed25519-pub-001",
        mldsa65_public_key="mldsa65-pub-001",
    )

    assert block.ed25519_public_key == (
        "ed25519-pub-001"
    )


def test_contains_mldsa():

    block = TcuIdentityBlock(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        ed25519_public_key="ed25519-pub-001",
        mldsa65_public_key="mldsa65-pub-001",
    )

    assert block.mldsa65_public_key == (
        "mldsa65-pub-001"
    )


def test_serializes():

    block = TcuIdentityBlock(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        ed25519_public_key="ed25519-pub-001",
        mldsa65_public_key="mldsa65-pub-001",
    )

    assert block.to_dict() == {
        "did":
            "did:tcn:gcp:us-central1:tcu-node-02",
        "ed25519_public_key":
            "ed25519-pub-001",
        "mldsa65_public_key":
            "mldsa65-pub-001",
    }

