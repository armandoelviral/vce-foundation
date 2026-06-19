class SignatureReport:

    def __init__(
        self,
        signatures,
    ):

        self.signatures = signatures

    def signature_count(
        self,
    ) -> int:

        return len(
            self.signatures
        )

    def signature_ids(
        self,
    ):

        return list(
            self.signatures.keys()
        )

    def to_dict(
        self,
    ):

        return {
            "signature_count":
                self.signature_count(),

            "signature_ids":
                self.signature_ids(),
        }
