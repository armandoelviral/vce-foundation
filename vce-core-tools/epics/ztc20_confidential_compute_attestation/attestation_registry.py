from typing import List

from epics.ztc20_confidential_compute_attestation.attestation_evidence import (
    AttestationEvidence,
)


class AttestationRegistry:

    def __init__(self):

        self._records: List[
            AttestationEvidence
        ] = []

    def add(
        self,
        evidence: AttestationEvidence,
    ) -> None:

        self._records.append(
            evidence
        )

    def all(
        self,
    ) -> List[AttestationEvidence]:

        return list(
            self._records
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )
