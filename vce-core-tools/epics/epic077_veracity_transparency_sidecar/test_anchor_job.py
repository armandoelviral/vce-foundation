from epics.epic077_veracity_transparency_sidecar.anchor_job import (
    AnchorJob,
)
from epics.epic077_veracity_transparency_sidecar.anchor_status import (
    AnchorStatus,
)


def build_job():

    return AnchorJob(
        job_id="job-001",
        proof_hash="proof-hash-001",
        target_backend="rekor",
        status=AnchorStatus.PENDING_TRANSPARENCY,
    )


def test_anchor_job_creation():

    job = build_job()

    assert job.job_id == "job-001"
    assert job.proof_hash == "proof-hash-001"
    assert job.target_backend == "rekor"
    assert job.status == AnchorStatus.PENDING_TRANSPARENCY


def test_anchor_job_mark_anchoring():

    job = build_job()

    updated = job.mark_anchoring()

    assert updated.status == AnchorStatus.ANCHORING
    assert job.status == AnchorStatus.PENDING_TRANSPARENCY


def test_anchor_job_mark_anchored():

    job = build_job()

    updated = job.mark_anchored()

    assert updated.status == AnchorStatus.TRANSPARENCY_ANCHORED


def test_anchor_job_mark_retrying_increments_retry_count():

    job = build_job()

    updated = job.mark_retrying()

    assert updated.status == AnchorStatus.RETRYING
    assert updated.retry_count == 1


def test_anchor_job_mark_failed():

    job = build_job()

    updated = job.mark_failed()

    assert updated.status == AnchorStatus.FAILED
