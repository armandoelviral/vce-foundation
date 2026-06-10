from epics.epic077_veracity_transparency_sidecar.anchor_job import (
    AnchorJob,
)
from epics.epic077_veracity_transparency_sidecar.anchor_status import (
    AnchorStatus,
)


class AnchorWorker:

    def process(
        self,
        job: AnchorJob,
    ):

        if job.status not in {
            AnchorStatus.PENDING_TRANSPARENCY,
            AnchorStatus.RETRYING,
        }:
            return job

        anchoring = job.mark_anchoring()

        return anchoring.mark_anchored()
