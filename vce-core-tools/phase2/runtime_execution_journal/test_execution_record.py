from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)


def test_record_contains_execution_id():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    assert (
        record.execution_id
        == "exec-001"
    )


def test_record_contains_opcode():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    assert record.opcode == "ADD"


def test_record_contains_output():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    assert record.output_data == "3"


def test_record_serializes():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    assert record.to_dict() == {
        "execution_id": "exec-001",
        "opcode": "ADD",
        "input_data": "1,2",
        "output_data": "3",
    }
