class PolicyActivationReport:

    def __init__(
        self,
        activations,
    ):

        self.activations = activations

    def activation_count(
        self,
    ) -> int:

        return len(
            self.activations
        )

    def activation_ids(
        self,
    ):

        return list(
            self.activations.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "activation_count":
                self.activation_count(),

            "activation_ids":
                self.activation_ids(),
        }
