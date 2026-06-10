from epics.epic077_veracity_transparency_sidecar.anchor_job import (
    AnchorJob,
)
from epics.epic077_veracity_transparency_sidecar.anchor_queue import (
    AnchorQueue,
)
from epics.epic077_veracity_transparency_sidecar.anchor_status import (
    AnchorStatus,
)


def build_job(job_id="job-001"):

    return AnchorJob(
        job_id=job_id,
        proof_hash=f"proof-hash-{job_id}",
        target_backend="rekor",
        status=AnchorStatus.PENDING_TRANSPARENCY,
    )


def test_anchor_queue_starts_empty():

    queue = AnchorQueue()

    assert queue.is_empty() is True
    assert queue.size() == 0


def test_anchor_queue_enqueue_increases_size():

    queue = AnchorQueue()

    queue.enqueue(
        build_job()
    )

    assert queue.size() == 1
    assert queue.is_empty() is False


def test_anchor_queue_dequeue_returns_first_job():

    queue = AnchorQueue()

    first = build_job(
        "job-001"
    )

    second = build_job(
        "job-002"
    )

    queue.enqueue(
        first
    )

    queue.enqueue(
        second
    )

    assert queue.dequeue() == first
    assert queue.dequeue() == second


def test_anchor_queue_dequeue_empty_returns_none():

    queue = AnchorQueue()

    assert queue.dequeue() is None
