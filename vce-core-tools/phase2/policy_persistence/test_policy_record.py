from phase2.policy_persistence.policy_record import (
    PolicyRecord,
)


def test_record_contains_policy_id():

    record = PolicyRecord(
        policy_id="policy-001",
        version=1,
        rule="allow_signed_artifacts_only",
    )

    assert record.policy_id == "policy-001"


def test_record_contains_version():

    record = PolicyRecord(
        policy_id="policy-001",
        version=1,
        rule="allow_signed_artifacts_only",
    )

    assert record.version == 1


def test_record_contains_rule():

    record = PolicyRecord(
        policy_id="policy-001",
        version=1,
        rule="allow_signed_artifacts_only",
    )

    assert record.rule == "allow_signed_artifacts_only"


def test_record_serializes():

    record = PolicyRecord(
        policy_id="policy-001",
        version=1,
        rule="allow_signed_artifacts_only",
    )

    assert record.to_dict() == {
        "policy_id": "policy-001",
        "version": 1,
        "rule": "allow_signed_artifacts_only",
    }
