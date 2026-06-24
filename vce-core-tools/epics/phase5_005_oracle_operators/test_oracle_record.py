from epics.phase5_005_oracle_operators.oracle_record import (
    OracleRecord,
)


def test_oracle_record_creation():
    record = OracleRecord(
        oracle_id="oracle.001",
        operator_id="operator.001",
        oracle_type="physical",
    )

    assert record.oracle_id == "oracle.001"


def test_rejects_empty_oracle_id():
    try:
        OracleRecord(
            oracle_id="",
            operator_id="operator.001",
            oracle_type="physical",
        )
        assert False
    except ValueError as exc:
        assert "oracle_id" in str(exc)


def test_rejects_empty_operator_id():
    try:
        OracleRecord(
            oracle_id="oracle.001",
            operator_id="",
            oracle_type="physical",
        )
        assert False
    except ValueError as exc:
        assert "operator_id" in str(exc)
