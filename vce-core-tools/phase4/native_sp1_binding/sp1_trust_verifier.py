class SP1TrustVerifier:

    @staticmethod
    def verify(
        claim,
    ) -> bool:

        return bool(
            claim.citizen_did
        )
