from epics.phase4_036_constitutional_sustainability.sustainability_audit import (
    audit_sustainability,
)
from epics.phase4_036_constitutional_sustainability.sustainability_depletion import (
    SustainabilityDepletionRecord,
)
from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)


def test_sustainability_audit():
    records = [
        SustainabilityRecord(
            sustainability_id="sus.001",
            source_id="stability.001",
            sustainability_amount=100,
            rationale="long-term continuity",
        )
    ]

    depletions = [
        SustainabilityDepletionRecord(
            depletion_id="depletion.001",
            sustainability_id="sus.001",
            depletion_amount=40,
            reason="resource exhaustion",
        )
    ]

    audit = audit_sustainability(records, depletions)

    assert audit["sustainability_count"] == 1
    assert audit["depletion_count"] == 1
    assert audit["total_sustainability"] == 100
    assert audit["total_depletion"] == 40


def test_empty_sustainability_audit():
    audit = audit_sustainability([], [])

    assert audit["sustainability_count"] == 0
    assert audit["depletion_count"] == 0
    assert audit["total_sustainability"] == 0
    assert audit["total_depletion"] == 0
