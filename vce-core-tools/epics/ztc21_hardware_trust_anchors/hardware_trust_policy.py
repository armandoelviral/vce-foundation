class HardwareTrustPolicy:

    def admit(
        self,
        verified: bool,
    ) -> bool:

        return verified
