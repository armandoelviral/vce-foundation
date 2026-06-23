from phase4.constitutional_obligations_layer.duty_appeal import (
    DutyAppeal,
)


def test_contains_appeal_id():

    appeal = DutyAppeal(
        appeal_id="duty-appeal-001",
        violation_id="violation-001",
    )

    assert appeal.appeal_id == "duty-appeal-001"


def test_contains_violation_id():

    appeal = DutyAppeal(
        appeal_id="duty-appeal-001",
        violation_id="violation-001",
    )

    assert appeal.violation_id == "violation-001"


def test_serializes():

    appeal = DutyAppeal(
        appeal_id="duty-appeal-001",
        violation_id="violation-001",
    )

    assert appeal.to_dict() == {
        "appeal_id": "duty-appeal-001",
        "violation_id": "violation-001",
    }
