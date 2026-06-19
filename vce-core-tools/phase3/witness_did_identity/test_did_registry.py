from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)

from phase3.witness_did_identity.did_registry import (
    DidRegistry,
)


def test_registry_starts_empty():

    registry = DidRegistry()

    assert registry.count() == 0


def test_registry_accepts_document():

    registry = DidRegistry()

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    registry.add(document)

    assert registry.count() == 1


def test_registry_returns_document():

    registry = DidRegistry()

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    registry.add(document)

    recovered = registry.get(
        "did:vcr:gcp:us-central1:fp001"
    )

    assert recovered == document


def test_missing_document_returns_none():

    registry = DidRegistry()

    assert registry.get(
        "did:vcr:missing"
    ) is None


def test_registry_lists_dids():

    registry = DidRegistry()

    registry.add(
        DidDocumentRecord(
            did="did:vcr:gcp:us-central1:fp001",
            controller="did:vcr:authority:main",
            classical_key_id="key-classical-1",
            pqc_key_id="key-postquantum-1",
        )
    )

    registry.add(
        DidDocumentRecord(
            did="did:vcr:aws:us-east-1:fp002",
            controller="did:vcr:authority:main",
            classical_key_id="key-classical-1",
            pqc_key_id="key-postquantum-1",
        )
    )

    assert registry.did_ids() == [
        "did:vcr:gcp:us-central1:fp001",
        "did:vcr:aws:us-east-1:fp002",
    ]
