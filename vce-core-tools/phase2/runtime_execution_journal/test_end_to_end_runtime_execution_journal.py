from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)

from phase2.runtime_execution_journal.execution_journal import (
    ExecutionJournal,
)

from phase2.runtime_execution_journal.execution_query import (
    ExecutionQuery,
)

from phase2.runtime_execution_journal.execution_verifier import (
    ExecutionVerifier,
)

from phase2.runtime_execution_journal.execution_attestation import (
    ExecutionAttestation,
)

from phase2.runtime_execution_journal.execution_report import (
    ExecutionReport,
)


def test_end_to_end_execution_journal_flow():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    journal = ExecutionJournal()

    journal.append(record)

    assert journal.count() == 1

    query = ExecutionQuery(journal)

    results = query.by_opcode(
        "ADD"
    )

    assert len(results) == 1

    verified = ExecutionVerifier.verify(
        results[0],
        expected_output="3",
    )

    assert verified is True

    attestation = ExecutionAttestation.attest(
        attestation_id="att-001",
        execution=results[0],
    )

    assert attestation.subject == "execution"

    report = ExecutionReport(
        results
    )

    assert (
        report.total_executions()
        == 1
    )

    assert report.opcodes() == [
        "ADD"
    ]
