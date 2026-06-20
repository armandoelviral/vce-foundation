from phase4.hot_consensus_cold_proof.proof_job_record import (
    ProofJobRecord,
)

from phase4.hot_consensus_cold_proof.proof_job_queue import (
    ProofJobQueue,
)


def test_queue_starts_empty():

    queue = ProofJobQueue()

    assert queue.count() == 0


def test_enqueue_job():

    queue = ProofJobQueue()

    job = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    queue.enqueue(job)

    assert queue.count() == 1


def test_dequeue_job():

    queue = ProofJobQueue()

    job = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    queue.enqueue(job)

    recovered = queue.dequeue()

    assert recovered == job

    assert queue.count() == 0


def test_dequeue_empty_returns_none():

    queue = ProofJobQueue()

    assert queue.dequeue() is None


def test_fifo_order():

    queue = ProofJobQueue()

    job1 = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    job2 = ProofJobRecord(
        job_id="job-002",
        execution_request_id="request-002",
        prover_type="SP1",
        status="PENDING",
    )

    queue.enqueue(job1)
    queue.enqueue(job2)

    assert queue.dequeue() == job1
    assert queue.dequeue() == job2
