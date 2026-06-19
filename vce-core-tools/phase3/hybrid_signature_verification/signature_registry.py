from phase3.hybrid_signature_verification.hybrid_signature_record import (
    HybridSignatureRecord,
)


class SignatureRegistry:

    def __init__(self):

        self._signatures = {}

    def add(
        self,
        signature_id: str,
        signature: HybridSignatureRecord,
    ) -> None:

        self._signatures[
            signature_id
        ] = signature

    def get(
        self,
        signature_id: str,
    ):

        return self._signatures.get(
            signature_id
        )

    def count(
        self,
    ) -> int:

        return len(
            self._signatures
        )

    def signature_ids(
        self,
    ):

        return list(
            self._signatures.keys()
        )
