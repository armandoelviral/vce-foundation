class ReleaseGatePolicy:

    def approve(
        self,
        security_validated: bool,
        governance_approved: bool,
    ) -> bool:

        return (
            security_validated
            and governance_approved
        )
