from epics.ztc13_transparency_federation.cross_anchor_record import (
    CrossAnchorRecord,
)

from epics.ztc13_transparency_federation.cross_anchor_verifier import (
    CrossAnchorVerifier,
)


def test_accepts_matching_cross_anchor():

    verifier = CrossAnchorVerifier()

    record = CrossAnchorRecord(
        source_registry="registry-a",
        target_registry="registry-b",
        source_anchor_id="anchor-001",
        target_anchor_id="anchor-001",
    )

    assert verifier.verify(record)


def test_rejects_mismatched_cross_anchor():

    verifier = CrossAnchorVerifier()

    record = CrossAnchorRecord(
        source_registry="registry-a",
        target_registry="registry-b",
        source_anchor_id="anchor-001",
        target_anchor_id="anchor-002",
    )

    assert not verifier.verify(record)
