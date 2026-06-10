from dataclasses import dataclass

from epics.epic077_veracity_transparency_sidecar.anchor_status import (
    AnchorStatus,
)


@dataclass(frozen=True)
class AnchorJob:
    job_id: str
    proof_hash: str
    target_backend: str
    status: AnchorStatus
    retry_count: int = 0

    def mark_anchoring(self):

        return AnchorJob(
            job_id=self.job_id,
            proof_hash=self.proof_hash,
            target_backend=self.target_backend,
            status=AnchorStatus.ANCHORING,
            retry_count=self.retry_count,
        )

    def mark_anchored(self):

        return AnchorJob(
            job_id=self.job_id,
            proof_hash=self.proof_hash,
            target_backend=self.target_backend,
            status=AnchorStatus.TRANSPARENCY_ANCHORED,
            retry_count=self.retry_count,
        )

    def mark_retrying(self):

        return AnchorJob(
            job_id=self.job_id,
            proof_hash=self.proof_hash,
            target_backend=self.target_backend,
            status=AnchorStatus.RETRYING,
            retry_count=self.retry_count + 1,
        )

    def mark_failed(self):

        return AnchorJob(
            job_id=self.job_id,
            proof_hash=self.proof_hash,
            target_backend=self.target_backend,
            status=AnchorStatus.FAILED,
            retry_count=self.retry_count,
        )
