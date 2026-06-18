from phase2.runtime_execution_journal.execution_record import (
    ExecutionRecord,
)

from phase2.runtime_execution_journal.execution_attestation import (
    ExecutionAttestation,
)


def test_execution_attestation_subject():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    attestation = ExecutionAttestation.attest(
        attestation_id="att-001",
        execution=record,
    )

    assert attestation.subject == "execution"


def test_execution_attestation_uses_execution_id():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    attestation = ExecutionAttestation.attest(
        attestation_id="att-001",
        execution=record,
    )

    assert (
        attestation.evidence_hash
        == "exec-001"
    )


def test_execution_attestation_preserves_attestation_id():

    record = ExecutionRecord(
        execution_id="exec-001",
        opcode="ADD",
        input_data="1,2",
        output_data="3",
    )

    attestation = ExecutionAttestation.attest(
        attestation_id="att-001",
        execution=record,
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
