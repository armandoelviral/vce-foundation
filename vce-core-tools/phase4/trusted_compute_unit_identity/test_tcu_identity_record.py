from phase4.trusted_compute_unit_identity.tcu_identity_record import (
    TcuIdentityRecord,
)

from phase4.trusted_compute_unit_identity.tcu_identity_block import (
    TcuIdentityBlock,
)

from phase4.trusted_compute_unit_identity.tcu_identity_signatures import (
    TcuIdentitySignatures,
)


def test_contains_identity():

    record = build_record()

    assert record.identity.did.startswith("did:")


def test_contains_identity_hash():

    record = build_record()

    assert record.identity_hash == "identity-hash-001"


def test_contains_signatures():

    record = build_record()

    assert (
        record.signatures.ed25519_signature
        == "ed25519-sig-001"
    )


def test_serializes():

    record = build_record()

    data = record.to_dict()

    assert "identity" in data
    assert "identity_hash" in data
    assert "signatures" in data


def build_record():

    return TcuIdentityRecord(
        identity=TcuIdentityBlock(
            did="did:tcn:gcp:us-central1:tcu-node-02",
            ed25519_public_key="ed25519-pub-001",
            mldsa65_public_key="mldsa65-pub-001",
        ),
        identity_hash="identity-hash-001",
        signatures=TcuIdentitySignatures(
            ed25519_signature="ed25519-sig-001",
            mldsa65_signature="mldsa65-sig-001",
        ),
    )
