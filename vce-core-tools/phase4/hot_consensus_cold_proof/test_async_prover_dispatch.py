from phase4.hot_consensus_cold_proof.proof_job_record import (
    ProofJobRecord,
)

from phase4.hot_consensus_cold_proof.proof_job_queue import (
    ProofJobQueue,
)

from phase4.hot_consensus_cold_proof.async_prover_dispatch import (
    AsyncProverDispatch,
)


def test_dispatch_returns_job():

    queue = ProofJobQueue()

    job = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="SP1",
        status="PENDING",
    )

    queue.enqueue(job)

    dispatcher = AsyncProverDispatch(
        queue
    )

    dispatched = dispatcher.dispatch()

    assert dispatched == job


def test_dispatch_empty_queue_returns_none():

    queue = ProofJobQueue()

    dispatcher = AsyncProverDispatch(
        queue
    )

    assert dispatcher.dispatch() is None


def test_dispatch_removes_job_from_queue():

    queue = ProofJobQueue()

    queue.enqueue(
        ProofJobRecord(
            job_id="job-001",
            execution_request_id="request-001",
            prover_type="SP1",
            status="PENDING",
        )
    )

    dispatcher = AsyncProverDispatch(
        queue
    )

    dispatcher.dispatch()

    assert queue.count() == 0


def test_dispatch_preserves_prover_type():

    queue = ProofJobQueue()

    job = ProofJobRecord(
        job_id="job-001",
        execution_request_id="request-001",
        prover_type="RISC_ZERO",
        status="PENDING",
    )

    queue.enqueue(job)

    dispatcher = AsyncProverDispatch(
        queue
    )

    dispatched = dispatcher.dispatch()

    assert (
        dispatched.prover_type
        == "RISC_ZERO"
    )
