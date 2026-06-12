class GovernanceActiveRule:

    def is_active(
        self,
        governance_status,
    ):

        return governance_status == "ACTIVE"
