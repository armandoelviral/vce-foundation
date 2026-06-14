from epics.ztc16_key_rotation_lifecycle.activation_anchor import (
    ActivationAnchor,
)


def test_anchor_contains_anchor_id():

    anchor = ActivationAnchor(
        anchor_id="anchor-001",
        rotation_id="rotation-001",
    )

    assert anchor.anchor_id == "anchor-001"


def test_anchor_contains_rotation_id():

    anchor = ActivationAnchor(
        anchor_id="anchor-001",
        rotation_id="rotation-001",
    )

    assert anchor.rotation_id == "rotation-001"


def test_anchor_serializes():

    anchor = ActivationAnchor(
        anchor_id="anchor-001",
        rotation_id="rotation-001",
    )

    assert anchor.to_dict() == {
        "anchor_id": "anchor-001",
        "rotation_id": "rotation-001",
    }
