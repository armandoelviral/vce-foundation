from epics.phase5_005_oracle_operators.oracle_record import (
    OracleRecord,
)
from epics.phase5_005_oracle_operators.oracle_state import (
    OracleState,
)


def test_builds_oracle_state():
    state = OracleState.from_records(
        [
            OracleRecord(
                "oracle.001",
                "operator.001",
                "physical",
            )
        ]
    )

    assert state.total_oracles == 1


def test_empty_state():
    state = OracleState.from_records([])

    assert state.total_oracles == 0
