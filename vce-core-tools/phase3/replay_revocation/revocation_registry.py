from phase3.replay_revocation.replay_revocation_record import (
    ReplayRevocationRecord,
)


class RevocationRegistry:

    def __init__(self):

        self._revocations = {}

    def add(
        self,
        revocation: ReplayRevocationRecord,
    ) -> None:

        self._revocations[
            revocation.revocation_id
        ] = revocation

    def get(
        self,
        revocation_id: str,
    ):

        return self._revocations.get(
            revocation_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._revocations
        )

    def revocations(
        self,
    ):

        return list(
            self._revocations.values()
        )
