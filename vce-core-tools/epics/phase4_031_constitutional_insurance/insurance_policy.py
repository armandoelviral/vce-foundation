from dataclasses import dataclass


@dataclass(frozen=True)
class InsurancePolicy:
    policy_id: str
    holder_id: str
    coverage_amount: int
    covered_risk: str

    def __post_init__(self):
        if not self.policy_id:
            raise ValueError("policy_id is required")

        if not self.holder_id:
            raise ValueError("holder_id is required")

        if self.coverage_amount <= 0:
            raise ValueError("coverage_amount must be positive")

        if not self.covered_risk:
            raise ValueError("covered_risk is required")
