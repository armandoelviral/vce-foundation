from phase3.governance_policy_enforcement.policy_activation_record import (
    PolicyActivationRecord,
)


class PolicyActivationRegistry:

    def __init__(self):

        self._activations = {}

    def add(
        self,
        record: PolicyActivationRecord,
    ) -> None:

        self._activations[
            record.activation_id
        ] = record

    def get(
        self,
        activation_id: str,
    ):

        return self._activations.get(
            activation_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._activations
        )

    def activation_ids(
        self,
    ):

        return list(
            self._activations.keys()
        )
