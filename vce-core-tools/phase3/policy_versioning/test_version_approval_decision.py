from phase3.policy_versioning.version_approval_decision import (
    VersionApprovalDecision,
)


def test_approve_version():

    decision = (
        VersionApprovalDecision.from_evaluation(
            True
        )
    )

    assert (
        decision.status
        == "APPROVE_VERSION"
    )


def test_reject_version():

    decision = (
        VersionApprovalDecision.from_evaluation(
            False
        )
    )

    assert (
        decision.status
        == "REJECT_VERSION"
    )


def test_decision_serializes():

    decision = (
        VersionApprovalDecision.from_evaluation(
            True
        )
    )

    assert decision.to_dict() == {
        "status": "APPROVE_VERSION"
    }
