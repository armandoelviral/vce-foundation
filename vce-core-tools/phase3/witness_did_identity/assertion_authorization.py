from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)


class AssertionAuthorization:

    @staticmethod
    def is_authorized(
        document: DidDocumentRecord,
    ) -> bool:

        if not document.controller:
            return False

        if not document.pqc_key_id:
            return False

        return True
