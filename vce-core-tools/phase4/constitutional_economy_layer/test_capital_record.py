from phase4.constitutional_economy_layer.capital_record import (
    CapitalRecord,
)


def test_contains_identity():

    record = CapitalRecord(
        identity_id="identity-001",
        capital=100,
    )

    assert record.identity_id == "identity-001"


def test_contains_capital():

    record = CapitalRecord(
        identity_id="identity-001",
        capital=100,
    )

    assert record.capital == 100


def test_serializes():

    record = CapitalRecord(
        identity_id="identity-001",
        capital=100,
    )

    assert record.to_dict() == {
        "identity_id": "identity-001",
        "capital": 100,
    }
