from epics.ztc6_execution_provenance_binding.execution_provenance_record import (
    ExecutionProvenanceRecord,
)


def test_record_contains_execution_binding():

    record = ExecutionProvenanceRecord(
        artifact_hash="artifact-001",
        execution_id="execution-001",
        result_hash="result-001",
    )

    assert record.artifact_hash == "artifact-001"
    assert record.execution_id == "execution-001"
    assert record.result_hash == "result-001"


def test_record_serializes():

    record = ExecutionProvenanceRecord(
        artifact_hash="artifact-001",
        execution_id="execution-001",
        result_hash="result-001",
    )

    assert record.to_dict() == {
        "artifact_hash": "artifact-001",
        "execution_id": "execution-001",
        "result_hash": "result-001",
    }
