class WitnessAttestationPolicy:

    def admit(
        self,
        verified: bool,
    ) -> bool:

        return verified
