from phase4.hot_consensus_cold_proof.proof_job_queue import (
    ProofJobQueue,
)


class AsyncProverDispatch:

    def __init__(
        self,
        queue: ProofJobQueue,
    ):

        self.queue = queue

    def dispatch(
        self,
    ):

        return self.queue.dequeue()
