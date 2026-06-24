from epics.phase4_037_constitutional_prosperity.prosperity_accrual import (
    calculate_total_prosperity,
)
from epics.phase4_037_constitutional_prosperity.prosperity_record import (
    ProsperityRecord,
)


def test_calculates_total_prosperity():
    records = [
        ProsperityRecord("prosperity.001", "sustainability.001", 100, "growth"),
        ProsperityRecord("prosperity.002", "sustainability.002", 50, "growth"),
    ]

    assert calculate_total_prosperity(records) == 150


def test_empty_prosperity():
    assert calculate_total_prosperity([]) == 0


def test_single_prosperity():
    records = [
        ProsperityRecord("prosperity.001", "sustainability.001", 75, "growth")
    ]

    assert calculate_total_prosperity(records) == 75
