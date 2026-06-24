from dataclasses import dataclass

from epics.phase5_006_reality_verification.reality_claim import (
    RealityClaim,
)


@dataclass(frozen=True)
class RealityState:
    total_claims: int

    @classmethod
    def from_records(
        cls,
        records: list[RealityClaim],
    ):
        return cls(
            total_claims=len(records)
        )
