from typing import List

from epics.ztc20_confidential_compute_attestation.attestation_admission_record import (
    AttestationAdmissionRecord,
)


class AttestedWitnessRegistry:

    def __init__(self):

        self._records: List[
            AttestationAdmissionRecord
        ] = []

    def add(
        self,
        record: AttestationAdmissionRecord,
    ) -> None:

        self._records.append(
            record
        )

    def count(
        self,
    ) -> int:

        return len(
            self._records
        )

    def is_attested(
        self,
        witness_id: str,
    ) -> bool:

        return any(
            record.witness_id == witness_id
            and record.admitted
            for record in self._records
        )
