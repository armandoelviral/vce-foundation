from phase4.constitutional_rights_layer.rights_protection import (
    RightsProtection,
)


def test_protects_right():

    protection = RightsProtection(
        right_id="right-001",
        protected=True,
    )

    assert protection.protected is True


def test_serializes():

    protection = RightsProtection(
        right_id="right-001",
        protected=True,
    )

    assert protection.to_dict() == {
        "right_id": "right-001",
        "protected": True,
    }
