from dataclasses import dataclass

from epics.phase5_005_oracle_operators.oracle_record import (
    OracleRecord,
)


@dataclass(frozen=True)
class OracleState:
    total_oracles: int

    @classmethod
    def from_records(
        cls,
        records: list[OracleRecord],
    ):
        return cls(
            total_oracles=len(records)
        )
