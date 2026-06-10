from epics.epic077_veracity_transparency_sidecar.anchor_job import (
    AnchorJob,
)


class AnchorQueue:

    def __init__(self):

        self._jobs = []

    def enqueue(
        self,
        job: AnchorJob,
    ):

        self._jobs.append(
            job
        )

    def dequeue(
        self,
    ):

        if not self._jobs:
            return None

        return self._jobs.pop(0)

    def size(
        self,
    ):

        return len(
            self._jobs
        )

    def is_empty(
        self,
    ):

        return self.size() == 0
