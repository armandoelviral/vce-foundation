from phase4.constitutional_identity_layer.identity_recovery import (
    IdentityRecovery,
)


def test_contains_identity():

    recovery = IdentityRecovery(
        identity_id="identity-001",
        recovered=True,
    )

    assert recovery.identity_id == "identity-001"


def test_contains_recovered():

    recovery = IdentityRecovery(
        identity_id="identity-001",
        recovered=True,
    )

    assert recovery.recovered is True


def test_serializes():

    recovery = IdentityRecovery(
        identity_id="identity-001",
        recovered=True,
    )

    assert recovery.to_dict() == {
        "identity_id": "identity-001",
        "recovered": True,
    }
