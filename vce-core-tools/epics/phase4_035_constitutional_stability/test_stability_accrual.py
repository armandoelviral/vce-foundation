from epics.phase4_035_constitutional_stability.stability_accrual import (
    calculate_total_stability,
)
from epics.phase4_035_constitutional_stability.stability_record import (
    StabilityRecord,
)


def test_calculates_total_stability():
    records = [
        StabilityRecord(
            "s1",
            "t1",
            100,
            "continuity",
        ),
        StabilityRecord(
            "s2",
            "t2",
            50,
            "continuity",
        ),
    ]

    assert calculate_total_stability(
        records
    ) == 150


def test_empty_stability():
    assert calculate_total_stability([]) == 0


def test_single_stability():
    records = [
        StabilityRecord(
            "s1",
            "t1",
            75,
            "continuity",
        )
    ]

    assert calculate_total_stability(
        records
    ) == 75
