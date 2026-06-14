class WitnessReadmissionPolicy:

    def is_eligible(
        self,
        suspended: bool,
        recovered: bool,
    ) -> bool:

        return (
            suspended
            and recovered
        )
