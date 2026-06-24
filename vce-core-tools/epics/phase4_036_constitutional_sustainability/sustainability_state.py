from dataclasses import dataclass

from epics.phase4_036_constitutional_sustainability.sustainability_depletion import (
    SustainabilityDepletionRecord,
)
from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)


@dataclass(frozen=True)
class SustainabilityState:
    total_sustainability: int
    total_depletion: int
    net_sustainability: int

    @classmethod
    def from_records(
        cls,
        sustainability_records,
        depletions,
    ):
        total_sustainability = sum(
            record.sustainability_amount
            for record in sustainability_records
        )

        total_depletion = sum(
            depletion.depletion_amount
            for depletion in depletions
        )

        return cls(
            total_sustainability=total_sustainability,
            total_depletion=total_depletion,
            net_sustainability=
            total_sustainability - total_depletion,
        )
