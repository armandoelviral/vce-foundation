from epics.ztc6_execution_provenance_binding.execution_provenance_record import (
    ExecutionProvenanceRecord,
)

from epics.ztc6_execution_provenance_binding.provenance_attestation import (
    ProvenanceAttestation,
)


def test_builds_attestation():

    record = ExecutionProvenanceRecord(
        artifact_hash="artifact-001",
        execution_id="execution-001",
        result_hash="result-001",
    )

    attestation = ProvenanceAttestation.build(
        record
    )

    assert attestation["artifact_hash"] == "artifact-001"
    assert attestation["execution_id"] == "execution-001"
    assert attestation["result_hash"] == "result-001"


def test_attestation_contains_binding_hash():

    record = ExecutionProvenanceRecord(
        artifact_hash="artifact-001",
        execution_id="execution-001",
        result_hash="result-001",
    )

    attestation = ProvenanceAttestation.build(
        record
    )

    assert "binding_hash" in attestation
