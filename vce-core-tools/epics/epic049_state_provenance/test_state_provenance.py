from epics.epic049_state_provenance.provenance import (
    ProvenanceRecord,
)


def test_provenance_links_parent_and_child():

    record = ProvenanceRecord(
        snapshot_hash="bbb",
        parent_hash="aaa",
    )

    assert record.snapshot_hash == "bbb"
    assert record.parent_hash == "aaa"
