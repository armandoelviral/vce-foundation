from dataclasses import dataclass

from epics.phase5_002_witness_attestation.witness_record import (
    WitnessRecord,
)


@dataclass(frozen=True)
class WitnessState:
    total_witnesses: int

    @classmethod
    def from_records(
        cls,
        records: list[WitnessRecord],
    ):
        return cls(
            total_witnesses=len(records)
        )
