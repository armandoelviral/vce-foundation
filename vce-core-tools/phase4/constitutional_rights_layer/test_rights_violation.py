from phase4.constitutional_rights_layer.rights_violation import (
    RightsViolation,
)


def test_contains_right_id():

    violation = RightsViolation(
        right_id="right-001",
        violation_type="due_process_violation",
    )

    assert violation.right_id == "right-001"


def test_contains_violation_type():

    violation = RightsViolation(
        right_id="right-001",
        violation_type="due_process_violation",
    )

    assert (
        violation.violation_type
        == "due_process_violation"
    )


def test_serializes():

    violation = RightsViolation(
        right_id="right-001",
        violation_type="due_process_violation",
    )

    assert violation.to_dict() == {
        "right_id": "right-001",
        "violation_type": "due_process_violation",
    }
