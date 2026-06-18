from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.attestation_persistence.attestation_store import (
    AttestationStore,
)

from phase2.attestation_persistence.attestation_query import (
    AttestationQuery,
)


def test_query_returns_records_by_subject():

    store = AttestationStore()

    store.add(
        AttestationRecord(
            attestation_id="att-001",
            subject="runtime-state",
            evidence_hash="hash-001",
        )
    )

    query = AttestationQuery(store)

    results = query.by_subject("runtime-state")

    assert len(results) == 1
    assert results[0].attestation_id == "att-001"


def test_query_returns_empty_for_unknown_subject():

    store = AttestationStore()

    query = AttestationQuery(store)

    assert query.by_subject("missing") == []


def test_query_filters_multiple_subjects():

    store = AttestationStore()

    store.add(
        AttestationRecord(
            attestation_id="att-001",
            subject="runtime-state",
            evidence_hash="hash-001",
        )
    )

    store.add(
        AttestationRecord(
            attestation_id="att-002",
            subject="recovery",
            evidence_hash="hash-002",
        )
    )

    query = AttestationQuery(store)

    results = query.by_subject("recovery")

    assert len(results) == 1
    assert results[0].attestation_id == "att-002"
