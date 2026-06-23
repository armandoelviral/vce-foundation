from epics.phase4_031_constitutional_insurance.insurance_policy import (
    InsurancePolicy,
)


class InsuranceRegistry:
    def __init__(self):
        self._policies = []
        self._policy_ids = set()

    def add(self, policy: InsurancePolicy):
        if policy.policy_id in self._policy_ids:
            raise ValueError("duplicate policy")

        self._policies.append(policy)
        self._policy_ids.add(policy.policy_id)

    def policies(self):
        return list(self._policies)
