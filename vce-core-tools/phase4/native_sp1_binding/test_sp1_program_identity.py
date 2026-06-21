from phase4.native_sp1_binding.sp1_program_identity import (
    SP1ProgramIdentity,
)


def test_contains_program_id():

    identity = SP1ProgramIdentity(
        tcu_did="did:tcn:test:01",
        program_id="fibonacci-program",
        program_hash="sha256:abc123",
    )

    assert identity.program_id == (
        "fibonacci-program"
    )


def test_contains_program_hash():

    identity = SP1ProgramIdentity(
        tcu_did="did:tcn:test:01",
        program_id="fibonacci-program",
        program_hash="sha256:abc123",
    )

    assert identity.program_hash == (
        "sha256:abc123"
    )


def test_serializes():

    identity = SP1ProgramIdentity(
        tcu_did="did:tcn:test:01",
        program_id="fibonacci-program",
        program_hash="sha256:abc123",
    )

    assert identity.to_dict() == {
        "tcu_did": "did:tcn:test:01",
        "program_id": "fibonacci-program",
        "program_hash": "sha256:abc123",
    }
