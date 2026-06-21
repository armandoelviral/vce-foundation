from phase4.trusted_compute_network_governance.governance_verifier import (
    GovernanceVerifier,
)


class MockCitizen:

    def __init__(self, status):

        self.status = status


def test_active_citizen():

    citizen = MockCitizen("ACTIVE")

    assert (
        GovernanceVerifier.verify(
            citizen
        )
        is True
    )


def test_suspended_citizen():

    citizen = MockCitizen("SUSPENDED")

    assert (
        GovernanceVerifier.verify(
            citizen
        )
        is False
    )


def test_revoked_citizen():

    citizen = MockCitizen("REVOKED")

    assert (
        GovernanceVerifier.verify(
            citizen
        )
        is False
    )
