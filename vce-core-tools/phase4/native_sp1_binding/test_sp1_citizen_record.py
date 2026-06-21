from phase4.native_sp1_binding.sp1_citizen_record import (
    SP1CitizenRecord,
)


def test_contains_did():

    record = SP1CitizenRecord(
        tcu_did="did:tcn:test:01",
        program_id="fibonacci-program",
        verification_key="0x123",
        proof_digest="proof-001",
        public_values={"n": 1},
    )

    assert record.tcu_did == (
        "did:tcn:test:01"
    )


def test_contains_program():

    record = SP1CitizenRecord(
        tcu_did="did:tcn:test:01",
        program_id="fibonacci-program",
        verification_key="0x123",
        proof_digest="proof-001",
        public_values={"n": 1},
    )

    assert record.program_id == (
        "fibonacci-program"
    )


def test_contains_vk():

    record = SP1CitizenRecord(
        tcu_did="did:tcn:test:01",
        program_id="fibonacci-program",
        verification_key="0x123",
        proof_digest="proof-001",
        public_values={"n": 1},
    )

    assert record.verification_key == (
        "0x123"
    )


def test_serializes():

    record = SP1CitizenRecord(
        tcu_did="did:tcn:test:01",
        program_id="fibonacci-program",
        verification_key="0x123",
        proof_digest="proof-001",
        public_values={"n": 1},
    )

    assert record.to_dict() == {
        "tcu_did": "did:tcn:test:01",
        "program_id": "fibonacci-program",
        "verification_key": "0x123",
        "proof_digest": "proof-001",
        "public_values": {
            "n": 1,
        },
    }
