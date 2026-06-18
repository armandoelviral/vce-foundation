from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)

from phase2.provenance_persistence.provenance_store import (
    ProvenanceStore,
)


def test_store_starts_empty():

    store = ProvenanceStore()

    assert store.count() == 0


def test_store_accepts_record():

    store = ProvenanceStore()

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    store.add(record)

    assert store.count() == 1


def test_store_returns_record():

    store = ProvenanceStore()

    record = ProvenanceRecord(
        subject_id="artifact-001",
        origin_id="execution-001",
        provenance_hash="hash-001",
    )

    store.add(record)

    recovered = store.get(
        "artifact-001"
    )

    assert recovered == record


def test_unknown_record_returns_none():

    store = ProvenanceStore()

    assert store.get(
        "missing"
    ) is None
