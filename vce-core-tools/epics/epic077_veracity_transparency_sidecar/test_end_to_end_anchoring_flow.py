from epics.epic077_veracity_transparency_sidecar.anchor_job import (
    AnchorJob,
)
from epics.epic077_veracity_transparency_sidecar.anchor_queue import (
    AnchorQueue,
)
from epics.epic077_veracity_transparency_sidecar.anchor_status import (
    AnchorStatus,
)
from epics.epic077_veracity_transparency_sidecar.anchor_worker import (
    AnchorWorker,
)


def test_end_to_end_anchoring_flow():

    queue = AnchorQueue()
    worker = AnchorWorker()

    job = AnchorJob(
        job_id="job-001",
        proof_hash="proof-hash-001",
        target_backend="rekor",
        status=AnchorStatus.PENDING_TRANSPARENCY,
    )

    queue.enqueue(
        job
    )

    assert queue.size() == 1

    dequeued = queue.dequeue()

    assert dequeued == job
    assert queue.is_empty() is True

    result = worker.process(
        dequeued
    )

    assert result.status == AnchorStatus.TRANSPARENCY_ANCHORED
    assert result.proof_hash == "proof-hash-001"
    assert result.target_backend == "rekor"


def test_end_to_end_retrying_job_flow():

    queue = AnchorQueue()
    worker = AnchorWorker()

    job = AnchorJob(
        job_id="job-002",
        proof_hash="proof-hash-002",
        target_backend="private-log",
        status=AnchorStatus.RETRYING,
        retry_count=1,
    )

    queue.enqueue(
        job
    )

    result = worker.process(
        queue.dequeue()
    )

    assert result.status == AnchorStatus.TRANSPARENCY_ANCHORED
    assert result.retry_count == 1
    assert result.target_backend == "private-log"
