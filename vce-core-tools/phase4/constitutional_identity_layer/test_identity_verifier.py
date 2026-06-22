from phase4.constitutional_identity_layer.identity_verifier import (
    IdentityVerifier,
)


class MockIdentity:

    def __init__(
        self,
        sovereign,
        revoked,
        continuous,
    ):
        self.sovereign = sovereign
        self.revoked = revoked
        self.continuous = continuous


def test_valid_identity():

    identity = MockIdentity(
        sovereign=True,
        revoked=False,
        continuous=True,
    )

    assert (
        IdentityVerifier.verify(identity)
        is True
    )


def test_revoked_identity():

    identity = MockIdentity(
        sovereign=True,
        revoked=True,
        continuous=True,
    )

    assert (
        IdentityVerifier.verify(identity)
        is False
    )


def test_non_sovereign_identity():

    identity = MockIdentity(
        sovereign=False,
        revoked=False,
        continuous=True,
    )

    assert (
        IdentityVerifier.verify(identity)
        is False
    )


def test_discontinuous_identity():

    identity = MockIdentity(
        sovereign=True,
        revoked=False,
        continuous=False,
    )

    assert (
        IdentityVerifier.verify(identity)
        is False
    )
