from phase3.witness_did_identity.vcr_did_record import (
    VcrDidRecord,
)

from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)

from phase3.witness_did_identity.did_registry import (
    DidRegistry,
)

from phase3.witness_did_identity.did_resolver import (
    DidResolver,
)

from phase3.witness_did_identity.verification_method_evaluation import (
    VerificationMethodEvaluation,
)

from phase3.witness_did_identity.assertion_authorization import (
    AssertionAuthorization,
)

from phase3.witness_did_identity.did_attestation import (
    DidAttestation,
)


def test_end_to_end_witness_did_identity():

    did_record = VcrDidRecord(
        did="did:vcr:gcp:us-central1:fp001",
        controller="did:vcr:authority:main",
    )

    document = DidDocumentRecord(
        did=did_record.did,
        controller=did_record.controller,
        classical_key_id="key-classical-1",
        pqc_key_id="key-postquantum-1",
    )

    registry = DidRegistry()

    registry.add(document)

    resolver = DidResolver(
        registry
    )

    resolved = resolver.resolve(
        did_record.did
    )

    assert resolved == document

    evaluation = (
        VerificationMethodEvaluation.evaluate(
            resolved
        )
    )

    assert evaluation is True

    authorized = (
        AssertionAuthorization.is_authorized(
            resolved
        )
    )

    assert authorized is True

    attestation = (
        DidAttestation.attest(
            attestation_id="att-001",
            document=resolved,
        )
    )

    assert (
        attestation.subject
        == "witness_did_identity"
    )

    assert (
        attestation.evidence_hash
        == did_record.did
    )
