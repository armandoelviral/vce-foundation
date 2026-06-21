from phase4.trusted_compute_unit_identity.tcu_identity_block import (
    TcuIdentityBlock,
)

from phase4.trusted_compute_unit_identity.tcu_identity_hasher import (
    TcuIdentityHasher,
)


def test_generates_identity_hash():

    block = TcuIdentityBlock(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        ed25519_public_key="ed25519-pub-001",
        mldsa65_public_key="mldsa65-pub-001",
    )

    result = TcuIdentityHasher.hash_identity(
        block
    )

    assert isinstance(result, str)
    assert len(result) == 64


def test_same_identity_same_hash():

    block = TcuIdentityBlock(
        did="did:tcn:gcp:us-central1:tcu-node-02",
        ed25519_public_key="ed25519-pub-001",
        mldsa65_public_key="mldsa65-pub-001",
    )

    h1 = TcuIdentityHasher.hash_identity(block)
    h2 = TcuIdentityHasher.hash_identity(block)

    assert h1 == h2
