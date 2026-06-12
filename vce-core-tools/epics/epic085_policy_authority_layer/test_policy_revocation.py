from epics.epic085_policy_authority_layer.policy_revocation import (
    PolicyRevocation,
)


def build_revocation(
    active=True,
):

    return PolicyRevocation(
        policy_id="clinical-admission-policy",
        policy_version="1.0.0",
        revoked_by="governance-board",
        revoked_at="2026-06-10T00:30:00Z",
        reason="POLICY_SUPERSEDED",
        active=active,
    )


def test_policy_revocation_creation():

    revocation = build_revocation()

    assert revocation.policy_id == "clinical-admission-policy"
    assert revocation.policy_version == "1.0.0"


def test_policy_revocation_is_active():

    revocation = build_revocation()

    assert revocation.is_revoked() is True


def test_policy_revocation_can_be_inactive():

    revocation = build_revocation(
        active=False
    )

    assert revocation.is_revoked() is False


def test_policy_revocation_contains_reason():

    revocation = build_revocation()

    assert revocation.reason == "POLICY_SUPERSEDED"


def test_policy_revocation_serializes():

    revocation = build_revocation()

    payload = revocation.to_dict()

    assert payload["policy_id"] == "clinical-admission-policy"
    assert payload["revoked_by"] == "governance-board"
    assert payload["reason"] == "POLICY_SUPERSEDED"
    assert payload["active"] is True
