from phase4.native_sp1_integration.sp1_guest_program import (
    SP1GuestProgram,
)


def test_guest_program_contains_program_id():

    program = SP1GuestProgram(
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
        output_hash="output-hash-001",
    )

    assert program.program_id == "sp1-guest-001"


def test_guest_program_contains_input_hash():

    program = SP1GuestProgram(
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
        output_hash="output-hash-001",
    )

    assert program.input_hash == "input-hash-001"


def test_guest_program_contains_output_hash():

    program = SP1GuestProgram(
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
        output_hash="output-hash-001",
    )

    assert program.output_hash == "output-hash-001"


def test_guest_program_serializes():

    program = SP1GuestProgram(
        program_id="sp1-guest-001",
        input_hash="input-hash-001",
        output_hash="output-hash-001",
    )

    assert program.to_dict() == {
        "program_id": "sp1-guest-001",
        "input_hash": "input-hash-001",
        "output_hash": "output-hash-001",
    }
