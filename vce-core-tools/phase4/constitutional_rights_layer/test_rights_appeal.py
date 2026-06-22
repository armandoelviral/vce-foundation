from phase4.constitutional_rights_layer.rights_appeal import (
    RightsAppeal,
)


def test_contains_appeal_id():

    appeal = RightsAppeal(
        appeal_id="rights-appeal-001",
        violation_id="violation-001",
    )

    assert appeal.appeal_id == "rights-appeal-001"


def test_contains_violation_id():

    appeal = RightsAppeal(
        appeal_id="rights-appeal-001",
        violation_id="violation-001",
    )

    assert appeal.violation_id == "violation-001"


def test_serializes():

    appeal = RightsAppeal(
        appeal_id="rights-appeal-001",
        violation_id="violation-001",
    )

    assert appeal.to_dict() == {
        "appeal_id": "rights-appeal-001",
        "violation_id": "violation-001",
    }
