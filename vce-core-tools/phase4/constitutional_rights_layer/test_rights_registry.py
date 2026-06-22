from phase4.constitutional_rights_layer.rights_registry import (
    RightsRegistry,
)

from phase4.constitutional_rights_layer.constitutional_right import (
    ConstitutionalRight,
)


def test_contains_rights():

    registry = RightsRegistry(
        rights=[
            ConstitutionalRight(
                right_id="right-001",
                right_name="due_process",
            ),
        ]
    )

    assert len(registry.rights) == 1


def test_serializes():

    registry = RightsRegistry(
        rights=[
            ConstitutionalRight(
                right_id="right-001",
                right_name="due_process",
            ),
        ]
    )

    assert registry.to_dict() == {
        "rights": [
            {
                "right_id": "right-001",
                "right_name": "due_process",
            }
        ]
    }
