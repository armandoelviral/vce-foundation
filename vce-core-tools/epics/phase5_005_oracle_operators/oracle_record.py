from dataclasses import dataclass


@dataclass(frozen=True)
class OracleRecord:
    oracle_id: str
    operator_id: str
    oracle_type: str

    def __post_init__(self):
        if not self.oracle_id:
            raise ValueError("oracle_id is required")

        if not self.operator_id:
            raise ValueError("operator_id is required")

        if not self.oracle_type:
            raise ValueError("oracle_type is required")
