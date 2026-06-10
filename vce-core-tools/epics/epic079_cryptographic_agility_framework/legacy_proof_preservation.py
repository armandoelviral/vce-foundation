class LegacyProofPreservation:

    def __init__(
        self,
        supported_epochs,
    ):

        self._supported_epochs = (
            supported_epochs
        )

    def can_verify(
        self,
        proof,
    ):

        for signature in proof.signatures:

            if (
                signature.cryptographic_epoch
                not in self._supported_epochs
            ):
                return False

        return True
