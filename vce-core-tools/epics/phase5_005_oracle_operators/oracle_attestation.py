from epics.phase5_005_oracle_operators.oracle_record import (
    OracleRecord,
)


def attest_oracle(oracle: OracleRecord):
    return {
        "attested": True,
        "oracle_id": oracle.oracle_id,
        "operator_id": oracle.operator_id,
    }
