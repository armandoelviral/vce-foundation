from phase4.trusted_compute_unit_identity.tcu_identity_signatures import (
    TcuIdentitySignatures,
)


def test_contains_ed25519_signature():

    signatures = TcuIdentitySignatures(
        ed25519_signature="ed25519-sig-001",
        mldsa65_signature="mldsa65-sig-001",
    )

    assert signatures.ed25519_signature == (
        "ed25519-sig-001"
    )


def test_contains_mldsa_signature():

    signatures = TcuIdentitySignatures(
        ed25519_signature="ed25519-sig-001",
        mldsa65_signature="mldsa65-sig-001",
    )

    assert signatures.mldsa65_signature == (
        "mldsa65-sig-001"
    )


def test_serializes():

    signatures = TcuIdentitySignatures(
        ed25519_signature="ed25519-sig-001",
        mldsa65_signature="mldsa65-sig-001",
    )

    assert signatures.to_dict() == {
        "ed25519_signature":
            "ed25519-sig-001",
        "mldsa65_signature":
            "mldsa65-sig-001",
    }
