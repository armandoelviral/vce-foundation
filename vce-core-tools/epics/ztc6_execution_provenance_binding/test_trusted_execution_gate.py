from epics.ztc6_execution_provenance_binding.execution_provenance_record import (
    ExecutionProvenanceRecord,
)

from epics.ztc6_execution_provenance_binding.provenance_attestation import (
    ProvenanceAttestation,
)

from epics.ztc6_execution_provenance_binding.trusted_execution_gate import (
    TrustedExecutionGate,
)


def test_accepts_valid_attestation():

    record = ExecutionProvenanceRecord(
        artifact_hash="artifact-001",
        execution_id="execution-001",
        result_hash="result-001",
    )

    attestation = ProvenanceAttestation.build(
        record
    )

    assert TrustedExecutionGate.admit(
        attestation
    )


def test_rejects_incomplete_attestation():

    attestation = {
        "artifact_hash": "artifact-001",
        "execution_id": "execution-001",
    }

    assert not TrustedExecutionGate.admit(
        attestation
    )
