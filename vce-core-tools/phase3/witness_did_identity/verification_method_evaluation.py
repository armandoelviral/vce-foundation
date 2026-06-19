from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)


class VerificationMethodEvaluation:

    @staticmethod
    def evaluate(
        document: DidDocumentRecord,
    ) -> bool:

        if not document.classical_key_id:
            return False

        if not document.pqc_key_id:
            return False

        return True
