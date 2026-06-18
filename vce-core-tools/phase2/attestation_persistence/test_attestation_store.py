from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase2.attestation_persistence.attestation_store import (
    AttestationStore,
)


def test_store_starts_empty():

    store = AttestationStore()

    assert store.count() == 0


def test_store_accepts_record():

    store = AttestationStore()

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    store.add(record)

    assert store.count() == 1


def test_store_returns_record_by_id():

    store = AttestationStore()

    record = AttestationRecord(
        attestation_id="att-001",
        subject="runtime-state",
        evidence_hash="hash-001",
    )

    store.add(record)

    recovered = store.get("att-001")

    assert recovered == record


def test_unknown_record_returns_none():

    store = AttestationStore()

    assert store.get("missing") is None
