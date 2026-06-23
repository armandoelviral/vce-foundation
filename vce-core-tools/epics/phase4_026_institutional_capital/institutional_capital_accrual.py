from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


def calculate_institutional_capital(
    registry: InstitutionalCapitalRegistry,
    institution_id: str,
) -> int:
    records = registry.records_for(institution_id)
    return sum(record.capital_delta for record in records)
