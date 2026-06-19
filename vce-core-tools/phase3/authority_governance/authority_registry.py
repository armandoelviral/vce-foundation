from phase3.authority_governance.authority_record import (
    AuthorityRecord,
)


class AuthorityRegistry:

    def __init__(self):

        self._authorities = {}

    def add(
        self,
        authority: AuthorityRecord,
    ) -> None:

        self._authorities[
            authority.authority_id
        ] = authority

    def get(
        self,
        authority_id: str,
    ):

        return self._authorities.get(
            authority_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._authorities
        )

    def authority_ids(
        self,
    ):

        return list(
            self._authorities.keys()
        )
