from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)


def calculate_total_coverage(
    policies: list[InsurancePolicy],
) -> int:
    return sum(
        policy.coverage_amount
        for policy in policies
    )
