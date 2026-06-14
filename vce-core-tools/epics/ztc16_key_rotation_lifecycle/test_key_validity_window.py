from epics.ztc16_key_rotation_lifecycle.key_validity_window import (
    KeyValidityWindow,
)


def test_window_contains_key_id():

    window = KeyValidityWindow(
        key_id="key-001",
        start_anchor="anchor-100",
        end_anchor="anchor-200",
    )

    assert window.key_id == "key-001"


def test_window_contains_start_and_end_anchors():

    window = KeyValidityWindow(
        key_id="key-001",
        start_anchor="anchor-100",
        end_anchor="anchor-200",
    )

    assert window.start_anchor == "anchor-100"
    assert window.end_anchor == "anchor-200"


def test_window_serializes():

    window = KeyValidityWindow(
        key_id="key-001",
        start_anchor="anchor-100",
        end_anchor="anchor-200",
    )

    assert window.to_dict() == {
        "key_id": "key-001",
        "start_anchor": "anchor-100",
        "end_anchor": "anchor-200",
    }
