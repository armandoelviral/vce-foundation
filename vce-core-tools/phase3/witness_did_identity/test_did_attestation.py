from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)

from phase3.witness_did_identity.did_attestation import (
    DidAttestation,
)


def test_attestation_subject():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    attestation = DidAttestation.attest(
        attestation_id="att-001",
        document=document,
    )

    assert (
        attestation.subject
        == "witness_did_identity"
    )


def test_attestation_uses_did():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    attestation = DidAttestation.attest(
        attestation_id="att-001",
        document=document,
    )

    assert (
        attestation.evidence_hash
        == "did:vcr:gcp:us-central1:fp001"
    )


def test_attestation_preserves_id():

    document = DidDocumentRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    attestation = DidAttestation.attest(
        attestation_id="att-001",
        document=document,
    )

    assert (
        attestation.attestation_id
        == "att-001"
    )
