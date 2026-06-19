from phase3.admission_control_engine.admission_policy_record import (
    AdmissionPolicyRecord,
)


class AdmissionPolicyRegistry:

    def __init__(self):

        self._policies = {}

    def add(
        self,
        policy: AdmissionPolicyRecord,
    ) -> None:

        self._policies[
            policy.policy_id
        ] = policy

    def get(
        self,
        policy_id: str,
    ):

        return self._policies.get(
            policy_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._policies
        )
