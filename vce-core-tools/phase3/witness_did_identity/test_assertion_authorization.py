from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)

from phase3.witness_did_identity.assertion_authorization import (
    AssertionAuthorization,
)


def test_document_with_pqc_key_is_authorized():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        AssertionAuthorization.is_authorized(
            document
        )
        is True
    )


def test_document_without_pqc_key_is_not_authorized():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="",
    )

    assert (
        AssertionAuthorization.is_authorized(
            document
        )
        is False
    )


def test_authorization_requires_controller():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        AssertionAuthorization.is_authorized(
            document
        )
        is False
    )
