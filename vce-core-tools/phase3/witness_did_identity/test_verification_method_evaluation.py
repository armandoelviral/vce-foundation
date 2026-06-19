from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)

from phase3.witness_did_identity.verification_method_evaluation import (
    VerificationMethodEvaluation,
)


def test_document_with_both_keys_is_valid():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        VerificationMethodEvaluation.evaluate(
            document
        )
        is True
    )


def test_missing_classical_key_fails():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="",
        pqc_key_id="key-postquantum-1",
    )

    assert (
        VerificationMethodEvaluation.evaluate(
            document
        )
        is False
    )


def test_missing_pqc_key_fails():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="",
    )

    assert (
        VerificationMethodEvaluation.evaluate(
            document
        )
        is False
    )
