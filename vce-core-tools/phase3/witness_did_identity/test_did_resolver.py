from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)

from phase3.witness_did_identity.did_registry import (
    DidRegistry,
)

from phase3.witness_did_identity.did_resolver import (
    DidResolver,
)


def test_resolves_existing_document():

    registry = DidRegistry()

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    registry.add(document)

    resolver = DidResolver(
        registry
    )

    resolved = resolver.resolve(
        "did:vcr:gcp:us-central1:fp001"
    )

    assert resolved == document


def test_returns_none_when_missing():

    registry = DidRegistry()

    resolver = DidResolver(
        registry
    )

    assert resolver.resolve(
        "did:vcr:missing"
    ) is None


def test_resolved_document_contains_pqc_key():

    registry = DidRegistry()

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    registry.add(document)

    resolver = DidResolver(
        registry
    )

    resolved = resolver.resolve(
        "did:vcr:gcp:us-central1:fp001"
    )

    assert (
        resolved.pqc_key_id
        == "key-postquantum-1"
    )
