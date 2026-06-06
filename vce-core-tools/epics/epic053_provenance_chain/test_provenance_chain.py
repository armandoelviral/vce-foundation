from epics.epic049_state_provenance.provenance import (
    ProvenanceRecord,
)

from epics.epic053_provenance_chain.provenance_chain import (
    ProvenanceChain,
)


def test_add_and_retrieve_latest_record():

    chain = ProvenanceChain()

    chain.add(
        ProvenanceRecord(
            snapshot_hash="aaa",
            parent_hash=None,
        )
    )

    chain.add(
        ProvenanceRecord(
            snapshot_hash="bbb",
            parent_hash="aaa",
        )
    )

    latest = chain.latest()

    assert latest.snapshot_hash == "bbb"


def test_retrieves_parent_record():

    chain = ProvenanceChain()

    parent = ProvenanceRecord(
        snapshot_hash="aaa",
        parent_hash=None,
    )

    child = ProvenanceRecord(
        snapshot_hash="bbb",
        parent_hash="aaa",
    )

    chain.add(parent)
    chain.add(child)

    assert (
        chain.parent_of("bbb")
        == parent
    )
