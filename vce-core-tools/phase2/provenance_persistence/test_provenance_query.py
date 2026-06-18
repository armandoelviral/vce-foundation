from phase2.provenance_persistence.provenance_record import (
    ProvenanceRecord,
)

from phase2.provenance_persistence.provenance_store import (
    ProvenanceStore,
)

from phase2.provenance_persistence.provenance_query import (
    ProvenanceQuery,
)


def test_query_returns_record_by_subject():

    store = ProvenanceStore()

    store.add(
        ProvenanceRecord(
            subject_id="artifact-001",
            origin_id="execution-001",
            provenance_hash="hash-001",
        )
    )

    query = ProvenanceQuery(store)

    result = query.by_subject(
        "artifact-001"
    )

    assert result.subject_id == "artifact-001"


def test_query_returns_none_for_missing_subject():

    store = ProvenanceStore()

    query = ProvenanceQuery(store)

    assert query.by_subject(
        "missing"
    ) is None


def test_query_returns_correct_origin():

    store = ProvenanceStore()

    store.add(
        ProvenanceRecord(
            subject_id="artifact-001",
            origin_id="execution-001",
            provenance_hash="hash-001",
        )
    )

    query = ProvenanceQuery(store)

    result = query.by_subject(
        "artifact-001"
    )

    assert (
        result.origin_id
        == "execution-001"
    )
