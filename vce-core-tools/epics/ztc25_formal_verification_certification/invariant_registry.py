from typing import List

from epics.ztc25_formal_verification_certification.formal_invariant import (
    FormalInvariant,
)


class InvariantRegistry:

    def __init__(self):

        self._invariants: List[
            FormalInvariant
        ] = []

    def add(
        self,
        invariant: FormalInvariant,
    ) -> None:

        self._invariants.append(
            invariant
        )

    def exists(
        self,
        invariant_id: str,
    ) -> bool:

        return any(
            invariant.invariant_id == invariant_id
            for invariant in self._invariants
        )

    def all(
        self,
    ) -> List[FormalInvariant]:

        return list(
            self._invariants
        )

    def count(
        self,
    ) -> int:

        return len(
            self._invariants
        )
