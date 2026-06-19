from phase3.witness_vote_verification.vote_registry import (
    VoteRegistry,
)


class VoteQuery:

    def __init__(
        self,
        registry: VoteRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        vote_id: str,
    ):

        return self.registry.get(
            vote_id
        )
