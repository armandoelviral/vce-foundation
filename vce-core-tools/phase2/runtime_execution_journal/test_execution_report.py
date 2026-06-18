from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)

from phase2.runtime_execution_journal.execution_report import (
    ExecutionReport,
)


def test_report_contains_total_executions():

    records = [
        ExecutionRecord(
            execution_id="exec-001",
            opcode="ADD",
            input_data="1,2",
            output_data="3",
        ),
        ExecutionRecord(
            execution_id="exec-002",
            opcode="SUB",
            input_data="5,2",
            output_data="3",
        ),
    ]

    report = ExecutionReport(records)

    assert report.total_executions() == 2


def test_report_lists_opcodes():

    records = [
        ExecutionRecord(
            execution_id="exec-001",
            opcode="ADD",
            input_data="1,2",
            output_data="3",
        ),
        ExecutionRecord(
            execution_id="exec-002",
            opcode="SUB",
            input_data="5,2",
            output_data="3",
        ),
    ]

    report = ExecutionReport(records)

    assert report.opcodes() == [
        "ADD",
        "SUB",
    ]


def test_report_serializes():

    records = [
        ExecutionRecord(
            execution_id="exec-001",
            opcode="ADD",
            input_data="1,2",
            output_data="3",
        )
    ]

    report = ExecutionReport(records)

    assert report.to_dict() == {
        "total_executions": 1,
        "opcodes": [
            "ADD",
        ],
    }
