from phase4.hot_consensus_cold_proof.proof_job_record import (
    ProofJobRecord,
)


def test_contains_job_id():

    record = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    assert record.job_id == "job-001"


def test_contains_execution_request_id():

    record = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    assert (
        record.execution_request_id
        == "request-001"
    )


def test_contains_prover_type():

    record = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    assert record.prover_type == "SP1"


def test_contains_status():

    record = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    assert record.status == "PENDING"


def test_serializes():

    record = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    assert record.to_dict() == {
        "job_id": "job-001",
        "execution_request_id": "request-001",
        "prover_type": "SP1",
        "status": "PENDING",
    }
