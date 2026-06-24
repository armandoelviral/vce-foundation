from epics.phase5_005_oracle_operators.oracle_attestation import (
    attest_oracle,
)
from epics.phase5_005_oracle_operators.oracle_record import (
    OracleRecord,
)


def test_attests_oracle():
    oracle = OracleRecord(
        "oracle.001",
        "operator.001",
        "physical",
    )

    result = attest_oracle(oracle)

    assert result["attested"] is True


def test_contains_oracle_id():
    oracle = OracleRecord(
        "oracle.001",
        "operator.001",
        "physical",
    )

    result = attest_oracle(oracle)

    assert result["oracle_id"] == "oracle.001"
