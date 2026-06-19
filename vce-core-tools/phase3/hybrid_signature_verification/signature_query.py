from phase3.hybrid_signature_verification.signature_registry import (
    SignatureRegistry,
)


class SignatureQuery:

    def __init__(
        self,
        registry: SignatureRegistry,
    ):

        self.registry = registry

    def by_id(
        self,
        signature_id: str,
    ):

        return self.registry.get(
            signature_id
        )
