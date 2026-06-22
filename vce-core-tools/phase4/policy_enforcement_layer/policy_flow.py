from phase4.policy_enforcement_layer.policy_record import (
    PolicyRecord,
)

from phase4.policy_enforcement_layer.policy_registry import (
    PolicyRegistry,
)

from phase4.policy_enforcement_layer.policy_activation import (
    PolicyActivation,
)

from phase4.policy_enforcement_layer.policy_state import (
    PolicyState,
)

from phase4.policy_enforcement_layer.policy_verifier import (
    PolicyVerifier,
)


class PolicyFlow:

    @staticmethod
    def generate():

        policy = PolicyRecord(
            policy_id="policy-001",
            policy_name="minimum_reputation_100",
            active=False,
        )

        activated_policy = (
            PolicyActivation.activate(
                policy
            )
        )

        registry = PolicyRegistry(
            policies=[
                activated_policy
            ]
        )

        state = PolicyState(
            policy_id="policy-001",
            policy_state="ENFORCED",
        )

        valid = (
            PolicyVerifier.verify(
                state
            )
        )

        return {
            "policy":
                activated_policy.to_dict(),
            "registry":
                registry.to_dict(),
            "state":
                state.to_dict(),
            "valid":
                valid,
        }
