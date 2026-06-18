from phase2.witness_persistence.witness_vote_store import (
    WitnessVoteStore,
)


class WitnessVoteQuery:

    def __init__(
        self,
        store: WitnessVoteStore,
    ):

        self.store = store

    def by_decision(
        self,
        decision_id: str,
    ):

        return [
            vote
            for vote
            in self.store.all()
            if vote.decision_id == decision_id
        ]
