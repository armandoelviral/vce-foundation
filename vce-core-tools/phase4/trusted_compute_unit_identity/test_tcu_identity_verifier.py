from phase4.trusted_compute_unit_identity.tcu_identity_verifier import (
    TcuIdentityVerifier,
)

from phase4.trusted_compute_unit_identity.tcu_identity_record import (
    TcuIdentityRecord,
)

from phase4.trusted_compute_unit_identity.tcu_identity_block import (
    TcuIdentityBlock,
)

from phase4.trusted_compute_unit_identity.tcu_identity_signatures import (
    TcuIdentitySignatures,
)


def test_valid_identity_record():

    record = build_record()

    assert (
        TcuIdentityVerifier.verify(record)
        is True
    )


def test_missing_identity_hash():

    record = build_record()

    record = TcuIdentityRecord(
        identity=record.identity,
        identity_hash="",
        signatures=record.signatures,
    )

    assert (
        TcuIdentityVerifier.verify(record)
        is False
    )


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
