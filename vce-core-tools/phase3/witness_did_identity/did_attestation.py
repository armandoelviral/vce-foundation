from phase2.attestation_persistence.attestation_record import (
    AttestationRecord,
)

from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)


class DidAttestation:

    @staticmethod
    def attest(
        attestation_id: str,
        document: DidDocumentRecord,
    ) -> AttestationRecord:

        return AttestationRecord(
            attestation_id=attestation_id,
            subject="witness_did_identity",
            evidence_hash=document.did,
        )
