from dataclasses import dataclass

from epics.phase4_031_constitutional_insurance.claim_record import (
    ClaimRecord,
)
from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)


@dataclass(frozen=True)
class InsuranceState:
    total_coverage: int
    total_claims: int
    remaining_coverage: int

    @classmethod
    def from_records(
        cls,
        policies: list[InsurancePolicy],
        claims: list[ClaimRecord],
    ):
        total_coverage = sum(
            policy.coverage_amount
            for policy in policies
        )

        total_claims = sum(
            claim.claim_amount
            for claim in claims
        )

        return cls(
            total_coverage=total_coverage,
            total_claims=total_claims,
            remaining_coverage=(
                total_coverage - total_claims
            ),
        )
