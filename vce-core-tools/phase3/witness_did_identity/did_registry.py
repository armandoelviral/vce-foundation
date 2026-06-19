from phase3.witness_did_identity.did_document_record import (
    DidDocumentRecord,
)


class DidRegistry:

    def __init__(self):

        self._documents = {}

    def add(
        self,
        document: DidDocumentRecord,
    ) -> None:

        self._documents[
            document.did
        ] = document

    def get(
        self,
        did: str,
    ):

        return self._documents.get(
            did
        )

    def count(
        self,
    ) -> int:

        return len(
            self._documents
        )

    def did_ids(
        self,
    ):

        return list(
            self._documents.keys()
        )
