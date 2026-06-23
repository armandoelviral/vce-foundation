from phase4.constitutional_economy_layer.capital_registry import (
    CapitalRegistry,
)

from phase4.constitutional_economy_layer.capital_record import (
    CapitalRecord,
)


def test_contains_records():

    registry = CapitalRegistry(
        records=[
            CapitalRecord(
                identity_id="identity-001",
                capital=100,
            )
        ]
    )

    assert len(registry.records) == 1


def test_serializes():

    registry = CapitalRegistry(
        records=[
            CapitalRecord(
                identity_id="identity-001",
                capital=100,
            )
        ]
    )

    assert registry.to_dict() == {
        "records": [
            {
                "identity_id": "identity-001",
                "capital": 100,
            }
        ]
    }
