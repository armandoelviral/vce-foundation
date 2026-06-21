class GovernanceVerifier:

    @staticmethod
    def verify(
        citizen,
    ) -> bool:

        return (
            citizen.status
            == "ACTIVE"
        )
