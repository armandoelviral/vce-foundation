from epics.ztc6_execution_provenance_binding.execution_provenance_record import (
    ExecutionProvenanceRecord,
)

from epics.ztc6_execution_provenance_binding.provenance_verifier import (
    ProvenanceVerifier,
)


def test_accepts_complete_record():

    record = ExecutionProvenanceRecord(
        artifact_hash="artifact-001",
        execution_id="execution-001",
        result_hash="result-001",
    )

    assert ProvenanceVerifier.verify(
        record
    )


def test_rejects_missing_artifact_hash():

    record = ExecutionProvenanceRecord(
        artifact_hash="",
        execution_id="execution-001",
        result_hash="result-001",
    )

    assert not ProvenanceVerifier.verify(
        record
    )
