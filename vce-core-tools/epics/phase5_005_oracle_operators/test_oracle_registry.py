from epics.phase5_005_oracle_operators.oracle_record import OracleRecord
from epics.phase5_005_oracle_operators.oracle_registry import OracleRegistry


def test_registry_stores_oracle():
    registry = OracleRegistry()

    registry.add(
        OracleRecord(
            "oracle.001",
            "operator.001",
            "physical",
        )
    )

    assert len(registry.records()) == 1


def test_rejects_duplicate_oracle():
    registry = OracleRegistry()

    oracle = OracleRecord(
        "oracle.001",
        "operator.001",
        "physical",
    )

    registry.add(oracle)

    try:
        registry.add(oracle)
        assert False
    except ValueError:
        assert True


def test_returns_copy():
    registry = OracleRegistry()

    registry.add(
        OracleRecord(
            "oracle.001",
            "operator.001",
            "physical",
        )
    )

    items = registry.records()
    items.clear()

    assert len(registry.records()) == 1
