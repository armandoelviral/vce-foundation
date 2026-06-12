from epics.epic085_policy_authority_layer.policy_approval_workflow import (
    PolicyApproval,
)


def build_approval(
    status="APPROVED",
):

    return PolicyApproval(
        policy_id="clinical-admission-policy",
        policy_version="1.0.0",
        approved_by="governance-board",
        approved_at="2026-06-10T00:00:00Z",
        approval_status=status,
    )


def test_policy_approval_creation():

    approval = build_approval()

    assert approval.policy_id == "clinical-admission-policy"
    assert approval.policy_version == "1.0.0"


def test_policy_approval_accepts_approved_status():

    approval = build_approval(
        status="APPROVED"
    )

    assert approval.is_approved() is True


def test_policy_approval_rejects_pending_status():

    approval = build_approval(
        status="PENDING"
    )

    assert approval.is_approved() is False


def test_policy_approval_rejects_rejected_status():

    approval = build_approval(
        status="REJECTED"
    )

    assert approval.is_approved() is False


def test_policy_approval_serializes():

    approval = build_approval()

    payload = approval.to_dict()

    assert payload["policy_id"] == "clinical-admission-policy"
    assert payload["approved_by"] == "governance-board"
    assert payload["approval_status"] == "APPROVED"
