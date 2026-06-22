from phase4.constitutional_rights_layer.constitutional_right import (
    ConstitutionalRight,
)


def test_contains_right_id():

    right = ConstitutionalRight(
        right_id="right-001",
        right_name="due_process",
    )

    assert (
        right.right_id
        == "right-001"
    )


def test_contains_right_name():

    right = ConstitutionalRight(
        right_id="right-001",
        right_name="due_process",
    )

    assert (
        right.right_name
        == "due_process"
    )


def test_serializes():

    right = ConstitutionalRight(
        right_id="right-001",
        right_name="due_process",
    )

    assert right.to_dict() == {
        "right_id":
            "right-001",
        "right_name":
            "due_process",
    }
