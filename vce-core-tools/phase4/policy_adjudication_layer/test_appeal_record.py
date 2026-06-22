from phase4.policy_adjudication_layer.appeal_record import (
    AppealRecord,
)


def test_contains_appeal_id():

    appeal = AppealRecord(
        appeal_id="appeal-001",
        decision_id="decision-001",
        status="OPEN",
    )

    assert (
        appeal.appeal_id
        == "appeal-001"
    )


def test_contains_decision_id():

    appeal = AppealRecord(
        appeal_id="appeal-001",
        decision_id="decision-001",
        status="OPEN",
    )

    assert (
        appeal.decision_id
        == "decision-001"
    )


def test_contains_status():

    appeal = AppealRecord(
        appeal_id="appeal-001",
        decision_id="decision-001",
        status="OPEN",
    )

    assert (
        appeal.status
        == "OPEN"
    )


def test_serializes():

    appeal = AppealRecord(
        appeal_id="appeal-001",
        decision_id="decision-001",
        status="OPEN",
    )

    assert appeal.to_dict() == {
        "appeal_id":
            "appeal-001",
        "decision_id":
            "decision-001",
        "status":
            "OPEN",
    }
