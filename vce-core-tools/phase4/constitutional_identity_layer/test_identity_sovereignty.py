from phase4.constitutional_identity_layer.identity_sovereignty import (
    IdentitySovereignty,
)


def test_contains_identity():

    sovereignty = IdentitySovereignty(
        identity_id="identity-001",
        sovereign=True,
    )

    assert (
        sovereignty.identity_id
        == "identity-001"
    )


def test_contains_sovereignty():

    sovereignty = IdentitySovereignty(
        identity_id="identity-001",
        sovereign=True,
    )

    assert sovereignty.sovereign is True


def test_serializes():

    sovereignty = IdentitySovereignty(
        identity_id="identity-001",
        sovereign=True,
    )

    assert sovereignty.to_dict() == {
        "identity_id": "identity-001",
        "sovereign": True,
    }
