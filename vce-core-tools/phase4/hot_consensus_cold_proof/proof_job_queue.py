from collections import deque

from phase4.hot_consensus_cold_proof.proof_job_record import (
    ProofJobRecord,
)


class ProofJobQueue:

    def __init__(self):

        self._queue = deque()

    def enqueue(
        self,
        job: ProofJobRecord,
    ) -> None:

        self._queue.append(job)

    def dequeue(
        self,
    ):

        if not self._queue:
            return None

        return self._queue.popleft()

    def count(
        self,
    ) -> int:

        return len(self._queue)
