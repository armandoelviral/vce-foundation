from phase4.hot_consensus_cold_proof.proof_result_record import (
    ProofResultRecord,
)

from phase4.hot_consensus_cold_proof.proof_attachment import (
    ProofAttachment,
)


def test_attachment_contains_execution_request_id():

    attachment = (
        ProofAttachment.attach(
            execution_request_id="request-001",
            proof_result=ProofResultRecord(
                result_id="result-001",
                job_id="job-001",
                proof_hash="proof-hash-001",
                status="COMPLETED",
            ),
        )
    )

    assert (
        attachment.execution_request_id
        == "request-001"
    )


def test_attachment_contains_proof_hash():

    attachment = (
        ProofAttachment.attach(
            execution_request_id="request-001",
            proof_result=ProofResultRecord(
                result_id="result-001",
                job_id="job-001",
                proof_hash="proof-hash-001",
                status="COMPLETED",
            ),
        )
    )

    assert (
        attachment.proof_hash
        == "proof-hash-001"
    )


def test_attachment_contains_result_id():

    attachment = (
        ProofAttachment.attach(
            execution_request_id="request-001",
            proof_result=ProofResultRecord(
                result_id="result-001",
                job_id="job-001",
                proof_hash="proof-hash-001",
                status="COMPLETED",
            ),
        )
    )

    assert (
        attachment.result_id
        == "result-001"
    )


def test_attachment_serializes():

    attachment = (
        ProofAttachment.attach(
            execution_request_id="request-001",
            proof_result=ProofResultRecord(
                result_id="result-001",
                job_id="job-001",
                proof_hash="proof-hash-001",
                status="COMPLETED",
            ),
        )
    )

    assert attachment.to_dict() == {
        "execution_request_id": "request-001",
        "result_id": "result-001",
        "proof_hash": "proof-hash-001",
    }
