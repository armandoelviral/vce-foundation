from phase4.native_sp1_integration.sp1_proof_request import (
    SP1ProofRequest,
)


def test_contains_request_id():

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    assert request.request_id == "proof-001"


def test_contains_program_id():

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    assert request.program_id == "sp1-guest-001"


def test_contains_input_hash():

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    assert request.input_hash == "input-hash-001"


def test_serializes():

    request = SP1ProofRequest(
        request_id="proof-001",
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
    )

    assert request.to_dict() == {
        "request_id": "proof-001",
        "program_id": "sp1-guest-001",
        "input_hash": "input-hash-001",
    }
