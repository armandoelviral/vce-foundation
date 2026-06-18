from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)

from phase2.runtime_execution_journal.execution_verifier import (
    ExecutionVerifier,
)


def test_verifier_accepts_matching_output():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    assert (
        ExecutionVerifier.verify(
            record,
            expected_output="3",
        )
        is True
    )


def test_verifier_rejects_mismatch():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    assert (
        ExecutionVerifier.verify(
            record,
            expected_output="999",
        )
        is False
    )


def test_verifier_rejects_empty_output():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="",
    )

    assert (
        ExecutionVerifier.verify(
            record,
            expected_output="",
        )
        is False
    )
