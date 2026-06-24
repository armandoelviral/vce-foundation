from epics.phase4_036_constitutional_sustainability.sustainability_record import SustainabilityRecord
from epics.phase4_036_constitutional_sustainability.sustainability_accrual import calculate_total_sustainability


def test_calculates_total():
    records = [
        SustainabilityRecord("a", "b", 100, "x"),
        SustainabilityRecord("c", "d", 50, "y"),
    ]

    assert calculate_total_sustainability(records) == 150


def test_empty():
    assert calculate_total_sustainability([]) == 0


def test_single():
    records = [
        SustainabilityRecord("a", "b", 75, "x")
    ]

    assert calculate_total_sustainability(records) == 75
