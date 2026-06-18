from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)

from phase2.runtime_execution_journal.execution_journal import (
    ExecutionJournal,
)

from phase2.runtime_execution_journal.execution_query import (
    ExecutionQuery,
)


def test_query_returns_execution_by_opcode():

    journal = ExecutionJournal()

    journal.append(
        ExecutionRecord(
            execution_id="exec-001",
            opcode="ADD",
            input_data="1,2",
            output_data="3",
        )
    )

    query = ExecutionQuery(journal)

    results = query.by_opcode(
        "ADD"
    )

    assert len(results) == 1
    assert results[0].execution_id == "exec-001"


def test_query_returns_empty_for_unknown_opcode():

    journal = ExecutionJournal()

    query = ExecutionQuery(
        journal
    )

    assert query.by_opcode(
        "MISSING"
    ) == []


def test_query_filters_multiple_opcodes():

    journal = ExecutionJournal()

    journal.append(
        ExecutionRecord(
            execution_id="exec-001",
            opcode="ADD",
            input_data="1,2",
            output_data="3",
        )
    )

    journal.append(
        ExecutionRecord(
            execution_id="exec-002",
            opcode="SUB",
            input_data="5,2",
            output_data="3",
        )
    )

    query = ExecutionQuery(
        journal
    )

    results = query.by_opcode(
        "SUB"
    )

    assert len(results) == 1
    assert results[0].execution_id == "exec-002"
