from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)


def test_contains_did():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        document.did
        == "did:vcr:gcp:us-central1:fp001"
    )


def test_contains_controller():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        document.controller
        == "did:vcr:authority:main"
    )


def test_contains_classical_key_id():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        document.classical_key_id
        == "key-classical-1"
    )


def test_contains_pqc_key_id():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        document.pqc_key_id
        == "key-postquantum-1"
    )


def test_serializes():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert document.to_dict() == {
        "did": "did:vcr:gcp:us-central1:fp001",
        "controller": "did:vcr:authority:main",
        "classical_key_id": "key-classical-1",
        "pqc_key_id": "key-postquantum-1",
    }
