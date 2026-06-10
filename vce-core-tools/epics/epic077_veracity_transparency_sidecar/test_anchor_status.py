from epics.epic077_veracity_transparency_sidecar.anchor_status import (
    AnchorStatus,
)


def test_anchor_status_contains_required_states():

    assert AnchorStatus.LOCAL_COMMITTED.value == "LOCAL_COMMITTED"
    assert (
        AnchorStatus.PENDING_TRANSPARENCY.value
        == "PENDING_TRANSPARENCY"
    )
    assert AnchorStatus.ANCHORING.value == "ANCHORING"
    assert (
        AnchorStatus.TRANSPARENCY_ANCHORED.value
        == "TRANSPARENCY_ANCHORED"
    )
    assert AnchorStatus.RETRYING.value == "RETRYING"
    assert AnchorStatus.FAILED.value == "FAILED"


def test_anchor_status_is_string_enum():

    assert isinstance(
        AnchorStatus.LOCAL_COMMITTED.value,
        str,
    )
