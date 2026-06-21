from phase4.native_sp1_binding.sp1_verification_key_binding import (
    SP1VerificationKeyBinding,
)


def test_contains_did():

    binding = SP1VerificationKeyBinding(
        tcu_did="did:tcn:test:01",
        verification_key="0x123",
    )

    assert binding.tcu_did == (
        "did:tcn:test:01"
    )


def test_contains_vk():

    binding = SP1VerificationKeyBinding(
        tcu_did="did:tcn:test:01",
        verification_key="0x123",
    )

    assert binding.verification_key == "0x123"


def test_serializes():

    binding = SP1VerificationKeyBinding(
        tcu_did="did:tcn:test:01",
        verification_key="0x123",
    )

    assert binding.to_dict() == {
        "tcu_did": "did:tcn:test:01",
        "verification_key": "0x123",
    }
