from phase4.native_sp1_binding.sp1_trust_verifier import (
    SP1TrustVerifier,
)


class MockClaim:

    def __init__(
        self,
        citizen_did,
    ):
        self.citizen_did = citizen_did


def test_valid_citizen():

    claim = MockClaim(
        "did:tcn:test:01",
    )

    assert (
        SP1TrustVerifier.verify(
            claim
        )
        is True
    )


def test_missing_citizen():

    claim = MockClaim(
        "",
    )

    assert (
        SP1TrustVerifier.verify(
            claim
        )
        is False
    )


def test_none_citizen():

    claim = MockClaim(
        None,
    )

    assert (
        SP1TrustVerifier.verify(
            claim
        )
        is False
    )
