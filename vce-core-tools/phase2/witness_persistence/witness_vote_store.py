from phase2.witness_persistence.witness_vote_record import (
    WitnessVoteRecord,
)


class WitnessVoteStore:

    def __init__(self):

        self._records = {}

    def add(
        self,
        vote: WitnessVoteRecord,
    ) -> None:

        key = (
            vote.witness_id,
            vote.decision_id,
        )

        self._records[key] = vote

    def get(
        self,
        witness_id: str,
        decision_id: str,
    ):

        return self._records.get(
            (
                witness_id,
                decision_id,
            )
        )

    def all(self):

        return list(
            self._records.values()
        )

    def count(self) -> int:

        return len(
            self._records
        )
