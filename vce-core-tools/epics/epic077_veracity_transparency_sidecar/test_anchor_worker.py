from epics.epic077_veracity_transparency_sidecar.anchor_job import (
    AnchorJob,
)
from epics.epic077_veracity_transparency_sidecar.anchor_status import (
    AnchorStatus,
)
from epics.epic077_veracity_transparency_sidecar.anchor_worker import (
    AnchorWorker,
)


def build_job(status=AnchorStatus.PENDING_TRANSPARENCY):

    return AnchorJob(
        job_id="job-001",
        proof_hash="proof-hash-001",
        target_backend="rekor",
        status=status,
    )


def test_anchor_worker_processes_pending_job():

    worker = AnchorWorker()

    result = worker.process(
        build_job()
    )

    assert result.status == AnchorStatus.TRANSPARENCY_ANCHORED


def test_anchor_worker_processes_retrying_job():

    worker = AnchorWorker()

    result = worker.process(
        build_job(
            status=AnchorStatus.RETRYING
        )
    )

    assert result.status == AnchorStatus.TRANSPARENCY_ANCHORED


def test_anchor_worker_ignores_already_anchored_job():

    worker = AnchorWorker()

    job = build_job(
        status=AnchorStatus.TRANSPARENCY_ANCHORED
    )

    result = worker.process(
        job
    )

    assert result == job
