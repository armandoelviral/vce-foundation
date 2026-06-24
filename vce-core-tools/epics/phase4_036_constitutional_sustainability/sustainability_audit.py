from epics.phase4_036_constitutional_sustainability.sustainability_depletion import (
    SustainabilityDepletionRecord,
)
from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)


def audit_sustainability(
    sustainability_records: list[SustainabilityRecord],
    depletions: list[SustainabilityDepletionRecord],
):
    return {
        "sustainability_count": len(
            sustainability_records
        ),
        "depletion_count": len(
            depletions
        ),
        "total_sustainability": sum(
            record.sustainability_amount
            for record in sustainability_records
        ),
        "total_depletion": sum(
            depletion.depletion_amount
            for depletion in depletions
        ),
    }
