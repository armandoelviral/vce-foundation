from phase4.hot_consensus_cold_proof.proof_result_record import (
    ProofResultRecord,
)


def test_contains_result_id():

    result = ProofResultRecord(
        result_id="result-001",
        job_id="job-001",
        proof_hash="proof-hash-001",
        status="COMPLETED",
    )

    assert result.result_id == "result-001"


def test_contains_job_id():

    result = ProofResultRecord(
        result_id="result-001",
        job_id="job-001",
        proof_hash="proof-hash-001",
        status="COMPLETED",
    )

    assert result.job_id == "job-001"


def test_contains_proof_hash():

    result = ProofResultRecord(
        result_id="result-001",
        job_id="job-001",
        proof_hash="proof-hash-001",
        status="COMPLETED",
    )

    assert result.proof_hash == "proof-hash-001"


def test_contains_status():

    result = ProofResultRecord(
        result_id="result-001",
        job_id="job-001",
        proof_hash="proof-hash-001",
        status="COMPLETED",
    )

    assert result.status == "COMPLETED"


def test_serializes():

    result = ProofResultRecord(
        result_id="result-001",
        job_id="job-001",
        proof_hash="proof-hash-001",
        status="COMPLETED",
    )

    assert result.to_dict() == {
        "result_id": "result-001",
        "job_id": "job-001",
        "proof_hash": "proof-hash-001",
        "status": "COMPLETED",
    }
