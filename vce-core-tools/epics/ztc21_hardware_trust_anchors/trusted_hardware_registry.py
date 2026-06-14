from typing import List

from epics.ztc21_hardware_trust_anchors.hardware_admission_record import (
    HardwareAdmissionRecord,
)


class TrustedHardwareRegistry:

    def __init__(self):

        self._records: List[
            HardwareAdmissionRecord
        ] = []

    def add(
        self,
        record: HardwareAdmissionRecord,
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

    def is_trusted(
        self,
        provider: str,
    ) -> bool:

        return any(
            record.provider == provider
            and record.admitted
            for record in self._records
        )
