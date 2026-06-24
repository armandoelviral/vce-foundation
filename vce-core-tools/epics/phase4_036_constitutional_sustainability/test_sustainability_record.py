from epics.phase4_036_constitutional_sustainability.sustainability_record import (
    SustainabilityRecord,
)


def test_sustainability_record_creation():
    record = SustainabilityRecord(
        "sus.001",
        "stability.001",
        100,
        "continuity",
    )

    assert record.sustainability_amount == 100


def test_rejects_empty_id():
    try:
        SustainabilityRecord(
            "",
            "stability.001",
            100,
            "continuity",
        )
        assert False
    except ValueError:
        assert True


def test_rejects_non_positive_amount():
    try:
        SustainabilityRecord(
            "sus.001",
            "stability.001",
            0,
            "continuity",
        )
        assert False
    except ValueError:
        assert True
