from dataclasses import dataclass

from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


@dataclass(frozen=True)
class InstitutionalCapitalState:
    institution_id: str
    total_capital: int
    record_count: int

    @classmethod
    def from_registry(
        cls,
        registry: InstitutionalCapitalRegistry,
        institution_id: str,
    ):
        records = registry.records_for(institution_id)

        return cls(
            institution_id=institution_id,
            total_capital=sum(
                record.capital_delta
                for record in records
            ),
            record_count=len(records),
        )
