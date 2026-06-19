from phase3.policy_versioning.policy_version_record import (
    PolicyVersionRecord,
)


def test_contains_policy_id():

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    assert record.policy_id == "trust-policy"


def test_contains_version():

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    assert record.version == "v1"


def test_contains_approver():

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    assert record.approved_by == "auth-001"


def test_serializes():

    record = PolicyVersionRecord(
        policy_id="trust-policy",
        version="v1",
        approved_by="auth-001",
    )

    assert record.to_dict() == {
        "policy_id": "trust-policy",
        "version": "v1",
        "approved_by": "auth-001",
    }
