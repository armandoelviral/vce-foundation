from epics.phase4_026_institutional_capital.institutional_capital_registry import (
    InstitutionalCapitalRegistry,
)


def audit_institutional_capital(
    registry: InstitutionalCapitalRegistry,
    institution_id: str,
) -> dict:
    records = registry.records_for(institution_id)

    positive_capital = sum(
        record.capital_delta for record in records if record.capital_delta > 0
    )
    negative_capital = sum(
        record.capital_delta for record in records if record.capital_delta < 0
    )

    return {
        "institution_id": institution_id,
        "total_capital": positive_capital + negative_capital,
        "positive_capital": positive_capital,
        "negative_capital": negative_capital,
        "record_count": len(records),
        "records": records,
    }

