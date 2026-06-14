from epics.ztc13_transparency_federation.cross_anchor_record import (
    CrossAnchorRecord,
)


def test_cross_anchor_record_contains_source_and_target():

    record = CrossAnchorRecord(
        source_registry="registry-a",
        target_registry="registry-b",
        source_anchor_id="anchor-a",
        target_anchor_id="anchor-b",
    )

    assert record.source_registry == "registry-a"
    assert record.target_registry == "registry-b"
    assert record.source_anchor_id == "anchor-a"
    assert record.target_anchor_id == "anchor-b"


def test_cross_anchor_record_serializes():

    record = CrossAnchorRecord(
        source_registry="registry-a",
        target_registry="registry-b",
        source_anchor_id="anchor-a",
        target_anchor_id="anchor-b",
    )

    assert record.to_dict() == {
        "source_registry": "registry-a",
        "target_registry": "registry-b",
        "source_anchor_id": "anchor-a",
        "target_anchor_id": "anchor-b",
    }
