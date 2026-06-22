from phase4.policy_enforcement_layer.policy_record import (
    PolicyRecord,
)


class PolicyActivation:

    @staticmethod
    def activate(
        policy: PolicyRecord,
    ) -> PolicyRecord:

        return PolicyRecord(
            policy_id=policy.policy_id,
            policy_name=policy.policy_name,
            active=True,
        )
