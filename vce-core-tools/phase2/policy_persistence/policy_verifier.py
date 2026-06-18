from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)


class PolicyVerifier:

    @staticmethod
    def verify(
        policy,
        expected_version: int,
    ) -> bool:

        if policy is None:
            return False

        return (
            policy.version
            == expected_version
        )
