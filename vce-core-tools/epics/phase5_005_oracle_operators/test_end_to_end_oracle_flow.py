from epics.phase5_005_oracle_operators.oracle_attestation import (
    attest_oracle,
)
from epics.phase5_005_oracle_operators.oracle_record import (
    OracleRecord,
)
from epics.phase5_005_oracle_operators.oracle_registry import (
    OracleRegistry,
)


def test_end_to_end_oracle_flow():
    registry = OracleRegistry()

    registry.add(
        OracleRecord(
            oracle_id="oracle.001",
            operator_id="operator.001",
            oracle_type="physical",
        )
    )

    result = attest_oracle(
        registry.records()[0]
    )

    assert result["attested"] is True
    assert result["oracle_id"] == "oracle.001"

