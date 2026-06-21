from phase4.trusted_compute_network_governance.governance_verifier import (
    GovernanceVerifier,
)


class Citizen:

    def __init__(self):

        self.status = "ACTIVE"


class GovernanceFlow:

    @staticmethod
    def generate():

        citizen = Citizen()

        governance_valid = (
            GovernanceVerifier.verify(
                citizen
            )
        )

        return {
            "citizen_status":
                citizen.status,
            "governance_valid":
                governance_valid,
        }
