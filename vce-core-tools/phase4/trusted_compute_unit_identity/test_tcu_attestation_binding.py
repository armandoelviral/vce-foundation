from phase4.trusted_compute_unit_identity.tcu_attestation_binding import (
    TcuAttestationBinding,
)


def test_contains_identity_hash():

    binding = TcuAttestationBinding(
        identity_hash="identity-hash-001",
        attestation_root="attestation-root-001",
    )

    assert (
        binding.identity_hash
        == "identity-hash-001"
    )


def test_contains_attestation_root():

    binding = TcuAttestationBinding(
        identity_hash="identity-hash-001",
        attestation_root="attestation-root-001",
    )

    assert (
        binding.attestation_root
        == "attestation-root-001"
    )


def test_serializes():

    binding = TcuAttestationBinding(
        identity_hash="identity-hash-001",
        attestation_root="attestation-root-001",
    )

    assert binding.to_dict() == {
        "identity_hash":
            "identity-hash-001",
        "attestation_root":
            "attestation-root-001",
    }
