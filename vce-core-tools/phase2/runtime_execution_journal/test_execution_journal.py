from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)

from phase2.runtime_execution_journal.execution_journal import (
    ExecutionJournal,
)


def test_journal_starts_empty():

    journal = ExecutionJournal()

    assert journal.count() == 0


def test_journal_accepts_record():

    journal = ExecutionJournal()

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    journal.append(record)

    assert journal.count() == 1


def test_journal_returns_record_by_id():

    journal = ExecutionJournal()

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    journal.append(record)

    recovered = journal.get(
        "exec-001"
    )

    assert recovered == record


def test_unknown_execution_returns_none():

    journal = ExecutionJournal()

    assert journal.get(
        "missing"
    ) is None
